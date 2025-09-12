# Docker Guidelines

## 8.1 Multi-stage Builds
- ✅ Separate build stage from runtime stage
- ✅ Copy only necessary artifacts to final stage
- ✅ Use different base images for build and runtime
- ❌ NO include build tools in final image

## 8.2 Bootstrap with Node Command
- ✅ Use `CMD ["node", "app.js"]` directly
- ✅ Avoid npm overhead
- ✅ Better system signal handling
- ❌ NO use `npm start` as main command

## 8.3 Let Docker Handle Replication
- ✅ Use Docker/Kubernetes for restart policies
- ✅ Implement health checks in container
- ✅ Trust orchestrator for high availability
- ❌ NO use PM2 inside containers

## 8.4 Use .dockerignore
- ✅ Create comprehensive .dockerignore
- ✅ Exclude node_modules, .git, .env
- ✅ Exclude development and testing files
- ❌ NO copy unnecessary files to container

## 8.5 Clean Dependencies Before Production
- ✅ Use `npm ci --only=production`
- ✅ Remove devDependencies in final image
- ✅ Minimize image size
- ❌ NO include development dependencies

## 8.6 Graceful Shutdown
- ✅ Handle SIGTERM and SIGINT signals
- ✅ Close connections gracefully
- ✅ Implement timeout for forced shutdown
- ❌ NO terminate abruptly

## 8.7 Set Memory Limits
- ✅ Configure --memory in Docker
- ✅ Use --max-old-space-size in Node.js
- ✅ Coordinate limits between Docker and V8
- ❌ NO leave limits unconfigured

## 8.8 Efficient Caching
- ✅ Copy package.json before source code
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

## 8.13 Clean NODE_MODULE Cache
- ✅ Use `npm ci` which cleans cache automatically
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