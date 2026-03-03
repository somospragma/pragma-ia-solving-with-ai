# Knobs Reference — Widgetbook 3.x

Guía de selección de knobs por tipo de parámetro.

---

## Regla de selección rápida

| Tipo de parámetro | Knob a usar |
|---|---|
| `String` requerido | `context.knobs.string` |
| `String?` opcional | `context.knobs.stringOrNull` |
| `bool` requerido | `context.knobs.boolean` |
| `bool?` opcional | `context.knobs.booleanOrNull` |
| `int` acotado (progreso, tamaño) | `context.knobs.int.slider` |
| `int` libre | `context.knobs.int.input` |
| `double` entre 0.0 y 1.0 (opacidad) | `context.knobs.double.slider` |
| `double` libre | `context.knobs.double.input` |
| `Color` | `context.knobs.color` |
| `Color?` | `context.knobs.colorOrNull` |
| `enum` / lista de opciones | `context.knobs.list` |
| `DateTime` | `context.knobs.dateTime` |
| `Duration` | `context.knobs.duration` |
| `IconData` | `context.knobs.list` con `Icons.*` |
| Asset image (`String` path PNG/JPEG) | Hardcodear path + assets declarados en pubspec |
| SVG (`String` path) | Hardcodear path + assets declarados en pubspec |
| `ImageProvider` | `NetworkImage` (catálogo) o `AssetImage` (si assets declarados) |
| Objeto complejo | Hardcodear + `// TODO` |
| Callback | `print()` descriptivo |

---

## API completa

### String
```dart
context.knobs.string(label: 'text', initialValue: 'Hello World')
context.knobs.stringOrNull(label: 'subtitle', initialValue: null)
```

### Boolean
```dart
context.knobs.boolean(label: 'enabled', initialValue: true)
context.knobs.booleanOrNull(label: 'showBadge', initialValue: null)
```

### Integer
```dart
// Valor acotado con slider
context.knobs.int.slider(
  label: 'progress',
  initialValue: 50,
  min: 0,
  max: 100,
  divisions: 10,
)

// Valor libre con input
context.knobs.int.input(label: 'itemCount', initialValue: 5)

// Opcionales
context.knobs.intOrNull.input(label: 'maxLines', initialValue: null)
context.knobs.intOrNull.slider(
  label: 'steps',
  initialValue: null,
  min: 0,
  max: 10,
  divisions: 10,
)
```

### Double
```dart
// Slider para valores entre 0.0 y 1.0
context.knobs.double.slider(
  label: 'opacity',
  initialValue: 1.0,
  min: 0.0,
  max: 1.0,
  divisions: 20,
)

// Input para valores libres
context.knobs.double.input(label: 'elevation', initialValue: 4.0)

// Opcionales
context.knobs.doubleOrNull.input(label: 'borderWidth', initialValue: null)
context.knobs.doubleOrNull.slider(
  label: 'scale',
  initialValue: null,
  min: 0.5,
  max: 2.0,
  divisions: 15,
)
```

### Color
```dart
context.knobs.color(label: 'backgroundColor', initialValue: Colors.blue)
context.knobs.colorOrNull(label: 'borderColor', initialValue: null)
```

### Lista / Enum
```dart
context.knobs.list<TextAlign>(
  label: 'textAlign',
  initialOption: TextAlign.center,
  options: TextAlign.values,
  labelBuilder: (value) => value.name,
)

// Enum parcial (no todos los valores)
context.knobs.list<ButtonSize>(
  label: 'size',
  initialOption: ButtonSize.medium,
  options: [ButtonSize.small, ButtonSize.medium, ButtonSize.large],
  labelBuilder: (value) => value.name,
)
```

### DateTime
```dart
context.knobs.dateTime(
  label: 'selectedDate',
  initialValue: DateTime.now(),
  start: DateTime.now().subtract(const Duration(days: 365)),
  end: DateTime.now().add(const Duration(days: 365)),
)
```

### Duration
```dart
context.knobs.duration(
  label: 'animationDuration',
  initialValue: const Duration(milliseconds: 300),
)
```

---

## Iconos e imágenes

> **Requisito previo:** Para que cualquier asset (PNG, JPEG, SVG) se cargue correctamente
> en Widgetbook, los paths deben estar declarados en `widgetbook_[appname]/pubspec.yaml`.
> Ver `references/setup.md` § Assets — imágenes e iconos del proyecto.

### IconData — seleccionar icono con knob

`IconData` no tiene knob nativo: usar `context.knobs.list` con un conjunto curado
de iconos relevantes para el componente. Nunca intentar exponer todos los `Icons.*`.

```dart
// Seleccionar entre iconos relevantes para el caso de uso
final icon = context.knobs.list<IconData>(
  label: 'icon',
  initialOption: Icons.star,
  options: [
    Icons.star,
    Icons.favorite,
    Icons.bookmark,
    Icons.check_circle,
    Icons.info,
    Icons.warning,
  ],
  labelBuilder: (icon) {
    const names = {
      Icons.star: 'star',
      Icons.favorite: 'favorite',
      Icons.bookmark: 'bookmark',
      Icons.check_circle: 'check_circle',
      Icons.info: 'info',
      Icons.warning: 'warning',
    };
    return names[icon] ?? 'icon';
  },
);
```

> **Seleccionar iconos del dominio:** Elegir los iconos que el widget realmente usará
> en producción — no una lista genérica. Si el widget siempre muestra el mismo icono,
> hardcodearlo directamente (`icon: Icons.arrow_forward`) sin knob.

### Widget icono — hardcodear sin knob

Si el parámetro es `Widget` y el widget siempre recibe un icono concreto:

```dart
// Parámetro: Widget? leadingIcon
leadingIcon: const Icon(Icons.notifications, size: 24),

// Parámetro: Widget? trailingIcon  
trailingIcon: const Icon(Icons.chevron_right, size: 20),
```

### Asset PNG / JPEG — usar path con assets declarados

Cuando el parámetro es un `String` con la ruta del asset:

```dart
// Hardcodear un path real del proyecto
// El asset DEBE estar declarado en widgetbook_[appname]/pubspec.yaml
imagePath: 'assets/images/product_placeholder.png',

// Si el componente acepta el Widget directamente:
image: Image.asset(
  'assets/images/product_placeholder.png',
  fit: BoxFit.cover,
),
```

### Asset SVG — usar path con assets declarados

Si el proyecto usa `flutter_svg`:

```dart
// Hardcodear path del SVG real del proyecto
// El asset DEBE estar declarado en widgetbook_[appname]/pubspec.yaml
iconPath: 'assets/icons/ic_home.svg',

// Si el componente recibe el Widget directamente:
icon: SvgPicture.asset(
  'assets/icons/ic_home.svg',
  width: 24,
  height: 24,
),

// Con knob para alternar entre varios SVGs del proyecto
final iconPath = context.knobs.list<String>(
  label: 'icon',
  initialOption: 'assets/icons/ic_home.svg',
  options: [
    'assets/icons/ic_home.svg',
    'assets/icons/ic_profile.svg',
    'assets/icons/ic_settings.svg',
  ],
  labelBuilder: (path) => path.split('/').last.replaceAll('.svg', ''),
);
// Uso:
SvgPicture.asset(iconPath, width: 24, height: 24)
```

### ImageProvider — preferir NetworkImage en el catálogo

Cuando el parámetro es `ImageProvider` o `String` URL de red, usar `NetworkImage`
para el catálogo: no requiere declarar assets y siempre muestra una imagen real.

```dart
// NetworkImage — no requiere configurar assets
avatarImage: const NetworkImage('https://picsum.photos/200'),

// Con knob para cambiar entre variantes de imagen de red
final imageUrl = context.knobs.list<String>(
  label: 'image',
  initialOption: 'https://picsum.photos/400/300?random=1',
  options: [
    'https://picsum.photos/400/300?random=1',
    'https://picsum.photos/400/300?random=2',
    'https://picsum.photos/400/300?random=3',
  ],
  labelBuilder: (url) => 'Imagen ${url.split('random=').last}',
);
// Uso:
Image.network(imageUrl, fit: BoxFit.cover)
```

### Regla de decisión — ¿asset o network?

| Situación | Estrategia |
|---|---|
| El componente carga imágenes desde URL (avatar, producto) | `NetworkImage` o `Image.network` |
| El componente usa assets del proyecto (íconos, ilustraciones) | Asset path + declarar en pubspec |
| El SVG es un ícono del design system | Asset path + declarar en pubspec |
| Se quiere alternar entre múltiples imágenes con knob | `context.knobs.list<String>` con paths o URLs |
| El parámetro es opcional (`ImageProvider?`) | `null` si no es relevante para la variante |

### Objeto complejo — hardcodear con TODO
```dart
// Cuando el tipo no es mappeable a un knob simple
final config = CardConfiguration(
  borderRadius: 12.0,
  elevation: 4.0,
  padding: const EdgeInsets.all(16),
); // TODO: configurar CardConfiguration manualmente según necesidad
```

### Callbacks — siempre con print descriptivo
```dart
// Simple
onPressed: () => print('Button pressed'),

// Con dato
onChanged: (value) => print('Value changed: $value'),

// Con objeto
onItemSelected: (item) => print('Item selected: ${item.id} - ${item.name}'),

// Async
onSave: () async {
  print('Save started');
  await Future.delayed(const Duration(seconds: 1));
  print('Save completed');
},
```

### State management — mock provider con datos del dominio

Los datos del mock deben reflejar el dominio real del proyecto — nunca usar
valores genéricos como "test", "lorem ipsum" o datos placeholder.
Antes de crear el mock, revisar los modelos del proyecto para usar campos
y valores coherentes.

```dart
// ✅ Mock contextualizado al dominio (e-commerce)
@UseCase(name: 'with_data', type: OrderSummaryWidget)
Widget buildOrderSummaryWidgetWithDataUseCase(BuildContext context) {
  return MockOrderProvider(
    order: Order(
      id: 'ORD-2024-1587',
      customerName: 'María García López',
      items: [
        OrderItem(name: 'Camiseta Running Pro', quantity: 2, price: 49.99),
        OrderItem(name: 'Zapatillas Trail X3', quantity: 1, price: 129.90),
      ],
      total: 229.88,
      status: OrderStatus.pending,
    ), // TODO: ajustar campos según el modelo real del proyecto
    child: OrderSummaryWidget(
      onConfirm: () => print('Order ORD-2024-1587 confirmed'),
    ),
  );
}

// ❌ Mock genérico — no hacer esto
return MockOrderProvider(
  order: Order.mock(), // datos vacíos o placeholder
  child: OrderSummaryWidget(onConfirm: () => print('confirmed')),
);
```
