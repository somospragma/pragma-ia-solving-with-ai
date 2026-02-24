# Failures — Capa de Dominio

`lib/core/error/failures.dart`

> **Principio clave:** los `Failure` **no almacenan `String message`**.
> Almacenan una `FailureMessageKey` que la UI resuelve con `AppLocalizations`.
> Ver `references/i18n_errors.md` para la implementacion completa de i18n.

```dart
import 'package:flutter/widgets.dart';
import 'failure_message_key.dart';

/// Jerarquia sellada de fallos del dominio.
/// Sin Strings hardcodeados — los mensajes se resuelven en la UI con i18n.
sealed class Failure {
  const Failure();

  /// Clave ARB para mensajes estandar.
  FailureMessageKey? get messageKey => null;

  /// Mensaje literal para casos dinamicos (validacion, reglas de negocio).
  String? get literalMessage => null;

  /// Resuelve el mensaje final traducido. Llamar SIEMPRE desde la UI.
  String localizedMessage(BuildContext context) =>
      messageKey?.resolve(context) ?? literalMessage ?? '';
}

// Red / API

final class NetworkFailure extends Failure {
  const NetworkFailure();
  @override FailureMessageKey get messageKey => FailureMessageKey.network;
}

final class ServerFailure extends Failure {
  const ServerFailure({this.key = FailureMessageKey.server});
  final FailureMessageKey key;
  @override FailureMessageKey get messageKey => key;
}

final class UnauthorizedFailure extends Failure {
  const UnauthorizedFailure();
  @override FailureMessageKey get messageKey => FailureMessageKey.unauthorized;
}

final class NotFoundFailure extends Failure {
  const NotFoundFailure();
  @override FailureMessageKey get messageKey => FailureMessageKey.notFound;
}

final class TimeoutFailure extends Failure {
  const TimeoutFailure();
  @override FailureMessageKey get messageKey => FailureMessageKey.timeout;
}

// Firebase

final class AuthFailure extends Failure {
  const AuthFailure({required this.authKey});
  final FailureMessageKey authKey;
  @override FailureMessageKey get messageKey => authKey;
}

final class FirestoreFailure extends Failure {
  const FirestoreFailure();
  @override FailureMessageKey get messageKey => FailureMessageKey.firestore;
}

final class StorageFailure extends Failure {
  const StorageFailure();
  @override FailureMessageKey get messageKey => FailureMessageKey.storage;
}

// Base de Datos Local

final class DatabaseFailure extends Failure {
  const DatabaseFailure({this.dbKey = FailureMessageKey.database});
  final FailureMessageKey dbKey;
  @override FailureMessageKey get messageKey => dbKey;
}

// Cache

final class CacheFailure extends Failure {
  const CacheFailure();
  @override FailureMessageKey get messageKey => FailureMessageKey.cache;
}

// Validacion / Negocio — mensaje dinamico, NO en ARB
// Excepcion justificada: estos mensajes los genera el dominio en runtime.

final class ValidationFailure extends Failure {
  const ValidationFailure({required this.message});
  final String message;
  @override String? get literalMessage => message;
}

final class BusinessRuleFailure extends Failure {
  const BusinessRuleFailure({required this.message});
  final String message;
  @override String? get literalMessage => message;
}

// Inesperado

final class UnexpectedFailure extends Failure {
  const UnexpectedFailure();
  @override FailureMessageKey get messageKey => FailureMessageKey.unexpected;
}
```

## Uso con pattern matching (Dart 3.3+)

```dart
// En UI — siempre usar localizedMessage(context)
void _handleFailure(Failure failure, BuildContext context) {
  switch (failure) {
    case NetworkFailure():
      _showOfflineBanner();
    case UnauthorizedFailure():
      _redirectToLogin();
    case ServerFailure() || TimeoutFailure():
      _showRetrySnackbar(failure.localizedMessage(context));
    case ValidationFailure(:final message):
      _showFieldError(message); // mensaje ya viene del dominio
    default:
      _showGenericError(failure.localizedMessage(context));
  }
}
```

## Extension helper para UI

```dart
extension FailureX on Failure {
  IconData get icon => switch (this) {
    NetworkFailure()      => Icons.wifi_off_rounded,
    UnauthorizedFailure() => Icons.lock_outline_rounded,
    TimeoutFailure()      => Icons.timer_off_outlined,
    ServerFailure()       => Icons.cloud_off_rounded,
    DatabaseFailure()     => Icons.storage_rounded,
    _                     => Icons.error_outline_rounded,
  };

  bool get isRetryable =>
      this is NetworkFailure ||
      this is ServerFailure  ||
      this is TimeoutFailure;
}
```
