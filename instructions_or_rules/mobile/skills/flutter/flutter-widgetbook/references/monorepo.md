# Monorepo — Configuración de Widgetbook en Monorepositorio

---

## Tabla de contenidos

1. [Detectar si es monorepo](#1-detectar-si-es-monorepo)
2. [Elegir estrategia](#2-elegir-estrategia)
3. [Estrategia A — Single Widgetbook](#3-estrategia-a--single-widgetbook)
4. [Estrategia B — Per-package Widgetbook](#4-estrategia-b--per-package-widgetbook)
5. [Configuración con Melos](#5-configuración-con-melos)
6. [Comandos en monorepo](#6-comandos-en-monorepo)

---

## 1. Detectar si es monorepo

Buscar estos indicadores:

| Indicador | Significado |
|---|---|
| Archivo `melos.yaml` en la raíz | Monorepo gestionado con Melos |
| Carpeta `packages/` con subcarpetas que tienen `pubspec.yaml` | Monorepo con paquetes compartidos |
| Carpeta `apps/` con múltiples apps | Monorepo multi-app |
| Múltiples `pubspec.yaml` en subdirectorios del mismo repositorio | Monorepo manual |

Si **ninguno** de estos indicadores está presente → usar el setup estándar en `references/setup.md`.

---

## 2. Elegir estrategia

| Estrategia | Cuándo usarla | Resultado |
|---|---|---|
| **Single Widgetbook** | Se quiere un catálogo único con componentes de todos los paquetes | Una carpeta `widgetbook_[appname]/` en la raíz del monorepo |
| **Per-package Widgetbook** | Cada paquete tiene su propio catálogo independiente | Una carpeta `widgetbook_[appname]/` dentro de cada paquete/app |

Si no es claro cuál elegir, **preguntar al usuario**. Si el usuario no tiene preferencia, preferir **Single Widgetbook** por simplicidad.

---

## 3. Estrategia A — Single Widgetbook

Un solo Widgetbook en la raíz del monorepo que cataloga componentes de todos los paquetes.

### Estructura del monorepo

```
monorepo/
├── my_app/
├── packages/
│   └── my_design_system/
└── widgetbook_[appname]/                  ← Widgetbook único para todo el monorepo
    ├── pubspec.yaml
    ├── build.yaml
    └── lib/
        ├── main.dart
        ├── ui_system/
        ├── features/
        └── shared/
```

### widgetbook_[appname]/pubspec.yaml

```yaml
name: widgetbook_workspace
description: Catálogo de componentes del monorepo

publish_to: none

environment:
  sdk: '>=3.0.0 <4.0.0'
  flutter: '>=3.19.0'

dependencies:
  flutter:
    sdk: flutter
  widgetbook: ^3.13.0
  widgetbook_annotation: ^3.13.0
  # Referenciar cada paquete del monorepo que contenga widgets a catalogar
  my_design_system:
    path: ../packages/my_design_system
  my_app:
    path: ../my_app

dev_dependencies:
  widgetbook_generator: ^3.13.0
  build_runner:
  flutter_test:
    sdk: flutter
```

> **Clave:** Cada paquete que contenga widgets a catalogar debe aparecer como dependencia
> con `path:` relativo desde la carpeta `widgetbook_[appname]/`.

### build.yaml (igual que setup estándar)

```yaml
targets:
  $default:
    builders:
      widgetbook_generator:
        options:
          root_dir: lib
```

### Imports en los use cases

Los use cases importan widgets usando el nombre del paquete correspondiente:

```dart
// Widget del design system (paquete compartido)
import 'package:my_design_system/src/buttons/primary_button.dart';

// Widget de la app principal
import 'package:my_app/features/auth/presentation/login_screen.dart';
```

---

## 4. Estrategia B — Per-package Widgetbook

Cada paquete o app tiene su propio Widgetbook independiente. Más flexible pero requiere mantener múltiples catálogos.

### Estructura del monorepo

```
monorepo/
├── my_app/
│   └── widgetbook_my_app/              ← Widgetbook de la app
│       ├── pubspec.yaml
│       └── lib/
├── packages/
│   └── my_design_system/
│       └── widgetbook_my_design_system/          ← Widgetbook del design system
│           ├── pubspec.yaml
│           └── lib/
```

### my_app/widgetbook_my_app/pubspec.yaml

```yaml
name: my_app_widgetbook_workspace
description: Catálogo de componentes de my_app

publish_to: none

environment:
  sdk: '>=3.0.0 <4.0.0'
  flutter: '>=3.19.0'

dependencies:
  flutter:
    sdk: flutter
  widgetbook: ^3.13.0
  widgetbook_annotation: ^3.13.0
  my_app:
    path: ../

dev_dependencies:
  widgetbook_generator: ^3.13.0
  build_runner:
  flutter_test:
    sdk: flutter
```

### packages/my_design_system/widgetbook_my_design_system/pubspec.yaml

```yaml
name: my_design_system_widgetbook_workspace
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
  my_design_system:
    path: ../

dev_dependencies:
  widgetbook_generator: ^3.13.0
  build_runner:
  flutter_test:
    sdk: flutter
```

> **Nota:** Cada widgetbook referencia **solo** su paquete padre con `path: ../`.

---

## 5. Configuración con Melos

Si el monorepo usa [Melos](https://melos.invertase.dev/) para gestionar dependencias:

### melos.yaml

```yaml
name: my_project

packages:
  - apps/**
  - packages/**
  - widgetbook_[appname]/          # Single Widgetbook en la raíz
  # O para per-package:
  # - apps/**/widgetbook_*/
  # - packages/**/widgetbook_*/
```

### pubspec.yaml del widgetbook (con Melos)

Cuando Melos gestiona las dependencias, usar **versiones** en vez de `path:`:

```yaml
name: widgetbook_workspace

dependencies:
  flutter:
    sdk: flutter
  widgetbook: ^3.13.0
  widgetbook_annotation: ^3.13.0
  my_design_system: ^1.0.0       # Melos resuelve el path automáticamente
  my_app: ^1.0.0                 # Melos resuelve el path automáticamente

dev_dependencies:
  widgetbook_generator: ^3.13.0
  build_runner:
```

Después de configurar, ejecutar:

```bash
melos bootstrap
```

> **Si hay problemas de dependencias con Melos:** cambiar de versiones (`^1.0.0`) a paths
> explícitos (`path: ../packages/my_design_system`) o viceversa, según qué resuelva
> los conflictos.

---

## 6. Comandos en monorepo

```bash
# Single Widgetbook — desde la raíz del monorepo
cd widgetbook_[appname] && flutter pub get
cd widgetbook_[appname] && dart run build_runner build --delete-conflicting-outputs
cd widgetbook_[appname] && flutter run -d chrome

# Per-package — desde cada widgetbook individual
cd my_app/widgetbook_my_app && flutter pub get
cd my_app/widgetbook_my_app && dart run build_runner build --delete-conflicting-outputs

cd packages/my_design_system/widgetbook_my_design_system && flutter pub get
cd packages/my_design_system/widgetbook_my_design_system && dart run build_runner build --delete-conflicting-outputs

# Con Melos — bootstrap global
melos bootstrap
```

---

## Referencia

Documentación oficial: [docs.widgetbook.io/essentials/monorepo](https://docs.widgetbook.io/essentials/monorepo)
