# 📄 Regla de Bloques Dinámicos y Splat Expressions

**ID:** PC-IAC-014  
**Tipo:** Sintaxis HCL / Control de Recursos  
**Pilares AWS Well-Architected:** Operational Excellence, Security  
**Versión:** 1.0  
**Fecha:** 10 de diciembre de 2025

---

## 1. Propósito y Alcance

Esta regla define el uso obligatorio del bloque `dynamic` y la sintaxis de *Splat Expressions* (`[*]`) para iterar sobre listas de configuraciones y extraer colecciones de IDs. Su objetivo es mantener los bloques de recursos limpios, evitar la duplicación de código y simplificar la manipulación de datos en colecciones.

**Aplicable a:** Bloques `resource` que utilizan listas de configuraciones anidadas y la extracción de *outputs* o *data* de colecciones.

---

## 2. Uso Obligatorio del Bloque `dynamic`

El bloque `dynamic` es obligatorio para cualquier atributo de recurso que acepte una lista de bloques anidados y cuya configuración provenga de una variable o *local* compleja.

### 2.1. Sustitución de `count` para Bloques

* **Regla:** Se prohíbe el uso de `count` para generar bloques anidados si la lista de configuraciones es variable. En su lugar, debe usarse `dynamic`.
* **Ejemplo (Aceptado):** Uso de `dynamic` para generar reglas de *Ingress/Egress* en un *Security Group* a partir de un mapa de reglas.

    ```hcl
    resource "aws_security_group" "example" {
      # ...
      dynamic "ingress" {
        for_each = var.ingress_rules # Itera sobre la lista de reglas
        content {
          from_port   = ingress.value.from_port
          to_port     = ingress.value.to_port
          protocol    = ingress.value.protocol
          # ...
        }
      }
    }
    ```

### 2.2. Prohibición de Bloques Repetidos Estáticos

Se prohíbe la declaración de múltiples bloques de configuración idénticos (ej. múltiples bloques `ingress { ... }`) si pueden ser generados a partir de una lista.

---

## 3. Extracción de Datos con Splat Expressions

La sintaxis de *Splat Expressions* (`[*]`) es la forma preferida y obligatoria para extraer listas de atributos de una colección de recursos, *data sources* o *outputs*.

### 3.1. Extracción Simple de IDs

Para obtener una lista de IDs de un recurso creado con `count` o `for_each`, se debe usar la sintaxis `[*].id`.

* **Patrón Obligatorio:** Evitar iteraciones o funciones redundantes (`for` o `tolist` innecesarios) para la extracción directa.

    ```hcl
    # Extracción eficiente de IDs de subred
    output "subnet_ids" {
      description = "Lista de IDs de las subredes."
      value       = aws_subnet.example[*].id
    }
    ```

### 3.2. Extracción de Atributos Anidados (Tuplas)

Cuando se trabaja con recursos creados con `for_each`, el *Splat Expression* debe aplicarse sobre los `values()` del mapa para obtener una lista y luego el atributo deseado.

* **Patrón Obligatorio:**

    ```hcl
    # Extracción de ARNs de una colección creada con for_each
    output "cluster_arns" {
      value = values(aws_ecs_cluster.this)[*].arn
    }
    ```

---

## 4. Criterios de Cumplimiento

✅ Se utiliza el bloque `dynamic` para generar bloques de configuración anidados a partir de una variable.  
✅ Se prohíbe la declaración manual de bloques de recursos idénticos que pueden ser generados dinámicamente.  
✅ Se utiliza la sintaxis de *Splat Expressions* (`[*].id` o `values(...)[*].arn`) para extraer colecciones de IDs/ARNs de manera eficiente.  
✅ Se evita el uso de `for` loops redundantes cuando se puede usar un *Splat Expression* simple.

---

## 5. Relación con Pilares AWS Well-Architected

| Pilar | Cómo contribuye esta regla |
| :--- | :--- |
| **Operational Excellence** | El uso de `dynamic` y *Splat Expressions* simplifica significativamente el código de los recursos y reduce el riesgo de errores al gestionar listas complejas. |
| **Security** | El control estricto sobre cómo se generan las reglas de seguridad (ej. `ingress/egress` en SG) reduce la posibilidad de que se omita una regla en una configuración manual. |