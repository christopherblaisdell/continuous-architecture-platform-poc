---
agent: "agent"
description: "Run a structured security review on a NovaTrek solution design using OWASP Top 10, Spring Boot patterns, and NovaTrek data ownership rules. Produces a severity-rated findings report."
---

# Security Review — NovaTrek Architecture

You are performing a structured security review of a NovaTrek Adventures architecture solution design. This review applies the OWASP Top 10, Spring Boot security patterns, and NovaTrek-specific data ownership rules.

## Review Scope

Identify the solution design to review. If not specified, ask for the ticket ID (e.g., NTK-10005).

Read ALL files in the solution directory: `architecture/solutions/_NTK-XXXXX-*/`

## Security Review Checklist

Work through each category systematically. For every finding, assign a severity rating.

### Severity Ratings

| Rating | Definition | Action |
|--------|-----------|--------|
| CRITICAL | Exploitable vulnerability, data breach risk | Must fix before merge |
| HIGH | Security weakness with clear attack vector | Should fix before merge |
| MEDIUM | Defense-in-depth gap, hardening opportunity | Fix in next iteration |
| LOW | Best practice deviation, minor hardening | Track for future |
| INFO | Observation, no immediate risk | Document only |

### 1. Authentication and Identity (OWASP A07)

- Does the solution route ALL guest identity resolution through `svc-guest-profiles`?
- Are there shadow guest records in other services? (Anti-pattern: services maintaining their own copy of guest identity)
- For temporary profiles (ADR-008): is the session scope bounded? Is there an expiration mechanism?
- Are authentication tokens scoped to the minimum required access?
- Is session management secure (ADR-009: session-scoped kiosk access)?

### 2. Authorization and Access Control (OWASP A01)

- Are API endpoints protected by role-based access control?
- Can a guest access another guest's data through ID enumeration?
- Are kiosk sessions isolated per guest (no cross-session data leakage)?
- Do impact assessments specify who can call each new/modified endpoint?

### 3. Data Integrity and Ownership (NovaTrek-Specific)

- Does the solution respect data ownership boundaries? Reference `architecture/metadata/` for the ownership table:
  - Check-in records owned by `svc-check-in`
  - Guest profiles owned by `svc-guest-profiles`
  - Reservations owned by `svc-reservations`
  - Daily schedules owned by `svc-scheduling-orchestrator`
- Are cross-service data flows going through published API endpoints (not direct database access)?
- Does the solution use PATCH semantics for updates (ADR-010), not full entity replacement?
- Is optimistic locking (`@Version` / `_rev`) present on mutable entities (ADR-011)?

### 4. Input Validation (OWASP A03)

- Are all new API endpoints validated at the boundary?
- Are confirmation codes, reservation IDs, and guest identifiers validated for format and length?
- For the four-field identity verification (ADR-007): are all four fields validated?
- Are error responses safe (no stack traces, no internal IDs leaked)?

### 5. PII and Sensitive Data (OWASP A02)

- What PII fields are handled? (Guest names, emails, phone numbers, waiver data)
- Is PII transmitted only over encrypted channels?
- Is PII stored only in the owning service's data store?
- Are PII fields logged? (They should not be)
- Is there a data retention policy for temporary guest profiles?

### 6. Safety and Business Logic (NovaTrek-Specific)

- Does the solution handle unknown adventure categories safely?
- CRITICAL RULE: Unknown/unmapped categories MUST default to Pattern 3 (Full Service), NEVER Pattern 1 (ADR-005)
- Are waiver validations enforced before check-in completion?
- Does `svc-safety-compliance` remain the sole authority for waiver status?

### 7. Cross-Service Communication (OWASP A08, A10)

- Are new cross-service calls documented in `architecture/metadata/cross-service-calls.yaml`?
- Are synchronous call chains bounded (no unbounded cascade failures)?
- Are fallback paths defined for when downstream services are unavailable?
- Is there timeout/retry configuration for new integration points?

### 8. Injection and API Security (OWASP A03)

- Are OpenAPI specs for new/modified endpoints complete with types and constraints?
- Are query parameters sanitized in API specifications?
- Are enum values validated against known domain values?

## Output Format

Produce a structured security review report:

```markdown
# Security Review: NTK-XXXXX — [Solution Title]

**Reviewer**: AI Security Review (ECC-adapted)
**Date**: [today]
**Solution**: [solution folder path]
**Overall Risk Rating**: [CRITICAL/HIGH/MEDIUM/LOW]

## Summary

[2-3 sentence summary of findings]

## Findings

### [SEVERITY] Finding 1: [Title]

**Category**: [OWASP category or NovaTrek-specific]
**Location**: [file path and section]
**Description**: [what was found]
**Risk**: [what could go wrong]
**Recommendation**: [how to fix]

### [SEVERITY] Finding 2: [Title]
...

## Statistics

| Severity | Count |
|----------|-------|
| CRITICAL | X |
| HIGH | X |
| MEDIUM | X |
| LOW | X |
| INFO | X |

## Checklist Summary

| Category | Status | Notes |
|----------|--------|-------|
| Authentication & Identity | PASS/FAIL/PARTIAL | ... |
| Authorization & Access Control | PASS/FAIL/PARTIAL | ... |
| Data Integrity & Ownership | PASS/FAIL/PARTIAL | ... |
| Input Validation | PASS/FAIL/PARTIAL | ... |
| PII & Sensitive Data | PASS/FAIL/PARTIAL | ... |
| Safety & Business Logic | PASS/FAIL/PARTIAL | ... |
| Cross-Service Communication | PASS/FAIL/PARTIAL | ... |
| Injection & API Security | PASS/FAIL/PARTIAL | ... |
```

## Rules

- NEVER fabricate findings — only report issues supported by evidence in the solution files
- ALWAYS cite the specific file and section where the issue was found
- ALWAYS cross-reference with existing ADRs in `decisions/` to check if a concern is already addressed
- ALWAYS check the OpenAPI specs in `architecture/specs/` for the affected services
- If the solution has no security issues, say so — do not invent problems to fill the report
