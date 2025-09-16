# Instructions Orchestrator — Next.js Project

```yaml
name: "Next.js Project"
version: "2.0"
applies_to: ["frontend", "nextjs", "react", "typescript"]
status: "Active"
authors:
  - name: "Burke Holland"
    email: "burkeholland@gmail.com"
  - name: "Santiago Betancur"
    email: "santiago.betancur@pragma.com.co"
tags: ["nextjs", "react", "typescript", "app-router", "ssr", "ssg"]
last_updated: "2025-09-16"
```

## Instructions Management

### Main Modules

- [01-context.md](./01-context.md) - General project and domain context
- [02-code-guidelines.md](./02-code-guidelines.md) - Code standards and conventions
- [03-technology.md](./03-technology.md) - Next.js-specific guidelines
- [04-quality.md](./04-quality.md) - Testing and quality practices
- [05-process.md](./05-process.md) - Workflow and processes
- [99-agent-considerations.md](./99-agent-considerations.md) - AI agent guidelines

### Application Guide

**Architecture/Setup**: Load `01-context.md` + `03-technology.md`
**Component/Route Development**: Load `02-code-guidelines.md` + `03-technology.md`
**Testing/Performance**: Load `04-quality.md` + `02-code-guidelines.md`
**Process/Deployment**: Load `05-process.md`
**AI Behavior**: Load `99-agent-considerations.md`

### Priority Order

1. **Critical**: Context + Technology (`01`, `03`)
2. **High**: Code Guidelines + Quality (`02`, `04`)
3. **Medium**: Process (`05`)
4. **As Needed**: Agent Considerations (`99`)
