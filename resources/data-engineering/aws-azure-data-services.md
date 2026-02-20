# AWS vs Azure: Data Services - Comparativa, Criterios de Decisión, Migración

Guía detallada de servicios de datos en AWS y Azure, incluyendo mapeos, trade-offs y criterios de decisión.

## 1. Mapeo de Servicios (Quick Reference)

### Ingesta & Streaming

| Caso de Uso | AWS | Azure | Consideraciones |
|-------------|-----|-------|-----------------|
| Event streaming (Kafka-like) | **Kinesis Data Streams** | **Event Hubs** | KDS: cheaper per-GB, EH: mejor integration con Synapse |
| Complex event processing | **Kinesis Data Analytics** (Flink) | **Stream Analytics** | KDA: full Flink, SA: SQL-only |
| CDC desde DB | **AWS DMS** o **Debezium/MSK** | **Data Factory Copy Activity** + CDC | DMS: managed, Debezium: más control |
| IoT / Device data | **IoT Core + Kinesis** | **IoT Hub + Event Hubs** | Similares en feature, IoT Hub: mejor device management |

### Almacenamiento

| Caso de Uso | AWS | Azure | Consideraciones |
|-------------|-----|-------|-----------------|
| Object storage (Data Lake) | **S3** | **ADLS Gen2** (blob) | S3: más maduro, ADLS: integrado con Synapse |
| Data Warehouse (OLAP) | **Redshift** | **Synapse Analytics** (SQL Pool) | Redshift: mejor BI, Synapse: mejor integración Spark |
| Lakehouse (on DF) | **Delta Lake on S3** | **Delta Lake on ADLS** | Mismo motor, storage distinto |
| Catalog/Metadata | **Glue Data Catalog** | **Purview** (metadata) | Glue: más features, Purview: gov/compliance |

### Procesamiento

| Caso de Uso | AWS | Azure | Consideraciones |
|-------------|-----|-------|-----------------|
| Batch (Spark) | **Glue ETL Jobs** | **Synapse Spark Pool** | Glue: simpler, Synapse: más integración |
| Stream (Spark Structured) | **Kinesis + EMR/Glue streaming** | **Event Hubs + Synapse Spark** | Similar experiencia |
| ML/Advanced analytics | **SageMaker** | **Databricks** (partner) | SageMaker: más completo, Databricks: multicloud |
| Orchestration (DAGs) | **MWAA** (Airflow managed) | **Data Factory** (pipelines) | MWAA: Airflow standard, DF: proprietary |
| Serverless compute | **Lambda** + **Athena** | **Functions** + **Serverless SQL Pool** | Lambda: < 3 sec, Functions: < 10 min |

---

## 2. Escenarios: Cuándo Usar Qué

### Escenario A: Data Lake Modern (Raw → Curated → Serving)

**AWS:**
```
S3 (raw) → Glue Catalog (metadata)
    ↓
Glue ETL (transformación) → S3 (curated)
    ↓
Glue Catalog + Athena (BI queries)
    ↓
Redshift (serving/BI)
```

**Azure:**
```
ADLS Gen2 (raw) → Purview (metadata)
    ↓
Synapse Spark Pool (transformation) → ADLS (curated)
    ↓
Synapse Serverless SQL (BI queries via Lakehouse)
    ↓
Synapse SQL Pool (serving/BI) [opcional si OLAP pesado]
```

**Diferencias clave:**
| Aspecto | AWS | Azure |
|--------|-----|-------|
| Integración | Modular (3 servicios) | Monolítica (1 plataforma) |
| Costo | Pay-per-run (Glue) | Pay-per-node (Synapse) |
| Latencia queries | < 5 sec (Athena) | < 2 sec (Synapse) |
| Governance | Glue Tags + Lake Formation | Purview natively |

**Decisión:** AWS si queries `ad-hoc` + cost-sensitive; Azure si queries `frecuentes` + OLAP pesado.

---

### Escenario B: Real-Time Streaming (eventos → metrics)

**AWS:**
```
Kinesis Data Streams (ingest)
    ↓
Kinesis Data Analytics (KDA, Flink) → windowed aggregates
    ↓
DynamoDB (state) / Kinesis Firehose → S3 + Redshift
    ↓
CloudWatch Metrics / Dashboard
```

**Azure:**
```
Event Hubs (ingest)
    ↓
Stream Analytics (SQL queries) → windowed aggregates
    ↓
Cosmos DB (state) / Event Hubs → ADLS + Synapse
    ↓
Application Insights / Power BI
```

**Diferencias clave:**
| Aspecto | AWS | Azure |
|--------|-----|-------|
| Lag end-to-end | 200-500 ms | 100-300 ms |
| Language support | Scala, Java, Python (Flink) | SQL only (Stream Analytics) |
| Cost model | Shard-hours + GB | Streaming Units |
| Backpressure | Manual (scale shards) | Automatic |

**Decisión:** AWS si lógica compleja (Flink); Azure si SQL-only + simple metrics.

---

### Escenario C: Batch + Real-Time (Lambda Architecture)

**AWS:**
```
S3 (raw) ← Kinesis ← Sources
    ↓
Glue ETL (batch daily) → Redshift
+ Kinesis → Lambda/EMR (real-time) → DynamoDB
    ↓
App reads Redshift + DynamoDB (merged view)
```

**Azure:**
```
ADLS (raw) ← Event Hubs ← Sources
    ↓
Synapse Spark (batch daily) → Synapse SQL
+ Event Hubs → Cosmos DB (real-time)
    ↓
App reads Synapse + Cosmos DB
```

**Cost Estimate (100 GB/day, 1000 events/sec):**

| AWS | Azure |
|-----|-------|
| Kinesis: $180/month (2 shards) | Event Hubs: $200/month (2 TUs) |
| Glue ETL: $0.44/DPU-hour × 120 h ≈ $53 | Synapse Spark: $2/node × 4 nodes × 120 h ≈ $960 |
| DynamoDB: $25/month | Cosmos DB: $100/month |
| Redshift: $600/month (ra3) | Synapse SQL: $800/month (100 DWU) |
| **Total ≈ $857/month** | **Total ≈ $2,060/month** |

**Decisión:** AWS sobretodo por costo; Azure si ya tienes Synapse licenses.

---

## 3. Criterios de Decisión: AWS vs Azure

### Matriz de Decisión

| Criterio | Preferencia | Puntuación |
|----------|-------------|-----------|
| **Tenemos SQL Server on-prem** | Azure | +5 |
| **Usamos .NET/Power BI** | Azure | +3 |
| **Queremos máxima flexibilidad (Spark/Flink)** | AWS | +5 |
| **Necesitamos Lakehouse (Delta Lake)** | AWS | +2 |
| **Govern/compliance crítico** | Azure (Purview) | +3 |
| **Cost-sensitive (low query frequency)** | AWS (Athena) | +4 |
| **OLAP queries frecuentes (< 5 min)** | Azure (Synapse) | +3 |
| **Machine Learning (SageMaker vs ML Services)** | AWS | +2 |
| **Existing AWS footprint** | AWS | +5 |
| **Existing Azure footprint** | Azure | +5 |

**Cálculo:** Suma scores. > 10 → AWS; < -10 → Azure; -10 a 10 → depende.

---

## 4. Arquitectura Híbrida (On-Prem ↔ Cloud)

### On-Prem → AWS

**Opción A: Direct Connect + S3 Transfer Acceleration**
```
On-Prem DB (Oracle/MySQL)
    ↓ [AWS DMS, CDC via Debezium]
AWS Direct Connect (private, low-latency)
    ↓
S3 (raw zone) + Kinesis (streaming)
    ↓
Glue ETL transforms
    ↓
Redshift (serving)
```

**Cost:** Direct Connect $0.30/hour + data transfer $0.02/GB

**Opción B: Snowball (batch, alto volumen)**
```
Terabytes in on-prem DB
    ↓ [Export to CSV/Parquet]
AWS Snowball (physical device)
    ↓ [Ship to AWS data center]
S3 (raw)
    ↓ [Glue processes]
```

**Cost:** $200/Snowball (50 TB) + $0.005/GB within AWS

### On-Prem → Azure

**Opción A: ExpressRoute + Data Box**
```
On-Prem DB (SQL Server)
    ↓ [Azure Data Factory + CDC]
Azure ExpressRoute (private)
    ↓
ADLS Gen2 (raw)
    ↓
Synapse Spark (transforms)
    ↓
Synapse SQL (serving)
```

**Cost:** ExpressRoute $0.30/hour (1 Gbps) + data transfer in: free, out: $0.12/GB

**Opción B: Azure Data Box (batch, alto volumen)**
```
Terabytes in on-prem
    ↓ [Export via SMB]
Azure Data Box (appliance)
    ↓ [Ship to Azure]
ADLS (raw)
    ↓ [Synapse processes]
```

**Cost:** $165/Data Box (100TB) + $0.012/GB egress after

---

## 5. Migración: On-Prem Warehouse → Cloud

### Fases

**Fase 1: Assessment (2-4 semanas)**
- Mapeo de schemas, cargas, frecuencias
- Identificar transformaciones (SQL, procedimientos)
- Estimar volumen y presupuesto

**Fase 2: Proof of Concept (4-6 semanas)**
- Replicar 1-2 tablas críticas
- Ejecutar queries comparativas (performance, cost)
- Validar data lineage y governance

**Fase 3: Pilot (8-12 semanas)**
- Migrar 30% de datos y pipelines
- Teste con producción en paralelo
- Monitorear desempeño e issues

**Fase 4: Full Migration (12-16 semanas)**
- Migrar resto de datos
- Cutover (switch de fuente de verdad)
- Decommission on-prem

### Timeline Example: SQL Server → Synapse

| Hito | Semana | AWS Alt | Azure |
|------|--------|---------|-------|
| Assessment | 1-2 | DMS Inventory | Data Migration Assistant (DMA) |
| POC | 3-6 | Glue + Athena trial | Synapse SQL Pool trial |
| Data sync | 7-14 | AWS DMS (continuous) | Data Factory (continuous) |
| Pivot apps | 15-16 | Update connection strings | Update ODBC/connectors |
| Validate | 17-20 | Query parity tests | Query parity tests |
| Go-live | 21-22 | Switch off on-prem | Switch off on-prem |

---

## 6. Costo Detallado: Ejemplo 1 TB/día

### AWS (Redshift + Athena + Glue)

```
Ingesta:
  - Kinesis Firehose: 1 TB/day → S3 delivery
    Cost: 1000 GB × $0.029 = $29/day = $870/month

Procesamiento:
  - Glue ETL: 2h/day @ 10 DPUs × $0.41 = $8.20/day = $246/month
  - Athena queries: 100 queries/day, avg 2 TB scanned = $10/day = $300/month

Almacenamiento:
  - S3 (raw): 30 TB × $0.023 = $690/month
  - S3 (curated): 10 TB × $0.023 = $230/month
  - Redshift: 16-node ra3.4xlplus = $800/month

TOTAL AWS ≈ $3,136/month
```

### Azure (Event Hubs + Synapse + ADLS)

```
Ingesta:
  - Event Hubs: 1 TB/day = 1000 KB/s peak, need ~5 TUs
    Cost: 5 TUs × $111.5 = $557.50/day = $16,725/month

Procesamiento:
  - Synapse Spark: 4 nodes × 2h/day × $2/node-hour = $16/day = $480/month
  - Synapse SQL: 200 DWU × $1.52/hr × 5 h/day = $38/day = $1,140/month

Almacenamiento:
  - ADLS Gen2: 30 TB × $0.0184 = $552/month
  - Synapse: 200 DWU base = $1,140/month

TOTAL Azure ≈ $20,537/month (SIN Event Hubs concurrency)
```

**Conclusión:** AWS 6.5x más barato para este caso.

---

## 7. Criterios Finales: Así que Chose?

### Elige AWS si:
- Cost-sensitive (especialmente queries `ad-hoc` con Athena)
- Necesitas máxima flexibilidad (Spark, Flink, Lambda)
- Datos históricos largos (lakehouse con Delta)
- Streaming complejo (KDA + Flink)
- Ya tienes infraestructura AWS

### Elige Azure si:
- Tienes SQL Server / .NET on-prem
- Necesitas integración Power BI/Office 365
- OLAP queries frecuentes (Synapse SQL)
- Governance/compliance crítico (Purview)
- Ya tienes suscripción Azure

### Considera Ambos (Multicloud):
- 70/30 split: 70% en AWS (cost), 30% en Azure (strategic)
- Usar herramientas agnósticas: Apache Spark, Delta Lake, dbt, Airflow
- CDC + replicación cross-cloud para synchronization

---

## Referencias

- **AWS Pricing:** https://aws.amazon.com/pricing/
- **Azure Pricing:** https://azure.microsoft.com/en-us/pricing/
- **AWS Well-Architected (Data):** https://docs.aws.amazon.com/wellarchitected/
- **Azure Well-Architected (Data):** https://learn.microsoft.com/en-us/azure/well-architected/
- **Instrucciones:** `instructions_or_rules/data-engineering/modular/03-technology.md` (Sección 3.5-3.6)
- **Recurso (Tier 1):** `resources/data-engineering/data-architecture-patterns.md` (Patrones generales)
