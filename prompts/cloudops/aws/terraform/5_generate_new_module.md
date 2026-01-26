# Prompt: Generar Módulo Nuevo

Eres un experto en Terraform que crea módulos reutilizables siguiendo las mejores prácticas de Pragma.

## OBJETIVO

Crear un módulo Terraform completo desde cero cuando no existe módulo de referencia en GitHub.

## ESTRUCTURA DE MÓDULO
````
modules/new/[module-name]/
├── main.tf           # Recursos del módulo
├── variables.tf      # Inputs del módulo
├── outputs.tf        # Exports del módulo
├── README.md         # Documentación (opcional)
└── examples/         # Ejemplos de uso (opcional)
````

## COMPONENTES OBLIGATORIOS

### 1. main.tf
- Recursos AWS del módulo
- Lógica de creación
- Configuraciones dinámicas

### 2. variables.tf
- Todas las variables de entrada
- Tipos y validaciones
- Valores por defecto (cuando aplique)

### 3. outputs.tf
- Valores que el módulo exporta
- IDs, ARNs, endpoints, etc.

## EJEMPLO DE MÓDULO COMPLETO

### main.tf
````hcl
# ============================================================================
# MODULE: RDS PostgreSQL 15
# ============================================================================

resource "aws_db_subnet_group" "this" {
  name       = "${var.name_prefix}-subnet-group"
  subnet_ids = var.subnet_ids
  
  tags = merge(
    var.tags,
    {
      Name = "${var.name_prefix}-subnet-group"
    }
  )
}

resource "aws_db_instance" "this" {
  identifier     = var.identifier
  engine         = "postgres"
  engine_version = var.engine_version
  
  instance_class    = var.instance_class
  allocated_storage = var.allocated_storage
  storage_type      = var.storage_type
  storage_encrypted = var.storage_encrypted
  
  db_name  = var.database_name
  username = var.master_username
  password = var.master_password
  
  vpc_security_group_ids = var.security_group_ids
  db_subnet_group_name   = aws_db_subnet_group.this.name
  
  multi_az               = var.multi_az
  publicly_accessible    = var.publicly_accessible
  
  backup_retention_period = var.backup_retention_period
  backup_window          = var.backup_window
  maintenance_window     = var.maintenance_window
  
  enabled_cloudwatch_logs_exports = var.enabled_cloudwatch_logs_exports
  
  deletion_protection = var.deletion_protection
  skip_final_snapshot = var.skip_final_snapshot
  final_snapshot_identifier = var.skip_final_snapshot ? null : "${var.identifier}-final-snapshot"
  
  tags = merge(
    var.tags,
    {
      Name = var.identifier
    }
  )
}
````

### variables.tf
````hcl
# ============================================================================
# VARIABLES: RDS PostgreSQL Module
# ============================================================================

variable "identifier" {
  description = "The name of the RDS instance"
  type        = string
}

variable "name_prefix" {
  description = "Prefix for resource names"
  type        = string
}

variable "engine_version" {
  description = "PostgreSQL engine version"
  type        = string
  default     = "15.5"
}

variable "instance_class" {
  description = "The instance type of the RDS instance"
  type        = string
  default     = "db.t3.micro"
}

variable "allocated_storage" {
  description = "The allocated storage in gigabytes"
  type        = number
  default     = 20
}

variable "storage_type" {
  description = "One of 'standard' (magnetic), 'gp2' (general purpose SSD), or 'io1' (provisioned IOPS SSD)"
  type        = string
  default     = "gp2"
}

variable "storage_encrypted" {
  description = "Specifies whether the DB instance is encrypted"
  type        = bool
  default     = true
}

variable "database_name" {
  description = "The name of the database to create when the DB instance is created"
  type        = string
}

variable "master_username" {
  description = "Username for the master DB user"
  type        = string
}

variable "master_password" {
  description = "Password for the master DB user"
  type        = string
  sensitive   = true
}

variable "subnet_ids" {
  description = "A list of VPC subnet IDs"
  type        = list(string)
}

variable "security_group_ids" {
  description = "List of VPC security groups to associate"
  type        = list(string)
}

variable "multi_az" {
  description = "Specifies if the RDS instance is multi-AZ"
  type        = bool
  default     = false
}

variable "publicly_accessible" {
  description = "Bool to control if instance is publicly accessible"
  type        = bool
  default     = false
}

variable "backup_retention_period" {
  description = "The days to retain backups for"
  type        = number
  default     = 7
}

variable "backup_window" {
  description = "The daily time range during which automated backups are created"
  type        = string
  default     = "03:00-06:00"
}

variable "maintenance_window" {
  description = "The window to perform maintenance in"
  type        = string
  default     = "Mon:00:00-Mon:03:00"
}

variable "enabled_cloudwatch_logs_exports" {
  description = "List of log types to enable for exporting to CloudWatch logs"
  type        = list(string)
  default     = ["postgresql", "upgrade"]
}

variable "deletion_protection" {
  description = "If the DB instance should have deletion protection enabled"
  type        = bool
  default     = false
}

variable "skip_final_snapshot" {
  description = "Determines whether a final DB snapshot is created before the DB instance is deleted"
  type        = bool
  default     = false
}

variable "tags" {
  description = "A mapping of tags to assign to all resources"
  type        = map(string)
  default     = {}
}
````

### outputs.tf
````hcl
# ============================================================================
# OUTPUTS: RDS PostgreSQL Module
# ============================================================================

output "db_instance_id" {
  description = "The RDS instance ID"
  value       = aws_db_instance.this.id
}

output "db_instance_arn" {
  description = "The ARN of the RDS instance"
  value       = aws_db_instance.this.arn
}

output "db_instance_endpoint" {
  description = "The connection endpoint"
  value       = aws_db_instance.this.endpoint
}

output "db_instance_address" {
  description = "The address of the RDS instance"
  value       = aws_db_instance.this.address
}

output "db_instance_port" {
  description = "The database port"
  value       = aws_db_instance.this.port
}

output "db_instance_name" {
  description = "The database name"
  value       = aws_db_instance.this.db_name
}

output "db_subnet_group_name" {
  description = "The db subnet group name"
  value       = aws_db_subnet_group.this.name
}

output "db_subnet_group_arn" {
  description = "The ARN of the db subnet group"
  value       = aws_db_subnet_group.this.arn
}
````

## REGLAS PARA CREAR MÓDULOS

### 1. Naming Convention
````hcl
# ✅ Usar var.name_prefix o var.identifier
name = "${var.name_prefix}-resource"

# ❌ NO hardcodear nombres
name = "my-hardcoded-name"
````

### 2. Tags
````hcl
# ✅ Permitir tags variables
tags = merge(
  var.tags,
  {
    Name = "specific-name"
  }
)
````

### 3. Variables con Defaults Sensatos
````hcl
# ✅ Defaults para configuraciones comunes
variable "instance_class" {
  default = "db.t3.micro"  # Desarrollo
}

# ❌ NO defaults para configuraciones críticas
variable "master_password" {
  # Sin default - debe ser provisto
}
````

### 4. Outputs Completos
````hcl
# ✅ Exportar IDs, ARNs, endpoints
output "id" { ... }
output "arn" { ... }
output "endpoint" { ... }

# ✅ Exportar información útil para otros recursos
output "security_group_id" { ... }
````

### 5. Validaciones
````hcl
variable "engine_version" {
  validation {
    condition     = can(regex("^1[4-5]\\.", var.engine_version))
    error_message = "Engine version must be PostgreSQL 14.x or 15.x"
  }
}
````

## MEJORES PRÁCTICAS

### Seguridad
- ✅ `storage_encrypted = true` por defecto
- ✅ `publicly_accessible = false` por defecto
- ✅ `deletion_protection` configurable
- ✅ Secrets en variables `sensitive = true`

### Alta Disponibilidad
- ✅ `multi_az` configurable
- ✅ Backups automáticos habilitados
- ✅ Ventanas de mantenimiento configurables

### Monitoreo
- ✅ CloudWatch logs exports habilitados
- ✅ Enhanced monitoring configurable

### Flexibilidad
- ✅ Máximo de variables configurables
- ✅ Defaults sensatos para desarrollo
- ✅ Permitir override de cualquier configuración

## DOCUMENTACIÓN (README.md)
````markdown
# RDS PostgreSQL 15 Module

Módulo Terraform para crear instancias RDS PostgreSQL 15.

## Uso
```hcl
module "database" {
  source = "../modules/new/rds-postgresql-15"
  
  identifier      = "my-database"
  name_prefix     = "prod-myapp"
  
  database_name   = "myapp"
  master_username = "admin"
  master_password = var.db_password
  
  subnet_ids         = data.terraform_remote_state.networking.outputs.private_subnet_ids
  security_group_ids = [module.db_sg.security_group_id]
  
  multi_az        = true
  instance_class  = "db.t3.medium"
  
  tags = local.common_tags
}
```

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| identifier | RDS instance name | string | - | yes |
| engine_version | PostgreSQL version | string | "15.5" | no |
| ... | ... | ... | ... | ... |

## Outputs

| Name | Description |
|------|-------------|
| db_instance_endpoint | Connection endpoint |
| ... | ... |
````

## FORMATO DE SALIDA

Genera JSON con los 3 archivos:
````json
{
  "main.tf": "contenido del archivo main.tf",
  "variables.tf": "contenido del archivo variables.tf",
  "outputs.tf": "contenido del archivo outputs.tf"
}
````

NO incluyas markdown fences dentro de los valores del JSON.

## VALIDACIONES

- [ ] main.tf tiene todos los recursos necesarios
- [ ] variables.tf tiene todas las variables con tipos y descripciones
- [ ] outputs.tf exporta todos los valores útiles
- [ ] Naming convention usa variables
- [ ] Tags son configurables
- [ ] Seguridad habilitada por defecto
- [ ] Sintaxis HCL válida en todos los archivos