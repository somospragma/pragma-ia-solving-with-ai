# Design — Service Documentation Skill

## Arquitectura

La solución se compone de tres artefactos acoplados por contrato funcional, no por automatización técnica:

1. **Plantilla operativa reutilizable**
   [plantilla-doc.md](../../plantilla-doc.md) se mantiene como estructura base reusable para documentar servicios desde una perspectiva operativa. Conserva la estructura necesaria para soporte, operación y mantenimiento, usando placeholders y ejemplos agnósticos cuando ayudan a diligenciar sin inventar datos.

2. **SKILL de diligenciamiento**
   El SKILL se diseña como guía de trabajo para completar la plantilla en dos modos:
   - Entrevista guiada por secciones
   - Intake único con autocompletado de borrador

   El SKILL debe definir:
   - Triggers de activación
   - Secuencia de preguntas mínimas por sección
   - Reglas para uso de N/A
   - Reglas para señalar incertidumbre
   - Validaciones cruzadas de coherencia
   - Formato de salida listo para copiar en la plantilla

3. **Prompt complementario**
   Un prompt reusable actúa como entrypoint para disparar el SKILL con mejores prácticas de prompting. Convierte los tips existentes en una guía operativa para obtener respuestas más consistentes y auditables.

### Flujo lógico

1. El usuario solicita crear o completar documentación operativa de un servicio.
2. El prompt complementario induce al agente a trabajar paso a paso, preguntar faltantes y explicitar límites.
3. El SKILL determina el modo de operación:
   - Si el contexto es incompleto, usa entrevista guiada.
   - Si el contexto es suficiente, arma un borrador completo.
   - Si existe un documento fuente, audita o refina con foco en vacíos operativos.
4. El resultado se valida contra reglas de consistencia y se materializa sobre la plantilla operativa.

## Decisiones Técnicas

| Decisión | Alternativas | Justificación |
|----------|-------------|---------------|
| Mantener una solución de tres artefactos coordinados | Crear solo el SKILL o solo refactorizar la plantilla | El problema real combina una plantilla operativa reusable, guía de diligenciamiento y calidad del prompting. Resolver solo una parte deja huecos funcionales. |
| Soportar dos modos en el SKILL | Elegir solo entrevista guiada o solo autocompletado | Los usuarios pueden llegar con contexto incompleto o con un intake casi listo. Ambos flujos son necesarios para reutilización real. |
| Añadir auditoría o refinamiento como tercer modo | Limitar el alcance a creación desde cero | En documentación operativa es frecuente partir de un documento existente y mejorar su capacidad real de soporte sin rehacerlo por completo. |
| Recomendar dominio `arquitectura` para el SKILL | Usar `mobile/cross-cutting` o crear un dominio nuevo | `arquitectura` es el encaje más coherente con documentación de servicio, diseño operativo y continuidad. La alternativa propuesta no sigue la organización por dominio documentada. |
| Refactorizar la plantilla in place | Mover de inmediato la plantilla a `resources/arquitectura/` | Mantenerla en su ubicación actual reduce fricción y preserva compatibilidad. Un eventual traslado puede planearse como iteración posterior. |
| Usar placeholders y ejemplos agnósticos | Dejar la plantilla casi vacía o llenarla con ejemplos muy concretos | Los placeholders y ejemplos controlados ayudan a diligenciar con foco operativo sin inducir invención ni amarrar la plantilla a un caso único. |
| Convertir pro tips en reglas operativas del prompt | Copiar literalmente el prompt existente | El prompt complementario debe ser accionable y específico al flujo de documentación, no una simple recopilación de tips. |

## Archivos Afectados

| Archivo | Acción | Descripción |
|---------|--------|-------------|
| [plantilla-doc.md](../../plantilla-doc.md) | Modificar | Mantener una plantilla reusable y operable, con placeholders y ejemplos agnósticos para distintos tipos de servicio. |
| [prompts/transversal/pro_tips-prompt.md](../../prompts/transversal/pro_tips-prompt.md) | Referencia | Usar sus principios para diseñar el nuevo prompt complementario sin duplicarlo innecesariamente. |
| instructions_or_rules/arquitectura/skills/service_documentation_template/SKILL.md | Crear | Nuevo SKILL para diligenciamiento de documentación operativa. Ruta propuesta sujeta a aprobación humana. |
| prompts/arquitectura/generar_documentacion_servicio_operable.md | Crear | Prompt reusable para activar el flujo del SKILL con mejores prácticas de prompting. |
| [docs/project-structure.md](../../docs/project-structure.md) | Referencia | Validar consistencia con la organización por dominio y tipo de artefacto. |
| [CONTRIBUTING.md](../../CONTRIBUTING.md) | Referencia | Validar naming, ubicación y checklist de contribución. |

## Validación de Diseño

- La plantilla debe poder adaptarse a backend, mobile, integración o servicios internos sin cambiar su estructura base.
- El SKILL debe explicitar cuándo preguntar, cuándo usar N/A y cuándo declarar falta de contexto.
- El SKILL debe distinguir entre creación desde intake y auditoría de documentos existentes.
- El prompt debe mejorar la calidad del resultado sin duplicar innecesariamente la lógica del SKILL.
- La ruta final del SKILL debe aprobarse antes de implementación, porque la propuesta inicial del usuario no coincide con las convenciones del repo.

## Referencias

- [docs/project-structure.md](../../docs/project-structure.md)
- [docs/tech-stack.md](../../docs/tech-stack.md)
- [docs/implementation.md](../../docs/implementation.md)
- [CONTRIBUTING.md](../../CONTRIBUTING.md)
- [plantilla-doc.md](../../plantilla-doc.md)
- [prompts/transversal/pro_tips-prompt.md](../../prompts/transversal/pro_tips-prompt.md)

---
> ⏸️ **Gate:** Esperar aprobación humana antes de continuar a `tasks.md`