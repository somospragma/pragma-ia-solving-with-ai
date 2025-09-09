# Performance Guidelines

## 7.1 Don't Block Event Loop
- ✅ Avoid CPU intensive synchronous operations
- ✅ Use Worker Threads for CPU-intensive tasks
- ✅ Break long tasks into small chunks
- ✅ Use setImmediate() to yield control
- ❌ NO long loops without yielding
- ❌ NO complex regex synchronously

## 7.2 Prefer Native JS Methods
- ✅ Use Array.map(), Array.filter(), Array.reduce() natives
- ✅ Leverage performance of native implementations
- ✅ Reduce external dependencies
- ❌ NO use libraries when natives are sufficient