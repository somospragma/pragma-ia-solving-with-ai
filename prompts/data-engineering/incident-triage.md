## PROMPT: Triage de Incidentes en Pipelines de Datos (Falta Datos, Schema Drift, Degradación)

**ROL:** Data Engineer On-Call / Incident Commander. Diagnostica y mitiga incidentes de datos rápidamente.

**CONTEXTO:** Se te dará un incidente activo (alertas, logs, cambios recientes). Ejecuta triage estructura y propone mitigaciones inmediatas.

### INCIDENTES COMUNES & CHECKLIST

**Incidente: Datos no llegaron (0 filas después de ventana SLA)**

Triage inmediato:
1. ¿Source está activo? (revisar logs, ping endpoint, revisar CDC lag)
2. ¿Schema válido? (schema drift en upstream?)
3. ¿Job ejecutó? (revisar job status, orchestrator logs)
4. ¿Hay errores en DLQ / dead-letter queue?
5. ¿Network está up? (conectividad a BD/API)

Mitigación rápida:
- Trigger manual del job con window anterior
- Escalar a Data Platform si es infraestructura
- Comunicar delay a consumidores

---

**Incidente: Schema Drift (tipos cambiaron, nuevas columnas, removidas)**

Triage inmediato:
1. ¿Qué cambió? (revisar source schema, CDC logs)
2. ¿Cuándo cambió? (identificar run afectada)
3. ¿Consumidores rompieron? (revisar logs de jobs downstream)
4. ¿Es backward compatible? (nueva columna nullable vs deletada)

Mitigación rápida:
- Si compatible: actualizar schema, rescan validaciones
- Si breaking: bloquear ingest, activar Data Contract notification
- Notificar consumidores con timeline
- Referir a data-contract-patterns.md para evolución

---

**Incidente: Job degradado (lentitud, errores intermitentes, DPU spike)**

Triage inmediato:
1. ¿Volumen aumentó? (revisar source row counts)
2. ¿Hay skew nuevo? (revisar partición distribution)
3. ¿Cambios recientes en código? (git diff vs versión anterior)
4. ¿Resource contention? (memory, CPU, I/O)
5. ¿Dependencias externas lentas? (BD connections, API latency)

Mitigación rápida:
- Aumentar recursos temporalmente (scale up)
- Aplicar salting si skew detectado
- Rollback a versión anterior si hay cambios recientes
- Investigar en paralelo (referir a performance-optimization.md)

---

### SECUENCIA DE PASOS (Todos los incidentes)

1. **Clasificación:**
   - Criticidad: P1 (SLA breach), P2 (partial data), P3 (performance degrade)
   - Scope: 1 job vs multiple vs platform

2. **Recolección rápida:**
   - Last successful run timestamp
   - Error messages (Slack alerts, CloudWatch, DataDog)
   - Recent changes (code, configs, upstream systems)

3. **Diagnosticación:**
   - Seguir checklist según tipo (arriba)
   - Paralelizar investigaciones

4. **Mitigación & Comunicación:**
   - Acción inmediata (manual trigger, resource scale, rollback)
   - Notificar stakeholders (Slack, runbook)
   - Documentar en incident tracker

5. **Resolución & Post-Mortem:**
   - Root cause + permanent fix
   - Monitoring/alerting improvements
   - Runbook update

---

## 🚨 ESCALATION MATRIX & SLA

**Use esta tabla para saber cuándo escalar y a quién, según el tipo de incidente:**

### Incidente P1 (CRÍTICO): Datos no llegaron, SLA breached

| Paso | Quién | Acción | SLA |
|------|-------|--------|-----|
| **Detección** | On-Call Engineer | Alert in Slack + incident tracker | <2 min |
| **Diagnosticación** | Data Engineer | Follow "Datos no llegaron" checklist | <5 min |
| **Escala inmediata (si infraestructura)** | Data Platform / SRE | Check S3/ADLS buckets, connectivity, schema registry | <5 min total |
| **Escala inmediata (si source)** | Data Owner (upstream team) | Check source system availability, CDC | <5 min total |
| **Mitigación** | On-Call Engineer | Trigger manual rerun with prior window; notify consumers | <15 min total |
| **Resolution** | Data Engineer + Data Owner | Root cause analysis + permanent fix | <4 hours |

---

### Incidente P2 (MAYOR): Schema breaking change, partial data loss

| Paso | Quién | Acción | SLA |
|------|-------|--------|-----|
| **Detección & Triage** | Data Engineer | Determine: compatible vs breaking | <10 min |
| **If backward compatible** | Data Engineer | Update schema, rescan validations, resume | <1 hour |
| **If breaking** | Data Owner | Block ingest; decide migration/revert | <15 min total |
| **Impact notification** | Data Owner + Analytics leads | Communicate with downstream consumers | <15 min |
| **Recovery** | Data Platform + Data Engineer | If data lost: backfill or rollback | <4 hours |
| **Prevention** | Data Owner | Update data contract; implement schema validation in CI | <1 week |

---

### Incidente P3 (MENOR): Job slow, intermittent errors, no SLA breach yet

| Paso | Quién | Acción | SLA |
|------|-------|--------|-----|
| **Diagnosis** | Data Engineer | Self-serve using performance-optimization.md | <1 hour |
| **Quick fix** | Data Engineer | Apply tuning (scale up, salting, retry policy) in staging | <1 hour |
| **Test & Deploy** | Data Engineer | Validate in staging; monitor in production | <2 hours |
| **Escalate if unsolved** | Data Platform SRE | If > 2 hours: investigate infrastructure or design | <4 hours |
| **Root cause** | Data Engineer + Data Platform | Permanent fix (monitoring, alerting, redesign) | <1 week |

---

### Guía Rápida: ¿Cuándo escalar?

- **Escalar a Data Platform / SRE si:** Infraestructura issue (S3 bucket inaccessible, network timeout, service degradation)
- **Escalar a Data Owner si:** Data/source issue (schema change, upstream API changed, CDC lag)
- **Escalar a Product/Business si:** SLA breach affecting external customers (revenue impact)
- **Self-serve if:** Single job performance issue solvable with tuning (< 2 hours diagnosed)

---

### Comunicación a Stakeholders (Template)

**For P1 SLA breach:**
```
🚨 #data-incident: <pipeline name> SLA breached
- Impact: <X rows> not loaded to <table>; <Y downstream jobs> affected
- Status: Investigating (see runbook: <link>)
- ETA: <time to mitigation>
- Owner: @Data-Platform oncall
```

---

## 📚 REFERENCIAS RELACIONADAS

- **Instrucciones:** `instructions_or_rules/data-engineering/modular/06-process.md` (Sección 5.4 Runbook Degradación)
- **Instrucciones:** `instructions_or_rules/data-engineering/modular/04-quality.md` (Sección 4.5 Monitoring & Metrics)
- **Resource (Tier 2):** `resources/data-engineering/testing-data-pipelines.md` (Cómo evitar incidentes con tests)
- **Resource (Tier 1):** `resources/data-engineering/data-contract-patterns.md` (Schema drift management)
- **Prompt (Tier 2):** `prompts/data-engineering/performance-optimization.md` (Para degradación de performance)
