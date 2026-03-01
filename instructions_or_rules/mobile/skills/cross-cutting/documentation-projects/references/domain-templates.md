# Documentation Templates by Domain

Reference templates showing expected structure for each project domain.
When used in real projects, fill with actual project data, not placeholders.

---

## Índice de Plantillas

1. [Backend (Microservicios)](#backend-microservicios)
2. [Frontend (SPA/PWA)](#frontend-spapwa)
3. [Mobile (Flutter/React Native)](#mobile-flutterreact-native)
4. [QA / Testing Automation](#qa--testing-automation)
5. [Infraestructura (DevOps/CloudOps)](#infraestructura-devopscloudops)

---

## Backend (Microservicios)

### 1. project-overview.md (Plantilla Backend)

```markdown
# [SERVICE_NAME] - Visión General

## Visión del Proyecto
Servicio [CAPABILITIES] que proporciona [BUSINESS_VALUE]. Diseñado para:
- Escalar horizontalmente
- Integrarse con otros microservicios
- Mantener alta disponibilidad

## Objetivos Principales
1. **Confiabilidad:** 99.9% uptime mínimo
2. **Performance:** Latencia p99 < [LATENCY_ms]ms
3. **Escalabilidad:** Soportar [SCALE] rps
4. **Mantenibilidad:** Código modular y testeable
5. **Seguridad:** Cumplir estándares [SECURITY_STANDARD]

## Problemas Resueltos
- **Latencia en requests:** Mediante caching y optimización
- **Acoplamiento:** Arquitectura desacoplada con eventos
- **Escalabilidad manual:** Auto-scaling horizontal

## Stack Arquitectónico
- Patrón: Microservicios con Domain-Driven Design
- Comunicación: [SYNC/ASYNC] via [PROTOCOL]
- Persistencia: [DATABASE_TYPE]

## Principios SOLID
- S: Cada servicio tiene una responsabilidad
- O: Extensible sin cambiar código existente
- L: Implementaciones son intercambiables
- I: Interfaces específicas por cliente
- D: Depende de abstracciones, no implementaciones
```

### 2. requirements.md (Plantilla Backend)

```markdown
# [SERVICE_NAME] - Requirements

## Requisitos Funcionales

### RF-001: [Core Functionality]
**Descripción:** El servicio debe [CAPABILITY] cuando [CONDITION]

**Criterios de Aceptación:**
- ✅ Procesa [OPERATION] en < [TIME]ms
- ✅ Retorna [RESPONSE_FORMAT]
- ✅ Valida [VALIDATION_RULES]

**Prioridad:** CRÍTICA

### RF-002: [Secondary Functionality]
[Repetir patrón]

## Requisitos Técnicos

### RT-001: Performance
**Description:** P99 latency < [LATENCY]ms under [LOAD]

### RT-002: Escalabilidad
**Description:** Soportar [SCALE] requests/segundo

### RT-003: Disponibilidad
**Description:** 99.9% uptime SLA

## Requisitos de Calidad
- Unit Test Coverage: [TARGET]%
- Integration Test Coverage: [TARGET]%
- Code Review requerido antes de merge
- Linting y formatting automático

## Requisitos de Ambiente

| Ambiente | Características |
|----------|-----------------|
| **DEV** | Local, base de datos en memoria |
| **QA** | Integración con otros servicios QA |
| **STAGING** | Mirror de PROD con datos test |
| **PROD** | Multi-región, alta disponibilidad |
```

### 3. tech-stack.md (Plantilla Backend)

```markdown
# [SERVICE_NAME] - Tech Stack

## Lenguaje Principal

**[LANGUAGE]** v[VERSION]

**Justificación:**
- Rendimiento: [PERFORMANCE_BENEFIT]
- Ecosistema: [ECOSYSTEM_BENEFIT]
- Comunidad: [COMMUNITY_SIZE]

**Alternativas Consideradas:**
- [ALTERNATIVE_1]: Rechazada porque [REASON]
- [ALTERNATIVE_2]: Rechazada porque [REASON]

## Frameworks Clave

### [WEB_FRAMEWORK]
- **Propósito:** Request handling, routing, middleware
- **Versión:** [VERSION]
- **Justificación:** Rendimiento + features nativos
- **Alternativas:** [FRAMEWORKS_DESCARTADOS]

### [ORM_FRAMEWORK]
- **Propósito:** Abstracción de base de datos
- **Versión:** [VERSION]
- **Justificación:** Queries type-safe, migrations
- **Alternativas:** [ALTERNATIVES]

### [TESTING_FRAMEWORK]
- **Propósito:** Pruebas unitarias e integración
- **Versión:** [VERSION]

## Herramientas de Desarrollo

| Herramienta | Propósito | Versión |
|-------------|-----------|---------|
| [BUILD_TOOL] | Compilación y empaquetado | [VERSION] |
| [PACKAGE_MANAGER] | Gestión de dependencias | [VERSION] |
| [LINTER] | Code quality | [VERSION] |
| [FORMATTER] | Code style | [VERSION] |

## Base de Datos

**Tipo:** [DATABASE_TYPE] / [DATABASE_NAME]

**Justificación:**
- Escalabilidad: [REASON]
- Queries: [REASON]
- Comparación con alternativas: [ALTERNATIVES]

## Infraestructura

- **Container:** [CONTAINER_TECH]
- **Orquestación:** [ORCHESTRATION_TOOL]
- **Logging:** [LOGGING_TOOL]
- **Monitoring:** [MONITORING_TOOL]
- **Alerting:** [ALERTING_TOOL]
```

---

## Frontend (SPA/PWA)

### project-overview.md (Plantilla Frontend)

```markdown
# [APP_NAME] - Visión General

## Visión
Aplicación [DESCRIPTION] que proporciona experiencia [USER_EXPERIENCE] mediante:
- Interfaz responsiva
- Performance optimizado
- Accesibilidad estándar

## Objetivos Principales
1. **Experiencia de Usuario:** [METRIC] score
2. **Performance:** Core Web Vitals: LCP < [MS]ms
3. **Accesibilidad:** WCAG 2.1 AA compliant
4. **Offline:** Funcionalidad offline con PWA
5. **SEO:** Indexable y optimizado para motores de búsqueda

## Principios de Diseño
- Mobile-first responsive design
- Component reusability
- State management centralizado
- Testing en todas las capas (unit, integration, E2E)
```

---

## Mobile (Flutter/React Native)

### project-overview.md (Plantilla Mobile)

```markdown
# [APP_NAME] - Visión General

## Visión
Aplicación móvil [DESCRIPTION] disponible en [PLATFORMS] que:
- Sincroniza datos sin conexión
- Proporciona experiencia nativa
- Integra con backend

## Objetivos Principales
1. **Disponibilidad:** iOS [VERSION]+ y Android [VERSION]+
2. **Performance:** Startup < [MS]ms
3. **Offline:** Funcionalidad básica sin conexión
4. **Seguridad:** Encriptación de datos local
5. **Integración:** APIs backend consistentes

## Arquitectura
- Patrón: MVVM / MVP con State Management
- Persistencia: Local database + sync
- APIs: REST / GraphQL
```

---

## QA / Testing Automation

### project-overview.md (Plantilla QA)

```markdown
# [AUTOMATION_PROJECT] - Visión General

## Visión
Framework de automatización para [APPLICATION] cubriendo [TEST_TYPES]:
- Pruebas funcionales
- Pruebas de regresión
- Pruebas de integración
- Pruebas de performance

## Objetivos Principales
1. **Cobertura:** [COVERAGE]% de funcionalidades críticas
2. **Velocidad:** Suite completa < [TIME]min
3. **Mantenibilidad:** Tests agnósticos a cambios de UI
4. **Reporte:** Dashboard de resultados en tiempo real
5. **CI/CD:** Ejecución automática en cada commit

## Estrategia de Testing
- Pirámide: Unit (Muchos) → Integration (Algunos) → E2E (Pocos)
- Herramientas: [TOOLS]
- Reportes: [REPORTING_TOOL]
```

---

## Infraestructura (DevOps/CloudOps)

### project-overview.md (Plantilla Infraestructura)

```markdown
# [INFRASTRUCTURE_PROJECT] - Visión General

## Visión
Infraestructura como código para [APPLICATION] que proporciona:
- Ambiente consistente (DEV/QA/PROD)
- Escalabilidad automática
- Alta disponibilidad
- Seguridad y compliance

## Objetivos Principales
1. **Reproducibilidad:** Ambientes idénticos
2. **Escalabilidad:** Auto-scaling horizontal y vertical
3. **Disponibilidad:** 99.99% uptime SLA
4. **Seguridad:** Encriptación, VPC aislada, security groups
5. **Cost Optimization:** Utilización eficiente de recursos

## Cloud Provider
- **Proveedor:** [CLOUD_PROVIDER]
- **Regiones:** [REGIONS]
- **SLA:** [SLA]
```

---

## ¿Cómo Usar Estas Plantillas?

1. **Selecciona tu dominio** en el índice arriba
2. **Copia la plantilla** del documento que necesitas
3. **Reemplaza `[PLACEHOLDER]`** con datos de tu proyecto
4. **Generaliza:** Cambia datos específicos a genéricos si es necesario
5. **Valida:** Verifica que no haya URLs, nombres o datos sensibles
