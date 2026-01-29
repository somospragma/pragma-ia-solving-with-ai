# AWS EC2 Cost Validation - OnDemand vs Spot vs Reserved

## Descripción General

Herramienta de validación y comparación de costos para instancias EC2 en diferentes modalidades de compra (On-Demand, Spot, Reserved Instances) usando precios actuales de AWS Pricing API.

---

## Configuración Técnica

### Región
- **Fija**: `us-east-1` (US East N. Virginia)

### Herramientas MCP Requeridas
```json
{
  "awslabs.aws-pricing-mcp-server": "Obtener precios vigentes de EC2 (OnDemand, Spot, Reserved)"
}
```

### Parámetros de Entrada (Configurables por Usuario)
```
region: "us-east-1"                    # Fija
aws_profile: <user-defined>            # Perfil AWS del usuario (ej: "chapter", "prod", "dev")
aws_credentials_source: "profile" | "env"  # Fuente de credenciales

instances: [
  "m5.large",
  "c6i.xlarge",
  "t3.medium"
]

purchase_options: [
  "OnDemand",
  "Spot",
  "RI_1yr_Standard_NoUpfront"
]

operating_system: "Linux"              # Fijo para este análisis
tenancy: "Shared"                      # Fijo para este análisis
```

**Nota**: El `aws_profile` debe ser especificado por el usuario según su configuración local de AWS CLI.

---

## Definiciones Operativas

### Modalidades de Compra

#### On-Demand
```
- Pago por hora sin compromiso
- Precio más alto
- Flexible, sin restricciones
- Ideal para: Cargas impredecibles, desarrollo/testing
```

#### Spot
```
- Precio dinámico basado en oferta/demanda
- Hasta 90% descuento vs On-Demand
- Puede ser interrumpido por AWS
- Precio actual (no histórico)
- Ideal para: Cargas tolerantes a interrupciones, batch jobs
```

#### Reserved Instances (RI) - 1 año, Standard, No Upfront
```
- Compromiso de 1 año
- Descuento ~30-40% vs On-Demand
- Standard: Flexible en familia de instancia (dentro de la misma generación)
- No Upfront: Pago mensual, sin pago inicial
- Ideal para: Cargas predecibles, producción estable
```

---

## Tareas de Análisis

### 1. Consulta de Precios - On-Demand

Para cada instancia en us-east-1:

```
Consulta MCP:
get_pricing(
  service="AmazonEC2",
  region="us-east-1",
  filters=[
    {"Field": "instanceType", "Value": "m5.large", "Type": "EQUALS"},
    {"Field": "location", "Value": "US East (N. Virginia)", "Type": "EQUALS"},
    {"Field": "operatingSystem", "Value": "Linux", "Type": "EQUALS"},
    {"Field": "tenancy", "Value": "Shared", "Type": "EQUALS"},
    {"Field": "preReservedCapacityType", "Value": "OnDemand", "Type": "EQUALS"}
  ]
)

Resultado esperado:
{
  "instanceType": "m5.large",
  "purchaseOption": "OnDemand",
  "pricePerHourUsd": 0.096,
  "sku": "6QCMYABX3D",
  "effectiveDate": "2026-01-29",
  "currency": "USD"
}
```

### 2. Consulta de Precios - Spot

Para cada instancia en us-east-1:

```
Consulta MCP:
get_pricing(
  service="AmazonEC2",
  region="us-east-1",
  filters=[
    {"Field": "instanceType", "Value": "m5.large", "Type": "EQUALS"},
    {"Field": "location", "Value": "US East (N. Virginia)", "Type": "EQUALS"},
    {"Field": "operatingSystem", "Value": "Linux", "Type": "EQUALS"},
    {"Field": "tenancy", "Value": "Shared", "Type": "EQUALS"},
    {"Field": "purchaseType", "Value": "Spot", "Type": "EQUALS"}
  ]
)

Resultado esperado:
{
  "instanceType": "m5.large",
  "purchaseOption": "Spot",
  "pricePerHourUsd": 0.032,
  "sku": "6QCMYABX3E",
  "effectiveDate": "2026-01-29",
  "currency": "USD",
  "notes": "Spot price; subject to fluctuation"
}
```

### 3. Consulta de Precios - Reserved Instances (1yr, Standard, No Upfront)

Para cada instancia en us-east-1:

```
Consulta MCP:
get_pricing(
  service="AmazonEC2",
  region="us-east-1",
  filters=[
    {"Field": "instanceType", "Value": "m5.large", "Type": "EQUALS"},
    {"Field": "location", "Value": "US East (N. Virginia)", "Type": "EQUALS"},
    {"Field": "operatingSystem", "Value": "Linux", "Type": "EQUALS"},
    {"Field": "tenancy", "Value": "Shared", "Type": "EQUALS"},
    {"Field": "reservedInstanceType", "Value": "Standard", "Type": "EQUALS"},
    {"Field": "reservedInstanceTerm", "Value": "1yr", "Type": "EQUALS"},
    {"Field": "offeringType", "Value": "No Upfront", "Type": "EQUALS"}
  ]
)

Resultado esperado:
{
  "instanceType": "m5.large",
  "purchaseOption": "RI_1yr_Standard_NoUpfront",
  "pricePerHourUsd": 0.067,
  "sku": "6QCMYABX3F",
  "effectiveDate": "2026-01-29",
  "currency": "USD",
  "notes": "RI Standard, 1yr, No Upfront; monthly payment"
}
```

### 4. Cálculo de Costos Mensuales

Para cada combinación (instancia + modalidad):

```
MonthlyCostUSD = pricePerHourUsd * 730 horas/mes

Ejemplo:
- m5.large On-Demand: $0.096/h * 730 = $70.08/mes
- m5.large Spot: $0.032/h * 730 = $23.36/mes
- m5.large RI 1yr NoUpfront: $0.067/h * 730 = $48.91/mes
```

### 5. Cálculo de Diferencias vs On-Demand

Para cada modalidad:

```
Ahorro % = ((OnDemand_Price - Alternative_Price) / OnDemand_Price) * 100

Ejemplo:
- Spot vs OnDemand: ((0.096 - 0.032) / 0.096) * 100 = 66.67% ahorro
- RI vs OnDemand: ((0.096 - 0.067) / 0.096) * 100 = 30.21% ahorro
```

### 6. Resumen por Modalidad

Calcular totales mensuales para todas las instancias:

```
OnDemand_Total = sum(m5.large + c6i.xlarge + t3.medium) On-Demand
Spot_Total = sum(m5.large + c6i.xlarge + t3.medium) Spot
RI_Total = sum(m5.large + c6i.xlarge + t3.medium) RI 1yr NoUpfront

Ahorro_Spot_vs_OnDemand = OnDemand_Total - Spot_Total
Ahorro_RI_vs_OnDemand = OnDemand_Total - RI_Total
```

---

## Salidas

### 1. CSV: `ec2-cost-validation-us-east-1.csv`

**Formato**: UTF-8, delimitado por comas, con escaping de comillas

**Columnas**:
```
InstanceType,PurchaseOption,SKU,PricePerHourUSD,MonthlyCostUSD,EffectiveDate,Notes
```

**Definición de Columnas**:
```
InstanceType: m5.large, c6i.xlarge, t3.medium
PurchaseOption: OnDemand | Spot | RI_1yr_Standard_NoUpfront
SKU: Identificador único de AWS Pricing
PricePerHourUSD: Precio por hora (número con 4 decimales)
MonthlyCostUSD: Costo mensual (730h/mes, número con 2 decimales)
EffectiveDate: Fecha de vigencia del precio (YYYY-MM-DD)
Notes: Descripción adicional (ej: "Spot price; subject to fluctuation")
```

**Ejemplo**:
```
InstanceType,PurchaseOption,SKU,PricePerHourUSD,MonthlyCostUSD,EffectiveDate,Notes
m5.large,OnDemand,6QCMYABX3D,0.0960,70.08,2026-01-29,Linux; shared tenancy
m5.large,Spot,6QCMYABX3E,0.0320,23.36,2026-01-29,Spot price; subject to fluctuation
m5.large,RI_1yr_Standard_NoUpfront,6QCMYABX3F,0.0670,48.91,2026-01-29,RI Standard; 1yr; No Upfront
c6i.xlarge,OnDemand,6QCMYABX3G,0.1700,124.10,2026-01-29,Linux; shared tenancy
c6i.xlarge,Spot,6QCMYABX3H,0.0510,37.23,2026-01-29,Spot price; subject to fluctuation
c6i.xlarge,RI_1yr_Standard_NoUpfront,6QCMYABX3I,0.1190,86.87,2026-01-29,RI Standard; 1yr; No Upfront
t3.medium,OnDemand,6QCMYABX3J,0.0416,30.37,2026-01-29,Linux; shared tenancy
t3.medium,Spot,6QCMYABX3K,0.0125,9.13,2026-01-29,Spot price; subject to fluctuation
t3.medium,RI_1yr_Standard_NoUpfront,6QCMYABX3L,0.0290,21.17,2026-01-29,RI Standard; 1yr; No Upfront
```

**Reglas CSV**:
- Tiempos en formato YYYY-MM-DD
- Números: 4 decimales para precios/hora, 2 decimales para costos mensuales
- UTF-8 encoding
- Escapar comillas en Notes si es necesario

### 2. JSON: `ec2-cost-validation-us-east-1.json`

**Estructura**:

```json
{
  "metadata": {
    "region": "us-east-1",
    "currency": "USD",
    "source": "AWS Pricing API via MCP",
    "generated_at": "2026-01-29T14:30:00Z",
    "aws_profile": "user-specified",
    "operating_system": "Linux",
    "tenancy": "Shared",
    "monthly_hours": 730
  },
  "items": [
    {
      "instance_type": "m5.large",
      "purchase_option": "OnDemand",
      "sku": "6QCMYABX3D",
      "price_per_hour_usd": 0.0960,
      "monthly_cost_usd": 70.08,
      "effective_date": "2026-01-29",
      "notes": "Linux; shared tenancy"
    },
    {
      "instance_type": "m5.large",
      "purchase_option": "Spot",
      "sku": "6QCMYABX3E",
      "price_per_hour_usd": 0.0320,
      "monthly_cost_usd": 23.36,
      "effective_date": "2026-01-29",
      "notes": "Spot price; subject to fluctuation"
    },
    {
      "instance_type": "m5.large",
      "purchase_option": "RI_1yr_Standard_NoUpfront",
      "sku": "6QCMYABX3F",
      "price_per_hour_usd": 0.0670,
      "monthly_cost_usd": 48.91,
      "effective_date": "2026-01-29",
      "notes": "RI Standard; 1yr; No Upfront"
    },
    {
      "instance_type": "c6i.xlarge",
      "purchase_option": "OnDemand",
      "sku": "6QCMYABX3G",
      "price_per_hour_usd": 0.1700,
      "monthly_cost_usd": 124.10,
      "effective_date": "2026-01-29",
      "notes": "Linux; shared tenancy"
    },
    {
      "instance_type": "c6i.xlarge",
      "purchase_option": "Spot",
      "sku": "6QCMYABX3H",
      "price_per_hour_usd": 0.0510,
      "monthly_cost_usd": 37.23,
      "effective_date": "2026-01-29",
      "notes": "Spot price; subject to fluctuation"
    },
    {
      "instance_type": "c6i.xlarge",
      "purchase_option": "RI_1yr_Standard_NoUpfront",
      "sku": "6QCMYABX3I",
      "price_per_hour_usd": 0.1190,
      "monthly_cost_usd": 86.87,
      "effective_date": "2026-01-29",
      "notes": "RI Standard; 1yr; No Upfront"
    },
    {
      "instance_type": "t3.medium",
      "purchase_option": "OnDemand",
      "sku": "6QCMYABX3J",
      "price_per_hour_usd": 0.0416,
      "monthly_cost_usd": 30.37,
      "effective_date": "2026-01-29",
      "notes": "Linux; shared tenancy"
    },
    {
      "instance_type": "t3.medium",
      "purchase_option": "Spot",
      "sku": "6QCMYABX3K",
      "price_per_hour_usd": 0.0125,
      "monthly_cost_usd": 9.13,
      "effective_date": "2026-01-29",
      "notes": "Spot price; subject to fluctuation"
    },
    {
      "instance_type": "t3.medium",
      "purchase_option": "RI_1yr_Standard_NoUpfront",
      "sku": "6QCMYABX3L",
      "price_per_hour_usd": 0.0290,
      "monthly_cost_usd": 21.17,
      "effective_date": "2026-01-29",
      "notes": "RI Standard; 1yr; No Upfront"
    }
  ],
  "totals": {
    "OnDemand_monthly_usd": 224.55,
    "Spot_monthly_usd": 69.72,
    "RI_1yr_Standard_NoUpfront_monthly_usd": 156.95,
    "savings": {
      "Spot_vs_OnDemand_usd": 154.83,
      "Spot_vs_OnDemand_percent": 68.96,
      "RI_vs_OnDemand_usd": 67.60,
      "RI_vs_OnDemand_percent": 30.10
    }
  }
}
```

**Reglas JSON**:
- Formato válido JSON (validable con `jq` o similar)
- Números: 4 decimales para precios/hora, 2 decimales para costos
- Fechas en ISO8601 UTC
- Metadata incluye contexto completo (región, SO, tenancy, horas/mes)
- Totales incluyen ahorros en USD y porcentaje

---

## Reglas de Implementación

### Consultas MCP
- Todas las consultas deben usar AWS Pricing API via MCP
- Incluir `SKU` y `EffectiveDate` en todas las salidas
- Validar que precios sean recientes (< 7 días)
- Precios Spot deben ser actuales (no promedio histórico)

### Formato de Datos
- Tiempos: ISO8601 UTC (ej: 2026-01-29T14:30:00Z)
- Números: 4 decimales para precios/hora, 2 decimales para costos mensuales
- CSV: UTF-8, delimitado por comas, con escaping de comillas
- JSON: Válido, indentado con 2 espacios

### Validaciones
- Verificar que PricePerHourUSD > 0
- Verificar que MonthlyCostUSD = PricePerHourUSD * 730
- Verificar que SKU no está vacío
- Verificar que EffectiveDate es reciente

### Instancias Fijas
- m5.large
- c6i.xlarge
- t3.medium

### Modalidades Fijas
- OnDemand
- Spot (precio actual)
- RI_1yr_Standard_NoUpfront

### SO y Tenancy Fijos
- Operating System: Linux
- Tenancy: Shared

---

## Interpretación de Resultados

### Cuándo usar cada modalidad

**On-Demand**:
- Cargas impredecibles
- Desarrollo/testing
- Corta duración
- Máxima flexibilidad

**Spot**:
- Cargas tolerantes a interrupciones
- Batch jobs, procesamiento de datos
- Máximo ahorro (hasta 90%)
- Riesgo: puede ser interrumpido

**Reserved Instances (1yr)**:
- Cargas predecibles y estables
- Producción 24/7
- Ahorro ~30-40%
- Compromiso de 1 año

### Ejemplo de Análisis

```
Escenario: 3 instancias corriendo 24/7 durante 1 año

On-Demand:
  m5.large: $70.08/mes × 12 = $840.96/año
  c6i.xlarge: $124.10/mes × 12 = $1,489.20/año
  t3.medium: $30.37/mes × 12 = $364.44/año
  Total: $2,694.60/año

Spot (con riesgo de interrupción):
  m5.large: $23.36/mes × 12 = $280.32/año
  c6i.xlarge: $37.23/mes × 12 = $446.76/año
  t3.medium: $9.13/mes × 12 = $109.56/año
  Total: $836.64/año
  Ahorro: $1,857.96/año (68.96%)

Reserved Instances (1yr, Standard, No Upfront):
  m5.large: $48.91/mes × 12 = $587.00/año
  c6i.xlarge: $86.87/mes × 12 = $1,042.44/año
  t3.medium: $21.17/mes × 12 = $254.04/año
  Total: $1,883.48/año
  Ahorro: $811.12/año (30.10%)
```

---

## Próximos Pasos

1. **Revisar Precios**: Validar que los precios coincidan con AWS Console
2. **Evaluar Modalidad**: Seleccionar según patrón de uso
3. **Considerar Riesgo**: Spot es más barato pero puede interrumpirse
4. **Planificar Compra**: RI requiere compromiso de 1 año
5. **Monitorear**: Ejecutar análisis mensualmente para detectar cambios de precio
