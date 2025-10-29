# Calidad Transversal - Reglas Completas (calidad-all-full)
Este documento consolida las reglas completas de calidad para todas las herramientas y dimensiones.

---
## Estrategia y Gobierno
### Política y Estrategia de Pruebas

#### Mínimos
Definir y documentar los pilares estratégicos y de gobierno de las pruebas, alineándolos con la política de calidad del negocio y el ciclo de desarrollo.

#### Way to do it (Reglas de Desarrollo)
- Definir el alcance de pruebas por niveles (Unitaria, Integración, Sistema, Aceptación). 
- Establecer los objetivos y los KPIs (p. ej., Defect Density, Defect Leakage). 
- Estandarizar la selección de técnicas de diseño (basadas en riesgo/requisitos). 
- Especificar las necesidades de Entornos y Datos de prueba.

---
### Planificación de Pruebas

#### Mínimos
Implementar un proceso formal de análisis y evaluación de riesgos de producto para determinar el alcance y el énfasis de las pruebas requeridas.

#### Way to do it (Reglas de Desarrollo)
- Crear una matriz de riesgo (Impacto vs. Probabilidad) para funcionalidades y atributos de calidad. 
- Establecer umbrales de cobertura obligatorios (p. ej., por riesgo). 
- Definir el plan de Regresión y el cronograma para mitigar los riesgos identificados.

---
### Entorno de Prueba

#### Mínimos
Establecer y controlar los recursos físicos y lógicos necesarios (sistemas, datos, configuración) para la ejecución de pruebas, asegurando su disponibilidad y aislamiento.

#### Way to do it (Reglas de Desarrollo)
- Definir la arquitectura del Entorno de Pruebas (infraestructura, versiones). 
- Implementar la gestión de datos de prueba (TDM, incluyendo enmascaramiento). 
- Coordinar la disponibilidad y el control de la configuración (Configuration Management).

---

## Herramientas y Framework de Automatización
### Herramienta de gestión de pruebas (ALM)

#### Mínimos
Seleccionar e implementar una herramienta que soporte el ciclo de vida completo de la prueba y la trazabilidad bidireccional entre requisitos, casos y defectos.

#### Way to do it (Reglas de Desarrollo)
- Configurar alguna herramienta ALM (Azure, Jira, BugTracker)para vincular automáticamente requisitos, casos de prueba y defectos. - Establecer plantillas estándar para la documentación de artefactos (Plan, Caso, Informe). 
- Centralizar la gestión de versiones de artefactos.

---
### Automatización de pruebas unitarias

#### Mínimos
Establecer la prueba unitaria como el primer nivel de pruebas y el más denso, integrando su ejecución obligatoria en el proceso de build y deployment.

#### Way to do it (Reglas de Desarrollo)
- Definir el Framework preferido para cada tecnología (p. ej., Jest/Mocha para JS/TS, JUnit/TestNG para Java, PyTest para Python). 
- Establecer el umbral mínimo de cobertura de 80% de líneas/métodos como requisito de build. 
- Aplicar prácticas de TDD.

#### Tecnología
javascript-typescript

---
### Automatización con Playwright

#### Mínimos
- Aplicar patrones de diseño POM o Screenplay.
- Organizar el código en capas independientes de herramientas externas, navegadores o servicios de backend.
- Centralizar la lógica de interacción en los Page Objects, evitando que los tests accedan directamente a selectores.
- Definir reglas de dependencia claras: los tests dependen de los Page Objects, que a su vez dependen de utilidades o servicios.
- Ninguna capa interna debe conocer detalles de capas externas.
- Cada módulo debe tener una única responsabilidad y comunicarse mediante interfaces bien definidas.
- Depender de abstracciones (interfaces o clases base) para facilitar el reemplazo de implementaciones concretas.
- Evitar dependencias innecesarias
- Apalancarse en Buenas practicas de POO y principios en la codificacion

#### Way to do it (Reglas de Desarrollo)
Dependencias y Configuración
Gestión de dependencias: usa package.json con versiones fijas; evita rangos abiertos salvo en librerías muy mantenidas.
Configuración centralizada: define playwright.config.ts con ambientes (dev, qa, prod) usando projects y env variables.
Fixtures reutilizables: define datos de prueba en fixtures/ y usa test.extend() para compartir contexto entre pruebas.

Arquitectura del Proyecto
Estructura modular: separa el proyecto en carpetas tests, pages, utils, config, fixtures.
Page Object Model (POM): cada página debe tener su propia clase con métodos que representen acciones y elementos.
ScreenplayBDD:  Usar maquetación por encarpetamiento teniendo en cuenta Task, PageUI, Question etc...
Evitar dependecnias innecesarios: No incluir librerías externas si Playwright ya ofrece la funcionalidad nativamente

Diseño de Pruebas(Buenas practicas)
Un test por flujo: cada archivo de prueba debe validar un flujo completo (ej. login, compra, navegación).
AAA (Arrange-Act-Assert): estructura cada test siguiendo este patrón.

Integración y Ejecución
Pruebas paralelas: habilita workers para acelerar ejecución.
Ambientes aislados: usa baseURL y contextOptions para separar datos entre ambientes.

Documentación
README obligatorio: explica estructura, reglas de dependencias, cómo ejecutar pruebas y cómo agregar nuevas.
Comentarios mínimos: el código debe ser autoexplicativo; comenta solo lógica compleja.

#### Tecnología
playwright, javascript-typescript

---
### Automatización de pruebas frontend

#### Mínimos
Utilizar Cypress para pruebas de Componente y E2E, aprovechando su arquitectura y depuración amigable para desarrolladores en aplicaciones web modernas.

#### Way to do it (Reglas de Desarrollo)
- Definir los casos de uso para Cypress (p. ej., pruebas E2E y de Componente/Integración Frontend). 
- Asegurar que los tests sigan la práctica de limpieza de estado antes de cada ejecución (vía API o database seeding). 
- Utilizar la sintaxis cy.*.

#### Tecnología
cypress, javascript-typescript

---
### Automatización con Selenium

#### Mínimos
Implementar pruebas End-to-End tradicionales controlando navegadores mediante WebDriver, integrando con frameworks de soporte (TestNG, JUnit, etc.) para validaciones consistentes.

#### Way to do it (Reglas de Desarrollo)
- Definir el uso de WebDrivers estandarizados. 
- Implementar patrones de diseño (p. ej., POM) para la organización del código. 
- Asegurar que la ejecución sea compatible con una Selenium Grid para pruebas paralelas y cross-browser.

#### Tecnología
Selenium, java

---
### Automatización con Serenity BDD

#### Mínimos
Definir escenarios en lenguaje Gherkin (Given, When, Then) e implementar automatización en la capa superior de la pirámide, enfocándose en la trazabilidad y documentación automática del proceso.

#### Way to do it (Reglas de Desarrollo)
- Requerir que los casos de prueba sigan el formato Gherkin para la capa de negocio. 
- Utilizar la capacidad de generación de reportes de Serenity BDD para trazar los escenarios a los requisitos de forma clara.

#### Tecnología
serenity-bdd, java

---
### Golden Test Frontend

#### Mínimos
Comparar la salida visual de un componente o interfaz con una referencia preestablecida ("base de oro"), asegurando que los cambios no alteren de manera no deseada el diseño o la apariencia.

#### Way to do it (Reglas de Desarrollo)
- Establecer una "base de oro" de referencias visuales por componente. 
- Configurar la herramienta (p. ej., Applitools o librerías de Flutter/React) para ignorar áreas dinámicas (fechas, IDs) y solo comparar el layout y estilo. Integrar en pipelines de Pull Request.

#### Tecnología
flutter

---
### Mutation Test

#### Mínimos
Evaluar la efectividad de los tests existentes al introducir cambios pequeños y controlados (mutaciones) en el código, simulando errores para verificar si las pruebas los detectan.

#### Way to do it (Reglas de Desarrollo)
- Definir un Umbral Mínimo de Puntuación de Mutación (p. ej., 60-70%). 
- Integrar la herramienta (PITest/Stryker) en el pipeline y ejecutar solo en código que ya tiene una alta cobertura unitaria (p. ej., >80%).

#### Tecnología
python

---
### Automatización de pruebas con Karate

#### Mínimos
Unificar la automatización de pruebas de API, servicios web y UI en un solo framework mediante scripts declarativos tipo BDD.

#### Way to do it (Reglas de Desarrollo)
- Establecer el uso de Karate para automatización de APIs (REST/SOAP) y validaciones JSON/XML. 
- Definir una convención para el mocking de servicios externos. 
- Usar la sintaxis Gherkin específica de Karate.

#### Tecnología
java, Karate

---
### Automatización de pruebas mobile

#### Mínimos
Asegurar la calidad y funcionalidad de aplicaciones móviles nativas, híbridas o web en distintos dispositivos y sistemas operativos.

#### Way to do it (Reglas de Desarrollo)
- Definir Appium (o frameworks nativos) como framework de automatización móvil. 
- Establecer la Matriz de Dispositivos (versiones de OS y modelos a cubrir). 
- Implementar patrones de diseño (p. ej., POM o Screenplay) específicos para Mobile.

#### Tecnología
java, flutter, Appium

---
### Widget Test

#### Mínimos
Verificar el comportamiento y la apariencia de los componentes o widgets en la interfaz de usuario, comprobando que los elementos interactúan correctamente y se renderizan como se espera.

#### Way to do it (Reglas de Desarrollo)
- Usar las herramientas nativas de prueba de frameworks de UI (p. ej., Flutter, React Testing Library, Vue Test Utils). 
- Asegurar que los tests se ejecuten sin un navegador completo (simulando el árbol de widgets) para mayor velocidad.

#### Tecnología
flutter

---
### Gestión de datos de pruebas

#### Mínimos
Definir explícitamente la creación, manipulación y edición de los datos de prueba específicos y genéricos para aumentar la reproducibilidad y cumplimiento normativo.

#### Way to do it (Reglas de Desarrollo)
- Emplear herramientas o librerías de preparación/generación de datos de prueba (fakers). 
- Formalizar el procedimiento de Enmascaramiento de Datos Sensibles (camuflaje) en entornos no productivos.
-  Archivar y documentar conjuntos de datos genéricos.

---
### Gestión de entornos

#### Mínimos
Definir la especificación de requisitos del entorno de prueba al inicio del proyecto para asegurar un entorno administrado y controlado.

#### Way to do it (Reglas de Desarrollo)
- Utilizar herramientas de Infraestructura como Código (IaC) (Terraform, Kubernetes) para la creación rápida y reproducible de entornos de prueba. 
- Definir un proceso de Reserva de Ambientes o de Autodestrucción para optimizar recursos.

---

## Integración y Estandarización de Procesos
### Organización de Pruebas

#### Mínimos
- Establecer una estructura de Roles y Responsabilidades formalizada. 
- Crear un marco de Competencias para el personal de QA para institucionalizar la prueba como disciplina.

#### Way to do it (Reglas de Desarrollo)
- Documentar el organigrama de QA y la Matriz de Competencias (Junior, Advanced, Senior, Master). 
- Definir los roles de pruebas con sus tareas. 
- Asegurar la objetividad (separación de funciones entre desarrollo y QA de sistema/aceptación).

---
### Programa de Formación de Pruebas

#### Mínimos
Desarrollar un programa de formación continuo con módulos específicos para elevar el nivel de competencia y la calidad del personal involucrado en las pruebas.

#### Way to do it (Reglas de Desarrollo)
- Identificar las brechas de conocimiento (p. ej., TDD, automatización con K6/Playwright, BDD, OWASP). 
- Establecer una Matriz de Crecimiento y un plan de capacitación formativa (cursos, mentorías) para cubrir las necesidades estratégicas.

---
### Ciclo de Vida de las Pruebas e Integración

#### Mínimos
Estandarizar el flujo de trabajo de pruebas, asegurando la trazabilidad y los puntos de integración obligatorios con el ciclo de vida de desarrollo (SDLC).

#### Way to do it (Reglas de Desarrollo)
- Definir los Criterios de Entrada/Salida (Definición de Done) para cada nivel de prueba. 
- Asegurar que los requisitos sean testeables. Documentar el flujo de trabajo de CI/CD para integrar la ejecución automatizada en todas las etapas.

---

## Medición, Control y Evaluación de calidad
### Monitorización y Control de Pruebas

#### Mínimos
Realizar revisiones periódicas del progreso y la calidad del producto y del proceso, asegurando que las actividades se realicen conforme al plan y que las desviaciones se identifiquen.

#### Way to do it (Reglas de Desarrollo)
- Definir puntos de control (Milestones) e hitos de las pruebas. 
- Generar informes periódicos de Estado de la Ejecución y Calidad del Producto (p. ej., Burn-down charts de defectos). 
- Utilizar la herramienta ALM para la trazabilidad y el reporting.

---
### Mediciones de Pruebas

#### Mínimos
Establecer objetivos de medición alineados con los objetivos de negocio y las necesidades de información para asegurar el logro de los objetivos de calidad.

#### Way to do it (Reglas de Desarrollo)
- Definir métricas clave de Eficacia (p. ej., Tasa de Detección de Defectos) y Eficiencia (p. ej., Costo por Prueba, Tiempo de Ejecución). 
- Documentar el Diccionario de Métricas (fórmula, objetivo, frecuencia).

---
### Evaluación de la Calidad del Producto

#### Mínimos
Medir cuantitativamente la calidad del producto (y sus productos de trabajo intermedios) y comparando estos datos con los objetivos de calidad definidos.

#### Way to do it (Reglas de Desarrollo)
- Seleccionar métricas que proporcionen información relevante: Densidad de Defectos, Tasa de Escape de Defectos a producción, Puntaje de Seguridad (SonarQube/Checkmarx). 
- Generar un Reporte de Calidad al final de cada ciclo/versión.

---
### Revisiones entre Pares

#### Mínimos
Implementar un proceso formal de revisión por pares para artefactos críticos (código, requisitos, casos de prueba, diseño) en fases tempranas.

#### Way to do it (Reglas de Desarrollo)
- Establecer la Revisión de Código (Code Review) como obligatoria para cualquier merge (vía Pull Request). Definir Criterios de Entrada y Salida para las revisiones (p. ej., Checklist de pruebas).

---
### Revisiones entre Pares Avanzadas

#### Mínimos
definir directrices de medición para las revisiones, incluyendo reglas, listas de control y técnicas de muestreo.

#### Way to do it (Reglas de Desarrollo)
- Sin definir.

---

## Mejora continua
### Prevención de Defectos

#### Mínimos
Definir un esquema de clasificación detallado de defectos para analizar los más críticos y frecuentes y determinar su causa raíz para evitar su recurrencia.

#### Way to do it (Reglas de Desarrollo)
- Implementar técnicas de Análisis de Causa Raíz (p. ej., 5 Porqués, Diagrama de Ishikawa) en defectos críticos. 
- Generar propuestas de acción/solución para modificar los procesos de desarrollo y prueba.

---
### Control de Calidad

#### Mínimos
Aplicar métodos estadísticos y de control de procesos para comprender las variaciones y asegurar que el proceso de pruebas es estadísticamente estable y predecible.

#### Way to do it (Reglas de Desarrollo)
- Establecer Gráficos de Control (p. ej., para la Tasa de Inserción de Defectos o el Tiempo de Ejecución de Pruebas). 
- Calcular Intervalos de Confianza para la estimación de la fiabilidad del producto. 
- Analizar las variaciones fuera de los límites aceptables para investigar la causa raíz.

---
### Optimización del Proceso de Pruebas

#### Mínimos
Gestionar el ciclo de vida de la mejora continua (identificación, evaluación, piloto, despliegue) y establecer una librería de activos de prueba reutilizables.

#### Way to do it (Reglas de Desarrollo)
- Implementar un repositorio central de Activos de Prueba Reutilizables (casos, plantillas, scripts y datos de prueba). 
- Fomentar la innovación mediante la evaluación de nuevas herramientas y técnicas (p. ej., a través de proyectos piloto). 
- Definir un proceso para la evaluación de la madurez del proceso (p. ej., con TMMi o CMMI).

---
### Inteligencia Artificial (IA)

#### Mínimos
Invertir en modelos predictivos (Machine Learning) entrenados con datos históricos y emplear herramientas basadas en IA para mejorar la efectividad (selección, generación) y la eficiencia del proceso.

#### Way to do it (Reglas de Desarrollo)
- Entrenar modelos para predecir dónde fallará el software (Risk-based Testing automatizado). 
- Usar herramientas de IA para la selección óptima de casos de prueba de regresión o para la generación asistida de scripts de prueba E2E. 
- Evaluar herramientas de curación de locators basadas en IA.

---
### Pruebas Automatizadas de Código Estático - Pipelines Units Tests

#### Mínimos
Configurar pipelines CI/CD (por ejemplo, con Jenkins, GitHub Actions o Azure DevOps) para ejecutar análisis de código estático (SonarQube, ESLint, PMD) y unit tests automáticos (JUnit, Mocha, Jest) en cada commit o pull request, asegurando calidad continua desde el desarrollo.

#### Way to do it (Reglas de Desarrollo)
- Configurar pipelines (Jenkins, GitHub Actions) para ejecutar análisis de código estático (SonarQube, ESLint) y unit tests obligatoriamente en cada Pull Request. 
- Establecer reglas de "Quality Gate" que bloqueen el merge si la cobertura es <80% o si hay vulnerabilidades críticas.

#### Tecnología
java, python, javascript-typescript

---

## Procesos y Metodologías
### Diseño y Ejecución de Pruebas

#### Mínimos
- Asegurar el uso sistemático de técnicas de diseño de pruebas apropiadas para maximizar la cobertura efectiva. 
-Estandarizar el ciclo de vida y la categorización de incidentes.

#### Way to do it (Reglas de Desarrollo)
- Requerir la aplicación de técnicas de Caja Negra (p. ej., Partición Equivalente, Valor Límite, tablas de decision) 
-Requerir la aplicacion de tecnicas de Caja Blanca (p. ej., Cobertura de Sentencias). 
- Establecer una plantilla de Caso de Prueba Estándar con pasos claros y un esquema de clasificación de defectos (Claficiacion, Severidad, Prioridad).

---
### Pruebas No Funcionales con Jmeter

#### Mínimos
- Ejecutar pruebas de rendimiento (carga, estrés) bajo condiciones controladas, simulando el comportamiento esperado del usuario y midiendo métricas clave.

#### Way to do it (Reglas de Desarrollo)
- Definir escenarios de carga basados en transacciones críticas y perfiles de usuario esperados. 
-Establecer métricas de Tiempos de Respuesta (p. ej., Percentil 95 < 2 segundos) y Throughput mínimos aceptables. - Configurar los listeners de JMeter para reportar métricas clave en formato procesable.

#### Tecnología
jmeter

---
### Pruebas No Funcionales con K6

#### Mínimos
Utilizar K6 para la ejecución de pruebas de rendimiento ligeras, modernas y con integración en CI/CD facilitada por su uso de JavaScript.

#### Way to do it (Reglas de Desarrollo)
- Priorizar K6 para servicios Backend y pruebas de stress ligeras. 
- Definir la estructura del script K6 en JavaScript para reporte automático de métricas y definición de umbrales (thresholds) que detengan la prueba si fallan.

#### Tecnología
k6

---
### Profiling App

#### Mínimos
Integrar herramientas de profiling en el ciclo de desarrollo para monitorear el uso de recursos críticos (CPU, memoria, latencia de UI) durante la ejecución de las pruebas.

#### Way to do it (Reglas de Desarrollo)
- Establecer umbrales máximos para el uso de Memoria Heap y CPU. 
- Definir la instrumentación necesaria (Dynatrace, VisualVM, Android Profiler, etc.) para analizar el rendimiento en transacciones críticas. 
- Correr profiling en el entorno más cercano a producción.

---
### Pruebas No Funcionales otros tipos

#### Mínimos
Realizar pruebas complementarias no funcionales basadas en estándares de la industria y requisitos específicos del producto para evaluar la experiencia de usuario

#### Way to do it (Reglas de Desarrollo)
- Accesibilidad: Aplicar checklists con validaciones minimas basados en WCAG (Web Content Accessibility Guidelines). 
- Usabilidad: Realizar pruebas con usuarios finales para evaluar el flujo, la eficiencia y la satisfacción. - Herramientas: 
- Usar linters de accesibilidad y checkers automáticos.

---
### Gestión de defectos

#### Mínimos
Institucionalizar un flujo de trabajo estandarizado para el manejo de defectos (detección, registro, clasificación, asignación, corrección, re-prueba, cierre).

#### Way to do it (Reglas de Desarrollo)
- Configurar la herramienta ALM/Bugs para forzar la asignación de campos clave (Severidad, Prioridad, Componente/Módulo). 
- Establecer un SLA para el tiempo de resolución basado en la Severidad. Definir el rol responsable de la validación del fix (QA/Tester).

---

## Seguridad y cumplimiento
### Pruebas de seguridad

#### Mínimos
Implementar pruebas de seguridad (análisis de vulnerabilidades) para detectar y mitigar vulnerabilidades en componentes del código, protegiendo la aplicación contra ataques.

#### Way to do it (Reglas de Desarrollo)
- SAST (Static Analysis): Configurar SonarQube/Checkmarx para escanear código en cada build. DAST (Dynamic Analysis): Implementar OWASP ZAP o similar en el entorno de QA/Staging para escaneo dinámico. - Bloquear builds con vulnerabilidades de Severidad Alta o Crítica.

---
### Cumplimiento normativo

#### Mínimos
Integrar los requisitos de cumplimiento (legales, contractuales) directamente en los criterios de aceptación y los casos de prueba para asegurar la validez legal y contractual del producto.

#### Way to do it (Reglas de Desarrollo)
- Asegurar que los requisitos de cumplimiento (p. ej., GDPR, PCI DSS, Leyes de Accesibilidad) estén documentados como Casos de Prueba de Aceptación (UAT) obligatorios. 
- Vincular estos requisitos críticos a la ejecución formal de pruebas y a los informes de calidad.

---
### Protección de datos

#### Mínimos
Formalizar el procedimiento de camuflar datos confidenciales (enmascaramiento) en el Entorno de Pruebas y controlar el acceso y el archivado de los datos.

#### Way to do it (Reglas de Desarrollo)
- Implementar técnicas de Enmascaramiento de Datos Sensibles (camuflaje/tokenización) usando librerías o herramientas ETL en entornos no productivos. Definir políticas de Acceso Restringido y Archivado Seguro de los datos de prueba, cumpliendo la normativa interna y legal (p. ej., PII, datos bancarios).

---

