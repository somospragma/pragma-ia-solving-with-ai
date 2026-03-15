---
name: "specs-driven"
description: "How to use Spec-Driven Development to specify new features. Make sure to use this skill whenever the user asks to specify a feature, write requirements, create a technical design document, or break down tasks for a new feature. This skill guides you through creating requirements.md, design.md, and tasks.md sequentially, with human approval gates."
---

# Pragma IA — Específicación de Funcionalidades (Specs Skill)

Esta skill te enseña cómo estructurar las funcionalidades usando el flujo de Spec-Driven Development (SDD) de Pragma.

El objetivo fundamental del Spec-Driven Development es alinear la visión técnica y funcional con el usuario antes de escribir una sola línea de código. Empezar a programar o diseñar prematuramente suele resultar en re-trabajos costosos. Por esta razón, el flujo está dividido en 3 fases secuenciales, y es vital que te detengas a confirmar con el usuario al final de cada fase para asegurar que vamos en la dirección correcta.

## Cuándo usar esta skill
Úsala siempre que:
- El usuario te pida desarrollar o especificar una nueva funcionalidad.
- El usuario te pida que le ayudes a definir una nueva funcionalidad.
- El usuario te pida crear requerimientos para una nueva feature.
- El usuario te pida delinear el diseño (arquitectura) de una feature antes de programarla.
- El usuario te solicite dividir una funcionalidad en micro-tareas o checklists dentro de `.specs/`.

## El Flujo de Trabajo Secuencial

Para cada nueva feature, crea una carpeta en `.specs/{feature_name}/`. Procede fase por fase, y espera la retroalimentación del usuario antes de avanzar a la siguiente.

### Fase 1: Requerimientos funcionales (`requirements.md`)

En esta fase, el objetivo es entender qué vamos a construir y sus restricciones.
1. Copia la plantilla de requerimientos desde tus recursos empaquetados (`assets/requirements.md`) al nuevo destino: `cp assets/requirements.md .specs/{feature_name}/requirements.md`
2. Si el nombre de la feature no está claro, propón uno en snake_case (ej: `login_jwt`) y crea la carpeta correspondiente `.specs/{feature_name}/`.
3. Conversa con el usuario para determinar los RF (Requerimientos Funcionales) y los RNF (Requerimientos No Funcionales).
4. Completa y reemplaza el contenido dentro de `.specs/{feature_name}/requirements.md` utilizando las herramientas de edición de archivos, asegurándote de no perder la estructura existente.
5. **Gate de Aprobación:** Detente aquí. Notifica al usuario que los requerimientos están listos para revisión. Al pedir su aprobación, evitamos diseñar una arquitectura para requerimientos incorrectos.

### Fase 2: Diseño y Arquitectura (`design.md`)

Una vez que el usuario confirma que los requerimientos son correctos, pasamos a decidir cómo lo vamos a construir.
1. Copia la plantilla de diseño desde tus recursos empaquetados (`assets/design.md`) al nuevo destino: `cp assets/design.md .specs/{feature_name}/design.md`
2. Investiga el código base para entender los impactos técnicos (Backend, Frontend, etc.).
3. Completa y reemplaza el contenido de `.specs/{feature_name}/design.md` documentando las decisiones técnicas, diagramas (si aplican) y la lista de archivos afectados.
4. **Gate de Aprobación:** Detente aquí. Pide al usuario que revise el diseño. Esto permite corregir el enfoque técnico antes de crear el checklist de ejecución (tareas).

### Fase 3: Tareas de Ejecución (`tasks.md`)

Cuando el diseño arquitectónico está aprobado, lo traducimos a pasos ejecutables.
1. Copia la plantilla de tareas desde tus recursos empaquetados (`assets/tasks.md`) al nuevo destino: `cp assets/tasks.md .specs/{feature_name}/tasks.md`
2. Convierte el diseño técnico en una lista de micro-tareas accionables y atómicas y agrégalas a `.specs/{feature_name}/tasks.md`. Usa un formato de checklist (`- [ ]`) y mantén la sección de Validación Final de la plantilla.
3. Informa al usuario que el plan de tareas está listo, y pregunta si desea empezar a ejecutar la primera tarea.

## Ejemplo Práctico

**Input del usuario:** "Quiero preparar las especificaciones para un sistema de referidos en la app."

**Tu flujo de pensamiento y respuesta:**
Como el usuario quiere especificar una funcionalidad, debo aplicar el flujo SDD. Empezaré únicamente con la Fase 1. Para ello leeré la plantilla de requirements y redactaré un borrador.

*Respuesta:* "¡Claro! Empecemos con la Fase 1 de Requerimientos. He creado el documento inicial en `.specs/sistema_referidos/requirements.md`. Por favor revísalo, dime si falta alguna regla de negocio, y cuando lo apruebes, pasaré a redactar el diseño arquitectónico."

---
El éxito de este proceso radica en la colaboración paso a paso. Recuerda siempre explicarle al usuario qué fase has completado y esperar su luz verde para continuar.
