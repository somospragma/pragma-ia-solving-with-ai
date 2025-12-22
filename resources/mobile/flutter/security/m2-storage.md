# M2. Almacenamiento Inseguro de Datos

Esta categoría cubre el almacenamiento inseguro de datos sensibles en el dispositivo, incluyendo texto plano, bases de datos sin cifrar y caché.

---

## Check M2-A: Almacenamiento de datos sensibles en texto plano

**ID:** `M2-A-PLAINTEXT-STORAGE`  
**Objetivo:** Evitar guardar tokens, passwords, PII en almacenamiento no cifrado.  
**Ámbito:** `lib/**.dart`

**Método de búsqueda:** Semantic + Lexical search  
**Patterns de código inseguro:**

```dart
// PATRÓN 1: SharedPreferences con datos sensibles
SharedPreferences prefs = await SharedPreferences.getInstance();
prefs.setString('token', authToken);        // INSEGURO
prefs.setString('password', userPass);      // INSEGURO
prefs.setString('api_key', apiKey);         // INSEGURO
prefs.setString('refresh_token', refresh);  // INSEGURO

// PATRÓN 2: File storage sin cifrado
final file = File('${dir.path}/credentials.txt');
await file.writeAsString(token);            // INSEGURO

// PATRÓN 3: Hive sin cifrado
final box = await Hive.openBox('secure');   // INSEGURO si contiene datos sensibles
box.put('token', authToken);
```

**Búsqueda lexical:**
```regex
SharedPreferences.*\.(setString|setInt)\s*\(\s*['"](?:token|password|secret|key|credential|pin|ssn|credit)
File\(.*\)\.writeAsString\([^)]*(?:token|password|secret)
Hive\.openBox(?!\(.*encryptionKey).*\n.*\.put\([^)]*(?:token|password)
```

**Criterio:**
- ❌ **Falla:** Datos sensibles en SharedPreferences, File, o Hive sin cifrado
- ✅ **Cumple:** Uso de `flutter_secure_storage` o Hive con `HiveAesCipher`

**Severidad:** `CRITICAL`  
**Automatización:** 🟢 Alta (90%)

**Remediación:**

```dart
// ✅ SOLUCIÓN 1: flutter_secure_storage (Keychain/Keystore)
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

final storage = FlutterSecureStorage();

// Guardar
await storage.write(key: 'auth_token', value: token);
await storage.write(key: 'refresh_token', value: refreshToken);

// Leer
final token = await storage.read(key: 'auth_token');

// Eliminar al logout
await storage.delete(key: 'auth_token');
await storage.deleteAll();
```

```dart
// ✅ SOLUCIÓN 2: Hive con cifrado
import 'package:hive/hive.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

// Generar o recuperar clave de cifrado
final secureStorage = FlutterSecureStorage();
var encryptionKeyString = await secureStorage.read(key: 'hive_encryption_key');

if (encryptionKeyString == null) {
  final key = Hive.generateSecureKey();
  await secureStorage.write(
    key: 'hive_encryption_key',
    value: base64UrlEncode(key),
  );
  encryptionKeyString = base64UrlEncode(key);
}

final encryptionKey = base64Url.decode(encryptionKeyString);

// Abrir box cifrado
final encryptedBox = await Hive.openBox(
  'secureBox',
  encryptionCipher: HiveAesCipher(encryptionKey),
);

// Uso normal
encryptedBox.put('token', authToken);
```

**Falsos positivos permitidos:**
```dart
// OK: Datos NO sensibles en SharedPreferences
prefs.setBool('theme_mode_dark', true);      // OK
prefs.setString('language', 'es');           // OK
prefs.setInt('onboarding_completed', 1);     // OK
```

---

## Check M2-B: Base de datos local sin cifrado

**ID:** `M2-B-UNENCRYPTED-DB`  
**Objetivo:** Detectar SQLite/Drift sin cifrado para datos sensibles.  
**Ámbito:** `lib/**.dart`, `pubspec.yaml`

**Método de búsqueda:** Lexical search de imports + Semantic search  
**Detección:**

```yaml
# pubspec.yaml - Verificar dependencias
dependencies:
  sqflite: ^2.0.0        # ⚠️ Sin cifrado
  # Debería ser:
  # sqflite_sqlcipher: ^2.0.0  # ✅ Con cifrado
  
  drift: ^2.0.0          # ⚠️ Verificar configuración
```

```dart
// PATRÓN INSEGURO: sqflite sin cifrado
import 'package:sqflite/sqflite.dart';

final database = await openDatabase('app.db');  // ⚠️ Sin password

// Guardar datos sensibles
await db.insert('users', {
  'email': email,
  'token': authToken,     // ⚠️ INSEGURO
});
```

**Búsqueda lexical:**
```regex
import\s+['"]package:sqflite/sqflite\.dart['"](?!.*sqlcipher)
openDatabase\s*\([^)]*\)(?!.*password)
```

**Criterio:**
- ❌ **Falla:** `sqflite` usado sin `sqlcipher` + datos sensibles detectados
- ✅ **Cumple:** `sqflite_sqlcipher` o `drift` con cifrado

**Severidad:** `CRITICAL`  
**Automatización:** 🟢 Alta (85%)

**Remediación:**

```dart
// ✅ SOLUCIÓN 1: sqflite_sqlcipher
import 'package:sqflite_sqlcipher/sqflite.dart';

final database = await openDatabase(
  'app.db',
  password: encryptionKey,  // ✅ Cifrado
  version: 1,
  onCreate: (db, version) async {
    await db.execute('''
      CREATE TABLE users(
        id INTEGER PRIMARY KEY,
        email TEXT,
        token TEXT
      )
    ''');
  },
);
```

```dart
// ✅ SOLUCIÓN 2: Drift con cifrado
import 'package:drift/drift.dart';
import 'package:drift/native.dart';
import 'package:sqlite3/sqlite3.dart';
import 'package:path/path.dart' as p;

LazyDatabase _openConnection() {
  return LazyDatabase(() async {
    final dbFolder = await getApplicationDocumentsDirectory();
    final file = File(p.join(dbFolder.path, 'app.db'));
    
    return NativeDatabase(file, setup: (database) {
      // ✅ Habilitar cifrado SQLCipher
      database.execute("PRAGMA key = '$encryptionKey';");
    });
  });
}

@DriftDatabase(tables: [Users])
class AppDatabase extends _$AppDatabase {
  AppDatabase() : super(_openConnection());
  
  @override
  int get schemaVersion => 1;
}
```

---

## Check M2-C: Datos sensibles en caché y archivos temporales

**ID:** `M2-C-CACHE-LEAKAGE`  
**Objetivo:** Detectar persistencia de datos sensibles en caché/temp.  
**Ámbito:** `lib/**.dart`

**Método de búsqueda:** Semantic search  
**Patterns:**

```dart
// PATRÓN 1: Uso de Directory.systemTemp con datos sensibles
final tempDir = await getTemporaryDirectory();
final file = File('${tempDir.path}/token.txt');
await file.writeAsString(token);  // ⚠️ INSEGURO

// PATRÓN 2: CachedNetworkImage con headers de autenticación
CachedNetworkImage(
  imageUrl: 'https://api.com/user/avatar',
  httpHeaders: {'Authorization': 'Bearer $token'},  // ⚠️ Token en caché
)

// PATRÓN 3: HTTP client cache con datos sensibles
final dio = Dio();
dio.interceptors.add(DioCacheInterceptor());  // ⚠️ Puede cachear tokens
```

**Criterio:**
- ⚠️ **Advertencia:** Archivos temporales con datos potencialmente sensibles
- ❌ **Falla:** Caché de imágenes con headers de autenticación

**Severidad:** `MEDIUM`  
**Automatización:** 🟡 Media (65%)

**Remediación:**

```dart
// ✅ SOLUCIÓN 1: Evitar caché con autenticación
CachedNetworkImage(
  imageUrl: 'https://api.com/user/avatar',
  cacheKey: 'avatar_${userId}_${timestamp}',  // Cache key único sin token
  // NO incluir headers de auth aquí
)

// Obtener imagen con auth en backend proxy o signed URL

// ✅ SOLUCIÓN 2: Limpiar archivos temporales al logout
Future<void> clearSensitiveData() async {
  // Limpiar secure storage
  await FlutterSecureStorage().deleteAll();
  
  // Limpiar caché de imágenes
  await DefaultCacheManager().emptyCache();
  
  // Limpiar archivos temporales custom
  final tempDir = await getTemporaryDirectory();
  if (tempDir.existsSync()) {
    tempDir.deleteSync(recursive: true);
  }
}
```

```dart
// ✅ SOLUCIÓN 3: Configurar Dio sin caché de headers sensibles
final dio = Dio();

dio.interceptors.add(
  DioCacheInterceptor(
    options: CacheOptions(
      store: MemCacheStore(),  // Solo en memoria
      policy: CachePolicy.noCache,  // No cachear por defecto
      hitCacheOnErrorExcept: [401, 403],  // No usar caché en errores de auth
      maxStale: const Duration(hours: 1),
      priority: CachePriority.normal,
      cipher: null,  // No cachear datos sensibles
      keyBuilder: (request) {
        // ✅ No incluir headers de auth en la cache key
        return request.uri.toString();
      },
      allowPostMethod: false,  // No cachear POST
    ),
  ),
);

// Agregar auth después del interceptor de caché
dio.interceptors.add(
  InterceptorsWrapper(
    onRequest: (options, handler) {
      options.headers['Authorization'] = 'Bearer $token';
      return handler.next(options);
    },
  ),
);
```

---

## Resumen M2

| Check | Severidad | Automatización | Esfuerzo Fix |
|-------|-----------|----------------|--------------|
| M2-A | CRITICAL | 🟢 90% | Alto |
| M2-B | CRITICAL | 🟢 85% | Alto |
| M2-C | MEDIUM | 🟡 65% | Medio |

**Total checks:** 3  
**Severidad crítica:** 2  
**Severidad alta:** 1  
**Severidad media:** 0  
**Severidad baja:** 0

---

**Última actualización:** 2025-11-12  
**Versión:** 1.0