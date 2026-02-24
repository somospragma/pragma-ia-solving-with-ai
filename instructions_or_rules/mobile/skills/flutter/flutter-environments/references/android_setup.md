# Android Setup — productFlavors, Firebase y Signing

`android/app/build.gradle.kts` · `android/key.properties`

> **Nota:** Este documento usa Kotlin DSL (`.kts`) para compatibilidad con Gradle 9+.

---

## Tabla de contenidos

1. [productFlavors en build.gradle](#1-productflavors-en-buildgradle)
2. [google-services.json por flavor](#2-google-servicesjson-por-flavor)
3. [Signing config por flavor](#3-signing-config-por-flavor)
4. [key.properties — credenciales del keystore](#4-keyproperties--credenciales-del-keystore)
5. [Íconos y nombre de app por flavor](#5-íconos-y-nombre-de-app-por-flavor)

---

## 1. productFlavors en build.gradle.kts

`android/app/build.gradle.kts`

```kotlin
android {
    compileSdk = 34

    defaultConfig {
        minSdk = 21
        targetSdk = 34
        versionCode = 1
        versionName = "1.0.0"
    }

    flavorDimensions += "environment"

    productFlavors {
        create("dev") {
            dimension = "environment"
            applicationId = "com.example.myapp.dev"
            resValue("string", "app_name", "MyApp Dev")
            // Variable accesible desde Dart via String.fromEnvironment
            // (solo para valores no sensibles — los sensibles van en envied)
            buildConfigField("String", "FLAVOR", "\"dev\"")
        }
        create("staging") {
            dimension = "environment"
            applicationId = "com.example.myapp.staging"
            resValue("string", "app_name", "MyApp Staging")
            buildConfigField("String", "FLAVOR", "\"staging\"")
        }
        create("prod") {
            dimension = "environment"
            applicationId = "com.example.myapp"
            resValue("string", "app_name", "MyApp")
            buildConfigField("String", "FLAVOR", "\"prod\"")
        }
    }

    buildTypes {
        getByName("debug") {
            isDebuggable = true
            isShrinkResources = false
            isMinifyEnabled = false
        }
        getByName("release") {
            isDebuggable = false
            isShrinkResources = true
            isMinifyEnabled = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }

    // Combina flavor + buildType: devDebug, stagingRelease, prodRelease, etc.
}
```

---

## 2. google-services.json por flavor

Cada flavor necesita su propio `google-services.json` descargado desde
la consola de Firebase (proyecto distinto por ambiente recomendado).

```
android/app/
├── src/
│   ├── dev/
│   │   └── google-services.json      ← Firebase proyecto "myapp-dev"
│   ├── staging/
│   │   └── google-services.json      ← Firebase proyecto "myapp-staging"
│   └── prod/
│       └── google-services.json      ← Firebase proyecto "myapp-prod"
```

El plugin `com.google.gms.google-services` recoge automáticamente el archivo
del directorio `src/<flavorName>/` cuando se compila ese flavor — sin script adicional.

### build.gradle.kts raíz (android/build.gradle.kts)

```kotlin
plugins {
    id("com.android.application") version "8.2.0" apply false
    id("org.jetbrains.kotlin.android") version "1.9.20" apply false
    id("com.google.gms.google-services") version "4.4.0" apply false
    id("com.google.firebase.crashlytics") version "2.9.9" apply false
}
```

### android/app/build.gradle.kts — aplicar plugins

```kotlin
plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("com.google.gms.google-services")
    id("com.google.firebase.crashlytics")
}
```

---

## 3. Signing config por flavor

```kotlin
// android/app/build.gradle.kts
import java.util.Properties
import java.io.FileInputStream

// Leer key.properties — generado por CI o creado localmente (gitignored)
val keystoreProperties = Properties()
val keystorePropertiesFile = rootProject.file("key.properties")
if (keystorePropertiesFile.exists()) {
    keystoreProperties.load(FileInputStream(keystorePropertiesFile))
}

android {
    signingConfigs {
        create("dev") {
            keyAlias = keystoreProperties["devKeyAlias"] as String?
            keyPassword = keystoreProperties["devKeyPassword"] as String?
            storeFile = keystoreProperties["devStoreFile"]?.let { file(it) }
            storePassword = keystoreProperties["devStorePassword"] as String?
        }
        create("staging") {
            keyAlias = keystoreProperties["stagingKeyAlias"] as String?
            keyPassword = keystoreProperties["stagingKeyPassword"] as String?
            storeFile = keystoreProperties["stagingStoreFile"]?.let { file(it) }
            storePassword = keystoreProperties["stagingStorePassword"] as String?
        }
        create("prod") {
            keyAlias = keystoreProperties["prodKeyAlias"] as String?
            keyPassword = keystoreProperties["prodKeyPassword"] as String?
            storeFile = keystoreProperties["prodStoreFile"]?.let { file(it) }
            storePassword = keystoreProperties["prodStorePassword"] as String?
        }
    }

    buildTypes {
        getByName("release") {
            // Cada flavor aplica su signingConfig en su bloque
        }
    }

    productFlavors {
        getByName("dev") {
            // ...
            signingConfig = signingConfigs.getByName("dev")
        }
        getByName("staging") {
            // ...
            signingConfig = signingConfigs.getByName("staging")
        }
        getByName("prod") {
            // ...
            signingConfig = signingConfigs.getByName("prod")
        }
    }
}
```

---

## 4. key.properties — credenciales del keystore

`android/key.properties` — **gitignored**, generado por CI o localmente.

```properties
# Dev keystore
devStoreFile=../keystores/dev.jks
devStorePassword=dev_store_password
devKeyAlias=dev
devKeyPassword=dev_key_password

# Staging keystore
stagingStoreFile=../keystores/staging.jks
stagingStorePassword=staging_store_password
stagingKeyAlias=staging
stagingKeyPassword=staging_key_password

# Prod keystore
prodStoreFile=../keystores/prod.jks
prodStorePassword=prod_store_password
prodKeyAlias=prod
prodKeyPassword=prod_key_password
```

CI genera este archivo desde secrets antes de ejecutar `flutter build`.
Ver `references/cicd.md` para los scripts de generación.

---

## 5. Íconos y nombre de app por flavor

Cada flavor puede tener sus propios recursos en `src/<flavor>/res/`:

```
android/app/src/
├── dev/
│   └── res/
│       └── mipmap-*/
│           └── ic_launcher.png       ← Ícono con badge "DEV"
├── staging/
│   └── res/
│       └── mipmap-*/
│           └── ic_launcher.png       ← Ícono con badge "STG"
└── prod/
    └── res/
        └── mipmap-*/
            └── ic_launcher.png       ← Ícono de producción limpio
```

Android fusiona automáticamente los recursos del flavor con los de `main/`.
Los recursos del flavor tienen prioridad sobre los de `main/`.
