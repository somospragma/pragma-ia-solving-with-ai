---
name: documentation-projects
description: Skill para crear, estructurar y mantener documentación de proyectos genérica,  reutilizable y agnóstica al dominio. ACTÍVALO cuando el usuario mencione:documentación, proyecto, especificaciones, arquitectura, requisitos, features,  estructura, flujos de usuario, onboarding, specs, decision records, o cualquier  conversación sobre documentar un proyecto nuevo o existente. USO RECOMENDADO: Usar SIEMPRE que se deba documentar un proyecto nuevo, completar documentación faltante, transformar documentación específica a genérica,  o validar calidad de documentación existente contra estándares.
---

# Skill: Project Documentation Structure

## When to Use This Skill

- Create documentation for new project from scratch
- Analyze and complete existing documentation
- Generate reusable and domain-agnostic templates
- Validate documentation completeness and structure
- Improve documentation organization and clarity
- Standardize documentation across team

---

## Skill Principles

| Principle | Meaning |
|-----------|---------|
| Don't Assume | Ask clarifying questions when details are ambiguous |
| Domain-Agnostic | Works across backend, frontend, mobile, infra, QA, etc. |
| Reusable | Skill itself is generic; outputs use real project data |
| Structured | Each document follows consistent, proven structure |
| Modular | 7 documents are independent but interconnected |
| Flexible | Adapts to project type without losing consistency |

---

## 7 Core Documents

This skill generates or completes:

```
docs/
├── index.md                  Navigation guide and entry point
├── project-overview.md       Vision, goals, problems solved
├── requirements.md           Functional, technical, quality requirements
├── project-structure.md      Architecture and code organization
├── tech-stack.md             Technologies and justifications
├── features.md               Feature specifications
├── implementation.md         Development approach and standards
└── user-flow.md              User and data flows
```

---

## Flujo de Ejecución (Árbol de Decisión)

### PASO 1: Validar Contexto

**Pregunta:** ¿Tenemos claridad sobre el dominio, tipo y alcance del proyecto?

- **SÍ** → Continúa a PASO 2 (Mapeo)
- **NO** → Vuelve a la ENTREVISTA (formula preguntas clarificadoras)

**Preguntas de Clarificación Recomendadas:**
- ¿Cuál es el dominio? (Backend, Frontend, Mobile, Infra, QA, Integración, etc.)
- ¿Es proyecto nuevo o documentación existente a mejorar?
- ¿Qué audiencia principal? (Desarrolladores, arquitectos, DevOps, QA)
- ¿Restricciones de confidencialidad o datos sensibles?

---

### PASO 2: Mapear Documentación Existente

**Ejecuta:** Auditoría binaria usando esta matriz:

```
Matriz de Análisis - Para cada documento:
┌─────────────────────┬────────┬────────────┬──────────┬─────────────┐
│ Documento           │Existe ▼│Contenido ▼ │Genérico ▼│Acción       │
├─────────────────────┼────────┼────────────┼──────────┼─────────────┤
│index.md             │  ?     │    ?       │   ?      │ Investigar  │
│project-overview.md  │  ?     │    ?       │   ?      │ Investigar  │
│requirements.md      │  ?     │    ?       │   ?      │ Investigar  │
│project-structure.md │  ?     │    ?       │   ?      │ Investigar  │
│tech-stack.md        │  ?     │    ?       │   ?      │ Investigar  │
│features.md          │  ?     │    ?       │   ?      │ Investigar  │
│implementation.md    │  ?     │    ?       │   ?      │ Investigar  │
│user-flow.md         │  ?     │    ?       │   ?      │ Investigar  │
└─────────────────────┴────────┴────────────┴──────────┴─────────────┘

Clasificar CONTENIDO como:
  [Completo] Tiene estructura + detalle
  [Parcial] Tiene estructura pero falta detalle (TBD, placeholders)
  [Vacío] Solo headers sin contenido

Clasificar GENERICIDAD como:
  [Genérico] Sin nombres reales, URLs, credenciales, datos específicos
  [Mixto] Contiene algunos datos específicos
  [Específico] Lleno de datos reales que requiere transformación

VALIDACION CRITICA - Edición de Documentación Existente:
  Si el documento ya existe y está incompleto o parcial:
  - NO alteres la estructura existente
  - Complementa el contenido faltante respetando formato y organización actual
  - Adapta recomendaciones del skill al estándar ya establecido
  - Valida que cambios sean coherentes con decisiones arquitectónicas previas
```

---

### PASO 3: Cuestionario Específico (Si falta contenido)

**Para CADA documento faltante o incompleto, formula preguntas:**

#### Si falta `index.md` o está vacío:
```
CUESTIONARIO - INDEX.MD

1. METADATA:
   - ¿Cuál es la última fecha de actualización?
   - ¿Cuál es la versión de la documentación?
   - ¿Quién es el responsable (autor/team)?

2. ESTRUCTURA:
   - ¿Cuál es el orden lógico de lectura? (ej: overview → requirements → structure)
   - ¿Hay guías separadas para diferentes roles? (developers, architects, DevOps)
   - ¿Existen secciones de setup, configuración o prerequisites?

3. NAVEGACIÓN:
   - ¿Cada documento debe tener tabla de contenidos?
   - ¿Links internos entre documentos?
   - ¿Links externos a recursos (wikis, GitHub, etc.)?

PLANTILLA GENÉRICA DE OUTPUT:
---
name: [PROJECT_NAME]
version: 1.0
last_updated: [DATE]
author: [TEAM/PERSON]

## Archivos y sus propósitos

La documentación se organiza en 7 documentos independientes pero interconectados:

### [project-overview.md](project-overview.md)
Contiene la declaración de visión principal, los objetivos principales y una explicación general de lo que el proyecto busca resolver o lograr. Este documento actúa como la guía para todas las demás decisiones.

### [requirements.md](requirements.md)
Desglosa tanto las funciones del sistema (requisitos funcionales como "sistema puede procesar [OPERATION]") como su rendimiento (requisitos técnicos como "latencia p99 < [LATENCY]ms").

### [project-structure.md](project-structure.md)
Describe la estructura del sistema: cómo se conectan y comunican las diferentes partes, cómo se ve la estructura de las capas y cómo fluyen los datos a través de la aplicación.

### [tech-stack.md](tech-stack.md)
Justifica las elecciones tecnológicas, explicando por qué se seleccionaron herramientas, frameworks o lenguajes específicos para las diferentes partes del proyecto y cómo funcionan juntos.

### [features.md](features.md)
Profundiza en las características individuales de la funcionalidad, describiendo exactamente cómo debería funcionar cada una, incluyendo casos extremos y cualquier regla de negocio o requisito de validación específico.

### [implementation.md](implementation.md)
Abarca cómo se construirá el proyecto: el enfoque de desarrollo, los estándares de codificación y las directrices técnicas específicas que el equipo debe seguir.

### [user-flow.md](user-flow.md)
Mapea los flujos funcionales de los usuarios y los datos a través del sistema: una hoja de ruta detallada que muestra cada paso e interacción en la aplicación.

## Documentos Clave
- [project-overview.md] - Visión general
- [requirements.md] - Requisitos funcionales y técnicos
- [project-structure.md] - Arquitectura y estructura
- [tech-stack.md] - Tecnologías seleccionadas
- [features.md] - Funcionalidades detalladas
- [implementation.md] - Guía de desarrollo
- [user-flow.md] - Flujos de usuario y datos

## Guías por Rol
### Para Nuevos Desarrolladores
1. Lee project-overview.md
2. Lee requirements.md y project-structure.md
3. Lee implementation.md y tech-stack.md

### Para Arquitectos/Tech Leads
1. Lee project-overview.md
2. Lee requirements.md
3. Lee project-structure.md y tech-stack.md
---
```

#### Si falta `project-overview.md`:
```
CUESTIONARIO - PROJECT-OVERVIEW.MD

1. VISIÓN:
   - ¿Cuál es el propósito principal del proyecto?
   - ¿Qué capacidad técnica busca habilitar?
   - ¿Cuál es el largo plazo esperado?

2. OBJETIVOS (3-5 principales):
   - ¿Qué debe lograr el proyecto en corto plazo meses 1-3?
   - ¿Qué debe lograr en mediano plazo meses 3-6?
   - ¿Qué debe lograr en largo plazo?

3. PROBLEMAS RESUELTOS:
   - ¿Qué problema técnico aborda?
   - ¿Qué ineficiencias elimina?
   - ¿Qué capacidades nuevas habilita?

4. PRINCIPIOS ARQUITECTÓNICOS:
   - ¿Sigue SOLID, DRY, KISS?
   - ¿Qué patrones de diseño (si aplica)?

PLANTILLA GENÉRICA DE OUTPUT:
---
# [PROJECT_NAME] - Visión General

## Visión
[Descripción agnóstica de qué es el proyecto sin nombres reales]

## Objetivos Principales
1. [Objetivo 1 - en términos técnicos generales]
2. [Objetivo 2]
3. [Objetivo 3]
4. [Objetivo 4]
5. [Objetivo 5]

## Problemas Resueltos
- Problema 1: [Descripción general sin contexto específico]
- Problema 2: [Descripción general sin contexto específico]

## Principios Arquitectónicos
- Single Responsibility: [cómo aplica en este proyecto]
- DRY (Don't Repeat Yourself): [cómo aplica]
---
```

#### Si falta `requirements.md`:
```
CUESTIONARIO - REQUIREMENTS.MD

1. FUNCIONALES (RF):
   - ¿Cuáles son las 3-5 specificaciones funcionales críticas?
   - ¿Cuál es el criterio de aceptación para cada RF?
   - ¿Cuál es la prioridad de cada RF? (CRÍTICA, ALTA, MEDIA)

2. TÉCNICOS (RT):
   - ¿Cuál es el lenguaje principal? [LENGUAJE_PRINCIPAL]
   - ¿Cuáles frameworks? [FRAMEWORKS]
   - ¿Qué requisitos de performance? (latencia, throughput)
   - ¿Qué requisitos de escalabilidad?

3. CALIDAD (RQ):
   - ¿Coverage de tests esperado? (70%, 80%, 90%)
   - ¿Buenas prácticas de código?
   - ¿Documentación de código?
   - ¿Code review process?

4. AMBIENTE (RA):
   - ¿Cuáles ambientes? (DEV, QA, STAGING, PROD)
   - ¿Qué características especiales por ambiente?
   - ¿Restricciones de cada ambiente?

PLANTILLA GENÉRICA DE OUTPUT:
---
# Requirements

## Requisitos Funcionales
### RF-001: [Funcionalidad genérica 1]
**Descripción:** [Descripción sin datos reales]
**Criterios de Aceptación:**
- ✅ [Criterio 1]
- ✅ [Criterio 2]
**Prioridad:** ALTA/CRÍTICA

## Requisitos Técnicos
### RT-001: [Requisito técnico 1]
**Descripción:** [Descripción agnóstica]
**Criterios:** [Criterios técnicos generalizados]
**Prioridad:** CRÍTICA

## Requisitos de Calidad
### RQ-001: [Calidad 1]
**Descripción:** [Descripción genérica]
**Criterios:** [Criterios de calidad]
**Prioridad:**

## Requisitos de Ambiente
### RA-001: [Ambiente 1]
**Descripción:** [Descripción genérica]
**Criterios:** [Criterios técnicos generalizados]
**Prioridad:**
---
```

#### Si falta `project-structure.md`:
```
CUESTIONARIO - PROJECT-STRUCTURE.MD

1. ARQUITECTURA:
   - ¿Qué patrón arquitectónico? (MVC, Hexagonal, Layered, Microservicios)
   - ¿Cómo se organiza el código? (por feature, por layer, híbrido)
   - ¿Cuál es el flujo de datos?

2. CAPAS PRINCIPALES:
   - ¿Cuántas capas principales? (3, 4, 5...)
   - ¿Cuál es el propósito de cada capa?
   - ¿Cómo se comunican entre capas?

3. MÓDULOS:
   - ¿Cuáles son los módulos/packages independientes?
   - ¿Qué responsabilidad tiene cada módulo?
   - ¿Hay utilidades compartidas?

PLANTILLA GENÉRICA DE OUTPUT:
---
# Project Structure

## Patrón Arquitectónico
[PATTERN] es un patrón que proporciona:
- Separación de responsabilidades
- Modularidad
- Facilidad para testing

## Estructura Visual
\`\`\`
[PROJECT_ROOT]/
├── docs/
├── src/
│   ├── main/
│   │   ├── layer-1/      [Descripción agnóstica]
│   │   ├── layer-2/      [Descripción agnóstica]
│   │   └── shared/       [Utilidades compartidas]
│   └── test/
├── config/
└── README.md
\`\`\`

## Principios de Organización
- **Modularidad:** Cada módulo independiente
- **Claridad:** Estructura predecible
- **Escalabilidad:** Fácil agregar nuevos módulos
---
```

#### Si falta `tech-stack.md`:
```
CUESTIONARIO - TECH-STACK.MD

1. LENGUAJE PRINCIPAL:
   - ¿Cuál es el lenguaje base? (Java, Python, Go, TypeScript, etc.)
   - ¿Por qué se eligió este lenguaje?
   - ¿Versión mínima requerida?

2. FRAMEWORKS PRINCIPALES:
   - ¿Cuáles son los frameworks críticos?
   - ¿Cuál es la alternativa descartada y por qué?
   - ¿Cómo se justifica cada selección?

3. HERRAMIENTAS:
   - ¿Build system? (Maven, Gradle, Bazel)
   - ¿Testing frameworks?
   - ¿CI/CD pipelines?
   - ¿Monitoring/Logging?

4. FUTURO:
   - ¿Hay tecnologías en evaluación?
   - ¿Hay planes de actualización conocidos?

PLANTILLA GENÉRICA DE OUTPUT:
---
# Tech Stack

## Lenguaje Principal
**[LANGUAGE_NAME]** v[VERSION]
- Justificación: [Razonamient agnóstico]
- Alternativas consideradas: [Alternatives]

## Frameworks Clave
### [FRAMEWORK_1]
- Propósito: [Descripción agnóstica]
- Versión: [VERSION]
- Justificación: [Razones generales]
- Alternativas: [Frameworks alternativos considerados]

## Herramientas de Desarrollo
| Herramienta | Propósito | Estado |
|-------------|-----------|--------|
| [TOOL_1] | [Purpose] | Activo |
| [TOOL_2] | [Purpose] | Evaluación |

## Decisiones Técnicas Documentadas
[Registrar key decisions sin datos específicos]

---
```

#### Si falta `features.md`:
```
CUESTIONARIO - FEATURES.MD

1. FEATURES PRINCIPALES:
   - ¿Cuáles son las 3-5 features principales?
   - ¿Cómo funciona cada una sin entrar en detalles extensos?
   - ¿Cuál es el flujo de cada feature?

2. CASOS EXTREMOS:
   - ¿Qué casos especiales (edge cases) existen?
   - ¿Cómo se manejan errores?
   - ¿Cuál es el comportamiento en fallo?

3. VALIDACIONES:
   - ¿Qué reglas de negocio se aplican?
   - ¿Qué validaciones deben hacerse?

PLANTILLA GENÉRICA DE OUTPUT:
---
# Features

## [FEATURE_1_NAME]
**Propósito:** [Descripción agnóstica de qué hace]

### Flujo Normal
1. [Paso 1 - sin datos reales]
2. [Paso 2]
3. [Paso 3]

### Casos Extremos
- Caso: [Edge case 1]
  Comportamiento: [Cómo se maneja]
- Caso: [Edge case 2]
  Comportamiento: [Cómo se maneja]

### Validaciones
- ✓ [Validación 1]
- ✓ [Validación 2]

---
```

#### Si falta `implementation.md`:
```
CUESTIONARIO - IMPLEMENTATION.MD

1. PREPARACIÓN:
   - ¿Cuáles son los prerequisites?
   - ¿Qué software se necesita instalar?
   - ¿Cuáles son los pasos de setup?

2. ESTÁNDARES DE CÓDIGO:
   - ¿Convenciones de nombre? (camelCase, snake_case, PascalCase)
   - ¿Formato de código? (indentation, line length)
   - ¿Comentarios y documentación?
   - ¿Tests en cada commit?

3. GIT WORKFLOW:
   - ¿Branching strategy? (git flow, trunk-based)
   - ¿Commit message format? (conventional commits)
   - ¿PR/Code review process?
   - ¿Merge strategy?

4. CI/CD:
   - ¿Qué checks automáticos?
   - ¿Qué tests ejecutan?
   - ¿Qué artifacts se generan?

PLANTILLA GENÉRICA DE OUTPUT:
---
# Implementation Guide

## Preparación del Entorno

### Prerequisites
- [SOFTWARE_1]: [VERSION] o superior
- [SOFTWARE_2]: [VERSION] o superior

### Setup Inicial
\`\`\`bash
# Step 1: [Descripción agnóstica]
[comando genérico]

# Step 2: [Descripción agnóstica]
[comando genérico]
\`\`\`

## Estándares de Codificación

### Convenciones
| Aspecto | Estándar |
|---------|----------|
| Variables | camelCase |
| Clases | PascalCase |
| Constantes | UPPER_SNAKE_CASE |

### Documentación
- Docstrings en función principal
- Comentarios para lógica compleja
- README en cada módulo

## Git Workflow
1. Crear rama: `git checkout -b feature/[FEATURE_NAME]`
2. Commit: `git commit -m "feat([SCOPE]): [description]"`
3. Push: `git push origin feature/[FEATURE_NAME]`
4. PR: Crear Pull Request con descripción

---
```

#### Si falta `user-flow.md`:
```
CUESTIONARIO - USER-FLOW.MD

1. FLUJOS PRINCIPALES:
   - ¿Cuál es el flujo más importante?
   - ¿Cuáles son los pasos del flujo?
   - ¿Cómo fluyen los datos?

2. ACTORES/ROLES:
   - ¿Quién inicia el flujo? (Usuario, Sistema, Evento)
   - ¿Qué permisos se requieren?

3. ALTERNATIVAS:
   - ¿Flujos alternativos o excepciones?
   - ¿Puntos de fallo?

PLANTILLA GENÉRICA DE OUTPUT:
---
# User Flows

## [FLOW_1_NAME]

### Flujo Normal
\`\`\`
Actor: [ROLE/USER_TYPE]
Precondición: [Condición inicial agnóstica]

1. [Paso 1 - sin datos específicos]
2. [Paso 2]
3. [Paso 3]

Postcondición: [Estado final esperado]
\`\`\`

### Flujos Alternativos
**Caso 1:** [Escenario alternativo]
- Pasos: [Steps]
- Resultado: [Result]

## [FLOW_2_NAME]
[Repetir patrón]

---
```

---

### PASO 4: Generar Documentos

**Para CADA documento generado, usa SIEMPRE este formato:**

```markdown
---DOCUMENTO----
Nombre: [Nombre exacto del archivo]
Propósito: [Para qué sirve en 1 línea]

Contenido Genérico:
  [El contenido del documento aquí, con placeholders [PLACEHOLDER]]

Validación de Genericidad:
  [OK] No contiene: credenciales, tokens, paths absolutos
  [OK] Contiene: ejemplos agnósticos
  [OK] Es entendible: alguien fuera del contexto entiende
  [OK] Es reutilizable: aplica para implementarciones similares

Checklist de Contenido:
  [OK] Tiene tabla de contenidos
  [OK] Tiene metadata (fecha, versión, autor)
  [OK] Tiene descripciones claras
  [OK] Tiene ejemplos (si aplica)
  [OK] Tiene referencias a otros documentos (si aplica)
---/DOCUMENTO---
```

---

### PASO 5: Validar y Reportar

**Checklist Final de Completitud:**

```
VALIDACIÓN ANTES DE ENTREGAR:

7 DOCUMENTOS PRINCIPALES:
  [_] index.md - guía de navegación
  [_] project-overview.md - visión y objetivos
  [_] requirements.md - requisitos funcionales y técnicos
  [_] project-structure.md - arquitectura y estructura
  [_] tech-stack.md - tecnologías y justificaciones
  [_] features.md - features y funcionalidades
  [_] implementation.md - guía de desarrollo
  [_] user-flow.md - flujos de usuario y datos

VALIDACIÓN DE CADA DOCUMENTO:
  [_] Estructura: clear markdown headers
  [_] Metadata: fecha, versión, autor
  [_] Genericidad: URLs, nombres, datos reales donde corresponda
  [_] Placeholders: [PLACEHOLDER] donde corresponda
  [_] Referencias: links entre documentos correctos
  [_] Claridad: entendible sin contexto externo

VALIDACIÓN DE CONTENIDO:
  [_] Cero TBD no resueltos (o documentados por qué faltan)
  [_] Todos los ejemplos son genéricos
  [_] Uso mínimo de emoticons (solo para alertas o énfasis, no en contenido principal)

ENTREGABLES:
  [_] 7 archivos .md generados
  [_] Cada archivo tiene VALIDACIÓN de genericidad
  [_] REPORTE FINAL generado (FASE 5)
  [_] Cuestionamientos sin respuesta documentados
```

---

## Patrones por Dominio

### Si es Backend (Microservicios / Monolito / APIs)
Enfatiza:
- Arquitectura de capas (Controller → Service → Repository)
- REST APIs y endpoints (genéricos como `[HTTP_METHOD] /[RESOURCE_PATH]`)
- Bases de datos (`[DATABASE_TYPE]`)
- Autenticación y autorización

📝 Ejemplos Genéricos en tech-stack:
- Language: `[PRIMARY_LANGUAGE]` (e.g., Java, Python, Go)
- Frameworks: `[WEB_FRAMEWORK]`, `[ORM_FRAMEWORK]`
- Database: `[DATABASE_TYPE]` (SQL/NoSQL)
- Authentication: `[AUTH_METHOD]` (JWT, OAuth, etc.)

### Si es Frontend (SPA / PWA / Web)
Enfatiza:
- Componentes y composición
- Estado management (`[STATE_MANAGEMENT_SOLUTION]`)
- Flujos de usuario UI
- Responsive design

📝 Ejemplos Genéricos en tech-stack:
- Framework: `[UI_FRAMEWORK]` (React, Vue, Angular)
- State: `[STATE_MANAGER]` (Redux, Vuex, Context)
- Build: `[BUILD_TOOL]` (Webpack, Vite, etc.)

### Si es Mobile (Native / Cross-platform / Flutter)
Enfatiza:
- Plataformas (iOS/Android/ambas)
- Ciclo de vida de app
- Integración con APIs backend
- Permisos y lifecycle

📝 Ejemplos Genéricos en tech-stack:
- Framework: `[MOBILE_FRAMEWORK]` (Flutter, React Native, Swift)
- Plataformas: `[PLATFORM_1]`, `[PLATFORM_2]`
- Build system: `[BUILD_SYSTEM]`
- Testing: `[TESTING_FRAMEWORK]`

### Si es QA / Testing Automation
Enfatiza:
- Frameworks de testing (`[TEST_FRAMEWORK]`)
- Estrategia de cobertura
- Tipos de tests (unitarios, integración, E2E)
- CI/CD de pruebas

📝 Ejemplos Genéricos en tech-stack:
- Language: `[AUTOMATION_LANGUAGE]` (Java, Python, JavaScript)
- Framework: `[TEST_FRAMEWORK]` (JUnit, Pytest, Jest, Cypress)
- Reporting: `[REPORTING_TOOL]`
- Coverage target: `[COVERAGE_PERCENTAGE]`

### Si es Infraestructura (DevOps / CloudOps)
Enfatiza:
- Provisioning (`[IaC_TOOL]`)
- Deployment (`[CONTAINER_TECH]`)
- Monitoring y observabilidad
- Seguridad y compliance

📝 Ejemplos Genéricos en tech-stack:
- Cloud: `[CLOUD_PROVIDER]` (AWS, GCP, Azure)
- IaC: `[IaC_TOOL]` (Terraform, CloudFormation)
- Containers: `[CONTAINER_TECH]` (Docker, Kubernetes)
- Monitoring: `[MONITORING_TOOL]`

---

## Validaciones Integradas en Cada Paso

| Fase | Validación | Criterios |
|------|-----------|-----------|
| **PASO 1** | Contexto claro | ¿Conocemos dominio, tipo, audiencia? |
| **PASO 2** | Auditoría completada | ¿Matriz de análisis rellena 100%? |
| **PASO 3** | Cuestionamientos | ¿Formuladas todas las preguntas críticas? |
| **PASO 4** | Documentos generados | ¿Cada doc tiene validación de genericidad? |
| **PASO 5** | Checklist final | ¿Pasan todas las validaciones de contenido? |

---

## 🎯 Indicadores de Éxito de Este Skill

✅ **El resultado ES exitoso si:**
- ✓ Genera 7 documentos con estructura clara
- ✓ Documentos son reutilizables en otros proyectos similares
- ✓ Preguntas sin respuesta documentadas explícitamente
- ✓ Cada documento tiene validación de genericidad

❌ **El resultado NO es exitoso si:**
- ✗ Contiene credenciales o datos sensibles
- ✗ Tiene TBDs sin documentar por qué faltan
- ✗ Falta alguno de los 7 documentos sin justificación

---

## Referencias y Recursos Asociados

Este skill genera recursos mediante:

1. **SKILL.md** (este archivo)
   - Instrucciones completas del flujo
   - Plantillas genéricas para cada documento
   - Cuestionarios para cada sección

2. **referenced-template/** (opcional, para ampliar)
   - Templates detalladas por dominio
   - Ejemplos paso a paso
   - Checklists interactivos

3. **scripts/** (opcional, para automatizar)
   - Validador de genericidad
   - Generador de matriz de análisis
   - Checker de TBDs no resueltos

---

## Próximos Pasos Recomendados

Después de ejecutar este skill:

1. Ejecuta FASE 5 (REPORTE FINAL) para documentar completitud
2. Revisa cada documento generado con equipo
3. Completa TBDs documentados en cuestionamientos
4. Valida genericidad contra datos reales del proyecto
5. Usa documentos como referencia para nuevos proyectos
6. Itera y mejora plantillas según feedback del equipo
