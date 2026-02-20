# MCP - Ingeniería de Datos

Este directorio contiene instrucciones y guías para implementar MCPs (Minimal Minimum Viable Products) de Ingeniería de Datos y pipelines de datos en plataformas AWS y Azure.

## 📋 Estructura

- **`mcp-data-engineering.md`** — Resumen de alto nivel del MCP (punto de entrada rápido).
- **`modular/`** — Orquestador modular y módulos detallados:
  - `instructions.md` — Índice y guía de navegación.
  - `01-context.md` — Contexto, alcance y stakeholders.
  - `02-guidelines.md` — Principios, código, SOLID, OOP, testing, documentación, code review.
  - `03-technology.md` — Stacks recomendados (AWS/Azure), conectores, formatos, arquitecturas híbridas.
  - `04-quality.md` — Testing, coverage, Data Quality, monitoring.
  - `05-process.md` — IaC, CI/CD, runbooks, backfill, operación.
  - `99-agent-considerations.md` — Notas para agentes (Copilot, Amazon Q).
  - `*-checklist.md` — Checklists para validación de arquitecturas (streaming, batch, hybrid).
  - `great-expectations-example.md` — Guía de uso de Great Expectations.

## 🚀 Cómo empezar

### 1. **Lectura rápida (5 min)**
Lee `mcp-data-engineering.md` para entender reglas críticas, alcance y responsabilidades.

### 2. **Modelo mental de módulos**
Lee `modular/instructions.md` para ver cómo se organizan los módulos y qué cargar según tu tarea.

### 3. **Por contexto de trabajo**

- **Diseñando arquitectura:** Carga `01-context.md` + `03-technology.md` (platform focus).
- **Implementando pipeline:** Carga `02-guidelines.md` + `04-quality.md` (código y calidad).
- **Desplegando a producción:** Carga `05-process.md` + `04-quality.md` (operación e IaC).
- **Validando ingestas:** Usa `streaming-ingest-checklist.md`, `batch-ingest-checklist.md` o `hybrid-architecture-checklist.md`.
- **AI asistentes:** Usa `99-agent-considerations.md` para instruir agentes (Copilot, Amazon Q).

## 🔧 Hidratación para tu proyecto

Este MCP es un **marco transversal**. Para adaptarlo a tu proyecto:

1. **Reemplaza placeholders:**
   - `domain.entity` → tu modelo de datos específico.
   - `MyJob`, `my-topic` → nombres reales de jobs y streams.
   - Conectores genéricos → tus conectores específicos (qué DB usas, APIs, formatos).

2. **Personaliza por tecnología:**
   - Si usas **AWS Glue/EMR:** Enfatiza secciones de Glue en `03-technology.md` y runbooks en `05-process.md`.
   - Si usas **Azure Synapse/Databricks:** Usa mappings Azure en `03-technology.md`.
   - Si es **hybrid (on-prem + cloud):** Carga `hybrid-architecture-checklist.md`.

3. **Añade reglas específicas:**
   - En `02-guidelines.md`: Políticas de tu equipo (naming, standards, SLAs).
   - En `04-quality.md`: Umbrales de cobertura, herramientas específicas (Deequ vs Great Expectations).
   - En `05-process.md`: Rutas de deploy, teams slack, rotación de on-call.

4. **Publica el orquestador en tu repo:**
   ```bash
   # Para GitHub Copilot:
   cp modular/instructions.md ../.github/copilot-instructions.md
   
   # O para Amazon Q:
   cp modular/*.md ../.amazonq/rules/
   ```

## 📖 Documentación detalles

- **Validaciones de datos:** [batch-ingest-checklist.md](./modular/batch-ingest-checklist.md) y [streaming-ingest-checklist.md](./modular/streaming-ingest-checklist.md) cubren tipos, schemas, naming, checksums, DLQ, canary testing.
- **Arquitecturas híbridas:** [hybrid-architecture-checklist.md](./modular/hybrid-architecture-checklist.md) cubre conectividad, gateways, security, observabilidad distribuida.
- **Calidad de código:** [02-guidelines.md](./modular/02-guidelines.md) sección 2.12 incluye code review checklist, 2.5 SOLID, 2.14 OOP.
- **Testing & Coverage:** [04-quality.md](./modular/04-quality.md) cubre pytest, coverage gates, edge cases, CI pipeline stages.
- **Runbooks:** [05-process.md](./modular/05-process.md) incluye triage para degradación Glue/Synapse, backfill seguro, network outage.
- **Data Quality Framework:** [great-expectations-example.md](./modular/great-expectations-example.md) con tutorial e integración en CI.

## 🔗 Referencias externas

- **Estándar de instrucciones:** [Estándar para las Instrucciones.md](../../alejandría/Estándar%20para%20las%20Instrucciones.md)
- **AWS Well-Architected (Data):** https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html
- **Azure Well-Architected (Data):** https://learn.microsoft.com/en-us/azure/well-architected/what-is-well-architected-framework
- **Great Expectations:** https://greatexpectations.io/
- **Deequ (AWS):** https://github.com/awslabs/deequ

## ⚙️ Integración con agentes

Si usas **GitHub Copilot** o **Amazon Q**:

1. Copia el orquestador (`modular/instructions.md`) a `.github/copilot-instructions.md` o `.amazonq/rules/`.
2. Referencia módulos específicos en tus prompts vs cargar el archivo completo (respect context window limits).
3. Para agentes, prioriza **reglas críticas** (idempotencia, contracts, observabilidad) y solicita **cambios incrementales con tests**.

Ver `99-agent-considerations.md` para ejemplos de prompts.

## 📝 Notas

- **Tamaño de archivo:** Respeta el límite de 12,000 caracteres por archivo de instrucciones (Windsurf/Copilot).
- **Versionado de schemas:** Usa `domain.entity.v{version}` y versionado semántico.
- **Backward compatibility:** Documenta breaking changes en **Data Contracts**.
- **Observability first:** Incluye métricas y logging mínimo desde la primera PR.

## 🤝 Contribución

Si encuentras gaps o tienes sugerencias para mejorar estas instrucciones:
1. Abre una PR en esta rama (`feature/data-science` o similar).
2. Valida cambios con el Estándar y alineación con AWS/Azure Well-Architected.
3. Actualiza checklists y runbooks si aplica.

---

**Última actualización:** 20 de febrero de 2026  
**Versión:** 1.0  
**Owner:** Data Engineering Chapter
