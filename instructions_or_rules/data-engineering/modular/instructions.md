```yaml
name: "MCP - Ingeniería de Datos (Orquestador)"
version: "1.0"
applies_to: ["data-engineering"]
status: "Active"
authors:
  - name: "Data Engineering Chapter"
tags: ["data-engineering","etl","streaming","lakes","warehouses","governance"]
last_updated: "2026-02-19"
```

## Instructions Management

### Main Modules

- [01-context.md](./01-context.md) - Contexto y alcance del proyecto
- [02-guidelines.md](./02-guidelines.md) - Reglas de codificación y arquitectura de pipelines
- [03-technology.md](./03-technology.md) - Tecnologías, conectores y formatos recomendados
- [04-quality.md](./04-quality.md) - Calidad, testing y gates
- [05-airflow.md](./05-airflow.md) - Airflow & MWAA: Implementation, deployment y operaciones
- [06-process.md](./06-process.md) - Despliegue, IaC y operación
- [99-agent-considerations.md](./99-agent-considerations.md) - Consideraciones para agentes de IA
- [streaming-ingest-checklist.md](./streaming-ingest-checklist.md) - Checklist para ingestas en streaming
- [batch-ingest-checklist.md](./batch-ingest-checklist.md) - Checklist para ingestas batch
- [hybrid-architecture-checklist.md](./hybrid-architecture-checklist.md) - Checklist para arquitecturas híbridas

### Context Selection by Task

**Architecture/Platform**: Load `01-context.md` + `03-technology.md`
**Pipeline Implementation**: Load `02-guidelines.md` + `04-quality.md`
**Deployment/Operations**: Load `06-process.md` + `04-quality.md`
**AI Assistance / Agents**: Load `99-agent-considerations.md`

### Priority Order

1. **Critical**: Context + Technology (`01`, `03`)
2. **High**: Guidelines + Quality (`02`, `04`)
3. **Medium**: Process (`05`)
4. **As Needed**: Agent Considerations (`99`)

### Platform Focus

- **Este MCP se especializa en tecnologías AWS y Azure.**
- Las decisiones de diseño y selección de servicios deben seguir los principios del Well-Architected Framework de cada proveedor, con un enfoque en soluciones de datos.
  - AWS Well-Architected: https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html
  - Azure Well-Architected: https://learn.microsoft.com/en-us/azure/well-architected/what-is-well-architected-framework

Al documentar tecnologías y patrones en `03-technology.md`, indicar claramente las recomendaciones por proveedor y las correspondencias entre servicios (por ejemplo, S3 ↔ ADLS, Glue/EMR ↔ Synapse/Databricks).
