# Hexagonal Architecture (Ports & Adapters) - Java Spring Boot

**Use for:** Complex business domains, Banking/Financial systems, multiple data sources/integrations.

## 1. Package Structure
```
src/main/java/com/company/[domain]/
├── application/port/{in,out}/    # Use Case & Repository Interfaces  
├── application/service/          # Application Services (Orchestration)
├── domain/{model,service}/       # Pure Business Logic (Zero Framework)
└── infrastructure/adapter/{in,out}/ # Controllers, Repositories, External APIs
```

## 2. Core Rules

### Domain Layer
* **NO Spring imports** - Pure business logic only
* **Rich models** - Business logic in entities, not services
* **Value objects** - Money, Email, AccountNumber (immutable)

```java
// ✅ Pure Domain
public class Account {
    public TransactionResult withdraw(Money amount) {
        if (balance.isLessThan(amount)) throw new InsufficientFundsException();
        return TransactionResult.success(balance.subtract(amount));
    }
}

// ❌ Framework contamination  
@Entity public class Account { @Id private String id; }
```

### Application Layer
* **Ports define contracts** - Inbound (use cases) + Outbound (repositories)
* **Services orchestrate** - NO business rules, only coordination

```java
public interface ProcessPaymentUseCase { PaymentResult process(Command cmd); }
public interface PaymentRepository { void save(Payment p); }

@Service
public class PaymentService implements ProcessPaymentUseCase {
    public PaymentResult process(Command cmd) {
        Payment payment = Payment.create(cmd.getAmount());
        repository.save(payment);
        return PaymentResult.success();
    }
}
```

### Infrastructure Layer
* **Adapters implement ports** - Controllers (inbound), Repositories (outbound)
* **Framework-specific code only**

---

## 3. Security & Compliance Integration

### Banking/Retail Specific Requirements
* **PCI-DSS Compliance:** Sensitive data (card numbers, PINs) must only exist in the domain layer with proper encryption.
* **Audit Trail:** All use cases must implement audit logging through outbound ports.

```java
// Audit Port for compliance
public interface AuditPort {
    void logTransaction(TransactionAudit audit);
}

// Domain service with audit integration
@Service
public class PaymentApplicationService implements ProcessPaymentUseCase {
    private final AuditPort auditPort;
    
    @Override
    public PaymentResult processPayment(ProcessPaymentCommand command) {
        // Business logic
        Payment payment = Payment.create(command.getAmount(), command.getAccountId());
        
        // Compliance audit
        auditPort.logTransaction(TransactionAudit.builder()
            .transactionId(payment.getId())
            .amount(payment.getAmount().getMaskedValue()) // Masked for PCI
            .timestamp(Instant.now())
            .build());
            
        return PaymentResult.success(payment.getId());
    }
}
```

---

## 4. Testing Strategy

### Domain Testing (Pure Unit Tests)
```java
class AccountTest {
    @Test
    void shouldThrowExceptionWhenWithdrawingMoreThanBalance() {
        // Given
        Account account = Account.create(AccountId.of("123"), Money.of(100));
        
        // When & Then
        assertThatThrownBy(() -> account.withdraw(Money.of(150)))
            .isInstanceOf(InsufficientFundsException.class);
    }
}
```

### Application Testing (Integration with Mocked Ports)
```java
@ExtendWith(MockitoExtension.class)
class PaymentApplicationServiceTest {
    @Mock private PaymentRepository paymentRepository;
    @Mock private NotificationPort notificationPort;
    
    @InjectMocks
    private PaymentApplicationService service;
    
    @Test
    void shouldProcessPaymentSuccessfully() {
        // Test orchestration logic
    }
}
```

### Infrastructure Testing (Testcontainers)
```java
@SpringBootTest
@Testcontainers
class JpaPaymentRepositoryTest {
    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:15");
    
    @Test
    void shouldSaveAndRetrievePayment() {
        // Test actual database integration
    }
}
```

---

## 5. AWS Integration Patterns

### Configuration Management
```java
@Configuration
public class PaymentConfiguration {
    
    @Bean
    public PaymentRepository paymentRepository(
            SpringDataPaymentRepository springRepository) {
        return new JpaPaymentRepository(springRepository);
    }
    
    @Bean
    public NotificationPort notificationPort(
            @Value("${aws.sns.topic.arn}") String topicArn,
            SnsClient snsClient) {
        return new SnsNotificationAdapter(topicArn, snsClient);
    }
}
```

### Secrets Management
```java
// Outbound port for secrets
public interface SecretsPort {
    String getSecret(String secretName);
}

// AWS Secrets Manager adapter
@Component
public class AwsSecretsAdapter implements SecretsPort {
    private final SecretsManagerClient secretsClient;
    
    @Override
    public String getSecret(String secretName) {
        GetSecretValueRequest request = GetSecretValueRequest.builder()
            .secretId(secretName)
            .build();
        return secretsClient.getSecretValue(request).secretString();
    }
}
```

---

## 6. Performance & Monitoring

### Resilience Patterns
```java
@Component
public class ResilientPaymentGatewayAdapter implements PaymentGatewayPort {
    private final CircuitBreaker circuitBreaker;
    private final Retry retry;
    
    @Override
    public PaymentGatewayResponse processPayment(PaymentGatewayRequest request) {
        return circuitBreaker.executeSupplier(
            retry.decorate(() -> paymentGatewayClient.process(request))
        );
    }
}
```

### Observability
```java
// Metrics port for monitoring
public interface MetricsPort {
    void incrementCounter(String name, String... tags);
    void recordTimer(String name, Duration duration, String... tags);
}

// Application service with metrics
@Service
public class PaymentApplicationService implements ProcessPaymentUseCase {
    private final MetricsPort metricsPort;
    
    @Override
    public PaymentResult processPayment(ProcessPaymentCommand command) {
        Timer.Sample sample = Timer.start();
        try {
            // Business logic
            PaymentResult result = doProcessPayment(command);
            metricsPort.incrementCounter("payment.processed", "status", "success");
            return result;
        } catch (Exception e) {
            metricsPort.incrementCounter("payment.processed", "status", "error");
            throw e;
        } finally {
            sample.stop(Timer.builder("payment.processing.time").register(meterRegistry));
        }
    }
}
```

---

## 7. Migration & Refactoring Guidelines

When refactoring existing code to Hexagonal Architecture:

1. **Start with Domain:** Extract business logic from controllers/services into pure domain objects.
2. **Define Ports:** Create interfaces for external dependencies.
3. **Implement Adapters:** Move Spring-specific code to infrastructure layer.
4. **Test Isolation:** Ensure domain tests have zero external dependencies.

**Remember:** Hexagonal Architecture is about **dependency inversion** and **testability**. The domain should never depend on infrastructure concerns.