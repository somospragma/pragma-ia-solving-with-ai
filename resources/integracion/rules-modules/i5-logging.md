# I5 - Logging y Observabilidad

## Descripción
Este ruleset evalúa las prácticas de logging, monitoreo y observabilidad en servicios de integración.

## Severidad: HIGH

## Reglas

### 5.1 Niveles de Log Apropiados
**Severidad**: MEDIUM

**Descripción**: Usar niveles de log correctamente.

**Criterios**:
- ✅ **ERROR**: Errores que requieren atención inmediata
- ✅ **WARN**: Situaciones anómalas que no detienen el flujo
- ✅ **INFO**: Eventos importantes del negocio
- ✅ **DEBUG**: Información detallada para troubleshooting
- ✅ **TRACE**: Información muy detallada (solo desarrollo)

**Ejemplos**:
```
ERROR: Failed to process payment - transaction rolled back
WARN: Response time exceeded threshold (5s)
INFO: Order 12345 created successfully
DEBUG: Transforming customer data: {...}
```

---

### 5.2 Correlation ID
**Severidad**: HIGH

**Descripción**: Incluir correlation ID en todos los logs.

**Criterios**:
- ✅ Generar correlation ID al inicio del flujo
- ✅ Propagar ID a través de todos los servicios
- ✅ Incluir en headers HTTP (X-Correlation-ID)
- ✅ Loggear ID en cada entrada de log

**Ejemplo**:
```
INFO [correlationId=abc-123-def-456] Processing order
INFO [correlationId=abc-123-def-456] Calling payment service
ERROR [correlationId=abc-123-def-456] Payment failed
```

---

### 5.3 Structured Logging
**Severidad**: MEDIUM

**Descripción**: Usar formato estructurado (JSON) para logs.

**Criterios**:
- ✅ Formato JSON para facilitar parsing
- ✅ Campos consistentes: timestamp, level, message, correlationId
- ✅ Metadata adicional como campos separados
- ✅ Compatible con herramientas de análisis (ELK, Splunk)

**Ejemplo**:
```json
{
  "timestamp": "2024-01-15T10:30:00.123Z",
  "level": "INFO",
  "correlationId": "abc-123",
  "service": "order-service",
  "message": "Order created",
  "orderId": "12345",
  "customerId": "67890"
}
```

---

### 5.4 No Loggear Datos Sensibles
**Severidad**: CRITICAL

**Descripción**: Evitar logging de información sensible.

**Criterios**:
- ❌ No loggear: passwords, tokens, API keys
- ❌ No loggear: números de tarjeta, CVV
- ❌ No loggear: PII sin enmascarar
- ✅ Enmascarar datos sensibles si es necesario

**Ejemplo de Enmascaramiento**:
```
✅ Correcto: "cardNumber": "****-****-****-1234"
❌ Incorrecto: "cardNumber": "4532-1234-5678-1234"
```

---

### 5.5 Contexto de Negocio
**Severidad**: MEDIUM

**Descripción**: Incluir contexto de negocio relevante en logs.

**Criterios**:
- ✅ IDs de entidades (orderId, customerId, etc.)
- ✅ Operación de negocio ejecutada
- ✅ Usuario o sistema que inició la operación
- ✅ Resultado de la operación

---

### 5.6 Performance Metrics
**Severidad**: HIGH

**Descripción**: Loggear métricas de rendimiento.

**Criterios**:
- ✅ Tiempo de respuesta por operación
- ✅ Tiempo de llamadas a servicios externos
- ✅ Tamaño de payloads
- ✅ Throughput (requests/segundo)

**Ejemplo**:
```
INFO [correlationId=abc-123] Operation completed
  duration: 1234ms
  externalCallDuration: 890ms
  payloadSize: 15KB
```

---

### 5.7 Health Checks
**Severidad**: HIGH

**Descripción**: Implementar endpoints de health check.

**Criterios**:
- ✅ Endpoint /health o /actuator/health
- ✅ Verificar dependencias críticas
- ✅ Respuesta rápida (<1 segundo)
- ✅ Formato estándar

**Ejemplo**:
```json
GET /health
{
  "status": "UP",
  "components": {
    "database": {"status": "UP"},
    "paymentService": {"status": "UP"},
    "cache": {"status": "DOWN", "error": "Connection timeout"}
  }
}
```

---

### 5.8 Métricas Expuestas
**Severidad**: MEDIUM

**Descripción**: Exponer métricas para monitoreo.

**Criterios**:
- ✅ Endpoint /metrics (Prometheus format)
- ✅ Métricas de negocio (orders_created, payments_processed)
- ✅ Métricas técnicas (cpu_usage, memory_usage)
- ✅ Métricas de errores (error_rate, error_count)

---

### 5.9 Distributed Tracing
**Severidad**: MEDIUM

**Descripción**: Implementar tracing distribuido.

**Criterios**:
- ✅ Integración con Jaeger, Zipkin o similar
- ✅ Spans para operaciones importantes
- ✅ Propagación de trace context
- ✅ Visualización de flujos end-to-end

---

### 5.10 Alertas Configuradas
**Severidad**: HIGH

**Descripción**: Configurar alertas para eventos críticos.

**Criterios**:
- ✅ Alertas para tasa de errores alta
- ✅ Alertas para latencia elevada
- ✅ Alertas para servicios caídos
- ✅ Alertas para umbrales de negocio

---

## Checklist de Evaluación

| ID | Criterio | Cumple | Observaciones |
|----|----------|--------|---------------|
| 5.1 | Niveles de log apropiados | ⬜ | |
| 5.2 | Correlation ID | ⬜ | |
| 5.3 | Structured logging | ⬜ | |
| 5.4 | No loggear datos sensibles | ⬜ | |
| 5.5 | Contexto de negocio | ⬜ | |
| 5.6 | Performance metrics | ⬜ | |
| 5.7 | Health checks | ⬜ | |
| 5.8 | Métricas expuestas | ⬜ | |
| 5.9 | Distributed tracing | ⬜ | |
| 5.10 | Alertas configuradas | ⬜ | |
