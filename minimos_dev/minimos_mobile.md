# Actividades core para el desarrollo mobile

Este documento establece las actividades core (requeridas, buenas prácticas y deseables) que deben promover todos los proyectos de desarrollo mobile en Pragma, garantizando la calidad, mantenibilidad y seguridad del código.

# 🏛️ Arquitectura

## 🎨 Diseño de Arquitectura
[Documentación de referencia en Alejandría](https://alejandria.pragma.co/es/private/conocimiento-aplicado/dise%C3%B1o-arquitectura/kc-cc/arquitectura-patrones-principios/arquitectura-limpia/mobile-arquitecture-blueprint)

- **[Requerido]** (Agnóstico): Definir una arquitectura limpia y desacoplada, considerando:
    - Arquitectura limpia: 3 capas (presentación, dominio, datos).
    - Dependencia de abstracciones y no de implementaciones (Repository, UseCase, BloC/Provider).
    - Uso de un gestor de inyección de dependencias (`Get_it`, `Dagger Hilt`, `Swinject`).
    - Configuración para ambientes de compilación (`Flavors`, `schemes`).
    - Centralización de labels y configuración para internacionalización.
    - **Recurso:** [Mobile Architecture Blueprint](https://drive.google.com/file/d/16tcOS_u6xwShOeFQyLjFCLqbWjoiOB2x/view?usp=sharing)

- **[Requerido]** (Flutter): Utilizar el arquetipo base de Flutter.
    - **Recurso:** [Flutter Archetype](https://github.com/somospragma/pragma-mason-bricks.git)

- **[Requerido]** (Android): Utilizar el arquetipo base de Android.
    - **Recurso:** [Android Archetype](https://gitlab.com/chapter-mobile/arquitectura/arquetipos/android)

- **[Requerido]** (iOS): Utilizar el arquetipo base de iOS.
    - **Recurso:** [iOS Archetype](https://gitlab.com/chapter-mobile/arquitectura/arquetipos/ios)

---
## 📁 Estructura del Proyecto
[Documentación de referencia en Alejandría (Monorepo)](https://alejandria.pragma.co/es/private/conocimiento-aplicado/dise%C3%B1o-arquitectura/kc-cc/arquitectura-patrones-principios/arquitectura-limpia/monorepo-flutter) | [Documentación de referencia en Alejandría (Multirepo)](https://alejandria.pragma.co/es/private/conocimiento-aplicado/dise%C3%B1o-arquitectura/kc-cc/arquitectura-patrones-principios/arquitectura-limpia/multirepo-flutter)

- **[Requerido]** (Flutter): Modelar la estructura del proyecto de acuerdo a la definición estándar.
    - **Recursos:**
        - [Monorepo Project Structure](https://docs.google.com/document/d/1DYF0q5zJXQituHaadhpQ8jqJS71Q_McbOEie3ipfMJU/edit?usp=drive_link)
        - [Multirepo Project Structure](https://docs.google.com/document/d/1TR8PdxQBUdx7LzaKrn2T3V_gviQrAst6of8dRAJkpl0/edit?usp=drive_link)

---
## 📦 Patrón Repositorio
[Documentación de referencia en Alejandría](https://alejandria.pragma.co/es/private/conocimiento-aplicado/dise%C3%B1o-arquitectura/kc-cc/arquitectura-patrones-principios/patron-repository/repository-pattern)

- **[Requerido]** (Agnóstico): Implementar el patrón repositorio para la capa de datos:
    - Generar abstracción del Repositorio (interfaz).
    - Generar implementación del Repositorio.
    - Generar abstracción de cada DataSource (interfaz).
    - Generar implementación de cada DataSource.
    - Generar los Models necesarios.

---
## 🔗 Dependencias
[Documentación de referencia en Alejandría](https://alejandria.pragma.co/es/private/conocimiento-aplicado/desarrollo/kc-cc/desarrollo-web-mobile/manejo-dependencias/web-views)

- **[Buena Práctica]** (Flutter): Gestionar correctamente las dependencias y la comunicación con capas nativas o web:
    - Ejecutar JS mediante webview y comunicarse con `postmessage`.
    - Manejar paquetes locales (monorepo) y globales.
    - Comunicación con nativo mediante `plugin` (para APIs o SDK).
    - **Recursos:**
        - [JS Flutter compability](https://github.com/somospragma/mobile-js-compability-flutter-examples.git)
        - [Postmessage example](https://github.com/somospragma/mobile-postmessage-flutter-example.git)

---
## 🖌️ Motor de Renderizado
[Documentación de referencia en Alejandría](https://alejandria.pragma.co/es/private/conocimiento-aplicado/desarrollo/kc-cc/desarrollo-web-mobile/renderizado/rendering-engine-flutter)

- **[Buena Práctica]** (Flutter): Usar el motor de renderizado `canvas kit`.

---
## 🧩 Modularización
[Documentación de referencia en Alejandría](https://alejandria.pragma.co/es/private/conocimiento-aplicado/desarrollo/kc-cc/desarrollo-web-mobile/modularizacion/modularizacion-apps-mobiles)

- **[Buena Práctica]** (Agnóstico): Cumplir con los criterios de modularización expuestos en la documentación.
    - **Recurso:** [Mobile Apps Modularization](https://drive.google.com/drive/folders/1_mXbGMDq-rLZjNJwDPUfBsoT3HIDQCP6?usp=drive_link)

---
## 🔄 Patrón de Estado (State)
[Documentación de referencia en Alejandría](https://alejandria.pragma.co/es/private/conocimiento-aplicado/dise%C3%B1o-arquitectura/kc-cc/arquitectura-patrones-principios/patron-state/state-pattern)

- **[Buena Práctica]** (Agnóstico): Elegir un patrón de estado según las necesidades del proyecto o característica a desarrollar, en línea con las definiciones de arquitectura del proyecto.
    - **Recursos:**
        - [Riverpod state management](https://youtu.be/Tb_T8_Rm2hE?si=J-HZVJJaf6gfkMjT)
        - [BLoC state management example](https://gitlab.com/chapter-mobile/arquitectura/arquetipos/flutter/bloc_exampleproject)
- **[Deseable]** (Flutter): Usar `BLoC` como gestor de estado.
- **[Deseable]** (Flutter): Usar `Riverpod` como gestor de estado.

---

# 💻 Codificación (Coding)

## 📜 Guías de Estilo (Guidelines)
[Documentación de referencia en Alejandría (Flutter)](https://alejandria.pragma.co/es/private/conocimiento-aplicado/desarrollo/kc-cc/desarrollo-web-mobile/guidelines/flutter) | [Referencia (Android)](https://alejandria.pragma.co/es/private/conocimiento-aplicado/desarrollo/kc-cc/desarrollo-web-mobile/guidelines/android) | [Referencia (iOS)](https://alejandria.pragma.co/es/private/conocimiento-aplicado/desarrollo/kc-cc/desarrollo-web-mobile/guidelines/ios)

- **[Buena Práctica]** (Flutter): Cumplir con las definiciones de la guía de estilo.
    - **Recurso:** [Flutter Guidelines](https://pragma.workplace.com/work/knowledge/3131198117184239/)
- **[Buena Práctica]** (Android): Cumplir con las definiciones de la guía de estilo.
    - **Recurso:** [Android Guidelines](https://pragma.workplace.com/work/knowledge/3131185727185478)
- **[Buena Práctica]** (iOS): Cumplir con las definiciones de la guía de estilo.
    - **Recurso:** [iOS Guidelines](https://pragma.workplace.com/work/knowledge/3131194520517932)

---
## 🔍 Linters
[Documentación de referencia en Alejandría](https://alejandria.pragma.co/es/private/conocimiento-aplicado/devsecops/kc-cc/2-pilar-integracion-continua-ci/analisis-estatico-codigo/static-analysis-flutter)

- **[Buena Práctica]** (Flutter): Implementar la dependencia `VeryGood Analysis` y validar los resultados del análisis estático.
    - **Recurso:** [Very Good Analysis](https://pub.dev/packages/very_good_analysis)

---
## ✨ Código Limpio (Clean Code)
[Documentación de referencia en Alejandría](https://alejandria.pragma.co/es/private/conocimiento-aplicado/desarrollo/kc-cc/codificacion/CleanCode)

- **[Buena Práctica]** (Flutter): Aplicar prácticas de código limpio:
    - Nombres de variables en `camelCase`.
    - Nombres de clases en `PascalCase`.
    - Nombres de archivo en `snake_case`.
    - Indentación de 2 espacios.
    - Condicionales y bucles envueltos por `{ }`.
    - Documentación (`///`) para clases y métodos con lógica compleja.
    - **Recurso:** [Clean Code Practices](https://dart.dev/effective-dart)

---
## 📐 Principios SOLID y Patrones GoF
[Documentación de referencia en Alejandría](https://alejandria.pragma.co/es/private/conocimiento-aplicado/dise%C3%B1o-arquitectura/kc-cc/arquitectura-patrones-principios/patrones-gof/factory-method/factory-method-flutter)

- **[Deseable]** (Flutter): Cumplir con los principios de Responsabilidad Única e Inversión de Dependencia, y aplicar patrones de diseño GoF donde sea necesario (`Factory`, `Builder`, `Observer`, `Strategy`, etc.).
    - **Recursos:**
        - [Factory Pattern](https://youtu.be/WReszJmcyWA?si=0mLI62RbogdqYwHe)
        - [Abstract Factory Pattern](https://youtu.be/phMmDWULxZs?si=HC9E4L7gkNCeelL9)
        - [Builder Pattern](https://youtu.be/DWAiinPRdhI?si=EO18LkAS_beNqDye)
        - [Decorator Pattern](https://youtu.be/Ll4hGNmSkVk?si=J9hddiCeZShyYJ7h)
        - [Facade Pattern](https://youtu.be/cqWvRpATEbM?si=XSW85CmuG_jY7Vr1)

---
## ⚠️ Excepciones
[Documentación de referencia en Alejandría](https://alejandria.pragma.co/es/private/conocimiento-aplicado/observabilidad/kc-cc/logs-mobile)

- **[Buena Práctica]** (Agnóstico): Gestionar adecuadamente las excepciones y fallos:
    - Definición de excepciones personalizadas.
    - Definición de `failures` (Network, Server, Cache, Timeout, etc.).
    - Manejar excepciones y `failures` particulares del proyecto.

---
## 📊 Análisis Estático
[Documentación de referencia en Alejandría](https://alejandria.pragma.co/es/private/conocimiento-aplicado/devsecops/kc-cc/2-pilar-integracion-continua-ci/analisis-estatico-codigo/static-analysis-flutter)

- **[Requerido]** (Flutter): Garantizar una cobertura de pruebas (`coverage`) superior o igual al 70% mediante `LCOV`.

---

# 🔒 Seguridad

## Ofuscación
[Documentación de referencia en Alejandría (Android)](https://alejandria.pragma.co/es/private/conocimiento-aplicado/seguridad-ingenieria-caos/kc-cc/ofuscacion/android) | [Referencia (Flutter)](https://alejandria.pragma.co/es/private/conocimiento-aplicado/seguridad-ingenieria-caos/kc-cc/ofuscacion/flutter)

- **[Requerido]** (Android): Realizar la minificación, optimización y ofuscación del código, configurando `proguard` si es necesario.
    - **Recurso:** [Android Shrink and Obfuscate](https://developer.android.com/build/shrink-code?hl=es-419)
- **[Requerido]** (Flutter): Realizar la ofuscación de código para apps Flutter (no web).
    - **Recurso:** [Flutter Obfuscate](https://docs.flutter.dev/deployment/obfuscate)

---
## 🤫 Datos Sensibles
[Documentación de referencia en Alejandría](https://alejandria.pragma.co/es/private/conocimiento-aplicado/seguridad-ingenieria-caos/kc-cc/sensitive-data)

- **[Buena Práctica]** (Agnóstico): Proteger la información sensible de la aplicación:
    - Usar `keystore` (Android) y `keychain` (iOS).
    - Usar manejadores de secretos para datos como API Keys.
    - Usar almacenamiento seguro y cifrado (`securestorage`) en otros casos.

---
## 🛡️ OWASP Top 10 Mobile
[Documentación de referencia en Alejandría](https://alejandria.pragma.co/es/private/conocimiento-aplicado/seguridad-ingenieria-caos/kc-cc/owasp)

- **[Deseable]** (Agnóstico): Cubrir la lista de chequeo de nivel 1 de la "Mobile Application Security Checklist" de OWASP.
    - **Recurso:** [Owasp Top 10 mobile 2024](https://drive.google.com/drive/folders/13ucdMXJRJ9_U435IDGukr9My2zmKk_6o?usp=drive_link)

---
## 🏃 RASP (Runtime Application Self-Protection)
[Documentación de referencia en Alejandría](https://alejandria.pragma.co/es/private/conocimiento-aplicado/seguridad-ingenieria-caos/kc-cc/rasp)

- **[Deseable]** (Agnóstico): Determinar la necesidad de incorporar herramientas RASP como `Talsec FreeRasp`, `AppDome` o `GuardSquare`.

---

# 🧪 Pruebas (Testing)

## Pruebas Unitarias
[Documentación de referencia en Alejandría](https://alejandria.pragma.co/es/private/conocimiento-aplicado/testing/kc-cc/fundamentos-calidad-software/tipos-niveles-pruebas/pruebas-unitarias/mobile)

- **[Buena Práctica]** (Flutter): Aplicar pruebas unitarias a las capas de datos y dominio:
    - Aplicar el patrón AAA (Arrange, Act, Assert).
    - Probar `DataSources`.
    - Probar `Repositories` (mockeando `DataSources`).
    - Probar `UseCases` (mockeando `Repositories`).
    - **Recursos:**
        - [Unit Test in Dart and Flutter](https://youtu.be/vWJFd2lqKg8?si=11L-XngdLNku_Tv9)
        - [Unit Test and Mocks](https://youtu.be/EOlggsZ9uBE?si=ODbm18PzOJ6n2fZs)

---
## 🖼️ Pruebas de Widgets
[Documentación de referencia en Alejandría](https://alejandria.pragma.co/es/private/conocimiento-aplicado/testing/kc-cc/fundamentos-calidad-software/tipos-niveles-pruebas/Widget-test)

- **[Buena Práctica]** (Flutter): Probar widgets críticos, dinámicos y con interacción del usuario:
    - Widgets críticos: `StatefulWidgets`, formularios con validaciones, animaciones.
    - Widgets dinámicos: `FutureBuilder`, `StreamBuilder`, `Provider`/`BLoC`.
    - Widgets con gestos: botones, listas y scroll.
    - **Recurso:** [Widget testings in Flutter](https://youtu.be/5N5qb1RGrig?si=g3ns2jOhTJvdy7DH)

---
## 🔗 Pruebas de Integración
[Documentación de referencia en Alejandría](https://alejandria.pragma.co/es/private/conocimiento-aplicado/testing/kc-cc/fundamentos-calidad-software/tipos-niveles-pruebas/Integration-test)

- **[Buena Práctica]** (Flutter): Probar los flujos principales en su camino feliz, de acuerdo al plan de pruebas del equipo de QA.
    - **Recurso:** [Integration test in Flutter](https://youtu.be/KSYw_LZXV4k?si=HFljgj25r3Cmf06S)

---
## 🏆 Pruebas Golden
[Documentación de referencia en Alejandría](https://alejandria.pragma.co/es/private/conocimiento-aplicado/testing/kc-cc/fundamentos-calidad-software/tipos-niveles-pruebas/Golden-testing)

- **[Deseable]** (Flutter): Implementar pruebas Golden para verificar la consistencia visual de los componentes de la UI.

---
## 🧬 Pruebas de Mutación
[Documentación de referencia en Alejandría](https://alejandria.pragma.co/es/private/conocimiento-aplicado/testing/kc-cc/fundamentos-calidad-software/tipos-niveles-pruebas/pruebas-de-mutacion)

- **[Deseable]** (Flutter): Configurar pruebas de mutación para evaluar la calidad del set de pruebas existente.
    - **Recursos:**
        - [Mutation test in Flutter Part 1](https://youtu.be/2HA1WYkx5mo?si=N9pZQgH3n3cuSJ4Q)
        - [Mutation test in Flutter Part 2](https://youtu.be/SEdJEK4QsAA?si=9Wj-MljpEkhr6GyU)

---
## 🛡️ Pruebas de Seguridad
[Documentación de referencia en Alejandría](https://alejandria.pragma.co/es/private/conocimiento-aplicado/testing/kc-cc/fundamentos-calidad-software/tipos-niveles-pruebas/Security-Testing)

- **[Requerido]** (Agnóstico): Realizar pruebas de seguridad a los compilados con **Mobile Security Framework (MobSF)** en cada sprint y mantener una calificación "A" (Bajo Riesgo).
    - **Recurso:** [Mobile Security Framework](https://docs.google.com/document/d/1wJpSDQg6pL1c-3i3atYu_ejqgdaPduZRQL0BK1sRIuE/edit?usp=sharing)

---
## ⏱️ Profiling de la App
[Documentación de referencia en Alejandría](https://alejandria.pragma.co/e/es/private/conocimiento-aplicado/testing/kc-cc/fundamentos-calidad-software/tipos-niveles-pruebas/profiling-app)

- **[Buena Práctica]** (Flutter): Validar que los consumos de memoria y CPU se mantengan por debajo de umbrales predefinidos.
    - **Recurso:** [Performance and Profiling in Flutter](https://youtu.be/cqH5HXz_3e0?si=L_SnR-FQBJwdrYWW)

---

# 🔭 Observabilidad

## 📈 Monitoreo de Usuario Real (RUM)
[Documentación de referencia en Alejandría](https://alejandria.pragma.co/es/private/conocimiento-aplicado/observabilidad/kc-cc/rum/flutter)

- **[Requerido]** (Flutter/Android/iOS): Integrar **Firebase Crashlytics** para detectar fallas en tiempo real, personalizar reportes y definir alertas.
    - **Recurso:** [Configuración Crashlytics](https://firebase.google.com/docs/crashlytics/get-started?hl=es-419&platform=flutter)
- **[Deseable]** (Flutter/Android/iOS): Integrar **Firebase Performance Monitor** para obtener información sobre el rendimiento, monitorear métricas predeterminadas y personalizadas, y definir umbrales de alerta.
    - **Recurso:** [Configuración Performance Monitor](https://firebase.google.com/docs/perf-mon/flutter/get-started?hl=es-419)

---
## 📝 Logs
[Documentación de referencia en Alejandría](https://alejandria.pragma.co/es/private/conocimiento-aplicado/observabilidad/kc-cc/logs-mobile)

- **[Requerido]** (Agnóstico): Gestionar los logs de forma segura y eficiente:
    - Los logs del sistema operativo no deben contener datos sensibles (tokens, IDs de usuario).
    - Los logs del sistema deben estar apagados en compilados de `release`.
    - Utilizar diferentes niveles de logs: `Debug`, `Error`, `Info`.

---

# 🚀 DevSecOps

## 🏷️ Versionamiento Semántico
[Documentación de referencia en Alejandría](https://alejandria.pragma.co/es/private/conocimiento-aplicado/devsecops/kc-cc/1-pilar-gestion-de-la-configuracion/sistema-de-control-de-versiones/versionamiento-semantico)

- **[Buena Práctica]** (Agnóstico): Seguir las pautas de `semver.org`.
    - **Recurso:** [Semantic Versioning](https://semver.org/)

---
## 💬 Commits Convencionales
[Documentación de referencia en Alejandría](https://alejandria.pragma.co/es/private/conocimiento-aplicado/devsecops/kc-cc/1-pilar-gestion-de-la-configuracion/bests-practices)

- **[Buena Práctica]** (Agnóstico): Seguir las pautas de `conventionalcommits.org`.
    - **Recurso:** [Conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)

---
## 🌿 Estrategia de Ramas (Branching)
[Documentación de referencia en Alejandría](https://alejandria.pragma.co/es/private/conocimiento-aplicado/devsecops/kc-cc/1-pilar-gestion-de-la-configuracion/estrategia-branch)

- **[Buena Práctica]** (Agnóstico): Seguir el estándar de versionamiento Pragma.
    - **Recurso:** [Estándar de Versionamiento](https://docs.google.com/document/d/1BRYMjc8vJU-3Ncj5BVEaHTSDjBsyoFaYcqDsJ0N22r0/edit?usp=sharing)

---
## ☁️ Ambientes Preproductivos
[Documentación de referencia en Alejandría](https://alejandria.pragma.co/es/private/conocimiento-aplicado/devsecops/kc-cc/4-pilar-despliegue-entrega-continua-cd/preproductive-environments)

- **[Buena Práctica]** (Agnóstico): Contar con distribución para ambientes de Desarrollo y QA, utilizando mecanismos como `AppCenter` o `Firebase AppDistribution`.
    - **Recursos:**
        - [Visual Studio AppCenter](https://learn.microsoft.com/en-us/appcenter/)
        - [Firebase App Distrubution](https://firebase.google.com/docs/app-distribution?hl=es-419)

---
## SonarQube / SonarCloud
[Documentación de referencia en Alejandría](https://alejandria.pragma.co/es/private/conocimiento-aplicado/devsecops/kc-cc/2-pilar-integracion-continua-ci/analisis-estatico-codigo/sonar/flutter)

- **[Requerido]** (Flutter/Android/iOS): Configurar la verificación de calidad de código con Sonar, definiendo un *quality gate* estricto:
    - Menos del 5% de líneas duplicadas.
    - Calificación "A" en deuda técnica, vulnerabilidades, code smells y bugs.

---
## 🛠️ Pipeline de Build
[Documentación de referencia en Alejandría (Android)](https://alejandria.pragma.co/es/private/conocimiento-aplicado/devsecops/kc-cc/4-pilar-despliegue-entrega-continua-cd/cd-android) | [Referencia (iOS)](https://alejandria.pragma.co/es/private/conocimiento-aplicado/devsecops/kc-cc/2-pilar-integracion-continua-ci/analisis-estatico-codigo/sonar/ios)

- **[Requerido]** (Android/iOS): Definir un pipeline con un mínimo de 2 stages (Build, Deploy), integraciones con Sonar y AppCenter, y aprobaciones para el despliegue.
    - **Recursos:**
        - [Android Pipeline Steps](https://docs.google.com/document/d/18iP7p_SI0kdi_L1WRrVr3S6gECsR5ak74ImfxIYwJXg/edit?usp=sharing)
        - [iOS Pipeline Steps](https://docs.google.com/document/d/1gYo7lY3lxAMpjdcMeP2ULIZg6vaSii7thdt4hkPuTWs/edit?usp=sharing)

---
## 🔑 Cuentas de Desarrollador
[Documentación de referencia en Alejandría](https://alejandria.pragma.co/es/private/conocimiento-aplicado/infraestructura/kc-cc/accounts/developers-accounts)

- **[Requerido]** (Agnóstico): Gestionar las cuentas de desarrollador para las tiendas (`PlayStore`, `AppStore`, `Huawei`).

---
## ✍️ Certificados y Firmas
[Documentación de referencia en Alejandría (Android)](https://alejandria.pragma.co/es/private/conocimiento-aplicado/seguridad-ingenieria-caos/kc-cc/certificados/certificates-firms-android) | [Referencia (iOS)](https://alejandria.pragma.co/es/private/conocimiento-aplicado/seguridad-ingenieria-caos/kc-cc/certificados/certificates-firms-ios)

- **[Requerido]** (Android): Firmar todo compilado en modo `release` que apunte a producción.
    - **Recurso:** [Android Certificate](https://developer.android.com/studio/publish/app-signing?hl=es-419)
- **[Requerido]** (iOS): Gestionar los certificados y provisiones para la firma de la aplicación.
    - **Recurso:** [iOS Certificate](https://developer.apple.com/documentation/xcode/distribution)

---

# 🎨 UX/UI

## 🧩 Sistema de Diseño
[Documentación de referencia en Alejandría](https://alejandria.pragma.co/es/private/conocimiento-aplicado/desarrollo/kc-cc/desarrollo-web-mobile/sistema-disenio/design-system-mobile)

- **[Deseable]** (Flutter): Definir un sistema de diseño, su gobierno, sus componentes y la pertinencia de usar un `storybook` como `Widgetbook`.
    - **Recurso:** [Widgetbook for Flutter](https://docs.widgetbook.io/)

---

# 🔩 Infraestructura IT

## 💻 Hardware
[Documentación de referencia en Alejandría](https://alejandria.pragma.co/es/private/conocimiento-aplicado/infraestructura/kc-cc/hardware/hardware-mobile)

- **[Requerido]** (Agnóstico): Contar con el hardware necesario:
    - Equipos Macbook con procesadores Apple Silicon.
    - Dispositivos móviles de prueba habilitados para depuración USB.

---
## 📦 Software
[Documentación de referencia en Alejandría](https://alejandria.pragma.co/es/private/conocimiento-aplicado/infraestructura/kc-cc/software/software-mobile)

- **[Requerido]** (Agnóstico): Tener instalado el software base para el desarrollo: `Xcode`, `Cocoapods`, `Node JS`, `NVM`, `VSCode`, `Android Studio`, SDKs (`Android`, `Flutter`, `Dart`), `Java JDK 17`, `Gradle`, `Homebrew`, `FVM`, `Git`, etc.