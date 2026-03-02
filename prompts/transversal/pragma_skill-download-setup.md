# Prompt: Descarga y Configuración de Skills desde Repositorio

**Objetivo Principal:**
Descargar una skill específica desde un repositorio remoto, almacenarla en una ruta local, validar si ya existe (para actualizar, no duplicar).

**Parámetros Configurables (Variables de Usuario):**
- `REPOSITORY_URL`: URL del repositorio remoto (ej: https://github.com/anthropics/skills/)
- `SKILL_FOLDER_PATH`: Ruta de la carpeta dentro del repositorio (ej: skills/skill-creator)
- `LOCAL_STORAGE_PATH`: Ruta local del computador donde almacenar (ej: ~/.agent/skills/)

---

**Instrucciones:**

### **Fase 1: Cuestionamiento y Claridad**
- **PIENSA detenidamente, paso a paso**
- Antes de proceder, valida estos parámetros:
  - ¿El `REPOSITORY_URL` es correcto y accesible?
  - ¿El `SKILL_FOLDER_PATH` existe dentro del repositorio?
  - ¿El `LOCAL_STORAGE_PATH` está bien escrito? (ej: expandir `~` si aplica)
  - ¿El repositorio requiere autenticación o token?
- **Si tienes alguna duda, PREGUNTA** - No asumas ni inventes valores

### **Fase 2: Validación de Prerequisitos**
1. Verifica si la ruta local `${LOCAL_STORAGE_PATH}` existe en el sistema.
   - Si NO existe: créala con permisos de lectura-escritura.
   - Si ya existe: continúa.

2. Determina si la carpeta `${SKILL_FOLDER_PATH}` **ya existe** dentro de `${LOCAL_STORAGE_PATH}`.
   - Si existe → si es posible pregunta si se debe proceder con **ACTUALIZACIÓN** (reemplazar contenido, mantener estructura).
   - Si NO existe → procedera con **CREACIÓN NUEVA**.

### **Fase 3: Descarga desde Repositorio**
1. Accede al repositorio remoto usando `${REPOSITORY_URL}`.
2. Descarga **solo** la carpeta especificada en `${SKILL_FOLDER_PATH}`.
3. Almacena el contenido en `${LOCAL_STORAGE_PATH}`.
4. **Validación post-descarga:**
   - Verifica que los archivos se hayan descargado completamente.
   - Confirma la cantidad de archivos descargados.
   - Si hay errores, reporta específicamente qué falló.

### **Fase 4: Validación Post-Descarga**
1. Verifica que la carpeta `${SKILL_FOLDER_PATH}` se encuentre en `${LOCAL_STORAGE_PATH}`.
2. Confirma que todos los archivos se hayan transferido correctamente.
3. Valida la estructura de directorios y que contenga los archivos esperados.

### **Fase 5: Reporte Final y Validación**
- **Estado de Descarga:** Exitosa / Con advertencias / Fallida (detalla si aplica)
- **Estado de Carpeta Local:** Creada nueva / Actualizada
- **Resumen de Archivos:** Número de archivos descargados y ubicación
- **Próximos Pasos:** Listar acciones recomendadas para el usuario

**Recomendación Opcional - Configuración de VS Code:**

Aunque la skill está descargada y disponible, es recomendable configurar VS Code para optimizar la detección automática:

1. Abre el archivo `settings.json` de VS Code:
   - Ubicación macOS: `~/Library/Application Support/Code/User/settings.json`
   - Ubicación Windows: `%APPDATA%\Code\User\settings.json`

2. Busca o crea la clave `"chat.agentSkillsLocations"` con el siguiente formato:
   ```json
   "chat.agentSkillsLocations": {
     "${LOCAL_STORAGE_PATH}": true
   }
   ```

3. Si la configuración ya existe y contiene la referencia a `${LOCAL_STORAGE_PATH}`, no es necesario hacer cambios.

4. Reinicia VS Code para que la skill sea detectada completamente.

---

**Principios Aplicados:**
- Genérico para cualquier gestor de repositorios
- Variables claramente definidas para reutilización
- Cuestionamiento activo integrado (no asume)
- Validaciones en cada fase
- Respuesta flexible según capacidades del agente
- Reporte detallado al final
