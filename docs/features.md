# Pragma IA - Features

## Feature 1: Instrucciones Personalizadas por Dominio

**Propósito:** Permitir crear instrucciones base que personalicen el comportamiento de asistentes de IA para dominios técnicos específicos.

### Flujo Normal
1. Usuario accede a instrucciones_or_rules/[dominio]/
2. Descubre instrucción relevante para su tecnología (Backend Java, React Frontend, Flutter Mobile, etc.)
3. Copia instrucción completa a su configuración personal
4. Asistente de IA usa la instrucción como base para todas las respuestas
5. Usuario experimenta mejoras en relevancia y calidad de sugerencias

### Casos Extremos
- **Caso:** Usuario necesita instrucción que no existe
  Comportamiento: Consulta _estandar-instructions/ para ver plantilla y puede crear una nueva contribuyendo al repositorio
  
- **Caso:** Usuario trabaja en múltiples tecnologías
  Comportamiento: Puede combinar instrucciones o crear orquestaciones usando instructions-orchestrator-template

- **Caso:** Instrucción es obsoleta (tecnología deprecada)
  Comportamiento: Archivo marcado como [deprecated] con referencia a reemplazo sugerido

### Validaciones
- Toda instrucción debe tener: nombre, descripción, versión, dominio
- La instrucción debe ser agnóstica a la herramienta (Copilot, Amazon Q, etc.)
- Deben incluir al menos 1 ejemplo de uso
- No deben tener TBD sin documentar

---

## Feature 2: Prompts Reutilizables para Tareas Específicas

**Propósito:** Centralizar prompts efectivos para tareas comunes (crear tests, generar documentación, revisar código, etc.) que usuarios puedan copiar y adaptar.

### Flujo Normal
1. Usuario enfrenta tarea específica (ej: "generar tests unitarios para un micro-servicio Java")
2. Busca en prompts/backend/java/ o prompts/qa-testing/test_automation/
3. Encuentra prompt relevante (ej: "backend_java_test_archunit.md")
4. Copia el prompt y lo adapta a su contexto específico
5. Lo envía al asistente de IA en el chat
6. Obtiene respuesta que mejora significativamente con el prompt especializado

### Casos Extremos
- **Caso:** Usuario necesita combinar múltiples prompts
  Comportamiento: Lee guía en transversal/pro_tips-prompt.md sobre composición de prompts
  
- **Caso:** Resultado de prompt no es el esperado
  Comportamiento: Puede mejorar el prompt y contribuir versión mejorada

- **Caso:** Prompt aplica a múltiples dominios
  Comportamiento: Copiado en transversal/ con referencias a especializaciones por dominio

### Validaciones
- Cada prompt debe resolver un problema específico
- Títulos y descripciones deben ser claros sobre qué hace
- Debe incluir contexto: "cuando usar esto"
- Deben incluir ejemplos de entrada/salida esperada

---

## Feature 3: Recursos Reutilizables vía MCP

**Propósito:** Exponer plantillas, ejemplos y guías mediante Pragma MCP para que asistentes puedan acceder sin copy/paste manual.

### Flujo Normal
1. Usuario en chat dice "dame un ejemplo de..." 
2. Asistente activa MCP y consulta recursos/ disponibles
3. Resourcese relevante se carga automáticamente en contexto
4. Asistente genera respuesta usando el recurso como base
5. Usuario recibe respuesta mejorada con ejemplos precisos

### Casos Extremos
- **Caso:** Usuario solicita recurso que no existe
  Comportamiento: Asistente sugiere recurso similar o recomienda crear uno nuevo
  
- **Caso:** Recurso es muy grande
  Comportamiento: MCP retorna resumen + link para versión completa

- **Caso:** Múltiples versiones de recurso (deprecated vs new)
  Comportamiento: MCP retorna versión stable, marca deprecated

### Validaciones
- Todos los recursos deben tener descripción clara (metadata)
- Deben ser formatos estándar (Markdown, JSON, código válido)
- Deben incluir contexto de cuándo aplican
- No deben depender de referencias externas para ser útiles

---

## Feature 4: Chatmodes Personalizados (GitHub Copilot)

**Propósito:** Definir comportamientos específicos de GitHub Copilot para contextos particulares (code review, crear documentación, diseño arquitectónico, etc.).

### Flujo Normal
1. Usuario abre GitHub Copilot en VS Code
2. Selecciona chatmode personalizado (@chatmode-design-review, @chatmode-testing, etc.)
3. Copilot carga configuración que define:
   - Herramientas disponibles (codebase search, reference docs, etc.)
   - Límites de comportamiento (foco solo en seguridad, performance, etc.)
   - Contexto disponible (solo tests, docstrings, etc.)
4. Usuario mantiene conversación en el contexto limitado
5. Respuestas son más enfocadas porque el chatmode define límites

### Casos Extremos
- **Caso:** Usuario necesita salir del chatmode
  Comportamiento: Puede volver a chat normal o seleccionar otro chatmode
  
- **Caso:** Chatmode no tiene herramienta que necesita
  Comportamiento: Solicitud sale del chatmode y se maneja en chat normal

- **Caso:** Nuevo contexto emerge durante conversación
  Comportamiento: Usuario puede cambiar de chatmode sin perder historial

### Validaciones
- Debe tener descripción clara de propósito
- Metadata clara (nombre, versión, dominio)
- Herramientas deben ser válidas en Copilot
- Límites deben ser claros (qué está fuera del scope)

---


## Feature 5: Documentación Centralizada

**Propósito:** Proporcionar guía completa sobre el uso y contribución al repositorio.

### Flujo Normal
1. Nuevo usuario consulta docs/index.md
2. Navega a documento relevante (project-overview, implementation, etc.)
3. Encuentra respuestas a cómo usar, contribuir, entender decisiones
4. Puede explorar en profundidad detalles específicos
5. Entiende política de contribución y estándares

### Casos Extremos
- **Caso:** Usuario busca documentación que no existe
  Comportamiento: README.md indica dónde solicitar mejora
  
- **Caso:** Documentación está desactualizada
  Comportamiento: Marca [OUTDATED] y proporciona link a versión correcta

### Validaciones
- Documentación debe estar actualizada (verificada en cada release)
- Links deben ser válidos
- Debe cubrir: propósito, estructura, cómo contribuir, ejemplos

## Feature 6: Skills Reutilizables

**Propósito:** Encapsular procesos complejos (crear característica completa, documentar proyecto, validar código) como skills que pueden ser consultados o invocados.

### Flujo Normal
1. Usuario necesita realizar tarea compleja (ej: "crear documentación de proyecto")
2. Descubre skill en ./instructions_or_rules/**/skills (ej: documentation-projects)
3. Consulta SKILL.md
4. Sigue el flujo paso a paso
5. Asistente entiende el skill y proporciona asistencia contextualizada a cada paso
6. Resultado es una salida de calidad que sigue estándares

### Casos Extremos
- **Caso:** Usuario quiere modificar un skill
  Comportamiento: Puede crear una versión adaptada en su rama local

- **Caso:** Skill está deprecado
  Comportamiento: Documentación marca versión nueva o alternativa

### Validaciones
- Debe tener SKILL.md con estructura clara
- Descripciones deben ser claros sobre cuándo usar cada skill
- Cada skill debe resolver un dominio específico

---