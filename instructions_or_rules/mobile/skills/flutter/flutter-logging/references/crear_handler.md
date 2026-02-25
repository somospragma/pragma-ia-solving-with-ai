# Crear un handler nuevo

Para agregar un servicio nuevo (ej. Amplitude, Mixpanel), sigue estos pasos:

---

## Paso 1: Agregar dependencias

```bash
flutter pub add amplitude_flutter
flutter pub upgrade --major-versions amplitude_flutter
flutter pub outdated
```

---

## Paso 2: Implementar el handler

```dart
// handlers/amplitude_handler.dart
final class AmplitudeHandler implements LogHandler {
  const AmplitudeHandler({required this.apiKey});
  final String apiKey;

  @override String get name => 'amplitude';

  @override Future<void> initialize() async { /* setup SDK */ }

  @override
  Future<void> log(LogEvent event) async {
    // Cada handler decide qué categorías procesar
    // Amplitude típicamente solo quiere eventos de negocio
    if (event.category != LogCategory.business) return;
    // ... enviar evento
  }

  @override Future<void> dispose() async {}
}
```

---

## Paso 3: Agregar al enum `LogProvider`

En `logger_config.dart`:

```dart
enum LogProvider { crashlytics, sentry, datadog, grafana, amplitude }
```

---

## Paso 4: Agregar case en `_buildHandler()`

```dart
LogProvider.amplitude => AmplitudeHandler(apiKey: Env.amplitudeKey),
```

---

## Paso 5: Cambiar el proveedor activo

```dart
static const LogProvider activeProvider = LogProvider.amplitude;
```

> **Cambiar de proveedor = cambiar una línea.** El código cliente (`AppLogger.error()`, etc.) no cambia.
