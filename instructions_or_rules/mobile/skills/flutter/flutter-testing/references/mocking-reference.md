# Mocking & Dependency Injection Reference

Guía detallada para crear mocks efectivos, configurar inyección de dependencias y testear código complejo.

## ¿Por Qué Mockear?

### Beneficios
- **Velocidad**: Tests unitarios sin I/O
- **Aislamiento**: Probar solo tu código
- **Consistencia**: Comportamiento predecible
- **Parallelización**: Ejecutar tests en paralelo sin conflictos

### Costos
- Overhead de setup
- Riesgo de divergencia (mock != realidad)
- Mantenimiento

## Comparación de Librerías de Mocking

| Librería | Null Safety | Sintaxis | Casos de Uso |
|---|---|---|---|
| **Mocktail** | ✅ Full | Moderna | General (Recomendado) |
| **Mockito** | ⚠️ Limitado | Antigua | Legado |
| **Fake** (Manual) | ✅ Full | Verbosa | Casos específicos |

## Setup Inicial

```yaml
dev_dependencies:
  test: ^1.24.0
  mocktail: ^1.0.0
  bloc_test: ^9.1.0
```

## Mocktail Fundamentals

### 1. Crear Mocks Básicos

```dart
// Librería a mockear
abstract class UserRepository {
  Future<User> getUser(String id);
  Future<void> deleteUser(String id);
  Future<List<User>> getAllUsers();
}

// Crear mock
class MockUserRepository extends Mock implements UserRepository {}

// En el test
void main() {
  late MockUserRepository mockRepository;

  setUp(() {
    mockRepository = MockUserRepository();
  });

  test('example', () {
    // Test aquí
  });
}
```

### 2. Stubbing (Configurar Respuestas)

```dart
test('should get user successfully', () {
  // Configurar el mock para retornar un valor
  when(() => mockRepository.getUser('123')).thenAnswer(
    (_) async => User(id: '123', name: 'John'),
  );

  // El mock ahora simula ese comportamiento
  final user = await mockRepository.getUser('123');
  expect(user.id, '123');
});
```

### 3. Verification (Verificar Llamadas)

```dart
test('should call repository exactly once', () {
  when(() => mockRepository.getUser('123')).thenAnswer(
    (_) async => User(id: '123', name: 'John'),
  );

  // Código en test
  mockRepository.getUser('123');

  // Verificar que se llamó exactamente 1 vez
  verify(() => mockRepository.getUser('123')).called(1);

  // O verificar que fue llamado N veces
  verify(() => mockRepository.getUser(any())).called(greaterThan(0));
});
```

### 4. Matchers para Parámetros

```dart
// Hacer match en argumentos sin importar valores exactos
when(() => mockRepository.getUser(any())).thenAnswer(
  (_) async => testUser,
);

// Con predicado personalizado
when(() => mockRepository.getUser(
  argThat(startsWith('user-')),
)).thenAnswer((_) async => testUser);

// Named parameters
when(() => mockRepository.updateUser(
  id: any(named: 'id'),
  name: 'John',
)).thenAnswer((_) async => testUser);
```

## Patrones Avanzados de Mocking

### 1. Mock con Comportamiento Complejo

```dart
// Caso: Mock que se comporta diferente según parámetros
late MockUserRepository mockRepository;

setUp(() {
  mockRepository = MockUserRepository();

  // Usuario válido
  when(() => mockRepository.getUser('valid-id')).thenAnswer(
    (_) async => User(id: 'valid-id', name: 'Alice'),
  );

  // Usuario no encontrado
  when(() => mockRepository.getUser('invalid-id')).thenThrow(
    NotFoundException('User not found'),
  );

  // Cualquier otro ID
  when(() => mockRepository.getUser(any())).thenAnswer(
    (_) async => User(id: 'default', name: 'Default User'),
  );
});

test('handles valid ID', () async {
  final user = await mockRepository.getUser('valid-id');
  expect(user.name, 'Alice');
});

test('throws for invalid ID', () {
  expect(
    () => mockRepository.getUser('invalid-id'),
    throwsA(isA<NotFoundException>()),
  );
});
```

### 2. Fallback Values (Valores Défault)

```dart
// Caso: Parámetro de tipo personalizado
class GetUserParams extends Equatable {
  final String id;
  const GetUserParams(this.id);
  
  @override
  List<Object> get props => [id];
}

// Mock con UseCase que requiere GetUserParams
class MockGetUserUseCase extends Mock implements GetUser {}

void main() {
  late MockGetUserUseCase mockUseCase;

  setUp(() {
    mockUseCase = MockGetUserUseCase();
    
    // ⚠️ Registrar fallback para tipos personalizados
    registerFallbackValue(const GetUserParams('test'));
  });

  test('calls usecase with correct params', () {
    when(() => mockUseCase(any())).thenAnswer(
      (_) async => Right(testUser),
    );

    // Ahora puedo usar 'any()' con GetUserParams
    mockUseCase(const GetUserParams('123'));
    
    verify(() => mockUseCase(any())).called(1);
  });
}
```

### 3. Streaming Behavior

```dart
// Mock para métodos que retornan Stream
class MockUserRepository extends Mock implements UserRepository {
  Stream<List<User>> watchUsers();
}

test('should listen to user stream', () {
  // Configurar stream
  when(() => mockRepository.watchUsers()).thenAnswer(
    (_) => Stream.fromIterable([
      [user1],
      [user1, user2],
      [user1, user2, user3],
    ]),
  );

  expect(
    mockRepository.watchUsers(),
    emitsInOrder([
      [user1],
      [user1, user2],
      [user1, user2, user3],
    ]),
  );
});
```

### 4. Callbacks y Void Methods

```dart
// Mock de método void
class MockLogger extends Mock implements Logger {
  void log(String message);
}

test('should log error message', () {
  final mockLogger = MockLogger();

  // No necesita thenAnswer para void
  mockLogger.log('Error occurred');

  // Verificar que se llamó
  verify(() => mockLogger.log('Error occurred')).called(1);
});

// Con callbacks
class MockCallback extends Mock {
  void onSuccess(String result);
  void onError(Exception error);
}

test('calls appropriate callback', () {
  final mockCallback = MockCallback();

  // Código que invoca callbacks
  try {
    // ...
    mockCallback.onSuccess('Result');
  } catch (e) {
    mockCallback.onError(e as Exception);
  }

  verify(() => mockCallback.onSuccess('Result')).called(1);
  verifyNever(() => mockCallback.onError(any()));
});
```

## Inyección de Dependencias

### Por Qué Inyectar Dependencias

```dart
// ❌ MAL: Acoplamiento directo
class UserService {
  final repository = UserRepository();  // Difícil de testear
}

// ✅ BIEN: Inyección de dependencias
class UserService {
  final UserRepository repository;
  
  UserService({required this.repository});  // Fácil de testear
}
```

### Get_it (Service Locator)

```dart
// setup_service_locator.dart
import 'package:get_it/get_it.dart';

final getIt = GetIt.instance;

void setupServiceLocator() {
  // Registrar dependencia real
  getIt.registerSingleton<UserRepository>(
    UserRepositoryImpl(),
  );

  // Registrar usecase
  getIt.registerSingleton<GetUser>(
    GetUser(getIt<UserRepository>()),
  );

  // Registrar BLoC
  getIt.registerSingleton<UserBloc>(
    UserBloc(getUser: getIt<GetUser>()),
  );
}

// En test
void main() {
  setUp(() {
    // Limpiar antes de cada test
    getIt.reset();
    
    // Registrar mocks
    getIt.registerSingleton<UserRepository>(MockUserRepository());
    getIt.registerSingleton<GetUser>(GetUser(getIt<UserRepository>()));
  });
}
```

### Patrón de Factory (Recomendado para Testing)

```dart
// Mejor que Service Locator para tests
class UserBloc extends Bloc<UserEvent, UserState> {
  final GetUser getUser;
  
  UserBloc({required this.getUser}) : super(UserInitial()) {
    on<GetUserEvent>(_onGetUserEvent);
  }

  Future<void> _onGetUserEvent(
    GetUserEvent event,
    Emitter<UserState> emit,
  ) async {
    // ...
  }
}

// En test - Inyectar directamente
void main() {
  late MockGetUser mockGetUser;
  late UserBloc userBloc;

  setUp(() {
    mockGetUser = MockGetUser();
    
    // No usar Service Locator
    userBloc = UserBloc(getUser: mockGetUser);
  });

  tearDown(() {
    userBloc.close();
  });
}
```

## Testing de Código Complejo

### 1. Testing de Transformaciones de Datos

```dart
// Mapper complejo
class UserMapper {
  static User toDomain(UserModel model) {
    return User(
      id: model.id,
      name: model.name.trim(),
      email: model.email.toLowerCase(),
      isActive: model.status == 'active',
      createdAt: DateTime.parse(model.createdAt),
    );
  }

  static UserModel toModel(User entity) {
    return UserModel(
      id: entity.id,
      name: entity.name,
      email: entity.email,
      status: entity.isActive ? 'active' : 'inactive',
      createdAt: entity.createdAt.toIso8601String(),
    );
  }
}

// Tests exhaustivos
void main() {
  group('UserMapper', () {
    test('toDomain maps model to entity correctly', () {
      // Arrange
      final model = UserModel(
        id: '123',
        name: '  John Doe  ',  // Con espacios
        email: 'JOHN@EXAMPLE.COM',  // Mayúsculas
        status: 'active',
        createdAt: '2024-02-23T10:00:00Z',
      );

      // Act
      final entity = UserMapper.toDomain(model);

      // Assert
      expect(entity.id, '123');
      expect(entity.name, 'John Doe');  // Trim
      expect(entity.email, 'john@example.com');  // Lower
      expect(entity.isActive, true);
      expect(entity.createdAt, DateTime.parse('2024-02-23T10:00:00Z'));
    });

    test('toModel handles inactive status', () {
      // Arrange
      final entity = User(
        id: '123',
        name: 'John',
        email: 'john@example.com',
        isActive: false,
      );

      // Act
      final model = UserMapper.toModel(entity);

      // Assert
      expect(model.status, 'inactive');
    });

    test('roundtrip preserves data', () {
      // Arrange
      final originalEntity = User(
        id: '123',
        name: 'John Doe',
        email: 'john@example.com',
        isActive: true,
      );

      // Act
      final model = UserMapper.toModel(originalEntity);
      final resultEntity = UserMapper.toDomain(model);

      // Assert
      expect(resultEntity, originalEntity);
    });
  });
}
```

### 2. Testing de Validadores

```dart
// Validador
class EmailValidator {
  static bool validate(String email) {
    final regex = RegExp(
      r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    );
    return regex.hasMatch(email);
  }
}

// Tests exhaustivos
void main() {
  group('EmailValidator', () {
    test('validates correct email addresses', () {
      expect(EmailValidator.validate('user@example.com'), true);
      expect(EmailValidator.validate('user.name@example.co.uk'), true);
      expect(EmailValidator.validate('user+tag@example.com'), true);
    });

    test('rejects invalid email addresses', () {
      expect(EmailValidator.validate('invalidemail'), false);
      expect(EmailValidator.validate('user@'), false);
      expect(EmailValidator.validate('@example.com'), false);
      expect(EmailValidator.validate('user@.com'), false);
      expect(EmailValidator.validate('user @example.com'), false);
    });

    test('handles edge cases', () {
      expect(EmailValidator.validate(''), false);
      expect(EmailValidator.validate(' '), false);
      expect(EmailValidator.validate('user@example'), false);
    });
  });
}
```

### 3. Testing de Lógica Condicional Compleja

```dart
// Lógica compleja
class DiscountStrategy {
  static double calculateDiscount(
    double amount,
    int loyaltyPoints,
    bool isPremium,
    bool isHoliday,
  ) {
    double discount = 0;

    // Base discount por loyaltyPoints
    if (loyaltyPoints >= 1000) {
      discount += 0.15;  // 15%
    } else if (loyaltyPoints >= 500) {
      discount += 0.10;  // 10%
    } else if (loyaltyPoints >= 100) {
      discount += 0.05;  // 5%
    }

    // Premium member adicional
    if (isPremium) {
      discount += 0.05;
    }

    // Holiday special
    if (isHoliday) {
      discount += 0.10;
    }

    // Cap máximo
    if (discount > 0.30) {
      discount = 0.30;  // 30% máximo
    }

    return amount * (1 - discount);
  }
}

// Tests exhaustivos cubriendo todas las combinaciones
void main() {
  group('DiscountStrategy', () {
    test('applies no discount for new customers', () {
      final result = DiscountStrategy.calculateDiscount(100, 0, false, false);
      expect(result, 100);
    });

    test('applies discount for loyalty points', () {
      expect(
        DiscountStrategy.calculateDiscount(100, 100, false, false),
        85,  // 5% discount
      );
      expect(
        DiscountStrategy.calculateDiscount(100, 500, false, false),
        90,  // 10% discount
      );
      expect(
        DiscountStrategy.calculateDiscount(100, 1000, false, false),
        85,  // 15% discount
      );
    });

    test('applies premium discount', () {
      final withoutPremium = DiscountStrategy.calculateDiscount(100, 100, false, false);
      final withPremium = DiscountStrategy.calculateDiscount(100, 100, true, false);
      expect(withPremium, lessThan(withoutPremium));
    });

    test('applies holiday discount', () {
      final normal = DiscountStrategy.calculateDiscount(100, 100, false, false);
      final holiday = DiscountStrategy.calculateDiscount(100, 100, false, true);
      expect(holiday, lessThan(normal));
    });

    test('caps max discount at 30%', () {
      // Combinar todos los descuentos posibles
      final result = DiscountStrategy.calculateDiscount(100, 1000, true, true);
      // 15% + 5% + 10% = 30% máximo
      expect(result, 70);  // 100 * 0.70
    });

    test('applies stacking discounts correctly', () {
      // 15% (loyalty) + 5% (premium) = 20% total
      final result = DiscountStrategy.calculateDiscount(100, 1000, true, false);
      expect(result, 80);
    });
  });
}
```

## Mejores Prácticas de Mocking

### ✅ Hacer

- Mockear solo dependencias externas
- Un mock por dependencia
- Nombres claros: `MockUserRepository`
- Registrar fallbacks para tipos personalizados
- Verificar llamadas críticas
- Reset de mocks en setUp

### ❌ Evitar

- Mockear demasiado (cuidado con overspec)
- Mocks que cambian constantemente
- Mockear lo que estás testando
- Tests acoplados a implementación
- Verificar demasiadas llamadas internas

## Debugging de Mocks

```dart
// Verificar qué se pidió al mock
test('debug mock calls', () {
  final mockRepository = MockUserRepository();

  when(() => mockRepository.getUser(any())).thenAnswer(
    (_) async => testUser,
  );

  // Hacer algo con el mock
  mockRepository.getUser('123');
  mockRepository.getUser('456');

  // Verificar todas las llamadas
  final calls = verify(
    () => mockRepository.getUser(any()),
  ).captured;

  print('Called with: $calls');  // ['123', '456']
});

// No se llamó en absoluto
test('verify never called', () {
  final mockRepository = MockUserRepository();

  verifyNever(() => mockRepository.deleteUser(any()));
});

// No más interacciones
test('verify no more interactions', () {
  final mockRepository = MockUserRepository();

  when(() => mockRepository.getUser('123')).thenAnswer(
    (_) async => testUser,
  );

  mockRepository.getUser('123');

  verifyNoMoreInteractions(mockRepository);  // Pass
});
```

## Template de Test con Mocking Completo

```dart
void main() {
  late MockUserRepository mockRepository;
  late GetUser useCase;

  setUp(() {
    mockRepository = MockUserRepository();
    useCase = GetUser(mockRepository);
    
    // Registrar fallbacks
    registerFallbackValue(const GetUserParams(''));
  });

  tearDown(() {
    reset(mockRepository);  // Limpiar después de cada test
  });

  group('GetUser UseCase', () {
    test('should return user when repository succeeds', () async {
      // Arrange
      when(() => mockRepository.getUser(any()))
          .thenAnswer((_) async => testUser);

      // Act
      final result = await useCase(const GetUserParams('123'));

      // Assert
      expect(result, const Right(testUser));
      verify(() => mockRepository.getUser('123')).called(1);
      verifyNoMoreInteractions(mockRepository);
    });

    test('should return failure when repository fails', () async {
      // Arrange
      when(() => mockRepository.getUser(any()))
          .thenThrow(ServerException());

      // Act
      final result = await useCase(const GetUserParams('123'));

      // Assert
      expect(result, isA<Left>());
      verify(() => mockRepository.getUser('123')).called(1);
    });
  });
}
```
