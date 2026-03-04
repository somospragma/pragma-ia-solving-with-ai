# Variantes — Cuántas y Cuáles Generar

---

## Regla general

### UI System (componentes)

| Complejidad del widget | Variantes mínimas |
|---|---|
| Atom simple (botón, badge, icono) | 2-4 |
| Molecule (card, list tile) | 2-3 |
| Organism (form, list) | 2-3 |
| Widget con muchos estados | Una por estado relevante |

### Features (pantallas)

| Tipo de pantalla | Variantes mínimas |
|---|---|
| Listado (home, catálogo, historial) | 3-4: default, loading, empty, error |
| Detalle (producto, perfil, orden) | 2-3: default, loading, error |
| Formulario (login, registro, checkout) | 2-3: default, validation_error, prefilled |
| Dashboard / resumen | 2-3: default, loading, empty |

Para la guía completa de variantes de pantallas, ver `references/features_guide.md`.

Más variantes no siempre es mejor — cada una debe demostrar algo
que las otras no muestran.

---

## Estados que siempre hay que cubrir (si el widget los tiene)

> **Regla de implementación:** si el estado se controla con un parámetro del constructor (`isLoading`, `isEnabled`, `isEmpty`...) → **knob**. Solo crear un `@UseCase` separado si el widget renderiza una estructura visual diferente que no puede controlarse con un parámetro.

| Estado | `name` si es `@UseCase` | Knob equivalente | Implementación preferida |
|---|---|---|---|
| Estado base funcional | `'default'` | — | `@UseCase` siempre |
| Cargando datos | `'loading'` | `context.knobs.boolean(label: 'Loading')` | **Knob** si hay un prop `isLoading` |
| Deshabilitado | `'disabled'` | `context.knobs.boolean(label: 'Enabled')` | **Knob** si hay un prop `isEnabled` / `enabled` |
| Sin datos / vacío | `'empty'` | `context.knobs.boolean(label: 'Empty')` | **Knob** si el widget acepta lista vacía o nullable |
| Error | `'error'` | `context.knobs.boolean(label: 'Error')` | **Knob** si hay un prop `hasError` / `errorMessage` |
| Con contenido máximo | `'full'` | `context.knobs.int.slider(label: 'itemCount')` | **Knob** con valor alto en el slider |
| Solo lectura | `'read_only'` | `context.knobs.boolean(label: 'ReadOnly')` | **Knob** si hay un prop `readOnly` |

---

## Estrategia por tipo de componente

### Botones

> **Regla:** Un único `@UseCase(name: 'default')` con knobs para todos los estados y variantes visuales. Solo crear `@UseCase` adicionales si el widget renderiza estructuras radicalmente distintas (ver Regla de oro más abajo).

```dart
// default — un use case, con knobs:
//   - label/text (string)
//   - variant (list<ButtonVariant>)  ← primary, secondary, ghost, destructive…
//   - size (list<ButtonSize>)        ← small, normal, large…
//   - icon (list<IconData>)
//   - iconPosition (list<IconPosition>) ← start, end
//   - showIcon (boolean)
//   - isLoading (boolean)            ← NO crear @UseCase 'loading' aparte
//   - isEnabled (boolean)            ← NO crear @UseCase 'disabled' aparte
```

### Campos de texto / inputs
```dart
// default   — campo vacío interactivo
// with_value — campo con contenido
// error      — mostrando mensaje de error
// disabled   — no editable
```

### Cards / List tiles
```dart
// default    — con datos completos
// minimal    — con solo los campos requeridos
// loading    — skeleton o shimmer (si aplica)
```

### Listas
```dart
// with_data   — lista con N items (usar List.generate para volumen realista)
// empty       — sin items, estado vacío
// loading     — estado de carga
```

### Formularios
```dart
// default     — campos vacíos
// with_errors — validación activada con errores visibles
// prefilled   — campos con datos de ejemplo
```

---

## Regla de oro: knobs primero, variantes solo cuando hay diferencia estructural

> **Un `@UseCase` separado solo se justifica cuando el widget renderiza una estructura visual fundamentalmente diferente que no puede controlarse con un knob.**

| Situación | Decisión |
|---|---|
| Estado `loading`, `disabled`, `showIcon`, posición del ícono... | **Knob** — el mismo widget, solo cambia un parámetro |
| Variante visual del componente (`primary`, `secondary`, `ghost`...) | **Knob `list<Enum>`** — el mismo widget con una prop distinta |
| El widget renderiza una estructura completamente diferente (ej. progress bar activa vs ícono) | **`@UseCase` separado** |

### ✅ Patrón correcto para botones — una variante, todos los estados como knobs

Todos los estados (loading, disabled) **y** los tipos visuales (primary, secondary...) se exponen como knobs dentro de un único `@UseCase`:

```dart
@UseCase(name: 'default', type: AppButton)
Widget buildAppButtonUseCase(BuildContext context) {
  // Knobs de contenido
  final label = context.knobs.string(label: 'Text', initialValue: 'Continuar');

  // Knob de variante visual — dropdown con todos los tipos del enum
  final variant = context.knobs.list<ButtonVariant>(
    label: 'Variant',
    initialOption: ButtonVariant.primary,
    options: ButtonVariant.values,
    labelBuilder: (v) => v.name,
  );

  // Knobs de tamaño y comportamiento
  final size = context.knobs.list<ButtonSize>(
    label: 'Size',
    initialOption: ButtonSize.normal,
    options: ButtonSize.values,
    labelBuilder: (v) => v.name,
  );

  // Knobs del ícono
  final icon = context.knobs.list<IconData>(
    label: 'Icon',
    initialOption: Icons.balance,
    options: [Icons.balance, Icons.star, Icons.favorite, Icons.check_circle],
    labelBuilder: (i) => {
      Icons.balance: 'balance',
      Icons.star: 'star',
      Icons.favorite: 'favorite',
      Icons.check_circle: 'check_circle',
    }[i] ?? 'icon',
  );

  final iconPosition = context.knobs.list<IconPosition>(
    label: 'Icon position',
    initialOption: IconPosition.start,
    options: IconPosition.values,
    labelBuilder: (p) => p.name,
  );

  // Knobs de estado — NO crear @UseCase separados para estos
  final showIcon = context.knobs.boolean(label: 'Show icon', initialValue: true);
  final isLoading = context.knobs.boolean(label: 'Loading', initialValue: false);
  final isEnabled = context.knobs.boolean(label: 'Enabled', initialValue: true);

  context.setCodePreview('''
AppButton(
  label: '$label',
  variant: ButtonVariant.${variant.name},
  size: ButtonSize.${size.name},
  icon: Icons.${icon.toString().split('.').last},
  iconPosition: IconPosition.${iconPosition.name},
  showIcon: $showIcon,
  isLoading: $isLoading,
  isEnabled: $isEnabled,
  onPressed: () {},
)''');

  return AppButton(
    label: label,
    variant: variant,
    size: size,
    icon: icon,
    iconPosition: iconPosition,
    showIcon: showIcon,
    isLoading: isLoading,
    isEnabled: isEnabled,
    onPressed: () => print('AppButton pressed'),
  );
}
```

### ✅ Variantes separadas justificadas — estructura visual radicalmente diferente

Solo cuando el widget **no puede renderizar** todos sus estados con un único árbol de widgets controlado por parámetros:

```dart
@UseCase(name: 'default', type: UploadButton)
Widget buildUploadButtonUseCase(BuildContext context) { /* estado normal */ }

@UseCase(name: 'uploading', type: UploadButton)
Widget buildUploadButtonUploadingUseCase(BuildContext context) { /* progress bar activa, estructura distinta */ }

@UseCase(name: 'success', type: UploadButton)
Widget buildUploadButtonSuccessUseCase(BuildContext context) { /* checkmark animado */ }

@UseCase(name: 'error', type: UploadButton)
Widget buildUploadButtonErrorUseCase(BuildContext context) { /* ícono de error + retry */ }
```

### ❌ Antipatrón — NO crear un @UseCase por estado cuando un knob basta

```dart
// ❌ Incorrecto: tres use cases para lo que son solo cambios de parámetros
@UseCase(name: 'primary_disabled', type: AppButton)
Widget buildAppButtonPrimaryDisabledUseCase(BuildContext context) {
  return AppButton(variant: ButtonVariant.primary, isEnabled: false, ...);
}

@UseCase(name: 'primary_loading', type: AppButton)
Widget buildAppButtonPrimaryLoadingUseCase(BuildContext context) {
  return AppButton(variant: ButtonVariant.primary, isLoading: true, ...);
}

@UseCase(name: 'primary_with_icon', type: AppButton)
Widget buildAppButtonPrimaryWithIconUseCase(BuildContext context) {
  return AppButton(variant: ButtonVariant.primary, showIcon: true, ...);
}
// ✅ Correcto: un solo use case 'default' con knobs isEnabled, isLoading y showIcon
```

---

## Datos de prueba realistas — contextualizados al proyecto

**Regla clave:** antes de escribir cualquier mock o valor inicial, identificar el dominio
de la app (fintech, e-commerce, salud, educación, logística, etc.) y usar datos coherentes
con ese contexto. Nunca usar "lorem ipsum", "text", "value", "test" ni datos genéricos.

### Cómo identificar el dominio

1. Revisar el nombre del paquete en `pubspec.yaml`
2. Leer los modelos de datos en `lib/models/` o `lib/domain/`
3. Ver las pantallas existentes en `lib/features/` o `lib/screens/`
4. Inferir el dominio de la terminología usada en el código

### Ejemplos por dominio

**Fintech / Banca:**
```dart
context.knobs.string(label: 'accountHolder', initialValue: 'María García López')
context.knobs.double.input(label: 'balance', initialValue: 2450.75)
context.knobs.string(label: 'transactionDescription', initialValue: 'Transferencia a Carlos Pérez')
context.knobs.list<String>(label: 'accountType', initialOption: 'Ahorros', options: ['Ahorros', 'Corriente', 'Nómina'])

final transactions = List.generate(15, (i) => Transaction(
  id: '$i',
  description: 'Pago servicio ${['Luz', 'Agua', 'Internet', 'Gas'][i % 4]}',
  amount: (i + 1) * 23.50,
  date: DateTime.now().subtract(Duration(days: i)),
));
```

**E-commerce:**
```dart
context.knobs.string(label: 'productName', initialValue: 'Camiseta Básica Premium')
context.knobs.double.input(label: 'price', initialValue: 49.99)
context.knobs.int.slider(label: 'stock', initialValue: 24, min: 0, max: 100)
context.knobs.string(label: 'category', initialValue: 'Ropa deportiva')

final products = List.generate(20, (i) => Product(
  id: '$i',
  name: 'Producto ${['Running', 'Training', 'Casual', 'Outdoor'][i % 4]} ${i + 1}',
  price: 29.99 + (i * 10),
  imageUrl: 'https://picsum.photos/200/200?random=$i',
));
```

**Salud / Telemedicina:**
```dart
context.knobs.string(label: 'patientName', initialValue: 'Ana Martínez')
context.knobs.string(label: 'specialty', initialValue: 'Cardiología')
context.knobs.string(label: 'doctorName', initialValue: 'Dr. Roberto Sánchez')
context.knobs.dateTime(label: 'appointmentDate', initialValue: DateTime.now().add(const Duration(days: 3)))

final appointments = List.generate(8, (i) => Appointment(
  id: '$i',
  doctorName: 'Dr. ${['López', 'García', 'Martín', 'Torres'][i % 4]}',
  specialty: ['Cardiología', 'Dermatología', 'Pediatría', 'Neurología'][i % 4],
  dateTime: DateTime.now().add(Duration(days: i + 1)),
));
```

**Educación:**
```dart
context.knobs.string(label: 'courseName', initialValue: 'Introducción a Flutter')
context.knobs.string(label: 'instructorName', initialValue: 'Prof. Laura Vega')
context.knobs.int.slider(label: 'progressPercent', initialValue: 65, min: 0, max: 100)
context.knobs.int.input(label: 'enrolledStudents', initialValue: 142)
```

### ❌ Antipatrones — nunca usar estos valores

```dart
// ❌ Genérico / sin contexto
context.knobs.string(label: 'text', initialValue: 'text')
context.knobs.string(label: 'name', initialValue: 'Lorem ipsum')
context.knobs.string(label: 'title', initialValue: 'Title')
context.knobs.double.input(label: 'value', initialValue: 0.0)
context.knobs.string(label: 'description', initialValue: 'Description here')

// ❌ Datos test/placeholder
final items = List.generate(5, (i) => Item(name: 'Item $i'));
```

### Para listas — volumen y datos realistas

```dart
// ✅ Suficiente para probar scroll, rendimiento y variación visual
final items = List.generate(20, (i) => ProductItem(
  id: '$i',
  name: 'Producto ${i + 1}',
  price: 19.99 + (i * 5.50),
));
```

---

## Code preview por variante

El code preview se muestra **fuera del device frame**, en el panel de la página de Widgetbook.
Cada use case llama a `context.setCodePreview(...)` con la **llamada al constructor del widget**,
interpolando los valores actuales de los knobs — el panel se actualiza en tiempo real.

> El código mostrado es la instanciación del widget (lo que el desarrollador copiaría en su app),
> no la función del use case. Nunca embeber paneles de código dentro del widget retornado.

```dart
import '../../../shared/code_preview_addon.dart';

// ✅ Un único use case — todos los estados son knobs, NO @UseCase separados
@UseCase(name: 'default', type: AppButton)
Widget buildAppButtonUseCase(BuildContext context) {
  final label    = context.knobs.string(label: 'Text', initialValue: 'Confirmar');
  final variant  = context.knobs.list<ButtonVariant>(
    label: 'Variant',
    initialOption: ButtonVariant.primary,
    options: ButtonVariant.values,
    labelBuilder: (v) => v.name,
  );
  final isLoading = context.knobs.boolean(label: 'Loading', initialValue: false);
  final isEnabled = context.knobs.boolean(label: 'Enabled', initialValue: true);

  context.setCodePreview('''
AppButton(
  label: '$label',
  variant: ButtonVariant.${variant.name},
  isLoading: $isLoading,
  isEnabled: $isEnabled,
  onPressed: () {},
)''');

  return AppButton(
    label: label,
    variant: variant,
    isLoading: isLoading,
    isEnabled: isEnabled,
    onPressed: () => print('AppButton pressed'),
  );
}

// ❌ NO hacer esto — 'loading' no es una variante estructural, es un knob
// @UseCase(name: 'loading', type: AppButton)
// Widget buildAppButtonLoadingUseCase(BuildContext context) { ... }
```

### ✗ Antipatrón — nunca hacer esto

```dart
// ❌ NO embeber code preview dentro del use case
@UseCase(name: 'loading', type: AppButton)
Widget buildAppButtonLoadingUseCase(BuildContext context) {
  return Column(
    children: [
      AppButton(label: 'Guardando...', isLoading: true, onPressed: () {}),
      SizedBox(height: 24),
      _CodePreviewPanel(tabs: [...]),  // ❌ Se renderiza DENTRO del móvil
    ],
  );
}
```
