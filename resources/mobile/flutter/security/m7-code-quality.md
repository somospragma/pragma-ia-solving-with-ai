# M7. Calidad del Código Cliente

Esta categoría cubre problemas de calidad de código que pueden llevar a vulnerabilidades de seguridad.

---

## Check M7-A: Logging de información sensible

**ID:** `M7-A-SENSITIVE-LOGGING`  
**Objetivo:** Detectar logs que exponen tokens, passwords, PII en consola o archivos.  
**Ámbito:** `lib/**.dart`

**Método de búsqueda:** Lexical search  
**Patterns inseguros:**

```dart
// PATRÓN 1: print() con datos sensibles
print('User token: $authToken');  // ❌ PELIGRO
print('Password: $userPassword');  // ❌ PELIGRO
print('API Response: ${response.body}');  // ⚠️ Puede contener datos sensibles

// PATRÓN 2: debugPrint sin condicional
debugPrint('Credit card: ${creditCard.number}');  // ❌ PELIGRO

// PATRÓN 3: Logger con nivel incorrecto
logger.info('Auth token: $token');  // ❌ Token en logs

// PATRÓN 4: Logging de excepciones con datos sensibles
try {
  await api.login(email, password);
} catch (e) {
  print('Login failed: $email, $password, $e');  // ❌❌ PELIGRO EXTREMO
}

// PATRÓN 5: Developer menu con datos sensibles
void _showDebugInfo() {
  showDialog(
    context: context,
    builder: (context) => AlertDialog(
      title: Text('Debug Info'),
      content: Text('Token: $token\nUser ID: $userId'),  // ❌ Expone datos
    ),
  );
}
```

**Búsqueda lexical:**
```regex
(print|debugPrint|logger\.(info|debug|warning))\([^)]*\b(token|password|secret|api[_-]?key|ssn|credit|cvv|pin)\b
print.*response\.body
print.*stackTrace
catch.*print.*password
```

**Criterio:**
- ❌ **Falla:** Logs con tokens, passwords, API keys, PII
- ⚠️ **Advertencia:** Logging de response bodies sin sanitización
- ✅ **Cumple:** Logs condicionales con `kDebugMode` + datos sanitizados

**Severidad:** `MEDIUM`  
**Automatización:** 🟢 Alta (85%)

**Remediación:**

```dart
// ✅ SOLUCIÓN 1: Logging condicional solo en debug
import 'package:flutter/foundation.dart';

void logDebug(String message) {
  if (kDebugMode) {
    print(message);
  }
}

// Uso
logDebug('User logged in: $userId');  // ✅ Solo en debug

// ✅ SOLUCIÓN 2: Logger con sanitización
class SecureLogger {
  static final _sensitivePatterns = [
    RegExp(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),  // Emails
    RegExp(r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b'),  // Credit cards
    RegExp(r'\b\d{3}-\d{2}-\d{4}\b'),  // SSN
    RegExp(r'Bearer\s+[A-Za-z0-9\-._~+/]+=*'),  // Bearer tokens
    RegExp(r'AIza[0-9A-Za-z\-_]{35}'),  // Google API keys
  ];
  
  static String sanitize(String message) {
    var sanitized = message;
    
    for (var pattern in _sensitivePatterns) {
      sanitized = sanitized.replaceAll(pattern, '***REDACTED***');
    }
    
    return sanitized;
  }
  
  static void log(String message) {
    if (kDebugMode) {
      print(sanitize(message));
    }
  }
  
  static void logError(String message, [dynamic error, StackTrace? stackTrace]) {
    final sanitizedMessage = sanitize(message);
    final sanitizedError = error != null ? sanitize(error.toString()) : '';
    
    if (kDebugMode) {
      print('ERROR: $sanitizedMessage');
      if (sanitizedError.isNotEmpty) {
        print('Details: $sanitizedError');
      }
      if (stackTrace != null) {
        print(stackTrace);
      }
    }
    
    // ✅ Enviar a servicio de logging (sin datos sensibles)
    _sendToRemoteLogging(sanitizedMessage, sanitizedError);
  }
  
  static Future<void> _sendToRemoteLogging(String message, String error) async {
    // Firebase Crashlytics, Sentry, etc.
  }
}
```

```dart
// ✅ SOLUCIÓN 3: Interceptor HTTP con sanitización
class LoggingInterceptor extends Interceptor {
  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    if (kDebugMode) {
      final sanitizedHeaders = _sanitizeHeaders(options.headers);
      final sanitizedData = _sanitizeData(options.data);
      
      print('→ ${options.method} ${options.uri}');
      print('  Headers: $sanitizedHeaders');
      print('  Data: $sanitizedData');
    }
    
    handler.next(options);
  }
  
  @override
  void onResponse(Response response, ResponseInterceptorHandler handler) {
    if (kDebugMode) {
      final sanitizedData = _sanitizeData(response.data);
      
      print('← ${response.statusCode} ${response.requestOptions.uri}');
      print('  Data: $sanitizedData');
    }
    
    handler.next(response);
  }
  
  Map<String, dynamic> _sanitizeHeaders(Map<String, dynamic> headers) {
    final sanitized = Map<String, dynamic>.from(headers);
    
    // ✅ Ocultar headers sensibles
    const sensitiveHeaders = ['Authorization', 'Cookie', 'X-API-Key'];
    
    for (var header in sensitiveHeaders) {
      if (sanitized.containsKey(header)) {
        sanitized[header] = '***REDACTED***';
      }
    }
    
    return sanitized;
  }
  
  dynamic _sanitizeData(dynamic data) {
    if (data == null) return null;
    
    if (data is Map) {
      final sanitized = Map<String, dynamic>.from(data);
      
      // ✅ Ocultar campos sensibles
      const sensitiveFields = [
        'password', 'token', 'secret', 'api_key',
        'credit_card', 'ssn', 'pin', 'cvv'
      ];
      
      for (var field in sensitiveFields) {
        if (sanitized.containsKey(field)) {
          sanitized[field] = '***REDACTED***';
        }
      }
      
      return sanitized;
    }
    
    return data;
  }
}
```

```dart
// ✅ SOLUCIÓN 4: Manejo seguro de excepciones
Future<void> loginUser(String email, String password) async {
  try {
    await api.login(email, password);
  } catch (e, stackTrace) {
    // ❌ NUNCA hacer esto:
    // print('Login failed: $email, $password, $e');
    
    // ✅ Logging seguro:
    SecureLogger.logError(
      'Login failed for user',  // No incluir email
      e,
      stackTrace,
    );
    
    // ✅ Enviar a analytics (sin PII)
    FirebaseAnalytics.instance.logEvent(
      name: 'login_failed',
      parameters: {
        'error_type': e.runtimeType.toString(),
        'timestamp': DateTime.now().toIso8601String(),
        // NO incluir email, password, o detalles del usuario
      },
    );
  }
}
```

---

## Check M7-B: Manejo inadecuado de excepciones

**ID:** `M7-B-POOR-EXCEPTION-HANDLING`  
**Objetivo:** Detectar bloques catch vacíos o que exponen stack traces al usuario.  
**Ámbito:** `lib/**.dart`

**Método de búsqueda:** Lexical search  
**Patterns inseguros:**

```dart
// PATRÓN 1: Catch vacío
try {
  await riskyOperation();
} catch (e) {
  // ❌ Ignorar silenciosamente
}

// PATRÓN 2: Catch genérico sin logging
try {
  await api.fetchData();
} catch (e) {
  return null;  // ⚠️ Falla silenciosamente
}

// PATRÓN 3: Mostrar stack trace al usuario
try {
  await processPayment();
} catch (e, stackTrace) {
  showDialog(
    context: context,
    builder: (context) => AlertDialog(
      title: Text('Error'),
      content: Text('$e\n$stackTrace'),  // ❌❌ Expone detalles internos
    ),
  );
}

// PATRÓN 4: Catch demasiado amplio
try {
  await complexOperation();
} on Exception catch (e) {
  // ⚠️ Captura todo Exception, puede ocultar bugs
  print('Something went wrong');
}
```

**Búsqueda lexical:**
```regex
catch\s*\([^)]+\)\s*\{\s*\}
catch.*\n.*showDialog.*stackTrace
catch.*\n.*Text\(.*\$e
on\s+Exception\s+catch
```

**Criterio:**
- ❌ **Falla:** Bloques catch vacíos
- ❌ **Falla:** Stack traces mostrados al usuario
- ⚠️ **Advertencia:** Catch genéricos sin logging
- ✅ **Cumple:** Logging apropiado + mensajes user-friendly

**Severidad:** `MEDIUM`  
**Automatización:** 🟢 Alta (80%)

**Remediación:**

```dart
// ✅ SOLUCIÓN 1: Manejo específico de excepciones
Future<User?> fetchUserProfile(String userId) async {
  try {
    final response = await api.getUser(userId);
    return User.fromJson(response.data);
    
  } on NetworkException catch (e) {
    // ✅ Error de red - mensaje específico
    SecureLogger.logError('Network error fetching user', e);
    _showUserMessage('No hay conexión a internet');
    return null;
    
  } on UnauthorizedException catch (e) {
    // ✅ No autorizado - redirigir a login
    SecureLogger.logError('Unauthorized access', e);
    _handleUnauthorized();
    return null;
    
  } on ValidationException catch (e) {
    // ✅ Error de validación - mostrar al usuario
    _showUserMessage(e.message);
    return null;
    
  } catch (e, stackTrace) {
    // ✅ Error inesperado - logging completo
    SecureLogger.logError('Unexpected error fetching user', e, stackTrace);
    _showUserMessage('Ocurrió un error inesperado');
    
    // ✅ Reportar a Crashlytics
    FirebaseCrashlytics.instance.recordError(e, stackTrace);
    
    return null;
  }
}

void _showUserMessage(String message) {
  Get.snackbar(
    'Error',
    message,  // ✅ Mensaje user-friendly, NO stack traces
    snackPosition: SnackPosition.BOTTOM,
  );
}
```

```dart
// ✅ SOLUCIÓN 2: Excepciones personalizadas
class AppException implements Exception {
  final String message;
  final String? code;
  final dynamic originalError;
  
  AppException(this.message, {this.code, this.originalError});
  
  @override
  String toString() => message;
}

class NetworkException extends AppException {
  NetworkException(String message, {dynamic originalError})
      : super(message, code: 'NETWORK_ERROR', originalError: originalError);
}

class UnauthorizedException extends AppException {
  UnauthorizedException(String message)
      : super(message, code: 'UNAUTHORIZED');
}

class ValidationException extends AppException {
  final Map<String, String>? fieldErrors;
  
  ValidationException(String message, {this.fieldErrors})
      : super(message, code: 'VALIDATION_ERROR');
}
```

```dart
// ✅ SOLUCIÓN 3: Global error handler
class GlobalErrorHandler {
  static void handleError(dynamic error, StackTrace? stackTrace) {
    // ✅ Logging seguro
    SecureLogger.logError('Global error', error, stackTrace);
    
    // ✅ Reportar a servicio de monitoreo
    if (!kDebugMode) {
      FirebaseCrashlytics.instance.recordError(error, stackTrace);
    }
    
    // ✅ Mostrar mensaje apropiado al usuario
    String userMessage = 'Ocurrió un error inesperado';
    
    if (error is AppException) {
      userMessage = error.message;
    } else if (error is NetworkException) {
      userMessage = 'No hay conexión a internet';
    }
    
    Get.snackbar('Error', userMessage);
  }
}

// Uso en main.dart
void main() {
  FlutterError.onError = (details) {
    GlobalErrorHandler.handleError(details.exception, details.stack);
  };
  
  PlatformDispatcher.instance.onError = (error, stack) {
    GlobalErrorHandler.handleError(error, stack);
    return true;
  };
  
  runApp(MyApp());
}
```

---

## Resumen M7

| Check | Severidad | Automatización | Esfuerzo Fix |
|-------|-----------|----------------|--------------|
| M7-A | MEDIUM | 🟢 85% | Medio |
| M7-B | MEDIUM | 🟢 80% | Medio |

**Total checks:** 2  
**Severidad crítica:** 0  
**Severidad alta:** 0  
**Severidad media:** 2  
**Severidad baja:** 0

---

**Última actualización:** 2025-11-12  
**Versión:** 1.0