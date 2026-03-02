# Guía de Contribución

¡Bienvenido! Este documento te guía paso a paso para contribuir al repositorio `pragma-ia-solving-with-ai`. Nuestro objetivo es centralizar artefactos reutilizables de IA (instrucciones, prompts, chatmodes y recursos) de calidad consistente y alta.

**Tabla de contenidos**
- [Antes de Empezar](#antes-de-empezar)
- [Tipos de Contribuciones](#tipos-de-contribuciones)
- [Proceso de Contribución](#proceso-de-contribución)
- [Estándares de Contenido](#estándares-de-contenido)
- [Convenciones de Commits](#convenciones-de-commits)
- [Checklist de Validación](#checklist-de-validación)
- [Preguntas Frecuentes](#preguntas-frecuentes)

---

## Antes de Empezar

### Lee la Documentación Clave
Familiarízate con la estructura y propósito del proyecto:
1. [project-overview.md](docs/project-overview.md) - ¿Qué es este proyecto?
2. [project-structure.md](docs/project-structure.md) - Cómo está organizado
3. [requirements.md](docs/requirements.md) - Requisitos de artefactos
4. [implementation.md](docs/implementation.md) - Estándares de contenido

### Verifica tu Entorno
```bash
# Clona el repositorio
git clone https://github.com/somospragma/pragma-ia-solving-with-ai.git
cd pragma-ia-solving-with-ai
```

---

## Tipos de Contribuciones

### ✅ Contribuciones Aceptadas

#### 1. **Nuevas Instrucciones Personalizadas**
- Instrucciones contextuales para dominios específicos (backend, frontend, mobile, etc.)
- Ubicación: `instructions_or_rules/<domain>/`
- Forma: Archivos Markdown con metadata YAML

#### 2. **Nuevos Prompts Reutilizables**
- Prompts para tareas específicas de desarrollo
- Ubicación: `prompts/<domain>/`
- Forma: Archivos Markdown con frontmatter

#### 3. **Nuevos Recursos**
- Plantillas, ejemplos, guías reutilizables
- Ubicación: `resources/<domain>/`
- Forma: Archivos Markdown/JSON/YAML

#### 4. **Nuevos Chatmodes (GitHub Copilot)**
- Comportamientos personalizados para Copilot Chat
- Ubicación: `chatmodes/<domain>/`
- Forma: Archivos Markdown con configuración

#### 6. **Correcciones y Actualizaciones**
- Corregir errores, fechas desactualizadas, links rotos
- Mejorar ejemplos o claridad

#### 7. **Nuevos Skills**
- Guías reutilizables para patrones, buenas prácticas, estándares
- Ubicación: `instructions_or_rules/<domain>/skills/<skill-name>/`
- Forma: SKILL.md con metadata

---

## Proceso de Contribución

### Paso 1: Crea una Rama

```bash
# Asegúrate de estar en develop
git checkout develop
git pull origin develop

# Crea una rama con nombre descriptivo
git checkout -b feat/backend-java-exceptions
# O para bugfixes:
git checkout -b fix/broken-link-mobile-flutter
```

### Paso 2: Organiza tu Artefacto

**Para nuevas instrucciones (ejemplo):**
```
instructions_or_rules/backend/java/
└── backend_java_exceptions.md
```

**Para nuevos prompts (ejemplo):**
```
prompts/mobile/flutter/
└── mobile_flutter_logging_setup.md
```

### Paso 3: Crea el Artefacto con Metadata

Incluye metadata YAML completa (name, version, updated, author, domain, type, status, references) seguida de tu contenido con descripción, contexto, dominios, ejemplos, casos límite y referencias cruzadas.

Consulta [docs/implementation.md#documentación-mínima](docs/implementation.md#documentación-mínima) para la especificación completa de cada sección y formato requerido.

**Estructura referencia rápida:**
- Secciones H2: Descripción, Contexto de Uso, Dominios Aplicables, Ejemplos, Casos Límite, Referencias Cruzadas
- Código en bloques con lenguaje especificado
- Links con formato `[Texto](path/to/file.md)`

### Paso 4: Commit tus Cambios

Usa **Conventional Commits**:

```bash
# Nuevo artefacto
git add instructions_or_rules/backend/java/backend_java_exceptions.md
git commit -m "feat(backend): agregar patrón de excepciones para Java

Incluye:
- Clasificación de excepciones checked/unchecked
- Ejemplos prácticos con Spring Boot
- Best practices de manejo

Closes #123"

# O para bugfixes
git commit -m "fix(docs): corregir link roto en requirements

El link a project-overview.md no existía.

Fixes #456"
```

### Paso 5: Push y Pull Request

```bash
# Push a tu rama
git push origin feat/backend-java-exceptions

# Luego crea un PR en GitHub con:
# - Título: feat(backend): agregar patrón de excepciones para Java
# - Descripción: Explica QUÉ, POR QUÉ y CÓMO de tu contribución
# - References: Incluye "Closes #123" si resuelve un issue
```

---

## Estándares de Contenido

Todos los estándares de contenido están documentados en los siguientes documentos:

- **Convenciones de Nombres, Metadata y Documentación Mínima:** [docs/implementation.md](docs/implementation.md#estándares-de-contenido)
- **Requisitos Funcionales y Técnicos:** [docs/requirements.md](docs/requirements.md)

**Resumen rápido:**
- Archivos: `snake_case.md`
- Metadata: YAML completo (name, version, updated, author, domain, type, status, references)
- Documentación: descripción, contexto, ejemplos, casos límite, referencias cruzadas
- Calidad: sin TBD, ejemplos ejecutables, agnóstico a tecnología

---

## Convenciones de Commits

Todos los commits **DEBEN** seguir [Conventional Commits](https://www.conventionalcommits.org/).

**Formato:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Tipos:** `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `style`, `perf`
**Scopes:** `backend`, `frontend`, `mobile`, `cloudops`, `devsecops`, `qa`, `arquitectura`, `integracion`, `docs`, `skills`

---

## Checklist de Validación

Antes de enviar tu Pull Request, verifica **obligatoriamente** este checklist.

### Metadata y Documentación
- [ ] Metadata YAML completa (name, version, updated, author, domain, type, status, references)
- [ ] Descripción clara en primeras líneas
- [ ] Sin "TBD", "TODO" o placeholders indefinidos
- [ ] Al menos 1 ejemplo práctico y ejecutable
- [ ] Casos límite/edge cases identificados
- [ ] Referencias cruzadas a otros artefactos

### Formato y Estructura
- [ ] Nombre de archivo en `snake_case.md`
- [ ] Markdown válido (sin errores de sintaxis)
- [ ] Encabezados en PascalCase (`# Title`, `## Section`)
- [ ] Links internos con formato `[Texto](path/to/file.md)`
- [ ] Código en bloques con lenguaje especificado

### Organización
- [ ] Archivo en carpeta correcta (`<tipo>/<domain>/<subtema>`)
- [ ] No duplica artefactos existentes
- [ ] Si actualiza existente, versionamiento incrementado
- [ ] Dominio válido (backend, frontend, mobile, etc.)
- [ ] Tipo válido (instruction, prompt, resource, chatmode)

### Git y Commits
- [ ] Rama creada desde `develop` (naming: `feat/...` o `fix/...`)
- [ ] Commits siguen [Conventional Commits](https://www.conventionalcommits.org/)
- [ ] Mensaje claro y descriptivo
- [ ] Footer incluye referencias (`Closes #XXX`, `Fixes #YYY`)

---

## Preguntas Frecuentes

### P: ¿Dónde debo poner mi artefacto?
**R:** Usa esta jerarquía:
- `instructions_or_rules/<domain>/<subtema>/` para instrucciones
- `instructions_or_rules/<domain>/skills/<skill-name>/` para skills
- `prompts/<domain>/<subtema>/` para prompts
- `resources/<domain>/<subtema>/` para recursos
- `chatmodes/<domain>/<subtema>/` para chatmodes

**Dominios válidos:** `backend`, `frontend`, `mobile`, `cloudops`, `devsecops`, `qa`, `arquitectura`, `integracion`

### P: ¿Cuál es la diferencia entre Instruction, Prompt y Resource?
**R:** Consulta [docs/requirements.md](docs/requirements.md#requisitos-funcionales) para detalles completos:
- **Instruction:** Estándares de proceso (cómo hacer cosas)
- **Prompt:** Plantillas invocables para tareas específicas
- **Resource:** Documentación y ejemplos reutilizables

### P: ¿Qué versión inicial debo usar?
**R:** Usa `1.0.0` para nuevos artefactos. Incrementa según [Semantic Versioning](https://semver.org/): `major.minor.patch`

### P: ¿Puedo incluir código en mis contribuciones?
**R:** Sí, siempre que:
- Sea ejecutable y válido
- Incluya explicaciones claras
- Use el lenguaje correcto en bloques ` ```language `
- Proporcione ejemplos de uso reales

### P: ¿Qué significa "agnóstico a tecnología"?
**R:** Tu artefacto debería ser adaptable. En lugar de:
> "Solo funciona en Spring Boot"

Mejor:
> "Ejemplos en Spring Boot, pero puede adaptarse a cualquier framework Java"

### P: ¿Puedo contribuir si no sé mucho de IA?
**R:** ¡Absolutamente! Este proyecto es para:
- ✅ Desarrolladores escribiendo instrucciones/prompts para su dominio
- ✅ QA/Testing compartiendo estándares
- ✅ Arquitectos documentando patrones
- ✅ Cualquiera que tenga expertise y quiera compartirlo

No necesitas ser experto en IA, solo en tu dominio.

---

## Soporte y Contacto

¿Preguntas o dudas?
- 📖 Revisa [project-overview.md](docs/project-overview.md)
- � Reporta problemas en [Issues](https://github.com/somospragma/pragma-ia-solving-with-ai/issues)

---

**¡Gracias por contribuir!** 🎉
