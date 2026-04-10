# Cross-Diagram Prompts for PUML Chunking Evaluation
#
# Category B: Each prompt requires synthesizing information from multiple
# diagrams. Tests whether Copilot's retrieval (RAG) can locate and combine
# relevant chunks across different PUML files.
#
# Usage: Paste each prompt into Copilot Chat and evaluate accuracy.
# Score: 1.0 = fully correct, 0.5 = partially correct, 0.0 = wrong/hallucinated

## B1 — Cross-Service Participant Matching

### B1.1: Kafka Usage Across Diagrams
**Prompt**: "Which test diagrams use Kafka, and what events does each diagram publish?"
**Expected**:
- NTK-10020: evacuation.initiated, evacuation.completed/failed, incident.logged
- NTK-10021: schedule.day.completed, schedule.finalized
- NTK-10022: dashboard.update
- NTK-10023: loyalty.transaction.completed
- NTK-10024: partner.webhook.received, partner.webhook.completed
- NTK-10025: guest.profile.merged
**Tests**: Whether retrieval finds Kafka interactions across all 6 diagrams

### B1.2: svc-notifications Callers
**Prompt**: "Which diagrams call svc-notifications and what type of notification does each send?"
**Expected**:
- NTK-10020: emergency evacuation alerts (multi-channel: SMS, push, email)
- NTK-10021: itinerary confirmation to guests
- NTK-10023: loyalty payment failed notification
- NTK-10024: reservation waitlisted notification, ops alert for non-retryable errors
- NTK-10025: profile merge completion to guest, ops confirmation to agent
**Tests**: Whether retrieval correlates a service across diagrams

### B1.3: Database Participants
**Prompt**: "List all diagrams that include PostgreSQL database participants and summarize what each stores."
**Expected**:
- NTK-10020: evacuation records, incident audit trail
- NTK-10021: schedule records, day assignments with optimistic locking
- NTK-10022: tracking_metrics (cycle snapshots, historical data)
- NTK-10023: loyalty_transactions (idempotency), points_ledger, guest_points
- NTK-10024: processed_webhooks (idempotency, reconciliation status)
- NTK-10025: guests, guest_redirects, merge_audit_log (profiles-db); reservations (reservations-db); guest_points, points_ledger (loyalty-db)
**Tests**: Whether retrieval finds database interactions in all diagrams

---

## B2 — Architectural Pattern Recognition

### B2.1: Saga Patterns
**Prompt**: "Which diagrams implement the saga pattern? Compare their compensation strategies."
**Expected**:
- NTK-10020: Multi-service compensation (refund + loyalty credit + notification)
- NTK-10023: Points reversal after payment failure (restore debit, cancel discount, notify)
- NTK-10025: Rollback snapshot with create/destroy lifecycle, multi-service undo across 7 services
**Tests**: Whether retrieval identifies saga-shaped flows across diagrams

### B2.2: Idempotency Patterns
**Prompt**: "Which diagrams implement idempotency checks and how?"
**Expected**:
- NTK-10023: idempotency_key (TXN-{date}-{sequence}) in loyalty_transactions table, 24h TTL
- NTK-10024: webhook_id deduplication in processed_webhooks table; refund idempotency_key RF-{id}-WH-{id}
**Tests**: Whether retrieval finds idempotency patterns in different forms

### B2.3: Optimistic Locking
**Prompt**: "Where is optimistic locking used across the test diagrams?"
**Expected**:
- NTK-10021: _rev field on daily schedule, ADR-011
- NTK-10024: _rev on trip capacity update (409 Conflict + re-read + retry)
- NTK-10025: _rev=42 on guest profile update during merge
**Tests**: Whether retrieval finds _rev/version patterns

---

## B3 — Sequence vs C4/ERD Cross-Reference

### B3.1: Emergency Response Mapping
**Prompt**: "Compare the emergency evacuation sequence diagram with the emergency response component diagram. Which sequence diagram services map to which C4 components?"
**Expected**: Sequence participants (weather, safety, location, guides, transport, notify) map to external services in C4; the orchestration logic maps to evac_controller → evac_engine → evac_coordinator → compensation_handler internal pipeline
**Tests**: Whether retrieval connects sequence participants to C4 components

### B3.2: Guest Profile ERD Validation
**Prompt**: "Does the guest identity ERD match the database operations in the guest profile merge sequence diagram? Identify any discrepancies."
**Expected**: ERD defines 8 entities that correspond to all database operations in the sequence; check_in_records entity matches CI- migrations; merged_from array, merged_into, guest_redirects table, merge_audit_log all appear in both
**Tests**: Whether retrieval cross-references ERD entities with sequence DB operations

### B3.3: Tracking Pipeline Architecture
**Prompt**: "How does the real-time pipeline topology diagram relate to the tracking sequence diagram? Which C4 containers correspond to which sequence participants?"
**Expected**: C4 tracking_svc = sequence tracking; C4 ws_gateway = sequence ws; C4 redis = sequence cache; C4 data sources (location_svc, weather_svc, etc.) = sequence par block participants; C4 ext_weather = sequence extweather
**Tests**: Whether retrieval maps C4 containers to sequence aliases
