# Security Guidelines

## 6.1 Static Code Analysis for Security
- ✅ Use tools like SpotBugs (with FindSecBugs plugin), PMD, SonarQube security rules.
- ✅ Configure security rules in ESLint
- ✅ Detect insecure patterns automatically
- ❌ NO ignore security warnings

## 6.2 Rate Limiting
- ✅ Implement rate limiting
- ✅ Configure appropriate limits per IP/user
- ❌ NO allow unlimited requests

## 6.3 Secret Management
- ✅ Use environment variables for secrets
- ✅ Never commit credentials
- ✅ Use tools like Vault for secret management
- ❌ NO hardcode passwords or API keys

## 6.4 Query Injection Prevention
- ✅ Use JPA/Hibernate or prepared statements (JdbcTemplate, PreparedStatement).
- ✅ Validate and sanitize user input
- ✅ Use prepared statements
- ❌ NO build queries with string concatenation

## 6.5 Generic Security Practices
- ✅ Implement robust authentication and authorization
- ✅ Use HTTPS for all communications
- ✅ Validate all user input
- ✅ Implement security logging
- ❌ NO trust client input

## 6.6 Secure HTTP Headers
- ✅ Use Spring Security to configure CSP, HSTS, X-Frame-Options.
- ✅ Remove headers revealing server information
- ❌ NO use insecure default headers

## 6.7 Dependency Vulnerability Scanning
- ✅ Automate scans with OWASP Dependency-Check, Snyk, Sonatype OSS Index.
- ✅ Fix vulnerabilities quickly.
- ❌ NO ignore vulnerability alerts

## 6.8 Password Protection
- ✅ Use bcrypt, scrypt, or argon2 for hashing
- ✅ Never store passwords in plain text
- ✅ Use appropriate salt and cost factor
- ❌ NO use MD5, SHA1, or weak algorithms

## 6.9 Output Escaping
- ✅ Sanitize all output going to browser
- ✅ Use libraries like OWASP Java Encoder.
- ✅ Implement CSP to prevent XSS
- ❌ NO trust user input without sanitization

## 6.10 JSON Schema Validation
- ✅ Use JSON Schema for validation
- ✅ Validate structure, types, and ranges
- ✅ Reject invalid payloads immediately
- ❌ NO process JSON without validation

## 6.11 JWT Blocklisting
- ✅ Implement blacklist for revoked tokens
- ✅ Use Redis or similar for fast storage
- ✅ Verify blacklist on each request
- ❌ NO depend only on token expiration

## 6.12 Brute Force Prevention
- ✅ Implement rate limiting on login
- ✅ Use CAPTCHA after failed attempts
- ✅ Implement temporary account lockout
- ❌ NO allow unlimited login attempts

## 6.13 Non-root User
- ✅ Create dedicated user for application
- ✅ Use USER in Dockerfile
- ✅ Configure minimal necessary permissions
- ❌ NO run as root in production

## 6.14 Payload Size Limits
- ✅ Configure request size limits
- ✅ Configure spring.servlet.multipart.max-request-size and server.tomcat.max-swallow-size.
- ✅ Implement in reverse proxy too
- ❌ NO allow unlimited payloads

## 6.15 Avoid eval Statements
- ✅ Never use reflection with untrusted input.
- ✅ Use safe parsers (Jackson, Gson) instead of eval.
- ❌ NO execute untrusted dynamic code

## 6.16 Prevent Evil RegEx
- ✅ Validate complex regular expressions
- ✅ Use timeouts for regex execution
- ✅ Avoid patterns susceptible to ReDoS
- ❌ NO use unvalidated regex from user input

## 6.17 Safe Module Loading
- ✅ Use explicit classpaths and classloaders.
- ✅ Validate dynamic paths against whitelist
- ✅ Avoid require() with user input
- ❌ NO allow arbitrary module loading

## 6.18 Sandbox Unsafe Code
- ✅ Use JVM SecurityManager alternatives or container sandboxing (Docker/K8s).
- ✅ Isolate untrusted code execution
- ✅ Limit available resources in sandbox
- ❌ NO execute untrusted code directly

## 6.19 Child Process Safety
- ✅ Validate child_process arguments
- ✅ Avoid shell injection
- ✅ Prefer ProcessBuilder over Runtime.exec.
- ❌ NO pass user input directly to shell

## 6.20 Hide Error Details
- ✅ Return generic messages to client
- ✅ Log complete details internally
- ✅ Don't reveal stack traces in production
- ❌ NO expose sensitive information in errors

## 6.21 Configure 2FA
- ✅ Enable two-factor authentication(Spring Security + TOTP/OTP).
- ✅ Use limited access tokens
- ❌ NO use only password for critical accounts

## 6.22 Session Middleware Settings
- ✅ Configure secure: true for HTTPS
- ✅ Use httpOnly: true for cookies
- ✅ Configure sameSite appropriately
- ❌ NO use insecure default settings

## 6.23 Avoid DOS Attacks
- ✅ Configure memory and CPU limits
- ✅ Implement circuit breakers
- ✅ Monitor resources and fail gracefully
- ❌ NO allow unlimited resource consumption

## 6.24 Prevent Unsafe Redirects
- ✅ Validate redirect URLs against whitelist
- ✅ Use relative URLs when possible
- ✅ Avoid redirects based on user input
- ❌ NO allow arbitrary redirects

## 6.25 Avoid Publishing Secrets
- ✅ Exclude sensitive files via .dockerignore, .gitignore, or build config.
- ✅ Review content before publishing
- ✅ Verify packaged JARs/WARs before publishing.
- ❌ NO include .env, keys, or credentials

## 6.26 Inspect Outdated Packages
- ✅ Use mvn versions:display-dependency-updates or gradle dependencyUpdates.
- ✅ Keep dependencies updated
- ✅ Evaluate security risks in old versions
- ❌ NO use very outdated dependencies

## 6.27 Explicit Java Module Usage
- ✅ Use JPMS (module-info.java) to declare dependencies.
- ✅ Make explicit what modules are part of JDK vs external libs.
- ✅ Prevent shadowing of native modules
- ❌ NO use ambiguous imports for native modules