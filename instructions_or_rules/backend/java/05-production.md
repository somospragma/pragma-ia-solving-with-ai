# Production Guidelines

## 5.1 Monitoring
- ✅ Monitor JVM metrics: heap, GC pauses, threads, CPU, process RAM.
- ✅ Configure alerts for critical metrics
- ✅ Measure errors per minute and response time
- ✅ Use tools like Prometheus + Grafana, Datadog, New Relic, APM.
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
- ✅ Use Maven/Gradle lock files (mvn dependency:go-offline, Gradle dependency-lock).
- ✅ Commit lock files
- ✅ Use exact versions in production
- ❌ NO allow uncontrolled automatic updates

## 5.5 Guard Process Uptime
- ✅ Run apps under systemd, Kubernetes, or Docker for supervision.
- ✅ Configure health checks
- ✅ Implement graceful shutdown
- ❌ NO depend on single process without supervision

## 5.6 Utilize All CPU Cores
- ✅ Run multiple JVM instances behind a load balancer.
- ✅ Leverage all available cores
- ✅ Implement load balancing between processes
- ❌ NO use only one process on multi-core server

## 5.7 Create Maintenance Endpoint
- ✅ Expose /actuator/health with Spring Boot Actuator.
- ✅ Verify dependencies status (DB, external services)
- ✅ Return useful debugging information
- ❌ NO expose sensitive information

## 5.8 APM Products
- ✅ Implement Application Performance Monitoring
- ✅ Detect memory leaks and performance issues
- ✅ Monitor business transactions
- ❌ NO wait for problems to manifest

## 5.9 Production-Ready Code
- ✅ Remove System.out.println and debugging leftovers.
- ✅ Configure environment variables and application-prod.yml.
- ✅ Optimize for production performance
- ❌ NO deploy development code

## 5.10 Memory Usage Management
- ✅ Monitor heap usage and memory leaks
- ✅ Configure appropriate memory limits
- ✅ Use profiling tools when necessary
- ❌ NO ignore memory growth

## 5.11 Frontend Assets Out of JVM
- ✅ Serve static files from CDN or reverse proxy
- ✅ Use Spring Boot only for APIs and business logic.
- ✅ Optimize asset delivery
- ❌ NO use Node.js as static file server

## 5.12 Strive for Stateless
- ✅ Store state in DB or external cache
- ✅ Make application horizontally scalable
- ✅ Avoid local state dependencies
- ❌ NO store critical state in process memory

## 5.13 Vulnerability Detection Tools
- ✅ Use OWASP Dependency-Check, Snyk, or Maven/Gradle security scanners.
- ✅ Integrate in CI/CD pipeline
- ✅ Update vulnerable dependencies regularly
- ❌ NO ignore security alerts

## 5.14 Transaction ID Logging
- ✅ Generate unique ID per request
- ✅ Propagate ID through entire transaction
- ✅ Include in all related logs
- ❌ NO log without transaction context

## 5.15 Set Production Profile
- ✅ Run with -Dspring.profiles.active=prod.
- ✅ Enable performance optimizations
- ✅ Disable development features
- ❌ DO NOT run with dev profile in production.

## 5.16 Automated Deployments
- ✅ Use CI/CD pipelines with blue-green or rolling deployments.
- ✅ Automate deployment process
- ✅ Include automatic rollback on failures
- ❌ NO manual deployments in production

## 5.17 Use LTS Java
- ✅ Deploy only with LTS JDK (17, 21).
- ✅ Plan upgrades with LTS calendar
- ✅ Avoid experimental versions in production
- ❌ NO use non-LTS versions in production

## 5.18 Log to stdout
- ✅ Write logs to stdout/stderr
- ✅ Let infrastructure handle log routing
- ✅ Use external tools for log aggregation
- ❌ NO write directly to files from app

## 5.19 Deterministic Dependency Installation
- ✅ Use mvn verify or gradle build --offline for deterministic builds.
- ✅ Ensure build reproducibility with lock files.
- ✅ Cache dependencies in CI/CD.
- ❌ DO NOT rely on dynamic + version ranges.