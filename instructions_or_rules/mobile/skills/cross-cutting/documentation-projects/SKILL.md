---
name: documentation-projects
description: Create, structure, audit, and complete project documentation using a proven 7-document framework (index, overview, requirements, project-structure, tech-stack, features, implementation, user-flow). Use this skill ALWAYS when the user wants to document a new or existing project, write a README or onboarding guide, draft technical specs or architecture docs, audit docs for gaps or TBDs, write requirements or feature specs, generate ADRs (Architecture Decision Records), create handoff or runbook docs, or describe project structure to new team members. Also activate for phrases like "necesito documentar mi proyecto", "help me write the docs", "crea una wiki para mi proyecto", "arma la documentación técnica", "que debería incluir nuestra documentación", or "tengo documentación incompleta". Do NOT skip this skill when the user has partial docs that need completion — it handles both new and existing incomplete documentation.
---

# Skill: Project Documentation Structure

## Cuando Usar Este Skill

- Crear documentación completa para un proyecto nuevo
- Completar o mejorar documentación existente (parcial, con TBDs, desactualizada)
- Convertir documentación con datos reales en templates genéricos reutilizables
- Auditar calidad y completitud de documentación existente
- Estandarizar documentación entre proyectos del equipo

---

## 7 Documentos Base

```
docs/
├── index.md                  Guía de navegación y punto de entrada
├── project-overview.md       Visión, objetivos, problemas resueltos
├── requirements.md           Requisitos funcionales, técnicos y de calidad
├── project-structure.md      Arquitectura y organización de código
├── tech-stack.md             Tecnologías con justificaciones
├── features.md               Especificación de funcionalidades
├── implementation.md         Guía de desarrollo y estándares
└── user-flow.md              Flujos de usuario y de datos
```

---

## Scripts de Análisis Disponibles

Cuando el usuario proporcione una carpeta `docs/` existente, usa estos scripts antes de proponer cambios:

```bash
# PASO 2 — Auditoría automática: genera la matriz de estado de cada documento
python3 scripts/analyze_docs.py path/to/docs/

# PASO 2 — Análisis de completitud: identifica TBDs, secciones vacías, % de cobertura
python3 scripts/analyze_completeness.py path/to/docs/

# PASO 5 — Validación final: verifica que los 7 documentos cumplen la estructura
python3 scripts/validate_structure.py path/to/docs/
```

Los scripts detectan automáticamente: documentos faltantes, secciones vacías, TBDs no resueltos,
y datos sensibles (URLs, emails, IPs, tokens, rutas absolutas).

---

## Flujo de Ejecución (5 Pasos)

### PASO 1: Validar Contexto

¿Tenemos claridad sobre dominio, tipo y audiencia del proyecto?

**Si NO:** Formula estas preguntas antes de continuar:
- ¿Cuál es el dominio? (Backend, Frontend, Mobile, Infra, QA, Integración)
- ¿Es proyecto nuevo o documentación existente a mejorar?
- ¿Qué audiencia? (Desarrolladores, arquitectos, DevOps, QA)
- ¿Hay restricciones de confidencialidad?

**Si SÍ:** Continúa a PASO 2.

---

### PASO 2: Auditar Documentación Existente

Si hay una carpeta `docs/` existente, ejecuta primero los scripts de análisis.
Si no hay docs previos, clasifica todos como `CREAR`.

Completa esta matriz para cada documento:

```
Documento            │ Existe │ Contenido          │ Genérico │ Acción
─────────────────────┼────────┼────────────────────┼──────────┼────────────
index.md             │  ?     │ Completo/Parcial/   │ Genérico/│ CREAR /
project-overview.md  │        │ Vacío              │ Específico│ COMPLETAR /
requirements.md      │        │                    │          │ GENERALIZAR /
project-structure.md │        │                    │          │ LISTO
tech-stack.md        │        │                    │          │
features.md          │        │                    │          │
implementation.md    │        │                    │          │
user-flow.md         │        │                    │          │
```

**VALIDACIÓN CRÍTICA:** Si el documento ya existe y está incompleto:
- NO alteres la estructura existente
- Complementa el contenido faltante respetando formato actual
- Valida que cambios sean coherentes con decisiones arquitectónicas previas

---

### PASO 3: Entrevistar al Usuario (Solo para Documentos Faltantes)

Para cada documento con acción `CREAR` o `COMPLETAR`, carga el archivo de cuestionarios:

> Lee `references/questionnaires.md` — contiene cuestionarios específicos y plantillas
> detalladas para cada uno de los 7 documentos.

Adapta las preguntas al dominio detectado. No hagas preguntas que ya respondió el contexto.

---

### PASO 4: Generar Documentos

Para cada documento a generar, presenta el contenido así:

```
--- DOCUMENTO ---
Nombre: [nombre-del-archivo.md]
Propósito: [una línea]
Acción: [CREAR / COMPLETAR / GENERALIZAR]

[Contenido del documento]

Validación:
  [OK] Sin credenciales, tokens, rutas absolutas, emails reales
  [OK] Contenido comprensible sin contexto externo
  [OK] Referencias a otros documentos correctas
--- /DOCUMENTO ---
```

---

### PASO 5: Validar y Reportar

Ejecuta `validate_structure.py` sobre la carpeta docs/ generada.

Checklist final antes de entregar:

```
DOCUMENTOS:
  [_] 7 documentos presentes o ausencia justificada
  [_] Ningún TBD sin documentar por qué falta
  [_] Links entre documentos correctos

CONTENIDO:
  [_] Sin datos sensibles (tokens, rutas, emails reales)
  [_] Metadata: fecha, versión, autor en cada doc
  [_] Entendible sin contexto externo
```

---

## Patrones por Dominio

Adapta el enfoque según el dominio detectado. Para plantillas detalladas por dominio,
carga `references/domain-templates.md`.

| Dominio | Énfasis Principal | Stack Típico |
|---------|------------------|--------------|
| **Backend** | Capas (Controller→Service→Repository), REST APIs, DB | Java/Python/Go + Spring/FastAPI + SQL/NoSQL |
| **Frontend** | Componentes, state management, flujos UI, responsive | React/Vue/Angular + Redux/Zustand + Vite |
| **Mobile** | Plataformas (iOS/Android), lifecycle, integración APIs | Flutter/React Native + BLoC/Riverpod |
| **QA/Testing** | Frameworks de testing, cobertura, tipos de test, CI | JUnit/Pytest/Jest/Cypress + Allure/Playwright |
| **Infra/CloudOps** | IaC, containers, monitoring, seguridad, compliance | Terraform + Docker/K8s + Grafana + AWS/GCP/Azure |

Para cada dominio, carga `references/domain-templates.md` y usa la plantilla adecuada
antes de generar los documentos.

---

## Principios del Skill

| Principio | Significado |
|-----------|-------------|
| No Asumir | Pregunta cuando hay ambigüedad en dominio o requisitos |
| Agnóstico | Aplica a backend, frontend, mobile, infra, QA, etc. |
| Preservar | No rompas estructura de docs que ya existen |
| Lean | Genera solo los documentos necesarios, sin overhead |
| Verificable | Cada entrega pasa validación de genericidad y estructura |

---

## Indicadores de Éxito

**El resultado ES exitoso cuando:**
- Los 7 documentos tienen estructura clara y contenido relevante
- Ningún documento tiene TBDs sin justificar
- Los documentos son reutilizables como templates en proyectos similares
- `validate_structure.py` reporta ≥ 6/7 documentos válidos

**El resultado NO es exitoso cuando:**
- Contiene credenciales, tokens, rutas absolutas o emails reales
- Hay TBDs sin documentar por qué faltan
- Falta alguno de los 7 documentos sin justificación explícita

