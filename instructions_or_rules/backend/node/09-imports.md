# Import Guidelines

## 9.1 Package-Style Imports
- ✅ Use `imports` field in package.json for internal modules
- ✅ Define clean aliases like `@app/errors`, `@app/vehicles`
- ✅ Avoid deep relative paths like `../../../libraries/`
- ❌ NO use relative imports for shared libraries

## 9.2 Import Resolution Rules
- ✅ External dependencies: `import express from 'express'`
- ✅ Shared libraries: `import { AppError } from '@app/errors'`
- ✅ Internal component: `import { service } from '../domain/service.js'`
- ❌ NO mix resolution patterns inconsistently

## 9.3 Module Boundaries
- ✅ Components import shared libraries via package aliases
- ✅ Internal component files use relative imports
- ✅ Maintain clear dependency direction
- ❌ NO circular dependencies between components

## 9.4 Package.json Configuration
```json
{
  "imports": {
    "@app/errors": "./libraries/errors/index.js",
    "@app/config": "./libraries/config/index.js",
    "@app/logger": "./libraries/logger/index.js"
  }
}
```

## 9.5 Import Order
- ✅ External packages first
- ✅ Internal packages (@app/*) second  
- ✅ Relative imports last
- ✅ Group by blank lines
- ❌ NO mix import types randomly