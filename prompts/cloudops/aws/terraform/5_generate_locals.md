# Prompt: Generar locals.tf

Eres un experto en Terraform que genera archivos `locals.tf` con variables locales calculadas y transformaciones de datos.

## OBJETIVO

Generar el archivo `locals.tf` que define:
1. Common tags (obligatorio)
2. Nombres dinámicos calculados
3. Transformaciones de datos
4. Valores reutilizables

## ESTRUCTURA DE locals.tf
```hcl
# ============================================================================
# LOCALS: [NOMBRE_DOMINIO]
# ============================================================================

locals {
  # --------------------------------------------------------------------------
  # Common Tags (Obligatorio)
  # --------------------------------------------------------------------------
  
  common_tags = {
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "Terraform"
    Domain      = "networking"  # networking, security, workload, etc.
    CreatedAt   = timestamp()
  }
  
  # --------------------------------------------------------------------------
  # Naming Convention
  # --------------------------------------------------------------------------
  
  # Prefijo estándar: {environment}-{project}
  name_prefix = "${var.environment}-${var.project_name}"
  
  # Nombres de recursos calculados
  vpc_name        = "${local.name_prefix}-vpc"
  public_subnet   = "${local.name_prefix}-public"
  private_subnet  = "${local.name_prefix}-private"
  nat_gateway     = "${local.name_prefix}-nat"
  
  # --------------------------------------------------------------------------
  # Data Transformations
  # --------------------------------------------------------------------------
  
  # Calcular CIDRs de subnets automáticamente
  public_subnet_cidrs = [
    for idx in range(length(var.availability_zones)) :
    cidrsubnet(var.vpc_cidr, 8, idx)
  ]
  
  private_subnet_cidrs = [
    for idx in range(length(var.availability_zones)) :
    cidrsubnet(var.vpc_cidr, 8, idx + 10)
  ]
  
  # --------------------------------------------------------------------------
  # Feature Flags
  # --------------------------------------------------------------------------
  
  # Habilitar NAT Gateway solo en prod/qa
  enable_nat = contains(["prod", "qa"], var.environment)
  
  # Multi-AZ solo en prod
  multi_az = var.environment == "prod"
}
```

## COMMON TAGS (Obligatorio)

**SIEMPRE incluir estos tags:**
```hcl
locals {
  common_tags = {
    Environment = var.environment        # dev, qa, prod
    Project     = var.project_name       # Nombre del proyecto
    ManagedBy   = "Terraform"            # Identificar recursos IaC
    Domain      = "networking"           # Dominio actual
    
    # Opcionales pero recomendados:
    Team        = var.team_name          # Si aplica
    CostCenter  = var.cost_center        # Si aplica
    CreatedAt   = timestamp()            # Fecha de creación
  }
}
```

## NAMING CONVENTION

**Formato estándar:** `{environment}-{project}-{resource}`
```hcl
locals {
  name_prefix = "${var.environment}-${var.project_name}"
  
  # Ejemplos:
  vpc_name            = "${local.name_prefix}-vpc"
  alb_name            = "${local.name_prefix}-alb"
  ecs_cluster_name    = "${local.name_prefix}-ecs-cluster"
  rds_identifier      = "${local.name_prefix}-db"
}
```

## DATA TRANSFORMATIONS

### Cálculo de CIDRs
```hcl
locals {
  # Dividir VPC en subnets públicas/privadas
  public_subnet_cidrs = [
    for idx in range(length(var.availability_zones)) :
    cidrsubnet(var.vpc_cidr, 8, idx)
  ]
  
  private_subnet_cidrs = [
    for idx in range(length(var.availability_zones)) :
    cidrsubnet(var.vpc_cidr, 8, idx + 100)
  ]
}
```

### Mapeo de Valores
```hcl
locals {
  # Mapeo de ambientes a tamaños de instancia
  instance_type_map = {
    dev  = "t3.small"
    qa   = "t3.medium"
    prod = "m5.large"
  }
  
  instance_type = local.instance_type_map[var.environment]
}
```

### Listas Filtradas
```hcl
locals {
  # Filtrar subnets privadas de remote state
  private_subnets = [
    for subnet in data.terraform_remote_state.networking.outputs.subnet_ids :
    subnet if subnet.type == "private"
  ]
}
```

## FEATURE FLAGS
```hcl
locals {
  # Habilitar características por ambiente
  enable_nat_gateway       = contains(["qa", "prod"], var.environment)
  enable_vpn_gateway       = var.environment == "prod"
  enable_multi_az          = var.environment == "prod"
  enable_deletion_protection = var.environment == "prod"
  
  # Configuraciones por ambiente
  backup_retention = var.environment == "prod" ? 30 : 7
  log_retention    = var.environment == "prod" ? 90 : 7
}
```

## LOCALS POR DOMINIO

### NETWORKING
```hcl
locals {
  common_tags         = { ... }
  name_prefix         = "${var.environment}-${var.project_name}"
  vpc_name            = "${local.name_prefix}-vpc"
  public_subnet_cidrs = [ ... ]
  private_subnet_cidrs = [ ... ]
  enable_nat          = var.environment != "dev"
}
```

### SECURITY
```hcl
locals {
  common_tags    = { ... }
  name_prefix    = "${var.environment}-${var.project_name}"
  sg_name        = "${local.name_prefix}-web-sg"
  iam_role_name  = "${local.name_prefix}-ecs-role"
  kms_key_alias  = "alias/${local.name_prefix}-key"
}
```

### WORKLOAD
```hcl
locals {
  common_tags        = { ... }
  name_prefix        = "${var.environment}-${var.project_name}"
  alb_name           = "${local.name_prefix}-alb"
  ecs_cluster_name   = "${local.name_prefix}-cluster"
  rds_identifier     = "${local.name_prefix}-db"
  
  # Configuraciones dinámicas
  min_capacity = var.environment == "prod" ? 2 : 1
  max_capacity = var.environment == "prod" ? 10 : 2
}
```

## MEJORES PRÁCTICAS

- ✅ Usar locals para valores calculados o transformados
- ✅ Centralizar naming convention
- ✅ Documentar transformaciones complejas
- ✅ Agrupar locals por propósito
- ✅ Usar feature flags para diferencias por ambiente
- ❌ NO usar locals para valores simples que ya son variables
- ❌ NO hacer transformaciones excesivamente complejas

## FORMATO DE SALIDA

Genera SOLO código Terraform válido. NO uses markdown fences.

Empieza directamente con:
```
# ============================================================================
# LOCALS: NETWORKING
# ============================================================================
```

## VALIDACIONES

- [ ] common_tags está incluido
- [ ] name_prefix sigue formato {environment}-{project}
- [ ] Transformaciones de datos son correctas
- [ ] Feature flags son claros y documentados
- [ ] Sintaxis HCL válida