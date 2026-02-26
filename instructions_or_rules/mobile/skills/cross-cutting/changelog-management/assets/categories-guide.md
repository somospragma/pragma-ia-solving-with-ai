# Changelog Categories Guide

Quick reference for when to use each category and what to write in each.

## The 6 Categories

### 1. ✨ Added

**When to use:** New features, functionality users can now use, new capabilities

**Perspective:** User-facing benefit

**Examples:**
- ✅ Added dark mode support
- ✅ Added ability to export data as CSV
- ✅ Added search filters to product list
- ✅ Added two-factor authentication
- ✅ Added keyboard shortcuts (Cmd+S to save)

**Not to use for:**
- ❌ Added unit tests (internal improvement)
- ❌ Added support for new database (unless user-visible)
- ❌ Added internal logging (unless feature that users care about)

**Pattern:**
```markdown
### Added
- User can now [do something new]
- New [feature] for [use case]
- Support for [new capability]
```

---

### 2. 🔧 Changed

**When to use:** Behavior changes, modifications to existing features, improvements to existing functionality

**Perspective:** User impact (even if still backward compatible)

**Examples:**
- ✅ Changed default timeout from 30s to 60s
- ✅ Improved search performance by 40%
- ✅ Changed UI layout for better accessibility
- ✅ Changed password minimum length from 6 to 8 characters
- ✅ Improved error messages to be more helpful

**Backward Compatibility:**
- If still backward compatible: Goes in `Changed`
- If breaks existing behavior: Mark as **BREAKING CHANGE**

**Not to use for:**
- ❌ Internal refactoring (unless impacts user-visible behavior)
- ❌ Optimizations users don't notice (minor performance)
- ❌ Code reorganization

**Pattern:**
```markdown
### Changed
- Changed [what changed] from [old] to [new]
- Improved [feature] by [benefit]
```

---

### 3. ⚠️ Deprecated

**When to use:** Features that will be removed in future version

**Timeline Required:** Always specify when it will be removed

**Migration Path Required:** Always explain what to use instead

**Examples:**
- ✅ Deprecated old authentication method (use OAuth 2.0 instead)
- ✅ Deprecated XML export (JSON available, XML removal in v2.0)
- ✅ Deprecated Python 2.7 support (Python 3.6+ required in v1.1)
- ✅ Deprecated `getUserData()` API call (use `getUser()` instead)

**Rules:**
- Must include migration path
- Must include removal timeline
- Users need time to migrate (at least one major version)
- Should be in CHANGELOG in current and next versions

**Pattern:**
```markdown
### Deprecated
- [Old feature] (use [new feature] instead)
  Removal: v2.0.0 in [month/year]
  Migration: See [guide link]
```

---

### 4. 🗑️ Removed

**When to use:** Features that were previously `Deprecated` and are now actually removed

**Rules:**
- Only remove if previously deprecation was announced and given time to migrate
- Features should be deprecated for at least one major version first

**Examples:**
- ✅ Removed legacy API v1 endpoints (deprecated in v1.5)
- ✅ Removed Flash-based video player (deprecated in v1.8)
- ✅ Removed Python 2.7 support (announced in v2.0)
- ✅ Removed old authentication system

**Not to use for:**
- ❌ Features never announced as deprecated
- ❌ Testing old code path
- ❌ Removing code locally (only public APIs)

**Pattern:**
```markdown
### Removed
- Removed [old feature] (was deprecated in v1.5)
- Removed [old system] (migrate to [new system])
```

---

### 5. 🐛 Fixed

**When to use:** Bug fixes, corrections, patches for existing bugs

**Specificity Required:** Be specific about what was broken

**Examples:**
- ✅ Fixed login page crash when entering special characters
- ✅ Fixed memory leak in background sync process
- ✅ Fixed typo in welcome email
- ✅ Fixed sorting not working on mobile devices
- ✅ Fixed database connection timeout on slow networks

**Not to use for:**
- ❌ Code cleanup (use `Changed` or `Refactored`)
- ❌ Performance improvements (usually `Changed`)
- ❌ Internal restructuring

**Pattern:**
```markdown
### Fixed
- Fixed [what was broken]
- Fixed [bug] when [condition]
```

---

### 6. 🔒 Security

**When to use:** Vulnerability fixes, security patches, CVE addresses

**Critical Information Required:**
- What the vulnerability was
- Severity level (Critical, High, Medium)
- Who is affected
- What users should do

**Examples:**
- ✅ Fixed SQL injection vulnerability in search
- ✅ Fixed XSS vulnerability in user comments
- ✅ Fixed privilege escalation in admin panel
- ✅ Updated vulnerable dependency (CVE-2024-1234)

**Rules:**
- Always be specific about the security issue
- Include severity level
- Include who should upgrade
- Include CVE number if available
- Encourage immediate upgrade

**Pattern:**
```markdown
### Security
- Fixed [vulnerability name]
  Severity: [Critical/High/Medium]
  Affects: [who is affected]
  Action: [upgrade immediately/update optional]
  Details: [link to security advisory]
```

---

## Decision Tree

**Is this a new user capability?**
→ Yes = `Added`
→ No = Next question

**Is this a change to existing feature (but still backward compatible)?**
→ Yes = `Changed`
→ No = Next question

**Is this a breaking change?**
→ Yes = `Changed` (with **BREAKING CHANGE** label)
→ No = Next question

**Is this a feature that will be removed in future?**
→ Yes = `Deprecated`
→ No = Next question

**Is this a feature removal (after previous deprecation)?**
→ Yes = `Removed`
→ No = Next question

**Is this a bug fix?**
→ Yes = `Fixed`
→ No = Next question

**Is this a security issue?**
→ Yes = `Security`
→ No = This might not go in CHANGELOG (internal change only)

---

## Common Categorization Examples

### Authentication Feature

```markdown
## First Release (Announcement)
### Added
- User authentication system
- Login with email and password
- Password recovery flow

## Later Release (Improvement)
### Changed
- Improved authentication security
- Added support for biometric login

## Even Later (New Option)
### Added
- Two-factor authentication support

## Much Later (Old Method)
### Deprecated
- Password-only authentication
  Users should enable 2FA
  Removal: v3.0.0

## Final Release (Cleanup)
### Removed
- Pass-only authentication without 2FA
```

### API Changes

```markdown
## v1.5.0
### Added
- New API v2 with improved response format

### Deprecated
- Old API v1 endpoints
  Use new v2 endpoints
  Removal: v2.0.0

## v2.0.0
### Changed
- **BREAKING**: Removed API v1
  All clients must migrate to v2

### Removed
- Old API v1 endpoints
```

### Bug with Security Impact

```markdown
### Fixed
- Fixed memory leak in data sync

### Security
- Fixed buffer overflow in image processing
  Severity: Critical
  Affects: All users
  Action: Upgrade immediately
```

---

## What NOT to Include

Material thatdoes **NOT** go in changelog (too internal):

- ❌ Refactoring for code quality (unless impacts users)
- ❌ Adding tests
- ❌ Updating dependencies (unless security or breaking change)
- ❌ Deploy process changes
- ❌ Documentation-only updates (unless it's important guidance)
- ❌ CI/CD pipeline improvements
- ❌ Code comments or naming improvements

**Exception**: If these changes significantly impact users, they can be mentioned:
- Security: "Updated vulnerable dependency (CVE-2024-xxx)"
- Performance: "Improved search performance by 50%"
- Stability: "Fixed memory leak causing crashes"

---

## Entry Length Guidelines

### Per-Entry

**Short entries:**
```markdown
### Added
- Dark mode support
- Export as PDF
- Keyboard shortcuts
```

**Longer entries (with sub-bullets):**
```markdown
### Added
- Complete authentication system
  - Email/password login
  - OAuth 2.0 integration
  - Two-factor authentication
  - Session management
```

**Very detailed entries (with rationale):**
```markdown
### Security
- Fixed critical SQL injection in search
  Severity: Critical
  Affects: All users with search permissions
  Action: Upgrade immediately
  Discovery: Internal security audit
  Details: https://security.example.com/advisory-001
```

---

## Order of Categories in Release

Always use this order if multiple categories present:

1. Added
2. Changed
3. Deprecated
4. Removed
5. Fixed
6. Security

```markdown
## [2.0.0] - 2011-04-08

### Added
- First new thing

### Changed
- First change

### Deprecated
- First deprecation

### Removed
- First removal

### Fixed
- First bug fix

### Security
- First security fix
```

This standardization helps users quickly scan for what they need.

---

## Quick Reference Table

| Question | Answer | Category |
|----------|--------|----------|
| New user capability? | Yes | **Added** |
| Change to existing feature? | Yes (no breaking) | **Changed** |
| Breaking change? | Yes | **Changed** (marked BREAKING) |
| Will be removed soon? | Yes | **Deprecated** |
| Was deprecated, now removed? | Yes | **Removed** |
| Bug fix? | Yes | **Fixed** |
| Security vulnerability? | Yes | **Security** |
| Internal improvement? | Yes | Don't include |

---

## See Also

- [Keep a Changelog Rules](../references/keepachangelog-rules.md)
- [Changelog Examples](../references/changelog-examples.md)
- [Changelog Template](changelog-template.md)
- [Semantic Versioning Guide](../SKILL.md#semantic-versioning-guide)
