# Assumptions — NTK-10009

## A1: Reservation Includes Adventure Date and Cancellation Timestamp

**Assumption**: svc-reservations exposes the adventure date and a cancellation timestamp on the reservation object, enabling automated policy evaluation (e.g., "cancelled 48 hours before adventure date").

**Risk if invalid**: Policy engine cannot compute refund tier automatically; falls back to agent review for all requests.

**Mitigation**: If cancellation timestamp is missing, require agents to manually enter the cancellation date.

## A2: Refund Policies Are Stable Enough for YAML Configuration

**Assumption**: Refund policies (cancellation windows, refund percentages, exception rules) change infrequently (quarterly or less). YAML-driven configuration deployed via CI/CD is sufficient; runtime-editable policies are not required.

**Risk if invalid**: Frequent policy changes require deployments for each update.

**Mitigation**: If policies change frequently, migrate to a database-driven policy store with an admin UI (phase 2).

## A3: Payment Processor Supports Webhook for Chargebacks

**Assumption**: The external payment processor sends webhook notifications for chargebacks and disputes, enabling automatic dispute creation in svc-payments.

**Risk if invalid**: Chargebacks are discovered only during manual reconciliation, delaying response.

**Mitigation**: If webhooks are unavailable, implement a daily batch import from processor reports.

## A4: Three Escalation Tiers Are Sufficient

**Assumption**: Auto-approve, agent review, and manager escalation cover all dispute scenarios. No regulatory body or external arbitration tier is needed.

**Risk if invalid**: Some disputes require external mediation (e.g., credit card processor arbitration). These can be tracked as ESCALATED with an external reference.

## A5: Existing Refund Endpoint Consumers Are Tolerant of Additional Fields

**Assumption**: Adding new optional fields (dispute_id, policy_evaluation_id) to the Refund response schema does not break existing consumers, as they ignore unknown fields.

**Risk if invalid**: Tightly coupled consumers fail on schema changes.

**Mitigation**: New fields are nullable and optional. Existing consumers that use strict parsing will need a minor update.
