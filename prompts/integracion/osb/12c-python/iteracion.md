# Iteración de Migración OSB 12c → AWS Lambda

## Objetivo
Migrar servicios OSB a AWS Lambda de forma iterativa, un servicio a la vez, manteniendo paridad funcional.

**Principio:** OSB queda intacto. Solo extraemos lógica y reimplementamos en Lambda.

---

## Proceso de Iteración (Por Servicio)

### PASO 1: Análisis OSB 

#### 1.1 Identificar Servicio
- Seleccionar servicio OSB a migrar
- Priorizar por: criticidad, complejidad, dependencias

#### 1.2 Documentar Componente
Crear archivo `EXTRACTION.md`:

```markdown
# Extracción: [Nombre Servicio OSB]

## Servicio Original
- **Nombre:** CustomerOrderProxy
- **Tipo:** Proxy Service / Business Service / Pipeline
- **Endpoint:** /orders/create
- **Método:** POST
- **Volumetría:** 50 TPS promedio, 200 TPS pico

## Input/Output
### Request Schema
[XML/JSON del request]

### Response Schema
[XML/JSON del response]

## Lógica de Negocio
1. Validar customerId en CRM
2. Transformar XML → JSON
3. Calcular total
4. Verificar inventario
5. Generar orderId

## Transformaciones
- XQuery: [descripción]
- XSLT: [descripción]
- Java Callout: [descripción]

## Dependencias Externas
- CRM API: https://crm.example.com/api/v1
- Inventory Service: http://inventory.internal/check
- Payment Gateway: https://payment.example.com/process

## Decisión de Arquitectura
- [ ] Lambda simple (< 5 pasos)
- [ ] Step Functions (> 5 pasos, orquestación compleja)
- [ ] API Gateway (endpoint REST)
- [ ] SQS trigger (asíncrono)
```

---

### PASO 2: Implementación Lambda

#### 2.1 Crear Estructura
```bash
./create-service.sh customer-order
cd lambda-services/customer-order
```

Genera:
```
customer-order/
├── src/
│   ├── handler.py
│   ├── models.py
│   ├── services/
│   ├── clients/
│   └── requirements.txt
├── tests/
├── template.yaml
├── parameters-dev.json
├── parameters-qa.json
├── parameters-prod.json
└── EXTRACTION.md
```

#### 2.2 Implementar Handler
Editar `src/handler.py`:

```python
import json
from services.validation import validate_customer
from services.transformation import transform_order
from clients.inventory_client import check_inventory

def lambda_handler(event, context):
    try:
        # Parse
        body = json.loads(event.get('body', '{}'))
        
        # Validate
        validate_customer(body['customerId'])
        
        # Transform
        order = transform_order(body)
        
        # Process
        check_inventory(order['items'])
        order_id = generate_order_id()
        
        # Response
        return {
            'statusCode': 200,
            'body': json.dumps({
                'orderId': order_id,
                'status': 'CREATED'
            })
        }
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
```

#### 2.3 Implementar Lógica de Negocio
- `services/validation.py` - Validaciones
- `services/transformation.py` - Transformaciones
- `clients/inventory_client.py` - Clientes externos

#### 2.4 Definir Schemas
Editar `src/models.py`:

```python
from pydantic import BaseModel
from typing import List

class OrderItem(BaseModel):
    productId: str
    quantity: int

class OrderRequest(BaseModel):
    customerId: str
    items: List[OrderItem]

class OrderResponse(BaseModel):
    orderId: str
    status: str
```

---

### PASO 3: Testing 

#### 3.1 Tests Unitarios
```bash
cd lambda-services/customer-order
pytest tests/ --cov=src --cov-report=term-missing
```

Objetivo: > 80% coverage

#### 3.2 Tests de Integración
```python
# tests/test_integration.py
def test_full_flow():
    event = {
        'body': json.dumps({
            'customerId': '123',
            'items': [{'productId': 'P1', 'quantity': 2}]
        })
    }
    response = lambda_handler(event, {})
    assert response['statusCode'] == 200
```

---

### PASO 4: CloudFormation

#### 4.1 Seleccionar Template
Ver archivo `cloudformation.md` para templates:
- `service-template.yaml` - Lambda básica
- `api-service-template.yaml` - Lambda + API Gateway
- `vpc-service-template.yaml` - Lambda en VPC
- `stepfunctions-template.yaml` - Orquestación compleja

#### 4.2 Personalizar Parámetros
Editar `parameters-dev.json`

#### 4.3 Validar Template
```bash
aws cloudformation validate-template --template-body file://template.yaml
```

---

### PASO 5: Despliegue Dev 

```bash
./deploy.sh customer-order dev
```

Verificar:
- Lambda creada
- Logs en CloudWatch
- DLQ configurada
- Alarmas activas

---

### PASO 6: Validación Dev 

#### 6.1 Pruebas Funcionales
```bash
# Invocar Lambda
aws lambda invoke \
  --function-name customer-order-dev \
  --payload '{"body": "{\"customerId\":\"123\"}"}' \
  response.json

cat response.json
```

#### 6.2 Revisar Logs
```bash
aws logs tail /aws/lambda/customer-order-dev --follow
```

#### 6.3 Verificar Métricas
- Invocations
- Errors
- Duration
- Throttles


#### 6.4 Tests Funcionales
- Casos de éxito
- Casos de error
- Casos límite

#### 8.2 Tests de Carga
```bash
# Usar Artillery, JMeter o similar
artillery quick --count 100 --num 10 https://api-qa.example.com/orders/create
```



## Checklist por Servicio

### Documentación
- [ ] EXTRACTION.md actualizado
- [ ] README.md con instrucciones
- [ ] Diagramas de arquitectura
- [ ] Runbook de troubleshooting

## Referencias

- **Arquitectura AWS:** Ver `arquitectura.md`
- **Templates CloudFormation:** Ver `cloudformation.md`
- **Reglas de Migración:** Ver `rules.md`

---

## Reglas de Oro

1. **Un servicio a la vez** - No paralelizar hasta dominar el proceso
2. **Tests primero** - No desplegar sin > 80% coverage
3. **Dev → QA → Prod** - Sin excepciones
4. **Infrastructure as Code** - Todo en CloudFormation
5. **Monitoring desde día 1** - Logs, métricas y alarmas obligatorias
6. **Rollback plan** - Siempre listo antes de desplegar
7. **Documentación obligatoria** - EXTRACTION.md + README.md
8. **No tocar OSB** - Solo leer, nunca modificar
9. **Validación paralela** - Comparar respuestas antes de cutover
10. **Gradual cutover** - 10% → 50% → 100%
