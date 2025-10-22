# Calidad Transversal - Rules para Agentes AI y Desarrolladores
Este documento establece las reglas y estándares mínimos de calidad para el desarrollo de software, aplicables de manera transversal (Backend, Frontend, Mobile, Integraciones).
---
## Arquitectura y Diseño (Mantenibilidad, Fiabilidad)
### Mínimos
- **[DRY] No Repetir Código:** Extraer funcionalidad común en módulos compartidos y crear componentes reutilizables.
- **[KISS] Mantener Simple:** Evitar la complejidad innecesaria. Preferir estructuras y lógica simples y legibles.
- **[YAGNI] Solo lo Necesario:** Evitar la optimización o implementación prematura de funcionalidad que "quizás" se necesite en el futuro.
- **Responsabilidad Única:** Mantener funciones, métodos y clases con una única responsabilidad clara.
### Way to do it (Buenas Prácticas)
- **Patrones de Diseño:** Seguir el patrón SOLID, especialmente la Inversión de Dependencias (Dependency Inversion).
- **Separación de Intereses:** Implementar el patrón de diseño **Atomic Design** o similar para estructurar la interfaz de usuario.
- **Módulos Compartidos:** Extraer la lógica de negocio, utilidades o servicios transversales en módulos claramente definidos.
---
## Seguridad (Confiabilidad)
### Mínimos
- **Validación de Entradas (Inputs):** Validar y sanitizar todas las entradas de datos, tanto a nivel de *frontend* (UX) como en el *backend* (seguridad).
- **Control de Acceso:** Implementar un mecanismo robusto de autenticación y autorización para asegurar que solo los usuarios permitidos puedan acceder a los recursos.
- **Conexiones Seguras:** Asegurar el uso obligatorio de **HTTPS** con certificados SSL/TLS válidos en todas las comunicaciones.
### Way to do it (Reglas de Implementación)
- **OWASP TOP 10 (Web y API):** Implementar cada una de las indicaciones/recomendaciones listadas en el **OWASP TOP 10 de Seguridad** (Web y API).
- **Vulnerabilidades de Librerías:** Implementar **Dependency Pinning** para bibliotecas (fijar versiones) y utilizar herramientas de escaneo de vulnerabilidades (p. ej., SonarQube, Snyk).
- **Ofuscación (Mobile/Frontend):**
  - **Aplicar** minificación y ofuscación solo para *builds* de *release*, no en *debug*.
  - **Generar** archivos de *mapping* por cada *build* para permitir la des-ofuscación de *stack traces*.
  - **Generar** listado de exclusiones para código que no se debe ofuscar (p. ej., reflexión, llamadas dinámicas, código nativo, bibliotecas de terceros).
  - **Validar** el *build* ofuscado comparando el tamaño y probando la des-ofuscación.
---
## Mantenibilidad y Legibilidad (Estandarización)
### Mínimos
- **Código Auto-Documentado:** Escribir código legible, sencillo y conciso. El código debe ser un activo, no un lastre.
- **Nomenclatura Consistente:** Usar nombres claros, descriptivos y consistentes para variables, funciones, clases y archivos.
- **Documentación Mínima:** Documentar el código de forma concisa (comentarios solo si explican el *por qué*, no el *qué*).
- **Estilo de Código:** Seguir las convenciones de estilo del lenguaje (indentación, espacios, etc.) y usar herramientas de formateo.
### Way to do it (Reglas de Desarrollo)
- **Formatters y Linters:**
  - Usar **ESLint** (o equivalente) para análisis de código estático y detección temprana de errores.
  - Usar **Prettier** (o equivalente) para formato de código automático y consistente.
- **Refactorización:** Refactorizar periódicamente para mejorar la legibilidad y mantenimiento del código.
- **Limpieza de Código:** Eliminar código muerto, innecesario o sin uso.
---
## Calidad del Código (Pruebas y Verificación)
### Mínimos
- **Pruebas Unitarias:** Escribir pruebas **antes** de implementar la funcionalidad (Ciclo Red-Green-Refactor, TDD).
- **Cobertura Mínima:** Establecer un porcentaje de cobertura de pruebas unitarias como requisito obligatorio de *build* (Ver **calidad-pipeline-rules.md**).
### Way to do it (Reglas de Desarrollo)
- **TDD (Test-Driven Development):** Seguir el ciclo **Red-Green-Refactor** para el desarrollo de nuevas funcionalidades.
- **Control de Flujo:** Utilizar interceptores (o *middlewares*) para manejar preocupaciones transversales como autenticación, *logging* y manejo de errores.
---
## Rendimiento (Performance)
### Mínimos
- **Monitoreo:** Utilizar herramientas de monitoreo para medir el rendimiento, teniendo en cuenta las métricas específicas de cada plataforma/servicio.
- **Liberación de Recursos:** Siempre liberar los recursos no utilizados (memoria, conexiones, *streams*).
- **Optimización de Procesamiento:** Evitar bloquear el hilo principal de ejecución con tareas de larga duración o de procesamiento costoso.
- **Uso de Recursos:** Evitar el acceso innecesario a recursos externos (servicios o bases de datos) o locales (almacenamiento).
### Way to do it (Reglas de Optimización)
- **Carga de Recursos:**
  - Implementar **Skeleton UI** durante la carga de recursos de interfaz.
  - Realizar un uso correcto de la **Carga Perezosa (*Lazy Loading*)** para posponer recursos o vistas no requeridas inmediatamente.
  - Implementar la **optimización de imágenes** utilizando formatos modernos (WebP, AVIF) y/o tamaños adaptativos.
---
## Trazabilidad y Manejo de Errores (Confiabilidad)
### Mínimos
- **Manejo Controlado de Errores:** Implementar un mecanismo de manejo controlado de errores que **no interrumpa** el funcionamiento del sistema.
- **Monitorización de Errores:** Implementar un servicio de monitoreo remoto (*Observability*) para identificar errores en tiempo real en producción.
- **Feedback al Usuario:** Dar retroalimentación clara, entendible y no técnica al usuario si ocurre un error (no exponer errores no controlados).
### Way to do it (Reglas de Logging y Excepciones)
- **Captura de Errores:**
  - Utilizar bloques **try-catch** y límites de error adecuados para la tecnología.
  - **Evitar ignorar** la excepción de un *try/catch*.
- **Clasificación de Logs:** Usar la clasificación de *logs* adecuadamente (Info, Warning, Error, Debug) al depurar y trazar.
- **Tipado de Errores:**
  - Utilizar excepciones tipadas que describan semánticamente el problema (o fábricas personalizadas).
  - Utilizar el **patrón Result (Success-Failure)** para manejar explícitamente los errores en la capa de negocio.
- **Seguridad en Logs:** Evitar exponer **información sensible** (passwords, tokens, PII) en *logs* o mensajes de error internos.
---
## Experiencia de Usuario y Accesibilidad (Usabilidad)
### Mínimos
- **Diseño Adaptativo (Responsive):** Implementar *media queries* para diseño responsivo.
- **Mobile-First:** Utilizar un enfoque de desarrollo *Mobile-First*.
- **Evitar *Overflow*:** Prevenir el desbordamiento de contenido en pantallas pequeñas.
- **HTML Semántico:** Utilizar **HTML 5 semántico** (cuando aplique a *frontend*).
### Way to do it (Reglas de Interfaz)
- **Accesibilidad:**
  - Añadir etiquetas y roles **ARIA** (**Accessible Rich Internet Applications**).
  - Asegurar el soporte de **navegación por teclado** para todos los elementos interactivos.
- **Estándares de *Styling*:** Usar metodologías como **BEM/SASS** (o equivalentes) para una estructura de estilos consistente y mantenible.
---
## Documentación
### Mínimos
- **README:** Crear y mantener un archivo **README** por repositorio, con la información esencial del proyecto (setup, *scripts* principales, arquitectura).
### Way to do it (Reglas de Artefactos)
- **Arquitectura:** Documentar las decisiones de diseño y la arquitectura del sistema.
- **APIs:** Documentar las APIs de manera formal (p. ej., con **OpenAPI/Swagger**).