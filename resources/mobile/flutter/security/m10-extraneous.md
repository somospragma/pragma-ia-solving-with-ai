# M10. Funcionalidad Extraña

Esta categoría cubre código de debugging, backdoors, y funcionalidad no destinada a producción.

---

## Check M10-A: Features y endpoints de debugging

**ID:** `M10-A-DEBUG-FEATURES`  
**Objetivo:** Detectar rutas, menús, o funcionalidad de debug accesible en producción.  
**Ámbito:** `lib/**.dart`

**Método de búsqueda:** Lexical + Semantic search  
**Patterns:**

```dart
// PATRÓN 1: Rutas de debug
final routes = {
  '/': (context) => HomeScreen(),
  '/profile': (context) => ProfileScreen(),
  '/debug': (context) => DebugScreen(),  // ❌ Ruta de debug
  '/test': (context) => TestScreen(),    // ❌ Ruta de test
  '/dev': (context) => DevToolsScreen(), // ❌ Herramientas de dev
};

// PATRÓN 2: Dev menu siempre habilitado
class AppSettings {
  static const bool enableDevMenu = true;  // ❌ PELIGRO
}

// PATRÓN 3: Bypass de autenticación
Future<bool> login(String email, String password) async {
  // ❌❌ PELIGRO EXTREMO - Backdoor
  if (email == 'admin@dev.com' && password == 'dev123') {
    return true;
  }
  
  return await _authenticateWithServer(email, password);
}

// PATRÓN 4: Logs de debugging sin condicional
void processPayment(Payment payment) {
  // ❌ Debug logging sin kDebugMode
  print('Processing payment: ${payment.toJson()}');
  debugPrint('Card number: ${payment.cardNumber}');
  
  _submitPayment(payment);
}

// PATRÓN 5: Gestos secretos para abrir debug panel
Widget build(BuildContext context) {
  return GestureDetector(
    onLongPress: () {
      // ❌ Siempre disponible, debería ser solo en debug
      Navigator.push(context, MaterialPageRoute(
        builder: (context) => DebugPanel(),
      ));
    },
    child: MyApp(),
  );
}
```

**Búsqueda lexical:**
```bash
# Rutas de debug/test/dev
grep -rE "['\"]/(debug|test|dev|admin|backdoor)['\"]" lib/ --exclude-dir=test

# Dev menu habilitado
grep -r "enableDevMenu\s*=\s*true" lib/

# Bypass de autenticación
grep -r "bypassAuth\|skipAuth\|devLogin" lib/

# Debug panels sin condicional
grep -r "DebugPanel\|DebugScreen\|DevTools" lib/ | grep -v "kDebugMode"
```

**Criterio:**
- ❌ **Falla:** Rutas `/debug`, `/test`, `/dev` accesibles
- ❌ **Falla:** Bypass de autenticación o backdoors
- ⚠️ **Advertencia:** Dev menu sin protección por `kDebugMode`
- ✅ **Cumple:** Funcionalidad de debug solo disponible en debug builds

**Severidad:** `HIGH`  
**Automatización:** 🟢 Alta (80%)

**Remediación:**

```dart
// ✅ SOLUCIÓN 1: Rutas condicionales basadas en build mode
import 'package:flutter/foundation.dart';

class AppRoutes {
  static Map<String, WidgetBuilder> getRoutes() {
    final routes = <String, WidgetBuilder>{
      '/': (context) => HomeScreen(),
      '/profile': (context) => ProfileScreen(),
      '/settings': (context) => SettingsScreen(),
    };
    
    // ✅ Rutas de debug solo en modo debug
    if (kDebugMode) {
      routes.addAll({
        '/debug': (context) => DebugScreen(),
        '/test': (context) => TestScreen(),
      });
    }
    
    return routes;
  }
}

// Uso en MaterialApp
MaterialApp(
  routes: AppRoutes.getRoutes(),
  ...
)
```

```dart
// ✅ SOLUCIÓN 2: Dev menu protegido
import 'package:flutter/foundation.dart';

class DevMenu extends StatelessWidget {
  // ✅ Solo disponible en debug
  static bool get isAvailable => kDebugMode;
  
  @override
  Widget build(BuildContext context) {
    // ✅ Doble verificación
    if (!kDebugMode) {
      return SizedBox.shrink();
    }
    
    return FloatingActionButton(
      onPressed: () => _showDevPanel(context),
      child: Icon(Icons.developer_mode),
    );
  }
  
  void _showDevPanel(BuildContext context) {
    showModalBottomSheet(
      context: context,
      builder: (context) => DevPanelContent(),
    );
  }
}
```

```dart
// ✅ SOLUCIÓN 3: Eliminar backdoors completamente
// ❌ NUNCA hacer esto
Future<bool> login(String email, String password) async {
  if (email == 'admin@dev.com' && password == 'dev123') {
    return true;  // ❌❌ BACKDOOR
  }
  return await _authenticateWithServer(email, password);
}

// ✅ Autenticación sin bypass
Future<bool> login(String email, String password) async {
  // ✅ SIEMPRE autenticar con servidor
  return await _authenticateWithServer(email, password);
}

// ✅ Si necesitas credenciales de prueba, usa entorno de staging
Future<bool> login(String email, String password) async {
  // Validación solo en entorno de desarrollo
  if (kDebugMode && _isTestCredential(email)) {
    return await _authenticateWithTestServer(email, password);
  }
  
  // Producción siempre usa servidor real
  return await _authenticateWithServer(email, password);
}
```

```dart
// ✅ SOLUCIÓN 4: Debug panel con seguridad
class SecureDebugPanel extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    // ✅ Triple verificación
    if (!kDebugMode) return SizedBox.shrink();
    
    return GestureDetector(
      // ✅ Gesto complejo (no accidental)
      onLongPress: () {
        if (kDebugMode) {
          _showAuthenticatedDebugPanel(context);
        }
      },
      child: Container(
        width: 50,
        height: 50,
        color: Colors.transparent,
      ),
    );
  }
  
  Future<void> _showAuthenticatedDebugPanel(BuildContext context) async {
    // ✅ Requiere contraseña incluso en debug (opcional)
    final authenticated = await _showPasswordDialog(context);
    
    if (authenticated) {
      Navigator.push(
        context,
        MaterialPageRoute(builder: (context) => DebugPanel()),
      );
    }
  }
}
```

---

## Check M10-B: Paquetes de desarrollo en dependencies

**ID:** `M10-B-DEV-DEPENDENCIES`  
**Objetivo:** Verificar que paquetes de testing no estén en `dependencies` (solo en `dev_dependencies`).  
**Ámbito:** `pubspec.yaml`

**Método de búsqueda:** Lexical search  
**Pattern:**

```yaml
# ❌ MAL - Paquetes de test en dependencies
dependencies:
  flutter:
    sdk: flutter
  mockito: ^5.4.0      # ❌ Debería estar en dev_dependencies
  test: ^1.24.0        # ❌ Debería estar en dev_dependencies
  flutter_test:        # ❌ Debería estar en dev_dependencies
    sdk: flutter

# ✅ BIEN
dependencies:
  flutter:
    sdk: flutter
  http: ^1.1.0
  provider: ^6.0.0

dev_dependencies:
  flutter_test:        # ✅ Correcto
    sdk: flutter
  mockito: ^5.4.0      # ✅ Correcto
  test: ^1.24.0        # ✅ Correcto
  build_runner: ^2.4.0 # ✅ Correcto
```

**Búsqueda lexical:**
```bash
# Buscar paquetes de test en dependencies
grep -A 100 "^dependencies:" pubspec.yaml | grep -B 1 "^dev_dependencies:" | grep -E "(flutter_test|mockito|test|fake|mock_)"
```

**Criterio:**
- ⚠️ **Advertencia:** Paquetes de test en `dependencies`
- ✅ **Cumple:** Paquetes de test solo en `dev_dependencies`

**Severidad:** `MEDIUM`  
**Automatización:** 🟢 Alta (100%)

**Remediación:**

```yaml
# ✅ pubspec.yaml correcto
name: my_app
description: Production mobile app

dependencies:
  flutter:
    sdk: flutter
  # Solo dependencias de producción
  http: ^1.1.0
  provider: ^6.0.0
  flutter_secure_storage: ^9.0.0
  dio: ^5.4.0

dev_dependencies:
  flutter_test:
    sdk: flutter
  # Todas las dependencias de desarrollo y testing
  mockito: ^5.4.0
  build_runner: ^2.4.0
  flutter_lints: ^3.0.0
  test: ^1.24.0
  integration_test:
    sdk: flutter
```

---

## Check M10-C: Código de debugging sin condicionales

**ID:** `M10-C-UNCONDITIONAL-DEBUG`  
**Objetivo:** Detectar `print()` y `debugPrint()` sin verificación de `kDebugMode`.  
**Ámbito:** `lib/**.dart`

**Método de búsqueda:** Lexical search  
**Patterns:**

```dart
// PATRÓN 1: print() sin condicional
void fetchData() async {
  print('Fetching data...');  // ⚠️ Se ejecuta en producción
  final data = await api.getData();
  print('Data received: $data');  // ⚠️ Puede contener datos sensibles
}

// PATRÓN 2: debugPrint() sin condicional
void processPayment(Payment payment) {
  debugPrint('Processing: ${payment.toJson()}');  // ⚠️ Ejecuta en producción
}

// PATRÓN 3: Logging verbose
class ApiService {
  void request(String url) {
    print('→ GET $url');  // ⚠️ Sin condicional
    // ...
  }
}
```

**Búsqueda lexical:**
```bash
# print() sin kDebugMode
grep -rE "^\s*print\(" lib/ | grep -v "kDebugMode"

# debugPrint() sin kDebugMode
grep -r "debugPrint" lib/ | grep -v "kDebugMode"

# Logging frameworks sin nivel condicional
grep -rE "logger\.(debug|info|verbose)" lib/ | grep -v "kReleaseMode"
```

**Criterio:**
- ⚠️ **Advertencia:** `print()` o `debugPrint()` sin `kDebugMode`
- ✅ **Cumple:** Todo logging condicional o removido en release

**Severidad:** `LOW`  
**Automatización:** 🟢 Alta (95%)

**Remediación:**

```dart
// ✅ SOLUCIÓN 1: Wrapper condicional
import 'package:flutter/foundation.dart';

void log(String message) {
  if (kDebugMode) {
    print(message);
  }
}

// Uso
void fetchData() async {
  log('Fetching data...');  // ✅ Solo en debug
  final data = await api.getData();
  log('Data received');     // ✅ Solo en debug
}
```

```dart
// ✅ SOLUCIÓN 2: Usar paquete logger con configuración
import 'package:logger/logger.dart';
import 'package:flutter/foundation.dart';

final logger = Logger(
  level: kReleaseMode ? Level.error : Level.debug,  // ✅ Nivel según build mode
  printer: PrettyPrinter(
    methodCount: kDebugMode ? 2 : 0,  // ✅ Stack trace solo en debug
    errorMethodCount: 8,
    lineLength: 120,
    colors: true,
    printEmojis: true,
    printTime: true,
  ),
);

// Uso
void fetchData() async {
  logger.d('Fetching data...');  // ✅ No se muestra en release (Level.error)
  final data = await api.getData();
  logger.i('Data received');     // ✅ No se muestra en release
}
```

```dart
// ✅ SOLUCIÓN 3: Eliminar con ProGuard (Android)
// proguard-rules.pro
-assumenosideeffects class android.util.Log {
    public static *** d(...);
    public static *** v(...);
    public static *** i(...);
}

// Esto elimina todos los logs en el APK final
```

```dart
// ✅ SOLUCIÓN 4: Custom logger que sanitiza
import 'package:flutter/foundation.dart';

class SecureLogger {
  static void log(String message) {
    if (!kDebugMode) return;
    
    // ✅ Sanitizar antes de loggear
    final sanitized = _sanitize(message);
    print(sanitized);
  }
  
  static String _sanitize(String message) {
    // Remover tokens, passwords, etc
    return message
        .replaceAll(RegExp(r'token["\']?\s*:\s*["\'][^"\']+["\']', caseSensitive: false), 'token: ***')
        .replaceAll(RegExp(r'password["\']?\s*:\s*["\'][^"\']+["\']', caseSensitive: false), 'password: ***')
        .replaceAll(RegExp(r'Bearer\s+[^\s]+'), 'Bearer ***');
  }
}
```

---

## Resumen M10

| Check | Severidad | Automatización | Esfuerzo Fix |
|-------|-----------|----------------|--------------|
| M10-A | HIGH | 🟢 80% | Medio |
| M10-B | MEDIUM | 🟢 100% | Bajo |
| M10-C | LOW | 🟢 95% | Bajo |

**Total checks:** 3  
**Severidad crítica:** 0  
**Severidad alta:** 1  
**Severidad media:** 2  
**Severidad baja:** 1

---

**Última actualización:** 2025-11-12  
**Versión:** 1.0