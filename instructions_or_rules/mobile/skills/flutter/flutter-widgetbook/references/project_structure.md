# Estructura del Proyecto — Detección y Ubicación de Archivos

Antes de generar un use case, detectar qué estructura usa el proyecto
para colocar el archivo en el lugar correcto.

El Widgetbook tiene **dos secciones**: UI System (componentes) y Features (pantallas).
Ambas coexisten en `widgetbook_[appname]/lib/`.

---

## Paso 1 — Detectar la estructura

Buscar en `widgetbook_[appname]/lib/` las carpetas existentes:

### 1a. Buscar `ui_system/` y `features/`

Si ya existen `widgetbook_[appname]/lib/ui_system/` y `widgetbook_[appname]/lib/features/` → la estructura ya está correcta. Continuar al paso 2.

### 1b. Si NO existen — detectar estructura legacy y migrar

Si `widgetbook_[appname]/lib/` tiene carpetas de componentes directamente en la raíz (`atoms/`, `molecules/`, `organisms/`, `components/`), esa es una **estructura legacy**. Crear `ui_system/` y mover todo adentro:

```
# Legacy (antes)                      # Correcto (ahora)
widgetbook_[appname]/lib/             widgetbook_[appname]/lib/
├── atoms/          ───────────→      ├── ui_system/
├── molecules/                       │   ├── atoms/
└── organisms/                       │   ├── molecules/
                                      │   └── organisms/
                                      ├── features/
                                      └── shared/
```

### 1c. Si NO existe NADA — crear la estructura desde cero

**Acción imperativa:** Crear estas carpetas antes de generar cualquier use case:

```bash
# Siempre crear estas dos carpetas raíz
mkdir -p widgetbook_[appname]/lib/ui_system
mkdir -p widgetbook_[appname]/lib/features
mkdir -p widgetbook_[appname]/lib/shared
```

Luego, según el estilo del proyecto principal:

### Estructura A — Atomic Design + Features
Indicadores en el proyecto principal: carpetas `atoms/`, `molecules/`, `organisms/` o nomenclatura de Atomic Design

```bash
mkdir -p widgetbook_[appname]/lib/ui_system/atoms
mkdir -p widgetbook_[appname]/lib/ui_system/molecules
mkdir -p widgetbook_[appname]/lib/ui_system/organisms
mkdir -p widgetbook_[appname]/lib/ui_system/templates
```

Resultado:
```
widgetbook_[appname]/lib/
├── main.dart               ← Entry point
├── main.directories.g.dart ← Generado por build_runner
├── ui_system/              ← Componentes del Design System
│   ├── atoms/
│   │   ├── button/
│   │   └── text_field/
│   ├── molecules/
│   │   ├── card/
│   │   └── list_tile/
│   └── organisms/
│       └── checkout_form/
├── features/               ← Pantallas
│   ├── auth/
│   │   ├── login_screen/
│   │   └── register_screen/
│   ├── home/
│   │   └── home_screen/
│   └── profile/
│       └── profile_screen/
└── shared/
```

### Estructura B — Por componentes + Features
Indicadores en el proyecto principal: carpeta `components/`, `widgets/` o sin Atomic Design

```bash
mkdir -p widgetbook_[appname]/lib/ui_system/components
```

Resultado:
```
widgetbook_[appname]/lib/
├── main.dart               ← Entry point
├── main.directories.g.dart ← Generado por build_runner
├── ui_system/              ← Componentes del Design System
│   └── components/
│       ├── buttons/
│       ├── cards/
│       └── forms/
├── features/               ← Pantallas
│   ├── auth/
│   ├── home/
│   └── profile/
└── shared/
```

> **Regla:** Nunca colocar use cases de componentes directamente en `widgetbook_[appname]/lib/`. Siempre dentro de `ui_system/`.
> **Regla:** Nunca colocar use cases de pantallas fuera de `features/`. Siempre dentro de `features/`.

---

## Paso 2 — Determinar si es componente o pantalla

| El usuario pide catalogar... | Sección | Ubicación |
|---|---|---|
| Botón, card, input, badge, icon, etc. | UI System | `lib/ui_system/[atoms\|molecules\|organisms\|components]/` |
| Login, home, detalle, checkout, perfil, etc. | Features | `lib/features/[feature]/[screen]/` |

Si es una **pantalla**, seguir `references/features_guide.md` para el proceso completo.
Si es un **componente**, continuar con el paso 3.

---

## Paso 3 — Clasificar el componente (solo para Atomic Design)

| Categoría | Criterio | Ejemplos |
|---|---|---|
| **Atom** | Widget sin hijos componibles, unidad mínima de UI | `PrimaryButton`, `AppTextField`, `StatusBadge`, `AppIcon` |
| **Molecule** | Composición de 2-4 átomos con una función específica | `SearchBar`, `ProductCard`, `UserAvatar`, `FormField` |
| **Organism** | Sección compleja con múltiples moléculas | `CheckoutForm`, `ProductList`, `NavigationBar`, `LoginForm` |
| **Template** | Layout de pantalla sin datos reales | `DashboardTemplate`, `DetailTemplate` |

**Regla de duda:** si un widget acepta widgets hijos arbitrarios (`child`, `children`)
y no tiene lógica de negocio, probablemente es Molecule o superior.

---

## Paso 4 — Nombre y ubicación del archivo

### Para componentes (UI System)
```
widgetbook/lib/
└── ui_system/
    └── [atoms|molecules|organisms|components]/
        └── [nombre_en_snake_case]/
            └── [nombre_en_snake_case].use_case.dart
```

| Widget | Categoría | Ruta del archivo |
|---|---|---|
| `PrimaryButton` | Atom | `ui_system/atoms/primary_button/primary_button.use_case.dart` |
| `ProductCard` | Molecule | `ui_system/molecules/product_card/product_card.use_case.dart` |
| `CheckoutForm` | Organism | `ui_system/organisms/checkout_form/checkout_form.use_case.dart` |
| `CustomSlider` | Atom | `ui_system/atoms/custom_slider/custom_slider.use_case.dart` |

### Para pantallas (Features)
```
widgetbook/lib/
└── features/
    └── [nombre_feature]/
        └── [nombre_screen_snake_case]/
            └── [nombre_screen_snake_case].use_case.dart
```

| Pantalla | Feature | Ruta del archivo |
|---|---|---|
| `LoginScreen` | auth | `features/auth/login_screen/login_screen.use_case.dart` |
| `HomeScreen` | home | `features/home/home_screen/home_screen.use_case.dart` |
| `ProductDetailScreen` | catalog | `features/catalog/product_detail_screen/product_detail_screen.use_case.dart` |
| `ProfileScreen` | profile | `features/profile/profile_screen/profile_screen.use_case.dart` |

---

## Paso 5 — Registrar en widgetbook.dart (si aplica)

Si el proyecto no usa `build_runner` para generar el árbol automáticamente,
recordar agregar el nuevo use case al `WidgetbookComponent` correspondiente
en el archivo principal de Widgetbook.

Si usa `@App` con `build_runner`, el archivo se detecta automáticamente.

---

## Setup del proyecto (referencia)

### pubspec.yaml — dependencias requeridas
```yaml
dependencies:
  widgetbook: ^3.13.0

dev_dependencies:
  widgetbook_annotation: ^3.13.0
  widgetbook_generator: ^3.13.0
  build_runner: ^2.4.0
```

### widgetbook_[appname]/lib/main.dart — entry point
```dart
import 'package:flutter/material.dart';
import 'package:widgetbook/widgetbook.dart';
import 'package:widgetbook_annotation/widgetbook_annotation.dart';

import 'main.directories.g.dart';
import 'shared/code_preview_addon.dart';

void main() => runApp(const WidgetbookApp());

@App()
class WidgetbookApp extends StatelessWidget {
  const WidgetbookApp({super.key});

  @override
  Widget build(BuildContext context) {
    return Widgetbook.material(
      directories: directories,  // generado por build_runner
      addons: [
        const CodePreviewAddon(),  // señ el primero de la lista
        MaterialThemeAddon(
          themes: [
            WidgetbookTheme(name: 'Light', data: AppTheme.light),
            WidgetbookTheme(name: 'Dark', data: AppTheme.dark),
          ],
          initialTheme: WidgetbookTheme(name: 'Light', data: AppTheme.light),
        ),
        TextScaleAddon(min: 1.0, max: 2.0),
        LocalizationAddon(
          locales: AppLocalizations.supportedLocales,
          localizationsDelegates: AppLocalizations.localizationsDelegates,
        ),
        DeviceFrameAddon(devices: [
          Devices.ios.iPhone13,
          Devices.ios.iPadPro11Inches,
          Devices.android.samsungGalaxyS20,
        ]),
      ],
    );
  }
}
```

### Comando para regenerar el árbol tras agregar use cases
```bash
dart run build_runner build --delete-conflicting-outputs
```

---

## Carpeta shared/ — widgets del catálogo

Crear `widgetbook_[appname]/lib/shared/` para widgets reutilizables dentro del propio Widgetbook:

```
widgetbook_[appname]/lib/shared/
├── code_preview_addon.dart  ← Addon de code preview (obligatorio, crear una sola vez)
├── mock_providers.dart      ← Wrappers de providers para aislar pantallas
└── mock_data.dart           ← Datos mock compartidos entre use cases
```

Importar en cada use case que lo necesite:
```dart
// Desde ui_system/atoms/button/ → 3 niveles arriba
import '../../../shared/code_preview_addon.dart';
import '../../../shared/mock_data.dart';

// Desde features/auth/login_screen/ → 3 niveles arriba
import '../../../shared/code_preview_addon.dart';
import '../../../shared/mock_providers.dart';
```
