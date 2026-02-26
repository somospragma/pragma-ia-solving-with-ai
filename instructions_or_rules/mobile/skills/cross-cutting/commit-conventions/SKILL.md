---
name: commit-conventions
description: Conventional Commits specification for commit messages including types (feat, fix, docs, etc), scopes, and message body/footer conventions. Use when writing commit messages, understanding commit structure, or reviewing commit history.
metadata:
  author: Pragma Mobile Chapter
  version: "1.0"
---

# Commit Conventions

This skill explains how to write structured, meaningful commit messages using Conventional Commits specification.

## Commit Message Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Components

**Type** (required) - What kind of change:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style (formatting, trailing commas - no functional change)
- `refactor`: Code refactoring (no feature change, no bug fix)
- `test`: Adding or updating tests
- `chore`: Build process, dependencies, configuration
- `ci`: CI/CD configuration changes

**Scope** (optional) - What part of codebase:
- Feature name: `feat(auth):`
- Package name: `feat(commons):`
- Module: `fix(di):`
- Specific component: `style(user):`

**Description** (required) - Concise summary:
- Imperative mood ("add feature", not "added feature")
- Not capitalized
- No period at end
- Maximum 50 characters

**Body** (optional) - Detailed explanation:
- Explain what and why, not how
- Use imperative mood
- Separate from description with blank line
- Wrap at 72 characters
- Use when commit may not be obvious

**Footer** (optional) - References and breaking changes:
- Reference issues: `Closes #123`, `Fixes #456`
- Breaking changes: `BREAKING CHANGE: description`

## Examples

### Simple Feature

```
feat(auth): implement login with email and password

This commit adds the complete authentication flow including:
- User login form with validation
- Session management
- Error handling for invalid credentials
```

### Bug Fix

```
fix(user_profile): correct user avatar image not displaying

The image URL was incorrectly parsed from the API response.
Changed from `response.image` to `response.avatar_url` to match
actual API contract.

Closes #234
```

### Documentation

```
docs(README): update installation instructions for new setup process
```

### Code Style

```
style(analysis_options): add trailing commas to functions

No functional changes - purely formatting for improved readability
and auto-format compatibility.
```

### Refactoring

```
refactor(user_repository): extract caching logic to separate method

Improve code readability by moving cache strategy to dedicated
_getFromCacheOrRemote method.
```

### Test Addition

```
test(get_user_usecase): add tests for error scenarios

Adds comprehensive error handling tests:
- Repository returns null
- Exception thrown by repository
- Network timeout
- Invalid user ID
```

### Chore

```
chore(pubspec): upgrade pip to 8.1.0
```

### Multiple Lines Example

```
feat(maps): add geolocation feature for user location tracking

Implement complete geolocation feature including:
- Permission handling for Location services
- Real-time location updates
- Location caching and history
- Background location updates

Uses geolocator package v10.0.0

Closes #567
BREAKING CHANGE: LocationService API changed from callback-based
to Stream-based to support real-time updates.
```

## Writing Effective Commits

### Do's ✅

```bash
✅ Commit frequently (small, logical units)
✅ Use imperative mood ("add feature", "fix bug")
✅ Clear, descriptive messages
✅ One logical change per commit
✅ Fix related issues in footer

git commit -m "feat(auth): implement password reset flow"
git commit -m "docs(implementation): update testing guidelines"
```

### Don'ts ❌

```bash
❌ Vague messages ("update stuff", "fix things")
❌ Multiple unrelated changes in one commit
❌ Long description in subject line
❌ Passive voice ("was fixed", "has been added")
❌ Mixing features and fixes in one commit

# ❌ BAD
git commit -m "update code"
git commit -m "fixed bugs and added features and updated docs"
git commit -m "feat: implemented authentication, user profile, dashboard"
```

## Scope Guidelines

Choose scope based on impact scale:

```
feat(auth): ← Whole auth feature
feat(login_form): ← Specific component
feat(di): ← Dependency injection system
docs(project-structure): ← Specific doc
```

## Breaking Changes

Clearly indicate breaking changes:

```
feat(api_client)!: change authentication header format

BREAKING CHANGE: Authorization header changed from
'Bearer <token>' to 'X-Auth-Token: <token>'

Old code:
  headers: {'Authorization': 'Bearer $token'}

New code:
  headers: {'X-Auth-Token': '$token'}
```

Or with exclamation mark:

```
feat(user_repository)!: change getUser return type to Future<UserEntity>

Previously returned UserModel directly.
Now properly returns typed Result<UserEntity, Exception>.
```

## Scope Reference

Common scopes in this project:

```
# Features
feature-name  (auth, maps, user-profile, dashboard)

# Packages
commons, main, di, config

# Layers
domain, data, presentation, di

# Specific components
user, auth_page, user_mapper

# Configuration
pubspec, analysis_options, git_hooks
```

## Commit Best Practices

### Atomic Commits

Each commit should be a complete, standalone unit:

```bash
# ✅ GOOD - Related changes in one commit
git commit -m "feat(auth): implement email validation

- Add email regex pattern
- Add validation to login form  
- Add tests for validation"

# ❌ BAD - Unrelated changes
git commit -m "feat(auth): add validation and update docs and fix typo"
```

### Frequent, Small Commits

```bash
# ✅ GOOD - Logical progression
git commit -m "feat(auth): add auth repository abstract class"
git commit -m "feat(auth): implement email login usecase"
git commit -m "feat(auth): create login page UI"
git commit -m "test(auth): add authentication tests"

# ❌ BAD - Large monolithic commit
git commit -m "feat(auth): implement complete authentication system with UI and tests"
```

### Fix Mistakes Properly

```bash
# Fix in previous commit (not yet pushed)
git commit --amend -m "feat(auth): corrected implementation"

# Fix in earlier commit (create new commit)
git commit -m "fix(auth): resolve issue from login feature"

# Interactive rebase for local-only commits (not yet pushed)
git rebase -i HEAD~3
```

## Viewing Commit History

```bash
# View conventional commits clearly
git log --oneline
git log --format="%h %s" --graph

# Filter by type
git log --grep="^feat"   # Features only
git log --grep="^fix"    # Fixes only

# View specific range
git log develop..feature/hu-123
```

## Validation (Optional)

Commitlint can automatically validate commit messages:

```bash
# Validate last commit
commitlint --from HEAD~1

# Validate all commits in range
commitlint --from origin/develop --to HEAD
```

## Maintaining Changelog

**Before committing significant changes**, update the CHANGELOG.md file following Keep a Changelog format or skills changelog guidelines.

### When to Update CHANGELOG

Update CHANGELOG for commits that:
- ✅ Add new features (`feat`)
- ✅ Fix bugs (`fix`)
- ✅ Make breaking changes
- ✅ Add significant documentation (`docs` for major updates)
- ✅ Deprecate functionality
- ✅ Remove features
- ❌ NOT for: chore, style, test, refactor (unless significant)

### Workflow

```bash
# 1. Make your code changes
# 2. Update CHANGELOG.md with your changes (see skill changelog management)
# 3. Create code commit with conventional format
git commit -m "feat(auth): implement JWT authentication"

# 4. Create separate commit for CHANGELOG update
git commit -m "docs(changelog): add JWT authentication feature entry"

# ❌ No combine preferred add .:
git add . && git commit -m "feat(auth): implement JWT authentication

Adds JWT-based authentication with token refresh functionality

Updated CHANGELOG.md with new feature entry"
```

### Example Workflow

```bash
# After implementing a feature
git add lib/src/data/repositories/user_repository_impl.dart
git commit -m "feat(user): add user profile repository implementation"

# Update CHANGELOG.md in [Unreleased] section
# Add: "- Add user profile repository with caching support"
git add CHANGELOG.md
git commit -m "docs(changelog): add user profile repository entry"
```

For detailed guidance on changelog structure and best practices, see Changelog Management skill or [Keep a Changelog Official](https://keepachangelog.com/) - Full specification.

## For Extended Guidance

- [conventional-commits.md](./references/conventional-commits.md) - detailed examples 
- [Conventional Commits Spec](https://www.conventionalcommits.org/) - Official specification
