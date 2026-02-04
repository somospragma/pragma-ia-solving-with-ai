# Import Guidelines

## 9.1 Package-Style Imports
- ✅ Use Java package conventions(com.company.errors, com.company.vehicles).
- ✅ Define clear module boundaries (domain, application, infrastructure).
- ✅ Avoid deep relative paths or exposing internal implementation.
- ❌ NO use relative imports for shared libraries

## 9.2 Import Resolution Rules
- ✅ External dependencies: `import org.springframework.web.bind.annotation.RestController;`
- ✅ Shared libraries: `import com.company.shared.errors.AppError;`
- ✅ Internal component: `import com.company.orders.service.OrderService;`
- ❌ NO mix resolution patterns inconsistently

## 9.3 Module Boundaries
- ✅ Components import shared libraries via package aliases
- ✅ Internal components import only their domain or shared modules.
- ✅ Maintain clear dependency direction
- ❌ NO circular dependencies between components

## 9.4 Maven/Gradle Configuration
```Gradle settings.gradle:
    include(":shared:errors")
    include(":shared:config")
    include(":shared:logger")

In module build.gradle:
    dependencies {
      implementation project(":shared:errors")
      implementation project(":shared:config")
      implementation project(":shared:logger")
    }
```

## 9.5 Import Order
- ✅ Standard Java imports (java.*, javax.*) first.
- ✅ External dependencies (org.*, spring.*) second.
- ✅ Internal company libraries (com.company.*) third.
- ✅ Local module imports last.
- ✅ Separate groups with blank lines.
- ❌ NO mix import types randomly