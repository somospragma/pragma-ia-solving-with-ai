# AppLogger — Fachada y LoggerConfig por Flavor

`lib/core/logging/app_logger.dart` · `lib/core/config/logger_config.dart`

---

## app_logger.dart

```dart
import 'dart:async';
import 'package:flutter/foundation.dart';
import 'log_event.dart';
import 'log_level.dart';
import 'log_handler.dart';

/// Fachada pública — único punto de entrada para todo el logging de la app.
///
/// Nunca importes Crashlytics, Sentry, DataDog o Grafana fuera de sus handlers.
/// Todo pasa por aquí. Usa el patrón Strategy: un solo handler activo,
/// intercambiable sin modificar el código cliente.
abstract final class AppLogger {
  static LogHandler? _handler;
  static LogLevel _minLevel = LogLevel.debug;

  /// Handler activo actual — útil para LogSyncWorker.
  static LogHandler? get handler => _handler;

  /// Inicializar con el handler activo para el flavor actual.
  /// Llamar en main() antes de runApp().
  static Future<void> initialize({
    required LogHandler handler,
    LogLevel minLevel = LogLevel.debug,
  }) async {
    _handler = handler;
    _minLevel = minLevel;
    await _handler!.initialize();
  }

  /// Cambiar el handler en runtime (ej. para A/B testing de proveedores).
  /// Llama dispose() en el anterior e initialize() en el nuevo.
  static Future<void> switchHandler(LogHandler newHandler) async {
    await _handler?.dispose();
    _handler = newHandler;
    await _handler!.initialize();
  }

  static Future<void> dispose() async {
    await _handler?.dispose();
  }

  // ─── API pública ────────────────────────────────────────────────────────────

  static Future<void> error(
    String message, {
    Object? error,
    StackTrace? stackTrace,
    Map<String, Object?> context = const {},
  }) =>
      _log(LogEvent(
        level: LogLevel.error,
        category: LogCategory.error,
        message: message,
        error: error,
        stackTrace: stackTrace,
        context: context,
      ));

  static Future<void> fatal(
    String message, {
    Object? error,
    StackTrace? stackTrace,
    Map<String, Object?> context = const {},
  }) =>
      _log(LogEvent(
        level: LogLevel.fatal,
        category: LogCategory.error,
        message: message,
        error: error,
        stackTrace: stackTrace,
        context: context,
      ));

  static Future<void> info(
    String message, {
    Map<String, Object?> context = const {},
  }) =>
      _log(LogEvent(
        level: LogLevel.info,
        category: LogCategory.debug,
        message: message,
        context: context,
      ));

  static Future<void> debug(
    String message, {
    Map<String, Object?> context = const {},
  }) =>
      _log(LogEvent(
        level: LogLevel.debug,
        category: LogCategory.debug,
        message: message,
        context: context,
      ));

  static Future<void> navigation({
    required String from,
    required String to,
    Map<String, Object?> context = const {},
  }) =>
      _log(LogEvent(
        level: LogLevel.info,
        category: LogCategory.navigation,
        message: 'navigate',
        context: {'from': from, 'to': to, ...context},
      ));

  static Future<void> performance(
    String message, {
    required int durationMs,
    Map<String, Object?> context = const {},
  }) =>
      _log(LogEvent(
        level: LogLevel.info,
        category: LogCategory.performance,
        message: message,
        context: {'duration_ms': durationMs, ...context},
      ));

  static Future<void> business(
    String event, {
    Map<String, Object?> context = const {},
  }) =>
      _log(LogEvent(
        level: LogLevel.info,
        category: LogCategory.business,
        message: event,
        context: context,
      ));

  // ─── Internos ───────────────────────────────────────────────────────────────

  static Future<void> _log(LogEvent event) async {
    if (event.level < _minLevel) return;

    if (_handler != null) {
      await _safeLog(_handler!, event);
    }
  }

  /// Los errores de logging nunca deben romper la app.
  static Future<void> _safeLog(LogHandler handler, LogEvent event) async {
    try {
      await handler.log(event);
    } catch (e, st) {
      // Solo en debug — evita bucle infinito de logging de errores de logging
      if (kDebugMode) debugPrint('[AppLogger] ${handler.name} falló: $e\n$st');
    }
  }
}
```

---

## logger_config.dart — handler activo por flavor

```dart
import 'package:flutter/foundation.dart';
import '../logging/app_logger.dart';
import '../logging/log_handler.dart';
import '../logging/handlers/console_handler.dart';
import '../logging/handlers/crashlytics_handler.dart';
import '../logging/handlers/sentry_handler.dart';
import '../logging/handlers/datadog_handler.dart';
import '../logging/handlers/grafana_handler.dart';

enum AppFlavor { dev, staging, prod }

/// Proveedor de logging a usar en staging/prod.
/// Cambiar aquí para migrar de servicio — ningún otro archivo necesita cambios.
enum LogProvider { crashlytics, sentry, datadog, grafana }

abstract final class LoggerConfig {
  /// Proveedor activo para staging/prod.
  /// → CAMBIAR AQUÍ para migrar de servicio de logging.
  static const LogProvider activeProvider = LogProvider.sentry;

  /// Inicializa AppLogger con el handler correcto para el flavor.
  /// Llamar en main() de cada flavor antes de runApp().
  static Future<void> initialize(AppFlavor flavor) async {
    final handler = switch (flavor) {
      // Dev: solo consola, sin ruido en servicios externos
      AppFlavor.dev => ConsoleHandler(),

      // Staging/Prod: usar el proveedor configurado
      AppFlavor.staging || AppFlavor.prod => _buildHandler(flavor),
    };

    await AppLogger.initialize(
      handler: handler,
      minLevel: flavor == AppFlavor.dev ? LogLevel.debug : LogLevel.info,
    );
  }

  /// Construye el handler según el proveedor activo.
  static LogHandler _buildHandler(AppFlavor flavor) {
    final env = flavor == AppFlavor.staging ? 'staging' : 'prod';

    return switch (activeProvider) {
      LogProvider.crashlytics => CrashlyticsHandler(),

      LogProvider.sentry => SentryHandler(
          dsn: flavor == AppFlavor.staging
              ? Env.sentryDsnStaging
              : Env.sentryDsnProd,
        ),

      LogProvider.datadog => DataDogHandler(
          clientToken: Env.datadogToken,
          applicationId: Env.datadogAppId,
          env: env,
        ),

      LogProvider.grafana => GrafanaHandler(
          endpoint: Env.grafanaEndpoint,
          labels: {'app': 'my_app', 'env': env},
        ),
    };
  }
}
```

---

## main.dart — inicialización completa

```dart
// main_prod.dart (cada flavor tiene su propio main)

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Firebase solo si usas Crashlytics
  if (LoggerConfig.activeProvider == LogProvider.crashlytics) {
    await Firebase.initializeApp();
  }

  // Registrar handlers de error global ANTES de runApp
  GlobalErrorHandler.initialize();

  // Inicializar logger con flavor prod
  await LoggerConfig.initialize(AppFlavor.prod);

  runZonedGuarded(
    () => runApp(ProviderScope(child: const MyApp())),
    (error, stack) => AppLogger.fatal('unhandled_error', error: error, stackTrace: stack),
  );
}
```
