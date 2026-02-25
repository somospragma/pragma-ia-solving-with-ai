# CrashlyticsHandler — Firebase Crashlytics

`handlers/crashlytics_handler.dart`

## Dependencias

### Verificación de versiones de dependencias

**OBLIGATORIO antes de agregar cualquier paquete:**

1. **Consultar pub.dev** — Antes de escribir cualquier dependencia en `pubspec.yaml`, buscar la última versión estable en:
   - [`firebase_crashlytics`](https://pub.dev/packages/firebase_crashlytics)
   - [`firebase_analytics`](https://pub.dev/packages/firebase_analytics)

2. **Instalar la dependencia** — *El usuario debe ejecutar estos comandos manualmente (NO auto-ejecutar):*

```bash
flutter pub add firebase_crashlytics firebase_analytics
```

> ⚠️ **IMPORTANTE:** La IA debe mostrar estos comandos al usuario para ejecución manual. No ejecutar automáticamente para evitar versiones desactualizadas.

> Requiere configuración adicional: `flutterfire configure` y agregar `google-services.json` (Android) / `GoogleService-Info.plist` (iOS).

```dart
import 'package:firebase_crashlytics/firebase_crashlytics.dart';
import '../log_event.dart';
import '../log_handler.dart';

/// Envía errores y fatales a Firebase Crashlytics.
/// Los eventos de navegación se registran como breadcrumbs (custom keys).
final class CrashlyticsHandler implements LogHandler {
  @override
  String get name => 'crashlytics';

  @override
  Future<void> initialize() async {
    await FirebaseCrashlytics.instance
        .setCrashlyticsCollectionEnabled(true);
  }

  @override
  Future<void> log(LogEvent event) async {
    // Añadir contexto como custom keys para cada reporte
    event.context.forEach((key, value) {
      FirebaseCrashlytics.instance.setCustomKey(key, value?.toString() ?? '');
    });

    switch (event.category) {
      case LogCategory.error:
        await FirebaseCrashlytics.instance.recordError(
          event.error ?? event.message,
          event.stackTrace,
          reason: event.message,
          fatal: event.level == LogLevel.fatal,
          information: [event.context.toString()],
        );

      case LogCategory.navigation:
        // Breadcrumb de navegación — ayuda a reconstruir el flujo antes del crash
        FirebaseCrashlytics.instance.log(
          'NAV: ${event.context['from']} → ${event.context['to']}',
        );

      default:
        FirebaseCrashlytics.instance.log(
          '[${event.level.name}] ${event.message}',
        );
    }
  }

  @override
  Future<void> dispose() async {}
}
```

---

## Manejo de errores fatales de Flutter

Para capturar todos los errores no manejados (síncronos y asíncronos), configura los handlers globales en `main()`:

```dart
import 'dart:ui';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_crashlytics/firebase_crashlytics.dart';
import 'package:flutter/material.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();

  // Opción 1: Forma simplificada — pasa todos los errores fatales directamente
  FlutterError.onError = FirebaseCrashlytics.instance.recordFlutterFatalError;

  // Opción 2: Con acceso a errorDetails — útil si necesitas lógica adicional
  // FlutterError.onError = (errorDetails) {
  //   // Aquí puedes agregar lógica personalizada antes de reportar
  //   FirebaseCrashlytics.instance.recordFlutterFatalError(errorDetails);
  // };

  // Capturar errores asíncronos no manejados por el framework de Flutter
  PlatformDispatcher.instance.onError = (error, stack) {
    FirebaseCrashlytics.instance.recordError(error, stack, fatal: true);
    return true;
  };

  runApp(const MyApp());
}
```

### Notas importantes

- **`FlutterError.onError`** — Captura errores síncronos del framework de Flutter (widgets, rendering, etc.)
- **`PlatformDispatcher.instance.onError`** — Captura errores asíncronos no manejados (Futures, Isolates, etc.)
- Ambos deben configurarse **antes** de `runApp()` para garantizar cobertura completa
- `recordFlutterFatalError` automáticamente marca el error como fatal y extrae el stack trace del `FlutterErrorDetails`
