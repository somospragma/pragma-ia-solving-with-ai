---
name: flutter-testing
description: Contiene buenas prácticas para realizar pruebas en Flutter, incluyendo pruebas unitarias, de widget y de integración.
metadata:
  author: Pragma Mobile Chapter
  version: "1.0"
---

# Flutter Testing Skill

Este documento define las reglas y mejores prácticas para implementar testing en aplicaciones Flutter siguiendo los estándares de Pragma.

## Principios Fundamentales

### Arquitectura y Testabilidad
- **Separación de responsabilidades**: La arquitectura limpia de 3 capas (Presentation, Domain, Data) facilita el testing aislado de cada componente.
- **Inversión de dependencias**: Todos los componentes deben depender de abstracciones (interfaces/clases abstractas), no de implementaciones concretas.
- **Capa Domain pura**: Domain debe ser Dart puro sin dependencias de Flutter, lo que permite ejecutar tests unitarios rápidamente sin inicializar el framework Flutter.
- **Modelos inmutables**: Todos los modelos de datos y estados deben tener propiedades `final` para garantizar predictibilidad en los tests.
- **Inyección de dependencias**: Usar Get_it o similar para facilitar el mocking y la sustitución de dependencias en tests.

### Patrón AAA (Arrange-Act-Assert)
Todas las pruebas unitarias y de widget deben seguir este patrón:
```dart
test('should return valid data when call is successful', () {
  // Arrange: Preparar datos y configurar mocks
  when(() => mockRepository.getData()).thenAnswer((_) async => expectedData);
  
  // Act: Ejecutar la acción a probar
  final result = await useCase.call();
  
  // Assert: Verificar el resultado esperado
  expect(result, equals(Right(expectedData)));
  verify(() => mockRepository.getData()).called(1);
});
```

## Tipos de Pruebas Generales

Flutter requiere una estrategia multi-nivel de testing para garantizar calidad. Este documento presenta un overview de cada tipo; para detalles especializados, consultar los documentos de referencias.

| Tipo de Prueba | Objetivo | Velocidad | Cobertura | Documento de Referencia |
|---|---|---|---|---|
| **Unit Tests** | Lógica aislada (UseCases, Repositories, Mappers) | ⚡⚡⚡ Rápido | Alta en Domain | [unit-testing-reference.md](references/unit-testing-reference.md) |
| **Mutation Tests** | Validar efectividad de los tests existentes | 🐢 Muy lento | Complementaria | [mutation-testing-reference.md](references/mutation-testing-reference.md) |
| **Widget Tests** | Renderizado y interacción de UI | ⚡⚡ Medio | Media en Presentation | [widget-testing-reference.md](references/widget-testing-reference.md) |
| **Integration Tests** | Flujos completos end-to-end | 🐢 Lento | Baja pero crítica | [integration-testing-reference.md](references/integration-testing-reference.md) |
| **Golden Tests** | Diseño visual y regresiones de UI | ⚡⚡ Medio | Complementaria | [golden-testing-reference.md](references/golden-testing-reference.md) |

### Temas Especializados

**Mocking & Dependency Injection** - [mocking-reference.md](references/mocking-reference.md)
- ✅ Cuándo usar: En TODOS los tests (unit, widget, integration) cuando necesites aislar dependencias externas
- ✅ Casos comunes: HTTP clients, repositorios, servicios, puertos I/O
- ✅ Decisión crítica: Mockito (type-safe, @GenerateMocks) vs Mocktail (manual, pragmático)
- Ver SKILL.md sección "Decisión: Mockito vs Mocktail" para elegir automáticamente

**Testing Native Plugins** - [native-plugins-testing-reference.md](references/native-plugins-testing-reference.md)
- ✅ Cuándo usar: Cuando tu app depende de plugins nativos (GPS, cámara, permisos, sensores)
- ✅ Desafío: No puedes testear código Kotlin/Swift directamente, necesitas aislar
- ✅ Patrón: Crear interface en Dart → Mock MethodChannel → Test sin compilar nativo
- ✅ Ejemplos: LocationDataSource, PermissionHandler, HttpService vía MethodChannel

### Estrategia Recomendada (Pirámide de Testing)

```
        🔼 Integration Tests (5-10%)
       🔷 Widget Tests (20-30%)
      🔶 Mutation Tests (Complementario)
     🔸 Unit Tests (60-70%)
```

### 1. Unit Tests (Pruebas Unitarias)
**Objetivo**: Probar lógica de negocio aislada sin dependencias externas.

**Qué probar**:
- ✅ UseCases de la capa Domain
- ✅ Repositories (implementaciones de Data layer)
- ✅ DataSources (Local y Remote)
- ✅ Mappers y converters (toJson, fromJson, toEntity, toModel)
- ✅ Validators y utilidades
- ✅ BLoCs/Cubits (estados y lógica)

**Paquetes requeridos**:
```yaml
dev_dependencies:
  test: ^1.24.0
  mocktail: ^1.0.0  # Preferir mocktail sobre mockito por null-safety
  bloc_test: ^9.1.0
```

**Estructura de carpetas**:
```
test/
  domain/
    usecases/
      get_user_usecase_test.dart
  data/
    repositories/
      user_repository_impl_test.dart
    datasources/
      user_remote_datasource_test.dart
    models/
      user_model_test.dart
  presentation/
    bloc/
      user_bloc_test.dart
```

**Reglas específicas**:
- Un archivo de test por cada archivo de implementación
- Nomenclatura: `{nombre_archivo}_test.dart`
- Agrupar tests relacionados usando `group()`
- Usar `setUp()` para inicializar mocks compartidos
- Usar `tearDown()` para limpiar recursos si es necesario
- Tests deben ser independientes entre sí
- Tests deben ser determinísticos (mismo resultado cada vez)

### 2. Widget Tests
**Objetivo**: Probar widgets de forma aislada verificando UI y comportamiento.

**Qué probar**:
- ✅ Renderizado correcto de widgets
- ✅ Interacciones de usuario (tap, scroll, input)
- ✅ Navegación entre pantallas
- ✅ Actualización de UI según estados del BLoC
- ✅ Validación de formularios
- ✅ Widgets personalizados

**Paquetes requeridos**:
```yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
  mocktail: ^1.0.0
  bloc_test: ^9.1.0
```

**Estructura**:
```
test/
  presentation/
    widgets/
      custom_button_test.dart
    pages/
      home_page_test.dart
```

**Ejemplo de Widget Test**:
```dart
testWidgets('should display error message when BLoC emits error state', 
  (WidgetTester tester) async {
  // Arrange
  whenListen(
    mockUserBloc,
    Stream.fromIterable([UserError('Network error')]),
    initialState: UserInitial(),
  );

  // Act
  await tester.pumpWidget(
    MaterialApp(
      home: BlocProvider<UserBloc>.value(
        value: mockUserBloc,
        child: UserPage(),
      ),
    ),
  );
  await tester.pumpAndSettle();

  // Assert
  expect(find.text('Network error'), findsOneWidget);
});
```

**Reglas específicas**:
- Usar `pumpWidget()` para renderizar el widget
- Usar `pump()` o `pumpAndSettle()` para procesar frames
- Usar `find.byType()`, `find.text()`, `find.byKey()` para localizar widgets
- Mockear BLoCs y providers usando `mocktail` y `bloc_test`
- Simular interacciones con `tester.tap()`, `tester.enterText()`, etc.
- Verificar navegación con `find.byType(TargetPage)`

### 3. Integration Tests
**Objetivo**: Probar flujos completos de la aplicación end-to-end.

**Qué probar**:
- ✅ Flujos críticos de usuario (login, checkout, etc.)
- ✅ Navegación entre múltiples pantallas
- ✅ Integración con servicios reales (opcional)
- ✅ Persistencia de datos

**Paquetes requeridos**:
```yaml
dev_dependencies:
  integration_test:
    sdk: flutter
  flutter_test:
    sdk: flutter
```

**Estructura**:
```
integration_test/
  app_test.dart
  login_flow_test.dart
```

**Reglas específicas**:
- Usar `IntegrationTestWidgetsFlutterBinding.ensureInitialized()`
- Limitar a flujos críticos debido al tiempo de ejecución
- Considerar usar datos de prueba en backend/API de staging
- Ejecutar con: `flutter test integration_test`

## Mocking y Stubbing

### Decisión: Mockito vs Mocktail

**Tabla de Decisión Rápida**:

| Caso | Mockito (Official) | Mocktail (Alternativa) |
|------|------------------|----------------------|
| HTTP Client (typed) | ✅ Recomendado | Posible |
| Repository Interface | Alternativa | ✅ Recomendado |
| Service Externo | ✅ Code Generation | Manual |
| Código .mocks.dart | ✅ Sí (requiere build_runner) | ❌ No |
| Null-Safety | ✅ Sí | ✅ Sí |

**Recomendación**: Usa **Mockito para servicios complejos** (HTTP), **Mocktail para repos internas**.

### Usar Mocktail (Preferido para Contratos Locales)
```dart
import 'package:mocktail/mocktail.dart';

// Crear mock
class MockUserRepository extends Mock implements UserRepository {}

// En setUp
late MockUserRepository mockRepository;

setUp(() {
  mockRepository = MockUserRepository();
});

// Stubbing (configurar respuesta)
when(() => mockRepository.getUser(any())).thenAnswer(
  (_) async => Right(testUser),
);

// Verification (verificar llamada)
verify(() => mockRepository.getUser(userId)).called(1);
verifyNoMoreInteractions(mockRepository);
```

### Usar Mockito (Official Flutter para HTTP/Servicios Externos)

Ver: [Mockito (Official Flutter Approach)](references/unit-testing-reference.md#mockito-official-flutter-approach) en unit-testing-reference para detalles con @GenerateMocks.

### Reglas de Mocking
- ✅ Mockear todas las dependencias externas
- ✅ Registrar fallbacks para tipos personalizados: `registerFallbackValue(TestEntity())`
- ✅ Mockear abstracciones, no implementaciones concretas
- ✅ Verificar que los métodos se llamen con los parámetros correctos
- ❌ No mockear clases del mismo layer que estás probando
- ❌ No mockear clases sealed o con constructores privados

## Testing de BLoCs/Cubits

### Usar bloc_test
```dart
blocTest<UserBloc, UserState>(
  'should emit [UserLoading, UserLoaded] when GetUserEvent is added',
  build: () {
    when(() => mockGetUserUseCase(any())).thenAnswer(
      (_) async => Right(testUser),
    );
    return UserBloc(getUserUseCase: mockGetUserUseCase);
  },
  act: (bloc) => bloc.add(GetUserEvent(userId: '123')),
  expect: () => [
    UserLoading(),
    UserLoaded(user: testUser),
  ],
  verify: (_) {
    verify(() => mockGetUserUseCase(Params(userId: '123'))).called(1);
  },
);
```

### Reglas específicas
- ✅ Probar cada evento y su secuencia de estados
- ✅ Probar casos de éxito y error
- ✅ Verificar que el useCase se llame con los parámetros correctos
- ✅ Usar `seed()` para establecer estado inicial si es necesario
- ✅ Usar `wait` para delays si hay lógica con timers
- ✅ Probar que no se emitan estados adicionales con `expect: () => []`

## Cobertura de Código

### Objetivo de Cobertura
- **Mínimo aceptable**: 70%
- **Objetivo ideal**: 80%+
- **Capa Domain**: 90%+ (crítica para lógica de negocio)
- **Capa Data**: 80%+
- **Capa Presentation**: 70%+ (widgets complejos pueden ser costosos de probar)

### Generar reporte de cobertura
```bash
flutter test --coverage
genhtml coverage/lcov.info -o coverage/html
open coverage/html/index.html
```

### Excluir archivos generados
```yaml
# En tu test config o script
--exclude-from-coverage=**/*.g.dart
--exclude-from-coverage=**/*.freezed.dart
--exclude-from-coverage=**/main.dart
```

## Golden Tests (Testing Visual)

**→ Referencia detallada: [Golden Testing Reference](references/golden-testing-reference.md)**

### Para widgets críticos de UI
```dart
testWidgets('CustomButton should match golden file', (tester) async {
  await tester.pumpWidget(
    MaterialApp(
      home: Scaffold(
        body: CustomButton(
          text: 'Test Button',
          onPressed: () {},
        ),
      ),
    ),
  );
  
  await expectLater(
    find.byType(CustomButton),
    matchesGoldenFile('goldens/custom_button.png'),
  );
});
```

### Reglas
- ✅ Usar para widgets de diseño complejo
- ✅ Versionar los archivos golden en Git
- ✅ Ejecutar en un solo tipo de dispositivo/OS para consistencia
- ✅ Actualizar con: `flutter test --update-goldens`
- ⚠️ Usar con moderación (son costosos de mantener)

## Testing Asíncrono

### Manejo de Futures
```dart
test('should complete async operation', () async {
  // Usar async/await
  final result = await repository.fetchData();
  expect(result, isA<SuccessState>());
});
```

### Manejo de Streams
```dart
test('should emit multiple values', () {
  // Usar expectLater para streams
  expect(
    repository.watchData(),
    emitsInOrder([
      isA<LoadingState>(),
      isA<SuccessState>(),
    ]),
  );
});
```

## Organización y Nomenclatura

### Nomenclatura de Tests
```dart
// ✅ Bueno: Descriptivo y claro
test('should return User when repository call is successful', () {});

// ❌ Malo: Vago
test('test user', () {});
```

### Agrupación con group()
```dart
group('GetUserUseCase', () {
  group('call', () {
    test('should return User when repository returns success', () {});
    test('should return Failure when repository returns error', () {});
    test('should throw Exception when userId is empty', () {});
  });
});
```

### Datos de Prueba (Test Fixtures)
```dart
// test/fixtures/test_data.dart
final testUser = User(
  id: '123',
  name: 'Test User',
  email: 'test@example.com',
);

final testUserModel = UserModel(
  id: '123',
  name: 'Test User',
  email: 'test@example.com',
);

// test/fixtures/fixture_reader.dart
import 'dart:io';

String fixture(String name) => File('test/fixtures/$name').readAsStringSync();
```

## Buenas Prácticas Adicionales

### Performance
- ✅ Tests unitarios deben ejecutarse en < 100ms cada uno
- ✅ Tests de widget deben ejecutarse en < 500ms cada uno
- ✅ Evitar llamadas reales a red o bases de datos
- ✅ Usar `setUpAll()` para inicialización costosa compartida

### Mantenibilidad
- ✅ Un test = una responsabilidad/comportamiento
- ✅ Tests deben ser legibles sin ver la implementación
- ✅ Evitar lógica compleja dentro de tests
- ✅ Reutilizar helpers y factories para crear objetos de prueba
- ✅ Mantener tests actualizados con el código de producción

### CI/CD
- ✅ Ejecutar todos los tests en pipeline antes de merge
- ✅ Fallar el build si la cobertura cae por debajo del umbral
- ✅ Ejecutar `flutter analyze` antes de tests
- ✅ Cache de dependencias para acelerar ejecución

### Comandos Útiles
```bash
# Ejecutar todos los tests
flutter test

# Ejecutar tests específicos
flutter test test/domain/usecases/get_user_usecase_test.dart

# Ejecutar con cobertura
flutter test --coverage

# Ejecutar tests de integración
flutter test integration_test

# Watch mode (re-ejecutar al cambiar archivos)
flutter test --watch

# Ejecutar con más detalle
flutter test --verbose
```

## Casos Especiales

### Testing de Widgets con Provider/Riverpod
```dart
testWidgets('should display data from provider', (tester) async {
  await tester.pumpWidget(
    ProviderScope(
      overrides: [
        userProvider.overrideWith((ref) => mockUser),
      ],
      child: MaterialApp(home: UserWidget()),
    ),
  );
  
  expect(find.text(mockUser.name), findsOneWidget);
});
```

### Testing de Navegación
```dart
testWidgets('should navigate to detail page on tap', (tester) async {
  await tester.pumpWidget(MaterialApp(
    home: HomePage(),
    routes: {
      '/detail': (_) => DetailPage(),
    },
  ));
  
  await tester.tap(find.byKey(Key('detail_button')));
  await tester.pumpAndSettle();
  
  expect(find.byType(DetailPage), findsOneWidget);
});
```

### Testing de Formularios
```dart
testWidgets('should validate email input', (tester) async {
  await tester.pumpWidget(MaterialApp(home: LoginForm()));
  
  // Ingresar email inválido
  await tester.enterText(find.byKey(Key('email_field')), 'invalid-email');
  await tester.tap(find.byKey(Key('submit_button')));
  await tester.pump();
  
  // Verificar mensaje de error
  expect(find.text('Please enter a valid email'), findsOneWidget);
});
```

## Checklist de Testing

Antes de considerar una feature completa, verificar:

- [ ] Tests unitarios para todos los UseCases
- [ ] Tests unitarios para Repositories
- [ ] Tests unitarios para DataSources
- [ ] Tests para BLoCs/Cubits con bloc_test
- [ ] Tests de widget para componentes personalizados
- [ ] Tests de widget para páginas principales
- [ ] Cobertura mínima del 70% alcanzada
- [ ] Todos los tests pasan localmente
- [ ] Todos los tests pasan en CI/CD
- [ ] No hay warnings en `flutter analyze`
- [ ] Mocks creados para todas las dependencias externas
- [ ] Tests siguen el patrón AAA
- [ ] Nomenclatura descriptiva y clara
- [ ] Test fixtures organizados y reutilizables

## Recursos y Referencias

### Documentos de Referencia Especializados

Este SKILL proporciona una visión general. Para profundizar en temas específicos, consulta:

- **[INDEX de Referencias](references/INDEX.md)** - Guía completa de todos los documentos
- **[Unit Testing Reference](references/unit-testing-reference.md)** - Tests unitarios exhaustivos
- **[Mutation Testing Reference](references/mutation-testing-reference.md)** - Validar efectividad de tests
- **[Widget Testing Reference](references/widget-testing-reference.md)** - UI testing detallado
- **[Integration Testing Reference](references/integration-testing-reference.md)** - Flujos end-to-end
- **[Golden Testing Reference](references/golden-testing-reference.md)** - Testing visual
- **[Mocking & Dependency Injection Reference](references/mocking-reference.md)** - Patrones de mocking
- **[Native Plugins & Dependencies Reference](references/native-plugins-testing-reference.md)** - Testing de plugins

### Paquetes Oficiales
- [test](https://pub.dev/packages/test) - Framework de testing de Dart
- [flutter_test](https://api.flutter.dev/flutter/flutter_test/flutter_test-library.html) - Testing de widgets
- [integration_test](https://docs.flutter.dev/testing/integration-tests) - Tests de integración
- [bloc_test](https://pub.dev/packages/bloc_test) - Testing de BLoCs
- [mocktail](https://pub.dev/packages/mocktail) - Mocking library

### Documentación Externa
- [Flutter Testing Guide](https://docs.flutter.dev/testing)
- [Unit Testing Best Practices](https://docs.flutter.dev/cookbook/testing/unit/introduction)
- [Widget Testing Best Practices](https://docs.flutter.dev/cookbook/testing/widget/introduction)
- [BLoC Testing](https://bloclibrary.dev/#/fluttertodostutorial)
- [Mutation Testing Wikipedia](https://en.wikipedia.org/wiki/Mutation_testing)



