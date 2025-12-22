# M8. Manipulación de Código

Esta categoría cubre la protección contra modificación del código y binarios de la aplicación.

---

## Check M8-A: Ofuscación deshabilitada en producción (Android)

**ID:** `M8-A-NO-OBFUSCATION`  
**Objetivo:** Verificar que ProGuard/R8 esté habilitado para release builds.  
**Ámbito:** `android/app/build.gradle`

**Método de búsqueda:** Lexical search  
**Pattern inseguro:**

```gradle
// android/app/build.gradle
android {
    buildTypes {
        release {
            minifyEnabled false  // ❌ Ofuscación deshabilitada
            shrinkResources false  // ⚠️ Sin eliminación de recursos
        }
    }
}
```

**Búsqueda lexical:**
```bash
grep -A 5 "buildTypes" android/app/build.gradle | grep -A 3 "release" | grep "minifyEnabled false"
```

**Criterio:**
- ❌ **Falla:** `minifyEnabled false` en release
- ⚠️ **Advertencia:** `minifyEnabled true` pero sin reglas ProGuard
- ✅ **Cumple:** Ofuscación habilitada + reglas configuradas

**Severidad:** `MEDIUM`  
**Automatización:** 🟢 Alta (100%)

**Remediación:**

```gradle
// ✅ android/app/build.gradle
android {
    buildTypes {
        release {
            // ✅ Habilitar ofuscación y shrinking
            minifyEnabled true
            shrinkResources true
            
            // ✅ Usar reglas ProGuard
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
            
            // ✅ Configuraciones adicionales de seguridad
            signingConfig signingConfigs.release
        }
        
        debug {
            // Debug puede tener ofuscación deshabilitada
            minifyEnabled false
        }
    }
}
```

```proguard
# ✅ android/app/proguard-rules.pro

# Mantener clases de Flutter
-keep class io.flutter.app.** { *; }
-keep class io.flutter.plugin.** { *; }
-keep class io.flutter.util.** { *; }
-keep class io.flutter.view.** { *; }
-keep class io.flutter.** { *; }
-keep class io.flutter.plugins.** { *; }

# Mantener clases usadas por reflexión
-keepattributes *Annotation*
-keepattributes Signature
-keepattributes InnerClasses

# Mantener modelos de datos (JSON serialization)
-keep class com.example.app.models.** { *; }
-keepclassmembers class * {
    @com.google.gson.annotations.SerializedName <fields>;
}

# Ofuscar strings sensibles
-adaptclassstrings

# Optimizaciones agresivas
-optimizationpasses 5
-dontusemixedcaseclassnames
-dontskipnonpubliclibraryclasses
-verbose

# Eliminar logs en release
-assumenosideeffects class android.util.Log {
    public static *** d(...);
    public static *** v(...);
    public static *** i(...);
}
```

---

## Check M8-B: Símbolos de debug no eliminados (iOS)

**ID:** `M8-B-DEBUG-SYMBOLS`  
**Objetivo:** Verificar que símbolos de debug se eliminen en release builds iOS.  
**Ámbito:** `ios/Runner.xcodeproj/project.pbxproj`

**Método de búsqueda:** Lexical search  
**Pattern:**

```bash
grep "STRIP_INSTALLED_PRODUCT" ios/Runner.xcodeproj/project.pbxproj
grep "DEBUG_INFORMATION_FORMAT" ios/Runner.xcodeproj/project.pbxproj
```

**Criterio:**
- ⚠️ **Advertencia:** `STRIP_INSTALLED_PRODUCT = NO` en Release
- ⚠️ **Advertencia:** `DEBUG_INFORMATION_FORMAT = dwarf-with-dsym` en Release
- ✅ **Cumple:** Símbolos eliminados en Release

**Severidad:** `MEDIUM`  
**Automatización:** 🟢 Alta (90%)

**Remediación:**

```xml
<!-- ✅ ios/Runner.xcodeproj/project.pbxproj -->
<!-- Buscar la sección Release y asegurar: -->

/* Release */
buildSettings = {
    ...
    STRIP_INSTALLED_PRODUCT = YES;  /* ✅ Eliminar símbolos */
    STRIP_STYLE = "non-global";
    DEAD_CODE_STRIPPING = YES;
    DEBUG_INFORMATION_FORMAT = "dwarf";  /* ✅ No incluir dsym */
    ENABLE_BITCODE = NO;  /* Flutter no soporta bitcode */
    DEPLOYMENT_POSTPROCESSING = YES;
    COPY_PHASE_STRIP = YES;
    ...
}
```

**Configurar en Xcode:**
1. Abrir `ios/Runner.xcworkspace`
2. Seleccionar target "Runner"
3. Build Settings → Release
4. Buscar "Strip Installed Product" → YES
5. Buscar "Debug Information Format" → DWARF (sin dsym)

---

## Validación adicional para M8

### Verificar ofuscación Dart (Flutter)

```bash
# ✅ Compilar con ofuscación de código Dart
flutter build apk --obfuscate --split-debug-info=build/app/outputs/symbols

# ✅ Compilar iOS con ofuscación
flutter build ios --release --obfuscate --split-debug-info=build/ios/symbols
```

**Agregar a scripts de CI/CD:**

```yaml
# .github/workflows/release.yml
name: Release Build

on:
  push:
    tags:
      - 'v*'

jobs:
  build-android:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        
      - name: Build APK with obfuscation
        run: |
          # ✅ SIEMPRE usar --obfuscate en producción
          flutter build apk --release \
            --obfuscate \
            --split-debug-info=build/symbols \
            --no-tree-shake-icons
          
      - name: Upload symbols
        uses: actions/upload-artifact@v3
        with:
          name: android-symbols
          path: build/symbols
```

---

## Check M8-C: Detección de root/jailbreak

**ID:** `M8-C-ROOT-DETECTION`  
**Objetivo:** Implementar detección de dispositivos comprometidos.  
**Ámbito:** `lib/**.dart`

**Método de búsqueda:** Semantic search  
**Detección de implementación:**

```dart
// ⚠️ Verificar si existe implementación de root/jailbreak detection
import 'package:flutter_jailbreak_detection/flutter_jailbreak_detection.dart';
// O
import 'package:safe_device/safe_device.dart';
```

**Criterio:**
- ⚠️ **Advertencia:** Apps con datos sensibles sin detección de root/jailbreak
- ✅ **Cumple:** Implementación de detección (especialmente en apps financieras)

**Severidad:** `MEDIUM` (HIGH para apps financieras)  
**Automatización:** 🟡 Media (40%)

**Remediación:**

```dart
// ✅ SOLUCIÓN 1: Detección básica con flutter_jailbreak_detection
import 'package:flutter_jailbreak_detection/flutter_jailbreak_detection.dart';

class SecurityService {
  Future<bool> isDeviceSecure() async {
    try {
      final jailbroken = await FlutterJailbreakDetection.jailbroken;
      final developerMode = await FlutterJailbreakDetection.developerMode;
      
      return !jailbroken && !developerMode;
    } catch (e) {
      SecureLogger.logError('Error checking device security', e);
      // ✅ Por seguridad, asumir comprometido si falla la detección
      return false;
    }
  }
  
  Future<void> checkDeviceSecurity() async {
    final isSecure = await isDeviceSecure();
    
    if (!isSecure) {
      _handleUnsafeDevice();
    }
  }
  
  void _handleUnsafeDevice() {
    Get.dialog(
      AlertDialog(
        title: Text('Dispositivo no seguro'),
        content: Text(
          'Esta aplicación no puede ejecutarse en dispositivos rooteados o con jailbreak por seguridad.',
        ),
        actions: [
          TextButton(
            onPressed: () => SystemNavigator.pop(),
            child: Text('Salir'),
          ),
        ],
      ),
      barrierDismissible: false,
    );
  }
}
```

```dart
// ✅ SOLUCIÓN 2: Detección avanzada con safe_device
import 'package:safe_device/safe_device.dart';

class AdvancedSecurityService {
  Future<DeviceSecurityStatus> checkDeviceSecurity() async {
    final isJailBroken = await SafeDevice.isJailBroken;
    final canMockLocation = await SafeDevice.canMockLocation;
    final isRealDevice = await SafeDevice.isRealDevice;
    final isDevelopmentModeEnable = await SafeDevice.isDevelopmentModeEnable;
    final isOnExternalStorage = await SafeDevice.isOnExternalStorage;
    final isSafeDevice = await SafeDevice.isSafeDevice;
    
    return DeviceSecurityStatus(
      isJailBroken: isJailBroken,
      canMockLocation: canMockLocation,
      isRealDevice: isRealDevice,
      isDevelopmentModeEnable: isDevelopmentModeEnable,
      isOnExternalStorage: isOnExternalStorage,
      isSafeDevice: isSafeDevice,
    );
  }
  
  Future<void> enforceSecurityPolicy() async {
    final status = await checkDeviceSecurity();
    
    if (!status.isSafeDevice) {
      // ✅ Logging de dispositivo inseguro
      SecurityLogger.logUnauthorizedAttempt(
        'unsafe_device_detected',
        'device_security_check',
      );
      
      // ✅ Decisión basada en nivel de seguridad requerido
      if (status.isJailBroken) {
        // Alto riesgo - bloquear completamente
        _blockApp('Dispositivo con jailbreak/root detectado');
      } else if (status.isDevelopmentModeEnable) {
        // Medio riesgo - advertencia
        _showWarning('Modo desarrollador habilitado');
      } else if (status.canMockLocation) {
        // Bajo riesgo para la mayoría de apps
        _showWarning('Ubicación simulada detectada');
      }
    }
  }
  
  void _blockApp(String reason) {
    Get.offAll(() => BlockedScreen(reason: reason));
  }
  
  void _showWarning(String message) {
    Get.snackbar(
      'Advertencia de seguridad',
      message,
      duration: Duration(seconds: 5),
      backgroundColor: Colors.orange,
    );
  }
}

class DeviceSecurityStatus {
  final bool isJailBroken;
  final bool canMockLocation;
  final bool isRealDevice;
  final bool isDevelopmentModeEnable;
  final bool isOnExternalStorage;
  final bool isSafeDevice;
  
  DeviceSecurityStatus({
    required this.isJailBroken,
    required this.canMockLocation,
    required this.isRealDevice,
    required this.isDevelopmentModeEnable,
    required this.isOnExternalStorage,
    required this.isSafeDevice,
  });
}
```

```dart
// ✅ SOLUCIÓN 3: Integración en main.dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // ✅ Verificar seguridad del dispositivo al inicio
  final securityService = SecurityService();
  await securityService.checkDeviceSecurity();
  
  runApp(MyApp());
}
```

---

## Resumen M8

| Check | Severidad | Automatización | Esfuerzo Fix |
|-------|-----------|----------------|--------------|
| M8-A | MEDIUM | 🟢 100% | Bajo |
| M8-B | MEDIUM | 🟢 90% | Bajo |
| M8-C | MEDIUM | 🟡 40% | Medio |

**Total checks:** 3  
**Severidad crítica:** 0  
**Severidad alta:** 0  
**Severidad media:** 3  
**Severidad baja:** 0

---

**Última actualización:** 2025-11-12  
**Versión:** 1.0