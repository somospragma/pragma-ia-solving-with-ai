# Changelog Template

Copy and paste this template when creating a new changelog:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- List new features here

### Changed
- List behavior changes here

### Deprecated
- List deprecated features here (with migration path)

### Removed
- List removed features here (only if previously deprecated)

### Fixed
- List bug fixes here

### Security
- List security fixes here

## [X.Y.Z] - YYYY-MM-DD
### Added
- First feature

### Fixed
- First bug fix

## [X.Y.Z-1] - YYYY-MM-DD
### Added
- First feature on previous version

[unreleased]: https://github.com/org/repo/compare/vX.Y.Z...HEAD
[X.Y.Z]: https://github.com/org/repo/releases/tag/vX.Y.Z
[X.Y.Z-1]: https://github.com/org/repo/releases/tag/vX.Y.Z-1
```

## Quick Copy-Paste Sections

### When Adding to [Unreleased]

Copy this section and add it:

```markdown
### Added
- New feature description

```

Or for a fix:

```markdown
### Fixed
- Bug description

```

### When Creating New Version

```markdown
## [X.Y.Z] - YYYY-MM-DD
### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security

```

### For Breaking Changes

```markdown
### Changed
- **BREAKING CHANGE**: Description of what breaks
  Old behavior: How it worked before
  New behavior: How it works now
  Migration: How to update (link to migration guide)

```

### For Deprecations

```markdown
### Deprecated
- `old_function()` - Use `new_function()` instead
  Timeline: Will be removed in v2.0.0

```

## Minimal vs Complete

### Minimal Changelog

```markdown
# Changelog

All notable changes documented here.

## [1.0.0] - 2011-04-08
### Added
- Initial release

[1.0.0]: https://github.com/org/repo/releases/tag/v1.0.0
```

### Complete Changelog

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Feature in development

## [2.1.0] - 2026-02-18
### Added
- User profile customization

### Changed
- Improved search speed

### Fixed
- Old bug fix

## [2.0.0] - 2011-04-08
### Changed
- **BREAKING**: API response format changed

### Removed
- Old authentication method

## [1.0.0] - 2025-12-25
### Added
- Initial stable release

[unreleased]: https://github.com/org/repo/compare/v2.1.0...HEAD
[2.1.0]: https://github.com/org/repo/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/org/repo/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/org/repo/releases/tag/v1.0.0
```

## Validation Checklist

Before committing your changelog entry:

- [ ] Added entry to `[Unreleased]` section (not to a version section)
- [ ] Used correct category (Added, Changed, Deprecated, Removed, Fixed, Security)
- [ ] Entry is written from user perspective (not technical jargon)
- [ ] Entry is clear and concise (1-2 lines maximum)
- [ ] Spelling and grammar are correct
- [ ] Related entries are grouped together
- [ ] No abbreviations or unclear terms
- [ ] Links to issues/PRs are added if relevant
- [ ] Breaking changes are clearly marked with **BREAKING CHANGE**

## Commands to Generate Sections

### Extract Unreleased Section

```bash
sed -n '/## \[Unreleased\]/,/## \[/p' CHANGELOG.md | head -n -1
```

### List All Sections

```bash
grep "^## \[" CHANGELOG.md
```

### Generate Version Links

```bash
# For git tag v1.2.0 compared to previous tag v1.1.0
echo "[1.2.0]: https://github.com/org/repo/compare/v1.1.0...v1.2.0"
```

## Next Steps

1. Copy the template above to start your CHANGELOG.md
2. Read [keepachangelog-rules.md](../references/keepachangelog-rules.md) for full rules
3. Review [changelog-examples.md](../references/changelog-examples.md) for patterns
4. Reference [categories-guide.md](categories-guide.md) when writing entries
