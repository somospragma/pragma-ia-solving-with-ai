1. Fundamentos de Oracle Service Bus 12c

Explícame Oracle Service Bus 12c como si fuera un lenguaje de integración declarativo.
Describe Proxy Services, Pipelines, Business Services y Message Context,
pensando en qué responsabilidades tendría cada uno en una arquitectura Java moderna.

---
2. Proxy Services → APIs Java


Dado un Proxy Service de OSB 12c,
explícame cómo convertirlo en una API Java 21.

Incluye:
- Contrato (OpenAPI o equivalente)
- Endpoint REST
- Validación de entrada
- Manejo de errores

---
3. Pipelines y Message Flow → Application Services

Explícame cómo un Pipeline de OSB 12c
(secuencias, branches, stages, error handlers)
se traduce a capas de aplicación en Java 21.

Usa un enfoque de clean architecture o hexagonal.

---
4. Service Callouts y Routing → Clients y Orquestación

¿Cómo se reemplaza un Service Callout de OSB 12c
por código Java 21?

Incluye:
- HTTP clients
- Timeouts y retries
- Ruteo condicional
- Buenas prácticas modernas

---
5. Transformaciones (XQuery / XSLT) → Java Mapping

Explícame cómo migrar transformaciones XQuery/XSLT
de OSB 12c a Java 21.

Propón:
- Estructura de mappers
- Uso de librerías modernas
- Estrategias de validación

---
6. Java Callouts → Código reutilizable

Explícame cómo funcionan los Java Callouts en OSB 12c
y cómo extraer esa lógica para reutilizarla
en una arquitectura Java 21 independiente.

---
7. Manejo de errores y fault policies
¿Cómo se migran los error handlers y fault policies
de OSB 12c a Java 21?

Incluye:
- Excepciones
- Respuestas estandarizadas
- Observabilidad

---
8. Seguridad (Policies → Código / Infra)

Explícame cómo migrar políticas de seguridad de OSB 12c
(auth, authz, certificados, headers)
a una arquitectura Java 21 moderna.


---
9. JMS / Async → Mensajería moderna

¿Cómo se reemplaza el uso de JMS en OSB 12c
por mecanismos modernos en Java 21?

Incluye patrones y decisiones arquitectónicas.

---
10. Estructura final del código Java 21

Propón una estructura de proyecto Java 21
para reemplazar un conjunto de Proxy Services de OSB 12c.

Incluye paquetes, responsabilidades y buenas prácticas.

---
11. Estrategia de migración por oleadas

Ayúdame a definir una estrategia de migración por oleadas
desde OSB 12c a Java 21,
identificando quick wins, riesgos y criterios de priorización.


---
12. Checklist de salida (decommission OSB)

Dame un checklist técnico para apagar OSB 12c
una vez que los servicios han sido migrados a Java 21.
