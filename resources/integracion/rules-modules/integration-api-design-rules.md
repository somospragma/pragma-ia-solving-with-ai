# Reglas de Diseño de APIs y Contratos de Integración

## 1. Diseño RESTful

### 1.1 Principios REST
- Usar recursos como sustantivos (no verbos)
- Aplicar métodos HTTP correctamente:
  - **GET**: Recuperar recursos (idempotente, sin efectos secundarios)
  - **POST**: Crear nuevos recursos
  - **PUT**: Actualizar recursos completos (idempotente)
  - **PATCH**: Actualizar recursos parcialmente
  - **DELETE**: Eliminar recursos (idempotente)

### 1.2 Estructura de URIs
```
✅ Correcto:
GET /api/v1/customers
GET /api/v1/customers/{id}
POST /api/v1/customers
PUT /api/v1/customers/{id}
DELETE /api/v1/customers/{id}
GET /api/v1/customers/{id}/orders

❌ Incorrecto:
GET /api/v1/getCustomers
POST /api/v1/createCustomer
GET /api/v1/customer-delete/{id}
```

### 1.3 Códigos de Estado HTTP
- **2xx Success**:
  - 200 OK: Operación exitosa con respuesta
  - 201 Created: Recurso creado exitosamente
  - 204 No Content: Operación exitosa sin respuesta
- **4xx Client Errors**:
  - 400 Bad Request: Request inválido
  - 401 Unauthorized: Autenticación requerida
  - 403 Forbidden: Sin permisos
  - 404 Not Found: Recurso no encontrado
  - 409 Conflict: Conflicto de estado
  - 422 Unprocessable Entity: Validación fallida
- **5xx Server Errors**:
  - 500 Internal Server Error: Error del servidor
  - 502 Bad Gateway: Error de gateway
  - 503 Service Unavailable: Servicio no disponible
  - 504 Gateway Timeout: Timeout de gateway

## 2. Versionamiento de APIs

### 2.1 Estrategias
```
✅ URI Versioning (Recomendado):
/api/v1/customers
/api/v2/customers

✅ Header Versioning:
Accept: application/vnd.company.v1+json

✅ Query Parameter:
/api/customers?version=1

❌ Evitar: Sin versionamiento
```

### 2.2 Compatibilidad
- Mantener compatibilidad hacia atrás cuando sea posible
- Agregar campos opcionales, no eliminar existentes
- Deprecar versiones con aviso previo (6-12 meses)
- Documentar breaking changes claramente

## 3. Paginación, Filtrado y Ordenamiento

### 3.1 Paginación
```json
GET /api/v1/customers?page=1&size=20

Response:
{
  "data": [...],
  "pagination": {
    "page": 1,
    "size": 20,
    "totalPages": 5,
    "totalElements": 100
  }
}
```

### 3.2 Filtrado
```
GET /api/v1/customers?status=active&country=US
GET /api/v1/orders?minAmount=100&maxAmount=1000
```

### 3.3 Ordenamiento
```
GET /api/v1/customers?sort=lastName,asc&sort=firstName,asc
```

## 4. Estructura de Respuestas

### 4.1 Respuestas Exitosas
```json
{
  "data": {
    "id": "123",
    "name": "John Doe",
    "email": "john@example.com"
  },
  "metadata": {
    "timestamp": "2024-01-15T10:30:00Z",
    "version": "v1"
  }
}
```

### 4.2 Respuestas de Error
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ],
    "timestamp": "2024-01-15T10:30:00Z",
    "traceId": "abc-123-def-456"
  }
}
```

## 5. Diseño SOAP

### 5.1 Estructura WSDL
- Definir tipos de datos con XSD
- Usar namespaces apropiados
- Documentar operaciones y parámetros
- Versionar schemas

### 5.2 WS-Security
```xml
<wsse:Security>
  <wsse:UsernameToken>
    <wsse:Username>user</wsse:Username>
    <wsse:Password Type="PasswordDigest">...</wsse:Password>
  </wsse:UsernameToken>
</wsse:Security>
```

### 5.3 SOAP Faults
```xml
<soap:Fault>
  <faultcode>soap:Client</faultcode>
  <faultstring>Invalid Request</faultstring>
  <detail>
    <errorCode>ERR_001</errorCode>
    <errorMessage>Missing required field</errorMessage>
  </detail>
</soap:Fault>
```

## 6. Contratos de Datos

### 6.1 JSON Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "id": {"type": "string"},
    "name": {"type": "string", "minLength": 1},
    "email": {"type": "string", "format": "email"},
    "age": {"type": "integer", "minimum": 0}
  },
  "required": ["name", "email"]
}
```

### 6.2 XML Schema (XSD)
```xml
<xs:element name="Customer">
  <xs:complexType>
    <xs:sequence>
      <xs:element name="id" type="xs:string"/>
      <xs:element name="name" type="xs:string"/>
      <xs:element name="email" type="xs:string"/>
    </xs:sequence>
  </xs:complexType>
</xs:element>
```

## 7. Especificaciones OpenAPI

### 7.1 Estructura Básica
```yaml
openapi: 3.0.0
info:
  title: Customer API
  version: 1.0.0
  description: API para gestión de clientes
servers:
  - url: https://api.example.com/v1
paths:
  /customers:
    get:
      summary: Listar clientes
      parameters:
        - name: page
          in: query
          schema:
            type: integer
      responses:
        '200':
          description: Lista de clientes
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CustomerList'
components:
  schemas:
    Customer:
      type: object
      properties:
        id:
          type: string
        name:
          type: string
```

## 8. APIs Asíncronas

### 8.1 AsyncAPI
```yaml
asyncapi: 2.0.0
info:
  title: Order Events API
  version: 1.0.0
channels:
  order/created:
    subscribe:
      message:
        payload:
          type: object
          properties:
            orderId:
              type: string
            customerId:
              type: string
```

### 8.2 Webhooks
- Implementar retry con backoff exponencial
- Validar signatures (HMAC)
- Soportar idempotencia
- Documentar eventos y payloads

## 9. Seguridad en APIs

### 9.1 Autenticación
- OAuth 2.0 / OpenID Connect (recomendado)
- API Keys (solo para APIs internas)
- JWT tokens
- Mutual TLS para B2B

### 9.2 Rate Limiting
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640000000
```

### 9.3 CORS
```
Access-Control-Allow-Origin: https://example.com
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Content-Type, Authorization
```

## 10. HATEOAS

### 10.1 Hypermedia Links
```json
{
  "id": "123",
  "name": "John Doe",
  "_links": {
    "self": {"href": "/customers/123"},
    "orders": {"href": "/customers/123/orders"},
    "update": {"href": "/customers/123", "method": "PUT"},
    "delete": {"href": "/customers/123", "method": "DELETE"}
  }
}
```

## 11. Documentación

### 11.1 Elementos Requeridos
- Descripción clara del propósito
- Ejemplos de request/response
- Códigos de error posibles
- Requisitos de autenticación
- Rate limits
- Changelog de versiones

### 11.2 Herramientas
- Swagger UI para OpenAPI
- Postman Collections
- API Blueprint
- RAML

## 12. Mejores Prácticas

### 12.1 Naming Conventions
- Usar kebab-case o camelCase consistentemente
- Nombres descriptivos y concisos
- Plural para colecciones (/customers)
- Singular para recursos individuales (/customer/{id})

### 12.2 Performance
- Implementar ETags para caching
- Soportar compresión (gzip)
- Usar campos sparse (field selection)
- Implementar GraphQL para queries complejas

### 12.3 Idempotencia
- GET, PUT, DELETE deben ser idempotentes
- POST puede usar Idempotency-Key header
- Validar operaciones duplicadas
