# pragma-ia-solving-with-ai

Repositorio que busca centralizar distintos artefactos de IA, como: Instructions, Prompts y Chatmodes.

## 🚀 Guía de Inicio Rápido

1. **🤖 Revisa la [Comparativa GitHub Copilot vs Amazon Q](https://alejandria.pragma.co/es/private/conocimiento-aplicado/inteligencia-artificial/kc-cc/gen-ai/asistentes-code/amazonq-vs-copilot)**, si quieres entender cuál es la herramienta de IA más adecuada para tu proyecto
2. **📋 Revisa el [Estándar de Instrucciones](https://alejandria.pragma.co/es/private/conocimiento-aplicado/inteligencia-artificial/kc-cc/gen-ai/asistentes-code/estandar-instrucciones)**, si quieres entender cómo se crearon las instrucciones efectivas para agentes de IA disponibilizadas en este repositorio
3. **🎯 Explora las [Funcionalidades de Personalización](#funcionalidades-de-personalización-de-los-agentes)** para transformar tu experiencia con agentes de IA

---

## Estructura del Repositorio

```plaintext
📁 chatmodes/               → Modos de chat personalizados
📁 instructions_or_rules/   → Instrucciones personalizadas por chapter y estándares
📁 prompts/                 → Prompts reutilizables para tareas específicas  
📁 resources/               → Recursos reutilizables invocados desde el Pragma MCP
📄 CONTRIBUTING.md          → Guía para contribuir al repositorio
```

## 📝 Contribuir

¡Las contribuciones son bienvenidas! Consulta nuestra [Guía de Contribución](./CONTRIBUTING.md) para obtener detalles sobre cómo enviar nuevas instrucciones y prompts.
> Guía de contribución por definir.

---

## Funcionalidades de Personalización de los Agentes

Actualmente, los Agentes ofrecen diversas formas para personalizar la asistencia de la Inteligencia Artificial, entre esas destacan:

| **📋 [Instrucciones Personalizadas](#instrucciones-personalizadas)** | **🎯 [Prompts Reutilizables](#prompts-reutilizables)** | **🧩 [Modos de Chat (SOLO Copilot)](#modos-de-chat-personalizados-en-github-copilot)** |
| --- | --- | --- |
| Define pautas comunes para tareas como generación de código, revisiones y mensajes de commit. Describe _cómo_ deben realizarse las tareas. | Crea prompts reutilizables e independientes para tareas específicas. Describe _qué_ debe hacerse con pautas opcionales específicas de la tarea. | Define el comportamiento del chat, herramientas disponibles y patrones de interacción con el código base dentro de límites específicos para cada solicitud. |

> **💡 Pro Tip:** Las instrucciones personalizadas solo afectan al Chat (no a las completaciones de código en línea). Puedes combinar los tres tipos de personalización: usa instrucciones personalizadas para pautas generales, archivos de prompts para tareas específicas y modos de chat para controlar el contexto de interacción.

### Instrucciones Personalizadas

Instrucciones específicas de equipo y proyecto para mejorar el comportamiento de asistentes de IA como GitHub Copilot y Amazon Q Developer para tecnologías específicas y prácticas de programación:

#### Por Chapter - Instrucciones

| Chapter | Descripción |
| -------- | ----------- |
| [📱 Frontend](instructions/frontend/) | Instrucciones para desarrollo frontend (React, Angular, Vue, etc.) |
| [⚙️ Backend](instructions/backend/) | Instrucciones para desarrollo backend (APIs, bases de datos, etc.) |
| [📲 Mobile](instructions/mobile/) | Instrucciones para desarrollo móvil (React Native, Flutter, etc.) |
| [🚀 DevOps](instructions/devops/) | Instrucciones para DevOps e infraestructura |
| [🧪 QA & Testing](instructions/qa-testing/) | Instrucciones para testing y quality assurance |
| [🔄 Transversal](instructions/transversal/) | Instrucciones transversales aplicables a múltiples áreas |

#### Configuración en Instrucciones Personalizadas

> 💡 **Uso en GitHub Copilot**: GitHub Copilot soporta varios tipos de instrucciones personalizadas:
>
> - **Repository-wide**: Archivo `.github/copilot-instructions.md` que aplica a todo el repositorio
> - **Path-specific**: Archivos `.github/instructions/NOMBRE.instructions.md` con frontmatter para paths específicos
>
> Las instrucciones se aplican automáticamente al Chat, Code Review y Copilot Coding Agent. Para más detalles, consulta la [documentación oficial de Custom Instructions](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions)

> 💡 **Uso en Amazon Q**: Utiliza estas instrucciones como "Project Rules" creando archivos `.md` en la carpeta `.amazonq/rules/` de tu proyecto. Amazon Q las aplicará automáticamente como contexto en todas las conversaciones del equipo. Puedes crear las reglas usando el botón "Rules" en el chat de Amazon Q o manualmente en el sistema de archivos. Para más detalles, consulta la [documentación oficial de Project Rules](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/context-project-rules.html).

### Prompts Reutilizables

Plantillas de prompts listas para usar para escenarios de desarrollo específicos y tareas, definiendo texto de prompt con un modo específico, modelo y conjunto de herramientas disponibles.

#### Por Chapter - Prompts

| Chapter | Descripción |
| -------- | ----------- |
| [📱 Frontend](prompts/frontend/) | Prompts para desarrollo frontend (React, Angular, Vue, etc.) |
| [⚙️ Backend](prompts/backend/) | Prompts para desarrollo backend (APIs, bases de datos, etc.) |
| [📲 Mobile](prompts/mobile/) | Prompts para desarrollo móvil (React Native, Flutter, etc.) |
| [🚀 DevOps](prompts/devops/) | Prompts para DevOps e infraestructura |
| [🧪 QA & Testing](prompts/qa-testing/) | Prompts para testing y quality assurance |
| [🔄 Transversal](prompts/transversal/) | Prompts transversales aplicables a múltiples áreas |

#### Configuración en Prompts Reutilizables

> 💡 **Uso en GitHub Copilot**: Usa `/nombre-del-prompt` en el chat de VS Code o presiona el botón ejecutar mientras tienes un prompt abierto. Para más detalles, consulta la [documentación oficial de Prompt Files](https://docs.github.com/en/copilot/concepts/prompting/response-customization#about-prompt-files) y [VS Code Prompt Files](https://code.visualstudio.com/docs/copilot/copilot-customization#_reusable-prompt-files-experimental)

> 💡 **Uso en Amazon Q Developer**: Guarda estos prompts en tu biblioteca personal usando `@Prompts > Create a new prompt` en el chat de Amazon Q. Los prompts se almacenan en `~/.aws/amazonq/prompts/` y pueden reutilizarse con `@nombre-del-prompt` en cualquier conversación. Para más detalles, consulta la [documentación oficial de Prompt Library](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/context-prompt-library.html).

### Modos de Chat Personalizados en GitHub Copilot

Los modos de chat personalizados definen comportamientos específicos y herramientas para GitHub Copilot Chat, permitiendo asistencia mejorada consciente del contexto para tareas o flujos de trabajo particulares.

#### Por Chapter - Chat Modes

| Chapter | Descripción |
| -------- | ----------- |
| [📱 Frontend](chatmodes/frontend/) | Chat modes para desarrollo frontend (React, Angular, Vue, etc.) |
| [⚙️ Backend](chatmodes/backend/) | Chat modes para desarrollo backend (APIs, bases de datos, etc.) |
| [📲 Mobile](chatmodes/mobile/) | Chat modes para desarrollo móvil (React Native, Flutter, etc.) |
| [🚀 DevOps](chatmodes/devops/) | Chat modes para DevOps e infraestructura |
| [🧪 QA & Testing](chatmodes/qa-testing/) | Chat modes para testing y quality assurance |
| [🔄 Transversal](chatmodes/transversal/) | Chat modes transversales aplicables a múltiples áreas |

#### Ejemplos Disponibles - Chat Modes

| Título | Descripción |
| ------ | ----------- |
| [Ejemplo de Chatmode](chatmodes/example.chatmode.md) | Pendiente por implementar. |

> 💡 **Uso**: Crea nuevos modos de chat usando el comando `Chat: Configure Chat Modes...`, luego cambia tu modo de chat en la entrada de Chat de _Agent_ o _Ask_ a tu propio modo.

---

## 📚 Recursos Adicionales

- [Documentación de Personalización de VS Code Copilot](https://code.visualstudio.com/docs/copilot/copilot-customization) - Documentación oficial de Microsoft
- [Documentación de GitHub Copilot Chat](https://code.visualstudio.com/docs/copilot/chat/copilot-chat) - Guía completa de funciones de chat
- [Modos de Chat Personalizados](https://code.visualstudio.com/docs/copilot/chat/chat-modes) - Configuración avanzada de chat
- [Configuración de VS Code](https://code.visualstudio.com/docs/getstarted/settings) - Guía de configuración general de VS Code
- [Cheat Sheet Copilot | VS Code](https://code.visualstudio.com/docs/copilot/reference/copilot-vscode-features) - Tips y uso de Github Copilot en VS Code
- [Windsurf AI IDE Documentation](https://docs.windsurf.com/windsurf/cascade/memories) - Límites técnicos específicos

## 🤖 Secciones Adicionales

> Por definir...
