```markdown
# Quality & Testing

## 4.1. Testing Strategy

- Unit tests for transformations and helpers
- Integration tests against synthetic or sampled datasets in CI
- Contract tests to validate schema and expectations

## 4.2. Code Coverage & Metrics

- **Target coverage:** Mantén cobertura >= 80% de líneas ejecutables; prioriza funciones críticas.
- **Cobertura de líneas vs branches:** Cobertura de líneas (ejecutadas) no es suficiente; valida también branch coverage (if/else) para lógica condicional.
- **Métricas a medir:**
  - Line coverage: % de líneas ejecutadas por tests.
  - Branch coverage: % de caminos condicionales cubiertos.
  - Cyclomatic complexity: Número de caminos lógicos; mantén funciones simples (< 10).
  
- **Excluir de cobertura:** Código de setup/teardown, imports innecesarios, código legacy sin tests. Usa `# pragma: no cover`.
- **Herramientas recomendadas:**
  - Python: `pytest` + `pytest-cov` + `coverage.py` para reportes.
  - PySpark: Valida cobertura en lógica transformación (no en framework).
  
- **Gates en CI:** Fallar build si cobertura cae por debajo del threshold; reportar en PR.
- **Reportes públicos:** Genera HTML report de cobertura; optional: coverage badges en README.

## 4.3. Data Quality Checks

- Schema validation, null checks, uniqueness, referential integrity
- Statistical checks: distributions, sudden drifts, percentage of nulls
- Implement Quality Gates in CI and block merges on critical failures

## 4.4. Edge Case Testing & Robustness

- **Boundary conditions:** Tests con valores en los límites (min/max, primero/último).
- **Null/empty inputs:** Cómo se comporta con DataFrames vacíos, nulls masivos, strings vacíos.
- **Data type mismatches:** Qué pasa si el tipo es inesperado (string en lugar de int).
- **Negative values / ranges inesperados:** Validar comportamiento con valores que violan dominio (edad negativa, porcentaje > 100).
- **Unicode/special characters:** Caracteres especiales, emojis, encoding issues.
- **Sorting & order:** Tests que no asumen orden específico; evita falsos positivos.

## 4.5. Monitoring & Metrics

- Track throughput, processing lag, success rate, data freshness, size
- Expose dataset health endpoint or metrics to observability platform

## 4.6. Test Organization & CI Pipeline

- `tests/unit/` para tests aislados; `tests/integration/` para tests con dependencias.
- **CI pipeline stages:**
  1. Lint + Static analysis (code quality).
  2. Unit tests + coverage gate.
  3. Integration tests (con datos sample).
  4. Contract tests (schema + expectations).
  5. Optional: Performance/load tests.
  
- **Fail fast:** Lint y unit tests primero (rápido); integration después.
- **Reports:** Publicar resultado de tests y cobertura como artifact en CI; incluir en PR checks.

## 4.7. Coverage Example (pytest)

Pequeño ejemplo de configuración:

```bash
# Instalar
pip install pytest pytest-cov

# Ejecutar con reporte
pytest --cov=src --cov-report=html --cov-report=term-missing --cov-fail-under=80

# Generar badge (opcional)
coverage-badge -o coverage.svg
```

Configurar `pyproject.toml`:
```ini
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=src --cov-report=html --cov-fail-under=80"

[tool.coverage.run]
branch = true
omit = ["**/tests/**", "**/site-packages/**"]
```

Gates recomendadas en CI (GitHub Actions ejemplo):
```yaml
- name: Run tests and coverage
  run: pytest --cov --cov-fail-under=80
  
- name: Upload coverage report
  uses: codecov/codecov-action@v3
```

```
