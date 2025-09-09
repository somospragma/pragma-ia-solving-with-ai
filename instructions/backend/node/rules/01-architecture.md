# Architecture Guidelines

## 1.1 Structure by Business Components
- ✅ Create separate folders for each business domain (`orders`, `users`, `payments`)
- ✅ Each component must have its own `package.json`
- ✅ Maintain autonomous components with own API, logic, and data access
- ✅ Use structure: `apps/` (components) and `libraries/` (shared functionality)
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
- ✅ Each module must have its own `package.json`
- ✅ Define public interface using `package.json.main` or `package.json.exports`
- ✅ Consider publishing as private npm packages
- ❌ NO allow clients to access internal module functionality

## 1.4 Environment-Aware, Secure Configuration
- ✅ Allow reading from files AND environment variables
- ✅ Keep secrets outside committed code
- ✅ Use hierarchical configuration for easier findability
- ✅ Implement type support and validation
- ✅ Specify defaults for each key
- ✅ Use libraries like `convict`, `env-var`, `zod`
- ❌ NO hardcode configuration in code

## 1.5 Framework Selection Considerations
- ✅ Evaluate: Nest.js, Fastify, Express, AWS SAM/Serverless Framework
- ✅ Nest.js: for OOP teams and large applications
- ✅ Fastify: for reasonably-sized components and simple Node.js mechanics
- ✅ Express: when having experienced architect and granular control
- ✅ AWS SAM/Serverless Framework: for serverless architectures and cloud-native applications
- ❌ NO choose based on partial information

## 1.6 TypeScript Usage Guidelines
- ✅ Use for defining variable and function return types
- ✅ Use advanced features only when really necessary
- ✅ Keep syntax simple with primitive types
- ❌ NO use sophisticated features unnecessarily
- ❌ NO increase complexity without clear benefit