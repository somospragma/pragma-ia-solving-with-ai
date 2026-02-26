# Conventional Commits Specification

This is the detailed specification for the Conventional Commits format used in this project.

## Full Specification

### Structure

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Type

MUST be one of the following:

- **`feat`** - A commit that adds a new feature to the application or library
- **`fix`** - A commit that patches a bug in your codebase
- **`docs`** - A commit that updates documentation (README, guides, etc)
- **`style`** - A commit that does not affect code logic:
  - Formatting (indentation, semicolons, spacing)
  - Trailing commas
  - Line breaks
  - **No functional changes**
- **`refactor`** - A code change that neither fixes a bug nor adds a feature
  - Extracting methods
  - Renaming variables
  - Reorganizing code structure
- **`perf`** - A code change that improves performance
  - Optimizations
  - Caching improvements
  - Reducing memory usage
- **`test`** - Adding missing tests or correcting existing tests
  - Unit tests
  - Integration tests
  - Widget tests
  - Test infrastructure changes
- **`build`** - Changes affecting build system or dependencies
  - Updating dependencies
  - Build configuration
  - Gradle changes
  - Build script modifications
- **`ci`** - Changes to CI/CD configuration
  - GitHub Actions
  - CI pipeline setup
  - Testing infrastructure

### Scope (Optional)

The scope SHOULD specify what is being changed. Examples:

- Feature name: `feat(auth):`
- Package name: `feat(commons):`
- Module name: `fix(di):`
- Component: `style(user_cubit):`
- Problem it solves: `fix(memory-leak):`

Scope helps readers quickly understand the impact area.

### Description

The description MUST:

- Use the imperative, present tense ("add" not "adds", "added", "adding")
- Not capitalize the first letter
- Not end with a period (.)
- Be 50 characters or less
- Clearly explain what the commit does

Good descriptions:
```
feat(auth): add email verification flow
fix(user_profile): correct avatar image not displaying
docs(setup): update installation instructions
test(payment): add edge case tests for tax calculation
```

Bad descriptions:
```
feat(auth): Added Email Verification Flow.    # Capitalized, period, past tense
fix(user_profile): Fixed avatars              # Vague
Update stuff                                  # No type, no scope
refactor: code cleanup 😀                     # No scope, emoji
```

### Body (Optional)

The body SHOULD be present when the commit needs explanation beyond what the subject provides.

The body MUST:

- Be separated from the description by a blank line
- Use imperative, present tense
- Explain **what** and **why**, not **how**
- Wrap at 72 characters
- Reference related issues: `Closes #123`

Example:

```
feat(maps): add geolocation tracking

Implement complete geolocation feature enabling:
- Real-time user location updates
- Location history tracking
- Background location services
- Geofence alerts

Uses geolocator package v10.0.0 for maximum
compatibility across iOS and Android platforms.

Closes #567
Relates to #789
```

### Footer (Optional)

Footers SHOULD communicate:

1. **Issue References**
   - `Closes #123` - Closes issue #123
   - `Fixes #456` - Fixes bug #456  
   - `Relates to #789` - Related to issue #789
   - `References #101` - References issue #101

2. **Breaking Changes**
   - `BREAKING CHANGE: <description>`
   - Description explains what changed and migration path

Example with breaking change:

```
feat(api)!: change authentication header format

BREAKING CHANGE: Authorization header format changed.

Old format:
  Authorization: Bearer <token>

New format:
  X-Auth-Token: <token>

Migrate by:
1. Update all API call headers
2. Remove 'Bearer' prefix from tokens
3. Use new 'X-Auth-Token' header name

Closes #234
```

## Real Examples

### Minimal Feature

```
feat(dashboard): add user statistics widget
```

### Feature with Details

```
feat(search): implement full-text search for products

Add full-text search capability enabling users to:
- Search across product names and descriptions
- Filter results by category and price range
- Sort results by relevance and date

Integrates with Elasticsearch for efficient indexing.

Closes #542
```

### Bug Fix

```
fix(image_upload): handle large files correctly

Previous implementation would crash when uploading
files larger than 10MB. Now implements chunked upload
for files larger than 5MB threshold.

Also improved error messages to be more user-friendly.

Fixes #289
```

### Refactoring

```
refactor(repository): extract cache logic to service

Extract caching strategy to dedicated CacheService
to improve code reusability and testability.

No functional changes.
```

### Documentation

```
docs(contributing): add debugging section with examples
```

### Test Addition

```
test(user_cubit): add tests for error handling

Add comprehensive error scenario tests:
- Repository timeout
- Network error
- Invalid user ID
- Null response handling

Covers all error paths in UserCubit.
```

### Multiple Changes (Should be separate commits)

```
# ✅ GOOD - Separate commits for each concern
git commit -m "feat(auth): add refresh token mechanism"
git commit -m "test(auth): add comprehensive token tests"  
git commit -m "docs(auth): update security guidelines"

# ❌ BAD - Everything in one
git commit -m "feat: add refresh token, tests, and docs"
```

## When to Commit

### Commit Frequently

Aim for small, logical units:

```bash
# Good commit sequence:
git commit -m "feat(user): add UserEntity class"
git commit -m "feat(user): implement UserRepository interface"
git commit -m "test(user): write repository tests"
git commit -m "feat(user): create user_cubit state management"
git commit -m "feat(ui): implement user detail page"

# Not:
git commit -m "feat: implement entire user feature with UI and tests"
```

### Atomic Changes

Each commit should be:
- Self-contained
- Logically complete
- Build and test successfully on its own

```bash
# ✅ GOOD - Logically complete
git commit -m "feat(login): add form validation"
# Changes: validation.dart + validation_test.dart + page widget update

# ❌ AVOID - Incomplete (tests don't run)
git commit -m "feat(login): add form validation"
# Changes: only validation.dart, forgotten test file
```

## Commit Message Tool

You can create a `.gitmessage` template:

```
# <type>(<scope>): <subject>
#
# <body>
#
# <footer>

# Type: feat, fix, docs, style, refactor, perf, test, build, ci
# Scope: What part of code is affected
# Subject: What this commit does (50 chars max, imperative mood)
#
# Body: Explain what and why (wrap at 72 chars)
# Footer: Closing issues, breaking changes
```

Use it with:

```bash
git config commit.template .gitmessage
```

## Benefits

Conventional Commits provide:

- ✅ **Readability** - Anyone can understand changes quickly
- ✅ **Automation** - Tools can parse commits automatically
- ✅ **Changelog Generation** - Auto-generate release notes
- ✅ **Semantic Versioning** - Determine version bumps (major/minor/patch)
- ✅ **Blame/History** - Easy to find related changes
- ✅ **Code Review** - Better context for reviewers

## See Also

- [Conventional Commits Official](https://www.conventionalcommits.org/)
