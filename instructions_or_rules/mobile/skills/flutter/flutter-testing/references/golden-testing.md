# Golden Testing Reference

Golden tests verifican la renderización visual correcta de widgets, detectando regresiones visuales.

## ¿Qué es Golden Testing?

Golden tests comparan capturas de pantalla (screenshots) de widgets con una "golden" (imagen de referencia). Si el widget renderiza diferente, el test falla.

### Casos de Uso

| Caso | ✅ Hacer | ❌ Evitar |
|---|---|---|
| Botones customizados | Sí | Verificar color exacto en matchers (demasiado frágil) |
| Cards complejas | Sí | Componentes triviales |
| Estados de formulario | Sí | Material widgets sin customización |
| Temas especiales | Sí | Tests de animaciones con golden |
| Textos largos con overflow | Sí | Widgets que cambian por versión de SO |

## Configuración

```yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
  # No requiere dependencias adicionales
```

### Estructura de Carpetas

```
test/
├── golden/
│   ├── goldens/
│   │   ├── custom_button.png
│   │   ├── user_card.png
│   │   └── login_form.png
│   └── widget_test.dart
```

## Implementación Básica

```dart
// test/golden/custom_button_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:my_app/widgets/custom_button.dart';

void main() {
  group('CustomButton Golden Tests', () {
    testWidgets('CustomButton default state', (WidgetTester tester) async {
      // Arrange
      await tester.binding.window.physicalSizeTestValue = Size(400, 200);
      addTearDown(tester.binding.window.clearPhysicalSizeTestValue);

      // Act
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: Center(
              child: CustomButton(
                label: 'Click me',
                onPressed: () {},
              ),
            ),
          ),
        ),
      );

      // Assert - Comparar con golden
      await expectLater(
        find.byType(CustomButton),
        matchesGoldenFile('goldens/custom_button.png'),
      );
    });

    testWidgets('CustomButton disabled state', (WidgetTester tester) async {
      // Arrange
      await tester.binding.window.physicalSizeTestValue = Size(400, 200);
      addTearDown(tester.binding.window.clearPhysicalSizeTestValue);

      // Act
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: Center(
              child: CustomButton(
                label: 'Disabled',
                onPressed: null,  // null = disabled
              ),
            ),
          ),
        ),
      );

      // Assert
      await expectLater(
        find.byType(CustomButton),
        matchesGoldenFile('goldens/custom_button_disabled.png'),
      );
    });

    testWidgets('CustomButton loading state', (WidgetTester tester) async {
      // Arrange
      await tester.binding.window.physicalSizeTestValue = Size(400, 200);
      addTearDown(tester.binding.window.clearPhysicalSizeTestValue);

      // Act
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: Center(
              child: CustomButton(
                label: 'Loading',
                isLoading: true,
                onPressed: () {},
              ),
            ),
          ),
        ),
      );

      // Assert
      await expectLater(
        find.byType(CustomButton),
        matchesGoldenFile('goldens/custom_button_loading.png'),
      );
    });
  });
}
```

## Patrones Avanzados

### 1. Testing de Tarjetas Complejas

```dart
void main() {
  group('UserCard Golden Tests', () {
    testWidgets('UserCard with complete data', (tester) async {
      // Arrange
      await tester.binding.window.physicalSizeTestValue = Size(400, 250);
      addTearDown(tester.binding.window.clearPhysicalSizeTestValue);

      final user = User(
        id: '123',
        name: 'John Doe',
        email: 'john@example.com',
        avatar: 'https://example.com/avatar.jpg',
        isActive: true,
      );

      // Act
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: UserCard(user: user),
          ),
        ),
      );

      // Assert
      await expectLater(
        find.byType(UserCard),
        matchesGoldenFile('goldens/user_card_complete.png'),
      );
    });

    testWidgets('UserCard with long text overflow', (tester) async {
      // Arrange
      await tester.binding.window.physicalSizeTestValue = Size(300, 250);
      addTearDown(tester.binding.window.clearPhysicalSizeTestValue);

      final user = User(
        id: '123',
        name: 'John Doe with a very long name that might overflow',
        email: 'john.doe.with.long.email.name@verylongdomainexample.com',
        isActive: true,
      );

      // Act
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: UserCard(user: user),
          ),
        ),
      );

      // Assert
      await expectLater(
        find.byType(UserCard),
        matchesGoldenFile('goldens/user_card_overflow.png'),
      );
    });

    testWidgets('UserCard inactive state', (tester) async {
      // Arrange
      await tester.binding.window.physicalSizeTestValue = Size(400, 250);
      addTearDown(tester.binding.window.clearPhysicalSizeTestValue);

      final user = User(
        id: '123',
        name: 'John Doe',
        email: 'john@example.com',
        isActive: false,  // Inactivo
      );

      // Act
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: UserCard(user: user),
          ),
        ),
      );

      // Assert
      await expectLater(
        find.byType(UserCard),
        matchesGoldenFile('goldens/user_card_inactive.png'),
      );
    });
  });
}
```

### 2. Testing de Formularios

```dart
void main() {
  group('LoginForm Golden Tests', () {
    testWidgets('LoginForm initial state', (tester) async {
      // Arrange
      await tester.binding.window.physicalSizeTestValue = Size(400, 600);
      addTearDown(tester.binding.window.clearPhysicalSizeTestValue);

      // Act
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: LoginForm(),
          ),
        ),
      );

      // Assert
      await expectLater(
        find.byType(LoginForm),
        matchesGoldenFile('goldens/login_form_empty.png'),
      );
    });

    testWidgets('LoginForm with validation errors', (tester) async {
      // Arrange
      await tester.binding.window.physicalSizeTestValue = Size(400, 600);
      addTearDown(tester.binding.window.clearPhysicalSizeTestValue);

      // Act
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: LoginForm(),
          ),
        ),
      );

      // Llenar con datos inválidos y validar
      await tester.enterText(find.byKey(Key('email')), 'invalid');
      await tester.tap(find.byKey(Key('submit')));
      await tester.pump();

      // Assert
      await expectLater(
        find.byType(LoginForm),
        matchesGoldenFile('goldens/login_form_errors.png'),
      );
    });

    testWidgets('LoginForm with loading indicator', (tester) async {
      // Arrange
      await tester.binding.window.physicalSizeTestValue = Size(400, 600);
      addTearDown(tester.binding.window.clearPhysicalSizeTestValue);

      // Act
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: LoginForm(isLoading: true),
          ),
        ),
      );

      // Assert
      await expectLater(
        find.byType(LoginForm),
        matchesGoldenFile('goldens/login_form_loading.png'),
      );
    });
  });
}
```

### 3. Testing de Temas

```dart
void main() {
  group('Widget Theme Golden Tests', () {
    testWidgets('CustomButton in light theme', (tester) async {
      // Arrange
      await tester.binding.window.physicalSizeTestValue = Size(400, 200);
      addTearDown(tester.binding.window.clearPhysicalSizeTestValue);

      // Act
      await tester.pumpWidget(
        MaterialApp(
          theme: ThemeData.light(),
          home: Scaffold(
            body: Center(
              child: CustomButton(label: 'Light Theme', onPressed: () {}),
            ),
          ),
        ),
      );

      // Assert
      await expectLater(
        find.byType(CustomButton),
        matchesGoldenFile('goldens/custom_button_light.png'),
      );
    });

    testWidgets('CustomButton in dark theme', (tester) async {
      // Arrange
      await tester.binding.window.physicalSizeTestValue = Size(400, 200);
      addTearDown(tester.binding.window.clearPhysicalSizeTestValue);

      // Act
      await tester.pumpWidget(
        MaterialApp(
          theme: ThemeData.dark(),
          home: Scaffold(
            body: Center(
              child: CustomButton(label: 'Dark Theme', onPressed: () {}),
            ),
          ),
        ),
      );

      // Assert
      await expectLater(
        find.byType(CustomButton),
        matchesGoldenFile('goldens/custom_button_dark.png'),
      );
    });
  });
}
```

### 4. Testing de Diferentes Tamaños de Pantalla

```dart
void main() {
  group('Responsive Golden Tests', () {
    testWidgets('Dashboard on phone (400x800)', (tester) async {
      // Arrange
      await tester.binding.window.physicalSizeTestValue = Size(400, 800);
      addTearDown(tester.binding.window.clearPhysicalSizeTestValue);

      // Act
      await tester.pumpWidget(MyApp());
      await tester.pumpAndSettle();

      // Assert
      await expectLater(
        find.byType(Dashboard),
        matchesGoldenFile('goldens/dashboard_phone.png'),
      );
    });

    testWidgets('Dashboard on tablet (1200x800)', (tester) async {
      // Arrange
      await tester.binding.window.physicalSizeTestValue = Size(1200, 800);
      addTearDown(tester.binding.window.clearPhysicalSizeTestValue);

      // Act
      await tester.pumpWidget(MyApp());
      await tester.pumpAndSettle();

      // Assert
      await expectLater(
        find.byType(Dashboard),
        matchesGoldenFile('goldens/dashboard_tablet.png'),
      );
    });
  });
}
```

## Crear y Actualizar Golden Files

### Crear Nuevos Golden Files

```bash
# Crear nuevos archivos golden (se crearán en test/goldens/)
flutter test --update-goldens test/golden/custom_button_test.dart
```

### Actualizar Golden Files Existentes

```bash
# Actualizar todos los archivos golden
flutter test --update-goldens

# Actualizar golden files específicos
flutter test --update-goldens test/golden/custom_button_test.dart
```

### Verificar Cambios

```bash
# Ver qué golden files fueron creados/modificados
git diff test/golden/goldens/

# Revisar cambios visuales antes de commit
# (Usar cliente Git con vista de imágenes, GitKraken, Tower, etc.)
```

## Testing de Iconografía y Gráficos

```dart
void main() {
  group('Icon Golden Tests', () {
    testWidgets('Icon collection colors', (tester) async {
      // Arrange
      await tester.binding.window.physicalSizeTestValue = Size(400, 600);
      addTearDown(tester.binding.window.clearPhysicalSizeTestValue);

      // Act
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: Wrap(
              children: [
                Icon(Icons.add, color: Colors.red),
                Icon(Icons.edit, color: Colors.blue),
                Icon(Icons.delete, color: Colors.orange),
                Icon(Icons.check, color: Colors.green),
              ],
            ),
          ),
        ),
      );

      // Assert
      await expectLater(
        find.byType(Wrap),
        matchesGoldenFile('goldens/icon_colors.png'),
      );
    });
  });
}
```

## Mejores Prácticas

### ✅ Usar Golden Tests Para:

- Componentes visualmente complejos
- Estados de UI distintos (normal, disabled, loading, error)
- Cambios en temas
- Validación post-refactoring visual
- Widgets customizados

### ❌ NO Usar Golden Tests Para:

- Comportamiento funcional (usar Widget Tests)
- Widgets de terceros
- Contenido dinámico que cambia (usar matchers)
- Animaciones (muy frágiles)
- Widgets que dependen de dispositivo

## Regresiones Visuales

### Detectar Cambios Intencionales

```bash
# Si un test falla porque cambió el widget propositalmente:

# 1. Verificar la carpeta failure/
screenshots/failures/custom_button.png

# 2. Comparar con el golden original
# 3. Si los cambios son deseados, actualizar:
flutter test --update-goldens test/golden/custom_button_test.dart

# 4. Revisar con git diff
git diff test/golden/goldens/custom_button.png

# 5. Commit
git add test/golden/goldens/
git commit -m "Update golden tests: CustomButton styling"
```

### Tratar Cambios No Intencionales

```bash
# Un golden test falló sin motivo aparente:

# 1. Revisar que no haya cambios en el código
git status

# 2. Verificar versión de Flutter
flutter --version

# 3. Si hay cambios reales sin querer, revertir
git checkout test/golden/goldens/custom_button.png

# 4. O restaurar desde control de versiones
git reset HEAD test/golden/goldens/

# 5. Investigar cambios recientes
git log --oneline test/presentation/widgets/custom_button.dart
```

## Integración en CI/CD

```yaml
# .github/workflows/golden-tests.yml
name: Golden Tests

on: [pull_request]

jobs:
  golden-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0  # Necesario para comparar con main
      
      - name: Setup Flutter
        uses: subosito/flutter-action@v2
      
      - name: Get dependencies
        run: flutter pub get
      
      - name: Run golden tests
        run: flutter test test/golden/
      
      - name: Upload failures on failure
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: golden-test-failures
          path: test/failures/
```

## Versionamiento de Golden Files

```bash
# Los archivos golden deben estar en el repositorio
# y versionados con git

# Estructura recomendada
test/
├── golden/
│   ├── goldens/              # Archivos de referencia (git tracked)
│   │   ├── custom_button.png
│   │   └── user_card.png
│   ├── failures/             # Fallos (git ignored)
│   └── widget_test.dart

# .gitignore
test/golden/failures/  # No versionear fallos
```

## Herramientas Útiles

### Comparar Golden Files

```bash
# macOS
open test/golden/goldens/custom_button.png
open test/golden/failures/custom_button.png

# Herramienta de diff
diff <(identify -version)

# O usar un diff visual
git difftool test/golden/goldens/custom_button.png
```

## Checklist para Golden Tests

- [ ] Solo widgets visualmente complejos
- [ ] Todas las variantes de estado cubiertas
- [ ] Archivos golden en repositorio
- [ ] Failures folder en .gitignore
- [ ] Tamaños de pantalla considerados
- [ ] Temas (light/dark) cubiertos
- [ ] Sin dependencias de datos dinámicos
- [ ] Integración en CI/CD
- [ ] Documentación de cambios visuales esperados
