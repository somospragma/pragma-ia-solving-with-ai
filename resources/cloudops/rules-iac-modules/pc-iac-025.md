# 📄 Regla de Procesamiento Obligatorio de Gobernanza en el Root

**ID:** PC-IAC-025  
**Tipo:** Flujo de Datos / Trazabilidad  
**Pilares AWS Well-Architected:** Operational Excellence  
**Versión:** 1.0  
**Fecha:** 11 de diciembre de 2025

---

## 1. Propósito y Alcance

Esta regla establece que el Módulo Raíz (IaC Root) es responsable de procesar, generar y asegurar la consistencia de las variables de Gobernanza (`client`, `project`, `environment`) al construir estructuras de datos complejas que consumen los módulos.

Evita que los módulos realicen transformaciones basadas exclusivamente en datos del Root, como la construcción de la Nomenclatura Estándar (PC-IAC-003).

**Aplicable a:** Bloques `module` en `main.tf` del Módulo Raíz (proyectos de dominio).

---

## 2. Flujo Obligatorio para Nomenclatura (Naming)

### 2.1. Nomenclatura Completa en el Root (Mandatorio)

Si un módulo requiere la Nomenclatura Estándar (PC-IAC-003), el Root debe inyectar el nombre final y completo dentro del payload de configuración, en lugar de pasar las partes (`client`, `project`, `environment`) para que el módulo las combine.

* **Regla:** El módulo de referencia solo debe consumir el nombre final del recurso (por ejemplo: `pragma-ecommerce-dev-dynamodb-orders`), y no construirlo internamente.

### 2.2. Uso Obligatorio de `locals.tf` del Root

La creación del payload de configuración que incluye la Nomenclatura Estándar debe ocurrir en `locals.tf` del Root (refuerza PC-IAC-021).

---

## 3. Ejemplo de Cumplimiento (Root)

### 3.1. Construcción en `locals.tf` del Root

```hcl
# locals.tf (del Root)
locals {
  # Prefijo de gobernanza
  governance_prefix = "${var.client}-${var.project}-${var.environment}"

  # PC-IAC-025: El Root construye la nomenclatura FINAL
  tables_config_final = {
    for key, config in var.tables : key => merge(config, {
      # Inyección del nombre FINAL en el payload
      name = "${local.governance_prefix}-dynamodb-${key}"
    })
  }
}
```

### 3.2. Invocación en `main.tf` del Root

```hcl
# main.tf (del Root)
module "dynamodb_tables" {
  source = "git::https://github.com/org/dynamodb-module.git?ref=v1.0.0"
  
  providers = {
    aws.project = aws.principal
  }
  
  # Variables de gobernanza se pasan para tagging y otros usos
  client      = var.client
  project     = var.project
  environment = var.environment
  
  # PC-IAC-025: Pasa el payload completo con el nombre ya construido
  tables = local.tables_config_final
}
```

---

## 4. Antipatrón: Construcción en el Módulo

### 4.1. Ejemplo INCORRECTO

❌ **NO HACER:**

**En el Módulo de Referencia:**
```hcl
# locals.tf (INCORRECTO - dentro del módulo)
locals {
  # ❌ El módulo construye la nomenclatura a partir de variables del Root
  table_names = {
    for key, config in var.tables_config :
    key => "${var.client}-${var.project}-${var.environment}-dynamodb-${key}"
  }
}
```

**Problemas:**
- El módulo depende de las variables de gobernanza para construir nombres
- No hay flexibilidad si el Root necesita una nomenclatura personalizada
- Viola el principio de que el Root es responsable de la gobernanza

### 4.2. Ejemplo CORRECTO

✅ **HACER:**

**En el Módulo de Referencia:**
```hcl
# variables.tf (módulo)
variable "tables_config" {
  description = "Map of table configurations with pre-constructed names"
  type = map(object({
    name = string  # ✅ El nombre viene ya construido desde el Root
    # ... otros atributos
  }))
}

# main.tf (módulo)
resource "aws_dynamodb_table" "this" {
  for_each = var.tables_config
  
  # ✅ Usa el nombre directamente, sin construirlo
  name = each.value.name
  # ...
}
```

---

## 5. Responsabilidades Claras

### 5.1. Responsabilidad del Root

El Módulo Raíz es responsable de:
- ✅ Construir el prefijo de gobernanza completo
- ✅ Inyectar la nomenclatura final en los payloads de configuración
- ✅ Validar la consistencia de las variables de gobernanza
- ✅ Aplicar reglas de negocio específicas del proyecto/ambiente

### 5.2. Responsabilidad del Módulo

El Módulo de Referencia es responsable de:
- ✅ Recibir configuración con nombres ya construidos
- ✅ Aplicar la lógica específica del recurso AWS
- ✅ Validar la integridad de la configuración recibida
- ❌ **NO** construir nomenclatura a partir de variables de gobernanza

---

## 6. Excepciones: Nomenclatura Interna

### 6.1. Sufijos y Componentes Internos

Si el módulo necesita agregar sufijos o componentes internos al nombre (ej. `-primary`, `-replica`), puede hacerlo **concatenando** al nombre base recibido:

```hcl
# Ejemplo válido: El módulo agrega sufijos internos
resource "aws_db_instance" "primary" {
  for_each = var.db_config
  
  # ✅ Usa el nombre base y agrega sufijo interno del módulo
  identifier = "${each.value.name}-primary"
}

resource "aws_db_instance" "replica" {
  for_each = var.db_config
  
  identifier = "${each.value.name}-read-replica-01"
}
```

---

## 7. Criterios de Cumplimiento

✅ El Root utiliza `locals.tf` para construir el payload de configuración de los módulos.  
✅ El payload de configuración inyecta el nombre final del recurso (Nomenclatura Estándar).  
✅ El módulo de referencia **no** construye la Nomenclatura Estándar a partir de variables de gobernanza (`client`, `project`, `environment`).  
✅ El módulo solo puede concatenar sufijos internos al nombre base recibido.

---

## 8. Relación con Pilares AWS Well-Architected

| Pilar | Cómo contribuye esta regla |
| :--- | :--- |
| **Operational Excellence** | La construcción centralizada de nomenclatura en el Root garantiza consistencia y facilita la evolución de las reglas de naming sin modificar los módulos. |

---

## 9. Beneficios

1. **Flexibilidad:** El Root puede aplicar reglas de nomenclatura personalizadas sin cambiar los módulos
2. **Portabilidad:** Los módulos son más portables al no depender de variables de gobernanza específicas
3. **Testabilidad:** Los módulos son más fáciles de probar al recibir configuración completa
4. **Mantenibilidad:** Cambios en las reglas de nomenclatura solo afectan al Root, no a los módulos
