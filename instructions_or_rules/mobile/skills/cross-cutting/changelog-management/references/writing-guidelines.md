# Changelog Writing Best Practices

Practical tips for writing clear, helpful changelog entries that users will appreciate.

## Perspective: Who Are You Writing For?

### Your Audiences

1. **End Users** - Using your app/library
   - "What can I now do that I couldn't before?"
   - "Will my setup break?"
   - "Should I update?"

2. **Developers** - Integrating your library
   - "Will this compile with my code?"
   - "What do I need to change?"
   - "Is there a migration guide?"

3. **Project Managers** - Tracking updates
   - "What's new for the customer?"
   - "What's fixed?"
   - "Are there risks?"

4. **Yourself** - 6 months later
   - "What was I thinking when I made this change?"
   - "Why was this important?"

**Write for all of them**, starting with end users.

## Writing Principles

### 1. User-Centric Language

Write what users **can do**, not what developers **did**:

```markdown
# ✅ GOOD - User understands benefit
### Added
- Users can now export reports as PDF
- You can schedule emails to send automatically

# ℹ️️ OKAY - Still clear but developer-focused
### Added
- Implemented PDF export feature
- Added email scheduling system

# ❌ BAD - Too technical, user doesn't understand
### Added
- Integrated PDFDocument library v3.2.1
- Added queue-based job processor with cron scheduling
```

### 2. Specific, Not Vague

Be specific about **what** changed and **how it affects users**:

```markdown
# ✅ GOOD - Specific, clear impact
### Changed
- Improved search speed from 2 seconds to 200ms for typical queries
- Changed password minimum from 6 to 8 characters (effective immediately)

# ❌ BAD - Vague, unclear impact
### Changed
- Improved performance
- Changed security requirements

# ❌ BAD - Too technical
### Changed
- Refactored database query optimizer
- Updated authentication middleware
```

### 3. Active Voice

Use active voice (subject does action) not passive voice:

```markdown
# ✅ GOOD - Active
### Added
- Users can now filter by date range
- We fixed the memory leak

# ❌ BAD - Passive
### Added
- Date range filtering was added
- The memory leak was fixed
```

### 4. Action-Oriented Verbs

Start entries with strong verbs:

**For Added:**
- Added, Introduces, Launches, Enables, Allows

```markdown
- Added dark mode support
- Introduces new export formats
- Enables biometric authentication
- Allows bulk operations
```

**For Fixed:**
- Fixed, Corrected, Resolved, Patched

```markdown
- Fixed typo in settings
- Corrected calculation error
- Resolved database connection issue
- Patched security vulnerability
```

**For Changed:**
- Changed, Improved, Enhanced, Updated, Refined

```markdown
- Changed default timeout behavior
- Improved search algorithm performance
- Enhanced error messages
- Updated styling system
```

## Practical Writing Tips

### Keep Entries Concise

**Good length:** 1-2 lines maximum per entry

```markdown
### Added
- Dark mode support
- CSV export functionality
- Ability to schedule reports

# Not:
### Added
- Dark mode support for both light and dark themes which can switch in real-time
- CSV and Excel export functionality with customizable formatting options
- Ability to schedule reports to run automatically at specific times or intervals
```

### Group Similar Changes

```markdown
# ✅ GOOD - Grouped logically
### Added
- User authentication system
- Email verification
- Password reset flow
- Session management

# ❌ SCATTERED - Hard to see the pattern
### Added
- User can now login
### Changed
- Email system improved
### Added
- Password reset available
### Fixed
- Session timeout bug
```

### Use Sub-bullets for Details

When one feature has multiple parts:

```markdown
### Added
- Complete user authentication system
  - Email/password login
  - OAuth 2.0 integration (Google, Apple)
  - Two-factor authentication
  - Remember me functionality

# Instead of:
### Added
- Email/password login
- OAuth 2.0 for Google
- OAuth 2.0 for Apple
- Two-factor authentication
- Remember me functionality
```

### Include Context When Needed

```markdown
# ✅ GOOD - Provides context
### Fixed
- Fixed login timing out on connections slower than 2Mbps
- Fixed typo in German translation (email subject)
- Fixed null reference error when opening projects with no tasks

# ❌ UNCLEAR - Missing context
### Fixed
- Fixed login issue
- Fixed typo
- Fixed null reference error
```

### Mark Breaking Changes Clearly

Never sneak breaking changes into `Changed`:

```markdown
# ❌ BAD - Breaking change not obvious
### Changed
- Updated API request format for better efficiency

# ✅ GOOD - Crystal clear it's breaking
### Changed
- **BREAKING CHANGE**: API request format changed
  Old format: `POST data as form fields`
  New format: `POST data as JSON`
  Migration: See upgrade guide

# Alternatively in a line:
### Changed
- **(BREAKING)** Changed API response format from XML to JSON
```

### Real Impact, Not Just Technical Details

```markdown
# ✅ GOOD - What it means for users
### Changed
- Improved document loading speed by 60% (notice smaller PDFs load instantly)
- Changed minimum iOS version to iOS 14 (get latest performance improvements)

# ❌ TOO TECHNICAL
### Changed
- Optimized image rendering pipeline
- Updated iOS target deployment
```

## Entry Structure

### Minimum Information Entry

```markdown
### Added
- New feature name
```

### Standard Entry (Recommended)

```markdown
### Added
- Feature name with brief benefit
- Another feature for another benefit
```

### Detailed Entry (When Needed)

```markdown
### Added
- New export formats (CSV, Excel, PDF)
  - Customizable column selection
  - Scheduled export via email
  - One-click download

### Fixed
- Fixed crash when uploading large files
  Caused: Out of memory error with files >100MB
  Impact: Affected 5% of users with large datasets
  Solution: Implemented chunked upload with progress tracking
```

## Tone and Clarity

### Professional but Friendly

```markdown
# ✅ GOOD - Professional and friendly
### Added
- You can now export your data! We support CSV, Excel, and PDF formats

# ✅ ALSO GOOD - Professional and clear
### Added
- Added CSV, Excel, and PDF export formats

# ❌ TOO CASUAL
### Added
- Awesome data export feature!!!1!

# ❌ TOO FORMAL
### Added
- The system now possesses the capability to export data in the CSV, XLSX, and PDF formats
```

### Consistency

Match tone with your brand:

**Casual brand:**
```markdown
### Added
- Dark mode—your eyes will thank you
- Bulk actions—do more with less clicking
```

**Professional brand:**
```markdown
### Added
- Dark mode support for extended usage comfort
- Bulk action capability for improved efficiency
```

**What you pick:** Be consistent throughout

## Special Entry Types

### Security Fixes

```markdown
### Security
- Fixed SQL injection vulnerability in search functionality
  Severity: Critical
  Affected: All users with search access
  Action: Please upgrade immediately
  Details: CVE-2024-12345 | security@example.com
```

### Deprecations

```markdown
### Deprecated
- Old authentication method (login with username/password)
  Use: OAuth 2.0 authentication instead
  Timeline: Will be removed in v2.0.0 (January 2027)
  Migration: See docs/auth-migration.md
```

### Performance Improvements

```markdown
### Changed
- Improved search performance
  Before: 2 seconds for 10,000 items
  After: 200ms for 10,000 items (10x faster)
  Benefit: Instant search results as you type

# Or shorter:
### Changed
- Search now 10x faster (instant results)
```

### Dependency Updates

```markdown
### Changed
- Updated Flutter SDK to 3.2.0
  Reason: Better performance and stability
  Action Required: Optional, but recommended

# Or for breaking:
### Changed
- **BREAKING**: Requires Flutter 3.2.0+
  Action: Run `flutter upgrade` before updating
```

## Common Mistakes to Fix

### ❌ Too Vague

```markdown
### Fixed
- Various bug fixes and improvements
```

**Better:**
```markdown
### Fixed
- Fixed login timeout on slow networks
- Fixed incorrect date formatting in some locales
```

### ❌ Too Technical

```markdown
### Changed
- Refactored UserCubit state management with improved reducer pattern
- Migrated from GetIt v7 to v8 with service locator improvements
```

**Better:**
```markdown
### Changed
- Improved app stability and reduced crashes
- Better performance when opening large documents
```

### ❌ Internal Details

```markdown
### Added
- Added 47 new unit tests
- Added debugging information to error logs
```

**Better:** (Skip these, unless they're public-facing features)

### ❌ Inconsistent Tense

```markdown
### Added
- New feature added
- You can export data
- Implements new API

### Fixed
- Fixed the bug
- Bug was corrected
- Resolves the timeout
```

**Better:** Use consistent past tense and voice

```markdown
### Added
- New export feature
- Data exports now supported
- Export capabilities added

### Fixed
- Fixed timeout bug
- Fixed database connection issue
- Fixed styling problem
```

## Changelog Entry Checklist

Before committing your changelog:

- [ ] Written from user perspective (not developer perspective)
- [ ] Specific about what changed and how it benefits/impacts users
- [ ] Using active voice and action verbs
- [ ] Concise (1-2 lines per entry)
- [ ] Correctly categorized (Added, Changed, Fixed, etc.)
- [ ] Related entries grouped together
- [ ] Spelling and grammar correct
- [ ] Technical jargon minimized or explained
- [ ] Breaking changes marked clearly with **BREAKING CHANGE**
- [ ] Entry adds value (not internal-only information)

## Examples

### Before Update

```markdown
## [Unreleased]
### Added
- Implemented PDF export with iText library
- New endpoint for exports
- Refactored export service

### Fixed
- Fixed NullPointerException in export handler
- Fixed file permission issues
```

### After Update (Better)

```markdown
## [Unreleased]
### Added
- Users can now export reports as PDF with full formatting

### Changed
- Improved export process to handle large files better

### Fixed
- Fixed export sometimes failing with permission errors
```

## See Also

- [Categories Guide](../assets/categories-guide.md) - When to use each category
- [Keep a Changelog Rules](keepachangelog-rules.md) - Formal specification
- [Changelog Examples](changelog-examples.md) - Real-world examples
- [Changelog Template](../assets/changelog-template.md) - Copy/paste template
