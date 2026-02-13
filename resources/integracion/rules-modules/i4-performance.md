# I4 - Rendimiento y Optimización

## Descripción
Este ruleset evalúa el rendimiento, escalabilidad y optimización de servicios de integración.

## Severidad: HIGH

## Reglas

### 4.1 Procesamiento Asíncrono
**Severidad**: MEDIUM

**Descripción**: Usar procesamiento asíncrono para operaciones largas.

**Criterios**:
- ✅ Operaciones >3 segundos deben ser asíncronas
- ✅ Retornar 202 Accepted con location header
- ✅ Endpoint para consultar estado
- ✅ Webhooks o polling para notificación

**Ejemplo**:
```
POST /api/v1/orders
Response: 202 Accepted
Location: /api/v1/orders/status/abc-123

GET /api/v1/orders/status/abc-123
Response: {"status": "processing", "progress": 50}
```

---

### 4.2 Connection Pooling
**Severidad**: HIGH

**Descripción**: Usar connection pooling para bases de datos y servicios externos.

**Criterios**:
- ✅ Pool configurado para DB connections
- ✅ Pool configurado para HTTP clients
- ✅ Tamaño de pool apropiado (10-50 típicamente)
- ✅ Timeout de idle connections
- ✅ Validación de conexiones

**Configuración Ejemplo**:
```yaml
datasource:
  pool:
    minSize: 5
    maxSize: 20
    maxWaitTime: 5000
    idleTimeout: 300000
```

---

### 4.3 Caché
**Severidad**: MEDIUM

**Descripción**: Implementar caché para datos frecuentemente accedidos.

**Criterios**:
- ✅ Caché para datos de referencia
- ✅ TTL apropiado configurado
- ✅ Estrategia de invalidación definida
- ✅ Headers de caché HTTP (ETag, Cache-Control)

**Estrategias de Caché**:
- **Cache-Aside**: Aplicación gestiona caché
- **Read-Through**: Caché carga datos automáticamente
- **Write-Through**: Escrituras pasan por caché
- **Write-Behind**: Escrituras asíncronas

---

### 4.4 Batch Processing
**Severidad**: MEDIUM

**Descripción**: Procesar múltiples items en lotes cuando sea posible.

**Criterios**:
- ✅ APIs soportan operaciones batch
- ✅ Tamaño de batch configurable
- ✅ Procesamiento paralelo dentro del batch
- ✅ Manejo de errores parciales

**Ejemplo**:
```
POST /api/v1/customers/batch
Body: [
  {"name": "Customer 1"},
  {"name": "Customer 2"}
]
```

---

### 4.5 Streaming para Mensajes Grandes
**Severidad**: HIGH

**Descripción**: Usar streaming para archivos y payloads grandes.

**Criterios**:
- ✅ Streaming para archivos >10MB
- ✅ No cargar todo en memoria
- ✅ Procesamiento incremental
- ✅ Soporte para multipart/form-data

---

### 4.6 Compresión
**Severidad**: LOW

**Descripción**: Habilitar compresión para reducir tamaño de payloads.

**Criterios**:
- ✅ Compresión gzip habilitada
- ✅ Accept-Encoding: gzip en requests
- ✅ Content-Encoding: gzip en responses
- ✅ Comprimir solo payloads >1KB

---

### 4.7 Paginación
**Severidad**: HIGH

**Descripción**: Implementar paginación para colecciones grandes.

**Criterios**:
- ✅ Límite máximo de items por página (ej: 100)
- ✅ Parámetros: page, size
- ✅ Metadata de paginación en respuesta
- ✅ Links a siguiente/anterior página

---

### 4.8 Índices de Base de Datos
**Severidad**: HIGH

**Descripción**: Crear índices apropiados para queries frecuentes.

**Criterios**:
- ✅ Índices en columnas de búsqueda
- ✅ Índices compuestos para queries complejas
- ✅ Evitar over-indexing
- ✅ Monitorear uso de índices

---

### 4.9 Lazy Loading
**Severidad**: MEDIUM

**Descripción**: Cargar datos relacionados solo cuando se necesiten.

**Criterios**:
- ✅ No cargar relaciones por defecto
- ✅ Parámetro para incluir relaciones (expand, include)
- ✅ Evitar N+1 queries

**Ejemplo**:
```
GET /api/v1/customers/123
GET /api/v1/customers/123?expand=orders,addresses
```

---

### 4.10 Throttling
**Severidad**: MEDIUM

**Descripción**: Implementar throttling para proteger recursos.

**Criterios**:
- ✅ Límites de tasa por cliente
- ✅ Límites de tasa por endpoint
- ✅ Respuesta 429 cuando se excede
- ✅ Headers informativos

---

## Checklist de Evaluación

| ID | Criterio | Cumple | Observaciones |
|----|----------|--------|---------------|
| 4.1 | Procesamiento asíncrono | ⬜ | |
| 4.2 | Connection pooling | ⬜ | |
| 4.3 | Caché | ⬜ | |
| 4.4 | Batch processing | ⬜ | |
| 4.5 | Streaming | ⬜ | |
| 4.6 | Compresión | ⬜ | |
| 4.7 | Paginación | ⬜ | |
| 4.8 | Índices de BD | ⬜ | |
| 4.9 | Lazy loading | ⬜ | |
| 4.10 | Throttling | ⬜ | |
