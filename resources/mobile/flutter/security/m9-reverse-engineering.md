# M9. Ingeniería Inversa

Esta categoría cubre la protección contra análisis del código y extracción de lógica de negocio.

---

## Check M9-A: Metadata y comentarios reveladores

**ID:** `M9-A-REVEALING-METADATA`  
**Objetivo:** Detectar comentarios, TODOs, y metadata que revelen información sensible.  
**Ámbito:** `lib/**.dart`, `pubspec.yaml`, `README.md`

**Método de búsqueda:** Lexical search  
**Patterns:**

```dart
// PATRÓN 1: TODOs con información sensible
// TODO: Cambiar password hardcodeado: admin123  // ❌ PELIGRO
// FIXME: API key temporal AIzaSyC1234567890  // ❌ PELIGRO
// HACK: Bypass de autenticación para testing  // ⚠️ Revelador

// PATRÓN 2: Comentarios con credenciales
// Credenciales de prueba:
// user: admin@example.com
// pass: Test123!  // ❌ PELIGRO

// PATRÓN 3: Comentarios sobre vulnerabilidades
// Esta función tiene un bug de seguridad pero funciona  // ⚠️ Revelador

// PATRÓN 4: URLs internas/staging
// const API_URL = 'https://internal-staging.company.com';  // ⚠️ Expone infraestructura

// PATRÓN 5: Metadata en pubspec.yaml
// pubspec.yaml
name: my_secret_project_codename  // ⚠️ Revelador
description: Internal admin tool with backdoor access  // ❌ PELIGRO
```

**Búsqueda lexical:**
```bash
# TODOs/FIXMEs con datos sensibles
grep -rE "TODO.*password|TODO.*secret|TODO.*admin|TODO.*key" lib/

# Comentarios con credenciales
grep -rE "//.*password.*:|//.*user.*:|//.*credential" lib/

# Comentarios sobre bugs/vulnerabilidades
grep -rE "//.*(bug|vulnerability|exploit|bypass|hack)" lib/

# URLs internas
grep -rE "(staging|internal|dev|test)\.(company|corp)" lib/

# Descripción reveladora en pubspec
grep -E "description:|name:" pubspec.yaml
```

**Criterio:**
- ❌ **Falla:** TODOs/comentarios con passwords, keys, o credenciales
- ⚠️ **Advertencia:** Comentarios que revelan lógica de seguridad
- ⚠️ **Advertencia:** Metadata reveladora (nombres internos, URLs)
- ✅ **Cumple:** Comentarios limpios, metadata genérica

**Severidad:** `LOW`  
**Automatización:** 🟢 Alta (85%)

**Remediación:**

```dart
// ❌ MAL
// TODO: Cambiar password hardcodeado: admin123
// FIXME: Esta API key es temporal: AIzaSyC1234567890

// ✅ BIEN
// TODO: Migrar a autenticación OAuth2
// FIXME: Obtener API key desde servidor de configuración

// ❌ MAL - Comentarios reveladores
// Esta función bypass autenticación si el usuario tiene email @company.com
if (email.endsWith('@company.com')) {
  return true;  // Backdoor para admins
}

// ✅ BIEN - Sin revelar lógica sensible
// Validación adicional para usuarios administrativos
if (_isAdminUser(email)) {
  return _validateAdminAccess();
}
```

```yaml
# ❌ MAL - pubspec.yaml
name: internal_banking_admin_backdoor
description: Admin tool with special access for internal auditing and backdoor access
homepage: https://internal-dev.banking-corp.com

# ✅ BIEN - pubspec.yaml
name: banking_admin_app
description: Administrative dashboard for banking operations
homepage: https://www.banking-corp.com
```

---

## Check M9-B: Código Dart sin ofuscar en producción

**ID:** `M9-B-UNOBFUSCATED-DART`  
**Objetivo:** Verificar que el código Dart esté ofuscado en builds de release.  
**Ámbito:** Scripts de build, workflows CI/CD

**Método de búsqueda:** Lexical search en archivos de automatización  
**Detección:**

```bash
# Buscar comandos de build sin --obfuscate
grep -r "flutter build" .github/workflows/ | grep -v "\--obfuscate"
grep -r "flutter build" .gitlab-ci.yml | grep -v "\--obfuscate"
grep -r "flutter build" Makefile | grep -v "\--obfuscate"
```

**Criterio:**
- ❌ **Falla:** `flutter build apk/ios` sin flag `--obfuscate`
- ⚠️ **Advertencia:** Ofuscación habilitada pero sin guardar símbolos
- ✅ **Cumple:** `--obfuscate` + `--split-debug-info` en todos los builds de release

**Severidad:** `MEDIUM`  
**Automatización:** 🟢 Alta (95%)

**Remediación:**

```yaml
# ✅ .github/workflows/release.yml
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
          # ✅ SIEMPRE incluir --obfuscate en producción
          flutter build apk --release \
            --obfuscate \
            --split-debug-info=build/app/outputs/symbols
          
      - name: Build App Bundle
        run: |
          flutter build appbundle --release \
            --obfuscate \
            --split-debug-info=build/app/outputs/symbols
          
      - name: Upload symbols to Firebase Crashlytics
        run: |
          # ✅ Subir símbolos para deobfuscar crash reports
          firebase crashlytics:symbols:upload \
            --app=1:1234567890:android:abc123 \
            build/app/outputs/symbols

  build-ios:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        
      - name: Build iOS with obfuscation
        run: |
          flutter build ios --release \
            --obfuscate \
            --split-debug-info=build/ios/symbols \
            --no-codesign
```

```makefile
# ✅ Makefile
.PHONY: build-release-android
build-release-android:
	@echo "Building Android release with obfuscation..."
	flutter build apk --release \
		--obfuscate \
		--split-debug-info=build/symbols/android \
		--target-platform android-arm,android-arm64

.PHONY: build-release-ios
build-release-ios:
	@echo "Building iOS release with obfuscation..."
	flutter build ios --release \
		--obfuscate \
		--split-debug-info=build/symbols/ios
```

```dart
// ✅ Configuración adicional en build.gradle
android {
    buildTypes {
        release {
            // ✅ Habilitar R8 full mode
            minifyEnabled true
            shrinkResources true
            
            // ✅ Usar ProGuard optimizado
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
            
            // ✅ Ofuscar nombres de recursos
            resourceShrinking 'strict'
        }
    }
}
```

---

## Estrategias adicionales de protección

### 1. String Obfuscation (Dart)

```dart
// ❌ Strings en claro son fáciles de extraer
const API_ENDPOINT = 'https://api.example.com/v1';
const SECRET_KEY = 'my_secret_key_123';

// ✅ Ofuscar strings sensibles (básico)
class ObfuscatedStrings {
  // Simple XOR obfuscation
  static String _decode(List<int> encoded, int key) {
    return String.fromCharCodes(
      encoded.map((byte) => byte ^ key),
    );
  }
  
  // Generado con script de ofuscación
  static String get apiEndpoint => _decode([
    104, 116, 116, 112, 115, 58, 47, 47, 97, 112, 105, 46, 101, 120, 97, 109, 112, 108, 101, 46, 99, 111, 109, 47, 118, 49
  ], 42);
}
```

### 2. Code Splitting

```dart
// ✅ Separar lógica sensible en archivos específicos
// lib/core/security/crypto_logic.dart
// lib/core/security/auth_logic.dart
// Estos archivos tendrán más ofuscación
```

### 3. Native Code para lógica crítica

```dart
// ✅ Para lógica MUY sensible, usar plugins nativos
// La ofuscación nativa (ProGuard/Swift) es más fuerte
import 'package:sensitive_logic/sensitive_logic.dart';

final result = await SensitiveLogic.performCriticalOperation();
```

---

## Resumen M9

| Check | Severidad | Automatización | Esfuerzo Fix |
|-------|-----------|----------------|--------------|
| M9-A | LOW | 🟢 85% | Bajo |
| M9-B | MEDIUM | 🟢 95% | Bajo |

**Total checks:** 2  
**Severidad crítica:** 0  
**Severidad alta:** 0  
**Severidad media:** 1  
**Severidad baja:** 1

---

**Última actualización:** 2025-11-12  
**Versión:** 1.0