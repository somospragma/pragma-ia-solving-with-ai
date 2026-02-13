# IS9 - Control de Acceso

## Descripción
Reglas para control de acceso y autorización granular.

## Severidad: HIGH

## Reglas

### IS9.1 Principio de Mínimo Privilegio
- ✅ Otorgar solo permisos necesarios
- ✅ Revisar permisos periódicamente
- ✅ Remover permisos no utilizados
- ✅ Cuentas de servicio con permisos limitados

### IS9.2 Role-Based Access Control (RBAC)
- ✅ Roles bien definidos
- ✅ Permisos asignados a roles
- ✅ Usuarios asignados a roles
- ✅ Jerarquía de roles si es necesario

### IS9.3 Attribute-Based Access Control (ABAC)
- ✅ Políticas basadas en atributos
- ✅ Contexto de acceso (tiempo, ubicación)
- ✅ Atributos de usuario y recurso
- ✅ Evaluación dinámica de políticas

### IS9.4 Validación de Autorización
- ✅ Validar en cada request
- ✅ No confiar en cliente
- ✅ Validar en backend
- ✅ Validar acceso a recursos específicos

### IS9.5 Segregación de Funciones
- ✅ Separar funciones críticas
- ✅ Aprobaciones de múltiples personas
- ✅ No permitir auto-aprobación
- ✅ Auditoría de acciones críticas

### IS9.6 Control de Acceso a APIs
- ✅ Autenticación requerida
- ✅ Autorización por endpoint
- ✅ Scopes/permisos granulares
- ✅ Rate limiting por usuario

### IS9.7 Control de Acceso a Datos
- ✅ Filtrado por permisos de usuario
- ✅ Row-level security
- ✅ Column-level security
- ✅ Enmascaramiento de datos sensibles

### IS9.8 Acceso Temporal
- ✅ Permisos con expiración
- ✅ Acceso just-in-time
- ✅ Revocación automática
- ✅ Auditoría de accesos temporales

### IS9.9 Control de Acceso a Configuración
- ✅ Solo administradores
- ✅ Cambios auditados
- ✅ Aprobación requerida
- ✅ Versionamiento de configuración

### IS9.10 Prevención de Privilege Escalation
- ✅ Validar permisos en cada operación
- ✅ No permitir cambio de roles sin autorización
- ✅ Validar tokens/sesiones
- ✅ Monitorear intentos de escalación
