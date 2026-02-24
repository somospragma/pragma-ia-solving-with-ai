# Feature Flags por Ambiente

`lib/core/config/app_config.dart` → `FeatureFlags`

---

## Principio

Los feature flags controlan qué funcionalidades están activas en cada ambiente.
Viven en `AppConfig` como campos tipados de `FeatureFlags` — no hay `if (flavor == 'prod')`
dispersos en el código de negocio. Esto permite activar una feature en staging para QA
sin tocar prod, o hacer rollout gradual cambiando solo el `.env`.

---

## Definición en .env

```dotenv
# .env.dev
ENABLE_NEW_CHECKOUT=true      # Activo en dev para desarrollo
ENABLE_ANALYTICS=false        # Apagado en dev para no contaminar datos
ENABLE_BIOMETRIC_AUTH=true
ENABLE_DARK_MODE_V2=true

# .env.staging
ENABLE_NEW_CHECKOUT=true      # Activo en staging para QA
ENABLE_ANALYTICS=true
ENABLE_BIOMETRIC_AUTH=true
ENABLE_DARK_MODE_V2=false

# .env.prod
ENABLE_NEW_CHECKOUT=false     # Apagado en prod hasta validar en staging
ENABLE_ANALYTICS=true
ENABLE_BIOMETRIC_AUTH=true
ENABLE_DARK_MODE_V2=false
```

---

## FeatureFlags — modelo tipado

```dart
// lib/core/config/feature_flags.dart

final class FeatureFlags {
  const FeatureFlags({
    required this.newCheckout,
    required this.analytics,
    required this.biometricAuth,
    required this.darkModeV2,
  });

  final bool newCheckout;
  final bool analytics;
  final bool biometricAuth;
  final bool darkModeV2;

  /// Helper para logging y debugging — muestra el estado de todos los flags.
  Map<String, bool> toMap() => {
    'new_checkout':   newCheckout,
    'analytics':      analytics,
    'biometric_auth': biometricAuth,
    'dark_mode_v2':   darkModeV2,
  };
}
```

---

## Consumo en la UI — con Riverpod

```dart
// Provider de acceso directo a flags
final featureFlagsProvider = Provider<FeatureFlags>(
  (ref) => ref.read(appConfigProvider).featureFlags,
);

// En un widget
final flags = ref.watch(featureFlagsProvider);

if (flags.newCheckout)
  const NewCheckoutScreen()
else
  const LegacyCheckoutScreen(),
```

---

## Consumo en la UI — con BLoC

```dart
// Inyectar AppConfig en el BLoC que lo necesita
class CheckoutBloc extends Bloc<CheckoutEvent, CheckoutState> {
  CheckoutBloc({required AppConfig config}) : _flags = config.featureFlags, ...;

  final FeatureFlags _flags;

  void _onCheckoutStarted(...) {
    if (_flags.newCheckout) {
      // flujo nuevo
    } else {
      // flujo legacy
    }
  }
}
```

---

## Logging del estado de flags al arrancar

Es útil loguear qué flags están activos al inicializar la app — facilita
el debugging en staging cuando QA reporta comportamientos inesperados:

```dart
// En main_staging.dart, después de inicializar AppConfig
AppLogger.info(
  'feature_flags_initialized',
  context: config.featureFlags.toMap(),
);
```

---

## Añadir un flag nuevo — checklist

1. Agregar la variable en los tres `.env.*` y en `.env.example`
2. Añadir el campo `@EnviedField` en `env_dev.dart`, `env_staging.dart`, `env_prod.dart`
3. Regenerar con `dart run build_runner build --delete-conflicting-outputs`
4. Añadir el campo en `FeatureFlags`
5. Pasarlo en `AppConfig.forFlavor()` para los tres flavors
6. Añadir el secret en GitHub Actions, Azure DevOps y los Fastlane `.env` de CI
