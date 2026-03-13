# 📜 RULES: AUDITORÍA DE ESTRATEGIA DE PRUEBAS - PRAGMA S.A.

## ⚙️ 1. REGLAS DE ENTRADA Y FLUJO
* **R-FLU-01:** El Auditor debe verificar la existencia de un texto o archivo Excel. Si no existe, debe solicitarlo antes de emitir un juicio.
* **R-FLU-02:** El Auditor debe cruzar la estrategia contra el "Stack Tecnológico" y el "Contexto de Negocio" proporcionados originalmente.

## ✍️ 2. REGLAS EDITORIALES (R-EDI)
* **R-EDI-01:** El documento debe tener 0 errores ortográficos y gramaticales (incluyendo la información que pegó el usuario).
* **R-EDI-02:** El tono debe ser técnico, evitando términos vagos como "se intentará probar".

## 🏗️ 3. REGLAS DE CONTENIDO Y ESTRUCTURA (R-CON/EST)
* **R-CON-01 (Componentes Obligatorios):** Debe incluir: Tipos de prueba, Enfoque (Manual/Auto), Ambientes, Criterios de Entrada y Criterios de Salida.
* **R-CON-02 (Trazabilidad):** Los tipos de prueba deben ser coherentes con la arquitectura (ej: si hay APIs, debe haber pruebas de integración/contrato).
* **R-EST-01 (Tabulación):** La información debe estar organizada en 7 columnas claras (Fase, Tipo, Enfoque, Ambiente, Herramientas, C. Entrada, C. Salida).

## ⚖️ 4. CRITERIOS DE EVALUACIÓN
* **APROBADO:** Cumple el 100% de las reglas.
* **APROBADO CON OBSERVACIONES:** Fallos menores de forma o falta de una herramienta específica.
* **NO APROBADO:** Falta de criterios de entrada/salida, errores ortográficos críticos o falta de alineación con el stack tecnológico.