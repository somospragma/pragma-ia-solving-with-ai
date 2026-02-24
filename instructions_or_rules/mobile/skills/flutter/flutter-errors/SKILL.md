---
name: flutter-error
description: Skill avanzado para manejo de errores en Flutter con Dart 3.3+, usando fpdart (Either/TaskEither),jerarquía de excepciones con sealed classes, integración con Riverpod y BLoC/Cubit, y manejo de errores globales con FlutterError.onError y PlatformDispatcher. Úsalo siempre que el usuario mencione errores en Flutter, excepciones, Either pattern, Result type, manejo de fallos en APIs REST con Dio, Firebase, bases de datos locales (ObjectBox, Drift/SQLite), crashes inesperados, o cuando pida estructura de archivos para manejo de errores. También aplica cuando el usuario quiera mejorar su arquitectura de errores, refactorizar try/catch dispersos, o implementar error boundaries. Úsalo incluso si el usuario solo menciona "cómo manejar errores en Flutter"sin especificar el patrón exacto.
metadata:
  author: Pragma Mobile Chapter
  version: "1.0"
---

# Flutter Advanced Error

Este documento define las reglas y mejores prácticas para el manejo de errores en aplicaciones Flutter siguiendo los estándares de Pragma.

## Principios de diseño

Estos principios explican el *por qué* detrás de cada decisión — tenlos presentes al generar código:

- **Los errores son valores, no excepciones.** Usar `Either<Failure, T>` en lugar de `throw` permite que el compilador fuerce el manejo de errores en el call site, eliminando los olvidos silenciosos.
- **El dominio no conoce la fuente del error.** Mapear a `Failure` en el datasource antes de que el error suba mantiene la capa de dominio limpia y testeable sin dependencias de Firebase, Dio o SQLite.
- **Todo error tiene un tipo explícito.** Las `sealed class` hacen el pattern matching exhaustivo: si añades un nuevo tipo de error, el compilador señala todos los lugares que lo ignoran.
- **Los mensajes de error se resuelven en la UI.** Los `Failure` cargan una `FailureMessageKey`, no un `String` hardcodeado, porque el idioma solo se conoce en la capa de presentación donde existe `BuildContext`.
- **Los crashes inesperados siempre se capturan.** Registrar `FlutterError.onError` y `PlatformDispatcher.onError` en `main()` garantiza que ningún error escape sin logueo.

---

## Estructura de archivos del proyecto

```
lib/
├── core/
│   ├── errors/
│   │   ├── failures.dart              ← Jerarquía sellada Failure + FailureMessageKey
│   │   ├── exceptions.dart            ← AppException por fuente técnica
│   │   ├── error_handler.dart         ← Mapper Exception → Failure
│   │   └── global_error_handler.dart  ← FlutterError + PlatformDispatcher
│   ├── network/
│   │   └── dio_error_interceptor.dart ← Convierte DioException → AppException
│   ├── l10n/
│   │   └── generated/                 ← Generado por flutter gen-l10n
│   └── widgets/
│       └── failure_view.dart          ← Widget reutilizable de error con i18n
│
├── l10n/
│   ├── app_en.arb                     ← Mensajes de error en inglés (template)
│   └── app_es.arb                     ← Mensajes de error en español
│
└── features/[feature]/
    ├── data/datasources/
    │   └── [x]_datasource.dart        ← TaskEither.tryCatch + ErrorHandler.map
    ├── domain/repositories/
    │   └── [x]_repository.dart        ← Interfaz: Either<Failure, T>
    └── presentation/
        ├── providers/                 ← Riverpod: AsyncNotifier con fold()
        └── bloc/                      ← BLoC: estados sellados con Failure
```

---

## Flujo de un error: de la fuente a la UI

```
[Dio / Firebase / ObjectBox / Drift]
        ↓  lanza excepción técnica (DioException, FirebaseException, etc.)
[Interceptor / Datasource]
        ↓  TaskEither.tryCatch → ErrorHandler.map → Failure con FailureMessageKey
[Repository]
        ↓  retorna Either<Failure, T> al dominio
[UseCase → Provider / BLoC]
        ↓  ejecuta .run() y hace fold() explícito
[UI Widget]
        ↓  failure.localizedMessage(context) → String traducido al locale activo
```

---

## Archivos de referencia

Lee el archivo correspondiente antes de generar código para esa capa:

| Qué implementar | Referencia |
|---|---|
| `Failure`, `FailureMessageKey`, extensiones UI | `references/failures.md` |
| `AppException`, `ErrorHandler`, mapeos HTTP/Firebase/SQLite | `references/exceptions.md` |
| `FailureMessageKey` enum, `Failure` con i18n, `FailureView` | `references/failure_message_key.md` |
| ARB (en/es), `l10n.yaml`, configuración de localizations | `references/i18n_errors.md` |
| Datasources ObjectBox y Drift con `TaskEither`, streams reactivos | `references/local_db_datasources.md` |
| `AsyncNotifier`, `FutureProvider`, `FailureView` con Riverpod | `references/riverpod_integration.md` |
| `Cubit`, `BLoC`, `BlocBuilder`/`BlocListener` con `Failure` | `references/bloc_integration.md` |
| `FlutterError.onError`, `PlatformDispatcher`, `BlocObserver` | `references/global_errors.md` |
| `DioErrorInterceptor`, `AuthInterceptor`, cliente Dio con Riverpod | `references/dio_interceptor.md` |

> `local_db_datasources.md` tiene más de 300 líneas — incluye tabla de contenidos al inicio.

---

## Patrón base en datasources

Todos los datasources siguen este patrón. `ErrorHandler.map` centraliza el mapeo para que el datasource no necesite conocer las reglas de traducción de errores:

```dart
TaskEither<Failure, T> fetchSomething() => TaskEither.tryCatch(
  () async { /* llamada real */ },
  (error, stackTrace) => ErrorHandler.map(error, stackTrace),
);
```

---

## Checklist antes de entregar código

- [ ] Datasource usa `TaskEither.tryCatch` con `ErrorHandler.map`
- [ ] Errores de Dio pasan por `DioErrorInterceptor` antes de llegar al datasource
- [ ] Repository retorna `Either<Failure, T>` — sin `throw` propio
- [ ] BLoC / Notifier hace `fold()` explícito — no `getOrElse` que oculte el Left
- [ ] Estado de error porta un `Failure`, no un `String`
- [ ] `GlobalErrorHandler.initialize()` está llamado en `main()` antes de `runApp`
- [ ] Excepciones de Firebase mapeadas desde `FirebaseException.code`
- [ ] Errores de ObjectBox envueltos en `ObjectBoxException`
- [ ] Errores de Drift envueltos en `DriftException` con `sqliteCode` si está disponible
- [ ] `Failure` usa `FailureMessageKey` — sin `String message` hardcodeado
- [ ] UI llama `failure.localizedMessage(context)` — nunca accede a `literalMessage` directamente
- [ ] Botón "Reintentar" usa `l.retryButton` del ARB
- [ ] Toda clave nueva existe en **ambos** `app_en.arb` y `app_es.arb`
- [ ] Usar importaciones absolutas con `package:` — nunca importaciones relativas (`import '../...'`)
- [ ] Se ejecutó `flutter gen-l10n` tras modificar los ARB
