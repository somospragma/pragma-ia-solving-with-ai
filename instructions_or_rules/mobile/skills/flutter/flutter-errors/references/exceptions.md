# Exceptions — Capa de Datos

`lib/core/error/exceptions.dart` y `lib/core/error/error_handler.dart`

---

## exceptions.dart

```dart
/// Excepciones tecnicas — solo viven en la capa de datos.
/// Nunca llegan a dominio ni a presentacion.
sealed class AppException implements Exception {
  const AppException({required this.message, this.cause});
  final String message;
  final Object? cause; // error original para debugging/logging
}

// Red

final class NetworkException extends AppException {
  const NetworkException({super.message = 'network_error', super.cause});
}

final class ServerException extends AppException {
  const ServerException({
    required this.statusCode,
    super.message = 'server_error',
    super.cause,
  });
  final int statusCode;
}

final class UnauthorizedException extends AppException {
  const UnauthorizedException({super.message = 'unauthorized', super.cause});
}

final class NotFoundException extends AppException {
  const NotFoundException({super.message = 'not_found', super.cause});
}

final class TimeoutException extends AppException {
  const TimeoutException({super.message = 'timeout', super.cause});
}

// Firebase

final class FirebaseAppException extends AppException {
  const FirebaseAppException({
    required this.code,
    required super.message,
    super.cause,
    required this.source,
  });
  final String code;
  final FirebaseSource source;
}

enum FirebaseSource { auth, firestore, storage, functions }

// ObjectBox

final class ObjectBoxException extends AppException {
  const ObjectBoxException({
    super.message = 'objectbox_error',
    super.cause,
    required this.operation,
  });
  final DbOperation operation;
}

// Drift (SQLite)

final class DriftException extends AppException {
  const DriftException({
    super.message = 'drift_error',
    super.cause,
    required this.operation,
    this.sqliteCode,
  });
  final DbOperation operation;
  final int? sqliteCode;
}

enum DbOperation { read, write, delete, query, transaction, migration }

// Cache

final class CacheException extends AppException {
  const CacheException({super.message = 'cache_error', super.cause});
}
```

---

## error_handler.dart — Mapper central Exception -> Failure

`lib/core/error/error_handler.dart`

```dart
import 'package:firebase_auth/firebase_auth.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/foundation.dart';

import 'exceptions.dart';
import 'failure_message_key.dart';
import 'failures.dart';

abstract final class ErrorHandler {
  /// Punto de entrada unico: convierte cualquier error/excepcion a Failure.
  /// Llamado desde datasources en el segundo argumento de TaskEither.tryCatch.
  static Failure map(Object error, [StackTrace? stackTrace]) {
    _logError(error, stackTrace);

    return switch (error) {
      NetworkException()      => const NetworkFailure(),
      TimeoutException()      => const TimeoutFailure(),
      UnauthorizedException() => const UnauthorizedFailure(),
      NotFoundException()     => const NotFoundFailure(),
      ServerException(:final statusCode) =>
          ServerFailure(key: _serverKey(statusCode)),
      FirebaseAppException(:final code, :final source) =>
          _mapFirebase(code, source),
      ObjectBoxException() =>
          const DatabaseFailure(),
      DriftException(:final sqliteCode) =>
          DatabaseFailure(dbKey: _driftKey(sqliteCode)),
      CacheException() =>
          const CacheFailure(),

      // Excepciones de Firebase sin wrapper propio (por si escapan)
      FirebaseAuthException(:final code) =>
          _mapFirebase(code, FirebaseSource.auth),
      FirebaseException(:final code, :final plugin) =>
          _mapFirebase(code, _pluginToSource(plugin)),

      _ => const UnexpectedFailure(),
    };
  }

  // Mapeo HTTP status code -> FailureMessageKey semantica
  static FailureMessageKey _serverKey(int code) => switch (code) {
    // 4XX - Errores del cliente
    400 => FailureMessageKey.serverBadRequest,
    401 => FailureMessageKey.serverUnauthorized,
    403 => FailureMessageKey.serverForbidden,
    404 => FailureMessageKey.serverNotFound,
    405 => FailureMessageKey.serverMethodNotAllowed,
    408 => FailureMessageKey.serverRequestTimeout,
    409 => FailureMessageKey.serverConflict,
    410 => FailureMessageKey.serverGone,
    413 => FailureMessageKey.serverPayloadTooLarge,
    415 => FailureMessageKey.serverUnsupportedMediaType,
    422 => FailureMessageKey.serverUnprocessable,
    429 => FailureMessageKey.serverTooManyRequests,
    // 5XX - Errores del servidor
    500 => FailureMessageKey.serverInternalError,
    501 => FailureMessageKey.serverNotImplemented,
    502 => FailureMessageKey.serverBadGateway,
    503 => FailureMessageKey.serverUnavailable,
    504 => FailureMessageKey.serverGatewayTimeout,
    _   => FailureMessageKey.server,
  };

  // Mapeo SQLite error code -> FailureMessageKey para Drift
  static FailureMessageKey _driftKey(int? sqliteCode) => switch (sqliteCode) {
    5  => FailureMessageKey.databaseBusy,
    8  => FailureMessageKey.databaseReadOnly,
    19 => FailureMessageKey.databaseConstraint,
    _  => FailureMessageKey.database,
  };

  static Failure _mapFirebase(String code, FirebaseSource source) =>
      switch (source) {
        FirebaseSource.auth      => AuthFailure(authKey: _authKey(code)),
        FirebaseSource.firestore => const FirestoreFailure(),
        FirebaseSource.storage   => const StorageFailure(),
        FirebaseSource.functions => const ServerFailure(),
      };

  // Firebase Auth error codes -> FailureMessageKey de auth
  static FailureMessageKey _authKey(String code) => switch (code) {
    'user-not-found'          => FailureMessageKey.authUserNotFound,
    'wrong-password'          => FailureMessageKey.authWrongPassword,
    'email-already-in-use'    => FailureMessageKey.authEmailInUse,
    'user-disabled'           => FailureMessageKey.authUserDisabled,
    'too-many-requests'       => FailureMessageKey.authTooManyRequests,
    'network-request-failed'  => FailureMessageKey.network,
    _                         => FailureMessageKey.authGeneric,
  };

  static FirebaseSource _pluginToSource(String plugin) => switch (plugin) {
    'firebase_auth'    => FirebaseSource.auth,
    'cloud_firestore'  => FirebaseSource.firestore,
    'firebase_storage' => FirebaseSource.storage,
    _                  => FirebaseSource.functions,
  };

  static void _logError(Object error, StackTrace? stackTrace) {
    // Conectar con Crashlytics, Sentry, etc.
    // FirebaseCrashlytics.instance.recordError(error, stackTrace);
    debugPrint('[ErrorHandler] $error\n$stackTrace');
  }
}
```
