# iOS Setup — Schemes, xcconfig, Firebase y Signing

`ios/Flutter/` · `ios/Runner.xcodeproj/`

---

## Tabla de contenidos

1. [Schemes — Dev, Staging, Prod](#1-schemes--dev-staging-prod)
2. [xcconfig — variables de compilación por ambiente](#2-xcconfig--variables-de-compilación-por-ambiente)
3. [GoogleService-Info.plist por scheme](#3-googleservice-infoplist-por-scheme)
4. [Run Script — copiar el plist correcto](#4-run-script--copiar-el-plist-correcto)
5. [Bundle ID y nombre de app por flavor](#5-bundle-id-y-nombre-de-app-por-flavor)
6. [Signing — certificates y provisioning profiles](#6-signing--certificates-y-provisioning-profiles)

---

## 1. Schemes — Dev, Staging, Prod

Xcode > Product > Scheme > Manage Schemes → crear tres schemes:

| Scheme | Build Configuration (Run) | Build Configuration (Archive) |
|---|---|---|
| `Dev` | `Debug-dev` | `Release-dev` |
| `Staging` | `Debug-staging` | `Release-staging` |
| `Prod` | `Debug-prod` | `Release-prod` |

Cada scheme se comparte marcando **Shared** (genera el `.xcscheme` en
`xcshareddata/xcschemes/` y se commitea al repo).

### Crear Build Configurations

Xcode > Project > Runner > Info > Configurations:
Duplicar `Debug` → `Debug-dev`, `Debug-staging`, `Debug-prod`
Duplicar `Release` → `Release-dev`, `Release-staging`, `Release-prod`

---

## 2. xcconfig — variables de compilación por ambiente

Flutter ya usa `Debug.xcconfig` y `Release.xcconfig` en `ios/Flutter/`.
Extiende ese sistema creando configs por flavor que los incluyen:

### ios/Flutter/Dev.xcconfig

```xcconfig
#include "Generated.xcconfig"
FLUTTER_TARGET=lib/main_dev.dart
APP_BUNDLE_ID=com.example.myapp.dev
APP_DISPLAY_NAME=MyApp Dev
FLUTTER_FLAVOR=dev
```

### ios/Flutter/Staging.xcconfig

```xcconfig
#include "Generated.xcconfig"
FLUTTER_TARGET=lib/main_staging.dart
APP_BUNDLE_ID=com.example.myapp.staging
APP_DISPLAY_NAME=MyApp Staging
FLUTTER_FLAVOR=staging
```

### ios/Flutter/Prod.xcconfig

```xcconfig
#include "Generated.xcconfig"
FLUTTER_TARGET=lib/main_prod.dart
APP_BUNDLE_ID=com.example.myapp
APP_DISPLAY_NAME=MyApp
FLUTTER_FLAVOR=prod
```

### Conectar xcconfig con Build Configurations

En Xcode > Project > Runner > Info > Configurations:
- `Debug-dev`     → `ios/Flutter/Dev.xcconfig`
- `Debug-staging` → `ios/Flutter/Staging.xcconfig`
- `Debug-prod`    → `ios/Flutter/Prod.xcconfig`
- `Release-dev`     → `ios/Flutter/Dev.xcconfig`
- `Release-staging` → `ios/Flutter/Staging.xcconfig`
- `Release-prod`    → `ios/Flutter/Prod.xcconfig`

### Info.plist — usar las variables del xcconfig

```xml
<!-- ios/Runner/Info.plist -->
<key>CFBundleIdentifier</key>
<string>$(APP_BUNDLE_ID)</string>

<key>CFBundleDisplayName</key>
<string>$(APP_DISPLAY_NAME)</string>
```

---

## 3. GoogleService-Info.plist por scheme

Descargar un `GoogleService-Info.plist` por proyecto Firebase y colocarlos:

```
ios/Runner/
├── GoogleService-Info-Dev.plist
├── GoogleService-Info-Staging.plist
└── GoogleService-Info-Prod.plist
```

**No agregar ninguno de estos al Build Phase "Copy Bundle Resources"** —
el Run Script del paso siguiente se encarga de copiar el correcto.

---

## 4. Run Script — copiar el plist correcto

En Xcode > Runner Target > Build Phases > + > New Run Script Phase
Arrastrar el script **antes** de "Copy Bundle Resources":

```bash
# Selecciona el GoogleService-Info.plist correcto según el flavor
# FLUTTER_FLAVOR viene definido en el xcconfig activo

PLIST_SOURCE="${SRCROOT}/Runner/GoogleService-Info-${FLUTTER_FLAVOR^}.plist"
PLIST_DEST="${BUILT_PRODUCTS_DIR}/${PRODUCT_NAME}.app/GoogleService-Info.plist"

if [ ! -f "$PLIST_SOURCE" ]; then
  echo "error: No se encontró GoogleService-Info-${FLUTTER_FLAVOR^}.plist"
  exit 1
fi

cp "$PLIST_SOURCE" "$PLIST_DEST"
echo "Copiado: $PLIST_SOURCE → $PLIST_DEST"
```

> `${FLUTTER_FLAVOR^}` capitaliza la primera letra: `dev` → `Dev`.

---

## 5. Bundle ID y nombre de app por flavor

El `APP_BUNDLE_ID` y `APP_DISPLAY_NAME` definidos en los xcconfig se
aplican en `Info.plist` con `$(APP_BUNDLE_ID)` y `$(APP_DISPLAY_NAME)`.

Esto permite instalar los tres flavors simultáneamente en el mismo dispositivo
— cada uno aparece como una app independiente con su propio ícono.

### Íconos por flavor

Xcode > Runner > Assets.xcassets → crear tres AppIcon sets:
- `AppIcon` → prod
- `AppIcon-Dev` → dev (con badge)
- `AppIcon-Staging` → staging (con badge)

En cada xcconfig, añadir:

```xcconfig
# Dev.xcconfig
ASSETCATALOG_COMPILER_APPICON_NAME=AppIcon-Dev

# Staging.xcconfig
ASSETCATALOG_COMPILER_APPICON_NAME=AppIcon-Staging

# Prod.xcconfig
ASSETCATALOG_COMPILER_APPICON_NAME=AppIcon
```

---

## 6. Signing — certificates y provisioning profiles

### Configuración en Xcode (manual signing recomendado para CI)

En Xcode > Runner Target > Signing & Capabilities, desactivar
"Automatically manage signing" para las configuraciones de Release.

Asignar por Build Configuration:

| Configuration | Bundle ID | Provisioning Profile |
|---|---|---|
| `Release-dev` | `com.example.myapp.dev` | `MyApp Dev Distribution` |
| `Release-staging` | `com.example.myapp.staging` | `MyApp Staging Distribution` |
| `Release-prod` | `com.example.myapp` | `MyApp Distribution` |

### ExportOptions.plist por flavor

CI necesita un `ExportOptions.plist` por flavor para `xcodebuild -exportArchive`:

```xml
<!-- ios/ExportOptions-prod.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" ...>
<plist version="1.0">
<dict>
    <key>method</key>
    <string>app-store</string>
    <key>teamID</key>
    <string>YOUR_TEAM_ID</string>
    <key>provisioningProfiles</key>
    <dict>
        <key>com.example.myapp</key>
        <string>MyApp Distribution</string>
    </dict>
    <key>signingCertificate</key>
    <string>Apple Distribution</string>
    <key>stripSwiftSymbols</key>
    <true/>
    <key>uploadBitcode</key>
    <false/>
</dict>
</plist>
```

Crear `ExportOptions-dev.plist` y `ExportOptions-staging.plist` equivalentes
con sus respectivos Bundle IDs y provisioning profiles.
