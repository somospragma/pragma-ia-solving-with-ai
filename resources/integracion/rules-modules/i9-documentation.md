# I9 - Documentación

## Descripción
Este ruleset evalúa la calidad y completitud de la documentación técnica y de negocio.

## Severidad: MEDIUM

## Reglas

### 9.1 Especificación de API
**Severidad**: HIGH

**Descripción**: Todas las APIs deben tener especificación formal.

**Criterios**:
- ✅ OpenAPI/Swagger para REST
- ✅ WSDL para SOAP
- ✅ AsyncAPI para eventos
- ✅ Especificación actualizada con el código
- ✅ Generación automática cuando sea posible

---

### 9.2 Descripción de Endpoints
**Severidad**: MEDIUM

**Descripción**: Cada endpoint debe estar documentado.

**Criterios**:
- ✅ Descripción clara del propósito
- ✅ Parámetros documentados (path, query, body)
- ✅ Respuestas documentadas (success, error)
- ✅ Códigos de estado HTTP explicados
- ✅ Requisitos de autenticación

**Ejemplo OpenAPI**:
```yaml
/customers/{id}:
  get:
    summary: Obtener cliente por ID
    description: Retorna los detalles de un cliente específico
    parameters:
      - name: id
        in: path
        required: true
        schema:
          type: string
    responses:
      '200':
        description: Cliente encontrado
      '404':
        description: Cliente no encontrado
      '401':
        description: No autenticado
```

---

### 9.3 Ejemplos de Request/Response
**Severidad**: MEDIUM

**Descripción**: Incluir ejemplos prácticos.

**Criterios**:
- ✅ Ejemplo de request exitoso
- ✅ Ejemplo de response exitoso
- ✅ Ejemplos de errores comunes
- ✅ Ejemplos en múltiples formatos (JSON, XML)

---

### 9.4 Códigos de Error Documentados
**Severidad**: HIGH

**Descripción**: Documentar todos los códigos de error posibles.

**Criterios**:
- ✅ Catálogo de códigos de error
- ✅ Descripción de cada código
- ✅ Causa probable
- ✅ Acción recomendada

**Ejemplo**:
```markdown
| Código | Descripción | Causa | Acción |
|--------|-------------|-------|--------|
| AUTH_001 | Token inválido | Token expirado o malformado | Renovar token |
| VAL_001 | Campo requerido | Falta campo obligatorio | Incluir campo |
```

---

### 9.5 Diagramas de Flujo
**Severidad**: MEDIUM

**Descripción**: Incluir diagramas para flujos complejos.

**Criterios**:
- ✅ Diagramas de secuencia
- ✅ Diagramas de flujo
- ✅ Diagramas de arquitectura
- ✅ Actualizados con cambios

**Herramientas**:
- PlantUML
- Mermaid
- Draw.io
- Lucidchart

---

### 9.6 README Completo
**Severidad**: MEDIUM

**Descripción**: Proyecto debe tener README informativo.

**Criterios**:
- ✅ Descripción del proyecto
- ✅ Requisitos y dependencias
- ✅ Instrucciones de instalación
- ✅ Instrucciones de ejecución
- ✅ Configuración requerida
- ✅ Links a documentación adicional

---

### 9.7 Guías de Troubleshooting
**Severidad**: MEDIUM

**Descripción**: Documentar problemas comunes y soluciones.

**Criterios**:
- ✅ Errores comunes documentados
- ✅ Pasos de diagnóstico
- ✅ Soluciones conocidas
- ✅ Contactos de soporte

**Ejemplo**:
```markdown
## Problema: Timeout al conectar a base de datos

### Síntomas
- Error: Connection timeout after 5000ms
- Logs muestran: "Unable to connect to database"

### Diagnóstico
1. Verificar conectividad de red
2. Validar credenciales
3. Revisar firewall

### Solución
- Aumentar timeout en configuración
- Verificar que DB esté accesible
```

---

### 9.8 SLAs y SLOs Documentados
**Severidad**: HIGH

**Descripción**: Documentar acuerdos de nivel de servicio.

**Criterios**:
- ✅ Disponibilidad esperada (ej: 99.9%)
- ✅ Tiempo de respuesta (ej: <200ms p95)
- ✅ Throughput (ej: 1000 req/s)
- ✅ Ventanas de mantenimiento
- ✅ Procedimientos de escalamiento

---

### 9.9 Changelog Mantenido
**Severidad**: MEDIUM

**Descripción**: Mantener historial de cambios.

**Criterios**:
- ✅ Archivo CHANGELOG.md
- ✅ Cambios por versión
- ✅ Breaking changes marcados
- ✅ Fechas de release

---

### 9.10 Documentación de Configuración
**Severidad**: HIGH

**Descripción**: Documentar todas las configuraciones.

**Criterios**:
- ✅ Variables de entorno documentadas
- ✅ Archivos de configuración explicados
- ✅ Valores por defecto indicados
- ✅ Configuraciones por ambiente

**Ejemplo**:
```markdown
## Variables de Entorno

| Variable | Descripción | Requerido | Default |
|----------|-------------|-----------|---------|
| DB_HOST | Host de base de datos | Sí | - |
| DB_PORT | Puerto de base de datos | No | 5432 |
| LOG_LEVEL | Nivel de logging | No | INFO |
```

---

## Checklist de Evaluación

| ID | Criterio | Cumple | Observaciones |
|----|----------|--------|---------------|
| 9.1 | Especificación de API | ⬜ | |
| 9.2 | Descripción de endpoints | ⬜ | |
| 9.3 | Ejemplos de request/response | ⬜ | |
| 9.4 | Códigos de error documentados | ⬜ | |
| 9.5 | Diagramas de flujo | ⬜ | |
| 9.6 | README completo | ⬜ | |
| 9.7 | Guías de troubleshooting | ⬜ | |
| 9.8 | SLAs y SLOs documentados | ⬜ | |
| 9.9 | Changelog mantenido | ⬜ | |
| 9.10 | Documentación de configuración | ⬜ | |
