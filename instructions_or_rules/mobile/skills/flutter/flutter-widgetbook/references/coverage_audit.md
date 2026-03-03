# Auditoría de Cobertura — Detectar Gaps en el Widgetbook

Verifica qué componentes y pantallas del proyecto principal **no están catalogados** en el
widgetbook. Úsalo al incorporar un widgetbook existente a un proyecto con componentes ya creados,
o periódicamente para detectar nuevos widgets/pantallas que se agregaron después del setup inicial.

---

## Cuándo ejecutar la auditoría

| Situación | Acción |
|---|---|
| Se incorporó widgetbook a un proyecto con componentes existentes | Auditar UI System completo |
| Se agregaron nuevas pantallas al proyecto y no se catalogaron | Auditar Features |
| El usuario pide "verifica qué falta en el widgetbook" / "qué componentes no están" | Auditoría completa |
| Se actualizó el Design System y pueden existir componentes nuevos | Auditar UI System |
| Se quiere saber la cobertura actual antes de una entrega | Auditoría completa |

---

## Proceso de auditoría — paso a paso

### Paso 1 — Escanear el proyecto principal

#### Para UI System (componentes)

Buscar todos los archivos de widgets del Design System en la app principal. Las ubicaciones típicas son:

```
lib/core/widgets/
lib/shared/widgets/
lib/design_system/
lib/ui/
lib/components/
lib/common/widgets/
lib/widgets/
lib/atoms/
lib/molecules/
lib/organisms/
```

Buscar archivos que:
- Terminen en `_widget.dart`, `_button.dart`, `_card.dart`, `_field.dart`, `_badge.dart`, `_tile.dart`, `_chip.dart`, `_icon.dart`, `_avatar.dart`, `_text.dart`
- Estén dentro de carpetas nombradas `atoms/`, `molecules/`, `organisms/`, `components/`, `widgets/`
- Exporten clases que extiendan `StatelessWidget` o `StatefulWidget`

**Comando de exploración:**
```bash
# Encontrar todos los archivos de widgets en el proyecto principal
find lib -name "*.dart" -path "*/widgets/*" -o \
         -name "*_widget.dart" -o \
         -name "*_button.dart" -o \
         -name "*_card.dart" -o \
         -name "*_field.dart" -o \
         -name "*_badge.dart" | sort
```

#### Para Features (pantallas)

Buscar pantallas en las ubicaciones típicas:

```
lib/features/**/presentation/
lib/features/**/*_screen.dart
lib/features/**/*_page.dart
lib/screens/
lib/pages/
lib/presentation/
```

**Comando de exploración:**
```bash
# Encontrar todas las pantallas del proyecto principal
find lib -name "*_screen.dart" -o \
         -name "*_page.dart" -o \
         -name "*_view.dart" | grep -v widgetbook | sort
```

---

### Paso 2 — Escanear el widgetbook actual

#### Use cases de UI System ya catalogados

```bash
# Ver qué componentes ya tienen use case
find widgetbook_[appname]/lib/ui_system -name "*.use_case.dart" | sort
```

#### Use cases de Features ya catalogados

```bash
# Ver qué pantallas ya tienen use case
find widgetbook_[appname]/lib/features -name "*.use_case.dart" | sort
```

---

### Paso 3 — Cruzar y detectar gaps

Comparar los resultados de los pasos 1 y 2:

**Para cada componente encontrado en el proyecto principal:**
- Derivar el nombre del widget (clase Dart) del nombre del archivo
- Buscar si existe `[nombre].use_case.dart` en `widgetbook_[appname]/lib/ui_system/`
- Si NO existe → **gap detectado** → agregar a la lista de pendientes

**Para cada pantalla encontrada en el proyecto principal:**
- Derivar el nombre de la clase del nombre del archivo
- Buscar si existe `[nombre].use_case.dart` en `widgetbook_[appname]/lib/features/`
- Si NO existe → **gap detectado** → agregar a la lista de pendientes

---

### Paso 4 — Reportar el resultado antes de generar

Antes de crear cualquier use case, presentar el reporte de cobertura al usuario:

```
## Reporte de cobertura — Widgetbook

### UI System
| Componente         | Archivo fuente                              | En widgetbook |
|--------------------|---------------------------------------------|---------------|
| PrimaryButton      | lib/core/widgets/primary_button.dart        | ✅ Catalogado  |
| AppTextField       | lib/core/widgets/app_text_field.dart        | ✅ Catalogado  |
| StatusBadge        | lib/shared/widgets/status_badge.dart        | ❌ Falta       |
| ProductCard        | lib/features/catalog/widgets/product_card.dart | ❌ Falta    |

Cobertura UI System: 2/4 (50%)

### Features
| Pantalla           | Archivo fuente                              | En widgetbook |
|--------------------|---------------------------------------------|---------------|
| LoginScreen        | lib/features/auth/login_screen.dart         | ✅ Catalogado  |
| HomeScreen         | lib/features/home/home_screen.dart          | ✅ Catalogado  |
| ProfileScreen      | lib/features/profile/profile_screen.dart    | ❌ Falta       |
| CheckoutScreen     | lib/features/checkout/checkout_screen.dart  | ❌ Falta       |
| OrderDetailScreen  | lib/features/orders/order_detail_screen.dart| ❌ Falta       |

Cobertura Features: 2/5 (40%)

### Resumen
- UI System: 2 faltantes → StatusBadge, ProductCard
- Features: 3 faltantes → ProfileScreen, CheckoutScreen, OrderDetailScreen
- Total gaps: 5 use cases por crear
```

> **Regla:** Siempre mostrar el reporte completo antes de comenzar a generar. Nunca crear
> use cases en silencio sin informar primero el estado de cobertura.

---

### Paso 5 — Priorizar y generar los gaps

Después del reporte, preguntar al usuario (si no es claro) en qué orden priorizar,
o proceder con todos si el usuario lo indica.

Para cada gap, seguir el proceso estándar según el tipo:

- **Componentes faltantes** → seguir `references/project_structure.md` + `references/variants_guide.md`
- **Pantallas faltantes** → seguir `references/features_guide.md`

Después de crear todos los use cases faltantes:

```bash
cd widgetbook_[appname] && dart run build_runner build --delete-conflicting-outputs
```

---

### Paso 6 — Verificar cobertura post-generación

Después del `build_runner`, repetir el escaneo y confirmar que los gaps ya no existen:

```bash
# Confirmar que el árbol de directorios incluye todos los nuevos use cases
grep -E "name:|type:" widgetbook_[appname]/lib/main.directories.g.dart | sort
```

Presentar el reporte actualizado comparando con el anterior.

---

## Señales de que un elemento debe excluirse de la auditoría

No todos los archivos `.dart` en carpetas de widgets deben catalogarse. Excluir:

| Archivo | Motivo |
|---|---|
| `*_mixin.dart` | Mixin, no widget renderizable |
| `*_extension.dart` | Extension, no widget |
| `*_theme.dart` | Tema/tokens de diseño, no widget |
| `*_model.dart` / `*_entity.dart` | Modelo de datos |
| `*_provider.dart` / `*_bloc.dart` / `*_cubit.dart` | State management |
| `*_service.dart` / `*_repository.dart` | Servicios |
| `index.dart` / `barrel.dart` | Barrel files (re-exports) |
| Widgets privados (`_MyWidget`) | Clases internas, no exportadas |
| Widgets de layout genérico que no tienen variantes visuales propias | Wrappers sin props públicas |

---

## Auditoría incremental — detectar cambios nuevos

Para proyectos que ya tienen widgetbook establecido, detectar solo lo agregado recientemente:

```bash
# Ver archivos de widgets modificados o creados en los últimos 30 días
find lib -name "*.dart" -newer widgetbook_[appname]/lib/main.dart \
  \( -path "*/widgets/*" -o -name "*_screen.dart" -o -name "*_page.dart" \) | sort
```

Este comando compara la fecha de modificación de los archivos con la del `main.dart` del
widgetbook, encontrando todo lo agregado después de la última vez que se actualizó el catálogo.

---

## Plantilla de reporte rápido

Usar esta plantilla al reportar antes de crear use cases:

```markdown
## Auditoría Widgetbook — [nombre del proyecto]

**UI System** — X/Y catalogados (Z%)
- ✅ [ComponenteA] → ya tiene use case
- ✅ [ComponenteB] → ya tiene use case
- ❌ [ComponenteC] → falta use case → `lib/ruta/componente_c.dart`
- ❌ [ComponenteD] → falta use case → `lib/ruta/componente_d.dart`

**Features** — X/Y catalogadas (Z%)
- ✅ [ScreenA] → ya tiene use case
- ❌ [ScreenB] → falta use case → `lib/features/feature/screen_b.dart`
- ❌ [ScreenC] → falta use case → `lib/features/feature/screen_c.dart`

**Acción propuesta:** Crear los N use cases faltantes. ¿Procedo con todos o prefieres priorizar alguno?
```
