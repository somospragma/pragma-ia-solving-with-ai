```markdown
# Code Guidelines & Pipeline Standards

## 2.1. Principles

- Idempotencia y determinismo en transformaciones
- Separación de concerns: ingestion, processing, serving
- Contracts-first: schemas y SLAs definidos antes de la implementación
- Observability-by-design: métricas y logs desde la primera PR

## 2.2. Pipeline Design

- Favor composability (micro-batches o operators reutilizables)
- Checkpoints y snapshots atómicos por etapa
- Retries exponenciales y DLQ para errores irreversibles

## 2.3. Code Quality

- Tests unitarios para UDFs y transformaciones
- Linters y formateadores cuando aplique (pyproject/ruff, scalafmt)
- Revisiones en PR y aprobación por dueño de datos

## 2.4. Naming & Conventions

- Datasets: `domain.entity.v{version}`
- Jobs: `team.feature.pipeline_name` 
- Use semantic versioning para contratos de datos

## 2.5. SOLID Principles & Code Design

- **Single Responsibility:** Cada función/clase tiene una responsabilidad clara; transformaciones no mezclan lógica de ingest, proc y serving.
- **Open/Closed:** Diseña pipelines extensibles sin modificar código existente (via configuración o plugins).
- **Liskov Substitution:** Si usas interfaces o clases base, cumple contratos; evita comportamientos sorpresa.
- **Interface Segregation:** Expone solo métodos necesarios; evita interfaces "gordas".
- **Dependency Inversion:** Inyecta dependencias (configs, conectores); evita hardcoding de credenciales o paths.

## 2.6. Error Handling & Logging

- **Error handling explícito:** Captura errores esperados y aplica retry logic; no dejes excepciones no manejadas.
- **Structured logging:** Usa formatos JSON o key-value; incluye `run_id`, `dataset_id`, `step_name`, `timestamp`.
- **Log levels:** DEBUG para debugging, INFO para hitos, WARNING para anomalías leves, ERROR para fallos, CRITICAL para paradas.
- **Exception messages:** Describe qué falló y por qué; incluye contexto suficiente para debugging (valores, configs, estado).
- **Correlation IDs:** Usa `trace_id` o `run_id` para correlacionar logs en pasos distribuidos.

## 2.7. Code Documentation

- **Docstrings:** Describe qué hace, inputs (parámetros), outputs (return), y excepciones esperadas.
- **Inline comments:** Explica el "por qué" (lógica compleja), no el "qué" (el código ya lo dice).
- **README o wiki:** Instrucciones de setup, ejecución local, troubleshooting y referencias.
- **Type hints:** En Python, usa type hints (`def process(df: DataFrame) -> DataFrame:`); mejora IDE support y detecta bugs.

## 2.8. Testing Patterns

- **Unit tests:** Prueba funciones aisladas; usa fixtures para datos reusables.
- **Parameterized tests:** Prueba múltiples casos con @pytest.mark.parametrize o equivalente.
- **Integration tests:** Prueba flujos end-to-end con datasets sample; usa entornos reproducibles.
- **Contract tests:** Valida que outputs cumplen con schema/SLA esperado.
- **Mocking:** Mock externas (APIs, DBs) para acelerar tests; usa containers si es posible para reproducer integración.
- **Test organization:** Folder `tests/` con estructura que refleja la del código; test runners en CI.

## 2.9. Performance & Optimization

- **Profiling first:** Antes de optimizar, mide dónde está el cuello de botella (CPU, I/O, shuffle, GC).
- **Particionado efectivo:** Particiona datos por dimensiones clave para paralelismo; evita skew.
- **Caching & memoization:** Cache resultados intermedios si se reutilizan; ojo con memory footprint.
- **Resource tuning:** Ajusta workers, shuffle partitions, batch size según volumen y hardware.
- **Materialize vs compute:** Decide si materializas resultados intermedios (disk cost) vs recomputas (CPU cost).

## 2.10. Edge Cases & Robustness

- **Negative testing:** Prueba con inputs inválidos, vacíos, null-heavy; qué pasa con ceros y valores extremos.
- **Boundary conditions:** Primeros/últimos elementos, cambios de timezones, daylight-saving, leap years.
- **Graceful degradation:** Si falla un paso, el pipeline se puede recuperar y no deja corrupción.
- **Idempotent writes:** Escrituras son idempotentes; no deja duplicados si el job reintenta.

## 2.11. Folder Structure & Modularity

```
pipeline-project/
├── src/
│   ├── ingest/          # Extractores y conectores
│   ├── transform/       # Lógica de transformación
│   ├── serving/         # Exportadores y APIs
│   └── utils/           # Helpers reutilizables
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── configs/             # Parámetros por entorno
├── docs/                # Documentación
└── scripts/             # Utilidades y runbooks
```

## 2.12. Code Review Checklist

Antes de mergear una PR, validar:
- [ ] Código cumple naming conventions y es legible.
- [ ] Tests unitarios + integración incluidos y pasan.
- [ ] Logs estructurados y niveles apropiados.
- [ ] Manejo de errores explícito; no hay excepciones silenciosas.
- [ ] Docstrings en funciones públicas.
- [ ] Cambios en schema documentados y versionados.
- [ ] IaC y configuración actualizada si aplica.
- [ ] Performance acceptablemente perfilada.
- [ ] No tiene hardcoded credenciales, paths o configuración.
- [ ] Aprobación del Data Owner o arquitecto si son cambios críticos.

## 2.13. Type Hints & Static Analysis

- **Python:** Usa `mypy`, `pyright` o similar para type checking en CI.
- **Spark/PySpark:** Valida tipos de columnas en DataFrames via schema asserts.
- **SQL:** Usa linters (`sqlfluff`) y formatters; mantén SQL legible y optimizable.
- **Config validation:** Usa Pydantic o dataclasses para validar configuraciones al startup.

```
