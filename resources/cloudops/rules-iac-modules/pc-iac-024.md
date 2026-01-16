# 📄 Regla de Trazabilidad de la Configuración Compleja

**ID:** PC-IAC-024  
**Tipo:** Flujo de Datos / Variables  
**Pilares AWS Well-Architected:** Operational Excellence  
**Versión:** 1.0  
**Fecha:** 10 de diciembre de 2025

---

## 1. Propósito y Alcance

Esta regla formaliza el punto de origen obligatorio para la configuración compleja de los módulos (ej. `sg_config`, `ecs_services`). Su objetivo es asegurar la trazabilidad, la gestión por ambiente (`tfvars`) y la limpieza del código base HCL.

**Aplicable a:** Todas las variables de tipo colección (`map` o `list` de objetos) definidas en `variables.tf` que actúan como *payloads* de configuración para módulos.

---

## 2. Origen Obligatorio de la Configuración

### 2.1. Prohibición de Configuración Local Estática

La configuración compleja que varía por ambiente (ej. `desired_count`, reglas de *ingress*, *target groups*) **no debe** ser definida estáticamente dentro de `locals.tf`.

* **Regla:** La fuente de verdad para estos valores debe ser el archivo de variables del ambiente (ej. `dev.tfvars`, `prod.tfvars`).

### 2.2. Flujo de Trazabilidad (Mandatorio)

Cualquier variable en `variables.tf` que sea un mapa o lista de objetos y que no sea una variable de gobernanza simple (como `client` o `project`), debe seguir este flujo riguroso: 

1.  **Declaración en `variables.tf`:** (Con un `default = {}` o `default = []` para manejar la opcionalidad).
2.  **Definición de Valores en `.tfvars`:** (Para separar la configuración del código).
3.  **Transformación en `locals.tf`:** (Donde ocurre la inyección de ARNs y IDs dinámicos, **PC-IAC-009**).
4.  **Consumo en `main.tf`:** (Donde el `module` llama al `local`, **PC-IAC-021**).

### 2.3. Uso de la Variable (`var.*`)

El `locals.tf` siempre debe consumir la variable de entrada (`var.*`) como base para la transformación.

* **Ejemplo de Cumplimiento:**

    ```hcl
    # locals.tf
    # Consume var.ecs_services, que viene de tfvars, y le añade los ARNs dinámicos.
    ecs_services_with_defaults = {
      for key, config in var.ecs_services : key => merge(config, {
        # ... lógica de inyección de ARNs y Subnets (PC-IAC-009) ...
      })
    }
    ```

---

## 3. Antipatrón: Configuración Hardcodeada

### 3.1. Ejemplo INCORRECTO

❌ **NO HACER:**
```hcl
# locals.tf (INCORRECTO)
locals {
  # ❌ Configuración hardcodeada directamente en locals
  ecs_services = {
    "api" = {
      desired_count = 3
      cpu           = 256
      memory        = 512
    }
    "worker" = {
      desired_count = 2
      cpu           = 512
      memory        = 1024
    }
  }
}
```

**Problema:** No hay trazabilidad de dónde vienen estos valores, y cambiarlos entre ambientes requiere modificar el código HCL.

### 3.2. Ejemplo CORRECTO

✅ **HACER:**

**1. En `terraform.tfvars`:**
```hcl
ecs_services = {
  "api" = {
    desired_count = 3
    cpu           = 256
    memory        = 512
    subnet_ids    = []  # Se llenará dinámicamente
  }
  "worker" = {
    desired_count = 2
    cpu           = 512
    memory        = 1024
    subnet_ids    = []
  }
}
```

**2. En `variables.tf`:**
```hcl
variable "ecs_services" {
  description = "Configuration for ECS services"
  type = map(object({
    desired_count = number
    cpu           = number
    memory        = number
    subnet_ids    = list(string)
  }))
  default = {}
}
```

**3. En `locals.tf`:**
```hcl
locals {
  # Transformación: inyectar subnet_ids dinámicos si están vacíos
  ecs_services_transformed = {
    for key, config in var.ecs_services : key => merge(config, {
      subnet_ids = length(config.subnet_ids) > 0 ? config.subnet_ids : data.aws_subnets.private.ids
    })
  }
}
```

**4. En `main.tf`:**
```hcl
module "ecs_services" {
  source = "..."
  
  services = local.ecs_services_transformed  # ✅ Consume local transformado
}
```

---

## 4. Separación por Ambiente

### 4.1. Estructura de Archivos por Ambiente

La configuración compleja debe gestionarse mediante archivos `.tfvars` separados por ambiente:

```
project/
├─ dev.tfvars
├─ qa.tfvars
├─ prod.tfvars
├─ variables.tf
├─ locals.tf
└─ main.tf
```

### 4.2. Diferencias de Configuración por Ambiente

**dev.tfvars:**
```hcl
ecs_services = {
  "api" = {
    desired_count = 1  # Menor capacidad en dev
    cpu           = 256
    memory        = 512
  }
}
```

**prod.tfvars:**
```hcl
ecs_services = {
  "api" = {
    desired_count = 10  # Mayor capacidad en prod
    cpu           = 1024
    memory        = 2048
  }
}
```

---

## 5. Criterios de Cumplimiento

✅ La configuración compleja se origina en un archivo `.tfvars` y no está codificada en `locals.tf`.  
✅ El `locals.tf` siempre utiliza `var.*` como el origen del mapa de configuración antes de aplicar la lógica de transformación (PC-IAC-009).  
✅ El `main.tf` consume el valor `local.*` para invocar el módulo (PC-IAC-021).  
✅ Existen archivos `.tfvars` separados por ambiente con las configuraciones específicas.

---

## 6. Relación con Pilares AWS Well-Architected

| Pilar | Cómo contribuye esta regla |
| :--- | :--- |
| **Operational Excellence** | La trazabilidad clara del origen de la configuración facilita el debugging, el mantenimiento y la gestión de cambios entre ambientes. |

---

## 7. Excepciones

### 7.1. Valores Calculados Puros

Si un valor es puramente calculado y no varía por ambiente (ej. transformaciones matemáticas, concatenaciones estándar), puede definirse directamente en `locals.tf`.

**Ejemplo Válido:**
```hcl
locals {
  # ✅ Valor calculado que no varía por ambiente
  total_capacity = sum([for svc in var.ecs_services : svc.desired_count])
}
```

### 7.2. Constantes del Módulo

Valores constantes que son intrínsecos al módulo y nunca varían pueden definirse en `locals.tf`.

**Ejemplo Válido:**
```hcl
locals {
  # ✅ Constantes del módulo
  supported_protocols = ["HTTP", "HTTPS", "TCP"]
  default_health_check_path = "/health"
}
```
