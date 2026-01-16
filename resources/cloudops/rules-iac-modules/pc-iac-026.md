# 📄 Regla de Patrón de Transformación en sample/ (Módulos de Referencia)

**ID:** PC-IAC-026  
**Tipo:** Flujo de Datos / Ejemplo de Uso  
**Pilares AWS Well-Architected:** Operational Excellence, Reliability  
**Versión:** 1.0  
**Fecha:** 11 de diciembre de 2025

---

## 1. Propósito y Alcance

Esta regla define el patrón obligatorio de separación de responsabilidades entre los archivos del directorio **`sample/`** dentro de los **Módulos de Referencia**. El directorio `sample/` actúa como un ejemplo de consumo del módulo y debe demostrar las mejores prácticas de uso.

**Objetivo:**
- Proporcionar un ejemplo funcional y completo de cómo consumir el módulo
- Mantener `sample/main.tf` limpio, enfocado únicamente en invocar el módulo padre
- Centralizar transformaciones de datos en `sample/locals.tf`
- Declarar configuraciones base sin IDs hardcodeados en `sample/terraform.tfvars`
- Demostrar el patrón de inyección dinámica de IDs mediante Data Sources

**Aplicable a:** Directorio `sample/` de **todos los módulos de referencia** (no aplica a dominios de proyectos).

**Nota Importante:** Esta regla es específica para la estructura de ejemplo (`sample/`) dentro de módulos de referencia. Los dominios de proyectos (Networking, Seguridad, Workload) siguen sus propias reglas de estructura definidas en otras PC-IAC.

---

## 2. Contexto: sample/ en Módulos de Referencia

### 2.1. Estructura del Módulo de Referencia

```
modulo-referencia-dynamodb/
├─ main.tf              # Implementación del módulo
├─ variables.tf         # Variables del módulo
├─ outputs.tf           # Outputs del módulo
├─ README.md            # Documentación del módulo
└─ sample/              # 👈 Directorio de ejemplo (esta regla aplica aquí)
   ├─ README.md         # Cómo ejecutar el ejemplo
   ├─ terraform.tfvars  # Configuración de ejemplo
   ├─ variables.tf      # Variables del ejemplo
   ├─ data.tf           # Data sources para el ejemplo
   ├─ locals.tf         # Transformaciones del ejemplo
   ├─ main.tf           # Invocación del módulo padre
   ├─ outputs.tf        # Outputs del ejemplo
   └─ providers.tf      # Configuración de provider
```

---

## 3. Flujo Obligatorio de Datos en sample/

### 3.1. Diagrama de Flujo

```
terraform.tfvars → variables.tf → data.tf → locals.tf → main.tf → ../
     (config)        (tipos)     (consulta)  (transform)  (invoca módulo padre)
```

### 3.2. Responsabilidades por Archivo en sample/

| Archivo | Responsabilidad | Contenido Permitido | Contenido Prohibido |
|---------|----------------|---------------------|---------------------|
| `terraform.tfvars` | Configuración declarativa de ejemplo | Variables con valores base, campos vacíos (`""`, `[]`) donde se necesiten IDs dinámicos | IDs hardcodeados de recursos (VPC, SG, Subnets, KMS Keys) |
| `variables.tf` | Definición de tipos para el ejemplo | Declaración de variables con `type`, `description`, `default` | Lógica o transformaciones |
| `data.tf` | Consulta de recursos existentes | Data sources para obtener IDs dinámicos (VPC, SG, Subnets, KMS, etc.) | Lógica o cálculos |
| `locals.tf` | Transformaciones del ejemplo | Construcción de nomenclatura, merge de configuraciones, inyección de IDs desde data sources | Declaración de recursos o invocación de módulos |
| `main.tf` | Invocación del módulo padre | Bloque `module` apuntando a `source = "../"` consumiendo valores de `local.*` | Bloques `locals {}`, lógica de transformación, resources |
| `providers.tf` | Configuración de provider | Declaración de provider AWS con región y alias | Backend (el estado es local para ejemplos) |

---

## 4. Patrón Obligatorio en sample/

### 4.1. terraform.tfvars (Configuración Declarativa de Ejemplo)

**Objetivo:** Declarar configuración base sin IDs de recursos hardcodeados.

**✅ CORRECTO:**
```hcl
# sample/terraform.tfvars
sg_config = {
  "nginx-service" = {
    description = "Security group for nginx ECS service"
    vpc_id      = ""  # ✅ Vacío - se llenará automáticamente desde data source
    service     = "ecs"
    application = "nginx"
    
    ingress = [
      {
        from_port       = 80
        to_port         = 80
        protocol        = "tcp"
        cidr_blocks     = []
        security_groups = []  # ✅ Vacío - se llenará con ID del SG del ALB
        description     = "Allow HTTP from ALB"
      }
    ]
    
    egress = [
      {
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
        description = "Allow all outbound traffic"
      }
    ]
  }
}
```

**❌ INCORRECTO:**
```hcl
# sample/terraform.tfvars
sg_config = {
  "nginx-service" = {
    vpc_id = "vpc-0a1b2c3d4e5f6g7h8"  # ❌ ID hardcodeado - no portátil
    ingress = [
      {
        security_groups = ["sg-0x1y2z3a4b5c6d7e8"]  # ❌ ID hardcodeado
      }
    ]
  }
}
```

### 4.2. locals.tf (Transformaciones y Enriquecimiento del Ejemplo)

**Objetivo:** Transformar configuración base agregando IDs dinámicos desde data sources.

**✅ CORRECTO:**
```hcl
# sample/locals.tf
locals {
  # Construir prefijo de gobernanza (PC-IAC-025)
  governance_prefix = "${var.client}-${var.project}-${var.environment}"
  
  # Transformar configuración agregando IDs dinámicos desde data sources
  sg_config_transformed = {
    for key, config in var.sg_config : key => merge(config, {
      # Inyectar VPC ID desde data source si está vacío (PC-IAC-009)
      vpc_id = length(config.vpc_id) > 0 ? config.vpc_id : data.aws_vpc.selected.id
      
      # Transformar reglas de ingress agregando SG del ALB automáticamente
      ingress = [
        for rule in config.ingress : merge(rule, {
          # Si security_groups está vacío y el puerto es 80, agregar SG del ALB
          security_groups = length(rule.security_groups) == 0 && rule.from_port == 80 
            ? [data.aws_security_group.alb_public.id] 
            : rule.security_groups
        })
      ]
    })
  }
}
```

**Patrón de Inyección Dinámica (PC-IAC-009):**
```hcl
# Detectar campos vacíos y llenarlos con data sources
campo = length(config.campo) > 0 ? config.campo : data.aws_resource.default.id
```

**❌ INCORRECTO:**
```hcl
# sample/locals.tf
locals {
  # ❌ Configuración hardcodeada en locals - debe venir de variables
  sg_config_transformed = {
    "nginx" = {
      vpc_id = data.aws_vpc.selected.id
      ingress = [...]
    }
  }
}
```

### 4.3. data.tf (Consulta de Recursos Externos para el Ejemplo)

**Objetivo:** Obtener IDs de recursos existentes para inyectar en locals.

**✅ CORRECTO:**
```hcl
# sample/data.tf

# Obtener VPC por tags de nomenclatura estándar
data "aws_vpc" "selected" {
  provider = aws.principal
  
  filter {
    name   = "tag:Name"
    values = ["${var.client}-${var.project}-${var.environment}-vpc"]
  }
}

# Obtener Security Group del ALB
data "aws_security_group" "alb_public" {
  provider = aws.principal
  
  filter {
    name   = "tag:Name"
    values = ["${var.client}-${var.project}-${var.environment}-sg-alb-public"]
  }
}

# Obtener Subnets privadas
data "aws_subnets" "private" {
  provider = aws.principal
  
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.selected.id]
  }
  
  filter {
    name   = "tag:Type"
    values = ["private"]
  }
}
```

### 4.4. main.tf (Invocación Limpia del Módulo Padre)

**Objetivo:** Solo invocar el módulo **padre** (ubicado en `../`) consumiendo valores transformados de `local.*`.

**✅ CORRECTO:**
```hcl
# sample/main.tf

############################################################################
# Invocación del Módulo Padre (DynamoDB)
############################################################################
module "dynamodb_tables" {
  source = "../"  # 👈 Apunta al directorio padre (el módulo de referencia)

  providers = {
    aws.project = aws.principal
  }

  # Variables obligatorias de gobernanza
  client      = var.client
  project     = var.project
  environment = var.environment

  # ✅ Configuración transformada desde locals (PC-IAC-026)
  tables_config = local.tables_config_transformed
}
```

**❌ INCORRECTO:**
```hcl
# sample/main.tf (INCORRECTO)

# ❌ PROHIBIDO: locals dentro de sample/main.tf
locals {
  tables_config_transformed = {
    for key, config in var.tables_config : key => merge(config, {
      kms_key_arn = data.aws_kms_key.dynamodb.arn
    })
  }
}

# ❌ El módulo consume un local definido en el mismo archivo
module "dynamodb_tables" {
  source = "../"
  tables_config = local.tables_config_transformed  # El local está en el lugar incorrecto
}
```

**Por qué es incorrecto:** Los bloques `locals` deben estar en `sample/locals.tf`, no en `sample/main.tf`.

---

## 5. Ejemplos Completos por Caso de Uso en sample/

### 5.1. Caso: Inyección de KMS Key ARN (Ejemplo DynamoDB)

**sample/terraform.tfvars:**
```hcl
# Configuración de ejemplo sin ARNs hardcodeados
tables_config = {
  "orders" = {
    hash_key       = "order_id"
    billing_mode   = "PAY_PER_REQUEST"
    kms_key_arn    = ""  # 👈 Se llenará automáticamente desde data source
    
    attributes = [
      { name = "order_id", type = "S" }
    ]
  }
  
  "products" = {
    hash_key       = "product_id"
    billing_mode   = "PAY_PER_REQUEST"
    kms_key_arn    = ""  # 👈 Se llenará automáticamente
    
    attributes = [
      { name = "product_id", type = "S" }
    ]
  }
}
```

**sample/data.tf:**
```hcl
# Consultar KMS key existente por alias
data "aws_kms_key" "dynamodb" {
  key_id = "alias/${var.client}-${var.project}-${var.environment}-kms-dynamodb"
}
```

**sample/locals.tf:**
```hcl
locals {
  # Prefijo de gobernanza para el ejemplo
  governance_prefix = "${var.client}-${var.project}-${var.environment}"
  
  # Transformar configuración inyectando KMS key ARN dinámico
  tables_config_transformed = {
    for key, config in var.tables_config : key => merge(config, {
      # Si kms_key_arn está vacío, inyectar desde data source
      kms_key_arn = length(config.kms_key_arn) > 0 ? config.kms_key_arn : data.aws_kms_key.dynamodb.arn
    })
  }
}
```

**sample/main.tf:**
```hcl
# Invocar el módulo padre
module "dynamodb_tables" {
  source = "../"  # 👈 Módulo padre
  
  providers = {
    aws.project = aws.principal
  }
  
  client      = var.client
  project     = var.project
  environment = var.environment
  
  # ✅ Usa configuración transformada desde locals
  tables_config = local.tables_config_transformed
}
```

### 5.2. Caso: Inyección de VPC ID y Subnets (Ejemplo ECS)

**sample/terraform.tfvars:**
```hcl
ecs_services = {
  "api" = {
    vpc_id     = ""   # Se llenará automáticamente
    subnet_ids = []   # Se llenarán automáticamente
    cpu        = 256
    memory     = 512
  }
}
```

**sample/data.tf:**
```hcl
# Consultar VPC por nomenclatura estándar
data "aws_vpc" "selected" {
  filter {
    name   = "tag:Name"
    values = ["${var.client}-${var.project}-${var.environment}-vpc"]
  }
}

# Consultar subnets privadas
data "aws_subnets" "private" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.selected.id]
  }
  
  filter {
    name   = "tag:Type"
    values = ["private"]
  }
}
```

**sample/locals.tf:**
```hcl
locals {
  # Transformar configuración inyectando IDs dinámicos
  ecs_services_transformed = {
    for key, config in var.ecs_services : key => merge(config, {
      vpc_id     = length(config.vpc_id) > 0 ? config.vpc_id : data.aws_vpc.selected.id
      subnet_ids = length(config.subnet_ids) > 0 ? config.subnet_ids : data.aws_subnets.private.ids
    })
  }
}
```

**sample/main.tf:**
```hcl
module "ecs_services" {
  source = "../"
  
  services = local.ecs_services_transformed  # ✅ Usa local transformado
}
```

---

## 6. Diferencia con Dominios de Proyectos

### 6.1. sample/ vs Dominios

| Aspecto | `sample/` (Módulos de Referencia) | Dominios (Networking, Seguridad, Workload) |
|---------|-----------------------------------|---------------------------------------------|
| **Propósito** | Ejemplo de uso del módulo | Infraestructura real del proyecto |
| **Source en main.tf** | `source = "../"` (módulo padre) | `source = "git::..."` (módulo remoto) |
| **Estado** | Local (no crítico) | Remoto S3 con cifrado |
| **Backend** | No configurado | Configurado en `versions.tf` |
| **Alcance** | Demostración de patrones | Implementación de producción |
| **Data Sources** | Obtienen recursos de ejemplo/dev | Obtienen recursos entre dominios (PC-IAC-017) |
| **Regla Aplicable** | **PC-IAC-026** (esta regla) | PC-IAC-021, PC-IAC-022, PC-IAC-024, PC-IAC-025 |

### 6.2. Ejemplo de Invocación

**En `sample/main.tf` (Módulos de Referencia):**
```hcl
module "dynamodb_tables" {
  source = "../"  # 👈 Consume el módulo padre localmente
  # ...
}
```

**En `workload/main.tf` (Dominios de Proyectos):**
```hcl
module "dynamodb_tables" {
  source = "git::https://github.com/org/dynamodb-module.git?ref=v1.0.0"  # 👈 Consume módulo remoto versionado
  # ...
}
```

---

## 7. Criterios de Cumplimiento

✅ El directorio `sample/` existe dentro del módulo de referencia.  
✅ `sample/terraform.tfvars` contiene configuración declarativa sin IDs hardcodeados.  
✅ `sample/data.tf` contiene data sources para obtener IDs dinámicos.  
✅ `sample/locals.tf` contiene **todas** las transformaciones e inyecciones dinámicas.  
✅ `sample/main.tf` **solo** contiene el bloque `module` con `source = "../"` (sin `locals {}`).  
✅ El módulo consume `local.*` desde `sample/locals.tf`.  
✅ `sample/README.md` documenta cómo ejecutar el ejemplo.

---

## 8. Relación con Pilares AWS Well-Architected

| Pilar | Cómo contribuye esta regla |
| :--- | :--- |
| **Operational Excellence** | El directorio `sample/` proporciona un ejemplo funcional que acelera la adopción del módulo y reduce errores de implementación. |
| **Reliability** | La inyección dinámica de IDs en el ejemplo demuestra el patrón correcto, evitando hardcodeo que causaría fallos en otros ambientes. |

---

## 9. Antipatrón Común: locals en sample/main.tf

### ❌ NUNCA hacer esto en sample/:

```hcl
# sample/main.tf (INCORRECTO)
locals {
  tables_config = { ... }  # ❌ Debe ir en sample/locals.tf
}

module "dynamodb_tables" {
  source = "../"
  tables_config = local.tables_config
}
```

### ✅ SIEMPRE hacer esto en sample/:

```hcl
# sample/locals.tf (CORRECTO)
locals {
  tables_config_transformed = { ... }
}

# sample/main.tf (CORRECTO)
module "dynamodb_tables" {
  source = "../"  # 👈 Invoca al módulo padre
  tables_config = local.tables_config_transformed
}
```

---

## 10. Resumen del Patrón en sample/

| Paso | Archivo en `sample/` | Acción |
|------|----------------------|--------|
| 1 | `terraform.tfvars` | Declarar configuración de ejemplo con campos vacíos (`""`, `[]`) |
| 2 | `variables.tf` | Definir tipos de las variables del ejemplo |
| 3 | `data.tf` | Consultar recursos existentes (VPC, SG, KMS) mediante data sources |
| 4 | `locals.tf` | Transformar configuración e inyectar IDs dinámicos desde data sources |
| 5 | `main.tf` | Invocar módulo padre (`source = "../"`) con `local.*` |

**El flujo es unidireccional y cada archivo en `sample/` tiene una responsabilidad única.**

---

## 11. Propósito del Directorio sample/

El directorio `sample/` sirve para:

1. **Documentación Viva:** Proporcionar un ejemplo ejecutable del módulo
2. **Testing Manual:** Permitir pruebas rápidas durante el desarrollo del módulo
3. **Onboarding:** Acelerar la curva de aprendizaje de nuevos usuarios del módulo
4. **Demostración de Patrones:** Mostrar las mejores prácticas de inyección dinámica
5. **Validación:** Verificar que el módulo funciona correctamente antes de publicar

**Importante:** El código en `sample/` es un **ejemplo**, no código de producción. Los dominios de proyectos reales deben seguir sus propias reglas de estructura.
