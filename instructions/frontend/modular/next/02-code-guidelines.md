# Code Guidelines & Standards

## 2.1. Design Principles & Best Practices

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

## 2.2. Naming Conventions

- **Folders:** `kebab-case` (e.g., `user-profile/`)
- **Files:** `PascalCase` for components, `camelCase` for utilities/hooks, `kebab-case` for static assets
- **Component Files:** Use `PascalCase` for component files and exports (e.g., `UserCard.tsx`)
- **Hook Files:** Use `camelCase` for hooks (e.g., `useUser.ts`)
- **Static Assets:** Use `snake_case` or `kebab-case` for static assets (e.g., `logo_dark.svg`)
- **Context Providers:** Name context providers as `XyzProvider` (e.g., `ThemeProvider`)
- **Variables/Functions:** `camelCase`
- **Types/Interfaces:** `PascalCase`
- **Constants:** `UPPER_SNAKE_CASE`

## 2.3. Key Code Conventions

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

## 2.4. Commenting Policy

- Write clear README and code comments.
- Document public APIs and components.
