# 📄 Regla de Versiones y Estabilidad

**ID:** PC-IAC-006  
**Tipo:** Versiones  
**Pilares AWS Well-Architected:** Operational Excellence, Security  
**Versión:** 1.0  
**Fecha:** 10 de diciembre de 2025

---

## 1. Propósito y Alcance

Esta regla define los estándares obligatorios para la declaración de la versión de Terraform y los *providers* requeridos. Su cumplimiento garantiza la estabilidad, previene cambios inesperados en el comportamiento y asegura la compatibilidad a largo plazo.

**Aplicable a:** El bloque `terraform { ... }` en `versions.tf` de la IaC de Referencia (Root) y en los Módulos de Referencia.

---

## 2. Requisitos de Versión de Terraform y Providers

### 2.1. Versión de Terraform (`required_version`)

La versión mínima de Terraform debe especificarse siempre.

* **Operador:** Usar siempre el operador `>=` para permitir actualizaciones menores sin intervención manual.
    * *Ejemplo:* `required_version = ">= 1.14.0"`

### 2.2. Pinning de Providers (`required_providers`)

El *pinning* de *providers* es obligatorio para evitar que una actualización mayor (cambios que rompen la compatibilidad) cause fallos.

* **Formato Estándar:** Usar rangos que aseguren estabilidad. Se recomienda el operador de tilde y mayor que (`~>`), o un rango cerrado, para evitar versiones mayores.
    * **Módulo Raíz (Root):** Utilizar un rango estricto. *Ejemplo:* `version = "~> 6.20.0"`
    * **Módulos de Referencia:** Utilizar un rango mínimo que sea compatible con el Root. *Ejemplo:* `version = ">= 4.31.0"`

---

## 3. Configuración Específica por Capa

### 3.1. Módulo Raíz (IaC Root)

El módulo raíz debe incluir el bloque `terraform { ... }` con la configuración del *backend* y los requisitos de versión.

* **`required_version` y `required_providers`:** Aplicar las reglas de *pinning* estricto (Sec. 2.1 y 2.2).
* **`backend` (Estado):** La configuración del estado es obligatoria y debe asegurar la integridad y la seguridad.
    * **Obligatorio:** Usar S3 con `encrypt = true` y un mecanismo de bloqueo (ej. `use_lockfile = true` o DynamoDB para bloqueo).

    ```hcl
    # Ejemplo en versions.tf (Root)
    terraform {
      required_version = ">= 1.14.0"
      required_providers {
        aws = {
          source  = "hashicorp/aws"
          version = "~> 6.20.0" 
        }
      }
      backend "s3" {
        bucket       = "nombre-del-bucket-estado"  
        key          = "ruta/a/terraform.tfstate"  
        region       = "us-east-1"  
        encrypt      = true  
        use_lockfile = true 
      }
    }
    ```

### 3.2. Módulos de Referencia

Los Módulos de Referencia deben definir sus dependencias de versión, pero **nunca** deben incluir la configuración de `backend`.

* **Alias Consumidor:** Deben incluir la declaración `configuration_aliases = [aws.project]` tal como se define en la **PC-IAC-005**.

    ```hcl
    # Ejemplo en versions.tf del Módulo de Referencia
    terraform {
      required_version = ">= 1.0.0"
      required_providers {
        aws = {
          source                = "hashicorp/aws"
          version               = ">= 4.31.0"
          configuration_aliases = [aws.project]
        }
      }
    }
    ```

---

## 4. Criterios de Cumplimiento

✅ El Módulo Raíz define `required_version`, `required_providers` y el bloque `backend` con cifrado.  
✅ El Módulo de Referencia define `required_version` y `required_providers` sin configurar `backend`.  
✅ La versión de Terraform se especifica con `>=`.  
✅ El *backend* S3 utiliza `encrypt = true` y mecanismo de bloqueo.

---

## 5. Relación con Pilares AWS Well-Architected

| Pilar | Cómo contribuye esta regla |
| :--- | :--- |
| **Operational Excellence** | El *pinning* de versiones previene fallos inesperados y asegura la reproducibilidad de los despliegues. |
| **Security** | La configuración obligatoria de `backend` con `encrypt = true` y el bloqueo de estado asegura que el estado de la infraestructura esté protegido en reposo y durante la modificación. |

---