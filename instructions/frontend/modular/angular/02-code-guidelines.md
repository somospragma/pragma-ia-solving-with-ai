# Code Guidelines & Standards

## 2.1. Design Principles & Best Practices

**Key Principles:**

- Apply immutability and pure functions where applicable
- Favor component composition for modularity
- Always keep in mind the single responsibility principle to keep things simple
- Prefers simplicity over unnecessary abstraction ("You Ain't Gonna Need It")
- Avoid external dependencies if Angular already provides a native solution

**TypeScript & Angular Guidelines:**

- Define data structures with interfaces for type safety
- Avoid any type, utilize the type system fully
- Use Typescript Utility Types for type transformations
- Organize files: imports, definition, implementation
- Use template strings for multi-line literals
- Utilize optional chaining and nullish coalescing
- Use standalone components when applicable
- Leverage Angular's signals system for efficient state management and reactive programming
- Use the inject function for injecting services directly within component, directive or service logic
- Use access modifiers to enable encapsulation by controlling the visibility and accessibility of class members
- Use TypeScript import aliases
- Prefer async/await syntax over Promise when applicable

## 2.2. Naming Conventions

**File Naming Conventions:**

- `.component.ts` for Components
- `-page.component.ts` for Pages
- `.service.ts` for Services
- `.module.ts` for Modules
- `.directive.ts` for Directives
- `.pipe.ts` for Pipes
- `.spec.ts` for Tests
- `-constant.ts` for global or domain constants
- All files use kebab-case

**Variable & Code Naming:**

- Use meaningful variable names (e.g., isActive, hasPermission)
- Use kebab-case for file names (e.g., user-profile.component.ts)
- Prefer named exports for components, services, and utilities

## 2.3. Key Code Conventions

<!-- ⚪ REEMPLAZAR POR PRETTIER + ESLINT -->

**Code Style:**

- Use single quotes for string literals
- Indent with 2 spaces
- Ensure clean code with no trailing whitespace
- Use const for immutable variables
- Use template strings for string interpolation
- Honor .prettierrc configuration
- Avoid using string and magic numbers, use variables or constants

**Import Order:**

1. Angular core and common modules
2. RxJS modules
3. Other Angular modules
4. Application core imports
5. Shared module imports
6. Environment-specific imports
7. Relative path imports

## 2.4. Commenting Policy

- Add TSDoc comments to services, directives, pipes and utilities
- Avoid obvious comments; document why, not what
