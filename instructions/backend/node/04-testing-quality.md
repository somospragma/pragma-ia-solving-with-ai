# Testing and Quality Guidelines

## 4.1 API Component Testing
- ✅ Implement component/integration tests
- ✅ Test APIs from consumer perspective
- ✅ Cover main business flows
- ✅ Use tools like supertest
- ❌ NO depend only on unit tests
- ❌ NO test only internal implementation

## 4.2 Test Name Structure
- ✅ Format: "When [scenario], should [expected behavior]"
- ✅ Include: condition, action, expected result
- ✅ Make names descriptive and specific
- ✅ Facilitate test purpose understanding
- ❌ NO use generic or ambiguous names
- ❌ NO omit test context

## 4.3 AAA Pattern
- ✅ Arrange: setup data and mocks
- ✅ Act: execute function under test (1 line)
- ✅ Assert: verify expected result (1 line)
- ✅ Visually separate the 3 sections
- ❌ NO mix phases
- ❌ NO make multiple actions or assertions

## 4.4 Unified Node Version
- ✅ Specify Node version in `.nvmrc`
- ✅ Use same version in development, testing, production
- ✅ Document required version in README
- ✅ Use tools like nvm or Volta
- ❌ NO allow inconsistent versions between environments
- ❌ NO ignore version differences

## 4.5 Avoid Global Test Fixtures
- ✅ Create specific data for each test
- ✅ Clean data after each test
- ✅ Use factories or builders for test data
- ✅ Keep tests independent
- ❌ NO share data between tests
- ❌ NO depend on test execution order
- ❌ NO skip tests to make them pass (it.skip, describe.skip, xit)
- ❌ NO use .only to avoid running other tests

## 4.6 Tag Tests
- ✅ Use tags like `@smoke`, `@integration`, `@unit`
- ✅ Allow selective test execution
- ✅ Categorize by speed and type
- ✅ Facilitate CI/CD with different testing levels
- ❌ NO execute all tests always
- ❌ NO mix test types without categorization

## 4.7 Test Coverage
- ✅ Measure code coverage
- ✅ Identify incorrect testing patterns
- ✅ Aim for high coverage but not obsessive 100%
- ✅ Use tools like Istanbul/NYC
- ❌ NO use coverage as only quality metric
- ❌ NO ignore quality for coverage

## 4.8 Production-like E2E Environment
- ✅ Use Docker for environment consistency
- ✅ Include all external dependencies
- ✅ Simulate production conditions
- ✅ Use docker-compose for orchestration
- ❌ NO test only in development environment
- ❌ NO ignore infrastructure differences

## 4.9 Static Analysis Refactoring
- ✅ Use tools like SonarQube, CodeClimate
- ✅ Monitor cyclomatic complexity
- ✅ Identify code smells automatically
- ✅ Integrate in CI/CD pipeline
- ❌ NO ignore technical debt
- ❌ NO postpone refactoring indefinitely

## 4.10 Mock External HTTP Services
- ✅ Use nock, msw or similar for mocking
- ✅ Simulate different response scenarios
- ✅ Test external service error handling
- ✅ Include timeouts and delays in mocks
- ❌ NO depend on real services in tests
- ❌ NO test only happy paths

## 4.11 Test Middlewares in Isolation
- ✅ Test middlewares independently
- ✅ Mock request/response objects
- ✅ Verify specific middleware behavior
- ✅ Use stubs for next() function
- ❌ NO test middlewares only in full context
- ❌ NO ignore edge cases in middlewares

## 4.12 Port Configuration
- ✅ Fixed port in production for configuration
- ✅ Random port in tests to avoid conflicts
- ✅ Use `port: 0` for automatic assignment in tests
- ✅ Allow parallel test execution
- ❌ NO hardcode ports in tests
- ❌ NO create port conflicts

## 4.13 Test Directory Structure
- ✅ Create `test/` directory mirroring project structure
- ✅ Separate by test type: `unit/`, `integration/`, `e2e/`, `performance/`
- ✅ Mirror source structure within each test type folder
- ✅ Use consistent naming: `*.unit.spec.ts`, `*.integration.spec.ts`, `*.e2e.spec.ts`, `*.performance.spec.ts`
- ✅ Keep test files organized by business domain
- ❌ NO mix different test types in same directory
- ❌ NO place tests randomly without structure

## 4.14 Test Five Possible Outcomes
- ✅ Test: response, state change, external API call, queue message, observability
- ✅ Cover all code paths
- ✅ Include edge cases and errors
- ✅ Verify side effects
- ❌ NO test only happy path
- ❌ NO ignore indirect outcomes