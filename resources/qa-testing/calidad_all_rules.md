# Evaluador de Reglas Transversales de Calidad de Software

## Paso 1: Obtención de Reglas
- Usa la herramienta getPragmaResources para obtener el recurso 'calidad-all-rules.md' desde el servidor MCP Pragma.
- Si la obtención es exitosa, utiliza el contenido de ese recurso como base para la evaluación.
- Si la obtención falla, notifica al usuario y detén el proceso.

## Paso 2: 1. Análisis Automático del Proyecto
Primero, analiza el repositorio actual para extraer automáticamente la siguiente información.

### Detección Automática de Información
1. **Analiza la estructura de directorios** del proyecto para identificar:
	- Archivos de configuración (package.json, pom.xml, requirements.txt, etc.)
	- Estructura de carpetas (src/, docs/, config/, etc.)
	- Archivos de entrada principales

2. **Identifica tecnologías automáticamente** examinando:
	- Archivos de dependencias y gestores de paquetes
	- Extensiones de archivos fuente
	- Archivos de configuración de frameworks
	- Scripts de construcción y despliegue

3. **Detecta patrones arquitectónicos** observando:
	- Estructura de carpetas (microservicios vs monolítica)
	- Archivos de configuración de contenedores (Dockerfile, docker-compose.yml)
	- Configuraciones de API (OpenAPI/Swagger)
	- Archivos de configuración de servidores

4. **Extrae información de configuración** de:
	- Variables de entorno (.env, config files)
	- Puertos configurados en servidores
	- Endpoints definidos en código
	- Configuraciones de base de datos

5. **Analiza frameworks específicos** identificando:
	- **Python**: Django (manage.py), Flask (app.py), FastAPI (main.py)
	- **JavaScript/TypeScript**: React (src/App.js), Angular (angular.json), Vue (vue.config.js)
	- **Java**: Spring Boot (application.properties), Quarkus, Micronaut
	- **IaC**: Terraform (*.tf), CloudFormation (*.yaml con AWSTemplateFormatVersion)

6. **Detecta herramientas DevOps**:
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

- Si el proyecto es un **arquetipo**  (por ejemplo, contiene principalmente archivos de IaC como Terraform, CloudFormation, ARM, etc.), **realiza el 3: Control de Acceso (ACL) en Recursos Críticos de Red**.
- Si el proyecto **productivo** (aplicaciones, servicios, etc.), **realiza** (2, 4, 5 y 6) y omite la Regla 3.

**Esto permite adaptar el análisis de seguridad al contexto real del proyecto y evitar revisiones irrelevantes.**

## Paso 3: Evaluación del Repositorio
- Analiza el repositorio actual aplicando las reglas que si apliquen segun el paso 2 y recomendaciones extraídas del contenido real de 'calidad-all-rules.md'.
- Para cada criterio, verifica el cumplimiento en el código y documentación del repositorio.

## Paso 4: Generación de Reporte
- Genera un reporte en formato Markdown en la carpeta 'reports', nombrado 'calidad_all_rules_report.md'.
- El reporte debe incluir:
  - Una tabla visual con los criterios evaluados y su estado (✔️ Cumple / ❌ No cumple / ⚠️ Parcial / N/A).
  - Recomendaciones específicas para cada criterio no cumplido.
  - Un resumen ejecutivo y pasos sugeridos para mejorar el cumplimiento.

### Ejemplo de tabla:
| Criterio | Estado | Recomendación |
|----------|--------|---------------|
| Cobertura de Pruebas | ✔️ | - |
| Documentación | ❌ | Actualizar README y comentarios |
| Integración Continua | ⚠️ | Configurar pipeline básico |

## Paso 5: Notificación
- Notifica al desarrollador la ubicación del reporte y los principales hallazgos.

## Instrucciones
- No omitas ningún criterio del recurso obtenido.
- Si algún criterio no aplica, indícalo como 'N/A'.
- El reporte debe ser claro, visual y accionable para el desarrollador.