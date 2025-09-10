# Estándar para los Instructions 📐

## Introducción

Este documento define un estándar para estructurar archivos de instrucciones para agentes de IA. La estructura propuesta es transversal para equipos de Frontend, Backend y Mobile, facilitando la implementación consistente de buenas prácticas de ingeniería y permitiendo la "hidratación" específica según el contexto tecnológico.

### Implementación Práctica

La plantilla debe "hidratarse" con:

1. **Reglas específicas** del Chapter → Tecnología → Proyecto
2. **Mínimos de desarrollo** implementados

### Evolución Continua

Este estándar debe evolucionar basado en:

- Cambios en las capacidades de los agentes de IA
- Retroalimentación práctica de los equipos de desarrollo
- Nuevas investigaciones sobre optimización de contexto para LLMs

## Limitaciones Técnicas para Agentes de IA

### Ventanas de Contexto: Teoría vs Realidad Práctica

Los agentes de IA comerciales implementan limitaciones de contexto significativamente menores a las capacidades técnicas de los modelos subyacentes por razones de costo y rendimiento.

**Límites Teóricos vs Prácticos (Septiembre 2025):**

**Claude Sonnet 4** [(Anthropic Documentation, 2025)](https://docs.anthropic.com/en/docs/about-claude/models):

- **Teórico**: 200K tokens de contexto, 1M tokens disponible en beta
- **Práctico en agentes**: ~128K tokens (*reportado empíricamente - no verificado oficialmente*)
- **Uso empírico**: ~64K tokens (*reportado empíricamente - no verificado oficialmente*)

**GitHub Copilot**:

- Límites no documentados públicamente, implementación optimizada para costos

**Consideraciones de Implementación:**

- **Restricciones por costos**: Los proveedores de agentes limitan el contexto para mantener viabilidad económica
- **Optimización de rendimiento**: Contextos menores mejoran tiempo de respuesta y estabilidad
- **Conversión tokens-caracteres**: Aproximadamente 1 token ≈ 0.75 palabras en español
- **Límites específicos para archivos de reglas**: Windsurf documenta un límite de 12,000 caracteres por archivo de reglas [(Windsurf Documentation, 2025)](https://docs.windsurf.com/windsurf/cascade/memories)
- **Competencia por contexto**: Los archivos de instrucciones compiten por espacio con código fuente, prompts del usuario y otros elementos

### Fenómenos de Rendimiento Documentados

**Efecto "Lost in the Middle"** [(Liu et al., 2023)](https://arxiv.org/abs/2307.03172):

- La información al inicio y final de documentos largos recibe mayor atención
- Degradación de rendimiento en el contenido medio de contextos muy largos
- **Aplicación práctica**: Colocar información crítica al inicio y final de las instrucciones

**Optimización de Memoria** [(Brown et al., 2020)](https://arxiv.org/abs/2005.14165):

- Los modelos retienen mejor conceptos definidos temprano y referenciados consistentemente
- La repetición estratégica de conceptos clave mejora la retención

## Mejores Prácticas de Ingeniería de Contexto

### Principios Fundamentales

#### Conexión Lógica: Limitaciones → Soluciones

Las limitaciones identificadas llevan directamente a estas estrategias:

1. **Por límites de contexto**: Usar estructura modular para proyectos complejos
2. **Por efecto de posición**: Colocar reglas críticas al inicio y recordatorios al final
3. **Por optimización de memoria**: Repetir conceptos clave y usar referencias consistentes

### Estructura Óptima de Archivos

#### Enfoque Unificado vs. Modular

- **Archivo único**: Para proyectos con <12.000 caracteres de instrucciones
- **Estructura modular**: Para casos complejos que requieren >12.000 caracteres de instrucciones

```plaintext
/instructions/
  instructions.md            # índice principal con frontmatter y enlaces
  01-context.md              # Sección 1: General Context
  02-code-guidelines.md      # Sección 2: Code Guidelines & Standards
  03-technology.md           # Sección 3: Technology-Specific Guidelines
  04-quality.md              # Sección 4: Quality & Engineering Excellence
  05-process.md              # Sección 5: Process Requirements
  06-operations.md           # Sección 6: Observability & Operations
  99-agent-notes.md          # notas específicas para el agente
```

### Sistema de Marcado para Secciones Específicas

El sistema de marcado propuesto permite identificar claramente qué secciones son específicas de ciertos contextos tecnológicos:

```plaintext
🔵 Frontend-specific
🟢 Backend-specific
🟡 Mobile-specific
⚪ Optional for all implementations
```

> Este marcado únicamente se muestra con fines explicativos en el template  y no debe quedar en el producto final.

## Recomendaciones para Implementación

### Metodología de Validación

1. **Pruebas de efectividad empíricas**: Evaluar periódicamente la comprensión del agente sobre diferentes secciones
2. **Iteración basada en resultados**: Ajustar estructura según performance observada
3. **Hidratación contextual**: Al adaptar la plantilla para un equipo específico, mantener la estructura fundamental pero adaptar el contenido

### Métricas de Éxito

- Reducción en aclaraciones necesarias del agente
- Mejora en la calidad del código generado
- Disminución en iteraciones de refinamiento
- Consistencia en aplicación de estándares

## Estructura Unificada Sugerida

[Estructura Unificada Markdown](./instructions-template.md)

## Estructura Modularizada Sugerida

[Estructura Modularizada Markdown](./instructions-orchestrator-template.md)

**Implementación Modular:**

1. Cada archivo modular DEBE seguir internamente la misma estructura de secciones definida en la Estructura Unificada
2. Mantener títulos de secciones principales consistentes
3. Trasladar el contenido a su archivo correspondiente según funcionalidad

> 💡 **Optimización**: Se sugiere que cada archivo modular debe respetar el límite de 12,000 caracteres según la documentación de Windsurf

## Conclusión

Si para un proyecto bastan instrucciones básicas, se pueden agrupar todas en un archivo como lo muestra la Estructura Unificada; pero si se requiere de un listado de reglas complejo y extenso se recomienda optar por la Estructura Modularizada (con Orquestador).

Ambas propuestas se limitan a sugerir un Template de alto nivel que marca la estructura que debe seguir el `Instrucctions.md` con el fin de optimizarse para Agentes. Adicionalmente, se debe “hidratar” esta plantilla con las reglas específicas (contenido) pertinentes al **Chapter → Tecnología → Proyecto** y asegurarse de implementar los **mínimos de desarrollo**; por ejemplo, la sub-sección de Testing debería incluir reglas como *“utilizar TDD”*, *“seguir el patrón AAA”* y *“seguir el principio FIRST”*.
