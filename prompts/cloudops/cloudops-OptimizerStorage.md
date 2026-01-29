# AWS EBS & Snapshots Huérfanos - Inventario y Análisis de Costos

## Descripción General

Herramienta automatizada que identifica volúmenes EBS y snapshots huérfanos (sin instancias o referencias asociadas) en AWS, calcula su costo mensual estimado y genera recomendaciones de optimización.

---

## Configuración Técnica

### Región
- **Fija**: `us-east-1` (US East N. Virginia)

### Herramientas MCP Requeridas
```json
{
  "awslabs.ec2-mcp-server": "Enumerar volúmenes EBS, snapshots, instancias, AMIs",
  "awslabs.aws-pricing-mcp-server": "Obtener precios vigentes de EBS y snapshots"
}
```

### Parámetros de Entrada (Configurables por Usuario)
```
region: "us-east-1"                          # Fija
age_days_threshold_for_snapshots: 30         # Marcar snapshots antiguos sin referencia (ajustable)
aws_profile: <user-defined>                  # Perfil AWS del usuario (ej: "chapter", "prod", "dev")
aws_credentials_source: "profile" | "env"    # Fuente de credenciales (profile o variables de entorno)
```

**Nota**: El `aws_profile` debe ser especificado por el usuario según su configuración local de AWS CLI. Si no se proporciona, usar credenciales por defecto del entorno.

---

## Definiciones Operativas

### Volumen EBS Huérfano
```
Criterios:
- State = "available"
- Attachments = [] (vacío, sin instancias asociadas)
- No está siendo usado por ninguna instancia EC2
```

### Snapshot Huérfano
```
Criterios (cualquiera de los siguientes):
1. VolumeId inexistente o borrado (volumen origen no existe)
2. No referenciado por ninguna AMI activa (pública o privada)
3. Antigüedad >= age_days_threshold_for_snapshots días
   Y no tiene tag "Retention=Keep" u otra política de retención explícita

Exclusiones:
- Snapshots con tag "Retention=Keep" (protegidos por política)
- Snapshots referenciados por AMIs activos
- Snapshots recientes (< age_days_threshold_for_snapshots)
```

### Casos Especiales a Validar
```
- Volúmenes con encrypted=false (sin cifrado)
- Snapshots públicos o compartidos con otras cuentas
- Snapshots en tier "Archive" (costo diferente, restore lento)
- Recursos sin tags (falta de gobierno de datos)
```

---

## Tareas de Análisis

### 1. Inventario de Volúmenes EBS

#### Recopilación de Datos
Para cada volumen en us-east-1:
```
- VolumeId (vol-xxxxx)
- Size (GiB)
- VolumeType (gp2, gp3, io1, io2, st1, sc1)
- State (available, in-use, deleting, deleted, error)
- Attachments (lista de instancias; vacío si huérfano)
- Encrypted (true/false)
- KmsKeyId (si encrypted=true)
- CreateTime (ISO8601 UTC)
- AvailabilityZone
- Iops (si aplica: io1, io2, gp3)
- Throughput (si aplica: gp3, st1)
- Tags (formato: key=value;key2=value2)
```

#### Filtrado de Huérfanos
```
Volumen_Huérfano = (State == "available") AND (Attachments.length == 0)
```

#### Salida Intermedia
```
volumeId, sizeGiB, volumeType, encrypted, kmsKeyId, createTime, iops, throughput, tags
```

### 2. Inventario de Snapshots

#### Recopilación de Datos
Para cada snapshot en us-east-1:
```
- SnapshotId (snap-xxxxx)
- VolumeId (volumen origen; puede no existir)
- Size (GiB)
- StartTime (ISO8601 UTC)
- State (completed, pending, error)
- Encrypted (true/false)
- KmsKeyId (si encrypted=true)
- StorageTier (Standard, Archive)
- Public (true/false)
- SharedWithAccounts (lista de account IDs)
- Tags (formato: key=value;key2=value2)
- Description (si aplica)
```

#### Validación de Referencias
Para cada snapshot:
```
1. Verificar si VolumeId existe:
   - Si NO existe → Marcar como "VolumeNotFound"
   
2. Verificar si está referenciado por AMIs activos:
   - Enumerar todos los AMIs (propios + compartidos)
   - Para cada AMI, revisar BlockDeviceMappings.SnapshotId
   - Si snapshot está en algún AMI → Marcar como "ReferencedByAMI"
   
3. Calcular antigüedad:
   - age_days = (now - StartTime).days
   - Si age_days >= age_days_threshold_for_snapshots → Marcar como "Old"
   
4. Revisar tags de retención:
   - Si tag "Retention=Keep" existe → Marcar como "RetentionProtected"
   
5. Determinar si es huérfano:
   - isOrphan = (VolumeNotFound OR (NOT ReferencedByAMI AND Old)) 
              AND NOT RetentionProtected
```

#### Salida Intermedia
```
snapshotId, volumeId, sizeGiB, startTime, storageTier, encrypted, kmsKeyId, 
public, sharedWithAccounts, referencedByAMIs, isOrphan, reason, tags
```

### 3. Consulta de Precios (AWS Pricing MCP)

#### Precios de Volúmenes EBS
Para cada `volumeType` en us-east-1:
```
Consulta MCP:
get_pricing(
  service="AmazonEBS",
  region="us-east-1",
  filters=[
    {"Field": "volumeType", "Value": "gp2", "Type": "EQUALS"},
    {"Field": "location", "Value": "US East (N. Virginia)", "Type": "EQUALS"}
  ]
)

Resultado esperado:
{
  "volumeType": "gp2",
  "pricePerGbMonth": 0.10,
  "sku": "ABCD1234EFGH5678",
  "effectiveDate": "2026-01-29",
  "currency": "USD"
}

Tipos a consultar: gp2, gp3, io1, io2, st1, sc1
```

#### Precios de Snapshots
Para cada `storageTier`:
```
Consulta MCP:
get_pricing(
  service="AmazonEBS",
  region="us-east-1",
  filters=[
    {"Field": "snapshotType", "Value": "Standard", "Type": "EQUALS"},
    {"Field": "location", "Value": "US East (N. Virginia)", "Type": "EQUALS"}
  ]
)

Resultado esperado:
{
  "snapshotType": "Standard",
  "pricePerGbMonth": 0.05,
  "sku": "IJKL9012MNOP3456",
  "effectiveDate": "2026-01-29",
  "currency": "USD"
}

Tipos a consultar: Standard, Archive
```

#### Mapeo de Precios
```
volumeType_prices = {
  "gp2": {"price": 0.10, "sku": "...", "date": "2026-01-29"},
  "gp3": {"price": 0.10, "sku": "...", "date": "2026-01-29"},
  "io1": {"price": 0.125, "sku": "...", "date": "2026-01-29"},
  "io2": {"price": 0.125, "sku": "...", "date": "2026-01-29"},
  "st1": {"price": 0.045, "sku": "...", "date": "2026-01-29"},
  "sc1": {"price": 0.015, "sku": "...", "date": "2026-01-29"}
}

snapshot_prices = {
  "Standard": {"price": 0.05, "sku": "...", "date": "2026-01-29"},
  "Archive": {"price": 0.01, "sku": "...", "date": "2026-01-29"}
}
```

### 4. Cálculo de Costos Mensuales

#### Para Volúmenes EBS
```
MonthlyCostUSD = sizeGiB * volumeType_prices[volumeType]["price"]

Ejemplo:
- Volumen gp2 de 100 GiB
- Precio: $0.10/GiB-mes
- Costo: 100 * 0.10 = $10.00/mes
```

#### Para Snapshots
```
MonthlyCostUSD = sizeGiB * snapshot_prices[storageTier]["price"]

Ejemplo:
- Snapshot Standard de 500 GiB
- Precio: $0.05/GiB-mes
- Costo: 500 * 0.05 = $25.00/mes

- Snapshot Archive de 500 GiB
- Precio: $0.01/GiB-mes
- Costo: 500 * 0.01 = $5.00/mes
```

### 5. Validación de Consistencia

Para cada recurso huérfano:
```
[ ] Verificar que SizeGiB > 0
[ ] Verificar que MonthlyCostUSD > 0
[ ] Verificar que PricingSku no está vacío
[ ] Verificar que PricingEffectiveDate es reciente (< 7 días)
[ ] Marcar casos especiales:
    - Encrypted=false → Flag "Unencrypted"
    - Public=true → Flag "Public"
    - SharedWithAccounts.length > 0 → Flag "Shared"
    - StorageTier="Archive" → Flag "Archive"
    - Tags vacío → Flag "NoTags"
```

---

## Salidas

### 1. CSV: `ebs-orphans-us-east-1.csv`

**Formato**: UTF-8, delimitado por comas, con escaping de comillas

**Columnas**:
```
ResourceKind,Id,ParentId,SizeGiB,TypeOrTier,Encrypted,KmsKeyId,StateOrTime,
Tags,MonthlyCostUSD,PricingSku,PricingEffectiveDate,Notes
```

**Definición de Columnas**:
```
ResourceKind: "EBS_VOLUME" | "SNAPSHOT"
Id: volumeId (vol-xxxxx) o snapshotId (snap-xxxxx)
ParentId: "" para volúmenes; volumeId para snapshots (o "N/A" si no existe)
SizeGiB: Tamaño en GiB (número)
TypeOrTier: volumeType (gp2, gp3, io1, io2, st1, sc1) o storageTier (Standard, Archive)
Encrypted: true | false
KmsKeyId: ARN de KMS key o "" si no cifrado
StateOrTime: createTime para volúmenes; startTime para snapshots (ISO8601 UTC)
Tags: key=value;key2=value2 o "" si no hay
MonthlyCostUSD: Costo mensual estimado (número con 2 decimales)
PricingSku: SKU de AWS Pricing
PricingEffectiveDate: Fecha de vigencia del precio (YYYY-MM-DD)
Notes: Descripción de por qué es huérfano y flags especiales
```

**Ejemplo - Volumen EBS Huérfano**:
```
EBS_VOLUME,vol-0123456789abcdef0,,"100","gp2","false","","2025-12-15T10:30:00Z",
"Name=OldBackup;Env=Dev","10.00","ABCD1234EFGH5678","2026-01-29",
"Detached; available; Unencrypted"
```

**Ejemplo - Snapshot Huérfano**:
```
SNAPSHOT,snap-0987654321fedcba0,"N/A","500","Standard","true",
"arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012",
"2025-11-01T14:22:00Z","Env=Prod;Retention=","25.00","IJKL9012MNOP3456","2026-01-29",
"Not referenced by AMI; >30d old; Shared with 2 accounts"
```

**Reglas CSV**:
- Tags en formato `key=value;key2=value2` (escapar `;` si está en valor)
- Tiempos en ISO8601 UTC
- Números con máximo 2 decimales para costos
- Si no hay huérfanos, generar archivo con headers y 0 filas

### 2. Markdown: `ebs-orphans-report-us-east-1.md`

**Estructura**:

## AWS EBS & Snapshots Huérfanos Report
### us-east-1 | Generated: 2026-01-29 14:30 UTC

---

## Resumen Ejecutivo

| Métrica | Valor |
|---------|-------|
| **Volúmenes EBS Huérfanos** | 12 |
| **Total Volúmenes (GiB)** | 1,250 |
| **Costo Volúmenes/Mes** | $125.00 |
| **Snapshots Huérfanos** | 45 |
| **Total Snapshots (GiB)** | 5,800 |
| **Costo Snapshots/Mes** | $290.00 |
| **Costo Mensual Total** | $415.00 |
| **Costo Anual Total** | $4,980.00 |
| **Recursos sin Cifrado** | 8 |

---

## Criterios de Análisis

- **Región**: us-east-1
- **Volumen Huérfano**: State=available, Attachments=0
- **Snapshot Huérfano**: VolumeId inexistente OR (No referenciado por AMI AND >30 días)
- **Exclusiones**: Snapshots con tag "Retention=Keep"
- **Fuente de Precios**: AWS Pricing API via MCP (effective_date=2026-01-29)

---

## ⚠️ Advertencias

- Validar antes de eliminar: algunos snapshots pueden ser necesarios para auditoría o compliance
- Revisar snapshots públicos/compartidos: pueden estar en uso por otras cuentas
- Snapshots en Archive: tiempos de restore pueden ser lentos (hasta 24h)
- Cifrado: volúmenes sin KMS están expuestos a riesgos de seguridad

---

## Top 10 Recursos por Costo Mensual

| Tipo | ID | Tamaño (GiB) | Costo/Mes (USD) | Razón | Flags |
|------|----|----|----|----|-----|
| SNAPSHOT | snap-0987654321fedcba0 | 1,200 | $60.00 | Not referenced by AMI; >30d | Shared |
| EBS_VOLUME | vol-0123456789abcdef0 | 500 | $50.00 | Detached; available | Unencrypted |
| SNAPSHOT | snap-1111111111111111 | 800 | $40.00 | Not referenced by AMI; >30d | Archive |
| EBS_VOLUME | vol-2222222222222222 | 300 | $30.00 | Detached; available | - |
| SNAPSHOT | snap-3333333333333333 | 600 | $30.00 | Volume not found | Public |
| EBS_VOLUME | vol-4444444444444444 | 250 | $25.00 | Detached; available | Unencrypted |
| SNAPSHOT | snap-5555555555555555 | 500 | $25.00 | Not referenced by AMI; >30d | - |
| EBS_VOLUME | vol-6666666666666666 | 200 | $20.00 | Detached; available | - |
| SNAPSHOT | snap-7777777777777777 | 400 | $20.00 | Not referenced by AMI; >30d | Shared |
| SNAPSHOT | snap-8888888888888888 | 350 | $17.50 | Not referenced by AMI; >30d | - |

---

## Volúmenes EBS Huérfanos

| Volume ID | Tamaño (GiB) | Tipo | Cifrado | Creado | Costo/Mes | Tags | Notas |
|-----------|----|----|----|----|----|----|-----|
| vol-0123456789abcdef0 | 100 | gp2 | ❌ No | 2025-12-15 | $10.00 | Name=OldBackup;Env=Dev | Detached; available |
| vol-2222222222222222 | 300 | gp3 | ✅ Sí | 2025-11-20 | $30.00 | Env=Staging | Detached; available |
| vol-4444444444444444 | 250 | io1 | ❌ No | 2025-10-05 | $25.00 | - | Detached; available; 1000 IOPS |
| vol-6666666666666666 | 200 | st1 | ✅ Sí | 2025-09-10 | $20.00 | Name=Archive;Owner=TeamA | Detached; available |
| vol-9999999999999999 | 400 | gp2 | ✅ Sí | 2025-08-01 | $40.00 | Env=Dev;Project=X | Detached; available |

---

## Snapshots Huérfanos

| Snapshot ID | Volumen Origen | Tamaño (GiB) | Tier | Cifrado | Creado | Antigüedad (días) | Costo/Mes | Razón | Flags |
|-----------|----|----|----|----|----|----|----|----|-----|
| snap-0987654321fedcba0 | N/A | 1,200 | Standard | ✅ Sí | 2025-11-01 | 90 | $60.00 | Not referenced by AMI; >30d | Shared (2 cuentas) |
| snap-1111111111111111 | vol-deleted | 800 | Archive | ✅ Sí | 2025-10-15 | 106 | $8.00 | Volume not found; >30d | - |
| snap-3333333333333333 | vol-deleted | 600 | Standard | ❌ No | 2025-09-20 | 132 | $30.00 | Volume not found; >30d | Public |
| snap-5555555555555555 | vol-deleted | 500 | Standard | ✅ Sí | 2025-08-10 | 172 | $25.00 | Not referenced by AMI; >30d | - |
| snap-7777777777777777 | vol-deleted | 400 | Standard | ✅ Sí | 2025-07-25 | 188 | $20.00 | Not referenced by AMI; >30d | Shared (1 cuenta) |

---

## Recomendaciones de Optimización

### 🗑️ Quick Win: Eliminar Snapshots Antiguos

**Impacto**: $180/mes ($2,160/año)  
**Acción**: Eliminar 28 snapshots con >30 días sin referencias  
**Riesgo**: Bajo (validar que no sean necesarios para auditoría)

**Snapshots a eliminar**:
- snap-0987654321fedcba0 (1,200 GiB, $60/mes)
- snap-1111111111111111 (800 GiB, $8/mes)
- snap-3333333333333333 (600 GiB, $30/mes)
- snap-5555555555555555 (500 GiB, $25/mes)
- snap-7777777777777777 (400 GiB, $20/mes)

---

### 💾 Convertir gp2 → gp3

**Impacto**: $0/mes (mismo precio, mejor performance)  
**Acción**: Migrar 5 volúmenes gp2 a gp3  
**Riesgo**: Bajo (sin costo, mejor performance)

**Volúmenes a migrar**:
- vol-0123456789abcdef0 (100 GiB)
- vol-9999999999999999 (400 GiB)

---

### 🔐 Cifrar Volúmenes/Snapshots

**Impacto**: +$0/mes (cifrado no tiene costo adicional)  
**Acción**: Habilitar cifrado KMS en 8 recursos  
**Riesgo**: Bajo (sin costo, mejora seguridad)

**Recursos sin cifrar**:
- vol-0123456789abcdef0 (100 GiB)
- vol-4444444444444444 (250 GiB)
- snap-3333333333333333 (600 GiB)

---

### 👁️ Revisar Snapshots Públicos/Compartidos

**Impacto**: Riesgo de seguridad  
**Acción**: Auditar 3 snapshots públicos/compartidos  
**Riesgo**: Medio (validar intención de compartir)

**Snapshots públicos/compartidos**:
- snap-0987654321fedcba0 (Compartido con 2 cuentas)
- snap-3333333333333333 (Público)
- snap-7777777777777777 (Compartido con 1 cuenta)

---

### 📋 Implementar Política de Tags

**Impacto**: Mejor gobierno de datos  
**Acción**: Agregar tags a 15 recursos sin etiquetas  
**Riesgo**: Bajo (solo metadatos)

**Tags recomendados**:
- `Environment`: prod/staging/dev
- `Owner`: team/person
- `CostCenter`: código de centro de costos
- `Retention`: Keep/Delete (para snapshots)

---

## Fuente de Datos

- **Fuente**: AWS EC2 API + AWS Pricing API via MCP
- **Precios Vigentes**: effective_date=2026-01-29
- **Región**: us-east-1
- **Perfil AWS**: chapter

### SKUs Utilizados

| Tipo | SKU |
|------|-----|
| gp2 | ABCD1234EFGH5678 |
| gp3 | EFGH5678IJKL9012 |
| io1 | IJKL9012MNOP3456 |
| io2 | MNOP3456PQRS7890 |
| st1 | PQRS7890TUVW1234 |
| sc1 | TUVW1234XYZA5678 |
| Snapshot Standard | XYZA5678BCDE9012 |
| Snapshot Archive | BCDE9012EFGH3456 |

---

**Generado**: 2026-01-29 14:30 UTC

---

## Reglas de Implementación

### Consultas MCP
- Todas las consultas deben usar MCP (EC2 + Pricing)
- Incluir `PricingSku` y `PricingEffectiveDate` en todas las salidas
- Validar que precios sean recientes (< 7 días)

### Formato de Datos
- Tiempos: ISO8601 UTC (ej: 2026-01-29T14:30:00Z)
- Tags: `key=value;key2=value2` (vacío si no hay)
- Números: máximo 2 decimales para costos
- CSV: UTF-8, delimitado por comas, con escaping de comillas

### Validaciones
- Verificar que SizeGiB > 0
- Verificar que MonthlyCostUSD > 0
- Marcar casos especiales (Unencrypted, Public, Shared, Archive, NoTags)
- Si no hay huérfanos, generar archivos con headers y 0 filas

### Exclusiones
- Snapshots con tag "Retention=Keep"
- Snapshots referenciados por AMIs activos
- Volúmenes en estado "in-use"

---

## Próximos Pasos

1. **Revisar Reporte**: Compartir con equipo de infraestructura correspondiente
2. **Validar Snapshots**: Confirmar que no son necesarios para auditoría/compliance
3. **Eliminar Huérfanos**: Ejecutar eliminación en fases (dev → staging → prod)
4. **Implementar Política**: Agregar tags y políticas de retención
5. **Monitorear**: Ejecutar análisis mensualmente

---
5. **Monitorear**: Ejecutar análisis mensualmente
