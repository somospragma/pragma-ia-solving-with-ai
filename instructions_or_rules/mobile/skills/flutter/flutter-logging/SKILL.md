---
name: flutter-logging
description: Skill avanzado para logging en Flutter con Dart 3.3+, usando el patrón Strategy (GoF) para intercambiar handlers de logging (Firebase Crashlytics, Sentry, DataDog, Grafana Faro) sin cambiar el código cliente. Incluye un Logger central como fachada única,niveles de severidad, logging de navegación, métricas de rendimiento y eventos de negocio, separado por flavors (dev/staging/prod). Úsalo siempre que el usuario mencione logging, logs, monitoreo, Crashlytics, Sentry, DataDog, Grafana, errores en producción, analytics, métricas de API, trazas de navegación, eventos de negocio, o quiera configurar observabilidad en Flutter. También aplica cuando el usuario quiera cambiar de servicio de logging, agregar un nuevo handler, o desacoplar el logging de un proveedor específico.
metadata:
  author: Pragma Mobile Chapter
  version: "1.0"
---

# Flutter Advanced Logging

Este documento define las reglas y mejores prácticas para implementar logging en aplicaciones Flutter siguiendo los estándares de Pragma.

## Principios de diseño

- **El código cliente nunca conoce el handler.** El `AppLogger` es la única fachada — ningún widget, BLoC ni usecase importa Crashlytics, Sentry o DataDog directamente. Esto permite cambiar o combinar servicios sin tocar la lógica de negocio.
- **Cada servicio es una Strategy intercambiable.** `LogHandler` define el contrato; `CrashlyticsHandler`, `SentryHandler`, `DataDogHandler` y `GrafanaHandler` lo implementan. El Logger mantiene **un solo handler activo** — cambiar de proveedor es tan simple como modificar una línea en `LoggerConfig`.
- **El ambiente determina qué handler se activa.** Dev usa `ConsoleHandler`. Staging y Prod usan el proveedor elegido (Crashlytics, Sentry, DataDog o Grafana). Esta decisión vive en la capa de configuración (`LoggerConfig`), no en el Logger.
- **Los logs tienen tipo semántico.** Un `LogEvent` no es solo un String — porta nivel, categoría (`error`, `navigation`, `performance`, `business`), contexto estructurado y timestamp. El handler activo decide cómo procesar cada categoría según las capacidades del servicio.

---

## Estructura de archivos del proyecto

```
lib/
├── core/
│   └── logging/
│       ├── app_logger.dart           ← Fachada pública — único punto de entrada
│       ├── log_event.dart            ← Modelo de evento estructurado
│       ├── log_level.dart            ← Enum: debug, info, warning, error, fatal
│       ├── log_handler.dart          ← Interfaz Strategy (contrato de cada handler)
│       ├── handlers/
│       │   ├── console_handler.dart     ← Dev: pretty-print en consola
│       │   ├── crashlytics_handler.dart ← Firebase Crashlytics
│       │   ├── sentry_handler.dart      ← Sentry
│       │   ├── datadog_handler.dart     ← DataDog
│       │   └── grafana_handler.dart     ← Grafana (HTTP)
├── core/
│   └── config/
│       └── logger_config.dart        ← Qué handlers se activan por flavor
│
└── features/[feature]/
    ├── presentation/
    │   ├── providers/                ← Riverpod: loguear desde Notifiers
    │   └── bloc/                     ← BLoC: loguear desde event handlers
    └── data/datasources/             ← Loguear latencia y errores de red
```

---

## Flujo de un log: del call site al servicio

```
AppLogger.error() / .info() / .navigation() / .performance()
        ↓  construye LogEvent estructurado
[LogHandler activo según LoggerConfig]
        ↓  ConsoleHandler (dev) | CrashlyticsHandler | SentryHandler | DataDogHandler | GrafanaHandler
```

---

## Archivos de referencia

Lee el archivo correspondiente antes de generar código para esa área:

| Qué implementar | Referencia |
|---|---|
| `LogEvent`, `LogLevel`, interfaz `LogHandler` (Strategy) | `references/core_models.md` |
| `AppLogger` fachada + `LoggerConfig` por flavor | `references/app_logger.md` |
| `ConsoleHandler`, `CrashlyticsHandler`, `SentryHandler`, `DataDogHandler`, `GrafanaHandler` | `references/console_handler.md`, `references/crashlytics_handler.md`, `references/sentry_handler.md`, `references/datadog_handler.md`, `references/grafana_handler.md` |
| Logging desde Riverpod, BLoC, datasources y navegación | `references/integration.md` |

---

## Uso básico desde cualquier capa

```dart
// Error con contexto estructurado (se enruta a Crashlytics + Sentry)
AppLogger.error(
  'checkout_failed',
  context: {'product_id': id, 'amount': total},
  error: failure,
  stackTrace: stackTrace,
);

// Evento de negocio (se enruta a DataDog + Grafana)
AppLogger.business('purchase_completed', context: {'revenue': 99.9});

// Métrica de rendimiento (latencia de API)
AppLogger.performance('api_latency', durationMs: elapsed, context: {'endpoint': '/orders'});

// Navegación (se enruta a todos los handlers activos)
AppLogger.navigation(from: 'HomeScreen', to: 'CheckoutScreen');
```

---

## Checklist antes de entregar código

- [ ] Ningún widget, BLoC ni usecase importa Crashlytics, Sentry, DataDog o Grafana directamente
- [ ] Todo log pasa por `AppLogger` — nunca `debugPrint` o `print` sueltos en producción
- [ ] **Dependencias siempre en la última versión estable de pub.dev:**
  1. Antes de agregar cualquier paquete, consultar https://pub.dev/packages/<paquete> para identificar la **última versión estable publicada** (ignorar prereleases/dev).
  2. **NUNCA ejecutar automáticamente** los comandos de instalación de dependencias. La IA debe **mostrar los comandos al usuario** para que los ejecute manualmente (botón RUN/Ejecutar). Esto evita que se instalen versiones desactualizadas del cache de la IA.
  3. Agregar con `flutter pub add <paquete>`.
  4. Ejecutar `flutter pub upgrade --major-versions <paquete>` para permitir saltos de versión mayor.
  5. Validar con `flutter pub outdated` que la versión instalada coincide con la última estable de pub.dev.
  6. Si `pub outdated` muestra una versión inferior a la publicada en pub.dev, ajustar el `environment.sdk` en `pubspec.yaml` o resolver conflictos de constraints hasta alcanzar la versión más reciente.
- [ ] Usar importaciones absolutas con `package:` — nunca importaciones relativas (`import '../...'`)
- [ ] `LoggerConfig` define el handler activo por flavor — no hay `if (kDebugMode)` dispersos
- [ ] Cada `LogHandler` implementa `dispose()` para liberar recursos al cerrar la app
- [ ] Los logs de error incluyen siempre `error` y `stackTrace` — nunca solo el mensaje
- [ ] Los eventos de negocio usan claves snake_case consistentes — facilita los dashboards
- [ ] En dev, `ConsoleHandler` está activo — los servicios externos no reciben ruido de desarrollo
- [ ] Cambiar de proveedor requiere solo modificar `LoggerConfig.handler` — ningún otro archivo cambia
