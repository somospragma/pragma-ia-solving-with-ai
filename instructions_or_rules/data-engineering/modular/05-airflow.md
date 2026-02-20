# Airflow & MWAA: Implementation, Deployment y Operaciones

Guía completa para implementar, desplegar y operar Airflow en AWS Managed Workflows (MWAA).

---

## 1. MWAA vs Self-Hosted Airflow

### Comparativa

| Aspecto | MWAA (AWS Managed) | Self-Hosted | Usar MWAA si... |
|--------|-------------------|-------------|-----------------|
| **Setup** | Completo en AWS | Manual (EC2/ECS) | No quieres ops de infraestructura |
| **Scaling** | Automático | Manual | Necesitas auto-scaling |
| **Updates** | AWS los maneja | Manual | Quieres último Airflow pero sin mantenimiento |
| **Costo** | ~$0.48/hour + storage | Flexible | Cargas pequeñas-medianas (<10 DAGs) |
| **Integración AWS** | Nativa | Via providers | Usas muchos servicios AWS |
| **Control** | Limitado (kubelet, security groups) | Completo | Necesitas personalización extrema |

**Recomendación:** Usa MWAA para la mayoría de equipos Pragma.

---

## 2. Setup Inicial de MWAA en AWS

### Paso 1: Crear Bucket S3 para DAGs y logs

```bash
aws s3api create-bucket \
    --bucket pragma-airflow-env \
    --region us-east-1

# Estructura esperada
s3://pragma-airflow-env/
├── dags/           # Aquí van los DAGs Python
├── plugins/        # Custom operators, hooks
├── requirements.txt # Dependencias Python
└── logs/           # Logs (MWAA escribe aquí)
```

### Paso 2: Crear IAM Role para MWAA

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "airflow:PublishMetrics",
      "Resource": "arn:aws:airflow:*:*:*"
    },
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "airflow.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::pragma-airflow-env/*",
        "arn:aws:s3:::pragma-airflow-env"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogStream",
        "logs:CreateLogGroup",
        "logs:PutLogEvents",
        "logs:GetLogEvents"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::pragma-airflow-env/logs/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "redshift:DescribeClusters",
        "redshift-data:ExecuteStatement",
        "redshift-data:DescribeStatement",
        "redshift-data:GetStatementResult"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "glue:*"
      ],
      "Resource": "*"
    }
  ]
}
```

### Paso 3: Crear Environment en MWAA

Via AWS Console o CLI:

```bash
aws mwaa create-environment \
    --name pragma-airflow-prod \
    --airflow-version 2.4.3 \
    --environment-class mw1.small \
    --max-workers 10 \
    --dag-s3-path s3://pragma-airflow-env/dags/ \
    --plugins-s3-path s3://pragma-airflow-env/plugins/ \
    --requirements-s3-path s3://pragma-airflow-env/requirements.txt \
    --execution-role-arn arn:aws:iam::ACCOUNT:role/MWAAExecutionRole \
    --region us-east-1 \
    --tags Environment=production Team=data-engineering
```

**Parámetros:**
- **airflow-version:** 2.4.3 o superior (soporte a Airflow 2.x)
- **environment-class:** mw1.small (dev), mw1.medium (staging), mw1.large (prod)
- **max-workers:** 10-25 para prod

---

## 3. Estructura de Proyecto Recomendada

```
pragma-airflow/
├── dags/
│   ├── data_engineering/
│   │   ├── ingest_apis_to_s3.py
│   │   ├── transform_batch.py
│   │   └── validate_quality.py
│   ├── analytics/
│   │   ├── analytics_dashboard.py
│   │   └── ml_predictions.py
│   └── __init__.py
├── plugins/
│   ├── operators/
│   │   ├── custom_s3_operator.py
│   │   └── redshift_operator.py
│   ├── hooks/
│   │   └── pragmadb_hook.py
│   └── __init__.py
├── tests/
│   ├── unit/
│   │   ├── test_extract_dag.py
│   │   └── test_transformations.py
│   └── integration/
│       └── test_e2e_pipeline.py
├── scripts/
│   ├── deploy.sh       # Deploy DAGs a S3/MWAA
│   ├── sync_requirements.sh
│   └── test_local.sh   # Test con docker-compose
├── requirements.txt    # Python deps
├── docker-compose.yml  # Local Airflow development
├── .gitignore
└── README.md

📌 **En S3:**
s3://pragma-airflow-env/
├── dags/               ← sync desde dags/
├── plugins/            ← sync desde plugins/
└── requirements.txt    ← sync desde ./requirements.txt
```

---

## 4. Deployment (CI/CD con GitHub Actions)

### Script: `scripts/deploy.sh`

```bash
#!/bin/bash

BUCKET="pragma-airflow-env"
REGION="us-east-1"

echo "📦 Syncing DAGs to S3..."
aws s3 sync ./dags s3://${BUCKET}/dags/ --delete --region ${REGION}

echo "📦 Syncing plugins to S3..."
aws s3 sync ./plugins s3://${BUCKET}/plugins/ --delete --region ${REGION}

echo "📦 Syncing requirements.txt to S3..."
aws s3 cp requirements.txt s3://${BUCKET}/requirements.txt --region ${REGION}

echo "✅ Deployment complete. DAG parsing will trigger in ~1 min."
```

### GitHub Actions Workflow: `.github/workflows/deploy-airflow.yml`

```yaml
name: Deploy Airflow DAGs

on:
  push:
    branches: [ main, develop ]
    paths:
      - dags/**
      - plugins/**
      - requirements.txt

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install apache-airflow[amazon] pandas pyarrow
      
      - name: Validate DAGs
        run: |
          airflow dags validate
      
      - name: Run unit tests
        run: |
          pytest tests/unit/ -v

  deploy:
    runs-on: ubuntu-latest
    needs: validate
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          role-to-assume: arn:aws:iam::ACCOUNT:role/GitHubActionsRole
          aws-region: us-east-1
      
      - name: Deploy to MWAA
        run: bash scripts/deploy.sh
```

---

## 5. Variables, Connections y Secrets

### Crear Variables en MWAA

**Via Airflow UI:**
1. Admin → Variables
2. Click "Create"
3. Key: `ENVIRONMENT`, Value: `production`
4. Save

**Via CLI:**
```bash
airflow variables set ENVIRONMENT production
airflow variables set SLACK_WEBHOOK https://hooks.slack.com/...
```

**Via AWS CLI (sin UI):**
```bash
aws mwaa create-cli-token --name pragma-airflow-prod --region us-east-1
# Extrae token...
airflow variables set ENVIRONMENT production  # Dentro del container
```

### Crear Connections

**Via Airflow UI:**
1. Admin → Connections
2. Click "Create"
3. Conn ID: `redshift_default`
4. Conn Type: `postgres` (Redshift es compatible)
5. Host: `redshift-cluster.xyz.us-east-1.redshift.amazonaws.com`
6. Port: `5439`
7. Login: `awsuser`
8. Password: `xxxxx`
9. Database: `dev`
10. Save

**Uso en DAG:**
```python
from airflow.providers.postgres.operators.postgres import PostgresOperator

redshift_query = PostgresOperator(
    task_id='redshift_query',
    postgres_conn_id='redshift_default',
    sql='SELECT * FROM sales LIMIT 10;',
    dag=dag,
)
```

---

## 6. Monitoreo y Alertas

### CloudWatch Alarms

```bash
aws cloudwatch put-metric-alarm \
    --alarm-name airflow-dag-failure \
    --alarm-description "Alert when DAG fails" \
    --metric-name DAGRunFailure \
    --namespace AWS/MWAA \
    --statistic Sum \
    --period 300 \
    --threshold 1 \
    --comparison-operator GreaterThanOrEqualToThreshold \
    --alarm-actions arn:aws:sns:us-east-1:ACCOUNT:airflow-alerts
```

### Slack Notifications

```python
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator
from airflow.utils.dates import days_ago

def on_dag_fail(context):
    """Send failure alert to Slack."""
    dag_run = context['dag_run']
    slack_msg = f"""
    ❌ DAG Failed: {dag_run.dag_id}
    Try: {context['task_instance'].try_number}
    Time: {dag_run.execution_date}
    """
    return slack_msg

dag = DAG(
    dag_id='data_engineering.analytics',
    on_failure_callback=on_dag_fail,
    start_date=days_ago(1),
)
```

---

## 7. Troubleshooting MWAA

| Problema | Síntoma | Solución |
|----------|---------|----------|
| **DAG no aparece** | Airflow UI vacío | Validar DAG; revisar S3 permisos |
| **Task fails con "access denied"** | Error en task logs | Revisar IAM role; añadir permisos S3/Glue |
| **Memory issues** | Job mata con OOM | Aumentar environment-class o max-workers |
| **Airflow UI lento** | UI tarda >10 seg | Reducir número de DAGs; añadir DB read replicas |
| **Secrets no se encuentran** | KeyError en Variable.get() | Verificar nombre exacto en Airflow UI |

---

## 8. Best Practices Operacionales

### Backup y Disaster Recovery

```bash
# Backup metadata DB
aws rds create-db-snapshot \
    --db-instance-identifier airflow \
    --db-snapshot-identifier airflow-backup-$(date +%Y%m%d)

# Exportar DAGs
aws s3 sync s3://pragma-airflow-env/dags/ ./dags-backup/
```

### Rotación de Logs

```python
# En MWAA, logs se envían a CloudWatch y S3
# Configurar retention en CloudWatch
aws logs put-retention-policy \
    --log-group-name /aws/airflow/dag-logs \
    --retention-in-days 30
```

### Upgrades de Airflow

1. Airflow anuncia nuevas versiones; AWS las añade a MWAA después de 1-2 meses
2. Testa en staging primero
3. Programa upgrade en horario bajo
4. MWAA tarda ~5-10 min en actualizar

---

---

## 9. Librerías y Operadores Custom Reutilizables

### 📦 Repositorio: ciencia-datos-datos-lib-py-operators

**Propósito:** Librería de operadores Airflow custom tuned para pipelines Pragma.

**Operadores disponibles:**
- `S3MultipartCopyOperator`: Copia archivos S3 grandes (soporta multipart ≤5GB o >5GB)
- `FileFerryOperator`: Transferencias S3↔SFTP vía AWS Lambda
- `FileFerryTransferSensor`: Monitor de estado de transferencias
- `FileFerryCompletionSensor`: Espera estado COMPLETED/PARTIALLY_COMPLETED/FAILED
- `FileFerryFailureSensor`: Detección de transferencias fallidas

**Repo:** https://github.com/carlosguzmanbaq/ciencia-datos-datos-lib-py-operators

**Casos de uso:**
- Pipelines que requieren copias S3 de archivos >5GB
- Integraciones S3↔SFTP sin escribir código custom
- Monitoreo de transferencias en tiempo real

**Instalación:**
```bash
pip install git+https://github.com/carlosguzmanbaq/ciencia-datos-datos-lib-py-operators.git
```

**Ejemplo DAG:**
```python
from airflow_operators.s3 import S3MultipartCopyOperator
from airflow_operators.fileferry import FileFerryOperator, FileFerryCompletionSensor

# Copiar archivo grande
copy_task = S3MultipartCopyOperator(
    task_id='copy_large_file',
    source_s3_key='s3://bucket-source/large-file.parquet',
    destination_s3_key='s3://bucket-dest/large-file.parquet',
    multipart_threshold=5 * 1024**3,  # 5GB
)

# Transferir a SFTP
transfer = FileFerryOperator(
    task_id='transfer_to_sftp',
    operation='upload',
    source_s3_path='s3://bucket/data/',
    target_sftp_path='/remote/data/',
)

# Esperar confirmación
wait_completion = FileFerryCompletionSensor(
    task_id='wait_transfer_done',
    transfer_id='{{ ti.xcom_pull(task_ids="transfer_to_sftp", key="transfer_id") }}',
    poke_interval=30,
)

copy_task >> transfer >> wait_completion
```

### 📦 Repositorio: ciencia-datos-datos-lib-py-fileferry (Dependencia)

**Propósito:** Servicio AWS Lambda que abstrae transferencias S3↔SFTP usando AWS Transfer Family.

**Funcionalidades:**
- Upload (S3→SFTP), Download (SFTP→S3), Delete, List, Get Status
- Batch orchestration, throttle control, session management
- Comprehensive error codes y retry handling

**Repo:** https://github.com/jersonferrerm/ciencia-datos-datos-lib-py-fileferry

**Caso de uso:** Backend de `FileFerryOperator`. Puedes invocar directamente si necesitas APIs REST.

**API REST Example:**
```bash
# Upload a S3→SFTP
curl -X POST https://lambda-endpoint/transfer \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "upload",
    "source_s3_path": "s3://bucket/data.csv",
    "target_sftp_path": "/sftp/data.csv",
    "sftp_connection_id": "prod-sftp-conn"
  }'
```

---

### REFERENCIAS RELACIONADAS

- **Prompt:** `prompts/data-engineering/airflow-dag-design.md` (Validación de DAGs)
- **Resource:** `resources/data-engineering/airflow-best-practices.md` (Patrones, logging, testing)
- **Instrucciones:** `instructions_or_rules/data-engineering/modular/02-guidelines.md` (Error handling, logging)
- **Resource:** `resources/data-engineering/aws-azure-data-services.md` (AWS services mapping)
- **🔗 Externos:** `ciencia-datos-datos-lib-py-operators` (Operadores custom), `ciencia-datos-datos-lib-py-fileferry` (Backend Lambda)
