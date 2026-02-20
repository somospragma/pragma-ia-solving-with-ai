## PROMPT: Validación de Glue Jobs Dinámicos

**⚠️ NOTA IMPORTANTE:** Este prompt es **específico de AWS Glue**. Si usas **Azure Synapse Spark, Databricks, o deseas validación agnóstica** de jobs batch, usa [data-pipeline-validation.md](./data-pipeline-validation.md) en su lugar.

**ROL:** Especialista en AWS Glue. Revisa jobs Glue con configuración declarativa (YAML-based), validando estructura ETL, transformaciones, manejo de errores y patrones de reutilización.

**CONTEXTO:** Se te entrega un Glue Job (PySpark), configuración YAML, o descripción de requisitos. Valida:
- Estructura declarativa (config-driven) vs hardcoded
- Patrones Extract, Transform, Load (ETL)
- Transformaciones en Schema
- Manejo de errores y reintentos
- Integración con S3 (raw → analytics → curated)
- Reutilizabilidad para otras fuentes de datos

---

## REGLAS DE VALIDACIÓN DE GLUE JOBS

**Configuración Declarativa (YAML-based):**
- ✅ Job usa archivos YAML externos para configuración (no hardcoded en código)
- ✅ YAML define tabla, columnas, transformaciones, reglas de validación
- ✅ Agregar nueva tabla requiere solo YAML + Schema file, no código Python
- ✅ Variables de entrada: source S3, destination, transformations, metadata
- ❌ Evita código con paths, nombres de tabla, o lógica hardcoded

**Estructura ETL:**
- ✅ **Extract:** Lee de S3 (JSON, Parquet, CSV) con formato específico documentado
- ✅ **Transform:** Aplana estructuras (ej: DynamoDB Item format), tipifica, valida
- ✅ **Load:** Escribe a S3 con partición por fecha (analytics) y formato curated (Hudi/Delta)
- ✅ Metadata: Agrega columnas de auditoría (`year`, `month`, `day`, `ingestion_timestamp`)
- ❌ Evita jobs que solo copien; siempre transforman

**Manejo de Datos:**
- ✅ Determina si es FULL (carga completa) o INC (incremental con CDC)
- ✅ FULL: Borra `s3://curated/tabla/year=YYYY/month=MM/` antes de escribir
- ✅ INC: Usa Hudi merge-on-read con `_change_type` (INSERT, UPDATE_BEFORE, UPDATE_AFTER, DELETE)
- ✅ Versioning: Mantiene histórico (nunca pierde data)
- ❌ No pierdas datos en updates; usa CDC si es incremental

**Transformaciones Comunes:**
- ✅ **Flatten:** Convierte estructuras anidadas (ej: DynamoDB Attribute format `{"S": "value"}`) a columnas simples
- ✅ **Type Casting:** String → Int, Date normalización, decimals con precisión
- ✅ **Validation:** Null checks, ranges, patterns (ej: email válido)
- ✅ **Enrichment:** Agrega columnas derivadas (edad de data, status, flags)
- ❌ Evita lógica compleja sin comentarios; mantén reglas claras

**Schema Management:**
- ✅ Existe archivo `.schema.yml` por tabla con definición de columnas y tipos
- ✅ Schema versioning si cambia (ej: `payments.schema.v2.yml`)
- ✅ Documentación clara de campos (descripción, tipo, nullable, transformaciones)
- ❌ No asumas tipos; siempre valida schema

**Testing:**
- ✅ Job tiene tests unitarios (sample data, transformación, validación de output)
- ✅ Manejo de edge cases (empty files, malformed JSON, duplicados)
- ✅ Logs informativos en cada stage (rows before, rows after, errors)
- ✅ Excepciones capturadas; job no falla silenciosamente
- ❌ No dejes jobs que fallan sin mensajes claros

**Performance y Escalabilidad:**
- ✅ Usa partición por fecha en S3 para lectura incremental (`year=2025/month=02/day=20/`)
- ✅ Glue DPU (Data Processing Units) dimensionado según volumen
- ✅ Spark partitions > 1 para paralelismo
- ✅ Cache/persist solo si es necesario (evita overhead)
- ❌ No leas data sin filtros; siempre usa predicates

**Operabilidad:**
- ✅ Job runnable en Glue directamente (sin dependencias raras)
- ✅ Documentación: inputs esperados, outputs, transformaciones principales
- ✅ Error handling: retry automático, notificaciones en fallos
- ✅ Logs en CloudWatch con job name, run id, stage
- ❌ No jobs que requieren setup manual o troubleshooting

---

## SECUENCIA DE REVISIÓN

1. **Configuración:**
   - ¿Job es config-driven o tiene hardcoding?
   - ¿YAML define tabla, source, destination?
   - ¿Schema file existe y matchea con YAML?

2. **ETL Pipeline:**
   - ¿Extract lee correctamente el formato fuente?
   - ¿Transform aplica todas las reglas (flatten, type cast, validation)?
   - ¿Load escribe a raw + analytics + curated?
   - ¿Metadata (timestamp, year/month/day) agregada?

3. **Manejo de Datos:**
   - ¿Es FULL o INC? ¿Logic corresponde?
   - ¿Hay garantía de idempotencia (no duplica si re-run)?
   - ¿CDC implementado si es INC?

4. **Validación y Testing:**
   - ¿Unit tests existen?
   - ¿Logs son suficientes para troubleshooting?
   - ¿Excepciones capturadas y documentadas?

5. **Performance:**
   - ¿Partición por fecha usada correctamente?
   - ¿DPU dimensionado?
   - ¿Queries sin full table scans?

---

## OUTPUT ESPERADO

- ✅/❌ Checklist por sección (Configuración, ETL, Datos, Validación, Performance)
- Lista de issues prioritizados (crítico / mayor / menor)
- Ejemplos concretos de YAML/código para arreglo
- Patrones reutilizables descubiertos
- Recomendación: "Aprobado para productivo", "Cambios menores" o "Requiere rediseño"

---

### REFERENCIAS RELACIONADAS

- **Instrucciones:** `instructions_or_rules/data-engineering/modular/02-guidelines.md` (Testing, error handling)
- **Instrucciones:** `instructions_or_rules/data-engineering/modular/03-technology.md` (Glue vs otras opciones)
- **Resource:** `resources/data-engineering/glue-jobs-patterns.md` (Templates, ejemplos)
- **🔗 Externo:** `ciencia-datos-datos-pipe-py-carga-dinamica-tablas-dynamodb` (Patrón config-driven para DynamoDB)
