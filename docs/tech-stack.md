# Pragma IA - Tech Stack

## Formato Principal: Markdown

**Justificación:**
- Legible en cualquier editor de texto
- Control de versiones friendly (Git)
- Soportado nativemente en GitHub
- Portable entre diferentes herramientas
- Agnóstico a tecnología de IA

**Alternativas consideradas:**
- [JSON] - Rechazado para instrucciones por ser menos legible
- [YAML] - Usado para metadata pero no para contenido principal

---

## Formatos Soportados

### Markdown
- **Propósito:** Instrucciones completas, prompts narrativos, documentación
- **Versión:** CommonMark con extensiones GFM (GitHub Flavored Markdown)
- **Justificación:** Estándar de facto, ampliamente soportado

### JSON
- **Propósito:** Chatmodes, configuraciones, metadata estructurada
- **Versión:** JSON5 para comentarios cuando es necesario
- **Justificación:** Serialización estructurada, fácil de parsear

### YAML
- **Propósito:** Frontmatter de metadata, configuraciones legibles
- **Versión:** YAML 1.2
- **Justificación:** Más legible que JSON, soportado en Jekyll/GitHub Pages

---

## Herramientas de Desarrollo

| Herramienta | Propósito | Estado |
|-------------|-----------|--------|
| Git | Control de versiones | Activo |
| GitHub | Repositorio y colaboración | Activo |
| Markdown | Formato de contenido | Activo |
| JSON | Configuraciones | Activo |
| Pragma MCP | Infraestructura para CI/CD | Activo |

---

## Asistentes de IA Soportados

### GitHub Copilot
- **Estado:** Soporte completo
- **Compatibilidad:** Instrucciones, prompts, chatmodes
- **Ventajas:** Chatmodes nativos, integración directa en VS Code

### Amazon Q Developer (AWS)
- **Estado:** Soporte completo
- **Compatibilidad:** Instrucciones, prompts, context
- **Ventajas:** Integración con herramientas AWS

### ChatGPT / Claude API
- **Estado:** Soporte parcial
- **Compatibilidad:** Instrucciones y prompts
- **Limitación:** Sin chatmodes específicos

### Open Source (Ollama, LM Studio)
- **Estado:** Soporte experimental
- **Compatibilidad:** Instrucciones y prompts básicos
- **Limitación:** Requiere adaptaciones para modelos específicos

---

## Decisiones Tecnológicas Documentadas

### Decisión 1: Markdown como formato principal
**Contexto:** Necesidad de formato legible y versionable
**Alternativas:** JSON, YAML, proprietary formats
**Decisión:** Markdown
**Justificación:** Legibilidad humana + git-friendly + portabilidad

### Decisión 2: GitHub como plataforma central
**Contexto:** Necesidad de control de versiones y colaboración
**Alternativas:** GitLab, Gitea, Bitbucket
**Decisión:** GitHub
**Justificación:** Integración GitHub Copilot nativa + adopción en Pragma

### Decisión 3: Estructura por dominio en lugar de tipo de artefacto
**Contexto:** Organización de miles de artefactos
**Alternativas:** Organizar solo por tipo (instructions/, prompts/ simple)
**Decisión:** Estructura por dominio + tipo
**Justificación:** Facilita navegación según especialidad técnica

---

## Integración con Pragma Infrastructure

### Pragma MCP (Model Context Protocol)
- **Función:** Expone resources vía API a asistentes
- **Ubicación:** Configurado apuntando a la carpeta `resources/`
- **Beneficio:** Recursos disponibles sin copia/paste manual

---

## Versionamiento y Mantenimiento

### Control de Versiones
- **Sistema:** Git
- **Rama principal:** `main` (producción)
- **Rama de desarrollo:** `develop` (staging)

### Historial de Cambios
- **Archivo:** CHANGELOG.md
- **Formato:** Keep a Changelog (https://keepachangelog.com/)
- **Actualizaciones:** Con cada cambio significativo

### Metadata de Artefactos
Cada artefacto importante incluye:
```yaml
---
name: [Nombre del artefacto]
version: [SEMVER: major.minor.patch]
updated: [ISO date]
author: [Creador/Responsable]
domain: [Dominio: backend, frontend, mobile, etc.]
status: [draft, stable, deprecated]
---
```
