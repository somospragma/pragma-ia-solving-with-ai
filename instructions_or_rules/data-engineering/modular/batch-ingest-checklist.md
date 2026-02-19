```markdown
# Checklist: Validación de arquitectura de ingesta batch

Checklist para validar pipelines de ingesta batch (files, bulk APIs, ETL por ventanas).

## Contexto y objetivos
- Describir dominio, owners y consumidores.
- Definir SLAs: máxima latencia aceptada por ventana, freshness, ventanas de procesamiento.

## Fuentes y formatos
- Tipos de fuente: dumps (SFTP/FTP), archivos en object storage, APIs bulk, export DB.
- Formatos: CSV/JSON/Parquet/AVRO. Definir codificación, delimitadores y esquema.

## Validaciones de llegada y esquema
- **Extensiones permitidas:** Lista clara (ej. .csv, .parquet, .avro). Rechazar otros y enviar a carpeta de cuarentena.
- **Naming convention:** Patrón de nombre de archivo obligatorio (p.ej. domain_entity_YYYYMMDD_HHMMSS.ext). Validar con regex en pipeline.
- **Encoding y delimitadores:** Confirmar encoding (UTF-8) y delimitador (comma/pipe); reprocesar o normalizar si difiere.
- **Headers y columnas esperadas:** Verificar presencia de header y correspondencia de columnas con el `schema` esperado.
- **Tipos de datos y nullability:** Validar tipos (int, float, string, date, timestamp, boolean) y restricciones de nulls según contrato.
- **Formato de fechas y zonas horarias:** Validar formatos (ISO8601 preferido) y normalizar zonas horarias.
- **Valores permitidos y rangos:** Chequear dominios (enums), rangos numéricos y límites lógicos (p.ej. porcentaje 0-100).
- **Checksums e integridad:** Validar checksum/size/row-count declarados por el productor.
- **Duplicados y claves primarias:** Detectar duplicados en la ventana y verificar claves únicas cuando aplique.
- **Schema evolution / mismatches:** Si el schema difiere, aplicar reglas: accept-with-mapping / reject-and-notify / require migration.
- **Sample validation:** Ejecutar validación sobre un sample (primer N archivos/rows) antes de procesar todo el lote.
- **Error handling:** Archivar vs cuarentena: definir carpeta de errored inputs y procedimiento de re-ingest.


## Contract & Schema
- Schema versionado en Git y publicado en catálogo.
- Validaciones de schema en CI antes de aceptar cambios.

## Ingestión y entrega de archivos
- Estrategia de landing zone (prefijo con timestamp) y naming convention.
- Validación de integridad al llegar (checksums, size, row counts).

## Particionado y organización en storage
- Particionar por fecha y por dimensiones clave; controlar número de ficheros por partición.
- Política de compaction y housekeeping para small-files.

## Checkpoints, idempotencia y deduplicación
- Procesos idempotentes: marca de runs, procesamiento por ventana, marca de consumo.
- Estrategias de dedupe y reconciliación (row-level id, hashes, incremental keys).

## Retries y errores
- Política de reintentos para ingest (retries por fallo de transferencia) y jobs.
- DLQ o folder de errored inputs para reprocesos manuales/automáticos.

## Backfill y reprocesos
- Procedimiento para backfills: snapshot inputs, ejecutar en staging, validar checks, promover.
- Controlar impacto en downstream (versionado temporal de tablas si necesario).

## Observabilidad y métricas mínimas
- Job duration, success/failure count, processed rows, late-arrival count, input file size and count.
- Exponer métricas en plataforma de monitoring y definir alertas para thresholds clave.

## Tests y validaciones en CI
- Unit tests para transformaciones, contract tests para schema, integration tests con sample files.
- Perf-smoke: validar que muestras representativas cumplen budget de tiempo.

## Seguridad y gobernanza
- Control de acceso a landing zones y raw data; cifrado y clasificación de PII.
- Políticas de retención y eliminación automatizadas.

## Infra & IaC
- Módulos IaC para provisioning de buckets/containers, roles y jobs.
- Validaciones `terraform plan` / `az cli` / `aws cli` en CI.

## Runbooks críticos a incluir
- Missing batch (no files), corrupted files, schema mismatch, backfill failure.

## Acceptance criteria (pre-promote)
- Llegada de archivos verificada y checksum match.
- Contract tests pasan.
- Perf-smoke dentro del budget.
- Observability endpoints y alertas configuradas.

```
