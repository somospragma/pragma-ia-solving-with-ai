```markdown
# Technology, Connectors & Formats

## 3.1. Recommended Stack

- Ingest: Kafka (CDC), Managed connectors, AWS Kinesis, Pub/Sub
- Processing: Spark, Flink, Dataflow, Beam, or serverless transformations
- Storage: Object storage (S3/GCS/Azure Blob) with zones (raw/curated/serving)
- Serving: BigQuery/Redshift/Snowflake or managed OLAP

## 3.2. File Formats & Partitioning

- Use columnar formats (Parquet/ORC) for curated/serving
- Partition by date and high-cardinality bucketing when needed
- Use compaction and small-file mitigation strategies

## 3.3. Connectors & CDC

- Prefer CDC (Debezium/Managed CDC) for transactional sources
- For third-party APIs use incremental syncs and rate-limit handling

## 3.4. Metadata & Catalog

- Publish schemas and dataset metadata to the corporate catalog with linage
- Version schemas in Git and link to dataset entries

## 3.5. Cloud Platforms: AWS & Azure (enfoque en datos)

- **Alcance:** Este MCP está especializado en implementaciones sobre AWS y Azure. Todas las recomendaciones deben interpretarse primero bajo los principios del Well-Architected Framework del proveedor, con atención a las dimensiones relevantes para datos: confiabilidad, seguridad, rendimiento, optimización de costos y excelencia operativa.
- **Guías oficiales:**
	- AWS Well-Architected: https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html
	- Azure Well-Architected: https://learn.microsoft.com/en-us/azure/well-architected/what-is-well-architected-framework

### Recomendaciones rápidas por proveedor (ejemplos)

- **AWS (ejemplos):**
	- Ingesta: Kinesis Data Streams / MSK / Managed CDC (DMS, Debezium en MSK)
	- Almacenamiento: S3 con zonas (raw/curated/serving), Glue Data Catalog
	- Procesamiento: AWS Glue, EMR (Spark), AWS Lambda para micro-transformaciones
	- Serving/Analítica: Redshift, Athena, Lake Formation para gobernanza

- **Azure (ejemplos):**
	- Ingesta: Event Hubs, Managed CDC connectors via Data Factory
	- Almacenamiento: Azure Data Lake Storage Gen2 (zonas raw/curated/serving)
	- Procesamiento: Azure Databricks, Synapse Spark, Azure Functions
	- Serving/Analítica: Azure Synapse Analytics, Synapse Serverless SQL, Purview para catálogo

### Mapeo de conceptos

- Equivalencias útiles: S3 ↔ ADLS Gen2, Glue Catalog ↔ Purview/Catalog, EMR/Glue ↔ Databricks/Synapse.
- Documentar en cada proyecto el mapeo escogido y los criterios de decisión (latencia, costo, operaciones).

## 3.6. Arquitecturas híbridas (On‑prem ↔ Cloud)

- **Alcance:** Recomendaciones para diseños que combinan recursos on‑premises con servicios en AWS/Azure.
- **Conectividad y red:** Preferir enlaces dedicados (AWS Direct Connect, Azure ExpressRoute) o VPNs gestionadas; documentar latencia, throughput y plan de failover.
- **Patrones de transferencia:** Edge buffering, push vs pull, gateways, agentes de sincronización (AWS DataSync, Azure File Sync, Storage Gateway) y replicación incremental.
- **Gateways y conectores:** Soporta soluciones gestionadas y agentes (Debezium/Kafka Connect self‑hosted, Storage Gateway, DataSync). Documentar autenticación, certificados y puertos.
- **Consistencia y reprocessing:** Definir puntos de corte (checkpoints) y estrategias de reconciliación; planificar backfills con snapshots y ventanas controladas.
- **Seguridad y residence:** Políticas de residencia de datos, cifrado en tránsito/ reposo y controles de acceso por red y rol.
- **Observabilidad híbrida:** Centralizar métricas y logs (log shipping, exporters) para correlación end‑to‑end incluyendo latencias de red.
- **Operación y runbooks:** Añadir runbooks específicos (network outage, partial sync, split‑brain) y pruebas periódicas de failover.
- **Costes y planificación:** Modelar egress, costes de enlace dedicado y batching windows para optimizar transferencia de datos.

### Mapeo técnico híbrido (ejemplos)

- On‑prem Kafka ↔ MSK / Event Hubs con Connectors y MirrorMaker para replicación.
- NAS / NFS ↔ S3/ADLS usando DataSync / Storage Gateway para transferencias eficientes y consistentes.
- Bases transaccionales on‑prem ↔ CDC → cloud ingestion usando Debezium en local + MSK/Bridge.

Documentar en cada proyecto las decisiones, los SLAs de red y los criterios de fallback.

```
