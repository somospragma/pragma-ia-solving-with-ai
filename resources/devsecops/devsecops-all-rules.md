# Guía de Análisis de Seguridad Integral para Workspaces Minimos DevSecOps Basado en el Framework de Madurez

Este documento sirve como contexto y referencia para que una IA o herramienta automatizada realice un análisis de seguridad general en un workspace, abarcando por enfoques o topicos que se de ahora en adelante serán Reglas: 2. almacenamiento seguro de información sensible, 3. control de acceso, 4. análisis estático (SAST), 5. análisis dinámico (DAST) y 6. composición de software (SCA).

## 1. Análisis Automático del Proyecto
Primero, analiza el repositorio actual para extraer automáticamente la siguiente información. 

### Detección Automática de Información
1.1 **Analiza la estructura de directorios** del proyecto para identificar:
   - Archivos de configuración (package.json, pom.xml, requirements.txt, etc.)
   - Estructura de carpetas (src/, docs/, config/, etc.)
   - Archivos de entrada principales

1.2 **Identifica tecnologías automáticamente** examinando:
   - Archivos de dependencias y gestores de paquetes
   - Extensiones de archivos fuente
   - Archivos de configuración de frameworks
   - Scripts de construcción y despliegue

1.3 **Detecta patrones arquitectónicos** observando:
   - Estructura de carpetas (microservicios vs monolítica)
   - Archivos de configuración de contenedores (Dockerfile, docker-compose.yml)
   - Configuraciones de API (OpenAPI/Swagger)
   - Archivos de configuración de servidores

1.4. **Extrae información de configuración** de:
   - Variables de entorno (.env, config files)
   - Puertos configurados en servidores
   - Endpoints definidos en código
   - Configuraciones de base de datos

1.5 **Analiza frameworks específicos** identificando:
   - **Python**: Django (manage.py), Flask (app.py), FastAPI (main.py)
   - **JavaScript/TypeScript**: React (src/App.js), Angular (angular.json), Vue (vue.config.js)
   - **Java**: Spring Boot (application.properties), Quarkus, Micronaut
   - **IaC**: Terraform (*.tf), CloudFormation (*.yaml con AWSTemplateFormatVersion)

1.6 **Detecta herramientas DevOps**:
   - CI/CD pipelines (.github/workflows/, .gitlab-ci.yml, Jenkinsfile)
   - Orchestration (Kubernetes yamls, Docker Compose)
   - Monitoring (Prometheus configs, Grafana dashboards)

### Información del Proyecto (Auto-extraída)
- **Nombre del Proyecto**: [EXTRAER_DE_PACKAGE_JSON_O_README]
- **Tipo de Aplicación**: [DETECTAR_POR_ESTRUCTURA_Y_DEPENDENCIAS]
- **Tecnologías Principales**: [EXTRAER_DE_ARCHIVOS_DE_DEPENDENCIAS]
- **Puerto/Endpoint Principal**: [BUSCAR_EN_CONFIGS_Y_CODIGO]
- **Arquitectura Base**: [INFERIR_DE_ESTRUCTURA_DE_CARPETAS]

**Luego, según el tipo de aplicación detectado:**

- Si el proyecto es de **infraestructura** (por ejemplo, contiene principalmente archivos de IaC como Terraform, CloudFormation, ARM, etc.), **realiza el 3: Control de Acceso (ACL) en Recursos Críticos de Red**.
- Si el proyecto **no es de infraestructura** (aplicaciones, servicios, etc.), **realiza solo las reglas** (2, 4, 5 y 6) y omite el la Regla 3.


**Esto permite adaptar el análisis de seguridad al contexto real del proyecto y evitar revisiones irrelevantes.**

---

## 2. Almacenamiento Seguro de Información Sensible

**Objetivo:** Garantizar que toda información de configuración sensible esté cifrada y protegida.

2.1 **Identificación de información sensible:**  
   - Buscar datos como contraseñas, claves API, tokens, secretos, certificados, credenciales, variables de entorno, etc.
2.2 **Almacenamiento seguro:**  
   - Verificar el uso de cifrado y herramientas seguras (Vault, KMS, SOPS, AWS Secrets Manager, Azure Key Vault, etc.).
2.3 **Ausencia de texto plano:**  
   - Revisar que no existan datos sensibles en texto plano en archivos, scripts o documentación.
2.4 **Validación de exclusión en control de versiones:**  
   - Confirmar que archivos como `.env`, `config`, `settings`, `secrets` estén en `.gitignore` y no versionados accidentalmente.
2.5 **Trazabilidad y control de versiones:**  
   - Asegurar que los archivos cifrados estén bajo control de versiones de forma segura.
2.6 **Justificación de excepciones:**  
   - Documentar cualquier excepción y los controles alternativos aplicados.

---

## 3. Control de Acceso (ACL) en Recursos Críticos de Red

**Objetivo:** Verificar que cada recurso crítico de red tenga una definición explícita y aplicada de control de acceso.

3.1 **Presencia de ACLs:**  
   - Buscar bloques, objetos o declaraciones con palabras clave como: acl, access_control, rule, allow, deny, ingress, egress, source, destination, port, protocol, cidr, principal, role, permission, policy, security_group, firewall_rule, network_policy.
3.2 **Aplicación efectiva:**  
   - Confirmar que la ACL esté asociada a un recurso real y no esté comentada ni deshabilitada.
3.3 **Principio de menor privilegio:**  
   - Revisar que no existan reglas con 0.0.0.0/0 en puertos críticos (22, 3389, 443, 80) sin justificación explícita.
3.4 **Unicidad por recurso:**  
   - Verificar que cada recurso tenga su propia ACL y no dependa de ACLs genéricas sin trazabilidad.
3.5 **Trazabilidad:**  
   - Asegurar que la ACL pueda rastrearse hasta su archivo de origen y esté bajo control de versiones.

---

## 4. Análisis Estático de Código (SAST)

**Objetivo:** Detectar vulnerabilidades de seguridad en el código fuente antes de su ejecución.

4.1 **Identificación de vulnerabilidades comunes:**  
   - Buscar patrones inseguros como inyecciones, uso inseguro de funciones, manejo incorrecto de datos externos, exposición de información sensible.
4.2 **Validación de prácticas seguras:**  
   - Verificar validación y sanitización de entradas, y gestión segura de errores.
4.3 **Revisión de autenticación y autorización:**  
   - Revisar controles de acceso en rutas, endpoints y funciones.
4.4 **Detección de información sensible:**  
   - Buscar credenciales o secretos expuestos en el código.
4.5 **Validación de dependencias:**  
   - Analizar archivos de dependencias para detectar librerías vulnerables.
4.6 **Reporte y trazabilidad:**  
   - Documentar vulnerabilidades con archivo y línea afectada, y sugerir correcciones.
4.7 **Justificación de excepciones:**  
   - Documentar excepciones justificadas y controles compensatorios.

---

## 5. Análisis Dinámico de Aplicaciones (DAST)

**Objetivo:** Identificar vulnerabilidades en la aplicación de un reporte externo (OWASP ZAP u otra herramienta DAST), Si el reporte no está disponible, indique si desea continuar con la validación por conocimiento propio.

5.1 **Recopilación de información:**  
   - Solicitar al desarrollador la URL base, endpoints, autenticación y roles, o analizar el workspace para identificar puntos de entrada.
5.2 **Análisis del workspace:**  
   - Buscar archivos que definan rutas, endpoints o configuraciones de red.
5.3 **Generación de scripts de ataque:**  
   - Crear scripts (fetch, curl, Postman, OWASP ZAP) para simular ataques: inyección, autenticación, acceso no autorizado, extracción de información sensible.
5.4 **Ejecución y orientación:**  
   - Guiar al desarrollador en la ejecución de scripts y análisis de respuestas.
5.5 **Documentación y remediación:**  
   - Documentar hallazgos y orientar sobre correcciones.
5.6 **Opciones y mejoras:**  
   - Recomendar integración de herramientas DAST en CI/CD y uso de extensiones de seguridad.

---

## 6. Análisis de Composición de Software (SCA)

**Objetivo:** Detectar vulnerabilidades y riesgos en las dependencias y componentes de terceros.

6.1 Valida si esta disponible el MCP de Trivy y la tool scan_filesystem, si no esta disponible o no se puede ejecutar, pregunta si dispone de un reporte externo (Trivy u otra herramienta SCA) e indique la ubicación del archivo y el formato utilizado (por ejemplo: /reports/trivy_scan_2025-11-20.json). Si el reporte no está disponible, indique si desea continuar con la validación por conocimiento propio.

6.2 **Recopilación de información:**  
   - Identificar archivos de dependencias (`pom.xml`, `build.gradle`, `package.json`, etc.).
6.3 **Inventario de componentes:**  
   - Listar todas las dependencias y sus versiones.
6.4 **Detección de vulnerabilidades:**  
   - Buscar vulnerabilidades conocidas en bases públicas (NVD, Snyk, osv.dev, etc.).
6.5 **Revisión de licencias:**  
   - Analizar licencias para detectar incompatibilidades o restricciones.
6.6 **Generación de reporte:**  
   - Documentar dependencias vulnerables, recomendaciones y conflictos de licencias.
6.7 **Opciones y mejoras:**  
   - Recomendar integración de herramientas SCA en CI/CD y mantener dependencias actualizadas.

---