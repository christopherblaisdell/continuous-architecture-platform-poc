# Architecture Decisions — NTK-10009

## ADR-NTK10009-001: Extend svc-payments Rather Than New Dispute Service

### Status

Accepted

### Date

2026-03-06

### Context and Problem Statement

Dispute and refund workflows require close integration with payment records (amounts, processor references, refund history). The question is whether to build dispute capabilities within svc-payments or create a separate svc-disputes microservice.

### Decision Drivers

- Data locality — disputes reference payment records directly
- Transaction integrity — refund processing must be atomic with dispute resolution
- Team ownership — NovaTrek Platform Team owns both payment and refund operations
- Operational simplicity — fewer services to deploy and monitor
- Bounded context — disputes are a sub-domain of payments, not an independent domain

### Considered Options

**Option 1: Extend svc-payments with dispute endpoints** (SELECTED)

- (+) Disputes have direct database access to payment and refund records
- (+) Refund creation atomic with dispute resolution (single transaction)
- (+) No cross-service call overhead for payment lookups
- (+) Same team owns the full financial lifecycle
- (-) Increases svc-payments complexity and deployment surface
- (-) Dispute queue UI requirements may differ from payment processing

**Option 2: Create separate svc-disputes microservice**

- (+) Clean separation of payment processing and dispute workflows
- (+) Independent deployment for dispute workflow changes
- (-) Requires cross-service calls for every payment lookup
- (-) Split transaction boundary — dispute resolution and refund creation span two services
- (-) Introduces unnecessary operational overhead for a tightly coupled domain

### Decision Outcome

Selected **Option 1: Extend svc-payments**. Disputes are a sub-domain of payments — they reference payment records, create refunds, and share the same financial audit requirements. Splitting them into a separate service creates artificial transaction boundaries without meaningful domain separation.

### Consequences

**Positive**: Atomic transactions between disputes and refunds; no cross-service latency for payment lookups.

**Negative**: svc-payments grows in complexity; deployment surface increases.

**Neutral**: Consistent with NovaTrek pattern of keeping sub-domains within their parent service.

---

## ADR-NTK10009-002: YAML-Driven Refund Policy Engine

### Status

Accepted

### Date

2026-03-06

### Context and Problem Statement

Refund eligibility depends on business rules (cancellation windows, refund percentages, exception categories). These rules must be codified to enable automated processing. The question is where and how to store refund policies.

### Decision Drivers

- Auditability — policies must be version-controlled for financial compliance
- Consistency — every refund request evaluated against the same rules
- Change management — policy changes should be reviewed and approved (not ad-hoc)
- Simplicity — avoid over-engineering for a manageable number of policy rules
- Precedent — ADR-004 established YAML-driven configuration for adventure classification

### Considered Options

**Option 1: YAML configuration file deployed with the service** (SELECTED)

- (+) Version-controlled in Git — full audit trail of policy changes
- (+) Policy changes go through PR review process
- (+) Follows ADR-004 precedent (configuration-driven classification)
- (+) Simple to implement — no additional infrastructure
- (-) Policy changes require a deployment
- (-) No runtime editing by business users

**Option 2: Database-stored policies with admin UI**

- (+) Business users can modify policies without deployments
- (+) Runtime-editable granularity
- (-) Policy changes bypass code review — audit trail is weaker
- (-) Risk of accidental policy misconfiguration in production
- (-) Requires building an admin UI (significant effort)

**Option 3: Rules engine (e.g., Drools)**

- (+) Complex conditional logic support
- (-) Massive over-engineering for what amounts to date-range and percentage calculations
- (-) Additional runtime dependency
- (-) Learning curve for the team

### Decision Outcome

Selected **Option 1: YAML configuration**. Refund policies are relatively simple (cancellation window thresholds mapped to refund percentages) and change infrequently. YAML in Git provides version control, PR-based review, and follows the ADR-004 precedent.

### Consequences

**Positive**: Full audit trail; policy changes reviewed by architects; follows established pattern.

**Negative**: Requires deployment for policy changes; business users cannot self-serve.

**Neutral**: If policy change frequency increases, migration to database-driven policies is straightforward.

---

## ADR-NTK10009-003: Three-Tier Escalation Model

### Status

Accepted

### Date

2026-03-06

### Context and Problem Statement

Not all refund requests are equal. Simple cancellation refunds within policy can be auto-approved, but edge cases (partial refunds, weather cancellations, complaints about service quality) and high-value disputes need human review. The question is how to structure the escalation workflow.

### Decision Drivers

- Efficiency — auto-approve straightforward cases to reduce agent workload
- Accountability — high-value decisions require appropriate authority level
- Flexibility — support for various dispute reasons and amounts
- Auditability — clear record of who approved what and why

### Considered Options

**Option 1: Three-tier escalation (auto / agent / manager)** (SELECTED)

- (+) Handles the full spectrum from simple to complex
- (+) Auto-approval reduces agent workload for policy-eligible refunds
- (+) Clear accountability — managers approve high-value exceptions
- (+) Each tier has defined authority limits (configurable thresholds)
- (-) More complex than a single-tier model

**Option 2: Single-tier (all disputes go to agent queue)**

- (+) Simpler implementation
- (-) Agents handle trivial cases that could be automated
- (-) No escalation path for complex disputes
- (-) High-value disputes handled by same authority as low-value

**Option 3: Two-tier (auto-approve + manual)**

- (+) Simpler than three-tier
- (-) No distinction between routine agent cases and high-value manager cases
- (-) Accountability gap for large refund amounts

### Decision Outcome

Selected **Option 1: Three-tier escalation**. The auto-approve tier handles the majority of refund requests (policy-eligible cancellations). Agent review handles edge cases. Manager escalation provides appropriate authority for high-value or exception cases.

**Tier thresholds** (configurable in YAML):

| Tier | Trigger | Authority |
|------|---------|-----------|
| Auto-approve | Policy-eligible, amount under threshold | System |
| Agent review | Not policy-eligible OR amount between thresholds | Guest Services Agent |
| Manager escalation | Amount above threshold OR exception category | Guest Services Manager |

### Consequences

**Positive**: Efficient handling across the full spectrum; clear accountability; configurable thresholds.

**Negative**: More complex workflow implementation; requires role-based access control for agent vs. manager tiers.

**Neutral**: Threshold values are configurable — can be tuned based on operational experience.
