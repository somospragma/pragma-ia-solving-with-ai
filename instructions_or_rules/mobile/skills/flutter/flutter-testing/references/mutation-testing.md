# Mutation Testing Reference

Mutation Testing valida la **calidad** de tus tests existentes alterando el código fuente para verificar si los tests pueden detectar esos cambios.

## ¿Por Qué Mutation Testing?

### Problema Común
Tests con cobertura del 100% pueden no ser efectivos:

```dart
// Código siendo testado
bool isAdult(int age) {
  return age >= 18;  // Bug: debería ser > 18
}

// Test "efectivo" que pasa
test('should return true for age 18', () {
  expect(isAdult(18), true);
});
```

Este test tiene "cobertura" pero no detectaría el bug con `>` en lugar de `>=`.

**Mutation Testing introduce cambios (mutations) al código:**
- `>=` cambia a `>`
- `18` cambia a `17` o `19`
- `true` cambia a `false`

Si los tests aún pasan, la mutación **sobrevivió** = test deficiente.

## Configuración

### Instalación de pitest (Dart/Flutter)

```bash
# Opción 1: Usar mutation_test (comunidad)
dart pub add --dev mutation_test

# Opción 2: Usar mutation_observer (más moderno)
dart pub add --dev mutation_observer
```

### Alternativas: Usando mutants en Dart

```yaml
dev_dependencies:
  test: ^1.24.0
  mutants: ^0.2.0
```

## Tipos de Mutaciones

### 1. Statement Mutaciones (Más Comunes)

```dart
// Original
int calcularPrecio(int cantidad, int precioUnitario) {
  return cantidad * precioUnitario;
}

// Mutations generadas:
int calcularPrecio(int cantidad, int precioUnitario) {
  return cantidad + precioUnitario;  // * → +
}

int calcularPrecio(int cantidad, int precioUnitario) {
  return cantidad - precioUnitario;  // * → -
}

int calcularPrecio(int cantidad, int precioUnitario) {
  return cantidad / precioUnitario;  // * → /
}

int calcularPrecio(int cantidad, int precioUnitario) {
  return 0;  // Retorno constante
}
```

### 2. Conditional Mutaciones

```dart
// Original
bool isElegible(int edad, bool esEstudiante) {
  return edad >= 18 && esEstudiante;
}

// Mutations:
bool isElegible(int edad, bool esEstudiante) {
  return edad > 18 && esEstudiante;      // >= → >
}

bool isElegible(int edad, bool esEstudiante) {
  return edad >= 19 && esEstudiante;     // 18 → 19
}

bool isElegible(int edad, bool esEstudiante) {
  return edad >= 18 || esEstudiante;     // && → ||
}

bool isElegible(int edad, bool esEstudiante) {
  return true;  // Siempre true
}
```

### 3. Return Mutaciones

```dart
// Original
Either<Failure, User> getUser() {
  // logic
  return Right(user);
}

// Mutations:
Either<Failure, User> getUser() {
  return Left(Failure());  // Right → Left
}

Either<Failure, User> getUser() {
  return null;  // Return nulo
}
```

## Implementación con Mutation Testing Libraries

### Usando mutation_test

```bash
# Instalar
dart pub add --dev mutation_test

# Generar y ejecutar
dart run mutation_test --help

# Ejecutar mutation testing
dart run mutation_test:create_mutants
dart test test/
```

### Ejemplo: Test Deficiente vs Efectivo

```dart
// Función a probar
class DiscountCalculator {
  static double calculateDiscount(double price, int quantity) {
    if (quantity < 5) {
      return price * 0.95;  // 5% discount
    } else if (quantity < 10) {
      return price * 0.90;  // 10% discount
    } else {
      return price * 0.85;  // 15% discount
    }
  }
}

// ❌ Tests INEFECTIVOS (sobreviven mutations)
void main() {
  group('DiscountCalculator - BAD TESTS', () {
    test('should apply discount for quantity >= 5', () {
      final result = DiscountCalculator.calculateDiscount(100, 5);
      expect(result, lessThan(100));  // ⚠️ Muy vago
    });

    test('should return a number', () {
      final result = DiscountCalculator.calculateDiscount(100, 10);
      expect(result, isA<double>());  // ⚠️ No valida valor específico
    });
  });

  // ✅ Tests EFECTIVOS (matan mutations)
  group('DiscountCalculator - GOOD TESTS', () {
    test('should apply 5% discount for quantity < 5', () {
      final result = DiscountCalculator.calculateDiscount(100, 4);
      expect(result, 95.0);  // ✅ Valor exacto
      expect(result, isNot(90.0));  // ✅ No es otro valor
    });

    test('should apply 10% discount for quantity between 5-9', () {
      final result = DiscountCalculator.calculateDiscount(100, 5);
      expect(result, 90.0);  // ✅ Valor exacto
    });

    test('should apply 10% discount for quantity 9', () {
      final result = DiscountCalculator.calculateDiscount(100, 9);
      expect(result, 90.0);  // ✅ Boundary testing
    });

    test('should apply 15% discount for quantity >= 10', () {
      final result = DiscountCalculator.calculateDiscount(100, 10);
      expect(result, 85.0);
      expect(result, isNot(90.0));
    });

    test('should handle large quantities', () {
      final result = DiscountCalculator.calculateDiscount(1000, 100);
      expect(result, 850.0);
    });

    test('should not exceed discount of 15%', () {
      final result = DiscountCalculator.calculateDiscount(100, 1000);
      expect(result, greaterThanOrEqualTo(85.0));
    });
  });
}
```

## Estrategia de Mutation Testing

### 1. Línea Base (Baseline)

```bash
# Ejecutar mutation testing inicial
dart run mutation_test:create_mutants
dart test test/ 2>&1 | grep "killed\|survived"

# Registrar resultados
# Killed: 145 mutations
# Survived: 23 mutations
# Mutation Score: 86%
```

### 2. Identificar Mutaciones Sobrevivientes

Las mutaciones que sobreviven indican tests débiles:

```dart
// 🔴 Esta mutación sobrevive
int calculateTotal(List<int> items) {
  int total = 0;
  for (int item in items) {
    total = total + item;  // Mutación: cambia a -= también sobrevive
  }
  return total;
}

// Test débil que permite sobrevivencia
test('should calculate total', () {
  expect(calculateTotal([1, 2, 3]), greaterThan(0));  // ⚠️ Muy vago
});

// Test mejorado
test('should calculate sum of items', () {
  expect(calculateTotal([1, 2, 3]), 6);  // ✅ Valor exacto
  expect(calculateTotal([]), 0);  // ✅ Edge case
  expect(calculateTotal([5]), 5);  // ✅ Single item
  expect(calculateTotal([0, 0, 0]), 0);  // ✅ Zeros
});
```

### 3. Mejorar Tests

Para cada mutación sobreviviente:

```dart
// Función con lógica compleja
String getGrade(int score) {
  if (score >= 90) return 'A';
  if (score >= 80) return 'B';
  if (score >= 70) return 'C';
  if (score >= 60) return 'D';
  return 'F';
}

// ❌ Tests iniciales débiles
test('should return A for high score', () {
  expect(getGrade(95), 'A');
});

// ✅ Tests mejorados (matan más mutations)
void main() {
  group('getGrade', () {
    // Boundary tests (matan > vs >=)
    test('should return A for score 90', () {
      expect(getGrade(90), 'A');
    });

    test('should return A for score above 90', () {
      expect(getGrade(95), 'A');
    });

    test('should not return A for score 89', () {
      expect(getGrade(89), isNot('A'));
      expect(getGrade(89), 'B');
    });

    // Todos los boundaries
    test('should return B for 80-89', () {
      expect(getGrade(80), 'B');
      expect(getGrade(85), 'B');
      expect(getGrade(89), 'B');
    });

    test('should return C for 70-79', () {
      expect(getGrade(70), 'C');
      expect(getGrade(75), 'C');
      expect(getGrade(79), 'C');
    });

    test('should return D for 60-69', () {
      expect(getGrade(60), 'D');
      expect(getGrade(65), 'D');
    });

    test('should return F for below 60', () {
      expect(getGrade(59), 'F');
      expect(getGrade(0), 'F');
    });

    // Otros casos
    test('should handle exact boundaries', () {
      const boundaries = {'90': 'A', '80': 'B', '70': 'C', '60': 'D'};
      boundaries.forEach((score, expected) {
        expect(getGrade(int.parse(score)), expected);
      });
    });
  });
}
```

## Mutation Score por Capa

### Domain Layer (Crítico)

- **Objetivo**: > 90% mutation score
- **Razón**: Lógica de negocio pura debe ser extremadamente bien testada

```dart
// business_logic.dart
class PriceCalculator {
  static double applyTax(double price, double taxRate) {
    if (taxRate < 0) throw ArgumentError('Tax rate cannot be negative');
    return price * (1 + taxRate);
  }
}

// Tests para objetivo de 90%+ mutation score
void main() {
  group('PriceCalculator', () {
    test('should accurately apply tax', () {
      expect(PriceCalculator.applyTax(100, 0.21), 121.0);
      expect(PriceCalculator.applyTax(50, 0.16), 58.0);
      expect(PriceCalculator.applyTax(100, 0), 100.0);  // Sin tax
    });

    test('should throw on negative tax', () {
      expect(
        () => PriceCalculator.applyTax(100, -0.1),
        throwsArgumentError,
      );
    });

    test('should handle edge cases', () {
      expect(PriceCalculator.applyTax(0, 0.21), 0);
      expect(PriceCalculator.applyTax(0.01, 0.21), 0.0121);
    });
  });
}
```

### Data Layer (Alto)

- **Objetivo**: > 85% mutation score
- **Razón**: Manejo de datos y conversiones es crítico

### Presentation Layer (Medio)

- **Objetivo**: > 75% mutation score
- **Razón**: Menos crítico que lógica de negocio pura

## Integración en CI/CD

```yaml
# .github/workflows/mutation-test.yml
name: Mutation Testing

on: [pull_request]

jobs:
  mutation-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Flutter
        uses: subosito/flutter-action@v2
      
      - name: Get dependencies
        run: flutter pub get
      
      - name: Run mutation tests
        run: |
          dart pub global activate mutation_test
          dart run mutation_test:create_mutants
          flutter test test/
      
      - name: Check mutation score
        run: |
          # Fallar si mutation score < 80%
          SCORE=$(dart run mutation_test:report | grep "Mutation Score" | awk '{print $NF}')
          if (( $(echo "$SCORE < 80" | bc -l) )); then
            echo "Mutation score too low: $SCORE%"
            exit 1
          fi
```

## Herramientas y Recursos

### Librerías Dart/Flutter
- [mutation_test](https://pub.dev/packages/mutation_test) - Mutation testing framework
- [mutation_observer](https://pub.dev/packages/mutation_observer) - Observer para observar mutaciones

### Librerías Externas
- [PIT](https://pitest.org/) - Para Java (referencia)
- [Stryker](https://stryker-mutator.io/) - Mutation testing platform

## Checklist: Cuando Usar Mutation Testing

- [ ] Proyecto con 70%+ cobertura de tests
- [ ] Tests críticos de lógica de negocio
- [ ] Fase de mejora continua de calidad
- [ ] Equipo maduro en testing
- [ ] Tiempo disponible para análisis de resultados

## Buenas Prácticas

### ✅ Hacer

- Usar mutation testing para complementar cobertura
- Enfocarse en mutaciones sobrevivientes en código crítico
- Establecer baseline de mutation score
- Mejorar tests incrementalmente

### ❌ Evitar

- Intentar alcanzar 100% mutation score (es impracticable)
- Escribir tests solo para "matar" mutaciones
- Usar mutation testing como único métrica
- Implementar en proyectos con baja cobertura (<70%)
