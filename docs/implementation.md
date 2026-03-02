# Pragma IA - Guía de Implementación

## Preparación del Entorno

### Prerequisites
- Git: v2.37+
- Markdown editor: VS Code con extensión Markdown Preview Enhanced (preferido)

### Setup Inicial
```bash
# Paso 1: Clonar el repositorio
git clone https://github.com/somospragma/pragma-ia-solving-with-ai.git
cd pragma-ia-solving-with-ai

# Paso 2: Crear rama de características
git checkout -b feature/[descripcion-corta]

# Paso 3: Verificar estructura
tree -d -L 2  # Revisar carpetas principales
```

---

## Estándares de Contenido

### Convenciones de Nombres

| Elemento | Estándar | Ejemplo |
|----------|----------|---------|
| Archivos | snake_case.md | backend_java_exceptions.md |
| Carpetas | snake_case / | instructions_or_rules/ |
| Títulos H1 | PascalCase con descripción | # Java Exception Handling Strategy |
| Secciones H2 | PascalCase | ## Error Handling Patterns |
| Links internos | [Texto](path/to/file.md) | [Requerimientos](docs/requirements.md) |

### Formato de Metadata

Cada artefacto principal debe incluir:
```yaml
---
name: [Nombre del artefacto]
version: [SEMVER: major.minor.patch]
updated: [ISO date: YYYY-MM-DD]
author: [Nombre o equipo]
domain: [backend, frontend, mobile, devops, devsecops, qa, arquitectura, integracion]
type: [instruction, prompt, resource, chatmode, skill]
status: [draft, stable, deprecated]
references: 
  - [Otro artefacto relacionado si existe]
---
```

### Documentación Mínima

Cada artefacto debe incluir:
1. **Descripción clara:** ¿Qué es y para qué sirve?
2. **Contexto de uso:** ¿Cuándo usar esto?
3. **Dominios aplicables:** ¿Qué tecnologías/áreas cubre?
4. **Ejemplos:** Al menos 1 ejemplo de uso real
5. **Casos limite:** Situaciones edge case y cómo se manejan

---

## Estándares de Codificación (para ejemplos de código)

### Convenciones Lingüísticas
- Comentarios en español (comentarios conceptuales)
- Código en inglés (siguiente estándar del lenguaje)
- Docstrings/comentarios iniciales pueden ser bilingües

### Validación de Código
- Todo código debe ser sintácticamente válido
- Debe poder ser copiado y ejecutado directamente
- No deben haber variables sin definición
- Imports/dependencies deben estar claros

---

## Git Workflow

### Crear Nueva Característica o Artefacto

```bash
# 1. Partir desde develop
git checkout develop
git pull origin develop

# 2. Crear rama feature
git checkout -b feature/[tipo]/[nombre-corto]

# Ejemplos:
git checkout -b feature/instruction/java-security-patterns
git checkout -b feature/prompt/testing-automation-e2e
git checkout -b feature/resource/microservices-template
```

### Commits

**Formato:** [Conventional Commits](https://www.conventionalcommits.org/)
```
feat([domain]): [descripción]

Body: [Descripción más detallada si es necesario]

Footer: [Referencias a issues o PRs]
```

**Ejemplos:**
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

### Push y Pull Request

```bash
# 1. Hacer push de rama
git push origin feature/[tipo]/[nombre]

# 2. Crear Pull Request
# - Ir a GitHub
# - Seleccionar rama develop como target
# - Llenar template PR
# - Solicitor review

# 3. Tras aprobación, mergear en develop
# 4. Periodicamente, mergear develop → main (release)
```

---

## Validación de Artefactos

### Checklist antes de Commit

- [ ] Metadata completa (name, version, updated, author, domain, type, status)
- [ ] Descripción clara en primera sección
- [ ] Al menos 1 ejemplo práctico incluido
- [ ] Archivos nombrados en snake_case
- [ ] No hay TBD sin documentar
- [ ] Links internos usan rutas relativas correctas
- [ ] Código de ejemplo es válido y executable (si aplica)
- [ ] Sin secretos, contraseñas o datos sensibles
- [ ] Ortografía y gramática revisadas

---

## Proceso de Review

### Qué esperar en una revisión

1. **Contenido:** ¿Es correcto, claro, útil?
2. **Estructura:** ¿Sigue estándares del repositorio?
3. **Cualidad:** ¿Es de estándar profesional?
4. **Cobertura:** ¿Hay gaps o ejemplos insuficientes?

### Cómo responder a comentarios

- Responder a todos los comentarios
- Marcar como "Resolved" tras hacer cambios
- Re-request review tras cambios significativos
- Usar Review Threads para mantener conversación organizada

---

## Política de Versionamiento

### Semantic Versioning: major.minor.patch

| Incremento | Cuándo | Ejemplo |
|-----------|--------|---------|
| MAJOR | Cambios que rompen compatibilidad | 1.0.0 → 2.0.0 |
| MINOR | Características nuevas compatibles | 1.0.0 → 1.1.0 |
| PATCH | Fixes y mejoras menores | 1.0.0 → 1.0.1 |

### Actualizar Versión
1. Cambiar `version:` en metadata del artefacto
2. Documentar en CHANGELOG.md bajo sección [Unreleased]
3. Incluir versión en commit message

---

## Ciclo de Release

### De Develop a Main

```bash
# 1. Feature se completa y approva en develop

# 2. Crear release branch
git checkout -b release/vX.Y.Z

# 3. Actualizar versiones y CHANGELOG

# 4. Crear tag
git tag -a vX.Y.Z -m "Release version X.Y.Z"

# 5. Mergear a main y back a develop
git checkout main
git merge --no-ff release/vX.Y.Z

# 6. Push
git push origin main --tags
git push origin develop
```

---

## Medidas de Calidad

### Documentación
- Coverage: Todos los artefactos del roadmap deben estar documentados
- Actualización: Revisada mínimo cada 3 meses
- Claridad: Legible por alguien nuevo en el dominio

### Código (en ejemplos)
- Sintaxis válida: Ejecutable sin modificaciones
- Seguridad: Sin hardcoded secrets o passwords
- Mejores prácticas: Sigue patrones del dominio

### Mantenimiento
- Estabilidad: Artefactos sin cambios por 6+ meses evaluados como stable
- Deprecación: Claramente marcados cuando son reemplazados
- Linaje: Referencias claras a predecessores/successores
