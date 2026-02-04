# Instructions Orchestrator — {{PROJECT_NAME}}

```yaml
name: "{{PROJECT_NAME}}"
version: "1.0"
applies_to: ["frontend", "backend", "mobile"] # Adapt if needed
status: "Active"
authors:
  - name: "{{AUTHOR_NAME}}"
    email: "{{EMAIL}}"
tags: ["{{TECHNOLOGY_1}}", "{{TECHNOLOGY_2}}"] # OPTIONAL
last_updated: "{{YYYY-MM-DD}}"
```

## Instructions Management

This project organizes instructions into specific modules that should be consulted according to the context:

### Main Modules

- [01-context.md](./01-context.md) - General project and domain context
- [02-code-guidelines.md](./02-code-guidelines.md) - Code standards and conventions
- [03-technology.md](./03-technology.md) - Specific technical guidelines
- [04-quality.md](./04-quality.md) - Quality and testing practices
- [05-process.md](./05-process.md) - Workflow and processes
- [06-operations.md](./06-operations.md) - Observability and operations
- [99-agent-considerations.md](./99-agent-considerations.md) - Additional considerations for AI agents

### Application Guide

1. **For new architecture or directory structure**: Consult `03-technology.md` first
2. **For code implementation**: Follow `02-code-guidelines.md` and the relevant sections of `03-technology.md`
3. **For testing and validation**: Refer to `04-quality.md`
4. **For PR and commit preparation**: Use `05-process.md`
5. **For instrumentation and monitoring**: Apply `06-operations.md`
