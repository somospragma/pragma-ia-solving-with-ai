# Diseño de APIs y Contratos de Integración

## Paso 0: Obtención de Reglas
- Usa la herramienta getPragmaResources para obtener el recurso 'integration-api-design-rules.md' desde el servidor MCP Pragma.
- Si la obtención es exitosa, utiliza el contenido de ese recurso como base para la evaluación.
- Si la obtención falla, notifica al usuario y detén el proceso.

## PASO 1: Análisis de Especificación
- Verifica la existencia de especificaciones de API (OpenAPI/Swagger, WSDL, AsyncAPI, etc.).
- Valida que las especificaciones cumplan con estándares de la industria.
- Identifica inconsistencias entre especificación e implementación.

## PASO 2: Evaluación de Diseño RESTful/SOAP
- Para APIs REST, verifica:
  - Uso correcto de métodos HTTP (GET, POST, PUT, PATCH, DELETE)
  - Estructura de URIs siguiendo convenciones RESTful
  - Versionamiento de API (URI, header, query param)
  - Códigos de estado HTTP apropiados
  - Paginación, filtrado y ordenamiento
  - HATEOAS (si aplica)

- Para APIs SOAP, verifica:
  - Estructura de WSDL correcta
  - Uso de WS-Security
  - Manejo de faults
  - Versionamiento de schemas

## PASO 3: Validación de Contratos
- Verifica la existencia de contratos de datos (XSD, JSON Schema, Avro, etc.).
- Valida que los contratos estén versionados.
- Comprueba la compatibilidad hacia atrás (backward compatibility).
- Identifica campos obligatorios vs opcionales.

## PASO 4: Evaluación de Documentación
- Verifica que cada endpoint/operación tenga:
  - Descripción clara del propósito
  - Ejemplos de request/response
  - Códigos de error documentados
  - Requisitos de autenticación
  - Rate limits y throttling

## PASO 5: Generación de Reporte
- Genera un reporte en formato Markdown en la carpeta 'reports', nombrado 'integration_api_design_report.md'.
- El reporte debe incluir:
  - Tabla de evaluación de endpoints/operaciones
  - Análisis de cumplimiento de estándares REST/SOAP
  - Recomendaciones de mejora
  - Checklist de documentación faltante

### Ejemplo de tabla:
| Endpoint/Operación | Método | Versionado | Documentado | Contrato | Estado |
|-------------------|--------|------------|-------------|----------|--------|
| /api/v1/customers | GET | ✔️ | ✔️ | ✔️ | ✔️ |
| /api/customers/{id} | PUT | ❌ | ⚠️ | ✔️ | ⚠️ |
| CustomerService.getCustomer | SOAP | ✔️ | ❌ | ✔️ | ⚠️ |

## Paso 6: Notificación
- Notifica al desarrollador la ubicación del reporte y los principales hallazgos.

## Instrucciones
- Evalúa tanto APIs síncronas (REST/SOAP) como asíncronas (eventos, mensajería).
- Considera las mejores prácticas de la plataforma específica (IIB, OSB, MuleSoft, etc.).
- Si algún criterio no aplica, indícalo como 'N/A'.
- El reporte debe ser claro, visual y accionable para el desarrollador.
