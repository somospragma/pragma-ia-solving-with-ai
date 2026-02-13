# Creación de Servicios de Integración

## Paso 0: Obtención de Reglas
- Usa la herramienta getPragmaResources para obtener los recursos: 'i1-architecture.md', 'i2-error-handling.md', 'i3-security.md', 'i4-performance.md', 'i5-logging.md', 'i6-data-transformation.md', 'i7-connectivity.md', 'i8-versioning.md', 'i9-documentation.md', 'i10-testing.md' desde el servidor MCP Pragma.
- Si la obtención es exitosa, utiliza el contenido de ese recurso como base para la evaluación.
- Si la obtención falla, notifica al usuario y detén el proceso.

## PASO 1 — Generar PLAN DE EJECUCIÓN
- Siempre genera un plan inicialmente antes de realizar cualquier otra acción.
- Genera un PLAN con estas características:

A. El plan debe incluir 10 pasos para analizar el proyecto siguiendo los siguientes rulesets en orden:
- i1-architecture.md
- i2-error-handling.md
- i3-security.md
- i4-performance.md
- i5-logging.md
- i6-data-transformation.md
- i7-connectivity.md
- i8-versioning.md
- i9-documentation.md
- i10-testing.md

B. Para cada paso del plan incluye:
- step o número del paso actual (1 al 10)
- ruleset_name (ej: "I3 - Seguridad en Integración")
- file_name (ej: "i3-security.md")
- ámbitos de análisis (ej: flows/**, services/**, configurations/**)
- qué verificará ese ruleset en forma resumida
- severidades esperadas (CRITICAL/HIGH/MEDIUM/LOW)
- dependencias o prerequisitos si existen

C. El agente debe **detenerse después de generar el plan** y esperar instrucciones del usuario para comenzar el análisis con todos los ruleset:
- "Empezar"
- "Cancelar"

## Paso 2: Evaluación del Servicio de Integración
- Analiza el servicio actual aplicando cada una de las reglas y buenas prácticas extraídas del contenido real de cada .md obtenido.
- Para cada criterio, verifica el cumplimiento en:
  - Código y flujos de integración
  - Configuración de conectores y adaptadores
  - Documentación del servicio
  - Políticas de seguridad y manejo de errores
- Considera la totalidad de las reglas de cada .md a evaluar.
- Evalúa según la plataforma de integración utilizada (IIB, OSB, MuleSoft, etc.).

## Paso 3: Generación de Reporte
- Si no existe, genera un reporte en formato Markdown en la carpeta 'reports', nombrado 'integration_service_rules_report.md'.
- Si existe, agrega los resultados adicionales en el mismo.
- El reporte debe incluir:
  - Una tabla visual con los criterios evaluados y su estado (✔️ Cumple / ❌ No cumple / ⚠️ Parcial / N/A).
  - Recomendaciones específicas para cada criterio no cumplido.
  - Un resumen ejecutivo y pasos sugeridos para mejorar el cumplimiento.

### Ejemplo de tabla:
| Criterio | Estado | Recomendación |
|----------|--------|---------------|
| Arquitectura de Flujos | ✔️ | - |
| Manejo de Errores | ❌ | Implementar try-catch en todos los nodos críticos |
| Seguridad | ⚠️ | Agregar validación de tokens |

## Paso 4: Notificación
- Notifica al desarrollador la ubicación del reporte y los principales hallazgos.

## Instrucciones
- No omitas ningún criterio del recurso obtenido.
- Si algún criterio no aplica, indícalo como 'N/A'.
- No agregues al contexto cualquier reporte previo existente, siempre aplica todo de nuevo.
- Siempre genera un nuevo reporte completo, sin importar si ya existe uno previo.
- El reporte debe ser claro, visual y accionable para el desarrollador.
