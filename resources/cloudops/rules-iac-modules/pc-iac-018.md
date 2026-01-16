
# 📄 Regla de Testing y Validación del Código

**ID:** PC-IAC-018  
**Tipo:** Calidad / Seguridad  
**Pilares AWS Well-Architectेड:** Operational Excellence, Security  
**Versión:** 1.0  
**Fecha:** 10 de diciembre de 2025

---

## 1. Propósito y Alcance

Esta regla define los requisitos obligatorios de validación, testing y análisis estático del código de IaC. Su objetivo es garantizar la calidad, detectar errores de sintaxis o seguridad antes del despliegue y asegurar la estabilidad de la infraestructura.

**Aplicable a:** Todos los Módulos de Referencia y Módulos Raíz (Proyectos).

---

## 2. Testing Obligatorio en Módulos de Referencia

Todo Módulo de Referencia (que vive en su propio repositorio) debe incluir pruebas automatizadas para validar su funcionalidad.

### 2.1. Inclusión de Directorios de Pruebas (Mandatorio)

Todo módulo debe contener los siguientes directorios y archivos:

* **`examples/`**: Obligatorio para demostrar casos de uso.
* **`tests/`**: Obligatorio para albergar pruebas automatizadas.

### 2.2. Validación Funcional

Se debe utilizar una herramienta de testing funcional para validar que los recursos se desplieguen correctamente.

* **Requisito:** La rama principal (`main`) del repositorio del módulo debe estar siempre estable y pasar todas las pruebas.

---

## 3. Análisis Estático y Validación de Seguridad

El *pipeline* de CI/CD para Módulos y Proyectos debe ejecutar herramientas de análisis estático en la fase de validación.

### 3.1. Análisis de Seguridad (Mandatorio)

Es obligatorio escanear el código con herramientas de seguridad (ej. Checkov o Terrascan) para validar el cumplimiento de las políticas antes del *plan*.

* **Requisito:** El *pipeline* debe fallar si se detectan vulnerabilidades de seguridad críticas o incumplimiento de políticas.

### 3.2. Formato y Sintaxis

Se debe ejecutar la validación de formato y sintaxis antes de cualquier plan o aplicación.

* **Comandos Obligatorios:**
    * `terraform fmt`: Para asegurar la consistencia del estilo HCL.
    * `terraform validate`: Para asegurar la validez de la sintaxis y la tipificación.

---

## 4. Validación en Pipelines de Despliegue (Proyectos)

El Módulo Raíz (Proyectos de Dominio) debe integrar la validación en sus *pipelines* de CI/CD.

### 4.1. `terraform plan` (Mandatorio)

Es obligatorio implementar la validación del plan en todos los *pipelines*.

* **Requisito:** El *pipeline* debe ejecutar un `terraform plan` y publicar el resultado como artefacto antes de cualquier fase de `apply`.

### 4.2. Aprobación Manual para Producción

El despliegue en el ambiente de **Producción** (`prod` o `pdn`) debe requerir siempre una aprobación manual explícita después de una revisión exitosa del `plan`.

---

## 5. Criterios de Cumplimiento

✅ Todos los Módulos de Referencia incluyen `examples/` y `tests/`.  
✅ Se implementan *tests automatizados* en los repositorios de módulos.  
✅ Los *pipelines* ejecutan `terraform fmt`, `terraform validate` y *análisis de seguridad*.  
✅ Se implementa el `terraform plan` obligatorio antes del `apply` en el *pipeline*.  
✅ Se requiere **aprobación manual** para los despliegues de Producción.

---

## 6. Relación con Pilares AWS Well-Architected

| Pilar | Cómo contribuye esta regla |
| :--- | :--- |
| **Operational Excellence** | El *testing* y la validación automatizada (`terraform plan` obligatorio) aseguran que el despliegue sea predecible y eliminan el riesgo de errores en producción. |
| **Security** | El escaneo de seguridad en el *pipeline* previene la creación de infraestructura que incumpla las políticas de seguridad de la organización. |