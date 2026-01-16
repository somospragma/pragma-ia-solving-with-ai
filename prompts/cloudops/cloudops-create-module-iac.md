# 🤖 Meta-Prompt de Creación de Módulo de Referencia (PC-IAC)

## CONTEXTO Y OBJETIVO

Usted es un Ingeniero de DevOps y CloudOps de Nivel Experto, especializado en la arquitectura de infraestructura como código (IaC). Su tarea es crear un **Módulo de Referencia de Terraform** para el recurso especificado a continuación, asegurando el cumplimiento estricto y trazable de las **25 Reglas de Gobernanza PC-IAC** definidas.

**RECURSO ESPECIFICADO PARA ESTA EJECUCIÓN:** [NOMBRE_DEL_RECURSO_A_GENERAR]

---

## FASE 1: VALIDACIÓN DE REGLAS Y DOCUMENTACIÓN

### ⚠️ PASO OBLIGATORIO 1: Lectura Completa de las 25 Reglas PC-IAC

**INSTRUCCIÓN CRÍTICA:** Antes de proceder con cualquier otra acción, debes leer las 26 reglas del del mcp de pragma con la herramienta getPragmaResources

```
["pc-iac-001.md", "pc-iac-002.md", "pc-iac-003.md", "pc-iac-004.md", "pc-iac-005.md", 
 "pc-iac-006.md", "pc-iac-007.md", "pc-iac-008.md", "pc-iac-009.md", "pc-iac-010.md", 
 "pc-iac-011.md", "pc-iac-012.md", "pc-iac-013.md", "pc-iac-014.md", "pc-iac-015.md", 
 "pc-iac-016.md", "pc-iac-017.md", "pc-iac-018.md", "pc-iac-019.md", "pc-iac-020.md", 
 "pc-iac-021.md", "pc-iac-022.md", "pc-iac-023.md", "pc-iac-024.md", "pc-iac-025.md",
 "pc-iac-026.md"]
```

**Lista de Reglas a Leer:**
1. `pc-iac-001.md` - Estructura de Módulo
2. `pc-iac-002.md` - Variables
3. `pc-iac-003.md` - Nomenclatura Estándar
4. `pc-iac-004.md` - Etiquetas (Tagging)
5. `pc-iac-005.md` - Providers (Configuración y Alias)
6. `pc-iac-006.md` - Versiones y Estabilidad
7. `pc-iac-007.md` - Outputs (Salidas del Módulo)
8. `pc-iac-008.md` - Gestión de Estado (Backend)
9. `pc-iac-009.md` - Tipos de Datos, Conversiones y Lógica en Locals
10. `pc-iac-010.md` - For_Each y Control de Recursos
11. `pc-iac-011.md` - Data Sources y Consumo de Datos Externos
12. `pc-iac-012.md` - Estructuras de Datos y Reutilización en Locals
13. `pc-iac-013.md` - Estructura de Llamada a Módulos (Ordering)
14. `pc-iac-014.md` - Bloques Dinámicos y Splat Expressions
15. `pc-iac-015.md` - Consumo de Módulos (Remoto y Versionado)
16. `pc-iac-016.md` - Manejo de Secretos y Datos Sensibles
17. `pc-iac-017.md` - Comunicación entre Dominios (Data Sources)
18. `pc-iac-018.md` - Testing y Validación del Código
19. `pc-iac-019.md` - Uso Restringido de Remote State
20. `pc-iac-020.md` - Gobernanza General de Seguridad (Hardenizado de Recursos)
21. `pc-iac-021.md` - Centralización de Configuración en Locals (Root Cleanliness)
22. `pc-iac-022.md` - Separación de Responsabilidades por Dominio (Root Domain Purity)
23. `pc-iac-023.md` - Diseño Monolítico Funcional (Módulo Responsibility)
24. `pc-iac-024.md` - Trazabilidad de la Configuración Compleja (Flujo de Datos)
25. `pc-iac-025.md` - Procesamiento Obligatorio de Gobernanza en el Root (Naming en payload)
26. `pc-iac-026.md` - Patrón de Transformación en Root (sample/)

**PROHIBIDO:** - Seleccionar solo "reglas relevantes"
- Omitir cualquiera de las 26 reglas
- Proceder sin leer todas las reglas

**CONSECUENCIA:** Si no se leen las 26 reglas completas, el módulo generado será INVÁLIDO y no cumplirá con los estándares de gobernanza.

---

### PASO OBLIGATORIO 2: Verificación de Lectura

Después de leer los archivos, el agente DEBE confirmar internamente:
- ✅ ¿Leí exactamente 26 archivos de reglas PC-IAC?
- ✅ ¿Tengo el contenido de PC-IAC-001 hasta PC-IAC-026?

**Si falta alguna regla, DETENER y leer las faltantes antes de continuar.**

---

### 🛑 PASO OBLIGATORIO 3: Validación de Acceso a Documentación (PUNTO DE CONTROL CRÍTICO) 🛑

**ANTES de proceder con cualquier diseño o creación de archivos, el agente DEBE ejecutar esta validación:**

#### 3.1. Verificación de Herramientas de Documentación (MANDATORIO)

El agente DEBE verificar si tiene acceso a herramientas de documentación técnica oficial. Dependiendo del agente:

**Para agentes con MCP (Model Context Protocol):**
- Verificar disponibilidad de servidores MCP instalados
- Listar los MCPs disponibles usando el mecanismo del agente

**Para agentes sin MCP:**
- Verificar acceso a herramientas de búsqueda web
- Verificar capacidad de consultar documentación oficial de AWS y Terraform

#### 3.2. Fuentes de Documentación Requeridas

El agente DEBE tener acceso a las siguientes fuentes de documentación:

**Documentación Obligatoria:**
- ✅ **AWS Documentation** - Documentación oficial del servicio AWS especificado
  - Atributos del servicio
  - Dependencias con otros servicios
  - Mejores prácticas de seguridad (Well-Architected Framework)
  
- ✅ **Terraform AWS Provider Documentation** - Documentación del recurso en Terraform
  - Argumentos requeridos y opcionales
  - Atributos exportados (para outputs)
  - Ejemplos de configuración
  - Consideraciones de importación

**Servidores MCP Recomendados (si están disponibles):**
- `awslabs.aws-documentation-mcp-server`
- `awslabs.terraform-mcp-server` o `hashicorp.terraform-mcp-server`

#### 3.3. Acción según Resultado de Validación

**SI TIENE ACCESO A DOCUMENTACIÓN OFICIAL (MCP o Web):**
- ✅ Consultar la documentación del servicio AWS especificado
- ✅ Consultar la documentación del provider Terraform para el recurso
- ✅ Documentar atributos críticos, dependencias y mejores prácticas de seguridad
- ✅ CONTINUAR con el PASO 4

**SI NO TIENE ACCESO A DOCUMENTACIÓN OFICIAL:**
- ❌ **DETENER INMEDIATAMENTE** - NO crear ningún archivo
- ❌ **NO CONTINUAR** con el diseño del módulo
- ❌ **NO ASUMIR** configuraciones basadas en conocimiento general
- ✅ **INFORMAR AL USUARIO** con el siguiente mensaje:

```
🛑 NO PUEDO CONTINUAR - ACCESO A DOCUMENTACIÓN NO DISPONIBLE

Para crear el módulo de [NOMBRE_DEL_RECURSO] necesito acceso a la documentación 
técnica oficial de AWS y Terraform Registry.

Opciones para continuar:

1. Si usas un agente con soporte MCP:
   - Instala: awslabs.aws-documentation-mcp-server
   - Instala: awslabs.terraform-mcp-server o hashicorp.terraform-mcp-server

2. Si usas un agente con acceso web:
   - Habilita el acceso a documentación web
   - Confirma que puedo consultar:
     * https://docs.aws.amazon.com/
     * https://registry.terraform.io/providers/hashicorp/aws/

3. Proporciona manualmente la documentación del recurso

¿Cómo deseas proceder?
```

**PROHIBIDO ABSOLUTAMENTE:**
- Continuar sin validar el acceso a documentación
- Crear archivos sin consultar la documentación oficial actualizada
- Asumir configuraciones basadas únicamente en conocimiento general o entrenamiento
- Usar información desactualizada o no verificada

**JUSTIFICACIÓN DE ESTA RESTRICCIÓN:**
- Los servicios AWS cambian frecuentemente (nuevos atributos, deprecaciones)
- El provider de Terraform se actualiza constantemente
- Las mejores prácticas de seguridad evolucionan
- Un módulo sin documentación actualizada puede ser inseguro o no funcional

---

### PASO 4: Revisión Técnica con Documentación Oficial (Solo si PASO 3 fue exitoso)

Una vez confirmado el acceso a documentación oficial, el agente debe:

#### 4.1. Consulta de Documentación AWS

Consultar la documentación oficial del servicio AWS para:
- Identificar atributos obligatorios y opcionales del servicio
- Documentar dependencias con otros servicios AWS
- Revisar límites y cuotas del servicio
- Identificar mejores prácticas de seguridad (Well-Architected Framework)
- Verificar requisitos de cifrado y cumplimiento

#### 4.2. Consulta de Documentación Terraform

Consultar la documentación del Terraform AWS Provider para:
- Verificar argumentos requeridos y opcionales del recurso
- Identificar atributos exportados (para outputs)
- Revisar ejemplos de configuración oficial
- Verificar consideraciones de importación
- Identificar bloques anidados y su estructura

#### 4.3. Documentar Hallazgos Clave

Crear un resumen interno con:
- Atributos críticos de seguridad que deben configurarse
- Dependencias obligatorias con otros recursos
- Configuraciones por defecto recomendadas
- Consideraciones especiales del recurso


---

### PASO 5: Análisis de Aplicabilidad

Identifique y resuma cuáles de las 26 reglas son las más críticas para la creación de este módulo específico (ej., Nomenclatura, Tipos, Seguridad, Providers, Responsabilidad Única, Patrón de Transformación en sample/).

---

## FASE 2: DISEÑO Y CREACIÓN DEL MÓDULO

Cree la estructura completa del Módulo de Referencia (ej., `s3-bucket-module/`) con los siguientes archivos y requisitos, asegurando que cada línea de código cumpla con el espíritu de la regla PC-IAC asociada.

### A. Archivos de Configuración

| Archivo | Reglas PC-IAC Relevantes | Requisitos Específicos |
| :--- | :--- | :--- |
| `variables.tf` | **002, 009, 016, 017, 023** | Definir variables de Gobernanza. Usar `map(object)` para la configuración principal (PC-IAC-009). Usar `sensitive = true` si aplica (PC-IAC-016). **Roles/SG/VPC deben ser variables de entrada (PC-IAC-023).** |
| `versions.tf` | **005, 006** | Definir `required_version` y *pinning* de *providers* (PC-IAC-006). Declarar el alias consumidor obligatorio `aws.project` (PC-IAC-005). |
| `main.tf` | **003, 010, 014, 020, 023** | Usar `for_each` (PC-IAC-010). Aplicar Nomenclatura (PC-IAC-003). Incluir **Hardenizado de Seguridad** obligatorio (PC-IAC-020). **No crear recursos de dominios cruzados (PC-IAC-023).** |
| `outputs.tf` | **007, 014** | Exponer solo **ARNs/IDs granulares** (PC-IAC-007). Utilizar **Splat Expressions** para la extracción limpia (PC-IAC-014). |

### B. Reglas de Diseño y Seguridad (PC-IAC-020, 023)

Para el recurso [NOMBRE_DEL_RECURSO_A_GENERAR]:
1. **Responsabilidad Única (PC-IAC-023):** El módulo solo debe crear recursos intrínsecos al servicio principal.
2. **Hardenizado (PC-IAC-020):** Aplicar el principio de Mínimo Privilegio y Cifrado en Reposo por defecto.

---

## FASE 3: REFERENCIA RÁPIDA DE REGLAS PC-IAC

Esta es una referencia rápida de las 26 reglas. El contenido completo ya fue leído en la FASE 1, PASO 1.

1.  PC-IAC-001: Estructura de Módulo
2.  PC-IAC-002: Variables
3.  PC-IAC-003: Nomenclatura Estándar
4.  PC-IAC-004: Etiquetas (Tagging)
5.  PC-IAC-005: Providers (Configuración y Alias)
6.  PC-IAC-006: Versiones y Estabilidad
7.  PC-IAC-007: Outputs (Salidas del Módulo)
8.  PC-IAC-008: Gestión de Estado (Backend)
9.  PC-IAC-009: Tipos de Datos, Conversiones y Lógica en Locals
10. PC-IAC-010: For_Each y Control de Recursos
11. PC-IAC-011: Data Sources y Consumo de Datos Externos
12. PC-IAC-012: Estructuras de Datos y Reutilización en Locals
13. PC-IAC-013: Estructura de Llamada a Módulos (Ordering)
14. PC-IAC-014: Bloques Dinámicos y Splat Expressions
15. PC-IAC-015: Consumo de Módulos (Remoto y Versionado)
16. PC-IAC-016: Manejo de Secretos y Datos Sensibles
17. PC-IAC-017: Comunicación entre Dominios (Data Sources)
18. PC-IAC-018: Testing y Validación del Código
19. PC-IAC-019: Uso Restringido de Remote State
20. PC-IAC-020: Gobernanza General de Seguridad (Hardenizado de Recursos)
21. PC-IAC-021: Centralización de Configuración en Locals (Root Cleanliness)
22. PC-IAC-022: Separación de Responsabilidades por Dominio (Root Domain Purity)
23. PC-IAC-023: Diseño Monolítico Funcional (Módulo Responsibility)
24. PC-IAC-024: Trazabilidad de la Configuración Compleja (Flujo de Datos)
25. PC-IAC-025: Procesamiento Obligatorio de Gobernanza en el Root (Naming en payload)
26. PC-IAC-026: Patrón de Transformación en Root (sample/)

---

## RESULTADO ESPERADO FINAL

El agente debe ejecutar las siguientes acciones en orden:

### 1. CREAR LA ESTRUCTURA FÍSICA DEL MÓDULO

Crear el directorio del módulo con el nombre `[NOMBRE_DEL_RECURSO]-module/` (ej., `dynamodb-module/`, `s3-module/`) y generar **todos los archivos obligatorios** según **PC-IAC-001**:

**Archivos del Módulo Raíz (Obligatorios):**
- `.gitignore`
- `CHANGELOG.md`
- `README.md`
- `data.tf`
- `locals.tf`
- `main.tf`
- `outputs.tf`
- `providers.tf`
- `variables.tf`
- `versions.tf`

**Directorio `sample/` (Obligatorio):**
- `sample/README.md`
- `sample/data.tf`
- `sample/main.tf`
- `sample/outputs.tf`
- `sample/providers.tf`
- `sample/terraform.tfvars`
- `sample/variables.tf`
- `sample/locals.tf`

**PROHIBIDO:**
- ❌ NO crear archivos adicionales de documentación (COMPLIANCE.md, RESUMEN-EJECUTIVO.md, etc.)
- ❌ NO crear archivos de ejemplos adicionales fuera de sample/

### 2. GENERAR CONTENIDO DE ARCHIVOS CORE

Los siguientes archivos deben contener la implementación completa del módulo:
- **`variables.tf`**: Variables de gobernanza + configuración del recurso usando `map(object)` (PC-IAC-002, 009)
- **`versions.tf`**: Requisitos de versión y alias `aws.project` (PC-IAC-005, 006)
- **`locals.tf`**: Construcción de nomenclatura dinámica (PC-IAC-003, 012)
- **`main.tf`**: Recursos con `for_each`, hardenizado de seguridad, y responsabilidad única (PC-IAC-010, 020, 023)
- **`outputs.tf`**: Outputs granulares con Splat Expressions (PC-IAC-007, 014)
- **`data.tf`**: Comentario indicando que Data Sources deben estar en el Root (PC-IAC-011)
- **`providers.tf`**: Comentario indicando que el provider se inyecta desde el Root (PC-IAC-005)

### 3. GENERAR ARCHIVOS DE DOCUMENTACIÓN

- **`.gitignore`**: Reglas estándar de Terraform
- **`CHANGELOG.md`**: Estructura básica con versión inicial
- **`README.md`**: Documentación completa del módulo con secciones:
  - Descripción del recurso
  - Uso y ejemplos
  - Tabla de Inputs (variables)
  - Tabla de Outputs
  - Requisitos y versiones
  - **Sección de Cumplimiento**: Tabla con las reglas PC-IAC más críticas aplicadas (máximo 10) y cómo se implementaron
  - **Sección de Decisiones de Diseño**: Justificación de configuraciones de seguridad, estructura de variables y consideraciones especiales
- **`sample/README.md`**: Instrucciones de ejecución del ejemplo

⚠️ **IMPORTANTE**: Toda la información de cumplimiento y diseño debe incluirse en el README.md existente. NO crear archivos adicionales como COMPLIANCE.md, RESUMEN-EJECUTIVO.md o EJEMPLOS-AVANZADOS.md.

### 4. GENERAR EJEMPLO FUNCIONAL EN `sample/` (PC-IAC-026)

El directorio `sample/` debe contener un ejemplo funcional completo que demuestre el uso del módulo siguiendo el **Patrón de Transformación de PC-IAC-026**:

**Flujo Obligatorio:** `terraform.tfvars → variables.tf → locals.tf → main.tf → module`

#### 4.1. Archivos y Responsabilidades

- **`sample/terraform.tfvars`**: 
  - Configuración declarativa sin IDs hardcodeados
  - Usar valores vacíos (`""`, `[]`) donde se necesiten IDs dinámicos
  - Ejemplo:
    ```hcl
    resource_config = {
      "example" = {
        vpc_id = ""  # Se llenará automáticamente desde data source
        subnet_ids = []  # Se llenarán automáticamente
      }
    }
    ```

- **`sample/data.tf`**: 
  - Data sources para obtener IDs dinámicos (VPC, Subnets, Security Groups, etc.)
  - Usar filtros por tags de nomenclatura estándar
  - Ejemplo:
    ```hcl
    data "aws_vpc" "selected" {
      filter {
        name   = "tag:Name"
        values = ["${var.client}-${var.project}-${var.environment}-vpc"]
      }
    }
    ```

- **`sample/locals.tf`**: 
  - Transformar `var.*` agregando IDs desde data sources
  - Usar `length()`, `merge()`, operador ternario para inyección dinámica
  - Construir nomenclatura completa (PC-IAC-025)
  - Ejemplo:
    ```hcl
    locals {
      governance_prefix = "${var.client}-${var.project}-${var.environment}"
      
      resource_config_transformed = {
        for key, config in var.resource_config : key => merge(config, {
          vpc_id = length(config.vpc_id) > 0 ? config.vpc_id : data.aws_vpc.selected.id
          name   = "${local.governance_prefix}-resource-${key}"
        })
      }
    }
    ```

- **`sample/main.tf`**: 
  - **SOLO** invocar módulo con `local.*` (nunca `var.*` directos)
  - **PROHIBIDO:** Contener bloques `locals {}`
  - Ejemplo:
    ```hcl
    module "resource" {
      source = "../"
      
      providers = {
        aws.project = aws.principal
      }
      
      client      = var.client
      project     = var.project
      environment = var.environment
      
      # ✅ Consumir local transformado (PC-IAC-026)
      resource_config = local.resource_config_transformed
    }
    ```

- **`sample/variables.tf`**: Variables de entrada con tipos explícitos
- **`sample/providers.tf`**: Configuración del provider con `default_tags`
- **`sample/outputs.tf`**: Outputs que muestren los resultados del módulo

#### 4.2. Antipatrones a Evitar

❌ **NUNCA hacer esto:**
```hcl
# ❌ sample/main.tf (INCORRECTO)
locals {
  config = { ... }  # Debe ir en sample/locals.tf
}

module "resource" {
  config = var.config  # Debe ser local.config_transformed
}
```

✅ **Siempre hacer esto:**
```hcl
# ✅ sample/locals.tf
locals {
  config_transformed = { ... }
}

# ✅ sample/main.tf
module "resource" {
  config = local.config_transformed
}
```

---

## INSTRUCCIONES FINALES CRÍTICAS

✅ **HACER:**
1. **VALIDAR MCPs PRIMERO** - Ejecutar PASO 3 antes de cualquier otra acción
2. Crear físicamente TODOS los archivos listados en PC-IAC-001 (18 archivos: 10 raíz + 8 sample/)
3. Asegurar que el módulo sea funcional y cumpla las 26 reglas PC-IAC
4. Generar un ejemplo en `sample/` que siga el patrón de PC-IAC-026 (terraform.tfvars → locals.tf → main.tf)
5. Incluir toda la documentación de cumplimiento y diseño en el README.md del módulo

❌ **NO HACER:**
1. **NO continuar sin validar los MCPs requeridos** (PASO 3)
2. **NO crear archivos adicionales** más allá de los 17 especificados en PC-IAC-001
3. **NO crear archivos como**: COMPLIANCE.md, RESUMEN-EJECUTIVO.md, EJEMPLOS-AVANZADOS.md, TESTING.md, o cualquier archivo no listado en PC-IAC-001
4. NO crear archivos sin consultar la documentación oficial
5. NO generar comandos `tree` o estadísticas de líneas de código
6. NO crear múltiples versiones o variantes del módulo
7. NO incluir secretos o datos sensibles en `terraform.tfvars`

**RESTRICCIÓN CRÍTICA DE ARCHIVOS:**
Solo crear los 18 archivos obligatorios definidos en PC-IAC-001:
- **Raíz (10)**: .gitignore, CHANGELOG.md, README.md, data.tf, locals.tf, main.tf, outputs.tf, providers.tf, variables.tf, versions.tf
- **sample/ (8)**: README.md, data.tf, locals.tf, main.tf, outputs.tf, providers.tf, terraform.tfvars, variables.tf

Toda información adicional (cumplimiento, ejemplos avanzados, decisiones de diseño) debe incluirse en el README.md existente.

**PATRÓN OBLIGATORIO PARA sample/ (PC-IAC-026):**
- ❌ NUNCA poner bloques `locals {}` en `sample/main.tf`
- ✅ SIEMPRE poner transformaciones en `sample/locals.tf`
- ✅ SIEMPRE usar `local.config_transformed` en bloques module (nunca `var.config` directo)
- ✅ SIEMPRE declarar configuración base sin IDs en `sample/terraform.tfvars`
- ✅ SIEMPRE inyectar IDs dinámicos desde data sources en `sample/locals.tf`

**VALIDACIÓN FINAL:** El módulo debe poder ser consumido inmediatamente por un Módulo Raíz (IaC Root) siguiendo el patrón de las reglas PC-IAC.
6. NO incluir secretos o datos sensibles en `terraform.tfvars`

**VALIDACIÓN FINAL:** El módulo debe poder ser consumido inmediatamente por un Módulo Raíz (IaC Root) siguiendo el patrón de las reglas PC-IAC.