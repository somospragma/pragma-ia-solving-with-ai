# Standard Layered Architecture - Java Spring Boot

**Use for:** Traditional enterprise applications, CRUD operations, rapid development with established patterns.

## 1. Package Structure
```
src/main/java/com/company/[domain]/
├── controller/{rest,dto,mapper}/     # Presentation Layer
├── service/{impl,validator}/         # Business Logic Layer  
├── repository/{entity,specification}/ # Data Access Layer
├── config/{security,database}/       # Configuration Layer
└── exception/{handler,custom}/       # Cross-cutting Concerns
```

## 2. Layer Rules

### Controllers (Presentation)
* **HTTP handling** - requests/responses, validation, auth
* **DTO mapping** - convert between web and service models

```java
@RestController
@RequestMapping("/api/v1/accounts")
@PreAuthorize("hasRole('CUSTOMER')")
public class AccountController {
    
    @PostMapping("/{accountId}/withdraw")
    public ResponseEntity<WithdrawalResponseDto> withdrawMoney(
            @PathVariable String accountId,
            @Valid @RequestBody WithdrawalRequestDto request) {
        
        WithdrawalCommand command = mapper.toCommand(request, accountId);
        WithdrawalResult result = accountService.withdrawMoney(command);
        return ResponseEntity.ok(mapper.toResponseDto(result));
    }
}
```

### Services (Business Logic)
* **Business rules** - core logic, validation, orchestration
* **Transaction management** - @Transactional boundaries

```java
@Service
@Transactional
public class AccountServiceImpl implements AccountService {
    
    @Override
    public WithdrawalResult withdrawMoney(WithdrawalCommand command) {
        AccountEntity account = accountRepository.findByIdWithLock(command.getAccountId())
            .orElseThrow(() -> new AccountNotFoundException());
        
        // Business validation
        validateWithdrawalRules(account, command);
        
        // Update balance
        account.setBalance(account.getBalance().subtract(command.getAmount()));
        accountRepository.save(account);
        
        // Audit for compliance
        auditService.logWithdrawal(command);
        
        return WithdrawalResult.success(account.getBalance());
    }
}
```

### Repositories (Data Access)
* **Data persistence** - CRUD operations, queries
* **JPA entities** - database mapping

```java
@Entity
@Table(name = "accounts")
public class AccountEntity {
    @Id private String id;
    @Column(precision = 19, scale = 2) private BigDecimal balance;
    @Enumerated(EnumType.STRING) private AccountStatus status;
    @Version private Long version;
}

@Repository
public interface AccountRepository extends JpaRepository<AccountEntity, String> {
    @Query("SELECT a FROM AccountEntity a WHERE a.id = :id")
    @Lock(LockModeType.PESSIMISTIC_WRITE)
    Optional<AccountEntity> findByIdWithLock(@Param("id") String id);
}
```

## 3. Banking/Retail Compliance

**PCI-DSS:** Mask sensitive data in logs, encrypt at rest
**Audit:** Log all transactions with masked account IDs

```java
@Component
public class ComplianceAuditService {
    @Async
    public void logTransactionEvent(TransactionAuditEvent event) {
        AuditEventEntity audit = AuditEventEntity.builder()
            .accountId(maskAccountId(event.getAccountId()))
            .amount(event.getAmount())
            .timestamp(Instant.now())
            .build();
        auditRepository.save(audit);
        sendToCloudWatch(audit);
    }
}
```

## 4. Testing Strategy

**Controller:** @WebMvcTest with mocked services
**Service:** @ExtendWith(MockitoExtension.class) with mocked repositories  
**Repository:** @DataJpaTest with Testcontainers
**Integration:** @SpringBootTest end-to-end

## 5. AWS Integration

**Caching:** Redis for frequently accessed data
**Monitoring:** Micrometer metrics to CloudWatch
**Secrets:** AWS Secrets Manager integration

## 6. Migration Steps

1. Extract business logic from controllers → service layer
2. Move business rules → dedicated service classes  
3. Replace JDBC → JPA repositories
4. Add security → controller-level auth
5. Implement monitoring → metrics throughout layers

**Key:** Clear separation of concerns with established enterprise patterns.