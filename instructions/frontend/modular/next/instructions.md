# Instructions Orchestrator — Next.js Project

```yaml
name: "Next.js Project"
version: "2.0"
applies_to: ["frontend", "nextjs", "react", "typescript"]
status: "Active"
context_optimization: true
ai_agent_optimized: true
authors:
  - name: "Burke Holland"
    email: "burkeholland@gmail.com"
  - name: "Santiago Betancur"
    email: "santiago.betancur@pragma.com.co"
tags: ["nextjs", "react", "typescript", "app-router", "ssr", "ssg"]
last_updated: "2025-09-15"
```

## 🎯 Context-Optimized Instructions Management

This orchestrator uses **task-context mapping** to ensure AI agents load only relevant instructions for specific development scenarios, optimizing context window usage for Next.js App Router development.

### Main Modules

- [01-context.md](./01-context.md) - General project and domain context
- [02-code-guidelines.md](./02-code-guidelines.md) - Code standards and conventions
- [03-technology.md](./03-technology.md) - Specific technical guidelines
- [04-quality.md](./04-quality.md) - Quality and testing practices
- [05-process.md](./05-process.md) - Workflow and processes
- [99-agent-considerations.md](./99-agent-considerations.md) - Additional considerations for AI agents

### Application Guide

1. **For new projects or architecture**: Consult `01-context.md` and `03-technology.md` first
2. **For component/route implementation**: Follow `02-code-guidelines.md` and relevant sections of `03-technology.md`
3. **For testing strategy and implementation**: Refer to `04-quality.md`
4. **For code review and PR preparation**: Use `05-process.md`
5. **For AI agent behavior**: Consult `99-agent-considerations.md`

### Priority Implementation Order

1. **Critical**: Context & Architecture (`01-context.md`, `03-technology.md`)
2. **High**: Code Guidelines (`02-code-guidelines.md`), Quality & Testing (`04-quality.md`)
3. **High**: Process & Workflow (`05-process.md`)
4. **As Needed**: Agent Considerations (`99-agent-considerations.md`)
