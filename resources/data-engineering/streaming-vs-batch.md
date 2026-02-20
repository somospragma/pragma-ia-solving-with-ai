# Streaming vs Batch: Trade-offs Profundos, Cuándo Elegir Cada Uno

Análisis detallado de streaming vs batch, incluyendo trade-offs técnicos, económicos y operacionales.

## 1. Comparativa de Características

### Latencia (Time to Insight)

| Aspecto | Batch | Streaming | Winner |
|--------|-------|-----------|--------|
| **Latency end-to-end** | 1-24 horas | 100 ms - 5 min | Streaming |
| **Data freshness** | 24h old | 2-5 min old | Streaming |
| **Historical analysis** | Hours, full history | Minutes, last N hours | Batch |
| **Real-time alerts** | No (next run) | Yes (immediate) | Streaming |

**Ejemplo real:**
- Batch: "¿Cuántos órdenes ayer?" → respuesta 24h después
- Streaming: "¿Órdenes ahora?" → respuesta < 1 segundo

---

### Complejidad de Implementación

| Aspecto | Batch | Streaming | Winner |
|--------|-------|-----------|--------|
| **Code complexity** | Simple (SQL, PySpark) | Medium-High (stateful, windows) |Batch |
| **State management** | None (stateless) | Critical (RocksDB, checkpoints) | Batch |
| **Testing** | Easy (deterministic, repeatable) | Hard (async, distributed) | Batch |
| **Debugging** | Logs + logs + logs | Distributed tracing | Batch |
| **Operational toil** | Low (cron job) | High (24/7 monitoring) | Batch |

**Ejemplo real:**
- Batch: `SELECT * FROM orders WHERE date = '2026-02-20'` (5 lines)
- Streaming: Flink state backend, checkpoint tunning, watermarking logic (500 lines)

---

### Costo

| Aspecto | Batch | Streaming | Winner |
|--------|-------|-----------|--------|
| **Compute cost** | ~$0 idle, $X on run | $Y/hour always-on | Batch |
| **Storage cost** | Cheap (archival) | Expensive (state, cache) | Batch |
| **Network cost** | Bulk transfer | Per-event transfer | Batch |
| **Monthly estimate** | $100-500 (small cluster) | $5,000-15,000 (broker + processors) | Batch |

**Ejemplo real (500 GB/day):**
```
Batch (Glue):
- Processing: 2h/day @ 10 DPU × $0.41 = $246/month
- Storage: $920/month
- Total: ~$1,150/month

Streaming (Kinesis + Flink):
- Kinesis: $870/month (per GB)
- Processors: $3,000+/month (always-on)
- Total: ~$3,900+/month (3-4x más caro)
```

---

### Escalabilidad

| Aspecto | Batch | Streaming | Ganador |
|--------|-------|-----------|--------|
| **Scale to 100 GB/day** | 10 DPU, simple | 20 shards, complex | Batch |
| **Scale to 1 TB/day** | 50 DPU, still easy | 100+ shards, hard tuning | Batch |
| **Scale to 10 TB/day** | 200 DPU, commodity | 1000+ shards, expensive | Batch |
| **Horizontal scaling** | Add DPU (linear) | Add shards + manage hotspots | Batch |

**Principio:** Streaming escala mejor **por evento** (add shards), batch escala mejor **por volumen** (add workers).

---

## 2. Arquitectura Patterns: Cuándo Usar Qué

### Pattern A: Pure Batch (Daily Warehouse Loads)

**Caso de uso:**
- Reporting (BI, dashboards with 24h lag acceptable)
- Data warehouse loads (Redshift, Snowflake)
- Historical analytics

**Arquitectura:**
```
Source (DB, API)
    ↓ [daily job]
S3 (raw)
    ↓ [Glue ETL daily]
S3 (curated) + Redshift
    ↓
BI tools (Tableau, Looker)
```

**Cost:** ~$500-1,500/month (small-medium warehouse)

**Operación:** Set-it-and-forget (cron, alerts on failure)

---

### Pattern B: Pure Streaming (Real-Time Metrics)

**Caso de uso:**
- Real-time dashboards (latency < 1 min critical)
- Fraud detection (decision < 100 ms)
- Live monitoring feeds

**Arquitectura:**
```
Events (Kafka)
    ↓ [Flink windowed aggregates]
Metrics (time-series DB)
    ↓ [Grafana, real-time dashboards]
    + [Alerting on thresholds]
```

**Cost:** ~$4,000-8,000/month (always-on processors)

**Operación:** 24/7 monitoring, on-call rotation

---

### Pattern C: Hybrid (Lambda) - Batch + Streaming

**Caso de uso:**
- Complete history (batch) + recent real-time (streaming)
- App needs both slow analytics + fast metrics
- Mixed latency requirements

**Arquitectura:**
```
Events (Kafka)
    ├→ [Streaming processor]
    │   ↓
    │   DynamoDB (last 24h)
    │
    └→ [Kinesis Firehose]
        ↓
        S3 (archival)
        ↓ [Daily Glue job]
        Redshift (historical)

App: Query Redshift (historical) + DynamoDB (recent)
```

**Cost:** ~$3,000-4,000/month (streaming overhead + batch)

**Operación:** Medium (monitor both paths)

---

### Pattern D: Kappa (Streaming-First without Batch Redundancy)

**Caso de uso:**
- Event log is source of truth (replayable)
- All analytics from one stream
- No need for batch

**Arquitectura:**
```
Events (Kafka, immutable log)
    ↓ [Flink streaming]
    ├→ Data Lake (Parquet, partitioned by time)
    ├→ Real-time store (DynamoDB for hot queries)
    └→ Warehouse (Redshift, fed by streaming)

Replay ability: re-run Flink from any timestamp
```

**Cost:** ~$2,500-3,500/month (streaming only, cheaper than Lambda)

**Operación:** Medium (monitor streaming pipeline)

---

## 3. Matriz de Decisión

### Criterio 1: Latencia Requerida

| Requisito | Recomendación |
|-----------|---|
| Hours OK (24h+) | **Batch** |
| Minutes OK (< 1 hour) | **Hybrid or Kappa** |
| Seconds required (< 10 sec) | **Streaming** |
| Milliseconds critical (< 100 ms) | **Streaming only** |

### Criterio 2: Volumen de Datos

| Volumen | Recomendación |
|--------|---|
| < 10 GB/day | Batch (simpler, cheaper) |
| 10-100 GB/day | Batch (still simple) |
| 100 GB - 1 TB/day | Hybrid (start Streaming) |
| > 1 TB/day | Streaming (batch becomes hard to scale) |

### Criterio 3: Complejidad de Lógica

| Lógica | Recomendación |
|-------|---|
| Simple (filters, aggregates) | Either (SQL is simple) |
| Medium (joins, UDFs) | Batch (easier testing) |
| Complex (stateful, windowed) | Batch first, then Streaming |
| Real-time ML model scores | **Streaming** (latency critical) |

### Criterio 4: Team Maturity

| Madurez | Recomendación |
|--------|---|
| New to data | **Batch** (Glue, dbt, simple) |
| Working with Spark | **Hybrid** (Spark Structured Streaming is good middle ground) |
| Kafka/Flink experienced | **Streaming or Kappa** |
| Fortune 500 big data | **Hybrid or Kappa** (all above) |

---

## 4. Scoring Decision Matrix

```
Latency required < 1 min?
  YES → Streaming/Hybrid
  NO → Batch

Volume > 500 GB/day?
  YES → Streaming/Hybrid
  NO → Batch (cheaper)

Real-time user-facing?
  YES → Streaming
  NO → Batch/Hybrid (batch is OK)

Team knows Spark Streaming?
  YES → Hybrid
  NO → Batch (learn Spark first)

Budget unlimited?
  YES → Streaming + Batch (best of both)
  NO → Batch (cheapest solution)
```

**Logic:**
- 3+ YES to Streaming → Choose Streaming
- 2+ YES to Batch → Choose Batch
- Mixed → Choose Hybrid

---

## 5. Implementación Step-by-Step

### Start with Batch, Upgrade if Needed

**Phase 1: Batch MVP (2-4 weeks)**
```
Source → Glue/Spark daily job → S3 + Redshift
Metrics: cost ~$500/mo, latency 24h, ops simple
```

**Phase 2: Monitor Latency Requests (ongoing)**
- User feedback: "Is 24h lag OK?"
- Metrics: Which queries need < 1 hour?

**Phase 3: Introduce Streaming (4-8 weeks if needed)**
```
Batch stays (historical)
+ Kiesis/Kafka + Flink for real-time metrics
= Hybrid architecture
```

**Phase 4: Optimize (8+ weeks)**
- If Streaming is robust, maybe drop Batch (Kappa)
- If Batch is heavily used, maybe de-emphasize Streaming

---

## 6. Casos Reales: Decisiones Tomadas

### Caso 1: Ecommerce Sales Platform
```
Requirements:
- BI dashboards (24h lag OK)
- Fraud detection (< 500 ms)
- Inventory updates (< 5 min)

Decision: HYBRID (Lambda)
- Batch: Daily sales warehouse (Glue → Redshift)
- Streaming: Fraud + inventory (Kinesis → DynamoDB)
Cost: $3,500/month
```

### Caso 2: Fintech Transaction Monitoring
```
Requirements:
- Regulatory reporting (daily)
- Real-time alerts (< 100 ms)
- Historical audit trail (all data)

Decision: KAPPA (Streaming-first)
- Kafka = event log (immutable)
- Flink = process all (replayable)
- Lake = Parquet storage
- Redshift = aggregate views
Cost: $2,800/month
Why Kappa not Lambda? Event log is regulatory requirement anyway
```

### Caso 3: Analytics Company
```
Requirements:
- Ad-hoc analyst queries (< 1 hour OK)
- No real-time requirements
- Large historical dataset (100 TB+)

Decision: BATCH
- Glue jobs (scheduled daily, hourly)
- Redshift (data warehouse)
- S3 (lake for archival)
Cost: $1,200/month
Why not Streaming? Adds complexity, not needed
```

---

## 7. Anti-Patterns (Lo que NO debes hacer)

### ❌ Anti-Pattern 1: Streaming for BI
```
DON'T:
  Events → Flink → Kafka stream → BI tool
  (Latency overkill, cost high, complexity unnecessary)

DO:
  Events → Daily Glue job → Redshift → BI tool
```

### ❌ Anti-Pattern 2: Batch for Real-Time Fraud
```
DON'T:
  Transaction → Batch job (next day) → Fraud score
  (Fraud already happened!)

DO:
  Transaction → Kafka → Flink (< 100 ms) → Fraud score → Block
```

### ❌ Anti-Pattern 3: Kappa Without Event Log
```
DON'T:
  Streaming pipeline without immutable log
  (Can't replay on bugs, missed data unrecoverable)

DO:
  Always have Kafka/S3 as event source for Kappa
```

### ❌ Anti-Pattern 4: Over-Scaling Batch
```
DON'T:
  10 TB/day with 500 DPU cluster (too expensive)
  
DO:
  10 TB/day → Consider Streaming (cheaper, faster at scale)
```

---

## 8. Checklist: Antes de Elegir

- [ ] **Latency:** Cuál es la latencia máxima aceptable?
- [ ] **Volume:** Cuántos GB/día operamos?
- [ ] **Complexity:** ¿Qué tipo de transformaciones?
- [ ] **Users:** ¿Usuarios en tiempo real o can wait?
- [ ] **Cost budget:** ¿Cuánto justifica el presupuesto?
- [ ] **Team:** ¿Qué stack conoce mi equipo?
- [ ] **Replayability:** ¿Necesito replayar datos?
- [ ] **Governance:** ¿Auditoría/compliance requirements?

---

## Referencias

- AWS Well-Architected (Analytics): https://docs.aws.amazon.com/architecture/
- Apache Kafka vs Batch: https://kafka.apache.org/use-cases
- Flink Documentation: https://nightlies.apache.org/flink/
- **Instrucciones:** `instructions_or_rules/data-engineering/modular/03-technology.md` (Sección 3.1-3.3)
- **Resource (Tier 1):** `resources/data-engineering/data-architecture-patterns.md` (Lambda vs Kappa patterns)
