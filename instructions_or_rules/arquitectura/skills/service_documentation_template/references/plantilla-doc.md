---

**Objetivo**: Consolidar la información relevante para que las áreas encargadas puedan soportar, operar y mantener los **Servicios** en producción.

<font color="red"> - _Crear una nueva página a partir de esta plantilla y conservar su estructura base._</font>

<font color="red"> - _Si alguna sección y/o dato no aplica, diligenciarla con "N/A"._</font>

---

[[_TABLE OF CONTENTS_]]

# 0. CONFIGURACIÓN DEL CONTEXTO
<br>

### 0.1 **Parámetros de adaptación**

_Completa esta sección antes de diligenciar el resto de la plantilla. Su objetivo es adaptar el documento al tipo de servicio, nivel de criticidad y stack real sin asumir tecnologías o dominios específicos._

|**Parámetro**|**Opciones de referencia**|**Selección / Valor**|
|--|--|--|
|**Tipo de servicio**| API, backend, frontend, móvil, batch, integración, analítica, infraestructura, otro | |
|**Dominio o capacidad**| Clientes, pagos, identidad, logística, datos, plataforma, otro | |
|**Criticidad del servicio**| Alta, Media, Baja | |
|**Infraestructura principal**| AWS, Azure, GCP, on-premise, híbrida, otra | |
|**Persistencia o almacenamiento**| SQL, NoSQL, caché, archivos, almacenamiento local, no aplica | |
|**Observabilidad**| Logs, métricas, trazas, tableros, alertas, no aplica | |
|**Audiencia principal del documento**| Soporte, operación, desarrollo, arquitectura, liderazgo, otra | |
|**Notas de alcance**| Qué cubre este documento y qué queda fuera | |

|**Version**|**Fecha**|**Comentarios**|
|--|--|--|
|N.N|DD/MM/AAAA|Comentario|

# 1. GENERALIDADES
<br>

### 1.1 **Información General Servicio**

|**Ítem**|**Descripción**|
|--|--|
| **Nombre**| Nombre del servicio |
|**Descripción**| ¿Para qué se usa?, ¿Qué usuarios la utilizan?, ¿Cómo funciona? y otra información relevante. |
|**Servicios asociados**| Se refiere a los servicios de TI que se asocian con este servicio de la siguiente manera:<br> **Me Impactan**: Escribe los servicios que consume y afectan su funcionamiento normal separados por comas.<br> **Impacto**: Identifica los servicios que consumen este servicio y se ven impactados por su mal funcionamiento, separados por comas.<br> ***_Ejemplo_***:<br> **Me Impactan**: Servicio1, Servicio2<br> **Impacto**: APIxx, Web1, App1 |
|**Nivel de prioridad del servicio**| Se refiere al nivel de prioridad de cara al negocio. Elegir una de estas opciones: [ <font color="red">Alta</font> / <font color="yellow">Media</font> / <font color="green">Baja</font> ] |
|**Horario de promesa del servicio (Formato 24H)**| _Ejemplo_: 7x24, L-V 08:00 - 22:00, L-S 03:00 - 23:00, L-D 05:00 - 23:59 & 00:00 - 02:00. |
|**Fechas y horario de alta transaccionalidad/uso del servicio**| Si existen horarios o fechas de uso elevado, documentarlos. _Ejemplo_: fin de mes, promociones, días festivos. |
|**Ventana de Mantenimiento**| Si el servicio es 7x24, registrar la ventana ideal para tareas que puedan afectar su disponibilidad. |
|**Célula de trabajo**| Nombre del equipo responsable del desarrollo del servicio. |
|**Responsable**| Nombre de la persona responsable al momento de diligenciar la documentación. |
<br>

### 1.2 **Descripción detallada del servicio**

Describe el servicio explicando sus funcionalidades, su valor operativo o de negocio, y cómo interactúan usuarios o servicios consumidores con él.

<br>

# 2. DISEÑOS

### 2.1 **Diagramas de Arquitectura / Componentes del Servicio**

- [Enlaces](URL) a estos diseños.
- Incluir los diagramas necesarios para entender el flujo del servicio en sus componentes.
- Si existen otros diagramas relevantes para la operación, incluirlos también.
<br>

### 2.2 **Blueprint o Flujo de la Experiencia**

- [Enlaces](URL) a los diseños del flujo.
- Incluir el enlace al flujo funcional o de experiencia en la herramienta que use el equipo.

# 3. OPERACIÓN

## <font color="MAGENTA"> **Infraestructura**</font>
<br>

### 3.1 **Nombre de recursos del servicio**

_Incluir en la siguiente tabla los recursos utilizados por el servicio. Pueden ser dedicados, compartidos o provistos por terceros, siempre que cumplan un rol relevante para la operación._
<br>

|  **Nombre de recurso**  |  **Tipo de recurso**  |  **Rol** | **Impacto en caso de afectación** | **Ruta de logs en caso de aplicar** |
|  --  |  --  |  --  | -- | -- |
| _Ejemplo_: ServicioIdentidadCache | Caché administrada | Acelera la consulta de datos frecuentes del servicio. | Aumento de latencia o indisponibilidad parcial en flujos dependientes. | /ruta/o/enlace/a/logs |

<br>

## <font color="MAGENTA"> **Bases de Datos**</font>

_Diligenciar la información de base de datos o almacenamiento persistente relevante para la operación._
<br>

### 3.3 **Información Plataforma BD**

|**Nombre Base Datos**|**Tipo Base de Datos**|**Detalle**|
|--|--|--|
| BasePrincipalServicio | SQL, NoSQL, caché local o almacenamiento embebido | Datos, configuración o estado que soportan la operación del servicio. |
|  |  |  |
<br>

## <font color="MAGENTA"> **Integración**</font>
<br>

### 3.4 **Información integraciones**

_Si aplica, incluir información de integraciones con terceros o con otros sistemas: APIs consumidas, endpoints, servicios web, direccionamientos, VPNs, certificados, colas o archivos._
<br>

## <font color="MAGENTA">**Observabilidad**</font>
<br>

### 3.5 **Tableros o Dashboards del servicio**

_Debe incluir los enlaces a los tableros, paneles o consultas usadas para operar el servicio._

| **Herramienta** | **Tipo** | **URL** |
| -- | -- | -- |
| Plataforma de monitoreo principal | Métricas, logs, trazas o alertas | [Tablero]() |
|  |  |  |
<br>

## <font color="MAGENTA"> **Estrategias de Recuperación**</font>
<br>

### 3.11 **Capas de la Aplicación o Componente**

_Diligenciar la siguiente información para cada capa relevante._

|  **Capa**  |  **¿Tiene alta disponibilidad?**  |  **Cantidad replicas Min - Max**  | **Tipo de Despliegue** | **Tipo de Recuperación**  |
|  --  |  --  |  --  |  --  |  --  |
|  Web, Presentación, Negocio o Base de Datos, etc.  | Si/No  |  5 - 20  |  Pipeline as code / Pipeline classic  |  Automático / Automático + Manual / Manual  |
|    |    |    |    |    |
<br>

## <font color="MAGENTA"> **Seguridad**</font>
<br>

### 3.12 **Reglas de Firewall**

_Diligenciar si se conocen reglas configuradas con IP/Puerto Origen/Destino._
<br>

# 4. SOLUCIÓN DE PROBLEMAS

### 4.1 **Ejemplo de transacción exitosa**

_Incluir ejemplos de transacciones exitosas o enlaces a esta información para entender cuál es una ejecución correcta del servicio._

_Ejemplo_
#### Request de referencia
```bash
curl --location 'https://[DOMINIO]/[SERVICIO]/[VERSION]/[RECURSO]' \
--header 'trace-id: [IDENTIFICADOR-TRAZA]' \
--header 'Accept: application/json' \
--header 'Authorization: Bearer [TOKEN]' \
--data '[PAYLOAD-OPCIONAL]'
```

#### Respuesta exitosa
```json
{
  "status": "success",
  "message": "Operación completada correctamente",
  "data": {
    "id": "[IDENTIFICADOR]",
    "timestamp": "[ISO-8601]"
  }
}
```

_Sugerencia_: Si el servicio no es HTTP, documentar el equivalente operativo: evento publicado, tarea batch exitosa, archivo generado o respuesta de un proceso interno.

<br>

### 4.2 **Respuestas**

_Diligenciar los códigos de respuesta y su descripción. También es válido poner enlaces a esta información._

Ejemplo.
- Código o evento: `200` / `SUCCESS`
- Descripción: Respuesta exitosa con datos válidos.
- Referencia: [Enlace a documentación interna](URL)

<br>

### 4.3 **Errores Conocidos**

_En esta sección es importante diligenciar los errores conocidos, su consecuencia, su causa y su solución._

| **Servicio/Capa** | **Error** | **Consecuencia** | **Causa** | **Solución** |
|--|--|--|--|--|
| _Ejemplo_ API / Aplicación / Base de datos | Timeout, respuesta inválida o inconsistencia de datos | Interrupción parcial o total del flujo dependiente | Saturación, dependencia degradada, error de configuración u otra causa confirmada | Acción de mitigación, workaround o referencia a runbook |
|  |  |  |  |  |
<br>