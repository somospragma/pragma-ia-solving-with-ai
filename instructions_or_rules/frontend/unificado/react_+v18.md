# Instructions.md — React + SASS + Vite + TypeScript Project

```yaml
name: "React + SASS + Vite + TypeScript Project"
version: "2.0"
applies_to: ["frontend", "react", "typescript"]
status: "Active"
authors:
  - name: "Jhon Hernandez"
    email: "jhon.hernandez@pragma.com.co"
  - name: "Esteban Cadavid"
    email: "esteban.cadavid@pragma.com.co"
  - name: "Santiago Betancur"
    email: "santiago.betancur@pragma.com.co"
tags: ["react", "typescript", "vite", "sass", "zustand", "hexagonal-architecture"]
last_updated: "2025-09-16"
```

---

## 1. General Context

### 1.1. Project Context

### 1.2. Technology Stack

- React > 18 — UI library
- TypeScript — Type safety and type-level design
- Vite — Fast bundler and dev server
- SASS — CSS preprocessor with BEM and variables
- React Testing Library (RTL) — Testing framework for React components
- Zustand — Lightweight global state management
- Axios — Promise-based HTTP client

### 1.3. Custom Project Sections

**Success Checklist:**

- Template initialized
- Feature scope validated
- DoR approved
- DoD met before PR
- Clean, testable, decoupled logic

**Emergency Protocol:**

- Not sure? Ask first
- Failing test? Fix before PR
- Missing tests? Block merge

---

## 2. Code Guidelines & Standards

### 2.1. Design Principles & Best Practices

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

### 2.2. Naming Conventions

**Component & Hook Naming:**

- ComponentName.tsx for components
- useFeature.ts for hooks
- feature.service.ts for services
- Folders in PascalCase, with index.ts

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

### 2.4. Commenting Policy

- Code commented and documented as part of Definition of Done

---

## 3. Technology-Specific Guidelines

### 3.1. Architecture & Directory Structure

**Atomic Design Methodology:**

Organize UI components following atomic design principles:

- **Atoms:** Basic, indivisible UI elements (buttons, inputs, labels, icons)
- **Molecules:** Simple combinations of atoms that work together as a functional unit (search boxes, form fields)
- **Organisms:** Complex UI components made of molecules and atoms (headers, navigation bars)
- **Templates:** Page-level layouts that define the structure and placement of organisms, molecules, and atoms
- **Pages:** Specific instances of templates with real content

**Clean Architecture Structure:**

#### src/config/

Global app configuration:

- Environment variables
- Route setup
- Authentication
- Middlewares and initial settings

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

**Use folder-per-component structure:**

```text
Button/
├── Button.tsx
├── Button.test.tsx
└── Button.module.scss
```

- Co-locate styles with components
- Place files (components, styles, tests) in component folders

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

**Testing:**

- Use RTL + Vitest
- Focus on integration tests
- Aim for ≥ 80% coverage
- Include A11Y tests

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

- Avoid dangerouslySetInnerHTML
- Sanitize everything
- Store tokens safely, prefer cookies (HttpOnly)
- Always limit the input maxlength
- Ensure HTTPS in production environments with proper SSL/TLS certificates

#### 4.4.2. Compliance Requirements

### 4.5. Performance & Optimization

**Performance:**

- Lazy load components (React.lazy)
- Memoize (React.memo, useMemo)
- Debounce heavy UI events
- Skeleton UI while is loading
- Implement image optimization using modern formats (WebP, AVIF) and compression techniques
- Apply minification and obfuscation for CSS and JavaScript files in production builds

### 4.6. Accessibility (A11Y)

**Accessibility (A11Y):**

- Use semantic HTML
- Add ARIA labels/roles
- Keyboard support

### 4.7. SEO & Metadata

**SEO Requirements:**

- Implement proper HTML5 semantic markup for improved accessibility and SEO
- Configure essential meta tags including title, description and others

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

### 5.3. Git Workflow

---

## 📢 Final Notes for the AI Agent

### Agent's Role & Capabilities

You are a highly skilled frontend engineer with over 10 years of experience, operating at a Staff Engineer level. You are an expert in React and TypeScript, with deep knowledge of modern frontend architecture, component design, performance optimization, and developer experience. Your responsibility is to deliver world-class, maintainable, scalable, and accessible code that aligns with the project's specific technical goals.

This template is designed for scalable, maintainable, modular React apps. All code should aim for clarity, performance, and reusability.
