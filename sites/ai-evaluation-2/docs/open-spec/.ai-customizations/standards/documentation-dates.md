# Documentation Date Standards

**Applicable Modes**: Corporate Compliance, Solution Architect

## Overview

Proper date management in documentation ensures traceability, compliance, and historical accuracy. All dates must follow ISO 8601 format, and historical documents require special handling to maintain point-in-time accuracy.

## ISO 8601 Date Format

### Standard Format
All dates MUST use ISO 8601 format: `YYYY-MM-DD`

**Examples**:
- 2024-03-15 ✅ CORRECT
- 03/15/2024 ❌ INCORRECT
- 15-Mar-2024 ❌ INCORRECT
- March 15, 2024 ❌ INCORRECT

### DateTime Format
When time is required: `YYYY-MM-DDTHH:mm:ssZ`

**Examples**:
- 2024-03-15T14:30:00Z (UTC)
- 2024-03-15T14:30:00-05:00 (Eastern Time)
- 2024-03-15T14:30:00+01:00 (Central European Time)

## Document Naming with Dates

### Historical Documents
Documents representing point-in-time decisions or states MUST include date prefix:

```
Format: YYYY-MM-DD-document-name.md

Examples:
2024-03-15-architecture-decision-api-versioning.md
2024-03-20-meeting-notes-security-review.md
2024-04-01-deployment-plan-phase-2.md
```

### Living Documents
Documents that are continuously updated should NOT have date prefix:

```
Examples:
architecture-overview.md (not 2024-03-15-architecture-overview.md)
api-documentation.md
deployment-guide.md
```

## Date Usage in Documents

### Document Headers
Every document should include creation and modification dates:

```markdown
# Document Title

**Created**: 2024-03-15
**Last Modified**: 2024-03-20
**Author**: John Smith
**Status**: Approved
```

### Version History
Track significant changes with dates:

```markdown
## Version History

| Date | Version | Author | Changes |
|------|---------|--------|---------|
| 2024-03-15 | 1.0 | John Smith | Initial version |
| 2024-03-18 | 1.1 | Jane Doe | Added security section |
| 2024-03-20 | 2.0 | John Smith | Major revision for new requirements |
```

### Meeting Documentation
```markdown
# Architecture Review Meeting

**Date**: 2024-03-15
**Time**: 14:00-15:30 UTC
**Attendees**: John Smith, Jane Doe, Bob Johnson

## Agenda
[Meeting content...]

## Decisions Made
- Decision 1 - Approved on 2024-03-15
- Decision 2 - Deferred to 2024-03-22
```

## Compliance Documentation

### Audit Trail Requirements
For compliance-critical documents:

```markdown
# Security Policy Document

**Effective Date**: 2024-04-01
**Review Date**: 2024-10-01
**Approval Date**: 2024-03-25
**Approved By**: Security Committee

## Document Control
- **Classification**: Confidential
- **Retention Period**: 7 years from 2024-04-01
- **Next Review**: 2024-10-01
```

### Change Log Format
```markdown
## Change Log

### 2024-03-20 - Major Update
- **Changed By**: Jane Doe
- **Approval**: Ticket #SEC-1234
- **Changes**:
  - Updated password policy from 8 to 12 characters
  - Added MFA requirement for all admin accounts
  - Revised incident response timeline

### 2024-03-15 - Initial Release
- **Created By**: John Smith
- **Approval**: Ticket #SEC-1000
- **Status**: Approved by Security Committee
```

## Architecture Decision Records (ADR)

### File Naming
```
decisions/
├── 2024-03-15-adr-001-api-versioning-strategy.md
├── 2024-03-20-adr-002-database-selection.md
├── 2024-04-01-adr-003-authentication-approach.md
└── 2024-04-05-adr-004-monitoring-tools.md
```

### ADR Date Sections
```markdown
# ADR-001: API Versioning Strategy

**Date**: 2024-03-15
**Status**: Accepted
**Deciders**: Architecture Review Board
**Decision Date**: 2024-03-15
**Review Date**: 2024-09-15

## Context
[As of 2024-03-15, our API serves 10,000 requests/day...]

## Decision
[Effective 2024-04-01, we will implement URL-based versioning...]
```

## Historical Reference Standards

### Referencing Past States
When referring to historical states, always include date:

```markdown
❌ INCORRECT:
"The system previously used MySQL"

✅ CORRECT:
"Prior to 2024-03-15, the system used MySQL"
"As of 2024-03-15, the system migrated to PostgreSQL"
```

### Timeline Documentation
```markdown
## Migration Timeline

### Phase 1: Planning (2024-01-15 to 2024-02-28)
- Requirements gathering completed 2024-01-30
- Architecture design approved 2024-02-15
- Resource allocation confirmed 2024-02-28

### Phase 2: Implementation (2024-03-01 to 2024-05-31)
- Development start: 2024-03-01
- Alpha release: 2024-04-15
- Beta release: 2024-05-15
- Production release: 2024-05-31
```

## Retention and Archival

### Document Lifecycle
```yaml
Document Types and Retention:
  Architecture Decisions: 
    Retention: Permanent
    Archive After: 2 years
    
  Meeting Notes:
    Retention: 3 years
    Archive After: 1 year
    
  Design Documents:
    Retention: 5 years after obsolete
    Archive After: System decommission + 1 year
    
  Compliance Documents:
    Retention: 7 years minimum
    Archive After: As per regulatory requirements
```

### Archive Naming
When archiving, maintain date information:
```
archive/
├── 2023/
│   ├── 2023-01-15-architecture-decision.md
│   └── 2023-12-31-year-end-review.md
├── 2024/
│   ├── 2024-01-15-Q1-planning.md
│   └── 2024-03-15-architecture-decision.md
```

## Date Validation Rules

### Consistency Checks
1. Creation date ≤ Last modified date
2. Decision date ≤ Effective date
3. Review date > Creation date
4. Archive date > Last modified date

### Future Dating
- Planning documents may have future dates
- Effective dates may be future
- Creation dates must never be future
- Decision dates must never be future

## Integration with Source Control

### Git Commit Messages with Dates
While Git tracks timestamps, include dates for significant changes:

```bash
git commit -m "2024-03-15: Implement new authentication flow per ADR-003"
git commit -m "2024-03-20: Update security policy effective 2024-04-01"
```

### Tagging Releases
```bash
git tag -a v2.1.0-2024-03-15 -m "Release 2.1.0 on 2024-03-15"
git tag -a security-audit-2024-03-15 -m "Security audit snapshot"
```

## Best Practices

### Do's ✅
1. Always use ISO 8601 format
2. Include timezone when time is specified
3. Date-prefix historical documents
4. Track all significant changes with dates
5. Maintain version history

### Don'ts ❌
1. Use ambiguous date formats (03/04/24)
2. Omit dates from decisions
3. Modify historical documents
4. Use relative dates ("last week")
5. Forget timezone information

## Compliance Checklist

For compliance-critical documents:
- [ ] Creation date documented
- [ ] Last modified date current
- [ ] All dates in ISO 8601 format
- [ ] Historical references include dates
- [ ] Version history maintained
- [ ] Approval dates recorded
- [ ] Review dates scheduled
- [ ] Retention period defined
- [ ] Archive date planned
- [ ] Timezone specified where needed

## Examples

### Decision Document
```markdown
# 2024-03-15-decision-microservices-migration.md

**Decision Date**: 2024-03-15
**Effective Date**: 2024-06-01
**Review Date**: 2025-03-15
**Expires**: 2026-03-15

## Background
As of 2024-03-15, our monolithic application serves 1M requests/day...

## Decision
Effective 2024-06-01, we will begin migrating to microservices...

## Timeline
- 2024-03-15: Decision approved
- 2024-04-01: Planning phase begins
- 2024-06-01: Implementation starts
- 2024-12-31: Target completion
```

### Compliance Report
```markdown
# Security Compliance Report

**Report Date**: 2024-03-15
**Period Covered**: 2024-01-01 to 2024-03-15
**Next Report Due**: 2024-06-15

## Compliance Status as of 2024-03-15
All systems compliant with security policy v2.3 (effective 2024-01-01)

## Changes Since 2023-12-31
- MFA implemented (completed 2024-02-15)
- Encryption upgraded (completed 2024-03-01)
```

---

Proper date documentation ensures our systems remain auditable, compliant, and historically accurate. Always use ISO 8601 format and maintain clear date references throughout all documentation.