# M4. Autenticación Insegura

Esta categoría cubre problemas relacionados con la implementación incorrecta de autenticación y gestión de sesiones.

---

## Check M4-A: Gestión insegura de sesión y tokens

**ID:** `M4-A-SESSION-MANAGEMENT`  
**Objetivo:** Detectar almacenamiento inseguro de tokens y falta de validación de expiración.  
**Ámbito:** `lib/**.dart`

**Método de búsqueda:** Semantic search  
**Patterns inseguros:**

```dart
// PATRÓN 1: Token en SharedPreferences
final prefs = await SharedPreferences.getInstance();
prefs.setString('auth_token', token);  // ❌ INSEGURO
prefs.setString('refresh_token', refreshToken);  // ❌ INSEGURO

// PATRÓN 2: JWT sin validación de expiración
String getToken() {
  return prefs.getString('token');  // ❌ No verifica si expiró
}

// PATRÓN 3: Token en variables globales
class AppState {
  static String authToken = '';  // ❌ INSEGURO
  static String userId = '';
}

// PATRÓN 4: No cerrar sesión al expirar
Future<void> makeApiCall() async {
  final response = await http.get(
    Uri.parse('https://api.example.com/data'),
    headers: {'Authorization': 'Bearer $token'},  // ❌ No valida expiración
  );
}

// PATRÓN 5: Refresh token sin rotación
Future<String> refreshAccessToken() async {
  final refreshToken = prefs.getString('refresh_token');
  final response = await http.post(
    Uri.parse('https://api.example.com/refresh'),
    body: {'refresh_token': refreshToken},
  );
  
  final newAccessToken = response.data['access_token'];
  prefs.setString('auth_token', newAccessToken);  // ❌ No actualiza refresh token
  
  return newAccessToken;
}
```

**Búsqueda lexical:**
```regex
SharedPreferences.*setString.*['\"](?:auth_)?token['\"]
prefs\.getString\(['\"]token['\"].*(?!.*isExpired|expired|exp)
static\s+String\s+.*token
```

**Criterio:**
- ❌ **Falla:** Tokens en SharedPreferences o variables globales
- ❌ **Falla:** No validar expiración de JWT antes de usar
- ⚠️ **Advertencia:** Refresh token sin rotación
- ✅ **Cumple:** Tokens en flutter_secure_storage + validación de expiración

**Severidad:** `HIGH`  
**Automatización:** 🟡 Media (60%)

**Remediación:**

```dart
// ✅ SOLUCIÓN 1: Almacenamiento seguro con FlutterSecureStorage
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:jwt_decoder/jwt_decoder.dart';

class AuthService {
  final _storage = FlutterSecureStorage();
  
  // ✅ Guardar tokens de forma segura
  Future<void> saveTokens(String accessToken, String refreshToken) async {
    await _storage.write(key: 'access_token', value: accessToken);
    await _storage.write(key: 'refresh_token', value: refreshToken);
  }
  
  // ✅ Obtener token con validación de expiración
  Future<String?> getValidAccessToken() async {
    final token = await _storage.read(key: 'access_token');
    
    if (token == null) return null;
    
    // ✅ Verificar si el token expiró
    if (JwtDecoder.isExpired(token)) {
      // Intentar refrescar
      return await refreshAccessToken();
    }
    
    return token;
  }
  
  // ✅ Refresh con rotación de tokens
  Future<String?> refreshAccessToken() async {
    final refreshToken = await _storage.read(key: 'refresh_token');
    
    if (refreshToken == null) {
      await logout();
      return null;
    }
    
    try {
      final response = await http.post(
        Uri.parse('https://api.example.com/auth/refresh'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'refresh_token': refreshToken}),
      );
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        
        // ✅ Guardar AMBOS tokens (rotación)
        await saveTokens(
          data['access_token'],
          data['refresh_token'],  // ✅ Nuevo refresh token
        );
        
        return data['access_token'];
      } else {
        await logout();
        return null;
      }
    } catch (e) {
      await logout();
      return null;
    }
  }
  
  // ✅ Logout limpia todo
  Future<void> logout() async {
    await _storage.delete(key: 'access_token');
    await _storage.delete(key: 'refresh_token');
    await _storage.deleteAll();
  }
}
```

```dart
// ✅ SOLUCIÓN 2: HTTP Interceptor con refresh automático
import 'package:dio/dio.dart';

class AuthInterceptor extends Interceptor {
  final AuthService _authService;
  
  AuthInterceptor(this._authService);
  
  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) async {
    // ✅ Obtener token válido (con auto-refresh)
    final token = await _authService.getValidAccessToken();
    
    if (token != null) {
      options.headers['Authorization'] = 'Bearer $token';
    }
    
    handler.next(options);
  }
  
  @override
  void onError(DioError err, ErrorInterceptorHandler handler) async {
    // ✅ Si recibimos 401, intentar refresh
    if (err.response?.statusCode == 401) {
      final newToken = await _authService.refreshAccessToken();
      
      if (newToken != null) {
        // ✅ Reintentar request con nuevo token
        final options = err.requestOptions;
        options.headers['Authorization'] = 'Bearer $newToken';
        
        try {
          final response = await Dio().fetch(options);
          handler.resolve(response);
          return;
        } catch (e) {
          // Falló el retry
        }
      }
      
      // ✅ No se pudo refrescar, forzar logout
      await _authService.logout();
    }
    
    handler.next(err);
  }
}
```

```dart
// ✅ SOLUCIÓN 3: Validación de expiración con margen de seguridad
class TokenValidator {
  // ✅ Verificar con margen de 5 minutos antes de expirar
  static bool isTokenValid(String token) {
    try {
      final decodedToken = JwtDecoder.decode(token);
      final exp = decodedToken['exp'];
      
      if (exp == null) return false;
      
      final expiryDate = DateTime.fromMillisecondsSinceEpoch(exp * 1000);
      final now = DateTime.now();
      
      // ✅ Refrescar 5 minutos antes de expirar
      final margin = Duration(minutes: 5);
      
      return expiryDate.isAfter(now.add(margin));
    } catch (e) {
      return false;
    }
  }
  
  // ✅ Obtener tiempo hasta expiración
  static Duration? getTimeUntilExpiry(String token) {
    try {
      final decodedToken = JwtDecoder.decode(token);
      final exp = decodedToken['exp'];
      
      if (exp == null) return null;
      
      final expiryDate = DateTime.fromMillisecondsSinceEpoch(exp * 1000);
      final now = DateTime.now();
      
      return expiryDate.difference(now);
    } catch (e) {
      return null;
    }
  }
}
```

```dart
// ✅ SOLUCIÓN 4: Biometría para re-autenticación
import 'package:local_auth/local_auth.dart';

class BiometricAuthService {
  final LocalAuthentication _localAuth = LocalAuthentication();
  
  // ✅ Requerir biometría en operaciones sensibles
  Future<bool> authenticateForSensitiveOperation() async {
    try {
      final canCheckBiometrics = await _localAuth.canCheckBiometrics;
      
      if (!canCheckBiometrics) return false;
      
      final authenticated = await _localAuth.authenticate(
        localizedReason: 'Por favor autentícate para continuar',
        options: const AuthenticationOptions(
          useErrorDialogs: true,
          stickyAuth: true,
          biometricOnly: true,  // ✅ Solo biometría, no PIN
        ),
      );
      
      return authenticated;
    } catch (e) {
      return false;
    }
  }
}
```

---

## Resumen M4

| Check | Severidad | Automatización | Esfuerzo Fix |
|-------|-----------|----------------|--------------|
| M4-A | HIGH | 🟡 60% | Alto |

**Total checks:** 1  
**Severidad crítica:** 0  
**Severidad alta:** 1  
**Severidad media:** 0  
**Severidad baja:** 0

---

**Última actualización:** 2025-11-12  
**Versión:** 1.0