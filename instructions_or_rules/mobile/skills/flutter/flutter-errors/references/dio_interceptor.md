# Dio Error Interceptor

`lib/core/network/dio_error_interceptor.dart`

---

## Interceptor completo

```dart
import 'package:dio/dio.dart';
import 'package:your_app/core/error/exceptions.dart';

/// Convierte errores de Dio en AppException antes de que lleguen al datasource.
/// Registrar en la instancia de Dio: dio.interceptors.add(DioErrorInterceptor())
class DioErrorInterceptor extends Interceptor {
  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    final exception = _mapDioException(err);
    // Reemplaza el error con nuestra excepción tipada
    handler.reject(
      DioException(
        requestOptions: err.requestOptions,
        error: exception,
        response: err.response,
        type: err.type,
      ),
    );
  }

  AppException _mapDioException(DioException e) => switch (e.type) {
    DioExceptionType.connectionTimeout ||
    DioExceptionType.sendTimeout    ||
    DioExceptionType.receiveTimeout => TimeoutException(cause: e),

    DioExceptionType.connectionError => NetworkException(cause: e),

    DioExceptionType.badResponse => _mapStatusCode(
      e.response?.statusCode ?? 0,
      e,
    ),

    DioExceptionType.cancel => NetworkException(
      message: 'Solicitud cancelada',
      cause: e,
    ),

    _ => NetworkException(cause: e),
  };

  AppException _mapStatusCode(int code, DioException e) => switch (code) {
    401 => UnauthorizedException(cause: e),
    403 => UnauthorizedException(
        message: 'No tienes permiso para esta acción',
        cause: e,
      ),
    404 => NotFoundException(cause: e),
    >= 500 => ServerException(
        statusCode: code,
        message: 'Error del servidor ($code)',
        cause: e,
      ),
    _ => ServerException(
        statusCode: code,
        cause: e,
      ),
  };
}
```

---

## Configuración del cliente Dio

```dart
// lib/core/network/dio_client.dart

import 'package:dio/dio.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'dio_client.g.dart';

@riverpod
Dio dioClient(DioClientRef ref) {
  final dio = Dio(
    BaseOptions(
      baseUrl: AppConfig.baseUrl,
      connectTimeout: const Duration(seconds: 10),
      receiveTimeout: const Duration(seconds: 15),
      sendTimeout: const Duration(seconds: 10),
      headers: {'Content-Type': 'application/json'},
    ),
  );

  dio.interceptors.addAll([
    DioErrorInterceptor(),
    AuthInterceptor(ref),          // Agrega Bearer token
    if (kDebugMode) LogInterceptor( // Solo en debug
      requestBody: true,
      responseBody: true,
    ),
  ]);

  return dio;
}
```

---

## Datasource usando el interceptor + TaskEither

```dart
// features/products/data/datasources/products_remote_datasource.dart

class ProductsRemoteDatasource {
  const ProductsRemoteDatasource({required Dio dio}) : _dio = dio;

  final Dio _dio;

  TaskEither<Failure, List<Product>> getProducts() =>
      TaskEither.tryCatch(
        () async {
          final response = await _dio.get<List<dynamic>>('/products');
          return (response.data ?? [])
              .map((e) => ProductDto.fromJson(e as Map<String, dynamic>))
              .map((dto) => dto.toDomain())
              .toList();
        },
        // El interceptor ya convirtió DioException en AppException
        // ErrorHandler.map maneja ambos tipos
        (error, stackTrace) => ErrorHandler.map(error, stackTrace),
      );

  TaskEither<Failure, Product> getProductById(String id) =>
      TaskEither.tryCatch(
        () async {
          final response = await _dio.get<Map<String, dynamic>>('/products/$id');
          return ProductDto.fromJson(response.data!).toDomain();
        },
        ErrorHandler.map,
      );

  TaskEither<Failure, Product> createProduct(CreateProductParams params) =>
      TaskEither.tryCatch(
        () async {
          final response = await _dio.post<Map<String, dynamic>>(
            '/products',
            data: params.toJson(),
          );
          return ProductDto.fromJson(response.data!).toDomain();
        },
        ErrorHandler.map,
      );
}
```

---

## Auth Interceptor (manejo de token expirado + retry)

```dart
class AuthInterceptor extends Interceptor {
  AuthInterceptor(this._ref);
  final Ref _ref;

  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    final token = _ref.read(authTokenProvider);
    if (token != null) {
      options.headers['Authorization'] = 'Bearer $token';
    }
    handler.next(options);
  }

  @override
  Future<void> onError(
    DioException err,
    ErrorInterceptorHandler handler,
  ) async {
    // Intentar refresh si el error es 401
    if (err.response?.statusCode == 401) {
      try {
        final newToken = await _ref.read(refreshTokenUseCaseProvider).call().run();
        newToken.fold(
          (_) => handler.next(err), // refresh falló, dejar pasar el error
          (token) async {
            // Reintentar la request original con nuevo token
            final opts = err.requestOptions;
            opts.headers['Authorization'] = 'Bearer $token';
            final response = await _ref.read(dioClientProvider).fetch(opts);
            handler.resolve(response);
          },
        );
      } catch (_) {
        handler.next(err);
      }
    } else {
      handler.next(err);
    }
  }
}
```
