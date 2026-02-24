# CI/CD — GitHub Actions, Azure DevOps y Fastlane

Inyección de secrets · generación de `.env` · build y firma por flavor

---

## Tabla de contenidos

1. [Principio de inyección de secrets](#1-principio-de-inyección-de-secrets)
2. [GitHub Actions — build por flavor](#2-github-actions--build-por-flavor)
3. [Azure DevOps — pipeline por flavor](#3-azure-devops--pipeline-por-flavor)
4. [Fastlane — lanes por flavor](#4-fastlane--lanes-por-flavor)
5. [Generación de key.properties en CI](#5-generación-de-keyproperties-en-ci)
6. [Generación de .env en CI](#6-generación-de-env-en-ci)

---

## 1. Principio de inyección de secrets

El repo nunca contiene secrets. El flujo es siempre:

```
CI Secrets (GitHub / Azure / Fastlane .env)
        ↓  script de preparación genera los archivos locales
.env.prod  /  key.properties  /  GoogleService-Info.plist
        ↓  dart run build_runner build
env_prod.g.dart  (ofuscado, embebido en binario)
        ↓  flutter build apk/ipa --flavor prod
APK / IPA firmado y listo
```

---

## 2. GitHub Actions — build por flavor

### .github/workflows/build-prod.yml

```yaml
name: Build Prod

on:
  push:
    branches: [main]

jobs:
  build-android:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.38.10'
          cache: true

      - name: Generar .env.prod
        run: |
          cat > .env.prod << EOF
          API_BASE_URL=${{ secrets.PROD_API_BASE_URL }}
          API_KEY=${{ secrets.PROD_API_KEY }}
          SENTRY_DSN=${{ secrets.PROD_SENTRY_DSN }}
          DATADOG_CLIENT_TOKEN=${{ secrets.PROD_DATADOG_TOKEN }}
          DATADOG_APPLICATION_ID=${{ secrets.PROD_DATADOG_APP_ID }}
          LOKI_ENDPOINT=${{ secrets.PROD_LOKI_ENDPOINT }}
          ENABLE_NEW_CHECKOUT=false
          ENABLE_ANALYTICS=true
          EOF

      - name: Generar key.properties
        run: |
          cat > android/key.properties << EOF
          prodStoreFile=../keystores/prod.jks
          prodStorePassword=${{ secrets.PROD_KEYSTORE_PASSWORD }}
          prodKeyAlias=${{ secrets.PROD_KEY_ALIAS }}
          prodKeyPassword=${{ secrets.PROD_KEY_PASSWORD }}
          EOF

      - name: Decodificar keystore
        run: |
          mkdir -p android/keystores
          echo "${{ secrets.PROD_KEYSTORE_BASE64 }}" | base64 --decode \
            > android/keystores/prod.jks

      - name: Instalar dependencias
        run: flutter pub get

      - name: Analizar código
        run: flutter analyze --fatal-infos

      - name: Ejecutar tests
        run: flutter test --coverage

      - name: Generar código envied
        run: dart run build_runner build --delete-conflicting-outputs

      - name: Build APK prod
        run: flutter build apk --flavor prod -t lib/main_prod.dart --release

      - uses: actions/upload-artifact@v4
        with:
          name: app-prod-release
          path: build/app/outputs/flutter-apk/app-prod-release.apk

  build-ios:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4

      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.38.10'
          cache: true

      - name: Generar .env.prod
        run: |
          cat > .env.prod << EOF
          API_BASE_URL=${{ secrets.PROD_API_BASE_URL }}
          API_KEY=${{ secrets.PROD_API_KEY }}
          SENTRY_DSN=${{ secrets.PROD_SENTRY_DSN }}
          DATADOG_CLIENT_TOKEN=${{ secrets.PROD_DATADOG_TOKEN }}
          DATADOG_APPLICATION_ID=${{ secrets.PROD_DATADOG_APP_ID }}
          LOKI_ENDPOINT=${{ secrets.PROD_LOKI_ENDPOINT }}
          ENABLE_NEW_CHECKOUT=false
          ENABLE_ANALYTICS=true
          EOF

      - name: Instalar certificados iOS
        uses: apple-actions/import-codesign-certs@v2
        with:
          p12-file-base64: ${{ secrets.IOS_PROD_CERT_BASE64 }}
          p12-password: ${{ secrets.IOS_PROD_CERT_PASSWORD }}

      - name: Instalar provisioning profile
        uses: apple-actions/download-provisioning-profiles@v1
        with:
          bundle-id: com.example.myapp
          issuer-id: ${{ secrets.APPSTORE_ISSUER_ID }}
          api-key-id: ${{ secrets.APPSTORE_KEY_ID }}
          api-private-key: ${{ secrets.APPSTORE_PRIVATE_KEY }}

      - name: Instalar dependencias
        run: |
          flutter pub get
          cd ios && pod install

      - name: Analizar código
        run: flutter analyze --fatal-infos

      - name: Ejecutar tests
        run: flutter test --coverage

      - name: Generar código envied
        run: dart run build_runner build --delete-conflicting-outputs

      - name: Build IPA prod
        run: |
          flutter build ipa --flavor prod -t lib/main_prod.dart \
            --export-options-plist ios/ExportOptions-prod.plist
```

---

## 3. Azure DevOps — pipeline por flavor

### azure-pipelines-prod.yml

```yaml
trigger:
  branches:
    include:
      - main

pool:
  vmImage: 'ubuntu-latest'   # usar 'macos-latest' para iOS

variables:
  flutterVersion: '3.38.10'

steps:
  - task: FlutterInstall@0
    inputs:
      version: $(flutterVersion)

  - script: |
      cat > .env.prod << EOF
      API_BASE_URL=$(PROD_API_BASE_URL)
      API_KEY=$(PROD_API_KEY)
      SENTRY_DSN=$(PROD_SENTRY_DSN)
      DATADOG_CLIENT_TOKEN=$(PROD_DATADOG_TOKEN)
      DATADOG_APPLICATION_ID=$(PROD_DATADOG_APP_ID)
      LOKI_ENDPOINT=$(PROD_LOKI_ENDPOINT)
      ENABLE_NEW_CHECKOUT=false
      ENABLE_ANALYTICS=true
      EOF
    displayName: 'Generar .env.prod'
    # Las variables $(VAR) se definen en Azure DevOps > Library > Variable Groups

  - script: |
      cat > android/key.properties << EOF
      prodStoreFile=../keystores/prod.jks
      prodStorePassword=$(PROD_KEYSTORE_PASSWORD)
      prodKeyAlias=$(PROD_KEY_ALIAS)
      prodKeyPassword=$(PROD_KEY_PASSWORD)
      EOF
    displayName: 'Generar key.properties'

  - script: |
      mkdir -p android/keystores
      echo $(PROD_KEYSTORE_BASE64) | base64 --decode > android/keystores/prod.jks
    displayName: 'Decodificar keystore'

  - script: flutter pub get
    displayName: 'Instalar dependencias'

  - script: flutter analyze --fatal-infos
    displayName: 'Analizar código'

  - script: flutter test --coverage
    displayName: 'Ejecutar tests'

  - script: dart run build_runner build --delete-conflicting-outputs
    displayName: 'Generar código envied'

  - script: |
      flutter build apk --flavor prod -t lib/main_prod.dart --release
    displayName: 'Build APK prod'

  - task: PublishBuildArtifacts@1
    inputs:
      pathToPublish: 'build/app/outputs/flutter-apk/app-prod-release.apk'
      artifactName: 'app-prod-release'
```

### Variable Groups en Azure DevOps

Ir a Pipelines > Library > + Variable Group → crear grupo `flutter-prod-secrets`:

| Variable | Valor | Secret |
|---|---|---|
| `PROD_API_BASE_URL` | `https://api.myapp.com` | No |
| `PROD_API_KEY` | `sk_prod_xxx` | **Sí** |
| `PROD_KEYSTORE_BASE64` | base64 del .jks | **Sí** |
| `PROD_KEYSTORE_PASSWORD` | `xxx` | **Sí** |
| `PROD_KEY_ALIAS` | `prod` | No |
| `PROD_KEY_PASSWORD` | `xxx` | **Sí** |

---

## 4. Fastlane — lanes por flavor

### Fastfile

```ruby
# fastlane/Fastfile

default_platform(:android)

# ─── Android ──────────────────────────────────────────────────────────────────

platform :android do
  lane :build_dev do
    generate_env(flavor: "dev")
    sh("dart run build_runner build --delete-conflicting-outputs",
       chdir: "../")
    gradle(
      task:              "assemble",
      flavor:            "dev",
      build_type:        "Debug",
      project_dir:       "android/",
    )
  end

  lane :build_prod do
    generate_env(flavor: "prod")
    generate_key_properties
    sh("dart run build_runner build --delete-conflicting-outputs",
       chdir: "../")
    gradle(
      task:              "bundle",       # AAB para Play Store
      flavor:            "prod",
      build_type:        "Release",
      project_dir:       "android/",
      properties: {
        "android.injected.signing.store.file"     => ENV["PROD_KEYSTORE_PATH"],
        "android.injected.signing.store.password" => ENV["PROD_KEYSTORE_PASSWORD"],
        "android.injected.signing.key.alias"      => ENV["PROD_KEY_ALIAS"],
        "android.injected.signing.key.password"   => ENV["PROD_KEY_PASSWORD"],
      }
    )
  end
end

# ─── iOS ──────────────────────────────────────────────────────────────────────

platform :ios do
  lane :build_prod do
    generate_env(flavor: "prod")
    sh("dart run build_runner build --delete-conflicting-outputs",
       chdir: "../")
    match(type: "appstore", app_identifier: "com.example.myapp")
    gym(
      scheme:                    "Prod",
      export_method:             "app-store",
      export_options:            "./ios/ExportOptions-prod.plist",
      configuration:             "Release-prod",
      output_directory:          "./build/ios",
      output_name:               "MyApp-prod.ipa",
    )
  end
end

# ─── Helper privado ───────────────────────────────────────────────────────────

private_lane :generate_env do |options|
  flavor = options[:flavor]
  env_content = [
    "API_BASE_URL=#{ENV["#{flavor.upcase}_API_BASE_URL"]}",
    "API_KEY=#{ENV["#{flavor.upcase}_API_KEY"]}",
    "SENTRY_DSN=#{ENV["#{flavor.upcase}_SENTRY_DSN"]}",
    "ENABLE_ANALYTICS=#{flavor == 'prod' ? 'true' : 'false'}",
  ].join("\n")
  File.write(".env.#{flavor}", env_content)
  UI.success("Generado .env.#{flavor}")
end

private_lane :generate_key_properties do
  content = [
    "prodStoreFile=../keystores/prod.jks",
    "prodStorePassword=#{ENV['PROD_KEYSTORE_PASSWORD']}",
    "prodKeyAlias=#{ENV['PROD_KEY_ALIAS']}",
    "prodKeyPassword=#{ENV['PROD_KEY_PASSWORD']}",
  ].join("\n")
  File.write("android/key.properties", content)
end
```

### .env de Fastlane (gitignored)

```dotenv
# fastlane/.env.secret — gitignored
PROD_API_BASE_URL=https://api.myapp.com
PROD_API_KEY=sk_prod_xxx
PROD_KEYSTORE_PASSWORD=xxx
PROD_KEY_ALIAS=prod
PROD_KEY_PASSWORD=xxx
```

---

## 5. Generación de key.properties en CI

### 5.1 Preparar el keystore para CI

El keystore (`.jks`) se almacena como secret en Base64:

```bash
# Generar el Base64 para subir al CI (ejecutar una sola vez localmente)
# macOS
base64 -i android/keystores/prod.jks | pbcopy

# Linux
base64 -w 0 android/keystores/prod.jks | xclip -selection clipboard

# Pegar el resultado en el secret PROD_KEYSTORE_BASE64
```

### 5.2 Secrets requeridos para firmado

| Secret | Descripción |
|--------|-------------|
| `KEYSTORE_BASE64` | Keystore (`.jks`) codificado en Base64 |
| `KEYSTORE_PASSWORD` | Contraseña del keystore |
| `KEY_ALIAS` | Alias de la clave |
| `KEY_PASSWORD` | Contraseña de la clave |

> **Nota**: La decodificación del keystore y generación de `key.properties` debe configurarse manualmente según el proveedor de CI/CD (GitHub Actions, Azure DevOps, Bitrise, Codemagic, etc.). Cada plataforma tiene sus propias acciones/tasks para manejo de archivos y secrets.

### 5.3 Estructura esperada de key.properties

```properties
storePassword=<KEYSTORE_PASSWORD>
keyPassword=<KEY_PASSWORD>
keyAlias=<KEY_ALIAS>
storeFile=<ruta-al-keystore.jks>
```

El archivo `key.properties` debe generarse en el CI antes del build, usando los secrets configurados en la plataforma.

### 5.4 Configurar build.gradle.kts para leer key.properties

```kotlin
// android/app/build.gradle.kts

import java.util.Properties
import java.io.FileInputStream

val keystoreProperties = Properties()
val keystorePropertiesFile = rootProject.file("key.properties")
if (keystorePropertiesFile.exists()) {
    keystoreProperties.load(FileInputStream(keystorePropertiesFile))
}

android {
    // ...
    
    signingConfigs {
        create("release") {
            keyAlias = keystoreProperties["keyAlias"] as String?
            keyPassword = keystoreProperties["keyPassword"] as String?
            storeFile = keystoreProperties["storeFile"]?.let { file(it) }
            storePassword = keystoreProperties["storePassword"] as String?
        }
    }
    
    buildTypes {
        release {
            signingConfig = signingConfigs.getByName("release")
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
}
```

### 5.5 Buenas prácticas de firmado

- **Nunca** commitear `key.properties` ni archivos `.jks` al repositorio
- Agregar al `.gitignore`:
  ```
  android/key.properties
  android/app/*.jks
  android/keystores/
  *.keystore
  ```
- Usar **Play App Signing** de Google Play Console para mayor seguridad — el keystore de subida puede rotarse sin afectar a usuarios
- Mantener un backup seguro del keystore fuera del CI (vault, 1Password, etc.)
- Para múltiples flavors, usar prefijos en los secrets: `DEV_KEYSTORE_BASE64`, `PROD_KEYSTORE_BASE64`

---

## 6. Generación de .env en CI

El patrón es siempre el mismo en los tres sistemas:

1. Los secrets se declaran en el CI (GitHub Secrets, Azure Variable Groups, Fastlane .env)
2. Un step/script genera los archivos `.env.*` en el workspace efímero del runner
3. `dart run build_runner build` lee los `.env.*` y genera los `*.g.dart` ofuscados
4. `flutter build` compila con los valores embebidos — el runner se destruye después

Los `.env.*` generados en el runner **nunca se suben como artefactos** — solo el APK/IPA firmado.
