# Reglas de Calidad MCP - Automatización Playwright

## Objetivo
Establecer criterios objetivos y verificables para evaluar la calidad de proyectos de automatización de pruebas E2E desarrollados con Playwright.

## Alcance
Aplica a proyectos que utilicen Playwright para automatización de interfaces web, APIs y pruebas end-to-end multiplataforma.

## Reglas MCP

### Regla 1: Documentación y Estructura Base
**Descripción**: El proyecto debe tener documentación clara y estructura organizada
**Criterios**:
- 1.1. DEBE existir README.md con instrucciones de instalación, configuración y ejecución
- 1.2. DEBE tener .gitignore apropiado para Node.js/TypeScript
- 1.3. DEBE usar control de versiones Git con commits descriptivos
- 1.4. DEBE tener estructura de carpetas organizada y lógica
**Evidencias**: README.md, .gitignore, historial Git, estructura de directorios
**Criticidad**: Crítica

### Regla 2: Configuración y Dependencias Playwright
**Descripción**: Configuración correcta del framework Playwright
**Criterios**:
- 2.1. DEBE existir archivo `playwright.config.ts` o `playwright.config.js` en la raíz
- 2.2. DEBE existir `package.json` con dependencia `@playwright/test`
- 2.3. DEBE definir al menos un proyecto de testing en configuración
- 2.4. DEBE configurar browsers (chromium, firefox, webkit) según necesidades
**Evidencias**: playwright.config.ts, package.json, configuración de browsers
**Criticidad**: Crítica

### Regla 3: Organización de Archivos y Carpetas
**Descripción**: Estructura modular y organizada de tests y recursos
**Criterios**:
- 3.1. DEBE existir carpeta `tests/` para archivos de prueba
- 3.2. DEBE existir carpeta `pages/` para Page Object Models
- 3.3. DEBE existir carpeta `utils/` o `helpers/` para funciones auxiliares
- 3.4. DEBE separar fixtures en carpeta `fixtures/` o archivo dedicado
**Evidencias**: Estructura de carpetas tests/, pages/, utils/, fixtures/
**Criticidad**: Alta

### Regla 4: Patrón de Diseño y Arquitectura
**Descripción**: Implementación de patrones de diseño apropiados
**Criterios**:
- 4.1. DEBE implementar Page Object Model (POM) o Screenplay pattern
- 4.2. Los page objects DEBEN estar en archivos separados por página/módulo
- 4.3. DEBE usar selectores estables (data-testid preferido)
- 4.4. NO DEBE tener lógica de negocio en archivos de test
**Evidencias**: Page objects, selectores, separación de responsabilidades
**Criticidad**: Crítica

### Regla 5: Convenciones de Nomenclatura y Estilo
**Descripción**: Consistencia en nombres y estilo de código
**Criterios**:
- 5.1. Los archivos de test DEBEN usar sufijo `.spec.ts` o `.test.ts`
- 5.2. Los page objects DEBEN usar sufijo `.page.ts`
- 5.3. Las clases DEBEN usar PascalCase
- 5.4. Los métodos y variables DEBEN usar camelCase
**Evidencias**: Nombres de archivos, clases, métodos, variables
**Criticidad**: Media

### Regla 6: Configuración de Proyectos y Ambientes
**Descripción**: Manejo apropiado de múltiples ambientes y proyectos
**Criterios**:
- 6.1. DEBE configurar múltiples projects para diferentes browsers/dispositivos
- 6.2. DEBE definir baseURL por ambiente
- 6.3. DEBE configurar variables de entorno para datos sensibles
- 6.4. DEBE usar archivos `.env` para configuración local
**Evidencias**: Configuración multi-proyecto, variables de entorno, archivos .env
**Criticidad**: Alta

### Regla 7: Tests Independientes y Aislados
**Descripción**: Tests autónomos y bien estructurados
**Criterios**:
- 7.1. Cada test DEBE ser independiente y ejecutable por separado
- 7.2. DEBE usar `beforeEach` para setup común
- 7.3. DEBE limpiar estado entre tests cuando sea necesario
- 7.4. NO DEBE depender del orden de ejecución de tests
**Evidencias**: Independencia de tests, setup/teardown apropiado
**Criticidad**: Crítica

### Regla 8: Fixtures y Setup
**Descripción**: Configuración reutilizable y eficiente
**Criterios**:
- 8.1. DEBE usar fixtures para setup complejo y reutilizable
- 8.2. DEBE implementar fixtures para autenticación cuando aplique
- 8.3. DEBE usar `test.beforeAll` para setup costoso compartido
- 8.4. DEBE implementar teardown apropiado en fixtures
**Evidencias**: Fixtures implementadas, setup/teardown
**Criticidad**: Alta

### Regla 9: Assertions y Validaciones
**Descripción**: Validaciones robustas y específicas
**Criterios**:
- 9.1. DEBE usar assertions específicas de Playwright (`expect(locator)`)
- 9.2. DEBE validar elementos visibles antes de interactuar
- 9.3. DEBE usar waits implícitos apropiados
- 9.4. DEBE implementar validaciones de estado de la aplicación
**Evidencias**: Assertions Playwright, validaciones de visibilidad, waits
**Criticidad**: Crítica

### Regla 10: Manejo de Datos de Prueba
**Descripción**: Gestión segura de datos de prueba
**Criterios**:
- 10.1. Los datos de prueba DEBEN estar externalizados (JSON, CSV)
- 10.2. DEBE usar generación dinámica de datos cuando sea necesario
- 10.3. NO DEBE tener credenciales hardcodeadas
- 10.4. DEBE implementar data-driven testing con `test.describe.parallel`
**Evidencias**: Archivos de datos externos, ausencia de credenciales hardcodeadas
**Criticidad**: Alta

### Regla 11: Paralelismo y Performance
**Descripción**: Optimización de ejecución de tests
**Criterios**:
- 11.1. DEBE configurar workers apropiados para el entorno
- 11.2. DEBE usar `test.describe.parallel` para tests independientes
- 11.3. DEBE configurar timeouts apropiados por tipo de test
- 11.4. DEBE optimizar selectores para mejor performance
**Evidencias**: Configuración de workers, paralelismo, timeouts
**Criticidad**: Baja

### Regla 12: Reportes y Trazabilidad
**Descripción**: Generación de reportes y evidencias
**Criterios**:
- 12.1. DEBE generar reportes HTML automáticamente
- 12.2. DEBE capturar screenshots en fallos
- 12.3. DEBE generar trazas para debugging (`trace: 'on-first-retry'`)
- 12.4. DEBE configurar video recording para tests críticos
**Evidencias**: Reportes HTML, screenshots, trazas, videos
**Criticidad**: Media

### Regla 13: Integración CI/CD
**Descripción**: Integración con pipelines de CI/CD
**Criterios**:
- 13.1. DEBE incluir configuración para ejecución en CI
- 13.2. DEBE generar reportes en formato JUnit XML
- 13.3. DEBE configurar headed/headless apropiadamente
- 13.4. DEBE usar Docker para consistencia de entorno
**Evidencias**: Archivos CI/CD, configuración Docker
**Criticidad**: Baja

### Regla 14: TypeScript y Tipado
**Descripción**: Uso apropiado de TypeScript
**Criterios**:
- 14.1. DEBE usar TypeScript como lenguaje preferido
- 14.2. DEBE definir tipos para page objects y fixtures
- 14.3. DEBE configurar `tsconfig.json` apropiadamente
- 14.4. DEBE usar interfaces para contratos de datos
**Evidencias**: Archivos .ts, tsconfig.json, tipos definidos
**Criticidad**: Media

### Regla 15: Manejo de Errores y Calidad
**Descripción**: Gestión robusta de errores y calidad de código
**Criterios**:
- 15.1. DEBE configurar retry logic para tests flaky
- 15.2. DEBE capturar y reportar errores de manera descriptiva
- 15.3. NO DEBE tener código comentado sin justificación
- 15.4. DEBE tener configuración de linting y formateo automático
**Evidencias**: Configuración de retry, manejo de errores, linting
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

## Criterios de Cumplimiento
- **Crítico**: Reglas 1, 2, 4, 7, 9 (Bloquean ejecución)
- **Alto**: Reglas 3, 6, 8, 10, 16 (Impactan mantenibilidad)
- **Medio**: Reglas 5, 12, 14, 15 (Mejoran calidad)
- **Bajo**: Reglas 11, 13 (Optimizaciones)

## Evidencias Esperadas en Repositorio
- `playwright.config.ts` configurado
- Carpeta `tests/` con archivos `.spec.ts`
- Carpeta `pages/` con page objects
- `package.json` con dependencias Playwright
- Reportes HTML en `playwright-report/`
- Screenshots y trazas en `test-results/`
- Configuración TypeScript (`tsconfig.json`)

## Estructura de Carpetas Recomendada
```
├── playwright.config.ts
├── package.json
├── tsconfig.json
├── tests/
│   ├── auth/
│   │   ├── login.spec.ts
│   │   └── registration.spec.ts
│   ├── e2e/
│   └── api/
├── pages/
│   ├── login.page.ts
│   ├── dashboard.page.ts
│   └── base.page.ts
├── fixtures/
│   ├── auth.fixture.ts
│   └── data.fixture.ts
├── utils/
│   ├── helpers.ts
│   └── test-data.ts
└── data/
    ├── users.json
    └── test-config.json
```

## Anti-patrones Comunes
- Tests dependientes entre sí
- Selectores frágiles (CSS complejos, XPath)
- No usar Page Object Model
- Hardcodear datos en tests
- No configurar waits apropiados
- Tests monolíticos muy largos
- No capturar evidencias en fallos
- Configuración de CI inadecuada
- No usar TypeScript
- Fixtures mal implementadas

## Ejemplo de Evaluación MCP

### Input
```
Proyecto con:
- playwright.config.ts ✓
- Carpeta tests/ con .spec.ts ✓
- Page objects implementados ✓
- TypeScript configurado ✓
- Sin fixtures ✗
- Datos hardcodeados ✗
- Reportes HTML ✓
- Sin configuración CI ✗
```

### Output
```
Evaluación Playwright MCP:
- Cumplimiento: 72%
- Crítico: 3/3 reglas ✓
- Alto: 6/8 reglas ✓
- Medio: 8/12 reglas ✓
- Bajo: 3/8 reglas ✓

Acciones requeridas:
1. Implementar fixtures para setup (Regla 7.1)
2. Externalizar datos de prueba (Regla 9.1)
3. Configurar pipeline CI/CD (Regla 12.1)
4. Configurar retry logic (Regla 14.1)

Estado: BUENA CALIDAD - Mejoras menores requeridas
```