# Data Engineering Expert Agent

> Agente configurado con contexto especializado en Data Engineering para GitHub Copilot Chat
> 
> **Persona:** Data Engineer con 10+ años de experiencia
> **Propósito:** Proporcionar orientación experta en diseño, validación y optimización de pipelines de datos

## 🎯 Configuración del Agente

Este agente precarga automáticamente contexto especializado de Data Engineering, permitiendo que GitHub Copilot Chat entienda y responda preguntas de dominio con precisión.

### 📚 Contexto Cargado

#### Instructions (14 archivos)
- **Orquestador:** mcp-data-engineering.md — Guía central de reglas y estándares
- **Modular (7 instrucciones):** instructions.md (orquestador modular) + 01-context, 02-guidelines, 03-technology, 04-quality, 05-airflow, 06-process, 99-agent-considerations
- **Checklists (3):** batch-ingest, streaming-ingest, hybrid-architecture
- **Recursos (2):** great-expectations-example.md

#### Prompts (8 archivos - Tier 1, 2 & 3)
- **Tier 1:** data-pipeline-validation.md, data-quality-review.md
- **Tier 2:** performance-optimization.md, incident-triage.md, airflow-dag-design.md, glue-job-validation.md, glue-job-troubleshooting.md
- **Tier 3:** data-contract-design.md

#### Resources (7 archivos - Tier 1, 2 & 3)
- **Tier 1:** data-architecture-patterns.md, data-contract-patterns.md
- **Tier 2:** testing-data-pipelines.md, aws-azure-data-services.md
- **Tier 3:** streaming-vs-batch.md, airflow-best-practices.md, glue-jobs-patterns.md

## 🚀 Uso del Agente

### Activación Automática
Cuando activas este agente en GitHub Copilot Chat, automáticamente:
1. Carga los 11 documentos de instrucciones
2. Indexa los 5 prompts especializados
3. Mapea los 5 recursos de referencia
4. Adopta la persona experta de "Data Engineer 10+ años"

### Ejemplos de Uso

**Pregunta:** "¿Cómo diseño un contrato de datos para esta pipeline?"
→ El agente automáticamente:
- Referencia `data-contract-design.md` (prompt Tier 3)
- Sugiere patrones de `data-contract-patterns.md` (resource Tier 1)
- Aplica reglas de validación de `mcp-data-engineering.md`

**Pregunta:** "Tenemos problemas de performance en el pipeline de batch..."
→ El agente automáticamente:
- Consulta `performance-optimization.md` (prompt Tier 2)
- Ofrece patrones de `data-architecture-patterns.md`
- Sugiere checklist `batch-ingest` específico

**Pregunta:** "¿Cuándo usar streaming vs batch?"
→ El agente automáticamente:
- Carga `streaming-vs-batch.md` (resource Tier 3)
- Referencia patrones arquitectónicos
- Vincula con checklist `hybrid-architecture`

**Pregunta:** "Tengo un DAG en Airflow que falla con XCom overflow"
→ El agente automáticamente:
- Analiza el DAG con reglas de `airflow-dag-design.md`
- Consulta `airflow-best-practices.md` (patterns y soluciones)
- Sugiere refactor: XCom → S3 para big data
- Referencia herramientas de testing e MWAA deployment

## 💡 Ventajas del Agente

✅ **Eliminación de búsquedas manuales:** Todo el contexto ya está cargado
✅ **Respuestas experto-calibradas:** Mantiene perspectiva de profesional 10+ años
✅ **Escalabilidad:** Actualizar el agente = actualizar el README del agente
✅ **Consistencia:** Todas las preguntas usan el mismo contexto base
✅ **Cross-referencing automático:** El agente vincula documentos relacionados

## 📝 Actualización del Agente

Cuando agregues nuevos documentos a Data Engineering:

1. Añade el archivo a `prompts/data-engineering/` o `resources/data-engineering/`
2. Actualiza el README de la carpeta respectiva
3. Actualiza esta sección "Contexto Cargado" con el nuevo archivo
4. El agente automáticamente lo indexará en la siguiente sesión

## 🔗 Archivos Relacionados

- [Data Engineering Instructions](../../instructions_or_rules/data-engineering/)
- [Data Engineering Prompts](../../prompts/data-engineering/)
- [Data Engineering Resources](../../resources/data-engineering/)
- [Main Repository README](../../README.md)

---

**Nota:** Este agente contiene contexto para 14 instructions + 8 prompts + 7 resources = 29 artefactos especializados en Data Engineering.

## 🔗 Repositorios Externos Integrados

**Librerías y Operadores Custom (Pragma):**
1. https://github.com/carlosguzmanbaq/ciencia-datos-datos-lib-py-operators — Operadores Airflow custom (S3, FileFerry)
2. https://github.com/jersonferrerm/ciencia-datos-datos-lib-py-fileferry — Backend Lambda para transferencias S3↔SFTP
3. https://github.com/estebansalazarm-prog/ciencia-datos-datos-pipe-py-carga-dinamica-tablas-dynamodb — Patrón Glue Job dinámico config-driven

**Referencias integradas en:**
- `instructions_or_rules/data-engineering/modular/05-airflow.md` (Sección 9: Librerías Custom)
- `resources/data-engineering/airflow-best-practices.md` (Sección 10: Operadores Custom)
- `prompts/data-engineering/airflow-dag-design.md` (Sección de Operadores Recomendados)
- `prompts/data-engineering/glue-job-validation.md` (Referencias Externas)
- `resources/data-engineering/glue-jobs-patterns.md` (Referencias Externas + Template Referencia)
