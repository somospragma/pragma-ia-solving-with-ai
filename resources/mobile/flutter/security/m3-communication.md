# M3. Comunicación Insegura

Esta categoría cubre problemas de seguridad en la comunicación de red, incluyendo HTTP sin TLS, validación de certificados y WebViews inseguros.

---

## Check M3-A: Tráfico HTTP sin TLS

**ID:** `M3-A-HTTP-PLAINTEXT`  
**Objetivo:** Detectar endpoints HTTP (no HTTPS) y bypass de validación de certificados.  
**Ámbito:** `lib/**.dart`, `AndroidManifest.xml`, `Info.plist`

**Método de búsqueda:** Lexical search  
**Patterns en código Dart:**

```dart
// PATRÓN 1: URLs HTTP
final response = await http.get(Uri.parse('http://api.example.com'));  // ⚠️ INSEGURO

// PATRÓN 2: Bypass de certificados SSL
class MyHttpOverrides extends HttpOverrides {
  @override
  HttpClient createHttpClient(SecurityContext? context) {
    return super.createHttpClient(context)
      ..badCertificateCallback = (X509Certificate cert, String host, int port) => true;  // ❌ PELIGRO
  }
}

// PATRÓN 3: Dio sin validación
final dio = Dio();
(dio.httpClientAdapter as DefaultHttpClientAdapter).onHttpClientCreate = (client) {
  client.badCertificateCallback = (cert, host, port) => true;  // ❌ PELIGRO
};
```

**Búsqueda lexical:**
```regex
['"]http://(?!localhost|127\.0\.0\.1)
badCertificateCallback\s*=\s*\([^)]*\)\s*=>\s*true
onHttpClientCreate.*badCertificateCallback
```

**Android - Cleartext Traffic:**
```xml
<!-- AndroidManifest.xml -->
<application
    android:usesCleartextTraffic="true">  <!-- ⚠️ PELIGRO -->
```

**iOS - ATS Bypass:**
```xml
<key>NSAllowsArbitraryLoads</key>
<true/>  <!-- ⚠️ PELIGRO -->
```

**Criterio:**
- ❌ **Falla:** URLs `http://` (excepto localhost en debug)
- ❌ **Falla:** `badCertificateCallback` retornando `true`
- ❌ **Falla:** `usesCleartextTraffic="true"` en Android
- ✅ **Cumple:** Solo HTTPS + validación de certificados habilitada

**Severidad:** `CRITICAL`  
**Automatización:** 🟢 Alta (95%)

**Remediación:**

```dart
// ✅ SOLUCIÓN 1: Usar HTTPS siempre
final response = await http.get(Uri.parse('https://api.example.com'));  // ✅ SEGURO

// ✅ SOLUCIÓN 2: NUNCA deshabilitar validación en producción
import 'package:flutter/foundation.dart';

class MyHttpOverrides extends HttpOverrides {
  @override
  HttpClient createHttpClient(SecurityContext? context) {
    return super.createHttpClient(context)
      ..badCertificateCallback = (cert, host, port) {
        if (kDebugMode && host == 'dev.example.com') {
          return true;  // Solo en debug y solo para dev server
        }
        return false;  // ✅ Validar en producción
      };
  }
}
```

```xml
<!-- AndroidManifest.xml -->
<application
    android:usesCleartextTraffic="false">  <!-- ✅ SEGURO -->
    
<!-- O mejor, usar Network Security Config -->
<application
    android:networkSecurityConfig="@xml/network_security_config">
```

```xml
<!-- res/xml/network_security_config.xml -->
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <base-config cleartextTrafficPermitted="false">
        <trust-anchors>
            <certificates src="system"/>
        </trust-anchors>
    </base-config>
    
    <!-- Solo para debug build -->
    <debug-overrides>
        <trust-anchors>
            <certificates src="user"/>
        </trust-anchors>
    </debug-overrides>
</network-security-config>
```

---

## Check M3-B: WebView con configuración insegura

**ID:** `M3-B-INSECURE-WEBVIEW`  
**Objetivo:** Detectar WebViews con JavaScript habilitado sin validación de URLs.  
**Ámbito:** `lib/**.dart`

**Método de búsqueda:** Lexical + Semantic search  
**Patterns inseguros:**

```dart
// PATRÓN 1: JavaScript habilitado sin restricciones
WebView(
  javascriptMode: JavascriptMode.unrestricted,  // ⚠️ PELIGRO si carga URLs no confiables
  initialUrl: userProvidedUrl,  // ❌ URL sin validar
)

// PATRÓN 2: Sin navigationDelegate
WebView(
  javascriptMode: JavascriptMode.unrestricted,
  // Sin control de navegación ❌
)

// PATRÓN 3: JavascriptChannels sin validación
WebView(
  javascriptMode: JavascriptMode.unrestricted,
  javascriptChannels: Set.from([
    JavascriptChannel(
      name: 'MessageHandler',
      onMessageReceived: (JavascriptMessage message) {
        eval(message.message);  // ❌❌ PELIGRO EXTREMO
      },
    ),
  ]),
)
```

**Búsqueda lexical:**
```regex
javascriptMode:\s*JavascriptMode\.unrestricted(?!.*navigationDelegate)
WebView\((?!.*navigationDelegate)
javascriptChannels:.*onMessageReceived.*(?!.*validate)
```

**Criterio:**
- ❌ **Falla:** JavaScript habilitado + URLs no validadas
- ❌ **Falla:** `JavascriptChannels` sin sanitización de inputs
- ✅ **Cumple:** JavaScript deshabilitado O validación estricta de URLs

**Severidad:** `HIGH`  
**Automatización:** 🟢 Alta (80%)

**Remediación:**

```dart
// ✅ SOLUCIÓN 1: Deshabilitar JavaScript si no es necesario
WebView(
  javascriptMode: JavascriptMode.disabled,  // ✅ Más seguro
  initialUrl: 'https://trusted-domain.com/content',
)

// ✅ SOLUCIÓN 2: JavaScript con validación estricta
WebView(
  javascriptMode: JavascriptMode.unrestricted,
  initialUrl: 'https://trusted-domain.com',
  
  // ✅ Validar todas las navegaciones
  navigationDelegate: (NavigationRequest request) {
    final uri = Uri.parse(request.url);
    
    // Whitelist de dominios permitidos
    const allowedDomains = ['trusted-domain.com', 'api.trusted-domain.com'];
    
    if (!allowedDomains.contains(uri.host)) {
      print('Blocked navigation to: ${request.url}');
      return NavigationDecision.prevent;
    }
    
    // Solo HTTPS
    if (uri.scheme != 'https') {
      return NavigationDecision.prevent;
    }
    
    return NavigationDecision.navigate;
  },
  
  // ✅ Sanitizar mensajes de JavaScript
  javascriptChannels: Set.from([
    JavascriptChannel(
      name: 'MessageHandler',
      onMessageReceived: (JavascriptMessage message) {
        final sanitizedMessage = _sanitizeInput(message.message);
        _handleMessage(sanitizedMessage);
      },
    ),
  ]),
)

String _sanitizeInput(String input) {
  // Remover caracteres peligrosos
  return input
      .replaceAll(RegExp(r'<script.*?>.*?</script>', caseSensitive: false), '')
      .replaceAll(RegExp(r'[<>"\']'), '');
}
```

---

## Resumen M3

| Check | Severidad | Automatización | Esfuerzo Fix |
|-------|-----------|----------------|--------------|
| M3-A | CRITICAL | 🟢 95% | Alto |
| M3-B | HIGH | 🟢 80% | Medio |

**Total checks:** 2  
**Severidad crítica:** 1  
**Severidad alta:** 1  
**Severidad media:** 0  
**Severidad baja:** 0

---

**Última actualización:** 2025-11-12  
**Versión:** 1.0