# I1 - Arquitectura de Integración

## Descripción
Este ruleset evalúa la arquitectura y estructura de los servicios de integración, asegurando que sigan patrones establecidos y mejores prácticas de diseño.

## Severidad: HIGH

## Reglas

### 1.1 Separación de Responsabilidades
**Severidad**: HIGH

**Descripción**: Los flujos deben estar organizados en capas claramente definidas.

**Criterios**:
- ✅ Capa de exposición (APIs, endpoints)
- ✅ Capa de orquestación (lógica de negocio)
- ✅ Capa de transformación (mapeos de datos)
- ✅ Capa de conectividad (adaptadores, conectores)

**Ejemplo Correcto**:
```
/flows
  /exposure
    - customer-api.xml
  /orchestration
    - customer-orchestration.xml
  /transformation
    - customer-transform.xsl
  /connectivity
    - database-connector.xml
```

**Ejemplo Incorrecto**:
```
/flows
  - customer-everything.xml (todo mezclado)
```

---

### 1.2 Modularización
**Severidad**: MEDIUM

**Descripción**: Flujos complejos deben dividirse en subprocesos reutilizables.

**Criterios**:
- ✅ Flujos no exceden 200 líneas de código
- ✅ Lógica repetida está en subprocesos
- ✅ Subprocesos tienen responsabilidad única
- ✅ Interfaces claras entre módulos

**Beneficios**:
- Facilita mantenimiento
- Mejora testabilidad
- Permite reutilización

---

### 1.3 Nomenclatura Consistente
**Severidad**: MEDIUM

**Descripción**: Todos los artefactos siguen convenciones de nombres establecidas.

**Criterios**:
- ✅ Formato: `{dominio}-{accion}-{tipo}.{ext}`
- ✅ Ejemplos:
  - `customer-create-api.xml`
  - `order-process-orchestration.xml`
  - `payment-transform.xsl`
- ✅ Sin espacios ni caracteres especiales
- ✅ Lowercase con guiones

---

### 1.4 Versionamiento de Servicios
**Severidad**: HIGH

**Descripción**: Servicios y APIs deben incluir versión explícita.

**Criterios**:
- ✅ Versión en URI: `/api/v1/customers`
- ✅ Versión en nombre de servicio: `CustomerServiceV1`
- ✅ Documentación de cambios entre versiones
- ✅ Estrategia de deprecación definida

---

### 1.5 Patrones de Integración
**Severidad**: HIGH

**Descripción**: Usar patrones de integración empresarial apropiados.

**Patrones Recomendados**:
- **Request-Reply**: Para operaciones síncronas
- **Fire-and-Forget**: Para notificaciones
- **Publish-Subscribe**: Para eventos
- **Message Router**: Para enrutamiento condicional
- **Content Enricher**: Para enriquecer mensajes
- **Splitter/Aggregator**: Para procesamiento por lotes

**Criterios**:
- ✅ Patrón apropiado para el caso de uso
- ✅ Documentación del patrón utilizado
- ✅ Implementación consistente

---

### 1.6 Gestión de Configuración
**Severidad**: CRITICAL

**Descripción**: Configuración separada de lógica de negocio.

**Criterios**:
- ✅ Archivos de propiedades por ambiente
- ✅ No hardcodear URLs, credenciales, timeouts
- ✅ Usar variables de entorno o gestores de configuración
- ✅ Configuración centralizada (Spring Cloud Config, Consul, etc.)

**Ejemplo**:
```properties
# dev.properties
api.endpoint=https://dev.api.example.com
api.timeout=5000

# prod.properties
api.endpoint=https://api.example.com
api.timeout=3000
```

---

### 1.7 Contratos de Servicio
**Severidad**: HIGH

**Descripción**: Todos los servicios deben tener contratos definidos.

**Criterios**:
- ✅ OpenAPI/Swagger para REST
- ✅ WSDL para SOAP
- ✅ AsyncAPI para eventos
- ✅ Schemas de validación (JSON Schema, XSD)
- ✅ Contratos versionados

---

### 1.8 Idempotencia
**Severidad**: HIGH

**Descripción**: Operaciones críticas deben ser idempotentes.

**Criterios**:
- ✅ GET, PUT, DELETE son idempotentes por diseño
- ✅ POST usa idempotency keys cuando es necesario
- ✅ Validación de operaciones duplicadas
- ✅ Documentación de comportamiento idempotente

---

### 1.9 Stateless vs Stateful
**Severidad**: MEDIUM

**Descripción**: Preferir diseños stateless cuando sea posible.

**Criterios**:
- ✅ Servicios no mantienen estado de sesión
- ✅ Estado necesario se pasa en cada request
- ✅ Si se requiere estado, usar almacenamiento externo (Redis, DB)
- ✅ Facilita escalabilidad horizontal

---

### 1.10 Dependency Management
**Severidad**: MEDIUM

**Descripción**: Gestionar dependencias entre servicios apropiadamente.

**Criterios**:
- ✅ Minimizar acoplamiento entre servicios
- ✅ Usar service discovery cuando sea apropiado
- ✅ Implementar circuit breakers para dependencias externas
- ✅ Documentar dependencias en diagramas

---

### 1.11 API Gateway Pattern
**Severidad**: MEDIUM

**Descripción**: Usar API Gateway para exponer servicios.

**Beneficios**:
- Punto único de entrada
- Autenticación/autorización centralizada
- Rate limiting
- Transformación de requests/responses
- Routing y load balancing

**Criterios**:
- ✅ Gateway implementado (Kong, Apigee, AWS API Gateway, etc.)
- ✅ Políticas de seguridad aplicadas
- ✅ Monitoreo centralizado

---

### 1.12 Event-Driven Architecture
**Severidad**: MEDIUM

**Descripción**: Para sistemas desacoplados, considerar arquitectura basada en eventos.

**Criterios**:
- ✅ Usar message brokers (Kafka, RabbitMQ, AWS SNS/SQS)
- ✅ Eventos bien definidos con schemas
- ✅ Idempotencia en consumidores
- ✅ Dead letter queues para errores

---

## Checklist de Evaluación

| ID | Criterio | Cumple | Observaciones |
|----|----------|--------|---------------|
| 1.1 | Separación de responsabilidades | ⬜ | |
| 1.2 | Modularización | ⬜ | |
| 1.3 | Nomenclatura consistente | ⬜ | |
| 1.4 | Versionamiento | ⬜ | |
| 1.5 | Patrones de integración | ⬜ | |
| 1.6 | Gestión de configuración | ⬜ | |
| 1.7 | Contratos de servicio | ⬜ | |
| 1.8 | Idempotencia | ⬜ | |
| 1.9 | Stateless design | ⬜ | |
| 1.10 | Dependency management | ⬜ | |
| 1.11 | API Gateway | ⬜ | |
| 1.12 | Event-driven architecture | ⬜ | |

## Recomendaciones

1. Revisar estructura de carpetas y reorganizar si es necesario
2. Refactorizar flujos monolíticos en módulos más pequeños
3. Estandarizar nomenclatura en todo el proyecto
4. Implementar versionamiento explícito
5. Documentar patrones de integración utilizados
6. Externalizar toda la configuración
7. Crear/actualizar contratos de servicio
