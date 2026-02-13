# IS2 - Cifrado de Datos

## Descripción
Reglas de seguridad para cifrado de datos en tránsito y en reposo.

## Severidad: CRITICAL

## Reglas

### IS2.1 TLS 1.2+ Obligatorio
- ✅ TLS 1.2 o superior
- ❌ No permitir SSL 3.0, TLS 1.0, TLS 1.1
- ✅ Cipher suites seguros
- ✅ Perfect Forward Secrecy (PFS)

### IS2.2 Certificados Válidos
- ✅ Certificados de CA confiable
- ✅ No usar certificados autofirmados en producción
- ✅ Validar fecha de expiración
- ✅ Renovar antes de expirar

### IS2.3 Cifrado en Reposo
- ✅ Cifrar datos sensibles en base de datos
- ✅ Cifrar archivos sensibles
- ✅ Usar algoritmos fuertes (AES-256)
- ✅ Gestión segura de claves

### IS2.4 Cifrado de Campos Sensibles
- ✅ Cifrar PII (nombres, emails, teléfonos)
- ✅ Cifrar datos financieros
- ✅ Cifrar credenciales
- ✅ Cifrado a nivel de campo

### IS2.5 Key Management
- ✅ Usar gestores de claves (KMS, Vault)
- ✅ Rotar claves periódicamente
- ✅ No hardcodear claves
- ✅ Separar claves por ambiente

### IS2.6 Hashing de Passwords
- ✅ Usar bcrypt, scrypt o Argon2
- ❌ No usar MD5 o SHA1
- ✅ Salt único por password
- ✅ Múltiples iteraciones

### IS2.7 Protección de Datos en Logs
- ❌ No loggear passwords
- ❌ No loggear tokens completos
- ❌ No loggear números de tarjeta
- ✅ Enmascarar datos sensibles

### IS2.8 Secure Communication Channels
- ✅ HTTPS para APIs REST
- ✅ WSS para WebSockets
- ✅ SFTP para transferencia de archivos
- ✅ Cifrado end-to-end cuando sea necesario

### IS2.9 Validación de Certificados
- ✅ Validación de certificados habilitada
- ✅ Verificar cadena de confianza
- ✅ Verificar revocación (OCSP, CRL)
- ❌ No deshabilitar validación

### IS2.10 Protección de Backups
- ✅ Cifrar backups
- ✅ Almacenamiento seguro
- ✅ Control de acceso a backups
- ✅ Pruebas de restauración
