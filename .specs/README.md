# Specs — Pragma IA

Directorio para especificaciones de nuevas funcionalidades siguiendo el flujo Spec-Driven Development.

## Uso

Para cada nueva feature, crear una carpeta con 3 archivos secuenciales:

```
.specs/{feature_name}/
├── requirements.md   ← Requerimientos funcionales (⏸️ aprobación humana)
├── design.md         ← Arquitectura y decisiones técnicas (⏸️ aprobación humana)
└── tasks.md          ← Micro-tareas con checkboxes (ejecución)
```

## Flujo

1. Completar `requirements.md` → **esperar aprobación**
2. Completar `design.md` → **esperar aprobación**
3. Ejecutar `tasks.md`

## Template

Ver [_template/](./_template/) para archivos base.
