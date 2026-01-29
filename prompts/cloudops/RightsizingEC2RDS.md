# AWS EC2/RDS Rightsizing & Graviton Migration Analysis

## Descripción General

Herramienta automatizada de optimización de costos que analiza instancias EC2 y bases de datos RDS en la región **us-east-1** para identificar recursos sobredimensionados basándose en:
- Utilización sostenida baja de CPU (<10% promedio, <20% p95)
- Patrones bajos de IOPS
- Oportunidades de migración a Graviton (ARM64)

---

## Configuración Técnica

### Región
- **Fija**: `us-east-1` (no configurable)

### Período Métrico
- **Ventana**: 30 días
- **Granularidad**: 5 minutos (máximo disponible en CloudWatch)
- **Retención CloudWatch**: 63 días para granularidad 5 min
- **Fuente de datos**: CloudWatch Metrics API

### Herramientas MCP Requeridas
```json
{
  "awslabs.ec2-mcp-server": "Enumerar instancias EC2 y metadatos",
  "awslabs.rds-mcp-server": "Enumerar instancias RDS y metadatos",
  "awslabs.cloudwatch-mcp-server": "Obtener métricas (CPU, IOPS, Network)",
  "awslabs.pricing-mcp-server": "Calcular ahorros potenciales (USD/mes)"
}
```

---

## Definiciones de Umbrales

### EC2 - Candidatos a Downsizing

**CPU Baja:**
- Promedio 30d: < 10%
- Percentil 95 (p95): < 20%
- Percentil 99 (p99): < 60% (exclusión si > 60% = batch/spike)

**IOPS Bajos (por volumen EBS):**
- Promedio Read IOPS 30d: < 50
- Promedio Write IOPS 30d: < 50
- Combinado (Read + Write): < 100 IOPS promedio
- Percentil 95: < 200 IOPS

**Exclusiones:**
- Instancias creadas hace < 72 horas
- Instancias con p99 CPU > 60% (cargas batch/spike)
- Instancias sin datos de métrica (< 80% de puntos de datos esperados)

### RDS - Candidatos a Downsizing

**CPU Baja:**
- Promedio 30d: < 10%
- Percentil 95 (p95): < 20%
- Percentil 99 (p99): < 60%

**IOPS Bajos:**
- Promedio Read IOPS 30d: < 100
- Promedio Write IOPS 30d: < 100
- Combinado: < 200 IOPS promedio
- Percentil 95: < 300 IOPS

**Exclusiones:**
- Instancias creadas hace < 72 horas
- Instancias con p99 CPU > 60%
- Instancias sin datos de métrica

---

## Tareas de Análisis

### 1. Análisis EC2

#### Recopilación de Datos
Para cada instancia en us-east-1:
- **InstanceId**, **InstanceType**, **Availability Zone**
- **Platform** (Linux/Windows), **OS** (Amazon Linux 2, Ubuntu, etc.)
- **Tenancy** (default/dedicated/host)
- **IAM Instance Profile**
- **VPC ID**, **Subnet ID**
- **Tags** (formato: `key=value;key2=value2`)
- **Launch Time** (para exclusión <72h)

#### Métricas CloudWatch (30 días, granularidad 5 min)
- **CPUUtilization**: avg, p95, p99
- **EBS Volumes** (por volumen adjunto):
  - VolumeReadOps: avg, p95
  - VolumeWriteOps: avg, p95
  - VolumeReadBytes: avg
  - VolumeWriteBytes: avg
  - BurstBalance: min (si aplica, para gp2)
- **Network**:
  - NetworkIn: avg (bytes/sec)
  - NetworkOut: avg (bytes/sec)

#### Clasificación
```
Candidate = YES si:
  (CPU_avg < 10% AND CPU_p95 < 20%) OR (IOPS_combined_avg < 100 AND IOPS_p95 < 200)
  AND CPU_p99 < 60%
  AND Launch_Time > 72h
  AND MetricDataPoints >= 80% de esperados

Reason = LowCPU | LowIOPS | Both
```

#### Recomendaciones Graviton
- **GravitonCandidate = YES** si existe tipo equivalente en familias: t4g, m6g, c7g, r6g, r7g
- **Ejemplo**: m5.large → m6g.large (mismo vCPU/RAM, ARM64)
- **ValidateGraviton = YES** (requiere validación manual antes de ejecutar)

#### Checklist de Compatibilidad ARM64
```
[ ] Arquitectura: AMI soporta ARM64 (aarch64)
[ ] SO: Amazon Linux 2, Ubuntu 20.04+, RHEL 8+, etc.
[ ] Runtimes: Python, Node.js, Java, Go compilados para ARM64
[ ] Librerías nativas: Verificar dependencias (ffmpeg, ImageMagick, etc.)
[ ] Drivers: Verificar drivers de hardware (GPU, NIC especializada)
[ ] Toolchains: Compiladores y herramientas de build compatibles
```

### 2. Análisis RDS

#### Recopilación de Datos
Para cada instancia/cluster:
- **DBInstanceIdentifier**, **Engine** (PostgreSQL/MySQL/MariaDB/Oracle/SQL Server), **Engine Version**
- **DB Instance Class** (db.m6i.large, etc.)
- **Multi-AZ** (Yes/No)
- **Storage Type** (gp2/gp3/io1/io2), **Allocated Storage (GB)**
- **Publicly Accessible** (Yes/No)
- **VPC ID**, **DB Subnet Group**
- **Tags**
- **Creation Time**

#### Métricas CloudWatch (30 días, granularidad 5 min)
- **CPUUtilization**: avg, p95, p99
- **ReadIOPS**: avg, p95
- **WriteIOPS**: avg, p95
- **FreeableMemory**: min (GB)
- **ReadLatency**: avg (ms) - si disponible
- **WriteLatency**: avg (ms) - si disponible
- **DatabaseConnections**: max

#### Clasificación
```
Candidate = YES si:
  (CPU_avg < 10% AND CPU_p95 < 20%) OR (IOPS_combined_avg < 200 AND IOPS_p95 < 300)
  AND CPU_p99 < 60%
  AND Creation_Time > 72h
  AND MetricDataPoints >= 80%

Reason = LowCPU | LowIOPS | Both
```

#### Recomendaciones Graviton
- **GravitonCandidate = YES** si engine/versión soporta Graviton:
  - PostgreSQL: 13.7+, 14.4+, 15+, 16+
  - MySQL: 8.0.28+
  - MariaDB: 10.6+
  - Oracle: 21c+ (solo db.r6g.*)
  - SQL Server: NO soporta Graviton
- **Ejemplo**: db.m6i.large → db.m6g.large
- **ValidateGraviton = YES**

#### Checklist de Compatibilidad Graviton
```
[ ] Engine/Versión: Soporta Graviton (ver tabla arriba)
[ ] Extensiones: Verificar extensiones PostgreSQL compiladas para ARM64
[ ] Parámetros: Revisar parámetros de grupo de parámetros (no hay incompatibilidades conocidas)
[ ] Drivers: Clientes (psycopg2, mysql-connector, etc.) soportan ARM64
[ ] Lambdas/Clientes: Aplicaciones conectadas compiladas para ARM64
[ ] Backups: Compatibilidad de snapshots (generalmente transparente)
```

### 3. Cálculo de Ahorros (MCP Pricing)

#### Datos Requeridos
- **Tipo actual**: m5.large
- **Tipo propuesto**: m6g.large o m5.medium
- **Región**: us-east-1
- **Tenancy**: default/dedicated
- **Período**: 730 horas/mes (promedio)

#### Consulta MCP Pricing
```
get_pricing(
  service="AmazonEC2",
  filters={
    "location": "US East (N. Virginia)",
    "instanceType": "m5.large",
    "tenancy": "On Demand",
    "operatingSystem": "Linux"
  }
)
```

#### Cálculo de Ahorro
```
CostoActual = PrecioHora_Actual × 730 horas/mes
CostoProyectado = PrecioHora_Propuesto × 730 horas/mes
AhorroMensual = CostoActual - CostoProyectado
AhorroAnual = AhorroMensual × 12
PorcentajeAhorro = (AhorroMensual / CostoActual) × 100%
```

#### Nota en CSV
```
"AWS Pricing via MCP (effective_date=2026-01-29, region=us-east-1)"
```

---

## Salidas

### 1. CSV: `rightsizing-ec2-rds-us-east-1.csv`

**Formato**: UTF-8, delimitado por comas, con escaping de comillas

**Columnas**:
```
ResourceKind,Id,CurrentType,ProposedType,GravitonCandidate,ValidateGraviton,Reason,
CPU_Avg_30d,CPU_p95_30d,CPU_p99_30d,IOPS_Read_Avg_30d,IOPS_Write_Avg_30d,
NetworkIn_Avg_Mbps,NetworkOut_Avg_Mbps,
EstSavingUSD_Monthly,EstSavingPercent,
MetricPeriod,MetricDataPoints,DataQuality,
Notes,Tags
```

**Ejemplo fila EC2**:
```
EC2,i-0123456789abcdef0,m5.large,m6g.large,YES,YES,LowCPU,
8.5,18.2,45.3,12.5,8.3,
2.1,1.8,
45.60,22.5,
30d_5min,8640,OK,
"AWS Pricing via MCP (effective_date=2026-01-29)",Name=WebServer;Env=Prod
```

**Ejemplo fila RDS**:
```
RDS,prod-db-01,db.m6i.large,db.m6g.large,YES,YES,LowIOPS,
9.2,17.5,52.1,85.3,72.1,
N/A,N/A,
38.25,18.0,
30d_5min,8640,OK,
"AWS Pricing via MCP (effective_date=2026-01-29)",Engine=PostgreSQL;Env=Prod
```

**Reglas**:
- Si `Candidate=NO`, `ProposedType` está vacío
- `Tags` en formato `key=value;key2=value2` (escapar `;` si está en valor)
- `MetricDataPoints`: número de puntos de datos recopilados / esperados (ej: "8640/8640")
- `DataQuality`: OK | Incomplete | Insufficient

### 2. Markdown: `rightsizing-ec2-rds-us-east-1.md`

**Estructura**:

```markdown
# AWS EC2/RDS Rightsizing Analysis Report
## us-east-1 | Generated: 2026-01-29 14:30 UTC

### Executive Summary
- **Total EC2 Instances Analyzed**: 45
- **EC2 Candidates for Rightsizing**: 12 (26.7%)
- **EC2 Graviton Migration Candidates**: 8 (17.8%)
- **Estimated Monthly Savings (EC2)**: $542.80
- **Estimated Annual Savings (EC2)**: $6,513.60

- **Total RDS Instances Analyzed**: 18
- **RDS Candidates for Rightsizing**: 5 (27.8%)
- **RDS Graviton Migration Candidates**: 3 (16.7%)
- **Estimated Monthly Savings (RDS)**: $287.50
- **Estimated Annual Savings (RDS)**: $3,450.00

- **Total Potential Savings**: $9,963.60/year

### Analysis Criteria
- **Metric Period**: 30 days (5-minute granularity)
- **CPU Threshold**: avg < 10%, p95 < 20%
- **IOPS Threshold**: combined < 100 (EC2) / < 200 (RDS)
- **Exclusions**: Instances < 72h old, p99 CPU > 60%
- **Data Quality**: Minimum 80% of expected data points

### Warnings & Considerations
⚠️ **Before implementing any changes**:
1. Validate ARM64 compatibility (see checklists below)
2. Test in non-production environment first
3. Plan maintenance windows (downtime required)
4. Verify application performance post-migration
5. Monitor for 7-14 days after change

---

## EC2 Rightsizing Recommendations

### Low CPU Utilization Candidates (LowCPU)
| Instance ID | Current Type | Proposed Type | Graviton | CPU Avg | CPU p95 | Monthly Savings | Risk Level |
|---|---|---|---|---|---|---|---|
| i-0123456789abcdef0 | m5.large | m5.medium | NO | 8.5% | 18.2% | $22.80 | Low |
| i-0987654321fedcba0 | m6i.xlarge | m6i.large | NO | 9.1% | 19.5% | $45.60 | Low |
| i-abcdef0123456789 | m5.large | m6g.large | YES | 7.8% | 17.3% | $45.60 | Medium |

### Low IOPS Candidates (LowIOPS)
| Instance ID | Current Type | Proposed Type | Graviton | Read IOPS | Write IOPS | Monthly Savings | Risk Level |
|---|---|---|---|---|---|---|---|
| i-1111111111111111 | i3.2xlarge | i3.xlarge | NO | 45.2 | 38.5 | $156.00 | Low |

### Graviton Migration Candidates (Both + Graviton)
| Instance ID | Current Type | Proposed Type | CPU Avg | IOPS Avg | Monthly Savings | Validation Required |
|---|---|---|---|---|---|---|
| i-abcdef0123456789 | m5.large | m6g.large | 7.8% | 85 | $45.60 | ✓ ARM64 AMI, Python 3.9+, no GPU |
| i-2222222222222222 | c5.2xlarge | c7g.2xlarge | 8.2% | 120 | $89.40 | ✓ Ubuntu 22.04, Node.js 18+, no native libs |

### EC2 Compatibility Checklist (Graviton)

#### Instance: i-abcdef0123456789 (m5.large → m6g.large)
```
[ ] Architecture: Verify AMI supports ARM64
    Command: aws ec2 describe-images --image-ids ami-xxxxx --query 'Images[0].Architecture'
    Expected: arm64
    
[ ] Operating System: Check OS version
    Command: cat /etc/os-release
    Expected: Amazon Linux 2, Ubuntu 20.04+, RHEL 8+
    
[ ] Runtimes: Verify application runtimes
    - Python: python --version (3.7+)
    - Node.js: node --version (14+)
    - Java: java -version (11+)
    
[ ] Native Libraries: Check for ARM64 compatibility
    - ffmpeg: ldd /usr/bin/ffmpeg | grep arm64
    - ImageMagick: identify -version
    - Custom libs: Recompile if needed
    
[ ] Drivers: Verify hardware drivers
    - NIC: ethtool -i eth0
    - GPU: nvidia-smi (if applicable)
    
[ ] Toolchains: Verify build tools
    - gcc: gcc --version (ARM64 support)
    - Docker: docker run --platform linux/arm64 ...
```

---

## RDS Rightsizing Recommendations

### Low CPU Utilization Candidates (LowCPU)
| DB Instance | Engine | Current Class | Proposed Class | Graviton | CPU Avg | CPU p95 | Monthly Savings |
|---|---|---|---|---|---|---|---|
| prod-db-01 | PostgreSQL 14 | db.m6i.large | db.m6i.medium | NO | 9.2% | 17.5% | $38.25 |
| staging-db | MySQL 8.0 | db.r6i.xlarge | db.r6i.large | NO | 8.7% | 18.1% | $76.50 |

### Low IOPS Candidates (LowIOPS)
| DB Instance | Engine | Current Class | Proposed Class | Graviton | Read IOPS | Write IOPS | Monthly Savings |
|---|---|---|---|---|---|---|---|
| analytics-db | PostgreSQL 15 | db.m6i.2xlarge | db.m6i.xlarge | YES | 95.3 | 72.1 | $89.40 |

### Graviton Migration Candidates (RDS)
| DB Instance | Engine | Current Class | Proposed Class | Monthly Savings | Validation Required |
|---|---|---|---|---|---|
| prod-db-01 | PostgreSQL 14 | db.m6i.large | db.m6g.large | $38.25 | ✓ Engine 13.7+, no custom extensions |
| analytics-db | PostgreSQL 15 | db.m6i.2xlarge | db.m6g.2xlarge | $89.40 | ✓ Engine 15+, verify pg_trgm, uuid-ossp |

### RDS Engine Support for Graviton
| Engine | Supported Versions | Graviton Family | Notes |
|---|---|---|---|
| PostgreSQL | 13.7+, 14.4+, 15+, 16+ | db.m6g, db.r6g, db.r7g | Full support |
| MySQL | 8.0.28+ | db.m6g, db.r6g, db.r7g | Full support |
| MariaDB | 10.6+ | db.m6g, db.r6g, db.r7g | Full support |
| Oracle | 21c+ | db.r6g (read replicas only) | Limited support |
| SQL Server | N/A | N/A | Not supported |

### RDS Compatibility Checklist (Graviton)

#### Instance: prod-db-01 (PostgreSQL 14, db.m6i.large → db.m6g.large)
```
[ ] Engine/Version: Verify Graviton support
    Current: PostgreSQL 14.5
    Required: PostgreSQL 13.7+
    Status: ✓ Compatible
    
[ ] Extensions: Check for ARM64 compatibility
    SELECT * FROM pg_extension;
    - uuid-ossp: ✓ Built-in, ARM64 compatible
    - pg_trgm: ✓ Built-in, ARM64 compatible
    - Custom extensions: Verify compilation for ARM64
    
[ ] Parameters: Review parameter group
    - No known incompatibilities with Graviton
    - Verify: shared_buffers, work_mem, maintenance_work_mem
    
[ ] Drivers: Verify client drivers
    - psycopg2: pip install psycopg2-binary (ARM64 wheel available)
    - JDBC: java -version (ARM64 JVM)
    - Node.js pg: npm install pg (ARM64 support)
    
[ ] Lambdas/Clients: Check connected applications
    - Lambda functions: Verify ARM64 runtime (Python 3.9+, Node.js 18+)
    - EC2 clients: Verify OS/runtime compatibility
    
[ ] Backups: Verify snapshot compatibility
    - Automated backups: Transparent, no action needed
    - Manual snapshots: Can be restored to Graviton instances
```

---

## Implementation Roadmap (30/60/90 Days)

### Phase 1: Testing (Days 1-30)
**Objective**: Validate compatibility and performance

**Week 1-2: Preparation**
- [ ] Select 2-3 low-risk candidates (LowCPU, non-critical)
- [ ] Create snapshots/backups
- [ ] Document current performance baseline
- [ ] Prepare rollback plan

**Week 3-4: Testing**
- [ ] Launch test instances/databases with proposed types
- [ ] Run application workload tests (24-48 hours)
- [ ] Monitor CPU, IOPS, latency, memory
- [ ] Validate ARM64 compatibility (if Graviton)
- [ ] Document results

**Success Criteria**:
- Performance within 5% of current
- No application errors
- Monitoring shows stable metrics

### Phase 2: Staging (Days 31-60)
**Objective**: Validate in production-like environment

**Week 5-6: Staging Deployment**
- [ ] Deploy to staging environment
- [ ] Run full regression tests
- [ ] Load testing (simulate peak traffic)
- [ ] Security scanning
- [ ] Cost validation

**Week 7-8: Monitoring**
- [ ] Monitor for 7-14 days
- [ ] Collect performance metrics
- [ ] Validate cost savings
- [ ] Get stakeholder approval

**Success Criteria**:
- All tests pass
- Performance acceptable
- Cost savings verified
- Stakeholder sign-off

### Phase 3: Production (Days 61-90)
**Objective**: Gradual rollout to production

**Week 9-10: Canary Deployment**
- [ ] Deploy to 10-20% of production instances
- [ ] Monitor for 3-5 days
- [ ] Collect metrics and feedback
- [ ] Adjust if needed

**Week 11-12: Full Rollout**
- [ ] Deploy to remaining instances
- [ ] Stagger deployments (avoid simultaneous changes)
- [ ] Monitor continuously
- [ ] Document lessons learned

**Success Criteria**:
- Zero critical incidents
- Performance meets SLA
- Cost savings achieved
- Team trained on new setup

---

## Risk Assessment

### Low Risk (Proceed with Confidence)
- **LowCPU only** (no IOPS changes)
- **Same instance family** (m5 → m5.medium)
- **Non-critical workloads** (dev, staging)
- **Downtime acceptable** (batch jobs, non-24/7)

### Medium Risk (Requires Testing)
- **Graviton migration** (ARM64 validation needed)
- **IOPS reduction** (verify storage performance)
- **Production workloads** (requires staging test)
- **Downtime limited** (requires maintenance window)

### High Risk (Proceed with Caution)
- **Critical production** (24/7 availability required)
- **Custom native libraries** (ARM64 compilation uncertain)
- **Significant IOPS reduction** (>50% decrease)
- **Untested workloads** (no staging environment)

---

## Appendix: Metric Definitions

### CPU Utilization
- **Average (avg)**: Mean CPU % over 30 days
- **Percentile 95 (p95)**: 95% of measurements below this value
- **Percentile 99 (p99)**: 99% of measurements below this value

### IOPS (Input/Output Operations Per Second)
- **Read IOPS**: Database/disk read operations per second
- **Write IOPS**: Database/disk write operations per second
- **Combined**: Read IOPS + Write IOPS

### Data Quality
- **OK**: ≥ 80% of expected data points collected
- **Incomplete**: 50-80% of expected data points
- **Insufficient**: < 50% of expected data points

### Pricing
- **Effective Date**: Date pricing data was retrieved
- **Region**: us-east-1 (US East N. Virginia)
- **Tenancy**: On-Demand (default)
- **OS**: Linux (unless specified)

---

## Next Steps

1. **Review Report**: Share with team and stakeholders
2. **Prioritize**: Select candidates by risk level and savings
3. **Test**: Follow 30/60/90 roadmap
4. **Implement**: Deploy changes in phases
5. **Monitor**: Track savings and performance
6. **Iterate**: Repeat analysis quarterly

---

**Report Generated**: 2026-01-29 14:30 UTC  
**Analysis Period**: 30 days (5-minute granularity)  
**Data Source**: CloudWatch Metrics + AWS Pricing API  
**Region**: us-east-1 (US East N. Virginia)
```

---

## Configuración MCP Recomendada

Agrega esto a tu `~/.kiro/settings/mcp.json`:

```json
    "awslabs.aws-pricing-mcp-server": {
      "command": "uvx",
      "args": [
         "awslabs.aws-pricing-mcp-server@latest"
      ],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR",
        "AWS_PROFILE": "your-aws-profile",
        "AWS_REGION": "us-east-1"
      },
      "disabled": false,
      "autoApprove": []
    }
```

---
