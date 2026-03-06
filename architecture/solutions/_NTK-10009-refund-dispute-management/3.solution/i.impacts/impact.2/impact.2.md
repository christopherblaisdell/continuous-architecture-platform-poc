# Impact Assessment — svc-notifications

| Field | Value |
|-------|-------|
| Service | svc-notifications |
| Impact Level | LOW |
| Change Type | Event consumer — new notification templates |
| Owner | Various |

## Overview

svc-notifications subscribes to dispute lifecycle events and sends email notifications to guests at each status change. No API contract changes to svc-notifications itself — only new event subscriptions and email templates.

## Changes Required

1. **New event subscriptions**: dispute.created, dispute.status_changed, dispute.resolved, dispute.escalated
2. **New email templates**:
   - Dispute received confirmation (dispute.created)
   - Dispute under review (dispute.status_changed to UNDER_REVIEW)
   - Dispute escalated (dispute.escalated)
   - Dispute resolved — refund approved (dispute.resolved with FULL_REFUND or PARTIAL_REFUND)
   - Dispute resolved — refund denied (dispute.resolved with DENIED)
3. **Template data**: Templates consume dispute fields (dispute_id, amount_requested, amount_approved, resolution, justification)

## Deployment Notes

- Deploy new templates BEFORE enabling dispute feature flag on svc-payments
- Templates use existing svc-notifications template engine — no infrastructure changes
