```markdown
# Instrucciones para Generar Diagrama de Software

Necesito que generes un documento completo de diagrama de arquitectura para mi proyecto de software. Utiliza la siguiente estructura y adapta el contenido según las características específicas del proyecto:

## Análisis Automático del Proyecto

Primero, analiza el repositorio actual para extraer automáticamente la siguiente información:

### Detección Automática de Información
1. **Analiza la estructura de directorios** del proyecto para identificar:
   - Archivos de configuración (package.json, pom.xml, requirements.txt, etc.)
   - Estructura de carpetas (src/, docs/, config/, etc.)

   ### 2. Diagrama C4 (PlantUML)

   Genera un diagrama en formato C4-PlantUML siguiendo el estándar C4. Utiliza el bloque PlantUML y las macros de C4 para definir los elementos arquitectónicos.

   #### Instrucciones para el Diagrama C4
   - Usa la sintaxis PlantUML con la librería C4-PlantUML.
   - El bloque debe iniciar con `@startuml` y terminar con `@enduml`.
   - Incluye la línea de importación según el nivel (Context, Container, Component):
     - `!includeurl https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml` (para diagrama de contexto)
     - O usa Container/Component según el nivel requerido.
   - Define los elementos con las macros C4: `Person`, `System`, `Container`, `Component`, etc.
   - Relaciona los elementos usando `Rel` o `Rel_D`.
   - Puedes usar colores y estilos personalizados si lo deseas, pero sigue la convención visual del estándar C4.

   #### Ejemplo Base de Diagrama C4-PlantUML
   ```plantuml
   @startuml
   !includeurl https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml

   Person(dev, "Desarrollador", "Usuario que desarrolla y mantiene el sistema")
   System_Boundary(s1, "[NOMBRE_PROYECTO]") {
     Container(web, "Frontend Web", "React", "Interfaz de usuario web")
     Container(api, "API Backend", "Node.js", "Expone servicios REST")
     ContainerDb(db, "Base de Datos", "PostgreSQL", "Almacena datos persistentes")
   }
   Rel(dev, web, "Usa")
   Rel(web, api, "Consume API")
   Rel(api, db, "Lee/Escribe")
   @enduml
   ```

   #### Capas Arquitectónicas a Incluir
   Analiza la estructura del proyecto y representa las capas como sistemas, contenedores o componentes según corresponda:

   1. **Cliente/Frontend**: Container o System
   2. **Gateway/Proxy**: Container
   3. **Servicios/API**: Container
   4. **Lógica de Negocio**: Component (si se detalla)
   5. **Datos/Persistencia**: ContainerDb
   6. **Infraestructura**: Container o System externo
   7. **Recursos Externos**: System_Ext

   **INSTRUCCIÓN**: Extrae y representa automáticamente los elementos y relaciones detectados en el análisis del proyecto.

   Puedes consultar la documentación oficial de C4-PlantUML aquí: https://github.com/plantuml-stdlib/C4-PlantUML
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