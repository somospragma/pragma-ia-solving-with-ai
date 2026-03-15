# Pragma IA - Flujos de Usuario

## Flujo 1: Usar Instrucciones Personalizadas en GitHub Copilot

### Precondiciones
- Usuario tiene GitHub Copilot instalado en VS Code
- Usuario conoce su dominio técnico principal (Backend Java, React, Flutter, etc.)

### Flujo Principal

```
Inicio
  ↓
1. Usuario enfrenta proyecto nuevo o cambio de tecnología
  ↓
2. Abre navegador → va a: https://github.com/somospragma/pragma-ia-solving-with-ai
  ↓
3. Navega a: instructions_or_rules/[dominio]/
   - Backend Java? → instructions_or_rules/backend/java/
   - Frontend React? → instructions_or_rules/frontend/modular/
   - Mobile Flutter? → instructions_or_rules/mobile/skills/
  ↓
4. Identifica instrucción relevante (ej: backend-spring-boot-patterns.md)
  ↓
5. Lee descripción y valida que es lo que necesita
  ↓
6. Copia instrucción completa
  ↓
7. Abre GitHub Copilot settings en VS Code
   - Settings → Extensions → GitHub Copilot → Prompt
  ↓
8. Pega instrucción en el textarea de "Custom Instructions"
  ↓
9. Abre chat de Copilot (Ctrl+Shift+I) y comienza a usar
  ↓
10. Copilot ahora sugiere siguiendo pautas de la instrucción
  ↓
Fin: Mejor asistencia contextualizada
```

### Flujos Alternativos

**Caso A: Instrucción no existe para su tecnología**
- Usuario busca en _estandar-instructions/ para ver plantilla
- Crea versión personalizada en rama local
- (Opcional) Contribuye versión mejorada al repositorio

**Caso B: Usuario necesita instrucción combinada (múltiples tecnologías)**
- Consulta instructions-orchestrator-template.md
- Combina instrucciones base creando instrucción personalizada
- Ajusta prioridades y énfasis según necesidad

**Caso C: Instrucción se vuelve obsoleta (tecnología deprecada)**
- Archivo marcado con status: deprecated
- Referencia a instrucción replacement sugerida
- Usuario actualiza a versión más reciente

---

## Flujo 2: Crear Prompt Especializado para Tarea Específica

### Precondiciones
- Usuario está en chat de Copilot o ChatGPT
- Usuario tiene tarea técnica específica

### Flujo Principal

```
Inicio
  ↓
1. Usuario enfrenta tarea específica específica
   Ejemplos: "generar tests unitarios", "crear documentación", "revisar código"
  ↓
2. Piensa: "¿existe un prompt para esto?"
  ↓
3. Abre Pragma IA → prompts/[dominio]/[tipo]/
   - Tests Java? → prompts/backend/java/test_*.md
   - Testing E2E? → prompts/qa-testing/test_automation/
   - Documentación API? → prompts/arquitectura/ o prompts/integracion/
  ↓
4. Lee lista de prompts disponibles en dominio
  ↓
5. Abre prompt que mejor se ajusta (ej: "qa-testing-e2e-automation.md")
  ↓
6. Lee descripción: "Cuándo usar esto", "Qué esperar"
  ↓
7. Copia el prompt completo
  ↓
8. Va al chat y pega el prompt
  ↓
9. Escribe su contexto específico después del prompt
  ↓
10. Envía mensaje
  ↓
11. Obtiene respuesta muy mejorada comparado a pedir sin prompt
  ↓
Fin: Tarea completada con calidad superior
```

### Flujos Alternativos

**Caso A: Prompt no existe para tarea específica**
- Usuario lee transversal/pro_tips-prompt.md
- Compone su propio prompt combinando elementos de prompts existentes
- (Opcional) Contribuye prompt mejorado al repo

**Caso B: Prompt necesita adaptación al contexto del usuario**
- Lee secciones de "Customización" si existen
- Modifica partes genéricas con su contexto específico
- Preserva estructura y lógica base del prompt

**Caso C: Resultado no es satisfactorio**
- Usuario itera sobre prompt ajustando criterios
- Documenta iteración que funcionó
- (Opcional) Sube mejora o feedback al repositorio

---

## Flujo 3: Descubrir y Usar Resources vía MCP

### Precondiciones
- Usuario tiene Pragma MCP configurado (ver tech-stack)
- Usuario está en chat con GitHub Copilot o asistente con MCP

### Flujo Principal

```
Inicio
  ↓
1. Usuario necesita template, ejemplo o guía
  ↓
2. Pide en chat: "Dame un ejemplo de [cosa]" o "Necesito template para [caso]"
  ↓
3. Asistente activa MCP y consulta carpeta resources/
  ↓
4. MCP busca en:
   - resources/[dominio]/[tipo]/
   - resources/transversal/ (si aplica globalmente)
  ↓
5. Retorna resource más relevante (metadata + contenido)
  ↓
6. Asistente incorpora resource como contexto en su respuesta
  ↓
7. Usuario recibe respuesta enriquecida con template/ejemplo preciso
  ↓
8. Copia y adapta resource a su proyecto
  ↓
Fin: Solución rápida basada en template probado
```

### Flujos Alternativos

**Caso A: Multiple recursos aplicables**
- MCP retorna resumen de opciones
- Usuario selecciona cuál usar
- Asistente carga resource selectivo

**Caso B: Resource no existe**
- Asistente sugiere resource similar disponible
- O sugiere crear nuevo resource
- Proporciona link a guía de contribución

**Caso C: Resource es muy grande**
- MCP retorna índice + resumen
- Usuario puede solicitar sección específica
- O recurre a documento completo en repo

---

## Flujo 4: Usar Chatmode Personalizado en GitHub Copilot

### Precondiciones
- Usuario tiene chatmode personalizado configurado
- Chatmode define contexto/herramientas específicas

### Flujo Principal

```
Inicio
  ↓
1. Usuario abre GitHub Copilot en VS Code
  ↓
2. Ve opciones de chatmodes en dropdown
   - @design-review
   - @security-audit
   - @testing-strategy
   - @documentation
  ↓
3. Selecciona chatmode relevante
   Ejemplo: Está haciendo code review → Selecciona @design-review
  ↓
4. Copilot carga configuración del chatmode
   - Define herramientas disponibles (code search, docs, etc.)
   - Define límites (enfoque solo en arquitectura, por ej)
   - Define contexto (solo analizar tests, por ej)
  ↓
5. Usuario hace preguntas dentro del contexto
  ↓
6. Copilot mantiene respuestas enfocadas dentro de límites
  ↓
7. Si usuario necesita salir del contexto, cambia de chatmode o vuelve a chat normal
  ↓
Fin: Conversación estructurada y enfocada
```

### Flujos Alternativos

**Caso A: Chatmode no tiene herramienta que necesita**
- Usuario solicita que Copilot active esa herramienta
- Respuesta sale del chatmode pero integra información
- O usuario cambia a chat normal

**Caso B: Necesidad transversal (cruza múltiples chatmodes)**
- Usuario puede cambiar entre chatmodes en una conversación
- Historial se mantiene
- Contexto se adapta al nuevo chatmode

**Caso C: Chatmode es muy restrictivo**
- Usuario puede crear nuevo chatmode personalizado
- O solicitar expansión de chatmode existente
- Contribuye versión mejorada en chatmodes/

---

## Flujo 5: Contribuir Nuevo Artefacto

### Precondiciones
- Usuario tiene fork del repositorio
- Usuario ha creado rama feature (ver implementation.md)

### Flujo Principal

```
Inicio
  ↓
1. Usuario tiene artefacto nuevo (instrucción, prompt, resource, etc.)
  ↓
2. Valida contra estándares (metadata, documentación, ejemplos)
  ↓
3. Coloca en carpeta correcta:
   - Instrucción nueva? → instructions_or_rules/[dominio]/
   - Prompt nuevo? → prompts/[dominio]/
   - Resource? → resources/[dominio]/
   - Chatmode? → chatmodes/
   - Skill? → skills/
  ↓
4. Nombra archivo en snake_case
  ↓
5. Documentación del cambio o uso:
   ./docs/[DOCUMENT.md]
  ↓
6. Hace commit con mensaje convencional
   git commit -m "feat(backend): agregar patrón [nombre]"
  ↓
7. Push a rama feature
   git push origin feature/[tipo]/[nombre]
  ↓
8. Abre Pull Request contra rama develop
   - Llena template PR
   - Describe qué se agregó y por qué
   - Solicita reviewers
  ↓
9. Responde comentarios de review
  ↓
10. Tras aprobación, PR se mergea a develop
  ↓
11. En próximo release, develop se mergea a main
  ↓
Fin: Artefacto visible para toda la comunidad
```

### Flujos Alternativos

**Caso A: Cambios solicitados en review**
- Usuario no termina review para si está completo
- Continúa iterando hasta aprobación

**Caso B: Conflicto de merge durante review**
- Usuario sincroniza su rama con develop
- Resuelve conflictos localmente
- Re-pushea cambios resueltos

**Caso C: Artefacto aplica a múltiples dominios**
- Ubicar en transversal/ con referencias a especializaciones
- O duplicar en dominios relevantes con referencias cruzadas

---

## Flujo 6: Ejecutar Skill Complejo (Ej: Documentar Proyecto)

### Precondiciones
- Usuario tiene proyecto que necesita ser documentado
- Usuario conoce el skill (ej: documentation-projects)

### Flujo Principal

```
Inicio
  ↓
1. Usuario necesita documentación para proyecto
  ↓
2. Descubre skill: instructions_or_rules/[dominio]/skills/[skill-name]
   Ejemplo: instructions_or_rules/mobile/skills/cross-cutting/documentation-projects
  ↓
3. Lee SKILL.md
  ↓
4. En cada paso, interactúa con agente para:
   - Clarificar ambigüedades
   - Responder preguntas del skill
   - Validar resultados
  ↓
5. Obtiene documentación completa de 7 documentos
  ↓
6. Revisa calidad y hace ajustes según feedback
  ↓
Fin: Documentación de proyecto lista y validada
```

### Flujos Alternativos

**Caso A: Skill no se ajusta exactamente a necesidad**
- Usuario evalua para mejorar o derivar skill
- Crea versión personalizada
- Contribuye versión mejorada

---
