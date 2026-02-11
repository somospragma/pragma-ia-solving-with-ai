# Prompt: Análisis de Componentes IIB

## Objetivo
Analizar componentes IIB (subflujos y transformaciones) para entender su lógica, flujo y comportamiento.

---

## Input

Proporciona el componente IIB:

```
TIPO: [Subflujo / XSLT / Mapping / ESQL / DFDL]
NOMBRE: [Nombre del componente]
PROPÓSITO: [Qué hace en términos de negocio]

CÓDIGO:
[Pegar código completo aquí]

INPUT EJEMPLO:
[Datos de entrada]

OUTPUT ESPERADO:
[Datos de salida]
```

---

## Output: Análisis de Componente

### 1. IDENTIFICACIÓN
```
Nombre: [Nombre]
Tipo: [Subflujo / XSLT / Mapping / ESQL / DFDL]
Categoría: [Error Handler / Transformer / Logger / Validator / Parser]
Propósito: [Descripción clara del objetivo]
Complejidad: [Baja / Media / Alta]
Reutilizable: [Sí / No]
```

### 2. SCHEMAS DE DATOS
```
INPUT:
  Formato: [XML / JSON / CSV / Binario]
  Estructura:
    [Describir estructura completa con tipos de datos]
  
  Ejemplo:
    [Datos de entrada de ejemplo]

OUTPUT:
  Formato: [XML / JSON / CSV / Binario]
  Estructura:
    [Describir estructura completa con tipos de datos]
  
  Ejemplo:
    [Datos de salida de ejemplo]
```

### 3. DIAGRAMA DE FLUJO
```
┌─────────────────────────────────────────────────────────┐
│ INICIO: [Nombre del componente]                         │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ PASO 1: [Descripción]                                   │
│ Nodo: [Tipo de nodo IIB]                                │
│ Acción: [Qué hace]                                      │
└─────────────────────────────────────────────────────────┘
                        ↓
              [¿Condición?] ──No──→ [Acción alternativa]
                   │ Sí
                   ↓
┌─────────────────────────────────────────────────────────┐
│ PASO 2: [Descripción]                                   │
│ Nodo: [Tipo de nodo IIB]                                │
│ Acción: [Qué hace]                                      │
└─────────────────────────────────────────────────────────┘
                        ↓
         ┌──────────────┴──────────────┐
         │                             │
    [Rama A]                      [Rama B]
         │                             │
         └──────────────┬──────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ PASO N: [Descripción]                                   │
│ Nodo: [Tipo de nodo IIB]                                │
│ Acción: [Qué hace]                                      │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ FIN: Output generado                                    │
└─────────────────────────────────────────────────────────┘

[Incluir manejo de errores en el diagrama si aplica]
```

### 4. FLUJO DE EJECUCIÓN DETALLADO
```
PASO 1: [Nombre del paso]
  Nodo IIB: [Tipo de nodo - ej: Compute, Mapping, TryCatch]
  Descripción: [Qué hace este paso]
  Variables Usadas:
    - [Variable 1]: [Propósito]
    - [Variable 2]: [Propósito]
  Variables Modificadas:
    - [Variable 1]: [Cómo se modifica]
  Lógica:
    [Descripción detallada de la lógica]
  Salida:
    [Qué produce este paso]

PASO 2: [Nombre del paso]
  Nodo IIB: [Tipo de nodo]
  Descripción: [Qué hace este paso]
  Condición: [Si hay condicional, describir]
  Variables Usadas:
    - [Variable 1]: [Propósito]
  Variables Modificadas:
    - [Variable 1]: [Cómo se modifica]
  Lógica:
    [Descripción detallada de la lógica]
  Salida:
    [Qué produce este paso]

[Continuar con todos los pasos...]
```

### 5. REGLAS DE NEGOCIO
```
REGLA 1: [Nombre de la regla]
  Descripción: [Qué valida o procesa]
  Condición: [Cuándo se aplica]
  Acción: [Qué hace cuando se cumple]
  Acción Alternativa: [Qué hace cuando NO se cumple]
  Prioridad: [Alta / Media / Baja]
  Impacto: [Qué pasa si esta regla falla]

REGLA 2: [Nombre de la regla]
  Descripción: [Qué valida o procesa]
  Condición: [Cuándo se aplica]
  Acción: [Qué hace cuando se cumple]
  Acción Alternativa: [Qué hace cuando NO se cumple]
  Prioridad: [Alta / Media / Baja]
  Impacto: [Qué pasa si esta regla falla]

[Continuar con todas las reglas identificadas...]
```

### 6. TRANSFORMACIONES DE DATOS
```
TRANSFORMACIÓN 1:
  Campo Origen: [path.completo.campo_origen]
  Tipo Origen: [String / Integer / Decimal / Array / Object / Date]
  Operación: [Directo / Cálculo / Split / Concatenación / Formato / Lookup]
  Descripción: [Cómo se transforma]
  Campo Destino: [path.completo.campo_destino]
  Tipo Destino: [String / Integer / Decimal / Array / Object / Date]
  Ejemplo:
    Input: [valor de ejemplo]
    Proceso: [pasos de transformación]
    Output: [valor transformado]

TRANSFORMACIÓN 2:
  Campo Origen: [path.completo.campo_origen]
  Tipo Origen: [Tipo]
  Operación: [Tipo de operación]
  Descripción: [Cómo se transforma]
  Campo Destino: [path.completo.campo_destino]
  Tipo Destino: [Tipo]
  Ejemplo:
    Input: [valor de ejemplo]
    Proceso: [pasos de transformación]
    Output: [valor transformado]

[Continuar con todas las transformaciones...]
```

### 7. MANEJO DE ERRORES
```
ERROR TIPO 1: [Nombre del error]
  Código: [Código de error si aplica]
  Condición: [Cuándo ocurre este error]
  Captura: [Cómo se captura - TryCatch / Validación / Otro]
  Acción: [Qué hace el componente cuando ocurre]
  Mensaje: [Mensaje de error generado]
  Propagación: [Se propaga al flujo padre / Se maneja localmente]
  Recuperación: [Es recuperable / No recuperable]

ERROR TIPO 2: [Nombre del error]
  Código: [Código de error si aplica]
  Condición: [Cuándo ocurre este error]
  Captura: [Cómo se captura]
  Acción: [Qué hace el componente cuando ocurre]
  Mensaje: [Mensaje de error generado]
  Propagación: [Se propaga / Se maneja localmente]
  Recuperación: [Es recuperable / No recuperable]

[Continuar con todos los tipos de error...]
```

### 8. DEPENDENCIAS
```
SUBFLUJOS INVOCADOS:
  1. [Nombre del subflujo]
     Propósito: [Para qué se invoca]
     Cuándo: [En qué paso del flujo]
     Input: [Qué datos recibe]
     Output: [Qué datos retorna]

  2. [Nombre del subflujo]
     Propósito: [Para qué se invoca]
     Cuándo: [En qué paso del flujo]
     Input: [Qué datos recibe]
     Output: [Qué datos retorna]

SERVICIOS EXTERNOS:
  1. [Nombre del servicio]
     Tipo: [REST / SOAP / Database / MQ / File]
     Endpoint: [URL o ubicación]
     Propósito: [Para qué se usa]
     Método: [GET / POST / etc.]
     Timeout: [Tiempo de espera]

  2. [Nombre del servicio]
     Tipo: [Tipo]
     Endpoint: [URL o ubicación]
     Propósito: [Para qué se usa]
     Método: [Método]
     Timeout: [Tiempo de espera]

VARIABLES DE ENTORNO:
  - [Variable 1]: [Tipo] - [Uso en el componente]
  - [Variable 2]: [Tipo] - [Uso en el componente]

PROPIEDADES CONFIGURABLES:
  - [Propiedad 1]: [Tipo] = [Valor Default] - [Descripción]
  - [Propiedad 2]: [Tipo] = [Valor Default] - [Descripción]
```

### 9. LÓGICA EN PSEUDOCÓDIGO
```
FUNCTION [nombre_componente](input):
  
  // ============================================
  // INICIALIZACIÓN
  // ============================================
  DECLARE [variable1] AS [tipo]
  DECLARE [variable2] AS [tipo]
  SET [variable1] = [valor inicial]
  
  // ============================================
  // VALIDACIONES
  // ============================================
  IF [condición validación 1] THEN
    [acción si falla]
    THROW ERROR "[mensaje]"
  END IF
  
  IF [condición validación 2] THEN
    [acción si falla]
    THROW ERROR "[mensaje]"
  END IF
  
  // ============================================
  // TRANSFORMACIONES
  // ============================================
  SET output.[campo1] = input.[campo_origen1]
  SET output.[campo2] = TRANSFORM(input.[campo_origen2])
  
  // ============================================
  // PROCESAMIENTO ITERATIVO
  // ============================================
  FOR EACH [elemento] IN input.[colección]:
    [lógica de procesamiento]
    SET [acumulador] = [acumulador] + [cálculo]
  END FOR
  
  // ============================================
  // ENRIQUECIMIENTO (si aplica)
  // ============================================
  CALL [servicio_externo] WITH [parámetros]
  SET output.[campo_enriquecido] = [resultado_servicio]
  
  // ============================================
  // CONSTRUCCIÓN DE OUTPUT
  // ============================================
  SET output.[campo_final1] = [valor]
  SET output.[campo_final2] = [valor]
  
  // ============================================
  // MANEJO DE ERRORES
  // ============================================
  CATCH [tipo_error]:
    LOG ERROR "[mensaje]"
    SET output.error = TRUE
    SET output.errorMessage = [mensaje]
  
  RETURN output
  
END FUNCTION
```

### 10. CASOS DE USO
```
CASO 1: FLUJO NORMAL (Happy Path)
  Descripción: [Escenario exitoso]
  Input:
    [Datos de entrada válidos]
  Proceso:
    1. [Paso 1 ejecutado]
    2. [Paso 2 ejecutado]
    3. [Paso N ejecutado]
  Output:
    [Resultado esperado]
  Tiempo Estimado: [X ms/seg]

CASO 2: ERROR DE VALIDACIÓN
  Descripción: [Escenario con datos inválidos]
  Input:
    [Datos de entrada inválidos]
  Proceso:
    1. [Validación falla en paso X]
    2. [Error capturado]
    3. [Respuesta de error generada]
  Output:
    [Mensaje de error]
  Tiempo Estimado: [X ms/seg]

CASO 3: CASO LÍMITE
  Descripción: [Escenario con datos en el límite]
  Input:
    [Datos límite - ej: array vacío, valores máximos]
  Proceso:
    1. [Cómo se maneja el caso límite]
    2. [Validaciones especiales]
  Output:
    [Resultado para caso límite]
  Tiempo Estimado: [X ms/seg]

CASO 4: SERVICIO EXTERNO NO DISPONIBLE
  Descripción: [Escenario con fallo de dependencia]
  Input:
    [Datos válidos]
  Proceso:
    1. [Intento de llamada a servicio]
    2. [Timeout o error de conexión]
    3. [Manejo de error]
  Output:
    [Respuesta de error o fallback]
  Tiempo Estimado: [X ms/seg]
```

### 11. NOTAS Y OBSERVACIONES
```
PUNTOS CLAVE:
  - [Observación importante 1]
  - [Observación importante 2]
  - [Observación importante 3]

COMPLEJIDADES:
  - [Complejidad 1]: [Descripción]
  - [Complejidad 2]: [Descripción]

MEJORAS SUGERIDAS:
  - [Sugerencia 1]: [Beneficio]
  - [Sugerencia 2]: [Beneficio]

RIESGOS IDENTIFICADOS:
  - [Riesgo 1]: [Impacto] - [Mitigación sugerida]
  - [Riesgo 2]: [Impacto] - [Mitigación sugerida]

DOCUMENTACIÓN ADICIONAL REQUERIDA:
  - [Qué falta documentar 1]
  - [Qué falta documentar 2]
```

---

## Ejemplo de Solicitud

```
Analiza este componente IIB:

TIPO: ESQL
NOMBRE: OrderTransformation
PROPÓSITO: Transformar pedido XML a JSON y calcular totales

CÓDIGO:
CREATE COMPUTE MODULE OrderTransformation
  CREATE FUNCTION Main() RETURNS BOOLEAN
  BEGIN
    DECLARE total DECIMAL 0;
    SET OutputRoot.JSON.Data.orderId = InputRoot.XMLNSC.Order.OrderId;
    
    DECLARE itemRef REFERENCE TO InputRoot.XMLNSC.Order.Items.Item[1];
    WHILE LASTMOVE(itemRef) DO
      SET total = total + (itemRef.Quantity * itemRef.Price);
      MOVE itemRef NEXTSIBLING;
    END WHILE;
    
    SET OutputRoot.JSON.Data.total = total;
    RETURN TRUE;
  END;
END MODULE;

INPUT EJEMPLO:
<Order>
  <OrderId>123</OrderId>
  <Items>
    <Item><Quantity>2</Quantity><Price>10.5</Price></Item>
    <Item><Quantity>1</Quantity><Price>5.0</Price></Item>
  </Items>
</Order>

OUTPUT ESPERADO:
{"orderId": "123", "total": 26.0}

GENERA análisis completo del componente.
```
