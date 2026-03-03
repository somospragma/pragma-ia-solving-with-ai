# Setup — Instalación desde Cero y Actualización

---

## Tabla de contenidos

1. [Setup desde cero](#1-setup-desde-cero)
2. [Estructura inicial de carpetas](#2-estructura-inicial-de-carpetas)
3. [main.dart completo](#3-maindart-completo)
4. [Code Preview — panel externo fuera del device frame](#4-code-preview--panel-externo-fuera-del-device-frame)
5. [Troubleshooting — Tema oscuro no se aplica](#5-troubleshooting--tema-oscuro-no-se-aplica)
6. [Actualizar dependencias en proyecto existente](#6-actualizar-dependencias-en-proyecto-existente)
7. [Comandos de referencia](#7-comandos-de-referencia)
---

## 1. Setup desde cero

### pubspec.yaml del proyecto principal

Agregar Widgetbook solo como dependencia de desarrollo — no afecta el bundle de producción:

```yaml
# pubspec.yaml (proyecto principal)
dev_dependencies:
  widgetbook_annotation: ^3.13.0
  widgetbook_generator: ^3.13.0
  build_runner: ^2.4.0
```

### pubspec.yaml de la carpeta widgetbook_[appname]/

Crear `widgetbook_[appname]/pubspec.yaml` como proyecto Flutter independiente:

```yaml
name: widgetbook_[appname]
description: Catálogo de componentes del Design System

publish_to: none

environment:
  sdk: '>=3.0.0 <4.0.0'
  flutter: '>=3.19.0'

dependencies:
  flutter:
    sdk: flutter
  widgetbook: ^3.13.0
  widgetbook_annotation: ^3.13.0
  # Importar el proyecto principal para acceder a los widgets reales
  your_app:
    path: ../

dev_dependencies:
  widgetbook_generator: ^3.13.0
  build_runner: ^2.4.0
  flutter_test:
    sdk: flutter
```

### build.yaml — configuración del generador

Crear `widgetbook_[appname]/build.yaml`:

```yaml
targets:
  $default:
    builders:
      widgetbook_generator:
        options:
          # Directorio raíz para buscar use cases anotados
          root_dir: lib
```

### Assets — imágenes e iconos del proyecto

> **Crítico:** `widgetbook_[appname]/` es un proyecto Flutter independiente.
> Los assets del proyecto principal (`your_app/assets/`) **no están disponibles**
> automáticamente en Widgetbook aunque `your_app` sea una dependencia por `path:`.
> Deben declararse explícitamente en `widgetbook_[appname]/pubspec.yaml`.

Agregar en `widgetbook_[appname]/pubspec.yaml` una sección `flutter.assets`
que apunte a los assets del proyecto principal usando rutas relativas:

```yaml
# widgetbook_[appname]/pubspec.yaml
flutter:
  uses-material-design: true
  assets:
    # Apuntar a las carpetas de assets del proyecto principal
    # El path es relativo desde widgetbook_[appname]/
    - ../assets/images/
    - ../assets/icons/
    - ../assets/fonts/
    # Si los SVGs están en una subcarpeta específica:
    - ../assets/icons/svg/
    # Agregar solo las carpetas que los use cases realmente usen
```

> **Paths relativos:** `../` sube un nivel (sale de `widgetbook_[appname]/`
> y entra al directorio raíz donde también está `your_app/`). Ajustar según
> la estructura real del proyecto.

**Ejemplo con estructura real:**
```
my_project/               ← raíz
├── my_app/               ← proyecto principal
│   ├── assets/
│   │   ├── images/       → declarar como: - ../my_app/assets/images/
│   │   └── icons/        → declarar como: - ../my_app/assets/icons/
│   └── pubspec.yaml
└── widgetbook_my_app/    ← widgetbook
    └── pubspec.yaml      ← aquí se declaran los assets
```

Si `widgetbook_[appname]/` está dentro de `your_app/`:
```
your_app/
├── assets/
│   ├── images/           → declarar como: - assets/images/
│   └── icons/            → declarar como: - assets/icons/
├── lib/
└── widgetbook_[appname]/
    └── pubspec.yaml      ← usar: - ../assets/images/
```

Después de agregar los assets, ejecutar:
```bash
cd widgetbook_[appname] && flutter pub get
```

> **flutter_svg:** Si el proyecto usa SVG con `flutter_svg`, agregar el paquete
> también en `widgetbook_[appname]/pubspec.yaml`:
> ```yaml
> dependencies:
>   flutter_svg: ^2.0.0   # misma versión que el proyecto principal
> ```

---

## 2. Estructura inicial de carpetas

Crear la siguiente estructura según la organización del proyecto.

**IMPORTANTE:** Siempre crear las carpetas raíz `ui_system/`, `features/` y `shared/` antes de generar use cases:

```bash
# Paso obligatorio — crear carpetas raíz
mkdir -p widgetbook_[appname]/lib/ui_system
mkdir -p widgetbook_[appname]/lib/features
mkdir -p widgetbook_[appname]/lib/shared
```

### Con Atomic Design

```bash
# Subcarpetas según Atomic Design
mkdir -p widgetbook_[appname]/lib/ui_system/atoms
mkdir -p widgetbook_[appname]/lib/ui_system/molecules
mkdir -p widgetbook_[appname]/lib/ui_system/organisms
mkdir -p widgetbook_[appname]/lib/ui_system/templates
```

Resultado:
```
widgetbook_[appname]/
├── pubspec.yaml
├── build.yaml
└── lib/
    ├── main.dart              ← Entry point de Widgetbook
    ├── main.directories.g.dart ← Generado por build_runner (árbol de use cases)
    ├── shared/
    │   └── code_preview_addon.dart ← Addon de code preview (crear una sola vez)
    ├── ui_system/              ← Componentes del Design System
    │   ├── atoms/              ← Unidades mínimas: Button, TextField, Badge
    │   ├── molecules/          ← Combinaciones: Card, SearchBar, FormField
    │   ├── organisms/          ← Secciones complejas: Form, List, Nav
    │   └── templates/          ← Layouts de pantalla
    ├── features/               ← Pantallas del proyecto
    └── shared/                 ← Widgets del catálogo
```

### Con carpetas de componentes

```bash
mkdir -p widgetbook_[appname]/lib/ui_system/components
```

Resultado:
```
widgetbook_[appname]/
├── pubspec.yaml
├── build.yaml
└── lib/
    ├── main.dart              ← Entry point
    ├── main.directories.g.dart ← Generado por build_runner
    ├── shared/
    │   └── code_preview_addon.dart ← Addon de code preview (crear una sola vez)
    ├── ui_system/              ← Componentes del Design System
    │   └── components/
    │       ├── buttons/
    │       ├── cards/
    │       └── forms/
    ├── features/               ← Pantallas del proyecto
    └── shared/                 ← Widgets del catálogo
```

---

## 3. main.dart completo

```dart
// widgetbook_[appname]/lib/main.dart

import 'package:flutter/material.dart';
import 'package:widgetbook/widgetbook.dart';
import 'package:widgetbook_annotation/widgetbook_annotation.dart';
import 'package:your_app/core/theme/app_theme.dart';
import 'package:your_app/core/l10n/generated/app_localizations.dart';

import 'main.directories.g.dart';
import 'shared/code_preview_addon.dart';

void main() => runApp(const WidgetbookApp());

@App()
class WidgetbookApp extends StatelessWidget {
  const WidgetbookApp({super.key});

  @override
  Widget build(BuildContext context) {
    return Widgetbook.material(
      directories: directories,
      addons: [
        // Code preview — panel de código debajo del device frame
        // DEBE ir primero para que envuelva correctamente el uso de los demás addons
        const CodePreviewAddon(),

        // Tema claro/oscuro — se inyecta globalmente en todos los use cases
        MaterialThemeAddon(
          themes: [
            WidgetbookTheme(name: 'Light', data: AppTheme.light),
            WidgetbookTheme(name: 'Dark', data: AppTheme.dark),
          ],
          initialTheme: WidgetbookTheme(name: 'Light', data: AppTheme.light),
        ),

        // Escala de texto — prueba accesibilidad
        TextScaleAddon(min: 1.0, max: 2.0, initialScale: 1.0),

        // Localización — prueba en/es sin cambiar el dispositivo
        LocalizationAddon(
          locales: AppLocalizations.supportedLocales,
          localizationsDelegates: AppLocalizations.localizationsDelegates,
          initialLocale: const Locale('es'),
        ),

        // Device frame — simula dispositivos reales
        DeviceFrameAddon(
          devices: [
            Devices.ios.iPhone13,
            Devices.ios.iPhone13ProMax,
            Devices.ios.iPadPro11Inches,
            Devices.android.samsungGalaxyS20,
            Devices.android.samsungGalaxyA50,
          ],
          initialDevice: Devices.ios.iPhone13,
        ),

        // Grid de alineación — útil para revisión con diseño
        GridAddon(gridSize: 8),

        // Alignment — centrar o alinear el componente en el canvas
        AlignmentAddon(initialAlignment: Alignment.center),
      ],
    );
  }
}
```

---

## 4. Code Preview — panel externo fuera del device frame

El code preview se muestra **debajo del device frame**, fuera del widget renderizado
en el móvil. Muestra la llamada al constructor del widget con los **valores actuales
de los knobs** — se actualiza en tiempo real al ajustar cualquier control.

Se implementa con un **custom addon** (`CodePreviewAddon`) que:
1. Envuelve cada use case en un `Column`: device frame arriba + panel de código abajo.
2. Expone `context.setCodePreview(String)` para que cada use case inyecte su snippet.
3. Muestra el panel con label DART, botón Copiar y texto seleccionable.
4. Incluye un botón **Ocultar / Mostrar código** en el header del panel para colapsar o expandir el contenido sin perder el header de referencia.

---

### Archivo: `widgetbook_[appname]/lib/shared/code_preview_addon.dart`

Crear este archivo una sola vez. Todos los use cases lo usan vía la extensión
`context.setCodePreview(...)`.

```dart
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:widgetbook/widgetbook.dart';

// ─────────────────────────────────────────────────────────────────────────────
// InheritedWidget — propaga el ValueNotifier por el árbol del use case
// ─────────────────────────────────────────────────────────────────────────────
class _CodePreviewScope extends InheritedWidget {
  const _CodePreviewScope({
    required this.notifier,
    required super.child,
  });

  final ValueNotifier<String> notifier;

  @override
  bool updateShouldNotify(_CodePreviewScope old) => notifier != old.notifier;

  static ValueNotifier<String>? of(BuildContext context) {
    return context
        .dependOnInheritedWidgetOfExactType<_CodePreviewScope>()
        ?.notifier;
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// Extensión de BuildContext — API pública para los use cases
// ─────────────────────────────────────────────────────────────────────────────
extension CodePreviewExtension on BuildContext {
  /// Registra el snippet de código que se mostrará debajo del device frame.
  /// Llamar dentro del builder del use case, antes de retornar el widget.
  ///
  /// El string debe contener la llamada al constructor del widget con los
  /// valores actuales de los knobs interpolados:
  ///
  /// ```dart
  /// context.setCodePreview('''
  /// PrimaryButton(
  ///   label: '$label',
  ///   isLoading: $isLoading,
  ///   onPressed: () {},
  /// )''');
  /// ```
  void setCodePreview(String code) {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _CodePreviewScope.of(this)?.value = code;
    });
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// Addon — registrar en main.dart → addons: [CodePreviewAddon(), ...]
// ─────────────────────────────────────────────────────────────────────────────
class CodePreviewAddon extends WidgetbookAddon<void> {
  const CodePreviewAddon() : super(name: 'Code Preview');

  @override
  void valueFromQueryGroup(Map<String, String> group) {}

  @override
  Widget buildUseCase(BuildContext context, Widget child, void setting) {
    final notifier = ValueNotifier<String>('');
    return _CodePreviewScope(
      notifier: notifier,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Expanded(child: child),
          ValueListenableBuilder<String>(
            valueListenable: notifier,
            builder: (_, code, __) => _CodePreviewPanel(code: code),
          ),
        ],
      ),
    );
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// Panel visual — con toggle para mostrar/ocultar el código
// ─────────────────────────────────────────────────────────────────────────────
class _CodePreviewPanel extends StatefulWidget {
  const _CodePreviewPanel({required this.code});

  final String code;

  @override
  State<_CodePreviewPanel> createState() => _CodePreviewPanelState();
}

class _CodePreviewPanelState extends State<_CodePreviewPanel> {
  bool _expanded = true;

  @override
  Widget build(BuildContext context) {
    if (widget.code.isEmpty) return const SizedBox.shrink();

    return Container(
      decoration: BoxDecoration(
        color: const Color(0xFF1E1E2E),
        border: Border(
          top: BorderSide(color: Colors.white.withOpacity(0.1)),
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          // Header — siempre visible
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
            child: Row(
              children: [
                const Icon(Icons.code, size: 16, color: Color(0xFF89B4FA)),
                const SizedBox(width: 8),
                const Text(
                  'Código Generado',
                  style: TextStyle(
                    color: Color(0xFFCDD6F4),
                    fontSize: 13,
                    fontWeight: FontWeight.w600,
                  ),
                ),
                const SizedBox(width: 8),
                if (_expanded)
                  Text(
                    'Este código se actualiza según los controles que ajustes.',
                    style: TextStyle(
                      color: Colors.white.withOpacity(0.45),
                      fontSize: 11,
                    ),
                  ),
                const Spacer(),
                if (_expanded) _CopyButton(code: widget.code),
                const SizedBox(width: 4),
                // Botón toggle
                _ToggleButton(
                  expanded: _expanded,
                  onToggle: () => setState(() => _expanded = !_expanded),
                ),
              ],
            ),
          ),
          // Contenido colapsable
          if (_expanded) ...[
            // Tag DART
            Padding(
              padding: const EdgeInsets.only(left: 16, bottom: 4),
              child: Text(
                'DART',
                style: TextStyle(
                  color: Colors.white.withOpacity(0.35),
                  fontSize: 10,
                  letterSpacing: 1.2,
                  fontWeight: FontWeight.w600,
                ),
              ),
            ),
            // Código
            SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              padding: const EdgeInsets.fromLTRB(16, 0, 16, 16),
              child: SelectableText(
                widget.code,
                style: const TextStyle(
                  fontFamily: 'monospace',
                  fontSize: 13,
                  color: Color(0xFFCDD6F4),
                  height: 1.6,
                ),
              ),
            ),
          ],
        ],
      ),
    );
  }
}

class _ToggleButton extends StatelessWidget {
  const _ToggleButton({required this.expanded, required this.onToggle});

  final bool expanded;
  final VoidCallback onToggle;

  @override
  Widget build(BuildContext context) {
    return TextButton.icon(
      onPressed: onToggle,
      icon: Icon(
        expanded ? Icons.keyboard_arrow_down : Icons.keyboard_arrow_up,
        size: 16,
        color: const Color(0xFF89B4FA),
      ),
      label: Text(
        expanded ? 'Ocultar' : 'Mostrar código',
        style: const TextStyle(
          fontSize: 12,
          color: Color(0xFF89B4FA),
        ),
      ),
      style: TextButton.styleFrom(
        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
        minimumSize: Size.zero,
        tapTargetSize: MaterialTapTargetSize.shrinkWrap,
      ),
    );
  }
}

class _CopyButton extends StatefulWidget {
  const _CopyButton({required this.code});
  final String code;

  @override
  State<_CopyButton> createState() => _CopyButtonState();
}

class _CopyButtonState extends State<_CopyButton> {
  bool _copied = false;

  Future<void> _copy() async {
    await Clipboard.setData(ClipboardData(text: widget.code));
    setState(() => _copied = true);
    await Future.delayed(const Duration(seconds: 2));
    if (mounted) setState(() => _copied = false);
  }

  @override
  Widget build(BuildContext context) {
    return TextButton.icon(
      onPressed: _copy,
      icon: Icon(
        _copied ? Icons.check : Icons.copy,
        size: 14,
        color: _copied ? const Color(0xFFA6E3A1) : const Color(0xFF89B4FA),
      ),
      label: Text(
        _copied ? 'Copiado' : 'Copiar',
        style: TextStyle(
          fontSize: 12,
          color: _copied ? const Color(0xFFA6E3A1) : const Color(0xFF89B4FA),
        ),
      ),
      style: TextButton.styleFrom(
        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
        minimumSize: Size.zero,
        tapTargetSize: MaterialTapTargetSize.shrinkWrap,
      ),
    );
  }
}
```

---

### Patrón en el use case — widget + setCodePreview

Cada use case debe:
1. Leer los knobs en variables locales.
2. Llamar a `context.setCodePreview(...)` con la **llamada al constructor** del widget,
   interpolando los valores de los knobs.
3. Retornar el widget usando esas mismas variables.

> **El código mostrado es la instanciación del widget** (lo que el desarrollador
> copiaría en su app), no la función del use case.

```dart
// widgetbook_[appname]/lib/ui_system/atoms/primary_button/primary_button.use_case.dart

import 'package:flutter/material.dart';
import 'package:widgetbook/widgetbook.dart';
import 'package:widgetbook_annotation/widgetbook_annotation.dart';
import 'package:your_app/core/widgets/primary_button.dart';
import '../../../shared/code_preview_addon.dart';

@UseCase(name: 'default', type: PrimaryButton)
Widget buildPrimaryButtonUseCase(BuildContext context) {
  // 1. Leer knobs en variables locales
  final label = context.knobs.string(label: 'label', initialValue: 'Confirmar');
  final isLoading = context.knobs.boolean(label: 'isLoading', initialValue: false);
  final isEnabled = context.knobs.boolean(label: 'isEnabled', initialValue: true);

  // 2. Registrar el código que se mostrará en el panel — interpolando los valores actuales
  context.setCodePreview('''
PrimaryButton(
  label: '$label',
  isLoading: $isLoading,
  isEnabled: $isEnabled,
  onPressed: () {},
)''');

  // 3. Retornar el widget con las mismas variables
  return PrimaryButton(
    label: label,
    isLoading: isLoading,
    isEnabled: isEnabled,
    onPressed: () => print('PrimaryButton pressed'),
  );
}
```

### ✗ Antipatrón — embedded code preview dentro del widget

```dart
// ❌ NUNCA — _CodePreviewPanel se renderizaría DENTRO del móvil
@UseCase(name: 'default', type: PrimaryButton)
Widget buildPrimaryButtonUseCase(BuildContext context) {
  return Column(
    children: [
      PrimaryButton(label: 'Confirmar', onPressed: () {}),
      _CodePreviewPanel(code: '...'),  // ❌ dentro del device frame
    ],
  );
}
```

---

## 5. Troubleshooting — Tema oscuro no se aplica

Si al cambiar de Light a Dark en Widgetbook los componentes no reflejan el cambio:

### Causa 1: Colores hardcodeados en el widget o use case
```dart
// ❌ No respeta el tema — siempre se ve igual
Container(color: const Color(0xFF1E1E1E))
Text('Hola', style: TextStyle(color: Colors.white))

// ✅ Se adapta al tema activo
Container(color: Theme.of(context).colorScheme.surfaceContainerHighest)
Text('Hola', style: TextStyle(color: Theme.of(context).colorScheme.onSurface))
```

### Causa 2: Widget envuelto en su propio MaterialApp o Theme
Si el use case envuelve el widget con `MaterialApp(...)` o `Theme(...)`, se ignora
el tema inyectado por `MaterialThemeAddon`. **Nunca envolver** — el tema ya viene
del addon global.

```dart
// ❌ Sobreescribe el tema del addon
return MaterialApp(theme: ThemeData.light(), home: MyWidget());

// ✅ El widget recibe el tema del addon directamente
return MyWidget();
```

### Causa 3: El widget no usa Theme.of(context)
Si el widget original define sus colores con constantes en vez de leerlos del tema,
el cambio de tema no tendrá efecto. Verificar que el widget usa:
```dart
final colors = Theme.of(context).colorScheme;
final textTheme = Theme.of(context).textTheme;
```

### Causa 4: initialTheme no configurado
Si `MaterialThemeAddon` no tiene `initialTheme`, Widgetbook toma el primero de
la lista. Para asegurar que ambos temas están disponibles y seleccionables:
```dart
MaterialThemeAddon(
  themes: [
    WidgetbookTheme(name: 'Light', data: AppTheme.light),
    WidgetbookTheme(name: 'Dark', data: AppTheme.dark),
  ],
  initialTheme: WidgetbookTheme(name: 'Light', data: AppTheme.light),
),
```

### Verificación rápida
1. Abrir Widgetbook en Chrome
2. En el panel lateral, buscar el selector de tema (dropdown "Theme")
3. Cambiar entre Light y Dark
4. Si el widget no cambia → revisar causas 1-3 arriba

---

## 6. Actualizar dependencias en proyecto existente

Cuando Widgetbook ya está instalado y se quiere actualizar:

```bash
# Actualizar a la última versión 3.x
flutter pub upgrade widgetbook widgetbook_annotation widgetbook_generator

# Verificar versiones activas
flutter pub deps | grep widgetbook

# Regenerar todo el árbol de directorios
dart run build_runner build --delete-conflicting-outputs
```

Si hay breaking changes al actualizar, revisar el [CHANGELOG de Widgetbook](https://github.com/widgetbook/widgetbook/blob/main/packages/widgetbook/CHANGELOG.md).

---

## 7. Comandos de referencia

```bash
# Generar/regenerar use cases y árbol de directorios
dart run build_runner build --delete-conflicting-outputs

# Watch mode durante desarrollo activo
dart run build_runner watch --delete-conflicting-outputs

# Ejecutar Widgetbook en el dispositivo/simulador
cd widgetbook_[appname] && flutter run -d chrome   # web (recomendado para diseño)
cd widgetbook_[appname] && flutter run             # dispositivo conectado

# Ejecutar golden tests
cd widgetbook_[appname] && flutter test
```


> **Monorepo:** Si el proyecto es un monorepositorio, ver `references/monorepo.md` para la configuración completa (single widgetbook, per-package, Melos).
