# IS8 - Prevención de Inyección

## Descripción
Reglas para prevenir ataques de inyección (SQL, XPath, Command, etc.).

## Severidad: CRITICAL

## Reglas

### IS8.1 SQL Injection Prevention
- ✅ Usar prepared statements
- ✅ Parametrizar todas las queries
- ❌ No construir SQL con concatenación
- ✅ ORM con protección integrada
- ✅ Validar entrada antes de usar en queries

### IS8.2 XPath Injection Prevention
- ✅ Parametrizar expresiones XPath
- ✅ Validar entrada XML
- ✅ Usar APIs seguras
- ✅ Escapar caracteres especiales XML

### IS8.3 LDAP Injection Prevention
- ✅ Validar entrada LDAP
- ✅ Escapar caracteres especiales
- ✅ Usar APIs parametrizadas
- ✅ Whitelist de caracteres permitidos

### IS8.4 Command Injection Prevention
- ❌ Evitar ejecución de comandos del sistema
- ✅ Si es necesario, usar whitelist estricta
- ✅ Validar y escapar todos los argumentos
- ✅ Usar APIs en lugar de shell commands

### IS8.5 NoSQL Injection Prevention
- ✅ Validar entrada para MongoDB, etc.
- ✅ Usar queries parametrizadas
- ✅ Validar tipos de datos
- ✅ Sanitizar operadores

### IS8.6 XML External Entity (XXE) Prevention
- ✅ Deshabilitar external entities
- ✅ Deshabilitar DTD processing
- ✅ Usar parsers seguros
- ✅ Validar XML contra schema

### IS8.7 Server-Side Template Injection Prevention
- ✅ No usar entrada de usuario en templates
- ✅ Sandbox para templates
- ✅ Validar entrada estrictamente
- ✅ Usar templates precompilados

### IS8.8 Expression Language Injection Prevention
- ✅ No evaluar expresiones de usuario
- ✅ Validar entrada antes de evaluar
- ✅ Usar whitelist de funciones
- ✅ Sandbox para evaluación

### IS8.9 Code Injection Prevention
- ❌ No usar eval() o similar
- ❌ No ejecutar código de usuario
- ✅ Validación estricta si es necesario
- ✅ Sandbox aislado

### IS8.10 Header Injection Prevention
- ✅ Validar headers HTTP
- ✅ Sanitizar valores de headers
- ✅ No incluir entrada de usuario en headers
- ✅ Validar CRLF characters
