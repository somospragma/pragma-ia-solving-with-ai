# Critical Validation Guidelines

## 0.1 NPM Dependencies Control
- ✅ Request explicit approval before any package.json changes
- ✅ Specify package name, version, and technical justification
- ✅ Stop execution until developer confirms dependency changes
- ✅ This rule takes precedence over all other guidelines
- ❌ NO install, add, or modify NPM packages without authorization
- ❌ NO assume dependency changes are acceptable

## 0.2 Context Verification Requirements
- ✅ Ask clarifying questions when context is missing
- ✅ Verify project type (MVP, POC, production)
- ✅ Confirm current state management approach
- ✅ Identify architectural restrictions and dependencies
- ✅ Understand exact use case requirements
- ❌ NO assume missing context information
- ❌ NO generate code based on assumptions
- ❌ NO invent project structure or patterns

## 0.3 Pre-Implementation Analysis
- ✅ Verify current project structure
- ✅ Identify existing dependencies and patterns
- ✅ Confirm architectural compatibility
- ✅ Validate integration with existing code
- ❌ NO proceed without structural analysis
- ❌ NO ignore existing project patterns

## 0.4 Mandatory Confirmations
- ✅ Request approval for package.json modifications
- ✅ Confirm folder structure changes
- ✅ Verify build/deployment configuration changes
- ✅ Validate new architectural pattern implementations
- ❌ NO make structural changes without confirmation
- ❌ NO implement new patterns without approval

## 0.5 Execution Halt Conditions
- ✅ Stop when project context is unclear
- ✅ Halt for unconfirmed dependency requirements
- ✅ Pause when conflicts with existing patterns exist
- ✅ Stop when critical implementation information is missing
- ❌ NO continue with uncertain project state
- ❌ NO proceed with incomplete requirements

## 0.6 Test Execution Mandate
- ✅ **EXECUTE tests after EVERY code change**
- ✅ **VERIFY 80% minimum coverage maintained**
- ✅ **ENSURE all tests pass before task completion**
- ✅ **CREATE tests for new/modified code**
- ✅ **REPORT test results in task summary**
- ❌ **NO task completion without test validation**
- ❌ **NO acceptance of failing tests**
- ❌ **NO coverage below 80% threshold**

## 0.7 Communication Protocol
- ✅ Communicate ALWAYS in Spanish with the developer
- ✅ Explain all actions before execution
- ✅ List files to be created or modified
- ✅ Specify required dependencies (without installing)
- ✅ Describe architectural impact
- ✅ Use confirmation format for major changes
- ❌ NO perform actions without explanation
- ❌ NO hide implementation details
- ❌ NO communicate in English unless explicitly requested

## 0.8 Rule Precedence Order
- ✅ Apply Test Execution Validation (00-test) FIRST always
- ✅ Apply Critical Validation (00-critical) SECOND always
- ✅ Follow with Architecture (01), Error Handling (02), Security (06)
- ✅ Then Code Style (03), Testing (04), Production (05)
- ✅ Finally Docker (08), Performance (07)
- ❌ NO skip test execution validation
- ❌ NO skip critical validation steps
- ❌ NO apply rules out of precedence order