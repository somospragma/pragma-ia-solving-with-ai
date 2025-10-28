# Parámetros de los Servidores MCP

Este documento describe los parámetros de configuración de los servidores MCP para DevSecOps/SREs, organizados por categorías para facilitar la navegación y configuración.

---

## 1. Análisis de Código y Calidad

### Sonarqube Cloud
**Descripción**: Servidor MCP para integración con SonarQube Cloud, permite análisis de calidad de código y seguridad.

| Parámetro | Valor |
|-----------|-------|
| Command | `docker` |
| Args | `["run", "-i", "--rm", "-e", "SONARQUBE_TOKEN", "-e", "SONARQUBE_ORG", "mcp/sonarqube"]` |
| Env | `SONARQUBE_TOKEN: <YourSonarQubeToken>`, `SONARQUBE_ORG: <YourOrganizationName>` |

### Sonarqube Server
**Descripción**: Servidor MCP para integración con instancias locales de SonarQube Server.

| Parámetro | Valor |
|-----------|-------|
| Command | `docker` |
| Args | `["run", "-i", "--rm", "-e", "SONARQUBE_TOKEN", "-e", "SONARQUBE_URL", "mcp/sonarqube"]` |
| Env | `SONARQUBE_TOKEN: <YourSonarQubeUserToken>`, `SONARQUBE_URL: <YourSonarQubeURL>` |

---

## 2. Servicios en la Nube - AWS

### aws-api
**Descripción**: Proporciona acceso directo a la API de AWS para consultas y operaciones.

| Parámetro | Valor |
|-----------|-------|
| Command | `uvx` |
| Args | `["awslabs.aws-api-mcp-server@latest"]` |
| Env | `FASTMCP_LOG_LEVEL: ERROR` |

### aws-knowledge
**Descripción**: Acceso a documentación y conocimientos de AWS.

| Parámetro | Valor |
|-----------|-------|
| Command | `uvx` |
| Args | `["awslabs.aws-knowledge-mcp-server@latest"]` |
| Env | `FASTMCP_LOG_LEVEL: ERROR`, `AWS_DOCUMENTATION_PARTITION: aws` |

### aws-cdk
**Descripción**: Soporte para AWS CDK (Cloud Development Kit).

| Parámetro | Valor |
|-----------|-------|
| Command | `uvx` |
| Args | `["awslabs.cdk-mcp-server@latest"]` |
| Env | `FASTMCP_LOG_LEVEL: ERROR` |

### aws-cloudformation
**Descripción**: Integración con AWS CloudFormation para plantillas de infraestructura.

| Parámetro | Valor |
|-----------|-------|
| Command | `uvx` |
| Args | `["awslabs.cfn-mcp-server@latest"]` |
| Env | `FASTMCP_LOG_LEVEL: ERROR` |

### aws-terraform
**Descripción**: Soporte para Terraform en entornos AWS.

| Parámetro | Valor |
|-----------|-------|
| Command | `uvx` |
| Args | `["awslabs.terraform-mcp-server@latest"]` |
| Env | `FASTMCP_LOG_LEVEL: ERROR` |

### aws-pricing
**Descripción**: Acceso a información de precios de AWS.

| Parámetro | Valor |
|-----------|-------|
| Command | `uvx` |
| Args | `["awslabs.aws-pricing-mcp-server@latest"]` |
| Env | `FASTMCP_LOG_LEVEL: ERROR` |

### aws-diagram
**Descripción**: Generación de diagramas para arquitecturas AWS.

| Parámetro | Valor |
|-----------|-------|
| Command | `uvx` |
| Args | `["awslabs.aws-diagram-mcp-server@latest"]` |
| Env | `FASTMCP_LOG_LEVEL: ERROR` |

### awslabs.iam-mcp-server
**Descripción**: Gestión de IAM (Identity and Access Management) en AWS.

| Parámetro | Valor |
|-----------|-------|
| Command | `uvx` |
| Args | `["awslabs.iam-mcp-server@latest"]` |
| Env | `AWS_PROFILE: your-aws-profile`, `AWS_REGION: us-east-1`, `FASTMCP_LOG_LEVEL: ERROR` |

### eks
**Descripción**: Soporte para Amazon EKS (Elastic Kubernetes Service).

| Parámetro | Valor |
|-----------|-------|
| Command | `uvx` |
| Args | `["awslabs.eks-mcp-server@latest"]` |
| Env | `FASTMCP_LOG_LEVEL: ERROR` |

### ecs
**Descripción**: Soporte para Amazon ECS (Elastic Container Service).

| Parámetro | Valor |
|-----------|-------|
| Command | `uvx` |
| Args | `["awslabs.ecs-mcp-server@latest"]` |
| Env | `FASTMCP_LOG_LEVEL: ERROR` |

### awslabs.code-doc-gen-mcp-server
**Descripción**: Generación automática de documentación de código.

| Parámetro | Valor |
|-----------|-------|
| Disabled | `false` |
| Timeout | `60` |
| Type | `stdio` |
| Command | `uv` |
| Args | `["tool", "run", "--from", "awslabs.code-doc-gen-mcp-server@latest", "awslabs.code-doc-gen-mcp-server.exe"]` |
| Env | `FASTMCP_LOG_LEVEL: ERROR`, `AWS_PROFILE: your-aws-profile`, `AWS_REGION: us-east-1` |

### awslabs.aws-diagram-mcp-server
**Descripción**: Servidor adicional para diagramas AWS.

| Parámetro | Valor |
|-----------|-------|
| Command | `uvx` |
| Args | `["awslabs.aws-diagram-mcp-server"]` |
| Env | `FASTMCP_LOG_LEVEL: ERROR` |
| AutoApprove | `[]` |
| Disabled | `false` |

---

---

## 4. Seguridad y Escaneo

### Trivy MCP
**Descripción**: Escaneo de vulnerabilidades y seguridad con Trivy.

| Parámetro | Valor |
|-----------|-------|
| Command | `trivy` |
| Args | `["mcp"]` |

---

## 3. Servicios en la Nube - Azure

### Azure Devops
**Descripción**: Integración con Azure DevOps para gestión de proyectos y CI/CD.

| Parámetro | Valor |
|-----------|-------|
| Type | `stdio` |
| Command | `npx` |
| Args | `["-y", "@azure-devops/mcp@next", "${input:ado_org}"]` |

**Inputs**:
- `ado_org`: Azure DevOps organization name (e.g. 'contoso') - promptString


---

### azure/azure-mcp
**Descripción**: Servidor MCP completo para servicios de Azure.

| Parámetro | Valor |
|-----------|-------|
| Type | `stdio` |
| Command | `npx` |
| Args | `["-y", "@azure/mcp@latest", "server", "start"]` |
| Env | `AZURE_TENANT_ID: ${input:azure_tenant_id}`, `AZURE_CLIENT_ID: ${input:azure_client_id}`, `AZURE_CLIENT_SECRET: ${input:azure_client_secret}`, `AZURE_SUBSCRIPTION_ID: ${input:azure_subscription_id}`, `AZURE_MCP_COLLECT_TELEMETRY: ${input:azure_mcp_collect_telemetry}` |
| Gallery | `https://api.mcp.github.com/2025-09-15/v0/servers/6cf2c8d0-6872-406b-bdeb-495272df709d` |
| Version | `1.0.0` |

**Inputs** (múltiples):
- `codacy_account_token`: Codacy Account Token for API access - promptString (password)
- `memory_file_path`: Path to the memory storage file (optional) - promptString
- `tfe_token`: Terraform API Token - promptString (password)
- `tfe_hostname`: Terraform hostname - promptString
- `azure_tenant_id`: Tenant ID (for service principal / workload identity auth) - promptString
- `azure_client_id`: Client ID (service principal or managed identity) - promptString
- `azure_client_secret`: Client secret (if using service principal secret) - promptString (password)
- `azure_subscription_id`: Optional: prefer a specific subscription by default - promptString
- `azure_mcp_collect_telemetry`: Set to 'false' to opt out of telemetry (default is true) - promptString

---

---

## 5. Infraestructura como Código

### hashicorp/terraform-mcp-server
**Descripción**: Soporte para Terraform Enterprise/Cloud.

| Parámetro | Valor |
|-----------|-------|
| Type | `stdio` |
| Command | `docker` |
| Args | `["run", "-i", "--rm", "run", "-i", "--rm", "-e", "TFE_TOKEN=${input:tfe_token}", "-e", "TFE_HOSTNAME=${input:tfe_hostname}", "hashicorp/terraform-mcp-server", "hashicorp/terraform-mcp-server:latest"]` |
| Gallery | `https://api.mcp.github.com/2025-09-15/v0/servers/34cd3839-461a-404a-a290-3d3bc9d8bee3` |
| Version | `1.0.0` |

---

## 6. Control de Versiones y Colaboración

### github
**Descripción**: Integración con GitHub para gestión de repositorios y colaboración.

| Parámetro | Valor |
|-----------|-------|
| Type | `http` |
| Url | `https://api.githubcopilot.com/mcp/` |
| Headers | `Authorization: Bearer ${input:github_mcp_pat}` |

**Inputs**:
- `github_mcp_pat`: GitHub Personal Access Token - promptString (password)

---

## Guías de Configuración en Agentes

- [Amazon Q Developer](https://alejandria.pragma.co/es/private/conocimiento-aplicado/inteligencia-artificial/kc-cc/mcp/pragma-mcps/amazon-q-developer)
- [Copilot](https://alejandria.pragma.co/es/private/conocimiento-aplicado/inteligencia-artificial/kc-cc/mcp/pragma-mcps/copilot)
- [SonarQube MCP Server](https://docs.sonarsource.com/sonarqube-for-vs-code/ai-capabilities/sonarqube-mcp-server?_gl=1*1bhxjqx*_gcl_au*MTUyOTA1ODUzNy4xNzU4MzA5ODc1*_ga*Nzc3NTEwMDU2LjE3MjY4NDQyMDg.*_ga_9JZ0GZ5TC6*czE3NjE2NjIxMDAkbzQ1JGcxJHQxNzYxNjYyMTA3JGo1NSRsMCRoMA)
- [AWS MCPs Server](https://github.com/awslabs/mcp?tab=readme-ov-file#infrastructure-as-code)
- [Trivy MCPs Server](https://github.com/aquasecurity/trivy-mcp/tree/main)
- [Azure Devops MCP Server](https://github.com/microsoft/azure-devops-mcp)
- [Azure Cloud MCP Server](https://github.com/microsoft/mcp/tree/main/servers/Azure.Mcp.Server)
- [Terraforms MCP Server](https://github.com/hashicorp/terraform-mcp-server)
- [GitHub MCP Server](https://github.com/github/github-mcp-server)

---

## Contribuciones e Historial de Versiones
| Versión | Área                    | Participantes                          | Fecha      | Comentario                                                                 |
|---------|--------------------------|----------------------------------------|------------|-----------------------------------------------------------------------------|
| 1.0.0   | Lider Chapter - DevSecOps  | Cristian Correa - Jhon Quevedo | 10/28/2025 | Se crea artefacto Template Markdown. |