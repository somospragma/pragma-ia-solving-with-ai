# IS1 - Autenticación y Autorización

## Descripción
Reglas de seguridad para autenticación y autorización en servicios de integración.

## Severidad: CRITICAL

## Reglas

### IS1.1 OAuth 2.0 / OpenID Connect
- ✅ Usar OAuth 2.0 para APIs REST
- ✅ OpenID Connect para autenticación de usuarios
- ✅ Tokens JWT con firma
- ✅ Validar tokens en cada request
- ✅ Refresh tokens para sesiones largas

### IS1.2 API Keys
- ✅ Solo para APIs internas
- ✅ Rotar periódicamente
- ✅ No incluir en URLs
- ✅ Usar headers (X-API-Key)

### IS1.3 Mutual TLS
- ✅ Para comunicaciones B2B críticas
- ✅ Certificados de cliente válidos
- ✅ Validación de certificados habilitada

### IS1.4 Control de Acceso Basado en Roles (RBAC)
- ✅ Roles definidos claramente
- ✅ Permisos granulares
- ✅ Principio de mínimo privilegio
- ✅ Auditoría de accesos

### IS1.5 No Usar Basic Auth sin TLS
- ❌ Evitar Basic Auth en HTTP
- ✅ Solo con HTTPS si es necesario
- ✅ Preferir OAuth 2.0

### IS1.6 Validación de Tokens
- ✅ Verificar firma del token
- ✅ Validar expiración
- ✅ Validar issuer y audience
- ✅ Validar scopes/permisos

### IS1.7 Session Management
- ✅ Timeouts de sesión apropiados
- ✅ Invalidación de sesiones
- ✅ Protección contra session fixation
- ✅ Tokens de sesión seguros

### IS1.8 Multi-Factor Authentication (MFA)
- ✅ MFA para operaciones críticas
- ✅ MFA para acceso administrativo
- ✅ Soporte para TOTP, SMS, biometría

### IS1.9 Auditoría de Autenticación
- ✅ Loggear intentos de autenticación
- ✅ Loggear fallos de autenticación
- ✅ Alertas por intentos sospechosos
- ✅ Incluir IP, timestamp, usuario

### IS1.10 Rate Limiting por Usuario
- ✅ Límites por usuario/cliente
- ✅ Protección contra brute force
- ✅ Bloqueo temporal después de fallos
