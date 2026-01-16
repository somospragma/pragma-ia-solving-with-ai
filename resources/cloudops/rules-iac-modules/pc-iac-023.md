## 📄 Regla de Diseño Monolítico Funcional (Módulo de Referencia)

**ID:** PC-IAC-023  
**Tipo:** Modularización / Responsabilidad Única  
**Pilares AWS Well-Architected:** Operational Excellence, Security  
**Versión:** 1.0  
**Fecha:** 10 de diciembre de 2025

---

## 1. Propósito y Alcance

Esta regla impone el principio de **Responsabilidad Única** en el diseño de los Módulos de Referencia. Su objetivo es asegurar que un módulo solo contenga los recursos necesarios para desplegar un único servicio o funcionalidad principal, delegando las dependencias externas (Networking, Seguridad, IAM) al consumidor (IaC Root).

**Aplicable a:** El bloque `main.tf` de todos los Módulos de Referencia.

---

## 2. Restricciones de Creación de Recursos

### 2.1. Monolítico Funcional (Mandatorio)

El Módulo de Referencia **solo debe crear** recursos directamente intrínsecos al servicio principal que representa.

* **Ejemplo Aceptado (Módulo de ECS Service):** Solo puede crear `aws_ecs_service`, `aws_ecs_task_definition`, `aws_cloudwatch_log_group`, y cualquier otro recurso **directamente encapsulado** por la definición del servicio.
* **Prohibido:** El módulo no debe crear recursos de infraestructura base o de seguridad.

### 2.2. Prohibición de Recursos de Gobernanza Cruzados

El Módulo de Referencia **no debe** crear recursos de los siguientes dominios:

* **Seguridad/IAM:** `aws_security_group`, `aws_iam_role`, `aws_iam_policy`.
* **Networking:** `aws_vpc`, `aws_subnet`, `aws_route_table`.
* **Balanceo (General):** `aws_lb` (ALB/NLB).

---

## 3. Manejo de Dependencias y Roles

### 3.1. Roles y Permisos (Data Sources/Inputs)

Si el módulo necesita un rol IAM (ej. `execution_role_arn` para ECS o `role_arn` para EKS), **debe recibir el ARN como una variable de entrada** (`var.role_arn`). 

* **Flujo:** El consumidor (IaC Root) es responsable de usar un *Data Source* o el *Output* del módulo de Seguridad para obtener el ARN y pasarlo al módulo.

### 3.2. Seguridad (SG) y Conectividad (VPC/Subnets)

El módulo **nunca** debe intentar crear su propio Security Group o buscar subredes.

* **Requisito:** Los IDs de la VPC, Subred y Security Group deben ser recibidos exclusivamente a través de variables de entrada (`var.vpc_id`, `var.subnet_ids`, `var.security_group_ids`).

---

## 4. Criterios de Cumplimiento

✅ El Módulo de Referencia solo contiene recursos intrínsecos al servicio principal (Monolítico Funcional).  
✅ Se prohíbe la creación de recursos de los dominios Seguridad, Networking e IAM.  
✅ Los ARNs de Roles y los IDs de Seguridad/VPC se reciben únicamente como variables de entrada.

---

## 5. Relación con Pilares AWS Well-Architected

| Pilar | Cómo contribuye esta regla |
| :--- | :--- |
| **Operational Excellence** | Aplicar el principio de Responsabilidad Única hace que el módulo sea predecible, más fácil de probar y reutilizar, ya que sus *inputs* son claros y sus *outputs* controlados. |
| **Security** | El módulo es totalmente agnóstico a las políticas de acceso y roles, ya que solo los consume. Esto asegura que el dominio de Seguridad mantenga el control centralizado de los permisos. |