---
name: flutter-widgetbook
description: Skill para crear y mantener Widgetbook 3.x en proyectos Flutter encualquier momento del ciclo de desarrollo: setup inicial desde cero, incorporación de componentes existentes (UI System) y pantallas completas (Features), y adición/actualización de use cases. Genera catálogo con dos secciones: UI System (componentes con Atomic Design) y Features (pantallas del proyecto con sus estados). Incluye code preview, knobs interactivos, datos mock del dominio y golden tests. Úsalo siempre que el usuario mencione Widgetbook, use case, catálogo de componentes, design system, storybook flutter, golden tests, knobs, variantes de widget, code preview, pantalla, feature, screen, page, o cuando pida "agrégalo al widgetbook", "crea el use case", "muestra el código en widgetbook", "configura widgetbook desde cero", "actualiza el catálogo", "documenta este componente visualmente", "agrega esta pantalla", "cataloga los features" o "actualiza el widgetbook con las pantallas".
metadata:
  author: Pragma Mobile Chapter
  version: "1.0"
---

# Flutter Widgetbook

> **Stack:** Widgetbook 3.x · widgetbook_annotation · build_runner · Atomic Design

---

## Detectar el modo de trabajo

Antes de cualquier otra cosa, identificar en qué momento del ciclo está el proyecto:

| Situación | Modo | Referencia |
|---|---|---|
| No existe carpeta `widgetbook_[appname]/` ni dependencias | **Setup desde cero** | `references/setup.md` |
| El proyecto es un monorepo (Melos, carpeta `packages/`, múltiples apps) | **Setup monorepo** | `references/monorepo.md` |
| Existe Widgetbook pero el componente no está catalogado | **Agregar componente** | `references/project_structure.md` + Proceso abajo |
| Existe Widgetbook pero la pantalla/feature no está catalogada | **Agregar feature** | `references/project_structure.md` + `references/features_guide.md` |
| El componente ya tiene use case y hay cambios | **Actualizar use case** | Proceso abajo |
| La pantalla ya tiene use case y hay cambios | **Actualizar feature** | `references/features_guide.md` |
| El usuario pide verificar qué falta, se incorporó widgetbook a un proyecto existente, o se quiere saber la cobertura actual | **Auditoría de cobertura** | `references/coverage_audit.md` |

---

## Clasificar el tipo de catálogo

Widgetbook organiza el contenido en **dos secciones**:

| Sección | Qué contiene | Ubicación en widgetbook/ |
|---|---|---|
| **UI System** | Componentes reutilizables: botones, cards, inputs, badges, etc. | `lib/ui_system/[atoms\|molecules\|organisms\|components]/` |
| **Features** | Pantallas completas del proyecto: login, home, detail, checkout, etc. | `lib/features/[nombre_feature]/[nombre_screen]/` |

Antes de generar un use case, determinar si el usuario pide catalogar un **componente** (UI System)
o una **pantalla** (Feature). Si no es claro, preguntar.

> **IMPORTANTE:** Los componentes van SIEMPRE dentro de `widgetbook_[appname]/lib/ui_system/`. Las pantallas van SIEMPRE dentro de `widgetbook_[appname]/lib/features/`. Nunca crear use cases directamente en `widgetbook_[appname]/lib/`.

---

## Proceso para generar o actualizar un Use Case

Seguir estos pasos en orden:

1. **Detectar modo** — setup, agregar o actualizar (tabla arriba).
2. **Detectar si es monorepo** — buscar indicadores: `melos.yaml`, carpeta `packages/`, múltiples `pubspec.yaml` en subdirectorios, o que el usuario lo mencione. Si es monorepo, leer `references/monorepo.md` para elegir la estrategia (single widgetbook vs per-package).
3. **Si es setup desde cero** — leer `references/setup.md` primero y completar la instalación antes de continuar.
4. **Si es auditoría de cobertura** — leer `references/coverage_audit.md` completo: escanear componentes y pantallas del proyecto principal, cruzarlos con `widgetbook_[appname]/lib/ui_system/` y `widgetbook_[appname]/lib/features/`, presentar el reporte de cobertura con gaps detectados y, solo después de que el usuario confirme, proceder a generar los use cases faltantes (volviendo al paso 5 para cada uno).
5. **Clasificar** — determinar si es UI System (componente) o Feature (pantalla).
6. **Verificar estructura de carpetas** — leer `references/project_structure.md` paso 1. **Confirmar que existen `widgetbook_[appname]/lib/ui_system/` y `widgetbook_[appname]/lib/features/`**. Si no existen, crearlas ANTES de continuar. Nunca colocar use cases fuera de estas carpetas.
7. **Analizar el widget/pantalla** — leer la clase completa: parámetros requeridos y opcionales, tipos, enums, callbacks, dependencias de estado o providers. Para pantallas: identificar también las dependencias de navegación, providers y servicios.
8. **Detectar ubicación exacta** — ver `references/project_structure.md` paso 4 para determinar la ruta completa del archivo.
9. **Planificar variantes** — ver `references/variants_guide.md` (componentes) o `references/features_guide.md` (pantallas) para decidir cuántos `@UseCase` necesita. **Regla de oro:** si el estado o el tipo visual del componente se controla con un parámetro del constructor (variant, isLoading, isEnabled, showIcon, iconPosition…) → usar un knob, NO crear un `@UseCase` separado. Solo crear múltiples `@UseCase` cuando el widget renderiza estructuras visuales radicalmente distintas que no pueden controlarse con parámetros.
10. **Seleccionar knobs** — ver `assets/knobs_reference.md` para elegir el tipo de knob por cada parámetro.
11. **Generar el use case con code preview** — seguir las convenciones de naming. Leer knobs en variables, llamar `context.setCodePreview(...)` con la instanciación del widget interpolando los valores, retornar el widget con esas mismas variables.
12. **Verificar errores Dart antes de build_runner** — analizar todos los archivos `.use_case.dart`, `shared/` y cualquier helper creado, excluyendo `main.dart` y archivos generados. Ver sección "Verificación Dart pre-build" abajo. Corregir **todos** los errores antes de continuar.
13. **Ejecutar build_runner** — después de crear o modificar cualquier archivo dentro de `widgetbook_[appname]/`, ejecutar **siempre** la generación de código. Ver sección "Generación con build_runner" abajo.
14. **Verificar el checklist** — confirmar cobertura antes de entregar.

---

## Verificación Dart pre-build — paso obligatorio antes de build_runner

Antes de ejecutar `build_runner`, **todos** los archivos `.use_case.dart`, `shared/` y cualquier helper
creado deben estar libres de errores Dart. De lo contrario, `build_runner` fallará o generará
un catálogo con use cases rotos.

> **Por qué excluir `main.dart`:** `main.dart` importa `main.directories.g.dart`, que aún no existe
> (o está desactualizado) en este punto del proceso. Los errores de ese import son esperados y no
> deben bloquear la verificación.

### Comando

```bash
# Analizar solo los use cases y helpers, excluyendo main.dart y archivos generados
cd widgetbook_[appname] && dart analyze lib/ui_system lib/features lib/shared
```

Si las carpetas `ui_system/` o `features/` aún no existen en este proyecto, ajustar el comando
a las carpetas reales que se crearon.

### Interpretar la salida

| Tipo de mensaje | Qué hacer |
|---|---|
| `error` en un `.use_case.dart` | **Corregir antes de continuar** — imports faltantes, tipos incorrectos, parámetros mal nombrados |
| `warning` en un `.use_case.dart` | Evaluar — si es un unused import o similar, eliminar el import |
| `info` / `hint` | Opcional — no bloquea el proceso |
| Cualquier mensaje en `main.dart` o `main.directories.g.dart` | Ignorar en este paso |

### Errores frecuentes y cómo resolverlos

| Error | Causa habitual | Solución |
|---|---|---|
| `Target of URI doesn't exist` | Import incorrecto al widget de la app | Verificar la ruta relativa/package del import |
| `The method 'X' isn't defined` | Knob o método inexistente en la API de Widgetbook | Revisar `assets/knobs_reference.md` |
| `Too many positional arguments` | Constructor del widget cambió | Releer la clase fuente y actualizar el use case |
| `Undefined name 'MockX'` | Clase mock no declarada o import faltante | Declarar `class MockX extends Mock implements X {}` a nivel de archivo |
| `Missing concrete implementation` | Mock incompleto | Agregar `@override` o usar `MockX() : super()` según el tipo de mock |
| `The name 'X' is already defined` | Dos use cases en el mismo archivo con la misma función auxiliar | Renombrar o mover la función |

### Flujo si hay errores

```
1. Leer el error completo (archivo, línea, mensaje)
2. Abrir el archivo indicado y corregir
3. Volver a ejecutar dart analyze lib/ui_system lib/features lib/shared
4. Repetir hasta que la salida no tenga ningún `error`
5. Continuar con el paso 13 (build_runner)
```

> **Regla absoluta:** Nunca ejecutar `build_runner` si `dart analyze` reporta errores en los use cases.
> Un use case con error de compilación rompe la generación de `main.directories.g.dart` completa.

---

## Generación con build_runner — paso obligatorio

Cada vez que se **crea, modifica o elimina** un archivo `.use_case.dart` o el `main.dart` de widgetbook, es **obligatorio** ejecutar `build_runner` para regenerar los archivos generados del `main.dart`.

> **Concepto clave:** En Widgetbook 3.x, `build_runner` **solo genera `main.directories.g.dart`** a partir de `main.dart`. Los archivos `.use_case.dart` **NO generan** archivos `.g.dart` propios. Las anotaciones `@UseCase` son escaneadas por el generador y consolidadas en `main.directories.g.dart`. Por lo tanto, los use cases **nunca deben tener** `part '*.use_case.g.dart'`.

### Comando

```bash
cd widgetbook_[appname] && dart run build_runner build --delete-conflicting-outputs
```

### Cuándo ejecutar

| Acción realizada | ¿Ejecutar build_runner? |
|---|---|
| Se creó un nuevo `.use_case.dart` | **Sí** — actualiza `main.directories.g.dart` con el nuevo use case |
| Se modificó un `@UseCase` existente (nombre, tipo) | **Sí** — actualiza `main.directories.g.dart` |
| Se eliminó un `.use_case.dart` | **Sí** — limpia el árbol de directorios |
| Se modificó `main.dart` (addons, configuración) | **Sí** — regenera `main.directories.g.dart` |
| Solo se cambió lógica interna del use case (knobs, layout) sin tocar anotaciones | **Sí** — el code preview y la metadata pueden depender del contenido generado |
| Se modificó un archivo fuera de `widgetbook_[appname]/` | No |

### Verificación post-generación

Después de ejecutar `build_runner`, confirmar que:

1. **No hay errores** en la salida del comando.
2. **Se generó el archivo del `main.dart`**:
   - `widgetbook_[appname]/lib/main.directories.g.dart` existe y contiene las entradas del nuevo use case.
3. **El árbol de directorios está actualizado** — el nuevo componente o pantalla aparece en `main.directories.g.dart`.
4. **Los use cases NO tienen archivos `.g.dart` propios** — si existen archivos como `*.use_case.g.dart`, eliminarlos.

Si `build_runner` falla:
- Verificar que `widgetbook_[appname]/pubspec.yaml` tiene las dependencias correctas (`widgetbook_generator`, `build_runner`).
- Ejecutar `cd widgetbook_[appname] && flutter pub get` antes de reintentar.
- Revisar que las anotaciones `@UseCase` son correctas.
- Verificar que `main.dart` tiene `import 'main.directories.g.dart';`.
- Verificar que los archivos `.use_case.dart` **NO** tienen `part '*.g.dart'`.

> **IMPORTANTE:** Nunca entregar un use case sin haber ejecutado `build_runner`. Sin regenerar `main.directories.g.dart`, el nuevo use case no aparecerá en el catálogo de Widgetbook.

---

## Convenciones de naming — exactas, sin variaciones

### Anotación
```dart
@UseCase(
  name: 'variantName',   // 'default' si es única; descriptivo si hay varias
  type: ComponentType,
)
```

### Firma del método
```dart
Widget build[ComponentName][VariantName]UseCase(BuildContext context) { }
```

**Ejemplos:**
- Única variante → `buildPrimaryButtonUseCase`
- Variantes estructuralmente distintas → `buildUploadButtonUploadingUseCase`, `buildUploadButtonSuccessUseCase`

> **No** nombrar variantes por estados que se controlan con knobs (loading, disabled, withIcon): esos van como knobs dentro del mismo use case, no como `@UseCase` separados.

### Names de variantes
- Una sola → `name: 'default'`
- Varias → snake_case descriptivo: `'with_icon'`, `'loading'`, `'disabled'`, `'empty_state'`
- Únicos dentro del mismo `type`

### Naming para Features (pantallas)

Misma convención que componentes, pero el `type` es la clase de la pantalla:

```dart
@UseCase(
  name: 'default',        // estado principal de la pantalla
  type: LoginScreen,
)
Widget buildLoginScreenUseCase(BuildContext context) { }

@UseCase(
  name: 'error',           // pantalla mostrando error de validación
  type: LoginScreen,
)
Widget buildLoginScreenErrorUseCase(BuildContext context) { }
```

**Ejemplos de names para pantallas:**
- `'default'` — pantalla en su estado principal con datos
- `'loading'` — pantalla cargando datos
- `'empty'` — pantalla sin datos
- `'success'` — pantalla mostrando resultado exitoso
- `'error'` — pantalla con estado de error
- `'logged_out'` — pantalla en estado no autenticado
- `'first_time'` — pantalla para usuario nuevo (onboarding)

---

## Code Preview — panel externo, fuera del device frame

El code preview se muestra **debajo del device frame**, fuera del widget renderizado
en el móvil. Muestra la **llamada al constructor del widget con los valores actuales
de los knobs** y se actualiza en tiempo real al ajustar cualquier control.

Se implementa mediante `CodePreviewAddon` (en `shared/code_preview_addon.dart`) y
la extensión `context.setCodePreview(String)` que cada use case llama antes de
retornar su widget. El panel incluye botón **Copiar**, botón **Ocultar / Mostrar código**
para colapsar o expandir el código sin perder el header, y texto seleccionable.

> **Regla clave:** El código que se muestra es la **instanciación del widget**
> (lo que el desarrollador copiaría en su app), no la función del use case.
> El use case NUNCA embebe paneles de código dentro del widget retornado.

### Patrón obligatorio en cada use case

```dart
import 'package:flutter/material.dart';
import 'package:widgetbook/widgetbook.dart';
import 'package:widgetbook_annotation/widgetbook_annotation.dart';
import 'package:your_app/core/widgets/primary_button.dart';
import '../../../shared/code_preview_addon.dart';

// Ejemplo mínimo para ilustrar el patrón del code preview.
// En un botón real, añadir también knobs de variant, size, icon, iconPosition,
// showIcon, etc. — ver references/variants_guide.md § Regla de oro.
@UseCase(name: 'default', type: PrimaryButton)
Widget buildPrimaryButtonUseCase(BuildContext context) {
  // 1. Leer knobs en variables locales
  final label = context.knobs.string(label: 'label', initialValue: 'Confirmar');
  final isLoading = context.knobs.boolean(label: 'isLoading', initialValue: false);
  final isEnabled = context.knobs.boolean(label: 'isEnabled', initialValue: true);

  // 2. Registrar el código con los valores actuales de los knobs interpolados
  //    El code preview muestra la instanciación del widget SIN el wrapper de fondo —
  //    el ColoredBox es scaffolding del catálogo, no código de producción.
  context.setCodePreview('''
PrimaryButton(
  label: '$label',
  isLoading: $isLoading,
  isEnabled: $isEnabled,
  onPressed: () {},
)''');

  // 3. Retornar el widget envuelto en ColoredBox con el fondo correcto según el tema.
  //    NO aplicar a templates ni a Features (tienen su propio Scaffold).
  final isDark = Theme.of(context).brightness == Brightness.dark;
  return ColoredBox(
    color: isDark ? AppColors.primary900 : AppColors.primary0,
    child: Center(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: PrimaryButton(
          label: label,
          isLoading: isLoading,
          isEnabled: isEnabled,
          onPressed: () => print('PrimaryButton pressed'),
        ),
      ),
    ),
  );
}
```

### Configuración en main.dart

Ver `references/setup.md` § 3 para el `main.dart` completo con `CodePreviewAddon`
registrado, y § 4 para el archivo `shared/code_preview_addon.dart` completo.

---

## Mocking de dependencias

Catalogar un widget con dependencias externas (providers, servicios, repositorios) requiere una estrategia explícita. Hay dos enfoques:

| Situación | Enfoque |
|---|---|
| Componente reutilizable que consulta un provider internamente | **Extracción** — extraer la dependencia a un parámetro del constructor |
| Pantalla completa que consume providers y no es refactorizable | **Mocking con librería** — `mocktail` + `ChangeNotifierProvider`/`MultiProvider` en el use case |
| Componente simple sin dependencias externas | Hardcodear valores directamente en el use case |

> Ver ejemplos completos, patrones de `when(...)` y reglas en `references/mocks.md`.

---

## Estructura de archivos generados

```
widgetbook_[appname]/
└── lib/
    ├── main.directories.g.dart                  ← Generado por build_runner (árbol de use cases)
    ├── shared/
    │   └── code_preview_addon.dart              ← Addon de code preview (crear una sola vez)
    ├── ui_system/                               ← Componentes del Design System
    │   └── [atoms|molecules|organisms|components]/
    │       └── [nombre_widget]/
    │           └── [nombre_widget].use_case.dart
    ├── features/                                ← Pantallas
    │   └── [nombre_feature]/
    │       └── [nombre_screen]/
    │           └── [nombre_screen].use_case.dart
    └── shared/                                  ← Widgets del catálogo
```

**Ejemplo concreto de features:**
```
widgetbook/lib/features/
├── auth/
│   ├── login_screen/
│   │   └── login_screen.use_case.dart
│   └── register_screen/
│       └── register_screen.use_case.dart
├── home/
│   └── home_screen/
│       └── home_screen.use_case.dart
└── profile/
    └── profile_screen/
        └── profile_screen.use_case.dart
```

---

## Reglas de generación

- El **tema se inyecta globalmente** — nunca envolver con `Theme(...)` ni `MaterialApp(...)`.
- Los **colores deben venir del tema** — usar `Theme.of(context).colorScheme` en vez de `Colors.white`, `Color(0xFF...)` o cualquier color hardcodeado. Solo así el tema Dark/Light se aplica correctamente.
- Los **use cases de UI System** (atoms, molecules, organisms, components —  todo excepto templates) deben envolver el widget en un `ColoredBox` con el color de fondo correcto según el tema activo, para que el componente se vea siempre sobre el fondo real de la app independientemente del canvas de Widgetbook:

  ```dart
  final isDark = Theme.of(context).brightness == Brightness.dark;
  return ColoredBox(
    color: isDark ? AppColors.primary900 : AppColors.primary0,
    child: Center(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: <TuWidget>(...),
      ),
    ),
  );
  ```

  > **No aplicar a templates ni a Features:** los templates ya definen su propio layout a pantalla completa; las pantallas de Features incluyen su propio `Scaffold`.
- Los **callbacks** siempre usan `print()` descriptivo — nunca `() {}` vacíos.
- Los **iconos e imágenes** (PNG, JPEG, SVG) requieren que sus paths estén declarados en `widgetbook_[appname]/pubspec.yaml` bajo `flutter.assets`. Para imágenes de red usar `NetworkImage`. Para `IconData` usar `context.knobs.list` con un conjunto curado. Ver `assets/knobs_reference.md` § Iconos e imágenes.
- Los **datos mock y valores iniciales deben reflejar el dominio del proyecto** — antes de generar un use case, analizar el contexto de la app (fintech, e-commerce, salud, educación, etc.) y usar nombres, valores y escenarios coherentes con ese dominio. Nunca usar "lorem ipsum", "text", "value", "test" ni datos genéricos.
- Las **dependencias externas** (providers, servicios, repositorios) se resuelven con una de las dos estrategias documentadas en la sección "Mocking de dependencias": **Extracción** (preferida para componentes) o **Mocking con librería** (para pantallas completas). Ver sección completa para ejemplos de código.
- Los **mocks se declaran a nivel de archivo** usando `mocktail` (`class MockX extends Mock implements X {}`), nunca dentro del método del use case. Los valores stubeados se conectan a knobs siempre que sea útil para la exploración interactiva.
- Los **objetos de dominio complejos** (modelos con muchos campos) se instancian con valores realistas del dominio. Si el constructor es muy largo, marcar con `// TODO: ajustar campos opcionales según el caso`.
- El **código es autodocumentado** — sin comentarios descriptivos innecesarios.
- Los archivos `.use_case.dart` **nunca** llevan `part '*.g.dart'`.
- **Cada use case llama `context.setCodePreview(...)`** antes de retornar el widget, con la instanciación del constructor usando los valores actuales de los knobs interpolados. El panel de código se actualiza en tiempo real.

---

## Archivos de referencia

| Qué hacer | Referencia |
|---|---|
| Setup desde cero o actualizar dependencias | `references/setup.md` |
| Setup en monorepo (single o per-package) | `references/monorepo.md` |
| Detectar estructura y ubicar archivos | `references/project_structure.md` |
| Decidir variantes para componentes | `references/variants_guide.md` |
| Decidir variantes para pantallas/features | `references/features_guide.md` |
| Mockear providers, servicios y repositorios en use cases | `references/mocks.md` |
| Elegir el knob correcto por tipo de parámetro | `assets/knobs_reference.md` |
| Iconos, SVG, PNG, JPEG en use cases | `assets/knobs_reference.md` § Iconos e imágenes + `references/setup.md` § Assets |
| Tema Dark/Light no se aplica | `references/setup.md` § Troubleshooting |
| Fondo del canvas incorrecto en un componente | `references/setup.md` § Fondo del canvas — ColoredBox |
| Detectar componentes y pantallas sin use case (gaps de cobertura) | `references/coverage_audit.md` |

---

## Checklist antes de entregar

### Compartido (UI System y Features)
- [ ] Modo detectado correctamente: setup / monorepo / agregar componente / agregar feature / actualizar / auditoría de cobertura
- [ ] Si el modo es auditoría: se escanearon componentes en `lib/` y pantallas en `lib/features/` (o equivalente), se cruzaron con `widgetbook_[appname]/lib/ui_system/` y `widgetbook_[appname]/lib/features/`, y se presentó el reporte de cobertura antes de generar cualquier use case (ver `references/coverage_audit.md`)
- [ ] Si es monorepo: estrategia elegida (single widgetbook o per-package) y `pubspec.yaml` con paths correctos
- [ ] Si es setup: `references/setup.md` completado antes de continuar
- [ ] Carpetas `widgetbook_[appname]/lib/ui_system/` y `widgetbook_[appname]/lib/features/` existen (si no, crearlas)
- [ ] Clasificación correcta: UI System (componente) o Feature (pantalla)
- [ ] Firma del método es exactamente `Widget build[X]UseCase(BuildContext context)`
- [ ] `name` en `@UseCase` es único dentro del mismo `type`
- [ ] Datos mock y valores iniciales coherentes con el dominio del proyecto
- [ ] Callbacks tienen `print()` descriptivo
- [ ] Hay variante para el estado default
- [ ] Objetos complejos tienen `// TODO`
- [ ] No hay colores hardcodeados — usa `Theme.of(context).colorScheme` para adaptarse a Dark/Light
- [ ] Si el use case usa assets (iconos SVG, PNG, JPEG): paths declarados en `widgetbook_[appname]/pubspec.yaml` bajo `flutter.assets`
- [ ] Si el use case usa imágenes de red: se usa `NetworkImage` o `Image.network` — no requiere declarar assets
- [ ] Code preview: `shared/code_preview_addon.dart` creado y `CodePreviewAddon` registrado en `main.dart`
- [ ] Cada use case importa `code_preview_addon.dart` y llama `context.setCodePreview(...)` con la instanciación del widget
- [ ] El use case retorna **solo el widget puro** — sin paneles de código embebidos dentro del widget
- [ ] El archivo se ubica en la carpeta correcta según la estructura del proyecto
- [ ] Se ejecutó `dart analyze lib/ui_system lib/features lib/shared` (o equivalente) dentro de `widgetbook_[appname]/` y no hay ningún `error` en los archivos `.use_case.dart` ni en `shared/` — los errores de `main.dart` se ignoran en este paso
- [ ] Se ejecutó `cd widgetbook_[appname] && dart run build_runner build --delete-conflicting-outputs`
- [ ] `main.directories.g.dart` se generó sin errores
- [ ] El nuevo use case aparece en `main.directories.g.dart`
- [ ] Los archivos `.use_case.dart` **NO** tienen `part '*.g.dart'`

### Específico UI System (componentes)
- [ ] Todos los parámetros requeridos cubiertos con knobs
- [ ] Parámetros visuales y de comportamiento usan knobs
- [ ] Los estados `loading`, `disabled`, `empty`, `error` están cubiertos: como **knob** si son parámetros del constructor, como `@UseCase` separado solo si producen una estructura visual radicalmente distinta (ver `references/variants_guide.md` § Regla de oro)
- [ ] El widget está envuelto en `ColoredBox(color: isDark ? AppColors.primary900 : AppColors.primary0, ...)` para que se vea sobre el fondo correcto en cualquier modo de tema — **excepto templates** (que definen su propio layout a pantalla completa)

### Específico Features (pantallas)
- [ ] Estrategia de mocking elegida: Extracción o Mocking con librería (ver sección "Mocking de dependencias")
- [ ] Si se usa `mocktail`: agregado a `dependencies` en `widgetbook_[appname]/pubspec.yaml` y ejecutado `flutter pub get`
- [ ] Mocks declarados a nivel de archivo (`class MockX extends Mock implements X {}`), fuera del método del use case
- [ ] Todos los providers/servicios stubeados con `when(...)` usando valores conectados a knobs donde sea útil
- [ ] Hay variantes para estados de la pantalla: default, loading, empty, error (si aplica)
- [ ] Los datos mock reflejan un escenario realista completo del flujo del dominio
- [ ] La pantalla no depende de rutas ni navegación real — se renderiza de forma aislada
- [ ] Si hay múltiples providers: se usa `MultiProvider` en el use case
