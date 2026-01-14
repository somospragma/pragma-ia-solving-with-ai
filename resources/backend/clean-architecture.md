# Clean Architecture - Java Spring Boot

This steering file enforces **Clean Architecture** principles for Java Spring Boot applications in our IT outsourcing environment. Use this for applications requiring strict separation of concerns, high testability, and framework independence.

**When to Apply:** Enterprise applications, Banking systems with complex business rules, applications requiring multiple UI interfaces or data sources.

---

## 1. Core Structure & Package Organization

```
src/main/java/com/company/[domain]/
├── entities/            # Enterprise Business Rules (Domain Entities)
│   ├── model/           # Core Business Objects
│   ├── gateway/         # Abstract Gateways (Repository Interfaces)
│   └── exception/       # Business Rule Exceptions
├── usecases/           # Application Business Rules (Use Cases)
│   ├── interactor/     # Use Case Implementations
│   ├── input/          # Input Boundaries (Interfaces)
│   ├── output/         # Output Boundaries (Interfaces)
│   └── model/          # Request/Response Models
├── adapters/           # Interface Adapters
│   ├── controller/     # Controllers (Web, CLI, etc.)
│   ├── presenter/      # Presenters (Response Formatting)
│   ├── gateway/        # Gateway Implementations
│   └── mapper/         # Data Transformation
└── frameworks/         # Frameworks & Drivers
    ├── web/            # Spring Web Configuration
    ├── persistence/    # JPA Entities & Repositories
    ├── external/       # External Service Clients
    └── config/         # Framework Configuration
```

---

## 2. Dependency Rule & Layer Responsibilities

### The Dependency Rule
**Source code dependencies must point inward only.** Inner circles cannot know about outer circles.

```
Frameworks & Drivers → Interface Adapters → Use Cases → Entities
```

### Layer Definitions

#### 1. Entities (Enterprise Business Rules)
* **Pure business logic** - no framework dependencies
* **Stable** - least likely to change when external factors change
* **Reusable** across different applications

```java
// ✅ CORRECT - Pure Entity
public class Account {
    private final AccountId id;
    private final Money balance;
    private final List<Transaction> transactions;
    
    public Account(AccountId id, Money initialBalance) {
        this.id = Objects.requireNonNull(id);
        this.balance = Objects.requireNonNull(initialBalance);
        this.transactions = new ArrayList<>();
        
        if (initialBalance.isNegative()) {
            throw new InvalidAccountException("Initial balance cannot be negative");
        }
    }
    
    public TransactionResult withdraw(Money amount, TransactionId transactionId) {
        validateWithdrawal(amount);
        
        Transaction transaction = Transaction.withdrawal(transactionId, amount, Instant.now());
        Money newBalance = this.balance.subtract(amount);
        
        return TransactionResult.success(
            new Account(this.id, newBalance, addTransaction(transaction))
        );
    }
    
    private void validateWithdrawal(Money amount) {
        if (amount.isNegative() || amount.isZero()) {
            throw new InvalidTransactionException("Withdrawal amount must be positive");
        }
        if (this.balance.isLessThan(amount)) {
            throw new InsufficientFundsException("Insufficient balance for withdrawal");
        }
    }
}
```

#### 2. Use Cases (Application Business Rules)
* **Application-specific business rules**
* **Orchestrate** the flow of data to and from entities
* **Independent** of UI, database, web frameworks

```java
// Input Boundary (Interface)
public interface WithdrawMoneyUseCase {
    WithdrawMoneyResponse execute(WithdrawMoneyRequest request);
}

// Use Case Implementation
public class WithdrawMoneyInteractor implements WithdrawMoneyUseCase {
    private final AccountGateway accountGateway;
    private final TransactionGateway transactionGateway;
    private final WithdrawMoneyOutputBoundary outputBoundary;
    private final AuditGateway auditGateway;
    
    public WithdrawMoneyInteractor(
            AccountGateway accountGateway,
            TransactionGateway transactionGateway,
            WithdrawMoneyOutputBoundary outputBoundary,
            AuditGateway auditGateway) {
        this.accountGateway = accountGateway;
        this.transactionGateway = transactionGateway;
        this.outputBoundary = outputBoundary;
        this.auditGateway = auditGateway;
    }
    
    @Override
    public WithdrawMoneyResponse execute(WithdrawMoneyRequest request) {
        try {
            // 1. Validate input
            validateRequest(request);
            
            // 2. Get account entity
            Account account = accountGateway.findById(request.getAccountId())
                .orElseThrow(() -> new AccountNotFoundException(request.getAccountId()));
            
            // 3. Execute business logic
            TransactionResult result = account.withdraw(
                Money.of(request.getAmount()), 
                TransactionId.generate()
            );
            
            // 4. Persist changes
            accountGateway.save(result.getUpdatedAccount());
            transactionGateway.save(result.getTransaction());
            
            // 5. Audit for compliance
            auditGateway.logWithdrawal(AuditEntry.builder()
                .accountId(request.getAccountId())
                .amount(request.getAmount())
                .timestamp(Instant.now())
                .userId(request.getUserId())
                .build());
            
            // 6. Format response
            return outputBoundary.presentSuccess(result);
            
        } catch (BusinessException e) {
            return outputBoundary.presentError(e);
        }
    }
    
    private void validateRequest(WithdrawMoneyRequest request) {
        if (request.getAccountId() == null) {
            throw new InvalidRequestException("Account ID is required");
        }
        if (request.getAmount() == null || request.getAmount().compareTo(BigDecimal.ZERO) <= 0) {
            throw new InvalidRequestException("Amount must be positive");
        }
    }
}
```

#### 3. Interface Adapters
* **Convert data** between use cases and external agencies
* **Controllers** convert HTTP requests to use case input
* **Presenters** format use case output for delivery

```java
// Controller (Inbound Adapter)
@RestController
@RequestMapping("/api/v1/accounts")
@Validated
public class AccountController {
    private final WithdrawMoneyUseCase withdrawMoneyUseCase;
    
    @PostMapping("/{accountId}/withdraw")
    public ResponseEntity<WithdrawMoneyResponse> withdrawMoney(
            @PathVariable String accountId,
            @Valid @RequestBody WithdrawMoneyWebRequest webRequest,
            HttpServletRequest httpRequest) {
        
        // Convert web request to use case input
        WithdrawMoneyRequest useCaseRequest = WithdrawMoneyRequest.builder()
            .accountId(AccountId.of(accountId))
            .amount(webRequest.getAmount())
            .userId(extractUserId(httpRequest))
            .build();
        
        // Execute use case
        WithdrawMoneyResponse response = withdrawMoneyUseCase.execute(useCaseRequest);
        
        // Return appropriate HTTP response
        return response.isSuccess() 
            ? ResponseEntity.ok(response)
            : ResponseEntity.badRequest().body(response);
    }
}

// Presenter (Output Boundary Implementation)
@Component
public class WithdrawMoneyPresenter implements WithdrawMoneyOutputBoundary {
    
    @Override
    public WithdrawMoneyResponse presentSuccess(TransactionResult result) {
        return WithdrawMoneyResponse.builder()
            .success(true)
            .transactionId(result.getTransaction().getId().getValue())
            .newBalance(result.getUpdatedAccount().getBalance().getValue())
            .timestamp(result.getTransaction().getTimestamp())
            .build();
    }
    
    @Override
    public WithdrawMoneyResponse presentError(BusinessException exception) {
        return WithdrawMoneyResponse.builder()
            .success(false)
            .errorCode(exception.getErrorCode())
            .errorMessage(exception.getMessage())
            .timestamp(Instant.now())
            .build();
    }
}
```

#### 4. Frameworks & Drivers
* **External agencies** - Web, Database, External Services
* **Most volatile** - likely to change frequently

```java
// JPA Entity (Framework Layer)
@Entity
@Table(name = "accounts")
public class AccountJpaEntity {
    @Id
    private String id;
    
    @Column(name = "balance", precision = 19, scale = 2)
    private BigDecimal balance;
    
    @Column(name = "created_at")
    private Instant createdAt;
    
    @Column(name = "updated_at")
    private Instant updatedAt;
    
    // Constructors, getters, setters
}

// Gateway Implementation (Interface Adapter)
@Repository
public class JpaAccountGateway implements AccountGateway {
    private final SpringDataAccountRepository repository;
    private final AccountMapper mapper;
    
    @Override
    public Optional<Account> findById(AccountId accountId) {
        return repository.findById(accountId.getValue())
            .map(mapper::toDomain);
    }
    
    @Override
    public void save(Account account) {
        AccountJpaEntity entity = mapper.toJpaEntity(account);
        repository.save(entity);
    }
}
```

---

## 3. Security & Compliance Integration

### Banking/Retail Security Requirements
* **Authentication/Authorization** handled in Framework layer
* **Business rules** for security in Entity layer
* **Audit logging** through Use Case layer

```java
// Entity with business security rules
public class Account {
    private static final Money DAILY_WITHDRAWAL_LIMIT = Money.of(new BigDecimal("5000.00"));
    
    public TransactionResult withdraw(Money amount, TransactionId transactionId, 
                                    List<Transaction> todaysTransactions) {
        // Business rule: Daily withdrawal limit
        Money todaysWithdrawals = calculateTodaysWithdrawals(todaysTransactions);
        if (todaysWithdrawals.add(amount).isGreaterThan(DAILY_WITHDRAWAL_LIMIT)) {
            throw new DailyLimitExceededException("Daily withdrawal limit exceeded");
        }
        
        // Continue with withdrawal logic...
    }
}

// Use Case with audit requirements
public class WithdrawMoneyInteractor implements WithdrawMoneyUseCase {
    
    @Override
    public WithdrawMoneyResponse execute(WithdrawMoneyRequest request) {
        // PCI-DSS Compliance: Mask sensitive data in logs
        log.info("Processing withdrawal for account: {}", 
            maskAccountId(request.getAccountId()));
        
        try {
            // Business logic...
            
            // Mandatory audit trail
            auditGateway.logWithdrawal(AuditEntry.builder()
                .accountId(request.getAccountId())
                .amount(request.getAmount())
                .timestamp(Instant.now())
                .userId(request.getUserId())
                .ipAddress(request.getClientIp())
                .userAgent(request.getUserAgent())
                .build());
                
        } catch (Exception e) {
            // Security: Never expose internal details
            log.error("Withdrawal failed for account: {}", 
                maskAccountId(request.getAccountId()), e);
            throw new WithdrawalProcessingException("Transaction could not be processed");
        }
    }
}
```

---

## 4. Testing Strategy

### Entity Testing (Pure Unit Tests)
```java
class AccountTest {
    
    @Test
    void shouldAllowWithdrawalWhenSufficientBalance() {
        // Given
        Account account = new Account(
            AccountId.of("ACC-123"), 
            Money.of(new BigDecimal("1000.00"))
        );
        Money withdrawalAmount = Money.of(new BigDecimal("500.00"));
        
        // When
        TransactionResult result = account.withdraw(
            withdrawalAmount, 
            TransactionId.generate(),
            Collections.emptyList()
        );
        
        // Then
        assertThat(result.isSuccess()).isTrue();
        assertThat(result.getUpdatedAccount().getBalance())
            .isEqualTo(Money.of(new BigDecimal("500.00")));
    }
    
    @Test
    void shouldRejectWithdrawalWhenInsufficientBalance() {
        // Given
        Account account = new Account(
            AccountId.of("ACC-123"), 
            Money.of(new BigDecimal("100.00"))
        );
        Money withdrawalAmount = Money.of(new BigDecimal("500.00"));
        
        // When & Then
        assertThatThrownBy(() -> account.withdraw(
            withdrawalAmount, 
            TransactionId.generate(),
            Collections.emptyList()
        )).isInstanceOf(InsufficientFundsException.class);
    }
}
```

### Use Case Testing (Isolated Business Logic)
```java
@ExtendWith(MockitoExtension.class)
class WithdrawMoneyInteractorTest {
    
    @Mock private AccountGateway accountGateway;
    @Mock private TransactionGateway transactionGateway;
    @Mock private WithdrawMoneyOutputBoundary outputBoundary;
    @Mock private AuditGateway auditGateway;
    
    @InjectMocks
    private WithdrawMoneyInteractor interactor;
    
    @Test
    void shouldExecuteWithdrawalSuccessfully() {
        // Given
        AccountId accountId = AccountId.of("ACC-123");
        Account account = new Account(accountId, Money.of(new BigDecimal("1000.00")));
        WithdrawMoneyRequest request = WithdrawMoneyRequest.builder()
            .accountId(accountId)
            .amount(new BigDecimal("500.00"))
            .userId("USER-123")
            .build();
        
        when(accountGateway.findById(accountId)).thenReturn(Optional.of(account));
        when(outputBoundary.presentSuccess(any())).thenReturn(
            WithdrawMoneyResponse.success("TXN-123", new BigDecimal("500.00"))
        );
        
        // When
        WithdrawMoneyResponse response = interactor.execute(request);
        
        // Then
        assertThat(response.isSuccess()).isTrue();
        verify(accountGateway).save(any(Account.class));
        verify(transactionGateway).save(any(Transaction.class));
        verify(auditGateway).logWithdrawal(any(AuditEntry.class));
    }
}
```

### Integration Testing (Full Stack)
```java
@SpringBootTest
@Testcontainers
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class WithdrawMoneyIntegrationTest {
    
    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:15");
    
    @Autowired
    private TestRestTemplate restTemplate;
    
    @Autowired
    private AccountRepository accountRepository;
    
    @Test
    void shouldProcessWithdrawalEndToEnd() {
        // Given
        AccountJpaEntity account = new AccountJpaEntity("ACC-123", new BigDecimal("1000.00"));
        accountRepository.save(account);
        
        WithdrawMoneyWebRequest request = new WithdrawMoneyWebRequest(new BigDecimal("500.00"));
        
        // When
        ResponseEntity<WithdrawMoneyResponse> response = restTemplate.postForEntity(
            "/api/v1/accounts/ACC-123/withdraw",
            request,
            WithdrawMoneyResponse.class
        );
        
        // Then
        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
        assertThat(response.getBody().isSuccess()).isTrue();
        
        // Verify database state
        AccountJpaEntity updatedAccount = accountRepository.findById("ACC-123").orElseThrow();
        assertThat(updatedAccount.getBalance()).isEqualByComparingTo(new BigDecimal("500.00"));
    }
}
```

---

## 5. AWS Integration & Configuration

### Dependency Injection Configuration
```java
@Configuration
public class UseCaseConfiguration {
    
    @Bean
    public WithdrawMoneyUseCase withdrawMoneyUseCase(
            AccountGateway accountGateway,
            TransactionGateway transactionGateway,
            WithdrawMoneyOutputBoundary outputBoundary,
            AuditGateway auditGateway) {
        return new WithdrawMoneyInteractor(
            accountGateway, 
            transactionGateway, 
            outputBoundary, 
            auditGateway
        );
    }
    
    @Bean
    public AuditGateway auditGateway(
            @Value("${aws.cloudwatch.log-group}") String logGroup,
            CloudWatchLogsClient cloudWatchClient) {
        return new CloudWatchAuditGateway(logGroup, cloudWatchClient);
    }
}
```

### External Service Integration
```java
// Gateway Interface (Use Case Layer)
public interface PaymentGateway {
    PaymentResult processPayment(PaymentRequest request);
}

// Implementation (Framework Layer)
@Component
public class StripePaymentGateway implements PaymentGateway {
    private final StripeClient stripeClient;
    private final CircuitBreaker circuitBreaker;
    
    @Override
    public PaymentResult processPayment(PaymentRequest request) {
        return circuitBreaker.executeSupplier(() -> {
            StripePaymentRequest stripeRequest = mapToStripeRequest(request);
            StripePaymentResponse stripeResponse = stripeClient.charge(stripeRequest);
            return mapToPaymentResult(stripeResponse);
        });
    }
}
```

---

## 6. Performance & Monitoring

### Metrics Integration
```java
// Use Case with metrics
public class WithdrawMoneyInteractor implements WithdrawMoneyUseCase {
    private final MeterRegistry meterRegistry;
    private final Timer withdrawalTimer;
    private final Counter successCounter;
    private final Counter errorCounter;
    
    public WithdrawMoneyInteractor(/* dependencies */, MeterRegistry meterRegistry) {
        // ... other dependencies
        this.meterRegistry = meterRegistry;
        this.withdrawalTimer = Timer.builder("withdrawal.processing.time")
            .description("Time taken to process withdrawal")
            .register(meterRegistry);
        this.successCounter = Counter.builder("withdrawal.success")
            .description("Successful withdrawals")
            .register(meterRegistry);
        this.errorCounter = Counter.builder("withdrawal.error")
            .description("Failed withdrawals")
            .register(meterRegistry);
    }
    
    @Override
    public WithdrawMoneyResponse execute(WithdrawMoneyRequest request) {
        return withdrawalTimer.recordCallable(() -> {
            try {
                WithdrawMoneyResponse response = doExecute(request);
                if (response.isSuccess()) {
                    successCounter.increment();
                } else {
                    errorCounter.increment();
                }
                return response;
            } catch (Exception e) {
                errorCounter.increment();
                throw e;
            }
        });
    }
}
```

---

## 7. Migration Guidelines

When refactoring to Clean Architecture:

1. **Extract Entities:** Move business logic from services to pure domain objects
2. **Define Use Cases:** Create interactors that orchestrate business flows
3. **Create Boundaries:** Define input/output interfaces for use cases
4. **Implement Adapters:** Convert between external formats and internal models
5. **Configure Dependencies:** Use dependency injection to wire layers together

**Key Principle:** Always respect the Dependency Rule - dependencies point inward only.