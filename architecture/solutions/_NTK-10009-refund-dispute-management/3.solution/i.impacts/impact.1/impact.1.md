# Impact Assessment — svc-payments (ENHANCED)

| Field | Value |
|-------|-------|
| Service | svc-payments |
| Impact Level | PRIMARY |
| Change Type | Enhanced — new endpoints, data model additions, policy engine |
| Owner | NovaTrek Platform Team |

## Overview

svc-payments is extended with dispute lifecycle management, a refund policy evaluation engine, and escalation workflows. The existing refund endpoint is preserved for backward compatibility; new endpoints add dispute tracking and management.

## Data Model Changes

**New tables**:

| Table | Purpose |
|-------|---------|
| disputes | Dispute lifecycle records (status, tier, justification, resolution) |
| refund_policy_evaluations | Audit trail of policy evaluations per refund request |

**New columns on existing refunds table**:

| Column | Type | Description |
|--------|------|-------------|
| dispute_id | UUID, nullable | Reference to associated dispute (if any) |
| policy_evaluation_id | UUID, nullable | Reference to the policy evaluation that determined this refund |

**disputes table schema**:

- `id` (UUID, PK)
- `payment_id` (UUID, FK to payments)
- `reservation_id` (UUID, cross-ref svc-reservations)
- `guest_id` (UUID, cross-ref svc-guest-profiles)
- `type` (ENUM: CANCELLATION, SERVICE_COMPLAINT, WEATHER, CHARGEBACK, OTHER)
- `status` (ENUM: OPENED, UNDER_REVIEW, ESCALATED, RESOLVED, CLOSED)
- `tier` (ENUM: AUTO, AGENT, MANAGER)
- `amount_requested` (DECIMAL)
- `amount_approved` (DECIMAL, nullable)
- `resolution` (ENUM: FULL_REFUND, PARTIAL_REFUND, DENIED, nullable)
- `justification` (TEXT — structured reason for the resolution)
- `assigned_to` (VARCHAR — agent or manager handling the dispute)
- `escalated_from` (UUID, nullable — previous dispute if escalated)
- `_rev` (INTEGER, optimistic locking)
- `created_at`, `updated_at`, `resolved_at` (TIMESTAMPTZ)

**Indexes**:

- `(status, tier, created_at)` — agent/manager queue queries
- `(payment_id)` — lookup disputes by payment
- `(guest_id, status)` — guest dispute history
- `(assigned_to, status)` — agent workload queries

## New API Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| POST | /disputes | Create a refund dispute |
| GET | /disputes | List disputes (filtered by status, tier, assigned_to) |
| GET | /disputes/{dispute_id} | Get dispute details |
| PATCH | /disputes/{dispute_id} | Update dispute (assign, escalate, add notes) |
| POST | /disputes/{dispute_id}/resolve | Resolve a dispute (approve/deny with justification) |
| GET | /disputes/queue | Agent/manager queue view |
| POST | /chargebacks | Ingest processor chargeback notification |
| POST | /refund-policy/evaluate | Evaluate refund eligibility against policy (dry-run) |

## Refund Policy Configuration

**File**: `config/refund-policies.yaml` deployed with svc-payments.

**Structure**:

```yaml
policies:
  cancellation:
    tiers:
      - window_hours: 48
        refund_percentage: 100
        tier: AUTO
      - window_hours: 24
        refund_percentage: 50
        tier: AUTO
      - window_hours: 0
        refund_percentage: 0
        tier: AGENT
  weather:
    refund_percentage: 100
    tier: AUTO
    requires_verification: true
  service_complaint:
    tier: AGENT
  chargeback:
    tier: MANAGER

escalation:
  auto_approve_max_amount: 500.00
  agent_max_amount: 2000.00
  manager_threshold: 2000.01
```

## Cross-Service Dependencies

| Dependency | Purpose | Call Pattern |
|-----------|---------|-------------|
| svc-reservations | Look up reservation dates for policy evaluation | Synchronous GET on dispute creation |
| svc-notifications | Guest notifications on dispute status changes | Event-driven (dispute.status_changed) |
| svc-analytics | Dispute metrics and trends | Event-driven (dispute.resolved) |

## Events Produced

| Event | Trigger | Consumers |
|-------|---------|-----------|
| dispute.created | New dispute opened | svc-notifications |
| dispute.status_changed | Any status transition | svc-notifications |
| dispute.resolved | Dispute resolved (approved/denied) | svc-notifications, svc-analytics |
| dispute.escalated | Dispute escalated to higher tier | svc-notifications |

## Backward Compatibility

- Existing POST /payments/{payment_id}/refund endpoint is PRESERVED unchanged
- Direct refunds (without dispute) continue to work as before
- New nullable fields on Refund response (dispute_id, policy_evaluation_id) are backward-compatible — existing consumers ignore unknown fields
- svc-payments version bumps from 1.0.0 to 1.1.0 (minor, non-breaking)

## Deployment Notes

- Database migration: create disputes + refund_policy_evaluations tables, add nullable columns to refunds
- Deploy refund-policies.yaml configuration
- Deploy svc-payments v1.1.0 with dispute endpoints feature-flagged
- Configure event bus topics
- Deploy notification templates for dispute status emails
- Enable feature flag after agent training
