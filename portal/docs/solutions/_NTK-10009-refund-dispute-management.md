---
title: "NTK-10009 — NTK-10009 Solution Design — Refund and Dispute Management Workflows"
description: "Solution design for NTK-10009"
---

# NTK-10009 — NTK-10009 Solution Design — Refund and Dispute Management Workflows

| Field | Value |
|-------|-------|
| **Status** | Proposed |
| **Version** | Date |
| **Author** | Solution Architect (AI-Assisted) |
| **Date** | 2026-03-06 |
| **Ticket** | NTK-10009 |

## Affected Capabilities

| Capability | Impact | Description |
|-----------|--------|-------------|
| [CAP-5.5 Refund and Dispute Management](../capabilities/index.md#cap-55-refund-and-dispute-management) | enhanced | svc-payments extended with dispute lifecycle, YAML-driven refund policy engine, and three-tier escalation |
| [CAP-5.4 Financial Reporting and Reconciliation](../capabilities/index.md#cap-54-financial-reporting-and-reconciliation) | enhanced | Dispute resolution records provide structured audit trail for financial reconciliation |

## Affected Services

- [svc-payments](../microservices/svc-payments.md)
- [svc-reservations](../microservices/svc-reservations.md)
- [svc-notifications](../microservices/svc-notifications.md)
- [svc-analytics](../microservices/svc-analytics.md)

## Architecture Decisions

- ADR-NTK10009-001
- ADR-NTK10009-002
- ADR-NTK10009-003

## Solution Contents

- Requirements
- Analysis
- Decisions
- Impact Assessments (2)
- User Stories
- Risk Assessment
- Capability Mapping

## Related Solutions

Solutions that share services or capabilities with this design:

| Solution | Shared Capabilities | Shared Services |
|----------|-------------------|-----------------|
| [NTK-10006 — NTK-10006 Solution Design — Real-Time Ad](_NTK-10006-real-time-adventure-tracking.md) | — | svc-notifications |
| [NTK-10008 — NTK-10008 Solution Design — Guest Review](_NTK-10008-guest-reviews-and-ratings.md) | — | svc-reservations |

---


## Problem Statement

svc-payments currently supports basic refund processing (POST /payments/{payment_id}/refund) but lacks structured dispute workflows. The capability gap (CAP-5.5 — partial) means:

1. **No dispute lifecycle** — chargebacks from payment processors have no internal tracking or resolution workflow
2. **No escalation tiers** — all refund requests are handled identically regardless of amount, reason, or complexity
3. **No automated notifications** — guests and operations staff receive no status updates during refund processing
4. **No audit trail** — refund decisions are not recorded with sufficient context for financial audit or regulatory review
5. **No policy enforcement** — cancellation and refund policies (e.g., 48-hour full refund, 24-hour 50% refund) are not codified in the system

## Solution Overview

Extend svc-payments with dispute management endpoints and a tiered refund workflow. The existing refund endpoint is preserved for backward compatibility; new endpoints add dispute tracking, policy evaluation, and escalation workflows.

### Key Design Decisions

1. **Extend svc-payments** rather than creating a new service — disputes are tightly coupled to payment data and refund processing
2. **Policy-driven refund evaluation** — refund eligibility and amounts computed from codified policies (YAML-driven) rather than manual agent decisions
3. **Three-tier escalation** — auto-approve (policy-eligible), agent review (edge cases), manager escalation (high-value or exceptions)
4. **Event-driven notifications** — dispute status changes emit events consumed by svc-notifications

### Architectural Pattern

```
Guest requests refund
       │
       ▼
  svc-payments
  (evaluate against refund policy)
       │
       ├─ Policy: AUTO-APPROVE → process refund immediately
       ├─ Policy: AGENT_REVIEW → create dispute, assign to agent queue
       └─ Policy: MANAGER_ESCALATION → create dispute, escalate
       │
       ▼
  Dispute Lifecycle
  (OPENED → UNDER_REVIEW → RESOLVED / ESCALATED → RESOLVED)
       │
       ├─ Each status change → emit dispute.status_changed event
       └─ Resolution → create refund (full/partial/denied) + notify guest
```

## Impacted Components

| Service | Change Type | Impact Level | Owner |
|---------|------------|-------------|-------|
| svc-payments | Enhanced — new endpoints + data model | PRIMARY | NovaTrek Platform Team |
| svc-reservations | Read integration | LOW | Booking Platform Team |
| svc-notifications | Event consumer | LOW | Various |
| svc-analytics | Event consumer | LOW | Various |

## Security Considerations

| Threat | Mitigation |
|--------|-----------|
| Refund fraud (duplicate requests) | Idempotency key on refund requests; one active dispute per payment |
| Unauthorized escalation | Role-based access — only AGENT and MANAGER roles can update disputes |
| Financial data exposure | Dispute details include payment amounts — standard bearer auth + audit logging |
| Policy manipulation | Refund policies stored as read-only YAML; changes require deployment (not runtime editable) |

## Prior Art

- **NTK-10004** (Schedule Overwrite Bug) — established PATCH semantics and optimistic locking patterns (ADR-010, ADR-011) reused for dispute updates
- **NTK-10002** (Adventure Category Classification) — established YAML-driven configuration pattern (ADR-004) reused for refund policy definitions
- **Existing svc-payments spec** — refund endpoint (POST /payments/{payment_id}/refund) preserved for backward compatibility

## Deployment Sequence

1. Database migration — add disputes table, refund_policy_evaluations table, new columns on refunds
2. Deploy refund policy YAML configuration
3. Deploy svc-payments v1.1.0 with new endpoints (feature-flagged)
4. Configure event bus topics (dispute.created, dispute.status_changed, dispute.resolved)
5. Deploy svc-notifications dispute notification templates
6. Enable feature flag for dispute workflows
7. Train guest services team on dispute queue

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | 2026-03-06 | Initial solution design |