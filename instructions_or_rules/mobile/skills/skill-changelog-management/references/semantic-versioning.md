# Semantic Versioning for Changelog

Detailed guide to semantic versioning to help determine which version number to use when releasing.

## Core Concept

Semantic Versioning (SemVer) is a version number system that communicates the type of changes:

```
MAJOR.MINOR.PATCH
  2  .  5  .  3
```

- **MAJOR** = Breaking changes
- **MINOR** = New backward-compatible features
- **PATCH** = Bug fixes and patches

## The Rules

### MAJOR Version (`X.0.0`)

**Increment when:** Making incompatible API changes, removing features, or changing behavior in breaking ways

**Examples:**
```
0.0.1 → 1.0.0 (First stable release)
1.5.0 → 2.0.0 (Removed deprecated API endpoints)
2.0.0 → 3.0.0 (Changed authentication system)
```

**What breaks:**
- Users must update code
- Configuration files may become invalid
- Migration path required
- Could break production systems

**User impact:** HIGH - requires immediate attention and migration

### MINOR Version (`X.Y.0`)

**Increment when:** Adding new backward-compatible functionality

**Examples:**
```
1.0.0 → 1.1.0 (Added new export format)
1.1.0 → 1.2.0 (Added search filters)
1.2.0 → 1.3.0 (Added user preferences)
```

**What's new:**
- New features available
- All existing code still works
- No migration needed
- Completely optional to use new feature

**User impact:** MEDIUM - beneficial but optional

### PATCH Version (`X.Y.Z`)

**Increment when:** Fixing bugs and making small improvements

**Examples:**
```
1.0.0 → 1.0.1 (Fixed login bug)
1.0.1 → 1.0.2 (Fixed typo)
1.0.2 → 1.0.3 (Improved performance)
```

**What's fixed:**
- Bug fixes
- Security patches
- Performance improvements
- No new features

**User impact:** LOW - improvements and fixes only

## When to Use What

### Example 1: New Search Feature

**Changelog:**
```markdown
### Added
- New advanced search filters
- Filter by category, price, and date
```

**Version decision:**
- New features (backward-compatible) = MINOR
- Old search still works
- Users can ignore new filters

```
Version: 1.0.0 → 1.1.0
```

### Example 2: Remove Old API Endpoint

**Changelog:**
```markdown
### Removed
- Removed /api/v1/users endpoint (deprecated in v1.5)

### Changed
- Use /api/v2/users endpoint instead
```

**Version decision:**
- Removing feature = MAJOR
- Breaking change - users must migrate
- Old code will break

```
Version: 1.5.0 → 2.0.0
```

### Example 3: Fix Memory Leak

**Changelog:**
```markdown
### Fixed
- Fixed memory leak in background sync
```

**Version decision:**
- Bug fix only = PATCH
- No new features
- No breaking changes
- Just improvement

```
Version: 1.0.0 → 1.0.1
```

### Example 4: Multiple Changes

**Changelog:**
```markdown
### Added
- New dark theme
- New export formats

### Fixed
- Fixed login timeout bug
- Fixed sorting issue
```

**Version decision:**
- Has new features (MINOR) + bug fixes (PATCH)
- Use MINOR (higher priority)
- The new features are the main reason to release

```
Version: 1.0.0 → 1.1.0
```

### Example 5: Complex Release

**Changelog:**
```markdown
### Added
- New authentication system

### Changed
- **BREAKING**: Changed API response format

### Removed
- Removed old API v1 endpoints

### Security
- Fixed SQL injection vulnerability
```

**Version decision:**
- Has breaking changes = MAJOR (highest priority)
- Breaking changes override everything
- Users must migrate

```
Version: 1.5.0 → 2.0.0
```

## Decision Flowchart

```
Any BREAKING CHANGES?
  Yes → MAJOR (X.0.0)
  No → Continue

New backward-compatible features?
  Yes → MINOR (X.Y.0)
  No → Continue

Bug fixes or improvements?
  Yes → PATCH (X.Y.Z)
  No → No release (wait for changes)
```

## Common Release Patterns

### Weekly Releases (Small Team)

```
v1.0.0 - Initial release
v1.0.1 - Bug fix (Friday patch)
v1.1.0 - New feature (next Monday release)
v1.1.1 - Critical bug fix (urgent)
v1.2.0 - Multiple new features
v2.0.0 - Major refactoring with breaking changes
```

### Monthly Releases

```
v1.0.0 - January 1st
v1.1.0 - February 1st (new features accumulate)
v1.2.0 - March 1st
v1.2.1 - March 15th (emergency fix)
v2.0.0 - April 1st (planned major release)
```

### By Milestone (Larger Projects)

```
v1.0-beta - Beta phase
v1.0-rc1 - Release candidate 1
v1.0.0 - Stable release
v1.1.0 - Feature milestone
v2.0.0 - Next major milestone
```

## Special Cases

### Pre-releases (Beta, RC)

For versions not yet ready for production:

```
v2.0.0-alpha.1     # Early preview
v2.0.0-beta.1      # User testing
v2.0.0-rc.1        # Release candidate (almost final)
v2.0.0              # Final (production ready)
```

Use format: `X.Y.Z-identifier.N`

### Internal vs Public Versions

**Internal development:**
```
v0.0.1-dev        # Development build
v0.0.1-internal   # Internal testing
```

**Public releases:**
```
v1.0.0           # Stable, users can use
v1.0.1           # Patch release
v1.1.0           # Feature release
```

### 0.x.y (Pre-1.0 Development)

Before v1.0, different rules apply:

```
v0.0.1          # Initial development
v0.0.2          # More development
v0.1.0          # First feature-complete version
v0.2.0          # Major changes (still unstable)
v1.0.0          # Stable, production ready
```

During 0.x phase:
- Breaking changes increment MINOR (not MAJOR)
- Use to signal stability (approaching 1.0)

## Communicating Versions

### In Marketing

- **v2.0.0**: "Major new release"
- **v1.5.0**: "Now with enhanced features"
- **v1.0.1**: "Important bug fix release"

### In Documentation

```markdown
# v2.0.0 - Major Upgrade Required
Users of v1.x must follow migration guide

# v1.5.0 - New Features Available
No migration required, update optional

# v1.0.1 - Bug Fix
Recommended for all users
```

### In Release Notes

**v2.0.0 (Major)**
```markdown
This version requires action from all users.
See migration guide: docs/v2.0-migration.md
```

**v1.5.0 (Minor)**
```markdown
New in this version:
- Dark mode (optional)
- Advanced search filters
Update recommended but not required.
```

**v1.0.1 (Patch)**
```markdown
This release fixes important bug in v1.0.0
All users recommended to update.
```

## Increment Examples

### Breaking Change in Hook System

```
- Current: v1.2.0
- Change: Changed hook API format
- New: v2.0.0  (breaking, major increment)
```

### Bug Fix in Current Release

```
- Current: v1.2.0
- Change: Fixed memory leak
- New: v1.2.1  (patch increment)
```

## Version Number Checklist

Before deciding on version number:

- [ ] Does this have breaking changes? → MAJOR
- [ ] Does this add new features? → MINOR (unless breaking)
- [ ] Does this only fix bugs? → PATCH
- [ ] Are we still in 0.x phase? → Increment accordingly
- [ ] Is this pre-release? → Add identifier (-alpha, -beta, -rc)
- [ ] Did we update CHANGELOG.md? → Yes, required
- [ ] Does our SemVer number match the changes? → Double check

## See Also

- [Semantic Versioning Official](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)