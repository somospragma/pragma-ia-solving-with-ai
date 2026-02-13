# I7 - Conectividad y Protocolos

## Descripción
Este ruleset evalúa la configuración y uso de conectores, protocolos y comunicación con sistemas externos.

## Severidad: HIGH

## Reglas

### 7.1 Timeouts Configurados
**Severidad**: CRITICAL

**Descripción**: Todos los conectores deben tener timeouts definidos.

**Criterios**:
- ✅ Connection timeout configurado
- ✅ Read/Response timeout configurado
- ✅ Timeouts apropiados por operación
- ✅ Documentados en SLA

**Ejemplo**:
```yaml
http:
  connectionTimeout: 5000  # 5 segundos
  responseTimeout: 30000   # 30 segundos
```

---

### 7.2 Connection Pooling
**Severidad**: HIGH

**Descripción**: Usar connection pooling para eficiencia.

**Criterios**:
- ✅ Pool habilitado para HTTP clients
- ✅ Pool habilitado para DB connections
- ✅ Tamaño de pool apropiado
- ✅ Timeout de idle connections
- ✅ Validación de conexiones

---

### 7.3 Keep-Alive
**Severidad**: MEDIUM

**Descripción**: Usar keep-alive para conexiones HTTP.

**Criterios**:
- ✅ Keep-alive habilitado
- ✅ Timeout de keep-alive configurado
- ✅ Máximo de requests por conexión

**Beneficios**:
- Reduce latencia
- Reduce overhead de TCP handshake
- Mejora throughput

---

### 7.4 Retry Policies
**Severidad**: HIGH

**Descripción**: Configurar políticas de reintento para conectores.

**Criterios**:
- ✅ Reintentos para errores transitorios
- ✅ Backoff exponencial
- ✅ Máximo de reintentos definido
- ✅ No reintentar errores permanentes

---

### 7.5 Circuit Breaker
**Severidad**: HIGH

**Descripción**: Implementar circuit breakers para servicios externos.

**Criterios**:
- ✅ Circuit breaker configurado
- ✅ Threshold de fallos definido
- ✅ Timeout de recuperación
- ✅ Fallback definido

---

### 7.6 Protocolos Seguros
**Severidad**: CRITICAL

**Descripción**: Usar protocolos seguros para comunicación.

**Criterios**:
- ✅ HTTPS en lugar de HTTP
- ✅ SFTP en lugar de FTP
- ✅ FTPS como alternativa
- ✅ TLS 1.2+ para todos los protocolos

---

### 7.7 Validación de Certificados
**Severidad**: CRITICAL

**Descripción**: Validar certificados SSL/TLS apropiadamente.

**Criterios**:
- ✅ Validación de certificados habilitada
- ✅ No deshabilitar validación en producción
- ✅ Truststore configurado correctamente
- ✅ Certificados no expirados

---

### 7.8 Compresión de Datos
**Severidad**: LOW

**Descripción**: Habilitar compresión para reducir ancho de banda.

**Criterios**:
- ✅ Compresión gzip habilitada
- ✅ Accept-Encoding en requests
- ✅ Content-Encoding en responses
- ✅ Comprimir solo payloads >1KB

---

### 7.9 Manejo de Reconexiones
**Severidad**: MEDIUM

**Descripción**: Manejar reconexiones automáticamente.

**Criterios**:
- ✅ Reconexión automática habilitada
- ✅ Backoff entre reconexiones
- ✅ Máximo de intentos de reconexión
- ✅ Logging de reconexiones

---

### 7.10 Protocolos Apropiados
**Severidad**: MEDIUM

**Descripción**: Usar el protocolo apropiado para cada caso de uso.

**Protocolos Comunes**:
- **HTTP/HTTPS**: APIs REST, webhooks
- **SOAP/HTTP**: Servicios SOAP
- **JMS/AMQP**: Mensajería asíncrona
- **JDBC**: Bases de datos
- **FTP/SFTP**: Transferencia de archivos
- **WebSocket**: Comunicación bidireccional en tiempo real
- **gRPC**: Comunicación de alto rendimiento

**Criterios**:
- ✅ Protocolo apropiado para el caso de uso
- ✅ Configuración óptima del protocolo
- ✅ Documentación del protocolo usado

---

## Checklist de Evaluación

| ID | Criterio | Cumple | Observaciones |
|----|----------|--------|---------------|
| 7.1 | Timeouts configurados | ⬜ | |
| 7.2 | Connection pooling | ⬜ | |
| 7.3 | Keep-alive | ⬜ | |
| 7.4 | Retry policies | ⬜ | |
| 7.5 | Circuit breaker | ⬜ | |
| 7.6 | Protocolos seguros | ⬜ | |
| 7.7 | Validación de certificados | ⬜ | |
| 7.8 | Compresión de datos | ⬜ | |
| 7.9 | Manejo de reconexiones | ⬜ | |
| 7.10 | Protocolos apropiados | ⬜ | |
