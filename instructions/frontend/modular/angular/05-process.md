# Process Requirements

## 5.1. Definition of Ready (DoR)

## 5.2. Definition of Done (DoD)

## 5.3. Git Workflow

**Git Flow Management:**
Follow this strict branching model for all projects:

- **main:** Production-ready code only. Direct commits are forbidden. All changes must come through pull requests from release or hotfix branches
- **develop:** Integration branch for features. Contains the latest development changes for the next release. All feature branches must be created from and merged back into develop
- **feature/[feature-name]:** Development of specific features. Must be created from develop and merged back into develop via pull request. Use descriptive names (e.g., feature/user-authentication, feature/dashboard-widgets)
