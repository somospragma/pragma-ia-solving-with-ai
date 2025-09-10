# Amazon Q vs. GitHub Copilot

Este documento presenta una comparativa rápida entre Amazon Q Developer y GitHub Copilot, evaluando sus capacidades y funcionalidades.

## **Tabla Comparativa | Resumen**

|            Característica            |                                                                                                                                   Amazon Q Developer                                                                                                                                   |                                                                                                                                           GitHub Copilot                                                                                                                                            |
| :----------------------------------: | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
|         **Modo Agente/Ask**          | Opera en un modo de agente conversacional. Acceso a tools básicas: fsRead, fsWrite, fsReplace, listDirectory, fileSearch, executeBash, codeReview, displayFindings Amazon Q tiene mucha menor adaptabilidad al lenguaje español respecto a Copilot, como se evidenció en algunas POCs. |                                                 Ofrece modo Agente, Ask y Edit (versión 'lite' del agente para interacciones rápidas, no puede iterar). Acceso a todas las tools disponibles en la actualidad y también de extensiones de VS Code.                                                  |
|              Checkpoint              |                                                                                                                                          NA.                                                                                                                                           |                                                                                                               Dispone de un sistema de "Checkpoints" y edición de prompts anteriores.                                                                                                               |
|      **Indexación de Proyecto**      |                                                                                                           Solo local. No tiene un límite predefinido; el usuario lo define.                                                                                                            | Admite indexación local y remota.Límites locales: \< 750 archivos (índice avanzado automático); 750-2500 archivos (índice manual); \> 2500 archivos (índice básico si no hay remoto). Indexación remota para [GitHub.com/Enterprise](https://GitHub.com/Enterprise) Cloud; se mantiene actualizada. |
|               Terminal               |                                                                                                        Directamente sobre el chat. NO tiene acceso a las terminales de VS Code.                                                                                                        |                                                                                Opción de integrar la terminal del agente con la terminal estándar de VS Code; Copilot tiene acceso y puede crear varias instancias.                                                                                 |
|              Seguridad               |                                                                                                                               Security Scanning avanzado                                                                                                                               |                                                                                                                                                 NA.                                                                                                                                                 |
|             Paralelismo              |                                                              Permite la ejecución de dos Chats simultáneamente. No cuenta con protección para tareas paralelas, pero el segundo chat puede releer y resolver conflictos.                                                               |                                                                                                                                                 NA.                                                                                                                                                 |
|     Configuración de MCP Server      |                                                                                                   Ofrece control granular de permisos por herramienta (requiere ajuste individual).                                                                                                    |                                                                                                               Tiene un marketplace. Detecta MCP Servers activos de Windsurf o Cursor.                                                                                                               |
|    **Características Exclusivas**    |                                                                           Integración nativa con IAM y completa con AWS; Debugging Assistance especializado; Security Scanning avanzado (específico de AWS).                                                                           |                                                            Remote Index para repositorios GitHub; Planning Mode específico; Checkpoints; Simple Browser/Preview; Asignación automática de Issues; Creación automática de Pull Requests.                                                             |
|               Pinning                |                                                                                                                       Ofrece varias de las opciones de Copilot.                                                                                                                        |                                                       El mejor sistema de Pinning que se ha explorado: Folders, Files completos o líneas seleccionadas, Tools, Secciones Markdown, Prompt Files, Instrucciones, Imágenes, problems, symbols.                                                        |
| Rules (Instrucciones para el agente) |                                                                                                             Permite manipular qué reglas usar desde una interfaz gráfica.                                                                                                              |                                                                                                                 Se pueden generar automáticamente con Copilot en un archivo ‘raíz’.                                                                                                                 |
|         Interfaz de Cambios          |                                                                  No tan avanzada como Copilot. Realiza los cambios de forma directa y luego ofrece la opción de revertirlos. Muestra los cambios solo al hacer clic.                                                                   |                                                                                             Proporciona un control granular y total sobre los cambios, mostrándolos visualmente sobre el archivo real.                                                                                              |
|            Planning Mode             |                                                                                                                              NA. Se puede hacer “a mano”.                                                                                                                              |                                                                                                                Ofrece un modo dedicado para la planificación de tareas y desarrollo.                                                                                                                |

## **GitHub Copilot: Características Exclusivas**

GitHub Copilot se destaca por las siguientes funcionalidades que no se encuentran en Amazon Q:

- **Remote Index para repositorios GitHub**.
- **Asignación automática de Issues**.
- **Creación automática de Pull Requests**.

### **GitHub Copilot: Capacidades y Observaciones Adicionales**

A continuación, se detallan observaciones y pruebas realizadas sobre las capacidades de GitHub Copilot:

- **Modo Agente/Ask:** GitHub Copilot ofrece un modo de agente conversacional ("Agent Mode") y un modo de pregunta ("Ask Mode"). Adicionalmente, cuenta con un modo de edición ("Edit Mode"), que funciona como una versión pequeña del agente para interacciones rápidas (por ejemplo, no puede iterar).
  - **Tools nativas a las que tiene acceso el modo agente:**
  - **Tools extra de extensiones:**
  - **Commands:**
- **Checkpoint:** Dispone de un sistema de "Checkpoints" que permite guardar el estado del trabajo y un historial de prompts anteriores para su edición y reutilización.
- **Indexación de Proyecto:**
  - **Indexación Local:** Para proyectos con menos de 750 archivos indexables, Copilot construye automáticamente un índice local avanzado. Para proyectos entre 750 y 2500 archivos indexables, se puede construir el índice local manualmente a través de la paleta de comandos. Si un proyecto supera los 2500 archivos indexables y no tiene un índice remoto, Copilot utiliza un índice básico.
  - **Indexación Remota:** Copilot puede utilizar índices de búsqueda de código remotos para repositorios alojados en GitHub.com o GitHub Enterprise Cloud. Estos índices se construyen automáticamente cuando se usa @workspace o \#codebase por primera vez, o se pueden forzar mediante el comando Build Remote Workspace Index. Una vez creado, el índice se mantiene actualizado con los cambios recientes en segundos.
  - doc: <https://code.visualstudio.com/docs/copilot/reference/workspace-context#:~:text=GitHub%20Remote%20indexing,available%20remote%20code%20search%20indexes>.
- **Terminal:** La interacción con la terminal se puede llevar a cabo directamente en el chat. Además, existe la opción de integrar la terminal del agente con la terminal estándar de VS Code, permitiendo que Copilot tenga acceso y cree múltiples instancias de terminal según sea necesario.
- **Seguridad:** Recientemente se ha añadido la funcionalidad de visualizar y exportar logs de actividad, lo que mejora la transparencia y la capacidad de auditoría de las interacciones con Copilot.
- **Paralelismo:** Actualmente, GitHub Copilot NO soporta la ejecución de múltiples conversaciones de forma paralela.
- **Configuración de MCP Server:** Permite una configuración sencilla de los MCP Servers a través de la paleta de comandos de VS Code. Además, Copilot detecta automáticamente MCP Servers activos de otras herramientas como Windsurf o Cursor y cuenta con un Marketplace para estos mismos.
- **Pinning:**
  - **Instrucciones:** Compatible con `Instructions.md` a nivel de workspace.
  - **Prompt Files:** Compatible con prompt files a nivel de workspace.
  - **Folders:** Permite anclado de carpetas.
  - **Files:** Permite anclado de archivos completos y selecciones de líneas puntuales.
  - **Tools:** Permite anclado de herramientas (built-in, extensiones, mcp servers)
  - **Markdown:** Permite anclado de secciones de un markdown (ej: anclar el título h2 del README ‘\#\# 1. Se debe…’’)

## **Amazon Q Developer: Características Destacadas**

Amazon Q Developer posee integraciones y funcionalidades clave dentro del ecosistema AWS:

- **Integración nativa con IAM**.
- **Integración completa con AWS**.
- **Debugging Assistance especializado**.
- **Security Scanning avanzado (específico de AWS)**.

### **Amazon Q Developer: Capacidades y Observaciones Adicionales**

A continuación, se detallan observaciones y pruebas realizadas sobre las capacidades de Amazon Q:

- **Modo Agente/Ask:** Amazon Q opera en un modo de agente conversacional.
  - **Acceso a tools:** Mínimamente puede leer el código base, hacer fetch, editar archivos y ejecutar comandos. Sin embargo, no demuestra tener acceso a otras Tools que Copilot sí tiene acceso:
  - **Commands:**
- **Sin Checkpoint:** A diferencia de otras herramientas, no dispone de un sistema de "checkpoint" para guardar estados.
- **Indexación de Proyecto:**
  - **SOLO LOCAL:** La indexación de proyectos se realiza únicamente de forma local.
  - **Límites:** No tiene un límite predefinido; el usuario es quien lo define.
  - doc: <https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/workspace-context.html>
- **Terminal:** La ejecución de comandos se realiza directamente sobre el chat. No parece haber una opción para interactuar con la terminal a través de VS Code de manera observable o manipulable por el usuario.
- **Seguridad:** Security Scanning avanzado
- **Paralelismo:** Permite la ejecución de dos tareas (conversaciones/chats) de forma simultánea.
  - **Protección de tareas paralelas:** No cuenta con un sistema de protección para tareas paralelas. Si dos chats intentan modificar el mismo archivo, se pueden generar errores. Sin embargo, el segundo chat es capaz de re-leer el archivo y resolver el conflicto.
- **Configuración de MCP Server:**
  - Permite la configuración a través de una interfaz gráfica, lo cual es estético pero podría ser menos eficiente que un archivo .json para configuraciones complejas.
  - **Control granular de permisos:** Ofrece un control granular de permisos por herramienta, lo cual es una ventaja significativa. Sin embargo, esto implica ingresar a cada configuración de MCP para ajustarlos (desventaja).
- **Pinning:**
  - **Prompt Files:** Es compatible con PromptFiles a nivel de usuario (/.aws).
  - **Folders:** Permite anclado de carpetas.
  - **Files:** Permite anclado de archivos.
  - **Code:** Permite anclado de código (subconjunto de archivos).
  - **Images:** Permite anclado de imágenes.
  - Posee una opción similar a @workspace de Copilot.
- **Rules:**
  - Se guardan a nivel de workspace, similar a Copilot, sin un archivo "raíz" centralizado.
  - **Ventaja:** Permite manipular las reglas a utilizar desde una interfaz gráfica, facilitando su gestión.
- **Interfaz de Cambios:**
  - No es tan avanzada como Copilot. Realiza los cambios de forma directa y luego ofrece la opción de revertirlos.
  - Copilot proporciona un control granular y total sobre los cambios, mostrándolos visualmente sobre el archivo real. Amazon Q solo muestra los cambios una vez que se hace clic sobre ellos.
- **Planning Mode:**
  - No lo trae integrado de manera nativa.
  - Puede reemplazarse manualmente si se le solicita explícitamente que lo realice en un archivo `.md`.

## **Conclusiones**

La **elección** entre **Amazon Q Developer y GitHub Copilot** **depende** en gran medida **del contexto**, las prioridades del equipo y la infraestructura tecnológica existente:

### Escenarios donde cada Agente podría ser la mejor opción

#### **Amazon Q Developer:**

1. **Entornos fuertemente acoplados a AWS.**
2. **Proyectos Backend con Java:** Según las pruebas exploratorias internas, Amazon Q ha mostrado un rendimiento superior en Backend Java.
3. **Beneficios económicos como Partner de AWS.**
4. **Equipos que valoran la especialización sobre la versatilidad general.**
5. **Proyectos Fintech/Banca:** Debido al control granular de Amazon Q sobre las herramientas de los MCP Servers y por su herramienta de Análisis de Seguridad.

#### **Github Copilot:**

1. **Desarrollo Frontend y Backend Node JS:** Las pruebas (de baja rigurosidad) indican que Copilot podría ofrecer un mejor rendimiento. Su integración de alto nivel con VS Code lo hace una opción sólida que le da **acceso a muchas Tools nativas del IDE**.
2. **Equipos que trabajan con múltiples lenguajes y plataformas (agnóstico a la nube):** GitHub Copilot se describe como una herramienta más _agnóstica a la plataforma_, con un amplio soporte de lenguajes y compatibilidad con varios IDEs (VS Code, JetBrains, Neovim).
3. **Proyectos que se benefician de la indexación remota de GitHub:** La capacidad de Copilot para indexar repositorios remotos directamente desde GitHub (Remote Index) es una ventaja significativa para equipos cuyo código base reside principalmente en GitHub.
4. **Vanguardia en funcionalidades:** Copilot ha demostrado integrar más rápidamente las últimas features del mercado respecto a Amazon Q, por ejemplo: **Planning Mode, Checkpoints, Preview/Simple Browser**.
5. **Control granular de cambios y visualización de _diffs_:** La interfaz de cambios de Copilot es superior, ofreciendo un control granular y una visualización clara de los cambios en tiempo real, lo que facilita la revisión y aceptación de las sugerencias de código.
6. **Sentimiento general del mercado y adopción.**
7. **Proyectos Enormes que se beneficien de indexación remota.**

En síntesis, **se recomienda una estrategia híbrida** donde la selección de la herramienta se adapte a las necesidades específicas de cada proyecto: **Amazon Q** para la eficiencia y optimización en el **_backend_** **Java/AWS**, y **GitHub Copilot** para la agilidad y versatilidad en desarrollos **Frontend** y **backend** **NodeJS**.

### Consideraciones Extra a tener en cuenta:**

- Microsoft es dueña y desarrolladora de Visual Studio Code, el IDE (o editor de texto) más utilizado en el mundo (para js, ts, py, entre otros); así mismo, es dueña y desarrolladora de Github Copilot, la herramienta agéntica (en formato plugin) más utilizada actualmente.

- Amazon Q seguramente dará acceso a Kiro (si este “experimento” tiene éxito), que es un fork de Visual Studio Code; si se da esta “migración”, sería una competencia frente a Copilot mucho más interesante en Front.

Con base a esto, mientras la comparación se haga frente al plugin “Amazon Q”, **no es factible que este Agente alcance a Copilot en integración a las tools y extensiones del IDE,** ni en adaptación a nuevas features de vanguardia.

#### VERSIÓN DEL FORMATO

##### **Información de la versión 1.0**

|        Elaborado por        |   Fecha    |
| :-------------------------: | :--------: |
|   Santiago Betancur Duque   | 2025/08/28 |
|   Bryan Villamil Acevedo    | 2025/08/28 |
| Luis Felipe Quintero Arenas | 2025/08/28 |
