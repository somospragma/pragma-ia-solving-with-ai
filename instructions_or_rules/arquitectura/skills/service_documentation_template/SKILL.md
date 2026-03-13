---
name: service_documentation_template
description: Usa este skill para crear, completar o auditar documentación operativa de un servicio o componente que deba quedar operable por soporte, operación o ingeniería. Actívalo cuando el usuario pida un runbook, handoff a soporte, ficha técnica operable, documentación de troubleshooting, recuperación, observabilidad, errores conocidos o preguntas guiadas para completar vacíos de una plantilla. También úsalo para convertir notas dispersas en un borrador operativo o revisar documentación de servicio por faltantes o inconsistencias. No lo uses para diseño de arquitectura, debugging de incidentes, dashboards, contratos API, pruebas, documentación funcional ni definición de SLOs o SLAs.
compatibility:
  tools:
    - Read
    - Write
    - Edit
---

# Plantilla De Documentación Operativa De Servicios

Usa este skill para convertir conocimiento disperso de un servicio en documentación que otro equipo realmente pueda operar. El objetivo no es producir un texto elegante; el objetivo es dejar un documento útil para soporte, operación o ingeniería sin obligarlos a adivinar contexto crítico.

## Recursos embebidos

Lee los recursos embebidos antes de redactar cuando apliquen:

- `references/plantilla-doc.md`: plantilla canónica de la estructura final. Léela antes de redactar o auditar el documento.

## Flujo de trabajo

Sigue esta secuencia:

1. Clasifica la tarea en uno de estos modos: entrevista guiada, borrador desde intake o auditoría/refinamiento.
2. Lee `references/plantilla-doc.md` antes de escribir contenido por sección.
3. Resume el contexto confirmado en términos operativos.
4. Recorre la plantilla en orden en vez de saltar de inmediato a troubleshooting.
5. Marca como `Pendiente de confirmar` lo que aplique pero no esté confirmado.
6. Usa `N/A` solo cuando una sección realmente no aplique.
7. Valida coherencia entre criticidad, dependencias, observabilidad, recuperación y errores conocidos antes de cerrar.

Prefiere siempre el siguiente paso útil más pequeño. Si el usuario todavía debe aportar contexto crítico, no adelantes un borrador enorme ni un cuestionario gigante. Haz avanzar el documento con la estructura mínima necesaria para destrabar la siguiente respuesta.

## Selección de modo

Elige el modo que realmente corresponda a la necesidad del usuario.

### Usa entrevista guiada cuando

- El usuario solo tiene notas parciales.
- El propósito, la criticidad o las dependencias del servicio todavía no están claros.
- Recuperación, observabilidad u ownership operativo siguen siendo desconocidos.
- El pedido se parece más a “ayúdame a completar esto” que a “aquí está el intake completo”.
- Los hechos conocidos son demasiado pocos para justificar tablas grandes ya diligenciadas.

### Usa borrador desde intake cuando

- El usuario ya entregó suficiente información para completar buena parte de la plantilla.
- El tipo de servicio, su propósito y su criticidad ya son conocidos.
- Existe suficiente contexto operativo para redactar sin demasiada ida y vuelta.

### Usa auditoría o refinamiento cuando

- El usuario quiere revisar un documento existente.
- El usuario pide detectar vacíos, inconsistencias o riesgos operativos.

## Modo entrevista guiada

Usa entrevista guiada para reducir suposiciones. Haz preguntas en bloques cortos para que el usuario pueda responder rápido y el documento mejore sección por sección.

### Cómo ejecutarlo

1. Haz preguntas en bloques de 3 a 5.
2. Empieza por identidad del servicio, propósito y criticidad operativa.
3. Luego avanza a dependencias, horarios, ownership y observabilidad.
4. En la primera respuesta, prioriza un resumen compacto del contexto más un bloque corto de preguntas. No rellenes tablas grandes salvo que eso realmente elimine ambigüedad.
5. Redacta solo las secciones que ya tengan suficiente base.
6. Mantén como `Pendiente de confirmar` los campos relevantes que sigan abiertos.

### Comportamiento en el primer turno

En la primera respuesta de entrevista guiada, optimiza para que sea fácil responder, no para que esté completa:

- Haz el conjunto más corto de preguntas que desbloquee la siguiente sección.
- Evita convertir la primera respuesta en un cuestionario largo.
- Evita llenar tablas amplias con puro `Pendiente de confirmar`.
- Si una sección parcial muy pequeña realmente ayuda, limítala a los pocos campos confirmados.

### Preguntas mínimas por sección

- Contexto: tipo de servicio, dominio, criticidad, audiencia, alcance.
- Generalidades: nombre, propósito, usuarios o consumidores, servicios upstream y downstream, expectativas de disponibilidad, owners.
- Diseño: diagramas, flujos o documentos fuente existentes.
- Operación: recursos, persistencia, integraciones, monitoreo, logs, alertas, recuperación, restricciones de seguridad.
- Troubleshooting: ejemplo de operación exitosa, resultados esperados, errores conocidos, mitigaciones actuales.

## Modo borrador desde intake

Usa este modo cuando el usuario quiera un primer borrador utilizable de inmediato.

### Cómo ejecutarlo

1. Convierte el intake en hechos operativos.
2. Identifica la información faltante antes de escribir.
3. Redacta la plantilla en orden.
4. Llena solo los campos soportados por input explícito del usuario o por una reformulación casi literal de ese input.
5. Mantén el borrador más estrecho que la evidencia disponible, no más amplio.
6. Cierra con una lista corta de elementos todavía pendientes de confirmar.
7. Prefiere la terminología del usuario sobre etiquetas renombradas o normalizadas, salvo que el usuario ya haya dado un nombre canónico oficial.

### Postura por defecto

En modo borrador desde intake, actúa de manera conservadora:

- Prefiere omitir y marcar `Pendiente de confirmar` antes que completar especulativamente.
- Prefiere frases cortas y factuales antes que expansión explicativa.
- Prefiere las etiquetas del usuario antes que reinterpretaciones con lenguaje arquitectónico.
- Prefiere “servicio descrito como X” antes que asignar un nombre oficial no dado.
- Prefiere dejar audiencia, ownership e intención operativa sin asignar salvo que se hayan declarado o sean inevitables por el pedido.

### Límite de inferencia

No inventes:

- SLAs o SLOs.
- Owners o nombres de equipos.
- Nombres oficiales del servicio si el usuario solo describió la capacidad.
- Audiencia objetivo si el usuario no la indicó y no es obvia por el pedido.
- Nombres de dominio o capacidad más allá de lo que el usuario explicitó.
- Roles concretos de recursos cuando el recurso fue nombrado pero su función no fue descrita.
- Picos esperados, supuestos de mantenimiento o consumidores implícitos.
- URLs, links de dashboards o endpoints.
- Cantidades de réplicas o topología de despliegue.
- Estrategias de recuperación o controles de seguridad.

Si el campo importa y el usuario no lo dio, márcalo como `Pendiente de confirmar`.

Cuando dudes entre un borrador amplio y uno más acotado pero fiel, elige el más acotado.

### Transformaciones permitidas

En este modo sí puedes:

- Reordenar los hechos del usuario para ajustarlos a la plantilla.
- Convertir una afirmación del usuario en una celda de tabla sin cambiar su significado.
- Repetir una dependencia o tecnología nombrada por el usuario en la sección relevante.
- Marcar campos ausentes pero relevantes como `Pendiente de confirmar`.

En este modo no puedes:

- Expandir un hecho en varios hechos no declarados.
- Convertir una descripción genérica en un nombre formal del servicio.
- Concluir audiencia de soporte, modelo de ownership o taxonomía de errores sin evidencia.
- Añadir detalle operativo ilustrativo que suene a conocimiento confirmado del sistema.

### Regla especial para secciones de troubleshooting

Las secciones `4.1`, `4.2` y `4.3` requieren evidencia más fuerte que el resto de la plantilla porque es muy fácil sobrellenarlas con detalle operativo plausible pero no verificado.

Cuando el usuario no haya dado un ejemplo real de request, un ejemplo real de response, un catálogo de respuestas, un patrón de incidentes o una lista de errores conocidos:

- No fabriques un ejemplo concreto de request o response, ni siquiera como mock lleno de placeholders.
- No inventes códigos HTTP, nombres de eventos o campos de token solo porque sean comunes.
- No rellenes `Errores conocidos` con filas especulativas basadas en intuición general de sistemas.
- En su lugar, indica que la sección aplica pero sigue `Pendiente de confirmar`, y lista exactamente qué evidencia hace falta para completarla.

### Fallback mínimo para las secciones 4.1 a 4.3

Si falta evidencia, usa esta postura:

- `4.1 Ejemplo de transacción exitosa`: describe qué tipo de evidencia se necesita, no un ejemplo fabricado.
- `4.2 Respuestas`: indica que el catálogo de respuestas depende del contrato real del API o del proceso y permanece `Pendiente de confirmar`.
- `4.3 Errores Conocidos`: deja la sección sin filas, salvo una nota indicando que incidentes conocidos, impacto, causa y mitigación deben confirmarse desde historial productivo o runbooks.

## Modo auditoría y refinamiento

Usa este modo cuando al usuario le importe más la calidad de un documento existente que generar uno nuevo desde cero.

### Cómo ejecutarlo

1. Revisa el documento sección por sección contra `references/plantilla-doc.md`.
2. Señala faltantes operativos, contradicciones y acoplamiento a cliente.
3. Prioriza los problemas que bloquearían soporte o recuperación durante un incidente.
4. Recomienda correcciones concretas.
5. Evita reescribir todo el documento salvo que el usuario lo pida.

### Si falta el documento fuente

Si el usuario pide una auditoría pero no comparte el documento ni un enlace:

1. Di explícitamente que la auditoría es provisional porque falta el documento fuente.
2. No finjas que auditaste contenido que no puedes ver.
3. Entrega una solicitud compacta de evidencia más el checklist mínimo que el documento debe cumplir.
4. Mantén la respuesta accionable, pero no la expandas en un ensayo genérico.

## Guía por sección

Sigue el orden de la plantilla en `references/plantilla-doc.md`.

### 0. Configuración del contexto

Confirma tipo de servicio, dominio, criticidad, infraestructura, persistencia, observabilidad, audiencia principal y alcance del documento.

### 1. Generalidades

Confirma nombre del servicio, propósito, relaciones entre servicios, prioridad, horario, ventana de mantenimiento, equipo y responsable.

### 2. Diseños

Apunta a diagramas o flujos cuando existan. Si deberían existir pero no están disponibles, usa `Pendiente de confirmar` en vez de inventar enlaces.

### 3. Operación

Captura los recursos que importan operativamente: infraestructura, persistencia, integraciones, dashboards, recuperación y restricciones de seguridad conocidas.

### 4. Solución de problemas

Describe cómo luce una ejecución sana, qué respuestas se esperan y qué fallas ya son conocidas, pero solo cuando exista evidencia suficiente.

Si el servicio no es HTTP, adapta esta sección al modelo real: job, batch, evento, cola, procesamiento de archivos o proceso interno.

## Estructura de salida

Usa exactamente una de estas formas de respuesta según el modo seleccionado.

### Salida para entrevista guiada

```md
Modo seleccionado: Entrevista guiada

## Resumen de contexto
- ...

## Preguntas pendientes
- ...

## Secciones con base suficiente
### 0. Configuración del contexto
...

## Checklist final
- [ ] ...
```

### Salida para borrador desde intake

```md
Modo seleccionado: Intake único

## Resumen de contexto
- ...

## Contenido para la plantilla
### 0. Configuración del contexto
...

### 1. Generalidades
...

### 2. Diseños
...

### 3. Operación
...

### 4. Solución de problemas
...

## Vacíos detectados
- ...

## Checklist final
- [ ] ...
```

### Salida para auditoría o refinamiento

```md
Modo seleccionado: Auditoría o refinamiento

## Resumen de contexto
- ...

## Hallazgos
- ...

## Ajustes recomendados
- ...

## Vacíos detectados
- ...

## Checklist final
- [ ] ...
```

## Validaciones de calidad

Antes de terminar, verifica estos puntos:

- Un servicio de alta criticidad no debería quedar con observabilidad o recuperación vacías salvo que esa ausencia quede explícitamente documentada.
- Un servicio `7x24` no debería omitir la ventana de mantenimiento sin explicación.
- Las integraciones críticas deberían aparecer tanto en operación como en troubleshooting o riesgos.
- Los errores conocidos deberían tener al menos causa, impacto o mitigación cuando exista evidencia.
- Si la audiencia es soporte u operación, el ejemplo de ejecución sana debería ser accionable y no abstracto.
- La entrevista guiada debe sentirse fácil de responder de una sola vez; si el bloque de preguntas se siente agotador, es demasiado grande.
- El modo auditoría no debe sobreafirmar certeza cuando falta el artefacto fuente.

## Errores a evitar

- No conviertas placeholders en datos inventados.
- No asumas un vendor específico solo porque sea común.
- No conviertas la respuesta en un resumen ejecutivo si el usuario necesita un documento operable.
- No dejes una sección relevante vacía sin indicar si es `N/A` o `Pendiente de confirmar`.
- No conviertas la entrevista guiada en un intake de más de 20 preguntas salvo que el usuario pida un cuestionario exhaustivo.
- No renombres silenciosamente el servicio, el equipo o la audiencia si el usuario no los definió.
- No trates la plantilla del repositorio como si fuera el documento bajo auditoría salvo que el usuario la haya dado explícitamente como objetivo de revisión.

## Ejemplos

**Ejemplo 1:**
Entrada: "Necesito documentar una API interna de identidad. Atiende autenticación y perfiles, es crítica, corre en nube pública, tiene PostgreSQL, Redis, tableros de métricas y logs, pero todavía no tengo claro el proceso de recuperación."
Salida esperada: seleccionar entrevista guiada, preguntar primero por owners, ventana de mantenimiento, enfoque de recuperación y dependencias críticas, redactar solo las secciones con base real y dejar recuperación como `Pendiente de confirmar` si el usuario sigue sin conocerla.

**Ejemplo 2:**
Entrada: "Necesito documentar un servicio pero solo sé que se llama GeneradorReportes, lo usa finanzas y corre por la noche."
Salida esperada: seleccionar entrevista guiada, hacer solo las primeras 3 a 5 preguntas necesarias para clasificar el componente y su criticidad, y evitar llenar casi toda la plantilla antes de que el usuario responda.

**Ejemplo 3:**
Entrada: "Audita esta documentación operativa" sin adjuntar el documento.
Salida esperada: indicar que la auditoría es provisional porque falta la fuente, pedir el artefacto y entregar un checklist corto de lo que se revisará cuando el documento sea compartido.

## Prompts iniciales de prueba

Usa estos prompts como set inicial de evaluación del skill.

**Prompt 1:**
"Ayúdame a llenar la documentación operativa de un servicio backend de autenticación. Es un API REST crítica, opera 7x24, usa PostgreSQL y Redis, corre en nube pública, tiene dashboards de métricas y logs, depende de un proveedor de identidad externo y de un servicio interno de perfiles. Quiero una salida lista para la plantilla y si falta algo lo debes marcar como pendiente de confirmar."

**Prompt 2:**
"Necesito documentar un servicio pero solo tengo estos datos: se llama GeneradorReportes, lo usa el equipo financiero para cierres diarios y corre una vez por noche. Hazme las preguntas necesarias para completar la plantilla operativa sin inventar información."

**Prompt 3:**
"Revisa una documentación operativa existente y dime si está incompleta o tiene vacíos críticos para soporte. Quiero hallazgos accionables sobre observabilidad, recuperación y errores conocidos, sin reescribir todo desde cero."