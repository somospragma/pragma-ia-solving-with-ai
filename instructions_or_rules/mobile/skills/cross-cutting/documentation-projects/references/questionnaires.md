# Cuestionarios y Plantillas por Documento

Este archivo contiene los cuestionarios detallados para entrevistar al usuario (PASO 3 del flujo)
y las plantillas genéricas de output para cada uno de los 7 documentos base.

Carga este archivo cuando identifiques que un documento está faltante o incompleto.

---

## index.md — Cuestionario

```
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
```

### Plantilla index.md

```markdown
---
name: [PROJECT_NAME]
version: 1.0
last_updated: [DATE]
author: [TEAM/PERSON]
---

## Archivos y sus propósitos

| Documento | Propósito |
|-----------|-----------|
| [project-overview.md](project-overview.md) | Visión, objetivos y problemas resueltos |
| [requirements.md](requirements.md) | Requisitos funcionales, técnicos y de calidad |
| [project-structure.md](project-structure.md) | Arquitectura y estructura de código |
| [tech-stack.md](tech-stack.md) | Tecnologías seleccionadas con justificación |
| [features.md](features.md) | Especificación de funcionalidades |
| [implementation.md](implementation.md) | Guía de desarrollo y estándares |
| [user-flow.md](user-flow.md) | Flujos de usuario y de datos |

## Guías por Rol

### Para Nuevos Desarrolladores
1. Lee project-overview.md
2. Lee requirements.md y project-structure.md
3. Lee implementation.md y tech-stack.md

### Para Arquitectos/Tech Leads
1. Lee project-overview.md
2. Lee requirements.md
3. Lee project-structure.md y tech-stack.md

### Para DevOps / SRE
1. Lee tech-stack.md
2. Lee implementation.md
3. Lee user-flow.md
```

---

## project-overview.md — Cuestionario

```
1. VISIÓN:
   - ¿Cuál es el propósito principal del proyecto?
   - ¿Qué capacidad técnica busca habilitar?
   - ¿Cuál es el largo plazo esperado?

2. OBJETIVOS (3-5 principales):
   - ¿Qué debe lograr en corto plazo (meses 1-3)?
   - ¿Qué debe lograr en mediano plazo (meses 3-6)?
   - ¿Qué debe lograr en largo plazo?

3. PROBLEMAS RESUELTOS:
   - ¿Qué problema técnico aborda?
   - ¿Qué ineficiencias elimina?
   - ¿Qué capacidades nuevas habilita?

4. PRINCIPIOS ARQUITECTÓNICOS:
   - ¿Sigue SOLID, DRY, KISS?
   - ¿Qué patrones de diseño (si aplica)?
```

### Plantilla project-overview.md

```markdown
# [PROJECT_NAME] - Visión General

## Visión
[Descripción de qué hace el proyecto y qué valor aporta]

## Objetivos Principales
1. [Objetivo 1 - corto plazo]
2. [Objetivo 2 - mediano plazo]
3. [Objetivo 3 - largo plazo]
4. [Objetivo 4]
5. [Objetivo 5]

## Problemas Resueltos
- **[Problema 1]:** [Descripción del problema y cómo se resuelve]
- **[Problema 2]:** [Descripción del problema y cómo se resuelve]

## Principios Arquitectónicos
- **Single Responsibility:** [cómo aplica en este proyecto]
- **DRY (Don't Repeat Yourself):** [cómo aplica]
- **[Otro principio relevante]:** [cómo aplica]
```

---

## requirements.md — Cuestionario

```
1. FUNCIONALES (RF):
   - ¿Cuáles son las 3-5 especificaciones funcionales críticas?
   - ¿Cuál es el criterio de aceptación para cada RF?
   - ¿Cuál es la prioridad de cada RF? (CRÍTICA, ALTA, MEDIA)

2. TÉCNICOS (RT):
   - ¿Cuál es el lenguaje principal?
   - ¿Cuáles frameworks se usan?
   - ¿Qué requisitos de performance? (latencia, throughput)
   - ¿Qué requisitos de escalabilidad?

3. CALIDAD (RQ):
   - ¿Coverage de tests esperado? (70%, 80%, 90%)
   - ¿Buenas prácticas de código obligatorias?
   - ¿Documentación de código requerida?
   - ¿Code review obligatorio?

4. AMBIENTE (RA):
   - ¿Cuáles ambientes? (DEV, QA, STAGING, PROD)
   - ¿Qué características especiales por ambiente?
   - ¿Restricciones de cada ambiente?
```

### Plantilla requirements.md

```markdown
# Requirements

## Requisitos Funcionales

### RF-001: [Funcionalidad principal]
**Descripción:** [Qué debe hacer el sistema]
**Criterios de Aceptación:**
- ✅ [Criterio 1]
- ✅ [Criterio 2]
**Prioridad:** CRÍTICA

### RF-002: [Segunda funcionalidad]
[Repetir patrón]

## Requisitos Técnicos

### RT-001: Performance
**Descripción:** [Requisito de rendimiento]
**Criterios:** [Métricas específicas]
**Prioridad:** ALTA

## Requisitos de Calidad

### RQ-001: Testing
**Descripción:** [Coverage y estrategia de pruebas]
**Criterios:** [Porcentaje mínimo y tipos de test]
**Prioridad:** ALTA

## Requisitos de Ambiente

| Ambiente | Características | Restricciones |
|----------|-----------------|---------------|
| DEV | [Características] | [Restricciones] |
| QA | [Características] | [Restricciones] |
| STAGING | [Características] | [Restricciones] |
| PROD | [Características] | [Restricciones] |
```

---

## project-structure.md — Cuestionario

```
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
```

### Plantilla project-structure.md

```markdown
# Project Structure

## Patrón Arquitectónico

**[PATTERN]** proporciona:
- Separación de responsabilidades
- Modularidad e independencia entre capas
- Facilidad para testing unitario

## Estructura Visual

\`\`\`
[PROJECT_ROOT]/
├── docs/                    Documentación del proyecto
├── src/
│   ├── [layer-1]/           [Descripción de responsabilidad]
│   ├── [layer-2]/           [Descripción de responsabilidad]
│   └── shared/              Utilidades compartidas
└── tests/
\`\`\`

## Descripción de Capas

| Capa | Responsabilidad | Dependencias |
|------|----------------|--------------|
| [layer-1] | [Qué hace] | [De qué depende] |
| [layer-2] | [Qué hace] | [De qué depende] |
| shared | Utilidades comunes | Ninguna |

## Principios de Organización
- **Modularidad:** Cada módulo es independiente
- **Claridad:** Estructura predecible y consistente
- **Escalabilidad:** Fácil agregar nuevos módulos
```

---

## tech-stack.md — Cuestionario

```
1. LENGUAJE PRINCIPAL:
   - ¿Cuál es el lenguaje base?
   - ¿Por qué se eligió?
   - ¿Versión mínima requerida?

2. FRAMEWORKS PRINCIPALES:
   - ¿Cuáles son los frameworks críticos?
   - ¿Cuál fue la alternativa descartada y por qué?
   - ¿Cómo se justifica cada selección?

3. HERRAMIENTAS:
   - ¿Build system?
   - ¿Testing frameworks?
   - ¿CI/CD pipelines?
   - ¿Monitoring/Logging?

4. FUTURO:
   - ¿Hay tecnologías en evaluación?
   - ¿Hay planes de actualización conocidos?
```

### Plantilla tech-stack.md

```markdown
# Tech Stack

## Lenguaje Principal

**[LANGUAGE_NAME]** v[VERSION]
- **Justificación:** [Razonamiento técnico]
- **Alternativas consideradas:** [Alternativas y por qué no se usaron]

## Frameworks Clave

### [FRAMEWORK_1]
- **Propósito:** [Para qué se usa]
- **Versión:** [VERSION]
- **Justificación:** [Razones técnicas clave]
- **Alternativas descartadas:** [Frameworks alternativos y por qué no]

## Herramientas de Desarrollo

| Herramienta | Propósito | Estado |
|-------------|-----------|--------|
| [TOOL_1] | [Propósito] | Activo |
| [TOOL_2] | [Propósito] | En evaluación |

## Decisiones Técnicas Registradas

| Decisión | Alternativas | Razón elección | Fecha |
|----------|--------------|----------------|-------|
| [TOOL/FRAMEWORK] | [Alternativas] | [Justificación] | [Fecha] |
```

---

## features.md — Cuestionario

```
1. FEATURES PRINCIPALES:
   - ¿Cuáles son las 3-5 features principales?
   - ¿Cómo funciona cada una en términos generales?
   - ¿Cuál es el flujo de cada feature?

2. CASOS EXTREMOS:
   - ¿Qué casos especiales (edge cases) existen?
   - ¿Cómo se manejan errores?
   - ¿Cuál es el comportamiento en fallo?

3. VALIDACIONES:
   - ¿Qué reglas de negocio se aplican?
   - ¿Qué validaciones deben hacerse?
```

### Plantilla features.md

```markdown
# Features

## [FEATURE_1_NAME]

**Propósito:** [Descripción de qué hace esta feature]

### Flujo Normal
1. [Paso 1]
2. [Paso 2]
3. [Paso 3]

### Casos Extremos
| Caso | Comportamiento esperado |
|------|------------------------|
| [Edge case 1] | [Cómo se maneja] |
| [Edge case 2] | [Cómo se maneja] |

### Validaciones
- ✓ [Validación 1]
- ✓ [Validación 2]

---

## [FEATURE_2_NAME]
[Repetir patrón]
```

---

## implementation.md — Cuestionario

```
1. PREPARACIÓN:
   - ¿Cuáles son los prerequisites?
   - ¿Qué software se necesita instalar?
   - ¿Cuáles son los pasos de setup?

2. ESTÁNDARES DE CÓDIGO:
   - ¿Convenciones de nombre? (camelCase, snake_case, PascalCase)
   - ¿Formato de código? (indentation, line length)
   - ¿Comentarios y documentación?

3. GIT WORKFLOW:
   - ¿Branching strategy? (git flow, trunk-based)
   - ¿Commit message format? (conventional commits)
   - ¿PR/Code review process?

4. CI/CD:
   - ¿Qué checks automáticos?
   - ¿Qué tests ejecutan?
   - ¿Qué artifacts se generan?
```

### Plantilla implementation.md

```markdown
# Implementation Guide

## Prerequisites

| Herramienta | Versión mínima | Instalación |
|-------------|---------------|-------------|
| [SOFTWARE_1] | [VERSION]+ | [Comando/link] |
| [SOFTWARE_2] | [VERSION]+ | [Comando/link] |

## Setup Inicial

\`\`\`bash
# 1. [Descripción del primer paso]
[comando]

# 2. [Descripción del segundo paso]
[comando]
\`\`\`

## Estándares de Codificación

| Aspecto | Estándar |
|---------|----------|
| Variables | camelCase |
| Clases | PascalCase |
| Constantes | UPPER_SNAKE_CASE |
| Archivos | kebab-case |

## Git Workflow

\`\`\`
main ← develop ← feature/[nombre] | fix/[nombre] | chore/[nombre]
\`\`\`

**Formato de commits:** `[type]([scope]): [description]`

## CI/CD Pipeline

| Stage | Checks | Criterio de paso |
|-------|--------|-----------------|
| Build | Compilación | Sin errores |
| Test | Unit + Integration | Coverage ≥ [X]% |
| Lint | Análisis estático | 0 errores |
| Deploy | [Ambiente] | Aprobación manual |
```

---

## user-flow.md — Cuestionario

```
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
```

### Plantilla user-flow.md

```markdown
# User Flows

## [FLOW_1_NAME]

**Actor:** [Quién lo inicia]  
**Precondición:** [Estado inicial necesario]

### Flujo Normal

\`\`\`
1. [Paso 1]
   → [Resultado]
2. [Paso 2]
   → [Resultado]
3. [Paso 3]
   → [Resultado final]
\`\`\`

### Flujos Alternativos

| Escenario | Pasos alternativos | Resultado |
|-----------|-------------------|-----------|
| [Caso 1] | [Pasos] | [Resultado] |
| [Error] | [Manejo del error] | [Mensaje/estado] |

**Postcondición:** [Estado final en flujo exitoso]

---

## [FLOW_2_NAME]
[Repetir patrón]
```
