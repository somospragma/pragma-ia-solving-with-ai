# Requirements — Service Documentation Skill

## Contexto

Se requiere una feature que permita estandarizar el diligenciamiento de una plantilla de documentación operativa de servicios a partir de tres artefactos coordinados:

1. Una plantilla operativa reutilizable alineada con soporte, operación y mantenimiento de servicios.
2. Un SKILL reutilizable inspirado en el enfoque de `~/.agent/skills/skill-creator/SKILL.md` para guiar el llenado o auditoría de la plantilla.
3. Un prompt complementario reutilizable que aplique los pro tips de [prompts/transversal/pro_tips-prompt.md](../../prompts/transversal/pro_tips-prompt.md) como heurísticas operativas.

La feature debe alinearse con las convenciones documentadas en [docs/implementation.md](../../docs/implementation.md), [docs/project-structure.md](../../docs/project-structure.md) y [CONTRIBUTING.md](../../CONTRIBUTING.md).

## Requerimientos Funcionales

| ID | Descripción | Prioridad | Criterio de Aceptación |
|----|-------------|-----------|------------------------|
| RF-001 | La feature debe entregar una plantilla operativa reutilizable para diligenciar servicios en producción. | ALTA | La plantilla contiene estructura y placeholders utilizables para documentar generalidades, diseño, operación, observabilidad, recuperación, seguridad y troubleshooting sin depender de un único tipo de sistema. |
| RF-002 | La plantilla debe seguir siendo útil para soporte, operación y mantenimiento en producción. | ALTA | La plantilla conserva las secciones necesarias para generalidades, diseño, operación, observabilidad, recuperación, seguridad y troubleshooting, con placeholders o ejemplos agnósticos. |
| RF-003 | El SKILL debe soportar modo entrevista guiada por secciones. | ALTA | El diseño del SKILL define un flujo donde el agente formula preguntas por sección, detecta vacíos y evita inventar información. |
| RF-004 | El SKILL debe soportar modo intake único con autocompletado de borrador. | ALTA | El diseño del SKILL define entradas mínimas, reglas de inferencia permitida y formato de salida para producir un primer borrador completo. |
| RF-004A | El SKILL debe soportar modo auditoría o refinamiento de documentación existente. | ALTA | El diseño del SKILL define cómo revisar un documento existente, detectar vacíos operativos y responder con hallazgos accionables sin reescribirlo por defecto. |
| RF-005 | El SKILL debe declarar triggers explícitos para documentación operativa y continuidad del servicio. | ALTA | La spec identifica frases de activación como documentación operativa, runbook, handover a soporte, troubleshooting, observabilidad, recuperación e integraciones. |
| RF-006 | El SKILL debe marcar información faltante, usar N/A cuando no aplique y no inventar datos. | ALTA | La spec define reglas explícitas para incertidumbre, faltantes y secciones no aplicables. |
| RF-007 | La feature debe incluir un prompt complementario que aplique los pro tips del repo. | MEDIA | Existe un prompt diseñado para activar el flujo del SKILL e incorporar razonamiento paso a paso, preguntas de aclaración, validación de límites y ajuste de profundidad según audiencia. |
| RF-008 | La feature debe respetar las convenciones de organización del repositorio. | ALTA | La spec propone ubicación final compatible con el patrón por dominio del repo y documenta que la ubicación en mobile/cross-cutting no es la recomendada. |
| RF-009 | La feature debe definir un conjunto inicial de escenarios de validación. | MEDIA | La spec incluye casos representativos con contexto completo, parcial, auditoría de documento existente y con secciones no aplicables. |

## Requerimientos No Funcionales

| ID | Descripción | Métrica |
|----|-------------|---------|
| RNF-001 | Alineación con estándares del repositorio | Los artefactos nuevos o modificados respetan naming, metadata, ejemplos, edge cases y referencias cruzadas según [docs/implementation.md](../../docs/implementation.md). |
| RNF-002 | Reusabilidad operativa de la plantilla | La plantilla puede ser adaptada a distintos servicios sin perder foco operativo ni depender de un documento fuente único. |
| RNF-003 | Reutilización y DRY | El SKILL y el prompt referencian documentación existente en lugar de duplicarla. |
| RNF-004 | Claridad de activación del SKILL | La descripción del SKILL cubre triggers suficientes para evitar under-triggering en escenarios de documentación operativa. |
| RNF-005 | Consistencia interna del borrador generado | El diseño define validaciones cruzadas entre prioridad, disponibilidad, observabilidad, recuperación e incidentes conocidos. |

## Referencias

- [docs/requirements.md](../../docs/requirements.md)
- [docs/implementation.md](../../docs/implementation.md)
- [docs/project-structure.md](../../docs/project-structure.md)
- [CONTRIBUTING.md](../../CONTRIBUTING.md)
- [plantilla-doc.md](../../plantilla-doc.md)
- [prompts/transversal/pro_tips-prompt.md](../../prompts/transversal/pro_tips-prompt.md)

---
> ⏸️ **Gate:** Esperar aprobación humana antes de continuar a `design.md`