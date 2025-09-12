# Docker Guidelines

## 8.1 Multi-stage Builds
- ✅ Separate build stage from runtime stage
- ✅ Copy only necessary artifacts to final stage
- ✅ Use different base images for build and runtime
- ❌ NO include build tools in final image

## 8.2 Bootstrap with Node Command
- ✅ Use CMD ["java", "-jar", "app.jar"] directly.
- ✅ Pass JVM flags via JAVA_OPTS.
- ✅ Better system signal handling
- ❌ DO NOT wrap in shell scripts unnecessarily.

## 8.3 Let Docker Handle Replication
- ✅ Use Docker/Kubernetes for restart policies
- ✅ Implement health checks in container (/actuator/health).
- ✅ Trust orchestrator for high availability
- ❌ DO NOT use external process managers (like PM2).

## 8.4 Use .dockerignore
- ✅ Create comprehensive .dockerignore
- ✅ Exclude test dependencies from final JAR/WAR.
- ✅ Minimize final image size.
- ❌ NO copy unnecessary files to container

## 8.5 Clean Dependencies Before Production
- ✅ Use reproducible builds (mvn verify, gradle build --no-daemon).
- ✅ Exclude test dependencies from final JAR/WAR.
- ✅ Minimize image size
- ❌ NO include development dependencies

## 8.6 Graceful Shutdown
- ✅ Handle SIGTERM and SIGINT signals
- ✅ Close connections gracefully
- ✅ Implement timeout for forced shutdown
- ❌ NO terminate abruptly

## 8.7 Set Memory Limits
- ✅ Configure --memory in Docker
- ✅ Use JAVA_OPTS with -Xmx/-Xms aligned to container memory.
- ✅ Coordinate limits between Docker and V8
- ❌ NO leave limits unconfigured

## 8.8 Efficient Caching
- ✅ Copy pom.xml / build.gradle first for dependency caching.
- ✅ Leverage Docker layer caching
- ✅ Order commands by change frequency
- ❌ NO invalidate cache unnecessarily

## 8.9 Explicit Image References
- ✅ Specify exact versions of base images
- ✅ Use immutable tags when possible
- ✅ Document versions used
- ❌ NO use :latest in production

## 8.10 Smaller Base Images
- ✅ Use Alpine Linux when appropriate
- ✅ Consider distroless images
- ✅ Balance size vs functionality
- ❌ NO use unnecessarily large images

## 8.11 Clean Build-time Secrets
- ✅ Use multi-stage builds for build secrets
- ✅ Use Docker secrets or BuildKit secrets
- ✅ Never pass secrets as ARG
- ❌ NO leave secrets in intermediate layers

## 8.12 Scan Images for Vulnerabilities
- ✅ Use tools like Clair, Trivy, Snyk
- ✅ Scan both OS and application dependencies
- ✅ Integrate in CI/CD pipeline
- ❌ NO deploy unscanned images

## 8.13 Clean Build Caches
- ✅ Clean Maven/Gradle cache in final stage if copied.
- ✅ Remove unnecessary cache in multi-stage builds
- ✅ Minimize final image size
- ❌ NO leave npm cache in final image

## 8.14 Generic Docker Practices
- ✅ Use non-root user
- ✅ Minimize number of layers
- ✅ Use COPY instead of ADD when appropriate
- ✅ Configure health checks
- ❌ NO run as root
- ❌ NO create unnecessary layers

## 8.15 Lint Dockerfile
- ✅ Use hadolint for Dockerfile linting
- ✅ Follow Docker best practices
- ✅ Integrate linting in CI/CD
- ❌ NO ignore linting warnings