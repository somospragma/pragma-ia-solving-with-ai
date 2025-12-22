# M5. Criptografía Insuficiente

Esta categoría cubre el uso de algoritmos criptográficos débiles o implementaciones incorrectas de criptografía.

---

## Check M5-A: Uso de algoritmos criptográficos débiles

**ID:** `M5-A-WEAK-CRYPTO`  
**Objetivo:** Detectar MD5, SHA1, DES, RC4 y otros algoritmos débiles.  
**Ámbito:** `lib/**.dart`

**Método de búsqueda:** Lexical search  
**Patterns inseguros:**

```dart
// PATRÓN 1: MD5 para passwords
import 'package:crypto/crypto.dart';

String hashPassword(String password) {
  return md5.convert(utf8.encode(password)).toString();  // ❌ MD5 es débil
}

// PATRÓN 2: SHA1 para datos sensibles
final hash = sha1.convert(utf8.encode(data));  // ⚠️ SHA1 está deprecado

// PATRÓN 3: Cifrado simétrico débil (simulado)
String encrypt(String data) {
  // Implementación custom insegura ❌
  return data.split('').reversed.join();
}

// PATRÓN 4: ECB mode (inseguro)
final cipher = AES.ECB();  // ❌ ECB no es seguro

// PATRÓN 5: Clave derivada de forma débil
final key = utf8.encode(password);  // ❌ No usa KDF
```

**Búsqueda lexical:**
```regex
md5\.convert.*password
\bsha1\.convert\b
\bDES\b|\bRC4\b|\bECB\b
AES\.ECB
utf8\.encode\(password\)(?!.*pbkdf2|argon2|scrypt)
```

**Criterio:**
- ❌ **Falla:** MD5/SHA1 usado para passwords o datos sensibles
- ❌ **Falla:** Algoritmos débiles (DES, RC4, ECB mode)
- ⚠️ **Advertencia:** Derivación de claves sin KDF
- ✅ **Cumple:** SHA256+, AES-GCM, PBKDF2/Argon2

**Severidad:** `HIGH`  
**Automatización:** 🟢 Alta (90%)

**Remediación:**

```dart
// ✅ SOLUCIÓN 1: SHA256 en lugar de MD5
import 'package:crypto/crypto.dart';

String hashData(String data) {
  return sha256.convert(utf8.encode(data)).toString();  // ✅ SHA256
}

// ✅ SOLUCIÓN 2: PBKDF2 para passwords
import 'package:pointycastle/export.dart';

String hashPassword(String password, String salt) {
  final pbkdf2 = PBKDF2KeyDerivator(HMac(SHA256Digest(), 64));
  
  pbkdf2.init(Pbkdf2Parameters(
    utf8.encode(salt),
    100000,  // ✅ 100k iteraciones
    32,      // 32 bytes de salida
  ));
  
  final key = pbkdf2.process(utf8.encode(password));
  return base64.encode(key);
}

// ✅ SOLUCIÓN 3: AES-GCM en lugar de ECB
import 'package:encrypt/encrypt.dart' as encrypt;

class SecureEncryption {
  // ✅ Generar clave segura
  static encrypt.Key generateKey() {
    return encrypt.Key.fromSecureRandom(32);  // AES-256
  }
  
  // ✅ Generar IV único por operación
  static encrypt.IV generateIV() {
    return encrypt.IV.fromSecureRandom(16);
  }
  
  // ✅ Cifrar con AES-GCM
  static String encryptData(String plaintext, encrypt.Key key) {
    final iv = generateIV();
    final encrypter = encrypt.Encrypter(
      encrypt.AES(key, mode: encrypt.AESMode.gcm),  // ✅ GCM mode
    );
    
    final encrypted = encrypter.encrypt(plaintext, iv: iv);
    
    // ✅ Retornar IV + ciphertext (ambos necesarios para descifrar)
    return '${iv.base64}:${encrypted.base64}';
  }
  
  // ✅ Descifrar
  static String decryptData(String ciphertext, encrypt.Key key) {
    final parts = ciphertext.split(':');
    final iv = encrypt.IV.fromBase64(parts[0]);
    final encrypted = encrypt.Encrypted.fromBase64(parts[1]);
    
    final encrypter = encrypt.Encrypter(
      encrypt.AES(key, mode: encrypt.AESMode.gcm),
    );
    
    return encrypter.decrypt(encrypted, iv: iv);
  }
}
```

```dart
// ✅ SOLUCIÓN 4: Argon2 (más seguro que PBKDF2)
import 'package:argon2/argon2.dart';

Future<String> hashPasswordWithArgon2(String password) async {
  final argon2 = Argon2();
  
  final result = await argon2.hashPasswordString(
    password,
    salt: Salt.newSalt(),  // ✅ Salt único
    iterations: 2,  // Iteraciones (memory-hard)
    memoryPowerOf2: 16,  // 64 MB de memoria
    desiredKeyLength: 32,
  );
  
  return result.encodedString;
}

Future<bool> verifyPassword(String password, String hash) async {
  final argon2 = Argon2();
  return await argon2.verifyHashString(password, hash);
}
```

---

## Check M5-B: Secretos y claves hardcodeadas

**ID:** `M5-B-HARDCODED-SECRETS`  
**Objetivo:** Detectar API keys, tokens, claves privadas en el código fuente.  
**Ámbito:** `lib/**.dart`, `android/**`, `ios/**`

**Método de búsqueda:** Lexical search con regex  
**Patterns:**

```dart
// PATRÓN 1: API keys
const API_KEY = 'AIzaSyC1234567890abcdefghijklmnop';  // ❌ Google API Key

// PATRÓN 2: AWS credentials
const AWS_ACCESS_KEY = 'AKIAIOSFODNN7EXAMPLE';  // ❌ AWS key

// PATRÓN 3: Stripe keys
const STRIPE_SECRET = 'sk_live_1234567890abcdefghijklmnop';  // ❌ Stripe secret

// PATRÓN 4: Private keys
const PRIVATE_KEY = '''
-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC...
-----END PRIVATE KEY-----
''';  // ❌❌ PELIGRO EXTREMO

// PATRÓN 5: Passwords hardcodeados
const DB_PASSWORD = 'MySecureP@ssw0rd123';  // ❌
```

**Búsqueda lexical con regex:**
```bash
# Google API Keys
grep -rE "AIza[0-9A-Za-z\-_]{35}" lib/ android/ ios/

# AWS Keys
grep -rE "AKIA[0-9A-Z]{16}" lib/ android/ ios/

# Stripe Keys
grep -rE "(sk|pk)_(live|test)_[0-9a-zA-Z]{24,}" lib/

# Generic secrets
grep -rE "(api[_-]?key|secret[_-]?key|password)\s*[:=]\s*['\"][^'\"]{16,}['\"]" lib/

# Private keys
grep -r "BEGIN.*PRIVATE KEY" lib/ android/ ios/

# JWT secrets
grep -rE "jwt[_-]?secret\s*[:=]" lib/

# Database URLs con credentials
grep -rE "mongodb://.*:.*@|postgres://.*:.*@|mysql://.*:.*@" lib/
```

**Criterio:**
- ❌ **Falla:** Cualquier patrón de API key/secret detectado
- ❌ **Falla:** Claves privadas en el código
- ⚠️ **Advertencia:** Constantes con nombres sospechosos (`API_KEY`, `SECRET`)
- ✅ **Cumple:** Uso de variables de entorno o backend

**Severidad:** `CRITICAL`  
**Automatización:** 🟢 Alta (95%)

**Remediación:**

```dart
// ❌ NUNCA HACER ESTO
const API_KEY = 'AIzaSyC1234567890abcdefghijklmnop';

// ✅ SOLUCIÓN 1: Dart defines (compile-time)
// Compilar: flutter build apk --dart-define=API_KEY=your_key_here
class AppConfig {
  static const apiKey = String.fromEnvironment('API_KEY');
  
  static void validate() {
    if (apiKey.isEmpty) {
      throw Exception('API_KEY no configurada');
    }
  }
}

// Uso
void main() {
  AppConfig.validate();
  runApp(MyApp());
}
```

```dart
// ✅ SOLUCIÓN 2: Obtener del backend
class ApiKeyService {
  Future<String> getApiKey() async {
    // ✅ Obtener desde backend autenticado
    final response = await http.get(
      Uri.parse('https://api.example.com/client-config'),
      headers: {'Authorization': 'Bearer $userToken'},
    );
    
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return data['api_key'];  // Key específica por usuario
    }
    
    throw Exception('No se pudo obtener API key');
  }
}
```

```dart
// ✅ SOLUCIÓN 3: Firebase Remote Config
import 'package:firebase_remote_config/firebase_remote_config.dart';

class RemoteConfigService {
  Future<String> getApiKey() async {
    final remoteConfig = FirebaseRemoteConfig.instance;
    
    await remoteConfig.setConfigSettings(RemoteConfigSettings(
      fetchTimeout: const Duration(seconds: 10),
      minimumFetchInterval: const Duration(hours: 1),
    ));
    
    await remoteConfig.fetchAndActivate();
    
    return remoteConfig.getString('api_key');
  }
}
```

```yaml
# ✅ SOLUCIÓN 4: .env files (no commitear)
# .env (agregar a .gitignore)
API_KEY=AIzaSyC1234567890abcdefghijklmnop
STRIPE_KEY=sk_test_xxxxxxxxxxxxx
```

```dart
// Usar flutter_dotenv
import 'package:flutter_dotenv/flutter_dotenv.dart';

Future<void> main() async {
  await dotenv.load(fileName: ".env");
  runApp(MyApp());
}

class ApiService {
  final apiKey = dotenv.env['API_KEY']!;
}
```

```gitignore
# ✅ .gitignore - OBLIGATORIO
.env
.env.local
.env.production
android/key.properties
ios/Runner/GoogleService-Info.plist
```

---

## Resumen M5

| Check | Severidad | Automatización | Esfuerzo Fix |
|-------|-----------|----------------|--------------|
| M5-A | HIGH | 🟢 90% | Medio |
| M5-B | CRITICAL | 🟢 95% | Bajo |

**Total checks:** 2  
**Severidad crítica:** 1  
**Severidad alta:** 1  
**Severidad media:** 0  
**Severidad baja:** 0

---

**Última actualización:** 2025-11-12  
**Versión:** 1.0