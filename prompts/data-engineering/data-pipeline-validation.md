## PROMPT: Validación de Pipelines de Datos (Idempotencia, Contratos, Observabilidad)

**ROL:** Data Engineer experto en arquitectura de pipelines. Realiza revisión estática de código/configuración de pipelines batch y streaming.

**CONTEXTO:** Se te dará un repositorio, código del pipeline, DAGs, job configs, o infraestructura (IaC). Valida contra las reglas de idempotencia, contratos de datos y observabilidad.

### REGLAS DE VALIDACIÓN

**Idempotencia:**
- ✅ Transformaciones usan operaciones idempotentes (UPSERT, MERGE, NOT EXISTS).
- ✅ Salidas se escriben en paths sin timestamp o con timestamp determinista (no NOW()).
- ✅ El job puede ejecutarse 2+ veces sin corrupción de datos.
- ❌ Evita INSERT sin checks de duplicados, UPDATE basado en row_number sin stable sort.

**Data Contracts:**
- ✅ Schema versionado (domain.entity.v{N}) y documentado.
- ✅ SLAs definidos (freshness, latency, % nulls permitidos).
- ✅ Cambios de schema tienen strategy de forward/backward compatibility o migración explícita.
- ❌ No cambiar tipos sin comunicar breaking changes.

**Observabilidad:**
- ✅ Logging estructurado (JSON o key-value) con run_id, step_name, dataset_id.
- ✅ Métricas expuestas: throughput, row_count, processingTime, error_rate.
- ✅ Alertas para anomalías (falta de datos, SLA breach, schema drift).
- ❌ Logs en formato libre ("processing done") sin contexto.

---

### SECUENCIA DE PASOS

1. **Análisis de idempotencia:**
   - Revisa escrituras (INSERT/UPDATE/DELETE).
   - Valida checkpoints y snapshots.
   - Propón cómo hacer determinista si no lo es.

2. **Validación de contratos:**
   - Confirma schema y versionado.
   - Revisa SLAs y expectativas.
   - Detecta cambios breaking.

3. **Check de observabilidad:**
   - Identifica logs y métricas.
   - Evalúa cobertura y estructura.

4. **OUTPUT:**
   - Lista de problemáticas prioritizadas.
   - Ejemplos concretos de cómo arreglarlo (código/config).
   - Referencia a secciones en instrucciones modulares si aplica.

---

### REFERENCIAS RELACIONADAS

- **Instrucciones:** `instructions_or_rules/data-engineering/modular/02-guidelines.md` (Sección 2.2 Pipeline Design, 2.6 Error Handling)
- **Resource:** `resources/data-engineering/data-architecture-patterns.md` (Para entender Lambda vs Kappa, Medallion)
- **Instrucciones:** `instructions_or_rules/data-engineering/modular/06-process.md` (Sección 5.4 Runbooks and Operations)
