```markdown
# Ejemplo: Great Expectations (validaciones de calidad de datos)

Este archivo muestra un ejemplo mínimo para integrar Great Expectations (GE) en un MCP.

1) Instalación (entorno local / CI)

```bash
python -m pip install "great_expectations>=0.15"
```

2) Inicializar GE (única vez por proyecto)

```bash
great_expectations init
```

3) Crear una expectation suite (ejemplo en Python)

```python
from great_expectations.core.batch import RuntimeBatchRequest
from great_expectations.data_context import DataContext

context = DataContext()
suite = context.create_expectation_suite(expectation_suite_name="mcp_example_suite", overwrite_existing=True)

# Ejemplo de expectations
batch_request = RuntimeBatchRequest(
    datasource_name="my_datasource",
    data_connector_name="default_runtime_data_connector",
    data_asset_name="incoming_files",
    runtime_parameters={"path": "s3://my-bucket/sample.csv"},
    batch_identifiers={"run_id": "12345"},
)

validator = context.get_validator(batch_request=batch_request, expectation_suite_name="mcp_example_suite")
validator.expect_column_values_to_not_be_null("id")
validator.expect_column_values_to_be_of_type("amount", "FLOAT")
validator.save_expectation_suite()

```

4) Validación via Checkpoint (ejemplo mínimo)

```bash
# Definir un checkpoint con `great_expectations` (o usar un checkpoint ya creado)
great_expectations checkpoint run --checkpoint-name default_checkpoint
```

5) Recomendaciones de expectations para MCP

- `expect_column_values_to_not_be_null` para claves primarias.
- `expect_column_values_to_be_unique` para identificadores cuando aplique.
- `expect_column_values_to_be_between` para rangos numéricos.
- `expect_column_values_to_match_regex` para formatos (emails, ids).
- `expect_table_row_count_to_be_between` para detectar drop/dup de archivos.

6) Integración en CI

- Añadir `great_expectations` en el paso de dependencias del pipeline.
- Ejecutar `great_expectations checkpoint run` y fallar el job si la validación retorna estado `failed`.

7) Observabilidad y reporting

- Configurar GE para publicar resultados en S3/Cloud Storage o en el dashboard de GE.
- Capturar métricas de calidad en tu sistema de observabilidad (via exporter o integraciones).

```
