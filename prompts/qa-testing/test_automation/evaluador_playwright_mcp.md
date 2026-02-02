# Evaluador de Reglas de Calidad MCP - Playwright Framework

## Paso 1: Obtención de Reglas
- Usa la herramienta getPragmaResources para obtener el recurso 'automation_playwright_rules.md' desde el servidor MCP Pragma.
- Si la obtención es exitosa, utiliza el contenido de ese recurso como base para la evaluación.
- Si la obtención falla, notifica al usuario y detén el proceso.

## Paso 2: Análisis Automático del Proyecto
Primero, analiza el repositorio actual para extraer automáticamente la siguiente información.

### Detección Automática de Información
1. **Analiza la estructura de directorios** del proyecto para identificar:
	- Archivos de configuración (playwright.config.ts, package.json, tsconfig.json, etc.)
	- Estructura de carpetas (tests/, pages/, utils/, fixtures/, etc.)
	- Archivos de prueba principales (.spec.ts, .test.ts)

2. **Identifica tecnologías automáticamente** examinando:
	- Archivos de dependencias npm/yarn (package.json)
	- Extensiones de archivos fuente (.ts, .js, .spec.ts)
	- Archivos de configuración de Playwright
	- Scripts de construcción y despliegue

3. **Detecta patrones arquitectónicos** observando:
	- Estructura de carpetas por funcionalidad (auth/, e2e/, api/)
	- Archivos de configuración de contenedores (Dockerfile, docker-compose.yml)
	- Configuraciones de Page Object Model
	- Archivos de configuración de browsers

4. **Extrae información de configuración** de:
	- Variables de entorno (.env, config files)
	- URLs base configuradas por ambiente
	- Configuraciones de fixtures y setup
	- Configuraciones de reportes y trazas

5. **Analiza frameworks específicos** identificando:
	- **Playwright**: playwright.config.ts, @playwright/test
	- **TypeScript**: tsconfig.json, archivos .ts
	- **Node.js**: package.json con dependencias Playwright
	- **Testing**: Page Objects, fixtures, assertions

6. **Detecta herramientas DevOps**:
	- CI/CD pipelines (.github/workflows/, .gitlab-ci.yml, Jenkinsfile)
	- Configuración de reportes (playwright-report/)
	- Docker para ejecución en CI

### Información del Proyecto (Auto-extraída)
- **Nombre del Proyecto**: [EXTRAER_DE_PACKAGE_JSON_O_README]
- **Tipo de Aplicación**: [DETECTAR_POR_ESTRUCTURA_Y_DEPENDENCIAS]
- **Tecnologías Principales**: [EXTRAER_DE_ARCHIVOS_DE_DEPENDENCIAS]
- **Framework de Testing**: [CONFIRMAR_PLAYWRIGHT_FRAMEWORK]
- **Arquitectura Base**: [INFERIR_DE_ESTRUCTURA_DE_CARPETAS]

**Luego, según el tipo de proyecto detectado:**

- Si el proyecto es de **automatización Playwright** (contiene playwright.config.ts y @playwright/test), **realiza todas las reglas de Playwright**.
- Si el proyecto **no es Playwright** (no contiene configuración Playwright), **marca como N/A** y notifica.

**Esto permite adaptar el análisis al contexto real del proyecto y evitar revisiones irrelevantes.**

## Paso 3: Evaluación del Repositorio
- Analiza el repositorio actual aplicando las reglas que sí apliquen según el paso 2 y recomendaciones extraídas del contenido real de 'automation_playwright_rules.md'.
- Para cada criterio, verifica el cumplimiento en el código y documentación del repositorio.

## Paso 4: Generación de Reporte
- Genera un reporte en formato Markdown en la carpeta 'reports', nombrado 'playwright_quality_report.md'.
- El reporte debe incluir:
  - Una tabla visual con los criterios evaluados y su estado (✔️ Cumple / ❌ No cumple / ⚠️ Parcial / N/A).
  - Recomendaciones específicas para cada criterio no cumplido.
  - Un resumen ejecutivo y pasos sugeridos para mejorar el cumplimiento.

### Ejemplo de tabla:
| Criterio | Estado | Recomendación |
|----------|--------|---------------|
| Configuración Playwright | ✔️ | - |
| Page Object Model | ❌ | Implementar POM |
| TypeScript | ⚠️ | Mejorar tipado |

## Paso 5: Notificación
- Notifica al desarrollador la ubicación del reporte y los principales hallazgos.

## Instrucciones
- No omitas ningún criterio del recurso obtenido.
- Si algún criterio no aplica, indícalo como 'N/A'.
- El reporte debe ser claro, visual y accionable para el desarrollador.