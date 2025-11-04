# Guía análisis de Actividades Core para Proyectos de Infraestructura Cloud Basado en el Framework de Madurez

Este documento establece una referencia base para realizar un análisis automatizado de las actividades fundamentales (core) en proyectos de infraestructura cloud. El objetivo es proporcionar un marco estructurado que permita a herramientas automatizadas y sistemas de IA evaluar de manera consistente la calidad, completitud y madurez de los proyectos de infraestructura cloud.

> **Nota:** Estos criterios evalúan la implementación de principios y prácticas de infraestructura cloud, siendo aplicables tanto a proyectos gestionados con IaC (Terraform, CloudFormation, etc.) como a infraestructura configurada manualmente.

---

## Gobernanza

### Directrices establecidas para asignación, nomenclatura y gestión de tags en recursos cloud

El proyecto debe contar con un sistema estructurado de clasificación mediante metadatos estandarizados que permita la identificación y gestión coherente de recursos cloud. Este sistema se fundamenta en una taxonomía jerárquica de categorización, convenciones de nomenclatura universales, y políticas de gobierno que aseguren cumplimiento continuo.

- **Obligatoriedad**: Aplicación de tags mínimos requeridos sin excepciones en todos los recursos desplegados.
- **Estandarización de valores**: Catálogo cerrado de valores permitidos por cada tipo de tag para evitar variaciones.
- **Validación preventiva**: Verificación de cumplimiento antes del despliegue, no después de la creación del recurso.

### Ambientes definidos para despliegue de aplicaciones

Debe existir un marco estructurado de categorización y caracterización de entornos que permita la segregación lógica y funcional de aplicaciones según su propósito, nivel de madurez y requisitos operacionales.

Se requiere un mínimo de tres ambientes completamente independientes para soportar el ciclo completo de desarrollo de software, garantizando que ningún cambio llegue a producción sin haber sido validado en contextos de menor criticidad.

- **Aislamiento total**: Independencia completa entre ambientes sin recursos compartidos que puedan generar contaminación cruzada.

### Cuentas organizadas con Landing Zone habilitada

El proyecto debe contar con un marco de gobernanza organizacional integral que estructure las cuentas cloud en una jerarquía coherente, implemente una Landing Zone con configuraciones predefinidas, aplique políticas corporativas de forma sistemática y centralice la gestión de identidades. 

- **Estructura organizacional**: Jerarquía de cuentas que refleje la estructura empresarial y facilite la gestión por unidades de negocio.
- **Fundación estandarizada**: Landing Zone con configuraciones predefinidas de seguridad, cumplimiento y operaciones aplicadas consistentemente.
- **Centralización de identidades**: Gestión unificada de identidades, autenticación y autorización a través de toda la organización cloud.
- **Herencia de gobernanza**: Aplicación automática de políticas corporativas desde niveles organizacionales superiores hacia subordinados.

## Fiabilidad

### Línea base de backups definida para el proyecto

Se requiere una estrategia integral de protección de datos que establezca los fundamentos, políticas y criterios para la implementación de respaldos según la criticidad y naturaleza de la información del proyecto.

- **Protección diferenciada por criticidad**: Nivel de respaldo proporcional al impacto de pérdida de datos en operaciones del negocio.
- **Frecuencia adecuada**: Intervalos de respaldo alineados con la tasa de cambio y requisitos de recuperación.
- **Retención por ciclo de vida**: Políticas de conservación que varían según antigüedad y tipo de dato.
- **Aislamiento geográfico**: Almacenamiento de copias en ubicaciones físicamente separadas del origen.

## Seguridad

### Seguridad de red establecida en la nube

El proyecto debe contar con una infraestructura de red aislada y controlada que proporcione la base de conectividad segura para todos los recursos en la nube, minimizando la superficie de ataque mediante controles estrictos de acceso.

- **Aislamiento por defecto**: Separación completa de recursos en red privada sin acceso público a menos que sea explícitamente requerido.
- **Segmentación por función**: División de la red en subredes especializadas según propósito, criticidad y requisitos de seguridad.
- **Exposición mínima**: Restricción por defecto de acceso público con apertura solo cuando existe justificación de negocio irrefutable.
- **Protección de puertos críticos**: Bloqueo absoluto de puertos administrativos y de gestión desde internet público.
- **Principio de menor privilegio**: Restricción de rangos IP origen al conjunto mínimo necesario en lugar de 0.0.0.0/0.
- **Escalabilidad de direccionamiento**: Espacio de direcciones IP que soporta crecimiento futuro sin requerir rediseño fundamental.

### Servicio de control de políticas activado en la nube

Debe existir un marco de gobernanza técnica que permita definir, aplicar y auditar políticas de seguridad y cumplimiento de forma centralizada y automatizada en toda la infraestructura cloud.

- **Control preventivo**: Bloqueo automático de acciones que violan políticas antes de que ocurran, no solo detección posterior.
- **Políticas como código**: Definición declarativa y versionada de restricciones que permite auditoría y evolución controlada.
- **Aplicación centralizada**: Gestión unificada de políticas que garantiza consistencia en toda la organización cloud.
- **Cumplimiento continuo**: Validación permanente del estado de conformidad sin ventanas de vulnerabilidad.
- **Granularidad de control**: Capacidad de aplicar políticas a diferentes niveles según estructura organizacional y criticidad.

### Políticas de seguridad organizacional y controles de acceso implementados

El proyecto debe contar con un sistema integral de seguridad organizacional que proteja los recursos cloud mediante la implementación de autenticación multifactor, la aplicación de políticas de seguridad corporativas, el control granular de accesos y la gestión centralizada de la postura de seguridad.

- **Autenticación reforzada**: Implementación obligatoria de MFA para cuentas privilegiadas, usuarios root y accesos críticos del sistema.
- **Segregación de recursos**: Aislamiento lógico y físico de recursos según criticidad y contexto organizacional.
- **Políticas de contraseñas robustas**: Aplicación de estándares de complejidad con mínimo 14 caracteres y prevención de reutilización.
- **Rotación de credenciales organizacionales**: Cambio automático de contraseñas cada 45 días para cuentas de usuario.
- **Gestión de costos integrada**: Políticas de seguridad que incluyan controles de costos y cumplimiento presupuestario.

### Secretos y credenciales gestionados de forma segura

Se requiere un sistema automatizado de gestión de secretos que proteja las credenciales de aplicaciones, servicios y APIs mediante rotación automática, almacenamiento seguro, distribución controlada y detección proactiva de exposiciones.

- **Rotación automática de secretos**: Cambio periódico y automático de claves API, tokens de acceso y certificados sin intervención manual.
- **Almacenamiento centralizado**: Gestión unificada de secretos en repositorios seguros con cifrado en reposo y en tránsito.
- **Distribución controlada**: Entrega segura de credenciales a aplicaciones y servicios mediante mecanismos de inyección automática.
- **Eliminación de hardcoding**: Remoción completa de credenciales embebidas en código fuente, configuraciones o imágenes.
- **Detección de exposiciones**: Monitoreo continuo de repositorios públicos, web y fuentes externas para detectar divulgación involuntaria de claves.
- **Rotación de accesos programáticos**: Cambio automático de claves de acceso y tokens con periodo máximo de 90 días.

## Mantenibilidad

### Recursos de infraestructura gestionados con IaC

El proyecto debe contar con un sistema de gestión de infraestructura basado en código que garantice la mantenibilidad, consistencia y evolución controlada de todos los recursos cloud.

- **Infraestructura declarativa**: Definición del estado deseado mediante código versionado que elimina la configuración manual.
- **Versionado y trazabilidad**: Control de cambios con historial completo que permite rollback y auditoría de modificaciones.
- **Automatización de ciclo de vida**: Gestión automatizada de creación, actualización y destrucción de recursos sin intervención manual.
- **Modularización y reutilización**: Componentes de infraestructura reutilizables que promueven consistencia y reducen duplicación.
- **Validación continua**: Verificación automática de configuraciones antes del despliegue para prevenir errores.
- **Documentación como código**: Especificaciones técnicas integradas en el código que se mantienen actualizadas automáticamente.

## Observabilidad

### Tráfico de red capturado en red privada virtual

El proyecto debe contar con un sistema de captura y análisis de tráfico de red que proporcione visibilidad completa sobre las comunicaciones dentro de la infraestructura de red privada virtual.

- **Captura no intrusiva**: Recolección de información de tráfico sin afectar el rendimiento ni la latencia de las comunicaciones.
- **Cobertura total**: Captura de flujos en todas las interfaces de red sin exclusiones.
- **Retención estructurada**: Almacenamiento de logs con periodo definido para análisis histórico y forense.
- **Centralización**: Agregación de logs de múltiples fuentes en repositorio unificado para correlación.
