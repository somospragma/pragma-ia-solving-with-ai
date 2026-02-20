# Testing Data Pipelines: Patrones de Test, Contract Tests, Data Quality Gates, CI

Este documento describe estrategias completas para testing pipelines de datos, incluyendo unit tests, integration tests, data quality validations y CI/CD gates.

## 1. Pirámide de Testing para Data Pipelines

```
                   ╱╲
                  ╱  ╲  E2E Tests (prod-like, full data)
                 ╱────╲ ~5% de cobertura, ~30 min c/u
                ╱      ╲
               ╱────────╲ Integration Tests
              ╱  Data    ╲ (sample datasets, real services)
             ╱   QA      ╲ ~20% de cobertura, ~5 min c/u
            ╱──────────────╲
           ╱                ╲ Unit Tests
          ╱  Performance     ╲ (transformaciones, lógica)
         ╱   & Contract      ╲ ~75% de cobertura, < 1 sec c/u
        ╱──────────────────────╲
```

---

## 2. Unit Tests: Transformaciones Puras

### Patrón: Given-When-Then

```python
# test_transformations.py
import pytest
from pyspark.sql import SparkSession
from my_pipeline.transforms import clean_customer

@pytest.fixture
def spark():
    return SparkSession.builder.getOrCreate()

@pytest.mark.parametrize("name,expected", [
    ("John Doe", "John Doe"),        # normal
    ("  john  ", "John"),             # whitespace + lower
    ("JANE-SMITH", "Jane-Smith"),     # hyphen preserved
    ("", "UNKNOWN"),                  # empty → default
])
def test_clean_customer_name(spark, name, expected):
    # Given
    input_df = spark.createDataFrame(
        [(name,)], schema="name string"
    )
    # When
    result = clean_customer(input_df)
    # Then
    assert result.select("name").collect()[0][0] == expected

# Edge cases obligatorios
def test_clean_customer_nulls(spark):
    input_df = spark.createDataFrame(
        [(None,)], schema="name string"
    )
    result = clean_customer(input_df)
    assert result.select("name").collect()[0][0] == "UNKNOWN"

def test_clean_customer_special_chars(spark):
    input_df = spark.createDataFrame(
        [("José María",)], schema="name string"
    )
    result = clean_customer(input_df)
    # Validar encoding UTF-8
    assert "ó" in result.select("name").collect()[0][0]
```

### Coverage objetivo: 80%+ (branch coverage)

```bash
pytest --cov=my_pipeline.transforms --cov-report=html --cov-fail-under=80
```

---

## 3. Contract Tests: Esquemas & SLAs

### Assert Schema Matches Contract

```python
# test_contracts.py
import pytest
from pyspark.sql.types import StructType, StructField, StringType

def test_customer_output_schema(spark):
    """Validar que output cumple contract v2"""
    result_df = run_pipeline(spark)
    
    expected_schema = StructType([
        StructField("customer_id", LongType(), False),
        StructField("email", StringType(), True),
        StructField("created_date", DateType(), False),
        # ... más campos
    ])
    
    assert result_df.schema == expected_schema

def test_customer_sla_freshness(spark):
    """Validar que data no es más vieja de 2 horas"""
    result_df = run_pipeline(spark)
    max_age = result_df.select(
        F.max(F.current_timestamp() - F.col("ingest_timestamp"))
    ).collect()[0][0]
    
    assert max_age.total_seconds() < 2 * 3600  # 2 horas en segundos

def test_customer_sla_completeness(spark):
    """Validar % nulls en campos críticos"""
    result_df = run_pipeline(spark)
    
    null_rates = {
        "customer_id": 0.0,  # Sin nulls permitidos
        "email": 0.05,       # <= 5% nulls aceptables
    }
    
    for col_name, max_null_rate in null_rates.items():
        null_count = result_df.filter(
            F.col(col_name).isNull()
        ).count()
        actual_rate = null_count / result_df.count()
        assert actual_rate <= max_null_rate, \
            f"{col_name}: {actual_rate*100:.1f}% nulls (max {max_null_rate*100:.1f}%)"
```

---

## 4. Integration Tests: End-to-End com Sample Data

### Estructura

```
tests/
├── unit/
│   └── test_transformations.py         (rápidos, < 1 sec)
├── integration/
│   ├── test_pipeline_e2e.py            (mid-speed, ~2-5 sec)
│   ├── fixtures/
│   │   ├── sample_customers.csv
│   │   ├── sample_orders.parquet
│   │   └── expected_output.json
│   └── conftest.py                     (setup compartido)
└── contract/
    └── test_contracts.py               (rápidos, < 1 sec)
```

### Ejemplo: Test E2E con Sample Data

```python
# tests/integration/test_pipeline_e2e.py
@pytest.fixture
def sample_customers(spark, tmp_path):
    """Crear DF de clientes sample"""
    data = [
        (1, "alice@example.com", "2024-01-01"),
        (2, "bob@example.com",   "2024-01-02"),
        (None, "invalid@example.com", "2024-01-03"),  # null PK
    ]
    df = spark.createDataFrame(
        data, schema="customer_id long, email string, created_date string"
    )
    path = f"{tmp_path}/customers.parquet"
    df.coalesce(1).write.parquet(path)
    return path

def test_full_pipeline(spark, sample_customers, tmp_path):
    """Test pipeline completo con datos sample"""
    output_path = f"{tmp_path}/output"
    
    # Ejecutar pipeline
    result = run_full_pipeline(
        input_path=sample_customers,
        output_path=output_path,
        spark=spark
    )
    
    # Validaciones
    assert result.count() == 2  # 3 input - 1 null
    assert result.filter(F.col("customer_id").isNull()).count() == 0
    assert result.select("email").distinct().count() == 2
    
    # Validar schema
    assert "transformed_date" in result.columns
    
    # Validar datos (spot checks)
    row = result.filter(F.col("customer_id") == 1).collect()[0]
    assert row["email"] == "alice@example.com"
```

---

## 5. Data Quality Gates en CI

### GitHub Actions: Data Quality Pipeline Stage

```yaml
# .github/workflows/data-quality.yml
name: Data Quality Tests

on: [pull_request, push]

jobs:
  tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install pyspark pytest pytest-cov great-expectations
      
      - name: Unit & Contract Tests
        run: |
          pytest tests/unit tests/contract --cov=src \
            --cov-report=xml --cov-fail-under=80 \
            -v
      
      - name: Integration Tests
        run: |
          pytest tests/integration -v --tb=short
      
      - name: Data Quality Checks (Great Expectations)
        run: |
          great_expectations checkpoint run ml_pipeline_checkpoint
          # Exit code != 0 si DQ checks fallan
      
      - name: Upload Coverage Reports
        if: always()
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml
          fail_ci_if_error: true
      
      - name: Comment PR with Results
        if: always()
        uses: actions/github-script@v6
        with:
          script: |
            // Leer results y comentar en PR
            const fs = require('fs');
            const coverage = fs.readFileSync('coverage.txt', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `### Data Quality Report\n${coverage}`
            });
```

### Criterios de Pass/Fail

| Stage | Criterio | Action |
|-------|----------|--------|
| Unit Tests | Coverage >= 80% | Fail PR si no |
| Contract Tests | Schema + SLA OK | Fail PR si breaking |
| Integration Tests | All pass | Warn PR si intermitente |
| DQ Checks | Critical gates | Fail PR si no |
| Performance | No degradation > 10% | Warn PR si sí |

---

## 6. Monitoreo Post-Deploy

### Métricas en Producción

```python
# Código en pipeline de producción
from datadog import initialize, api
import logging
import json

logger = logging.getLogger(__name__)

def log_metrics(run_id, stage_name, metrics):
    """Enviar métricas a observabilidad"""
    structured_log = {
        "run_id": run_id,
        "stage": stage_name,
        "throughput_rows_per_sec": metrics["rows"] / metrics["duration"],
        "row_count": metrics["rows"],
        "null_percentage": metrics["null_pct"],
        "processing_time_sec": metrics["duration"],
        "timestamp": datetime.utcnow().isoformat(),
    }
    logger.info(json.dumps(structured_log))

# En tu código Spark
result_df = transform_data(input_df)
metrics = {
    "rows": result_df.count(),
    "null_pct": calculate_nulls(result_df),
    "duration": timer.elapsed,
}
log_metrics(run_id=RUN_ID, stage_name="transform", metrics=metrics)
```

### Alertas

```yaml
# Datadog or similar alerting rule
alert: PipelineNullRateHigh
condition: |
  avg(last_1h): null_percentage > 5%
  AND stage == "curated"
action: |
  - Slack: notify #data-team
  - PagerDuty: if null_percentage > 20%
```

---

## 7. Checklist de Testing Completo

### Antes de PR
- [ ] Unit tests: >= 80% coverage, rápidos (< 30 sec)
- [ ] Contract tests: schema + SLA validados
- [ ] Edge cases: nulls, empty, special chars, encoding
- [ ] Logs: estructurados, con run_id y dataset_id
- [ ] Performance: no degradación > 10% vs baseline

### En PR Review
- [ ] Coverage no disminuyó
- [ ] Tests pasan en CI
- [ ] Cambios de schema? → data-contract-patterns.md
- [ ] Observabilidad: ¿nuevas métricas expuestas?

### Post-Merge (Producción)
- [ ] Monitoreo activo (primeras 24h)
- [ ] Alertas configuradas
- [ ] Runbook actualizado si new incidentes
- [ ] Datos validan contra expectations (DQ gates)

---

## 8. Herramientas Recomendadas

| Herramienta | Propósito | Setup |
|-------------|-----------|-------|
| **pytest** | Framework de tests | `pip install pytest` |
| **pytest-cov** | Cobertura | `pytest --cov=src` |
| **Great Expectations** | Data quality | `pip install great-expectations` |
| **dbt** | Documentación + tests | `dbt test` (si usas dbt) |
| **Testcontainers** | Spin up services (DB, Kafka) | `pip install testcontainers` |
| **Datadog / DataDog** | Monitoring producción | Integración nativa |

---

## Referencias

- [Pytest Documentation](https://docs.pytest.org/)
- [PySpark Testing Guide](https://spark.apache.org/docs/latest/testing.html)
- [Great Expectations Checkpoints](https://docs.greatexpectations.io/docs/guides/validation/checkpoints/)
- [GitHub Actions: Testing](https://docs.github.com/en/actions/automating-builds-and-testing/about-continuous-integration)
- **Instrucciones:** `instructions_or_rules/data-engineering/modular/04-quality.md` (Estrategia de testing)
