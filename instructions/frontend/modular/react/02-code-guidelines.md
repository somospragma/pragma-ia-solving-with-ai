# Code Guidelines & Standards

## 2.1. Design Principles & Best Practices

**Core Architecture Principles:**

- Follow SOLID, esp. Dependency Inversion
- Map external data to internal entities
- You write modular, typed, reusable, and standards-compliant code
- You prioritize security, accessibility (A11Y), performance, scalability, testability, and code clarity in every solution

**React + TypeScript Guidelines:**

- Use TypeScript only, no any
- Prefer interface or type
- Use ?., ??, and const
- Avoid magic strings
- Favor named exports
- Follow casing conventions (PascalCase, camelCase)

## 2.2. Naming Conventions

**Component & Hook Naming:**

- ComponentName.tsx for components
- useFeature.ts for hooks
- feature.service.ts for services
- Folders in PascalCase, with index.ts

## 2.3. Key Code Conventions

**File Import Order:**

1. React/core libs
2. Third-party libs
3. Project services/hooks
4. Shared utils
5. Relative imports

## 2.4. Commenting Policy

- Code commented and documented as part of Definition of Done
