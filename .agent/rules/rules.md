---
trigger: always_on
---

# Instructions - Pragma IA

**Contexto:** Asistencia para el repositorio `pragma-ia-solving-with-ai`

Este archivo contiene instrucciones contextuales para trabajar en este repositorio. Estas instrucciones mejoran la generación de código y artefactos alineándose con la documentación del proyecto.

---

## 1. CONTEXTO Y VISIÓN DEL PROYECTO

### Propósito
Centralizar y sistematizar **artefactos reutilizables de IA** (instrucciones, prompts, chatmodes y recursos) para capacitar a equipos de desarrollo a trabajar más efectivamente con asistentes de IA.

### Objetivos Principales
1. **Reutilización:** Repositorio único de artefactos agnósticos a tecnología para múltiples dominios
2. **Estandarización:** Formatos, patrones y estándares claros para resultados consistentes
3. **Accesibilidad:** Descubrimiento y uso de artefactos sin requerir conocimiento profundo de IA
4. **Escalabilidad:** Crecimiento coherente con nuevos dominios y casos de uso
5. **Documentación:** Sistema robusto explicando QUÉ, POR QUÉ y CÓMO usar

### Principios Arquitectónicos
- **Single Responsibility:** Cada artefacto resuelve UN problema específico
- **DRY (Don't Repeat Yourself):** Reutilización evita duplicación
- **Agnóstico a Tecnología:** Compatible con GitHub Copilot, Amazon Q, Claude, etc.
- **Documentación Clara:** Contexto, casos de uso y ejemplos en cada artefacto
- **Iteración Continua:** Evolución constante con feedback de usuarios

---

## 2. ESTRUCTURA DEL REPOSITORIO

### Carpetas Principales
```
instructions_or_rules/     → Instrucciones personalizadas por dominio
prompts/                   → Prompts reutilizables para tareas específicas
resources/                 → Plantillas, ejemplos y guías (invocables vía MCP)
chatmodes/                 → Comportamientos personalizados (GitHub Copilot)
docs/                      → Documentación del proyecto
```

### Dominios Soportados
- **backend** - Java, Node.js, Spring, Microservicios
- **frontend** - HTML, CSS, JavaScript, React, Angular
- **mobile** - Flutter, iOS, Android, Dart
- **cloudops** - AWS, Azure, GCP, Infraestructura como Código
- **devsecops** - Seguridad, Scanning, Auditoría
- **qa-testing** - Testing, Automatización, QA
- **arquitectura** - Patrones, Diseño, Decisiones Arquitectónicas
- **integracion** - APIs, Servicios, Orquestación

### Patrón de Organización
La estructura usa **Arquitectura Modular por Dominio:**
- Separación clara de responsabilidades
- Cada dominio es independiente pero interconectado
- Modularidad: escalable sin afectar lo existente
- Reutilización: estándares en `_estandar-instructions/` y transversales en `transversal/`

---

## 3. ESTÁNDARES DE CONTENIDO

### Convenciones de Nombres
```
Archivos:     snake_case.md                    (ej: backend_java_exceptions.md)
Carpetas:     snake_case/                      (ej: instructions_or_rules/)
Títulos H1:   PascalCase descriptivo           (ej: # Java Exception Handling Strategy)
Secciones H2: PascalCase                       (ej: ## Error Handling Patterns)
Links:        [Texto](path/to/file.md)         (ej: [Requirements](docs/requirements.md))
```

### Metadata Requerida (YAML Front Matter)
```yaml
---
name: [Nombre del artefacto]
version: [SEMVER: major.minor.patch]
updated: [ISO date: YYYY-MM-DD]
author: [Nombre o equipo]
domain: [backend|frontend|mobile|devops|devsecops|qa|arquitectura|integracion]
type: [instruction|prompt|resource|chatmode|skill]
status: [draft|stable|deprecated]
references: 
  - [Otro artefacto relacionado si existe]
---
```

### Documentación Mínima Requerida
Todo artefacto DEBE incluir:
1. **Descripción clara:** ¿Qué es y para qué sirve?
2. **Contexto de uso:** ¿Cuándo usar esto?
3. **Dominios aplicables:** ¿Qué tecnologías/áreas cubre?
4. **Ejemplos prácticos:** Al menos 1 ejemplo de uso real
5. **Casos límite:** Situaciones edge case y cómo se manejan
6. **Referencias cruzadas:** Links a artefactos relacionados

### Validaciones de Contenido
- [ ] Metadata completa (name, version, updated, author, domain, type, status)
- [ ] Descripción clara en primeras líneas
- [ ] Sin "TBD" o placeholders indefinidos
- [ ] Sin referencias externas no documentadas
- [ ] Ejemplo práctico incluido
- [ ] Formato de código válido y ejecutable
- [ ] Links internos verificados

---

## 4. REQUISITOS FUNCIONALES Y TÉCNICOS

### Requisitos Funcionales (RF)
- **RF-001:** Almacenar y organizar instrucciones personalizadas por dominio
- **RF-002:** Gestionar prompts reutilizables para tareas específicas
- **RF-003:** Mantener recursos reutilizables invocables vía MCP
- **RF-004:** Proporcionar chatmodes personalizados para GitHub Copilot

### Requisitos Técnicos (RT)
- **RT-001:** Formato de archivos: Markdown (instrucciones), JSON (chatmodes), YAML (metadata)
- **RT-002:** Estructura de carpetas predecible y escalable
- **RT-003:** Versionamiento con Git y CHANGELOG.md
- **RT-004:** Compatibilidad multi-herramienta (Copilot, Amazon Q, Claude)

### Requisitos de Calidad (RQ)
- **RQ-001:** Claridad y documentación completa
- **RQ-002:** Ejemplos prácticos y validables
- **RQ-003:** Artefactos agnósticos a tecnología (adaptables)

---

## 5. CONVENCIONES DE COMMITS

### Formato: Conventional Commits
Todos los commits DEBEN seguir [Conventional Commits](https://www.conventionalcommits.org/)

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Tipos Recomendados
```
feat       → Nueva característica o artefacto
fix        → Corrección de artefacto existente
docs       → Cambios en documentación
refactor   → Reestructuración sin cambiar funcionalidad
test       → Adición/mejora de tests
chore      → Cambios de configuración o setup
style      → Formato, sin cambiar significado
perf       → Mejora de rendimiento
```

### Scopes Recomendados
```
backend         → Artefactos de backend
frontend        → Artefactos de frontend
mobile          → Artefactos de mobile
cloudops        → Artefactos de cloudops
devsecops       → Artefactos de devsecops
qa              → Artefactos de qa-testing
arquitectura    → Artefactos de arquitectura
integracion     → Artefactos de integración
docs            → Documentación del proyecto
skills          → Nuevos skills
```

### Ejemplos Correctos
```
feat(backend): agregar patrón de excepciones para Java

Incluye:
- Clasificación de excepciones checked/unchecked
- Ejemplos prácticos
- Best practices de manejo

Closes #123
```

```
docs(docs): actualizar requirements con RT-004

Agrega requisito técnico para versionamiento de artefactos.

Refs #456
```

```
feat(mobile): crear instrucción de logging para Flutter

Incluye patrón Strategy para intercambiadores de handlers y documentación de Crashlytics, Sentry, DataDog.

Closes #789
```

---

## 6. PROTOCOLO DE SKILLS

**IMPORTANTE:** Todos los cambios deben validarse contra skills aplicables.

### Proceso de Aplicación de Skills

1. **Detecta automáticamente** skills relevantes basándote en:
   - Keywords en la solicitud (logging, tests, commits, changelog, etc.)
   - Tipos de cambios que se hacen (código, documentación, tests)
   - Dominios técnicos mencionados (flutter, backend, frontend, etc.)

2. **Lee el SKILL.md** correspondiente ANTES de implementar cambios

3. **Aplica las guidelines** de la skill consistentemente en todo el trabajo

4. **Valida el resultado** contra los estándares de la skill

5. **Menciona claramente** qué skill se usó al presentar cambios
   - Ejemplo: "Se aplicó **flutter-testing skill** para..."

---

## 7. REFERENCIAS A DOCUMENTACIÓN

### Documentos Clave por Rol

#### Para Nuevos Colaboradores
1. Leer [project-overview.md](../docs/project-overview.md) - Entiende QUÉ es el proyecto
2. Leer [features.md](../docs/features.md) - Detalle de funcionalidades
3. Leer [requirements.md](../docs/requirements.md) - Tipos de artefactos aceptados
4. Leer [implementation.md](../docs/implementation.md) - Estándares de contenido
5. Leer [project-structure.md](../docs/project-structure.md) - Organización del repositorio

#### Para Maintainers / Arquitectos
1. Leer [project-overview.md](../docs/project-overview.md) - Propósito y objetivos
2. Leer [requirements.md](../docs/requirements.md) - Requisitos funcionales y técnicos
3. Leer [features.md](../docs/features.md) - Descripción detallada de cada funcionalidad
4. Leer [project-structure.md](../docs/project-structure.md) - Arquitectura del sistema
5. Leer [tech-stack.md](../docs/tech-stack.md) - Tecnologías y justificaciones
6. Leer [implementation.md](../docs/implementation.md) - Estándares y procesos

### Documento de Referencia Rápida
- **Visión General:** [docs/project-overview.md](../docs/project-overview.md)
- **Estructura:** [docs/project-structure.md](../docs/project-structure.md)
- **Requisitos:** [docs/requirements.md](../docs/requirements.md)
- **Features:** [docs/features.md](../docs/features.md)
- **Implementación:** [docs/implementation.md](../docs/implementation.md)
- **Flujos de Usuario:** [docs/user-flow.md](../docs/user-flow.md)
- **Guía de Documentación:** [docs/index.md](../docs/index.md)

---

## 8. INSTRUCCIONES DE USO PARA IA

### Cuando Generes Código o Artefactos

**DEBES:**
- ✅ Seguir la estructura y convenciones del repositorio
- ✅ Respetar los estándares de nombres (snake_case para archivos, PascalCase para títulos)
- ✅ Incluir metadata YAML completa
- ✅ Proporcionar ejemplos prácticos y ejecutables
- ✅ Documentar casos límite y edge cases
- ✅ Incluir referencias cruzadas a artefactos relacionados
- ✅ Validar contra requisitos del proyecto
- ✅ Aplicar skills relevantes cuando detectes keywords
- ✅ Mencionar qué skill se aplicó

**NO DEBES:**
- ❌ Crear artefactos sin metadata completa
- ❌ Omitir documentación o ejemplos
- ❌ Usar names.PascalCase para archivos
- ❌ Colocar artefactos en carpetas incorrectas
- ❌ Crear duplicados de artefactos existentes sin referencias cruzadas
- ❌ Ignorar los estándares de commits
- ❌ Generar código/prompts sin validar aplicabilidad a dominio

### Cuando Sugieras Mejoras a Documentación

Si los cambios que se hacen podrían afectar la documentación actual:
- Revisar qué documentos podrían quedar obsoletos
- Recomendar actualizaciones explícitamente
- Aplicar cambios en el changelog
- Proporcionar diffs o sugerencias concretas

---

## 9. VALIDACIÓN FINAL

Antes de presentar cualquier trabajo, valida:
- [ ] Metadatos completos (name, version, updated, author, domain, type, status)
- [ ] Descripción clara en primeras líneas
- [ ] Sin TBD, TODO o placeholders indefinidos
- [ ] Ejemplo práctico ejecutable incluido
- [ ] Links internos funcionan (path/to/file.md)
- [ ] Sigue convenciones de nombres
- [ ] Estructura de carpetas correcta
- [ ] Requisitos funcionales/técnicos cubiertos
- [ ] Skills aplicables detectados y mencionados
- [ ] Commits seguirán Conventional Commits

---
