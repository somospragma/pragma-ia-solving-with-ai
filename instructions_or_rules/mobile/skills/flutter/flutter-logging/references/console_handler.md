# ConsoleHandler — Desarrollo

`handlers/console_handler.dart`

**Dependencias:** Ninguna adicional (usa `flutter/foundation.dart` del SDK).

```dart
import 'package:flutter/foundation.dart';
import '../log_event.dart';
import '../log_handler.dart';

/// Pretty-print en consola. Solo activo en dev.
/// Formatea los eventos para que sean fáciles de leer en el IDE.
final class ConsoleHandler implements LogHandler {
  @override
  String get name => 'console';

  @override
  Future<void> initialize() async {} // sin setup

  @override
  Future<void> log(LogEvent event) async {
    if (!kDebugMode) return; // nunca en release, por si acaso
    final icon = _icon(event.level);
    final ctx = event.context.isEmpty ? '' : ' | ${event.context}';
    final err = event.error != null ? '\n  ↳ ${event.error}' : '';
    debugPrint('$icon [${event.category.name}] ${event.message}$ctx$err');
  }

  @override
  Future<void> dispose() async {}

  String _icon(LogLevel level) => switch (level) {
    LogLevel.debug   => '🔍',
    LogLevel.info    => 'ℹ️',
    LogLevel.warning => '⚠️',
    LogLevel.error   => '🔴',
    LogLevel.fatal   => '💀',
  };
}
```
