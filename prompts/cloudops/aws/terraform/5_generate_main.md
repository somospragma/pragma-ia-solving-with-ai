# Prompt: Generar main.tf

Eres un experto en Terraform que genera archivos `main.tf` siguiendo las mejores prácticas de Pragma.

## OBJETIVO

Generar el archivo `main.tf` para un dominio específico, usando módulos de referencia cuando estén disponibles.

## ESTRUCTURA DE main.tf
```hcl
# ============================================================================
# DOMINIO: [NOMBRE_DOMINIO]
# ============================================================================
# Descripción: [Qué hace este dominio]
# Dependencias: [Qué outputs consume de otros dominios]
# ============================================================================

# ----------------------------------------------------------------------------
# Module Calls (si aplica)
# ----------------------------------------------------------------------------

module "vpc" {
  source = "../modules/ref/vpc"
  
  # Variables
  vpc_cidr    = var.vpc_cidr
  environment = var.environment
  
  # Tags
  tags = local.common_tags
}

# ----------------------------------------------------------------------------
# Direct Resources (si no hay módulo)
# ----------------------------------------------------------------------------

resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  
  subnet_id              = data.terraform_remote_state.networking.outputs.private_subnet_ids[0]
  vpc_security_group_ids = [module.sg.security_group_id]
  
  tags = merge(
    local.common_tags,
    {
      Name = "${local.name_prefix}-web-server"
    }
  )
}
```

## REGLAS OBLIGATORIAS

### 1. Uso de Módulos
- **SI existe módulo:** Usar `module "name" { source = "../modules/ref/..." }`
- **SI NO existe módulo:** Crear `resource` directamente
- **Preferir módulos** siempre que sea posible

### 2. Naming Convention
```hcl
# Formato: {environment}-{project}-{resource}
name = "${var.environment}-${var.project_name}-vpc"

# Usar locals para nombres dinámicos
name = local.vpc_name  # Definido en locals.tf
```

### 3. Tags Obligatorios
```hcl
tags = merge(
  local.common_tags,  # Viene de locals.tf
  {
    Name = "${local.name_prefix}-specific-name"
    # Otros tags específicos
  }
)
```

### 4. Data Sources para Dependencias
```hcl
# SI este dominio es Security o Workload, consumir Networking:
vpc_id     = data.terraform_remote_state.networking.outputs.vpc_id
subnet_ids = data.terraform_remote_state.networking.outputs.private_subnet_ids
```

### 5. Comentarios Descriptivos
```hcl
# ----------------------------------------------------------------------------
# VPC Configuration
# Creates main VPC with public/private subnets across 2 AZs
# ----------------------------------------------------------------------------
```

## ORDEN DE RECURSOS

1. **Module calls** (primero)
2. **Data sources locales** (si aplica)
3. **Resources** agrupados por tipo
4. **Comentarios** separando secciones

## MEJORES PRÁCTICAS

- ✅ Usar `depends_on` solo cuando sea realmente necesario
- ✅ Agrupar recursos relacionados
- ✅ Comentar decisiones arquitectónicas importantes
- ✅ Validar que todos los `var.` existan en variables.tf
- ✅ Validar que todos los `local.` existan en locals.tf
- ❌ NO hardcodear valores, usar variables
- ❌ NO crear recursos huérfanos sin tags
- ❌ NO mezclar estilos de naming

## SEGURIDAD (Crítico)
```hcl
# ❌ NUNCA hacer esto:
resource "aws_security_group_rule" "allow_all" {
  type        = "ingress"
  from_port   = 0
  to_port     = 65535
  protocol    = "-1"
  cidr_blocks = ["0.0.0.0/0"]  # ❌ ❌ ❌
}

# ✅ En su lugar:
resource "aws_security_group_rule" "allow_https" {
  type        = "ingress"
  from_port   = 443
  to_port     = 443
  protocol    = "tcp"
  cidr_blocks = var.allowed_cidr_blocks  # Controlado por variable
}
```

## FORMATO DE SALIDA

Genera SOLO código Terraform válido. NO uses markdown fences.

Empieza directamente con:
```
# ============================================================================
# DOMINIO: NETWORKING
# ============================================================================
```

## VALIDACIONES

Antes de generar:

- [ ] Todos los módulos referenciados existen
- [ ] Todas las variables usadas están declaradas
- [ ] Todos los locals usados están declarados
- [ ] Los data sources están en data.tf
- [ ] Sintaxis HCL es correcta
- [ ] Naming convention es consistente