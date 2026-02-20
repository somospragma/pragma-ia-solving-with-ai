# Glue Jobs Dinámicos: Patrones y mejores prácticas

Patrones reutilizables para implementar jobs Glue con configuración declarativa (YAML-based), basado en arquitectura probada de Pragma.

---

## 1. Arquitectura de Glue Job Config-Driven

La clave es **separar configuración de lógica**:

```
Glue Job (Python/PySpark)
├── config/
│   ├── reports/              # YAML por tabla (qué transformar)
│   │   ├── payments.yml
│   │   ├── orders.yml
│   │   └── customers.yml
│   └── report_config.py      # Parser centralizado
├── etl/
│   ├── extract.py            # Lee desde S3, según config
│   ├── transform.py          # Aplica transformaciones del YAML
│   ├── load.py               # Escribe a S3 (raw, analytics, curated)
│   └── metadata.py           # Agrega auditoría
├── addons/
│   └── schemas/              # .schema.yml con tipo de campos
├── tests/
│   ├── test_extract.py       # Unit tests
│   └── test_transform.py
└── main.py                   # Orquestador principal
```

---

## 2. Configuración YAML: Ejemplo DynamoDB

```yaml
# config/reports/payments.yml
---
table_name: payments
source:
  type: dynamodb_export
  s3_path: s3://pragma-raw/dynamodb-exports/payments/
  format: json
  
transformations:
  - flatten_dynamodb_struct: true        # Convierte Item format a columnas
  - type_casting:
      - field: payment_id
        type: string
      - field: amount
        type: decimal(10,2)
      - field: transaction_date
        type: timestamp
        pattern: "yyyy-MM-dd HH:mm:ss"
  - null_handling: drop                  # drop filas con nulls en keys
  
destination:
  analytics: s3://pragma-analytics/payments/
  curated: s3://pragma-curated/payments/
  format_analytics: parquet
  format_curated: hudi                   # Para CDC/upsert
  partitions:
    - year
    - month
    - day
  
metadata:
  add_ingestion_timestamp: true
  add_source_system: "dynamodb"
  add_processing_date: true
  
mode: FULL                               # FULL (replace) vs INC (merge)
schedule: '0 2 * * *'                   # 2 AM UTC daily
```

---

## 3. Parser de Configuración

```python
# config/report_config.py
import yaml
from typing import Dict, Any

class ReportConfig:
    def __init__(self, config_path: str):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
    
    def table_name(self) -> str:
        return self.config['table_name']
    
    def source_s3_path(self) -> str:
        return self.config['source']['s3_path']
    
    def transformations(self) -> Dict[str, Any]:
        return self.config.get('transformations', [])
    
    def destination_curated(self) -> str:
        return self.config['destination']['curated']
    
    def mode(self) -> str:
        """FULL (rewrite) or INC (merge/CDC)"""
        return self.config.get('mode', 'FULL')

# Uso:
config = ReportConfig('config/reports/payments.yml')
print(config.table_name())  # 'payments'
```

---

## 4. Extract: Leer según formato

```python
# etl/extract.py
from pyspark.sql import SparkSession
from config.report_config import ReportConfig

def extract_from_dynamodb_export(spark: SparkSession, config: ReportConfig) -> DataFrame:
    """
    Lee archivos JSON exportados desde DynamoDB.
    Formato: {"Item": {"id": {"S": "123"}, "amount": {"N": "50.00"}}}
    """
    df = spark.read.json(config.source_s3_path())
    
    # Validate
    if df.count() == 0:
        raise ValueError(f"No data found in {config.source_s3_path()}")
    
    return df

def extract_from_s3(spark: SparkSession, config: ReportConfig) -> DataFrame:
    """Lee Parquet, CSV, o Avro según extensión"""
    source = config.source_s3_path()
    format = config.config['source']['format']
    
    if format == 'parquet':
        return spark.read.parquet(source)
    elif format == 'csv':
        return spark.read.option("header", "true").csv(source)
    elif format == 'avro':
        return spark.read.format('avro').load(source)
    else:
        raise ValueError(f"Unsupported format: {format}")
```

---

## 5. Transform: Aplicar Transformaciones

### 5.1 Flatten DynamoDB Structure

```python
# etl/transform.py
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, get_json_object, from_json
from config.report_config import ReportConfig

def flatten_dynamodb_struct(df: DataFrame) -> DataFrame:
    """
    Convierte DynamoDB Item format a columnas planas.
    
    Entrada:
    {"Item": {"id": {"S": "123"}, "amount": {"N": "50.00"}}}
    
    Salida:
    | id  | amount |
    | 123 | 50.00  |
    """
    # Extraer el campo 'Item'
    df = df.select("Item")
    
    # Iterar columnas y extraer S, N, SS, NS, etc.
    # DynamoDB types: S=String, N=Number, B=Binary, SS/NS/BS=Sets, M=Map, L=List
    dynamodb_cols = df.schema['Item'].dataType.fields
    
    exprs = []
    for field in dynamodb_cols:
        field_name = field.name
        # DynamoDB format: {"S": "value"} → need to extract "value"
        exprs.append(
            col(f"Item.{field_name}").getItem(0).alias(field_name)  # Simplified; full impl más compluja
        )
    
    # En producción: usa librería `dynamodb-parquet` o custom parser
    return df.select(*exprs)

def apply_type_casting(df: DataFrame, transformations: list) -> DataFrame:
    """Aplicar type casts según YAML"""
    type_casting = next((t for t in transformations if 'type_casting' in t), None)
    
    if not type_casting:
        return df
    
    for cast in type_casting['type_casting']:
        field = cast['field']
        dtype = cast['type']
        df = df.withColumn(field, col(field).cast(dtype))
    
    return df

def apply_null_handling(df: DataFrame, transformations: list) -> DataFrame:
    """Null handling: drop vs fill"""
    null_handling = next((t for t in transformations if 'null_handling' in t), None)
    
    if null_handling and null_handling['null_handling'] == 'drop':
        # Drop filas con nulls en key fields
        key_fields = ['id', 'payment_id', 'order_id']  # Configurable
        return df.dropna(subset=key_fields, how='any')
    
    return df

def transform_pipeline(spark: SparkSession, df: DataFrame, config: ReportConfig) -> DataFrame:
    """Orquestador de transformaciones"""
    
    # 1. Flatten si es DynamoDB
    if config.config['source']['type'] == 'dynamodb_export':
        df = flatten_dynamodb_struct(df)
    
    # 2. Type casting
    df = apply_type_casting(df, config.transformations())
    
    # 3. Null handling
    df = apply_null_handling(df, config.transformations())
    
    print(f"✅ Transformed: {df.count()} rows, schema: {df.schema}")
    
    return df
```

---

## 6. Load: Escribir a S3 (Raw → Analytics → Curated)

```python
# etl/load.py
from pyspark.sql import DataFrame
from datetime import datetime
from config.report_config import ReportConfig

def load_to_s3(spark: SparkSession, df: DataFrame, config: ReportConfig, stage: str = 'analytics'):
    """
    Escribe a S3 con partición por year/month/day.
    
    Stages:
    - 'raw': copia 1:1 de fuente (sin transformar)
    - 'analytics': transformada, Parquet, particionada
    - 'curated': histórico con CDC (Hudi), pronto para BI
    """
    
    if stage == 'analytics':
        dest = config.destination_curated()
        fmt = config.config['destination']['format_analytics']
    elif stage == 'curated':
        dest = config.config['destination']['curated']
        fmt = config.config['destination']['format_curated']
    else:
        raise ValueError(f"Unknown stage: {stage}")
    
    partitions = config.config['destination'].get('partitions', ['year', 'month', 'day'])
    
    # Escribir con partición
    df.repartition(4)  # Optimize for parallel writes
    
    (df
     .write
     .format(fmt)
     .mode('overwrite' if config.mode() == 'FULL' else 'append')
     .partitionBy(*partitions)
     .save(dest))
    
    print(f"✅ Loaded to {stage}: {dest}")

def write_curated_hudi(spark: SparkSession, df: DataFrame, table_name: str, dest: str):
    """Escribir a Curated en formato Hudi (CDC support)"""
    
    df.write \
        .format("hudi") \
        .mode("upsert") \
        .option("hoodie.table.name", table_name) \
        .option("hoodie.datasource.write.recordkey.field", "id") \
        .option("hoodie.datasource.write.precombine.field", "_change_timestamp") \
        .option("hoodie.datasource.write.operation", "upsert") \
        .option("hoodie.datasource.write.hive_style_partitioning", "true") \
        .option("hoodie.upsert.shuffle.parallelism", 4) \
        .save(dest)
    
    print(f"✅ Hudi CDC table written: {dest}")
```

---

## 7. Main: Orquestador Glue

```python
# main.py
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame

from config.report_config import ReportConfig
from etl.extract import extract_from_dynamodb_export, extract_from_s3
from etl.transform import transform_pipeline
from etl.load import load_to_s3
from etl.metadata import add_metadata

# Parse arguments
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'REPORT_CONFIG'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

try:
    # Load config
    config = ReportConfig(args['REPORT_CONFIG'])
    table_name = config.table_name()
    print(f"🔄 Processing: {table_name}")
    
    # 1. Extract
    print(f"📥 Extract from {config.source_s3_path()}")
    df = extract_from_dynamodb_export(spark, config)
    print(f"   → {df.count()} rows")
    
    # 2. Transform
    print(f"⚙️  Transform")
    df = transform_pipeline(spark, df, config)
    
    # 3. Add metadata
    print(f"📝 Add metadata")
    df = add_metadata(spark, df, config)
    
    # 4. Load (FULL vs INC)
    print(f"📤 Load to S3 (mode: {config.mode()})")
    
    if config.mode() == 'FULL':
        # Reescribir entirely
        load_to_s3(spark, df, config, stage='curated')
    else:
        # Incremental con CDC
        load_to_s3(spark, df, config, stage='curated')  # Usa Hudi merge
    
    print(f"✅ SUCCESS: {table_name} processed")
    job.commit()
    
except Exception as e:
    print(f"❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
    job.commit()
    raise
```

---

## 8. Testing

```python
# tests/test_transform.py
import pytest
from pyspark.sql import SparkSession
from etl.transform import flatten_dynamodb_struct, apply_type_casting

@pytest.fixture
def spark():
    return SparkSession.builder.appName("test").getOrCreate()

def test_flatten_dynamodb_struct(spark):
    """Test conversion of DynamoDB Item format to flat columns"""
    
    data = [
        {"Item": {"id": {"S": "123"}, "amount": {"N": "50.00"}}},
        {"Item": {"id": {"S": "124"}, "amount": {"N": "75.50"}}},
    ]
    
    df = spark.createDataFrame(data)
    result = flatten_dynamodb_struct(df)
    
    assert result.columns == ['id', 'amount']
    assert result.count() == 2

def test_type_casting(spark):
    """Test type conversions"""
    
    data = [("123", "50.00"), ("124", "75.50")]
    df = spark.createDataFrame(data, ["id", "amount"])
    
    config = ReportConfig('test_config.yml')
    result = apply_type_casting(df, config.transformations())
    
    assert str(result.schema['amount'].dataType) == 'DecimalType(10,2)'
```

---

## 9. Cloud Deployment: AWS Glue Job Setup

```bash
# Crear Glue Job con config YAML
aws glue create-job \
    --name "glue-payments-dynamodb" \
    --role arn:aws:iam::123456789:role/GlueJobRole \
    --command Name=pythonshell,ScriptLocation=s3://pragma-scripts/glue/main.py,PythonVersion=3.9 \
    --max-retries 1 \
    --timeout 60 \
    --default-arguments '{
        "REPORT_CONFIG": "s3://pragma-config/reports/payments.yml",
        "--additional-python-modules": "pyyaml,boto3"
    }' \
    --glue-version 4.0

# Ejecutar con config
aws glue start-job-run \
    --job-name glue-payments-dynamodb \
    --arguments '{"--REPORT_CONFIG":"s3://pragma-config/reports/payments.yml"}'
```

---

## 10. Reutilización: Agregar Nueva Tabla

**Para agregar tabla `customers`:**

1. **Crear YAML** (`config/reports/customers.yml`):
```yaml
table_name: customers
source: {type: dynamodb_export, s3_path: "s3://pragma-raw/dynamodb-exports/customers/"}
transformations: [{flatten_dynamodb_struct: true}]
destination: {analytics: "s3://pragma-analytics/customers/", curated: "s3://pragma-curated/customers/"}
mode: FULL
```

2. **Crear Schema** (`addons/schemas/customers.schema.yml`):
```yaml
fields:
  - name: customer_id
    type: string
  - name: email
    type: string
  - name: created_at
    type: timestamp
```

3. **Run el job** (sin cambiar código):
```bash
aws glue start-job-run \
    --job-name glue-payments-dynamodb \
    --arguments '{"--REPORT_CONFIG":"s3://pragma-config/reports/customers.yml"}'
```

**✅ Ventajas:** 5 minutos para agregar tabla, reutilizar 100% del código.

---

### REFERENCIAS RELACIONADAS

- **Prompt:** `prompts/data-engineering/glue-job-validation.md` (Validación de jobs)
- **Instrucciones:** `instructions_or_rules/data-engineering/modular/02-guidelines.md` (Error handling, testing)
- **Instrucciones:** `instructions_or_rules/data-engineering/modular/03-technology.md` (Glue vs alternativas)
- **Instrucciones:** `instructions_or_rules/data-engineering/modular/06-process.md` (Despliegue en AWS Glue)
- **Resource:** `resources/data-engineering/data-contract-patterns.md` (Schema management)
- **🔗 Externo:** `ciencia-datos-datos-pipe-py-carga-dinamica-tablas-dynamodb` (Patrón referencia)
