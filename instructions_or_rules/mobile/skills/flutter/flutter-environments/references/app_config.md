# AppConfig — Configuración tipada, envied y entry points

`lib/core/config/` · `lib/main_*.dart`

---

## app_flavor.dart

```dart
enum AppFlavor { dev, staging, prod }
```

---

## Archivos .env — estructura y .gitignore

### .env.example (commiteado — documentación)

```dotenv
# API
API_BASE_URL=https://api.example.com
API_KEY=your_api_key_here

# Firebase Crashlytics — configuración via google-services.json
# No requiere variables adicionales aquí, solo habilitar el plugin en build.gradle.kts

# Feature flags
ENABLE_NEW_CHECKOUT=false
ENABLE_ANALYTICS=false
```

### .gitignore — entries requeridos

```gitignore
# Environments — nunca commitear
.env
.env.*
!.env.example

# Generados por envied — contienen los valores ofuscados
lib/core/config/env_dev.g.dart
lib/core/config/env_staging.g.dart
lib/core/config/env_prod.g.dart

# Android signing
android/key.properties
android/*.jks
android/*.keystore

# iOS signing
ios/certs/
*.p12
*.mobileprovision
```

---

## envied — definición por flavor

`pubspec.yaml`:
```yaml
dependencies:
  envied: ^0.5.4

dev_dependencies:
  envied_generator: ^0.5.4
  build_runner: ^2.4.0
```

### env_dev.dart

```dart
import 'package:envied/envied.dart';

part 'env_dev.g.dart';

// obfuscate: true embebe los valores XOR-encriptados en el binario.
// Nunca aparecen como strings en texto plano en el APK/IPA.
@Envied(path: '.env.dev', obfuscate: true)
abstract final class EnvDev {
  @EnviedField(varName: 'API_BASE_URL')
  static final String apiBaseUrl = _EnvDev.apiBaseUrl;

  @EnviedField(varName: 'API_KEY')
  static final String apiKey = _EnvDev.apiKey;

  @EnviedField(varName: 'ENABLE_NEW_CHECKOUT', defaultValue: false)
  static final bool enableNewCheckout = _EnvDev.enableNewCheckout;

  @EnviedField(varName: 'ENABLE_ANALYTICS', defaultValue: false)
  static final bool enableAnalytics = _EnvDev.enableAnalytics;
}
```

Replicar como `env_staging.dart` y `env_prod.dart` apuntando a `.env.staging` y `.env.prod`.

### Generación de código

```bash
# Regenerar tras cambiar un .env o una clase @Envied
dart run build_runner build --delete-conflicting-outputs
```

---

## app_config.dart — objeto tipado único

```dart
import 'app_flavor.dart';
import 'env_dev.dart';
import 'env_staging.dart';
import 'env_prod.dart';

/// Configuración de la app por flavor — único punto de acceso.
/// Ninguna capa importa EnvDev/Staging/Prod directamente fuera de aquí.
///
/// Firebase Crashlytics no requiere configuración en AppConfig —
/// se inicializa automáticamente via google-services.json por flavor.
final class AppConfig {
  const AppConfig._({
    required this.flavor,
    required this.appName,
    required this.apiBaseUrl,
    required this.apiKey,
    required this.featureFlags,
  });

  final AppFlavor flavor;
  final String appName;
  final String apiBaseUrl;
  final String apiKey;
  final FeatureFlags featureFlags;

  static AppConfig forFlavor(AppFlavor flavor) => switch (flavor) {
    AppFlavor.dev => AppConfig._(
        flavor:       AppFlavor.dev,
        appName:      'MyApp Dev',
        apiBaseUrl:   EnvDev.apiBaseUrl,
        apiKey:       EnvDev.apiKey,
        featureFlags: FeatureFlags(
          newCheckout: EnvDev.enableNewCheckout,
          analytics:   EnvDev.enableAnalytics,
        ),
      ),
    AppFlavor.staging => AppConfig._(
        flavor:       AppFlavor.staging,
        appName:      'MyApp Staging',
        apiBaseUrl:   EnvStaging.apiBaseUrl,
        apiKey:       EnvStaging.apiKey,
        featureFlags: FeatureFlags(
          newCheckout: EnvStaging.enableNewCheckout,
          analytics:   EnvStaging.enableAnalytics,
        ),
      ),
    AppFlavor.prod => AppConfig._(
        flavor:       AppFlavor.prod,
        appName:      'MyApp',
        apiBaseUrl:   EnvProd.apiBaseUrl,
        apiKey:       EnvProd.apiKey,
        featureFlags: FeatureFlags(
          newCheckout: EnvProd.enableNewCheckout,
          analytics:   EnvProd.enableAnalytics,
        ),
      ),
  };
}

final class FeatureFlags {
  const FeatureFlags({
    required this.newCheckout,
    required this.analytics,
  });
  final bool newCheckout;
  final bool analytics;
}
```

---

## Entry points — un main.dart por flavor

### main_dev.dart

```dart
import 'package:flutter/material.dart';
import 'core/config/app_config.dart';
import 'core/config/app_flavor.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  final config = AppConfig.forFlavor(AppFlavor.dev);

  // Firebase — usa google-services.json de src/dev/ automáticamente
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );

  // Logger — solo ConsoleSink en dev (ver skill flutter-advanced-logging)
  await LoggerConfig.initialize(AppFlavor.dev, logQueueDao);

  // Error handler global (ver skill flutter-error-handling)
  GlobalErrorHandler.initialize();

  runApp(
    ProviderScope(
      overrides: [appConfigProvider.overrideWithValue(config)],
      child: const MyApp(),
    ),
  );
}
```

Replicar como `main_staging.dart` y `main_prod.dart` pasando `AppFlavor.staging` / `AppFlavor.prod`.

---

## AppConfig en Riverpod

```dart
// lib/core/config/app_config_provider.dart
final appConfigProvider = Provider<AppConfig>(
  (_) => throw UnimplementedError('Override in ProviderScope at main'),
);

// Consumo desde cualquier capa:
final config = ref.read(appConfigProvider);
final apiUrl = config.apiBaseUrl;
```
