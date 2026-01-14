# Testing Standards - Java Spring Boot

**Mandatory for:** All Banking/Retail projects. Testing is part of Definition of Done.

## 1. Testing Pyramid & Coverage

```
                    E2E Tests (5%)
                 Integration Tests (15%)  
              Unit Tests (80%)
```

**Coverage Requirements:**
- **Unit Tests:** 80% line coverage on business logic
- **Integration Tests:** All API endpoints, repository operations
- **E2E Tests:** Critical user journeys, compliance flows

## 2. Architecture-Specific Testing

### Hexagonal Architecture
```java
// Domain - Pure unit tests (no mocks)
@Test void shouldRejectInsufficientFunds() {
    Account account = Account.create(Money.of(100));
    assertThatThrownBy(() -> account.withdraw(Money.of(150)))
        .isInstanceOf(InsufficientFundsException.class);
}

// Application - Mock ports only
@ExtendWith(MockitoExtension.class)
class PaymentServiceTest {
    @Mock PaymentRepository repository;
    @Mock AuditPort auditPort;
}
```

### Clean Architecture
```java
// Entities - No external dependencies
@Test void shouldCalculateDailyLimit() {
    Account account = new Account(AccountId.of("123"), Money.of(1000));
    TransactionResult result = account.withdraw(Money.of(500), todaysTransactions);
    assertThat(result.isSuccess()).isTrue();
}

// Use Cases - Mock gateways
@Test void shouldExecuteWithdrawal() {
    when(accountGateway.findById(any())).thenReturn(Optional.of(account));
    verify(auditGateway).logWithdrawal(any());
}
```

### Layered Architecture
```java
// Controllers - @WebMvcTest
@WebMvcTest(AccountController.class)
class AccountControllerTest {
    @MockBean AccountService accountService;
    
    @Test void shouldReturn200ForValidWithdrawal() throws Exception {
        mockMvc.perform(post("/api/v1/accounts/123/withdraw")
            .content("{\"amount\": 500.00}"))
            .andExpect(status().isOk());
    }
}
```

## 3. Banking/Retail Compliance Testing

### PCI-DSS Requirements
```java
@Test void shouldMaskSensitiveDataInLogs() {
    ListAppender<ILoggingEvent> logWatcher = new ListAppender<>();
    ((Logger) LoggerFactory.getLogger(AccountService.class)).addAppender(logWatcher);
    
    service.withdrawMoney(command);
    
    assertThat(logWatcher.list).noneMatch(log -> 
        log.getMessage().contains("4532-1234-5678-9012")); // Full card number
    assertThat(logWatcher.list).anyMatch(log -> 
        log.getMessage().contains("****-****-****-9012")); // Masked
}

@Test void shouldAuditAllTransactions() {
    service.withdrawMoney(command);
    verify(auditService).logWithdrawal(argThat(audit -> 
        audit.getAccountId().startsWith("****") && // Masked
        audit.getAmount().equals(command.getAmount())));
}
```

### Security Testing
```java
@Test void shouldRejectUnauthorizedAccess() {
    mockMvc.perform(post("/api/v1/accounts/123/withdraw")
        .header("Authorization", "Bearer invalid-token"))
        .andExpected(status().isUnauthorized());
}

@Test void shouldValidateInputSanitization() {
    WithdrawalRequest maliciousRequest = new WithdrawalRequest();
    maliciousRequest.setAmount(new BigDecimal("<script>alert('xss')</script>"));
    
    assertThatThrownBy(() -> service.withdrawMoney(toCommand(maliciousRequest)))
        .isInstanceOf(InvalidRequestException.class);
}
```

## 4. Test Categories & Performance

### Test Annotations
```java
@Tag("unit") @ExtendWith(MockitoExtension.class)
class BusinessLogicTest { /* Fast, isolated, < 100ms */ }

@Tag("integration") @SpringBootTest @Testcontainers
class DatabaseIntegrationTest { /* Real DB, < 5s */ }

@Tag("e2e") @SpringBootTest(webEnvironment = RANDOM_PORT)
class WithdrawalE2ETest { /* Complete journey, < 30s */ }
```

### Performance Testing
```java
@Test void shouldHandleConcurrentWithdrawals() {
    int threadCount = 10;
    CountDownLatch latch = new CountDownLatch(threadCount);
    ExecutorService executor = Executors.newFixedThreadPool(threadCount);
    
    for (int i = 0; i < threadCount; i++) {
        executor.submit(() -> {
            try { service.withdrawMoney(createCommand()); } 
            finally { latch.countDown(); }
        });
    }
    
    assertThat(latch.await(5, SECONDS)).isTrue();
}

@Test void shouldProcessWithdrawalUnder500ms() {
    StopWatch stopWatch = new StopWatch();
    stopWatch.start();
    service.withdrawMoney(command);
    stopWatch.stop();
    assertThat(stopWatch.getTotalTimeMillis()).isLessThan(500);
}
```

## 5. Test Data & Configuration

### Test Builders
```java
public class AccountTestDataBuilder {
    private String id = "ACC-123";
    private BigDecimal balance = new BigDecimal("1000.00");
    
    public static AccountTestDataBuilder anAccount() { return new AccountTestDataBuilder(); }
    public AccountTestDataBuilder withBalance(BigDecimal balance) { this.balance = balance; return this; }
    public AccountEntity build() { return AccountEntity.builder().id(id).balance(balance).build(); }
}

// Usage
@Test void shouldProcessWithdrawal() {
    AccountEntity account = anAccount().withBalance(new BigDecimal("2000.00")).build();
}
```

### Test Configuration
```yaml
# application-test.yml
spring:
  datasource.url: jdbc:h2:mem:testdb
  jpa.hibernate.ddl-auto: create-drop
  profiles.active: test

external:
  payment-gateway.enabled: false
  notification-service.enabled: false
```

## 6. Error Handling & CI/CD

### Exception Testing
```java
@Test void shouldHandleOptimisticLockingFailure() {
    AccountEntity account1 = repository.findById("ACC-123").get();
    AccountEntity account2 = repository.findById("ACC-123").get();
    
    account1.setBalance(new BigDecimal("500.00"));
    repository.save(account1);
    
    account2.setBalance(new BigDecimal("300.00"));
    assertThatThrownBy(() -> repository.save(account2))
        .isInstanceOf(OptimisticLockingFailureException.class);
}

@Test void shouldRetryOnTransientFailures() {
    when(externalService.process(any()))
        .thenThrow(new ConnectException("Connection failed"))
        .thenThrow(new ConnectException("Connection failed"))
        .thenReturn(successResponse);
    
    PaymentResult result = service.processPayment(request);
    assertThat(result.isSuccess()).isTrue();
    verify(externalService, times(3)).process(any());
}
```

### CI/CD Integration
```xml
<!-- Maven JaCoCo Configuration -->
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <configuration>
        <rules>
            <rule>
                <limits>
                    <limit>
                        <counter>LINE</counter>
                        <value>COVEREDRATIO</value>
                        <minimum>0.80</minimum>
                    </limit>
                </limits>
            </rule>
        </rules>
    </configuration>
</plugin>
```

### Test Execution Strategy
```bash
mvn test -Dgroups="unit"                    # < 2 minutes
mvn test -Dgroups="integration"             # < 10 minutes  
mvn test -Dgroups="unit,integration,e2e"    # < 30 minutes
```

## 7. Quality Gates & Review

### Mandatory Checks
- **Unit test coverage ≥ 80%** on business logic
- **All integration tests pass** for API endpoints
- **Security tests pass** for authentication/authorization
- **Performance tests meet SLA** (< 500ms for critical operations)
- **No critical/high vulnerabilities** in dependencies

### Test Review Checklist
- [ ] Tests follow AAA pattern (Arrange, Act, Assert)
- [ ] Test names describe behavior, not implementation
- [ ] No hardcoded values (use constants/builders)
- [ ] Proper exception testing with specific assertions
- [ ] Integration tests use real external dependencies
- [ ] Sensitive data is masked in test logs
- [ ] Tests are deterministic (no random values)
- [ ] Cleanup after tests (database, files, mocks)

**Remember:** Tests are living documentation. Write them for the next developer who needs to understand and maintain the code.