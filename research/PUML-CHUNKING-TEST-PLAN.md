# PlantUML Chunking End-to-End Test Plan

**Date:** 2026-04-10
**Status:** Plan
**Purpose:** Validate that Copilot's native chunking, the `puml-enricher.py` pipeline, and companion Markdown generation correctly preserve the semantic integrity of PlantUML diagrams across all complexity dimensions.

---

## Background

PlantUML has no Tree-sitter grammar in any AI coding platform. Copilot falls back to a 60-line `FixedWindowJaccardMatcher` sliding window with Jaccard similarity scoring. This destroys the structural relationships between participants (declared at the top) and their interactions (defined 60-120+ lines later). See [PlantUML Chunking Strategy](../../sites/ai-evaluation-2/docs/evidence/puml-chunking-strategy.md) and [Deep Research Results](../../sites/ai-evaluation-2/docs/research/deep-research-results-plantuml-chunking.md) for full analysis.

The workspace currently has 37 PUML files across 6 categories (Sequence, Component, System, Ticket, Endpoint, Event Flow). The longest is 133 lines (svc-payments--post-payments.puml). This is insufficient to stress-test the chunking boundaries comprehensively.

---

## Test Strategy

### What We Are Testing

1. **Copilot native chunking** -- Can `@workspace` queries accurately answer questions about PUML diagrams that span >60 lines, >120 lines, and >200 lines?
2. **puml-enricher.py output** -- Does the enricher correctly extract participants, relationships, control flow, and domain metadata from each diagram type?
3. **Companion Markdown generation** -- Can Copilot accurately answer the same questions using the enriched Markdown that it could not answer from raw PUML?
4. **Cross-file context** -- Can Copilot connect information across multiple PUML files (e.g., "which services participate in both check-in and scheduling")?
5. **!include resolution** -- Does Copilot understand theme.puml, include.puml, and templates.puml macros when they are included?

### Complexity Dimensions to Cover

| Dimension | Description | Chunking Risk |
|-----------|-------------|---------------|
| **File length** | Short (<60 lines), medium (60-120), long (120-200), very long (>200) | 60-line window misses participants or interactions |
| **Participant count** | Few (3-4), moderate (6-8), many (10+) | More participants = more declaration lines before interactions begin |
| **Nested alt/else depth** | Shallow (1 level), moderate (2 levels), deep (3+ levels) | Nested blocks span many lines; the `else` can be 80+ lines from the `alt` |
| **Loop + alt combination** | Loops containing alt blocks, or alts inside loops | The chunker splits the loop from its alt children |
| **Group/box compartments** | PlantUML `box` and `group` blocks around sections | Group boundaries severed from their contents |
| **Kafka event fan-out** | One event published, multiple consumers | Consumer reactions are far from the publish statement |
| **Multi-phase flows** | Diagrams with == phase dividers == spanning 3+ business phases | Each phase may land in a different chunk |
| **Cross-service callback chains** | Service A calls B, which async calls C, which callbacks to A | The callback is physically far from the initiating call |
| **C4 macros with !include** | Component diagrams using Container(), Rel(), Boundary() | Macros are opaque without include resolution |
| **Compensating transactions (saga)** | Happy path followed by multi-step rollback | Rollback steps are far from the triggering failure |
| **Database + cache + queue participants** | Mixed participant types (database, queue, participant) | Type semantics lost when declarations are in a different chunk |
| **Notes and annotations** | Extensive `note right`, `note over` blocks with payload details | Multi-line notes easily truncated |

---

## Phase 1: Create Test Diagrams via NovaTrek Tickets

Each ticket below maps to a specific chunking complexity dimension. When solved, each ticket will produce one or more PUML sequence diagrams that stress-test the identified weakness.

### Ticket 1: NTK-10020 -- Emergency Evacuation Orchestration Flow

**Complexity targets:** Very long (200+ lines), 12+ participants, deep nested alt/else (3 levels), multi-phase flow, compensating transactions, Kafka fan-out to 5+ consumers

**Ticket description:**
Design an emergency evacuation flow for when a severe weather alert or safety incident requires evacuating guests from an active trail. The flow involves: (1) weather/safety trigger detection, (2) guest location resolution via GPS, (3) guide notification and acknowledgment, (4) transport vehicle dispatch, (5) medical team standby, (6) guest notification via push/SMS, (7) reservation cancellation and refund processing, (8) incident logging and compliance reporting. If any critical step fails (guide unreachable, transport unavailable), the system must escalate to manual dispatch with fallback procedures.

**Expected PUML characteristics:**
- Participants: svc-weather, svc-safety-compliance, svc-location-services, svc-guide-management, svc-transport-logistics, svc-notifications, svc-guest-profiles, svc-reservations, svc-payments, svc-analytics, svc-check-in, Kafka, PostgreSQL
- 3 business phases: Detection, Evacuation Execution, Post-Incident
- Nested alt: weather severity (WATCH vs WARNING vs EMERGENCY), each with different escalation paths
- Saga pattern: reservation cancellation -> payment refund -> loyalty points restoration (with rollback if refund fails)
- Kafka fan-out: incident.declared event consumed by 5+ services
- Notes: payload details for GPS coordinates, estimated evacuation time, incident severity classification

**Chunking stress points:**
- Participant declarations (lines 1-30) completely severed from first interaction (line 40+)
- The EMERGENCY alt branch starts at ~line 80, its compensating transaction at ~line 180
- Kafka fan-out consumers are 50+ lines from the publish statement

---

### Ticket 2: NTK-10021 -- Multi-Day Trip Scheduling with Accommodation Handoffs

**Complexity targets:** Long (150+ lines), 10 participants, loop + alt combination, cross-service callback chain, multi-phase flow (day-by-day), database + cache interactions

**Ticket description:**
Design the scheduling flow for multi-day adventure packages (e.g., 3-day Rockies expedition). Each day requires: guide assignment, trail condition check, weather verification, accommodation booking handoff (hotel partner or campsite), gear swap for different terrain, and meal plan coordination. The orchestrator must handle day-over-day dependencies (Day 2 trail depends on Day 1 weather outcome), guide rotation policies (no guide works >2 consecutive high-difficulty days), and accommodation overbooking fallback.

**Expected PUML characteristics:**
- Loop block: `loop for each day in expedition`
- Inside loop: alt for weather (proceed / reroute / cancel-day), alt for accommodation (confirmed / overbooked / fallback)
- Cross-service callbacks: svc-scheduling-orchestrator requests accommodation from partner, partner async confirms via webhook, orchestrator resumes
- Database: schedule draft saved after each day's planning, with version/revision for optimistic locking
- Cache: Redis for guide availability bitmap (checked inside loop)
- == Day 1 Planning ==, == Day 2 Planning ==, == Finalization == phase dividers

**Chunking stress points:**
- The loop body spans 80+ lines; the loop keyword and its end are in different chunks
- Alt blocks inside the loop create 3-level nesting (loop > alt weather > alt accommodation)
- Callback from partner service is 40+ lines from the outgoing request

---

### Ticket 3: NTK-10022 -- Real-Time Adventure Tracking Dashboard Data Pipeline

**Complexity targets:** Long (140+ lines), 10+ participants, parallel processing (par block), mixed participant types (database, queue, WebSocket, cache, external API), extensive notes

**Ticket description:**
Design the real-time data pipeline feeding the Operations Dashboard. Every 30 seconds, the system aggregates: GPS positions from wristbands via svc-location-services, weather updates from svc-weather, trail condition changes from svc-trail-management, guide check-in heartbeats from svc-guide-management, and guest safety status from svc-safety-compliance. The pipeline must: merge data streams, compute aggregate metrics (guests per trail, safety incidents active, guides en route), push updates via WebSocket to the ops dashboard, and cache the latest snapshot in Redis for new dashboard connections.

**Expected PUML characteristics:**
- `par` (parallel) block with 5 concurrent data fetches
- WebSocket participant for dashboard push
- Redis cache participant for snapshot storage
- External API participant for weather data provider
- Extensive notes documenting payload schemas at each aggregation step
- Group block: "Data Aggregation Pipeline"
- Alt: stale data detection (if GPS timestamp > 60s old, mark as STALE)

**Chunking stress points:**
- The `par` block spans 40+ lines with 5 parallel branches
- WebSocket push is 60+ lines after the participant declaration
- Notes with payload schemas are 5-10 lines each, easily truncated
- Mixed participant types (database, queue, participant, boundary) confuse embedding models

---

### Ticket 4: NTK-10023 -- Loyalty Points Multi-Source Earning and Redemption Saga

**Complexity targets:** Medium-long (130+ lines), 8 participants, compensating transaction (full saga), nested opt blocks, cross-service validation chain, idempotency handling

**Ticket description:**
Design the loyalty points lifecycle for a single guest transaction. Points can be earned from: completed adventures, partner referrals, and promotional campaigns. Points can be redeemed for: trip discounts, gear upgrades, and partner vouchers. The flow must handle: concurrent earning + redemption in one transaction, insufficient points with partial redemption, expired points pruning, and fraud detection (suspicious earning patterns). If payment fails after points are deducted, the full points balance must be restored atomically.

**Expected PUML characteristics:**
- Saga: earn points -> apply discount -> process payment -> (on failure) restore points + cancel discount + notify guest
- `opt` blocks: optional promotional bonus, optional partner referral credit
- Idempotency: check if transaction already processed (prevents double-earning)
- Cross-service validation: svc-loyalty-rewards -> svc-guest-profiles (tier validation) -> svc-payments (fraud check) -> svc-reservations (apply discount)
- Database: points ledger with debit/credit entries (similar to payment ledger pattern)

**Chunking stress points:**
- The saga happy path ends at ~line 70; the compensating transaction starts at ~line 90 and references entities from line 20
- Opt blocks are easily confused with alt blocks by the chunker
- The idempotency check at the top is in a different chunk from the ledger write at the bottom

---

### Ticket 5: NTK-10024 -- Partner Integration Webhook Reconciliation Flow

**Complexity targets:** Long (160+ lines), 9 participants, ref blocks (diagram decomposition), critical section, retry with exponential backoff, mixed sync/async arrows, extensive annotations

**Ticket description:**
Design the reconciliation flow when partner booking webhooks arrive out of order or fail. Partners send booking confirmations, modifications, and cancellations via webhooks. The system must: (1) sequence webhooks by event timestamp (not arrival time), (2) detect and resolve conflicts (modification arrives before confirmation), (3) retry failed downstream updates with exponential backoff, (4) reconcile payment discrepancies between partner-reported and NovaTrek-calculated amounts, and (5) generate a daily reconciliation report. Include the dead-letter queue pattern for permanently failed events.

**Expected PUML characteristics:**
- `ref` block referencing the partner-booking-flow.puml diagram
- `critical` section for payment reconciliation (must not be interrupted)
- Retry loop with exponential backoff (loop with delay annotation)
- Mixed arrows: -> (sync), ->> (async response), --> (return), -[#red]> (error path)
- Dead-letter queue participant
- Daily batch reconciliation section (separate from real-time flow)
- Extensive annotations: webhook payload examples, conflict resolution rules, backoff timing

**Chunking stress points:**
- `ref` blocks are opaque to the chunker (it doesn't follow references)
- The `critical` section is a rarely used PlantUML construct; chunker may split it
- Retry loop with backoff spans 25+ lines; the backoff annotation is far from the loop keyword
- Mixed arrow types in dense sections create embedding noise
- The batch reconciliation section is a completely different operational mode but in the same file

---

### Ticket 6: NTK-10025 -- Guest Profile Merge and Data Migration Flow

**Complexity targets:** Very long (180+ lines), 11 participants, complex C4 component diagram companion, group blocks, destroy keyword, create keyword, multi-database interactions

**Ticket description:**
Design the flow for merging duplicate guest profiles discovered by the identity resolution engine. When svc-guest-profiles detects two profiles belonging to the same person (matching email + phone + name), it must: (1) designate primary and secondary profiles, (2) migrate reservations, loyalty points, waivers, check-in history, and payment methods from secondary to primary, (3) update all downstream service references, (4) tombstone the secondary profile (soft delete with redirect pointer), (5) notify the guest of the merge, and (6) generate an audit trail. If any migration step fails, the entire merge must be rolled back.

**Expected PUML characteristics:**
- `create` keyword for new merged profile entity
- `destroy` keyword for tombstoned secondary profile
- Group blocks: "Phase 1: Data Migration", "Phase 2: Reference Updates", "Phase 3: Cleanup"
- Multiple database participants: guest-profiles-db, reservations-db, loyalty-db, safety-db
- Cross-service fan-out: 6 services must update their foreign key references
- Audit trail: every step logged to svc-analytics with before/after state
- Full saga rollback: if loyalty points migration fails, undo reservation migration + restore secondary profile

**Chunking stress points:**
- `create` and `destroy` are uncommon PlantUML keywords; the chunker treats them as generic text
- Multiple database participants with similar names (all are "database" type) confuse embeddings
- The saga spans the entire file: rollback at line 170 must reference the initial state at line 25
- Group blocks are split across chunks, losing the phase boundary context

---

## Phase 2: Companion Component and C4 Diagrams

Each ticket above should also produce at least one companion diagram to test cross-diagram chunking:

| Ticket | Companion Diagram | Type | Chunking Test |
|--------|-------------------|------|---------------|
| NTK-10020 | Emergency response domain components | C4 Component | `!include` resolution, Container/Rel macros |
| NTK-10021 | Multi-day scheduling state machine | Activity diagram | Decision nodes spanning >60 lines |
| NTK-10022 | Real-time data pipeline topology | C4 Container | System boundary nesting, external API nodes |
| NTK-10024 | Webhook processing internal components | C4 Component | Detailed component decomposition (15+ components) |
| NTK-10025 | Guest identity data model | Entity relationship | 10+ entities with many-to-many relationships |

---

## Phase 3: Test Prompts

Each prompt below is designed to test a specific chunking failure mode. They should be executed against `@workspace` with ONLY the raw PUML files (no enricher output) first, then repeated after enricher processing to measure improvement.

### Category A: Single-Diagram Retrieval (Tests 60-line window boundary)

| ID | Prompt | Target Diagram | Expected Answer | Chunking Risk |
|----|--------|---------------|-----------------|---------------|
| A1 | "Which services does svc-weather notify during an emergency evacuation?" | NTK-10020 | svc-safety-compliance, svc-guide-management, svc-transport-logistics, svc-notifications | Weather participant declared at line ~8; its interactions start at line ~45 |
| A2 | "What happens if the payment refund fails during an emergency evacuation?" | NTK-10020 | Loyalty points restoration is skipped, incident is flagged for manual resolution, guest is notified of pending refund | Refund failure is in the compensating transaction at line ~180, 150+ lines from the trigger |
| A3 | "How does the scheduling orchestrator handle guide rotation across multi-day trips?" | NTK-10021 | No guide works >2 consecutive high-difficulty days; system checks guide history inside the day loop | Rotation logic inside a loop > alt nesting, physically far from the loop declaration |
| A4 | "What data is pushed to the ops dashboard via WebSocket?" | NTK-10022 | Aggregated GPS positions, weather updates, trail conditions, guide heartbeats, safety status, computed metrics | WebSocket push is 60+ lines after participant declaration and data aggregation |
| A5 | "If a guest's loyalty points are deducted but the payment fails, what happens?" | NTK-10023 | Points are restored, discount is cancelled, guest is notified -- full saga rollback | Saga rollback is 20+ lines after the failure point, 60+ lines after the earning |
| A6 | "What is the exponential backoff strategy for failed partner webhooks?" | NTK-10024 | Retry with increasing delays (1s, 2s, 4s, 8s, 16s), then move to dead-letter queue after 5 failures | Backoff details are in annotations far from the retry loop keyword |
| A7 | "In what order does the guest profile merge update downstream services?" | NTK-10025 | Reservations first, then loyalty points, then waivers, then check-in history, then payment methods, then notifications | The order is defined by the Group blocks; if chunked incorrectly, the order is lost |

### Category B: Cross-Diagram Queries (Tests multi-file context assembly)

| ID | Prompt | Target Diagrams | Expected Answer | Chunking Risk |
|----|--------|----------------|-----------------|---------------|
| B1 | "Which services participate in both the emergency evacuation flow AND the check-in process?" | NTK-10020 + check-in-process-flow | svc-safety-compliance, svc-gear-inventory (if gear evacuation), svc-guide-management, svc-notifications, Kafka | Must retrieve and cross-reference two different PUML files |
| B2 | "Compare how svc-payments handles payment failure in the reservation booking flow vs. the evacuation refund flow" | reservation-booking-flow + NTK-10020 | In booking: gear hold released, error returned. In evacuation: saga rollback, loyalty points restored, incident logged | Must retrieve compensating transaction sections from two files |
| B3 | "Which Kafka events does svc-analytics consume across all diagrams?" | All diagrams with Kafka | List of all events consumed by analytics across all flows | Must scan every PUML file for analytics as a Kafka consumer |
| B4 | "How does the scheduling orchestrator interact differently with svc-trail-management in single-day vs. multi-day trips?" | scheduling-orchestration-flow + NTK-10021 | Single-day: one-time trail condition check. Multi-day: per-day check inside loop with day dependency | Must compare loop vs. non-loop interaction patterns |

### Category C: Structural Understanding (Tests whether the model understands PUML syntax)

| ID | Prompt | Target Diagram | Expected Answer | Chunking Risk |
|----|--------|---------------|-----------------|---------------|
| C1 | "Draw me a text-based adjacency list of all service-to-service calls in the emergency evacuation flow" | NTK-10020 | Directed list of all -> and ->> arrows with labels | Model must parse arrow syntax correctly, not just find keywords |
| C2 | "Which calls in the partner webhook reconciliation are synchronous vs. asynchronous?" | NTK-10024 | List of -> (sync) and ->> (async) calls separately | Mixed arrow types are dense and confuse embeddings |
| C3 | "What are the three possible outcomes of the fraud detection step in the payment flow?" | svc-payments--post-payments | APPROVED (score <30), REVIEW (30-70), DECLINED (>70) | Three-way alt block with different response codes |
| C4 | "List all database tables referenced in the guest profile merge flow" | NTK-10025 | Tables from guest-profiles-db, reservations-db, loyalty-db, safety-db | Multiple database participants with INSERT/SELECT/UPDATE statements |

### Category D: Enricher Validation (Tests puml-enricher.py output quality)

| ID | Test | Method | Pass Criteria |
|----|------|--------|---------------|
| D1 | Run enricher on NTK-10020 diagram | `python3 scripts/puml-enricher.py --file [path]` | Output contains all 12+ participants, all Kafka events, all alt branches |
| D2 | Run enricher on NTK-10022 diagram | `python3 scripts/puml-enricher.py --file [path]` | Output contains par block contents as parallel data sources (not sequential) |
| D3 | Run enricher on NTK-10024 diagram | `python3 scripts/puml-enricher.py --file [path]` | Output contains ref block reference, critical section, retry pattern |
| D4 | Run enricher on NTK-10025 diagram | `python3 scripts/puml-enricher.py --file [path]` | Output contains create/destroy semantics, multi-database interactions, saga rollback |
| D5 | Run enricher on ALL test diagrams | `python3 scripts/puml-enricher.py` | Zero errors, all files produce output, all diagram types classified correctly |

---

## Phase 4: Automated Regression Harness

After manual testing, create a lightweight script that:

1. Takes a PUML file path and a question as input
2. Runs `puml-enricher.py` on the file
3. Compares the enriched output against expected extraction results (participants, relationships, events)
4. Reports pass/fail with specific missing elements

This is NOT an AI quality test (which would require subjective evaluation) -- it tests the enricher's structural extraction accuracy.

### Expected file structure:

```
tests/
  puml-chunking/
    fixtures/
      NTK-10020-emergency-evacuation.puml
      NTK-10021-multiday-scheduling.puml
      NTK-10022-realtime-tracking-pipeline.puml
      NTK-10023-loyalty-saga.puml
      NTK-10024-webhook-reconciliation.puml
      NTK-10025-guest-profile-merge.puml
    expected/
      NTK-10020-expected.yaml     (participants, relationships, events, alt-branches)
      NTK-10021-expected.yaml
      NTK-10022-expected.yaml
      NTK-10023-expected.yaml
      NTK-10024-expected.yaml
      NTK-10025-expected.yaml
    prompts/
      single-diagram-prompts.md   (Category A prompts with expected answers)
      cross-diagram-prompts.md    (Category B prompts with expected answers)
      structural-prompts.md       (Category C prompts with expected answers)
    test_enricher_extraction.py   (automated enricher validation)
    README.md                     (how to run)
```

---

## Implementation Sequence

| Step | Action | Depends On |
|------|--------|-----------|
| 1 | Register tickets NTK-10020 through NTK-10025 in tickets.yaml | -- |
| 2 | Create NTK-10020 emergency evacuation sequence diagram (200+ lines) | Step 1 |
| 3 | Create NTK-10021 multi-day scheduling sequence diagram (150+ lines) | Step 1 |
| 4 | Create NTK-10022 real-time tracking pipeline sequence diagram (140+ lines) | Step 1 |
| 5 | Create NTK-10023 loyalty saga sequence diagram (130+ lines) | Step 1 |
| 6 | Create NTK-10024 webhook reconciliation sequence diagram (160+ lines) | Step 1 |
| 7 | Create NTK-10025 guest profile merge sequence diagram (180+ lines) | Step 1 |
| 8 | Create companion C4/component diagrams for NTK-10020, 10022, 10024, 10025 | Steps 2-7 |
| 9 | Create test fixtures directory and expected extraction YAML files | Steps 2-7 |
| 10 | Create prompt files (Categories A-D) with expected answers | Steps 2-7 |
| 11 | Create test_enricher_extraction.py automated validation script | Steps 9 |
| 12 | Run enricher on all test diagrams, validate output | Steps 2-7, 11 |
| 13 | Execute Category A prompts against raw PUML (baseline) | Steps 2-7, 10 |
| 14 | Execute Category A prompts against enriched Markdown (comparison) | Step 12, 13 |
| 15 | Document results and chunking quality improvements | Steps 13-14 |

---

## Success Criteria

| Metric | Baseline (Raw PUML) | Target (Enriched) |
|--------|---------------------|--------------------|
| Category A prompts answered correctly | Expect <50% (60-line window kills context) | >90% |
| Category B cross-diagram prompts answered correctly | Expect <30% (multi-file assembly is hard) | >75% |
| Category C structural understanding prompts | Expect ~60% (lexical match helps) | >85% |
| Enricher extraction accuracy (Category D) | N/A | 100% (all participants, relationships, events extracted) |
| Enricher processes all 6 test diagrams without error | N/A | 100% |
