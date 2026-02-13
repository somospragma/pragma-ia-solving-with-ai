# I2 - Manejo de Errores y Excepciones

## Descripción
Este ruleset evalúa las estrategias de manejo de errores, reintentos y recuperación en servicios de integración.

## Severidad: CRITICAL

## Reglas

### 2.1 Try-Catch en Flujos Críticos
**Severidad**: CRITICAL

**Descripción**: Todos los flujos deben tener manejo de excepciones apropiado.

**Criterios**:
- ✅ Try-catch implementado en todos los flujos principales
- ✅ Catch específico por tipo de error
- ✅ Logging de errores con contexto
- ✅ Respuestas de error estandarizadas

**Ejemplo**:
```xml
<try>
  <flow>
    <!-- Lógica principal -->
  </flow>
  <catch type="CONNECTIVITY">
    <log level="ERROR" message="Connection failed: #[error.description]"/>
    <set-payload value='{"error": "SERVICE_UNAVAILABLE"}'/>
  </catch>
  <catch type="VALIDATION">
    <log level="WARN" message="Validation failed: #[error.description]"/>
    <set-payload value='{"error": "INVALID_INPUT"}'/>
  </catch>
</try>
```

---

### 2.2 Códigos de Error Estandarizados
**Severidad**: HIGH

**Descripción**: Usar catálogo de códigos de error consistente.

**Criterios**:
- ✅ Códigos de error documentados
- ✅ Formato: `{CATEGORIA}_{DESCRIPCION}`
- ✅ Ejemplos:
  - `AUTH_INVALID_TOKEN`
  - `VALIDATION_MISSING_FIELD`
  - `CONNECTIVITY_TIMEOUT`
  - `BUSINESS_INSUFFICIENT_FUNDS`

**Estructura de Respuesta de Error**:
```json
{
  "error": {
    "code": "VALIDATION_MISSING_FIELD",
    "message": "Required field 'email' is missing",
    "timestamp": "2024-01-15T10:30:00Z",
    "traceId": "abc-123-def-456",
    "details": [
      {
        "field": "email",
        "issue": "required"
      }
    ]
  }
}
```

---

### 2.3 Políticas de Reintento
**Severidad**: HIGH

**Descripción**: Implementar reintentos con backoff exponencial para errores transitorios.

**Criterios**:
- ✅ Reintentos solo para errores transitorios (timeouts, 503, etc.)
- ✅ No reintentar errores permanentes (400, 401, 404)
- ✅ Backoff exponencial: 1s, 2s, 4s, 8s
- ✅ Máximo de reintentos configurado (ej: 3)
- ✅ Jitter para evitar thundering herd

**Ejemplo de Configuración**:
```yaml
retry:
  maxAttempts: 3
  backoff:
    initialInterval: 1000
    multiplier: 2
    maxInterval: 10000
  retryableErrors:
    - CONNECTIVITY_TIMEOUT
    - HTTP_503
    - HTTP_429
```

---

### 2.4 Circuit Breaker
**Severidad**: HIGH

**Descripción**: Implementar circuit breakers para servicios externos.

**Criterios**:
- ✅ Circuit breaker en llamadas a servicios externos
- ✅ Estados: CLOSED, OPEN, HALF_OPEN
- ✅ Threshold de fallos configurado (ej: 50% en 10 requests)
- ✅ Timeout de recuperación (ej: 30 segundos)
- ✅ Fallback definido cuando circuito está abierto

**Estados del Circuit Breaker**:
- **CLOSED**: Operación normal, requests pasan
- **OPEN**: Demasiados fallos, requests fallan inmediatamente
- **HALF_OPEN**: Período de prueba, permite algunos requests

---

### 2.5 Timeouts Configurados
**Severidad**: CRITICAL

**Descripción**: Todos los conectores deben tener timeouts definidos.

**Criterios**:
- ✅ Connection timeout configurado
- ✅ Read/Response timeout configurado
- ✅ Timeouts apropiados por tipo de operación:
  - Queries rápidas: 2-5 segundos
  - Operaciones complejas: 10-30 segundos
  - Batch processing: 60+ segundos
- ✅ Timeouts documentados en SLA

---

### 2.6 Estrategias de Compensación
**Severidad**: HIGH

**Descripción**: Implementar rollback/compensación para transacciones distribuidas.

**Criterios**:
- ✅ Saga pattern para transacciones largas
- ✅ Operaciones de compensación definidas
- ✅ Idempotencia en compensaciones
- ✅ Logging de compensaciones ejecutadas

**Ejemplo de Saga**:
```
1. Crear orden → Compensación: Cancelar orden
2. Reservar inventario → Compensación: Liberar inventario
3. Procesar pago → Compensación: Reembolsar pago
```

---

### 2.7 Dead Letter Queues
**Severidad**: MEDIUM

**Descripción**: Usar DLQ para mensajes que fallan repetidamente.

**Criterios**:
- ✅ DLQ configurada para colas principales
- ✅ Mensajes movidos a DLQ después de max reintentos
- ✅ Proceso de revisión y reprocesamiento de DLQ
- ✅ Alertas cuando DLQ crece

---

### 2.8 Logging de Errores
**Severidad**: HIGH

**Descripción**: Registrar errores con contexto suficiente para troubleshooting.

**Criterios**:
- ✅ Nivel de log apropiado (ERROR para errores críticos)
- ✅ Incluir correlation ID
- ✅ Stack trace completo
- ✅ Contexto de negocio (IDs de entidades)
- ✅ No loggear datos sensibles

**Ejemplo**:
```
ERROR [correlationId=abc-123] Failed to process order
  orderId: 12345
  customerId: 67890
  error: Connection timeout to payment service
  stackTrace: ...
```

---

### 2.9 Manejo de Errores Parciales
**Severidad**: MEDIUM

**Descripción**: Manejar apropiadamente operaciones batch con fallos parciales.

**Criterios**:
- ✅ Continuar procesando items exitosos
- ✅ Reportar items fallidos
- ✅ Permitir reprocesamiento de fallidos
- ✅ Respuesta indica éxitos y fallos

**Ejemplo de Respuesta**:
```json
{
  "totalProcessed": 100,
  "successful": 95,
  "failed": 5,
  "errors": [
    {"itemId": "123", "error": "VALIDATION_ERROR"},
    {"itemId": "456", "error": "DUPLICATE"}
  ]
}
```

---

### 2.10 Graceful Degradation
**Severidad**: MEDIUM

**Descripción**: Degradar funcionalidad gracefully cuando servicios fallan.

**Criterios**:
- ✅ Fallback a funcionalidad reducida
- ✅ Usar datos en caché cuando sea apropiado
- ✅ Informar al usuario sobre funcionalidad limitada
- ✅ Recuperación automática cuando servicio vuelve

---

## Checklist de Evaluación

| ID | Criterio | Cumple | Observaciones |
|----|----------|--------|---------------|
| 2.1 | Try-catch implementado | ⬜ | |
| 2.2 | Códigos de error estandarizados | ⬜ | |
| 2.3 | Políticas de reintento | ⬜ | |
| 2.4 | Circuit breaker | ⬜ | |
| 2.5 | Timeouts configurados | ⬜ | |
| 2.6 | Estrategias de compensación | ⬜ | |
| 2.7 | Dead letter queues | ⬜ | |
| 2.8 | Logging de errores | ⬜ | |
| 2.9 | Manejo de errores parciales | ⬜ | |
| 2.10 | Graceful degradation | ⬜ | |
