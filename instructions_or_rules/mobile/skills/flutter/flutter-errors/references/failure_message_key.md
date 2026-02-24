# FailureMessageKey — Enum de Claves Semánticas i18n

`lib/core/error/failure_message_key.dart`

---

## Tabla de contenidos

1. [El problema](#el-problema)
2. [FailureMessageKey — enum completo](#failuremessagekey--enum-completo)
3. [Failures rediseñados — sin Strings hardcodeados](#failures-rediseñados--sin-strings-hardcodeados)
4. [FailureView — resolución en la UI](#failureview--resolución-en-la-ui)

---

## El problema

Los `Failure` viven en la **capa de dominio**, que no tiene `BuildContext`.  
Los mensajes traducidos solo existen en la **capa de presentación**, que sí tiene `BuildContext`.

**Solución:** los `Failure` NO almacenan `String message` hardcodeado.  
En su lugar almacenan una **clave semántica** (`FailureMessageKey`) que la UI resuelve con `AppLocalizations`.

```
Failure (dominio)          →  clave semántica (enum)
ErrorHandler (datos)       →  asigna la clave correcta
FailureView (presentación) →  clave.resolve(context) → String traducido
```

---

## FailureMessageKey — enum completo

```dart
import 'package:flutter/widgets.dart';
import 'package:your_app/core/l10n/generated/app_localizations.dart';

/// Clave semántica que apunta a una entrada del ARB.
/// Desacopla el dominio del idioma — la UI resuelve el texto.
enum FailureMessageKey {
  network,
  timeout,
  unauthorized,
  notFound,
  server,
  // 4XX - Errores del cliente
  serverBadRequest,
  serverUnauthorized,
  serverForbidden,
  serverNotFound,
  serverMethodNotAllowed,
  serverRequestTimeout,
  serverConflict,
  serverGone,
  serverPayloadTooLarge,
  serverUnsupportedMediaType,
  serverUnprocessable,
  serverTooManyRequests,
  // 5XX - Errores del servidor
  serverInternalError,
  serverNotImplemented,
  serverBadGateway,
  serverUnavailable,
  serverGatewayTimeout,
  authUserNotFound,
  authWrongPassword,
  authEmailInUse,
  authUserDisabled,
  authTooManyRequests,
  authGeneric,
  firestore,
  storage,
  database,
  databaseBusy,
  databaseReadOnly,
  databaseConstraint,
  cache,
  unexpected;

  /// Resuelve la clave al String traducido según el locale activo.
  String resolve(BuildContext context) {
    final l = AppLocalizations.of(context);
    return switch (this) {
      network                    => l.errorNetwork,
      timeout                    => l.errorTimeout,
      unauthorized               => l.errorUnauthorized,
      notFound                   => l.errorNotFound,
      server                     => l.errorServer,
      serverBadRequest           => l.errorServerBadRequest,
      serverUnauthorized         => l.errorServerUnauthorized,
      serverForbidden            => l.errorServerForbidden,
      serverNotFound             => l.errorServerNotFound,
      serverMethodNotAllowed     => l.errorServerMethodNotAllowed,
      serverRequestTimeout       => l.errorServerRequestTimeout,
      serverConflict             => l.errorServerConflict,
      serverGone                 => l.errorServerGone,
      serverPayloadTooLarge      => l.errorServerPayloadTooLarge,
      serverUnsupportedMediaType => l.errorServerUnsupportedMediaType,
      serverUnprocessable        => l.errorServerUnprocessable,
      serverTooManyRequests      => l.errorServerTooManyRequests,
      serverInternalError        => l.errorServerInternalError,
      serverNotImplemented       => l.errorServerNotImplemented,
      serverBadGateway           => l.errorServerBadGateway,
      serverUnavailable          => l.errorServerUnavailable,
      serverGatewayTimeout       => l.errorServerGatewayTimeout,
      authUserNotFound           => l.errorAuthUserNotFound,
      authWrongPassword          => l.errorAuthWrongPassword,
      authEmailInUse             => l.errorAuthEmailInUse,
      authUserDisabled           => l.errorAuthUserDisabled,
      authTooManyRequests        => l.errorAuthTooManyRequests,
      authGeneric                => l.errorAuthGeneric,
      firestore                  => l.errorFirestore,
      storage                    => l.errorStorage,
      database                   => l.errorDatabase,
      databaseBusy               => l.errorDatabaseBusy,
      databaseReadOnly           => l.errorDatabaseReadOnly,
      databaseConstraint         => l.errorDatabaseConstraint,
      cache                      => l.errorCache,
      unexpected                 => l.errorUnexpected,
    };
  }
}
```

---

## Failures rediseñados — sin Strings hardcodeados

`lib/core/error/failures.dart`

```dart
import 'failure_message_key.dart';

/// Los Failure ya NO tienen String message — tienen una clave i18n.
/// Excepción: ValidationFailure y BusinessRuleFailure, cuyo mensaje
/// viene del dominio (ya traducido o generado dinámicamente).
sealed class Failure {
  const Failure();

  /// Clave para mensajes estándar mapeados en el ARB.
  FailureMessageKey? get messageKey => null;

  /// Mensaje literal para casos dinámicos (validación, reglas de negocio).
  /// En estos casos messageKey es null.
  String? get literalMessage => null;

  /// Resuelve el mensaje final con el contexto para i18n.
  /// Usar SIEMPRE este método en la UI.
  String localizedMessage(BuildContext context) =>
      messageKey?.resolve(context) ?? literalMessage ?? '';
}

// ─── Red / API ────────────────────────────────────────────────────────────────

final class NetworkFailure extends Failure {
  const NetworkFailure();
  @override
  FailureMessageKey get messageKey => FailureMessageKey.network;
}

final class ServerFailure extends Failure {
  const ServerFailure({this.key = FailureMessageKey.server});
  final FailureMessageKey key;
  @override
  FailureMessageKey get messageKey => key;
}

final class UnauthorizedFailure extends Failure {
  const UnauthorizedFailure();
  @override
  FailureMessageKey get messageKey => FailureMessageKey.unauthorized;
}

final class NotFoundFailure extends Failure {
  const NotFoundFailure();
  @override
  FailureMessageKey get messageKey => FailureMessageKey.notFound;
}

final class TimeoutFailure extends Failure {
  const TimeoutFailure();
  @override
  FailureMessageKey get messageKey => FailureMessageKey.timeout;
}

// ─── Firebase ─────────────────────────────────────────────────────────────────

final class AuthFailure extends Failure {
  const AuthFailure({required this.authKey});
  final FailureMessageKey authKey;
  @override
  FailureMessageKey get messageKey => authKey;
}

final class FirestoreFailure extends Failure {
  const FirestoreFailure();
  @override
  FailureMessageKey get messageKey => FailureMessageKey.firestore;
}

final class StorageFailure extends Failure {
  const StorageFailure();
  @override
  FailureMessageKey get messageKey => FailureMessageKey.storage;
}

// ─── Base de Datos Local ──────────────────────────────────────────────────────

final class DatabaseFailure extends Failure {
  const DatabaseFailure({this.dbKey = FailureMessageKey.database});
  final FailureMessageKey dbKey;
  @override
  FailureMessageKey get messageKey => dbKey;
}

// ─── Caché ────────────────────────────────────────────────────────────────────

final class CacheFailure extends Failure {
  const CacheFailure();
  @override
  FailureMessageKey get messageKey => FailureMessageKey.cache;
}

// ─── Validación / Negocio — mensaje dinámico, NO en ARB ──────────────────────
//
// Estos mensajes los genera el dominio en tiempo de ejecución.
// Para traducciones estáticas conocidas, agrégalas al ARB y usa messageKey.

final class ValidationFailure extends Failure {
  /// [message] debe venir ya en el idioma correcto desde el dominio,
  /// o resolverse con AppLocalizations en el use case si hay contexto.
  const ValidationFailure({required this.message});
  final String message;
  @override
  String? get literalMessage => message;
}

final class BusinessRuleFailure extends Failure {
  const BusinessRuleFailure({required this.message});
  final String message;
  @override
  String? get literalMessage => message;
}

// ─── Inesperado ───────────────────────────────────────────────────────────────

final class UnexpectedFailure extends Failure {
  const UnexpectedFailure();
  @override
  FailureMessageKey get messageKey => FailureMessageKey.unexpected;
}
```

---

## FailureView — resolución en la UI

```dart
// lib/core/widgets/failure_view.dart

class FailureView extends StatelessWidget {
  const FailureView({super.key, required this.failure, this.onRetry});

  final Failure failure;
  final VoidCallback? onRetry;

  @override
  Widget build(BuildContext context) {
    final l = AppLocalizations.of(context);

    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(failure.icon, size: 48, color: Theme.of(context).colorScheme.error),
            const SizedBox(height: 16),
            Text(
              failure.localizedMessage(context), // ← resolución i18n aquí
              textAlign: TextAlign.center,
              style: Theme.of(context).textTheme.bodyLarge,
            ),
            if (onRetry != null && failure.isRetryable) ...[
              const SizedBox(height: 16),
              FilledButton.tonal(
                onPressed: onRetry,
                child: Text(l.retryButton), // ← también traducido
              ),
            ],
          ],
        ),
      ),
    );
  }
}
```

---

## Checklist

- [ ] `Failure` usa `messageKey` — ninguno tiene `String message` hardcodeado
- [ ] `ValidationFailure` y `BusinessRuleFailure` son la única excepción
- [ ] La UI **siempre** llama `failure.localizedMessage(context)`
- [ ] Cada `FailureMessageKey` tiene su entrada correspondiente en los ARB
