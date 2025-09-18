# Instructions.md — Next.js Project

```yaml
name: "Next.js Project"
version: "2.0"
applies_to: ["frontend", "nextjs", "react", "typescript"]
status: "Active"
authors:
  - name: "Burke Holland"
    email: "burkeholland@gmail.com"
  - name: "Santiago Betancur"
    email: "santiago.betancur@pragma.com.co"
tags: ["nextjs", "react", "typescript", "app-router", "ssr", "ssg"]
last_updated: "2025-09-16"
```

---

## 1. General Context

### 1.1. Project Context

This is a Next.js project using the modern **App Router** (`app/` directory) architecture. Use the `app/` directory for all new projects. Prefer it over the legacy `pages/` directory.

### 1.2. Technology Stack

### 1.3. Custom Project Sections

**Always use the latest documentation and guides:**

- For every Next.js related request, begin by searching for the most current Next.js documentation, guides, and examples.
- Use the following tools to fetch and search documentation if they are available:
  - `resolve_library_id` to resolve the package/library name in the docs.
  - `get_library_docs` for up to date documentation.

**Avoid Unnecessary Example Files:**
Do not create example/demo files (like ModalExample.tsx) in the main codebase unless the user specifically requests a live example, Storybook story, or explicit documentation component. Keep the repository clean and production-focused by default.

---

## 2. Code Guidelines & Standards

### 2.1. Design Principles & Best Practices

- **TypeScript:** Use TypeScript for all code. Enable `strict` mode in `tsconfig.json`.
- **ESLint & Prettier:** Enforce code style and linting. Use the official Next.js ESLint config.
- **Performance:**
  - Use built-in Image and Font optimization.
  - Use Suspense and loading states for async data.
  - Avoid large client bundles; keep most logic in Server Components.
- **Security:**
  - Sanitize all user input.
  - Use HTTPS in production.
  - Set secure HTTP headers.
- **Accessibility:** Use semantic HTML and ARIA attributes. Test with screen readers.
- **Documentation:**
  - Write clear README and code comments.
  - Document public APIs and components.

### 2.2. Naming Conventions

- **Folders:** `kebab-case` (e.g., `user-profile/`)
- **Files:** `PascalCase` for components, `camelCase` for utilities/hooks, `kebab-case` for static assets
- **Component Files:** Use `PascalCase` for component files and exports (e.g., `UserCard.tsx`)
- **Hook Files:** Use `camelCase` for hooks (e.g., `useUser.ts`)
- **Static Assets:** Use `snake_case` or `kebab-case` for static assets (e.g., `logo_dark.svg`)
- **Context Providers:** Name context providers as `XyzProvider` (e.g., `ThemeProvider`)
- **Variables/Functions:** `camelCase`
- **Types/Interfaces:** `PascalCase`
- **Constants:** `UPPER_SNAKE_CASE`

### 2.3. Key Code Conventions

**Component Best Practices:**

- **Component Types:**
  - **Server Components** (default): For data fetching, heavy logic, and non-interactive UI.
  - **Client Components:** Add `'use client'` at the top. Use for interactivity, state, or browser APIs.
- **When to Create a Component:**
  - If a UI pattern is reused more than once.
  - If a section of a page is complex or self-contained.
  - If it improves readability or testability.
- **File Naming:**
  - Match the component name to the file name.
  - For single-export files, default export the component.
  - For multiple related components, use an `index.ts` barrel file.
- **Component Location:**
  - Place shared components in `components/`.
  - Place route-specific components inside the relevant route folder.
- **Props:**
  - Use TypeScript interfaces for props.
  - Prefer explicit prop types and default values.

### 2.4. Commenting Policy

- Write clear README and code comments.
- Document public APIs and components.

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

**Next.js App Router Structure:**

**Use the `app/` directory** (App Router) for all new projects. Prefer it over the legacy `pages/` directory.

**Top-level folders:**

- `app/` — Routing, layouts, pages, and route handlers
- `public/` — Static assets (images, fonts, etc.)
- `lib/` — Shared utilities, API clients, and logic
- `components/` — Reusable UI components
- `contexts/` — React context providers
- `styles/` — Global and modular stylesheets
- `hooks/` — Custom React hooks
- `types/` — TypeScript type definitions

**Advanced Patterns:**

- **Colocation:** Place files (components, styles, tests) near where they are used, but avoid deeply nested structures.
- **Route Groups:** Use parentheses (e.g., `(admin)`) to group routes without affecting the URL path.
- **Private Folders:** Prefix with `_` (e.g., `_internal`) to opt out of routing and signal implementation details.
- **Feature Folders:** For large apps, group by feature (e.g., `app/dashboard/`, `app/auth/`).
- **Use `src/`** (optional): Place all source code in `src/` to separate from config files.

### 3.2. File & Component Structure

**Server and Client Component Integration (App Router):**

**Never use `next/dynamic` with `{ ssr: false }` inside a Server Component.** This is not supported and will cause a build/runtime error.

**Correct Approach:**

- If you need to use a Client Component (e.g., a component that uses hooks, browser APIs, or client-only libraries) inside a Server Component, you must:
  1. Move all client-only logic/UI into a dedicated Client Component (with `'use client'` at the top).
  2. Import and use that Client Component directly in the Server Component (no need for `next/dynamic`).
  3. If you need to compose multiple client-only elements (e.g., a navbar with a profile dropdown), create a single Client Component that contains all of them.

**Example:**

```tsx
// Server Component
import DashboardNavbar from '@/components/DashboardNavbar';

export default async function DashboardPage() {
  // ...server logic...
  return (
    <>
      <DashboardNavbar /> {/* This is a Client Component */}
      {/* ...rest of server-rendered page... */}
    </>
  );
}
```

**Why:**

- Server Components cannot use client-only features or dynamic imports with SSR disabled.
- Client Components can be rendered inside Server Components, but not the other way around.

**Summary:**
Always move client-only UI into a Client Component and import it directly in your Server Component. Never use `next/dynamic` with `{ ssr: false }` in a Server Component.

### 3.3. Dependencies & Package Management

### 3.4. API & Services Integration

**API Routes (Route Handlers):**

- **Prefer API Routes over Edge Functions** unless you need ultra-low latency or geographic distribution.
- **Location:** Place API routes in `app/api/` (e.g., `app/api/users/route.ts`).
- **HTTP Methods:** Export async functions named after HTTP verbs (`GET`, `POST`, etc.).
- **Request/Response:** Use the Web `Request` and `Response` APIs. Use `NextRequest`/`NextResponse` for advanced features.
- **Dynamic Segments:** Use `[param]` for dynamic API routes (e.g., `app/api/users/[id]/route.ts`).
- **Validation:** Always validate and sanitize input. Use libraries like `zod` or `yup`.
- **Error Handling:** Return appropriate HTTP status codes and error messages.
- **Authentication:** Protect sensitive routes using middleware or server-side session checks.

### 3.5. Environment Configuration

- **Environment Variables:** Store secrets in `.env.local`. Never commit secrets to version control.

### 3.6. State Management

### 3.7. Styling & Design System

**CSS Framework & Methodology:**

- Use Tailwind CSS or BEM methodology for consistent styling structure
- Implement responsive design principles for optimal multi-device experience
- Follow mobile-first approach in responsive design implementation
- Co-locate styles with components

---

## 4. Quality & Engineering Excellence

### 4.1. Testing Strategy & Implementation

- **Test Coverage Requirements:** Maintain minimum test coverage of 80% across the application
- **Testing:** Use Jest, React Testing Library, or Playwright. Write tests for all critical logic and components.
- **Co-locate tests with components** (e.g., `UserCard.test.tsx`).

### 4.2. Quality Gates & Acceptance Criteria

### 4.3. Error Handling & Validation

- **Validation:** Always validate and sanitize input. Use libraries like `zod` or `yup`.
- **Error Handling:** Return appropriate HTTP status codes and error messages.

### 4.4. Security & Compliance

#### 4.4.1. Data Protection

- Sanitize all user input.
- Use HTTPS in production.
- Set secure HTTP headers.

#### 4.4.2. Compliance Requirements

### 4.5. Performance & Optimization

**Performance Optimization:**

- Use built-in Image and Font optimization with modern formats for images (WebP, AVIF)
- Apply minification and obfuscation for CSS and JavaScript files in production builds
- Use Suspense and loading states for async data
- Avoid large client bundles; keep most logic in Server Components

### 4.6. Accessibility (A11Y)

- Implement proper HTML5 semantic and ARIA attributes. Test with screen readers.

### 4.7. SEO & Metadata

**SEO Requirements:**

- Configure essential meta tags including title, description and others
- Leverage Next.js built-in metadata API for dynamic meta tag management
- Use Next.js Image component for automatic optimization and better Core Web Vitals

---

## 📢 Final Notes for the AI Agent

### Agent's Role & Capabilities

- Always use the latest documentation and guides for Next.js
- Never use `next/dynamic` with `{ ssr: false }` inside a Server Component
- Keep the repository clean and production-focused by default
- Avoid creating unnecessary example files unless explicitly requested
