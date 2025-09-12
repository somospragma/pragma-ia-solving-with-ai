# Architecture Guidelines

## 1.1 Structure by Business Components
- ✅ Organize by domain (packages): `com.company.orders`, `com.company.users`, `com.company.payments`.  
- ✅ Use Maven/Gradle modules for bounded contexts when applicable. 
- ✅ Maintain autonomous components with own API, logic, and data access
- ❌ NO group files by technical role (`controllers/`, `services/`, `models/`)
- ❌ NO create direct dependencies between components

## 1.2 Layer Components with 3-Tiers
- ✅ Use 3 layers: `domain/` (entities + domain services), `application/` (use cases), `infrastructure/` (adapters)
- ✅ Domain: pure business logic entities and domain services
- ✅ Application: use cases that orchestrate operations without business logic
- ✅ Infrastructure: input adapters (controllers) and output adapters (repositories)
- ✅ Application orchestrates domain and infrastructure layers
- ❌ NO put business logic in application layer
- ❌ NO pass web objects (request/response) to domain layer
- ❌ NO mix business logic with technical details

## 1.3 Wrap Common Utilities as Packages
- ✅ Place reusable modules in `libraries/` folder
- ✅ Each module must have its own `build.gradle`
- ✅ Publish as internal artifacts
- ❌ NO allow clients to access internal module functionality

## 1.4 Environment-Aware, Secure Configuration
- ✅ Allow reading from files AND environment variables
- ✅ Keep secrets outside committed code
- ✅ Use hierarchical configuration for easier findability
- ✅ Implement type support and validation
- ✅ Specify defaults for each key
- ❌ NO hardcode configuration in code

## 1.5 Framework Selection Considerations
- ✅ Spring Boot (for maturity and ecosystem).
- ✅ Quarkus for applications with startup/ram constraints.  
- ✅ AWS SAM/Serverless Framework: for serverless architectures and cloud-native applications
- ❌ NO choose based on partial information

## 1.6 Java versions
- ✅ Prefer JDK LTS (17 or 21 depending on context).  
- ✅ Document version and use toolchains in CI. 