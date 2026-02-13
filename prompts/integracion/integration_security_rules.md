# Evaluador de Reglas y Buenas Prácticas de Seguridad para Integración

## Paso 0: Obtención de Reglas
- Usa la herramienta getPragmaResources para obtener los recursos: 'integration-security-i1.md', 'integration-security-i2.md', 'integration-security-i3.md', 'integration-security-i4.md', 'integration-security-i5.md', 'integration-security-i6.md', 'integration-security-i7.md', 'integration-security-i8.md', 'integration-security-i9.md', 'integration-security-i10.md' desde el servidor MCP Pragma.
- Si la obtención es exitosa, utiliza el contenido de ese recurso como base para la evaluación.
- Si la obtención falla, notifica al usuario y detén el proceso.

## PASO 1 — Generar PLAN DE EJECUCIÓN
- Siempre genera un plan inicialmente antes de realizar cualquier otra acción.
- Genera un PLAN con estas características:

A. El plan debe incluir 10 pasos para analizar el proyecto siguiendo los siguientes rulesets en orden:
- integration-security-i1.md (Autenticación y Autorización)
- integration-security-i2.md (Cifrado de Datos)
- integration-security-i3.md (Gestión de Credenciales)
- integration-security-i4.md (Validación de Entrada)
- integration-security-i5.md (Protección de APIs)
- integration-security-i6.md (Auditoría y Trazabilidad)
- integration-security-i7.md (Gestión de Certificados)
- integration-security-i8.md (Prevención de Inyección)
- integration-security-i9.md (Control de Acceso)
- integration-security-i10.md (Configuración Segura)

B. Para cada paso del plan incluye:
- step o número del paso actual (1 al 10)
- ruleset_name (ej: "I3 - Gestión de Credenciales")
- file_name (ej: "integration-security-i3.md")
- ámbitos de análisis (ej: flows/**, policies/**, configurations/**)
- qué verificará ese ruleset en forma resumida
- severidades esperadas (CRITICAL/HIGH/MEDIUM/LOW)
- dependencias o prerequisitos si existen

C. El agente debe **detenerse después de generar el plan** y esperar instrucciones del usuario para comenzar el análisis con todos los ruleset:
- "Empezar"
- "Cancelar"

## Paso 2: Evaluación del Proyecto de Integración
- Analiza el proyecto actual aplicando cada una de las reglas y buenas prácticas extraídas del contenido real de cada .md obtenido.
- Para cada criterio, verifica el cumplimiento en:
  - Flujos y servicios de integración
  - Configuración de seguridad (autenticación, autorización, cifrado)
  - Políticas de seguridad aplicadas
  - Gestión de credenciales y certificados
  - Validación de entrada y protección de APIs
- Considera la totalidad de las reglas de cada .md a evaluar.
- Evalúa según la plataforma de integración utilizada (IIB, OSB, MuleSoft, etc.).

## Paso 3: Generación de Reporte
- Si no existe, genera un reporte en formato Markdown en la carpeta 'reports', nombrado 'integration_security_rules_report.md'.
- Si existe, agrega los resultados adicionales en el mismo.
- El reporte debe incluir:
  - Una tabla visual con los criterios evaluados y su estado (✔️ Cumple / ❌ No cumple / ⚠️ Parcial / N/A).
  - Recomendaciones específicas para cada criterio no cumplido.
  - Un resumen ejecutivo y pasos sugeridos para mejorar el cumplimiento.

### Ejemplo de tabla:
| Criterio | Estado | Severidad | Recomendación |
|----------|--------|-----------|---------------|
| Autenticación OAuth2 | ✔️ | HIGH | - |
| Cifrado TLS 1.2+ | ❌ | CRITICAL | Actualizar a TLS 1.3 |
| Gestión de Secrets | ⚠️ | HIGH | Migrar a Vault o AWS Secrets Manager |
| Validación de XML/JSON | ❌ | MEDIUM | Implementar schemas de validación |

## Paso 4: Notificación
- Notifica al desarrollador la ubicación del reporte y los principales hallazgos.

## Instrucciones
- No omitas ningún criterio del recurso obtenido.
- Si algún criterio no aplica, indícalo como 'N/A'.
- No agregues al contexto cualquier reporte previo existente, siempre aplica todo de nuevo.
- Siempre genera un nuevo reporte completo, sin importar si ya existe uno previo.
- El reporte debe ser claro, visual y accionable para el desarrollador.
- Prioriza hallazgos de severidad CRITICAL y HIGH.
