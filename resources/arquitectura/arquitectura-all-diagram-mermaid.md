```markdown
# Instrucciones para Generar Diagrama de Software

Necesito que generes un documento completo de diagrama de arquitectura para mi proyecto de software. Utiliza la siguiente estructura y adapta el contenido según las características específicas del proyecto:

## Análisis Automático del Proyecto

Primero, analiza el repositorio actual para extraer automáticamente la siguiente información:

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

## Estructura del Documento Requerida

### 1. Título y Introducción
- Título descriptivo con el nombre del proyecto
- Sección de vista interactiva con instrucciones para Mermaid Preview
- Incluir captura de pantalla si está disponible
- Enlaces a herramientas de edición (Mermaid Live Editor)

### 2. Diagrama Mermaid
Genera un diagrama Mermaid con las siguientes características:

#### Configuración de Tema Dark (Obligatoria)
    ```mermaid
    %%{init: {
        'theme': 'dark',
        'themeVariables': {
            'background': '#181a20',
            'primaryColor': '#2c3e50',
            'primaryTextColor': '#ffffff',
            'primaryBorderColor': '#3498db',
            'lineColor': '#3498db',
            'edgeLabelBackground':'#2c3e50',
            'nodeTextColor':'#ffffff',
            'fontSize': '16px',
            'fontFamily': 'Arial, sans-serif'
        },
        'flowchart': {
            'nodeSpacing': 80,
            'rankSpacing': 120,
            'curve': 'basis',
            'padding': 20,
            'useMaxWidth': false,
            'htmlLabels': false
        }
    }}%%
    ```

#### Capas Arquitectónicas a Incluir
Organiza los componentes en subgrafos según estas capas típicas (adapta según el análisis del proyecto):

**INSTRUCCIÓN**: Analiza la estructura del proyecto actual para determinar qué capas están presentes:

1. **Capa de Cliente/Frontend** (si existe src/frontend, public/, componentes React/Vue/Angular)
   - Aplicaciones cliente detectadas
   - Interfaces de usuario encontradas
   - Aplicaciones móviles/web identificadas

2. **Capa de Gateway/Proxy** (si existe nginx.conf, traefik.yml, API Gateway configs)
   - Load balancers configurados
   - API Gateways detectados
   - Reverse proxies encontrados

3. **Capa de Servicios/API** (archivo principal del servidor, routes/, controllers/)
   - Servicios principales identificados
   - APIs REST/GraphQL detectadas
   - Microservicios encontrados

4. **Capa de Lógica de Negocio** (business/, services/, modules/, commons/)
   - Módulos core detectados
   - Procesadores identificados
   - Manejadores de eventos encontrados

5. **Capa de Datos/Persistencia** (models/, database/, config/db)
   - Bases de datos configuradas
   - Cachés detectados
   - Almacenamiento de archivos identificado

6. **Capa de Infraestructura** (logging/, monitoring/, config/)
   - Servicios de monitoreo configurados
   - Logging implementado
   - Configuración detectada

7. **Recursos Externos** (external/, integrations/, third-party configs)
   - APIs externas configuradas
   - Servicios de terceros detectados
   - Sistemas heredados identificados

#### Estilos de Colores
Incluye definiciones de estilos con colores distintivos para cada capa:

classDef cliente fill:#34495e,stroke:#3498db,stroke-width:3px,color:#ffffff
classDef gateway fill:#2c3e50,stroke:#e74c3c,stroke-width:3px,color:#ffffff
classDef servicios fill:#27ae60,stroke:#2ecc71,stroke-width:3px,color:#ffffff
classDef negocio fill:#e67e22,stroke:#f39c12,stroke-width:3px,color:#ffffff
classDef datos fill:#8e44ad,stroke:#9b59b6,stroke-width:3px,color:#ffffff
classDef infraestructura fill:#16a085,stroke:#1abc9c,stroke-width:3px,color:#ffffff
classDef externos fill:#f39c12,stroke:#f1c40f,stroke-width:3px,color:#000000

### 3. Detalles de Componentes (Auto-generados)
Para cada capa identificada en el análisis, incluye:

**INSTRUCCIÓN**: Extrae esta información automáticamente del código y configuraciones:

#### [Nombre de Capa Detectada] (Ej: Capa de Servicios identificada en src/)
- **Componente Principal**: [EXTRAER_DE_ARCHIVO_PRINCIPAL_O_MAIN]
- **Tecnología/Framework**: [DETECTAR_DE_IMPORTS_Y_DEPENDENCIAS]
- **Puerto/Endpoint**: [BUSCAR_EN_CONFIGS_SERVER_Y_ENV]
- **Características Clave**: [ANALIZAR_FUNCIONALIDADES_DEL_CODIGO]

### 4. Flujo de Datos (Basado en Análisis)
**INSTRUCCIÓN**: Analiza el flujo real del código para generar esta secuencia:

1. **[Paso extraído del entry point]**: [ANALIZAR_PUNTO_DE_ENTRADA]
2. **[Paso identificado en middleware/routes]**: [EXAMINAR_ROUTES_Y_MIDDLEWARE]
3. **[Paso detectado en business logic]**: [ANALIZAR_SERVICIOS_Y_LOGICA]
4. **[Paso encontrado en data layer]**: [EXAMINAR_ACCESO_A_DATOS]
5. **[Paso identificado en response]**: [ANALIZAR_FORMATO_RESPUESTA]

### 5. Características Clave del Sistema (Auto-detectadas)
**INSTRUCCIÓN**: Identifica estas características analizando el proyecto:

- **[Característica de Seguridad]**: [BUSCAR_AUTH_MIDDLEWARE_ENCRYPTION]
- **[Patrón de Diseño]**: [IDENTIFICAR_PATRONES_EN_ESTRUCTURA]
- **[Escalabilidad]**: [ANALIZAR_CONFIGS_DOCKER_CLUSTER]
- **[Performance]**: [DETECTAR_CACHE_OPTIMIZATION]
- **[Reliability]**: [BUSCAR_ERROR_HANDLING_LOGGING]

## Consideraciones Específicas (Auto-extraídas)
**INSTRUCCIÓN**: Extrae automáticamente del análisis del proyecto:

- **Seguridad**: [ANALIZAR_ARCHIVOS_AUTH_SECURITY_MIDDLEWARE]
- **Patrones de Diseño**: [IDENTIFICAR_EN_ESTRUCTURA_Y_CODIGO]
- **Escalabilidad**: [EXAMINAR_DOCKER_KUBERNETES_CONFIGS]
- **Deployment**: [ANALIZAR_CI_CD_SCRIPTS_DOCKERFILES]
- **Performance**: [DETECTAR_CACHING_OPTIMIZATION_CONFIGS]

## Salida Esperada
Genera un archivo Markdown completo que incluya:
1. Todas las secciones mencionadas
2. Un diagrama Mermaid funcional y visualmente atractivo
3. Descripciones técnicas precisas
4. Flujos de datos claros
5. Documentación que sirva tanto para desarrolladores como para stakeholders técnicos

## Información Adicional del Proyecto (Auto-detectada)
**INSTRUCCIÓN**: Analiza el proyecto actual para identificar automáticamente:

- **Módulos Especiales**: [ESCANEAR_CARPETAS_PERSONALIZADAS_Y_PLUGINS]
- **Integraciones Únicas**: [EXAMINAR_THIRD_PARTY_CONFIGS_Y_APIS]
- **Requisitos de Seguridad**: [ANALIZAR_AUTH_CONFIGS_Y_CERTIFICATES]
- **Configuraciones Especiales**: [REVISAR_ENV_FILES_Y_CONFIGS_CUSTOM]
- **Patrones Específicos**: [IDENTIFICAR_PATTERNS_ÚNICOS_DEL_PROYECTO]

```