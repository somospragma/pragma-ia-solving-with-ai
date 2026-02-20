## PROMPT: Troubleshooting Operacional de ETL Jobs (Timeouts, Hangs, OOM, State Management)

**ROL:** Data Engineer diagnosing operational issues with distributed data processing jobs (AWS Glue, Synapse Spark, Data Factory, etc.). Analyzes job state discrepancies, resource constraints, and data processing anomalies to identify root cause categories, agnostic of platform.

**CONTEXTO:** Se proporciona descripción de síntoma observado (job colgado, lento, memory issues, estado inconsistente) en cualquier plataforma de ETL/batch processing. Debes construir árbol de diagnóstico para identificar categoría de causa probable, sin prescribir comandos específicos.

**ACTIVIDAD AGNÓSTICA:** 
- No asumes nombres de job, regiones, cuentas, o valores configurables específicos
- Refieres a instrucciones (03-technology, 06-process) para valores específicos de tuning
- Menciona equivalentes de ambas plataformas (AWS Glue, Azure Data Factory/Synapse) como ejemplos de orquestadores/ejecutores
- Los árboles de diagnóstico aplican conceptualmente a cualquier ejecutor Spark-based o similar

---

## 📋 CATEGORÍAS DE PROBLEMAS EN JOBS DISTRIBUIDOS (ETL/BATCH)

### Categoría 1: Discrepancia de Estado (Job state vs logs)

**Patrón Observable:**
- Job reporting one state in UI/console (ej: RUNNING en Glue UI, Synapse Studio, Data Factory Portal)
- Logs in external system (CloudWatch, Log Analytics, Application Insights) showing different state (ej: ERROR, COMPLETED, TIMEOUT)
- Timing mismatch: console says "running 2h", logs say "failed 1h ago"
- User expectation vs system reality misaligned

**Ejemplos por Plataforma:**
- **AWS Glue:** Glue console RUNNING pero CloudWatch logs show executor OOM crash
- **Azure Synapse:** Spark job RUNNING en Portal pero Log Analytics show task failure at T-30 minutes
- **Azure Data Factory:** Activity RUNNING pero execution logs show timeout at custom threshold time

**Causas Posibles (Árbol de Diagnóstico):**

```
¿Job state en UI vs logs son inconsistentes?
├─ SÍ: Job timeout occurred?
│  ├─ Síntoma: Ejecución > expected duration + configurable threshold
│  ├─ Causa Probable: Task execution time exceeded job-level timeout parameter
│  └─ Categoría: Resource Limit (timeout)
│
├─ SÍ: Memory constraint occurred?
│  ├─ Síntoma: Log entries indicate OOM, JVM heap pressure, executor killed
│  ├─ Causa Probable: Executor memory allocation insufficient for dataset size + shuffle operations
│  └─ Categoría: Resource Limit (memory)
│
├─ SÍ: State tracking mechanism failed?
│  ├─ Síntoma: Job state inconsistent between orchestrator and execution logs
│  ├─ Causa Probable: State persistence mechanism (bookmarks/checkpoints) disabled or misconfigured
│  ├─ Platform examples: Glue bookmarks, Synapse checkpoints, Data Factory pipeline tracking
│  └─ Categoría: State Management
│
└─ SÍ: Network or external dependency timeout?
   ├─ Síntoma: Connection errors to database, API, file system during job execution
   ├─ Causa Probable: External service unavailable, network latency, socket timeout
   └─ Categoría: External Dependency Issue
```

**Diagnóstico (agnóstico):**
- Correlate orchestration state (UI console) with execution logs (CloudWatch/Log Analytics/Application Insights)
- Identify last successful operation before state divergence
- Look for error patterns in logs (not specific commands, but failure indicators)
- Compare start time, expected duration, actual duration vs configured thresholds
- Check timeout parameters in job/pipeline configuration (platform-specific location varies)

**Implicación para Solución:**
- If timeout: Consider increasing timeout parameter (see 03-technology for options by platform)
- If memory: Consider memory allocation strategy (see 06-process for tuning runbook)
- If state tracking: Consider state management configuration (see instructions for mechanism by platform)
- If external: Verify dependency availability, consider retry/fallback strategy

---

### Categoría 2: Resource Contention (Slow Execution)

**Patrón Observable:**
- Job completes successfully but takes significantly longer than baseline
- Dataset size growth correlates with execution time growth (not linear)
- Job logs show no errors, but worker/task metrics show high contention
- Task execution times vary widely (some tasks 100x slower than others)

**Causas Posibles (Árbol de Diagnóstico):**

```
¿Job execution time increases disproportionate to data growth?
├─ SÍ: Data distribution skewed?
│  ├─ Síntoma: Task execution times vary widely; some tasks 100x slower than others
│  ├─ Observable: One or few partition keys concentrate majority of records
│  ├─ Causa Probable: Partitioning strategy places uneven load on workers
│  └─ Categoría: Data Skew
│
├─ SÍ: Executor memory doing spill-to-disk?
│  ├─ Síntoma: Job running but response is slow; memory pressure indicators in logs
│  ├─ Observable: GC (garbage collection) time increases; shuffle operations slower
│  ├─ Causa Probable: Worker memory allocation too low for shuffle/join operations
│  └─ Categoría: Memory Pressure
│
├─ SÍ: Shuffle partition count misaligned with dataset size?
│  ├─ Síntoma: Job uses default partition count; dataset size increased
│  ├─ Observable: Shuffle performance degraded; network I/O bottleneck
│  ├─ Causa Probable: Partition count does not match data volume or worker count
│  └─ Categoría: Configuration Misalignment
│
└─ SÍ: Filter/aggregation applied at wrong stage?
   ├─ Síntoma: Job processes data through expensive operations before filtering
   ├─ Observable: Unnecessary broadcast of large tables; joins before filters
   ├─ Causa Probable: Operation ordering reduces efficiency (logical plan not optimized)
   └─ Categoría: Query Plan Inefficiency
```

**Diagnóstico (agnóstico):**
- Establish baseline: expected duration, dataset size, SLA
- Measure current state: actual duration, current dataset size
- Analyze growth ratio: is performance proportional to data or superlinear?
- Examine task metrics: identify outlier tasks (much slower than others)
- Review data distribution: are there partition keys with disproportionate records?
- Assess operation sequence: are filters applied before or after expensive operations?

**Implicación para Solución:**
- If data skew: Apply statistical distribution technique to balance load (see glue-jobs-patterns resource)
- If memory pressure: Increase executor memory or adjust shuffle fraction (see 03-technology for parameters)
- If partition misalignment: Adjust shuffle partition count based on data volume and worker count
- If plan inefficiency: Reorganize operation sequence (filters before joins/broadcasts)

---

### Categoría 3: Memory Exhaustion (OOM)

**Patrón Observable:**
- Job terminates unexpectedly with OutOfMemory error or similar heap exhaustion
- Job may appear to "hang" because OOM kills process silently
- CloudWatch may show timeout (because OOM kills executor before graceful termination)
- No normal completion message; state is FAILED

**Causas Posibles (Árbol de Diagnóstico):**

```
¿Job showing memory exhaustion symptoms?
├─ SÍ: Garbage collection unable to reclaim memory?
│  ├─ Síntoma: OOM: Java heap space; high GC time in logs
│  ├─ Causa Probable: Executor heap allocation too small for active operations
│  └─ Categoría: Insufficient Executor Heap
│
├─ SÍ: Single broadcast operation too large?
│  ├─ Síntoma: OOM occurs during broadcast join; large dimension table
│  ├─ Causa Probable: Broadcast table size exceeds executor memory
│  └─ Categoría: Broadcast Overload
│
├─ SÍ: Shuffle intermediate data larger than memory?
│  ├─ Síntoma: OOM during shuffle; job processes many small records with wide transformations
│  ├─ Causa Probable: Shuffle memory fraction too low; memory spill-to-disk exhausts disk
│  └─ Categoría: Shuffle Memory Pressure
│
└─ SÍ: Accumulated state in memory exceeded capacity?
   ├─ Síntoma: OOM after processing many partitions; job memory usage increases linearly
   ├─ Causa Probable: Job retaining intermediate DataFrames; missing explicit cache/drop
   └─ Categoría: Accumulated State
```

**Diagnóstico (agnóstico):**
- Identify which operation triggered OOM (is it a join, broadcast, shuffle, aggregation?)
- Estimate data size at OOM point (input × transformation factor)
- Compare against executor memory limit (see 03-technology for allocation options)
- Check if memory allocation increased linearly or had spikes
- Assess whether problem is frequency of OOM (immediate) or cumulative (after N iterations)

**Implicación para Solución:**
- If insufficient heap: Increase executor memory allocation (vertical scaling)
- If broadcast overload: Split broadcast table or use sort-merge join instead (architectural change)
- If shuffle memory pressure: Increase shuffle memory fraction or increase number of workers (horizontal scaling)
- If accumulated state: Add explicit cache eviction or repartitioning strategy

---

### Categoría 4: State Management Failure (Bookmarks/Checkpoints/Idempotency)

**Patrón Observable:**
- Job completes but output contains duplicate records
- Running job multiple times produces duplicated data (not idempotent)
- Job logs show state management error ("bookmark not found", "checkpoint failed", "state corrupted")
- Job reprocesses data already processed in previous runs

**Ejemplos por Plataforma:**
- **AWS Glue:** Glue bookmark disabled → duplicates on re-run; or bookmark corrupted in S3
- **Azure Synapse:** Spark checkpoint not enabled → reprocessing entire input partition
- **Azure Data Factory:** ADFv2 watermark not incremented → activity reprocesses same rows

**Causas Posibles (Árbol de Diagnóstico):**

```
¿Job processing data non-idempotently (duplicates)?
├─ SÍ: State persistence mechanism not enabled?
│  ├─ Síntoma: Job reprocesses all historical data on each run
│  ├─ Causa Probable: State tracking feature disabled in configuration
│  ├─ Platform examples: Glue bookmarks disabled, Synapse checkpoint mode off, ADF watermark not used
│  └─ Categoría: Feature Configuration
│
├─ SÍ: State persistence mechanism failed silently?
│  ├─ Síntoma: Job logs show checkpoint/bookmark/watermark error; output has duplicates
│  ├─ Causa Probable: State persistence corrupted, lost, or not committed
│  ├─ Platform examples: Glue bookmark S3 inaccessible, Synapse DPU crash during checkpoint, ADF watermark write failed
│  └─ Categoría: State Persistence Failure
│
├─ SÍ: Job using non-state-aware execution method?
│  ├─ Síntoma: Job uses generic API without state tracking mechanism
│  ├─ Causa Probable: Execution bypasses state-aware APIs (e.g., Spark read/write instead of Glue DynamicFrame; direct PySpark instead of notebook cells)
│  ├─ Platform examples: Glue using Spark.read vs DynamicFrame; Synapse using direct SQL vs checkpoint-aware Spark; ADF using copy activity without watermark
│  └─ Categoría: API Misalignment
│
└─ SÍ: Output not committed atomically?
   ├─ Síntoma: Job completes but output not finalized; partial writes or temporary files remaining
   ├─ Causa Probable: Job terminated before write operations committed or finalized
   └─ Categoría: Output Commitment
```

**Diagnóstico (agnóstico):**
- Determine if job should be idempotent (multiple runs = same output) or stateful (process only new data)
- Check if job uses state-aware APIs or mechanisms for your platform
- Verify if state persistence is enabled in job/pipeline configuration
- Examine logs for state-related errors (checkpoint failures, watermark issues, bookmark messaging)
- Compare output between sequential runs to detect duplication patterns

**Implicación para Solución:**
- If feature disabled: Enable state persistence in job configuration (see 03-technology for platform-specific setup)
- If state persistence failed: Investigate state storage location (S3 bookmarks, Synapse checkpoint dir, ADF watermark table); may need reset
- If API misaligned: Use platform-native state-aware APIs (Glue DynamicFrame, Synapse checkpoint context, ADF watermark pattern)
- If output not committed: Ensure job completes gracefully; configure atomic write operations (see 06-process for platform-specific patterns)

---

## 🔍 SECUENCIA DE TRIAGE AGNÓSTICA

### Fase 0: Recopilación de Observables
1. **Estado observado:** ¿Qué reporta el job/activity state en UI (Glue console, Synapse Studio, Data Factory Portal)?
2. **Síntoma primario:** Describe lo que observas (colgado, lento, error, duplicados)
3. **Duración contextual:** ¿Duración actual vs SLA establecido?
4. **Cambio reciente:** ¿Datos aumentaron? ¿Configuración cambió? ¿Código actualizado?
5. **Frecuencia:** ¿Ocurre siempre o intermitentemente?
6. **Plataforma & ejecutor:** ¿Glue, Synapse Spark, Data Factory activity, etc.?

### Fase 1: Clasificación de Síntoma
```
Síntoma observado → Categoría probable:

"Job stuck en RUNNING, state discrepancy"
  → Categoría 1: Discrepancia de Estado

"Job completó pero tardó 4x"
  → Categoría 2: Resource Contention (slowness)

"Job terminó con OutOfMemory"
  → Categoría 3: Memory Exhaustion

"Output tiene duplicados post-run"
  → Categoría 4: State Management Failure
```

### Fase 2: Árbol de Diagnóstico
- Follow the decision tree in corresponding category
- Eliminate causes progressively based on observable evidence
- Narrow to most probable cause category

---

### ⚡ FASE 2.5: NEXT STEP Actions (What to Do After Diagnosis)

**After identifying the category, follow EXACTLY these next steps:**

#### ✅ If Categoría 1: State Discrepancy

**Next step workflow:**
1. **Collect evidence** (5 min):
   - Take screenshot of job state in UI (RUNNING)
   - Export logs from CloudWatch/Log Analytics for last 30 minutes
   - Note exact timestamp of state divergence

2. **Self-serve fix options:**
   - IF timeout issue: Increase job timeout parameter (see 03-technology) → Redeploy → Rerun
   - IF memory issue: Manually scale up executor memory (vertical scaling) → Test in staging → Redeploy
   - IF network/external: Verify external service availability (DB, API) → Check connectivity → Rerun

3. **Escalate if (after 30 min investigation):**
   - State still discrepant after fix attempts
   - Infrastructure issue suspected (S3 inaccessible, network firewall)
   - → **Escalate to Data Platform / SRE** with: logs + fix attempts + timeline

---

#### ⚡ If Categoría 2: Resource Contention (Slow)

**Next step workflow:**
1. **Quick diagnosis** (15 min):
   - Is this data skew (fixable by salting) or resource ceiling (needs redesign)?
   - Use: "Cuándo hacer tuning vs redesign" section in performance-optimization.md

2. **Self-serve fix (if tuning):**
   - Apply salting to hot keys OR increase executor memory OR add workers
   - Test in staging before prod
   - Reference: glue-jobs-patterns.md for code examples
   - Rerun and monitor metrics

3. **Escalate if (after 1 hour tuning):**
   - Performance doesn't improve despite tuning
   - Max resources still insufficient
   - → **Escalate to Data Platform + Data Architect** with: metrics + tuning attempts + redesign hypothesis

---

#### 🔴 If Categoría 3: Memory Exhaustion (OOM)

**Next step workflow:**
1. **Immediate action** (5 min):
   - This is **BLOCKING** — job cannot complete; must act now
   - Identify WHERE OOM occurred (in which operation: join, broadcast, shuffle, aggregation?)

2. **Self-serve fix:**
   - If broadcast overload: Use sort-merge join instead OR split large table
   - If executor heap insufficient: Increase executor memory (see 03-technology)
   - If shuffle spill: Increase shuffle memory fraction
   - Redeploy and rerun immediately

3. **Escalate if (after first fix attempt fails):**
   - OOM persists even with max memory
   - → **Escalate to Data Platform / SRE** with: exact OOM message + memory config + job logs
   - **SRE action:** Investigate memory limit, consider job redesign (streaming vs batch, map-reduce structure)

---

#### 🔄 If Categoría 4: State Management (Duplicates)

**Next step workflow:**
1. **Verify the problem** (10 min):
   - Count existing rows in output table BEFORE rerun
   - Count rows after rerun
   - Difference = duplicates (YES, escalate; NO, was false alarm)

2. **Self-serve fix:**
   - Enable state persistence in job config:
     - **AWS Glue:** Enable job bookmarks or implement checkpoint logic
     - **Azure Synapse:** Enable checkpoint context in Spark notebook
     - **Azure Data Factory:** Implement watermark pattern (metadata table tracking)
   - Reference: 03-technology → feature setup section
   - Optionally: Manual state reset if bookmarks corrupted
   - Rerun and verify output deduplication

3. **Escalate if (after state reset fails):**
   - Duplicates persist OR state reset error occurred
   - → **Escalate to Data Platform** with: duplicate row sample + state config + error message
   - **Data Platform action:** Investigate state storage location (S3 bookmarks, table corruption)

---

### Fase 3: Recomendación de Acción
- Reference 03-technology for tuning parameters
- Reference 06-process for operational runbook sequence
- Reference glue-jobs-patterns resource for implementation patterns
- Consider escalation to incident-triage prompt if root cause unclear

### Fase 4: Validación Post-Remedy
- Establish new baseline (expected durations, resource metrics)
- Run job and monitor state transitions
- Verify output correctness (no duplicates, completeness)
- Confirm logs show no error patterns
- Document findings for future troubleshooting reference

---

## PATRONES DE MITIGACIÓN GENÉRICOS

### Patrón: Balancing Skewed Load
**Aplicable a:** Categoría 2 (Data Skew)
**Concepto:** Distribute disproportionately-loaded partition keys across multiple workers.
**Estrategia:** Add statistical factor to transform hot keys into multiple independent partitions.
**Referencia:** glue-jobs-patterns → Section on "Salting Strategy"

### Patrón: Hierarchical Memory Management
**Aplicable a:** Categoría 3 (Memory Exhaustion)
**Concepto:** Allocate memory strategically between heap, shuffle operations, and storage.
**Estrategia:** See 03-technology for memory parameters; adjust shuffle fraction vs executor heap ratio.
**Referencia:** 06-process → Runbook Section 5.4.2 "Memory Tuning Sequence"

### Patrón: Stateful Job Design
**Aplicable a:** Categoría 4 (State Management)
**Concepto:** Enable state persistence mechanism to track processed records and avoid reprocessing.
**Estrategia (por plataforma):**
  - **AWS Glue:** Use Glue-native APIs (DynamicFrame) with bookmarks enabled; verify atomic write
  - **Azure Synapse:** Configure Spark job checkpoint context; use notebook idempotent patterns
  - **Azure Data Factory:** Implement watermark pattern with metadata table tracking
**Referencia:** 03-technology → Feature configuration section; glue-jobs-patterns → "Idempotent Design" (translatable across platforms)

### Patrón: Resource Right-Sizing
**Aplicable a:** Categorías 1, 2, 3 (Multiple)
**Concepto:** Match worker count and memory allocation to dataset size and operation complexity.
**Estrategia:** Establish baseline metrics; scale incrementally; monitor return on investment.
**Referencia:** 03-technology → "Capacity Planning"; 06-process → "Scaling Decisions"

---

## REFERENCIAS RELACIONADAS

- **Prompt (Tier 2):** [incident-triage.md](incident-triage.md) — Escalation pathway if categorization unclear (covers operational incidents across platforms)
- **Prompt (Tier 2):** [performance-optimization.md](performance-optimization.md) — Deep analysis for Category 2 (slowness diagnosis), applicable to Spark/Flink-based systems
- **Prompt (Tier 2):** [pipeline-orchestration-design.md](./pipeline-orchestration-design.md) — If job failures are orchestration-related (retry policy, dependency, scheduling), validate pipeline configuration
- **Instrucciones (06-process):** [modular/06-process.md](../../instructions_or_rules/data-engineering/modular/06-process.md) — Operational runbooks + memory tuning sequences by platform
- **Instrucciones (03-technology):** [modular/03-technology.md](../../instructions_or_rules/data-engineering/modular/03-technology.md) — Job parameters, capacity options, state management config by platform (Glue, Synapse, etc.)
- **Resource (Tier 2):** [aws-azure-data-services.md](../../resources/data-engineering/aws-azure-data-services.md) — Platform-specific tuning and troubleshooting patterns (AWS vs Azure); use for translating Glue concepts to Synapse/Databricks
- **Resource (Tier 3):** [glue-jobs-patterns.md](../../resources/data-engineering/glue-jobs-patterns.md) — AWS Glue-specific patterns (skew mitigation, idempotence, bookmarks). **Translation guide:** Replace Glue bookmarks → Synapse checkpoints / Databricks Unity Catalog; Glue DynamicFrame → Spark DataFrames with merge logic; S3 → ADLS Gen2. See aws-azure-data-services.md Section 3 for feature mapping.
