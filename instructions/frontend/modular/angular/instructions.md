# Instructions Orchestrator — Angular Project

```yaml
name: "Angular Project"
version: "2.0"
applies_to: ["frontend", "angular", "typescript"]
status: "Active"
context_optimization: true
ai_agent_optimized: true
authors:
  - name: "Jaime Gallo"
    email: "jaime.gallom@pragma.com.co"
  - name: "Cristian Otálora"
    email: "cristian.otalora@pragma.com.co"
  - name: "Esteban García"
    email: "esteban.garcia@pragma.com.co"
tags: ["angular", "typescript", "tailwind", "sass", "standalone-components", "signals"]
last_updated: "2025-09-15"
```

## 🎯 Context-Optimized Instructions Management

This orchestrator uses **task-context mapping** to ensure AI agents load only relevant instructions for specific development scenarios, optimizing context window usage.

### Main Modules

- [01-context.md](./01-context.md) - General project and domain context
- [02-code-guidelines.md](./02-code-guidelines.md) - Code standards and conventions
- [03-technology.md](./03-technology.md) - Specific technical guidelines
- [04-quality.md](./04-quality.md) - Quality and testing practices
- [05-process.md](./05-process.md) - Workflow and processes
- [99-agent-considerations.md](./99-agent-considerations.md) - Additional considerations for AI agents

### Application Guide

1. **For new projects or architecture**: Consult `01-context.md` and `03-technology.md` first
2. **For component/service implementation**: Follow `02-code-guidelines.md` and relevant sections of `03-technology.md`
3. **For testing strategy and implementation**: Refer to `04-quality.md`
4. **For code review and PR preparation**: Use `05-process.md`
5. **For AI agent behavior**: Consult `99-agent-considerations.md`

### Priority Implementation Order

1. **Critical**: Context & Architecture (`01-context.md`, `03-technology.md`)
2. **High**: Code Guidelines (`02-code-guidelines.md`), Quality & Testing (`04-quality.md`)
3. **High**: Process & Workflow (`05-process.md`)
4. **As Needed**: Agent Considerations (`99-agent-considerations.md`)
