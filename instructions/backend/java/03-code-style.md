# Code Style Guidelines

## 3.1 Java Code Analysis Extensions
- ✅ Install and configure **Checkstyle** (enforce code formatting and conventions).  
- ✅ Add **SpotBugs** (static analysis for common bugs).  
- ✅ Use **PMD** (detect unused code, complexity, and bad practices).  
- ✅ Integrate **SonarQube/SonarCloud** for quality gates (coverage, security, smells).  
- ✅ Add **JUnit/Testcontainers rules** in CI pipelines for testing quality.  
- ❌ DO NOT rely only on manual code reviews — enforce automated rules.  

## 3.2 Formatting and conventions
- ✅ Use conventions: `UpperCamelCase` for classes, `camelCase` for methods/variables, `CONSTANTS_UPPER_SNAKE`.  
- ✅ Keep lines ≤ 140 characters.  

## 3.3 Function Naming
- ✅ Name all functions, including closures and callbacks
- ✅ Avoid anonymous functions
- ✅ Facilitate debugging and profiling
- ❌ NO use anonymous functions in production

## 3.4 Naming Conventions
- ✅ lowerCamelCase for variables, constants, functions
- ✅ UpperCamelCase for classes
- ✅ UPPER_SNAKE_CASE for global/static variables
- ✅ Descriptive but concise names
- ❌ NO mix naming conventions

## 3.5 Variable Declaration
- ✅ Use `final` for constants and variables that should not change (immutability).  
- ✅ Use explicit types (`int`, `String`, `List<User>`) for clarity in public APIs.  
- ✅ Use `var` for local variables when type inference improves readability (Java 10+).  
- ❌ DO NOT overuse `var` when it reduces code clarity.  
- ❌ DO NOT mutate variables unnecessarily; prefer immutability where possible.  

## 3.6 Null safety
- ✅ Use `Optional<T>` for return values that may be empty.  
- ✅ Validate nulls at boundaries (controllers/adapters).  

## 3.7 Lombok (if used)
- ✅ Use with moderation; prefer explicit constructors in critical entities.  
- ✅ Document usage and justify by performance/productivity.  

## 3.8 Module Imports
- ✅ Place all imports/requires at file beginning
- ✅ Order imports by: Java, javax, org, com (configurable in IDE).  
- ❌ NO require inside functions without specific reason
- ❌ NO unnecessary conditional imports

## 3.9 Module Entry Points
- ✅ Use a `Main` class with a clear `public static void main(String[] args)` as the entry point.  
- ✅ In Spring Boot, use `@SpringBootApplication` as the single entry point.  
- ✅ Define clear public interface
- ✅ Encapsulate internal functionality
- ❌ NO allow direct access to internal files
- ❌ NO expose internal module structure

## 3.10 Strict Equality
- ✅ Use `.equals()` and `.equalsIgnoreCase()` for object/string equality. 
- ✅ Avoid implicit type coercion
- ✅ Maintain consistency in comparisons
- ❌ NO use `==` or `!=` without specific reason
- ❌ NO depend on automatic type coercion

## 3.11 Asynchronous Programming
- ✅ Prefer `CompletableFuture` or reactive types (`Mono`, `Flux`) over manual threads.  
- ✅ Use `onErrorResume` for error handling.  
- ✅ Maintain readable and maintainable code
- ❌ DO NOT use nested callbacks (callback hell).  
- ❌ NO create callback hell

## 3.12 Lambdas and Method References
- ✅ Use lambda expressions for short, inline logic.  
- ✅ Use method references (`Class::method`) when concise.  
- ✅ Maintain `this` context explicitly when needed in inner classes. 
- ❌ DO NOT overuse lambdas for complex logic (prefer named methods).
- ❌ DO NOT misuse lambdas where clarity is reduced. 

## 3.13 Avoid Side Effects Outside Functions
- ✅ Keep side effects inside functions
- ✅ Avoid initialization code at module level
- ✅ Make code more testable and predictable
- ✅ Use factory patterns when necessary
- ❌ NO execute complex logic when importing module
- ❌ NO make network/DB calls at module level