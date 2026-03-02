# Pragma IA - Requisitos

## Requisitos Funcionales

### RF-001: Almacenar y Organizar Instrucciones Personalizadas
**Descripción:** El sistema debe permitir crear, almacenar y organizar instrucciones personalizadas por dominio (Backend, Frontend, Mobile, DevOps, QA, Arquitectura e Integración).

**Criterios de Aceptación:**
- Permite crear instrucciones nuevas siguiendo un formato estándar
- Las instrucciones se organizan por carpeta según capítulo (backend, frontend, mobile, etc.)
- Cada instrucción incluye metadata: nombre, descripción, versión
- Las instrucciones son agnósticas a la herramienta (Copilot, Amazon Q, etc.)

**Prioridad:** CRÍTICA

### RF-002: Gestionar Prompts Reutilizables
**Descripción:** El sistema debe permitir crear y organizar prompts reutilizables para tareas específicas.

**Criterios de Aceptación:**
- Prompts se almacenan en una estructura clara por dominio
- Cada prompt es independiente y apunta a solucionar un problema específico
- Incluye ejemplos de uso y variaciones esperadas
- Permite búsqueda y catalogación

**Prioridad:** CRÍTICA

### RF-003: Mantener Recursos Reutilizables
**Descripción:** El sistema debe centralizar recursos (plantillas, ejemplos, guías) que puedan ser invocados desde asistentes de IA.

**Criterios de Aceptación:**
- Recursos disponibles por MCP (Model Context Protocol)
- Cada recurso tiene descripción y propósito claro
- Soporta múltiples formatos (markdown, JSON, código, etc.)

**Prioridad:** ALTA

### RF-004: Proporcionar Chatmodes Personalizados
**Descripción:** El sistema debe permitir definir chatmodes que controlen el comportamiento de GitHub Copilot.

**Criterios de Aceptación:**
- Chatmodes definen herramientas disponibles para cada contexto
- Cada chatmode documenta su propósito y límites
- Compatible con sintaxis de GitHub Copilot

**Prioridad:** MEDIA

---

## Requisitos Técnicos

### RT-001: Formato de Archivos
**Descripción:** Todos los artefactos deben ser almacenados en formatos de texto plano legibles (Markdown, YAML, JSON).

**Criterios:** 
- [Markdown] para instrucciones y guías
- [JSON] para configuraciones y chatmodes
- [YAML] para metadata y definiciones
- [TXT] para contenido simple

**Prioridad:** CRÍTICA

### RT-002: Estructura de Carpetas
**Descripción:** El repositorio debe mantener una estructura clara y predecible.

**Criterios:** 
- Carpetas principales: instructions_or_rules/, prompts/, chatmodes/, resources/
- Subcarpetas por dominio: backend/, frontend/, mobile/, devsecops/, cloudops/, etc.
- Cada dominio puede tener subcarpetas adicionales (cross-cutting/, skills/, etc.)

**Prioridad:** CRÍTICA

### RT-003: Versionamiento
**Descripción:** Los artefactos deben permitir rastrear cambios y versiones.

**Criterios:** 
- Git como sistema de control de versiones
- CHANGELOG.md documenta cambios principales
- Cada artefacto importante incluye versionamiento en su metadata

**Prioridad:** ALTA

### RT-004: Compatibilidad Multi-herramienta
**Descripción:** Los artefactos deben ser compatibles con múltiples asistentes de IA.

**Criterios:** 
- Formato agnóstico: instrucciones sin sintaxis específica de Copilot
- Documentación clara de compatibilidad si existe limitación
- Ejemplos para herramientas populares

**Prioridad:** ALTA

---

## Requisitos de Calidad

### RQ-001: Claridad y Documentación
**Descripción:** Cada artefacto debe incluir documentación clara sobre su propósito y uso.

**Criterios:**
- Descripción clara en la metadata
- Ejemplos de uso cuando aplican
- Casos de uso específicos documentados
- No hay ambigüedades

**Prioridad:** CRÍTICA

### RQ-002: Precisión Técnica
**Descripción:** El contenido técnico debe ser preciso y actualizado.

**Criterios:**
- Código de ejemplo es válido y ejecutable
- Referencias a tecnologías son actuales
- Principios arquitectónicos son sólidos

**Prioridad:** CRÍTICA

### RQ-003: Reutilización y No-Duplicación
**Descripción:** Los artefactos deben ser reutilizables y evitar duplicación.

**Criterios:**
- Principio DRY aplicado
- No hay instrucciones similares duplicadas
- Plantillas base evitan repetición

**Prioridad:** ALTA

### RQ-004: Mantenimiento
**Descripción:** El repositorio debe ser fácil de mantener y evolucionar.

**Criterios:**
- Estructura predecible
- Documentación de cómo agregar nuevos artefactos
- Review process claro

**Prioridad:** ALTA

---

## Requisitos de Ambiente

| Ambiente | Características |
|----------|-----------------|
| **DEV** | Rama local, archivos sin revisar, experimentos |
| **STAGING** | Branch de desarrollo, PRs en revisión, cambios candidatos |
| **PROD** | Main branch, artefactos revisados y aprobados, documentación completa |

