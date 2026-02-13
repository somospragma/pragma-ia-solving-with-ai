# Guía de Migración OSB 12c → AWS Lambda
## Reglas Simplificadas para Python

---

## Principio Fundamental

Esta es una **REESCRITURA FUNCIONAL**, no una actualización de versión. Extraemos la lógica de OSB y la reimplementamos en AWS Lambda manteniendo la paridad funcional con arquitectura serverless.

---

## 1. Mapeo OSB → AWS

| Componente OSB | Servicio AWS | Implementación |
|----------------|--------------|----------------|
| **Proxy Service** | API Gateway + Lambda | Handler con event/context |
| **Business Service** | Lambda Client | Función helper HTTP |
| **Pipeline** | Lambda Function | Función con steps |
| **Message Flow** | Step Functions | State machine JSON |
| **XQuery/XSLT** | Lambda | Función Python |
| **JMS/MQ** | SQS/SNS | Event-driven trigger |
| **Security** | IAM + Secrets | Roles y policies |

---

## 2. Estructura Lambda Handler

```python
def lambda_handler(event, context):
    try:
        # 1. Parsear input
        body = json.loads(event.get('body', '{}'))
        
        # 2. Validar
        validated = validate_input(body)
        
        # 3. Transformar
        result = transform_data(validated)
        
        # 4. Responder
        return {
            'statusCode': 200,
            'body': json.dumps(result),
            'headers': {'Content-Type': 'application/json'}
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
```

---

## 3. Librerías Esenciales

### Core (siempre incluir)
- **boto3** - AWS SDK
- **pydantic** - Validación de datos

### Por caso de uso
- **XML:** `xmltodict` (ligero, evitar lxml)
- **HTTP:** `urllib3` o `requests`
- **SOAP:** `zeep` (solo si necesario)
- **Retry:** `tenacity`
- **Logging:** `aws-lambda-powertools`

---

## 4. Patrones de Migración

### Transformación de datos

```python
from pydantic import BaseModel
from typing import List

class Customer(BaseModel):
    name: str

def transform(customers: List[Customer]) -> List[dict]:
    return [{'name': c.name} for c in customers]
```

### Llamadas externas

```python
import urllib3
import json

http = urllib3.PoolManager()

def call_service(payload: dict) -> dict:
    response = http.request(
        'POST',
        'https://api.example.com',
        body=json.dumps(payload),
        headers={'Content-Type': 'application/json'}
    )
    return json.loads(response.data)
```

### Enrutamiento condicional

```python
def route_message(message: dict) -> dict:
    handlers = {
        'A': process_type_a,
        'B': process_type_b
    }
    handler = handlers.get(message['type'])
    return handler(message)
```

---

## 5. Configuración AWS

### Variables de entorno

```python
import os

CONFIG = {
    'api_url': os.environ['EXTERNAL_API_URL'],
    'timeout': int(os.environ.get('TIMEOUT', '30')),
    'retry': int(os.environ.get('RETRY_ATTEMPTS', '3'))
}
```

### Secrets Manager

```python
import boto3
import json

def get_secret(name: str) -> dict:
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=name)
    return json.loads(response['SecretString'])
```

---

## 6. Observabilidad

### Logging a CloudWatch

```python
import json
from datetime import datetime

def log_event(level: str, message: str, **kwargs):
    log_entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'level': level,
        'message': message,
        **kwargs
    }
    print(json.dumps(log_entry))
```

### Retry con backoff

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def call_api(url: str):
    # Retry automático
    pass
```

---

## 7. Anti-Patrones (EVITAR)

| ❌ NO HACER | ✓ HACER |
|-------------|---------|
| Dependencias pesadas (pandas, numpy) | Librerías ligeras (xmltodict, boto3) |
| Estado en memoria | DynamoDB o S3 para persistencia |
| Configuración hardcoded | Variables de entorno o Secrets Manager |
| Logging a archivos locales | `print()` para CloudWatch Logs |
| Timeouts > 15 minutos | Step Functions para procesos largos |
| Conexiones en cada invocación | Reutilizar conexiones fuera del handler |

---

## 8. Checklist de Migración

1. Identificar tipo de componente OSB (Proxy/Business/Pipeline)
2. Extraer lógica de negocio del XML/XQuery
3. Mapear transformaciones de datos a Python
4. Crear función Lambda con handler
5. Configurar variables de entorno
6. Implementar IAM roles y policies
7. Agregar logging estructurado
8. Implementar retry logic
9. Crear tests unitarios
10. Validar paridad funcional
11. Configurar API Gateway (si aplica)
12. Configurar Dead Letter Queue (DLQ)
13. Realizar pruebas de performance

---

## 9. requirements.txt

```txt
boto3==1.34.0
pydantic==2.5.0
tenacity==8.2.3
xmltodict==0.13.0
aws-lambda-powertools==2.30.0
```

---

## 10. Estructura de Proyecto

```
lambda-function/
├── handler.py          # Lambda handler
├── services/           # Lógica de negocio
├── clients/            # Clientes externos
├── models.py           # Pydantic schemas
├── utils.py            # Helpers
├── requirements.txt    # Dependencias
└── tests/              # Tests unitarios
```

---

## Reglas de Oro

1. **Minimizar dependencias** para reducir cold start
2. **Sin estado en memoria** - Lambda es stateless
3. **Timeout máximo 15 min** - usar Step Functions para más
4. **Variables de entorno** para configuración
5. **Secrets Manager** para credenciales
6. **CloudWatch** para logs (usar `print()`)
7. **Retry automático** con tenacity
8. **DLQ** para mensajes fallidos
9. **Tests unitarios** obligatorios
10. **Paridad funcional** con OSB original