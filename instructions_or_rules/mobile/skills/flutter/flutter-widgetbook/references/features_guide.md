# Features — Catalogar Pantallas del Proyecto

---

## Tabla de contenidos

1. [Cuándo catalogar una pantalla](#1-cuándo-catalogar-una-pantalla)
2. [Analizar la pantalla antes de generar](#2-analizar-la-pantalla-antes-de-generar)
3. [Aislar la pantalla de sus dependencias](#3-aislar-la-pantalla-de-sus-dependencias)
4. [Variantes de pantalla — estados a cubrir](#4-variantes-de-pantalla--estados-a-cubrir)
5. [Patrón completo de un feature use case](#5-patrón-completo-de-un-feature-use-case)
6. [Ubicación de archivos](#6-ubicación-de-archivos)
7. [Actualizar features existentes](#7-actualizar-features-existentes)

---

## 1. Cuándo catalogar una pantalla

| Situación | Acción |
|---|---|
| Se creó una nueva pantalla en el proyecto | Crear use case en `widgetbook_[appname]/lib/features/` |
| Se modificó una pantalla existente (nuevos campos, estados, layout) | Actualizar el use case existente |
| Se quiere documentar todas las pantallas del proyecto | Escanear `lib/features/` o `lib/screens/` y crear use cases faltantes |
| El usuario pide "agrega esta pantalla al widgetbook" | Crear use case para esa pantalla |

---

## 2. Analizar la pantalla antes de generar

Antes de escribir código, leer la pantalla completa e identificar:

### 2.1 — Dependencias a mockear

| Tipo de dependencia | Qué buscar | Cómo mockear |
|---|---|---|
| **State management** | `Provider`, `Bloc`, `Cubit`, `Riverpod`, `GetX` | Wrapper con datos mock |
| **Servicios/Repositorios** | Inyección de dependencias, `GetIt`, constructores | Instancia mock en el use case |
| **Navegación** | `Navigator.push`, `GoRouter`, `AutoRoute` | Callbacks con `print()` — no navegar |
| **API/Network** | `http`, `dio`, llamadas a backend | Datos hardcodeados del dominio |
| **Local storage** | `SharedPreferences`, `Hive`, `SQLite` | Datos mock inline |
| **Auth** | Token, user session, permisos | Mock de usuario autenticado |

### 2.2 — Estados visibles de la pantalla

Identificar todos los estados que la pantalla puede mostrar:

```
¿Tiene estado de carga? → variante 'loading'
¿Tiene estado vacío (sin datos)? → variante 'empty'
¿Tiene estado de error? → variante 'error'
¿Tiene estado de éxito/confirmación? → variante 'success'
¿Tiene variante para usuario nuevo? → variante 'first_time'
¿Tiene variante para usuario no autenticado? → variante 'logged_out'
¿Tiene variante con datos completos? → variante 'default' (siempre)
```

### 2.3 — Parámetros configurables con knobs

No todas las pantallas tienen parámetros explícitos como un componente.
Identificar qué se puede controlar desde knobs:

- **Datos del usuario** (nombre, avatar, rol)
- **Cantidad de items** en listas
- **Estado de formularios** (vacío, con errores, completo)
- **Flags de feature** (mostrar/ocultar secciones)
- **Permisos** (admin vs usuario normal)

---

## 3. Aislar la pantalla de sus dependencias

**Regla fundamental:** la pantalla debe renderizarse de forma aislada en Widgetbook,
sin depender del árbol de widgets real de la app, ni de navegación, ni de servicios remotos.

### 3.1 — Patrón: wrapper de providers

```dart
// Cuando la pantalla necesita providers del árbol
@UseCase(name: 'default', type: HomeScreen)
Widget buildHomeScreenUseCase(BuildContext context) {
  final userName = context.knobs.string(
    label: 'userName',
    initialValue: 'María García',
  );

  // Mock de los providers que la pantalla necesita
  return MockAppProviders(
    user: User(name: userName, email: 'maria@ejemplo.com'),
    products: _mockProducts,
    child: const HomeScreen(),
  );
}
```

### 3.2 — Patrón: inyección por constructor

```dart
// Si la pantalla acepta datos por constructor (preferido)
@UseCase(name: 'default', type: ProductDetailScreen)
Widget buildProductDetailScreenUseCase(BuildContext context) {
  return ProductDetailScreen(
    product: Product(
      id: 'PRD-001',
      name: context.knobs.string(label: 'productName', initialValue: 'Zapatillas Trail X3'),
      price: context.knobs.double.input(label: 'price', initialValue: 129.90),
      description: 'Zapatillas de trail running con suela Vibram y amortiguación premium.',
      imageUrl: 'https://picsum.photos/400/300?random=1',
      stock: context.knobs.int.slider(label: 'stock', initialValue: 15, min: 0, max: 100),
    ),
    onAddToCart: () => print('Product PRD-001 added to cart'),
    onBack: () => print('Navigate back'),
  );
}
```

### 3.3 — Patrón: reemplazar navegación con callbacks

```dart
// ❌ No hacer — depende de navegación real
onTap: () => Navigator.pushNamed(context, '/detail', arguments: item),

// ✅ Hacer — print descriptivo sin navegar
onTap: () => print('Navigate to detail: ${item.id} - ${item.name}'),
```

### 3.4 — Patrón: mock de Bloc/Cubit

```dart
@UseCase(name: 'default', type: OrderListScreen)
Widget buildOrderListScreenUseCase(BuildContext context) {
  return BlocProvider<OrderListCubit>.value(
    value: MockOrderListCubit(
      state: OrderListState.loaded(
        orders: _mockOrders,
      ),
    ),
    child: const OrderListScreen(),
  );
}

@UseCase(name: 'loading', type: OrderListScreen)
Widget buildOrderListScreenLoadingUseCase(BuildContext context) {
  return BlocProvider<OrderListCubit>.value(
    value: MockOrderListCubit(
      state: const OrderListState.loading(),
    ),
    child: const OrderListScreen(),
  );
}

@UseCase(name: 'empty', type: OrderListScreen)
Widget buildOrderListScreenEmptyUseCase(BuildContext context) {
  return BlocProvider<OrderListCubit>.value(
    value: MockOrderListCubit(
      state: const OrderListState.loaded(orders: []),
    ),
    child: const OrderListScreen(),
  );
}

@UseCase(name: 'error', type: OrderListScreen)
Widget buildOrderListScreenErrorUseCase(BuildContext context) {
  return BlocProvider<OrderListCubit>.value(
    value: MockOrderListCubit(
      state: const OrderListState.error(message: 'No se pudieron cargar las órdenes'),
    ),
    child: const OrderListScreen(),
  );
}
```

---

## 4. Variantes de pantalla — estados a cubrir

### Regla general para pantallas

| Estado | `name` sugerido | Cuándo incluirlo |
|---|---|---|
| Pantalla con datos completos | `'default'` | Siempre |
| Cargando datos del servidor | `'loading'` | Si la pantalla tiene fetch inicial |
| Sin datos / lista vacía | `'empty'` | Si la pantalla puede no tener contenido |
| Error de carga / red | `'error'` | Si la pantalla maneja errores |
| Formulario con errores de validación | `'validation_error'` | Si tiene formularios |
| Usuario no autenticado | `'logged_out'` | Si tiene contenido condicional por auth |
| Primera vez / onboarding | `'first_time'` | Si tiene flujo de primer uso |
| Datos máximos / saturación | `'full'` | Si la UI puede saturarse con muchos datos |

### Estrategia por tipo de pantalla

**Pantalla de listado (home, catálogo, historial):**
```
default     → lista con 10-20 items realistas
loading     → skeleton / shimmer / spinner
empty       → estado vacío con mensaje e ilustración
error       → error de red con botón de retry
```

**Pantalla de detalle (producto, perfil, orden):**
```
default     → todos los datos completos
loading     → cargando datos del item
error       → item no encontrado o error de red
```

**Pantalla de formulario (login, registro, checkout):**
```
default          → formulario vacío listo para llenar
validation_error → campos con errores de validación visibles
prefilled        → formulario con datos precargados (edición)
```

**Pantalla de auth (login, registro, recuperar contraseña):**
```
default     → formulario limpio
error       → credenciales inválidas / error de servidor
loading     → procesando autenticación
```

**Dashboard / pantalla principal:**
```
default     → datos cargados con métricas/resumen
loading     → cargando datos iniciales
empty       → usuario nuevo sin actividad
```

---

## 5. Patrón completo de un feature use case

```dart
// widgetbook_[appname]/lib/features/auth/login_screen/login_screen.use_case.dart

import 'package:flutter/material.dart';
import 'package:widgetbook/widgetbook.dart';
import 'package:widgetbook_annotation/widgetbook_annotation.dart';
import 'package:your_app/features/auth/presentation/login_screen.dart';
import '../../../shared/code_preview_addon.dart';

@UseCase(name: 'default', type: LoginScreen)
Widget buildLoginScreenUseCase(BuildContext context) {
  context.setCodePreview('''
LoginScreen(
  onLogin: (email, password) { /* handle login */ },
  onForgotPassword: () { /* navigate */ },
  onRegister: () { /* navigate */ },
)''');

  return LoginScreen(
    onLogin: (email, password) => print('Login attempt: $email'),
    onForgotPassword: () => print('Navigate to forgot password'),
    onRegister: () => print('Navigate to register'),
  );
}

@UseCase(name: 'error', type: LoginScreen)
Widget buildLoginScreenErrorUseCase(BuildContext context) {
  final errorMessage = context.knobs.string(
    label: 'errorMessage',
    initialValue: 'Credenciales inválidas. Verifica tu email y contraseña.',
  );

  context.setCodePreview('''
LoginScreen(
  initialError: '$errorMessage',
  onLogin: (email, password) { /* handle retry */ },
  onForgotPassword: () { /* navigate */ },
  onRegister: () { /* navigate */ },
)''');

  return LoginScreen(
    initialError: errorMessage,
    onLogin: (email, password) => print('Login retry: $email'),
    onForgotPassword: () => print('Navigate to forgot password'),
    onRegister: () => print('Navigate to register'),
  );
}

@UseCase(name: 'loading', type: LoginScreen)
Widget buildLoginScreenLoadingUseCase(BuildContext context) {
  context.setCodePreview('''
LoginScreen(
  isLoading: true,
  onLogin: (email, password) { /* handle login */ },
  onForgotPassword: () { /* navigate */ },
  onRegister: () { /* navigate */ },
)''');

  return LoginScreen(
    isLoading: true,
    onLogin: (email, password) => print('Login in progress'),
    onForgotPassword: () => print('Navigate to forgot password'),
    onRegister: () => print('Navigate to register'),
  );
}
```

---

## 6. Ubicación de archivos

### Regla: espejar la estructura de features del proyecto principal

Buscar la estructura de features en el proyecto principal y replicarla
en `widgetbook_[appname]/lib/features/`:

**Proyecto principal:**
```
lib/features/
├── auth/
│   ├── login_screen.dart
│   └── register_screen.dart
├── home/
│   └── home_screen.dart
└── profile/
    └── profile_screen.dart
```

**Widgetbook (espejo):**
```
widgetbook_[appname]/lib/
├── ui_system/          ← componentes (ver project_structure.md)
├── features/           ← pantallas (espejar del proyecto)
│   ├── auth/
│   │   ├── login_screen/
│   │   │   └── login_screen.use_case.dart
│   │   └── register_screen/
│   │       └── register_screen.use_case.dart
│   ├── home/
│   │   └── home_screen/
│   │       └── home_screen.use_case.dart
│   └── profile/
│       └── profile_screen/
│           └── profile_screen.use_case.dart
└── shared/
```

### Detectar pantallas en el proyecto

Buscar archivos que terminen en `_screen.dart`, `_page.dart` o `_view.dart`
en el proyecto principal:

```
lib/features/**/      → pantallas por feature
lib/screens/          → carpeta plana de pantallas
lib/pages/            → carpeta plana de páginas
lib/presentation/     → capa de presentación (Clean Architecture)
```

---

## 7. Actualizar features existentes

Cuando una pantalla del proyecto cambia y ya tiene use case en Widgetbook:

1. **Leer la pantalla actualizada** — identificar qué cambió: nuevos campos, estados, layout, dependencias.
2. **Comparar con el use case existente** — verificar si los knobs, mocks y variantes siguen siendo correctos.
3. **Actualizar lo necesario:**
   - Nuevo parámetro → agregar knob o mock correspondiente
   - Nuevo estado visual → agregar variante
   - Dependencia eliminada → remover mock
   - Cambio de modelo de datos → actualizar datos mock
4. **Regenerar** — ejecutar `dart run build_runner build --delete-conflicting-outputs`

### Señales de que un use case necesita actualización

- La pantalla tiene parámetros que no están en el use case
- El use case usa modelos con campos que ya no existen
- La pantalla tiene estados nuevos no cubiertos por variantes
- Los providers/blocs del use case no coinciden con los actuales
