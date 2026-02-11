# Templates CloudFormation

## Template Base Lambda

**Archivo:** `service-template.yaml`

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: Template base para servicios migrados de OSB

Parameters:
  ServiceName:
    Type: String
    Description: Nombre del servicio
  
  Environment:
    Type: String
    AllowedValues: [dev, qa, prod]
    Default: dev
  
  MemorySize:
    Type: Number
    Default: 512
    AllowedValues: [256, 512, 1024, 2048, 3008]
  
  Timeout:
    Type: Number
    Default: 30
    MinValue: 3
    MaxValue: 900

Conditions:
  IsProduction: !Equals [!Ref Environment, prod]

Resources:
  # Lambda Function
  ServiceFunction:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: !Sub '${ServiceName}-${Environment}'
      CodeUri: ./src
      Handler: handler.lambda_handler
      Runtime: python3.11
      MemorySize: !Ref MemorySize
      Timeout: !Ref Timeout
      ReservedConcurrentExecutions: !If [IsProduction, 100, 10]
      Environment:
        Variables:
          SERVICE_NAME: !Ref ServiceName
          ENVIRONMENT: !Ref Environment
          LOG_LEVEL: !If [IsProduction, 'INFO', 'DEBUG']
      DeadLetterQueue:
        Type: SQS
        TargetArn: !GetAtt ServiceDLQ.Arn
      Tracing: Active
      Policies:
        - AWSLambdaBasicExecutionRole
        - Version: '2012-10-17'
          Statement:
            - Effect: Allow
              Action: secretsmanager:GetSecretValue
              Resource: !Sub 'arn:aws:secretsmanager:${AWS::Region}:${AWS::AccountId}:secret:*'
      Tags:
        Service: !Ref ServiceName
        Environment: !Ref Environment
  
  # Dead Letter Queue
  ServiceDLQ:
    Type: AWS::SQS::Queue
    Properties:
      QueueName: !Sub '${ServiceName}-dlq-${Environment}'
      MessageRetentionPeriod: 1209600  # 14 días
  
  # CloudWatch Log Group
  ServiceLogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: !Sub '/aws/lambda/${ServiceName}-${Environment}'
      RetentionInDays: !If [IsProduction, 90, 30]
  
  # CloudWatch Alarms
  ErrorAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub '${ServiceName}-errors-${Environment}'
      MetricName: Errors
      Namespace: AWS/Lambda
      Statistic: Sum
      Period: 300
      EvaluationPeriods: 1
      Threshold: 5
      ComparisonOperator: GreaterThanThreshold
      Dimensions:
        - Name: FunctionName
          Value: !Ref ServiceFunction

Outputs:
  FunctionArn:
    Value: !GetAtt ServiceFunction.Arn
    Export:
      Name: !Sub '${ServiceName}-${Environment}-Arn'
  
  FunctionName:
    Value: !Ref ServiceFunction
  
  DLQUrl:
    Value: !Ref ServiceDLQ
```

---

## Template con API Gateway

**Archivo:** `api-service-template.yaml`

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Parameters:
  ServiceName:
    Type: String
  Environment:
    Type: String
    AllowedValues: [dev, qa, prod]
  ApiPath:
    Type: String
    Description: API path (ej. /orders/create)
  HttpMethod:
    Type: String
    Default: POST
    AllowedValues: [GET, POST, PUT, DELETE, PATCH]

Resources:
  ServiceFunction:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: !Sub '${ServiceName}-${Environment}'
      CodeUri: ./src
      Handler: handler.lambda_handler
      Runtime: python3.11
      MemorySize: 512
      Timeout: 30
      Events:
        ApiEvent:
          Type: Api
          Properties:
            Path: !Ref ApiPath
            Method: !Ref HttpMethod
            RestApiId: !Ref ServiceApi
  
  ServiceApi:
    Type: AWS::Serverless::Api
    Properties:
      Name: !Sub '${ServiceName}-api-${Environment}'
      StageName: !Ref Environment
      TracingEnabled: true
      MethodSettings:
        - ResourcePath: '/*'
          HttpMethod: '*'
          ThrottlingBurstLimit: 100
          ThrottlingRateLimit: 50

Outputs:
  ApiEndpoint:
    Value: !Sub 'https://${ServiceApi}.execute-api.${AWS::Region}.amazonaws.com/${Environment}${ApiPath}'
  
  FunctionArn:
    Value: !GetAtt ServiceFunction.Arn
```

---

## Template con VPC

**Archivo:** `vpc-service-template.yaml`

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Parameters:
  ServiceName:
    Type: String
  Environment:
    Type: String
  VpcId:
    Type: AWS::EC2::VPC::Id
    Description: VPC ID
  SubnetIds:
    Type: List<AWS::EC2::Subnet::Id>
    Description: Subnet IDs (privadas)

Resources:
  ServiceFunction:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: !Sub '${ServiceName}-${Environment}'
      CodeUri: ./src
      Handler: handler.lambda_handler
      Runtime: python3.11
      VpcConfig:
        SecurityGroupIds:
          - !Ref LambdaSecurityGroup
        SubnetIds: !Ref SubnetIds
  
  LambdaSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: !Sub 'SG for ${ServiceName}'
      VpcId: !Ref VpcId
      SecurityGroupEgress:
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          CidrIp: 0.0.0.0/0

Outputs:
  FunctionArn:
    Value: !GetAtt ServiceFunction.Arn
  
  SecurityGroupId:
    Value: !Ref LambdaSecurityGroup
```

---

## Template con Step Functions

**Archivo:** `stepfunctions-template.yaml`

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Parameters:
  WorkflowName:
    Type: String
  Environment:
    Type: String

Resources:
  # Lambda Functions
  Step1Function:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: !Sub '${WorkflowName}-step1-${Environment}'
      CodeUri: ./src/step1
      Handler: handler.lambda_handler
      Runtime: python3.11
  
  Step2Function:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: !Sub '${WorkflowName}-step2-${Environment}'
      CodeUri: ./src/step2
      Handler: handler.lambda_handler
      Runtime: python3.11
  
  # State Machine
  WorkflowStateMachine:
    Type: AWS::Serverless::StateMachine
    Properties:
      Name: !Sub '${WorkflowName}-${Environment}'
      DefinitionUri: statemachine.asl.json
      DefinitionSubstitutions:
        Step1FunctionArn: !GetAtt Step1Function.Arn
        Step2FunctionArn: !GetAtt Step2Function.Arn
      Policies:
        - LambdaInvokePolicy:
            FunctionName: !Ref Step1Function
        - LambdaInvokePolicy:
            FunctionName: !Ref Step2Function

Outputs:
  StateMachineArn:
    Value: !Ref WorkflowStateMachine
```

---

## Archivos de Parámetros

### parameters-dev.json
```json
[
  {
    "ParameterKey": "ServiceName",
    "ParameterValue": "customer-order"
  },
  {
    "ParameterKey": "Environment",
    "ParameterValue": "dev"
  },
  {
    "ParameterKey": "MemorySize",
    "ParameterValue": "512"
  },
  {
    "ParameterKey": "Timeout",
    "ParameterValue": "30"
  }
]
```

---

## Scripts de Despliegue

### deploy.sh
```bash
#!/bin/bash
set -e

SERVICE_NAME=$1
ENVIRONMENT=$2

if [ -z "$SERVICE_NAME" ] || [ -z "$ENVIRONMENT" ]; then
  echo "Usage: ./deploy.sh <service-name> <environment>"
  exit 1
fi

STACK_NAME="${SERVICE_NAME}-${ENVIRONMENT}"
TEMPLATE_FILE="template.yaml"
PARAMS_FILE="parameters-${ENVIRONMENT}.json"

echo "Deploying ${STACK_NAME}..."

# Validate
aws cloudformation validate-template \
  --template-body file://${TEMPLATE_FILE}

# Package (if needed)
aws cloudformation package \
  --template-file ${TEMPLATE_FILE} \
  --s3-bucket lambda-deployments-bucket \
  --output-template-file packaged.yaml

# Deploy
aws cloudformation deploy \
  --template-file packaged.yaml \
  --stack-name ${STACK_NAME} \
  --parameter-overrides file://${PARAMS_FILE} \
  --capabilities CAPABILITY_IAM \
  --no-fail-on-empty-changeset

# Get outputs
aws cloudformation describe-stacks \
  --stack-name ${STACK_NAME} \
  --query 'Stacks[0].Outputs' \
  --output table

echo "✅ Deployment complete!"
```

### delete.sh
```bash
#!/bin/bash
set -e

SERVICE_NAME=$1
ENVIRONMENT=$2
STACK_NAME="${SERVICE_NAME}-${ENVIRONMENT}"

echo "Deleting stack ${STACK_NAME}..."

aws cloudformation delete-stack --stack-name ${STACK_NAME}
aws cloudformation wait stack-delete-complete --stack-name ${STACK_NAME}

echo "✅ Stack deleted!"
```

