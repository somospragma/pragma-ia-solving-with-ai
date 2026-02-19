```markdown
# Checklist: Arquitectura Híbrida (On‑prem ↔ Cloud)

Use este checklist para validar aspectos críticos de una arquitectura híbrida de datos.

## Conectividad y Red
- Definir enlaces (Direct Connect / ExpressRoute) o VPN; documentar latencia, ancho de banda y SLAs.
- Plan de redundancia multi‑AZ / multi‑path si aplica.
- Revisar MTU, encriptación y puertos necesarios para conectores.

## Transfer Patterns y Gateways
- Seleccionar patrón: push (agents) vs pull (polling) vs streaming bridge.
- Validar uso de herramientas: AWS DataSync, Storage Gateway, Azure Data Box/ Data Factory, Kafka Mirror/Connect.
- Documentar retención temporal en edge / buffer y límites de backlog.

## Consistencia y Reprocessing
- Definir checkpoints, offsets persistentes y estrategia de reconciliación.
- Procedimiento de backfill controlado con snapshots y validaciones.

## Seguridad y Cumplimiento
- Políticas de residencia y clasificación de datos por jurisdicción.
- Cifrado in transit / at rest; rotación de claves y gestión de certificados.
- Control de accesos por red (security groups, NSGs) y roles mínimos.

## Observabilidad y Telemetría
- Centralizar logs y métricas (exporters/log shippers) para correlación end‑to‑end.
- Métricas de red: latency, packet loss, throughput; métricas de transfer: files/sec, bytes/sec.

## Operación y Runbooks Híbridos
- Runbook: network outage (re-routing, buffer draining, retry windows).
- Runbook: partial sync (reconcile differences, promote safe window).
- Runbook: split‑brain recovery and manual reconciliation.

## Performance & Cost
- Pruebas de ancho de banda y saturación antes de producción.
- Estimar costes de egress y enlaces dedicados; programar transfer windows para optimizar coste.

## IaC y Provisioning Híbrido
- IaC para recursos cloud y documentación de pasos manuales on‑prem (scripts de provisioning, agentes).
- Secret management y acceso temporizado para agentes on‑prem.

## Acceptance criteria
- Enlace de red desplegado y validado con pruebas de throughput/latency.
- Transferencia de muestra completa y validada contra checks de integridad.
- Runbooks revisados y propietarios asignados.
- Observability pipeline demostrado (logs + métricas centralizadas).

```
