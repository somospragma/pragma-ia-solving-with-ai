# Mobile Skills README

Este directorio organiza los agent skills para desarrollo mobile en Pragma. Discriminados por tecnología y por temas transversales (cross-cutting). Cada skill sigue la especificación de [Agent Skills](https://agentskills.io/home) y sus recomendaciones sobre el header.

## Estructura de carpetas

- android/ - Skills específicos para Android nativo
- ios/ - Skills específicos para iOS nativo
- flutter/ - Skills para Flutter
- react-native/ - Skills para React Native
- ionic/ - Skills para Ionic
- cross-cutting/ - Skills transversales y agnósticos (aplican a varias tecnologías)

Ejemplo de estructura:

```
mobile/skills/
  android/
  ios/
  flutter/
    flutter-testing/
      SKILL.md
      references/
        unit-testing.md
        widget-testing.md
        integration-testing.md
  react-native/
  ionic/
  cross-cutting/
    commit-conventions/
      SKILL.md
    changelog-management/
      SKILL.md
```

## Criterio de organización

1. **Por tecnología**: si el skill depende de herramientas, frameworks o APIs específicas (Flutter, Android, iOS, etc.), va en la carpeta de esa tecnología.

2. **Cross-cutting**: si el skill es agnóstico y aplica a varias tecnologías (ej. convenciones de commits, gestión de changelog, procesos de calidad), va en cross-cutting.

## Estructura mínima de un skill

Basado en https://agentskills.io/specification, un skill es una carpeta con mínimo un `SKILL.md`.

```
<skill-name>/
  SKILL.md
  references/   # opcional
  scripts/      # opcional
  assets/       # opcional
```

## Formato requerido de SKILL.md

Cada `SKILL.md` debe tener frontmatter YAML y contenido Markdown. Debe respetar la especificación y mantener el header custom actual de Pragma.

### Frontmatter (requerido)

- `name`: 1-64 caracteres, minúsculas y guiones (`a-z` y `-`), debe coincidir con el nombre de la carpeta.
- `description`: 1-1024 caracteres, describe qué hace el skill y cuándo usarlo.

### Frontmatter (opcional pero permitido por spec)

- `license`: licencia aplicable
- `compatibility`: requisitos de entorno
- `allowed-tools`: lista de herramientas preaprobadas

### Header custom actual (obligatorio en este repo)

Este repo ya usa el siguiente header y se debe conservar:

```yaml
---
name: <skill-name>
description: <descripción clara y cuándo usar>
metadata:
  author: Pragma Mobile Chapter
  version: "1.0"
---
```

### Body (contenido)

- Instrucciones claras y accionables
- Ejemplos de entrada/salida
- Casos edge relevantes
- Referencias a archivos dentro de la carpeta usando rutas relativas

## Buenas prácticas de contenido

- Mantener el `SKILL.md` debajo de 500 líneas cuando sea posible
- Mover detalles extensos a `references/`
- Evitar cadenas profundas de referencias
- Escribir pensando en uso por humanos y agentes

## Referencias opcionales

- `references/`: documentación extendida (índices, guías, ejemplos)
- `scripts/`: scripts ejecutables de apoyo
- `assets/`: plantillas, diagramas, datos

## Validación

Puedes validar un skill con la herramienta de referencia:
https://github.com/agentskills/agentskills/tree/main/skills-ref

```
skills-ref validate ./<skill-name>
```

## Resumen rápido

- Tecnología específica -> carpeta de esa tecnología
- Agnóstico -> cross-cutting
- Cada skill debe tener `SKILL.md` con frontmatter correcto
- Conservar el header custom con `metadata.author` y `metadata.version`
