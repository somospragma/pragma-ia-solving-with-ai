# Unit Testing Reference

Guía detallada para pruebas unitarias en Flutter. Unit tests validan la lógica de negocio aislada sin dependencias del framework.

## Configuración Inicial

### Paquetes Requeridos

```yaml
dev_dependencies:
  test: ^1.24.0
  mocktail: ^1.0.0
  bloc_test: ^9.1.0
```

### Estructura de Proyecto

```
test/
├── fixtures/
│   ├── test_data.dart
│   └── fixture_reader.dart
├── domain/
│   ├── usecases/
│   │   └── get_user_usecase_test.dart
│   └── entities/
├── data/
│   ├── repositories/
│   │   └── user_repository_impl_test.dart
│   ├── datasources/
│   │   ├── user_remote_datasource_test.dart
│   │   └── user_local_datasource_test.dart
│   └── models/
│       └── user_model_test.dart
└── presentation/
    └── bloc/
        └── user_bloc_test.dart
```

## Componentes Testeables

### 1. Domain Layer (Prioridad: CRÍTICA)

**UseCases** - Lógica pura de negocio

```dart
// lib/domain/usecases/get_user.dart
class GetUser {
  final UserRepository repository;
  
  GetUser(this.repository);
  
  Future<Either<Failure, User>> call(GetUserParams params) {
    return repository.getUser(params.id);
  }
}

class GetUserParams extends Equatable {
  final String id;
  
  const GetUserParams(this.id);
  
  @override
  List<Object> get props => [id];
}
```

**Test correspondiente**

```dart
// test/domain/usecases/get_user_test.dart
import 'package:dartz/dartz.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:my_app/domain/entities/user.dart';
import 'package:my_app/domain/usecases/get_user.dart';
import 'package:my_app/domain/repositories/user_repository.dart';

class MockUserRepository extends Mock implements UserRepository {}

void main() {
  late MockUserRepository mockRepository;
  late GetUser getUser;

  setUp(() {
    mockRepository = MockUserRepository();
    getUser = GetUser(mockRepository);
  });

  group('GetUser UseCase', () {
    const testId = '123';
    const testUser = User(id: '123', name: 'John Doe', email: 'john@example.com');

    test('should get user from the repository', () async {
      // Arrange
      when(() => mockRepository.getUser(testId)).thenAnswer(
        (_) async => const Right(testUser),
      );

      // Act
      final result = await getUser(const GetUserParams(testId));

      // Assert
      expect(result, const Right(testUser));
      verify(() => mockRepository.getUser(testId)).called(1);
      verifyNoMoreInteractions(mockRepository);
    });

    test('should return Failure when repository fails', () async {
      // Arrange
      when(() => mockRepository.getUser(testId)).thenAnswer(
        (_) async => Left(ServerFailure()),
      );

      // Act
      final result = await getUser(const GetUserParams(testId));

      // Assert
      expect(result, isA<Left>());
      verify(() => mockRepository.getUser(testId)).called(1);
    });

    test('should not call repository when params are invalid', () async {
      // Arrange - usar validación en el usecase
      
      // Act & Assert
      // Implementar validación de parámetros
    });
  });
}
```

## Mockito (Official Flutter Approach)

### ¿Cuándo Usar Mockito?

**OFICIAL**: Mockito con `@GenerateMocks` es recomendado por Flutter docs para servicios complejos con tipos específicos, especialmente HTTP clients.

### Setup Mockito

**pubspec.yaml**:
```yaml
dev_dependencies:
  mockito: ^5.4.0
  build_runner: ^2.4.0
```

**Generar mocks**:
```bash
dart run build_runner build
```

### Ejemplo Real: fetchAlbum con HTTP Client

**test/data/datasources/album_remote_datasource_test.dart**:
```dart
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';
import 'package:http/http.dart' as http;
import 'album_remote_datasource_test.mocks.dart'; // Generado

@GenerateMocks([http.Client])
void main() {
  group('AlbumRemoteDataSource with Mockito', () {
    late MockClient mockClient;
    late AlbumRemoteDataSource dataSource;

    setUp(() {
      mockClient = MockClient();
      dataSource = AlbumRemoteDataSourceImpl(client: mockClient);
    });

    test('fetchAlbum returns Album on 200 response', () async {
      // Arrange
      const testAlbumId = 1;
      final mockResponse = http.Response(
        '{"id": 1, "title": "Test Album", "userId": 1}',
        200,
      );
      
      when(mockClient.get(any)).thenAnswer((_) async => mockResponse);

      // Act
      final result = await dataSource.getAlbum(testAlbumId);

      // Assert
      expect(result.title, equals('Test Album'));
      expect(result.id, equals(1));
      verify(mockClient.get(
        Uri.parse('https://jsonplaceholder.typicode.com/albums/$testAlbumId'),
      )).called(1);
    });

    test('fetchAlbum throws AlbumException on 404', () async {
      // Arrange
      when(mockClient.get(any)).thenAnswer(
        (_) async => http.Response('Not Found', 404),
      );

      // Act & Assert
      expect(
        () => dataSource.getAlbum(999),
        throwsA(isA<AlbumException>()),
      );
    });

    test('fetchAlbum throws exception on network error', () async {
      // Arrange
      when(mockClient.get(any)).thenThrow(
        SocketException('Network error'),
      );

      // Act & Assert
      expect(
        () => dataSource.getAlbum(1),
        throwsA(isA<AlbumException>()),
      );
    });
  });
}
```

### Por Qué Mockito para HTTP

- **Type-safe**: `@GenerateMocks([http.Client])` genera MockClient tipado
- **Verificación fuerte**: `verify().called()` autocompleta con IDE
- **Less boilerplate**: Sin constructores manuales como con Mocktail
- **Official**: Recomendado en docs.flutter.dev/cookbook/testing/unit/mocking

### Mockito vs Mocktail Comparación

| Aspecto | Mockito | Mocktail |
|--------|---------|----------|
| Generación | `@GenerateMocks` (build_runner) | Manual |
| HTTP Client | ✅ Ideal | Funciona |
| Interfaces | ✅ Ambos | ✅ Ambos |
| Complejidad | Media (setup inicial) | Baja |
| Dependencies | mockito + build_runner | mocktail |
| Oficial | ✅ Recomendado Flutter | Comunitario |

### 2. Data Layer (Prioridad: ALTA)

**Repositories**

```dart
// test/data/repositories/user_repository_impl_test.dart
group('UserRepositoryImpl', () {
  late MockUserRemoteDataSource mockRemoteDataSource;
  late MockUserLocalDataSource mockLocalDataSource;
  late UserRepositoryImpl repository;

  setUp(() {
    mockRemoteDataSource = MockUserRemoteDataSource();
    mockLocalDataSource = MockUserLocalDataSource();
    repository = UserRepositoryImpl(
      remoteDataSource: mockRemoteDataSource,
      localDataSource: mockLocalDataSource,
    );
  });

  group('getUser', () {
    test('should return remote data when call to remote is successful', 
      () async {
      // Arrange
      when(() => mockRemoteDataSource.getUser('123')).thenAnswer(
        (_) async => testUserModel,
      );

      // Act
      final result = await repository.getUser('123');

      // Assert
      expect(result, const Right(testUser));
      verify(() => mockRemoteDataSource.getUser('123')).called(1);
    });

    test('should save user locally when remote call succeeds', () async {
      // Arrange
      when(() => mockRemoteDataSource.getUser('123')).thenAnswer(
        (_) async => testUserModel,
      );
      when(() => mockLocalDataSource.cacheUser(testUserModel)).thenAnswer(
        (_) async => Future.value(),
      );

      // Act
      await repository.getUser('123');

      // Assert
      verify(() => mockLocalDataSource.cacheUser(testUserModel)).called(1);
    });

    test('should return cached data when remote fails', () async {
      // Arrange
      when(() => mockRemoteDataSource.getUser('123')).thenThrow(
        ServerException(),
      );
      when(() => mockLocalDataSource.getUser('123')).thenAnswer(
        (_) async => testUserModel,
      );

      // Act
      final result = await repository.getUser('123');

      // Assert
      expect(result, const Right(testUser));
      verify(() => mockLocalDataSource.getUser('123')).called(1);
    });

    test('should return Failure when both remote and local fail', 
      () async {
      // Arrange
      when(() => mockRemoteDataSource.getUser('123')).thenThrow(
        ServerException(),
      );
      when(() => mockLocalDataSource.getUser('123')).thenThrow(
        CacheException(),
      );

      // Act
      final result = await repository.getUser('123');

      // Assert
      expect(result, isA<Left>());
    });
  });
});
```

**DataSources**

```dart
// test/data/datasources/user_remote_datasource_test.dart
group('UserRemoteDataSource', () {
  late MockHttpClient mockHttpClient;
  late UserRemoteDataSourceImpl dataSource;

  setUp(() {
    mockHttpClient = MockHttpClient();
    dataSource = UserRemoteDataSourceImpl(client: mockHttpClient);
  });

  test('should perform a GET request on /users/123', () async {
    // Arrange
    when(() => mockHttpClient.get(any())).thenAnswer(
      (_) async => http.Response(jsonEncode({'id': '123', ...}), 200),
    );

    // Act
    await dataSource.getUser('123');

    // Assert
    verify(() => mockHttpClient.get(
      Uri.parse('https://api.example.com/users/123'),
    )).called(1);
  });

  test('should throw ServerException when response code is not 200', 
    () async {
    // Arrange
    when(() => mockHttpClient.get(any())).thenAnswer(
      (_) async => http.Response('Server error', 500),
    );

    // Act & Assert
    expect(
      () => dataSource.getUser('123'),
      throwsA(isA<ServerException>()),
    );
  });
});
```

**Models (JSON Mapping)**

```dart
// test/data/models/user_model_test.dart
group('UserModel', () {
  test('should be a subclass of User entity', () {
    expect(testUserModel, isA<User>());
  });

  group('fromJson', () {
    test('should return a valid model when the JSON valid is passed', 
      () {
      // Arrange
      final Map<String, dynamic> jsonMap = {
        'id': '123',
        'name': 'John Doe',
        'email': 'john@example.com',
      };

      // Act
      final result = UserModel.fromJson(jsonMap);

      // Assert
      expect(result, testUserModel);
    });

    test('should throw when required fields are missing', () {
      // Arrange
      final Map<String, dynamic> invalidJson = {
        'name': 'John Doe',
        // falta 'id' y 'email'
      };

      // Act & Assert
      expect(
        () => UserModel.fromJson(invalidJson),
        throwsA(isA<ArgumentError>()),
      );
    });
  });

  group('toJson', () {
    test('should return a valid JSON map when model is valid', () {
      // Act
      final result = testUserModel.toJson();

      // Assert
      expect(result, {
        'id': '123',
        'name': 'John Doe',
        'email': 'john@example.com',
      });
    });
  });
});
```

### 3. Presentation Layer - BLoCs (Prioridad: MEDIA)

```dart
// test/presentation/bloc/user_bloc_test.dart
import 'package:bloc_test/bloc_test.dart';

void main() {
  late MockGetUser mockGetUser;
  late UserBloc userBloc;

  setUp(() {
    mockGetUser = MockGetUser();
    userBloc = UserBloc(getUser: mockGetUser);
  });

  tearDown(() {
    userBloc.close();
  });

  group('UserBloc', () {
    group('GetUserEvent', () {
      blocTest<UserBloc, UserState>(
        'emits [UserLoading, UserLoaded] when GetUserEvent is added and data is gotten successfully',
        build: () {
          when(() => mockGetUser(any())).thenAnswer(
            (_) async => const Right(testUser),
          );
          return userBloc;
        },
        act: (bloc) => bloc.add(const GetUserEvent('123')),
        expect: () => [
          UserLoading(),
          UserLoaded(user: testUser),
        ],
        verify: (_) {
          verify(() => mockGetUser(const GetUserParams('123'))).called(1);
        },
      );

      blocTest<UserBloc, UserState>(
        'emits [UserLoading, UserError] when GetUserEvent fails',
        build: () {
          when(() => mockGetUser(any())).thenAnswer(
            (_) async => Left(ServerFailure()),
          );
          return userBloc;
        },
        act: (bloc) => bloc.add(const GetUserEvent('123')),
        expect: () => [
          UserLoading(),
          UserError(message: 'Server error'),
        ],
      );

      blocTest<UserBloc, UserState>(
        'emits [UserError] with proper message on cache failure',
        build: () {
          when(() => mockGetUser(any())).thenAnswer(
            (_) async => Left(CacheFailure()),
          );
          return userBloc;
        },
        act: (bloc) => bloc.add(const GetUserEvent('123')),
        expect: () => [
          UserLoading(),
          UserError(message: 'Cache error'),
        ],
      );

      blocTest<UserBloc, UserState>(
        'does not emit any state when invalid params are provided',
        build: () => userBloc,
        act: (bloc) => bloc.add(const GetUserEvent('')),
        expect: () => [],
      );
    });

    group('UpdateUserEvent', () {
      blocTest<UserBloc, UserState>(
        'emits [UserLoading, UserUpdated] on success',
        build: () {
          when(() => mockUpdateUser(any())).thenAnswer(
            (_) async => const Right(updatedUser),
          );
          return userBloc;
        },
        act: (bloc) => bloc.add(UpdateUserEvent(user: updatedUser)),
        expect: () => [
          UserLoading(),
          UserUpdated(user: updatedUser),
        ],
      );
    });
  });
}
```

## Test Fixtures (Datos Reutilizables)

```dart
// test/fixtures/test_data.dart
import 'package:my_app/data/models/user_model.dart';
import 'package:my_app/domain/entities/user.dart';

const testUser = User(
  id: '123',
  name: 'John Doe',
  email: 'john@example.com',
);

const testUserModel = UserModel(
  id: '123',
  name: 'John Doe',
  email: 'john@example.com',
);

const updatedUser = User(
  id: '123',
  name: 'Jane Doe',
  email: 'jane@example.com',
);

// Factories para crear datos dinámicos
UserModel createUserModel({
  String id = '123',
  String name = 'Test User',
  String email = 'test@example.com',
}) {
  return UserModel(id: id, name: name, email: email);
}
```

```dart
// test/fixtures/fixture_reader.dart
import 'dart:io';

String fixture(String name) => File('test/fixtures/$name').readAsStringSync();

// Uso: 
// final jsonString = fixture('user.json');
// final jsonMap = jsonDecode(jsonString) as Map<String, dynamic>;
```

## Patrones Avanzados

### Testing de Streams

```dart
test('should emit multiple values over time', () {
  expect(
    repository.watchUsers(),
    emitsInOrder([
      isA<List<User>>().having((list) => list.length, 'length', 0),
      isA<List<User>>().having((list) => list.length, 'length', 1),
      isA<List<User>>().having((list) => list.length, 'length', 2),
    ]),
  );
});
```

### Testing con Delays

```dart
blocTest<UserBloc, UserState>(
  'emits state after delay',
  build: () => userBloc,
  act: (bloc) => bloc.add(GetUserEvent('123')),
  wait: const Duration(milliseconds: 500),
  expect: () => [UserLoading(), UserLoaded(user: testUser)],
);
```

### Testing de Excepciones

```dart
test('should throw ServerException on connection error', () {
  when(() => mockHttpClient.get(any())).thenThrow(
    SocketException('No host specified'),
  );

  expect(
    () => dataSource.getUser('123'),
    throwsA(isA<ServerException>()),
  );
});
```

## Comandos Útiles

```bash
# Ejecutar todos los unit tests
flutter test

# Ejecutar tests específicos
flutter test test/domain/usecases/get_user_test.dart

# Ejecutar con reporte de cobertura
flutter test --coverage

# Ejecutar con watch mode
flutter test --watch

# Ejecutar tests que coincidan con un patrón
flutter test --name "GetUser"

# Ejecutar con más detalles
flutter test --verbose
```

## Buenas Prácticas

### ✅ Hacer

- Tests independientes y sin side effects
- Agrupar tests relacionados con `group()`
- Usar `setUp()` y `tearDown()` para inicializar/limpiar
- Mockear todas las dependencias externas
- Un test = un comportamiento
- Nombres descriptivos: `test('should return user when repository succeeds')`
- Verificar interacciones con mocks

### ❌ Evitar

- Lógica compleja dentro de tests
- Llamadas reales a red o BD
- Tests que dependen del orden de ejecución
- Print statements (usar logs de development)
- Ignorar excepciones en mocks (registrar fallbacks)
- Tests de implementación en lugar de comportamiento

## Cobertura de Código

### Objetivos por Capa

| Capa | Cobertura Objetivo | Crítico |
|---|---|---|
| Domain (Entities, UseCases) | 90%+ | ✅ Sí |
| Data (Repositories, DataSources) | 85%+ | ✅ Sí |
| Presentation (BLoCs) | 75%+ | ✅ Sí |
| Presentation (Widgets) | 60%+ | ⚠️ Complementario |

### Generar Reporte

```bash
flutter test --coverage
genhtml coverage/lcov.info -o coverage/html
open coverage/html/index.html

# En CI/CD
flutter test --coverage
lcov --list coverage/lcov.info
```
