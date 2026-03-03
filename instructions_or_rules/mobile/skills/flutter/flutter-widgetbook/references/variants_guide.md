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

| Estado | `name` sugerido | Cuándo incluirlo |
|---|---|---|
| Estado base funcional | `'default'` | Siempre |
| Cargando datos | `'loading'` | Si tiene estado de carga |
| Deshabilitado | `'disabled'` | Si tiene `enabled: false` o similar |
| Sin datos / vacío | `'empty'` | Si puede renderizar sin contenido |
| Error | `'error'` | Si tiene estado de error visible |
| Con contenido máximo | `'full'` | Si el layout puede saturarse |
| Solo lectura | `'read_only'` | Si tiene modo de solo lectura |

---

## Estrategia por tipo de componente

### Botones
```dart
// default — estado normal interactivo con knobs
// loading  — indicador de carga activo
// disabled — no interactivo
// with_icon — variante con ícono (si aplica)
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

## Cuándo NO crear más variantes

- Si la variante se puede demostrar completamente con un knob → usar knob, no crear variante separada.
- Si la diferencia es solo de color o texto → usar knobs, no variante.
- Si el widget es tan simple que una variante con todos los knobs lo cubre → solo `'default'`.

**Ejemplo — botón simple: una sola variante es suficiente**
```dart
@UseCase(name: 'default', type: AppButton)
Widget buildAppButtonUseCase(BuildContext context) {
  return AppButton(
    label: context.knobs.string(label: 'label', initialValue: 'Confirmar'),
    isLoading: context.knobs.boolean(label: 'isLoading', initialValue: false),
    isEnabled: context.knobs.boolean(label: 'isEnabled', initialValue: true),
    onPressed: () => print('Button pressed'),
  );
}
```

**Ejemplo — botón con variantes justificadas: estados muy distintos visualmente**
```dart
@UseCase(name: 'default', type: UploadButton)
Widget buildUploadButtonUseCase(BuildContext context) { /* estado normal */ }

@UseCase(name: 'uploading', type: UploadButton)
Widget buildUploadButtonUploadingUseCase(BuildContext context) { /* progress bar activa */ }

@UseCase(name: 'success', type: UploadButton)
Widget buildUploadButtonSuccessUseCase(BuildContext context) { /* checkmark animado */ }

@UseCase(name: 'error', type: UploadButton)
Widget buildUploadButtonErrorUseCase(BuildContext context) { /* ícono de error + retry */ }
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

@UseCase(name: 'default', type: AppButton)
Widget buildAppButtonUseCase(BuildContext context) {
  final label = context.knobs.string(label: 'label', initialValue: 'Confirmar');
  final isLoading = context.knobs.boolean(label: 'isLoading', initialValue: false);
  final isEnabled = context.knobs.boolean(label: 'isEnabled', initialValue: true);

  context.setCodePreview('''
AppButton(
  label: '$label',
  isLoading: $isLoading,
  isEnabled: $isEnabled,
  onPressed: () {},
)''');

  return AppButton(
    label: label,
    isLoading: isLoading,
    isEnabled: isEnabled,
    onPressed: () => print('Button pressed'),
  );
}

@UseCase(name: 'loading', type: AppButton)
Widget buildAppButtonLoadingUseCase(BuildContext context) {
  context.setCodePreview('''
AppButton(
  label: 'Guardando...',
  isLoading: true,
  onPressed: () {},
)''');

  return AppButton(
    label: 'Guardando...',
    isLoading: true,
    onPressed: () => print('Button pressed'),
  );
}
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
