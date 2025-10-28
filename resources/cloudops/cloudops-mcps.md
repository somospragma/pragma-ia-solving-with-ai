# Parámetros de los Servidores MCP

Este documento describe los parámetros de configuración de los servidores MCP.

---

## Servidores MCP Analista CloudOps

### aws-api
- **Command**: `uvx`
- **Args**: `["awslabs.aws-api-mcp-server@latest"]`
- **Env**:
  - `FASTMCP_LOG_LEVEL`: `ERROR`

### aws-knowledge
- **Command**: `uvx`
- **Args**: `["awslabs.aws-knowledge-mcp-server@latest"]`
- **Env**:
  - `FASTMCP_LOG_LEVEL`: `ERROR`
  - `AWS_DOCUMENTATION_PARTITION`: `aws`

### cloudwatch
- **Command**: `uvx`
- **Args**: `["awslabs.cloudwatch-mcp-server@latest"]`
- **Env**:
  - `FASTMCP_LOG_LEVEL`: `ERROR`

### cost-explorer
- **Command**: `uvx`
- **Args**: `["awslabs.cost-explorer-mcp-server@latest"]`
- **Env**:
  - `FASTMCP_LOG_LEVEL`: `ERROR`

### aws-support
- **Command**: `uvx`
- **Args**: `["awslabs.aws-support-mcp-server@latest"]`
- **Env**:
  - `FASTMCP_LOG_LEVEL`: `ERROR`

### cloudwatch-appsignals
- **Command**: `uvx`
- **Args**: `["awslabs.cloudwatch-appsignals-mcp-server@latest"]`
- **Env**:
  - `FASTMCP_LOG_LEVEL`: `ERROR`

### eks
- **Command**: `uvx`
- **Args**: `["awslabs.eks-mcp-server@latest"]`
- **Env**:
  - `FASTMCP_LOG_LEVEL`: `ERROR`

### ecs
- **Command**: `uvx`
- **Args**: `["awslabs.ecs-mcp-server@latest"]`
- **Env**:
  - `FASTMCP_LOG_LEVEL`: `ERROR`

---

## Servidores MCP Analista DBA

### dynamodb
- **Command**: `uvx`
- **Args**: `["awslabs.dynamodb-mcp-server@latest"]`
- **Env**:
  - `FASTMCP_LOG_LEVEL`: `ERROR`

### aurora-postgresql
- **Command**: `uvx`
- **Args**: `["awslabs.postgres-mcp-server@latest"]`
- **Env**:
  - `FASTMCP_LOG_LEVEL`: `ERROR`

### aurora-mysql
- **Command**: `uvx`
- **Args**: `["awslabs.mysql-mcp-server@latest"]`
- **Env**:
  - `FASTMCP_LOG_LEVEL`: `ERROR`

### aurora-dsql
- **Command**: `uvx`
- **Args**: `["awslabs.aurora-dsql-mcp-server@latest"]`
- **Env**:
  - `FASTMCP_LOG_LEVEL`: `ERROR`

### documentdb
- **Command**: `uvx`
- **Args**: `["awslabs.documentdb-mcp-server@latest"]`
- **Env**:
  - `FASTMCP_LOG_LEVEL`: `ERROR`

### elasticache
- **Command**: `uvx`
- **Args**: `["awslabs.elasticache-mcp-server@latest"]`
- **Env**:
  - `FASTMCP_LOG_LEVEL`: `ERROR`

### redshift
- **Command**: `uvx`
- **Args**: `["awslabs.redshift-mcp-server@latest"]`
- **Env**:
  - `FASTMCP_LOG_LEVEL`: `ERROR`

### cost-explorer
- **Command**: `uvx`
- **Args**: `["awslabs.cost-explorer-mcp-server@latest"]`
- **Env**:
  - `FASTMCP_LOG_LEVEL`: `ERROR`

---

## Servidores MCP Arquitecto CloudOps

### aws-api
- **Command**: `uvx`
- **Args**: `["awslabs.aws-api-mcp-server@latest"]`
- **Env**:
  - `FASTMCP_LOG_LEVEL`: `ERROR`

### aws-knowledge
- **Command**: `uvx`
- **Args**: `["awslabs.aws-knowledge-mcp-server@latest"]`
- **Env**:
  - `FASTMCP_LOG_LEVEL`: `ERROR`
  - `AWS_DOCUMENTATION_PARTITION`: `aws`

### aws-cdk
- **Command**: `uvx`
- **Args**: `["awslabs.cdk-mcp-server@latest"]`
- **Env**:
  - `FASTMCP_LOG_LEVEL`: `ERROR`

### aws-cloudformation
- **Command**: `uvx`
- **Args**: `["awslabs.cfn-mcp-server@latest"]`
- **Env**:
  - `FASTMCP_LOG_LEVEL`: `ERROR`

### aws-terraform
- **Command**: `uvx`
- **Args**: `["awslabs.terraform-mcp-server@latest"]`
- **Env**:
  - `FASTMCP_LOG_LEVEL`: `ERROR`

### aws-pricing
- **Command**: `uvx`
- **Args**: `["awslabs.aws-pricing-mcp-server@latest"]`
- **Env**:
  - `FASTMCP_LOG_LEVEL`: `ERROR`

### aws-diagram
- **Command**: `uvx`
- **Args**: `["awslabs.aws-diagram-mcp-server@latest"]`
- **Env**:
  - `FASTMCP_LOG_LEVEL`: `ERROR`


---

## Guías de Configuración en Agentes

- [Amazon Q Developer](https://alejandria.pragma.co/es/private/conocimiento-aplicado/inteligencia-artificial/kc-cc/mcp/pragma-mcps/amazon-q-developer)
- [Copilot](https://alejandria.pragma.co/es/private/conocimiento-aplicado/inteligencia-artificial/kc-cc/mcp/pragma-mcps/copilot)

---

## Contribuciones e Historial de Versiones
| Versión | Área                    | Participantes                          | Fecha      | Comentario                                                                 |
|---------|--------------------------|----------------------------------------|------------|-----------------------------------------------------------------------------|
| 1.0.0   | Arquitectura - CloudOps  | Cristian Noguera | 23/09/2025 | Se crea artefacto Template Markdown. |