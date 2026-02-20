## PROMPT: Diseño de Data Contracts (Desde Cero)

**ROL:** Data Architect / Product Owner. Diseña data contracts completos para nuevos datasets o mejora contracts existentes.

**CONTEXTO:** Se te dará un dataset, tabla, o stream. Crea un contract integral con schemas, SLAs, versionado y gobernanza.

### PASOS PARA DISEÑAR UN CONTRACT

**Paso 1: Descubrimiento**
- ¿Qué datos? (dominio, entidad, grain)
- ¿De dónde vienen? (source, frecuencia)
- ¿Quién los usa? (consumidores, casos de uso)
- ¿Qué cambios esperados? (evolución, nuevas versiones)

**Paso 2: Schema Design**
- Identificar campos obligatorios vs opcionales
- Definir tipos (INT, STRING, DATE, DECIMAL, STRUCT)
- Establecer convenciones de naming (snake_case, prefixes)
- Prever nullable fields vs NOT NULL

Ejemplo:
```yaml
fields:
  order_id:
    type: BIGINT
    nullable: false
    uniqueness: PRIMARY_KEY
    description: "Unique order identifier"
  customer_id:
    type: BIGINT
    nullable: false
    description: "FK to customers"
  amount_usd:
    type: DECIMAL(12,2)
    nullable: false
    range: [0, 1000000]
  status:
    type: STRING
    nullable: false
    enum: ["pending", "shipped", "delivered", "cancelled"]
  created_date:
    type: DATE
    nullable: false
    format: "YYYY-MM-DD"
```

**Paso 3: SLA Definition**
- Freshness: ¿Cada cuánto se actualiza? (hourly, daily)
- Completeness: ¿% nulls permitidos por campo?
- Accuracy: ¿Uniqueness, referential integrity?
- Availability: ¿% uptime target?

Ejemplo:
```yaml
sla:
  freshness:
    max_lag_hours: 2
    frequency: "every 1 hour"
    critical_time_window: "08:00-20:00 UTC"
  completeness:
    min_rows_per_day: 1000
    null_tolerance:
      order_id: 0%
      customer_id: 0%
      amount_usd: 0%
      status: 0%
      created_date: 0%
  accuracy:
    uniqueness: "order_id must be globally unique"
    referential_integrity: "customer_id exists in customers.customer_id"
  availability:
    uptime_target: "99.5%"
    maintenance_window: "Sunday 02:00-04:00 UTC"
```

**Paso 4: Versioning Strategy**
- Initial version: v1
- Backward compatible changes: v1 → v1.1 (MINOR bump)
- Breaking changes: v1 → v2 (MAJOR bump)
- Deprecation timeline: 8 weeks notice before breaking change

Ejemplo:
```yaml
versions:
  v1:
    released: "2025-01-01"
    producer: "payments-team"
    status: "deprecated"
    sunset_date: "2026-03-01"
  v2:
    released: "2025-09-01"
    producer: "payments-team"
    status: "current"
    changes_from_v1:
      - removed: legacy_payment_method (nullable)
      - added: refund_amount (nullable, for refunds)
      - renamed: order_amount → amount_usd
```

**Paso 5: Governance & Ownership**
- Data Producer: team responsible for data creation
- Data Owner: person accountable for quality/SLA
- Consumers: teams using this contract
- Review cadence: quarterly SLA review

Ejemplo:
```yaml
governance:
  producer_team: "payments-platform"
  data_owner: "alice@company.com"
  secondary_owner: "bob@company.com"
  consumers:
    - team: "analytics"
      usage: "BI dashboards, revenue reporting"
    - team: "fraud-detection"
      usage: "Real-time fraud scoring"
  review_cadence: "quarterly"
  escalation_path: "data-platform@company.com"
```

**Paso 6: Testing & Validation Strategy**
- Unit tests: downstream transformations
- Contract tests: schema + SLA validations
- Integration tests: end-to-end flow
- Quality gates: automated DQ checks

Ejemplo:
```yaml
validation:
  unit_tests:
    - "test_amount_positivity.py"
    - "test_status_enum.py"
  contract_tests:
    - schema_matches_v2
    - uniqueness_order_id_global
    - null_rate_status < 0.1%
    - freshness_max_lag < 2h
  dq_checks:
    - "amount_usd range validation"
    - "referential integrity: customer_id"
    - "distribution drift detection"
  ci_gates:
    - "schema_validation (fail if breaking)"
    - "coverage >= 80%"
    - "SLA compliance >= 95%"
```

---

### TEMPLATE COMPLETO

```yaml
# Contract: domain.entity.v{N}
name: sales.order
version: 2
status: current

# Descubrimiento
description: "Order records from payment system. Includes order details, customer FK, and status."
domain: "sales"
grain: "one row per order"
frequency: "hourly updates"
sources:
  - system: "payment-gateway"
    table: "transactions"
    lag: "< 5 minutes"

# Schema
fields:
  order_id:
    type: BIGINT
    nullable: false
    uniqueness: PRIMARY_KEY
  customer_id:
    type: BIGINT
    nullable: false
  amount_usd:
    type: DECIMAL(12,2)
    nullable: false
    range: [0, 1000000]
  status:
    type: STRING
    nullable: false
    enum: ["pending", "shipped", "delivered", "cancelled"]
  created_date:
    type: DATE
    nullable: false
  created_at:
    type: TIMESTAMP
    nullable: false

# SLAs
sla:
  freshness:
    max_lag_hours: 2
    frequency: "every 1 hour"
  completeness:
    min_rows_per_day: 1000
    null_tolerance:
      order_id: 0%
  accuracy:
    uniqueness: "order_id globally unique"
  availability:
    uptime_target: "99.5%"

# Versioning & Evolution
versions:
  v2:
    released: "2026-02-01"
    changes: "added refund_amount"
  v1:
    released: "2025-01-01"
    status: "deprecated"

# Governance
producer_team: "sales-platform"
data_owner: "alice@company.com"
consumers:
  - "analytics-team"
  - "fraud-team"

# Validation
tests:
  contract:
    - "schema_v2_matches"
    - "uniqueness_order_id"
    - "freshness < 2h"
  quality:
    - "amount_range_valid"
    - "customer_id_referential_integrity"
```

---

### OUTPUT ESPERADO

1. **Contract YAML:** Completo (schema + SLA + versioning)
2. **Comunicación:** Template de anuncio para consumidores
3. **Testing:** Script para validar contract compliance
4. **Roadmap:** Timeline si hay breaking changes planeados

---

### REFERENCIAS RELACIONADAS

- **Resource (Tier 1):** `resources/data-engineering/data-contract-patterns.md` (Teoría: compatible vs breaking changes)
- **Resource (Tier 2):** `resources/data-engineering/testing-data-pipelines.md` (Testing para contracts)
- **Instructions:** `instructions_or_rules/data-engineering/modular/02-guidelines.md` (Sección 2.4 Naming & Contracts)
- **Instrucciones:** `instructions_or_rules/data-engineering/modular/04-quality.md` (Data Quality checks)
