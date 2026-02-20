# Data Architecture Patterns: Lambda vs Kappa, Medallion, Raw-Curated-Serving

Este documento describe patrones arquitectónicos para pipelines de datos, facilitando decisiones de diseño basadas en requisitos de latencia, complejidad operacional y costo.

## 1. Lambda Architecture (Batch + Streaming)

### Cuándo usarla
- Histórico importante y análisis en tiempo real simultáneamente.
- Distintas herramientas por capa (Spark Batch + Kafka Stream).
- Entorno organizacional que demanda máxima documentación (más capas = más visibilidad).

### Estructura
```
Source → Kafka → [Batch Layer] → HDFS/S3 (batch views)
              ↓
            [Speed Layer] → Redis/Kafka output (real-time views)
              ↓
         [Serving Layer] → App/Dashboard (merge batch + real-time)
```

### Ventajas
- ✅ Análisis complejos en batch con Spark SQL.
- ✅ Retroalimentación rápida vía speed layer.
- ✅ Histórico completo sin purgas.

### Desventajas
- ❌ 2 DAGs para mantener → duplicación de lógica.
- ❌ Merge de vistas batch + time es complejo (problema de "convergencia").
- ❌ Costo operacional: 2 frameworks, 2 pipelines.

### Ejemplo Real: AWS
- Batch: Glue ETL job diario (S3 → Redshift).
- Speed: Kinesis → Lambda → DynamoDB.
- Serving: Redshift + API (query Redshift + cache en DynamoDB).

---

## 2. Kappa Architecture (Streaming First)

### Cuándo usarla
- Latencia crítica (milliseconds).
- Requisitos de acumulativo/replay vía reprocessing.
- Organización con madurez en streaming (Kafka/Flink).

### Estructura
```
Source → Kafka (event log) → Streaming Engine (Flink/Spark Structured)
                             ↓
                        [Processing] → Sink (Data Lake / Warehouse)
                             ↓
                        [Serving] (API / BI)
```

### Ventajas
- ✅ Una sola código base (DRY).
- ✅ Replay automático si hay errores (event log es la fuente).
- ✅ Latencia uniforme: end-to-end ~ 1-5 min (vs batch 24h).

### Desventajas
- ❌ Análisis complejos (agregaciones por ventana) requieren Flink/Spark manejo de estado.
- ❌ State management complejo (checkpoint, rocksdb).
- ❌ Requiere infraestructura maduro de streaming.

### Ejemplo Real: Azure
- Topic: Event Hub (source).
- Processing: Azure Stream Analytics o Databricks Structured Streaming.
- Storage: ADLS (data lake).
- Serving: Power BI (reads desde data lake).

---

## 3. Medallion Architecture (Raw-Curated-Serving Zones)

### Estructura de Datos

Independiente de Lambda/Kappa, organiza **dónde viven** los datos:

```
S3/ADLS
├── RAW (Bronze)
│   ├── domain1/source1/  (raw dumps, minimal transformation)
│   └── domain2/source2/
├── CURATED (Silver)
│   ├── domain1/entity1/v1/  (cleaned, normalized, validated)
│   └── domain2/entity2/
└── SERVING (Gold)
    ├── mart_sales/        (denormalized, BI-ready)
    └── mart_finance/      (calculated metrics, KPIs)
```

### Raw (Bronze)

- **Qué:** Dump directo del source, mínima transformación.
- **Formato:** JSON, CSV, Parquet (tal como llega).
- **Retención:** Indefinida (backup histórico).
- **Contratos:** Ninguno (best-effort).
- **Acceso:** Solo por Data Platform team.

**Ejemplo:**
```
s3://my-datalake/raw/crm/customers/2026-02-20/customers_dump.json
→ sin transformación, sin validación de schema
```

### Curated (Silver)

- **Qué:** Limpieza, normalización, contratos de datos.
- **Formato:** Parquet particionado (high compression).
- **Retención:** 3+ años (OLAP friendly).
- **Contratos:** Schemas versionados, SLAs, reglas de negocio.
- **Acceso:** Data engineers, analytics engineers, data scientists.

**Ejemplo:**
```
s3://my-datalake/curated/sales/customer/v2/
├── customer_id (PK)
├── name (NOT NULL)
├── email (UNIQUE, REGEX)
├── created_date (YYYY-MM-DD)
└── ... (validated, deduplicated, type-safe)
```

### Serving (Gold)

- **Qué:** Marts, tablas analíticas, vistas denormalizadas.
- **Formato:** Parquet (optimizado para queries).
- **Retención:** 3-5 años (siguiendo políticas BI).
- **Contratos:** Column-level SLOs, refresh frequency.
- **Acceso:** BI tools, ML models, executives.

**Ejemplo:**
```
s3://my-datalake/serving/marts/sales/
├── fact_orders (grain: order_date x product x region)
├── dim_customer (snapshot diario)
└── dim_product (slowly changing, type 2)
(Optimizado para joins, sin duplicación)
```

---

## 4. Hybrid: Medallion + Lambda/Kappa

### Patrón Recomendado: Medallion + Kappa

Combina lo mejor: **una fuente único de verdad (streaming) + estructura clara (3 zonas).**

```
Kafka Topic (event log)
    ↓ [Streaming Job - Flink/Spark]
S3/ADLS CURATED (schemas versionados)
    ↓ [Batch Transformations] / [Incremental Updates]
S3/ADLS SERVING (marts denormalizados)
    ↓
[API, BI, ML Models]
```

**Ventajas:**
- Event log como audit trail.
- Schemas evolucionan de forma controlada (raw → curated).
- Serviring toma datos ya validados → menos sorpresas.

---

## 5. Decisión: Lambda vs Kappa

### Matriz de Decisión

| Criterio | Lambda | Kappa |
|----------|--------|-------|
| Latencia requerida | > 1 hora | < 10 min |
| Volumen diario | 1+ TB | < 100 GB/día |
| Complejidad de transformaciones | Media-Alta | Media |
| Madurez de streaming en org | Baja | Media-Alta |
| Costo infraestructura | Bajo (batch) | Medio (sempre on) |
| Mantenibilidad | Baja (2 DAGs) | Media-Alta (1 DAG) |

**Décision rápida:**
- Si `latency < 10 mins` → **Kappa**.
- Si `latency > 1 hora` pero `análisis complejos` → **Lambda**.
- Si `streaming mature` + `realtime crítico` → **Kappa**.
- Default para nuevos proyectos → **Kappa** (DevOps simplicity wins).

---

## 6. Meadows de Implementación

### Glue (AWS) + Medallion
```
1. Raw: S3 → Glue Job (auto schema detection) → S3 raw.
2. Curated: Glue Job (Spark SQL, DQ checks) → S3 curated.
3. Serving: Glue (enrich, denormalize) → Redshift.
```

### Synapse (Azure) + Medallion
```
1. Raw: Event Hub → Data Factory → ADLS raw.
2. Curated: Synapse Spark Pool (Scala/PySpark) → ADLS.
3. Serving: Synapse SQL Pool (MPP) → BI reports.
```

### Databricks + Medallion
```
1. Raw: Unity Catalog (bronze schema).
2. Curated: UC (silver schema, ACLs).
3. Serving: UC (gold, optimizaciones vía Z-order).
```

---

## Referencias

- AWS: [Data Warehouse Best Practices](https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/index.html)
- Azure: [Data Architecture Guide](https://learn.microsoft.com/en-us/azure/architecture/data-guide/)
- Databricks: [Medallion Architecture](https://www.databricks.com/blog/2022/06/24/use-the-medallion-architecture-to-build-medallion-lakehouses-on-databricks.html)
