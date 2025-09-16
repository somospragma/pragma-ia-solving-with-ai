# Instructions.md — flutter best practices

```yaml
name: "flutter best practices"
version: "1.0"
applies_to: ["mobile", "flutter", "dart"]
status: "Active"
authors:
  - name: "darry.morales"
    email: "darry.morales@pragma.com.co"
tags: ["Mobile","Flutter", "Dart"]
last_updated: "2025-09-15"
```

-----

## 1\. General Context

### 1.1. Project Context

### 1.2. Technology Stack

  - **Framework:** Flutter
  - **Language:** Dart
  - **State Management:** Flutter BLoC
  - **Dependency Injection:** get\_it
  - **Testing:** bloc\_test, Mocktail
  - **Code Generation:** json\_serializable, freezed

### 1.3. Custom Project Sections


-----

## 2\. Code Guidelines & Standards

### 2.1. Design Principles & Best Practices

  - **SOLID:** All code must adhere to the five SOLID principles to ensure it is maintainable, scalable, and testable.
  - **Clean Code:** Write readable, simple, and self-documenting code. Code should be an asset, not a liability.
  - **Decomposition:** Widgets and classes should have a single responsibility. Avoid massive widgets by breaking them down into smaller, reusable components.

### 2.2. Naming Conventions

  - **Files:** Use `snake_case` (e.g., `user_repository.dart`).
  - **Classes & Enums:** Use `PascalCase` (e.g., `class AuthenticationService`).
  - **Variables, Methods & Parameters:** Use `camelCase` (e.g., `final String userName`).
  - **Constants:** Use `camelCase` or `UPPER_SNAKE_CASE` for top-level constants (e.g., `const maxRetries` or `const MAX_RETRIES`).

### 2.3. Key Code Conventions

  - **Immutability:** Data models and states must be immutable. All properties should be `final`.
  - **Use `const`:** Use `const` constructors for widgets and objects wherever possible to improve performance.
  - **Avoid Magic Values:** Do not use hardcoded strings or numbers. Define them as constants in a centralized location.

### 2.4. Commenting Policy

  - **Purpose:** Comments should explain *why* something is done, not *what* is being done. The code itself should be clear enough to explain the 'what'.
  - **Documentation Comments:** Use `///` for Dart Doc comments on all public classes and methods to explain their purpose, parameters, and return values.
  - **No Commented-Out Code:** Dead or commented-out code must be removed before merging. Use Git for version history.

-----

## 3\. Technology-Specific Guidelines

### 3.1. Architecture & Directory Structure

  - **Clean Architecture:** The project follows Clean Architecture principles, separating logic into three layers: **Presentation**, **Domain**, and **Data**.
  - **Dependency Rule:** Dependencies must only flow inwards: `Presentation` → `Domain` → `Data`. The Domain layer must remain pure Dart with no Flutter dependencies.
  - **Directory Structure:** The project directories must reflect these layers (e.g., `/lib/features/[feature_name]/data`, `/lib/features/[feature_name]/domain`, `/lib/features/[feature_name]/presentation`).

### 3.2. File & Component Structure

  - **Data Models:** All data models must be immutable. They must include `copyWith`, `fromJson`, and `toJson` methods. Prefer using code generation tools like `json_serializable` or `freezed` to automate this.
  - **Widgets:** A widget file should ideally contain a single public widget. Private helper widgets can be defined within the same file.

### 3.3. Dependencies & Package Management

  - **Versioning:** Pin package versions in `pubspec.yaml` to avoid unexpected breaking changes. Use version ranges (`^x.y.z`) only for well-maintained packages.
  - **Updates:** Regularly review and update dependencies to incorporate security patches and improvements.

### 3.4. API & Services Integration

  - **Repository Pattern:** All data access must go through a Repository. The repository acts as the single source of truth and abstracts the data sources (remote API, local cache, etc.).
  - **Data Sources:** A repository will use one or more Data Sources. Each data source has a single responsibility (e.g., `UserRemoteDataSource` for API calls, `UserLocalDataSource` for database access).

### 3.5. Environment Configuration

  - **Flavors/Schemes:** The project must be configured with flavors (Android) and schemes (iOS) to support different environments (e.g., development, staging, production).
  - **Environment Variables:** Do not hardcode environment-specific values like API base URLs. Manage them through the environment configuration.

### 3.6. State Management

  - **BLoC Pattern:** Use the BLoC pattern for managing state in the Presentation layer.
  - **BLoC Dependencies:** A BLoC or Cubit must only depend on Use Case abstractions from the Domain layer. It must never access a Repository directly.
  - **Events & States:** BLoCs receive events and transform them into states. States should be immutable data classes representing the UI's condition.

-----

## 4\. Quality & Engineering Excellence

### 4.1. Testing Strategy & Implementation

  - **Arrange-Act-Assert (AAA):** All tests must follow the AAA pattern.
  - **Unit Tests:** All business logic (Use Cases, Repositories, BLoCs) must have 100% unit test coverage. Use `bloc_test` and `Mocktail` for BLoC testing.
  - **Widget Tests:** All widgets must have widget tests to verify UI rendering and interactions.
  - **Integration Tests:** Critical user flows must be covered by integration tests.

### 4.2. Quality Gates & Acceptance Criteria

  - **Test Coverage:** A minimum of **80%** test coverage is required for all new code. This is enforced by the CI pipeline.
  - **Static Analysis:** Code must pass all linter rules (`very_good_analysis` is recommended) with zero warnings or errors.
  - **SonarQube/SonarCloud:** All code must pass the defined Quality Gate, with 'A' ratings for Reliability, Security, and Maintainability.

### 4.3. Error Handling & Validation

  - **Failures:** Use a `Failure` class to represent domain-level errors (e.g., `ServerFailure`, `CacheFailure`) and return them from repositories using `Either`.
  - **Exceptions:** The Data layer should catch specific exceptions (e.g., `DioException`, `SocketException`) and map them to custom `Failure` types.
  - **UI Feedback:** The UI must handle all possible states, including loading, success, and error states, providing clear feedback to the user.

### 4.4. Security & Compliance

#### 4.4.1. Data Protection

  - **No Secrets in Code:** Never commit API keys, passwords, or other secrets to the repository. Use environment variables or a secure secrets management tool.
  - **Secure Storage:** Use the device's secure storage (Keystore for Android, Keychain for iOS) via packages like `flutter_secure_storage` for any sensitive data that must be persisted.
  - **Obfuscation:** All release builds must be obfuscated.

#### 4.4.2. Compliance Requirements


### 4.5. Performance & Optimization

  - **Use `const`:** Maximize the use of `const` constructors for widgets to reduce unnecessary rebuilds.
  - **Render Engine:** Use the `canvaskit` web renderer for better performance and rendering consistency on the web.
  - **Lazy Loading:** Use techniques like lazy loading and pagination (`ListView.builder`) for long lists to optimize memory and performance.

### 4.6. Accessibility (A11Y)


-----

## 5\. Process Requirements

### 5.1. Definition of Ready (DoR)


### 5.2. Definition of Done (DoD)


### 5.3. Git Workflow

  - **Branching Strategy:** Use a standardized branching strategy like GitFlow (main, develop, feature/..., hotfix/...).
  - **Conventional Commits:** All commit messages must follow the Conventional Commits specification.
  - **Pull Requests (PRs):** All code must be submitted via a PR. PRs must be reviewed by at least one other developer and pass all CI checks before being merged.

-----

## 6\. Observability & Operations

### 6.1. Monitoring & Traceability

  - **Crash Reporting:** Integrate a crash reporting tool like Firebase Crashlytics to monitor and triage crashes and non-fatal errors in real-time.
  - **Performance Monitoring:** Use a tool like Firebase Performance Monitoring to track app start time, screen transitions, and network request performance.

### 6.2. Logging Standards

  - **No Sensitive Data:** Logs must **never** contain personally identifiable information (PII) or other sensitive data (tokens, passwords, etc.).
  - **Log Levels:** Use appropriate log levels (e.g., DEBUG, INFO, WARNING, ERROR).
  - **Release Builds:** Verbose DEBUG logs must be disabled in all release builds.

### 6.3. Alerts & Incident Response


### 6.4. Performance Metrics & SLAs


-----

## 📢 Final Notes for the AI Agent

### Agent's Role & Capabilities

  - The AI agent's role is to assist in writing, refactoring, and reviewing code according to the standards defined in this document.
  - The agent should be able to identify deviations from these guidelines and suggest corrections.
  - The agent should use this document as its primary source of truth for project-specific conventions.