# 📋 REGLAS DE CREACION: MATRIZ DE RIESGOS QA - PRAGMA S.A.

Este conjunto de reglas define los criterios de aceptación para la creación y auditoría de matrices de riesgos de aseguramiento de calidad.

---

## ✍️ 1. REGLAS DE CALIDAD EDITORIAL (OBLIGATORIAS)

* **R-EDI-01 (Corrección Ortográfica):** El documento no debe contener errores de digitación, tildes o concordancia (ej. corregir "2 mese" por "2 meses").
* **R-EDI-02 (Tono Corporativo):** La redacción debe ser técnica, ejecutiva y evitar lenguaje coloquial.
* **R-EDI-03 (Estandarización de Nombres):** Los nombres de proyectos y objetivos deben iniciar con mayúscula y mantener coherencia en todo el documento.

---

## 🏗️ 2. REGLAS DE ESTRUCTURA DEL DOCUMENTO (EXCEL)

* **R-EST-01 (Nombre de Hoja):** La pestaña principal del archivo debe titularse estrictamente "Matriz de Riesgos".
* **R-EST-02 (Columnas Obligatorias):** El archivo debe contener exactamente las siguientes columnas en orden:
    1. ID (Formato R-001, R-002...)
    2. Tipo de Riesgo
    3. Descripción
    4. Área Impactada
    5. Probabilidad
    6. Impacto
    7. Consecuencia
    8. Mitigación

---

## 🧠 3. REGLAS DE CONTENIDO TÉCNICO

* **R-CON-01 (Tipificación):** Los riesgos deben clasificarse exclusivamente en las categorías: **Técnico, Negocio, Recursos o Cronograma**.
* **R-CON-02 (Escalas de Valoración):**
    * **Probabilidad:** Baja, Media, Alta.
    * **Impacto:** Menor, Mayor, Crítico.
* **R-CON-03 (Especificidad Técnica):** La descripción debe mencionar componentes del stack tecnológico cuando aplique (ej. mencionar Java o DynamoDB si hay riesgos de inconsistencia de datos).
* **R-CON-04 (Coherencia de Mitigación):** Cada acción de mitigación debe ser proactiva y ejecutable por el equipo de QA o infraestructura.

---

## 📊 4. REGLAS DE ANÁLISIS ESTRATÉGICO

* **R-STR-01 (Top Críticos):** El consultor debe presentar siempre un resumen con los 3 riesgos de mayor impacto para visibilidad gerencial.
* **R-STR-02 (Criterio de Priorización):** Cualquier riesgo que combine Probabilidad Alta e Impacto Crítico debe encabezar la lista (ID R-001).

---

## ⚖️ CRITERIOS DE APROBACIÓN DE LA MATRIZ

| Resultado | Requisito de Cumplimiento |
| :--- | :--- |
| **Aprobado** | Cumple con el 100% de las reglas editoriales, estructurales y técnicas. |
| **Aprobado con Observaciones** | Fallos menores en R-EDI (ortografía no crítica) o R-CON (mitigaciones poco detalladas). |
| **No Aprobado** | Ausencia de columnas obligatorias, errores de stack tecnológico o falta de análisis de riesgos críticos. |