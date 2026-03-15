# Copilot Instructions — Pragma IA Solving with AI

> Steering persistente para GitHub Copilot. Complementa [AGENTS.md](../AGENTS.md).

## Contexto

Repositorio de artefactos reutilizables de IA: instrucciones, prompts, chatmodes, resources y skills.
Detalle: [docs/project-overview.md](../docs/project-overview.md)

## Stack

Markdown (GFM) · YAML 1.2 · JSON5 · Git/GitHub · Pragma MCP
Detalle: [docs/tech-stack.md](../docs/tech-stack.md)

## Estructura

```
instructions_or_rules/   → Instrucciones por dominio
prompts/                 → Prompts reutilizables
resources/               → Plantillas y guías (MCP)
chatmodes/               → Comportamientos Copilot
docs/                    → Documentación del proyecto
.agent/rules/            → Instrucciones del agente
```

Detalle: [docs/project-structure.md](../docs/project-structure.md)

## Reglas Operativas

1. **DRY:** NO duplicar contenido de `docs/`. Referenciar con links relativos
2. **Metadata:** Todo artefacto lleva frontmatter YAML (name, version, updated, author, domain, type, status)
3. **Naming:** Archivos `snake_case.md`, carpetas `snake_case/`, H1 PascalCase
4. **Commits:** Conventional Commits — ver [CONTRIBUTING.md](../CONTRIBUTING.md)
5. **Skills:** Detectar por keywords → leer SKILL.md → aplicar → mencionar
6. **Validación:** Metadata + descripción + ejemplo práctico + links verificados

## Límites

- NUNCA modificar `.git/`
- SIEMPRE confirmar antes de eliminar archivos
- Deny list: `rm -rf`, `sudo`, `git push --force`

## Referencias Completas

- Reglas del agente: [.agent/rules/rules.md](../.agent/rules/rules.md)
- Implementación: [docs/implementation.md](../docs/implementation.md)
- Contribución: [CONTRIBUTING.md](../CONTRIBUTING.md)
