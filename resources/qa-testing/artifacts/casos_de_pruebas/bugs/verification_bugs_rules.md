# 📜 RULES: AUDITORÍA DE CLASIFICACIÓN Y PRIORIZACIÓN DE DEFECTOS - PRAGMA S.A.

## ⚙️ 1. REGLAS DE ENTRADA Y FLUJO
* **R-FLU-01:** El Auditor debe verificar la existencia de table o archivo Excel. Si no existe, debe solicitarlo antes de emitir juicio.
* **R-FLU-02:** El Auditor debe cruzar defectos contra el "Stack Tecnológico" y "Contexto de Negocio" proporcionados originalmente.

---

## ✍️ 2. REGLAS EDITORIALES (R-EDI)
* **R-EDI-01:** El documento debe tener 0 errores ortográficos y gramaticales (incluyendo información del usuario).
* **R-EDI-02:** El tono debe ser técnico, evitando términos vagos como "probablemente" o "quizás".
* **R-EDI-03:** Los nombres de módulos y severidades deben ser estandarizados (Crítico, Mayor, Menor, Trivial).

---

## 🏗️ 3. REGLAS DE CONTENIDO Y ESTRUCTURA (R-CON/EST)
* **R-CON-01 (Escalas):** Severidad debe ser exactamente: Crítico, Mayor, Menor o Trivial.
* **R-CON-02 (Probabilidad):** Debe ser exactamente: Alta, Media o Baja.
* **R-CON-03 (Impacto Negocio):** Debe ser exactamente: Alto, Medio o Bajo.
* **R-CON-04 (Prioridad):** Debe ser numérica (1-5, siendo 1 crítica).
* **R-CON-05 (Acciones Recomendadas):** Deben ser ejecutables (Fix inmediato, Planificar sprint, Documentar limitación, etc.).
* **R-EST-01 (Tabulación):** Información organizada en 8 columnas exactas: ID, Descripción, Módulo, Severidad, Probabilidad, Impacto, Prioridad, Acción.
* **R-CON-06 (Coerencia):** Validar que Severidad × Impacto sea congruente con Prioridad calculada.

---

## ⚖️ 4. CRITERIOS DE EVALUACIÓN
* **APROBADO:** Cumple el 100% de las reglas.
* **APROBADO CON OBSERVACIONES:** Fallos menores de forma o acciones poco detalladas.
* **NO APROBADO:** Escalas inválidas, inconsistencias Severidad/Prioridad, falta alineación con stack tecnológico.

---
