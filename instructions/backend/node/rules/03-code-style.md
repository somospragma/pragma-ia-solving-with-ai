# Code Style Guidelines

## 3.1 ESLint Usage
- ✅ Configure ESLint to detect code errors
- ✅ Use with Prettier for formatting
- ✅ Implement consistent style rules
- ✅ Integrate in CI/CD process
- ❌ NO depend only on manual formatting
- ❌ NO ignore ESLint warnings

## 3.2 Node.js ESLint Extensions
- ✅ Install eslint-plugin-node
- ✅ Use eslint-plugin-security
- ✅ Add eslint-plugin-mocha/jest per framework
- ✅ Configure Node.js specific rules
- ❌ NO use only vanilla JavaScript rules

## 3.3 Curly Braces Placement
- ✅ Place `{` on same line as declaration
- ✅ Follow standard JavaScript convention
- ❌ NO place `{` on new line

## 3.4 Statement Separation
- ✅ Use ESLint to detect separation issues
- ✅ Use Prettier or StandardJS for auto-formatting
- ✅ Avoid problematic automatic semicolon insertion
- ❌ NO create ambiguous statements
- ❌ NO depend on ASI without understanding

## 3.5 Function Naming
- ✅ Name all functions, including closures and callbacks
- ✅ Avoid anonymous functions
- ✅ Facilitate debugging and profiling
- ❌ NO use anonymous functions in production

## 3.6 Naming Conventions
- ✅ lowerCamelCase for variables, constants, functions
- ✅ UpperCamelCase for classes
- ✅ UPPER_SNAKE_CASE for global/static variables
- ✅ Descriptive but concise names
- ❌ NO mix naming conventions

## 3.7 Variable Declaration
- ✅ Use `const` by default
- ✅ Use `let` only when reassignment needed
- ✅ Never use `var`
- ❌ NO use `var` in modern code

## 3.8 Module Imports
- ✅ Place all imports/requires at file beginning
- ✅ Group imports by type (built-in, npm, local)
- ❌ NO require inside functions without specific reason
- ❌ NO unnecessary conditional imports

## 3.9 Module Entry Points
- ✅ Use `package.json.main` or `package.json.exports`
- ✅ Create `index.js` as default entry point
- ✅ Define clear public interface
- ✅ Encapsulate internal functionality
- ❌ NO allow direct access to internal files
- ❌ NO expose internal module structure

## 3.10 Strict Equality
- ✅ Use `===` and `!==` for strict comparisons
- ✅ Avoid implicit type coercion
- ✅ Maintain consistency in comparisons
- ❌ NO use `==` or `!=` without specific reason
- ❌ NO depend on automatic type coercion

## 3.11 Async/Await Usage
- ✅ Prefer async/await over callbacks
- ✅ Use promises for asynchronous operations
- ✅ Maintain readable and maintainable code
- ✅ Use try-catch with async/await
- ❌ NO use callbacks when async/await available
- ❌ NO create callback hell

## 3.12 Arrow Functions
- ✅ Use arrow functions for short functions
- ✅ Maintain `this` context when appropriate
- ✅ Use for callbacks and inline functions
- ✅ Leverage more concise syntax
- ❌ NO use when specific `this` binding needed
- ❌ NO use for object methods requiring `this`

## 3.13 Avoid Side Effects Outside Functions
- ✅ Keep side effects inside functions
- ✅ Avoid initialization code at module level
- ✅ Make code more testable and predictable
- ✅ Use factory patterns when necessary
- ❌ NO execute complex logic when importing module
- ❌ NO make network/DB calls at module level