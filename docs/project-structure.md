# Pragma IA - Estructura del Proyecto

## Patrón Arquitectónico

El proyecto usa una **Arquitectura Modular por Dominio** que proporciona:
- Separación clara de responsabilidades por área técnica (Backend, Frontend, Mobile, etc.)
- Modularidad: cada dominio es independiente pero interconectado
- Facilidad para navegación y descubrimiento de artefactos
- Escalabilidad: nuevos dominios pueden agregarse sin alterar existentes

## Estructura Visual

```
pragma-ia-solving-with-ai/
├── docs/
│   ├── index.md                           [Página inicial de documentación]
│   ├── project-overview.md                [Visión y objetivos]
│   ├── requirements.md                    [Requisitos]
│   ├── project-structure.md               [Este archivo]
│   ├── tech-stack.md                      [Tecnologías]
│   ├── features.md                        [Características]
│   ├── implementation.md                  [Guía de desarrollo]
│   └── user-flow.md                       [Flujos de usuario]
│
├── instructions_or_rules/
│   ├── _estandar-instructions/            [Plantillas base]
│   ├── backend/                           [Instrucciones Backend]
│   ├── frontend/                          [Instrucciones Frontend]
│   ├── mobile/                            [Instrucciones Mobile]
│   └── ...
│
├── prompts/
│   ├── arquitectura/                      [Prompts de arquitectura]
│   ├── backend/                           [Prompts backend]
│   ├── cloudops/                          [Prompts CloudOps]
│   ├── devsecops/                         [Prompts DevSecOps]
│   ├── frontend/                          [Prompts frontend]
│   ├── integracion/                       [Prompts integración]
│   ├── mobile/                            [Prompts mobile]
│   ├── qa-testing/                        [Prompts QA]
│   ├── transversal/                       [Prompts transversales]
│   └── ...
│
├── resources/
│   ├── arquitectura/                      [Recursos de arquitectura]
│   ├── backend/                           [Recursos backend]
│   ├── cloudops/                          [Recursos CloudOps]
│   ├── devsecops/                         [Recursos DevSecOps]
│   ├── frontend/                          [Recursos frontend]
│   ├── integracion/                       [Recursos integración]
│   ├── mobile/                            [Recursos mobile]
│   ├── qa-testing/                        [Recursos QA]
│   └── ...
│
├── chatmodes/
│   ├── example.chatmode.md                [Ejemplo de chatmode]
│   └── ...
│
├── skills/
│   └── [Colección de skills reutilizables]
│
├── README.md                              [Descripción del proyecto]
├── CONTRIBUTING.md                        [Guía de contribución]
├── CHANGELOG.md                           [Historial de cambios]
└── index.md                               [Guía de documentación]
```

---

## Principios de Organización

### Modularidad
Cada dominio es independiente. Los artefactos en un dominio no deben depender de otros dominios.

### Claridad Predecible
La estructura es consistente: `[tipo_artefacto]/[dominio]/[sub-categoría]/[nombre].md`

### Escalabilidad
Nuevos dominios se pueden agregar sin afectar lo existente.

### Reutilización
Los estándares en `_estandar-instructions/` y recursos en `transversal/` evitan duplicación.

---

## Módulos Principales

### 1. Instructions (`instructions_or_rules/`)
Instrucciones personalizadas que definen CÓMO realizar tareas.

### 2. Prompts (`prompts/`)
Prompts reutilizables que definen QUÉ se debe hacer.

### 3. Resources (`resources/`)
Recursos reutilizables invocables vía MCP (plantillas, ejemplos, guías).

### 4. Chatmodes (`chatmodes/`)
Comportamientos personalizados de GitHub Copilot.

### 5. Skills (`skills/`)
Procesos complejos encapsulados como skills reutilizables.

---

## Flujo de Datos

```
Usuario selecciona instrucción
    ↓
Aplica prompt específico
    ↓
Usa resources si es necesario
    ↓
Chatmode define límites
    ↓
IA genera respuesta
```
