# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **Flutter Mobile Development**
  - Flutter advanced logging skills with console and RUM (Real User Monitoring) support
  - Flutter environments agent skills for development configuration
  - Comprehensive Flutter testing agent skills: unit, widget, integration, mutation testing, and golden file testing
  - Flutter feature creation prompt with detailed steps for repository evaluation and report generation
  - Flutter UI component creation rules for building reusable components
  - Flutter security rules documentation with prompt evaluation guidelines

- **Integration & Migration**
  - OSB (Oracle Service Bus) 12c to Java 21 migration comprehensive prompts and rules
    - 12 detailed sections covering OSB components and Java 21 equivalents
    - Migration approach guidance for functional replacement strategy
    - Guidelines for rewriting OSB logic as modern Java 21 services
    - Constraint documentation and anti-pattern identification
  - IIB (IBM Integration Bus) documentation and migration guidance
  - Integration API design rules and performance rules

- **CloudOps & Infrastructure**
  - AWS IAM Users Audit guide with security best practices
    - MFA requirements and key rotation strategies
    - Inactivity checks and inline policy validation
    - Password policy requirements documentation
  - EC2 Cost Validation documentation covering OnDemand, Spot, and Reserved Instances
  - EBS and Snapshots optimization tool documentation with cost analysis
  - AWS EC2/RDS rightsizing documentation with Graviton migration analysis
  - CloudOps IaC reference modules creation prompts and rules for Terraform

- **QA & Testing**
  - QA testing artifacts and quality assurance documentation
  - Comprehensive quality rules and standards

- **DevSecOps**
  - DevSecOps comprehensive rules and security guidelines
  - DevSecOps prompts for security implementation

- **Frontend Development**
  - Frontend creational commits prompt for conventional commit messages
  - Frontend creational documentation prompt for effective documentation practices
  - Frontend unit test prompt for comprehensive test coverage
  - Frontend transversal rules for cross-cutting concerns

- **Backend Development**
  - Backend rules draft for Java development standards
  - Architecture-related documentation

### Changed

- **File Organization & Naming**
  - Renamed CloudOps documentation files for consistency:
    - `CostValidationEc2.md` → `cloudops-CostValidationEc2.md`
    - `OptimizerStorage.md` → `cloudops-OptimizerStorage.md`
    - `RightsizingEC2RDS.md` → `cloudops-RightsizingEC2RDS.md`
    - `AuditIamUser.md` → `cloudops-AuditIamUser.md`
  - Updated Flutter mobile security rules format for AI agent evaluation
  - Updated Flutter security rules documentation for enhanced clarity

### Fixed

- **Documentation & Prompts**
  - Fixed Flutter error agent skills documentation and naming
  - Fixed duplicate monitoring step in OptimizerStorage documentation
  - Fixed missing step for verifying file creation order in Flutter workflows
  - Fixed Flutter feature creation rules with variant and state usage guidance
  - Fixed Flutter security rules prompt documentation
  - Fixed steps for MCP Figma integration in UI rules

### Deprecated

- _No deprecated features in this release_

### Removed

- _No removed features in this release_

### Security

- _No security updates in this release_

---

## Comparison Links

[unreleased]: https://github.com/somospragma/pragma-ia-solving-with-ai/compare/v0.1.0...HEAD
