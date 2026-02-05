# Reglas de Calidad MCP - Automatización Karate

## Objetivo
Establecer criterios objetivos y verificables para evaluar la calidad de proyectos de automatización de pruebas desarrollados con Karate Framework.

## Alcance
Aplica a proyectos que utilicen Karate para automatización de APIs REST/GraphQL, servicios web y pruebas de integración.

## Reglas MCP

### Regla 1: Documentación y Estructura Base
**Descripción**: El proyecto debe tener documentación clara y estructura organizada
**Criterios**:
- 1.1. DEBE existir README.md con instrucciones de instalación, configuración y ejecución
- 1.2. DEBE tener .gitignore apropiado para Java/Maven/Gradle
- 1.3. DEBE usar control de versiones Git con commits descriptivos
- 1.4. DEBE tener estructura de carpetas organizada y lógica
**Evidencias**: README.md, .gitignore, historial Git, estructura de directorios
**Criticidad**: Crítica

### Regla 2: Configuración y Dependencias Karate
**Descripción**: Configuración correcta del framework Karate
**Criterios**:
- 2.1. DEBE existir archivo `karate-config.js` en la raíz del proyecto
- 2.2. DEBE existir al menos un archivo `.feature` en el proyecto
- 2.3. DEBE existir `pom.xml` o `build.gradle` con dependencia de Karate
- 2.4. DEBE definir perfiles de ambiente (dev, test, prod) en configuración
**Evidencias**: karate-config.js, archivos .feature, pom.xml/build.gradle
**Criticidad**: Crítica

### Regla 3: Organización de Archivos y Recursos
**Descripción**: Estructura modular y organizada de tests y recursos
**Criterios**:
- 3.1. Los archivos `.feature` DEBEN estar organizados en carpetas por funcionalidad
- 3.2. DEBE existir carpeta `classpath:` para recursos compartidos
- 3.3. Los archivos de datos DEBEN estar separados en carpeta `data/`
- 3.4. DEBE existir carpeta `utils/` para funciones JavaScript reutilizables
**Evidencias**: Estructura de carpetas features/, data/, utils/
**Criticidad**: Alta

### Regla 4: Convenciones de Nomenclatura y Estilo
**Descripción**: Consistencia en nombres y estilo de código
**Criterios**:
- 4.1. Los archivos `.feature` DEBEN usar nomenclatura descriptiva (ej: `user-registration.feature`)
- 4.2. Los scenarios DEBEN tener nombres descriptivos y únicos
- 4.3. Las variables DEBEN usar camelCase o snake_case consistentemente
- 4.4. Los tags DEBEN seguir convención `@smoke`, `@regression`, `@api`
**Evidencias**: Nombres de archivos, scenarios, variables, tags
**Criticidad**: Media

### Regla 5: Calidad de Scenarios y Gherkin
**Descripción**: Scenarios bien estructurados siguiendo BDD
**Criterios**:
- 5.1. Cada `.feature` DEBE tener al menos un `Background` o `Scenario`
- 5.2. Los scenarios DEBEN ser independientes entre sí
- 5.3. DEBE usar `Given`, `When`, `Then` apropiadamente según BDD
- 5.4. NO DEBE tener scenarios con más de 15 pasos
**Evidencias**: Archivos .feature, estructura de scenarios
**Criticidad**: Crítica

### Regla 6: Validaciones y Assertions
**Descripción**: Validaciones robustas de responses
**Criterios**:
- 6.1. DEBE validar status code en cada request HTTP
- 6.2. DEBE validar estructura de response con `match`
- 6.3. DEBE usar `match contains` para validaciones parciales
- 6.4. DEBE implementar validaciones de schema JSON cuando aplique
**Evidencias**: Validaciones en archivos .feature
**Criticidad**: Crítica

### Regla 7: Reutilización y Modularidad
**Descripción**: Código reutilizable y modular
**Criterios**:
- 7.1. DEBE usar `call read()` para reutilizar features comunes
- 7.2. DEBE definir funciones JavaScript en archivos `.js` separados
- 7.3. DEBE usar `karate-config.js` para configuración global
- 7.4. DEBE implementar data-driven testing con archivos externos
**Evidencias**: Uso de call read(), archivos .js, configuración global
**Criticidad**: Alta

### Regla 8: Manejo de Datos y Seguridad
**Descripción**: Gestión segura de datos de prueba
**Criterios**:
- 8.1. Los datos de prueba DEBEN estar externalizados (JSON, CSV, YAML)
- 8.2. DEBE usar `Examples:` para scenarios outline
- 8.3. NO DEBE tener datos sensibles hardcodeados
- 8.4. DEBE usar generación dinámica de datos cuando sea necesario
**Evidencias**: Archivos de datos externos, ausencia de credenciales hardcodeadas
**Criticidad**: Alta

### Regla 9: Configuración de Ambientes
**Descripción**: Manejo apropiado de múltiples ambientes
**Criterios**:
- 9.1. DEBE configurar URLs base por ambiente en `karate-config.js`
- 9.2. DEBE manejar autenticación por ambiente
- 9.3. DEBE configurar timeouts apropiados por ambiente
- 9.4. DEBE usar variables de entorno para configuración sensible
**Evidencias**: Configuración multi-ambiente, variables de entorno
**Criticidad**: Alta

### Regla 10: Reportes y Logging
**Descripción**: Generación de reportes y logs apropiados
**Criterios**:
- 10.1. DEBE generar reportes HTML automáticamente
- 10.2. DEBE configurar logging apropiado (`logback.xml`)
- 10.3. DEBE capturar requests/responses en logs
- 10.4. DEBE generar reportes en formato compatible con CI/CD
**Evidencias**: Reportes HTML, configuración de logging
**Criticidad**: Media

### Regla 11: Performance y Paralelismo
**Descripción**: Optimización de ejecución de tests
**Criterios**:
- 11.1. DEBE configurar ejecución paralela en `@parallel=false` cuando sea necesario
- 11.2. DEBE implementar `callSingle` para setup de datos compartidos
- 11.3. DEBE configurar thread count apropiado para el entorno
- 11.4. DEBE manejar timeouts de conexión y lectura
**Evidencias**: Configuración de paralelismo, timeouts
**Criticidad**: Baja

### Regla 12: Integración CI/CD
**Descripción**: Integración con pipelines de CI/CD
**Criterios**:
- 12.1. DEBE incluir configuración para Maven/Gradle en CI
- 12.2. DEBE generar reportes en formato JUnit XML
- 12.3. DEBE configurar tags para ejecución selectiva
- 12.4. DEBE fallar el build si las pruebas críticas fallan
**Evidencias**: Archivos CI/CD, configuración de build
**Criticidad**: Baja

### Regla 13: Manejo de Errores y Recuperación
**Descripción**: Gestión robusta de errores
**Criterios**:
- 13.1. DEBE implementar retry logic para requests flaky
- 13.2. DEBE capturar y reportar errores de manera descriptiva
- 13.3. DEBE usar `configure retry` apropiadamente
- 13.4. DEBE manejar excepciones de red y timeouts
**Evidencias**: Configuración de retry, manejo de errores
**Criticidad**: Baja

### Regla 14: Calidad de Código y Mantenimiento
**Descripción**: Código limpio y mantenible
**Criterios**:
- 14.1. NO DEBE tener código comentado sin justificación
- 14.2. DEBE tener configuración de IDE consistente (.editorconfig)
- 14.3. DEBE seguir convenciones de nomenclatura consistentes
- 14.4. DEBE tener configuración de linting y formateo automático
**Evidencias**: Ausencia de código comentado, .editorconfig, consistencia
**Criticidad**: Media

### Regla 16: Versionado y Conectividad
**Descripción**: Gestión de versiones y conectividad con herramientas
**Criterios**:
- 16.1. DEBE tener configuración de branches y protección en Git
- 16.2. DEBE usar versionado semántico en releases
- 16.3. DEBE tener configuración de conectividad VST/ALM apropiada
- 16.4. DEBE tener configuración de hooks de Git para calidad
**Evidencias**: Configuración Git, versionado, conectividad ALM
**Criticidad**: Alta

### Regla 17: Seguridad y Protección de Datos
**Descripción**: Implementación de medidas de seguridad para protección de datos sensibles
**Criterios**:
- 16.1. NO DEBE tener credenciales hardcodeadas en código fuente
- 16.2. DEBE usar variables de entorno para información sensible
- 16.3. DEBE implementar validación de entrada para prevenir inyección
- 16.4. DEBE enmascarar datos sensibles en logs y reportes
**Evidencias**: Ausencia de credenciales hardcodeadas, uso de variables de entorno, validación de inputs
**Criticidad**: Crítica

### Regla 18: Control de Acceso y Autenticación
**Descripción**: Gestión apropiada de acceso a recursos de testing
**Criterios**:
- 17.1. DEBE implementar autenticación segura para ambientes de testing
- 17.2. DEBE usar tokens seguros para APIs en tests
- 17.3. DEBE implementar timeout de sesiones en tests de larga duración
- 17.4. DEBE validar permisos antes de ejecutar acciones críticas
**Evidencias**: Configuración de autenticación, manejo de tokens, timeouts
**Criticidad**: Alta

### Regla 19: Cumplimiento y Auditoría
**Descripción**: Trazabilidad y cumplimiento normativo
**Criterios**:
- 18.1. DEBE generar logs de auditoría para acciones críticas
- 18.2. DEBE implementar trazabilidad de ejecuciones de tests
- 18.3. DEBE cumplir con estándares de retención de datos
- 18.4. DEBE documentar procesos de seguridad implementados
**Evidencias**: Logs de auditoría, trazabilidad, documentación de seguridad
**Criticidad**: Alta

## Criterios de Cumplimiento
- **Crítico**: Reglas 1, 2, 5, 6, 17 (Bloquean ejecución)
- **Alto**: Reglas 3, 7, 8, 9, 16, 18, 19 (Impactan mantenibilidad)
- **Medio**: Reglas 4, 10, 14 (Mejoran calidad)
- **Bajo**: Reglas 11, 12, 13 (Optimizaciones)

## Evidencias Esperadas en Repositorio
- `karate-config.js` configurado
- Archivos `.feature` organizados por módulos
- Carpeta `data/` con archivos de datos
- Carpeta `utils/` con funciones JavaScript
- `pom.xml`/`build.gradle` con dependencias
- Reportes HTML generados en `target/karate-reports/`
- Configuración de logging (`logback.xml`)

## Estructura de Carpetas Recomendada
```
src/test/java/
├── karate-config.js
├── features/
│   ├── users/
│   │   ├── user-registration.feature
│   │   └── user-authentication.feature
│   ├── products/
│   └── orders/
├── data/
│   ├── users.json
│   └── test-data.csv
├── utils/
│   ├── common-functions.js
│   └── data-generators.js
└── resources/
    └── logback.xml
```

## Anti-patrones Comunes
- Hardcodear URLs y credenciales en features
- Scenarios dependientes entre sí
- No usar tags para categorización
- Validaciones insuficientes de responses
- Datos de prueba mezclados con lógica
- No configurar timeouts apropiados
- Features monolíticas sin modularización
- No implementar retry para requests flaky

## Ejemplo de Evaluación MCP

### Input
```
Proyecto con:
- karate-config.js ✓
- 5 archivos .feature ✓
- pom.xml con karate-core ✓
- Datos hardcodeados en features ✗
- Sin carpeta utils/ ✗
- Reportes HTML generados ✓
```

### Output
```
Evaluación Karate MCP:
- Cumplimiento: 65%
- Crítico: 3/4 reglas ✓
- Alto: 2/4 reglas ✗
- Medio: 4/4 reglas ✓
- Bajo: 2/4 reglas ✓

Acciones requeridas:
1. Externalizar datos de prueba (Regla 7.1)
2. Crear carpeta utils/ con funciones JS (Regla 2.4)
3. Implementar configuración por ambientes (Regla 8.2)

Estado: REQUIERE MEJORAS
```