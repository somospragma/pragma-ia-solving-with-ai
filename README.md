# pragma-ia-solving-with-ai

Repositorio que busca centralizar distintos artefactos de IA, como Instructions, Prompts, Chatmodes, Agents y demás activos base.

## 🚀 Guía de Inicio Rápido

### Para Nuevos Usuarios

1. **📋 Revisa los [Estándares de Instrucciones](#estándares-de-instrucciones-para-ia)** para entender cómo crear instrucciones efectivas para agentes de IA
2. **⚖️ Consulta los [Mínimos de Desarrollo](#mínimos-de-desarrollo)** para conocer los estándares de calidad requeridos
3. **🎯 Explora las [Funcionalidades de Personalización](#funcionalidades-de-personalización-de-los-agentes)** para personalizar tu experiencia con agentes de IA
4. **📁 Navega por las carpetas específicas** de tu chapter (Frontend, Backend, Mobile, DevOps, QA, Transversal)

### Estructura del Repositorio

```plaintext
📁 instructions/     → Instrucciones personalizadas por chapter y estándares
📁 prompts/         → Prompts reutilizables para tareas específicas  
📁 chatmodes/       → Modos de chat personalizados
📁 minimos_dev/     → Estándares mínimos de desarrollo por chapter
📄 CONTRIBUTING.md  → Guía para contribuir al repositorio
```

## Estándares de Instrucciones para IA

📖 **[Ver Estándares Completos](instructions/standard/README.MD)** - Guía detallada con:

- Limitaciones técnicas actualizadas (Septiembre 2025)
- Mejores prácticas de ingeniería de contexto  
- Plantillas unificadas y modulares

### Plantillas Disponibles

| Plantilla | Uso Recomendado |
|-----------|-----------------|
| [📄 Unificada](instructions/standard/instructions-template.md) | Proyectos con <12K caracteres de instrucciones |
| [🗂️ Modular](instructions/standard/instructions-orchestrator-template.md) | Casos complejos que requieren >12K caracteres |

## Mínimos de Desarrollo

Estándares mínimos que deben cumplir todos los proyectos para garantizar calidad, mantenibilidad y seguridad del código.

### Por Chapter

| Chapter | Estándares Disponibles |
|---------|----------------------|
| 📱 Frontend | [Mínimos Frontend](minimos_dev/minimos_frontend.md) |
| ⚙️ Backend | _Por definir_ |
| 📲 Mobile | _Por definir_ |
| 🚀 DevOps | _Por definir_ |
| 🧪 QA & Testing | _Por definir_ |

> 💡 **Integración**: Los mínimos de desarrollo deben implementarse junto con los estándares de instrucciones para optimizar la asistencia de IA en cada project.

## Funcionalidades de Personalización de los Agentes

Actualmente, muchos Agentes ofrecen 3 formas principales para personalizar la asistencia de la Inteligencia Artificial:

| **📋 [Instrucciones Personalizadas](#instrucciones-personalizadas)** | **🎯 [Prompts Reutilizables](#prompts-reutilizables)** | **🧩 [Modos de Chat Personalizados](#modos-de-chat-personalizados-en-github-copilot)** |
| --- | --- | --- |
| Define pautas comunes para tareas como generación de código, revisiones y mensajes de commit. Describe _cómo_ deben realizarse las tareas. | Crea prompts reutilizables e independientes para tareas específicas. Describe _qué_ debe hacerse con pautas opcionales específicas de la tarea. | Define el comportamiento del chat, herramientas disponibles y patrones de interacción con el código base dentro de límites específicos para cada solicitud. |

> **💡 Pro Tip:** Las instrucciones personalizadas solo afectan a Copilot Chat (no a las completaciones de código en línea). Puedes combinar los tres tipos de personalización: usa instrucciones personalizadas para pautas generales, archivos de prompts para tareas específicas y modos de chat para controlar el contexto de interacción.

## 📝 Contribuir

¡Las contribuciones son bienvenidas! Consulta nuestra [Guía de Contribución](./CONTRIBUTING.md) para obtener detalles sobre cómo enviar nuevas instrucciones y prompts.
> Guía de contribución por definir.

## Instrucciones Personalizadas

Instrucciones específicas de equipo y proyecto para mejorar el comportamiento de GitHub Copilot para tecnologías específicas y prácticas de programación:

### Por Chapter - Instrucciones

| Chapter | Descripción |
| -------- | ----------- |
| [📱 Frontend](instructions/frontend/) | Instrucciones para desarrollo frontend (React, Angular, Vue, etc.) |
| [⚙️ Backend](instructions/backend/) | Instrucciones para desarrollo backend (APIs, bases de datos, etc.) |
| [📲 Mobile](instructions/mobile/) | Instrucciones para desarrollo móvil (React Native, Flutter, etc.) |
| [🚀 DevOps](instructions/devops/) | Instrucciones para DevOps e infraestructura |
| [🧪 QA & Testing](instructions/qa-testing/) | Instrucciones para testing y quality assurance |
| [🔄 Transversal](instructions/transversal/) | Instrucciones transversales aplicables a múltiples áreas |

> 💡 **Uso en Copilot**: Copia estas instrucciones a tu archivo `.github/copilot-instructions.md` o crea archivos `.github/.instructions.md` específicos para tareas en la carpeta `.github/instructions` de tu espacio de trabajo.

## Prompts Reutilizables

Plantillas de prompts listas para usar para escenarios de desarrollo específicos y tareas, definiendo texto de prompt con un modo específico, modelo y conjunto de herramientas disponibles.

### Por Chapter - Prompts

| Chapter | Descripción |
| -------- | ----------- |
| [📱 Frontend](prompts/frontend/) | Prompts para desarrollo frontend (React, Angular, Vue, etc.) |
| [⚙️ Backend](prompts/backend/) | Prompts para desarrollo backend (APIs, bases de datos, etc.) |
| [📲 Mobile](prompts/mobile/) | Prompts para desarrollo móvil (React Native, Flutter, etc.) |
| [🚀 DevOps](prompts/devops/) | Prompts para DevOps e infraestructura |
| [🧪 QA & Testing](prompts/qa-testing/) | Prompts para testing y quality assurance |
| [🔄 Transversal](prompts/transversal/) | Prompts transversales aplicables a múltiples áreas |

### Ejemplos Disponibles - Prompts

| Título | Descripción |
| ------ | ----------- |
| [Ejemplo de Prompts de IA](prompts/example.prompt.md) | Pendiente por implementar. |

> 💡 **Uso con Copilot**: Usa `/nombre-del-prompt` en el chat de VS Code, ejecuta el comando `Chat: Run Prompt`, o presiona el botón ejecutar mientras tienes un prompt abierto.

## Modos de Chat Personalizados en GitHub Copilot

Los modos de chat personalizados definen comportamientos específicos y herramientas para GitHub Copilot Chat, permitiendo asistencia mejorada consciente del contexto para tareas o flujos de trabajo particulares.

### Por Chapter - Chat Modes

| Chapter | Descripción |
| -------- | ----------- |
| [📱 Frontend](chatmodes/frontend/) | Chat modes para desarrollo frontend (React, Angular, Vue, etc.) |
| [⚙️ Backend](chatmodes/backend/) | Chat modes para desarrollo backend (APIs, bases de datos, etc.) |
| [📲 Mobile](chatmodes/mobile/) | Chat modes para desarrollo móvil (React Native, Flutter, etc.) |
| [🚀 DevOps](chatmodes/devops/) | Chat modes para DevOps e infraestructura |
| [🧪 QA & Testing](chatmodes/qa-testing/) | Chat modes para testing y quality assurance |
| [🔄 Transversal](chatmodes/transversal/) | Chat modes transversales aplicables a múltiples áreas |

### Ejemplos Disponibles - Chat Modes

| Título | Descripción |
| ------ | ----------- |
| [Ejemplo de Chatmode](chatmodes/example.chatmode.md) | Pendiente por implementar. |

> 💡 **Uso**: Crea nuevos modos de chat usando el comando `Chat: Configure Chat Modes...`, luego cambia tu modo de chat en la entrada de Chat de _Agent_ o _Ask_ a tu propio modo.

## 📚 Recursos Adicionales

- [Documentación de Personalización de VS Code Copilot](https://code.visualstudio.com/docs/copilot/copilot-customization) - Documentación oficial de Microsoft
- [Documentación de GitHub Copilot Chat](https://code.visualstudio.com/docs/copilot/chat/copilot-chat) - Guía completa de funciones de chat
- [Modos de Chat Personalizados](https://code.visualstudio.com/docs/copilot/chat/chat-modes) - Configuración avanzada de chat
- [Configuración de VS Code](https://code.visualstudio.com/docs/getstarted/settings) - Guía de configuración general de VS Code
- [Cheat Sheet Copilot | VS Code](https://code.visualstudio.com/docs/copilot/reference/copilot-vscode-features) - Tips y uso de Github Copilot en VS Code
- [Documentación de Anthropic Claude](https://docs.anthropic.com/en/docs/about-claude/models) - Información sobre modelos y limitaciones
- [Windsurf AI IDE Documentation](https://docs.windsurf.com/windsurf/cascade/memories) - Límites técnicos específicos

## 🤖 Secciones Adicionales

> Por definir...
