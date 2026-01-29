# AWS IAM Users Audit - Security Best Practices

## Descripción General

Herramienta de auditoría de seguridad que valida el cumplimiento de buenas prácticas en IAM Users, incluyendo MFA, rotación de claves, inactividad, políticas inline amplias y password policy.

---

## Configuración Técnica

### Región
- **Global**: IAM es un servicio global en AWS (no regional)

### Herramientas MCP Requeridas
```json
{
  "awslabs.iam-mcp-server": "Enumerar usuarios, claves, MFA, políticas, password policy",
  "awslabs.cloudtrail-mcp-server": "Obtener actividad de usuarios (últimos 90 días)"
}
```

### Parámetros de Entrada (Configurables por Usuario)
```
aws_profile: <user-defined>                    # Perfil AWS del usuario (ej: "chapter", "prod", "dev")
aws_credentials_source: "profile" | "env"      # Fuente de credenciales

audit_parameters:
  mfa_required: true                           # Validar MFA habilitado
  key_rotation_days: 90                        # Máximo días sin rotación de claves
  inactivity_threshold_days: 90                # Máximo días sin actividad
  check_inline_policies: true                  # Validar políticas inline amplias
  check_password_policy: true                  # Validar password policy robusta
  
severity_levels: ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]
```

**Nota**: El `aws_profile` debe ser especificado por el usuario según su configuración local de AWS CLI.

---

## Definiciones Operativas

### 1. MFA Habilitado

```
Criterio:
- Usuario tiene al menos 1 dispositivo MFA activo
- Tipos válidos: Virtual MFA, U2F, Hardware token

Estado:
- ✅ PASS: MFA habilitado
- ❌ FAIL: MFA no habilitado
- ⚠️ WARNING: MFA habilitado pero no usado recientemente

Severidad si falla:
- CRITICAL: Usuario con acceso a consola sin MFA
- HIGH: Usuario con claves de acceso sin MFA
```

### 2. Rotación de Claves de Acceso

```
Criterio:
- AccessKeyCreateDate <= 90 días desde hoy
- Máximo 2 claves activas por usuario

Estado:
- ✅ PASS: Claves rotadas dentro de 90 días
- ⚠️ WARNING: Clave próxima a cumplir 90 días (>75 días)
- ❌ FAIL: Clave sin rotar >90 días

Severidad si falla:
- HIGH: Clave sin rotar >90 días
- MEDIUM: Clave sin rotar >75 días
- LOW: Más de 2 claves activas
```

### 3. Usuarios Inactivos

```
Criterio:
- Última actividad (login, API call) > 90 días
- Basado en CloudTrail events

Estado:
- ✅ PASS: Usuario activo en últimos 90 días
- ⚠️ WARNING: Usuario inactivo 60-90 días
- ❌ FAIL: Usuario inactivo >90 días

Severidad si falla:
- MEDIUM: Usuario inactivo >90 días (considerar desactivar)
- LOW: Usuario inactivo 60-90 días (monitorear)
```

### 4. Políticas Inline Amplias

```
Criterio:
- Detectar políticas inline con:
  * Action: "*" (todas las acciones)
  * Resource: "*" (todos los recursos)
  * Effect: "Allow"

Combinaciones peligrosas:
- Action: "*" + Resource: "*" = CRÍTICO
- Action: "s3:*" + Resource: "*" = ALTO
- Action: "*" + Resource: "arn:aws:iam::*:*" = CRÍTICO

Estado:
- ✅ PASS: Sin políticas inline amplias
- ⚠️ WARNING: Política inline con permisos amplios pero limitados
- ❌ FAIL: Política inline con "*" en Action y Resource

Severidad si falla:
- CRITICAL: Action "*" + Resource "*"
- HIGH: Action "*" o Resource "*" (pero no ambos)
- MEDIUM: Política inline con permisos amplios (ej: s3:*)
```

### 5. Password Policy Robusta

```
Criterio (validar a nivel de cuenta):
- Longitud mínima: >= 14 caracteres
- Requiere mayúsculas: true
- Requiere minúsculas: true
- Requiere números: true
- Requiere símbolos: true
- Expiración: <= 90 días
- Historial: >= 24 contraseñas recordadas
- Bloqueo temporal: >= 5 intentos fallidos

Estado:
- ✅ PASS: Cumple todos los criterios
- ⚠️ WARNING: Cumple la mayoría pero falta alguno
- ❌ FAIL: No cumple criterios mínimos

Severidad si falla:
- CRITICAL: Sin password policy o muy débil
- HIGH: Falta requisito importante (ej: símbolos)
- MEDIUM: Falta requisito menor (ej: historial)
```

---

## Tareas de Auditoría

### 1. Enumerar IAM Users

Para cada usuario en la cuenta:

```
Datos a recopilar:
- UserName
- UserId
- Arn
- CreateDate
- PasswordLastUsed (si aplica)
- Tags (si existen)
- Groups (grupos a los que pertenece)
- AttachedPolicies (políticas adjuntas)
- InlinePolicies (políticas inline)
```

### 2. Validar MFA

Para cada usuario:

```
Consulta:
- ListMFADevices(UserName)

Resultado:
- MFADevices: lista de dispositivos MFA
- SerialNumber: identificador del dispositivo
- EnableDate: fecha de habilitación

Lógica:
- Si MFADevices.length > 0 → MFA habilitado ✅
- Si MFADevices.length == 0 → MFA no habilitado ❌
```

### 3. Validar Rotación de Claves

Para cada usuario:

```
Consulta:
- ListAccessKeys(UserName)

Resultado por clave:
- AccessKeyId
- Status (Active/Inactive)
- CreateDate
- LastUsedDate (si aplica)

Cálculo:
- age_days = (today - CreateDate).days
- Si age_days <= 90 → PASS ✅
- Si 75 < age_days <= 90 → WARNING ⚠️
- Si age_days > 90 → FAIL ❌

Validaciones adicionales:
- Contar claves activas (máximo 2)
- Si > 2 claves activas → WARNING
```

### 4. Validar Inactividad

Para cada usuario:

```
Consulta CloudTrail:
- LookupEvents(UserName, últimos 90 días)

Resultado:
- EventTime: timestamp del último evento
- EventName: tipo de evento (ConsoleLogin, AssumeRole, etc.)

Cálculo:
- last_activity = max(EventTime) de todos los eventos
- inactivity_days = (today - last_activity).days

Lógica:
- Si inactivity_days <= 90 → PASS ✅
- Si 60 < inactivity_days <= 90 → WARNING ⚠️
- Si inactivity_days > 90 → FAIL ❌

Nota: Si no hay eventos en CloudTrail, considerar como inactivo desde CreateDate
```

### 5. Validar Políticas Inline Amplias

Para cada usuario:

```
Consulta:
- ListUserPolicies(UserName)
- GetUserPolicy(UserName, PolicyName)

Para cada política inline:
- Parsear JSON de la política
- Buscar Statement con Effect: "Allow"
- Validar Action y Resource

Lógica de detección:
```

```python
for statement in policy["Statement"]:
    if statement["Effect"] == "Allow":
        actions = statement.get("Action", [])
        resources = statement.get("Resource", [])
        
        # Normalizar a lista
        if isinstance(actions, str):
            actions = [actions]
        if isinstance(resources, str):
            resources = [resources]
        
        # Detectar "*"
        has_wildcard_action = "*" in actions
        has_wildcard_resource = "*" in resources
        
        # Severidad
        if has_wildcard_action and has_wildcard_resource:
            severity = "CRITICAL"  # Action "*" + Resource "*"
        elif has_wildcard_action or has_wildcard_resource:
            severity = "HIGH"      # Uno de los dos es "*"
        elif any("*" in action for action in actions):
            severity = "MEDIUM"    # Wildcard en acción específica (ej: s3:*)
        else:
            severity = "LOW"       # Sin wildcards
```

### 6. Validar Password Policy

Consulta a nivel de cuenta:

```
Consulta:
- GetAccountPasswordPolicy()

Resultado:
{
  "MinimumPasswordLength": 14,
  "RequireSymbols": true,
  "RequireNumbers": true,
  "RequireUppercaseCharacters": true,
  "RequireLowercaseCharacters": true,
  "AllowUsersToChangePassword": true,
  "ExpirePasswords": true,
  "MaxPasswordAge": 90,
  "PasswordReusePrevention": 24,
  "HardExpiry": false
}

Validación:
- MinimumPasswordLength >= 14 → PASS
- RequireSymbols == true → PASS
- RequireNumbers == true → PASS
- RequireUppercaseCharacters == true → PASS
- RequireLowercaseCharacters == true → PASS
- MaxPasswordAge <= 90 → PASS
- PasswordReusePrevention >= 24 → PASS

Si falla alguno → WARNING o FAIL según cantidad
```

---

## Salida

### Markdown: `iam-users-audit-report-<account-id>.md`

**Estructura**:
## Salida

### Markdown: `iam-users-audit-report-<account-id>.md`

**Estructura**:

```markdown
# AWS IAM Users Audit Report
## Account: 123456789012 | Generated: 2026-01-29 14:30 UTC

---

## Executive Summary

| Métrica | Valor | Status |
|---------|-------|--------|
| **Total IAM Users** | 25 | - |
| **Users with MFA** | 20 | 80% ✅ |
| **Users without MFA** | 5 | 20% ❌ |
| **Keys rotated (<90d)** | 22 | 88% ✅ |
| **Keys not rotated (>90d)** | 3 | 12% ❌ |
| **Active users (<90d)** | 23 | 92% ✅ |
| **Inactive users (>90d)** | 2 | 8% ⚠️ |
| **Users with inline policies** | 8 | 32% ⚠️ |
| **Users with broad inline policies** | 3 | 12% ❌ |
| **Password Policy Status** | MEDIUM | ⚠️ |

---

## Hallazgos Críticos (CRITICAL)

### 1. Política Inline Amplísima: user-admin

**Severidad**: 🔴 CRITICAL  
**Usuario**: user-admin  
**Tipo**: Política Inline  
**Nombre Política**: AdminAccess

**Evidencia**:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "*",
      "Resource": "*"
    }
  ]
}
```

**Problema**: Acceso total a todos los servicios y recursos  
**Recomendación**: 
- Reemplazar con política administrada `AdministratorAccess` (mejor auditada)
- O usar políticas específicas por servicio
- Considerar usar roles en lugar de usuarios para acceso administrativo

---

## Hallazgos Altos (HIGH)

### 1. Usuario sin MFA: developer-01

**Severidad**: 🟠 HIGH  
**Usuario**: developer-01  
**Tipo**: MFA  
**Última Actividad**: 2026-01-28 (hace 1 día)

**Problema**: Usuario activo sin MFA habilitado  
**Recomendación**: 
- Habilitar MFA inmediatamente
- Usar virtual MFA (Google Authenticator, Authy) o hardware token
- Requerir MFA para acceso a consola

---

### 2. Clave de Acceso sin Rotar: data-processor

**Severidad**: 🟠 HIGH  
**Usuario**: data-processor  
**AccessKeyId**: AKIAIOSFODNN7EXAMPLE  
**Edad**: 125 días  
**Última Actividad**: 2026-01-15

**Problema**: Clave sin rotar >90 días  
**Recomendación**: 
- Rotar clave inmediatamente
- Crear nueva clave
- Actualizar aplicaciones con nueva clave
- Desactivar clave antigua después de 7 días
- Implementar rotación automática

---

### 3. Política Inline Amplia: lambda-executor

**Severidad**: 🟠 HIGH  
**Usuario**: lambda-executor  
**Tipo**: Política Inline  
**Nombre Política**: LambdaExecution

**Evidencia**:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:*",
      "Resource": "*"
    }
  ]
}
```

**Problema**: Acceso a todos los buckets S3 sin restricción  
**Recomendación**: 
- Limitar a buckets específicos
- Usar ARNs específicos en Resource
- Ejemplo: `"Resource": "arn:aws:s3:::my-bucket/*"`

---

## Hallazgos Medios (MEDIUM)

### 1. Usuario Inactivo: old-contractor

**Severidad**: 🟡 MEDIUM  
**Usuario**: old-contractor  
**Última Actividad**: 2025-10-15 (hace 106 días)  
**Inactividad**: 106 días

**Problema**: Usuario sin actividad >90 días  
**Recomendación**: 
- Desactivar usuario si ya no es necesario
- Revocar claves de acceso
- Remover de grupos
- Considerar eliminar si no se necesita

---

### 2. Password Policy Incompleta

**Severidad**: 🟡 MEDIUM  
**Tipo**: Password Policy  
**Nivel**: Cuenta

**Configuración Actual**:
```
✅ Longitud mínima: 14 caracteres
✅ Requiere mayúsculas: Sí
✅ Requiere minúsculas: Sí
✅ Requiere números: Sí
❌ Requiere símbolos: No
✅ Expiración: 90 días
✅ Historial: 24 contraseñas
✅ Bloqueo temporal: 5 intentos
```

**Problema**: Falta requisito de símbolos  
**Recomendación**: 
- Habilitar requisito de símbolos
- Aumentar longitud mínima a 16 caracteres
- Considerar expiración más corta (60 días)

---

## Hallazgos Bajos (LOW)

### 1. Múltiples Claves Activas: ci-user

**Severidad**: 🔵 LOW  
**Usuario**: ci-user  
**Claves Activas**: 3  
**Recomendación**: 
- Máximo 2 claves activas por usuario
- Desactivar clave más antigua
- Implementar política de máximo 2 claves

---

## Tabla Detallada: Usuarios

| Usuario | MFA | Claves | Edad Clave | Inactivo | Inline Policies | Status |
|---------|-----|--------|-----------|----------|-----------------|--------|
| user-admin | ✅ | 1 | 45d | 1d | 1 (CRITICAL) | 🔴 |
| developer-01 | ❌ | 2 | 60d | 1d | 0 | 🟠 |
| data-processor | ✅ | 1 | 125d | 15d | 0 | 🟠 |
| lambda-executor | ✅ | 1 | 30d | 5d | 1 (HIGH) | 🟠 |
| old-contractor | ✅ | 1 | 200d | 106d | 0 | 🟡 |
| ci-user | ✅ | 3 | 20d | 2h | 0 | 🔵 |
| ... | ... | ... | ... | ... | ... | ... |

---

## Recomendaciones Prioritarias

### Inmediato (Próximas 24 horas)

1. **Habilitar MFA en developer-01**
   - Impacto: Reduce riesgo de compromiso de credenciales
   - Esfuerzo: Bajo (5 minutos)
   - Severidad: HIGH

2. **Rotar clave de data-processor**
   - Impacto: Reduce riesgo de clave comprometida
   - Esfuerzo: Bajo (15 minutos)
   - Severidad: HIGH

### Corto Plazo (Próxima semana)

3. **Refinar políticas inline amplias**
   - user-admin: Usar AdministratorAccess o políticas específicas
   - lambda-executor: Limitar a buckets específicos
   - Impacto: Reduce riesgo de acceso no autorizado
   - Esfuerzo: Medio (1-2 horas)
   - Severidad: HIGH/MEDIUM

4. **Desactivar usuario inactivo**
   - old-contractor: Revocar acceso
   - Impacto: Reduce superficie de ataque
   - Esfuerzo: Bajo (10 minutos)
   - Severidad: MEDIUM

### Mediano Plazo (Próximo mes)

5. **Mejorar Password Policy**
   - Agregar requisito de símbolos
   - Aumentar longitud mínima
   - Impacto: Mejora seguridad de contraseñas
   - Esfuerzo: Bajo (5 minutos)
   - Severidad: MEDIUM

6. **Implementar rotación automática de claves**
   - Usar AWS Secrets Manager o similar
   - Impacto: Automatiza rotación de claves
   - Esfuerzo: Alto (4-8 horas)
   - Severidad: MEDIUM

---

## Checklist de Acciones

- [ ] Habilitar MFA en developer-01
- [ ] Rotar clave de data-processor
- [ ] Refinar política de user-admin
- [ ] Refinar política de lambda-executor
- [ ] Desactivar old-contractor
- [ ] Mejorar Password Policy
- [ ] Implementar rotación automática
- [ ] Revisar políticas adjuntas (managed policies)
- [ ] Auditar acceso a servicios críticos
- [ ] Documentar cambios en CMDB

---

## Fuente de Datos

- **Fuente**: AWS IAM API + CloudTrail
- **Fecha de Generación**: 2026-01-29 14:30 UTC
- **Perfil AWS**: Especificado por el usuario
- **Período de Auditoría**: 90 días
- **Cuenta AWS**: 123456789012

---

## Próximos Pasos

1. **Revisar Reporte**: Compartir con equipo de seguridad
2. **Priorizar Hallazgos**: Enfocarse en CRITICAL y HIGH
3. **Ejecutar Acciones**: Seguir checklist
4. **Validar Cambios**: Verificar que se aplicaron correctamente
5. **Repetir Auditoría**: Ejecutar mensualmente

---

**Generado**: 2026-01-29 14:30 UTC  
**Cuenta AWS**: 123456789012  
**Perfil AWS**: Especificado por el usuario  
**Período**: Últimos 90 días
```

---

## Reglas de Implementación

### Consultas IAM
- Todas las consultas deben usar IAM API
- Incluir timestamps en todos los eventos
- Validar que CloudTrail esté habilitado para obtener inactividad

### Formato de Datos
- Tiempos: ISO8601 UTC
- Severidad: CRITICAL, HIGH, MEDIUM, LOW, INFO
- Status: ✅ PASS, ⚠️ WARNING, ❌ FAIL

### Validaciones
- Verificar que usuario existe
- Verificar que CloudTrail está habilitado
- Validar que password policy existe

### Umbrales Fijos
- MFA: Requerido para todos
- Rotación de claves: 90 días máximo
- Inactividad: 90 días máximo
- Password Policy: Según criterios definidos

---

## Interpretación de Severidades

| Severidad | Descripción | Acción |
|-----------|-------------|--------|
| 🔴 CRITICAL | Riesgo inmediato de seguridad | Resolver en 24 horas |
| 🟠 HIGH | Riesgo significativo | Resolver en 1 semana |
| 🟡 MEDIUM | Riesgo moderado | Resolver en 1 mes |
| 🔵 LOW | Riesgo bajo | Resolver en 3 meses |
| ⚪ INFO | Información | Monitorear |

---

## Próximos Pasos

1. **Revisar Reporte**: Compartir con equipo de seguridad
2. **Priorizar Hallazgos**: Enfocarse en CRITICAL y HIGH
3. **Ejecutar Acciones**: Seguir checklist de recomendaciones
4. **Validar Cambios**: Verificar que se aplicaron correctamente
5. **Repetir Auditoría**: Ejecutar mensualmente para detectar cambios
