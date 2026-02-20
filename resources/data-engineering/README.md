# Data Engineering - Resources

Documentación técnica de referencia para patrones, decisiones de arquitectura y estándares de Data Engineering, organizados por nivel de complejidad.

---

## 🎯 Tier 1: Fundamentals
**Aprende:** Patrones arquitectónicos y diseño de contracts.

## 📚 Disponibles (Tier 1)

### [data-architecture-patterns.md](./data-architecture-patterns.md)
**Scope:** Patrones arquitectónicos: Lambda, Kappa, Medallion (Raw-Curated-Serving).

**Cubre:**
- Cuándo usar Lambda vs Kappa (matriz de decisión)
- Medallion architecture: qué va en cada zona
- Ejemplos: AWS Glue, Azure Synapse, Databricks
- Hybrid: Medallion + Kappa recomendado

**Lee cuando:**
- Estás diseñando un nuevo pipeline y dudas entre batch/streaming
- Necesitas entender cómo organizar datos (raw/curated/serving)
- Quieres guía de AWS vs Azure

**Tamaño:** ~4.5 KB, lectura ~15 min

---

### [data-contract-patterns.md](./data-contract-patterns.md)
**Scope:** Diseño de Data Contracts: anatomía, versionado, compatible vs breaking changes.

**Cubre:**
- Estructura completa de un contract (schema, SLAs, changelog)
- Forward/backward compatibility: qué es safe, qué es breaking
- Versionado semántico para schemas
- Timeline para cambios breaking
- Ejemplos: Git + Schema Registry
- SLA enforcement (freshness, completeness, accuracy, availability)

**Lee cuando:**
- Vas a cambiar un schema y necesitas no romper consumidores
- Definieres SLAs para datasets
- Quieres entender Data Contracts best practices

**Tamaño:** ~5 KB, lectura ~20 min

---

---

## ⚡ Tier 2: Advanced
**Aprende:** Testing, performance, decisiones cloud.

### [testing-data-pipelines.md](./testing-data-pipelines.md)
**Scope:** Testing completo: unit tests, contract tests, integration tests, DQ gates, CI/CD.

**Cubre:**
- Pirámide de testing (unit ~75%, integration ~20%, E2E ~5%)
- Patrones concretos: test transformations, contract tests, schema validation
- Integration tests con sample data (fixtures)
- Great Expectations checkpoints en CI
- GitHub Actions workflow ejemplo
- Métricas de monitoreo post-deploy

**Lee cuando:**
- Necesitas setup completo de testing para tu pipeline
- Quieres aumentar confianza antes de deploy
- Buscas reducir incidentes (testing previene bugs)

**Tamaño:** ~6 KB, lectura ~20 min

---

### [aws-azure-data-services.md](./aws-azure-data-services.md)
**Scope:** Comparativa AWS vs Azure: servicios, costs, criterios de decisión, migración.

**Cubre:**
- Mapeo 1-a-1 de servicios (Kinesis ↔ Event Hubs, Glue ↔ Synapse, etc)
- 3 escenarios reales: Data Lake, Streaming, Lambda
- Cost estimates detallados (100 GB/day, 1 TB/day)
- Criterios de decisión (matriz scoring)
- Arquitectura híbrida (on-prem ↔ cloud)
- Timeline de migración (on-prem warehouse → cloud)

**Lee cuando:**
- Evaluando si AWS o Azure para nuevo proyecto
- Planificando migración desde on-prem
- Necesitas cost estimates para steering
- Quieres entender trade-offs específicos

**Tamaño:** ~7 KB, lectura ~25 min

---

## � Disponibles (Tier 3)



## �🎯 Cómo Usar en Conversaciones

### Ejemplo 1: "¿Medallion architecture?"
```
→ Abre data-architecture-patterns.md
→ Busca "Medallion Architecture"
→ Lee: qué va en raw, curated, serving
→ Aplica a tu proyecto
```

### Ejemplo 2: "Cómo cambio un schema sin romper"
```
→ Abre data-contract-patterns.md
→ Busca "Compatible vs Incompatible"
→ Sigue timeline (8 semanas para breaking)
→ Usa template de comunicación
```

---

**Ver instrucciones modulares:** [instructions_or_rules/data-engineering/](../../instructions_or_rules/data-engineering/)
