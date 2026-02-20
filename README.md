# pragma-ia-solving-with-ai

Repositorio que busca centralizar distintos artefactos de IA, como: Instructions, Prompts y Agents.

## 🚀 Guía de Inicio Rápido

1. **🤖 Revisa la [Comparativa GitHub Copilot vs Amazon Q](https://alejandria.pragma.co/es/private/conocimiento-aplicado/inteligencia-artificial/kc-cc/gen-ai/asistentes-code/amazonq-vs-copilot)**, si quieres entender cuál es la herramienta de IA más adecuada para tu proyecto
2. **📋 Revisa el [Estándar de Instrucciones](https://alejandria.pragma.co/es/private/conocimiento-aplicado/inteligencia-artificial/kc-cc/gen-ai/asistentes-code/estandar-instrucciones)**, si quieres entender cómo se crearon las instrucciones efectivas para agentes de IA disponibilizadas en este repositorio
3. **🎯 Explora las [Funcionalidades de Personalización](#funcionalidades-de-personalización-de-los-agentes)** para transformar tu experiencia con agentes de IA

---

## Estructura del Repositorio

```plaintext
📁 .github/agents/  → Agentes de chat personalizados
📁 instructions/    → Instrucciones personalizadas por chapter y estándares
📁 prompts/         → Prompts reutilizables para tareas específicas  
📄 CONTRIBUTING.md  → Guía para contribuir al repositorio
```

## 📝 Contribuir

¡Las contribuciones son bienvenidas! Consulta nuestra [Guía de Contribución](./CONTRIBUTING.md) para obtener detalles sobre cómo enviar nuevas instrucciones y prompts.
> Guía de contribución por definir.

---

## Funcionalidades de Personalización de los Agentes

Actualmente, los Agentes ofrecen diversas formas para personalizar la asistencia de la Inteligencia Artificial, entre esas destacan:

| **📋 [Instrucciones Personalizadas](#instrucciones-personalizadas)** | **🎯 [Prompts Reutilizables](#prompts-reutilizables)** | **🤖 [Agentes de Chat (SOLO Copilot)](#agentes-de-chat-personalizados-en-github-copilot)** |
| --- | --- | --- |
| Define pautas comunes para tareas como generación de código, revisiones y mensajes de commit. Describe _cómo_ deben realizarse las tareas. | Crea prompts reutilizables e independientes para tareas específicas. Describe _qué_ debe hacerse con pautas opcionales específicas de la tarea. | Define el comportamiento del agente, contexto precargado, herramientas disponibles y patrones de interacción con el código base especializado para dominios particulares. |

> **💡 Pro Tip:** Las instrucciones personalizadas solo afectan al Chat (no a las completaciones de código en línea). Puedes combinar los tres tipos de personalización: usa instrucciones personalizadas para pautas generales, archivos de prompts para tareas específicas y agentes de chat para controlar el contexto de interacción especializado.

### Instrucciones Personalizadas

Instrucciones específicas de equipo y proyecto para mejorar el comportamiento de asistentes de IA como GitHub Copilot y Amazon Q Developer para tecnologías específicas y prácticas de programación:

#### Por Chapter - Instrucciones

| Chapter | Descripción |
| -------- | ----------- |
| [📱 Frontend](instructions/frontend/) | Instrucciones para desarrollo frontend (React, Angular, Vue, etc.) |
| [⚙️ Backend](instructions/backend/) | Instrucciones para desarrollo backend (APIs, bases de datos, etc.) |
| [📲 Mobile](instructions/mobile/) | Instrucciones para desarrollo móvil (React Native, Flutter, etc.) |
| [� Data Engineering](instructions_or_rules/data-engineering/) | Instrucciones para pipelines de datos, ingesta, calidad, operación |
| [�🚀 DevOps](instructions/devops/) | Instrucciones para DevOps e infraestructura |
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
| [� Data Engineering](prompts/data-engineering/) | Prompts para validación de pipelines, calidad de datos, performance |
| [�🚀 DevOps](prompts/devops/) | Prompts para DevOps e infraestructura |
| [🧪 QA & Testing](prompts/qa-testing/) | Prompts para testing y quality assurance |
| [🔄 Transversal](prompts/transversal/) | Prompts transversales aplicables a múltiples áreas |

#### Configuración en Prompts Reutilizables

> 💡 **Uso en GitHub Copilot**: Usa `/nombre-del-prompt` en el chat de VS Code o presiona el botón ejecutar mientras tienes un prompt abierto. Para más detalles, consulta la [documentación oficial de Prompt Files](https://docs.github.com/en/copilot/concepts/prompting/response-customization#about-prompt-files) y [VS Code Prompt Files](https://code.visualstudio.com/docs/copilot/copilot-customization#_reusable-prompt-files-experimental)

> 💡 **Uso en Amazon Q Developer**: Guarda estos prompts en tu biblioteca personal usando `@Prompts > Create a new prompt` en el chat de Amazon Q. Los prompts se almacenan en `~/.aws/amazonq/prompts/` y pueden reutilizarse con `@nombre-del-prompt` en cualquier conversación. Para más detalles, consulta la [documentación oficial de Prompt Library](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/context-prompt-library.html).

### Agentes de Chat Personalizados en GitHub Copilot

Los modos de chat personalizados definen comportamientos específicos y herramientas para GitHub Copilot Chat, permitiendo asistencia mejorada consciente del contexto para tareas o flujos de trabajo particulares.

#### Por Chapter - Chat Modes

| Chapter | Descripción |
| -------- | ----------- |
| [📱 Frontend](.github/agents/frontend.agent.md) | Chat modes para desarrollo frontend (React, Angular, Vue, etc.) |
| [⚙️ Backend](.github/agents/backend.agent.md) | Chat modes para desarrollo backend (APIs, bases de datos, etc.) |
| [📲 Mobile](.github/agents/mobile.agent.md) | Chat modes para desarrollo móvil (React Native, Flutter, etc.) |
| [📦 Data Engineering](.github/agents/data-engineering.agent.md) | Agente especializado para Data Engineering: pipelines Airflow/MWAA, Glue ETL, validación de datos, troubleshooting operacional |
| [🚀 DevOps](.github/agents/devops.agent.md) | Chat modes para DevOps e infraestructura |
| [🧪 QA & Testing](.github/agents/qa-testing.agent.md) | Chat modes para testing y quality assurance |
| [🔄 Transversal](.github/agents/transversal.agent.md) | Chat modes transversales aplicables a múltiples áreas |

#### Ejemplos Disponibles - Chat Modes

##### Data Engineering Agent

| Capacidad | Descripción |
| --------- | ----------- |
| **Validación de Pipelines** | Analiza idempotencia, contratos de datos y observabilidad en configuraciones Airflow/Glue |
| **Triage de Incidentes** | Diagnostica problemas operacionales: datos no llegados, schema drift, degradación de performance |
| **Diseño de DAGs** | Revisa estructura, operadores, manejo de XCom, retries, alertas, seguridad y observabilidad en Airflow |
| **Optimización de Performance** | Identifica skew de datos, particionado, tuning de recursos en pipelines Spark/Glue |
| **Troubleshooting de Jobs ETL** | Diagnóstico estructurado de jobs colgados, timeouts, OOM, state management (AWS Glue, Azure Synapse, Data Factory) |
| **Diseño de Data Contracts** | Especificación de SLAs, versionado de schema, definición de expectations de calidad |
| **Revisión de Calidad de Datos** | Validación con Great Expectations, detección de anomalías, completitud y distribución |

##### Otros Agentes

| Título | Descripción |
| ------ | ----------- |
| [Ejemplo de Chatmode](.github/agents/example.agent.md) | Pendiente por implementar. |

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

### Data Engineering: Sistema Completo de Pipelines de Datos

El framework de **Data Engineering** ofrece cobertura integral para el diseño, validación y operación de pipelines de datos en arquitecturas cloud (AWS/Azure):

**Instrucciones Especializadas:**
- Contexto de datos, guidelines de diseño (SOLID, testing, performance)
- Stack tecnológico (Kafka, Spark, Glue, Airflow/MWAA, Flink, dbt)
- Estrategia de calidad y testing
- Operación en cloud (IaC, CI/CD, runbooks operacionales)
- Consideraciones específicas para Airflow y despliegue en MWAA

**Prompts de Validación y Optimización:**
- Validación de idempotencia, contratos de datos y observabilidad
- Triage de incidentes en pipelines
- Optimización de performance (skew, particionado, resource tuning)
- Diseño de DAGs en Airflow y troubleshooting operacional
- Triage conceptual de problemas (timeouts, OOM, state management)
- Diseño de data contracts con versionado y SLAs
- Revisión de calidad de datos con Great Expectations

**Recursos de Referencia:**
- Patrones de arquitectura de datos (medallion, lambda vs kappa)
- Mejores prácticas de Airflow y testing
- Patrones de Glue jobs con configuración dinámica (YAML-based)
- Comparativa AWS/Azure con costos y equivalencias
- Testing strategies para pipelines

**Validación y Escenarios:**
- Cobertura completa de escenarios reales: desde "Primer DAG" hasta troubleshooting de jobs colgados
- Agnósticidad: Recomendaciones sin prescripciones inflexibles, adaptables a cualquier contexto
- Integración con repositorios externos (operadores, patrones de carga)
