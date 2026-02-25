# DataDogHandler — DataDog

`handlers/datadog_handler.dart`

## Dependencias

### Verificación de versiones de dependencias

**OBLIGATORIO antes de agregar cualquier paquete:**

1. **Consultar pub.dev** — Antes de escribir cualquier dependencia en `pubspec.yaml`, buscar la última versión estable en:
   - [`datadog_flutter_plugin`](https://pub.dev/packages/datadog_flutter_plugin)

2. **Instalar la dependencia** — *El usuario debe ejecutar estos comandos manualmente (NO auto-ejecutar):*

```bash
flutter pub add datadog_flutter_plugin
```

> ⚠️ **IMPORTANTE:** La IA debe mostrar estos comandos al usuario para ejecución manual. No ejecutar automáticamente para evitar versiones desactualizadas.

> Requiere `clientToken` y `applicationId` desde **DataDog → UX Monitoring → Setup**. Ajustar `DatadogSite` según región (us1, eu1, etc.).

```dart
import 'package:datadog_flutter_plugin/datadog_flutter_plugin.dart';
import '../log_event.dart' as log_event;
import '../log_handler.dart';
import '../log_level.dart' as log_level;

final class DataDogHandler implements LogHandler {
  DataDogHandler({
    required this.clientToken,
    required this.applicationId,
    required this.env,
    this.site = DatadogSite.us1,
    this.serviceName = 'flutter_app',
  });

  final String clientToken;
  final String applicationId;
  final String env;
  final DatadogSite site;
  final String serviceName;

  late final DatadogLogger _logger;

  @override
  String get name => 'datadog';

  @override
  Future<void> initialize() async {
    final configuration = DatadogConfiguration(
      clientToken: clientToken,
      env: env,
      site: site,
      nativeCrashReportEnabled: true,
      loggingConfiguration: DatadogLoggingConfiguration(),
      rumConfiguration: DatadogRumConfiguration(
        applicationId: applicationId,
      ),
    );

    await DatadogSdk.instance.initialize(configuration, TrackingConsent.granted);

    _logger = DatadogSdk.instance.logs!.createLogger(
      DatadogLoggerConfiguration(
        name: serviceName,
        networkInfoEnabled: true,
        remoteLogThreshold: LogLevel.debug,
      ),
    );
  }

  @override
  Future<void> log(log_event.LogEvent event) async {
    final attrs = Map<String, Object?>.from(event.context)
      ..['category'] = event.category.name
      ..['timestamp'] = event.timestamp.toIso8601String();

    final message = event.message;

    switch (event.level) {
      case log_level.LogLevel.debug:
        _logger.debug(message, attributes: attrs);
      case log_level.LogLevel.info:
        _logger.info(message, attributes: attrs);
      case log_level.LogLevel.warning:
        _logger.warn(message, attributes: attrs);
      case log_level.LogLevel.error:
        _logger.error(
          message,
          errorMessage: event.error?.toString(),
          attributes: attrs,
        );
      case log_level.LogLevel.fatal:
        _logger.error(
          message,
          errorMessage: event.error?.toString(),
          errorKind: 'Fatal',
          attributes: attrs,
        );
    }

    // Métricas de rendimiento como RUM actions
    if (event.category == log_event.LogCategory.performance) {
      DatadogSdk.instance.rum?.addAction(
        RumActionType.custom,
        message,
        attrs,
      );
    }
  }

  @override
  Future<void> dispose() async {}
}
```

---

## Configuración en `main.dart`

Datadog ofrece dos formas de inicialización:

### Opción 1: Usando `DatadogSdk.runApp` (Recomendado)

Configura automáticamente el manejo de errores:

```dart
import 'package:datadog_flutter_plugin/datadog_flutter_plugin.dart';
import 'package:flutter/material.dart';

Future<void> main() async {
  final configuration = DatadogConfiguration(
    clientToken: '<CLIENT_TOKEN>',
    env: '<ENV_NAME>',
    site: DatadogSite.us1,                   // Ajustar según región
    nativeCrashReportEnabled: true,
    loggingConfiguration: DatadogLoggingConfiguration(),
    rumConfiguration: DatadogRumConfiguration(
      applicationId: '<RUM_APPLICATION_ID>',
    ),
  );

  await DatadogSdk.runApp(configuration, TrackingConsent.granted, () async {
    runApp(const MyApp());
  });
}
```

> **Nota:** `clientToken` y `applicationId` se obtienen desde **DataDog → UX Monitoring → Setup**. El `env` corresponde al ambiente (`dev`, `staging`, `prod`).

### Opción 2: Inicialización manual con manejo de errores

Útil si necesitas lógica personalizada antes de `runApp`:

```dart
import 'dart:ui';
import 'package:datadog_flutter_plugin/datadog_flutter_plugin.dart';
import 'package:flutter/material.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  final configuration = DatadogConfiguration(
    clientToken: '<CLIENT_TOKEN>',
    env: '<ENV_NAME>',
    site: DatadogSite.us1,                   // Ajustar según región
    nativeCrashReportEnabled: true,
    loggingConfiguration: DatadogLoggingConfiguration(),
    rumConfiguration: DatadogRumConfiguration(
      applicationId: '<RUM_APPLICATION_ID>',
    ),
  );

  // Capturar errores de Flutter
  final originalOnError = FlutterError.onError;
  FlutterError.onError = (details) {
    FlutterError.presentError(details);
    DatadogSdk.instance.rum?.handleFlutterError(details);
    originalOnError?.call(details);
  };

  // Capturar errores asíncronos no manejados
  final platformOriginalOnError = PlatformDispatcher.instance.onError;
  PlatformDispatcher.instance.onError = (e, st) {
    DatadogSdk.instance.rum?.addErrorInfo(
      e.toString(),
      RumErrorSource.source,
      stackTrace: st,
    );
    return platformOriginalOnError?.call(e, st) ?? false;
  };

  await DatadogSdk.instance.initialize(configuration, TrackingConsent.granted);

  runApp(const MyApp());
}
```

---

## Envío de Logs

Después de inicializar Datadog con `DatadogLoggingConfiguration`, crea una instancia del logger:

```dart
final logger = DatadogSdk.instance.logs?.createLogger(
  DatadogLoggerConfiguration(
    remoteLogThreshold: LogLevel.warning,
  ),
);

logger?.debug("A debug message.");
logger?.info("Some relevant information?");
logger?.warn("An important warning…");
logger?.error("An error was met!");
```

### Logger con nombre y servicio personalizado

```dart
final secondLogger = DatadogSdk.instance.logs?.createLogger(
  DatadogLoggerConfiguration(
    service: 'my_app.additional_logger',
    name: 'Additional logger',
  ),
);

secondLogger?.info('Info from my additional logger.');
```

> **Nota:** Tags y atributos configurados en loggers son locales a cada logger.

---

## Track RUM Views

Datadog puede rastrear automáticamente rutas nombradas usando `DatadogNavigationObserver`:

```dart
MaterialApp(
  home: HomeScreen(),
  navigatorObservers: [
    DatadogNavigationObserver(DatadogSdk.instance),
  ],
);
```

### Personalizar nombres de vistas

Para renombrar vistas o proveer paths personalizados:

```dart
RumViewInfo? infoExtractor(Route<dynamic> route) {
  var name = route.settings.name;
  if (name == 'my_named_route') {
    return RumViewInfo(
      name: 'MyDifferentName',
      attributes: {'extra_attribute': 'attribute_value'},
    );
  }
  return defaultViewInfoExtractor(route);
}

var observer = DatadogNavigationObserver(
  datadogSdk: DatadogSdk.instance,
  viewInfoExtractor: infoExtractor,
);
```

### Usando `DatadogRouteAwareMixin`

Para control manual de vistas RUM:

```dart
class _MyHomeScreenState extends State<MyHomeScreen>
    with RouteAware, DatadogRouteAwareMixin {

  @override
  RumViewInfo get rumViewInfo => RumViewInfo(name: 'MyHomeScreen');
}
```

> **Nota:** Con código ofuscado, el nombre del widget se pierde. Usa `rumViewInfo` para mantener nombres correctos.

---

## Automatic Resource Tracking

Habilita tracking automático de recursos y llamadas HTTP:

```dart
final configuration = DatadogConfiguration(
  // ... otras configuraciones
  firstPartyHosts: ['example.com'],
)..enableHttpTracking();
```

> **Nota:** `firstPartyHosts` debe configurarse para habilitar Datadog Distributed Tracing. Puedes modificar el sampling rate con `traceSampleRate` en `DatadogRumConfiguration`.

---

## Tracking desde Background Isolates

Si el proyecto usa `Isolate` para trabajo en segundo plano:

```dart
import 'dart:isolate';
import 'package:datadog_flutter_plugin/datadog_flutter_plugin.dart';

Future<void> spawnBackgroundIsolate() async {
  final receivePort = ReceivePort();
  receivePort.listen((message) {
    // Procesar mensajes del isolate
  });
  await Isolate.spawn(_backgroundWork, receivePort.sendPort);
}

void _backgroundWork(SendPort port) async {
  // Adjuntar Datadog al isolate de background
  await DatadogSdk.instance.attachToBackgroundIsolate();

  // Tu trabajo en segundo plano aquí
  // Los logs y eventos RUM se enviarán correctamente
}
```

> **Nota:** Llamar `attachToBackgroundIsolate()` es obligatorio para que Datadog capture logs y eventos desde isolates secundarios.
