# Evaluador de Rendimiento y Optimización para Integración

## Paso 0: Obtención de Reglas
- Usa la herramienta getPragmaResources para obtener el recurso 'integration-performance-rules.md' desde el servidor MCP Pragma.
- Si la obtención es exitosa, utiliza el contenido de ese recurso como base para la evaluación.
- Si la obtención falla, notifica al usuario y detén el proceso.

## PASO 1: Generación de Plan de Análisis
- Genera un plan de análisis de rendimiento que incluya:
  - Componentes a evaluar (APIs, flujos, transformaciones, conectores)
  - Métricas objetivo por componente
  - Herramientas de medición a utilizar
  - Criterios de éxito (SLAs, SLOs)
- El agente debe presentar el plan y esperar confirmación del usuario antes de continuar.

## PASO 2: Análisis de Patrones de Rendimiento
- Identifica patrones que afectan el rendimiento:
  - Llamadas síncronas vs asíncronas
  - Uso de caché
  - Pooling de conexiones
  - Procesamiento por lotes (batch)
  - Paralelización de flujos
  - Uso de circuit breakers

## PASO 3: Evaluación de Transformaciones
- Analiza las transformaciones de datos:
  - Complejidad de mapeos XSLT/DataWeave/JSONata
  - Uso de transformaciones nativas vs custom
  - Tamaño de mensajes procesados
  - Transformaciones innecesarias o redundantes
  - Uso de streaming para mensajes grandes

## PASO 4: Análisis de Conectividad
- Evalúa la configuración de conectores:
  - Timeouts configurados apropiadamente
  - Connection pooling habilitado
  - Retry policies definidas
  - Uso de keep-alive
  - Compresión de datos habilitada

## PASO 5: Evaluación de Recursos
- Verifica el uso eficiente de recursos:
  - Gestión de memoria (memory leaks)
  - Uso de threads/workers
  - Manejo de transacciones
  - Liberación de recursos (conexiones, streams)
  - Configuración de heap/stack

## PASO 6: Análisis de Monitoreo
- Verifica la existencia de métricas de rendimiento:
  - Tiempo de respuesta por operación
  - Throughput (mensajes/segundo)
  - Tasa de errores
  - Uso de CPU/memoria
  - Latencia de red

## PASO 7: Generación de Reporte
- Genera un reporte en formato Markdown en la carpeta 'reports', nombrado 'integration_performance_report.md'.
- El reporte debe incluir:
  - Tabla de evaluación de rendimiento
  - Identificación de cuellos de botella
  - Recomendaciones de optimización priorizadas
  - Métricas actuales vs esperadas

### Ejemplo de tabla:
| Componente | Métrica | Valor Actual | Valor Esperado | Estado | Prioridad |
|------------|---------|--------------|----------------|--------|-----------|
| API Gateway | Latencia | 250ms | <100ms | ⚠️ | HIGH |
| Transform Flow | Throughput | 50 msg/s | 100 msg/s | ❌ | CRITICAL |
| DB Connector | Pool Size | 5 | 20 | ⚠️ | MEDIUM |
| Cache Hit Rate | % | 45% | >80% | ❌ | HIGH |

## Paso 8: Notificación
- Notifica al desarrollador la ubicación del reporte y los principales hallazgos.
- Prioriza recomendaciones por impacto en rendimiento.

## Instrucciones
- No omitas ningún criterio del recurso obtenido.
- Si algún criterio no aplica, indícalo como 'N/A'.
- Incluye recomendaciones específicas de la plataforma (IIB, OSB, MuleSoft, etc.).
- El reporte debe ser claro, visual y accionable para el desarrollador.
- Considera el contexto de carga esperada (volumen de transacciones).
