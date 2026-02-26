# Keep a Changelog - Complete Rules

The official specification for maintaining changelogs based on [Keep a Changelog](https://keepachangelog.com).

## Full Specification

### Format

A changelog is a file that contains a curated, chronologically ordered list of notable changes for each version of a project.

### Purpose

A changelog helps:
- Users understand what changed between versions
- Contributors understand the project's evolution
- Developers know if an update will break their code
- Release managers communicate impact to stakeholders

### Core Principles

1. **Chronological Order** - Newest version first
2. **Consistency** - Same format throughout
3. **Clarity** - Anyone can understand changes
4. **Completeness** - All notable changes included
5. **User-Focused** - Written for end users, not developers

## Structure

### Header with Version and Date

```markdown
## [X.Y.Z] - YYYY-MM-DD
```

- **X.Y.Z** = Semantic version (MAJOR.MINOR.PATCH)
- **YYYY-MM-DD** = Release date in ISO 8601 format
- Brackets around version for linking
- Unreleased section has no date

### Category Sections

Each release has up to 6 categories (only include sections with content):

```markdown
## [1.2.0] - 2011-04-08
### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security
```

**Do NOT create custom categories.** This standardization helps everyone quickly find information.

### Entries

Under each category, use bullet points:

```markdown
### Added
- Short, clear description of what was added
- Another new feature users can now use
- Feature with breaking change clearly marked
```

## The Six Categories

### 1. Added

New functionality, features, or capabilities that users can now use.

```markdown
### Added
- New dark theme support
- Email notification preferences
- Search filters for advanced queries
- Bulk export functionality
```

**Write from user perspective:**
- ✅ "Users can now export data in CSV format"
- ❌ "Implemented export feature"

### 2. Changed

Changes to existing functionality - behavioral changes, improvements, but still backward compatible.

```markdown
### Changed
- Improved upload speed for large files
- Enhanced error messages to be more helpful
- Changed default timeout from 30s to 60s
- Updated UI for better accessibility
```

**Mark clearly if there's breaking potential:**
```markdown
### Changed
- **BREAKING**: Changed API response format from XML to JSON
```

### 3. Deprecated

Features that will be removed in a future version. Users need time to migrate.

```markdown
### Deprecated
- `getUserData()` API endpoint (use `getUser()` instead)
- Legacy CSV export format (switch to new JSON format)
- Support for Internet Explorer 11 (ending in v3.0.0)
```

**Always include migration path:**
```markdown
### Deprecated
- Deprecated old authentication method
  Migrate: Use the new OAuth 2.0 flow
  Timeline: Will be removed in v2.0.0
```

### 4. Removed

Features that were previously deprecated and are now actually removed.

```markdown
### Removed
- Removed legacy API v1 endpoints
- Removed Flash-based video player
- Removed deprecated ConfigFile class
- Removed support for Python 2.7
```

**Only remove deprecated features:**
- Features should be in `Deprecated` for at least one major version before being `Removed`

### 5. Fixed

Bug fixes, corrections, and patches.

```markdown
### Fixed
- Fixed crash when uploading files over 100MB
- Fixed typo in welcome screen
- Fixed memory leak in data synchronization
- Fixed sorting not working on mobile devices
```

**Be specific about the problem:**
- ✅ "Fixed login page crash when entering special characters"
- ❌ "Fixed bug in authentication"

### 6. Security

Vulnerabilities and security fixes.

```markdown
### Security
- Fixed SQL injection vulnerability in search
- Patched XSS vulnerability in user comments
- Updated vulnerable dependency (CVE-2024-1234)
```

**Always include:**
- What the vulnerability was
- Any affected users
- How to upgrade/patch

## Unreleased Section

The `[Unreleased]` section comes first and collects all changes since the last release.

```markdown
## [Unreleased]
### Added
- New user dashboard feature
- Email digest notifications

### Fixed
- Login timeout on mobile networks

### Changed
- Improved search performance
```

**Rules:**
- Always include at the top
- Remove and move to version section when releasing
- Can have multiple categories
- No date (versions have dates, not "unreleased")

## Linking Versions

At the bottom of the changelog, add comparison links for easy navigation:

```markdown
## [1.2.0] - 2011-04-08
...

## [1.1.0] - 2026-01-15
...

[unreleased]: https://github.com/org/repo/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/org/repo/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/org/repo/releases/tag/v1.1.0
```

**Format:**
- `[unreleased]`: Compare unreleased changes with last tagged version
- `[X.Y.Z]`: Compare this version with previous version
- Links point to GitHub (or your VCS) for easy access

## Entry Guidelines

### Be Concise

```markdown
# ✅ GOOD - Clear and brief
### Added
- User can now export reports as PDF

# ❌ BAD - Too verbose
### Added
- Implementation of a new feature that allows users to take their data in the form of a PDF file which can then be sent to third parties or stored locally for archival purposes
```

### Use Active Voice

```markdown
# ✅ GOOD
### Fixed
- Fixed database connection timeout issue

# ❌ BAD
### Fixed
- Database connection timeout was fixed
```

### Group Related Changes

```markdown
# ✅ GOOD - Related authentication changes together
### Added
- User login system
- Two-factor authentication
- Session management

# ❌ LESS ORGANIZED - Scattered
### Added
- User login system
### Changed
- Session timeout behavior
### Added
- Two-factor authentication
```

### Reference Issues and PRs

```markdown
### Added
- New search filters (#123)

### Fixed
- Login crash on slow networks (fixes #456)
```

### Mark Breaking Changes

```markdown
## [2.0.0] - 2021-02-19
### Changed
- **BREAKING**: Removed `getUserData()` method
  Use `getUser()` instead

- **BREAKING**: Changed API request format
  Old: POST data as form fields
  New: POST data as JSON body

### Removed
- Removed legacy CSV import tool
```

## Examples

### Complete Changelog

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- New analytics dashboard
- Export charts as PNG

## [2.1.0] - 2021-02-19
### Added
- Dark mode support
- Keyboard shortcuts for common actions

### Changed
- Improved search performance by 40%
- Redesigned settings page

### Deprecated
- Old API endpoint `/api/v1/users` (use `/api/v2/users` instead)

### Fixed
- Fixed crash when opening very large files
- Fixed typos in French translations

## [2.0.0] - 2026-01-10
### Changed
- **BREAKING**: Changed authentication to OAuth 2.0

### Removed
- Removed deprecated custom auth system

## [1.9.0] - 2025-12-20
### Added
- Initial dark mode beta

[unreleased]: https://github.com/org/repo/compare/v2.1.0...HEAD
[2.1.0]: https://github.com/org/repo/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/org/repo/compare/v1.9.0...v2.0.0
[1.9.0]: https://github.com/org/repo/releases/tag/v1.9.0
```

### Per-Category Examples

```markdown
## [1.5.0] - 2011-04-08

### Added
- Support for exporting data in Excel format
- New dark theme
- API rate limit information in response headers
- German language translations

### Changed
- Improved performance of data synchronization by 30%
- Updated design of user profile page
- Changed password requirements from 6 to 8 characters minimum

### Deprecated
- Old XML export format (use JSON instead)
- Legacy authentication method (migrate to OAuth 2.0)

### Removed
- Removed Flash-based video player (use HTML5 video)
- Removed support for IE 11

### Fixed
- Fixed memory leak in background sync
- Fixed typo in welcome email
- Fixed sorting not working on mobile

### Security
- Fixed SQL injection vulnerability in search
- Updated vulnerable libraries (CVE-2024-0001, CVE-2024-0002)
```

## Common Patterns

### New Feature Launch

```markdown
### Added
- Complete user authentication system
  - Login with email/password
  - Password recovery flow
  - Two-factor authentication
  - Session management
```

### Major Refactoring (Customer Perspective)

```markdown
### Changed
- **Internal refactoring for reliability**
  Moved from legacy system to modern architecture
  Users will notice improved stability and faster response times
```

### Security Patch

```markdown
### Security
- Fixed critical vulnerability in file upload validation
  Severity: High
  Affects: All users with file upload capability
  Action: Upgrade immediately
  Details: https://security.example.com/cve-2024-xxxx
```

### Beta Feature to Stable

```
### Changed
- Dark theme moved from beta to stable (see v1.4.0 for beta notes)
```

### Deprecation Timeline

```markdown
### Deprecated
- `old_api_method()` - Deprecated in v2.0.0
  Migration: Use `new_api_method()` instead
  Removal: Will be removed in v3.0.0 (Q4 2026)
  Docs: See migration guide at docs/api-migration.md
```

## Validation Checklist

When writing a changelog entry:

- ☐ Correct semantic version (MAJOR.MINOR.PATCH)
- ☐ Correct date format (YYYY-MM-DD)
- ☐ Using only 6 standard categories
- ☐ Entries written from user perspective
- ☐ Clear, concise descriptions
- ☐ Spelling and grammar checked
- ☐ Related entries grouped together
- ☐ Breaking changes marked clearly
- ☐ Links and references working
- ☐ Categories only included if they have content
- ☐ Unreleased section at the top
- ☐ Version links at bottom updated

## See Also

- [Keep a Changelog Official](https://keepachangelog.com/)
- [Semantic Versioning](https://semver.org/)
- [Common Changelog Mistakes](https://keepachangelog.com/en/1.0.0/#bad-practices)
