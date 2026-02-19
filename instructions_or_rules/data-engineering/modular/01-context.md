```markdown
# Contexto General

## 1.1. Project Context

- Objetivo: Entregar pipelines confiables y observables que alimenten usuarios analíticos y ML.
- Alcance típico: Ingesta (CDC/APIs/files), procesamiento (stream/batch), almacenamiento (raw/curated/serving), entrega (tables/APIs).

## 1.2. Stakeholders

- Product Owner, Data Owner, Data Platform, Equipo de Feature, SRE, Security, QA.

## 1.3. Success Checklist

- Template inicializado y DoR aprobado
- Contratos de datos definidos y versionados
- Pruebas y gates implementados en CI

## 1.4. Emergency Protocol

- Failing critical pipeline? Escalar a on-call y activar Runbook de falta de datos.
- Backfill en progreso? Notificar consumidores y cerrar ventanas de ingest.

```
