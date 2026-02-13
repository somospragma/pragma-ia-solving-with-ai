# I3 - Seguridad en Integración

## Descripción
Este ruleset evalúa la implementación de controles de seguridad en servicios de integración.

## Severidad: CRITICAL

## Reglas

### 3.1 Autenticación
**Severidad**: CRITICAL

**Descripción**: Todos los endpoints deben requerir autenticación.

**Criterios**:
- ✅ OAuth 2.0 / OpenID Connect para APIs REST
- ✅ WS-Security para SOAP
- ✅ API Keys solo para APIs internas
- ✅ Mutual TLS para comunicaciones B2B
- ✅ No usar Basic Auth sin TLS

**Ejemplo OAuth 2.0**:
```
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

### 3.2 Autorización
**Severidad**: CRITICAL

**Descripción**: Implementar control de acceso basado en roles (RBAC).

**Criterios**:
- ✅ Validar permisos en cada operación
- ✅ Principio de mínimo privilegio
- ✅ Roles y permisos documentados
- ✅ Auditoría de accesos

---

### 3.3 Cifrado en Tránsito
**Severidad**: CRITICAL

**Descripción**: Usar TLS 1.2+ para todas las comunicaciones.

**Criterios**:
- ✅ TLS 1.2 o superior
- ✅ Certificados válidos y no expirados
- ✅ Cipher suites seguros
- ✅ No permitir SSL 3.0, TLS 1.0, TLS 1.1

---

### 3.4 Validación de Entrada
**Severidad**: HIGH

**Descripción**: Validar y sanitizar todos los inputs.

**Criterios**:
- ✅ Validación contra schemas (JSON Schema, XSD)
- ✅ Sanitización para prevenir inyección
- ✅ Validación de tipos de datos
- ✅ Límites de tamaño de payload
- ✅ Whitelist de caracteres permitidos

---

### 3.5 Gestión de Credenciales
**Severidad**: CRITICAL

**Descripción**: No hardcodear credenciales en código.

**Criterios**:
- ✅ Usar gestores de secretos (Vault, AWS Secrets Manager)
- ✅ Rotar credenciales periódicamente
- ✅ No loggear credenciales
- ✅ Cifrar credenciales en reposo

---

### 3.6 Rate Limiting
**Severidad**: HIGH

**Descripción**: Implementar límites de tasa para prevenir abuso.

**Criterios**:
- ✅ Rate limiting por cliente/IP
- ✅ Límites documentados
- ✅ Respuesta 429 Too Many Requests
- ✅ Headers informativos (X-RateLimit-*)

---

### 3.7 Protección contra Inyección
**Severidad**: CRITICAL

**Descripción**: Prevenir SQL injection, XPath injection, etc.

**Criterios**:
- ✅ Usar prepared statements
- ✅ Parametrizar queries
- ✅ Validar y escapar inputs
- ✅ No construir queries con concatenación

---

### 3.8 CORS Configurado
**Severidad**: MEDIUM

**Descripción**: Configurar CORS apropiadamente para APIs web.

**Criterios**:
- ✅ Whitelist de orígenes permitidos
- ✅ No usar wildcard (*) en producción
- ✅ Métodos HTTP permitidos definidos
- ✅ Headers permitidos definidos

---

### 3.9 Auditoría y Logging
**Severidad**: HIGH

**Descripción**: Registrar eventos de seguridad.

**Criterios**:
- ✅ Loggear intentos de autenticación
- ✅ Loggear cambios de autorización
- ✅ Loggear accesos a datos sensibles
- ✅ Incluir correlation ID y timestamp

---

### 3.10 Protección de Datos Sensibles
**Severidad**: CRITICAL

**Descripción**: Proteger PII y datos sensibles.

**Criterios**:
- ✅ Cifrar datos sensibles en reposo
- ✅ Enmascarar datos en logs
- ✅ Cumplir con GDPR/regulaciones
- ✅ Minimizar datos recolectados

---

## Checklist de Evaluación

| ID | Criterio | Cumple | Observaciones |
|----|----------|--------|---------------|
| 3.1 | Autenticación | ⬜ | |
| 3.2 | Autorización | ⬜ | |
| 3.3 | Cifrado TLS | ⬜ | |
| 3.4 | Validación de entrada | ⬜ | |
| 3.5 | Gestión de credenciales | ⬜ | |
| 3.6 | Rate limiting | ⬜ | |
| 3.7 | Protección contra inyección | ⬜ | |
| 3.8 | CORS configurado | ⬜ | |
| 3.9 | Auditoría y logging | ⬜ | |
| 3.10 | Protección de datos sensibles | ⬜ | |
