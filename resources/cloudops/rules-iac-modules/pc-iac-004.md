# 📄 Regla de Etiquetas Obligatorias (Tagging)

**ID:** PC-IAC-004  
**Tipo:** Etiquetas  
**Pilares AWS Well-Architected:** Cost Optimization, Operational Excellence, Security  
**Versión:** 1.0  
**Fecha:** 10 de diciembre de 2025

---

## 1. Propósito y Alcance

Esta regla define el estándar obligatorio para el etiquetado de recursos en AWS. El sistema de etiquetado opera en **dos capas** para garantizar la trazabilidad de costos, el cumplimiento de políticas y la flexibilidad del desarrollo.

**Aplicable a:**
1.  **Módulo Raíz (IaC de Referencia):** Definición de Tags Transversales.
2.  **Módulos de Referencia:** Aplicación de Tags Específicos y la etiqueta `Name`.

---

## 2. Capa 1: Etiquetas Transversales (Gobernanza y Costos)

Estas etiquetas son obligatorias para la asignación de costos y la identificación de alto nivel, y se aplican de forma masiva para asegurar la consistencia.

### 2.1. Aplicación Obligatoria (IaC de Referencia)

Las Etiquetas Transversales deben ser inyectadas en **todos** los recursos mediante el bloque `default_tags` del *provider* AWS en el módulo raíz (IaC de Referencia).

* **Requisito del Módulo Raíz:** El módulo raíz **debe** exponer la variable `common_tags` y utilizarla para el `default_tags` del *provider*.

    ```hcl
    # providers.tf del Módulo Raíz
    provider "aws" {
      alias = "principal"
      # ... configuración
      default_tags {
        tags = var.common_tags # Fuente de Tags Transversales
      }
    }
    ```

### 2.2. Etiquetas Transversales Mínimas

El mapa `common_tags` provisto por el usuario **debe** incluir, como mínimo, las siguientes claves:

* `Client`
* `Project`
* `Environment`
* `Owner`
* `CostCenter`

---

## 3. Capa 2: Etiquetas Específicas del Recurso (`Name` y `additional_tags`)

Esta capa permite la identificación única del recurso y la adición de etiquetas personalizadas por el usuario del módulo.

### 3.1. Etiqueta `Name` (Obligatoria y Explícita)

La etiqueta `Name` debe ser **aplicada explícitamente** en el bloque `tags` de **cada recurso** dentro de los Módulos de Referencia.

* **Construcción:** El valor de `Name` debe construirse utilizando la regla de nomenclatura **PC-IAC-003**, referenciando las variables locales (ej. `local.nombre_construido`).
* **Justificación:** Aplicarla explícitamente previene conflictos y asegura que el nombre sea visible inmediatamente.

### 3.2. Tags Adicionales (`additional_tags`)

Todo Módulo de Referencia que cree recursos debe exponer la variable `additional_tags` (dentro del mapa de configuración principal) para aceptar etiquetas personalizadas.

* **Aplicación (`merge` Obligatorio):** En el bloque `tags` del recurso, los tags específicos se deben combinar (mergear) con la etiqueta `Name` y los tags adicionales del usuario.

    ```hcl
    # tags en main.tf del Módulo de Referencia
    tags = merge(
      { Name = local.nombre_construido }, # Name (PC-IAC-003)
      each.value.additional_tags          # Tags específicos del usuario
    )
    ```

---

## 4. Criterios de Cumplimiento

✅ La IaC de Referencia usa `default_tags` para aplicar los *Tags* Transversales (Sec. 2.1).  
✅ La variable `common_tags` incluye el conjunto mínimo de etiquetas de gobernanza (Sec. 2.2).  
✅ Todo recurso que soporte etiquetas en el Módulo de Referencia incluye un bloque `tags = merge(...)`.  
✅ La etiqueta `Name` es siempre aplicada explícitamente y su valor cumple con **PC-IAC-003** (Sec. 3.1).  
✅ Los módulos exponen la opción para `additional_tags` para flexibilidad.

---

## 5. Relación con Pilares AWS Well-Architected

| Pilar | Cómo contribuye esta regla |
| :--- | :--- |
| **Cost Optimization** | Los tags obligatorios permiten la asignación de costos y la generación de reportes de facturación detallados. |
| **Operational Excellence** | El etiquetado consistente facilita la gestión de inventario, la automatización operativa y la aplicación de políticas. |
| **Security** | El etiquetado permite la aplicación de políticas de control de acceso basadas en atributos (ABAC). |

---