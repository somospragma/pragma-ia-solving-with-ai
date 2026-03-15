# Prompt: Descarga de Skill (estricto y simple)

## Objetivo
Descargar una carpeta de skill desde un repositorio y dejarla en una ruta local, sin duplicados ni temporales.

## Parámetros
- `REPOSITORY_URL` (obligatorio ej: https://github.com/anthropics/skills/tree/main/skills)
- `SKILL_FOLDER_PATH` (obligatorio ej: skills/skill-creator)
- `LOCAL_STORAGE_PATH` (obligatorio ej: ~/.agent/skills)
- `BRANCH_NAME` (default: `main`)

## Reglas de ejecución
- Ejecutar en `zsh` interactivo con comandos simples, cortos y evitando inconsistencias.
- Si falta un parámetro obligatorio: pregunta los valores.
- Normalizar `LOCAL_STORAGE_PATH`: expandir `~` y remover `/` final.
- Limpiar temporales siempre con `trap`.
- Ejecutar comandos simples, y no devolver scripts largos.
- Si `TARGET_DIR` existe, preguntar exactamente: **"¿Deseas eliminar la ruta existente y continuar?"**
   - Si responde no: `STATUS=SKIPPED`, `ERROR_CODE=E_CONFIRM`, `LOCAL_STATE=SIN_CAMBIOS`.
- No inventar resultados. Si hay duda o ambigüedad, preguntar antes de continuar.
- Si una validación no puede completarse, reportar la limitación en la salida final.

## Flujo mínimo
1. Validar `git`.
2. Resolver `TARGET_DIR=${LOCAL_STORAGE_PATH}/$(basename ${SKILL_FOLDER_PATH})`.
3. Si `TARGET_DIR` existe: pedir confirmación para eliminar.
4. Validar rama con match exacto: `git ls-remote --heads` contra `refs/heads/$BRANCH_NAME`.
5. Clonar optimizado: `--single-branch --filter=blob:none --sparse --no-checkout`.
6. Configurar `sparse-checkout` solo para `SKILL_FOLDER_PATH`.
7. Validar que la carpeta exista en el clon.
8. Si confirma: eliminar y continuar. Si no: terminar como `SKIPPED`.
9. Copiar con `cp -R` y validar conteo origen vs destino.
10. Reportar salida estándar.

## Salida estándar (obligatoria)
- `STATUS=SUCCESS|SKIPPED|FAILED`
- `ERROR_CODE=NONE|E_PARAMS|E_BRANCH|E_PATH|E_PERMS|E_COUNT|E_RUNTIME|E_CONFIRM`
- `LOCAL_STATE=CREADA_NUEVA|ACTUALIZADA|SIN_CAMBIOS`
- `TARGET_DIR=...`
- `FILES=...`

## Códigos de error
- `E_PARAMS`: parámetros inválidos o vacíos
- `E_BRANCH`: rama inexistente o inaccesible
- `E_PATH`: carpeta de skill no encontrada en repo
- `E_PERMS`: error de permisos en destino
- `E_COUNT`: conteo origen/destino no coincide
- `E_CONFIRM`: usuario no autorizó eliminar ruta existente
- `E_RUNTIME`: error no clasificado

## Configuración VS Code (opcional)
Recomienda que se incluya en la configuración del ide `chat.agentSkillsLocations` con `${LOCAL_STORAGE_PATH}`.
