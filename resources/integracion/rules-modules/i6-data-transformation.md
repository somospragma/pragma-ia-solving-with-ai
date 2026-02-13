# I6 - Transformación de Datos

## Descripción
Este ruleset evalúa las prácticas de transformación y mapeo de datos en servicios de integración.

## Severidad: MEDIUM

## Reglas

### 6.1 Validación Pre-Transformación
**Severidad**: HIGH

**Descripción**: Validar datos antes de transformar.

**Criterios**:
- ✅ Validar contra schema (JSON Schema, XSD)
- ✅ Verificar campos requeridos
- ✅ Validar tipos de datos
- ✅ Validar rangos y formatos
- ✅ Retornar 400 Bad Request si falla validación

---

### 6.2 Transformaciones Nativas
**Severidad**: MEDIUM

**Descripción**: Preferir transformaciones nativas de la plataforma.

**Criterios**:
- ✅ Usar DataWeave (MuleSoft)
- ✅ Usar XSLT (IIB/OSB)
- ✅ Usar JSONata
- ✅ Evitar código custom cuando sea posible

**Beneficios**:
- Mejor rendimiento
- Mantenimiento más fácil
- Menos bugs

---

### 6.3 Documentación de Mapeos
**Severidad**: MEDIUM

**Descripción**: Documentar transformaciones complejas.

**Criterios**:
- ✅ Comentarios en código de transformación
- ✅ Matriz de mapeo (source → target)
- ✅ Reglas de negocio aplicadas
- ✅ Valores por defecto documentados

**Ejemplo de Matriz**:
```
Source Field       | Target Field      | Transformation
-------------------|-------------------|------------------
customer.firstName | client.givenName  | Direct mapping
customer.lastName  | client.familyName | Direct mapping
customer.dob       | client.birthDate  | Format: YYYY-MM-DD
```

---

### 6.4 Manejo de Valores Nulos
**Severidad**: MEDIUM

**Descripción**: Manejar apropiadamente valores nulos y ausentes.

**Criterios**:
- ✅ Definir comportamiento para campos nulos
- ✅ Usar valores por defecto cuando sea apropiado
- ✅ Distinguir entre null y ausente
- ✅ Documentar comportamiento

**Ejemplo**:
```javascript
// DataWeave
{
  name: payload.name default "Unknown",
  age: payload.age default 0,
  email: payload.email // puede ser null
}
```

---

### 6.5 Conversión de Tipos Segura
**Severidad**: HIGH

**Descripción**: Realizar conversiones de tipos de forma segura.

**Criterios**:
- ✅ Validar antes de convertir
- ✅ Manejar errores de conversión
- ✅ No asumir formatos
- ✅ Usar funciones de conversión seguras

**Ejemplo**:
```javascript
// Incorrecto
let age = parseInt(input.age); // puede ser NaN

// Correcto
let age = parseInt(input.age);
if (isNaN(age)) {
  throw new ValidationError("Invalid age");
}
```

---

### 6.6 Encoding Correcto
**Severidad**: HIGH

**Descripción**: Manejar encoding de caracteres correctamente.

**Criterios**:
- ✅ Usar UTF-8 por defecto
- ✅ Especificar encoding en headers
- ✅ Convertir encoding cuando sea necesario
- ✅ Validar caracteres especiales

---

### 6.7 Transformaciones Reversibles
**Severidad**: LOW

**Descripción**: Cuando sea posible, hacer transformaciones reversibles.

**Criterios**:
- ✅ No perder información en transformación
- ✅ Permitir transformación inversa
- ✅ Documentar pérdida de información si existe

---

### 6.8 Optimización de Transformaciones
**Severidad**: MEDIUM

**Descripción**: Optimizar transformaciones para rendimiento.

**Criterios**:
- ✅ Evitar transformaciones innecesarias
- ✅ Transformar una sola vez
- ✅ Usar streaming para datos grandes
- ✅ Cachear transformaciones costosas

---

### 6.9 Soporte Multi-Formato
**Severidad**: MEDIUM

**Descripción**: Soportar múltiples formatos de datos.

**Criterios**:
- ✅ JSON ↔ XML
- ✅ CSV ↔ JSON
- ✅ Content negotiation (Accept header)
- ✅ Conversión automática cuando sea posible

**Ejemplo**:
```
Accept: application/json → Respuesta en JSON
Accept: application/xml → Respuesta en XML
```

---

### 6.10 Validación Post-Transformación
**Severidad**: MEDIUM

**Descripción**: Validar datos después de transformar.

**Criterios**:
- ✅ Validar contra schema de salida
- ✅ Verificar campos requeridos generados
- ✅ Validar integridad de datos
- ✅ Loggear advertencias si hay inconsistencias

---

## Checklist de Evaluación

| ID | Criterio | Cumple | Observaciones |
|----|----------|--------|---------------|
| 6.1 | Validación pre-transformación | ⬜ | |
| 6.2 | Transformaciones nativas | ⬜ | |
| 6.3 | Documentación de mapeos | ⬜ | |
| 6.4 | Manejo de valores nulos | ⬜ | |
| 6.5 | Conversión de tipos segura | ⬜ | |
| 6.6 | Encoding correcto | ⬜ | |
| 6.7 | Transformaciones reversibles | ⬜ | |
| 6.8 | Optimización | ⬜ | |
| 6.9 | Soporte multi-formato | ⬜ | |
| 6.10 | Validación post-transformación | ⬜ | |
