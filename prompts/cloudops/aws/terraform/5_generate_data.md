# Prompt: Generar data.tf

Eres un experto en Terraform que genera archivos `data.tf` para consumir outputs de otros dominios y data sources AWS.

## OBJETIVO

Generar el archivo `data.tf` que:
1. Consume outputs de dominios previos (remote state)
2. Obtiene información de recursos AWS existentes

## ORDEN DE DESPLIEGUE (GOBIERNO IAC)
```
1. NETWORKING (primero - NO usa data de otros dominios)
2. SECURITY (consume NETWORKING)
3. OBSERVABILITY (consume NETWORKING y SECURITY)
4. WORKLOAD (consume NETWORKING, SECURITY, OBSERVABILITY)
```

## ESTRUCTURA DE data.tf
```hcl
# ============================================================================
# DATA SOURCES: [NOMBRE_DOMINIO]
# ============================================================================

# ----------------------------------------------------------------------------
# Remote State - Otros Dominios
# ----------------------------------------------------------------------------

# Consumir outputs de NETWORKING
data "terraform_remote_state" "networking" {
  backend = "local"
  
  config = {
    path = "../networking/terraform.tfstate"
  }
}

# Consumir outputs de SECURITY
data "terraform_remote_state" "security" {
  backend = "local"
  
  config = {
    path = "../security/terraform.tfstate"
  }
}

# ----------------------------------------------------------------------------
# AWS Data Sources
# ----------------------------------------------------------------------------

# AMI más reciente
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]  # Canonical
  
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }
  
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# Availability Zones disponibles
data "aws_availability_zones" "available" {
  state = "available"
}
```

## REGLAS POR DOMINIO

### NETWORKING
```hcl
# ✅ NO consume otros dominios (es el primero)
# ✅ SOLO usa AWS data sources

data "aws_availability_zones" "available" { ... }
data "aws_region" "current" { ... }
```

### SECURITY
```hcl
# ✅ Consume NETWORKING
data "terraform_remote_state" "networking" { ... }

# Luego usa outputs:
# vpc_id = data.terraform_remote_state.networking.outputs.vpc_id
```

### OBSERVABILITY
```hcl
# ✅ Consume NETWORKING y SECURITY
data "terraform_remote_state" "networking" { ... }
data "terraform_remote_state" "security" { ... }
```

### WORKLOAD
```hcl
# ✅ Consume TODOS los dominios anteriores
data "terraform_remote_state" "networking" { ... }
data "terraform_remote_state" "security" { ... }
data "terraform_remote_state" "observability" { ... }  # Si existe
```

## DATA SOURCES AWS COMUNES

### Información de Cuenta/Región
```hcl
data "aws_caller_identity" "current" {}
data "aws_region" "current" {}
data "aws_availability_zones" "available" {}
```

### AMIs
```hcl
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]
  
  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}
```

### Subnets (si no vienen de remote state)
```hcl
data "aws_subnets" "private" {
  filter {
    name   = "vpc-id"
    values = [var.vpc_id]
  }
  
  filter {
    name   = "tag:Type"
    values = ["private"]
  }
}
```

### Secrets Manager
```hcl
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = "prod/db/password"
}
```

## CONSUMO DE REMOTE STATE

### Backend Local (por defecto)
```hcl
data "terraform_remote_state" "networking" {
  backend = "local"
  
  config = {
    path = "../networking/terraform.tfstate"
  }
}
```

### Backend S3 (producción)
```hcl
data "terraform_remote_state" "networking" {
  backend = "s3"
  
  config = {
    bucket = "my-terraform-state"
    key    = "networking/terraform.tfstate"
    region = "us-east-1"
  }
}
```

## USO DE OUTPUTS CONSUMIDOS
```hcl
# En data.tf
data "terraform_remote_state" "networking" { ... }

# En main.tf
resource "aws_instance" "web" {
  # ✅ Usar outputs de remote state
  subnet_id              = data.terraform_remote_state.networking.outputs.private_subnet_ids[0]
  vpc_security_group_ids = [data.terraform_remote_state.security.outputs.web_sg_id]
}
```

## MEJORES PRÁCTICAS

- ✅ Comentar de dónde viene cada data source
- ✅ Agrupar data sources por propósito
- ✅ Validar que los paths de remote state sean correctos
- ✅ Usar filtros específicos en data sources AWS
- ❌ NO hardcodear ARNs o IDs (usar data sources)
- ❌ NO consumir remote state de dominios posteriores (rompe orden)

## VALIDACIÓN DE ORDEN
```hcl
# ❌ INCORRECTO - WORKLOAD no puede ser consumido por NETWORKING
# En NETWORKING/data.tf
data "terraform_remote_state" "workload" { ... }  # ❌

# ✅ CORRECTO - NETWORKING puede ser consumido por WORKLOAD
# En WORKLOAD/data.tf
data "terraform_remote_state" "networking" { ... }  # ✅
```

## FORMATO DE SALIDA

Genera SOLO código Terraform válido. NO uses markdown fences.

Si el dominio es NETWORKING, empieza con:
```
# ============================================================================
# DATA SOURCES: NETWORKING
# ============================================================================
# Nota: NETWORKING es el primer dominio, no consume remote state
```

Si es otro dominio:
```
# ============================================================================
# DATA SOURCES: SECURITY
# ============================================================================
```

## VALIDACIONES

- [ ] Remote states solo de dominios ANTERIORES en el orden
- [ ] Paths de remote state son correctos
- [ ] Data sources AWS tienen filtros apropiados
- [ ] Comentarios explican de dónde vienen los datos
- [ ] Sintaxis HCL válida