# Arquitectura AWS - Migración OSB a Lambda

## Stack Tecnológico

### Servicios AWS por Componente OSB

| OSB Component | AWS Service | Propósito |
|---------------|-------------|-----------|
| Proxy Service | API Gateway + Lambda | Endpoints REST |
| Business Service | Lambda Function | Clientes externos |
| Pipeline simple | Lambda Function | Orquestación básica |
| Pipeline complejo | Step Functions | Orquestación avanzada |
| JMS/MQ | SQS/SNS | Mensajería asíncrona |
| Transformación | Lambda Function | Lógica de negocio |
| Throttling | API Gateway | Rate limiting |
| Security | IAM + Cognito + Secrets Manager | Autenticación/Autorización |

---

## Estructura de Proyecto Lambda

```
lambda-service-name/
├── src/
│   ├── handler.py          # Entry point
│   ├── models.py           # Pydantic schemas
│   ├── services/           # Lógica de negocio
│   │   ├── validation.py
│   │   └── transformation.py
│   ├── clients/            # Clientes externos
│   │   └── external_api.py
│   └── utils.py            # Helpers
├── tests/
│   ├── test_handler.py
│   └── test_services.py
├── template.yaml           # CloudFormation
├── parameters-dev.json
├── parameters-qa.json
├── parameters-prod.json
├── requirements.txt
└── EXTRACTION.md          # Documentación OSB
```

---

## Handler Pattern (Template)

```python
import json
from typing import Dict, Any

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Lambda handler template."""
    try:
        # 1. Parse input
        body = json.loads(event.get('body', '{}'))
        
        # 2. Validate
        validated = validate_input(body)
        
        # 3. Transform
        transformed = transform_data(validated)
        
        # 4. Process
        result = process_business_logic(transformed)
        
        # 5. Response
        return {
            'statusCode': 200,
            'body': json.dumps(result),
            'headers': {'Content-Type': 'application/json'}
        }
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
```

---

## Organización de Stacks

```
cloudformation/
├── shared/
│   ├── vpc.yaml                    # Red compartida
│   ├── security-groups.yaml        # Security groups
│   └── iam-roles.yaml              # Roles IAM
├── services/
│   ├── service-a/
│   │   ├── template.yaml
│   │   ├── parameters-dev.json
│   │   ├── parameters-qa.json
│   │   └── parameters-prod.json
│   └── service-b/
│       └── ...
└── monitoring/
    └── dashboards.yaml             # CloudWatch dashboards
```

---

## Recursos AWS por Lambda

### Mínimos Requeridos
- Lambda Function
- IAM Execution Role
- CloudWatch Log Group
- Dead Letter Queue (SQS)

### Opcionales según caso
- API Gateway (si es endpoint REST)
- VPC Configuration (si accede recursos privados)
- Secrets Manager (credenciales)
- CloudWatch Alarms (monitoreo)
- X-Ray Tracing (debugging)

## Métricas Clave

### Performance
- Latency (p50, p95, p99)
- Throughput (requests/sec)
- Cold starts (count)
- Memory utilization (%)

### Reliability
- Error rate (%)
- Throttles (count)
- DLQ messages (count)
- Availability (%)

### Cost
- Invocations (count)
- Duration (GB-seconds)
- Data transfer (GB)
- Cost per request ($)

---

## Alarmas CloudWatch

### Críticas (Pager)
- Error rate > 5%
- Latency p99 > 2s
- Availability < 99%

### Advertencia (Email)
- Error rate > 1%
- Latency p95 > 500ms
- Throttles > 10/min
- DLQ messages > 0

### Informativas (Dashboard)
- Cold starts > 20/min
- Memory > 80%
- Cost spike > 20%
