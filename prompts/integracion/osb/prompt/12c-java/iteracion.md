# CONTEXTO DEL PROYECTO
Estoy migrando un servicio de Oracle Service Bus 12c a un microservicio Java 21 con arquitectura limpia. 
Tengo un archivo "rules.md" con reglas del proyecto que debes respetar en todo momento.

## FASE 1: ANÁLISIS DEL SERVICIO OSB
**Objetivo:** Extraer y documentar el contexto de negocio del servicio OSB existente.

**Instrucciones:**
1. Analiza la carpeta "nombre_carpeta_fuentes" que contiene el servicio OSB
2. Crea una carpeta llamada "OSB Business Context"
3. Genera archivos markdown (.md) con la siguiente información:

   **Archivos a crear:**
   - `business-overview.md`: Descripción del propósito del negocio, casos de uso principales
   - `architecture.md`: Arquitectura actual (componentes, flujos, patrones identificados)
   - `integrations.md`: Sistemas externos, endpoints, protocolos de comunicación
   - `data-model.md`: Estructuras de datos, transformaciones, validaciones
   - `business-rules.md`: Reglas de negocio, validaciones, lógica condicional
   - `error-handling.md`: Manejo de errores, excepciones, estrategias de retry
   - `technical-details.md`: Detalles técnicos (XQuery, XSLT, pipelines, etc.)

**Entregables Fase 1:**
- Carpeta "OSB Business Context" con todos los archivos .md documentados
- Confirmación de que completaste esta fase antes de continuar

## FASE 2: DISEÑO DEL MICROSERVICIO JAVA
**Objetivo:** Diseñar la arquitectura del nuevo microservicio basándote en la documentación de Fase 1.

**Instrucciones:**
1. Lee completamente la documentación en "OSB Business Context"
2. Crea una carpeta llamada "PP-3250 ConsultaMultiplesProductosJava"
3. Diseña el microservicio con las siguientes especificaciones:

   **Stack Tecnológico:**
   - Java 21
   - Spring Boot 3.x
   - Arquitectura Limpia (Clean Architecture)
   - Maven/Gradle como gestor de dependencias

   **Capas de Arquitectura Limpia:**
```
   ├── domain/           (Entidades, Casos de Uso, Interfaces)
   ├── application/      (Servicios de aplicación, DTOs)
   ├── infrastructure/   (Adaptadores, Repositorios, Clientes HTTP)
   └── interfaces/       (Controladores REST, Configuración)
```

   **Archivos de diseño a crear:**
   - `architecture-design.md`: Diseño de arquitectura limpia aplicada
   - `api-specification.md`: Especificación de endpoints REST (OpenAPI/Swagger)
   - `migration-mapping.md`: Mapeo OSB → Java (dónde quedó cada componente)
   - `dependencies.md`: Dependencias y librerías a utilizar

**Entregables Fase 2:**
- Documentación de diseño completa
- Confirmación antes de proceder a la implementación

## FASE 3: IMPLEMENTACIÓN DEL MICROSERVICIO
**Objetivo:** Implementar el código Java del microservicio.

**Instrucciones:**
1. Crea la estructura del proyecto Maven/Gradle
2. Implementa las capas siguiendo Clean Architecture:

   **Domain Layer:**
   - Entidades de dominio (POJOs puros, sin dependencias de frameworks)
   - Casos de uso (interfaces de servicios)
   - Repositorios (interfaces, no implementaciones)
   - Excepciones de dominio

   **Application Layer:**
   - DTOs de entrada/salida
   - Servicios de aplicación (implementación de casos de uso)
   - Mapeadores (Entity ↔ DTO)
   - Validadores

   **Infrastructure Layer:**
   - Adaptadores de repositorio (implementaciones)
   - Clientes HTTP/REST para integraciones
   - Configuración de conexiones externas
   - Implementación de servicios de infraestructura

   **Interfaces Layer:**
   - Controladores REST
   - Manejo global de excepciones (@ControllerAdvice)
   - Configuración de Spring Boot
   - Documentación Swagger/OpenAPI

**Características obligatorias:**
- Manejo de excepciones robusto
- Logging estructurado (SLF4J + Logback)
- Validación de datos (Bean Validation)
- Configuración externalizada (application.yml)
- Métricas y health checks (Spring Actuator)

**Entregables Fase 3:**
- Código fuente completo del microservicio
- Archivo `pom.xml` o `build.gradle` configurado
- Archivo `README.md` del proyecto con instrucciones de ejecución