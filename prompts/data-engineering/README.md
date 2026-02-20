# Data Engineering - Prompts

Prompts reutilizables para tareas comunes de ingeniería de datos, organizados por nivel de complejidad.

---

## 🎯 Tier 1: Fundamentals
**Aprende:** Principios básicos de validación y calidad de datos.

### 📋 Disponibles (Tier 1)

### [data-pipeline-validation.md](./data-pipeline-validation.md)
**Propósito:** Validar pipelines contra reglas críticas: idempotencia, contratos de datos, observabilidad.

**Usa cuando:**
- Necesitas feedback en código de Spark/Flink/dbt antes de deploy
- Quieres verificar que el pipeline es idempotente
- Buscas confirmar que hay contratos de datos bien definidos

**Ejemplo de uso en Copilot:**
```
/data-pipeline-validation

Revisa mi job de Glue. El código está aquí: [pegar código]
¿Es idempotente? ¿Tiene observabilidad estructurada?
```

---

### [data-quality-review.md](./data-quality-review.md)
**Propósito:** Revisar cobertura de validaciones de datos, expectations, y DQ gates.

**Usa cuando:**
- Estás configurando Great Expectations o Deequ
- Necesitas asegurar que tus data quality gates son suficientes
- Quieres validar edge cases (nulls, encoding, distributions)

**Ejemplo de uso en Copilot:**
```
/data-quality-review

Aquí están mis expectations de GE. ¿Cubro todos los edge cases?
¿Puedo tener anomalías sin que fallen mis checks?
```

---

---

## ⚡ Tier 2: Advanced
**Aprende:** Performance, incidents, y optimizaciones avanzadas.

### [performance-optimization.md](./performance-optimization.md)
**Propósito:** Analizar y optimizar performance en pipelines. Identifica skew, particionado, query plans.

**Usa cuando:**
- Tu job Spark está lento o usa demasiados recursos
- Necesitas diagnosticar cuello de botella (CPU, I/O, memory spill)
- Quieres propuestas de optimización con impacto estimado

**Ejemplo de uso en Copilot:**
```
/performance-optimization

Mi job tarda 4 horas hoy vs 30 min hace una semana.
Datos crecieron de 100GB a 500GB. ¿Cómo optimizo?
```

---

### [incident-triage.md](./incident-triage.md)
**Propósito:** Diagnosticar y mitigar incidentes: datos faltantes, schema drift, degradación.

**Usa cuando:**
- Un pipeline explotó en producción
- Necesitas respuesta rápida (on-call)
- Seguir checklist estructurada vs improvisar

**Ejemplo de uso en Copilot:**
```
/incident-triage

Pipeline de ventas no entregó datos hoy. 
Última ejecución fue ayer a las 3 AM.
Sintoniza un plan de acción ahora.
```

---

### [airflow-dag-design.md](./airflow-dag-design.md)
**Propósito:** Validar DAGs de Airflow: estructura, operadores, XCom, retries, seguridad, observabilidad.

**Nota especial:** Este prompt es específico para Airflow/MWAA. **Para validación agnóstica de DAGs/Pipelines en múltiples plataformas (Airflow, Data Factory, Synapse), usa [pipeline-orchestration-design.md](./pipeline-orchestration-design.md).**

**Usa cuando:**
- Diseñas o revisas un DAG de Airflow antes de deploy
- Necesitas mejorar idempotencia o error handling
- Quieres validar configuración de retries, SLAs y alertas
- Tu contexto es AWS Airflow/MWAA

**Ejemplo de uso en Copilot:**
```
/airflow-dag-design

Tengo este DAG en Airflow. ¿Está listo para producción?
¿Hay problemas con XCom o retries?
```

---

### [pipeline-orchestration-design.md](./pipeline-orchestration-design.md)
**Propósito:** Validar diseño de pipelines de orquestación: DAGs (Airflow), Pipelines (Data Factory), Synapse Pipelines. **Agnóstico a plataforma.**

**Usa cuando:**
- Necesitas validación genérica para múltiples plataformas (AWS + Azure)
- Tienes Airflow Y Data Factory en tu arquitectura
- Quieres reglas de estructura/confiabilidad/observabilidad aplicables a cualquier orquestador
- No necesitas detalles específicos de sintaxis de cada plataforma

**Ejemplo de uso en Copilot:**
```
/pipeline-orchestration-design

Tengo un pipeline en Airflow y otro en Data Factory.
¿Me puedes validar ambos con los mismos criterios de confiabilidad?
```

**Contenido:** Estructura agnóstica + ejemplos específicos por plataforma (Airflow, Data Factory, Synapse).

---

### [glue-job-troubleshooting.md](./glue-job-troubleshooting.md)
**Propósito:** Diagnosticar y resolver problemas operacionales de ETL jobs: timeouts, hangs, OOM, state management (agnóstico de plataforma: AWS Glue, Azure Synapse, Data Factory).

**Usa cuando:**
- ETL job está "colgado" en ejecución pero logs muestran que falló (state discrepancy)
- Job es lento (duración aumentó 4x) sin errores visibles
- Hay OOM (Out of Memory) o task timeouts
- Output tiene duplicados (state management/checkpoint issues)
- Necesitas diagnóstico estructurado sin entrar en comandos específicos de plataforma

**Ejemplo de uso en Copilot:**
```
/glue-job-troubleshooting

Mi job de Glue/Synapse lleva 2 horas en RUNNING, pero logs muestran que falló hace 1 hora.
No veo error claro. ¿Qué está pasando?
```

**Nota:** Agnóstico a plataforma. Incluye ejemplos de AWS Glue, Azure Synapse Spark, y Azure Data Factory para patrones equivalentes.

---

### [glue-job-validation.md](./glue-job-validation.md)

**Usa cuando:**
- Diseñas o revisas un Glue job antes de deploy
- Necesitas validar que es config-driven (no hardcoded)
- Quieres asegurar que se puede reutilizar para otras tablas
- Validas transformaciones (flatten, type casting, null handling)

**Contenido:**
- Reglas para jobs dinámicos (YAML-based configuration)
- Patrones Extract, Transform, Load (ETL)
- Validación de schema, transformaciones, manejo de errores
- Checklist: from declarativa config → reutilizable

**Ejemplo de uso en Copilot:**
```
/glue-job-validation

Revisa mi job de Glue para procesar tablas DynamoDB.
¿Es reutilizable para otras tablas? ¿Cómo agrego nueva tabla sin código?
```

---

## 🚀 Tier 3: Specialized
**Aprende:** Diseño de contracts, decisiones de arquitectura, automatización.

### [data-contract-design.md](./data-contract-design.md)
**Propósito:** Diseñar data contracts completos desde cero, con schemas, SLAs, versionado y gobernanza.

**Usa cuando:**
- Necesitas crear un contrato para un nuevo dataset/tabla
- Quieres mejorar contracts existentes con SLAs/versionado
- Estás onboarding un nuevo equipo a data contracts
- Pre-launch validation para nuevos productos de datos

**Contenido:**
- 6 pasos estructurados: descubrimiento → schema → SLA → versioning → governance → testing
- Templates YAML completos (simple + complex)
- Ejemplos reales (órdenes, clientes, transacciones)
- Testing strategy (unit + contract + DQ)

**Ejemplo de uso en Copilot:**
```
/data-contract-design

Diseña un contrato para mi tabla de transacciones.
Tengo order_id, customer_id, amount, status, created_date.
Necesito 2h de freshness y SLAs claros.
```

**Relación:** Extiende `resources/data-engineering/data-contract-patterns.md` (Tier 1) con metodología práctica de diseño

---

## 📚 Relación General con Otros Recursos

| Necesitas... | Mira... |
|--------------|----------|
| Entender arquitectura (Lambda/Kappa) | `resources/data-engineering/data-architecture-patterns.md` (Tier 1) |
| Diseñar contracts | `resources/data-engineering/data-contract-patterns.md` (Tier 1) + este prompt (Tier 3) |
| Implementar testing completo | `resources/data-engineering/testing-data-pipelines.md` (Tier 2) |
| Comparar AWS vs Azure | `resources/data-engineering/aws-azure-data-services.md` (Tier 2) |
| Entender streaming vs batch | `resources/data-engineering/streaming-vs-batch.md` (Tier 3) |
| Instrucciones detalladas | `instructions_or_rules/data-engineering/` |

---

## 🚀 Quick Start
1. **Principiante:** Lee Tier 1 (validation + quality)
2. **Implementador:** Usa Tier 2 (performance + incidents + testing)
3. **Arquitecto:** Consulta Tier 3 (decisions + design) + chat mode
