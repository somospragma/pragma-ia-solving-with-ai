# Instructions.md — Angular Project

```yaml
name: "Angular Project"
version: "2.0"
applies_to: ["frontend", "angular", "typescript"]
status: "Active"
authors:
  - name: "Jaime Gallo"
    email: "jaime.gallom@pragma.com.co"
  - name: "Cristian Otálora"
    email: "cristian.otalora@pragma.com.co"
  - name: "Esteban García"
    email: "esteban.garcia@pragma.com.co"
tags: ["angular", "typescript", "tailwind", "sass", "standalone-components", "signals"]
last_updated: "2025-09-16"
```

---

## 1. General Context

### 1.1. Project Context

[Dominio de negocio, propósito, usuarios, casos de uso]

### 1.2. Technology Stack

### 1.3. Custom Project Sections

---

## 2. Code Guidelines & Standards

### 2.1. Design Principles & Best Practices

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

### 2.2. Naming Conventions

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

### 2.3. Key Code Conventions

**Linting & Formatting:**

- Use ESLint for static code analysis and error detection
- Use Prettier for automatic and consistent code formatting
- Configure and honor .eslintrc and .prettierrc configurations

**Code Style:**

- Use single quotes for string literals
- Indent with 2 spaces
- Ensure clean code with no trailing whitespace
- Use const for immutable variables
- Use template strings for string interpolation
- Avoid using string and magic numbers, use variables or constants

**Import Order:**

1. Angular core and common modules
2. RxJS modules
3. Other Angular modules
4. Application core imports
5. Shared module imports
6. Environment-specific imports
7. Relative path imports

### 2.4. Commenting Policy

- Add TSDoc comments to services, directives, pipes and utilities
- Avoid obvious comments; document why, not what

---

## 3. Technology-Specific Guidelines

### 3.1. Architecture & Directory Structure

**LIFT Principle (mandatory):**

- **Locate:** Code should be intuitive to find. A developer should be able to find what they need in seconds
- **Identify:** File names should clearly indicate their purpose and content
- **Flat:** Keep the folder structure as flat as possible for as long as possible. Avoid deep nesting
- **Try to be DRY:** Don't repeat yourself — extract common functionality into shared modules, create reusable components to eliminate code duplication

**Atomic Design:**
Organize UI components following atomic design methodology:

- **Atoms:** Basic, indivisible UI elements (buttons, inputs, labels, icons)
- **Molecules:** Simple combinations of atoms that work together as a functional unit (search boxes, form fields)
- **Organisms:** Complex UI components made of molecules and atoms (headers, navigation bars)
- **Templates:** Page-level layouts that define the structure and placement of organisms, molecules, and atoms
- **Pages:** Specific instances of templates with real content

### 3.2. File & Component Structure

### 3.3. Dependencies & Package Management

- When installing a package, install an exact version on production dependencies (field dependencies) to ensure consistency, reliability, and reproducibility of builds through developer machines and CI pipelines

### 3.4. API & Services Integration

**Angular-Specific Guidelines:**

- Use `HttpInterceptor` for cross-cutting concerns (auth, logging, error handling)
- Use Angular's DI system and the inject function for service injection

### 3.5. Environment Configuration

### 3.6. State Management

- Leverage Angular's signals system for efficient state management and reactive programming
- Use async pipe for observables in templates

### 3.7. Styling & Design Guidelines

**CSS Framework & Methodology:**

- Use Tailwind CSS or BEM methodology for consistent styling structure
- Implement responsive design principles for optimal multi-device experience
- Follow mobile-first approach in responsive design implementation

---

## 4. Quality & Engineering Excellence

### 4.1. Testing Strategy & Implementation

**Test Coverage Requirements:**

- Maintain minimum test coverage of 80% across the application
- Include unit tests for components, services, and utilities
- Implement integration tests for critical user flows

### 4.2. Quality Gates & Acceptance Criteria

### 4.3. Error Handling & Validation

**Error Handling and Validation:**

- Use proper error handling in services and components
- Use custom error types or factories
- Implement Angular form validation or custom validators

### 4.4. Security & Compliance

#### 4.4.1. Data Protection

**Security:**

- Prevent XSS with Angular's sanitization; avoid using innerHTML
- Sanitize dynamic content with built-in tools
- Avoid writing console.log statements to prevent information disclosure
- Ensure HTTPS in production environments with proper SSL/TLS certificates

#### 4.4.2. Compliance Requirements

### 4.5. Performance & Optimization

**Performance Optimization:**

- Optimize *ngFor with trackBy functions
- Use pure pipes for expensive computations
- Avoid direct DOM manipulation; use Angular's templating system
- Optimize rendering performance by deferring non-essential views
- Use Angular's signals system to manage state efficiently and reduce unnecessary re-renders
- Use the NgOptimizedImage directive to enhance image loading and performance
- Avoid computed properties (e.g. get prop() { }) when accessing variables from a HTML view. Prefer signals or observables
- Unsubscribe from observables using Angular lifecycle ngOnDestroy if there are not clean-up automatically
- Utilize deferrable views for optimizing component rendering, deferring non-critical views until necessary
- Implement image optimization using modern formats (WebP, AVIF) and compression techniques
- Apply minification and obfuscation for CSS and JavaScript files in production builds

**Web Vitals:**

- Focus on optimizing Web Vitals like LCP, INP, and CLS

### 4.6. Accessibility (A11Y)

- Ensure accessibility with semantic HTML and ARIA labels

### 4.7. SEO & Metadata

**SEO Requirements:**

- Implement proper HTML5 semantic markup for improved accessibility and SEO
- Configure essential meta tags including title, description and others

---

## 5. Process Requirements

### 5.1. Definition of Ready (DoR)

### 5.2. Definition of Done (DoD)

### 5.3. Git Workflow

**Git Flow Management:**
Follow this strict branching model for all projects:

- **main:** Production-ready code only. Direct commits are forbidden. All changes must come through pull requests from release or hotfix branches
- **develop:** Integration branch for features. Contains the latest development changes for the next release. All feature branches must be created from and merged back into develop
- **feature/[feature-name]:** Development of specific features. Must be created from develop and merged back into develop via pull request. Use descriptive names (e.g., feature/user-authentication, feature/dashboard-widgets)

---

## 📢 Final Notes for the AI Agent

### Agent's Role & Capabilities

- Expert in Angular, Tailwind, SASS, and TypeScript, focusing on scalable web development. Follow Angular's official documentation for best practices in Components, Services, and Modules.
- Provide clear, precise Angular and TypeScript examples
- Focus on reusability and modularity
- Follow Angular's style guide
- Optimize with Angular's best practices
- Implement lazy loading for feature modules and routes
- Implement route guards (`CanActivate`, `CanDeactivate`) instead of scattered logic
