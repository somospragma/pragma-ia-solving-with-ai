# IS7 - Gestión de Certificados

## Descripción
Reglas para gestión segura de certificados SSL/TLS.

## Severidad: HIGH

## Reglas

### IS7.1 Certificados de CA Confiable
- ✅ Usar certificados de CA reconocida
- ❌ No usar certificados autofirmados en producción
- ✅ Validar cadena de confianza
- ✅ Mantener truststore actualizado

### IS7.2 Monitoreo de Expiración
- ✅ Monitorear fechas de expiración
- ✅ Alertas 30 días antes de expirar
- ✅ Proceso de renovación definido
- ✅ Renovación automática cuando sea posible

### IS7.3 Rotación de Certificados
- ✅ Rotar certificados periódicamente
- ✅ Proceso de rotación sin downtime
- ✅ Mantener certificados antiguos temporalmente
- ✅ Documentar procedimiento

### IS7.4 Almacenamiento Seguro
- ✅ Keystores cifrados
- ✅ Passwords de keystore seguros
- ✅ Control de acceso a keystores
- ✅ No incluir en control de versiones

### IS7.5 Validación de Certificados
- ✅ Validación habilitada en clientes
- ✅ Verificar hostname
- ✅ Verificar fecha de validez
- ✅ Verificar revocación (OCSP, CRL)

### IS7.6 Certificados por Ambiente
- ✅ Certificados diferentes por ambiente
- ✅ Wildcard certificates cuando sea apropiado
- ✅ SAN (Subject Alternative Names) configurado
- ✅ Documentar certificados por ambiente

### IS7.7 Mutual TLS
- ✅ Certificados de cliente para B2B
- ✅ Validación de certificados de cliente
- ✅ Whitelist de certificados permitidos
- ✅ Revocación de certificados comprometidos

### IS7.8 Cipher Suites Seguros
- ✅ Solo cipher suites fuertes
- ❌ Deshabilitar cipher suites débiles
- ✅ Perfect Forward Secrecy (PFS)
- ✅ Actualizar según recomendaciones

### IS7.9 Inventario de Certificados
- ✅ Mantener inventario actualizado
- ✅ Documentar propósito de cada certificado
- ✅ Responsables definidos
- ✅ Auditoría periódica

### IS7.10 Respuesta a Compromiso
- ✅ Procedimiento de revocación definido
- ✅ Revocación inmediata si es comprometido
- ✅ Notificación a partes afectadas
- ✅ Emisión de nuevo certificado
