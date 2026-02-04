# Instructions.md — React + SASS + Vite + TypeScript + Storybook Project

```yaml
name: "React + SASS + Vite + TypeScript + Storybook Project"
version: "2.0"
applies_to: ["frontend", "react", "storybook", "typescript"]
status: "Active"
authors:
  - name: "Jhon Hernandez"
    email: "jhon.hernandez@pragma.com.co"
  - name: "Esteban Cadavid"
    email: "esteban.cadavid@pragma.com.co"
  - name: "Santiago Betancur"
    email: "santiago.betancur@pragma.com.co"
tags: ["react", "typescript", "vite", "sass", "storybook", "zustand", "component-driven"]
last_updated: "2025-09-16"
```

---

## 1. General Context

### 1.1. Project Context

### 1.2. Technology Stack

This template is optimized for projects using the following technologies:

- React > 18 — UI library
- TypeScript — Type safety and type-level design
- Vite — Fast bundler and dev server
- SASS — CSS preprocessor with BEM and variables
- React Testing Library (RTL) — Testing framework for React components
- Zustand — Lightweight global state management
- Axios — Promise-based HTTP client
- Storybook 8+ — UI explorer and component documentation

### 1.3. Custom Project Sections

**Success Checklist:**

- Template initialized
- Feature scope validated
- DoR approved
- DoD met before PR
- Clean, testable, decoupled logic
- All UI components appear correctly in Storybook
- Documentation is auto-generated in Storybook Docs tab

**Emergency Protocol:**

- Not sure? Ask first
- Failing test? Fix before PR
- Missing tests? Block merge

---

## 2. Code Guidelines & Standards

### 2.1. Design Principles & Best Practices

**Core Architecture Principles:**

- Storybook is the source of truth for UI components
- Storybook stories act as living documentation and test cases
- Follow SOLID, esp. Dependency Inversion
- Map external data to internal entities
- You must ensure that the project is storybook-first: components are always built and validated in isolation before being integrated into the app

### 2.2. Naming Conventions

**Component & Hook Naming:**

- ComponentName.tsx for components
- useFeature.ts for hooks
- feature.service.ts for services
- Folders in PascalCase, with index.ts
- Use Component.stories.tsx file colocated with the component

### 2.3. Key Code Conventions

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

### 2.4. Commenting Policy

- Code commented and documented as part of Definition of Done

---

## 3. Technology-Specific Guidelines

### 3.1. Architecture & Directory Structure

**Atomic Design Methodology:**

- **Atoms**: Basic building blocks (buttons, inputs, labels)
- **Molecules**: Groups of atoms (form fields, search boxes)
- **Organisms**: Complex components (headers, forms, product lists)
- **Templates**: Page layouts without content
- **Pages**: Specific instances of templates with real content

#### src/config/

Global app configuration:

- Environment variables
- Route setup
- Authentication
- Middlewares and initial settings

#### .storybook/

- main.ts (addons, frameworks)
- preview.ts (decorators, parameters, themes, global styles)
- manager.ts (UI customization if needed)

#### src/domain/

- Contains pure business logic
- Holds **frontend entities**, interfaces, and use cases
- **Key rule**: no matter where the data comes from, always work with the entities defined here
- The domain layer has no knowledge of APIs, databases, or external libraries

#### src/infrastructure/

- Real implementations of the interfaces defined in the domain layer
- **Gateways**: each gateway exposes specific functions to access APIs or other data sources
- **In the same gateway file**, data from external sources (DTOs) must be mapped into frontend entities
- Includes: DTOs, Mappers, Adapters for external services
- **Never** expose DTOs directly to `presentation` or `domain` — always return domain entities

#### src/presentation/

- UI: components, pages, styles, and state management
- **Features**: each feature includes its own hooks and UI logic
- Hooks **directly inject** the required gateway (using its domain interface) without complex DI containers
- Hooks **only work with frontend entities**, never with DTOs or external structures
- Hooks may handle local or global state (e.g., Zustand, Redux, etc.), but must receive data already mapped by the gateway

#### src/shared/

- Utilities, constants, and types **truly reusable** across the application
- **Key rule**: If a type or utility is specific to `infrastructure` or `presentation`, it must live **inside that layer**
- Example: a helper for a gateway belongs in `infrastructure/` next to that gateway, not in `shared`

#### public/

Static assets and SEO metadata

#### dist/

Build output

#### coverage/

Test coverage reports

### 3.2. File & Component Structure

**Storybook Guidelines:**

- Stories must cover: Default (base state), Variants (different props), Edge cases (empty, error states), Accessibility states (focus, disabled)
- Wrap stories with providers if needed (ThemeProvider, i18n, Zustand mock)
- Every new component must include .stories.tsx before being merged

### 3.3. Dependencies & Package Management

### 3.4. API & Services Integration

### 3.5. Environment Configuration

**Environment Variables:**
Location: /src/config/environment/

- .env.development: Local dev setup (never committed)
- .env.production: Deployment config
- .env.test: Dummy values for testing

**Ensure:**

- PUBLIC_ENV_AUTH_REDIRECT_URI = <http://localhost:3000> in development
- No real data in test envs
- Use .env properly
- Always use HTTPS endpoints

### 3.6. State Management

**State Management:**

- useState / useReducer for local
- Zustand (slices) for global
- React Query for server state

### 3.7. Routing & Navigation

- Use react-router-dom
- Add ProtectedRoute when needed

### 3.8. Styling & Design System

**CSS Framework & Methodology:**

- Use Tailwind CSS or BEM/SASS modules for consistent styling structure
- Implement responsive design principles for optimal multi-device experience
- Follow mobile-first approach in responsive design implementation
- Co-locate styles with components

---

## 4. Quality & Engineering Excellence

### 4.1. Testing Strategy & Implementation

**Testing Requirements:**

- Use RTL + Vitest
- Focus on integration tests
- **Maintain ≥ 80% test coverage** as a minimum requirement
- Include A11Y tests
- Test component stories in Storybook

### 4.2. Quality Gates & Acceptance Criteria

**Before Coding - Definition of Ready:**

- UI specs (Figma/tokens)
- API contract ready
- Task plan and scope
- Consider SEO, edge cases, accessibility

**After Coding - Definition of Done:**

- Feature complete
- All tests pass
- Lint clean
- A11Y/SEO validated
- Code commented and documented

### 4.3. Error Handling & Validation

**Error Handling:**

- Global error boundaries
- Contextual messages
- Fallback UIs

**Forms & Validation:**

- Use react-hook-form + zod
- Validate and sanitize inputs

### 4.4. Security & Compliance

#### 4.4.1. Data Protection

**Security:**

- **HTTPS in production**: Mandatory SSL/TLS certificates for all production environments
- Avoid dangerouslySetInnerHTML
- Sanitize everything
- Store tokens safely, prefer cookies (HttpOnly)
- Always limit the input maxlength
- Input validation and sanitization to prevent XSS attacks

#### 4.4.2. Compliance Requirements

### 4.5. Performance & Optimization

**Performance:**

- **Image optimization**: Use modern formats (WebP, AVIF) with fallbacks
- **Minification and obfuscation**: CSS and JavaScript files must be minified in production
- Lazy load components (React.lazy)
- Memoize (React.memo, useMemo)
- Debounce heavy UI events
- Skeleton UI while loading
- Bundle analysis and code splitting optimization

### 4.6. SEO & Accessibility

**SEO Requirements:**

- Implement proper HTML5 semantic markup for improved accessibility and SEO
- Configure essential meta tags including title, description and others

**Accessibility (A11Y):**

- Use semantic HTML
- Add ARIA labels/roles
- Keyboard support

---

## 5. Process Requirements

### 5.1. Definition of Ready (DoR)

**Validate Definition of Ready:**

- UI specs (Figma/tokens)
- API contract ready
- Task plan and scope
- Consider SEO, edge cases, accessibility

### 5.2. Definition of Done (DoD)

**Validate Definition of Done:**

- Feature complete
- All tests pass
- Lint clean
- A11Y/SEO validated
- Code commented and documented

---

## 📢 Final Notes for the AI Agent

### Agent's Role & Capabilities

You are a highly skilled frontend engineer with over 10 years of experience, operating at a Staff Engineer level. You are an expert in React, TypeScript, and component-driven development, with deep knowledge of Storybook, modern frontend architecture, design systems, performance optimization, and developer experience. Your responsibility is to deliver reusable UI components with excellent documentation and stories. You prioritize developer experience (DX), accessibility (A11Y), scalability, and testability.

This template is designed for scalable, maintainable, modular React apps. All code should aim for clarity, performance, and reusability.
