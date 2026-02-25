# GrafanaHandler — Grafana Faro

`handlers/grafana_handler.dart`

## Dependencias

### Verificación de versiones de dependencias

**OBLIGATORIO antes de agregar cualquier paquete:**

1. **Consultar pub.dev** — Antes de escribir cualquier dependencia en `pubspec.yaml`, buscar la última versión estable en:
   - [`faro`](https://pub.dev/packages/faro)

2. **Instalar la dependencia** — *El usuario debe ejecutar estos comandos manualmente (NO auto-ejecutar):*

```bash
flutter pub add faro
```

> ⚠️ **IMPORTANTE:** La IA debe mostrar estos comandos al usuario para ejecución manual. No ejecutar automáticamente para evitar versiones desactualizadas.

> Requiere `apiKey` y `collectorUrl` desde **Grafana Cloud → Faro → Setup**. La inicialización de Faro se hace en `main()`, no en el handler.

```dart
import 'dart:io';
import 'package:faro/faro.dart';
import '../log_event.dart';
import '../log_handler.dart';
import '../log_level.dart' as log_level;

/// Envía logs a Grafana Faro.
/// IMPORTANTE: Faro requiere inicialización especial en main() — ver abajo.
final class GrafanaFaroHandler implements LogHandler {
  const GrafanaFaroHandler({
    required this.appName,
    required this.appVersion,
    required this.appEnv,
    required this.apiKey,
    required this.collectorUrl,
    this.collectorHeaders = const {},
  });

  final String appName;
  final String appVersion;
  final String appEnv;
  final String apiKey;
  final String collectorUrl;
  final Map<String, String> collectorHeaders;

  @override
  String get name => 'grafana_faro';

  @override
  Future<void> initialize() async {
    // Faro se inicializa en main() con runApp especial — ver sección de integración
  }

  @override
  Future<void> log(LogEvent event) async {
    switch (event.category) {
      case LogCategory.error:
        Faro().pushError(
          type: event.error?.runtimeType.toString() ?? 'Exception',
          value: event.message,
          stacktrace: event.stackTrace,
          context: _stringifyContext(event.context),
        );

      case LogCategory.navigation:
        Faro().pushEvent(
          'navigation',
          attributes: {
            'from': event.context['from']?.toString() ?? '',
            'to': event.context['to']?.toString() ?? '',
          },
        );

      case LogCategory.performance:
        Faro().pushMeasurement(
          {'duration_ms': event.context['duration_ms'] ?? 0, ...event.context},
          event.message,
        );

      case LogCategory.business:
        Faro().pushEvent(event.message, attributes: _stringifyContext(event.context));

      default:
        Faro().pushLog(event.message, level: _faroLevel(event.level));
    }
  }

  @override
  Future<void> dispose() async {}

  LogLevel _faroLevel(log_level.LogLevel level) => switch (level) {
    log_level.LogLevel.debug   => LogLevel.debug,
    log_level.LogLevel.info    => LogLevel.info,
    log_level.LogLevel.warning => LogLevel.warn,
    log_level.LogLevel.error   => LogLevel.error,
    log_level.LogLevel.fatal   => LogLevel.error,
  };

  Map<String, String> _stringifyContext(Map<String, Object?> ctx) =>
      ctx.map((k, v) => MapEntry(k, v?.toString() ?? ''));
}
```

---

## Captura de duración de eventos

Para medir la duración de operaciones específicas, Faro proporciona métodos para marcar inicio y fin:

```dart
// Marcar inicio de una operación
Faro().markEventStart('api_call', 'fetch_user_profile');

// ... código de la operación ...

// Marcar fin y enviar la medición
Faro().markEventEnd('api_call', 'fetch_user_profile', attributes: {
  'user_id': '123',
  'endpoint': '/api/users/profile',
});
```

### Uso desde AppLogger

Para integrar con el sistema de logging, puedes agregar métodos auxiliares:

```dart
/// Extensión para medir duración de operaciones con Faro.
extension GrafanaPerformanceTracking on GrafanaFaroHandler {
  /// Inicia el tracking de una operación.
  void startTracking(String key, String name) {
    Faro().markEventStart(key, name);
  }

  /// Finaliza el tracking y envía la medición con contexto.
  void endTracking(String key, String name, {Map<String, Object?> context = const {}}) {
    Faro().markEventEnd(key, name, attributes: _stringifyContext(context));
  }

  Map<String, String> _stringifyContext(Map<String, Object?> ctx) =>
      ctx.map((k, v) => MapEntry(k, v?.toString() ?? ''));
}
```

### Ejemplo de uso en un datasource

```dart
Future<User> fetchUserProfile(String userId) async {
  final handler = AppLogger.handler as GrafanaFaroHandler?;
  handler?.startTracking('api', 'fetch_user_profile');

  try {
    final response = await _client.get('/users/$userId');
    return User.fromJson(response.data);
  } finally {
    handler?.endTracking('api', 'fetch_user_profile', context: {'user_id': userId});
  }
}
```

---

## Custom Session Attributes (Opcional)

> ⚠️ **Esta sección es opcional.** La configuración obligatoria está en [Integración en main.dart](#integración-en-maindart-para-grafana-faro). Los `sessionAttributes` son útiles solo si necesitas segmentar datos o agregar metadata personalizada.

Agrega atributos personalizados a todos los datos de sesión. Estos atributos se combinan con los atributos recopilados automáticamente (versión del SDK, versión de Dart, info del dispositivo, etc.) y son útiles para:

- **Control de acceso** — Permisos basados en labels
- **Segmentación de datos** — Labels de equipo, departamento o ambiente
- **Metadata personalizada** — Cualquier información adicional sobre la sesión

```dart
Faro().runApp(
  optionsConfiguration: FaroConfig(
    appName: Env.appName,
    appVersion: Env.appVersion,
    appEnv: 'prod',
    apiKey: Env.faroApiKey,
    collectorUrl: Env.faroCollectorUrl,
    sessionAttributes: {
      'team': 'mobile',
      'department': 'engineering',
      'environment': 'production',
      'cost_center': 1234,           // int - preservado para queries numéricos
      'is_beta_user': true,          // bool - preservado como booleano
    },
  ),
  appRunner: () => runApp(const MyApp()),
);
```

### Notas importantes

- Los atributos personalizados se combinan con los atributos por defecto (`faro_sdk_version`, `device_os`, `device_model`, etc.)
- Los atributos por defecto tienen precedencia si hay conflictos de nombres
- Los atributos de sesión se incluyen en toda la telemetría (logs, eventos, excepciones, traces)

### Manejo de tipos

Los atributos de sesión soportan valores tipados (`String`, `int`, `double`, `bool`):

| Contexto | Comportamiento |
|---|---|
| **Faro session** (`meta.session.attributes`) | Valores convertidos a String según el protocolo Faro |
| **Span resources** (`resource.attributes`) | Tipos preservados (`int`, `double`, `bool`, `String`), habilitando queries numéricos y filtrado en backends de traces |

---

## Integración en `main.dart` para Grafana Faro

Faro requiere envolver `runApp()` con su propio runner:

```dart
// main_prod.dart (cuando activeProvider == LogProvider.grafana)

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Habilitar tracking HTTP
  HttpOverrides.global = FaroHttpOverrides(HttpOverrides.current);

  // Registrar handlers de error global
  GlobalErrorHandler.initialize();

  // Faro envuelve runApp con su propia configuración
  Faro().runApp(
    optionsConfiguration: FaroConfig(
      appName: Env.appName,
      appVersion: Env.appVersion,
      appEnv: 'prod',
      apiKey: Env.faroApiKey,
      collectorUrl: Env.faroCollectorUrl,
      collectorHeaders: {
        // Headers personalizados si son necesarios
      },
    ),
    appRunner: () async {
      // Inicializar logger DESPUÉS de Faro
      await LoggerConfig.initialize(AppFlavor.prod);

      runApp(
        DefaultAssetBundle(
          bundle: FaroAssetBundle(),
          child: FaroUserInteractionWidget(child: const MyApp()),
        ),
      );
    },
  );
}
```
