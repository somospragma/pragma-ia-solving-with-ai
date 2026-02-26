# Changelog Examples for pragma-mason-brick

Real-world examples based on project structure and development patterns.

## Example 1: Adding a New Brick

When you add support for a new component type:

```markdown
## [0.0.4] - 2021-02-19
### Added
- New `component_service` for generating microservices
- Service layer generation with routing and error handling
- Automated dependency configuration for services
- Example implementation in hooks with error handling patterns

### Changed
- Updated Melos configuration to support monorepo project
- Enhanced commons library with service utilities

### Deprecated
- Old service patterns in component_clean_feature (use new component_service)

[0.0.4]: https://github.com/somospragma/pragma-ia-solving-with-ai/releases/tag/v0.0.4
```

## Example 2: Feature Addition (Clean Code)

When adding feature development capabilities:

```markdown
## [Unreleased]
### Added
- Comprehensive testing structure templates for features
  - Unit tests for entities and repositories
  - Integration tests for use cases
  - Widget tests for presentation layer
- Result pattern implementation examples in datasources
- Mapper pattern examples for entity transformation
- Local/remote datasource examples with caching strategy
- Dependency injection configuration guide

### Changed
- Improved pre-commit hook to support VS Code, Android Studio, and IntelliJ
- Enhanced documentation structure with clearer formatting

### Deprecated
- Basic script templates (replaced with professional grade scripts)
```

## Example 3: Documentation Update

When improving documentation:

```markdown
### Changed
- Reorganized project documentation structure
  - Added clear docs/ folder with standard sections
  - Created implementation guidelines
  - Added troubleshooting section
  - Updated architecture diagrams
- Improved README clarity with better formatting
```

## Example 4: Bug Fix

When fixing issues in component or hooks:

```markdown
### Fixed
- Fixed pre-commit hook failure on files with special characters in names
- Fixed injectable configuration not working in some IDE configurations
- Fixed router generation when feature names contain numbers
- Fixed pubspec.yaml not properly inheriting workspace dependencies
```

## Example 5: Breaking Change (Migration Required)

When major changes require user action:

```markdown
## [1.0.0] - 2026-03-01
### Changed
- **BREAKING**: Changed component configuration format
  Old format: YAML with nested structure
  New format: Simplified JSON for better IDE support
  Migration: See docs/migration-v1.md for step-by-step guide
  Timeline: Old format will be removed in v2.0.0

- **BREAKING**: Router API changed in component_clean_feature
  Old: `GoRoute(path: '/', builder: ...)`
  New: `GoRoute(path: '/', pageBuilder: ...)`
  Reason: Better support for named route transitions

### Removed
- Removed deprecated component `ui_component_kit` (was deprecated in v0.0.3)
- Removed legacy hook system (migrated to commons library)
```

## Example 6: Security Fix

When fixing vulnerability:

```markdown
### Security
- Fixed arbitrary code execution vulnerability in hooks
  Severity: Critical
  Affected: All users with custom component hooks
  Action: Please run `melos upgrade` immediately
  Details: https://github.com/somospragma/pragma-ia-solving-with-ai/security/advisories/GHSA-xxxx-yyyy-zzzz

- Updated vulnerable dependency (lodash) to 4.17.21
  Vulnerability: Prototype pollution in DefaultsDeep utility
  Severity: Medium
```

## Example 7: Phased Release

When rolling out features gradually:

```markdown
## [0.0.4] - 2021-02-19
### Added
- Beta: New `state_management_component` for view controler
  Note: Still in development, use at own risk

### Changed
- Migration script now automatically updates brick configs

### Fixed
- Fixed template variables not expanding in some edge cases
```

Then in next release, move from beta to stable:

```markdown
## [0.1.0] - 2026-03-01
### Added
- `state_management_component` now stable and ready for production
  Full support for BLoC and Cubit patterns with comprehensive testing

### Changed
- Improved `state_management_component` with additional configuration options
```

## Example 8: Multi-Feature Release

Larger release with multiple improvements:

```markdown
## [0.0.5] - 2026-04-01
### Added
- Pre-commit hook script for automatic code formatting
- Pre-push hook script for running tests before push
- Git hooks setup documentation
- Installation guides for macOS, Linux, and Windows
- Complete testing examples for all component layers

### Changed
- Improved error messages in hook validation
- Enhanced DI configuration with real project examples
- Restructured documentation for better navigation
- Updated example config files with better comments

### Fixed
- Fixed melos configuration not working with relative paths
- Fixed hook execution permissions on fresh clones
- Fixed template generation failing with non-ASCII characters
- Fixed router imports not being resolved correctly

### Removed
- Removed deprecated old cli commands

[0.0.5]: https://github.com/somospragma/pragma-ia-solving-with-ai/releases/tag/v0.0.5
```

## Example 9: Development Workflow

Showing how Unreleased grows, then gets released:

**Week 1: Development Phase**

```markdown
## [Unreleased]
### Added
- New authentication flow with social login support
- User profile management page

### Fixed
- Login timeout bug
```

**Week 2: Pre-Release Review**

```markdown
## [Unreleased]
### Added
- Complete authentication system with social login (Google, Apple, Microsoft)
- OAuth 2.0 implementation
- User profile management with avatar upload
- Session management with automatic refresh

### Fixed
- Fixed login timeout on slow connections (< 1seg)
- Fixed XSS vulnerability in user input validation
```

**Release Time: Move to Version Section**

```markdown
## [Unreleased]
### Added
# (empty, ready for next development cycle)

## [2.5.0] - 2026-02-28
### Added
- Complete authentication system with social login (Google, Apple, Microsoft)
- OAuth 2.0 implementation
- User profile management with avatar upload
- Session management with automatic refresh

### Fixed
- Fixed login timeout on slow connections (< 1seg)
- Fixed XSS vulnerability in user input validation
```

## Version Naming Conventions

- **0.0.1 - 0.0.9**: Initial development and bug fixes
- **0.1.0**: First project release
- **0.2.0**: Major feature addition
- **0.3.0**: Major feature addition
- **1.0.0**: Stable release suitable for production

Example progression:
```
v0.0.1: Initial project setup
v0.0.2: Refactored project configuration
v0.0.3: Added component o feature + DI support
v0.1.0: Melos integration + monorepo support
v0.2.0: Complete documentation structure
v1.0.0: Production-ready project and solid tooling
```

## Tips for Writing Entries

1. **Add entry immediately when make commit**
   - Don't wait pull request
   - Don't wait until release
   - Keep momentum of work clear

2. **Use consistent verb tenses**
   - "Added", "Fixed", "Changed" (consistent past tense)

3. **From user/developer perspective**
   - What can they do now?
   - What breaks for them?
   - What should they migrate?

4. **Link related issues**
   ```markdown
   - New feature X (#123)
   - Fixes critical bug (fixes #456)
   ```

5. **Group improvements together**
   ```markdown
   ### Changed
   - Improved brick validation
   - Improved error messages
   - Improved documentation
   ```
   Then be specific in each line

## Common Entry Templates

### New Feature
```markdown
### Added
- New <feature_name> <what_it_does>
  - Sub-feature 1
  - Sub-feature 2
```

### Bug Fix
```markdown
### Fixed
- Fixed <what was broken> <how it impacted users>
```

### Breaking Change
```markdown
### Changed
- **BREAKING**: <what changed>
  Old behavior: ...
  New behavior: ...
  Migration: See docs/migration.md
```

### Documentation
```markdown
### Changed
- Improved documentation structure
  - Added <what was added>
  - Updated <what was updated>
  - Clarified <what was clarified>
```

### Deprecation
```markdown
### Deprecated
- `old_method()` - Use `new_method()` instead
  Removal: Will be removed in v2.0.0
```
