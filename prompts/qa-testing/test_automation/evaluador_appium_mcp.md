# Evaluador de Reglas de Calidad MCP - Appium Framework

## Paso 1: Obtención de Reglas
- Usa la herramienta getPragmaResources para obtener el recurso 'automation_appium_rules.md' desde el servidor MCP Pragma.
- Si la obtención es exitosa, utiliza el contenido de ese recurso como base para la evaluación.
- Si la obtención falla, notifica al usuario y detén el proceso.

## Paso 2: Análisis Automático del Proyecto
Primero, analiza el repositorio actual para extraer automáticamente la siguiente información.

### Detección Automática de Información
1. **Analiza la estructura de directorios** del proyecto para identificar:
	- Archivos de configuración (wdio.conf.js, appium.conf.js, package.json, etc.)
	- Estructura de carpetas (android/, ios/, common/, pages/, utils/, etc.)
	- Archivos de prueba principales (.spec.js, .test.js)

2. **Identifica tecnologías automáticamente** examinando:
	- Archivos de dependencias npm/yarn (package.json)
	- Extensiones de archivos fuente (.js, .spec.js)
	- Archivos de configuración de Appium/WebDriverIO
	- Scripts de construcción y despliegue

3. **Detecta patrones arquitectónicos** observando:
	- Estructura de carpetas por plataforma (android/, ios/)
	- Archivos de configuración de contenedores (Dockerfile, docker-compose.yml)
	- Configuraciones de Page Object Model para móvil
	- Archivos de configuración de capabilities

4. **Extrae información de configuración** de:
	- Variables de entorno para paths de apps
	- Capabilities configuradas por plataforma
	- Configuraciones de dispositivos y emuladores
	- Configuraciones de reportes y screenshots

5. **Analiza frameworks específicos** identificando:
	- **Appium**: wdio.conf.js, appium server configuration
	- **WebDriverIO**: @wdio/cli, webdriverio dependencies
	- **Node.js**: package.json con dependencias Appium
	- **Mobile Testing**: capabilities, page objects, gestos

6. **Detecta herramientas DevOps**:
	- CI/CD pipelines (.github/workflows/, .gitlab-ci.yml, Jenkinsfile)
	- Configuración de matriz de dispositivos
	- Manejo de artefactos móviles (APK/IPA)

### Información del Proyecto (Auto-extraída)
- **Nombre del Proyecto**: [EXTRAER_DE_PACKAGE_JSON_O_README]
- **Tipo de Aplicación**: [DETECTAR_POR_ESTRUCTURA_Y_DEPENDENCIAS]
- **Tecnologías Principales**: [EXTRAER_DE_ARCHIVOS_DE_DEPENDENCIAS]
- **Framework de Testing**: [CONFIRMAR_APPIUM_FRAMEWORK]
- **Arquitectura Base**: [INFERIR_DE_ESTRUCTURA_DE_CARPETAS]

**Luego, según el tipo de proyecto detectado:**

- Si el proyecto es de **automatización Appium** (contiene wdio.conf.js y dependencias Appium), **realiza todas las reglas de Appium**.
- Si el proyecto **no es Appium** (no contiene configuración Appium), **marca como N/A** y notifica.

**Esto permite adaptar el análisis al contexto real del proyecto y evitar revisiones irrelevantes.**

## Paso 3: Evaluación del Repositorio
- Analiza el repositorio actual aplicando las reglas que sí apliquen según el paso 2 y recomendaciones extraídas del contenido real de 'automation_appium_rules.md'.
- Para cada criterio, verifica el cumplimiento en el código y documentación del repositorio.

## Paso 4: Generación de Reporte
- Genera un reporte COMPLETAMENTE NUEVO en formato Markdown en la carpeta 'reports', nombrado 'appium_quality_report.md'.
- **IMPORTANTE**: SOBRESCRIBE cualquier reporte anterior - NO conserves información de evaluaciones previas.
- El reporte debe incluir:
  - Una tabla visual con los criterios evaluados y su estado (✔️ Cumple / ❌ No cumple / ⚠️ Parcial / N/A).
  - Recomendaciones específicas para cada criterio no cumplido.
  - Un resumen ejecutivo y pasos sugeridos para mejorar el cumplimiento.

### Ejemplo de tabla:
| Criterio | Estado | Recomendación |
|----------|--------|---------------|
| Configuración Appium | ✔️ | - |
| Separación Plataformas | ❌ | Crear carpetas android/ios |
| Page Objects Móvil | ⚠️ | Mejorar abstracción |

## Paso 5: Notificación
- Notifica al desarrollador la ubicación del reporte y los principales hallazgos.

## Instrucciones
- No omitas ningún criterio del recurso obtenido.
- Si algún criterio no aplica, indícalo como 'N/A'.
- El reporte debe ser claro, visual y accionable para el desarrollador.
- **CRITICO**: Cada evaluación debe ser INDEPENDIENTE - no uses información de reportes anteriores.
- **CRITICO**: Genera un reporte COMPLETAMENTE NUEVO basado únicamente en el estado actual del repositorio.