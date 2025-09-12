# Error Handling Guidelines

## 2.1 Async Error Handling
- ✅ For async operations (CompletableFuture, Reactor), handle exceptions and log them.  
- ✅ For Reactor (WebFlux), use operators `onErrorResume`, `onErrorMap`.  

## 2.2 Custom exceptions
- ✅ Define `AppException extends RuntimeException` with fields: `code`, `httpStatus`, `isOperational`.  
- ✅ Do not throw generic `Exception`.  
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
- ✅ Use `@ControllerAdvice` with `@ExceptionHandler` for REST APIs.  
- ✅ Transform exceptions into safe responses (no stacktrace in production).  
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
- ✅ Use SLF4J + Logback/Log4j2 with structured appenders (JSON).
- ✅ Include correlation IDs and contexts (MDC).
- ❌ NO use print in production
- ❌ NO write directly to files

## 2.8 Test Error Flows
- ✅ Test negative scenarios besides positive ones
- ✅ Simulate uncaught exceptions
- ✅ Verify error handler works correctly
- ✅ Test correct error codes
- ❌ NO test only success cases

## 2.9 APM for Error Discovery
- ✅ Implement proactive monitoring
- ✅ Use APM tools (Micrometer, Prometheus, Grafana, New Relic, Datadog, Dynatrace) to detect issues. 
- ✅ Monitor performance and crashes automatically
- ✅ Configure alerts for critical errors
- ❌ NO depend only on manual logs

## 2.10 Fail Fast Validation
- ✅ Validate API input immediately
- ✅ Implement fail-fast pattern
- ✅ Validate at entry-points
- ❌ NO allow invalid data in system
- ❌ NO validate manually without libraries

## 2.13 Event Emitter Error Handling
- ✅ Use exceptionally / handle in CompletableFuture.
- ✅ In Reactor (Mono/Flux), use onErrorResume, onErrorMap.
- ✅ Configure global error handlers for WebFlux.
- ❌ NO ignore stream errors