# Mocking de dependencias

Catalogar un widget que tiene dependencias externas (providers, servicios, repositorios) requiere una estrategia explícita. Hay dos enfoques; elegir según el tipo de widget.

## Cuándo usar cada enfoque

| Situación | Enfoque |
|---|---|
| El widget recibe datos como parámetros pero internamente consulta un provider | **Extracción** — extraer la dependencia a un parámetro |
| El widget es una *pantalla completa* que consume providers y no se puede refactorizar | **Mocking con librería** — inyectar el provider mockeado en el árbol |
| El widget es un componente reutilizable simple | **Hardcodear valores** directo en el use case (sin provider) |

---

## Enfoque I: Extracción

La forma más sencilla: extraer la dependencia al constructor del widget y pasarla directamente en el use case. Cambia el árbol del widget pero hace el componente más testeable y portable.

**Widget original (con dependencia interna):**
```dart
class UserTile extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Consumer<UserProvider>(
      builder: (context, provider, child) => Text(provider.user),
    );
  }
}
```

**Widget refactorizado (dependencia extraída):**
```dart
class UserTile extends StatelessWidget {
  const UserTile({super.key, required this.user});
  final String user;

  @override
  Widget build(BuildContext context) => Text(user);
}
```

**Use case con extracción:**
```dart
@UseCase(name: 'default', type: UserTile)
Widget buildUserTileUseCase(BuildContext context) {
  final user = context.knobs.string(label: 'user', initialValue: 'Ana García');

  context.setCodePreview('''
UserTile(
  user: '\$user',
)''');

  return UserTile(user: user);
}
```

**Árbol resultante en Widgetbook:**
```
WidgetbookApp
└── UserTile
    └── Text
```

---

## Enfoque II: Mocking con librería (mocktail)

Cuando el widget es una pantalla completa que depende de providers y no es viable refactorizarla, inyectar el provider mockeado directamente en el árbol del use case.

### Paso 1 — Agregar `mocktail` al `pubspec.yaml` del widgetbook

```yaml
dependencies:
  # ...
  mocktail: ^1.0.0
```

> `mocktail` va en `dependencies` (no `dev_dependencies`) porque el widgetbook completo es una herramienta de desarrollo; no se incluye en el build de producción de la app.

### Paso 2 — Crear el mock y usarlo en el use case

```dart
import 'package:flutter/material.dart';
import 'package:mocktail/mocktail.dart';
import 'package:provider/provider.dart';
import 'package:widgetbook/widgetbook.dart';
import 'package:widgetbook_annotation/widgetbook_annotation.dart';
import 'package:my_app/features/home/home_screen.dart';
import 'package:my_app/providers/user_provider.dart';
import '../../../shared/code_preview_addon.dart';

// Mock definido a nivel de archivo (fuera del use case)
class MockUserProvider extends Mock implements UserProvider {}

@UseCase(name: 'default', type: HomeScreen)
Widget buildHomeScreenUseCase(BuildContext context) {
  final userName = context.knobs.string(label: 'userName', initialValue: 'Ana García');
  final isAuthenticated = context.knobs.boolean(label: 'isAuthenticated', initialValue: true);

  context.setCodePreview('''
HomeScreen()''');

  return ChangeNotifierProvider<UserProvider>(
    create: (_) {
      final provider = MockUserProvider();
      when(() => provider.user).thenReturn(userName);
      when(() => provider.isAuthenticated).thenReturn(isAuthenticated);
      return provider;
    },
    child: const HomeScreen(),
  );
}
```

**Árbol resultante en Widgetbook:**
```
WidgetbookApp
└── MockUserProvider     ← provider mockeado inyectado por el use case
    └── HomeScreen
        └── Consumer<UserProvider>
            └── Text
```

---

## Mocking de múltiples dependencias

Cuando una pantalla depende de varios providers, apilarlos con `MultiProvider`:

```dart
class MockAuthProvider extends Mock implements AuthProvider {}
class MockCartProvider extends Mock implements CartProvider {}

@UseCase(name: 'default', type: CheckoutScreen)
Widget buildCheckoutScreenUseCase(BuildContext context) {
  final userName = context.knobs.string(label: 'userName', initialValue: 'Carlos López');
  final itemCount = context.knobs.int.input(label: 'itemCount', initialValue: 3);
  final total = context.knobs.double.input(label: 'total', initialValue: 129.99);

  context.setCodePreview('''
CheckoutScreen()''');

  return MultiProvider(
    providers: [
      ChangeNotifierProvider<AuthProvider>(
        create: (_) {
          final auth = MockAuthProvider();
          when(() => auth.userName).thenReturn(userName);
          return auth;
        },
      ),
      ChangeNotifierProvider<CartProvider>(
        create: (_) {
          final cart = MockCartProvider();
          when(() => cart.itemCount).thenReturn(itemCount);
          when(() => cart.total).thenReturn(total);
          return cart;
        },
      ),
    ],
    child: const CheckoutScreen(),
  );
}
```

---

## Mocking de repositorios y servicios (sin provider)

Para widgets que inyectan repositorios o servicios directamente por constructor:

```dart
class MockProductRepository extends Mock implements ProductRepository {}

@UseCase(name: 'default', type: ProductDetailScreen)
Widget buildProductDetailScreenUseCase(BuildContext context) {
  final title = context.knobs.string(label: 'title', initialValue: 'Zapatillas Runner Pro');
  final price = context.knobs.double.input(label: 'price', initialValue: 89.99);

  final repo = MockProductRepository();
  when(() => repo.getProduct(any())).thenAnswer(
    (_) async => Product(title: title, price: price),
  );

  context.setCodePreview('''
ProductDetailScreen(
  repository: repository,
  productId: '123',
)''');

  return ProductDetailScreen(
    repository: repo,
    productId: '123',
  );
}
```

---

## Reglas

- Los mocks se declaran **a nivel de archivo**, fuera del método del use case, para que sean reutilizables entre variantes del mismo widget.
- Usar `when(() => mock.property).thenReturn(value)` para stubear propiedades síncronas.
- Usar `when(() => mock.method(any())).thenAnswer((_) async => value)` para métodos async.
- Los valores stubeados **deben estar conectados a knobs** siempre que sean útiles para exploración interactiva.
- Nunca depender del árbol real de la app ni de providers registrados globalmente — el use case debe ser completamente autónomo.
- `mocktail` va en `dependencies` (no `dev_dependencies`) del `widgetbook_[appname]/pubspec.yaml`.
