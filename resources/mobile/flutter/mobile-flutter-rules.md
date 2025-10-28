# Mobile Flutter Developer Rules

```yaml
name: "flutter best practices"
version: "1.0"
applies_to: ["mobile", "flutter", "developer" , "dart"]
status: "Active"
authors:
  - name: "darry.morales"
    email: "darry.morales@pragma.com.co"
tags: ["Mobile","Flutter", "Dart"]
last_updated: "2025-10-21"
```

## Mantenibilidad

- Usar patrones de arquitecturas limpias que permitan separación de responsabilidades.
- Organizar el código por capas independientes de frameworks, bases de datos e interfaces externas.
- Centralizar lógica de negocio sin generar dependencia directa del resto de capas.
- Establecer las reglas de dependencias desde las capas más externas hacia las capas más internas. Las capas internas no deben conocer las capas más externas.
- Mantener una alta cohesión y bajo acoplamiento entre las capas.
- Depender de abstracciones (interfaces o clases abstractas) y no de implementaciones concretas.
- Utilizar estrategias de inyección de dependencias para favorecer las pruebas del código.
- Evitar dependencias innecesarias.
- Arquitectura limpia: 3 capas, presentation, domain, data.
- Repository depende de abstracción de datasource.
- UseCase depende de abstracción de Repository.
- BloC o Provider depende de abstracción de UseCase.
- Entrega un BLoC por caso de uso, sin filtrar eventos de UI en la capa de dominio.
- Gestor de inyección de dependencias mediante Get_it.
- Configuración para ambientes de compilación mediante Flavors y Schemes.
- Agrega un README explicando las reglas de dependencias.
- Centralización de labels y configuración para internacionalización.
- Los modelos de datos y estados deben ser inmutables; todas las propiedades deben ser final.
- La capa Domain debe ser Dart puro, sin dependencias de Flutter.
- Versión fija de paquetes en pubspec.yaml; usar rangos solo para paquetes muy mantenidos.
- Los modelos de datos deben incluir métodos copyWith, fromJson y toJson, preferentemente usando herramientas de generación de código.
- Los repositorios deben ser la única fuente de acceso a datos y abstraer todas las fuentes de datos.
- Un BLoC o Cubit solo debe depender de abstracciones de casos de uso (UseCase) de la capa Domain; nunca debe acceder directamente a un repositorio.
- Las pruebas unitarias deben seguir el patrón Arrange-Act-Assert (AAA).
- Usar configuración personalizada para linters y análisis estático de código usando librerías o herramientas propias de la tecnología.
- Implementar las dependencias únicamente para compilación de desarrollo.
- Validar reglas y guías de estilo de codificación según la necesidad del proyecto.
- Implementar la dependencia flutter_lints.
- Integrar las reglas sugeridas en el archivo analysis_options.yaml.
- Validar la ejecución de las reglas de análisis con flutter analyze.
- Generar correcciones automáticas con el comando: `dart fix --apply`.
- Escribe código legible, sencillo y autodocumentado.
- El código debe ser un activo, no un lastre.
- Usar nombres claros, descriptivos y consistentes para variables, funciones y clases.
- Mantener funciones y métodos cortos, con una única responsabilidad.
- Evitar duplicidad de código; reutiliza funciones y componentes.
- Documentar el código de forma concisa: comentarios solo si explican lo que no es obvio.
- Eliminar código muerto, innecesario o sin uso.
- Preferir estructuras simples y legibles sobre complejas o “ingeniosas”.
- Sigue las convenciones de estilo del lenguaje (indentación, espacios, etc.).
- Refactoriza periódicamente para mejorar legibilidad y mantenimiento.
- Todo el codigo debe satisfacer los principios SOLID.
- Nombres de variables bajo camelCase.
- Nombres de clases bajo PascalCase.
- Nombres de archivo bajo snake_case.
- Indentación equivalente a 2 espacios.
- Condicionales y bucles envueltos por `{ }`.
- Documentación de clases, métodos de lógica compleja con ///
- Incluye comentarios con /// para API pública y ejemplos mínimos.
- No usar valores mágicos: define todas las constantes en una ubicación centralizada.
- Nunca dejar código comentado; debe eliminarse antes de hacer merge.
- Todos los commits deben seguir la especificación Conventional Commits.

## Trazabilidad

- Implemente siempre un manejo controlado de errores que no interrumpa el funcionamiento del sistema.
- Utilizar bloques try-catch y límites de error adecuados para la tecnología.
- Utilizar tipos de error o fábricas personalizadas.
- Evitar ignorar la excepción de un try/catch.
- Implementar un servicio de monitoreo remoto para identificar errores en tiempo real.
- Usar excepciones tipadas que describan semánticamente el problema.
- Usar la clasificación de logs adecuadamente al depurar errores (Info, Warning, Error, Debug).
- Utilizar el patrón Result (Success-Failure) para manejar explícitamente los errores.
- Dar retroalimentación clara y entendible al usuario si ocurre un error. El usuario no debe percibir errores no controlados.
- Evitar exponer información sensible en logs o mensajes de error internos.
- Validar adecuadamente los valores nulos usando los operadores null-aware del lenguaje Dart (`?`, `??`, `!`).
- Define valores por defecto al mapear objetos desde fuentes de datos externas para evitar errores por datos nulos.
- En BLoC, diferencia alertas (no bloqueantes) y modal (bloqueantes).
- No lanzar el objeto Exception de forma explícita, crea subclases descriptivas.
- Utilizar clases selladas para implementar Either y Optional.
- No usar lenguaje técnico en mensajes de feedback al usuario.
- No usar print para depurar la aplicación, utiliza el paquete developer oficial.
- Utiliza herramientas de monitoreo remoto como Crashlytics o Sentry según documentación oficial.

## Performance

- Optimizar imágenes utilizando formatos modernos (WebP, AVIF).
- Implementar Skeleton UI durante la carga de recursos.
- Evita bloquear el hilo principal con tareas de larga duración o procesamiento costoso.
- Usa carga perezosa para posponer vistas no requeridas inmediatamente.
- Libera recursos no utilizados siempre.
- Utiliza herramientas de monitoreo para medir el rendimiento según la plataforma.
- Evita acceso innecesario a servicios externos o bases de datos locales.
- Usa `const` siempre que sea posible para evitar reconstrucciones innecesarias en widgets.
- Utiliza el widget Container solo si requiere tres o más atributos o propiedades únicas.
- No uses Container para espacios vacíos, usa SizedBox.shrink.
- Carga widgets de forma perezosa usando ListView.builder, GridView.builder y PageView.builder.
- Evita el uso de shrinkWrap en widgets de carga perezosa.
- Evita reconstrucciones (setState, BloC, Riverpod) en lugares altos del árbol de widgets; hazlas en los nodos hoja.
- Prioriza el uso de StatelessWidget; usa StatefulWidget para animaciones, formularios, etc.
- Usa ValueNotifier sobre SetState en StatefulWidget.
- Utiliza Isolates para paralelizar tareas bloqueantes.
- Optimiza imágenes usando WebP y SVG.
- Usa variables de entorno para definir constantes resueltas en tiempo de compilación para mejorar Tree Shaking.
- Si usas controladores (StreamController, TextEditingController, etc.) llama a dispose() al cerrar la vista.
- Usa DevTools para monitorear el rendimiento y detectar fallos en el manejo de recursos.

## Seguridad

- Validar y sanear toda entrada de usuario y datos externos.
- Proteger credenciales y datos sensibles; nunca exponerlos en código o almacenamiento inseguro.
- Usa mecanismos seguros para el almacenamiento de credenciales.
- Usar cifrado seguro para los datos requeridos en reposo y en tránsito.
- Usar comunicación segura (HTTPS/TLS) en todas las conexiones.
- Implementar controles de acceso y autorización en backend.
- Mantener dependencias y librerías actualizadas y libres de vulnerabilidades conocidas.
- Prevenir vulnerabilidades comunes (XSS, CSRF, inyección de código, clickjacking).
- Manejar errores y excepciones sin exponer información interna o sensible.
- No registrar ni mostrar datos sensibles en logs, mensajes de error ni interfaces públicas.
- Las variables de ambiente de compilación deben almacenarse como secretos en el CI/CD o servicios especializados de gestión de secretos.
- Prevenir amenazas tipificadas en OWASP Mobile Application Security 2024.
- Aplicar minificación y ofuscación para builds de release, no en debug.
- Generar archivos de mapping por cada build para des-ofuscar stack traces.
- Generar listado y criterios de exclusión de código que no se debe ofuscar (código con reflexión, invocaciones dinámicas, bibliotecas de terceros, métodos llamados desde nativo deben conservar nombre y firma).
- Validar la ofuscación del build con desofuscación y lectura del archivo de mapping.
- Comparar el tamaño del build antes y después de optimización para cuantificar reducción.
- Deshabilitar logs DEBUG verbosos en builds de producción.

## Documentación

- Procurar un README claro, conciso pero detallado en cada proyecto.
