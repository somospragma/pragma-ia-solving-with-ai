# Core Models — LogEvent, LogLevel, LogHandler

`lib/core/logging/log_level.dart` · `log_event.dart` · `log_handler.dart`

---

## log_level.dart

```dart
/// Niveles de severidad — de menor a mayor impacto.
/// El nivel determina qué handlers reciben el evento (ver LoggerConfig).
enum LogLevel {
  debug,    // Solo dev: trazas detalladas de ejecución
  info,     // Flujo normal: inicialización, configuración
  warning,  // Situaciones inesperadas pero recuperables
  error,    // Fallos manejados: Failure del dominio, errores de red
  fatal;    // Crashes no recuperables: van siempre a Crashlytics + Sentry

  bool operator >=(LogLevel other) => index >= other.index;
}
```

---

## log_event.dart

```dart
import 'log_level.dart';

/// Evento de log estructurado — la unidad de información que viaja
/// desde el call site hasta cada handler. Inmutable y serializable.
final class LogEvent {
  const LogEvent({
    required this.level,
    required this.category,
    required this.message,
    this.context = const {},
    this.error,
    this.stackTrace,
    DateTime? timestamp,
  }) : timestamp = timestamp ?? DateTime.now(); // ignorado si se pasa explícito

  // Nivel de severidad
  final LogLevel level;

  // Categoría semántica — usada para enrutar a handlers específicos
  final LogCategory category;

  // Mensaje corto, legible, en snake_case: 'checkout_failed', 'api_latency'
  final String message;

  // Datos estructurados: producto_id, endpoint, duration_ms, etc.
  final Map<String, Object?> context;

  // Error y stack solo para level >= error
  final Object? error;
  final StackTrace? stackTrace;

  final DateTime timestamp;

  Map<String, Object?> toJson() => {
    'level': level.name,
    'category': category.name,
    'message': message,
    'context': context,
    'timestamp': timestamp.toIso8601String(),
    if (error != null) 'error': error.toString(),
  };
}

/// Categoría semántica — permite enrutar y filtrar en dashboards.
enum LogCategory {
  error,        // Errores y crashes → Crashlytics, Sentry
  navigation,   // Cambios de pantalla → todos los handlers activos
  performance,  // Latencia, duración → DataDog, Grafana
  business,     // Eventos de negocio → DataDog, Grafana
  debug,        // Trazas de desarrollo → solo ConsoleHandler
}
```

---

## log_handler.dart — Interfaz Strategy

```dart
import 'log_event.dart';

/// Contrato que todo handler debe implementar.
/// Cada servicio externo (Crashlytics, Sentry, DataDog, Grafana)
/// es una Strategy concreta de esta interfaz.
abstract interface class LogHandler {
  /// Nombre del handler — usado en logs de diagnóstico y configuración.
  String get name;

  /// Inicializa la conexión con el servicio externo.
  /// Llamar en LoggerConfig.initialize() antes de runApp().
  Future<void> initialize();

  /// Envía el evento al servicio. No lanza excepciones —
  /// los errores de logging nunca deben romper la app.
  Future<void> log(LogEvent event);

  /// Libera recursos al cerrar la app.
  Future<void> dispose();
}
```

---

## Manejo de categorías por handler

Cada handler decide internamente cómo procesar cada categoría según las
capacidades del servicio. El `AppLogger` despacha todos los eventos al
handler activo — es responsabilidad del handler filtrar o transformar.

| Categoría | Comportamiento típico |
|---|---|
| `error` / `fatal` | Todos los handlers lo procesan (crash reports, exceptions) |
| `navigation` | Breadcrumbs en Crashlytics/Sentry, eventos en DataDog/Grafana |
| `performance` | Métricas de latencia — algunos handlers lo ignoran (ej. Crashlytics) |
| `business` | Eventos de negocio — ideal para DataDog/Grafana, ignorado por Crashlytics |
| `debug` | Solo relevante para ConsoleHandler en desarrollo |

> Cada handler implementa su propia lógica en `log(LogEvent event)` para
> decidir qué hacer con cada categoría. Ver `handlers.md` para ejemplos.
