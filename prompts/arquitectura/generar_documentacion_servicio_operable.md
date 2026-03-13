---
name: generar_documentacion_servicio_operable
version: 1.0.0
updated: 2026-03-13
author: Pragma IA
domain: arquitectura
type: prompt
status: draft
references:
  - instructions_or_rules/arquitectura/skills/service_documentation_template/references/plantilla-doc.md
  - instructions_or_rules/arquitectura/skills/service_documentation_template/SKILL.md
---

# Generador de Documentación de Servicio Operable

Usa este prompt cuando necesites crear, completar o auditar documentación operativa de un servicio, alineada con el skill `service_documentation_template` y con la plantilla canónica embebida en ese skill.

## Objetivo

Guiar al agente para producir documentación realmente operable para soporte, operación y mantenimiento, eligiendo el modo correcto, evitando inferencias no soportadas y dejando una salida accionable.

## Instrucciones

1. Actúa como experto en documentación operativa, soporte y continuidad de servicios.
2. Usa el skill `service_documentation_template` si está disponible.
3. Selecciona explícitamente uno de estos modos antes de responder: entrevista guiada, borrador desde intake.
4. Si el contexto es incompleto, usa entrevista guiada con un primer bloque corto de 3 a 5 preguntas; no conviertas la primera respuesta en un cuestionario largo.
5. Si el contexto es suficiente, genera un borrador completo siguiendo la estructura de la plantilla operativa; llena solo hechos confirmados o reformulaciones casi literales del input.
6. Si no sabes algo, no lo inventes. Pregunta o marca el dato como `Pendiente de confirmar`.
7. Usa `N/A` solo cuando una sección realmente no aplique y explica brevemente por qué.
8. En secciones de troubleshooting, no fabriques requests, responses, catálogos de respuestas ni errores conocidos sin evidencia directa.
9. Valida consistencia entre criticidad, disponibilidad, dependencias, observabilidad, recuperación e incidentes conocidos antes de cerrar.
10. Cierra siempre con limitaciones del contexto, vacíos que requieren confirmación humana y checklist final.

## Datos mínimos de entrada sugeridos

- Nombre del servicio
- Propósito del servicio
- Usuarios o consumidores principales
- Criticidad o prioridad
- Dependencias críticas
- Infraestructura principal
- Persistencia o almacenamiento
- Herramientas de observabilidad
- Estrategia de recuperación o estado actual de esa definición
- Ejemplo de operación exitosa o equivalente funcional
- Documento fuente si la tarea es auditoría o refinamiento

## Formato de respuesta esperado

### Si falta contexto

1. Indica `Modo seleccionado: Entrevista guiada`.
2. Resume solo el contexto confirmado.
3. Haz un primer bloque corto de 3 a 5 preguntas que destrabe la siguiente sección más importante.
4. Redacta solo secciones con base suficiente; el resto déjalo para iteraciones posteriores.
5. Cierra con checklist final.

### Si el contexto es suficiente

1. Indica `Modo seleccionado: Intake único`.
2. Resume el contexto confirmado en términos operativos.
3. Entrega el contenido listo para copiar en la plantilla siguiendo el orden de secciones.
4. Marca como `Pendiente de confirmar` todo dato aplicable sin evidencia.
5. Cierra con vacíos detectados y checklist final.


## Ejemplo de activación

"Ayúdame a dejar operable la documentación de un servicio backend. Si falta contexto, entra en entrevista guiada con pocas preguntas; si alcanza, dame el borrador listo para la plantilla. Si comparto un documento existente, audítalo sin inventar datos y deja explícito qué queda pendiente de confirmar."