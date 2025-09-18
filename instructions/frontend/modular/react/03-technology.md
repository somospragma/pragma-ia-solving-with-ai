# Technology-Specific Guidelines

## 3.1. Architecture & Directory Structure

**Atomic Design Methodology:**

Organize UI components following atomic design principles:

- **Atoms:** Basic, indivisible UI elements (buttons, inputs, labels, icons)
- **Molecules:** Simple combinations of atoms that work together as a functional unit (search boxes, form fields)
- **Organisms:** Complex UI components made of molecules and atoms (headers, navigation bars)
- **Templates:** Page-level layouts that define the structure and placement of organisms, molecules, and atoms
- **Pages:** Specific instances of templates with real content

**Clean Architecture Structure:**

### src/config/

Global app configuration:

- Environment variables
- Route setup
- Authentication
- Middlewares and initial settings

### src/domain/

- Contains pure business logic
- Holds **frontend entities**, interfaces, and use cases
- **Key rule**: no matter where the data comes from, always work with the entities defined here
- The domain layer has no knowledge of APIs, databases, or external libraries

### src/infrastructure/

- Real implementations of the interfaces defined in the domain layer
- **Gateways**: each gateway exposes specific functions to access APIs or other data sources
- **In the same gateway file**, data from external sources (DTOs) must be mapped into frontend entities
- Includes: DTOs, Mappers, Adapters for external services
- **Never** expose DTOs directly to `presentation` or `domain` — always return domain entities

### src/presentation/

- UI: components, pages, styles, and state management
- **Features**: each feature includes its own hooks and UI logic
- Hooks **directly inject** the required gateway (using its domain interface) without complex DI containers
- Hooks **only work with frontend entities**, never with DTOs or external structures
- Hooks may handle local or global state (e.g., Zustand, Redux, etc.), but must receive data already mapped by the gateway

### src/shared/

- Utilities, constants, and types **truly reusable** across the application
- **Key rule**: If a type or utility is specific to `infrastructure` or `presentation`, it must live **inside that layer**
- Example: a helper for a gateway belongs in `infrastructure/` next to that gateway, not in `shared`

### public/

Static assets and SEO metadata

### dist/

Build output

### coverage/

Test coverage reports

## 3.2. File & Component Structure

**Use folder-per-component structure:**

```text
Button/
├── Button.tsx
├── Button.test.tsx
└── Button.module.scss
```

- Co-locate styles with components
- Place files (components, styles, tests) in component folders

## 3.3. Dependencies & Package Management

## 3.4. API & Services Integration

## 3.5. Environment Configuration

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

## 3.6. State Management

**State Management:**

- useState / useReducer for local
- Zustand (slices) for global
- React Query for server state

## 3.7. Routing & Navigation

- Use react-router-dom
- Add ProtectedRoute when needed

## 3.8. Styling & Design System

**CSS Framework & Methodology:**

- Use Tailwind CSS or BEM/SASS modules for consistent styling structure
- Implement responsive design principles for optimal multi-device experience
- Follow mobile-first approach in responsive design implementation
- Co-locate styles with components
