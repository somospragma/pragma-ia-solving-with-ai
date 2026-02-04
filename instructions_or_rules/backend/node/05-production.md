# Production Guidelines

## 5.1 Monitoring
- ✅ Monitor CPU, server RAM, Node process RAM
- ✅ Configure alerts for critical metrics
- ✅ Measure errors per minute and response time
- ✅ Use tools like Datadog, NewRelic, or ELK stack
- ❌ NO depend only on manual logs

## 5.2 Smart Logging
- ✅ Use structured logging with JSON
- ✅ Include correlation IDs in logs
- ✅ Implement different log levels
- ✅ Add relevant context to each log
- ❌ NO excessive or insufficient logging

## 5.3 Delegate to Reverse Proxy
- ✅ Use nginx/Apache for gzip, SSL, static files
- ✅ Implement rate limiting in proxy
- ✅ Handle load balancing externally
- ❌ NO implement these functions in Node.js

## 5.4 Lock Dependencies
- ✅ Use package-lock.json or yarn.lock
- ✅ Commit lock files
- ✅ Use exact versions in production
- ❌ NO allow uncontrolled automatic updates

## 5.5 Guard Process Uptime
- ✅ Use PM2, Forever, or systemd for automatic restart
- ✅ Configure health checks
- ✅ Implement graceful shutdown
- ❌ NO depend on single process without supervision

## 5.6 Utilize All CPU Cores
- ✅ Use cluster module or PM2 for multiple processes
- ✅ Leverage all available cores
- ✅ Implement load balancing between processes
- ❌ NO use only one process on multi-core server

## 5.7 Create Maintenance Endpoint
- ✅ Implement `/health` endpoint
- ✅ Verify dependencies status (DB, external services)
- ✅ Return useful debugging information
- ❌ NO expose sensitive information

## 5.8 APM Products
- ✅ Implement Application Performance Monitoring
- ✅ Detect memory leaks and performance issues
- ✅ Monitor business transactions
- ❌ NO wait for problems to manifest

## 5.9 Production-Ready Code
- ✅ Remove console.log and debugging code
- ✅ Configure appropriate environment variables
- ✅ Optimize for production performance
- ❌ NO deploy development code

## 5.10 Memory Usage Management
- ✅ Monitor heap usage and memory leaks
- ✅ Configure appropriate memory limits
- ✅ Use profiling tools when necessary
- ❌ NO ignore memory growth

## 5.11 Frontend Assets Out of Node
- ✅ Serve static files from CDN or reverse proxy
- ✅ Use Node.js only for application logic
- ✅ Optimize asset delivery
- ❌ NO use Node.js as static file server

## 5.12 Strive for Stateless
- ✅ Store state in DB or external cache
- ✅ Make application horizontally scalable
- ✅ Avoid local state dependencies
- ❌ NO store critical state in process memory

## 5.13 Vulnerability Detection Tools
- ✅ Use npm audit, Snyk, or similar
- ✅ Integrate in CI/CD pipeline
- ✅ Update vulnerable dependencies regularly
- ❌ NO ignore security alerts

## 5.14 Transaction ID Logging
- ✅ Generate unique ID per request
- ✅ Propagate ID through entire transaction
- ✅ Include in all related logs
- ❌ NO log without transaction context

## 5.15 Set NODE_ENV=production
- ✅ Configure NODE_ENV=production in production
- ✅ Enable performance optimizations
- ✅ Disable development features
- ❌ NO use development mode in production

## 5.16 Automated Deployments
- ✅ Implement blue-green or rolling deployments
- ✅ Automate deployment process
- ✅ Include automatic rollback on failures
- ❌ NO manual deployments in production

## 5.17 Use LTS Node.js
- ✅ Use LTS versions for stability
- ✅ Plan upgrades with LTS calendar
- ✅ Avoid experimental versions in production
- ❌ NO use non-LTS versions in production

## 5.18 Log to stdout
- ✅ Write logs to stdout/stderr
- ✅ Let infrastructure handle log routing
- ✅ Use external tools for log aggregation
- ❌ NO write directly to files from app

## 5.19 Install with npm ci
- ✅ Use `npm ci` in production and CI
- ✅ Install exactly what's specified in lock file
- ✅ Faster and more deterministic than `npm install`
- ❌ NO use `npm install` in production