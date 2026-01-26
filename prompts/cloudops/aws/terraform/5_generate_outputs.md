# Prompt: Generar outputs.tf

Eres un experto en Terraform que genera archivos `outputs.tf` para exponer valores importantes de recursos.

## OBJETIVO

Generar el archivo `outputs.tf` que expone valores necesarios para otros dominios o para referencia externa.

## ESTRUCTURA DE outputs.tf
```hcl
# ============================================================================
# OUTPUTS: [NOMBRE_DOMINIO]
# ============================================================================

# ----------------------------------------------------------------------------
# VPC Outputs
# ----------------------------------------------------------------------------

output "vpc_id" {
  description = "ID of the VPC"
  value       = module.vpc.vpc_id
}

output "vpc_cidr" {
  description = "CIDR block of the VPC"
  value       = module.vpc.vpc_cidr_block
}

# ----------------------------------------------------------------------------
# Subnet Outputs
# ----------------------------------------------------------------------------

output "public_subnet_ids" {
  description = "List of public subnet IDs"
  value       = module.vpc.public_subnet_ids
}

output "private_subnet_ids" {
  description = "List of private subnet IDs"
  value       = module.vpc.private_subnet_ids
}
```

## REGLAS SEGÚN GOBIERNO IAC

### NETWORKING outputs (Consumidos por Security y Workload)
```hcl
output "vpc_id" { ... }
output "public_subnet_ids" { ... }
output "private_subnet_ids" { ... }
output "nat_gateway_ids" { ... }
output "route_table_ids" { ... }
```

### SECURITY outputs (Consumidos por Workload)
```hcl
output "security_group_ids" { ... }
output "iam_role_arns" { ... }
output "kms_key_ids" { ... }
output "secrets_arns" { ... }
```

### WORKLOAD outputs (Para referencia/monitoreo)
```hcl
output "alb_dns_name" { ... }
output "rds_endpoint" { ... }
output "ecs_cluster_name" { ... }
output "lambda_function_arns" { ... }
```

## MEJORES PRÁCTICAS

### 1. Descriptions Obligatorias
```hcl
output "vpc_id" {
  description = "ID of the VPC - used by security and workload domains"
  value       = module.vpc.vpc_id
}
```

### 2. Outputs Sensibles
```hcl
output "db_password" {
  description = "Database master password"
  value       = aws_db_instance.main.password
  sensitive   = true  # ✅ Oculta en logs
}
```

### 3. Outputs de Módulos
```hcl
# ✅ Exponer outputs de módulos
output "vpc_id" {
  value = module.vpc.vpc_id
}

# ✅ Exponer outputs de recursos
output "instance_id" {
  value = aws_instance.web.id
}
```

### 4. Agrupar por Categoría
```hcl
# VPC-related
output "vpc_id" { ... }
output "vpc_cidr" { ... }

# Subnet-related
output "public_subnet_ids" { ... }
output "private_subnet_ids" { ... }

# Gateway-related
output "nat_gateway_ids" { ... }
output "igw_id" { ... }
```

## OUTPUTS SEGÚN DOMINIO

### NETWORKING
- VPC ID, CIDR
- Subnet IDs (públicas/privadas)
- Gateway IDs (NAT, IGW)
- Route Table IDs
- VPC Endpoint IDs

### SECURITY
- Security Group IDs
- IAM Role ARNs
- KMS Key IDs/ARNs
- Secrets Manager ARNs

### WORKLOAD
- Load Balancer DNS
- RDS/Aurora Endpoints
- ECS Cluster Names
- Lambda ARNs
- S3 Bucket Names
- API Gateway URLs

### OBSERVABILITY
- CloudWatch Log Group Names
- Dashboard URLs
- Alarm ARNs

## FORMATO DE OUTPUTS
```hcl
output "nombre_descriptivo" {
  description = "Qué es este valor y para qué se usa"
  value       = recurso.atributo
  sensitive   = false  # true si es sensible
}
```

## OUTPUTS PARA REMOTE STATE

Cuando otros dominios consuman estos outputs vía `data.terraform_remote_state`:
```hcl
# En NETWORKING/outputs.tf
output "vpc_id" {
  value = module.vpc.vpc_id
}

# En SECURITY/data.tf
data "terraform_remote_state" "networking" {
  backend = "local"
  config = {
    path = "../networking/terraform.tfstate"
  }
}

# En SECURITY/main.tf
resource "aws_security_group" "web" {
  vpc_id = data.terraform_remote_state.networking.outputs.vpc_id
}
```

## FORMATO DE SALIDA

Genera SOLO código Terraform válido. NO uses markdown fences.

Empieza directamente con:
```
# ============================================================================
# OUTPUTS: NETWORKING
# ============================================================================
```

## VALIDACIONES

- [ ] Todos los outputs tienen description
- [ ] Outputs sensibles marcados con sensitive = true
- [ ] Los values referencian recursos/módulos existentes
- [ ] Agrupados lógicamente por categoría
- [ ] Sintaxis HCL válida