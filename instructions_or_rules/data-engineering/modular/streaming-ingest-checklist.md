```markdown
# Checklist: Validación de arquitectura de ingesta streaming

Este checklist ayuda a validar una arquitectura de ingesta en streaming antes de pasar a producción.

## Contexto y objetivos
- Describir dominio, owners y consumidores.
- Definir SLAs: latency (p99/p95), freshness, throughput esperado.

## Fuentes e integración
- Identificar fuentes (DB, APIs, eventos) y volúmenes estimados.
- Verificar conectores CDC o adaptadores y límites de rate.

## Contratos de mensajes
- Esquema (Avro/Protobuf/JSON) definido y versionado.
- Publicado en catálogo y con pruebas de contract en CI.

## Broker y topología
- Broker elegido documentado (Kinesis/MSK/Event Hubs) y razón.
- Particionado: número inicial de shards/partitions y estrategia de key design.

## Backpressure, retries y DLQ
- Políticas de backpressure en producers/consumers.
- Retry policy y DLQ con alerting y proceso de reingest.

## Idempotencia y deduplicación
- Estrategia de dedupe (idempotent writes, dedupe keys, watermarks).

## Checkpointing y offsets
- Estrategia de checkpoints, retención y restauración (reprocessing).

## Particionado, paralelismo y hot-keys
- Plan de particionado y mitigación de hot-keys (salting, repartition).

## Storage & small-files
- Si persiste en object storage: estrategia de compaction y frecuencia.

## Observabilidad mínima
- Métricas: ingest-rate, consumer-lag, processing-latency, error-rate, throughput.
- Logs estructurados y correlación por `trace_id`/`run_id`.

## Validaciones de mensajes y esquema (llegada en streaming)
- **Formatos permitidos y serialización:** Definir y validar formatos soportados (Avro/Protobuf/JSON) y los serializers/deserializers en productores y consumidores.
- **Schema Registry:** Usar un Schema Registry (Confluent, AWS Glue Schema Registry, Azure Schema Registry); validar compatibilidad en el productor antes de publicar.
- **Topic/Stream naming convention:** Validar naming pattern y particiones esperadas; usar regex en el pipeline de ingest.
- **Timestamps y watermarking:** Validar que los mensajes incluyen `event_time` en formato acordado; definir y comprobar watermarking y late-arrival window.
- **Orden y idempotencia:** Definir requisitos de orden por key; validar presence de idempotency keys o dedupe strategy en consumidores.
- **Payload size & limits:** Rechazar/routear mensajes que excedan el tamaño máximo permitido; aplicar truncation policy donde aplique.
- **Schema con tipos y nullability:** Validar tipos (int, float, string, boolean, timestamp) y campos obligatorios; mapear cambios de schema a plan de evolución.
- **Values/domain checks:** Validar enums, ranges y formatos (emails, ids) y enviar mensajes inválidos a DLQ.
- **Heartbeat & health events:** Validar eventos de heartbeat y monitorizar gaps en heartbeat.
- **Encryption & auth metadata:** Comprobar headers/metadata necesarios para autenticación y cifrado (tokens, cert ids).
- **Sample validation / canary traffic:** Validar un porcentaje de tráfico (canary) antes de aceptar cambios en producción.
- **Corrupt / malformed messages:** Definir handler: reject+DLQ, sanitize+process, or alert+manual review.

## Herramientas y comandos (ejemplos)
Estas son herramientas prácticas y comandos de ejemplo que pueden usarse en validaciones y pruebas de ingest en streaming.

- kcat (aka kafkacat) — consumir y producir mensajes Kafka:
	- Consumir 10 mensajes: `kcat -C -b <broker:port> -t <topic> -o beginning -c 10`
	- Producir desde archivo: `kcat -P -b <broker:port> -t <topic> -K: < messages.json`

- Schema Registry (Confluent / AWS Glue / Azure):
	- Consultar schema (Confluent): `curl -s http://schema-registry:8081/subjects/<subject>/versions/latest | jq`.
	- Verificar compatibilidad (Confluent):
		`curl -s -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" --data '{"schema":"<schema-string>"}' http://schema-registry:8081/compatibility/subjects/<subject>/versions/latest`

- AWS Kinesis (ejemplos):
	- Enviar un registro: `aws kinesis put-record --stream-name my-stream --partition-key key1 --data $(echo -n '{"event":"x"}' | base64)`
	- Obtener registros (usar `shardIterator` con `get-shard-iterator` y `get-records` en scripts de diagnóstico).

- Validación de payloads:
	- JSON: `jq` para parseo y filtros; `ajv` para validar against JSON Schema.
	- Avro: `avro-tools` para inspeccionar y validar archivos Avro.
	- Protobuf: `protoc` para compilar/validar mensajes.

## Ejemplo: Canary test (envío controlado de tráfico)
Pequeño script de ejemplo para enviar mensajes canary y validar consumo:

```bash
# enviar 100 mensajes de prueba (kafka broker)
for i in $(seq 1 100); do
	msg="{\"id\":$i,\"event_time\":\"$(date -u +"%Y-%m-%dT%H:%M:%SZ")\",\"value\":$RANDOM}"
	echo "$msg" | kcat -P -b broker:9092 -t my-topic
done

# consumir y validar 10 mensajes
kcat -C -b broker:9092 -t my-topic -c 10 | jq .
```

Notas:
- Reemplazar `broker:9092`, `my-topic` y `schema-registry` por valores del entorno.
- Para Kinesis/Managed streaming sustituir por `aws kinesis put-record` y consumir con `aws kinesis get-records` o con consumidores SDK.
- Automatizar validaciones con scripts que llamen a `ajv`, `avro-tools` o validadores propios; enviar mensajes inválidos a DLQ y notificar al owner.

## Tests y validaciones
- Contract tests automáticos en PR.
- Perf-smoke (sample traffic) y e2e integration tests.
- Chaos tests para fallos de broker y latencia.

## Seguridad y gobernanza
- Cifrado en tránsito/reposo, ACLs, clasificación y manejo de PII.
- Política de retención y eliminación.

## Infra & IaC
- Módulos Terraform/ARM/Bicep reproducibles para dev/staging/prod.
- `terraform plan` / `az cli` / `aws cli` checks en CI.

## Well‑Architected mapping
- Documentar decisiones relevantes frente a AWS/Azure Well‑Architected (data lens).

## Runbooks críticos a incluir
- Missing data (ingest stopped), consumer lagging, schema drift, backfills.

## Acceptance criteria (pre-promote)
- Contract tests pasan.
- Perf-smoke dentro del budget (latency / throughput).
- IaC apply plan sin cambios no aprobados.
- Observability endpoints y alertas configuradas.

```
