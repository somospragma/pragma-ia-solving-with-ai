```markdown
# Agent Considerations & Hydration Notes

## 99.1. Summary for Agents

- Priorizar reglas críticas: idempotencia, contratos y observabilidad.
- Solicitar solo cambios incrementales acompañados de pruebas y muestras de datos.

## 99.2. Context Window Guidance

- Mantener la sección "Reglas Críticas" y los `Data Contracts` al inicio del orquestador.
- Referenciar módulos complementarios en el orquestador; no enviar archivos largos en un solo prompt.

## 99.3. Example Prompts

- "Dame un plan de tests para validar un backfill de `domain.entity.v2` que incluya checks de unicidad y drift." 
- "Genera un playbook para incidentes de schema drift con pasos automáticos y manuales."

```
