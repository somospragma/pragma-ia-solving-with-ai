# Integration Testing Reference

Integration tests prueban flujos completos de la aplicación end-to-end, desde la UI hasta todos los servicios.

## ¿Cuándo Usar Integration Tests?

### ✅ Usar para:
- Flujos críticos de usuario (login, checkout, compra)
- Navegación entre múltiples pantallas
- Sincronización de datos en tiempo real
- Comportamiento con conexión/desconexión de red
- Validación de persistencia de datos

### ❌ Evitar para:
- Validaciones de estilos visuales (usar Golden Tests)
- Lógica aislada (usar Unit Tests)
- Widgets individuales (usar Widget Tests)

## Configuración

```yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
  integration_test:
    sdk: flutter
```

## Estructura de Carpetas

```
integration_test/
├── app_test.dart
├── flows/
│   ├── login_flow_test.dart
│   ├── user_list_flow_test.dart
│   └── checkout_flow_test.dart
├── helpers/
│   ├── test_driver.dart
│   ├── mock_server.dart
│   └── test_data.dart
└── fixtures/
    └── mock_responses.json
```

## Official Setup: IntegrationTestWidgetsFlutterBinding

**⚠️ OBLIGATORIO**: Sin `IntegrationTestWidgetsFlutterBinding.ensureInitialized()`, los tests en device real FALLAN.

### Qué Hace IntegrationTestWidgetsFlutterBinding

- Inicializa Flutter en **device REAL** (no solo emulador)
- Activa reporting de **performance** y timeline
- Permite `flutter drive` y **Firebase Test Lab**
- Configura tamaño de pantalla y simulación de dispositivo
- Sin esto: tests corren solo en emulador/desktop

### Setup Básico

```dart
// integration_test/app_test.dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:my_app/main.dart';

void main() {
  // 🔴 PRIMERO: Inicializar binding (ejecuta en device real)
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('App Integration Tests', () {
    testWidgets('Full app smoke test', (tester) async {
      // Inicializar la app
      await tester.binding.window.physicalSizeTestValue = Size(1080, 1920);
      addTearDown(tester.binding.window.clearPhysicalSizeTestValue);

      // Ejecutar la app
      await tester.pumpWidget(MyApp());
      
      // Tests aquí
    });
  });
}
```

### Comparación: Contextos de Ejecución

| Contexto | Binding | Comando | Dispositivo |
|----------|---------|---------|-------------|
| Emulador/Desktop | `flutter_test` | `flutter test integration_test/` | Virtual |
| **Device Real** | **IntegrationTestWidgetsFlutterBinding** | **`flutter drive`** | **Físico** |
| Firebase Test Lab | IntegrationTestWidgetsFlutterBinding | Firebase CLI | múltiples dispositivos |

### Ejecutar Tests

```bash
# Desktop/Emulador
flutter test integration_test/app_test.dart

# Device Real
flutter drive --target=integration_test/app_test.dart
```

## Testing de Flujos Críticos

### 1. Flujo de Autenticación

```dart
// integration_test/flows/login_flow_test.dart
void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Login Flow', () {
    testWidgets('Complete login flow with valid credentials', (tester) async {
      // Arrange - Inicializar app
      await tester.pumpWidget(MyApp());
      await tester.pumpAndSettle();

      // Verificar que estamos en login
      expect(find.byType(LoginPage), findsOneWidget);

      // Act 1 - Ingresar email
      await tester.enterText(
        find.byKey(Key('email_field')),
        'test@example.com',
      );
      await tester.pump();

      // Act 2 - Ingresar password
      await tester.enterText(
        find.byKey(Key('password_field')),
        'password123',
      );
      await tester.pump();

      // Act 3 - Presionar login
      await tester.tap(find.byKey(Key('login_button')));
      await tester.pumpAndSettle(Duration(seconds: 3));

      // Assert - Navegó a home
      expect(find.byType(HomePage), findsOneWidget);
      
      // Verificar que los datos del usuario se cargaron
      expect(find.text('Welcome, Test User'), findsOneWidget);
    });

    testWidgets('Show error on invalid credentials', (tester) async {
      // Arrange
      await tester.pumpWidget(MyApp());
      await tester.pumpAndSettle();

      // Act
      await tester.enterText(find.byKey(Key('email_field')), 'wrong@example.com');
      await tester.enterText(find.byKey(Key('password_field')), 'wrongpassword');
      await tester.tap(find.byKey(Key('login_button')));
      await tester.pumpAndSettle(Duration(seconds: 3));

      // Assert
      expect(find.text('Invalid credentials'), findsOneWidget);
      expect(find.byType(HomePage), findsNothing);  // No navegó
    });

    testWidgets('Handle network error gracefully', (tester) async {
      // Arrange - Simular desconexión
      // (Usando mock server o interceptor de HTTP)
      
      await tester.pumpWidget(MyApp());
      await tester.pumpAndSettle();

      // Act
      await tester.enterText(find.byKey(Key('email_field')), 'test@example.com');
      await tester.enterText(find.byKey(Key('password_field')), 'password123');
      await tester.tap(find.byKey(Key('login_button')));
      await tester.pumpAndSettle(Duration(seconds: 3));

      // Assert
      expect(find.text('Network error'), findsOneWidget);
      expect(find.byType(HomePage), findsNothing);
    });

    testWidgets('Show loading indicator while authenticating', (tester) async {
      // Arrange
      await tester.pumpWidget(MyApp());
      await tester.pumpAndSettle();

      // Act
      await tester.enterText(find.byKey(Key('email_field')), 'test@example.com');
      await tester.enterText(find.byKey(Key('password_field')), 'password123');
      await tester.tap(find.byKey(Key('login_button')));
      
      // Assert - Verificar loading durante 1-2 segundos
      expect(find.byType(CircularProgressIndicator), findsOneWidget);
      
      await tester.pumpAndSettle(Duration(seconds: 3));
      expect(find.byType(CircularProgressIndicator), findsNothing);
    });

    testWidgets('Logout flow', (tester) async {
      // Arrange - Login primeiro
      await tester.pumpWidget(MyApp());
      await tester.pumpAndSettle();
      
      // Login (asumiendo que estamos autenticados)
      await _performLogin(tester);

      // Act - Abrir menú
      await tester.tap(find.byKey(Key('menu_button')));
      await tester.pumpAndSettle();

      // Logout
      await tester.tap(find.byType(ListTile).at(3)); // Logout option
      await tester.pumpAndSettle();

      // Assert
      expect(find.byType(LoginPage), findsOneWidget);
    });
  });
}

Future<void> _performLogin(WidgetTester tester) async {
  await tester.enterText(find.byKey(Key('email_field')), 'test@example.com');
  await tester.enterText(find.byKey(Key('password_field')), 'password123');
  await tester.tap(find.byKey(Key('login_button')));
  await tester.pumpAndSettle(Duration(seconds: 3));
}
```

### 2. Flujo de Listado y Detalle

```dart
// integration_test/flows/user_list_flow_test.dart
void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('User List Flow', () {
    testWidgets('Navigate through user list and view details', (tester) async {
      // Arrange - Login y cargar app principal
      await tester.pumpWidget(MyApp());
      await tester.pumpAndSettle();
      // (asumir que llegamos a lista de usuarios)

      // Act 1 - Verificar lista cargó
      await tester.pumpAndSettle(Duration(seconds: 2));
      expect(find.byType(UserListTile), findsWidgets);

      // Act 2 - Scroll para encontrar usuario específico
      await tester.drag(find.byType(ListView), Offset(0, -300));
      await tester.pumpAndSettle();

      // Act 3 - Tap en usuario
      await tester.tap(find.byKey(Key('user-tile-123')).first);
      await tester.pumpAndSettle();

      // Assert - Navegó a detalle
      expect(find.byType(UserDetailPage), findsOneWidget);
      
      // Act 4 - Verificar datos del usuario
      expect(find.text('John Doe'), findsOneWidget);
      expect(find.text('john@example.com'), findsOneWidget);

      // Act 5 - Volver atrás
      await tester.pageBack();
      await tester.pumpAndSettle();

      // Assert
      expect(find.byType(UserListPage), findsOneWidget);
    });

    testWidgets('Search users and view results', (tester) async {
      // Arrange
      await tester.pumpWidget(MyApp());
      await tester.pumpAndSettle(Duration(seconds: 2));

      // Act - Tap en búsqueda
      await tester.tap(find.byKey(Key('search_button')));
      await tester.pumpAndSettle();

      // Escribir búsqueda
      await tester.enterText(
        find.byKey(Key('search_field')),
        'John',
      );
      await tester.pumpAndSettle(Duration(seconds: 2));

      // Assert
      expect(find.byType(UserListTile), findsWidgets);
      // Verificar que solo muestra usuarios que coinciden
      expect(find.text('Jane'), findsNothing);
    });

    testWidgets('Filter users by status', (tester) async {
      // Arrange
      await tester.pumpWidget(MyApp());
      await tester.pumpAndSettle(Duration(seconds: 2));

      // Act - Abrir filtros
      await tester.tap(find.byKey(Key('filter_button')));
      await tester.pumpAndSettle();

      // Seleccionar filtro "Active"
      await tester.tap(find.byKey(Key('filter-active')));
      await tester.pumpAndSettle(Duration(seconds: 2));

      // Assert
      // Verificar que solo se muestran usuarios activos
      expect(find.byType(UserListTile), findsWidgets);
    });
  });
}
```

### 3. Flujo de Formulario y Submit

```dart
// integration_test/flows/form_flow_test.dart
void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Form Submission Flow', () {
    testWidgets('Complete form with validation', (tester) async {
      // Arrange
      await tester.pumpWidget(MyApp());
      await tester.pumpAndSettle();

      // Navegar a formulario
      await tester.tap(find.byKey(Key('create-user-button')));
      await tester.pumpAndSettle();

      // Act 1 - Intentar submit sin datos
      await tester.tap(find.byKey(Key('submit_button')));
      await tester.pump();

      // Assert - Mostrar validaciones
      expect(find.text('Name is required'), findsOneWidget);
      expect(find.text('Email is required'), findsOneWidget);

      // Act 2 - Llenar formulario
      await tester.enterText(find.byKey(Key('name_field')), 'New User');
      await tester.enterText(find.byKey(Key('email_field')), 'newuser@example.com');
      await tester.enterText(find.byKey(Key('phone_field')), '1234567890');
      await tester.pump();

      // Assert - Sin errores de validación
      expect(find.text('Name is required'), findsNothing);

      // Act 3 - Submit
      await tester.tap(find.byKey(Key('submit_button')));
      await tester.pumpAndSettle(Duration(seconds: 3));

      // Assert - Éxito
      expect(find.text('User created successfully'), findsOneWidget);
      expect(find.byType(UserDetailPage), findsOneWidget);
    });

    testWidgets('Edit existing user', (tester) async {
      // Arrange - Navegar a usuario y entrar en edición
      await tester.pumpWidget(MyApp());
      await tester.pumpAndSettle();
      await _navigateToUserDetail(tester);

      // Act - Tap en edit
      await tester.tap(find.byKey(Key('edit_button')));
      await tester.pumpAndSettle();

      // Cambiar nombre
      await tester.enterText(find.byKey(Key('name_field')), 'Updated Name');
      await tester.pump();

      // Submit
      await tester.tap(find.byKey(Key('save_button')));
      await tester.pumpAndSettle(Duration(seconds: 2));

      // Assert
      expect(find.text('User updated successfully'), findsOneWidget);
      expect(find.text('Updated Name'), findsOneWidget);
    });
  });
}

Future<void> _navigateToUserDetail(WidgetTester tester) async {
  // Helper para navegar al detalle
  await tester.tap(find.byKey(Key('user-tile-123')).first);
  await tester.pumpAndSettle();
}
```

### 4. Flujo de Compra (E-commerce)

```dart
// integration_test/flows/checkout_flow_test.dart
void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Checkout Flow', () {
    testWidgets('Complete purchase with valid payment', (tester) async {
      // Arrange
      await tester.pumpWidget(MyApp());
      await tester.pumpAndSettle();

      // Act 1 - Navegar a productos
      await tester.tap(find.byKey(Key('products_tab')));
      await tester.pumpAndSettle();

      // Act 2 - Agregar producto al carrito
      await tester.tap(find.byKey(Key('add-product-001')));
      await tester.pump();
      expect(find.byType(SnackBar), findsOneWidget);

      // Act 3 - Abrir carrito
      await tester.tap(find.byKey(Key('cart_button')));
      await tester.pumpAndSettle();

      // Assert - Producto en carrito
      expect(find.text('Product Name'), findsOneWidget);
      expect(find.text('\$99.99'), findsOneWidget);

      // Act 4 - Checkout
      await tester.tap(find.byKey(Key('checkout_button')));
      await tester.pumpAndSettle();

      // Act 5 - Ingresar dirección
      await tester.enterText(
        find.byKey(Key('address_field')),
        '123 Main St, City, State 12345',
      );
      await tester.pump();

      // Act 6 - Seleccionar método de pago
      await tester.tap(find.byKey(Key('payment-credit-card')));
      await tester.pump();

      // Act 7 - Confirmación
      await tester.tap(find.byKey(Key('confirm_order_button')));
      await tester.pumpAndSettle(Duration(seconds: 4));

      // Assert - Pedido creado
      expect(find.byType(OrderConfirmationPage), findsOneWidget);
      expect(find.text('Order #12345'), findsOneWidget);
    });

    testWidgets('Handle payment failure', (tester) async {
      // Arrange - Similar al anterior pero con tarjeta rechazada
      // ...

      // Act - Procesar pago con tarjeta inválida
      // ...

      // Assert
      expect(find.text('Payment declined'), findsOneWidget);
      expect(find.byType(OrderConfirmationPage), findsNothing);
    });
  });
}
```

## Testing con Mock Server

```dart
// integration_test/helpers/mock_server.dart
import 'package:mocktail/mocktail.dart';

class MockHttpClient extends Mock implements HttpClient {}

void setupMockHttpServer() {
  // Configurar respuestas simuladas para rutas específicas
  // Ejemplo usando Mockito o similar
}

// En el test:
void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  setUpAll(() {
    setupMockHttpServer();
  });

  group('Integration Tests with Mock Server', () {
    testWidgets('...', (tester) async {
      // Los tests automáticamente usan el mock server
    });
  });
}
```

## Testing de Conectividad

```dart
void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Network Connectivity Tests', () {
    testWidgets('Show offline indicator when disconnected', (tester) async {
      // Arrange
      await tester.pumpWidget(MyApp());
      await tester.pumpAndSettle();

      // Simular desconexión (usando Connectivity plugin)
      // connectivity.simulateConnectionLost();

      // Act
      await tester.pumpAndSettle();

      // Assert
      expect(find.byType(OfflineBanner), findsOneWidget);
      expect(find.text('No internet connection'), findsOneWidget);
    });

    testWidgets('Recover after reconnecting', (tester) async {
      // Arrange - Desconectado
      // ...

      // Act - Reconectar
      // connectivity.simulateConnectionRestored();
      await tester.pumpAndSettle();

      // Assert - Banner desaparece
      expect(find.byType(OfflineBanner), findsNothing);
    });
  });
}
```

## Testing de Persistencia Local

```dart
void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Data Persistence Tests', () {
    testWidgets('Data persists after app restart', (tester) async {
      // Arrange
      await tester.pumpWidget(MyApp());
      await tester.pumpAndSettle();

      // Act 1 - Crear dato
      await tester.tap(find.byKey(Key('create_item_button')));
      await tester.pumpAndSettle();

      await tester.enterText(find.byKey(Key('item_name')), 'Test Item');
      await tester.tap(find.byKey(Key('save_button')));
      await tester.pumpAndSettle();

      // Act 2 - Cerrar app
      // (En integration test real, sería diferente)
      
      // Act 3 - Abrir app nuevamente
      await tester.pumpWidget(MyApp());
      await tester.pumpAndSettle();

      // Assert - Dato aún existe
      expect(find.text('Test Item'), findsOneWidget);
    });
  });
}
```

## Ejecutar Integration Tests

```bash
# Ejecutar todos los integration tests
flutter test integration_test/

# Ejecutar test específico
flutter test integration_test/flows/login_flow_test.dart

# Ejecutar en dispositivo real
flutter test integration_test/ -d <device-id>

# Ejecutar en emulador específico
flutter test integration_test/ -d emulator-5554

# Con tiempo de espera extendido
flutter test integration_test/ --timeout=60s
```

## Mejores Prácticas

### ✅ Hacer

- Pruebas de flujos críticos de negocio
- Datos de prueba aislados y limpios
- Helpers y utilities para casos comunes
- Independencia entre tests
- Logs detallados para debugging
- Uso de screenshots en caso de fallo

### ❌ Evitar

- Pruebas de UI no crítica (usar Widget Tests)
- Tests muy largos o complejos
- Dependencias entre tests
- Hardcodear tiempos (usar pumpAndSettle)
- Testear código de terceros

## Checklist de Integration Testing

- [ ] Flujos críticos de usuario cubiertos
- [ ] Casos de éxito y error contemplados
- [ ] Manejo de conectividad de red
- [ ] Persistencia de datos validada
- [ ] Navegación correcta
- [ ] Mensajes de error apropiados
- [ ] Performance aceptable
- [ ] Documentación de setup requerido
