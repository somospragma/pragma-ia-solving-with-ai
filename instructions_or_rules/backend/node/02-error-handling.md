# Error Handling Guidelines

## 2.1 Async Error Handling
- ✅ Use async/await or promises instead of callbacks
- ✅ Implement try-catch for error handling
- ✅ Use .catch() in promise chains
- ❌ NO use Node.js callback style `function(err, response)`
- ❌ NO create "pyramid of doom" with nested callbacks

## 2.2 Extend Built-in Error Object
- ✅ Create AppError class that extends native Error
- ✅ Add useful properties (name, httpCode, isOperational)
- ✅ Use ESLint rule `no-throw-literal`
- ✅ Maintain stack trace information
- ❌ NO throw strings or custom types
- ❌ NO create multiple error classes for each case

## 2.3 Distinguish Operational vs Catastrophic Errors
- ✅ Mark errors as operational with `isOperational: true`
- ✅ Operational errors: handle and continue
- ✅ Catastrophic errors: restart application gracefully
- ✅ Use centralized factory to create errors
- ❌ NO treat all errors equally
- ❌ NO keep application alive with unknown errors

## 2.4 Centralized Error Handling
- ✅ Create centralized object for error handling
- ✅ Include logging, crash decision, and metrics
- ✅ Call from all entry-points
- ❌ NO duplicate error handling logic
- ❌ NO handle errors in multiple places

## 2.5 Document API Errors
- ✅ Document all possible API errors
- ✅ Use OpenAPI/Swagger for REST APIs
- ✅ Use schemas and comments for GraphQL
- ✅ Include error codes and descriptions
- ❌ NO leave errors undocumented

## 2.6 Graceful Process Exit
- ✅ Make error observable before exiting
- ✅ Close active connections
- ✅ Exit process on unknown errors
- ✅ Trust runtime (Docker, serverless) to restart
- ❌ NO continue with uncertain state
- ❌ NO ignore unfamiliar errors

## 2.7 Mature Logger Usage
- ✅ Use Pino or Winston instead of console.log
- ✅ Implement log levels, pretty print, coloring
- ✅ Write logs to stdout
- ✅ Allow custom properties in logs
- ❌ NO use console.log in production
- ❌ NO write directly to files

## 2.8 Test Error Flows
- ✅ Test negative scenarios besides positive ones
- ✅ Simulate uncaught exceptions
- ✅ Verify error handler works correctly
- ✅ Test correct error codes
- ❌ NO test only success cases

## 2.9 APM for Error Discovery
- ✅ Implement proactive monitoring
- ✅ Use APM tools to detect issues
- ✅ Monitor performance and crashes automatically
- ✅ Configure alerts for critical errors
- ❌ NO depend only on manual logs

## 2.10 Catch Unhandled Promise Rejections
- ✅ Register listener for `process.unhandledRejection`
- ✅ Handle uncaught rejected promises
- ✅ Implement appropriate logging
- ❌ NO ignore unhandled promise rejections
- ❌ NO depend only on `process.uncaughtException`

## 2.11 Fail Fast Validation
- ✅ Validate API input immediately
- ✅ Use libraries like ajv, zod, typebox
- ✅ Implement fail-fast pattern
- ✅ Validate at entry-points
- ❌ NO allow invalid data in system
- ❌ NO validate manually without libraries

## 2.12 Always Await Before Return
- ✅ Use `return await` when returning promise
- ✅ Declare function as `async` if returning promise
- ✅ Await explicitly before return
- ❌ NO return promises without await
- ❌ NO lose stack trace information

## 2.13 Event Emitter Error Handling
- ✅ Subscribe to 'error' event of EventEmitters
- ✅ Handle stream errors appropriately
- ✅ Use `{captureRejections: true}` for async handlers
- ✅ Handle EventTargets with process.on('error')
- ❌ NO use only try-catch with EventEmitters
- ❌ NO ignore stream errors