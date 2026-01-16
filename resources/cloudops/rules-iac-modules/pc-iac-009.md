# 📄 Regla de Tipos de Datos, Conversiones y Lógica en Locals

**ID:** PC-IAC-009  
**Tipo:** Flujo de Datos / Lógica Interna  
**Pilares AWS Well-Architected:** Operational Excellence, Security  
**Versión:** 1.0  
**Fecha:** 10 de diciembre de 2025

---

## 1. Propósito y Alcance

Esta regla define los estándares obligatorios para la tipificación explícita de datos y el manejo de conversiones y lógica. Su objetivo es asegurar la coherencia del tipo de datos y centralizar toda la lógica de inyección y transformación en el archivo `locals.tf`.

**Aplicable a:**
1.  Declaración de `type` en `variables.tf`.
2.  Todas las funciones de conversión y lógica condicional en `locals.tf`.

---

## 2. Tipificación y Conversión Obligatoria

### 2.1. Tipificación Explícita

La tipificación explícita en `variables.tf` es obligatoria para todos los atributos (referencia **PC-IAC-002**).

* **Requisito:** Evitar la dependencia de la inferencia de tipos de Terraform para garantizar la estabilidad.

### 2.2. Conversiones Estrictas en `locals.tf`

Cualquier valor que cambie de tipo (ej. de cadena a número, o de mapa a lista) debe ser convertido explícitamente en `locals.tf`.

| Conversión | Propósito | Ejemplo de Función |
| :--- | :--- | :--- |
| Colecciones | Asegurar el tipo correcto de colecciones. | `tolist()`, `toset()`, `tomap()` |
| Numérico/Texto | Transformar un valor cuando el atributo del recurso lo exige. | `tonumber()`, `tostring()` |
| Chequeo de Nulos | Usar funciones para manejar valores faltantes de forma segura. | `try()`, `can()` |

---

## 3. Lógica de Inyección y Transformación (Exclusiva de `locals.tf`)

### 3.1. Inyección de Valores Dinámicos (Mandatorio)

La inyección de valores generados dinámicamente (`data.*` o `module.*.output`) dentro de estructuras de variables complejas (`map(object)`) está **estrictamente prohibida** en el bloque `module` principal.

* **Flujo Obligatorio:** Si una configuración de entrada (`var.config`) necesita ser enriquecida con un ARN o ID dinámico, la lógica de *merge* debe residir **exclusivamente en `locals.tf`** para mantener las variables limpias.

### 3.2. Manejo de Valores Por Defecto y Nulos

La lógica para aplicar valores por defecto o reemplazar campos vacíos con valores dinámicos debe utilizar el operador ternario (`? :`) y las funciones de chequeo de longitud (`length()`) en `locals.tf`.

* **Patrón Obligatorio:** Este patrón es obligatorio para inyectar IDs y ARNs dinámicos que no pueden ir en `terraform.tfvars`.

    ```hcl
    locals {
      # Ejemplo de inyección dinámica
      services_with_defaults = {
        for key, config in var.services : key => merge(config, {
          vpc_id = length(config.vpc_id) > 0 ? config.vpc_id : data.aws_vpc.selected.id
        })
      }
    }
    ```

### 3.3. Uso de `try()` y `can()`

Para acceder a atributos anidados o *outputs* de recursos que podrían no existir, es obligatorio utilizar las funciones `try()` o `can()` para evitar fallos de ejecución.

---

## 4. Criterios de Cumplimiento

✅ Se utiliza la tipificación explícita en `variables.tf`.  
✅ La lógica de inyección de valores dinámicos (`data.*` o `module.*.output`) reside **exclusivamente** en `locals.tf`.  
✅ Se usan funciones de chequeo de longitud (`length()`) u operadores ternarios (`? :`) para aplicar valores dinámicos por defecto.  
✅ Se utilizan `try()` o `can()` cuando se accede a atributos que pueden ser `null` o no existir.  
✅ Se usan funciones de conversión explícita (`tolist()`, `tonumber()`, etc.) cuando se cambia el tipo de un valor.

---

## 5. Relación con Pilares AWS Well-Architected

| Pilar | Cómo contribuye esta regla |
| :--- | :--- |
| **Operational Excellence** | La centralización de la lógica en `locals.tf` y el uso de funciones seguras eliminan la fuente de errores de tipo y fallos de ejecución. |
| **Security** | El uso de `try()` y `can()` previene errores cuando los datos de *outputs* de seguridad (o módulos opcionales) son consumidos. |