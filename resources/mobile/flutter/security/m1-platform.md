# M1. Uso Inadecuado de la Plataforma

Esta categoría cubre el uso indebido de características de la plataforma o la falta de uso de controles de seguridad de la plataforma.

---

## Check M1-A: Debuggable activado en producción (Android)

**ID:** `M1-A-DEBUG-ENABLED`  
**Objetivo:** El APK/AAB de release no debe tener `android:debuggable="true"`.  
**Ámbito:** 
- `android/app/src/main/AndroidManifest.xml`
- `android/app/build.gradle`

**Método de búsqueda:** Lexical search  
**Patterns:**
```regex
android:debuggable\s*=\s*"true"
debuggable\s+true
```

**Comando de verificación:**
```bash
# Buscar en manifiestos
grep -r 'android:debuggable="true"' android/app/src/main/

# Buscar en build.gradle (release)
grep -A 10 "buildTypes" android/app/build.gradle | grep -A 5 "release" | grep "debuggable true"
```

**Criterio:**
- ✅ **Cumple:** No se encuentra `debuggable="true"` o solo existe en `debug/AndroidManifest.xml`
- ❌ **Falla:** Existe `debuggable="true"` en manifiesto principal o en `release` de build.gradle

**Severidad:** `HIGH`  
**Automatización:** 🟢 Alta (100%)

**Remediación:**
```xml
<!-- AndroidManifest.xml - ELIMINAR esta línea -->
<application
    android:debuggable="false">  <!-- O quitar completamente -->
```

```gradle
// build.gradle - Asegurar configuración correcta
android {
    buildTypes {
        release {
            debuggable false  // Explícito o quitar (false por defecto)
            minifyEnabled true
            shrinkResources true
        }
        debug {
            debuggable true  // OK solo en debug
        }
    }
}
```

**Referencias:**
- [Android Debuggable Security](https://developer.android.com/studio/publish/preparing#publishing-configure)

---

## Check M1-B: allowBackup habilitado sin restricciones (Android)

**ID:** `M1-B-BACKUP-ENABLED`  
**Objetivo:** Evitar copias de seguridad no controladas que expongan datos sensibles.  
**Ámbito:** `android/app/src/main/AndroidManifest.xml`

**Método de búsqueda:** Lexical search  
**Pattern:**
```regex
android:allowBackup\s*=\s*"true"
```

**Criterio:**
- ⚠️ **Advertencia:** `allowBackup="true"` sin `android:fullBackupContent` definido
- ❌ **Falla:** `allowBackup="true"` en apps con datos sensibles (tokens, PII)

**Severidad:** `MEDIUM`  
**Automatización:** 🟢 Alta (90%)

**Remediación:**
```xml
<!-- Opción 1: Deshabilitar backup completamente -->
<application
    android:allowBackup="false"
    android:fullBackupContent="false">

<!-- Opción 2: Backup controlado con exclusiones -->
<application
    android:allowBackup="true"
    android:fullBackupContent="@xml/backup_rules">
```

```xml
<!-- res/xml/backup_rules.xml -->
<?xml version="1.0" encoding="utf-8"?>
<full-backup-content>
    <exclude domain="sharedpref" path="secure_prefs.xml"/>
    <exclude domain="database" path="sensitive.db"/>
    <exclude domain="file" path="tokens/"/>
</full-backup-content>
```

---

## Check M1-C: App Transport Security (ATS) con excepciones amplias (iOS)

**ID:** `M1-C-ATS-BYPASS`  
**Objetivo:** Asegurar que ATS no esté completamente deshabilitado.  
**Ámbito:** `ios/Runner/Info.plist`

**Método de búsqueda:** Lexical search en XML/plist  
**Pattern:**
```xml
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsArbitraryLoads</key>
    <true/>
</dict>
```

**Criterio:**
- ❌ **Falla:** `NSAllowsArbitraryLoads = true` sin excepciones específicas
- ⚠️ **Advertencia:** Excepciones a dominios específicos sin justificación

**Severidad:** `HIGH`  
**Automatización:** 🟢 Alta (95%)

**Remediación:**
```xml
<!-- EVITAR: Bypass completo -->
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsArbitraryLoads</key>
    <false/>  <!-- Cambiar a false -->
</dict>

<!-- MEJOR: Excepciones específicas si es necesario -->
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSExceptionDomains</key>
    <dict>
        <key>legacy-api.example.com</key>
        <dict>
            <key>NSExceptionAllowsInsecureHTTPLoads</key>
            <true/>
            <key>NSIncludesSubdomains</key>
            <false/>
        </dict>
    </dict>
</dict>
```

---

## Check M1-D: Permisos excesivos o innecesarios (Android)

**ID:** `M1-D-EXCESSIVE-PERMISSIONS`  
**Objetivo:** Detectar permisos declarados que potencialmente no se usan.  
**Ámbito:** `android/app/src/main/AndroidManifest.xml` + `lib/**.dart`

**Método de búsqueda:** Lexical + Semantic cross-reference  
**Permisos a verificar:**
```xml
<uses-permission android:name="android.permission.CAMERA"/>
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION"/>
<uses-permission android:name="android.permission.RECORD_AUDIO"/>
<uses-permission android:name="android.permission.READ_CONTACTS"/>
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/>
<uses-permission android:name="android.permission.READ_PHONE_STATE"/>
```

**Validación cruzada:**
| Permiso | Verificar presencia en código |
|---------|-------------------------------|
| CAMERA | `image_picker`, `camera` package |
| ACCESS_FINE_LOCATION | `geolocator`, `location` package |
| RECORD_AUDIO | `audio_recorder`, `permission_handler` |
| READ_CONTACTS | `contacts_service`, `flutter_contacts` |

**Criterio:**
- ⚠️ **Advertencia:** Permiso declarado pero no se encuentra código relacionado
- ✅ **Cumple:** Permiso declarado y se detecta uso en código

**Severidad:** `MEDIUM`  
**Automatización:** 🟡 Media (70%)

**Remediación:**
```xml
<!-- Eliminar permisos no utilizados -->
<!-- ANTES -->
<uses-permission android:name="android.permission.CAMERA"/>
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION"/>

<!-- DESPUÉS (si solo se usa location) -->
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION"/>
```

---

## Check M1-E: Componentes Android exportados sin protección

**ID:** `M1-E-EXPORTED-COMPONENTS`  
**Objetivo:** Detectar Activities/Services/Receivers exportados sin `intent-filter` justificado.  
**Ámbito:** `android/app/src/main/AndroidManifest.xml`

**Método de búsqueda:** Lexical search con análisis estructural XML  
**Patterns:**
```regex
<activity[^>]+android:exported\s*=\s*"true"(?![^<]*<intent-filter)
<service[^>]+android:exported\s*=\s*"true"(?![^<]*<intent-filter)
<receiver[^>]+android:exported\s*=\s*"true"(?![^<]*<intent-filter)
```

**Criterio:**
- ❌ **Falla:** `exported="true"` sin `<intent-filter>` correspondiente
- ⚠️ **Advertencia:** `exported="true"` con `intent-filter` pero sin validación de datos

**Severidad:** `HIGH`  
**Automatización:** 🟢 Alta (85%)

**Remediación:**
```xml
<!-- ANTES: Componente expuesto innecesariamente -->
<activity
    android:name=".InternalActivity"
    android:exported="true"/>  <!-- PELIGRO -->

<!-- DESPUÉS: Proteger por defecto -->
<activity
    android:name=".InternalActivity"
    android:exported="false"/>  <!-- SEGURO -->

<!-- Si realmente necesita ser público -->
<activity
    android:name=".PublicActivity"
    android:exported="true"
    android:permission="android.permission.signature">
    <intent-filter>
        <action android:name="com.example.ACTION_VIEW"/>
    </intent-filter>
</activity>
```

**Nota importante (Android 12+):**
```xml
<!-- Android 12+ requiere declaración explícita -->
<activity
    android:name=".MyActivity"
    android:exported="false"/>  <!-- OBLIGATORIO declarar en targetSdk 31+ -->
```

---

## Check M1-F: Permisos sensibles iOS sin descripción

**ID:** `M1-F-IOS-PERMISSIONS`  
**Objetivo:** Verificar que permisos sensibles tengan descripciones claras.  
**Ámbito:** `ios/Runner/Info.plist`

**Método de búsqueda:** Lexical search de claves faltantes  
**Permisos a verificar:**
```xml
NSCameraUsageDescription
NSPhotoLibraryUsageDescription
NSLocationWhenInUseUsageDescription
NSLocationAlwaysUsageDescription
NSMicrophoneUsageDescription
NSContactsUsageDescription
NSCalendarsUsageDescription
NSBluetoothPeripheralUsageDescription
NSFaceIDUsageDescription
```

**Criterio:**
- ❌ **Falla:** Se usa funcionalidad pero falta la clave `*UsageDescription`
- ✅ **Cumple:** Todas las funcionalidades usadas tienen descripción

**Severidad:** `HIGH` (App Store rechaza apps sin esto)  
**Automatización:** 🟡 Media (75%)

**Remediación:**
```xml
<!-- Info.plist -->
<key>NSCameraUsageDescription</key>
<string>Esta app necesita acceso a la cámara para tomar fotos de productos</string>

<key>NSLocationWhenInUseUsageDescription</key>
<string>Usamos tu ubicación para mostrarte tiendas cercanas</string>

<key>NSPhotoLibraryUsageDescription</key>
<string>Necesitamos acceso a tus fotos para que puedas seleccionar una imagen de perfil</string>
```

---

## Resumen M1

| Check | Severidad | Automatización | Esfuerzo Fix |
|-------|-----------|----------------|--------------|
| M1-A | HIGH | 🟢 100% | Bajo |
| M1-B | MEDIUM | 🟢 90% | Bajo |
| M1-C | HIGH | 🟢 95% | Bajo |
| M1-D | MEDIUM | 🟡 70% | Medio |
| M1-E | HIGH | 🟢 85% | Bajo |
| M1-F | HIGH | 🟡 75% | Medio |

**Total checks:** 6  
**Severidad crítica:** 0  
**Severidad alta:** 3  
**Severidad media:** 2  
**Severidad baja:** 1

---

**Última actualización:** 2025-11-12  
**Versión:** 1.0