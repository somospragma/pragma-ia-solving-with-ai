# Instructions Orchestrator — Angular Project

```yaml
name: "Angular Project"
version: "2.0"
applies_to: ["frontend", "angular", "typescript"]
status: "Active"
authors:
  - name: "Jaime Gallo"
    email: "jaime.gallom@pragma.com.co"
  - name: "Cristian Otálora"
    email: "cristian.otalora@pragma.com.co"
  - name: "Esteban García"
    email: "esteban.garcia@pragma.com.co"
tags: ["angular", "typescript", "tailwind", "sass", "standalone-components", "signals"]
last_updated: "2025-09-16"
```

## Instructions Management

### Main Modules

- [01-context.md](./01-context.md) - General project and domain context
- [02-code-guidelines.md](./02-code-guidelines.md) - Code standards and conventions
- [03-technology.md](./03-technology.md) - Angular-specific guidelines
- [04-quality.md](./04-quality.md) - Testing and quality practices
- [05-process.md](./05-process.md) - Workflow and processes
- [99-agent-considerations.md](./99-agent-considerations.md) - AI agent guidelines

### Application Guide

**Architecture/Setup**: Load `01-context.md` + `03-technology.md`
**Component/Service Development**: Load `02-code-guidelines.md` + `03-technology.md`
**Testing/Debugging**: Load `04-quality.md` + `02-code-guidelines.md`
**Process/Deployment**: Load `05-process.md`
**AI Behavior**: Load `99-agent-considerations.md`

### Priority Order

1. **Critical**: Context + Technology (`01`, `03`)
2. **High**: Code Guidelines + Quality (`02`, `04`)
3. **Medium**: Process (`05`)
4. **As Needed**: Agent Considerations (`99`)
