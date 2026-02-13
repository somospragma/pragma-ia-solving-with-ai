# IS3 - Gestión de Credenciales y Secretos

## Descripción
Reglas para gestión segura de credenciales, API keys y secretos.

## Severidad: CRITICAL

## Reglas

### IS3.1 No Hardcodear Credenciales
- ❌ No credenciales en código fuente
- ❌ No credenciales en archivos de configuración
- ❌ No credenciales en control de versiones
- ✅ Usar gestores de secretos

### IS3.2 Gestores de Secretos
- ✅ HashiCorp Vault
- ✅ AWS Secrets Manager
- ✅ Azure Key Vault
- ✅ Google Secret Manager
- ✅ CyberArk

### IS3.3 Variables de Entorno
- ✅ Credenciales en variables de entorno
- ✅ No loggear variables de entorno
- ✅ Diferentes credenciales por ambiente
- ✅ Inyección segura en runtime

### IS3.4 Rotación de Credenciales
- ✅ Rotar passwords cada 90 días
- ✅ Rotar API keys periódicamente
- ✅ Rotación automática cuando sea posible
- ✅ Proceso documentado

### IS3.5 Principio de Mínimo Privilegio
- ✅ Credenciales con permisos mínimos
- ✅ Cuentas de servicio dedicadas
- ✅ No usar cuentas de administrador
- ✅ Revisar permisos periódicamente

### IS3.6 Cifrado de Credenciales
- ✅ Cifrar credenciales en reposo
- ✅ Cifrar en tránsito
- ✅ No almacenar en texto plano
- ✅ Usar algoritmos fuertes

### IS3.7 Auditoría de Acceso a Secretos
- ✅ Loggear acceso a secretos
- ✅ Loggear cambios de credenciales
- ✅ Alertas por accesos anómalos
- ✅ Revisión periódica de logs

### IS3.8 Separación por Ambiente
- ✅ Credenciales diferentes por ambiente
- ✅ No usar credenciales de producción en dev
- ✅ Aislamiento de secretos
- ✅ Control de acceso por ambiente

### IS3.9 Revocación de Credenciales
- ✅ Proceso de revocación definido
- ✅ Revocación inmediata en caso de compromiso
- ✅ Lista de credenciales activas
- ✅ Limpieza de credenciales obsoletas

### IS3.10 Protección de API Keys
- ✅ No incluir en URLs
- ✅ Usar headers (X-API-Key)
- ✅ Rate limiting por API key
- ✅ Monitoreo de uso
