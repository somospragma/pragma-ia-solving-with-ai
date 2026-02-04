# Test Execution Validation - CRITICAL RULE

## 0.0 Mandatory Test Execution Protocol
- ✅ **ALWAYS execute tests before ANY code change completion**
- ✅ **VERIFY test coverage meets 80% minimum threshold**
- ✅ **ENSURE tests exist for ALL modified code**
- ✅ **CONFIRM all tests pass before declaring task complete**
- ✅ **CREATE missing tests if coverage drops below threshold**
- ❌ **NO code changes without corresponding test validation**
- ❌ **NO task completion without test execution**
- ❌ **NO acceptance of failing tests**

## 0.1 Pre-Change Validation
- ✅ Run existing tests to establish baseline
- ✅ Identify which files will be modified
- ✅ Verify current test coverage for target files
- ✅ Plan test creation/modification strategy
- ❌ NO proceed without understanding current test state

## 0.2 During Development Validation
- ✅ Write tests BEFORE or ALONGSIDE code changes
- ✅ Follow TDD/BDD practices when possible
- ✅ Ensure new code has corresponding test coverage
- ✅ Maintain AAA pattern and naming conventions
- ❌ NO write code without considering test implications

## 0.3 Post-Change Validation Protocol
- ✅ **MANDATORY: Run `mvn test` / `./gradlew test` and generate JaCoCo report**
- ✅ **MANDATORY: Verify coverage meets 80% minimum**
- ✅ **MANDATORY: Confirm all tests pass (0 failures)**
- ✅ **MANDATORY: Check that new/modified code has tests**
- ❌ **NEVER complete task with failing tests**
- ❌ **NEVER accept coverage below 80%**

## 0.4 Test Coverage Requirements
- ✅ **Minimum 80% coverage for:**
  - Lines of code
  - Functions/methods
  - Branches/conditions
  - Statements
- ✅ **100% coverage required for:**
  - New functions/methods
  - Modified business logic
  - Error handling paths
- ❌ NO exceptions to minimum coverage rules

## 0.5 Test Types Validation
- ✅ **Unit tests**: For all individual functions/methods
- ✅ **Integration tests**: For API endpoints and service interactions
- ✅ **E2E tests**: For complete user workflows
- ✅ **Error scenario tests**: For all error handling paths
- ❌ NO missing test types for modified functionality

## 0.6 Execution Commands Validation
```bash
# MANDATORY execution sequence:
# Maven
mvn -T 1C clean test jacoco:report
mvn -DskipTests=false verify

# Gradle (wrapper)
./gradlew clean test jacocoTestReport
```

## 0.7 Failure Response Protocol
- ✅ **IF tests fail**: Fix code OR fix tests, then re-run
- ✅ **IF coverage drops**: Add missing tests, then re-run
- ✅ **IF new code untested**: Create tests, then re-run
- ✅ **REPEAT until all validations pass**
- ❌ **NEVER proceed with failing validations**

## 0.8 Task Completion Criteria
- ✅ **ALL tests pass (exit code 0)**
- ✅ **Coverage ≥ 80% for all metrics**
- ✅ **New/modified code has corresponding tests**
- ✅ **No test files missing for changed functionality**
- ✅ **Test execution output confirms success**
- ❌ **Task is NOT complete until ALL criteria met**

## 0.9 Documentation Requirements
- ✅ Include test execution results in task summary
- ✅ Report coverage percentages achieved
- ✅ List test files created/modified
- ✅ Confirm all validation criteria met
- ❌ NO task summary without test validation proof

## 0.10 Emergency Override Protocol
- ✅ **ONLY in critical production issues**
- ✅ **MUST document reason for override**
- ✅ **MUST create technical debt ticket**
- ✅ **MUST fix tests in next immediate task**
- ❌ **NO routine use of override**
- ❌ **NO multiple consecutive overrides**

---

**CRITICAL REMINDER**: This rule has HIGHEST PRIORITY and must be applied to EVERY code change, no exceptions. Test execution is not optional - it is mandatory for code quality and reliability.