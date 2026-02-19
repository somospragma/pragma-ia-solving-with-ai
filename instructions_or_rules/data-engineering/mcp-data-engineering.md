name: "MCP - Ingeniería de Datos"
description: "Instrucciones y reglas para diseñar, implementar y operar MCPs de Ingeniería de Datos en proyectos Pragma."
applyTo: data-engineering

> Orquestador modular completo: `modular/instructions.md`

**Meta**
- **Owner:** Data Engineering Chapter
- **Audience:** Ingenieros de datos, arquitectos, SREs, líderes técnicos
- **Template:** ../_estandar-instructions/instructions-orchestrator-template.md
- **Version:** 1.0

**Reglas Críticas (leer primero)**
- **Prioridad:** Diseñar pipelines con idempotencia y observabilidad desde el inicio.
- **Seguridad:** Enmascarar y cifrar datos sensibles en tránsito y reposo.
- **Contrato:** Definir contratos de datos (schemas + SLAs) antes de la entrega.

**Propósito y Alcance**
- **Propósito:** Proveer un conjunto de instrucciones estandarizadas para crear MCPs de Ingeniería de Datos (ingesta, almacenamiento, procesamiento, calidad, gobernanza y operación).
- **Alcance:** Aplica a proyectos que construyan o integren pipelines batch/stream, lagos de datos, almacenes analíticos y servicios de datos gestionados por equipos Pragma.

**Contexto del Proyecto**
- **Input esperado:** Fuentes de datos internas/externas, eventos y archivos.
- **Output esperado:** Datasets curados, APIs de datos, tablas analíticas y métricas.
- **Stakeholders:** Product Owner, Data Owner, Data Platform, Security, SRE, QA.

**Responsabilidades**
- **Equipo de Feature:** Implementación de transformaciones, tests y contratos.
- **Plataforma de Datos:** Infraestructura, despliegue, catálogo y observabilidad.
- **Security/Compliance:** Revisión de accesos, cifrado y auditoría.

**Arquitectura y Patrones Recomendados**
- **Patrón Lambda/Kappa:** Elegir Kappa para simplicidad cuando la plataforma soporta streaming nativo; Lambda sólo si hay necesidad clara de separar batch/stream.
- **Ingesta:** Conectores gestionados (CDC) o APIs con backpressure. Priorizar capturas incrementales.
- **Almacenamiento:** Separación clara entre raw, curated y serving zones. Prefiere formatos columnarios particionados (Parquet/ORC) y compresión adaptada.
- **Procesamiento:** Preferir frameworks manejados (Dataproc, EMR, Dataflow, Flink) o pipelines serverless según latencia/costo.

**Modelado y Contratos de Datos**
- **Schemas como contrato:** Versionar schemas (e.g., via Git) y publicar en catálogo. Cualquier cambio mayor requiere migración explícita.
- **Schema Evolution:** Usar compatibilidad hacia atrás/adelante según consumidores; documentar breaking changes.
- **Data Contracts:** Definir campos obligatorios, tipos, cardinalidades, y SLAs de freshness y calidad.

**Pipelines: Diseño y Buenas Prácticas**
- **Idempotencia:** Diseña transformaciones idempotentes; evita side-effects en pasos intermedios.
- **Atomicidad por etapa:** Almacena checkpoints atómicos y metadatos de ejecución.
- **Retries y DLQ:** Implementar políticas de reintento con dead-letter queues para errores persistentes.
- **Configurabilidad:** Parámetros de entorno y feature flags para togglear comportamientos sin redeploy.

**Calidad, Testing y Validación**
- **Pruebas unitarias:** Para transformaciones lógicas y UDFs.
- **Pruebas de integración:** Ejecutar sobre datasets representativos en CI con entornos reproducibles.
- **Data QA (contracts & checks):** Validaciones de schema, reglas de negocio, y reglas estadísticas (e.g., distribución, nulls, duplicados).
- **Gate de calidad:** Bloqueo automático si los checks críticos fallan.

**Observabilidad y Operaciones**
- **Métricas:** Throughput, lag, error-rate, cardinalidad, freshness, cost-per-run.
- **Logging estructurado:** Correlacionar trazas por run_id y dataset_id.
- **Alertas:** Definir umbrales y runbooks para incidentes comunes.
- **Catálogo/Metadata:** Registrar linaje, owners y descripciones en el catálogo corporativo.

**Infraestructura, IaC y Despliegue**
- **IaC obligatorio:** Declarar infra con módulos reutilizables (Terraform/CloudFormation). Mantener entornos parity (dev/staging/prod).
- **CI/CD:** Pipelines para tests unitarios, validaciones de contratos y despliegue automatizado.
- **Entornos aislados:** Datos sensibles en entornos con controles más estrictos.

**Seguridad, Privacidad y Cumplimiento**
- **Accesos por rol:** Principio de menor privilegio; auditar accesos periódicamente.
- **Protección de PII:** Tokenización, enmascaramiento o cifrado según clasificación.
- **Retención y eliminación:** Políticas claras y automáticas de retención.

**Costos y Performance**
- **Estimación de costo:** Modelar costo por volumen y frecuencia; optimizar particiones y tamaños de batch.
- **SLA de latencia:** Definir y validar mediante pruebas de carga.

**Runbooks y Playbooks**
- **Incidentes comunes:** Falta de datos, schema drift, backfills fallidos — pasos para identificación y mitigación.
- **Backfill seguro:** Procedimiento para reprocesos con control de ventanas y validaciones previas.

**Hydratación y Personalización (Cómo usar esta plantilla)**
- **Hidratar por proyecto:** Reemplazar secciones de "Contratos", "Owners" y "Conectores" con detalles del proyecto.
- **Mantener reglas críticas al inicio y recordatorios al final** según el Estándar.
- **Límites de archivo:** Si el contenido excede 12,000 caracteres, dividir siguiendo la estructura modular del orquestador.

**Notas para Agentes/Integraciones (para copilot/amazonq)**
- **Resumen para agentes:** Priorizar reglas críticas y contratos; solicitar sólo cambios incrementales con pruebas.
- **Context window:** Mantener secciones críticas en inicio/fin; referenciar archivos complementarios en `.github/instructions/`.

**Referencias**
- Plantilla Orquestador: [instructions-orchestrator-template.md](../_estandar-instructions/instructions-orchestrator-template.md)
- Plantilla Unificada: [instructions-template.md](../_estandar-instructions/instructions-template.md)

**Reglas Clave (resumen al final)**
- **Idempotencia:** obligatorio.
- **Contracts first:** definir schemas y SLAs antes de implementación.
- **Observabilidad desde PR:** incluir métricas y logging mínimo en cada merge.

Fin del documento MCP - Ingeniería de Datos
