# Single-Diagram Prompts for PUML Chunking Evaluation
#
# Category A: Each prompt targets a single diagram and tests whether
# Copilot can answer accurately without severing participant/interaction context.
#
# Usage: Paste each prompt into Copilot Chat (Agent Mode) and evaluate
# whether the answer is correct, partially correct, or wrong.
# Score: 1.0 = fully correct, 0.5 = partially correct, 0.0 = wrong/hallucinated

## A1 — Emergency Evacuation (NTK-10020)

### A1.1: Participant Count
**Prompt**: "How many participants are in the emergency evacuation sequence diagram? List all of them."
**Expected**: 14 participants (weather, safety, location, guides, transport, notify, profiles, checkin, reservations, payments, loyalty, analytics, kafka, db)
**Tests**: Whether chunking preserves all participant declarations

### A1.2: Nested Alt Depth
**Prompt**: "In the emergency evacuation diagram, what are the three weather alert levels and what happens for each?"
**Expected**: WATCH (enhanced monitoring), WARNING (pre-evacuation), EMERGENCY (full evacuation with transport dispatch)
**Tests**: Whether chunking preserves 3-level nested alt blocks

### A1.3: Saga Compensation
**Prompt**: "What compensating actions happen when the evacuation saga partially fails?"
**Expected**: Partial refund via svc-payments, loyalty credit via svc-loyalty-rewards, cancellation notification via svc-notifications
**Tests**: Whether chunking preserves compensation logic in else blocks

### A1.4: Kafka Fan-Out
**Prompt**: "Which services consume the evacuation.initiated Kafka event?"
**Expected**: svc-notifications, svc-analytics, svc-guide-management, svc-transport-logistics, svc-weather
**Tests**: Whether chunking preserves async arrow fan-out patterns

---

## A2 — Multi-Day Scheduling (NTK-10021)

### A2.1: Loop Structure
**Prompt**: "How does the multi-day scheduling diagram handle iteration across days?"
**Expected**: `loop for each day (day=1 to 3)` with nested weather alt (CLEAR/MARGINAL/SEVERE) and accommodation alt (HOTEL/CAMPSITE)
**Tests**: Whether chunking preserves loop + nested alt blocks

### A2.2: Cache Usage
**Prompt**: "What role does Redis play in multi-day adventure scheduling?"
**Expected**: Guide availability bitmap cache (BITCOUNT ops/guide-avail:{date}), used for fast availability checking with rotation policy enforcement
**Tests**: Whether chunking preserves non-standard participant types (Redis cache)

### A2.3: ADR References
**Prompt**: "Which architecture decision records are referenced in the multi-day scheduling diagram?"
**Expected**: ADR-010 (PATCH semantics), ADR-011 (optimistic locking)
**Tests**: Whether chunking preserves note blocks with ADR references

---

## A3 — Real-Time Tracking (NTK-10022)

### A3.1: Parallel Data Fetch
**Prompt**: "What data sources does the real-time tracking pipeline fetch in parallel?"
**Expected**: GPS Positions (svc-location-services), Weather (svc-weather), Trail Conditions (svc-trail-management), Guide Heartbeats (svc-guide-management), Safety Incidents (svc-safety-compliance)
**Tests**: Whether chunking preserves par block with 5 concurrent branches

### A3.2: Payload Schema
**Prompt**: "What fields are included in the GPS position payload from the tracking pipeline?"
**Expected**: wristband_id (UUID), lat, lng, altitude_m, speed_kmh, heading_deg, accuracy_m, timestamp_utc
**Tests**: Whether chunking preserves note blocks with detailed payload schemas

### A3.3: Stale Data Detection
**Prompt**: "How does the tracking pipeline handle stale GPS positions?"
**Expected**: Positions older than 60s are marked STALE; if stale > 5 min AND on high-difficulty trail, triggers safety check; logged to svc-analytics for device health monitoring
**Tests**: Whether chunking preserves alt block inside loop with conditional logic

---

## A4 — Loyalty Saga (NTK-10023)

### A4.1: Tier Multipliers
**Prompt**: "What are the loyalty tier multipliers in NovaTrek's rewards system?"
**Expected**: BRONZE=1.0x, SILVER=1.25x, GOLD=1.5x, PLATINUM=2.0x
**Tests**: Whether chunking preserves note blocks with structured data

### A4.2: Compensation Path
**Prompt**: "What happens to loyalty points when a payment fails during redemption?"
**Expected**: Points debit is reversed (COMPENSATION_REVERSAL entry in ledger), reservation discount is removed, guest is notified via push notification, earned points (1125) are NOT reversed
**Tests**: Whether chunking preserves else branch of alt with compensation saga

### A4.3: Idempotency
**Prompt**: "How does the loyalty service prevent duplicate point transactions?"
**Expected**: Idempotency key (TXN-{date}-{sequence}) checked against loyalty_transactions table; if exists, returns cached result; TTL 24 hours
**Tests**: Whether chunking preserves early-return logic

---

## A5 — Webhook Reconciliation (NTK-10024)

### A5.1: Retry Pattern
**Prompt**: "Describe the retry strategy for failed payment refunds in the webhook reconciliation flow."
**Expected**: 3 attempts with exponential backoff (2s, 4s delays), idempotency key per attempt, after 3 failures sends to dead letter queue
**Tests**: Whether chunking preserves nested retry alt blocks (3 levels deep)

### A5.2: Critical Section
**Prompt**: "What operations happen inside the critical section of the webhook processing flow?"
**Expected**: Capacity update with optimistic locking (PATCH trip capacity), conflict resolution via re-read + retry, reservation overflow analysis (FIFO by booking_date)
**Tests**: Whether chunking preserves critical/end blocks

### A5.3: Reconciliation Schedule
**Prompt**: "What does the nightly reconciliation batch job do?"
**Expected**: Finds webhooks in PROCESSING status older than 6 hours, reprocesses each (max 1 attempt), marks COMPLETED or FAILED, drains DLQ (retryable vs non-retryable), generates analytics report
**Tests**: Whether chunking preserves separated phase (== divider) with distinct logic

---

## A6 — Guest Profile Merge (NTK-10025)

### A6.1: Merge Phases
**Prompt**: "What are the three phases of the guest profile merge process?"
**Expected**: Phase 1 - Duplicate Detection (candidate scoring), Phase 2 - Merge Execution (saga across 7 services), Phase 3 - Post-Merge Notifications and Audit
**Tests**: Whether chunking preserves == Phase == dividers

### A6.2: Create/Destroy
**Prompt**: "What is the Rollback Snapshot in the guest profile merge and when is it destroyed?"
**Expected**: Created at start of Phase 2 to capture pre-merge state; contains both profiles, all FK references (reservations, check-ins, loyalty, payments, media); destroyed when saga completes; TTL 30 days for dispute resolution
**Tests**: Whether chunking preserves create/destroy lifecycle keywords

### A6.3: Group Block Count
**Prompt**: "How many group blocks are in the guest profile merge diagram and what are they?"
**Expected**: 7 groups — Step 2a (Update Primary Profile), 2b (Migrate Reservations), 2c (Migrate Check-ins), 2d (Merge Loyalty Accounts), 2e (Migrate Payment Records), 2f (Migrate Media Assets), 2g (Deactivate Secondary Profile)
**Tests**: Whether chunking preserves all 7 group/end block pairs
