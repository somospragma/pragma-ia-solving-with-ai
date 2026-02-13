# Evaluador de Reglas y Buenas Prácticas para Integración

## Paso 1: Obtención de Reglas
- Usa la herramienta getPragmaResources para obtener el recurso 'integration-rules.md' desde el servidor MCP Pragma.
- Si la obtención es exitosa, utiliza el contenido de ese recurso como base para la evaluación.
- Si la obtención falla, notifica al usuario y detén el proceso.

## Paso 2: Evaluación del Proyecto de Integración
- Analiza el proyecto actual aplicando cada una de las reglas y buenas prácticas extraídas del contenido real de 'integration-rules.md'.
- Para cada criterio, verifica el cumplimiento en:
  - Estructura de flujos/servicios
  - Configuración de conectores y adaptadores
  - Manejo de errores y excepciones
  - Logging y monitoreo
  - Documentación técnica

## Paso 3: Generación de Reporte
- Genera un reporte en formato Markdown en la carpeta 'reports', nombrado 'integration_rules_report.md'.
- El reporte debe incluir:
  - Una tabla visual con los criterios evaluados y su estado (✔️ Cumple / ❌ No cumple / ⚠️ Parcial / N/A).
  - Recomendaciones específicas para cada criterio no cumplido.
  - Un resumen ejecutivo y pasos sugeridos para mejorar el cumplimiento.

### Ejemplo de tabla:
| Criterio | Estado | Recomendación |
|----------|--------|---------------|
| Estructura de Flujos | ✔️ | - |
| Manejo de Errores | ❌ | Implementar estrategia de compensación |
| Logging | ⚠️ | Estandarizar niveles de log |
| Seguridad | ❌ | Implementar autenticación OAuth2 |

## Paso 4: Notificación
- Notifica al desarrollador la ubicación del reporte y los principales hallazgos.

## Instrucciones
- No omitas ningún criterio del recurso obtenido.
- Si algún criterio no aplica, indícalo como 'N/A'.
- El reporte debe ser claro, visual y accionable para el desarrollador.
- Considera las particularidades de la plataforma de integración utilizada (IIB, OSB, MuleSoft, etc.).
