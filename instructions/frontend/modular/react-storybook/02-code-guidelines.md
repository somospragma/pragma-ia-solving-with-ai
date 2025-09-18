# Code Guidelines & Standards

## 2.1. Design Principles & Best Practices

**Core Architecture Principles:**

- Storybook is the source of truth for UI components
- Storybook stories act as living documentation and test cases
- Follow SOLID, esp. Dependency Inversion
- Map external data to internal entities
- You must ensure that the project is storybook-first: components are always built and validated in isolation before being integrated into the app

## 2.2. Naming Conventions

**Component & Hook Naming:**

- ComponentName.tsx for components
- useFeature.ts for hooks
- feature.service.ts for services
- Folders in PascalCase, with index.ts
- Use Component.stories.tsx file colocated with the component

## 2.3. Key Code Conventions

**Linting & Formatting:**

- Use ESLint for static code analysis and error detection
- Use Prettier for automatic and consistent code formatting
- Configure and honor .eslintrc and .prettierrc configurations

**File Import Order:**

1. React/core libs
2. Third-party libs
3. Project services/hooks
4. Shared utils
5. Relative imports

**Coding Standards:**

- Use TypeScript only, no any
- Prefer interface or type
- Use ?., ??, and const
- Avoid magic strings
- Favor named exports
- Follow casing conventions (PascalCase, camelCase)
- Implement components in isolation
- Write stories with different states/variants

**Use folder-per-component structure:**

```text
Button/
├── Button.tsx
├── Button.test.tsx
├── Button.stories.tsx
└── Button.module.scss
```

## 2.4. Commenting Policy

- Code commented and documented as part of Definition of Done
