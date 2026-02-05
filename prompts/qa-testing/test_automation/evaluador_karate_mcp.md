# Evaluador de Reglas de Calidad MCP - Karate Framework

## Paso 1: Obtención de Reglas
- Usa la herramienta getPragmaResources para obtener el recurso 'automation_karate_rules.md' desde el servidor MCP Pragma.
- Si la obtención es exitosa, utiliza el contenido de ese recurso como base para la evaluación.
- Si la obtención falla, notifica al usuario y detén el proceso.

## Paso 2: Análisis Automático del Proyecto
Primero, analiza el repositorio actual para extraer automáticamente la siguiente información.

### Detección Automática de Información
1. **Analiza la estructura de directorios** del proyecto para identificar:
	- Archivos de configuración (karate-config.js, pom.xml, build.gradle, etc.)
	- Estructura de carpetas (features/, data/, utils/, classpath:, etc.)
	- Archivos .feature principales

2. **Identifica tecnologías automáticamente** examinando:
	- Archivos de dependencias Maven/Gradle
	- Extensiones de archivos fuente (.feature, .js)
	- Archivos de configuración de Karate
	- Scripts de construcción y despliegue

3. **Detecta patrones arquitectónicos** observando:
	- Estructura de carpetas por funcionalidad
	- Archivos de configuración de ambientes
	- Configuraciones de API (karate-config.js)
	- Archivos de configuración de logging

4. **Extrae información de configuración** de:
	- Variables de entorno en karate-config.js
	- URLs base configuradas por ambiente
	- Configuraciones de autenticación
	- Configuraciones de timeouts

5. **Analiza frameworks específicos** identificando:
	- **Karate**: karate-config.js, archivos .feature, funciones JavaScript
	- **Maven**: pom.xml con dependencias karate-core
	- **Gradle**: build.gradle con dependencias Karate
	- **Testing**: Scenarios, Background, Examples

6. **Detecta herramientas DevOps**:
	- CI/CD pipelines (.github/workflows/, .gitlab-ci.yml, Jenkinsfile)
	- Configuración de reportes (target/karate-reports/)
	- Tags para ejecución selectiva (@smoke, @regression)

### Información del Proyecto (Auto-extraída)
- **Nombre del Proyecto**: [EXTRAER_DE_POM_XML_O_README]
- **Tipo de Aplicación**: [DETECTAR_POR_ESTRUCTURA_Y_DEPENDENCIAS]
- **Tecnologías Principales**: [EXTRAER_DE_ARCHIVOS_DE_DEPENDENCIAS]
- **Framework de Testing**: [CONFIRMAR_KARATE_FRAMEWORK]
- **Arquitectura Base**: [INFERIR_DE_ESTRUCTURA_DE_CARPETAS]

**Luego, según el tipo de proyecto detectado:**

- Si el proyecto es de **automatización Karate** (contiene karate-config.js y archivos .feature), **realiza todas las reglas de Karate**.
- Si el proyecto **no es Karate** (no contiene configuración Karate), **marca como N/A** y notifica.

**Esto permite adaptar el análisis al contexto real del proyecto y evitar revisiones irrelevantes.**

## Paso 3: Evaluación del Repositorio
- Analiza el repositorio actual aplicando las reglas que sí apliquen según el paso 2 y recomendaciones extraídas del contenido real de 'automation_karate_rules.md'.
- Para cada criterio, verifica el cumplimiento en el código y documentación del repositorio.

## Paso 4: Generación de Reporte
- Genera un reporte COMPLETAMENTE NUEVO en formato Markdown en la carpeta 'reports', nombrado 'karate_quality_report.md'.
- **IMPORTANTE**: SOBRESCRIBE cualquier reporte anterior - NO conserves información de evaluaciones previas.
- El reporte debe incluir:
  - Una tabla visual con los criterios evaluados y su estado (✔️ Cumple / ❌ No cumple / ⚠️ Parcial / N/A).
  - Recomendaciones específicas para cada criterio no cumplido.
  - Un resumen ejecutivo y pasos sugeridos para mejorar el cumplimiento.

### Ejemplo de tabla:
| Criterio | Estado | Recomendación |
|----------|--------|---------------|
| Configuración Karate | ✔️ | - |
| Organización Features | ❌ | Separar por funcionalidad |
| Validaciones API | ⚠️ | Agregar validaciones de schema |

## Paso 5: Notificación
- Notifica al desarrollador la ubicación del reporte y los principales hallazgos.

## Instrucciones
- No omitas ningún criterio del recurso obtenido.
- Si algún criterio no aplica, indícalo como 'N/A'.
- El reporte debe ser claro, visual y accionable para el desarrollador.
- **CRITICO**: Cada evaluación debe ser INDEPENDIENTE - no uses información de reportes anteriores.
- **CRITICO**: Genera un reporte COMPLETAMENTE NUEVO basado únicamente en el estado actual del repositorio.