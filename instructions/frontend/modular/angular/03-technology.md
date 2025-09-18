# Technology-Specific Guidelines

## 3.1. Architecture & Directory Structure

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

## 3.2. File & Component Structure

## 3.3. Dependencies & Package Management

- When installing a package, install an exact version on production dependencies (field dependencies) to ensure consistency, reliability, and reproducibility of builds through developer machines and CI pipelines

## 3.4. API & Services Integration

**Angular-Specific Guidelines:**

- Use `HttpInterceptor` for cross-cutting concerns (auth, logging, error handling)
- Use Angular's DI system and the inject function for service injection

## 3.5. Environment Configuration

## 3.6. State Management

- Leverage Angular's signals system for efficient state management and reactive programming
- Use async pipe for observables in templates

## 3.7. Styling & Design Guidelines

**CSS Framework & Methodology:**

- Use Tailwind CSS or BEM methodology for consistent styling structure
- Implement responsive design principles for optimal multi-device experience
- Follow mobile-first approach in responsive design implementation
