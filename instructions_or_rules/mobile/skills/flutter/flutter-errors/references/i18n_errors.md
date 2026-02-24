# Internacionalización de Mensajes de Error — ARB + Flutter i18n

Stack: `flutter_localizations` · `intl` · archivos `.arb` · Dart 3.3+

---

## Tabla de contenidos

1. [Estructura de archivos](#1-estructura-de-archivos)
2. [Configuración l10n.yaml](#2-configuración-l10nyaml)
3. [Archivos ARB — claves de error](#3-archivos-arb--claves-de-error)
4. [MaterialApp — configuración](#4-materialapp--configuración-de-localizations)
5. [Checklist i18n](#5-checklist-i18n-de-errores)

> Para el enum `FailureMessageKey`, los `Failure` rediseñados y el `FailureView`, ver `references/failure_message_key.md`.

---

## 1. Estructura de archivos

```
lib/
├── core/
│   └── error/
│       ├── failures.dart              ← Failure con FailureMessageKey (sin Strings)
│       └── failure_message_key.dart   ← Enum de claves i18n
│
└── l10n/
    ├── app_en.arb                     ← Inglés (idioma base)
    ├── app_es.arb                     ← Español
    └── l10n.yaml                      ← Configuración del generador

# Generado automáticamente por flutter gen-l10n:
└── .dart_tool/flutter_gen/gen_l10n/
    └── app_localizations.dart
```

---

## 2. Configuración l10n.yaml

```yaml
# l10n.yaml — en la raíz del proyecto

arb-dir: lib/l10n
template-arb-file: app_en.arb
output-localization-file: app_localizations.dart
output-class: AppLocalizations
nullable-getter: false
synthetic-package: false          # genera en lib/, no en .dart_tool
output-dir: lib/core/l10n/generated
```

---

## 3. Archivos ARB — claves de error

### app_en.arb (base)

```json
{
  "@@locale": "en",

  "errorNetwork": "No internet connection.",
  "@errorNetwork": { "description": "Shown when the device has no network access" },

  "errorTimeout": "The request took too long. Check your connection.",
  "@errorTimeout": { "description": "Shown on connection or read timeout" },

  "errorUnauthorized": "Session expired. Please sign in again.",
  "@errorUnauthorized": { "description": "401 / invalid token" },

  "errorNotFound": "The requested resource does not exist.",
  "@errorNotFound": { "description": "404 responses" },

  "errorServer": "Server error. Please try again later.",
  "@errorServer": { "description": "5xx responses without specific mapping" },

  "errorServerBadRequest": "Invalid request.",
  "@errorServerBadRequest": { "description": "400 Bad Request" },

  "errorServerUnauthorized": "Session expired. Please sign in again.",
  "@errorServerUnauthorized": { "description": "401 Unauthorized" },

  "errorServerForbidden": "You don't have permission for this action.",
  "@errorServerForbidden": { "description": "403 Forbidden" },

  "errorServerNotFound": "The requested resource was not found.",
  "@errorServerNotFound": { "description": "404 Not Found" },

  "errorServerMethodNotAllowed": "This action is not allowed.",
  "@errorServerMethodNotAllowed": { "description": "405 Method Not Allowed" },

  "errorServerRequestTimeout": "The server took too long to respond.",
  "@errorServerRequestTimeout": { "description": "408 Request Timeout" },

  "errorServerConflict": "Conflict with the current state.",
  "@errorServerConflict": { "description": "409 Conflict" },

  "errorServerGone": "This resource is no longer available.",
  "@errorServerGone": { "description": "410 Gone" },

  "errorServerPayloadTooLarge": "The file or data is too large.",
  "@errorServerPayloadTooLarge": { "description": "413 Payload Too Large" },

  "errorServerUnsupportedMediaType": "Unsupported file format.",
  "@errorServerUnsupportedMediaType": { "description": "415 Unsupported Media Type" },

  "errorServerUnprocessable": "The submitted data is not valid.",
  "@errorServerUnprocessable": { "description": "422 Unprocessable Entity" },

  "errorServerTooManyRequests": "Too many requests. Please wait a moment.",
  "@errorServerTooManyRequests": { "description": "429 Too Many Requests" },

  "errorServerInternalError": "Internal server error. Please try again later.",
  "@errorServerInternalError": { "description": "500 Internal Server Error" },

  "errorServerNotImplemented": "This feature is not yet available.",
  "@errorServerNotImplemented": { "description": "501 Not Implemented" },

  "errorServerBadGateway": "Server communication error. Please try again.",
  "@errorServerBadGateway": { "description": "502 Bad Gateway" },

  "errorServerUnavailable": "Service unavailable. Please try again later.",
  "@errorServerUnavailable": { "description": "503 Service Unavailable" },

  "errorServerGatewayTimeout": "Server response timeout. Please try again.",
  "@errorServerGatewayTimeout": { "description": "504 Gateway Timeout" },

  "errorAuthUserNotFound": "No account found with that email.",
  "@errorAuthUserNotFound": {},

  "errorAuthWrongPassword": "Incorrect password.",
  "@errorAuthWrongPassword": {},

  "errorAuthEmailInUse": "This email is already registered.",
  "@errorAuthEmailInUse": {},

  "errorAuthUserDisabled": "This account has been disabled.",
  "@errorAuthUserDisabled": {},

  "errorAuthTooManyRequests": "Too many attempts. Please try again later.",
  "@errorAuthTooManyRequests": {},

  "errorAuthGeneric": "Authentication error. Please try again.",
  "@errorAuthGeneric": {},

  "errorFirestore": "Error accessing data.",
  "@errorFirestore": {},

  "errorStorage": "Error processing the file.",
  "@errorStorage": {},

  "errorDatabase": "Error accessing local database.",
  "@errorDatabase": {},

  "errorDatabaseBusy": "Database is busy. Please try again.",
  "@errorDatabaseBusy": {},

  "errorDatabaseReadOnly": "Write operation not permitted.",
  "@errorDatabaseReadOnly": {},

  "errorDatabaseConstraint": "Data integrity constraint violation.",
  "@errorDatabaseConstraint": {},

  "errorCache": "Error reading stored data.",
  "@errorCache": {},

  "errorValidation": "{message}",
  "@errorValidation": {
    "description": "Passes through a domain-specific validation message already translated",
    "placeholders": { "message": { "type": "String" } }
  },

  "errorUnexpected": "An unexpected error occurred.",
  "@errorUnexpected": {},

  "retryButton": "Retry",
  "@retryButton": {}
}
```

### app_es.arb

```json
{
  "@@locale": "es",

  "errorNetwork": "Sin conexión a internet.",
  "errorTimeout": "La solicitud tardó demasiado. Verifica tu conexión.",
  "errorUnauthorized": "Sesión expirada. Inicia sesión nuevamente.",
  "errorNotFound": "El recurso solicitado no existe.",
  "errorServer": "Error en el servidor. Intenta más tarde.",
  "errorServerBadRequest": "Solicitud inválida.",
  "errorServerUnauthorized": "Sesión expirada. Inicia sesión nuevamente.",
  "errorServerForbidden": "No tienes permiso para esta acción.",
  "errorServerNotFound": "El recurso solicitado no fue encontrado.",
  "errorServerMethodNotAllowed": "Esta acción no está permitida.",
  "errorServerRequestTimeout": "El servidor tardó demasiado en responder.",
  "errorServerConflict": "Conflicto con el estado actual.",
  "errorServerGone": "Este recurso ya no está disponible.",
  "errorServerPayloadTooLarge": "El archivo o datos son demasiado grandes.",
  "errorServerUnsupportedMediaType": "Formato de archivo no soportado.",
  "errorServerUnprocessable": "Los datos enviados no son válidos.",
  "errorServerTooManyRequests": "Demasiadas solicitudes. Espera un momento.",
  "errorServerInternalError": "Error interno del servidor. Intenta más tarde.",
  "errorServerNotImplemented": "Esta función aún no está disponible.",
  "errorServerBadGateway": "Error de comunicación con el servidor. Intenta de nuevo.",
  "errorServerUnavailable": "Servicio no disponible. Intenta más tarde.",
  "errorServerGatewayTimeout": "Tiempo de espera del servidor agotado. Intenta de nuevo.",
  "errorAuthUserNotFound": "No existe una cuenta con ese correo.",
  "errorAuthWrongPassword": "Contraseña incorrecta.",
  "errorAuthEmailInUse": "Este correo ya está registrado.",
  "errorAuthUserDisabled": "Esta cuenta ha sido deshabilitada.",
  "errorAuthTooManyRequests": "Demasiados intentos. Intenta más tarde.",
  "errorAuthGeneric": "Error de autenticación. Intenta de nuevo.",
  "errorFirestore": "Error al acceder a los datos.",
  "errorStorage": "Error al procesar el archivo.",
  "errorDatabase": "Error al acceder a la base de datos local.",
  "errorDatabaseBusy": "Base de datos ocupada. Intenta más tarde.",
  "errorDatabaseReadOnly": "Operación de escritura no permitida.",
  "errorDatabaseConstraint": "Violación de restricción de integridad.",
  "errorCache": "Error al leer datos almacenados.",
  "errorValidation": "{message}",
  "errorUnexpected": "Ocurrió un error inesperado.",
  "retryButton": "Reintentar"
}
```

---

## 4. MaterialApp — configuración de localizations

```dart
// main.dart o app.dart

MaterialApp.router(
  // ...
  localizationsDelegates: AppLocalizations.localizationsDelegates,
  supportedLocales: AppLocalizations.supportedLocales,
  // Opcional: forzar locale en desarrollo
  // locale: const Locale('es'),
)
```

---

## 5. Checklist i18n de errores

- [ ] Cada nueva entrada en ARB tiene su `@clave` con `description`
- [ ] `app_en.arb` es el archivo **template** — se agrega primero en inglés, luego en español
- [ ] Ejecutar `flutter gen-l10n` tras cada cambio en los ARB
- [ ] El botón "Reintentar" usa `l.retryButton` — no un String literal
- [ ] Todas las claves están presentes en **ambos** archivos ARB antes de hacer build
