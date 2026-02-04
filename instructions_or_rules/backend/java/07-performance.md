# Performance Guidelines

## 7.1 Don't Block Event Loop
- ✅ Avoid CPU intensive synchronous operations
- ✅ Use Worker Threads for CPU-intensive tasks
- ✅ Break long tasks into small chunks
- ✅ Use asynchronous processing with CompletableFuture, Project Reactor (Mono/Flux), or Kotlin coroutines.
- ❌ NO long loops without yielding
- ❌ NO complex regex synchronously

## 7.2 Prefer Native Java APIs
- ✅ Use Java Streams API (map, filter, reduce, collect) for collections.
- ✅ Prefer built-in concurrency utilities (Executors, CompletableFuture, java.util.concurrent).
- ✅ Reduce external dependencies
- ❌ NO use libraries when natives are sufficient