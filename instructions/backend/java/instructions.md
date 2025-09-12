# Instructions Orchestrator — Java Best Practices

```yaml
name: "Java Best Practices"
version: "1.0"
applies_to: ["backend", "api", "microservices"]
status: "Active"
authors:
  - name: "Java Best Practices Community"
    email: "******"
tags: ["java", "spring-boot", "backend", "api", "microservices", "docker", "security"]
last_updated: "2024-01-24"
```

## Instructions Management
This project organizes Java best practices into specific modules that should be consulted according to the development context:

### Main Modules
- [00-test-execution-validation.md](./00-test-execution-validation.md) - **TEST EXECUTION VALIDATION - HIGHEST PRIORITY**
- [00-critical-validation.md](./00-critical-validation.md) - **CRITICAL VALIDATION RULES - HIGHEST PRIORITY**
- [01-architecture.md](./01-architecture.md) - Project architecture and structure patterns
- [02-error-handling.md](./02-error-handling.md) - Error handling strategies and patterns
- [03-code-style.md](./03-code-style.md) - Code style and patterns guidelines
- [04-testing-quality.md](./04-testing-quality.md) - Testing and quality assurance practices
- [05-production.md](./05-production.md) - Production deployment and operations
- [06-security.md](./06-security.md) - Security best practices and guidelines
- [07-performance.md](./07-performance.md) - Performance optimization guidelines
- [08-docker.md](./08-docker.md) - Docker and containerization practices
- [09-imports.md](./09-imports.md) - Module import and resolution guidelines

### Application Guide
1. **ALWAYS FIRST**: Apply `00-test-execution-validation.md` - Execute tests for every change
2. **ALWAYS SECOND**: Apply `00-critical-validation.md` - Verify context and get approvals
2. **For new projects or architecture**: Consult `01-architecture.md`
3. **For error handling implementation**: Follow `02-error-handling.md`
4. **For code implementation**: Apply `03-code-style.md` and `09-imports.md` guidelines
5. **For testing strategy**: Refer to `04-testing-quality.md`
6. **For production deployment**: Use `05-production.md` and `08-docker.md`
7. **For security implementation**: Apply `06-security.md` throughout development
8. **For performance optimization**: Consult `07-performance.md`

### Priority Implementation Order
1. **TEST EXECUTION VALIDATION**: Always apply (00-test) first - Execute and validate tests
2. **CRITICAL VALIDATION**: Always apply (00-critical) second - Context verification and approvals
3. **Critical**: Architecture (01), Error Handling (02), Security (06)
3. **High**: Code Style (03), Imports (09), Testing (04), Production (05)
4. **Medium**: Docker (08), Performance (07)