# IS4 - Validación de Entrada

## Descripción
Reglas para validación y sanitización de datos de entrada.

## Severidad: HIGH

## Reglas

### IS4.1 Validación contra Schemas
- ✅ JSON Schema para APIs REST
- ✅ XSD para SOAP/XML
- ✅ Validación estricta
- ✅ Rechazar datos inválidos (400 Bad Request)

### IS4.2 Whitelist de Caracteres
- ✅ Definir caracteres permitidos
- ✅ Rechazar caracteres no permitidos
- ✅ Validación por tipo de campo
- ✅ Escapar caracteres especiales

### IS4.3 Validación de Tipos
- ✅ Validar tipos de datos
- ✅ Validar rangos numéricos
- ✅ Validar formatos (email, URL, fecha)
- ✅ Conversión segura de tipos

### IS4.4 Límites de Tamaño
- ✅ Límite de tamaño de payload
- ✅ Límite de longitud de strings
- ✅ Límite de elementos en arrays
- ✅ Protección contra DoS

### IS4.5 Sanitización de Entrada
- ✅ Sanitizar antes de procesar
- ✅ Remover caracteres peligrosos
- ✅ Normalizar datos
- ✅ Validar encoding (UTF-8)

### IS4.6 Prevención de Inyección SQL
- ✅ Usar prepared statements
- ✅ Parametrizar queries
- ✅ No construir SQL con concatenación
- ✅ ORM con protección integrada

### IS4.7 Prevención de XPath Injection
- ✅ Parametrizar expresiones XPath
- ✅ Validar entrada XML
- ✅ Usar APIs seguras
- ✅ Escapar caracteres especiales

### IS4.8 Prevención de Command Injection
- ✅ Evitar ejecución de comandos del sistema
- ✅ Si es necesario, usar whitelist
- ✅ Validar y escapar argumentos
- ✅ Usar APIs en lugar de shell

### IS4.9 Validación de Headers HTTP
- ✅ Validar headers personalizados
- ✅ Límite de tamaño de headers
- ✅ Validar Content-Type
- ✅ Protección contra header injection

### IS4.10 Validación de Archivos
- ✅ Validar tipo de archivo (MIME type)
- ✅ Validar extensión
- ✅ Límite de tamaño
- ✅ Escaneo de malware
