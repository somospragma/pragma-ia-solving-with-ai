# Errores Globales — FlutterError + PlatformDispatcher

`lib/core/error/global_error_handler.dart` + `main.dart`

---

## global_error_handler.dart

```dart
import 'dart:async';
import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';

abstract final class GlobalErrorHandler {
  /// Configura todos los hooks de error de Flutter.
  /// Llamar ANTES de runApp() — ver main.dart.
  static void initialize() {
    // 1. Errores síncronos del framework Flutter (layout, rendering, etc.)
    FlutterError.onError = (FlutterErrorDetails details) {
      _handle(
        error: details.exception,
        stackTrace: details.stack,
        context: details.context?.toDescription(),
        isFatal: false,
      );
    };

    // 2. Errores asíncronos no capturados en la zona de Flutter
    PlatformDispatcher.instance.onError = (error, stackTrace) {
      _handle(
        error: error,
        stackTrace: stackTrace,
        context: 'PlatformDispatcher',
        isFatal: true,
      );
      return true; // true = error manejado, no re-lanzar
    };
  }

  static void _handle({
    required Object error,
    StackTrace? stackTrace,
    String? context,
    required bool isFatal,
  }) {
    if (kDebugMode) {
      // En debug: mostrar en consola normalmente
      FlutterError.presentError(FlutterErrorDetails(
        exception: error,
        stack: stackTrace,
        context: ErrorDescription(context ?? ''),
      ));
      return;
    }

    // En release: enviar a servicio de monitoreo
    // FirebaseCrashlytics.instance.recordError(
    //   error,
    //   stackTrace,
    //   fatal: isFatal,
    //   information: [context ?? ''],
    // );
    debugPrint('[GlobalError] [$context] $error\n$stackTrace');
  }
}
```

---

## main.dart — configuración completa

```dart
import 'dart:async';
import 'package:flutter/material.dart';
import 'core/error/global_error_handler.dart';

Future<void> main() async {
  // Asegurar binding antes de cualquier operación
  WidgetsFlutterBinding.ensureInitialized();

  // Inicializar Firebase (si aplica)
  // await Firebase.initializeApp(options: DefaultFirebaseOptions.currentPlatform);
  // await FirebaseCrashlytics.instance.setCrashlyticsCollectionEnabled(!kDebugMode);

  // Registrar handlers ANTES de runApp
  GlobalErrorHandler.initialize();

  // Envolver en runZonedGuarded para capturar errores de zonas asíncronas
  // que PlatformDispatcher pueda perderse en algunas versiones
  runZonedGuarded(
    () => runApp(
      ProviderScope(  // o BlocObserver si usas solo BLoC
        child: const MyApp(),
      ),
    ),
    (error, stackTrace) {
      GlobalErrorHandler._handle(  // exponer como método interno si se necesita
        error: error,
        stackTrace: stackTrace,
        context: 'runZonedGuarded',
        isFatal: true,
      );
    },
  );
}
```

---

## BlocObserver global (para proyectos BLoC)

```dart
// lib/core/observers/app_bloc_observer.dart

class AppBlocObserver extends BlocObserver {
  const AppBlocObserver();

  @override
  void onError(BlocBase<dynamic> bloc, Object error, StackTrace stackTrace) {
    super.onError(bloc, error, stackTrace);
    // Errores no capturados en handlers de evento
    debugPrint('[BlocObserver] ${bloc.runtimeType}: $error');
    // FirebaseCrashlytics.instance.recordError(error, stackTrace);
  }

  @override
  void onChange(BlocBase<dynamic> bloc, Change<dynamic> change) {
    super.onChange(bloc, change);
    if (kDebugMode) {
      debugPrint('[BlocObserver] ${bloc.runtimeType}: ${change.nextState}');
    }
  }
}

// En main.dart:
// Bloc.observer = const AppBlocObserver();
```

---

## ErrorWidget personalizado (UI de fallback)

```dart
// En main.dart, dentro de MaterialApp o en main():

// Reemplaza la pantalla roja de errores en debug
ErrorWidget.builder = (FlutterErrorDetails details) {
  return Scaffold(
    backgroundColor: Colors.white,
    body: Center(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.error_outline, size: 64, color: Colors.red),
            const SizedBox(height: 16),
            const Text(
              'Algo salió mal',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            if (kDebugMode)
              Text(
                details.exceptionAsString(),
                textAlign: TextAlign.center,
                style: const TextStyle(fontSize: 12, color: Colors.grey),
              ),
          ],
        ),
      ),
    ),
  );
};
```

---

## ProviderObserver para Riverpod (equivalente al BlocObserver)

```dart
// lib/core/observers/app_provider_observer.dart

class AppProviderObserver extends ProviderObserver {
  const AppProviderObserver();

  @override
  void providerDidFail(
    ProviderBase<Object?> provider,
    Object error,
    StackTrace stackTrace,
    ProviderContainer container,
  ) {
    debugPrint('[ProviderObserver] ${provider.name ?? provider.runtimeType}: $error');
    // FirebaseCrashlytics.instance.recordError(error, stackTrace);
  }
}

// En main.dart:
// ProviderScope(
//   observers: [const AppProviderObserver()],
//   child: const MyApp(),
// )
```
