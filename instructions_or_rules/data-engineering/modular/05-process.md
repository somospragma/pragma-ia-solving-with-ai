```markdown
# Process, IaC & Operations

## 5.1. Infrastructure as Code

- Declare all infra with Terraform/CloudFormation/ARM modules
- Keep environments parity (dev/staging/prod) and use workspaces or accounts

## 5.2. CI/CD

- Pipeline stages: lint -> unit tests -> contract tests -> integration -> deploy
- Automatic migration plans for schema changes; manual approval for breaking changes

## 5.3. Runbooks & Backfills

- Standard runbooks for missing data, schema drift, and failed backfills
- Backfill procedure: snapshot inputs, run in isolated job, validate outputs, promote

## 5.4. Runbook: Degradación de jobs de procesamiento (Glue / Synapse)

### Síntoma de alerta
- Duración del job aumenta > X% respecto al baseline en N runs consecutivos
- Incremento en DPUs/consumo de recursos, aumento de errores o fallos intermitentes

### Objetivo
- Diagnosticar causa raíz rápida y aplicar mitigación para recuperar SLA. Si no resuelve, escalar según runbook de incidentes.

### Triage inmediato (0-30 mins)
1. Identificar runs recientes y `run_id` problemáticos

	- AWS Glue:
		```bash
		aws glue get-job-runs --job-name MyJob --max-items 50
		aws glue get-job-run --job-name MyJob --run-id <runId>
		```

	- Azure Synapse (usar portal o CLI para revisar runs):
		```bash
		# Listar blobs de entrada para entender volumen
		az storage blob list --account-name <account> --container-name <container> --prefix <prefix> --output table
		```

2. Exportar logs y revisar errores claves

	- AWS CloudWatch (Glue logs):
		```bash
		aws logs filter-log-events --log-group-name /aws-glue/jobs/output --log-stream-name-prefix MyJob --start-time <epoch-ms>
		```

	- Azure Monitor / Synapse logs: revisar en el portal o exportar queries desde Log Analytics

3. Verificar métricas de performance

	- CloudWatch: duración, DPUs, error-rate, shuffle spill
	- Azure Monitor: duration, failed runs, CPU/memory del pool

4. Medir volumen y small-files

	- AWS S3:
		```bash
		aws s3 ls s3://my-bucket/path/ --recursive --summarize
		aws s3api list-objects-v2 --bucket my-bucket --prefix path/ --query "Contents[?Size<`33554432`].Key" --output json
		```

	- Azure Storage:
		```bash
		az storage blob list --container-name <container> --account-name <account> --prefix <prefix> --query "[].{name:name, size:properties.contentLength}" --output table
		```

### Causas frecuentes y mitigaciones rápidas (30-120 mins)
- Volumen creciente / small-files: ejecutar job de compactación (merge Parquet) o activar compaction automática; aplicar particionado efectivo.
- Data skew: identificar key con skew y aplicar salting o repartition por hash balanceado.
- Memory / GC / OOM: aumentar workers/DPUs o reducir paralelismo (adjust `spark.sql.shuffle.partitions`), revisar persistencia innecesaria.
- Ineficiencias en código / UDFs: perf-profile, reescribir transformaciones costosas a operaciones nativas DataFrame.
- Schema drift: bloquear despliegues hasta validar cambios, ejecutar backfills controlados.
- Bookmarks/incremental desincronizados: revisar job bookmarks y, si necesario, ejecutar backfill controlado.

### Backfill seguro (procedimiento)
1. Snapshot de inputs (copiar prefijo S3 / contenedor con timestamp).
2. Ejecutar backfill en entorno aislado (staging) con sample de datos o ventana pequeña.
3. Ejecutar suite de `04-quality` (schema, uniqueness, distribution checks).
4. Validar outputs contra baseline; si OK, promover al entorno target y re-ejecutar consumidores.

### Escalamiento
- Si la mitigación no resuelve en 60–120 minutos: abrir incidente, notificar Data Owner y on-call SRE, proporcionar logs, métricas y pasos ya ejecutados.

### Post-mortem y acciones preventivas
- Documentar RCA en el MCP: causa, corrección aplicada, cambios requeridos (e.g., compaction cron, ajustes de particionado, límites en archivos pequeños).
- Añadir tests/perf-smoke en CI que validen la performance sobre muestras representativas.

### Checklist rápida (para incluir en la plantilla de PR/Runbook)
- [ ] `run_id` y logs exportados
- [ ] Comparación de input-size y #files con baseline
- [ ] Revisión Spark UI / GC / shuffle
- [ ] Decisión: scale / compact / repartition / code-fix
- [ ] Backfill staging ejecutado y checks verificados
- [ ] Post-mortem y actualización del MCP


## 5.4. Cost Controls

- Tagging, budgets and alerts; estimate cost per run for critical pipelines

```
