# Prompt: Transformación de Datos

## Objetivo
Transformar datos de cualquier formato de entrada a cualquier formato de salida, generando código implementable en cualquier lenguaje de programación de forma agnóstica.

---

## Instrucciones

Eres un experto en transformación de datos y arquitectura de integración. Tu tarea es:

1. **Analizar** la estructura de datos de entrada y salida proporcionada
2. **Identificar** las reglas de transformación necesarias
3. **Documentar** el mapeo de campos y lógica de negocio
4. **Generar** código optimizado en el lenguaje solicitado
5. **Proporcionar** tests y documentación técnica

---

## Input Esperado

Proporciona la siguiente información:

### 1. Formato de Entrada
```json
{
  "formato": "JSON / XML / CSV / SOAP / Flat File / Otro",
  "ejemplo": {
    // Tu estructura de datos de entrada aquí
  }
}
```

### 2. Formato de Salida Deseado
```json
{
  "formato": "JSON / XML / CSV / REST / Otro",
  "ejemplo": {
    // Tu estructura de datos de salida deseada aquí
  }
}
```

### 3. Reglas de Transformación (Opcional)
```
- Campo X debe mapearse a Campo Y
- Aplicar formato de fecha ISO 8601
- Calcular total sumando items
- Validar que campo Z no esté vacío
- etc.
```

### 4. Lenguaje Target
```
Python / Java / JavaScript / C# / Go / TypeScript / Otro
```

---

## Output Esperado

### 1. Análisis de la Transformación

**Formato Entrada:** [JSON / XML / CSV / etc.]

**Formato Salida:** [JSON / XML / CSV / etc.]

**Complejidad:** [Baja / Media / Alta]

**Input Schema:**
```
[Estructura de entrada con tipos de datos]
```

**Output Schema:**
```
[Estructura de salida con tipos de datos]
```

---

### 2. Mapeo de Campos

| Campo Origen | Transformación | Campo Destino | Regla |
|--------------|----------------|---------------|-------|
| customer.id | Directo | customerId | - |
| customer.name | Split | firstName, lastName | Separar por espacio |
| order.total | Cálculo | totalAmount | Sumar items * precio |
| order.date | Formato | orderDate | ISO 8601 |

---

### 3. Lógica de Negocio Identificada

- [ ] Validaciones (ej: campo requerido, formato, rango)
- [ ] Transformaciones de formato (ej: fecha, moneda)
- [ ] Cálculos (ej: suma, promedio, fórmulas)
- [ ] Enriquecimiento (ej: lookup, llamadas externas)
- [ ] Condicionales (ej: if-then-else, switch)
- [ ] Iteraciones (ej: loops sobre arrays)
- [ ] Agregaciones (ej: group by, distinct)

**Detalles:**
```
[Descripción de cada regla de negocio]
```

---

### 4. Consideraciones de Implementación

#### 4.1 Performance
- **Complejidad:** O(n) donde n es el número de items
- **Memoria:** Proporcional al tamaño del input
- **Optimizaciones sugeridas:** [Lista de optimizaciones]

#### 4.2 Manejo de Errores
- **Errores de validación:** Retornar código 400 con detalle
- **Errores de transformación:** Retornar código 500 con log
- **Timeout:** Configurar timeout de [X] segundos

#### 4.3 Dependencias Externas
- **Librerías necesarias:** [Lista de librerías por lenguaje]
  - Python: `datetime`, `json`, `decimal`
  - Java: `java.time`, `com.fasterxml.jackson`
  - JavaScript: `date-fns`, `lodash`

#### 4.4 Configuración
- **Variables de entorno:** [Lista de variables]
- **Parámetros configurables:** [Lista de parámetros]

---

### 5. Implementación en [Lenguaje Solicitado]

**Lenguaje:** [Python / Java / JavaScript / C# / Go / etc.]

**Código:**
```[lenguaje]
[Código completo implementando la transformación]
```

**Dependencias:**
```
[Archivo de dependencias: requirements.txt, pom.xml, package.json, etc.]
```

**Tests Unitarios:**
```[lenguaje]
[Tests para los casos de prueba definidos]
```

---

### 6. Diagrama de Arquitectura

```
┌─────────────┐
│   Input     │
│   (JSON)    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Validación  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│Transformación│
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Cálculos   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Output    │
│   (JSON)    │
└─────────────┘
```

---

### 7. Migración y Deployment

#### 7.1 Checklist de Implementación
- [ ] Análisis de transformación completado
- [ ] Mapeo de campos documentado
- [ ] Código implementado en lenguaje target
- [ ] Tests unitarios creados y pasando
- [ ] Manejo de errores implementado
- [ ] Performance validado
- [ ] Documentación actualizada

#### 7.2 Estrategia de Deployment
- **Ambiente:** [Lambda / Container / VM]
- **CI/CD:** [Pipeline sugerido]
- **Rollback:** [Plan de rollback]
- **Monitoreo:** [Métricas a monitorear]

---

## Ejemplo de Uso del Prompt

**Usuario:**
```
Necesito transformar datos de este formato JSON:
{
  "cliente": {
    "identificacion": "12345",
    "nombreCompleto": "Juan Pérez"
  },
  "pedido": {
    "articulos": [
      {"cantidad": 2, "precioUnitario": 10.50}
    ]
  }
}

A este formato:
{
  "customerId": "12345",
  "firstName": "Juan",
  "lastName": "Pérez",
  "orderTotal": 21.00
}

Lenguaje target: Python para AWS Lambda
```

**Asistente:**
[Seguirá la estructura completa definida arriba, generando todos los apartados]
