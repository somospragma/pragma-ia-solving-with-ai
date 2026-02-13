# I8 - Versionamiento y Gestión de Cambios

## Descripción
Este ruleset evalúa las prácticas de versionamiento de APIs, servicios y contratos.

## Severidad: HIGH

## Reglas

### 8.1 Versionamiento Explícito
**Severidad**: HIGH

**Descripción**: Todos los servicios y APIs deben tener versión explícita.

**Criterios**:
- ✅ Versión en URI: `/api/v1/customers`
- ✅ Versión en nombre de servicio
- ✅ Versión en contratos (WSDL, OpenAPI)
- ✅ Semantic versioning (MAJOR.MINOR.PATCH)

**Estrategias de Versionamiento**:
```
✅ URI Versioning: /api/v1/customers
✅ Header Versioning: Accept: application/vnd.api.v1+json
✅ Query Parameter: /api/customers?version=1
```

---

### 8.2 Compatibilidad Hacia Atrás
**Severidad**: HIGH

**Descripción**: Mantener compatibilidad hacia atrás cuando sea posible.

**Criterios**:
- ✅ Agregar campos opcionales, no eliminar
- ✅ No cambiar tipos de datos existentes
- ✅ No cambiar semántica de operaciones
- ✅ Deprecar en lugar de eliminar

**Cambios Compatibles**:
- ✅ Agregar nuevo endpoint
- ✅ Agregar campo opcional
- ✅ Agregar valor a enum
- ✅ Hacer campo requerido opcional

**Cambios Incompatibles (Breaking)**:
- ❌ Eliminar endpoint
- ❌ Eliminar campo
- ❌ Cambiar tipo de dato
- ❌ Hacer campo opcional requerido
- ❌ Cambiar formato de respuesta

---

### 8.3 Estrategia de Deprecación
**Severidad**: HIGH

**Descripción**: Deprecar versiones antiguas gradualmente.

**Criterios**:
- ✅ Anunciar deprecación con 6-12 meses de anticipación
- ✅ Marcar endpoints como deprecated en documentación
- ✅ Incluir header de deprecación en respuestas
- ✅ Proveer guía de migración
- ✅ Monitorear uso de versiones deprecadas

**Ejemplo de Header**:
```
Deprecation: true
Sunset: Sat, 31 Dec 2024 23:59:59 GMT
Link: <https://api.example.com/docs/migration>; rel="deprecation"
```

---

### 8.4 Múltiples Versiones en Paralelo
**Severidad**: MEDIUM

**Descripción**: Soportar múltiples versiones simultáneamente.

**Criterios**:
- ✅ Mantener al menos 2 versiones activas
- ✅ Routing automático por versión
- ✅ Monitoreo por versión
- ✅ Documentación de todas las versiones activas

---

### 8.5 Versionamiento de Contratos
**Severidad**: HIGH

**Descripción**: Versionar contratos de datos (schemas).

**Criterios**:
- ✅ JSON Schema versionado
- ✅ XSD versionado
- ✅ OpenAPI spec versionado
- ✅ Contratos en control de versiones (Git)

**Ejemplo**:
```
/schemas
  /v1
    - customer.schema.json
  /v2
    - customer.schema.json
```

---

### 8.6 Changelog Documentado
**Severidad**: MEDIUM

**Descripción**: Mantener changelog de cambios entre versiones.

**Criterios**:
- ✅ Archivo CHANGELOG.md
- ✅ Cambios agrupados por versión
- ✅ Fecha de cada release
- ✅ Breaking changes claramente marcados
- ✅ Guías de migración

**Formato**:
```markdown
# Changelog

## [2.0.0] - 2024-01-15
### Breaking Changes
- Removed deprecated field `oldField`
- Changed response format for /customers

### Added
- New endpoint /customers/{id}/orders
- Support for pagination

### Fixed
- Fixed timeout issue in payment service
```

---

### 8.7 Feature Flags
**Severidad**: MEDIUM

**Descripción**: Usar feature flags para cambios graduales.

**Criterios**:
- ✅ Feature flags para funcionalidad nueva
- ✅ Habilitar/deshabilitar sin redespliegue
- ✅ Rollout gradual (canary, blue-green)
- ✅ Monitoreo por feature flag

---

### 8.8 Notificación a Consumidores
**Severidad**: HIGH

**Descripción**: Notificar a consumidores sobre cambios.

**Criterios**:
- ✅ Email a consumidores registrados
- ✅ Anuncio en portal de desarrolladores
- ✅ Headers de deprecación en respuestas
- ✅ Período de gracia antes de eliminar versión

---

### 8.9 Testing de Compatibilidad
**Severidad**: MEDIUM

**Descripción**: Probar compatibilidad entre versiones.

**Criterios**:
- ✅ Tests de regresión para versiones antiguas
- ✅ Contract testing (Pact, Spring Cloud Contract)
- ✅ Validación de schemas
- ✅ Tests de migración

---

### 8.10 Documentación de Versiones
**Severidad**: HIGH

**Descripción**: Documentar todas las versiones activas.

**Criterios**:
- ✅ Documentación por versión
- ✅ Diferencias entre versiones documentadas
- ✅ Guías de migración disponibles
- ✅ Ejemplos actualizados por versión

---

## Checklist de Evaluación

| ID | Criterio | Cumple | Observaciones |
|----|----------|--------|---------------|
| 8.1 | Versionamiento explícito | ⬜ | |
| 8.2 | Compatibilidad hacia atrás | ⬜ | |
| 8.3 | Estrategia de deprecación | ⬜ | |
| 8.4 | Múltiples versiones en paralelo | ⬜ | |
| 8.5 | Versionamiento de contratos | ⬜ | |
| 8.6 | Changelog documentado | ⬜ | |
| 8.7 | Feature flags | ⬜ | |
| 8.8 | Notificación a consumidores | ⬜ | |
| 8.9 | Testing de compatibilidad | ⬜ | |
| 8.10 | Documentación de versiones | ⬜ | |
