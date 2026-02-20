# Airflow Best Practices & Patterns: MWAA, DAG Design, Operaciones

Guía detallada de patrones, configuración y best practices para Airflow en AWS MWAA (Managed Workflows for Apache Airflow).

---

## 1. Estructura de DAG: Patrón Recomendado

### Template Básico

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.amazon.aws.operators.s3 import S3CreateBucketOperator
from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator
from airflow.utils.dates import days_ago

# ==================== DAG Definition ====================
default_args = {
    'owner': 'data-engineering',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'email': ['alerts@pragma.co'],
    'email_on_failure': True,
    'email_on_retry': False,
}

dag = DAG(
    dag_id='data_engineering.ingest_apis_to_s3',
    description='Ingest API data, transform, validate, and load to S3',
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval='0 2 * * *',  # 2 AM UTC daily
    catchup=False,  # No retroactive runs
    tags=['data-engineering', 'batch', 'production'],
    max_active_runs=1,  # Evita runs simultáneas
)

# ==================== Functions ====================
def extract_from_api(**context):
    """Extract data from external API and save metadata to XCom."""
    import requests
    run_id = context['run_id']
    
    # Fetch data
    response = requests.get('https://api.example.com/data', timeout=60)
    response.raise_for_status()
    
    # Save to S3
    s3_path = f"s3://my-bucket/raw/api-data/{run_id}/data.json"
    # ... save logic ...
    
    # Push metadata to XCom
    context['task_instance'].xcom_push(key='file_path', value=s3_path)
    context['task_instance'].xcom_push(key='row_count', value=len(response.json()))
    
    return {'status': 'success', 'rows': len(response.json())}

# ==================== Tasks ====================
extract = PythonOperator(
    task_id='extract_api_data',
    python_callable=extract_from_api,
    op_kwargs={},
    provide_context=True,
    execution_timeout=timedelta(minutes=30),
    pool='api_pool',  # Limit to 1 concurrent API call
    pool_slots=1,
)

transform = BashOperator(
    task_id='transform_with_spark',
    bash_command=(
        'aws s3 cp s3://my-bucket/scripts/transform.py /tmp/ && '
        'python /tmp/transform.py --input {{ ti.xcom_pull(task_ids="extract_api_data", key="file_path") }} '
        '--output s3://my-bucket/curated/{{ ds }}/'
    ),
    execution_timeout=timedelta(minutes=120),
    retries=1,  # Fewer retries for Spark jobs
)

validate = PythonOperator(
    task_id='validate_quality',
    python_callable=lambda: print("Great Expectations validation..."),
    execution_timeout=timedelta(minutes=30),
)

# ==================== Dependencies ====================
extract >> transform >> validate
```

**Key Points:**
- ✅ `owner`, `retries`, `retry_delay`, `email` en `default_args`
- ✅ `schedule_interval`, `catchup=False` (sin retroactive runs)
- ✅ `max_active_runs=1` (evita paralelismo no intencionado)
- ✅ `execution_timeout` en cada tarea
- ✅ `pool` y `pool_slots` para limitar concurrencia
- ✅ `tags` para organizar y filtrar
- ✅ XCom solo para metadata (paths, counts)
- ✅ Dependencias claras con `>>`

---

## 2. XCom: Paso de Datos Entre Tareas

### ❌ MAL: XCom para big data

```python
def extract_data(**context):
    df = pd.read_csv('huge_file.csv')  # 1GB
    context['task_instance'].xcom_push(key='dataframe', value=df)  # ❌ MALO

def transform_data(**context):
    df = context['task_instance'].xcom_pull(task_ids='extract', key='dataframe')
    # XCom serializa/deserializa → overhead enorme
```

### ✅ BIEN: XCom para metadata, S3 para datos

```python
def extract_data(**context):
    df = pd.read_csv('huge_file.csv')
    s3_path = 's3://my-bucket/raw/data.parquet'
    df.to_parquet(s3_path)
    
    # Solo guardar la ruta
    context['task_instance'].xcom_push(key='file_path', value=s3_path)
    context['task_instance'].xcom_push(key='row_count', value=len(df))

def transform_data(**context):
    s3_path = context['task_instance'].xcom_pull(task_ids='extract', key='file_path')
    df = pd.read_parquet(s3_path)
    # Transformar...
```

---

## 3. Retries, SLAs y Alertas

### Configuración por Criticidad

| Tipo de Tarea | Retries | Delay | SLA | Action en Fallo |
|---------------|---------|-------|-----|-----------------|
| **Crítico (datos financieros)** | 3-5 | 10-30 min | 2h | Slack + PagerDuty + Email |
| **Importante (análisis)** | 2-3 | 5-10 min | 4-6h | Slack + Email |
| **No crítico (logs)** | 1-2 | 2-5 min | N/A | Log + Airflow UI |

### Ejemplo

```python
from airflow.models import Variable
from airflow.exceptions import AirflowException

def alert_slack(context):
    """Handler for task failures."""
    task = context['task']
    dag_run = context['dag_run']
    message = f"❌ Task '{task.task_id}' failed in DAG '{dag_run.dag_id}'"
    # Enviar a Slack...

default_args = {
    'owner': 'data-engineering',
    'retries': 3,
    'retry_delay': timedelta(minutes=10),
    'sla': timedelta(hours=2),  // Task debe completar en 2h
    'on_failure_callback': alert_slack,
}
```

### SLA en MWAA

- SLA se monitorea a nivel DAG run.
- Si excede tiempo, Airflow marca como `sla_miss`.
- Integra con CloudWatch Alarms para notificaciones.

---

## 4. Secrets, Credentials y Seguridad

### ❌ MAL: Hardcoding

```python
def extract_data(**context):
    api_key = 'sk-1234567890'  # ❌ NUNCA HAGAS ESTO
    response = requests.get('https://api.example.com', headers={'key': api_key})
```

### ✅ BIEN: AWS Secrets Manager

```python
from airflow.providers.amazon.aws.hooks.secrets_manager import SecretsManagerHook

def extract_data(**context):
    # Opción 1: Via Variable
    api_key = Variable.get('API_KEY', deserialize_json=False)
    
    # Opción 2: Via Connection
    conn = BaseHook.get_connection('external_api')
    api_key = conn.password
    
    # Opción 3: Via Secrets Manager (en AWS)
    hook = SecretsManagerHook(aws_conn_id='aws_default')
    secret = hook.get_secret_string('external-api-key')
    
    response = requests.get('https://api.example.com', headers={'key': api_key})
```

### En MWAA: Configurar Connections

1. Airflow UI → Admin → Connections → Create
2. Llena conn_id, conn_type, host, login, password
3. Usa en DAG: `conn = BaseHook.get_connection('conn_id')`

---

## 5. Logging y Observabilidad

### Logs Estructurados

```python
import logging

logger = logging.getLogger(__name__)

def extract_data(run_id, **context):
    logger.info(
        "Starting extract",
        extra={
            'run_id': run_id,
            'task_id': context['task'].task_id,
            'try_number': context['task_instance'].try_number,
            'dataset': 'api_data',
        }
    )
    
    rows = 1000
    logger.info(
        f"Extracted {rows} rows",
        extra={'run_id': run_id, 'row_count': rows}
    )
```

### Exportar Logs a CloudWatch

En MWAA, habilita "Logs Configuration" para exportar a CloudWatch:
- `DAG Logs` → `/aws/airflow/dag-logs/`
- `Task Logs` → `/aws/airflow/task-logs/`
- `Scheduler Logs` → `/aws/airflow/scheduler-logs/`

---

## 6. Testing de DAGs

### Validación Básica

```bash
# Validar sintaxis
airflow dags validate

# Test unitario de tarea
airflow tasks test <dag_id> <task_id> <execution_date>

# Ejemplo
airflow tasks test data_engineering.ingest_apis_to_s3 extract_api_data 2026-02-01
```

### Test con pytest

```python
# tests/test_dag.py
import pytest
from airflow.models import DAG
from airflow.utils.dates import days_ago

def test_dag_loads():
    """Test that DAG loads without errors."""
    from dags.data_engineering.ingest_apis import dag
    assert dag is not None
    assert dag.dag_id == 'data_engineering.ingest_apis_to_s3'

def test_dag_has_required_tasks():
    """Test that DAG has expected tasks."""
    from dags.data_engineering.ingest_apis import dag
    task_ids = [t.task_id for t in dag.tasks]
    assert 'extract_api_data' in task_ids
    assert 'transform_with_spark' in task_ids
    assert 'validate_quality' in task_ids

def test_dag_dependencies():
    """Test task dependencies."""
    from dags.data_engineering.ingest_apis import dag
    # extract >> transform >> validate
    extract = dag.get_task('extract_api_data')
    assert len(extract.downstream_list) == 1
    assert extract.downstream_list[0].task_id == 'transform_with_spark'
```

---

## 7. Patrón: Dynamic DAGs

Útil cuando número de tareas varía (ej: procesar múltiples buckets, datasources).

```python
DATASETS = ['dataset_a', 'dataset_b', 'dataset_c']

for dataset in DATASETS:
    task = PythonOperator(
        task_id=f'process_{dataset}',
        python_callable=process_dataset,
        op_kwargs={'dataset': dataset},
        dag=dag,
    )
```

**Cuidado:**
- ✅ Mantén `task_id` determinístico (evita random UUIDs)
- ❌ No uses `len(list_that_changes)` directamente (puede romper backfills)

---

## 8. MWAA-Specific Configuration

### IAM Roles y Permisos

MWAA requiere roles para:
- Leer DAGs de S3
- Escribir logs a CloudWatch
- Acceder a otros servicios (Glue, S3, Redshift, etc.)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::my-bucket/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    },
    {
      "Effect": "Allow",
      "Action": "redshift:DescribeClusters",
      "Resource": "*"
    }
  ]
}
```

### Variables de Entorno en MWAA

En Airflow UI → Admin → Variables:
```
ENVIRONMENT=production
WORKSPACE=pragma-data-dev
SLACK_WEBHOOK=https://hooks.slack.com/...
```

Acceso en DAG:
```python
env = Variable.get('ENVIRONMENT', 'development')
slack_url = Variable.get('SLACK_WEBHOOK')
```

---

## 9. Troubleshooting Común

| Problema | Causa | Solución |
|----------|-------|----------|
| **Task hangs indefinitely** | Timeout no configurado | Añade `execution_timeout` |
| **XCom push fails (large data)** | Datos > 48KB | Mueve a S3, usa ruta en XCom |
| **Credentials not found** | Variable/Connection missing | Verifica en Airflow UI |
| **DAG not appears in UI** | Sintaxis error | Ejecuta `airflow dags validate` |
| **SLA breach misses** | SLA configurado mal | Usa `timedelta(hours=X)` |

---

---

## 10. Librerías y Operadores Custom

### Usar Operadores Custom de Pragma

**Librería:** `ciencia-datos-datos-lib-py-operators`  
**Repo:** https://github.com/carlosguzmanbaq/ciencia-datos-datos-lib-py-operators

Operadores pre-construidos para casos comunes en pipelines:

```python
from airflow_operators.s3 import S3MultipartCopyOperator  # Para archivos >5GB
from airflow_operators.fileferry import FileFerryOperator, FileFerryCompletionSensor

# En tu DAG:
copy_large = S3MultipartCopyOperator(
    task_id='copy_large_files',
    source_s3_key='s3://src/data/2gb-file.parquet',
    destination_s3_key='s3://dst/data/2gb-file.parquet',
)

send_to_sftp = FileFerryOperator(
    task_id='sync_to_sftp',
    operation='upload',
    source_s3_path='s3://bucket/curated/',
    target_sftp_path='/vendor/data/',
    retry_limit=3,
)

copy_large >> send_to_sftp
```

**Backend Lambda:** `ciencia-datos-datos-lib-py-fileferry`  
**Repo:** https://github.com/jersonferrerm/ciencia-datos-datos-lib-py-fileferry

---

### REFERENCIAS RELACIONADAS

- **Prompt:** `prompts/data-engineering/airflow-dag-design.md` (Revisión y validación de DAGs)
- **Instrucciones:** `instructions_or_rules/data-engineering/modular/05-airflow.md` (Despliegue en MWAA, operaciones)
- **Instrucciones:** `instructions_or_rules/data-engineering/modular/02-guidelines.md` (Error handling, logging)
- **Resource:** `resources/data-engineering/data-architecture-patterns.md` (Patrones Lambda/Kappa)
- **🔗 Externos:** `ciencia-datos-datos-lib-py-operators`, `ciencia-datos-datos-lib-py-fileferry`
