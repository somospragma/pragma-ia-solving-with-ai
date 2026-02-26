# Widget Testing Reference

Guía detallada para pruebas de widgets en Flutter. Widget tests validan renderizado, interacción y comportamiento de UI sin ejecutar la app completa.

## Ventajas del Widget Testing

| Aspecto | Unit Test | Widget Test | Integration Test |
|---|---|---|---|
| Velocidad | ⚡⚡⚡ | ⚡⚡ | 🐢 |
| Realismo | Bajo | Medio-Alto | Alto |
| Aislamiento | Total | Parcial | Nulo |
| UI Testing | ❌ | ✅ | ✅ |
| Ideal para | Lógica | Componentes | Flujos E2E |

## Configuración

```yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
  mocktail: ^1.0.0
  bloc_test: ^9.1.0
```

## Estructura de Carpetas

```
test/
├── presentation/
│   ├── widgets/
│   │   ├── custom_button_test.dart
│   │   ├── user_card_test.dart
│   │   └── form_input_test.dart
│   ├── pages/
│   │   ├── home_page_test.dart
│   │   ├── detail_page_test.dart
│   │   └── login_page_test.dart
│   └── fixtures/
│       └── test_widget.dart
```

## Conceptos Fundamentales

### WidgetTester

```dart
testWidgets('description', (WidgetTester tester) async {
  // tester proporciona métodos para interactuar con widgets
  await tester.pumpWidget(...);     // Renderizar widget
  await tester.tap(find.byText('Button'));  // Simular tap
  await tester.enterText(find.byKey(Key('input')), 'text');  // Input
  await tester.pumpAndSettle();     // Esperar animaciones
});
```

## WidgetTester Lifecycle: pump() vs pumpAndSettle()

### Explicación Oficial

Flutter renderiza frames en ciclos. El timing es crítico para tests:

- **pump()**: Avanza 1 frame. Para cambios de estado inmediatos (setState)
- **pump(Duration)**: Avanza N milisegundos a través de frames (para animations parciales)
- **pumpAndSettle()**: Repite pump() hasta que NO HAY más frames (timeout 10s default)

### El Problema Real de pumpAndSettle()

```
⚠️ NUNCA uses pumpAndSettle() si NO SABES cuándo termina la animación
→ Resultado: TimeoutException después de 10 segundos esperando algo que NUNCA se detiene
```

### Decisión Rápida: Cuándo Usar Cada Una

**pump()** → setState finalizó en este frame:
```dart
await tester.tap(find.byIcon(Icons.add));
await tester.pump(); // Renderiza cambio de contador
expect(find.text('1'), findsOneWidget); // PASA
```

**pump(Duration)** → Necesitas frame anterior de animación (testing parcial):
```dart
await tester.tap(find.byType(FloatingActionButton));
await tester.pump(const Duration(milliseconds: 500)); // 50% de animación
// Verificar estado intermedio
expect(opacityOf(find.byType(MyWidget)), lessThan(1.0));
```

**pumpAndSettle()** → Animación con duración DESCONOCIDA (solo para dismiss/transitions):
```dart
// Drag con dismiss animation de duración variable
await tester.drag(find.byType(Dismissible), const Offset(500, 0));
await tester.pumpAndSettle(); // Espera a que termine (típicamente 200-500ms)
expect(find.text('Item'), findsNothing); // Item desapareció
```

### Error Común

```dart
// ❌ INCORRECTO: pumpAndSettle() en app normal
testWidgets('Wrong timing', (tester) async {
  await tester.pumpWidget(MyApp());
  await tester.pumpAndSettle(); // FALLA: App nunca "settles"
  // → TimeoutException después de 10s
});

// ✅ CORRECTO: pump() después de setState
testWidgets('Correct timing', (tester) async {
  await tester.pumpWidget(MyApp());
  await tester.pump(); // Single frame para rendering inicial
});

// ✅ CORRECTO: pumpAndSettle() solo para animaciones desconocidas
testWidgets('Dismiss animation', (tester) async {
  await tester.pumpWidget(MyApp());
  await tester.drag(find.byType(Dismissible), const Offset(500, 0));
  await tester.pumpAndSettle(); // Okay: dismiss tiene duración conocida
});
```

### Para AI Agents

```
IF duración_animación = DESCONOCIDA → pumpAndSettle()
IF duración_animación = CONOCIDA     → pump(Duration)
IF cambio_setState_inmediato         → pump()
IF duda                              → pump() y revisar si falla
```

### Ciclo de Vida en Widget Tests

```dart
testWidgets('widget lifecycle', (WidgetTester tester) async {
  // 1. ARRANGE: Construir el widget
  await tester.pumpWidget(
    MaterialApp(
      home: MyWidget(),
    ),
  );
  
  // 2. ACT: Realizar acciones
  await tester.tap(find.byType(ElevatedButton));
  await tester.pump();  // Procesar frame
  await tester.pumpAndSettle();  // Esperar animaciones
  
  // 3. ASSERT: Verificar resultado
  expect(find.text('Updated Text'), findsOneWidget);
});
```

## Finding Widgets

### Métodos Principales

```dart
// finder es el objeto que busca widgets en el árbol

// Por tipo
find.byType(ElevatedButton)

// Por texto
find.text('Click me')
find.textContaining('Click')  // Búsqueda parcial

// Por clave
find.byKey(Key('my-button'))
find.byKey(ValueKey('unique-id'))

// Por propiedad de widget
find.byWidgetPredicate((widget) => 
  widget is Text && widget.data?.contains('Error') ?? false
)

// Combinaciones
find.byType(Column).first
find.byType(Column).last
find.byType(Column).at(0)

// Ancestros y descendientes
find.ancestor(of: find.byKey(Key('child')), matching: find.byType(Row))
find.descendant(of: find.byType(ListView), matching: find.byType(ListTile))
```

### Verificar Encontrados

```dart
expect(find.text('Hello'), findsOneWidget);           // Exactamente 1
expect(find.text('Item'), findsWidgets);              // 1 o más
expect(find.text('Missing'), findsNothing);           // 0
expect(find.text('Item'), findsNWidgets(3));          // Exactamente 3
expect(find.byType(Button), findsWidgetCount(5));     // Exactamente 5
```

## Patrones de Testing Comunes

### 1. Testing de Widgets Simples

```dart
void main() {
  group('CustomButton', () {
    testWidgets('should render with correct text', (tester) async {
      // Arrange
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomButton(
              label: 'Press me',
              onPressed: () {},
            ),
          ),
        ),
      );

      // Assert
      expect(find.text('Press me'), findsOneWidget);
      expect(find.byType(ElevatedButton), findsOneWidget);
    });

    testWidgets('should call onPressed when tapped', (tester) async {
      // Arrange
      bool pressed = false;
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomButton(
              label: 'Press me',
              onPressed: () => pressed = true,
            ),
          ),
        ),
      );

      // Act
      await tester.tap(find.byType(ElevatedButton));
      await tester.pump();  // Procesar cambios

      // Assert
      expect(pressed, true);
    });

    testWidgets('should be disabled when loading', (tester) async {
      // Arrange
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomButton(
              label: 'Loading...',
              isLoading: true,
              onPressed: () {},
            ),
          ),
        ),
      );

      // Act & Assert
      final button = find.byType(ElevatedButton);
      expect(button, findsOneWidget);
      // Verificar que el botón está deshabilitado
      final ElevatedButton widget = tester.widget(button);
      expect(widget.onPressed, null);
    });
  });
}
```

### 2. Testing de Formularios

```dart
testWidgets('should validate email input', (tester) async {
  // Arrange
  await tester.pumpWidget(
    MaterialApp(
      home: LoginForm(),
    ),
  );

  // Act - Email inválido
  await tester.enterText(
    find.byKey(Key('email_field')),
    'invalid-email',
  );
  await tester.tap(find.byKey(Key('submit_button')));
  await tester.pump();

  // Assert
  expect(find.text('Please enter a valid email'), findsOneWidget);
});

testWidgets('should submit form with valid data', (tester) async {
  // Arrange
  bool formSubmitted = false;
  
  await tester.pumpWidget(
    MaterialApp(
      home: LoginForm(
        onSubmit: (email, password) => formSubmitted = true,
      ),
    ),
  );

  // Act
  await tester.enterText(find.byKey(Key('email_field')), 'user@example.com');
  await tester.enterText(find.byKey(Key('password_field')), 'password123');
  await tester.tap(find.byKey(Key('submit_button')));
  await tester.pumpAndSettle();

  // Assert
  expect(formSubmitted, true);
});

testWidgets('should clear form on reset', (tester) async {
  // Arrange
  await tester.pumpWidget(
    MaterialApp(
      home: LoginForm(),
    ),
  );

  // Act - Ingresar datos
  await tester.enterText(find.byKey(Key('email_field')), 'test@example.com');
  await tester.enterText(find.byKey(Key('password_field')), 'password');
  
  // Presionar reset
  await tester.tap(find.byKey(Key('reset_button')));
  await tester.pump();

  // Assert
  expect(find.byType(TextField), findsWidgets);
  final emailField = tester.widget<TextField>(find.byKey(Key('email_field')));
  expect(emailField.controller?.text, '');
});
```

### 3. Testing con BLoC

```dart
testWidgets('should display loading then data', (tester) async {
  // Arrange
  final mockUserBloc = MockUserBloc();
  
  whenListen(
    mockUserBloc,
    Stream.fromIterable([
      UserLoading(),
      UserLoaded(user: testUser),
    ]),
    initialState: UserInitial(),
  );

  // Act
  await tester.pumpWidget(
    MaterialApp(
      home: BlocProvider<UserBloc>.value(
        value: mockUserBloc,
        child: UserPage(),
      ),
    ),
  );
  await tester.pump();  // Renderizar UserInitial
  
  expect(find.byType(LoadingWidget), findsNothing);
  
  await tester.pump();  // Renderizar UserLoading
  expect(find.byType(LoadingWidget), findsOneWidget);
  
  await tester.pumpAndSettle();  // Renderizar UserLoaded
  expect(find.text(testUser.name), findsOneWidget);
});

testWidgets('should display error message', (tester) async {
  // Arrange
  final mockUserBloc = MockUserBloc();
  
  whenListen(
    mockUserBloc,
    Stream.fromIterable([
      UserError(message: 'Network error'),
    ]),
  );

  // Act
  await tester.pumpWidget(
    MaterialApp(
      home: BlocProvider<UserBloc>.value(
        value: mockUserBloc,
        child: UserPage(),
      ),
    ),
  );
  await tester.pumpAndSettle();

  // Assert
  expect(find.text('Network error'), findsOneWidget);
});
```

### 4. Testing de Scroll

```dart
testWidgets('should scroll list to bottom', (tester) async {
  // Arrange
  await tester.pumpWidget(
    MaterialApp(
      home: Scaffold(
        body: ListView.builder(
          itemCount: 100,
          itemBuilder: (_, i) => ListTile(title: Text('Item $i')),
        ),
      ),
    ),
  );

  // Act - Scroll a bottom
  await tester.drag(find.byType(ListView), Offset(0, -500));
  await tester.pumpAndSettle();

  // Assert
  expect(find.text('Item 99'), findsOneWidget);
  expect(find.text('Item 1'), findsNothing);  // Fuera de pantalla
});

testWidgets('should scroll to top on button tap', (tester) async {
  // Arrange
  final scrollController = ScrollController();
  
  await tester.pumpWidget(
    MaterialApp(
      home: Scaffold(
        body: ListView.builder(
          controller: scrollController,
          itemCount: 100,
          itemBuilder: (_, i) => ListTile(title: Text('Item $i')),
        ),
        floatingActionButton: FloatingActionButton(
          onPressed: () {
            scrollController.animateTo(
              0,
              duration: Duration(milliseconds: 500),
              curve: Curves.easeInOut,
            );
          },
        ),
      ),
    ),
  );

  // Act
  await tester.drag(find.byType(ListView), Offset(0, -500));
  await tester.pumpAndSettle();
  
  await tester.tap(find.byType(FloatingActionButton));
  await tester.pumpAndSettle();

  // Assert
  expect(find.text('Item 1'), findsOneWidget);
});
```

### 5. Testing de Diálogos

```dart
testWidgets('should show dialog on button tap', (tester) async {
  // Arrange
  await tester.pumpWidget(
    MaterialApp(
      home: Scaffold(
        body: ElevatedButton(
          onPressed: () {
            showDialog(
              context: context,
              builder: (_) => AlertDialog(
                title: Text('Confirm'),
                content: Text('Do you agree?'),
                actions: [
                  TextButton(onPressed: () => Navigator.pop(context, false), child: Text('No')),
                  TextButton(onPressed: () => Navigator.pop(context, true), child: Text('Yes')),
                ],
              ),
            );
          },
          child: Text('Show Dialog'),
        ),
      ),
    ),
  );

  // Act
  await tester.tap(find.text('Show Dialog'));
  await tester.pumpAndSettle();

  // Assert
  expect(find.text('Confirm'), findsOneWidget);
  expect(find.text('Do you agree?'), findsOneWidget);
  expect(find.byType(AlertDialog), findsOneWidget);

  // Interactuar con el diálogo
  await tester.tap(find.text('Yes'));
  await tester.pumpAndSettle();

  // Verificar que se cerró
  expect(find.byType(AlertDialog), findsNothing);
});
```

### 6. Testing de Navegación

```dart
testWidgets('should navigate to detail page', (tester) async {
  // Arrange
  await tester.pumpWidget(
    MaterialApp(
      home: HomePage(),
      routes: {
        '/detail': (_) => DetailPage(),
      },
    ),
  );

  // Act
  await tester.tap(find.byKey(Key('detail_button')));
  await tester.pumpAndSettle();

  // Assert
  expect(find.byType(DetailPage), findsOneWidget);
});

testWidgets('should pass arguments to next page', (tester) async {
  // Esta es una forma de testear navegación con argumentos
  // Depende de tu implementación específica
  
  final navigatorObserver = MockNavigatorObserver();
  
  // Arrange
  await tester.pumpWidget(
    MaterialApp(
      home: HomePage(),
      navigatorObservers: [navigatorObserver],
      routes: {
        '/detail': (_) => DetailPage(),
      },
    ),
  );

  // Act
  await tester.tap(find.byKey(Key('detail_button')));
  await tester.pumpAndSettle();

  // Assert
  verify(() => navigatorObserver.didPush(any(), any())).called(1);
});
```

## Manejo de Tiempo y Animaciones

### Controlar Tiempo

```dart
testWidgets('should show loading for 2 seconds', (tester) async {
  // Arrange
  await tester.pumpWidget(
    MaterialApp(
      home: LoadingScreen(),
    ),
  );

  // Assert initial state
  expect(find.byType(LoadingIndicator), findsOneWidget);

  // Avanzar tiempo 1 segundo
  await tester.pump(Duration(seconds: 1));
  expect(find.byType(LoadingIndicator), findsOneWidget);

  // Avanzar otro segundo
  await tester.pump(Duration(seconds: 1));
  expect(find.byType(HomeScreen), findsOneWidget);
});
```

### Animaciones

```dart
testWidgets('should animate widget opacity', (tester) async {
  // Arrange
  await tester.pumpWidget(
    MaterialApp(
      home: FadeInWidget(
        duration: Duration(milliseconds: 500),
        child: Text('Fade in'),
      ),
    ),
  );

  // Assert - Inicial opacidad 0
  var opacityWidget = tester.widget<Opacity>(find.byType(Opacity));
  expect(opacityWidget.opacity, 0);

  // Act - Avanzar 250ms (mitad de la animación)
  await tester.pump(Duration(milliseconds: 250));
  opacityWidget = tester.widget<Opacity>(find.byType(Opacity));
  expect(opacityWidget.opacity, greaterThan(0));
  expect(opacityWidget.opacity, lessThan(1));

  // Act - Completar animación
  await tester.pumpAndSettle();
  opacityWidget = tester.widget<Opacity>(find.byType(Opacity));
  expect(opacityWidget.opacity, 1);
});
```

## Testing con Matchers Avanzados

```dart
// Widgets existentes
find.byType(Text)

// Por propiedades
find.byWidgetPredicate((widget) {
  if (widget is Text) {
    return widget.style?.color == Colors.red;
  }
  return false;
})

// Ancestros/Descendientes
find.ancestor(
  of: find.byKey(Key('child')),
  matching: find.byType(Container),
)

find.descendant(
  of: find.byType(ListView),
  matching: find.byKey(Key('list-item')),
)
```

## Pruebas de Tamaño y Posición

```dart
testWidgets('should render widget with correct size', (tester) async {
  // Arrange
  await tester.pumpWidget(
    MaterialApp(
      home: Scaffold(
        body: SizedBox(width: 200, height: 100, child: Text('Test')),
      ),
    ),
  );

  // Assert
  final sizedBox = tester.widget<SizedBox>(find.byType(SizedBox));
  expect(sizedBox.width, 200);
  expect(sizedBox.height, 100);

  // Or using renderBox
  final renderBox = tester.renderObject<RenderBox>(find.byType(SizedBox));
  expect(renderBox.size.width, 200);
});
```

## Mejores Prácticas

### ✅ Hacer

- Tests enfocados en comportamiento, no en implementación
- Usar `pumpAndSettle()` para animaciones
- Mockear BLoCs/Providers externos
- Agrupar tests relacionados con `group()`
- Usar keys para widgets dinámicos
- Verificar estados de carga, éxito y error
- Tests independientes sin side effects

### ❌ Evitar

- Testear detalles de diseño visual (usar Golden Tests para eso)
- Lógica compleja dentro de tests
- Tests que dependen del orden de ejecución
- Hardcodear timestamps o tiempos
- No esperar a que terminen animaciones
- Testear widgets de terceros

## Comandos Útiles

```bash
# Ejecutar widget tests
flutter test test/presentation/

# Ejecutar test específico
flutter test test/presentation/widgets/custom_button_test.dart

# Watch mode
flutter test --watch

# Generar cobertura
flutter test --coverage test/presentation/

# Ejecutar con seed específico
flutter test --test-randomness-seed=12345
```

## Estructura Template

```dart
void main() {
  group('CustomWidget', () {
    testWidgets('should render correctly', (tester) async {
      // Arrange
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomWidget(/* props */),
          ),
        ),
      );

      // Assert
      expect(find.byType(CustomWidget), findsOneWidget);
    });

    testWidgets('should handle user interaction', (tester) async {
      // Arrange
      bool tapped = false;
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomWidget(
              onTap: () => tapped = true,
            ),
          ),
        ),
      );

      // Act
      await tester.tap(find.byType(GestureDetector));
      await tester.pump();

      // Assert
      expect(tapped, true);
    });
  });
}
```
