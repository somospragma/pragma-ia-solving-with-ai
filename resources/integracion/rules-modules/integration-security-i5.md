# IS5 - Protección de APIs

## Descripción
Reglas para protección y seguridad de APIs expuestas.

## Severidad: HIGH

## Reglas

### IS5.1 Rate Limiting
- ✅ Límites por cliente/IP
- ✅ Límites por endpoint
- ✅ Respuesta 429 Too Many Requests
- ✅ Headers informativos (X-RateLimit-*)

### IS5.2 Throttling
- ✅ Limitar requests por segundo
- ✅ Protección contra spike de tráfico
- ✅ Queue para requests excedentes
- ✅ Configuración por tier de cliente

### IS5.3 API Gateway
- ✅ Usar API Gateway (Kong, Apigee, AWS API Gateway)
- ✅ Políticas de seguridad centralizadas
- ✅ Autenticación en gateway
- ✅ Transformación y validación

### IS5.4 CORS Configurado
- ✅ Whitelist de orígenes permitidos
- ❌ No usar wildcard (*) en producción
- ✅ Métodos HTTP permitidos definidos
- ✅ Headers permitidos definidos

### IS5.5 Protección contra DDoS
- ✅ Rate limiting agresivo
- ✅ IP blacklisting
- ✅ WAF (Web Application Firewall)
- ✅ CDN con protección DDoS

### IS5.6 Input Validation
- ✅ Validar todos los inputs
- ✅ Validar path parameters
- ✅ Validar query parameters
- ✅ Validar request body

### IS5.7 Output Encoding
- ✅ Encodear respuestas apropiadamente
- ✅ Content-Type correcto
- ✅ Prevenir XSS en respuestas
- ✅ Sanitizar datos de salida

### IS5.8 Error Handling Seguro
- ❌ No exponer stack traces
- ❌ No exponer información del sistema
- ✅ Mensajes de error genéricos
- ✅ Loggear detalles internamente

### IS5.9 HTTPS Obligatorio
- ✅ Forzar HTTPS
- ✅ Redirect HTTP → HTTPS
- ✅ HSTS header
- ✅ Secure cookies

### IS5.10 API Versioning
- ✅ Versionamiento explícito
- ✅ Deprecación gradual
- ✅ Múltiples versiones soportadas
- ✅ Documentación por versión
