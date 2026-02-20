## PROMPT: Diseño de DAG en Airflow para Pipelines de Datos

**⚠️ NOTA IMPORTANTE:** Este prompt es **específico de Airflow/MWAA (AWS)**. Si usas **Azure Data Factory, Synapse Pipelines, o deseas validación agnóstica de orquestación**, usa [pipeline-orchestration-design.md](./pipeline-orchestration-design.md) en su lugar.

**ROL:** Arquitecto de Airflow experto. Revisa diseño de DAGs, estructura de tareas, dependencias y configuración operacional.

**CONTEXTO:** Se te entrega un DAG Airflow (Python), un diagrama de flujo, o una descripción de requisitos. Valida:
- Estructura idempotenta de tareas
- Manejo de XCom y paso de datos
- Configuración de retries, alertas y SLAs
- Observabilidad (logs, métricas)
- Seguridad (credentials, IAM, secrets)

---

## REGLAS DE DISEÑO DE DAG

**Estructura y Composición:**
- ✅ DAG está claramente definido con `dag_id`, `owner`, `start_date`, `schedule_interval`, `catchup`.
- ✅ Tareas son reutilizables o composables (no megatareas).
- ✅ Dependencias explícitas (no hay caminos ocultos de datos).
- ✅ DAG es stateless entre ejecuciones (idempotencia).
- ❌ Evita DAGs dinámicos sin control de nombre.

**Operadores y Tareas:**
- ✅ Operador elegido es el correcto según caso (HttpSensor/SimpleHttpOperator para APIs, SparkSubmitOperator para Spark, S3Operator para uploads).
- ✅ Tareas definen claros `upstream` y `downstream`.
- ✅ Timeouts y `execution_timeout` están configurados.
- ✅ `task_id` es descriptivo y único.
- ❌ Evita BashOperator con comandos complejos; usa Python si es posible.

**Paso de Datos (XCom):**
- ✅ XCom se usa para pequeños datos (paths, IDs, counts) no binarios.
- ✅ Nombres de XCom son descriptivos (`xcom_pull(task_ids='extract', key='file_path')`).
- ✅ S3 o volumes for big data (DataFrames, archivos); XCom solo para metadata.
- ❌ No uses XCom para pasar DataFrames; es ineficiente.

**Retries y Alertas:**
- ✅ `retries` y `retry_delay` definidos según SLA del job (critically important tasks requieren más reintentos que non-critical).
- ✅ `pool` y `pool_slots` para limitar paralelismo (evita sobrecargar recursos).
- ✅ `sla` definido según ventana de tiempo esperada del job; alertas configuradas.
- ✅ `on_failure_callback` y `on_retry_callback` para notificaciones.
- ❌ No dejes retries infinitos o sin delays.

**Configuración y Secretos:**
- ✅ Credentials vienen de `Variable` o `Connection` (no hardcoded).
- ✅ IAM roles / permisos mínimos (least privilege).
- ✅ Secretos en AWS Secrets Manager / Azure KeyVault; Airflow los extrae.
- ✅ Environment variables o conn strings via `conn_id` y Airflow connections.
- ❌ Nunca hardcodees credenciales en DAGs.

**Testing y Validación:**
- ✅ DAG pasa proceso de validación (syntax check, dependency verification).
- ✅ Cada tarea tiene condiciones de éxito explícitas (no falla silenciosamente).
- ✅ Logs son estructurados (incluyen run ID, task ID, attempt metadata).
- ✅ DAG tiene tests unitarios para transformaciones lógicas (si aplica).
- ❌ DAG no debe fallar con errores cryptic o sin mensajes de diagnóstico.

**Observabilidad:**
- ✅ Cada tarea loguea entrada/salida con contexto.
- ✅ Métricas expuestas (duration, rows procesadas, errores).
- ✅ Integración con CloudWatch (AWS) o Application Insights (Azure).
- ✅ Alertas en Slack, PagerDuty u otro si incidentes.
- ❌ No dejes DAGs con logs vacíos.

---

## SECUENCIA DE REVISIÓN

1. **Estructura general:**
   - ¿DAG está bien inicializado? ¿Tiene owner, schedule_interval, catchup?
   - ¿Hay dependencias circulares?

2. **Tareas individuales:**
   - ¿Operador es correcto?
   - ¿Parámetros (timeout, retry, pool) están ajustados?
   - ¿Artefactos/outputs se guardan correctamente?

3. **Flujo de datos:**
   - ¿XCom se usa solo para metadata?
   - ¿Big data va a S3/ADLS, no a XCom?
   - ¿Dependencias son explícitas?

4. **Error handling:**
   - ¿Retries están configurados?
   - ¿SLAs definidos?
   - ¿Callbacks para fallos/alertas?

5. **Seguridad y configuración:**
   - ¿Credenciales vienen de Variables/Connections?
   - ¿No hay hardcoding de secrets?
   - ¿IAM/roles son least privilege?

6. **Observabilidad:**
   - ¿Logs tienen contexto?
   - ¿Métricas expuestas?
   - ¿Alertas configuradas?

---

## OUTPUT

- Lista de issues prioritizados (crítico / mayor / menor).
- Ejemplos concretos de código para arreglo.
- Referencias a secciones en instrucciones si aplica.
- Recomendación: "Aprobado para productivo", "Cambios menores" o "Requiere rediseño".

---

---

## Operadores y Librerías Custom Recomendadas

Al revisar DAGs, considera usar operadores pre-construidos de Pragma:

### 📦 Instalación & Setup

```bash
# Instalar las librerías desde PyPI
pip install ciencia-datos-datos-lib-py>=1.0.0
pip install ciencia-datos-datos-lib-py-operators>=2.1.0

# O en requirements.txt para ambiente Airflow/MWAA:
ciencia-datos-datos-lib-py>=1.0.0
ciencia-datos-datos-lib-py-operators>=2.1.0
```

### ✅ S3MultipartCopyOperator (Para copias de >5GB)

**Cuándo usar:** Copias grandes de S3→S3 que requieren timeout/retry robusto.

```python
from ciencia_datos.operators import S3MultipartCopyOperator

# ❌ EVITAR (BashOperator con aws s3 cp):
# - Falla sin retry en timeout
# - No gestiona multipart (lento en >5GB)
copy_bad = BashOperator(
    task_id='copy',
    bash_command='aws s3 cp s3://src/large.parquet s3://dst/large.parquet --region us-east-1',
)

# ✅ USAR (S3MultipartCopyOperator):
# - Auto-detects tamaño y usa multipart
# - Retry + exponential backoff nativo
# - Logs detallados por chunk
copy_good = S3MultipartCopyOperator(
    task_id='copy_large_parquet',
    source_s3_key='s3://src-bucket/large.parquet',
    destination_s3_key='s3://dst-bucket/processed/large.parquet',
    multipart_threshold=5 * 1024**3,          # Trigger multipart para >5GB
    chunk_size=100 * 1024**1024,              # 100MB per chunk
    max_retries=3,
    retry_delay=300,                          # 5 min between retries
    conn_id='aws_default',                    # Connection name in Airflow
)
```

**Parámetros clave:**
- `multipart_threshold`: Tamaño mínimo para usar multipart (default: 5GB)
- `chunk_size`: Tamaño de cada chunk en multipart (default: 100MB)
- `max_retries`: Reintentos si falla (default: 3)
- `retry_delay`: Segundos entre reintentos (exponential backoff)

---

### ✅ FileFerryOperator (Para transferencias S3↔SFTP)

**Cuándo usar:** Enviar/recibir datos desde proveedores externos via SFTP sin SSL headaches.

```python
from ciencia_datos.operators import FileFerryOperator

# Ejemplo: Upload batch diária a vendor SFTP
transfer_to_vendor = FileFerryOperator(
    task_id='daily_upload_to_vendor',
    operation='upload',                       # 'upload' o 'download'
    source_s3_path='s3://bucket/daily-batch/',
    target_sftp_path='/vendor/incoming/',
    sftp_conn_id='vendor_sftp',               # SFTP connection in Airflow
    pattern='*.parquet',                      # Match files
    archive_after=True,                       # Move source to /archive after success
    parallel_workers=4,                       # Concurrent uploads
)

# Ejemplo: Download forecasts from external system
transfer_from_vendor = FileFerryOperator(
    task_id='fetch_forecasts_from_api',
    operation='download',
    source_sftp_path='/api-exports/forecasts/',
    target_s3_path='s3://bucket/forecasts/{{ ds }}/',  # Partition by date
    sftp_conn_id='external_api',
    pattern='forecast_*.csv',
    retry_failed=True,                        # Retry failed files
)
```

**Parámetros clave:**
- `operation`: 'upload' (S3→SFTP) o 'download' (SFTP→S3)
- `parallel_workers`: Concurrencia para múltiples archivos
- `archive_after`: Mover source a carpeta /archive post-transferencia
- `pattern`: Glob pattern para seleccionar archivos

---

### REFERENCIAS RELACIONADAS

- **Instrucciones:** `instructions_or_rules/data-engineering/modular/02-guidelines.md` (Sección 2.2 Pipeline Design, 2.6 Error Handling)
- **Resource:** `resources/data-engineering/airflow-best-practices.md` (Patrones, configuración, patterns reusables)
- **Instrucciones:** `instructions_or_rules/data-engineering/modular/03-technology.md` (Stack recomendado)
- **Instrucciones:** `instructions_or_rules/data-engineering/modular/05-airflow.md` (MWAA, despliegue, operaciones)
- **🔗 Externos:** `ciencia-datos-datos-lib-py-operators`, `ciencia-datos-datos-lib-py-fileferry`
