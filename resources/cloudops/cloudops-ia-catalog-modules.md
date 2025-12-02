# Terraform Modules Catalog - AI Agent Reference

## Introduction

This catalog provides a comprehensive reference of Terraform modules available for AWS infrastructure deployment. Each module is documented with its primary function, AWS resources, capabilities, dependencies, and source URL to enable efficient querying and identification by AI agents and developers.

## Modules Table

| Module Name | Primary Function | AWS Resources Included | Key Capabilities | Dependencies | Module URL |
|-------------|------------------|------------------------|------------------|--------------|------------|
| cloudops-ref-repo-aws-bedrock-guardrails-terraform | Creates and manages AWS Bedrock Guardrails for AI generative applications with security controls and content moderation | aws_bedrock_guardrail, aws_bedrock_guardrail_version | Content filtering, topic blocking, word filtering, sensitive information redaction, contextual grounding, configurable thresholds | Requires AWS Bedrock access, IAM permissions for Bedrock | https://github.com/somospragma/cloudops-ref-repo-aws-bedrock-guardrails-terraform/tree/v1.0.0 |
| cloudops-ref-repo-aws-agentai-security-terraform | Provides complete web security solution using AWS WAF v2 to protect web applications and APIs against common threats | aws_wafv2_web_acl, aws_wafv2_rule_group, aws_wafv2_ip_set | Managed rule groups, rate limiting, IP blocking, geo-blocking, custom rules, CloudWatch metrics integration | Requires existing ALB or CloudFront distribution | https://github.com/somospragma/cloudops-ref-repo-aws-agentai-security-terraform |
| cloudops-ref-repo-aws-vpc-terraform | Creates complete Virtual Private Cloud infrastructure with public/private subnets, routing, and flow logs | aws_vpc, aws_subnet, aws_internet_gateway, aws_nat_gateway, aws_route_table, aws_flow_log, aws_cloudwatch_log_group | Multi-AZ support, public/private subnet configuration, NAT Gateway, Internet Gateway, VPC Flow Logs to CloudWatch, customizable CIDR blocks | IAM role for Flow Logs, CloudWatch Logs permissions | https://github.com/somospragma/cloudops-ref-repo-aws-vpc-terraform/tree/v1.0.1 |
| cloudops-ref-repo-aws-ecs-cluster-terraform | Creates ECS Cluster with security best practices and standardized naming conventions | aws_ecs_cluster, aws_ecs_cluster_capacity_providers, aws_cloudwatch_log_group | Container Insights, Fargate/EC2 capacity providers, CloudWatch logging, encryption at rest | IAM roles for ECS tasks and services | https://github.com/somospragma/cloudops-ref-repo-aws-ecs-cluster-terraform/tree/v1.0.0 |
| cloudops-ref-repo-aws-elb-terraform | Creates and configures AWS load balancers (ALB and NLB) with target groups, listeners, rules, and WAF integration | aws_lb, aws_lb_target_group, aws_lb_listener, aws_lb_listener_rule, aws_wafv2_web_acl_association | Multiple target groups, health checks, SSL/TLS termination, path-based routing, host-based routing, WAF integration, access logs | Requires existing VPC, subnets, security groups, optional ACM certificate for HTTPS | https://github.com/somospragma/cloudops-ref-repo-aws-elb-terraform/tree/feature/elb-module-maps |
| cloudops-ref-repo-aws-sg-terraform | Creates and manages Security Groups with multiple ingress and egress rules | aws_security_group, aws_security_group_rule | Multiple security groups creation, dynamic rule management, CIDR and security group source references, protocol and port configuration | Requires existing VPC | https://github.com/somospragma/cloudops-ref-repo-aws-sg-terraform/tree/feature/sg-module-mapobject |
| cloudops-ref-repo-aws-ecr-terraform | Creates Elastic Container Registry repositories with lifecycle policies | aws_ecr_repository, aws_ecr_lifecycle_policy | Image scanning on push, encryption at rest, lifecycle policies for image retention, immutable tags support | KMS key for encryption (optional) | https://github.com/somospragma/cloudops-ref-repo-aws-ecr-terraform/tree/feature/ecr-module-init |
| cloudops-ref-repo-aws-iam-terraform | Creates and manages IAM resources including roles, policies, and groups | aws_iam_role, aws_iam_policy, aws_iam_role_policy_attachment, aws_iam_group, aws_iam_user | Custom IAM policies, role trust relationships, policy attachments, assume role configuration, service-linked roles | None | https://github.com/somospragma/cloudops-ref-repo-aws-iam-terraform/tree/feature/iam-module-init |
| cloudops-ref-repo-aws-vpc-endpoint-terraform | Creates VPC Endpoints for private connectivity to AWS services | aws_vpc_endpoint, aws_vpc_endpoint_route_table_association, aws_vpc_endpoint_subnet_association | Interface and Gateway endpoints, private DNS support, security group association, route table integration | Requires existing VPC, subnets, security groups, route tables | https://github.com/somospragma/cloudops-ref-repo-aws-vpc-endpoint-terraform/tree/feature/vpce-module-init |
| cloudops-ref-repo-aws-transversal-terraform | Combines VPC, VPC endpoints, and security groups submodules for complete network infrastructure | Submodules: vpc, vpc_endpoints, security_groups | Complete network infrastructure deployment, integrated security, standardized configuration | None (creates all required resources) | https://github.com/somospragma/cloudops-ref-repo-aws-transversal-terraform/tree/feature/transversal-module-init |
| cloudops-ref-repo-aws-rds-terraform | Creates RDS database instances with encryption and backup configuration | aws_db_instance, aws_db_subnet_group, aws_db_parameter_group, aws_db_option_group | Multi-AZ deployment, automated backups, encryption at rest, parameter groups, option groups, snapshot management | Requires existing VPC, security groups, subnets, KMS key | https://github.com/somospragma/cloudops-ref-repo-aws-rds-terraform/tree/v1.0.0 |
| cloudops-ref-repo-aws-kms-terraform | Creates and manages AWS KMS keys with security best practices | aws_kms_key, aws_kms_alias, aws_kms_grant | Key rotation, key policies, multi-region keys, key aliases, grants for service integration | IAM permissions for key management | https://github.com/somospragma/cloudops-ref-repo-aws-kms-terraform/tree/feature/kms-module-map |
| cloudops-ref-repo-aws-workload-terraform | Combines ELB, IAM, ECS cluster, ECS service, and security groups for complete workload deployment | Submodules: elb, iam, ecs_cluster, ecs_service, security_groups | Complete containerized workload deployment, load balancing, auto-scaling, service discovery | Requires existing VPC and subnets | https://github.com/somospragma/cloudops-ref-repo-aws-workload-terraform/tree/feature/workload-module-init |
| cloudops-ref-repo-aws-ecs-service-terraform | Creates and manages ECS services with multi-container support, auto-scaling, and monitoring | aws_ecs_service, aws_ecs_task_definition, aws_appautoscaling_target, aws_appautoscaling_policy, aws_cloudwatch_metric_alarm | Multiple container definitions, service auto-scaling, load balancer integration, health checks, CloudWatch alarms, service discovery | Requires existing ECS cluster, task execution role, VPC, subnets, security groups | https://github.com/somospragma/cloudops-ref-repo-aws-ecs-service-terraform/tree/v1.0.0 |
| cloudops-ref-repo-aws-sm-terraform | Creates and manages secrets in AWS Secrets Manager with mandatory encryption | aws_secretsmanager_secret, aws_secretsmanager_secret_version, aws_secretsmanager_secret_policy | Automatic rotation, KMS encryption, resource policies, version management, cross-account access | Requires KMS key for encryption | https://github.com/somospragma/cloudops-ref-repo-aws-sm-terraform/tree/v1.0.0 |
| cloudops-ref-repo-aws-s3-terraform | Creates and manages multiple S3 buckets with enterprise features for security, compliance, and cost optimization | aws_s3_bucket, aws_s3_bucket_versioning, aws_s3_bucket_encryption, aws_s3_bucket_public_access_block, aws_s3_bucket_lifecycle_configuration, aws_s3_bucket_policy | Versioning, encryption at rest, lifecycle policies, public access blocking, bucket policies, logging, replication, object lock | KMS key for encryption (optional) | https://github.com/somospragma/cloudops-ref-repo-aws-s3-terraform/tree/v1.0.1 |
| cloudops-ref-repo-aws-efs-terraform | Creates and manages Amazon EFS file systems with encryption, access points, and lifecycle policies | aws_efs_file_system, aws_efs_mount_target, aws_efs_access_point, aws_efs_backup_policy | Encryption at rest and in transit, automatic backups, lifecycle management, access points, performance modes, throughput modes | Requires existing VPC, subnets, security groups, KMS key for encryption | https://github.com/somospragma/cloudops-ref-repo-aws-efs-terraform/tree/feature/efs-module-init |
| cloudops-ref-repo-aws-persistence-terraform | Combines RDS, KMS, and security groups for complete persistence infrastructure with global/primary/secondary RDS clusters | Submodules: rds, kms, security_groups | Global database clusters, multi-region replication, automated failover, encryption at rest | Requires existing VPC and subnets | https://github.com/somospragma/cloudops-ref-repo-aws-persistence-terraform/tree/feature/persistency-module-init |
| cloudops-ref-repo-aws-dynamo-terraform | Creates and manages DynamoDB tables with capacity configuration, encryption, and global replication | aws_dynamodb_table, aws_dynamodb_global_table, aws_dynamodb_table_item, aws_appautoscaling_target, aws_appautoscaling_policy | On-demand or provisioned capacity, auto-scaling, global tables, point-in-time recovery, encryption at rest, stream configuration | KMS key for encryption (optional) | https://github.com/somospragma/cloudops-ref-repo-aws-dynamo-terraform/tree/v1.0.0 |
| cloudops-ref-repo-aws-glue-job-terraform | Creates and manages AWS Glue jobs for ETL processing with IAM roles and logging | aws_glue_job, aws_iam_role, aws_iam_role_policy, aws_cloudwatch_log_group | Support for Glue ETL, Python Shell, and Glue Ray jobs, CloudWatch logging, configurable worker types, job parameters | Requires S3 bucket for scripts and temporary data | https://github.com/somospragma/cloudops-ref-repo-aws-glue-job-terraform/tree/feature/glue_job-module-init |
| cloudops-ref-repo-aws-glue-crawler-terraform | Creates and configures AWS Glue Crawler with catalog database and connections | aws_glue_crawler, aws_glue_catalog_database, aws_glue_connection, aws_iam_role | Multiple data source support (S3, JDBC, DynamoDB), scheduled crawling, schema detection, partition discovery | Requires IAM role with Glue permissions, data source access | https://github.com/somospragma/cloudops-ref-repo-aws-glue-crawler-terraform/tree/feature/crawler-module-init |
| cloudops-ref-repo-aws-lambda-terraform | Creates and configures AWS Lambda functions with support for local or S3 source code | aws_lambda_function, aws_lambda_permission, aws_cloudwatch_log_group, aws_lambda_event_source_mapping | Multiple runtime support, environment variables, VPC configuration, layers support, event source mappings, CloudWatch logging | Requires IAM execution role, optional VPC and security groups | https://github.com/somospragma/cloudops-ref-repo-aws-lambda-terraform/tree/feature/lambda-module-jarvis |
| cloudops-ref-repo-aws-cognito-terraform | Creates multiple Cognito User Pools with domains, clients, and federated identity providers | aws_cognito_user_pool, aws_cognito_user_pool_domain, aws_cognito_user_pool_client, aws_cognito_identity_provider | Password policies, MFA configuration, OAuth2 flows, social identity providers (Google, Facebook), custom domains, user attributes | Optional ACM certificate for custom domains | https://github.com/somospragma/cloudops-ref-repo-aws-cognito-terraform/tree/feature/cognito-module-init |
| cloudops-ref-repo-aws-sqs-terraform | Creates and configures Amazon SQS queues with security best practices | aws_sqs_queue, aws_sqs_queue_policy | Standard and FIFO queues, dead letter queues, message retention, visibility timeout, encryption at rest, access policies | KMS key for encryption (optional) | https://github.com/somospragma/cloudops-ref-repo-aws-sqs-terraform/tree/v1.0.1 |
| cloudops-ref-repo-aws-eks-terraform | Creates and manages Amazon EKS clusters with security and configuration best practices | aws_eks_cluster, aws_eks_node_group, aws_eks_addon, aws_iam_role, aws_security_group | Managed node groups, Fargate profiles, cluster add-ons, OIDC provider, encryption at rest, private endpoint access | Requires existing VPC and subnets, IAM roles for cluster and nodes | https://github.com/somospragma/cloudops-ref-repo-aws-eks-terraform/tree/feature/init-module-eks |
| cloudops-ref-repo-aws-route53-terraform | Creates and manages Route 53 hosted zones (public and private) with DNS records | aws_route53_zone, aws_route53_record, aws_route53_health_check | Public and private hosted zones, multiple record types (A, AAAA, CNAME, MX, TXT), health checks, alias records | For private zones, requires existing VPC | https://github.com/somospragma/cloudops-ref-repo-aws-route53-terraform/tree/module-route53-init |
| cloudops-ref-repo-aws-acm-terraform | Creates and manages SSL/TLS certificates in AWS Certificate Manager with DNS or EMAIL validation | aws_acm_certificate, aws_acm_certificate_validation, aws_route53_record | DNS and email validation, wildcard certificates, certificate renewal, multiple domain names (SAN) | For DNS validation, requires Route 53 hosted zone | https://github.com/somospragma/cloudops-ref-repo-aws-acm-terraform/tree/v1.0.0 |
| cloudops-ref-repo-aws-cloudfront-terraform | Creates and manages CloudFront distributions for content delivery with S3 or ALB origins | aws_cloudfront_distribution, aws_cloudfront_origin_access_control, aws_cloudfront_cache_policy, aws_cloudfront_origin_request_policy | Multiple origins, cache behaviors, SSL/TLS certificates, custom error responses, geo-restrictions, WAF integration, logging | Requires S3 bucket or ALB as origin, optional ACM certificate, WAF web ACL | https://github.com/somospragma/cloudops-ref-repo-aws-cloudfront-terraform/tree/feature/init-module-cloudfront |
| cloudops-ref-repo-aws-waf-terraform | Deploys AWS WAF resources to protect web applications from exploits and attacks | aws_wafv2_web_acl, aws_wafv2_rule_group, aws_wafv2_ip_set, aws_wafv2_regex_pattern_set | Managed rule groups, custom rules, rate limiting, IP sets, regex patterns, CloudWatch metrics, logging | S3 bucket for WAF logs (optional) | https://github.com/somospragma/cloudops-ref-repo-aws-waf-terraform/tree/feature/waf-module-init-maps |
| cloudops-ref-repo-aws-lambda-layers-terraform | Creates and configures reusable AWS Lambda Layers for sharing code and dependencies | aws_lambda_layer_version | Multiple runtime support, version management, code sharing across functions, S3 or local source | S3 bucket for layer code (optional) | https://github.com/somospragma/cloudops-ref-repo-aws-lambda-layers-terraform/tree/feature/refactor-layer-module |
| cloudops-ref-repo-aws-bedrock-knowledgebase-terraform | Creates and configures Knowledge Bases in AWS Bedrock with multiple data source types | aws_bedrockagent_knowledge_base, aws_bedrockagent_data_source, aws_opensearchserverless_collection, aws_iam_role | Vector database integration (OpenSearch Serverless), S3 data sources, embedding models, chunking strategies | Requires S3 bucket for data sources, IAM roles for Bedrock access | https://github.com/somospragma/cloudops-ref-repo-aws-bedrock-knowledgebase-terraform/tree/init-module-bedrock-kc |
| cloudops-ref-repo-aws-bedrock-agent-terraform | Creates and configures AWS Bedrock agents with action groups, guardrails, and custom prompts | aws_bedrockagent_agent, aws_bedrockagent_agent_action_group, aws_bedrockagent_agent_alias | Action groups with Lambda functions, knowledge base integration, guardrails, custom prompt templates, agent aliases | Requires Lambda functions for action groups, optional knowledge base, guardrails | https://github.com/somospragma/cloudops-ref-repo-aws-bedrock-agent-terraform/tree/init-module-bedrock-agent |
| cloudops-ref-repo-aws-bedrock-flow-terraform | Creates and configures AWS Bedrock Flows with multiple node types and complex processing logic | aws_bedrockagent_flow, aws_bedrockagent_flow_version, aws_bedrockagent_flow_alias | Multiple node types (prompt, condition, knowledge base, agent), flow versioning, aliases, complex branching logic | Requires IAM role for flow execution, optional knowledge bases and agents | https://github.com/somospragma/cloudops-ref-repo-aws-bedrock-flow-terraform/tree/init-module-bedrock-flow |
| cloudops-ref-repo-aws-vpc-cloudformation | CloudFormation template to deploy VPC with DNS enabled and corporate tagging | AWS::EC2::VPC | DNS support, DNS hostnames, customizable CIDR, tagging | None | https://github.com/somospragma/cloudops-ref-repo-aws-vpc-cloudformation |
| cloudops-ref-repo-aws-ec2-cloudformation | CloudFormation template to deploy EC2 instance in existing VPC and subnet | AWS::EC2::Instance | AMI selection, instance type configuration, security group association, subnet placement | Requires existing VPC and subnet | https://github.com/somospragma/cloudops-ref-repo-aws-ec2-cloudformation |
| cloudops-ref-repo-aws-vpc-endpoint-interface-cloudformation | CloudFormation template to deploy VPC Endpoint Interface for regional services | AWS::EC2::VPCEndpoint | Private connectivity to AWS services, security group association, subnet placement | Requires existing VPC, subnets, security groups | https://github.com/somospragma/cloudops-ref-repo-aws-vpc-endpoint-interface-cloudformation |
| cloudops-ref-repo-aws-redshift-terraform | Creates and manages Amazon Redshift resources (provisioned and serverless) for data warehouse solutions | aws_redshift_cluster, aws_redshift_subnet_group, aws_redshift_parameter_group, aws_redshiftserverless_namespace, aws_redshiftserverless_workgroup | Provisioned and serverless options, encryption at rest, automated snapshots, parameter groups, VPC deployment, enhanced VPC routing | Requires existing VPC, subnets, security groups, KMS key for encryption | https://github.com/somospragma/cloudops-ref-repo-aws-redshift-terraform/tree/init-module-redshift |
| cloudops-ref-repo-aws-vpc-endpoint-gateway-cloudformation | CloudFormation template to deploy VPC Endpoint Gateway for S3 or DynamoDB | AWS::EC2::VPCEndpoint | Private connectivity to S3 and DynamoDB, route table association | Requires existing VPC and route tables | https://github.com/somospragma/cloudops-ref-repo-aws-vpc-endpoint-gateway-cloudformation |
| cloudops-ref-repo-aws-eventbridge-terraform | Provides complete solution for managing Amazon EventBridge with buses, rules, Lambda targets, and DLQ | aws_cloudwatch_event_bus, aws_cloudwatch_event_rule, aws_cloudwatch_event_target, aws_sqs_queue | Custom event buses, event pattern matching, scheduled rules, multiple target types, dead letter queues, cross-account events | Requires Lambda functions or other target resources, SQS queue for DLQ | https://github.com/somospragma/cloudops-ref-repo-aws-eventbridge-terraform/tree/feature/eventbridge-init-module |
| cloudops-ref-repo-aws-codestar-terraform | Creates and configures AWS CodeStar connections for integrating third-party repositories (GitHub/Bitbucket) | aws_codestarconnections_connection | GitHub and Bitbucket integration, OAuth authentication, connection management | GitHub or Bitbucket account | https://github.com/somospragma/cloudops-ref-repo-aws-codestar-terraform/tree/feature/codestar-module-init |
| cloudops-ref-repo-aws-codebuild-terraform | Creates and configures AWS CodeBuild projects for building, testing, and deploying applications | aws_codebuild_project, aws_iam_role, aws_cloudwatch_log_group | Multiple source types (CodeCommit, GitHub, S3), build environments, cache configuration, VPC support, CloudWatch logging | Requires IAM role with CodeBuild permissions, S3 bucket for artifacts | https://github.com/somospragma/cloudops-ref-repo-aws-codebuild-terraform/tree/feature/codebuild-module-init |
| cloudops-ref-repo-aws-athena-terraform | Creates and manages AWS Athena workgroups, databases, and views with enterprise-level security | aws_athena_workgroup, aws_athena_database, aws_athena_named_query, aws_glue_catalog_database | Query result encryption, workgroup configuration, data catalog integration, query result location, cost controls | Requires S3 bucket for query results, Glue catalog database | https://github.com/somospragma/cloudops-ref-repo-aws-athena-terraform/tree/feature/athena-module-init |
| cloudops-ref-repo-aws-codepipeline-terraform | Creates and configures AWS CodePipeline for implementing enterprise CI/CD workflows | aws_codepipeline, aws_iam_role, aws_s3_bucket | Multi-stage pipelines, source/build/deploy stages, approval actions, cross-region deployments, artifact management | Requires CodeBuild projects, deployment targets, S3 bucket for artifacts | https://github.com/somospragma/cloudops-ref-repo-aws-codepipeline-terraform/tree/feature/codepipeline-module-init |
| cloudops-ref-repo-aws-networking-terraform | Combines networking submodules for complete network infrastructure (Note: Description suggests RDS/KMS/SG but name indicates networking) | Submodules: rds, kms, security_groups | Network infrastructure deployment with database and encryption support | Requires existing VPC | https://github.com/somospragma/cloudops-ref-repo-aws-networking-terraform |
| cloudops-ref-repo-aws-mcp-role-configs | Optimized MCP server configurations for different AWS CloudOps roles | Configuration files | Role-based MCP server setups, pre-configured tools and permissions | MCP server installation | https://github.com/somospragma/cloudops-ref-repo-aws-mcp-role-configs |
| cloudops-ref-repo-aws-parameterstore-terraform | Creates and manages parameters in AWS Systems Manager Parameter Store | aws_ssm_parameter | String, StringList, and SecureString parameters, KMS encryption, parameter hierarchies, versioning | KMS key for SecureString parameters | https://github.com/somospragma/cloudops-ref-repo-aws-parameterstore-terraform/tree/feature/init-module-parameterstore |
| cloudops-ref-repo-aws-rds-sql-terraform | Deploys Amazon RDS instances with SQL Server Standard Edition | aws_db_instance, aws_db_subnet_group, aws_db_parameter_group | SQL Server Standard Edition, automated backups, Multi-AZ deployment, encryption at rest, parameter groups | Requires existing VPC, subnets, security groups, KMS key | https://github.com/somospragma/cloudops-ref-repo-aws-rds-sql-terraform/tree/init-module-rds-sql |
| cloudops-ref-repo-aws-lambda-layers-builder-terraform | Manages building and compiling AWS Lambda Layers with dependency installation | null_resource, local-exec provisioner | Automated build scripts execution, dependency installation, layer packaging, multi-runtime support | Requires build tools (npm, pip, etc.) installed locally | https://github.com/somospragma/cloudops-ref-repo-aws-lambda-layers-builder-terraform/tree/feature/init-lambda-layers-builders-module |
| cloudops-ref-repo-aws-sg-rules-terraform | Creates and manages Security Group rules in modular way, unifying ingress and egress in single variable | aws_security_group_rule | Unified rule management, CIDR and security group references, protocol and port configuration, description support | Requires existing security groups | https://github.com/somospragma/cloudops-ref-repo-aws-sg-rules-terraform |
| cloudops-ref-repo-aws-mcp-security-terraform | Provides comprehensive security infrastructure for MCP applications including encryption, authentication, and WAF | aws_kms_key, aws_cognito_user_pool, aws_wafv2_web_acl, aws_secretsmanager_secret, aws_iam_role | End-to-end encryption, OAuth2 authentication, WAF protection, secrets management, IAM roles and policies | None (creates all security resources) | https://github.com/somospragma/cloudops-ref-repo-aws-mcp-security-terraform/tree/feature/mcp-security-module-init |
| cloudops-ref-repo-aws-mcp-workload-terraform | Deploys complete infrastructure for MCP servers on AWS with Lambda, API Gateway, and OAuth2 authentication | aws_lambda_function, aws_api_gateway_rest_api, aws_cognito_user_pool, aws_cognito_user_pool_client | Serverless MCP server deployment, API Gateway integration, Cognito authentication, Lambda function management | Requires VPC and subnets (optional for Lambda VPC config) | https://github.com/somospragma/cloudops-ref-repo-aws-mcp-workload-terraform/tree/feature/mcp-workload-module-init |
| cloudops-ref-repo-aws-agentai-networking-terraform | Provides complete and secure network infrastructure for AI applications with VPC and four subnet types | aws_vpc, aws_subnet, aws_internet_gateway, aws_nat_gateway, aws_route_table, aws_vpc_endpoint | Four subnet types (public, private, data, AI), VPC endpoints for AWS services, NAT Gateway, Internet Gateway, flow logs | IAM role for VPC Flow Logs | https://github.com/somospragma/cloudops-ref-repo-aws-agentai-networking-terraform |
| cloudops-ref-repo-aws-agentai-persistence-terraform | Creates persistence infrastructure for Agent AI applications with Aurora PostgreSQL Serverless v2 optimized for vector storage | aws_rds_cluster, aws_rds_cluster_instance, aws_db_subnet_group, aws_rds_cluster_parameter_group | Aurora PostgreSQL Serverless v2, pgvector extension support, auto-scaling, encryption at rest, automated backups | Requires existing VPC, subnets, security groups, KMS key | https://github.com/somospragma/cloudops-ref-repo-aws-agentai-persistence-terraform |
| cloudops-ref-repo-aws-agentai-workload-frontend-terraform | Deploys complete infrastructure for hosting Agent AI frontends with S3, CloudFront, and security features | aws_s3_bucket, aws_cloudfront_distribution, aws_cloudfront_origin_access_control, aws_kms_key, aws_wafv2_web_acl | Static website hosting, CloudFront CDN, Origin Access Control, KMS encryption, WAF protection, SSL/TLS certificates | Requires ACM certificate for custom domain | https://github.com/somospragma/cloudops-ref-repo-aws-agentai-workload-frontend-terraform |
| cloudops-ref-repo-aws-agentai-workload-agent-terraform | Creates complete AI Agent solution based on Amazon Bedrock with Agent, Knowledge Base, Lambda, and API Gateway | aws_bedrockagent_agent, aws_bedrockagent_knowledge_base, aws_lambda_function, aws_api_gateway_rest_api, aws_opensearchserverless_collection | Bedrock Agent with action groups, Knowledge Base with vector search, Lambda function integration, API Gateway endpoints, OpenSearch Serverless | Requires S3 bucket for knowledge base data, IAM roles for Bedrock and Lambda | https://github.com/somospragma/cloudops-ref-repo-aws-agentai-workload-agent-terraform |

---

## Module Categories

### Networking
- **cloudops-ref-repo-aws-vpc-terraform**: VPC infrastructure
- **cloudops-ref-repo-aws-vpc-endpoint-terraform**: VPC endpoints
- **cloudops-ref-repo-aws-sg-terraform**: Security groups
- **cloudops-ref-repo-aws-sg-rules-terraform**: Security group rules
- **cloudops-ref-repo-aws-transversal-terraform**: Complete network infrastructure
- **cloudops-ref-repo-aws-networking-terraform**: Network infrastructure with database support
- **cloudops-ref-repo-aws-agentai-networking-terraform**: AI-optimized network infrastructure

### Compute
- **cloudops-ref-repo-aws-ecs-cluster-terraform**: ECS clusters
- **cloudops-ref-repo-aws-ecs-service-terraform**: ECS services
- **cloudops-ref-repo-aws-lambda-terraform**: Lambda functions
- **cloudops-ref-repo-aws-lambda-layers-terraform**: Lambda layers
- **cloudops-ref-repo-aws-lambda-layers-builder-terraform**: Lambda layer builder
- **cloudops-ref-repo-aws-eks-terraform**: EKS clusters
- **cloudops-ref-repo-aws-ec2-cloudformation**: EC2 instances (CloudFormation)

### Storage
- **cloudops-ref-repo-aws-s3-terraform**: S3 buckets
- **cloudops-ref-repo-aws-efs-terraform**: EFS file systems
- **cloudops-ref-repo-aws-ecr-terraform**: Container registries

### Database & Persistence
- **cloudops-ref-repo-aws-rds-terraform**: RDS databases
- **cloudops-ref-repo-aws-rds-sql-terraform**: RDS SQL Server
- **cloudops-ref-repo-aws-dynamo-terraform**: DynamoDB tables
- **cloudops-ref-repo-aws-redshift-terraform**: Redshift data warehouse
- **cloudops-ref-repo-aws-persistence-terraform**: Complete persistence infrastructure
- **cloudops-ref-repo-aws-agentai-persistence-terraform**: AI-optimized persistence

### Security & Identity
- **cloudops-ref-repo-aws-iam-terraform**: IAM resources
- **cloudops-ref-repo-aws-kms-terraform**: KMS keys
- **cloudops-ref-repo-aws-waf-terraform**: WAF protection
- **cloudops-ref-repo-aws-cognito-terraform**: Cognito user pools
- **cloudops-ref-repo-aws-sm-terraform**: Secrets Manager
- **cloudops-ref-repo-aws-parameterstore-terraform**: Parameter Store
- **cloudops-ref-repo-aws-mcp-security-terraform**: MCP security infrastructure
- **cloudops-ref-repo-aws-agentai-security-terraform**: AI application security

### Load Balancing & CDN
- **cloudops-ref-repo-aws-elb-terraform**: Load balancers (ALB/NLB)
- **cloudops-ref-repo-aws-cloudfront-terraform**: CloudFront distributions

### DNS & Certificates
- **cloudops-ref-repo-aws-route53-terraform**: Route 53 hosted zones
- **cloudops-ref-repo-aws-acm-terraform**: ACM certificates

### Data Processing & Analytics
- **cloudops-ref-repo-aws-glue-job-terraform**: Glue ETL jobs
- **cloudops-ref-repo-aws-glue-crawler-terraform**: Glue crawlers
- **cloudops-ref-repo-aws-athena-terraform**: Athena workgroups

### Messaging & Events
- **cloudops-ref-repo-aws-sqs-terraform**: SQS queues
- **cloudops-ref-repo-aws-eventbridge-terraform**: EventBridge buses and rules

### CI/CD
- **cloudops-ref-repo-aws-codestar-terraform**: CodeStar connections
- **cloudops-ref-repo-aws-codebuild-terraform**: CodeBuild projects
- **cloudops-ref-repo-aws-codepipeline-terraform**: CodePipeline workflows

### AI & Machine Learning
- **cloudops-ref-repo-aws-bedrock-guardrails-terraform**: Bedrock Guardrails
- **cloudops-ref-repo-aws-bedrock-knowledgebase-terraform**: Bedrock Knowledge Bases
- **cloudops-ref-repo-aws-bedrock-agent-terraform**: Bedrock Agents
- **cloudops-ref-repo-aws-bedrock-flow-terraform**: Bedrock Flows
- **cloudops-ref-repo-aws-agentai-workload-agent-terraform**: Complete AI Agent solution
- **cloudops-ref-repo-aws-agentai-workload-frontend-terraform**: AI frontend hosting

### Composite/Workload Modules
- **cloudops-ref-repo-aws-workload-terraform**: Complete containerized workload
- **cloudops-ref-repo-aws-mcp-workload-terraform**: MCP server workload

### Configuration & Tools
- **cloudops-ref-repo-aws-mcp-role-configs**: MCP role configurations

---

## AI Query Examples

Use these example queries to search for modules:

### By Service
- "Find modules for VPC networking with flow logs"
- "Identify modules that create Lambda functions with IAM roles"
- "Locate modules for S3 bucket creation with encryption"
- "Search for ECS cluster and service deployment modules"
- "Find modules for RDS database with encryption"

### By Functionality
- "Find modules that require KMS keys"
- "Identify modules with CloudWatch logging integration"
- "Locate modules supporting multi-AZ deployment"
- "Search for modules with auto-scaling capabilities"
- "Find modules with WAF integration"

### By Use Case
- "Find modules for serverless application deployment"
- "Identify modules for data warehouse solutions"
- "Locate modules for AI agent deployment"
- "Search for modules for CI/CD pipeline setup"
- "Find modules for complete workload infrastructure"

### By Security Features
- "Find modules with encryption at rest"
- "Identify modules with OAuth2 authentication"
- "Locate modules with security group management"
- "Search for modules with secrets management"
- "Find modules with WAF protection"

### By AI/ML Capabilities
- "Find modules for AWS Bedrock agents"
- "Identify modules for knowledge base creation"
- "Locate modules for vector database storage"
- "Search for modules for AI application security"
- "Find modules for generative AI guardrails"

### By Dependencies
- "Find modules that require existing VPC"
- "Identify modules that need KMS keys"
- "Locate modules requiring IAM roles"
- "Search for modules needing security groups"
- "Find standalone modules with no dependencies"

---

## Notes

1. **Version References**: Most modules include version tags (e.g., `v1.0.0`) or branch references (e.g., `feature/module-init`). Always check the repository for the latest stable version.

2. **CloudFormation Templates**: Three modules are CloudFormation templates rather than Terraform modules:
   - cloudops-ref-repo-aws-vpc-cloudformation
   - cloudops-ref-repo-aws-ec2-cloudformation
   - cloudops-ref-repo-aws-vpc-endpoint-interface-cloudformation
   - cloudops-ref-repo-aws-vpc-endpoint-gateway-cloudformation

3. **Composite Modules**: Several modules combine multiple submodules for complete infrastructure deployment:
   - cloudops-ref-repo-aws-transversal-terraform (VPC + endpoints + security groups)
   - cloudops-ref-repo-aws-workload-terraform (ELB + IAM + ECS + security groups)
   - cloudops-ref-repo-aws-persistence-terraform (RDS + KMS + security groups)

4. **AI-Specific Modules**: Multiple modules are optimized for AI/ML workloads:
   - Bedrock-related modules for generative AI
   - Agent AI modules for complete AI application infrastructure
   - MCP modules for Model Context Protocol implementations

5. **Security Best Practices**: All modules follow Pragma CloudOps security standards including:
   - Encryption at rest and in transit
   - Least privilege IAM policies
   - Network isolation
   - Audit logging
   - Compliance tagging
