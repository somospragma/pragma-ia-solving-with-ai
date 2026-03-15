---
trigger: always_on
---

# Instructions - Pragma IA

**Contexto:** Asistencia para el repositorio `pragma-ia-solving-with-ai`

> Instrucciones operativas del agente. Para contexto completo del proyecto, consultar [AGENTS.md](../../AGENTS.md) y la documentación en `docs/`.

---

## 1. FUENTES DE VERDAD

> NO duplicar contenido de estos documentos. Referenciarlos siempre.

| Documento | Propósito |
|-----------|-----------|
| [project-overview.md](../../docs/project-overview.md) | Visión, objetivos, principios |
| [requirements.md](../../docs/requirements.md) | Requisitos RF, RT, RQ |
| [features.md](../../docs/features.md) | Funcionalidades detalladas |
| [project-structure.md](../../docs/project-structure.md) | Estructura de carpetas |
| [tech-stack.md](../../docs/tech-stack.md) | Stack tecnológico |
| [implementation.md](../../docs/implementation.md) | Estándares de contenido y naming |
| [CONTRIBUTING.md](../../CONTRIBUTING.md) | Proceso de contribución y commits |

---

## 2. ESTÁNDARES DE CONTENIDO (resumen operativo)

> Detalle completo en [implementation.md](../../docs/implementation.md)

### Naming
- Archivos: `snake_case.md` — Carpetas: `snake_case/`
- H1: PascalCase descriptivo — H2: PascalCase
- Links: `[Texto](path/to/file.md)`

### Metadata YAML Obligatoria
```yaml
---
name: "[Nombre]"
version: "[SEMVER]"
updated: "[YYYY-MM-DD]"
author: "[Nombre o equipo]"
domain: "[backend|frontend|mobile|devops|devsecops|qa|arquitectura|integracion]"
type: "[instruction|prompt|resource|chatmode|skill]"
status: "[draft|stable|deprecated]"
references:
  - "[Artefacto relacionado]"
---
```

### Documentación Mínima por Artefacto
1. Descripción clara
2. Contexto de uso
3. Dominios aplicables
4. Al menos 1 ejemplo práctico
5. Casos límite
6. Referencias cruzadas

---

## 3. CONVENCIONES DE COMMITS

> Detalle completo en [CONTRIBUTING.md](../../CONTRIBUTING.md)

Formato: [Conventional Commits](https://www.conventionalcommits.org/)

```
<type>(<scope>): <subject>
```

**Tipos:** `feat` · `fix` · `docs` · `refactor` · `test` · `chore` · `style` · `perf`

**Scopes:** `backend` · `frontend` · `mobile` · `cloudops` · `devsecops` · `qa` · `arquitectura` · `integracion` · `docs` · `skills`

---

## 4. PROTOCOLO DE SKILLS

**IMPORTANTE:** Todos los cambios deben validarse contra skills aplicables.

1. **Detecta** skills por keywords, tipo de cambio, dominio
2. **Lee** `SKILL.md` ANTES de implementar
3. **Aplica** guidelines consistentemente
4. **Valida** resultado contra estándares
5. **Menciona** skill usado: _"Se aplicó **X skill** para..."_

---

## 5. REGLAS OPERATIVAS DEL AGENTE

### DEBES
- ✅ Consultar [AGENTS.md](../../AGENTS.md) y docs/ como fuente de verdad
- ✅ Seguir estructura y convenciones del repositorio
- ✅ Incluir metadata YAML completa en todo artefacto
- ✅ Proporcionar al menos 1 ejemplo práctico
- ✅ Documentar casos límite
- ✅ Incluir referencias cruzadas
- ✅ Aplicar skills relevantes
- ✅ Seguir Conventional Commits

### NO DEBES
- ❌ Duplicar contenido de `docs/` en artefactos
- ❌ Crear artefactos sin metadata
- ❌ Omitir documentación o ejemplos
- ❌ Usar PascalCase para nombres de archivos
- ❌ Colocar artefactos en carpetas incorrectas
- ❌ Ignorar estándares de commits

### Cuando Sugieras Mejoras
- Revisar qué docs podrían quedar obsoletos
- Recomendar actualizaciones
- Aplicar cambios en CHANGELOG.md
- Proporcionar diffs concretos

---

## 6. VALIDACIÓN FINAL

Antes de presentar cualquier trabajo:
- [ ] Metadata completa
- [ ] Descripción clara
- [ ] Sin TBD/TODO/placeholders
- [ ] Ejemplo práctico incluido
- [ ] Links internos verificados
- [ ] Convenciones de nombres
- [ ] Estructura de carpetas correcta
- [ ] Skills aplicados y mencionados
- [ ] Commits Conventional
