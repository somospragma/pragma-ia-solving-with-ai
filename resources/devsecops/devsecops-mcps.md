# Servidores MCP DevSecOps

Este documento describe los parámetros de configuración de los servidores MCP para DevSecOps/SREs, organizados por categorías para facilitar la navegación y configuración.


<br>

---
<br>

## 1. Servicios Devops

### Azure Devops
**Descripción**: Integración con Azure DevOps para gestión de proyectos y CI/CD.
**Prerequisitos**: Perfil de usuario con permisos de administrador en la Organizacion de  Azure DevOps preferiblemente.

| Parámetro | Valor |
|-----------|-------|
| Type | `stdio` |
| Command | `npx` |
| Args | `["-y", "@azure-devops/mcp@next", "organization_name"` |
[Azure Devops MCP Server](https://github.com/microsoft/azure-devops-mcp)

**Inputs**:
- `organization_name`: Azure DevOps organization name

---

### github
**Descripción**: Integración con GitHub para gestión de repositorios y colaboración.

| Parámetro | Valor |
|-----------|-------|
| Type | `http` |
| Url | `https://api.githubcopilot.com/mcp/` |

---

<br>

## 2. Seguridad y Escaneo

### Trivy MCP
**Descripción**: Escaneo de vulnerabilidades y seguridad con Trivy.
**Prerequisitos**:
1. Trivy debe estar instalado en tu sistema operativo

    **Windows**
	
- Descarga el archivo `trivy_x.xx.x_windows-64bit.zip` desde la página de [releases](https://github.com/aquasecurity/trivy/releases/).
	
- Descomprime el archivo y cópialo en cualquier carpeta.

    **Linux**
- Descarga el archivo binario adecuado para tu distribución desde la página de [releases](https://github.com/aquasecurity/trivy/releases/)
- Descomprime el archivo y mueve el binario a una ubicación en tu PATH, por ejemplo: `/usr/local/bin`
- Asegúrate de que el binario tenga permisos de ejecución: `chmod +x /usr/local/bin/trivy`

    **Mac**
- Usa Homebrew para instalar Trivy ejecutando: `brew install aquasecurity/trivy/trivy`

2. **Crea la variable de entorno**

3. Instalación del Plugin MCP:
	- Usa el sistema de gestión de plugins integrado de Trivy para instalar el plugin MCP:
	- Ejecuta: `trivy plugin install mcp`
	- Este comando instalará la última versión del plugin MCP de Trivy.

4. Optimización de VS Code para escaneo de seguridad:
	- Para aprovechar al máximo Trivy MCP en VS Code, puedes agregar sugerencias para ejecutar Trivy en los momentos adecuados:

	**Usa archivos de instrucciones personalizados**

	Crea un archivo en el workspace `Add Context... (Parte superior izquierda del chat copilot) -> Instructions... -> Configure Instructions -> + New Instructions File... -> .gitHub/intructions -> trivy -> Enter ` con el siguiente contenido json y valida que siempre se adjunte.

	```markdown
	---
	applyTo: '**'
	---
	
	# Trivy Security Scanning Instructions
	After making changes to packages or manifest files, scan for security vulnerabilities.
	Fixes should only be according to the desired version reported by the scanner. If the scanner reports a fix unrelated to our change, ignore it.
	After performing the fix, scan the project for security vulnerabilities again.
	If changes are made to infrastructure as code files such as Terraform, CloudFormation, Kubernetes manifests, Dockerfiles etc, run a scan for security vulnerabilities and misconfigurations.
	Fixes should only be according to the desired version reported by the scanner. If the scanner reports a fix unrelated to our change, ignore it.
	After performing the fix, scan the project for security vulnerabilities and misconfigurations again.
	```


Más información: [VS Code Copilot Custom Instructions](https://aka.ms/vscode-ghcp-custom-instructions)


| Parámetro | Valor |
|-----------|-------|
| Command | `Path donde se descomprimio trivy.exe` |
| Args | `["mcp"]` |
[Trivy MCPs Server](https://github.com/aquasecurity/trivy-mcp/tree/main)

---
<br>

## 3. Análisis de Código y Calidad

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
[SonarQube MCP Server](https://docs.sonarsource.com/sonarqube-for-vs-code/ai-capabilities/sonarqube-mcp-server?_gl=1*1bhxjqx*_gcl_au*MTUyOTA1ODUzNy4xNzU4MzA5ODc1*_ga*Nzc3NTEwMDU2LjE3MjY4NDQyMDg.*_ga_9JZ0GZ5TC6*czE3NjE2NjIxMDAkbzQ1JGcxJHQxNzYxNjYyMTA3JGo1NSRsMCRoMA)

---
<br>

## 4. Servicios en la Nube - AWS/Azure

### aws-api
**Descripción**: Proporciona acceso directo a la API de AWS para consultas y operaciones.
**Prerequisitos**: Perfil de AWS con credenciales y permisos para la acción `pricing:DescribeServices`.

| Parámetro | Valor |
|-----------|-------|
| Command | `uvx` |
| Args | `["awslabs.aws-api-mcp-server@latest"]` |
| Env | `FASTMCP_LOG_LEVEL: ERROR` |
[AWS MCPs Server](https://github.com/awslabs/mcp?tab=readme-ov-file#infrastructure-as-code)

### aws-knowledge
**Descripción**: Acceso a documentación y conocimientos de AWS.
**Prerequisitos**: Perfil de AWS con credenciales y permisos para la acción `pricing:DescribeServices`.

| Parámetro | Valor |
|-----------|-------|
| Command | `uvx` |
| Args | `["mcp-proxy", "--transport", "streamablehttp", "https://knowledge-mcp.global.api.aws"]` |
| Env | `FASTMCP_LOG_LEVEL: ERROR`, `AWS_DOCUMENTATION_PARTITION: aws` |
[AWS MCPs Server](https://github.com/awslabs/mcp?tab=readme-ov-file#infrastructure-as-code)

### aws-cdk
**Descripción**: Soporte para AWS CDK (Cloud Development Kit).
**Prerequisitos**: Perfil de AWS con credenciales y permisos para la acción `pricing:DescribeServices`.

| Parámetro | Valor |
|-----------|-------|
| Command | `uvx` |
| Args | `["awslabs.cdk-mcp-server@latest"]` |
| Env | `FASTMCP_LOG_LEVEL: ERROR` |
[AWS MCPs Server](https://github.com/awslabs/mcp?tab=readme-ov-file#infrastructure-as-code)

### aws-cloudformation
**Descripción**: Integración con AWS CloudFormation para plantillas de infraestructura.
**Prerequisitos**: Perfil de AWS con credenciales y permisos para la acción `pricing:DescribeServices`.

| Parámetro | Valor |
|-----------|-------|
| Command | `uvx` |
| Args | `["awslabs.cfn-mcp-server@latest"]` |
| Env | `FASTMCP_LOG_LEVEL: ERROR` |
[AWS MCPs Server](https://github.com/awslabs/mcp?tab=readme-ov-file#infrastructure-as-code)

### aws-terraform
**Descripción**: Soporte para Terraform en entornos AWS.
**Prerequisitos**: Perfil de AWS con credenciales y permisos para la acción `pricing:DescribeServices`.

| Parámetro | Valor |
|-----------|-------|
| Command | `uvx` |
| Args | `["awslabs.terraform-mcp-server@latest"]` |
| Env | `FASTMCP_LOG_LEVEL: ERROR` |
[AWS MCPs Server](https://github.com/awslabs/mcp?tab=readme-ov-file#infrastructure-as-code)

### aws-pricing
**Descripción**: Acceso a información de precios de AWS.
**Prerequisitos**: Perfil de AWS con credenciales y permisos para la acción `pricing:DescribeServices`.

| Parámetro | Valor |
|-----------|-------|
| Command | `uvx` |
| Args | `["--from", "awslabs.aws-pricing-mcp-server@latest", "awslabs.aws-pricing-mcp-server.exe"]` |
| Env | `FASTMCP_LOG_LEVEL: ERROR` |
[AWS MCPs Server](https://github.com/awslabs/mcp?tab=readme-ov-file#infrastructure-as-code)

### aws-diagram
**Descripción**: Generación de diagramas para arquitecturas AWS.
**Prerequisitos**: Perfil de AWS con credenciales y permisos para la acción `pricing:DescribeServices`.

| Parámetro | Valor |
|-----------|-------|
| Command | `uvx` |
| Args | `["awslabs.aws-diagram-mcp-server@latest"]` |
| Env | `FASTMCP_LOG_LEVEL: ERROR` |
[AWS MCPs Server](https://github.com/awslabs/mcp?tab=readme-ov-file#infrastructure-as-code)

### awslabs.iam-mcp-server
**Descripción**: Gestión de IAM (Identity and Access Management) en AWS.
**Prerequisitos**: Perfil de AWS con credenciales y permisos para la acción `pricing:DescribeServices`.

| Parámetro | Valor |
|-----------|-------|
| Command | `uvx` |
| Args | `["awslabs.iam-mcp-server@latest"]` |
| Env | `AWS_PROFILE: your-aws-profile`, `AWS_REGION: us-east-1`, `FASTMCP_LOG_LEVEL: ERROR` |
[AWS MCPs Server](https://github.com/awslabs/mcp?tab=readme-ov-file#infrastructure-as-code)

### eks
**Descripción**: Soporte para Amazon EKS (Elastic Kubernetes Service).
**Prerequisitos**: Perfil de AWS con credenciales y permisos para la acción `pricing:DescribeServices`.

| Parámetro | Valor |
|-----------|-------|
| Command | `uvx` |
| Args | `["awslabs.eks-mcp-server@latest"]` |
| Env | `FASTMCP_LOG_LEVEL: ERROR` |
[AWS MCPs Server](https://github.com/awslabs/mcp?tab=readme-ov-file#infrastructure-as-code)

### ecs
**Descripción**: Soporte para Amazon ECS (Elastic Container Service).
**Prerequisitos**: Perfil de AWS con credenciales y permisos para la acción `pricing:DescribeServices`.

| Parámetro | Valor |
|-----------|-------|
| Command | `uvx` |
| Args | `["awslabs.ecs-mcp-server@latest"]` |
| Env | `FASTMCP_LOG_LEVEL: ERROR` |
[AWS MCPs Server](https://github.com/awslabs/mcp?tab=readme-ov-file#infrastructure-as-code)

### awslabs.code-doc-gen-mcp-server
**Descripción**: Generación automática de documentación de código.
**Prerequisitos**: Perfil de AWS con credenciales y permisos para la acción `pricing:DescribeServices`.

| Parámetro | Valor |
|-----------|-------|
| Disabled | `false` |
| Timeout | `60` |
| Type | `stdio` |
| Command | `uv` |
| Args | `["tool", "run", "--from", "awslabs.code-doc-gen-mcp-server@latest", "awslabs.code-doc-gen-mcp-server.exe"]` |
| Env | `FASTMCP_LOG_LEVEL: ERROR`, `AWS_PROFILE: your-aws-profile`, `AWS_REGION: us-east-1` |
[AWS MCPs Server](https://github.com/awslabs/mcp?tab=readme-ov-file#infrastructure-as-code)

### awslabs.aws-diagram-mcp-server
**Descripción**: Servidor adicional para diagramas AWS.
**Prerequisitos**: Perfil de AWS con credenciales y permisos para la acción `pricing:DescribeServices`.

| Parámetro | Valor |
|-----------|-------|
| Command | `uvx` |
| Args | `["awslabs.aws-diagram-mcp-server"]` |
| Env | `FASTMCP_LOG_LEVEL: ERROR` |
| AutoApprove | `[]` |
| Disabled | `false` |
[AWS MCPs Server](https://github.com/awslabs/mcp?tab=readme-ov-file#infrastructure-as-code)

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
[Azure Cloud MCP Server](https://github.com/microsoft/mcp/tree/main/servers/Azure.Mcp.Server)

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
<br>

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
[Terraforms MCP Server](https://github.com/hashicorp/terraform-mcp-server)

---
<br>
<br>

# Guías de Configuración en Agentes

- [Amazon Q Developer](https://alejandria.pragma.co/es/private/conocimiento-aplicado/inteligencia-artificial/kc-cc/mcp/pragma-mcps/amazon-q-developer)
- [Copilot](https://alejandria.pragma.co/es/private/conocimiento-aplicado/inteligencia-artificial/kc-cc/mcp/pragma-mcps/copilot)

---
<br>

## Contribuciones e Historial de Versiones
| Versión | Área                    | Participantes                          | Fecha      | Comentario                                                                 |
|---------|--------------------------|----------------------------------------|------------|-----------------------------------------------------------------------------|
| 1.0.0   | Lider Chapter - DevSecOps  | Cristian Correa - Jhon Quevedo | 10/28/2025 | Se crea artefacto Template Markdown. |