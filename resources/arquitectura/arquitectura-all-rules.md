# Framework de Arquitectura: Reglas y Recomendaciones

Este documento centraliza las reglas mínimas y las buenas prácticas que deben ser consideradas en todos los proyectos para garantizar la calidad, escalabilidad y mantenibilidad de la arquitectura de software.

---

## Mínimos (Obligatorio)

Esta sección contiene las reglas **obligatorias** que todo proyecto debe cumplir. Son la base para una arquitectura robusta y alineada con los objetivos del negocio.

-   **MIN001 (Objetivos técnicos del proyecto):**
    1.  Implementa y documenta los OKRs técnicos del proyecto.
    2.  Define o adopta una arquitectura de referencia como guía.
    3.  Utiliza Registros de Decisiones de Arquitectura (ADRs) para documentar las decisiones técnicas clave.

-   **MIN002 (Alineación con el negocio):**
    1.  Crea un "Mapa de Objetivos" o "Lean Value Tree" para visualizar la conexión entre tecnología y negocio.
    2.  Utiliza el "Business Model Canvas" para entender y documentar el contexto del negocio.

-   **MIN003 (Métricas de éxito técnico):**
    1.  Define y documenta los KPIs, SLIs y SLOs del servicio.
    2.  Configura herramientas de monitoreo (ej. CloudWatch, X-Ray) para dar seguimiento a los SLIs/SLOs definidos.

-   **MIN004 (Identificación de dominios):**
    1.  Ejecuta talleres de "Event Storming" con expertos de negocio para descubrir los dominios.
    2.  Modela los dominios y sus interacciones usando "Domain Storytelling".

-   **MIN005 (Redundancia o solapamiento):**
    1.  Crea y mantén un "Context Map" para visualizar las relaciones e identificar solapamientos entre contextos.

-   **MIN006 (Definición de contextos delimitados):**
    1.  Documenta los límites de cada "Bounded Context" utilizando los patrones y artefactos de DDD.

-   **MIN007 (Claridad en límites de contexto):**
    1.  Define los contratos de servicio usando especificaciones como OpenAPI o AsyncAPI.
    2.  Utiliza un "API Gateway" para gestionar y exponer las interfaces entre contextos.

-   **MIN008 (Glosario compartido):**
    1.  Crea y mantén un "Glosario de Lenguaje Ubicuo" en una herramienta centralizada (ej. Confluence, Wiki).

-   **MIN009 (Accesibilidad del lenguaje):**
    1.  Publica el glosario en una Wiki o herramienta similar y asegúrate de que sea parte del material de onboarding.

-   **MIN010 (Definición de drivers):**
    1.  Utiliza el método "Architecture Katas" o "Quality Storming" para identificar y priorizar los atributos de calidad.

-   **MIN011 (Identificación de restricciones):**
    1.  Documenta las restricciones en Registros de Decisiones de Arquitectura (ADRs) para formalizar su impacto.

-   **MIN012 (Validación de restricciones):**
    1.  Valida formalmente las restricciones documentadas mediante la firma o aprobación de los stakeholders.

-   **MIN013 (Identificación de riesgos):**
    1.  Conduce talleres de "Risk Storming" para la identificación colaborativa de riesgos.
    2.  Mantén un registro de riesgos actualizado en una herramienta de gestión (ej. Jira Risk Logs).

-   **MIN014 (Asignación de responsables por riesgo):**
    1.  Define y asigna los roles usando una matriz RACI.
    2.  Configura tableros de seguimiento para monitorear el estado de los riesgos asignados.

---

## Buenas Prácticas

Esta sección contiene **recomendaciones y oportunidades de mejora** que los proyectos pueden adoptar para elevar su madurez arquitectónica y eficiencia operativa.

-   **BP001 (Validación de cumplimiento):**
    1.  Integra la validación de métricas como un paso obligatorio en el pipeline de CI/CD.

-   **BP002 (Uso de KPIs):**
    1.  Implementa un dashboard (ej. en Grafana, PowerBI) para visualizar y reportar los KPIs definidos.

-   **BP003 (Responsables por dominio):**
    1.  Utiliza una matriz RACI para asignar y comunicar las responsabilidades de cada owner de dominio.

-   **BP004 (Segmentación de dominios):**
    1.  Aplica el patrón "Subdomain Segregation" para clasificar y documentar los dominios (Core, Supporting, Generic).

-   **BP006 (Independencia entre contextos):**
    1.  Implementa patrones de integración como "Event-Carried State Transfer" o "CQRS" para asegurar el bajo acoplamiento.

-   **BP007 (Estrategia de desacoplamiento):**
    1.  Aplica patrones como "Anti-Corruption Layer (ACL)" o "Conformist" según la relación entre contextos.

-   **BP008 (Reflejo del lenguaje en la implementación):**
    1.  Establece revisiones de código (Pull Requests) que validen el uso del Lenguaje Ubicuo en el código fuente.

-   **BP009 (Evolución del lenguaje ubicuo):**
    1.  Agenda sesiones periódicas de refinamiento del modelo de dominio para actualizar el lenguaje.

-   **BP010 (Impacto de las restricciones):**
    1.  Utiliza "Trade-off analysis" para evaluar y documentar cómo las restricciones afectan las decisiones de diseño.

-   **BP011 (Mitigación de restricciones):**
    1.  Crea un "Plan de Mitigación" formal para cada restricción que presente un riesgo significativo.

-   **BP012 (Planes de mitigación por riesgo):**
    1.  Documenta los "Planes de mitigación" en una "matriz de riesgos" o herramienta similar.

-   **BP013 (Evaluación continua de riesgos):**
    1.  Establece "Revisiones periódicas" de riesgos dentro de las "ceremonias ágiles" (ej. Sprint Review).
