# Data Contracts: Patrones de Versionado, SLAs y Evolución de Schemas

Una Data Contract es un **acuerdo explícito entre productor y consumidor** sobre estructura, calidad y disponibilidad de datos. Este documento describe cómo diseñarlas, versionarlas y evolucionar sin romper consumidores.

## 1. Anatomía de una Data Contract

Una contract completa incluye:

```yaml
# Contract: sales.order.v2
---
name: sales.order
version: 2  # Semantic versioning
owner: sales-platform-team
consumers:
  - finance-team (analytics)
  - warehouse-team (reporting)
  - ml-team (predictions)

# Estructura (Schema)
schema:
  order_id:
    type: BIGINT
    nullable: false
    uniqueness: PRIMARY_KEY
  customer_id:
    type: BIGINT
    nullable: false
  order_date:
    type: DATE
    nullable: false
    format: "YYYY-MM-DD"
  amount_usd:
    type: DECIMAL(12,2)
    nullable: false
    range: [0, 1000000]
  status:
    type: STRING
    nullable: false
    enum: ["pending", "shipped", "delivered", "cancelled"]
  created_at:
    type: TIMESTAMP
    nullable: false

# SLAs (Service Level Agreements)
sla:
  freshness:
    max_lag_hours: 2  # Data no más viejo de 2 horas
    frequency: "every 1 hour"
  completeness:
    min_rows_per_day: 1000
    null_tolerance:
      amount_usd: 0%  # 0% nulls allowed
      order_date: 0%
  accuracy:
    uniqueness: order_id must be unique (global)
  availability:
    uptime_target: "99.5%"

# Histórico de cambios
changelog:
  v2:
    date: 2026-02-20
    changes:
      - added: refund_amount (nullable, for reshipments)
      - deprecated: legacy_sku (to be removed in v4)
  v1:
    date: 2025-01-01
    changes:
      - initial: basic order schema
```

---

## 2. Ciclo de Vida: Forward & Backward Compatibility

### Cambio COMPATIBLE (No breaking)

**Agregación de columnas opcionales:**
```
v2 → v3: agregar `discount_code` (NULLABLE)
✅ Consumidores v2 siguen trabajando (ignoran la columna).
✅ Productores v3 rellenan con NULL si no hay dato.
✅ Consumidores v3 pueden verificar presence antes de usar.
```

**Renaming con alias:**
```
v2: `order_amount`
v3: `order_amount_usd` (rename), pero mantener alias `order_amount` → `order_amount_usd`
✅ Código legacy sigue leyendo `order_amount`.
✅ Código nuevo usa `order_amount_usd`.
```

**Extensión de enums (compatible hacia atrás):**
```
v2: status ∈ {pending, shipped, delivered, cancelled}
v3: status ∈ {pending, shipped, delivered, cancelled, returned, refunded}
✅ Consumidores v2 ven `returned` como value desconocido (manejar con default).
✅ No rompe parsing.
```

---

### Cambio INCOMPATIBLE (Breaking)

**Estas acciones REQUIEREN nuevaversion major y plan de migración:**

1. **Eliminar columnas:**
   ```
   v2 → v3: remover `legacy_sku`
   ❌ Consumidores v2 fallan (column not found).
   ✅ Solución: Deprecate en v2, eliminar en v4+2 releases.
   ```

2. **Cambiar tipos:**
   ```
   v2: amount BIGINT
   v3: amount DECIMAL  (or STRING)
   ❌ Consumidores v2 fallan (type mismatch).
   ✅ Solución: Crear nueva columna `amount_new`, mantener `amount`, migrar gradualmente.
   ```

3. **Restricturar nullability:**
   ```
   v2: notes NULLABLE
   v3: notes NOT NULL
   ❌ Consumidores esperan nulls, fallan cuando se aplica NOT NULL.
   ✅ Solución: Comenzar validation, deprecate nulls, cambiar en v+2.
   ```

4. **Cambiar cardinalidad o claves:**
   ```
   v2: order_id PRIMARY_KEY (1 fila por order)
   v3: order_id permite duplicates (agregó items detallados)
   ❌ Consumidores usan distinct(order_id), obtienen resultados incorrectos.
   ✅ Solución: Crear nueva tabla `order_items`, mantener esquema de `orders`.
   ```

---

## 3. Estrategia de Versionado

### Semantic Versioning para Schemas

```
domain.entity.v{MAJOR}.{MINOR}.{PATCH}
```

- **MAJOR:** Breaking changes (requiere migración consumidor).
- **MINOR:** Compatible changes (nuevas columnas, nuevos enums).
- **PATCH:** Non-schema changes (SLA adjustments, documentation).

### Tabla de Versiones

| Cambio | Tipo | MAJOR | MINOR | PATCH | Acción |
|--------|------|-------|-------|-------|--------|
| Agregar columna NULLABLE | Compatible | - | ↑ | - | Publicar v+.1.0, deprecate notice 4 semanas |
| Remover columna | Breaking | ↑ | ✓ | - | Deprecate 8 semanas, migrar consumidores, release v+1.0 |
| Cambiar tipo | Breaking | ↑ | ✓ | - | Coexistir columnas (old/new), migrar gradualmente |
| Cambiar SLA | Non-breaking | - | - | ↑ | Comunicar a consumidores, update contract |
| Renaming (con alias) | Compatible | - | ↑ | - | Alias vivo 3+ releases, deprecate en v+1 |

---

## 4. Comunicación de Cambios

### Timeline para Breaking Changes

```
Semana 1: Propuesta de cambio + impacto (Slack, PR)
Semana 2-4: Deprecation notice publicado
Semana 5-8: Consumidores migran código + tests
Semana 9: Release v{MAJOR+1}.0
```

### Template de Notificación de Cambio

```markdown
## Data Contract Change: sales.order v2 → v3

**Change Type:** COMPATIBLE (Minor version bump)
**Effective Date:** 2026-03-15
**Migration Required:** No

### What's New
- Added: `refund_amount` (DECIMAL, nullable) for reshipments
- Added: `shipping_carrier` (STRING, nullable) for logistics tracking

### Files to Update
- Schema DDL: `schemas/sales/order.yaml`
- Tests: `tests/contracts/test_order_v3.py`

### Examples
```python
# Before (v2)
df = spark.table("sales.order").select("order_id", "amount")

# After (v3, backwards compatible)
df = spark.table("sales.order").select("order_id", "amount", "refund_amount")
# Can ignore `refund_amount` if not needed
```

### Questions?
→ Slack #data-contracts or @sales-platform-team
```

---

## 5. Implementación: Git + Schema Registry

### Opción A: Versionado en Git

```
schemas/
├── data-engineering/
│   ├── sales/
│   │   └── order/
│   │       ├── order.v1.avsc  (Avro schema)
│   │       ├── order.v2.avsc
│   │       └── contract.yaml  (SLAs, owners, changelog)
│   └── finance/
│       └── invoice/
│           ├── invoice.v1.avsc
│           └── contract.yaml
```

**Ventajas:**
- ✅ Version control integral.
- ✅ PR reviews antes de cambios.
- ✅ Histórico completo.

**Desventajas:**
- ❌ No hay enforcement automático en runtime.

### Opción B: Schema Registry (Confluent / AWS Glue)

```
Producer writes to Kafka topic → Schema Registry validates
                                 (v2 required)
Consumer reads → Compatibility check
                (fetch v1? compatibility=BACKWARD)
```

**Ventajas:**
- ✅ Enforcement automático: rechaza writes no compatibles.
- ✅ Central registry (UI para exploración).
- ✅ Integración nativa con Kafka.

**Desventajas:**
- ❌ Overhead operacional (otro componente).
- ❌ Documentación de SLAs fuera del registry.

### Recomendación

**Usar Git + Schema Registry:**
- Git: Source of truth para schemas + contracts + changelog.
- Registry: Enforcement en runtime.
- Pipeline: PR merge → schema registry update.

---

## 6. Ejemplo: Evolución Paso a Paso

### Cambio: Agregar `refund_amount` a sales.order

**Paso 1: Propuesta (Git branch)**
```
Branch: feature/order-refund-tracking
Modified: schemas/sales/order/contract.yaml
- Version: 2 → 3 (MINOR)
- Added: refund_amount field
- Updated: SLA (freshness adjusted)
- Created: migration guide
```

**Paso 2: Review & Merge**
```
Revisores: @sales-platform, @ml-team, @finance-team
Approval: Confirmar compatibilidad
Merge: → main
```

**Paso 3: Registrar en Schema Registry**
```bash
# Post-merge CI job
./scripts/publish-schema.sh schemas/sales/order/order.v3.avsc

# Output: Schema v3 registered, compatibility: BACKWARD OK
```

**Paso 4: Consumidores Opten (No es urgente)**
```python
# Consumidor puede ignorar refund_amount por ahora
df = spark.table("sales.order").selectExpr("order_id", "amount")

# O adoptar gradualmente
df = spark.table("sales.order").selectExpr(
  "order_id", 
  "amount", 
  "coalesce(refund_amount, 0) as refund_amount"
)
```

**Paso 5: Deprecación (8 semanas después si breaking)**
```
N/A: Este cambio es compatible, sin deprecación.
```

---

## 7. SLA Examples

### Freshness SLA

```yaml
freshness:
  target_lag_minutes: 60
  warning_threshold: 45 min
  critical_threshold: 90 min
  
# Enforcement in CI
if data_age > 90min:
  alert slack://sales-team  (critical)
else if data_age > 45min:
  alert slack://data-platform (warning)
```

### Completeness SLA

```yaml
completeness:
  min_rows_per_batch: 1000
  null_tolerance:
    amount: 0%         (crítico, no nulls)
    notes: 100%        (opcional, puede ser todo nulls)
    status: 0.1%       (< 0.1% nulls acceptable)
```

### Accuracy SLA

```yaml
accuracy:
  uniqueness:
    order_id: GLOBALLY UNIQUE (duplicates = 0)
  freshness: max_lag_hours: 2
  data_quality_score: >= 95%  (% rows passing all checks)
```

---

## Referencias

- [Apache Avro Schema Evolution](https://avro.apache.org/docs/current/spec.html#Schema+Resolution)
- [Confluent Schema Registry Compatibility](https://docs.confluent.io/cloud/current/client-apps/schemas/manage-schemas.html)
- [Great Expectations Data Contracts](https://docs.greatexpectations.io/docs/guides/expectations/)
- [AWS Glue Data Catalog Schema Versioning](https://docs.aws.amazon.com/glue/latest/dg/schema-registry-concept.html)
