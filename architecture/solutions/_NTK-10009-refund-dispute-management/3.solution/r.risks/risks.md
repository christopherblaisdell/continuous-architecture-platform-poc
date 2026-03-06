# Risks — NTK-10009

## R1: Refund Policy Misconfiguration

**Likelihood**: Low
**Impact**: High

**Description**: An error in the refund policy YAML (e.g., setting 100% refund for all tiers) could auto-approve all refund requests regardless of eligibility, resulting in financial loss.

**Mitigation**: Policy changes go through PR review with mandatory architect approval. Policy file includes validation schema. Automated tests verify policy logic for known scenarios. Auto-approve has a configurable maximum amount threshold as a safety net.

**Residual Risk**: Low — PR review and automated tests catch most errors.

## R2: Dispute Queue Backlog

**Likelihood**: Medium
**Impact**: Medium

**Description**: Seasonal surges (weather-related cancellations) could flood the agent review queue, delaying dispute resolution beyond acceptable SLA.

**Mitigation**: Weather-related disputes are auto-approved per policy (100% refund). Agent queue is monitored with alerting thresholds. Manager can temporarily raise auto-approve threshold to reduce queue pressure.

**Residual Risk**: Low — weather (the most common surge cause) is auto-approved.

## R3: Chargeback Response Window Deadline

**Likelihood**: Medium
**Impact**: High

**Description**: Payment processors impose strict response deadlines for chargeback disputes (typically 7-14 days). If svc-payments does not route chargebacks to the manager tier promptly, the response window may expire.

**Mitigation**: Chargebacks are auto-escalated to MANAGER tier on ingestion. Daily alert for unresolved chargebacks approaching deadline. Chargeback response deadline stored on dispute record.

**Residual Risk**: Medium — depends on timely chargeback webhook delivery from processor and manager response time.

## R4: Duplicate Dispute Submissions

**Likelihood**: Medium
**Impact**: Low

**Description**: A guest submits multiple dispute requests for the same payment, creating duplicate records.

**Mitigation**: Uniqueness constraint on (payment_id, status != CLOSED). Only one active dispute per payment allowed. Subsequent requests return the existing dispute.

**Residual Risk**: Low — database constraint enforces uniqueness.

## R5: Agent Authorization Boundary Violations

**Likelihood**: Low
**Impact**: Medium

**Description**: An agent approves a refund above their authority threshold, bypassing the manager escalation tier.

**Mitigation**: Tier assignment is policy-driven, not agent-selectable. Resolution endpoint validates that the resolver's role matches the required tier. Audit log captures all resolution actions.

**Residual Risk**: Low — system-enforced authorization boundaries.
