---
name: skill-changelog-management
description: Maintain clear, organized release notes following Keep a Changelog and Semantic Versioning standards. This skill ensures your changelog communicates changes effectively to users and developers.
license: Complete terms in LICENSE.txt
---

# Changelog Management Skill

Maintain clear, organized release notes following Keep a Changelog and Semantic Versioning standards. This skill ensures your changelog communicates changes effectively to users and developers.

## Quick Reference

| What | Where | When |
|------|-------|------|
| **Unreleased changes** | `[Unreleased]` section | As you develop |
| **Release version** | Version header with date | When releasing |
| **Section headers** | Added, Changed, Deprecated, Removed, Fixed, Security | Always use these 6 categories |
| **Entry format** | Bullet points with brief description | Each change |
| **Breaking changes** | Mark clearly in description or use BREAKING CHANGE footer | Major versions |
| **Release notes** | Create from Unreleased section | Before version tag |

## Essential Rules

### 1. **Unreleased Section Always Comes First**

```markdown
## [Unreleased]
### Added
- New feature description

### Changed
- Behavior change description

### Fixed
- Bug fix description
```

The `[Unreleased]` section captures all changes since the last release.

### 2. **Use Only These 6 Categories**

- **Added** - New features or functionality
- **Changed** - Changes in existing functionality
- **Deprecated** - Soon-to-be removed features
- **Removed** - Previously deprecated features now removed
- **Fixed** - Bug fixes
- **Security** - Vulnerability fixes or security improvements

Not all categories need to appear in every release.

### 3. **Version Format: [X.Y.Z] - YYYY-MM-DD**

```markdown
## [1.2.0] - 2011-04-08
### Added
- New authentication module
### Fixed
- Login page crash on slow networks
```

- Use semantic versioning: MAJOR.MINOR.PATCH
- Include full date in ISO format
- Bracketed version with links at bottom

### 4. **Write Clear, User-Focused Descriptions**

```markdown
# ✅ GOOD - User understands the impact
### Added
- Added full-text search across all products
- Implemented dark mode support for iOS

# ❌ BAD - Too vague or technical
### Added
- Refactored search component
- Updated dependencies
```

### 5. **Group Related Changes**

```markdown
### Added
- User authentication system
- Two-factor authentication
- Email verification flow

# Better organization than scattered entries
```

### 6. **Mark Breaking Changes Explicitly**

```markdown
## [2.0.0] - 2021-02-19
### Changed
- **BREAKING CHANGE**: Removed deprecated `getUserData()` method
- **BREAKING CHANGE**: Changed API response format from XML to JSON
- Changed default cache TTL from 5 minutes to 2 minutes

### Removed
- Removed support for API v1 endpoints
```

## Development Workflow

### When Developing

1. **Add entry to `[Unreleased]`**
   ```markdown
   ## [Unreleased]
   ### Added
   - New comprehensive user profile page
   ```

2. **Use appropriate category** based on change type

3. **Write from user perspective**
   - "Users can now export data" ✅
   - "Implemented export feature" ❌

4. **Keep entries brief** - Save details for pull request descriptions

### Before Release

1. **Review all `[Unreleased]` entries**
   - Remove duplicates
   - Ensure clarity
   - Group related items

2. **Create new version section**
   ```markdown
   ## [1.2.0] - 2011-04-08
   ### Added
   - Feature A
   ### Fixed
   - Bug fix B
   ```

3. **Move entries from `[Unreleased]` to version section**

4. **Update comparison links at bottom**
   ```markdown
   [unreleased]: https://github.com/org/repo/compare/v1.2.0...HEAD
   [1.2.0]: https://github.com/org/repo/releases/tag/v1.2.0
   ```

5. **Create git tag**
   ```bash
   git tag -a v1.2.0 -m "Release v1.2.0"
   git push origin v1.2.0
   ```

## Semantic Versioning Guide

| Change Type | Version | Example |
|------------|---------|---------|
| **Breaking API change** | MAJOR | 1.0.0 → 2.0.0 |
| **New backward-compatible feature** | MINOR | 1.0.0 → 1.1.0 |
| **Bug fix, patch** | PATCH | 1.0.0 → 1.0.1 |

```
MAJOR: Removed old API, changed authentication method → v1.0.0 → v2.0.0
MINOR: Added new search feature, new export formats → v1.0.0 → v1.1.0
PATCH: Fixed login bug, improved performance → v1.0.0 → v1.0.1
```

## Common Mistakes

### ❌ Mixing Technical and User Details

```markdown
# BAD
### Added
- Refactored UserCubit using BLoC pattern
- Migrated to GetIt for dependency injection

# GOOD
### Added
- Improved user authentication reliability
```

### ❌ Forgetting Unreleased Section

```markdown
# BAD - Version jumps around
## [2.0.0]
## [1.9.0]

# GOOD - Unreleased always first
## [Unreleased]
## [2.0.0]
## [1.9.0]
```

### ❌ Inconsistent Categorization

```markdown
# BAD - Fixed goes under Added
### Added
- Fixed typo in welcome message
- Fixed memory leak

# GOOD
### Fixed
- Typo in welcome message
- Memory leak in data loader
```

### ❌ No Breaking Change Markers

```markdown
# BAD - Users don't see breaking change
### Changed
- Updated API response format

# GOOD
### Changed
- **BREAKING CHANGE**: API response format changed from XML to JSON
  Old format: <user><name>...</name></user>
  New format: {"user": {"name": "..."}}
```

## Tools & Validation

### Validate Changelog Format

```bash
# Simple check for structure
grep -E "^## \[" CHANGELOG.md

# Check for required sections in unreleased
grep -A 5 "## \[Unreleased\]" CHANGELOG.md | grep -E "### (Added|Changed|Deprecated|Removed|Fixed|Security)"
```

### Generate Release Notes

```bash
# Extract unreleased section for release notes
sed -n '/## \[Unreleased\]/,/## \[/p' CHANGELOG.md | head -n -1
```

### Link Version References

```bash
# Add comparison links at bottom of CHANGELOG.md
echo "[unreleased]: https://github.com/org/repo/compare/v1.2.0...HEAD" >> CHANGELOG.md
echo "[1.2.0]: https://github.com/org/repo/releases/tag/v1.2.0" >> CHANGELOG.md
```

## See Also

- [Keep a Changelog Official](https://keepachangelog.com/) - Full specification
- [Semantic Versioning](https://semver.org/) - Version numbering system

## Next Steps

1. ✅ Read this skill to understand changelog structure
2. Read [keepachangelog-rules.md](references/keepachangelog-rules.md) for detailed rules
3. Review [changelog-examples.md](references/changelog-examples.md) for content patterns
4. Review [writing-guidelines.md](references/writing-guidelines.md) for best practices in writing entries
5. Follow [categories-guide.md](assets/categories-guide.md) when writing entries
6. Use [changelog-template.md](assets/changelog-template.md) as reference
