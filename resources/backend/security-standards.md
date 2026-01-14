# Security Standards - Java Spring Boot

**Mandatory for:** All Banking/Retail projects. Zero tolerance for security violations.

## 1. Security Principles & Compliance

### Core Rules
- **Zero Trust:** Never trust, always verify
- **Defense in Depth:** Multiple security layers
- **Least Privilege:** Minimum required permissions
- **Fail Secure:** System fails to secure state

### Compliance Standards
- **PCI-DSS Level 1:** Payment card data protection
- **SOX/GDPR/CCPA:** Financial/privacy controls
- **OWASP Top 10 2021:** Web application security
- **NIST/ISO 27001:** Cybersecurity frameworks
- **FFIEC/PSD2:** Banking regulations

## 2. Authentication & Authorization

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        return http
            .sessionManagement(session -> session.sessionCreationPolicy(STATELESS))
            .authorizeHttpRequests(authz -> authz
                .requestMatchers("/api/v1/auth/**").permitAll()
                .requestMatchers(GET, "/api/v1/accounts/**").hasRole("CUSTOMER")
                .requestMatchers("/api/v1/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated())
            .oauth2ResourceServer(oauth2 -> oauth2.jwt(withDefaults()))
            .build();
    }
}

@Service
public class AccountService {
    @PreAuthorize("@accountSecurity.canAccess(#accountId, authentication.name)")
    public AccountSummary getAccount(String accountId) { /* implementation */ }
}
```

## 3. OWASP Top 10 2021 Prevention

### A01 - Broken Access Control
```java
// ✅ CORRECT - Resource-level authorization
@PreAuthorize("hasRole('CUSTOMER') and @accountSecurity.isOwner(#accountId, authentication.name)")
public TransferResult transfer(@PathVariable String accountId, @RequestBody TransferRequest request) {
    if (request.getAmount().compareTo(new BigDecimal("10000")) > 0) {
        throw new AccessDeniedException("Transfer amount exceeds daily limit");
    }
    return transferService.transfer(accountId, request);
}
```

### A02 - Cryptographic Failures
```java
// ✅ CORRECT - Strong AES-GCM encryption
@Component
public class CryptographicService {
    public String encryptSensitiveData(String plaintext) {
        Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
        // Use secure random IV, proper key management
        return Base64.getEncoder().encodeToString(encrypted);
    }
}

@Entity
public class PaymentCardEntity {
    @Convert(converter = EncryptedStringConverter.class)
    private String cardNumber; // Encrypted at rest
}
```

### A03 - Injection Prevention
```java
// ✅ CORRECT - Parameterized queries
@Query("SELECT a FROM AccountEntity a WHERE a.userId = :userId AND a.status = :status")
List<AccountEntity> findByUserIdAndStatus(@Param("userId") String userId, @Param("status") AccountStatus status);

// ✅ CORRECT - Input validation
@PostMapping("/{accountId}/withdraw")
public ResponseEntity<WithdrawalResponse> withdraw(
        @PathVariable @Pattern(regexp = "^[A-Z0-9-]{8,20}$") String accountId,
        @Valid @RequestBody WithdrawalRequest request) {
    validateWithdrawalRequest(request);
    return ResponseEntity.ok(accountService.withdraw(accountId, request));
}
```

### A04 - Insecure Design
```java
// ✅ CORRECT - Secure by design with validation layers
@Transactional
public TransferResult processTransfer(TransferRequest request) {
    validateTransferRequest(request);
    validateBusinessRules(request);
    
    FraudScore fraudScore = fraudDetectionService.assessTransfer(request);
    if (fraudScore.isHigh()) return TransferResult.blocked("Fraud risk detected");
    
    if (rateLimitService.isExceeded(request.getFromAccountId())) 
        return TransferResult.blocked("Rate limit exceeded");
    
    return executeSecureTransfer(request);
}
```

### A05-A10 - Additional Protections
- **A05 Security Misconfiguration:** Production-only security headers, error handling
- **A06 Vulnerable Components:** OWASP dependency check, version enforcement
- **A07 Auth Failures:** Account lockout, strong passwords, session management
- **A08 Integrity Failures:** Digital signatures, secure deserialization
- **A09 Logging Failures:** Structured security logging, SIEM integration
- **A10 SSRF:** URL validation, IP allowlisting, secure HTTP clients

## 4. Data Protection & PCI-DSS

### Sensitive Data Handling
```java
@Component
public class SensitiveDataProcessor {
    public PaymentResult processPayment(PaymentRequest request) {
        // ✅ CORRECT - Mask sensitive data in logs
        log.info("Processing payment for account: {}", maskAccountNumber(request.getAccountNumber()));
        
        // Encrypt before storing
        String encryptedCardNumber = encryptionUtil.encrypt(request.getCardNumber());
        return processEncryptedPayment(encryptedCardNumber);
    }
    
    private String maskAccountNumber(String accountNumber) {
        return accountNumber == null || accountNumber.length() <= 4 ? "****" 
            : "****" + accountNumber.substring(accountNumber.length() - 4);
    }
}
```

### GDPR/CCPA Compliance
```java
@Service
public class GdprComplianceService {
    // Right to be Forgotten
    @Transactional
    public void deleteCustomerData(String customerId, String legalBasis) {
        auditService.logDataDeletion(customerId, legalBasis);
        CustomerEntity customer = customerRepository.findById(customerId).orElseThrow();
        customer.setEmail("anonymized@deleted.com");
        customer.setConsentGiven(false);
        customerRepository.save(customer);
    }
}
```

## 5. Security Testing & Monitoring

### Security Testing
```java
@Test @Tag("security")
void shouldPreventSqlInjection() throws Exception {
    mockMvc.perform(get("/api/v1/accounts/search").param("userId", "'; DROP TABLE accounts; --"))
        .andExpect(status().isBadRequest());
    assertThat(accountRepository.count()).isGreaterThan(0);
}

@Test @Tag("security")
void shouldIncludeSecurityHeaders() throws Exception {
    mockMvc.perform(get("/api/v1/accounts/123"))
        .andExpect(header().string("X-Content-Type-Options", "nosniff"))
        .andExpect(header().string("X-Frame-Options", "DENY"));
}
```

### Security Monitoring
```java
@Component
public class SecurityMonitoringService {
    @EventListener
    public void handleSecurityEvent(SecurityEvent event) {
        log.info("Security event: type={}, user={}, ip={}", 
            event.getType(), maskUserId(event.getUserId()), maskIpAddress(event.getClientIp()));
        
        if (event.getSeverity() == SecuritySeverity.CRITICAL) {
            alertingService.sendImmediateAlert(event);
        }
    }
}
```

## 6. AWS Security Integration

### Secrets Management
```java
@Configuration
public class AwsSecretsConfig {
    @Bean
    public DatabaseConfig databaseConfig(SecretsManagerClient secretsClient) {
        String secretValue = getSecret(secretsClient, "banking-app/database");
        return objectMapper.readValue(secretValue, DatabaseConfig.class);
    }
}
```

### Rate Limiting & CORS
```java
@Component
public class RateLimitingFilter implements Filter {
    private static final int MAX_REQUESTS_PER_MINUTE = 60;
    
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) {
        String clientIp = getClientIp((HttpServletRequest) request);
        if (isRateLimitExceeded(clientIp)) {
            ((HttpServletResponse) response).setStatus(HttpStatus.TOO_MANY_REQUESTS.value());
            return;
        }
        chain.doFilter(request, response);
    }
}
```

## 7. Security Checklist & Kiro Integration

### Development Checklist
- [ ] All endpoints require authentication
- [ ] Method-level authorization implemented  
- [ ] Input validation on all user inputs
- [ ] Sensitive data encrypted at rest
- [ ] SQL injection prevention (parameterized queries)
- [ ] HTTPS enforced, security headers configured
- [ ] Rate limiting implemented

### Kiro Security Assistance
```java
// Ask Kiro to analyze security vulnerabilities
// "Review this code for security issues"

// ❌ Vulnerable code Kiro will identify
@GetMapping("/accounts/{id}")
public Account getAccount(@PathVariable String id) {
    return accountRepository.findByQuery("SELECT * FROM accounts WHERE id = " + id);
}

// ✅ Kiro-suggested secure version
@GetMapping("/accounts/{id}")
@PreAuthorize("@accountSecurity.canAccess(#id, authentication.name)")
public Account getAccount(@PathVariable String id) {
    return accountRepository.findById(id).orElseThrow();
}
```

**Remember:** Use Kiro to review code for security issues, generate secure alternatives, and create comprehensive security tests.