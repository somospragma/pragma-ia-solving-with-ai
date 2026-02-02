# Reglas de Calidad MCP - Automatización Appium

## Objetivo
Establecer criterios objetivos y verificables para evaluar la calidad de proyectos de automatización de pruebas móviles desarrollados con Appium.

## Alcance
Aplica a proyectos que utilicen Appium para automatización de aplicaciones móviles nativas, híbridas y web en Android e iOS.

## Reglas MCP

### Regla 1: Documentación y Estructura Base
**Descripción**: El proyecto debe tener documentación clara y estructura organizada
**Criterios**:
- 1.1. DEBE existir README.md con instrucciones de instalación, configuración y ejecución
- 1.2. DEBE tener .gitignore apropiado para Node.js/móvil
- 1.3. DEBE usar control de versiones Git con commits descriptivos
- 1.4. DEBE tener estructura de carpetas organizada y lógica
**Evidencias**: README.md, .gitignore, historial Git, estructura de directorios
**Criticidad**: Crítica

### Regla 2: Configuración y Dependencias Appium
**Descripción**: Configuración correcta del framework Appium
**Criterios**:
- 2.1. DEBE existir configuración de Appium (appium.conf.js, wdio.conf.js o similar)
- 2.2. DEBE existir `package.json` con dependencias de Appium/WebDriverIO
- 2.3. DEBE definir capabilities para Android y/o iOS
- 2.4. DEBE configurar Appium server y drivers apropiados
**Evidencias**: wdio.conf.js, package.json, capabilities configuradas
**Criticidad**: Crítica

### Regla 3: Estructura de Archivos y Plataformas
**Descripción**: Organización por plataformas y funcionalidades
**Criterios**:
- 3.1. DEBE separar tests por plataforma (android/, ios/, common/)
- 3.2. DEBE existir carpeta `pages/` o `screens/` para page objects
- 3.3. DEBE existir carpeta `utils/` para funciones auxiliares
- 3.4. DEBE separar capabilities por plataforma y dispositivo
**Evidencias**: Estructura android/, ios/, pages/, utils/, config/
**Criticidad**: Alta

### Regla 4: Patrón de Diseño y Arquitectura
**Descripción**: Implementación de patrones de diseño apropiados para móvil
**Criterios**:
- 4.1. DEBE implementar Page Object Model (POM) o Screenplay pattern
- 4.2. Los page objects DEBEN estar separados por pantalla/módulo
- 4.3. DEBE abstraer diferencias entre plataformas en page objects
- 4.4. NO DEBE tener lógica de UI en archivos de test
**Evidencias**: Page objects, abstracción de plataformas
**Criticidad**: Crítica

### Regla 5: Capabilities y Configuración de Dispositivos
**Descripción**: Configuración apropiada de dispositivos y capabilities
**Criterios**:
- 5.1. DEBE definir capabilities centralizadas por dispositivo/plataforma
- 5.2. DEBE configurar matriz de dispositivos para testing
- 5.3. DEBE usar variables de entorno para paths de apps
- 5.4. DEBE configurar timeouts apropiados por plataforma
**Evidencias**: Capabilities centralizadas, matriz de dispositivos, variables de entorno
**Criticidad**: Crítica

### Regla 6: Convenciones de Nomenclatura
**Descripción**: Consistencia en nombres y estilo de código
**Criterios**:
- 6.1. Los archivos de test DEBEN usar sufijo `.spec.js` o `.test.js`
- 6.2. Los page objects DEBEN usar sufijo `.page.js` o `.screen.js`
- 6.3. Las clases DEBEN usar PascalCase
- 6.4. Los selectores DEBEN usar convención consistente por plataforma
**Evidencias**: Nombres de archivos, clases, selectores
**Criticidad**: Media

### Regla 7: Selectores y Localizadores
**Descripción**: Uso de selectores estables y apropiados para móvil
**Criterios**:
- 7.1. DEBE usar selectores estables (accessibility id preferido)
- 7.2. DEBE definir selectores por plataforma cuando sea necesario
- 7.3. DEBE evitar selectores frágiles (xpath complejos)
- 7.4. DEBE implementar fallback strategies para localizadores
**Evidencias**: Selectores por plataforma, accessibility ids, fallback strategies
**Criticidad**: Alta

### Regla 8: Manejo de Waits y Sincronización
**Descripción**: Sincronización apropiada para aplicaciones móviles
**Criterios**:
- 8.1. DEBE usar waits explícitos en lugar de sleeps
- 8.2. DEBE implementar waits para elementos específicos de mobile
- 8.3. DEBE configurar timeouts diferenciados por tipo de acción
- 8.4. DEBE manejar estados de carga de aplicación
**Evidencias**: Waits explícitos, timeouts configurados
**Criticidad**: Alta

### Regla 9: Tests Independientes y Setup
**Descripción**: Tests autónomos y configuración apropiada
**Criterios**:
- 9.1. Cada test DEBE ser independiente y ejecutable por separado
- 9.2. DEBE implementar setup/teardown apropiado por test
- 9.3. DEBE manejar instalación/desinstalación de apps cuando sea necesario
- 9.4. DEBE resetear estado de aplicación entre tests
**Evidencias**: Independencia de tests, setup/teardown, manejo de apps
**Criticidad**: Crítica

### Regla 10: Manejo de Datos de Prueba
**Descripción**: Gestión segura de datos de prueba
**Criterios**:
- 10.1. Los datos de prueba DEBEN estar externalizados
- 10.2. DEBE usar generación dinámica de datos cuando sea necesario
- 10.3. NO DEBE tener credenciales hardcodeadas
- 10.4. DEBE manejar datos específicos por plataforma
**Evidencias**: Archivos de datos externos, ausencia de credenciales hardcodeadas
**Criticidad**: Alta

### Regla 11: Gestos y Acciones Móviles
**Descripción**: Implementación de gestos nativos móviles
**Criterios**:
- 11.1. DEBE implementar gestos nativos (swipe, tap, pinch)
- 11.2. DEBE manejar orientación de dispositivo cuando aplique
- 11.3. DEBE implementar scroll y navegación apropiados
- 11.4. DEBE manejar teclado virtual y inputs específicos
**Evidencias**: Gestos implementados, manejo de orientación, scroll
**Criticidad**: Media

### Regla 12: Paralelismo y Ejecución
**Descripción**: Optimización de ejecución paralela
**Criterios**:
- 12.1. DEBE configurar ejecución paralela por dispositivo
- 12.2. DEBE manejar múltiples sesiones de Appium
- 12.3. DEBE configurar workers apropiados para dispositivos disponibles
- 12.4. DEBE implementar queue de dispositivos para ejecución
**Evidencias**: Configuración paralela, manejo de sesiones
**Criticidad**: Baja

### Regla 13: Reportes y Evidencias
**Descripción**: Generación de reportes y evidencias móviles
**Criterios**:
- 13.1. DEBE generar reportes HTML con screenshots
- 13.2. DEBE capturar screenshots en fallos automáticamente
- 13.3. DEBE generar logs detallados de Appium
- 13.4. DEBE incluir información de dispositivo en reportes
**Evidencias**: Reportes HTML, screenshots, logs de Appium
**Criticidad**: Media

### Regla 14: Integración CI/CD
**Descripción**: Integración con pipelines de CI/CD móvil
**Criterios**:
- 14.1. DEBE configurar ejecución en dispositivos reales o emuladores
- 14.2. DEBE generar reportes en formato compatible con CI
- 14.3. DEBE configurar matriz de dispositivos en pipeline
- 14.4. DEBE manejar artefactos de aplicación (APK/IPA)
**Evidencias**: Configuración CI/CD, matriz de dispositivos, artefactos
**Criticidad**: Baja

### Regla 15: Manejo de Errores y Recuperación
**Descripción**: Gestión robusta de errores móviles
**Criterios**:
- 15.1. DEBE implementar retry logic para acciones flaky
- 15.2. DEBE manejar crashes de aplicación
- 15.3. DEBE capturar y reportar errores específicos de mobile
- 15.4. DEBE implementar recovery scenarios
**Evidencias**: Retry logic, manejo de crashes, recovery scenarios
**Criticidad**: Media

### Regla 16: Performance y Optimización
**Descripción**: Optimización de performance para móvil
**Criterios**:
- 16.1. DEBE optimizar tiempo de inicio de sesiones
- 16.2. DEBE reutilizar sesiones cuando sea apropiado
- 16.3. DEBE configurar capabilities mínimas necesarias
- 16.4. DEBE monitorear uso de recursos de dispositivos
**Evidencias**: Optimización de sesiones, capabilities mínimas
**Criticidad**: Baja

### Regla 17: Calidad de Código y Mantenimiento
**Descripción**: Código limpio y mantenible
**Criterios**:
- 17.1. NO DEBE tener código comentado sin justificación
- 17.2. DEBE tener configuración de IDE consistente (.editorconfig)
- 17.3. DEBE seguir convenciones de nomenclatura consistentes
- 17.4. DEBE tener configuración de linting y formateo automático
**Evidencias**: Ausencia de código comentado, .editorconfig, linting
**Criticidad**: Media

### Regla 18: Versionado y Conectividad
**Descripción**: Gestión de versiones y conectividad con herramientas
**Criterios**:
- 18.1. DEBE tener configuración de branches y protección en Git
- 18.2. DEBE usar versionado semántico en releases
- 18.3. DEBE tener configuración de conectividad VST/ALM apropiada
- 18.4. DEBE tener configuración de hooks de Git para calidad
**Evidencias**: Configuración Git, versionado, conectividad ALM
**Criticidad**: Alta

## Criterios de Cumplimiento
- **Crítico**: Reglas 1, 2, 4, 5, 9 (Bloquean ejecución)
- **Alto**: Reglas 3, 7, 8, 10, 18 (Impactan mantenibilidad)
- **Medio**: Reglas 6, 11, 13, 15, 17 (Mejoran calidad)
- **Bajo**: Reglas 12, 14, 16 (Optimizaciones)

## Evidencias Esperadas en Repositorio
- Archivo de configuración Appium (wdio.conf.js, appium.conf.js)
- Carpetas separadas por plataforma (android/, ios/)
- Page objects implementados por pantalla
- Capabilities centralizadas por dispositivo
- `package.json` con dependencias Appium
- Reportes HTML con screenshots
- Logs de ejecución detallados
- Configuración de matriz de dispositivos

## Estructura de Carpetas Recomendada
```
├── wdio.conf.js
├── package.json
├── tests/
│   ├── android/
│   │   ├── login.spec.js
│   │   └── checkout.spec.js
│   ├── ios/
│   │   ├── login.spec.js
│   │   └── checkout.spec.js
│   └── common/
│       └── shared.spec.js
├── pages/
│   ├── android/
│   │   ├── login.page.js
│   │   └── home.page.js
│   ├── ios/
│   │   ├── login.page.js
│   │   └── home.page.js
│   └── base.page.js
├── utils/
│   ├── device-utils.js
│   ├── gesture-utils.js
│   └── data-helpers.js
├── config/
│   ├── android-caps.js
│   ├── ios-caps.js
│   └── device-matrix.js
└── data/
    ├── test-data.json
    └── users.json
```

## Anti-patrones Comunes
- Tests dependientes entre plataformas
- Selectores hardcodeados sin abstracción
- No manejar diferencias entre Android/iOS
- Usar sleeps en lugar de waits explícitos
- No implementar page objects
- Capabilities mal configuradas
- No capturar evidencias en fallos
- Tests monolíticos sin modularización
- No manejar gestos nativos apropiadamente
- Configuración de CI inadecuada para móviles

## Ejemplo de Evaluación MCP

### Input
```
Proyecto con:
- wdio.conf.js configurado ✓
- Separación Android/iOS ✓
- Page objects implementados ✓
- Capabilities centralizadas ✓
- Selectores hardcodeados ✗
- Sin manejo de gestos ✗
- Reportes con screenshots ✓
- Sin configuración CI ✗
```

### Output
```
Evaluación Appium MCP:
- Cumplimiento: 68%
- Crítico: 4/4 reglas ✓
- Alto: 6/8 reglas ✓
- Medio: 8/12 reglas ✓
- Bajo: 4/8 reglas ✓

Acciones requeridas:
1. Abstraer selectores por plataforma (Regla 6.2)
2. Implementar gestos nativos (Regla 10.1)
3. Configurar pipeline CI/CD móvil (Regla 13.1)
4. Implementar retry logic (Regla 14.1)

Estado: CALIDAD ACEPTABLE - Mejoras requeridas
```