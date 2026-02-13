# IS6 - Auditoría y Trazabilidad

## Descripción
Reglas para auditoría, logging y trazabilidad de eventos de seguridad.

## Severidad: HIGH

## Reglas

### IS6.1 Logging de Eventos de Seguridad
- ✅ Loggear intentos de autenticación
- ✅ Loggear fallos de autorización
- ✅ Loggear acceso a datos sensibles
- ✅ Loggear cambios de configuración

### IS6.2 Correlation ID
- ✅ ID único por transacción
- ✅ Propagar a través de servicios
- ✅ Incluir en todos los logs
- ✅ Facilitar troubleshooting

### IS6.3 Información en Logs de Auditoría
- ✅ Timestamp preciso
- ✅ Usuario/sistema que ejecuta acción
- ✅ Acción ejecutada
- ✅ Resultado (éxito/fallo)
- ✅ IP de origen
- ✅ Datos relevantes (IDs de entidades)

### IS6.4 Protección de Logs
- ✅ Logs inmutables
- ✅ Almacenamiento seguro
- ✅ Control de acceso a logs
- ✅ Cifrado de logs sensibles

### IS6.5 Retención de Logs
- ✅ Política de retención definida
- ✅ Cumplir con regulaciones (GDPR, etc.)
- ✅ Archivado de logs antiguos
- ✅ Eliminación segura

### IS6.6 Monitoreo de Anomalías
- ✅ Detectar patrones anómalos
- ✅ Alertas por actividad sospechosa
- ✅ Múltiples fallos de autenticación
- ✅ Acceso desde IPs inusuales

### IS6.7 Audit Trail Completo
- ✅ Registro de todas las operaciones críticas
- ✅ Cambios en datos sensibles
- ✅ Cambios de permisos
- ✅ Cambios de configuración

### IS6.8 No Loggear Datos Sensibles
- ❌ No loggear passwords
- ❌ No loggear tokens completos
- ❌ No loggear números de tarjeta
- ✅ Enmascarar PII si es necesario

### IS6.9 Centralización de Logs
- ✅ Logs centralizados (ELK, Splunk)
- ✅ Búsqueda y análisis facilitados
- ✅ Correlación entre servicios
- ✅ Dashboards de seguridad

### IS6.10 Alertas de Seguridad
- ✅ Alertas en tiempo real
- ✅ Notificación a equipo de seguridad
- ✅ Escalamiento automático
- ✅ Runbooks para respuesta
