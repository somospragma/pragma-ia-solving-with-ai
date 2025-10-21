# Frontend - Rules para Agentes AI y Desarrolladores

<!-- TODO: Cómo se debe estructurar? por FM, Atributo de Calidad? -->
<!-- TODO: Se deben finalizar los FM, para tener columnas como Atributo de Calidad para filtrar -->

## Accesibilidad

- Use semantic HTML 5
- Add ARIA labels/roles
- Keyboard support

---

## Arquitectura

- Implement Atomic Design Methodology

- Follow SOLID, especially Dependency Inversion

- Follow DRY (Don't repeat yourself) — extract common functionality into shared modules, create reusable components to eliminate code duplication

- Follow YAGNI (You Ain't Gonna Need It) - avoid unnecessary premature optimization

- Follow KISS (Keep It Simple, Stupid) - avoid unnecessary complexity

---

<!-- TODO: Se debería estructurar el MD en Mínimos, buenas prácticas y deseables. -->
## Calidad

- Follow TDD cycle: Red-Green-Refactor
- Write test BEFORE implement functionalities
- Use ESLint for static code analysis and error detection
- Use Prettier for automatic and consistent code formatting

---

## Estándares

- Use interceptors for cross-cutting concerns (auth, logging, error handling)
- Use BEM/SASS modules for consistent styling structure

---

## Experiencia de usuario

-IMPLEMENT media queries for responsive design
-PREVENT content overflow on small screens
-USE a mobile-first approach

---

## Mantenibilidad

- Escribe código legible, sencillo y autodocumentado.
- El código debe ser un activo, no un lastre.
- Usar nombres claros, descriptivos y consistentes para variables, funciones y clases.
- Mantener funciones y métodos cortos, con una única responsabilidad.
- Evitar duplicidad de código; reutiliza funciones y componentes.
- Documentar el código de forma concisa: comentarios solo si explican lo que no es obvio.
- Eliminar código muerto, innecesario o sin uso.
- Preferir estructuras simples y legibles sobre complejas o "ingeniosas".
- Sigue las convenciones de estilo del lenguaje (indentación, espacios, etc.).
- Refactoriza periódicamente para mejorar legibilidad y mantenimiento.

---

## Performance

- Implementar la optimización de imágenes utilizando formatos modernos (WebP, AVIF).
- Implementar Skeleton UI durante la carga de recursos.
- Evita bloquear el hilo principal de ejecucion por tareas de larga duración o de procesamiento costoso.
- Realizar un uso correcto de la carga perezosa para posponer vistas que no son requeridas inmediatamente.
- Siempre liberar los recursos no utilizados.
- Utilizar herramientas de monitoreo para medir el rendimiento, teniendo en cuenta las metricas específicas de cada plataforma.
- Evitar el acceso innecesario a recursos como servicios externos o bases de datos locales.

---

## Seguridad

- Apiicar minificación y obfuscación para builds de release, no en debug.
- Generar archivos de mapping por cada build que se realice, esto es necesario para des-ofuscar stack traces.
- Generar listado de exclusiones y los criterios de exclusión de código que no se debe ofuscar, como código que usa reflexión o invocaciones dinamica, codigo de bibliotecas de terceros, métodos que son llamados desde código nativo (C/C++) deben conservar sus nombres y firmas originales.
- Validar que el buid generado este ofuscado correctamente  implementando la desosfucacion de codigo y su posterior lectura usando el archivo de mapping generado.
- Comparar el tamaño del build generado antes y despues de aplicar la optimización para cuantificar la reducción de tamaño.

- Validate and sanitize inputs

- Implementando un mecanismo de autenticación/autorización

- Implementando cada una de las indicaciones/recomendaciones que se indican en el OWASP TOP 10 de seguridad

- Implementando cada una de las indicaciones/recomendaciones que se indican en el OWASP TOP 10 para APIs

- Implement Dependecy Pinning for libraries

- Ensure HTTPS with SSL/TLS certificates

---

<!-- TODO: FM de Documentación no tiene atributos de calidad. -->
## Documentación

- Creando un archivo README

---

<!-- TODO: Esto NO es trazabilidad. -->
## Trazabilidad

- Implemente siempre un manejo controlado de errores que no interrumpa el funcionamiento del sistema.
- Utilizar bloques try-catch y límites de error adecuados para la tecnología.
- Utilizar tipos de error o fábricas personalizadas.
- Evitar ignorar la excepción de un try/catch.
- Implementar un servicio de monitoreo remoto para identificar errores en tiempo real.
- Usar excepciones tipadas que describan semánticamente el problema.
- Usar la clasificación de logs adecuadamente al depurar errores (Info, Warning, Error, Debug).
- Utilizar el patrón Result (Success-Failure) para manejar explicitamente los errores.
- Dar retroalimentación clara y entendible al usuario si ocurre un error. El usuario no debe percibir errores no controlados.
- Evitar exponer información sensible en logs o mensajes de error internos.

---
