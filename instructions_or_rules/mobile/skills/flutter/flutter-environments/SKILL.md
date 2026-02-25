---
name: flutter-environments
description: Skill avanzado para configuración de flavors, schemes, build variants y ambientes de compilación en Flutter para iOS y Android, usando envied con obfuscate:true para proteger secrets, Firebase por flavor, feature flags, signing config y CI/CD con GitHub Actions, Fastlane y Azure DevOps. Úsalo siempre que el usuario mencione flavors, ambientes, dev/staging/prod, build variants, schemes, xcconfig, productFlavors, envied, variables de entorno, .env, secrets, Firebase por ambiente, google-services.json, GoogleService-Info.plist, signing, keystore, certificates, CI/CD con Flutter, o quiera separar configuración entre ambientes. También aplica cuando el usuario quiera agregar un nuevo ambiente, migrar de un solo main.dart a múltiples entry points, o proteger API keys en el binario compilado.
metadata:
  author: Pragma Mobile Chapter
  version: "1.0"
---

# Flutter Flavors & Build Environments

Este documento define las reglas y mejores prácticas para implementar configuraciones de ambientes de compulación diferentes en aplicaciones Flutter siguiendo los estándares de Pragma.

---

## Principios de diseño

- **Un entry point por flavor.** `main_dev.dart`, `main_staging.dart` y `main_prod.dart` son el único lugar donde se decide qué configuración, qué sinks de logging y qué Firebase se inicializan. Nada de `if (kDebugMode)` dispersos en el código de negocio.
- **Los secrets nunca viajan en el repo.** Las API keys viven en archivos `.env` ignorados por git. `envied` los lee en tiempo de compilación y los embebe en el binario con `obfuscate: true` — ni en el repo ni en texto plano en el APK/IPA.
- **La configuración es un objeto tipado, no un Map de Strings.** `AppConfig` es una clase con campos fuertemente tipados accesible desde cualquier capa. Elimina los magic strings y los `String.fromEnvironment` dispersos.
- **iOS y Android son paralelos.** Cada decisión que se toma en Android (productFlavor, google-services.json por carpeta) tiene su equivalente exacto en iOS (scheme, xcconfig, GoogleService-Info.plist por carpeta). El skill siempre cubre ambas plataformas.
- **CI/CD inyecta los secrets — nunca se commitean.** GitHub Actions, Azure DevOps y Fastlane reciben los secrets como variables de entorno del pipeline y generan los `.env` en tiempo de build. El repo solo contiene `.env.example` como documentación.

---

## Estructura de archivos del proyecto

```
├── .env.dev                          ← Gitignored — generado en CI o local
├── .env.staging                      ← Gitignored
├── .env.prod                         ← Gitignored
├── .env.example                      ← Commiteado — documenta las keys requeridas
│
├── lib/
│   ├── main_dev.dart                 ← Entry point dev
│   ├── main_staging.dart             ← Entry point staging
│   ├── main_prod.dart                ← Entry point prod
│   └── core/
│       └── config/
│           └── env/
│               ├── app_config.dart       ← Objeto tipado de configuración por flavor
│               ├── app_flavor.dart       ← Enum AppFlavor { dev, staging, prod }
│               ├── env_dev.dart          ← Generado por envied desde .env.dev
│               ├── env_staging.dart      ← Generado por envied desde .env.staging
│               └── env_prod.dart         ← Generado por envied desde .env.prod
│
├── android/
│   ├── app/
│   │   ├── src/dev/google-services.json
│   │   ├── src/staging/google-services.json
│   │   ├── src/prod/google-services.json
│   │   └── build.gradle              ← productFlavors + signingConfigs
│   └── key.properties                ← Gitignored — keystore passwords
│
└── ios/
    ├── Runner/
    │   ├── GoogleService-Info-Dev.plist
    │   ├── GoogleService-Info-Staging.plist
    │   └── GoogleService-Info-Prod.plist
    ├── Flutter/
    │   ├── Dev.xcconfig
    │   ├── Staging.xcconfig
    │   └── Prod.xcconfig
    └── Runner.xcodeproj/
        └── xcshareddata/xcschemes/   ← Dev.xcscheme, Staging.xcscheme, Prod.xcscheme
```

---

## Archivos de referencia

Lee el archivo correspondiente antes de generar código para esa área:

| Qué implementar | Referencia |
|---|---|
| `AppFlavor`, `AppConfig`, `envied` con `obfuscate:true`, entry points | `references/app_config.md` |
| Android: `productFlavors`, `google-services.json` por flavor, signing | `references/android_setup.md` |
| iOS: schemes, xcconfig, `GoogleService-Info.plist` por flavor, signing | `references/ios_setup.md` |
| Feature flags por ambiente | `references/feature_flags.md` |
| CI/CD: GitHub Actions, Azure DevOps, Fastlane — inyección de secrets | `references/cicd.md` |

> `android_setup.md`, `ios_setup.md` y `cicd.md` tienen más de 300 líneas — cada uno incluye tabla de contenidos al inicio.

---

## Comandos de ejecución por flavor

```bash
# Desarrollo
flutter run --flavor dev -t lib/main_dev.dart

# Staging
flutter run --flavor staging -t lib/main_staging.dart

# Producción
flutter build apk --flavor prod -t lib/main_prod.dart
flutter build ipa --flavor prod -t lib/main_prod.dart
```

---

## Checklist antes de entregar configuración

- [ ] `.env.*` está en `.gitignore` — nunca commiteado
- [ ] `.env.example` documenta todas las keys con valores de placeholder
- [ ] `envied` usa `obfuscate: true` en todos los `@Envied` — sin excepción
- [ ] Los archivos `*.g.dart` generados por envied están en `.gitignore`
- [ ] `AppConfig` es el único lugar donde se accede a `EnvDev/Staging/Prod` — nada los importa directamente fuera de `app_config.dart`
- [ ] Android tiene `google-services.json` en `src/dev/`, `src/staging/`, `src/prod/`
- [ ] iOS tiene un `GoogleService-Info.plist` por scheme y un Run Script que copia el correcto
- [ ] Cada flavor tiene su propio `applicationId`/`bundleId` — permiten instalar los 3 simultáneamente
- [ ] Los keystores y `.p12` nunca están en el repo — viven en CI secrets o en vault
- [ ] Usar importaciones absolutas con `package:` — nunca importaciones relativas (`import '../...'`)
- [ ] CI genera los `.env` desde secrets antes de ejecutar `flutter build`
