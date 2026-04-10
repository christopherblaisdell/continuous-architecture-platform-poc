# Structural Prompts for PUML Chunking Evaluation
#
# Category C: Tests whether Copilot can answer questions about PUML syntax
# structure (alt/else, loop, par, group, ref, critical, create/destroy)
# without confusing blocks from different hierarchy levels.
#
# Category D: Enricher validation prompts that test whether the enriched
# Markdown produced by puml-enricher.py is findable and accurate.
#
# Usage: Paste each prompt into Copilot Chat and evaluate accuracy.

## C1 — Nesting Depth

### C1.1: Deepest Nesting
**Prompt**: "Which test diagram has the deepest nesting of PlantUML control structures? Count the levels."
**Expected**: NTK-10024 has the deepest: loop → ref → alt → alt → alt (5 levels for the retry logic). NTK-10020 has 3-level nested alt (WATCH/WARNING/EMERGENCY). NTK-10021 has loop → alt → alt (3 levels).
**Tests**: Whether chunking preserves block nesting hierarchy

### C1.2: Control Structure Inventory
**Prompt**: "List all PlantUML control structures (alt, loop, par, group, ref, critical, opt, create, destroy) used across the test diagrams and which diagram uses each."
**Expected**:
- alt/else: NTK-10020, 10021, 10022, 10023, 10024, 10025
- loop: NTK-10021, 10022, 10024, 10025
- par: NTK-10022
- group: NTK-10023, 10025
- ref: NTK-10024
- critical: NTK-10024
- opt: NTK-10023
- create/destroy: NTK-10025
**Tests**: Whether retrieval correctly attributes structures to diagrams

---

## C2 — Phase/Divider Structure

### C2.1: Phase Dividers
**Prompt**: "Which diagrams use `== Phase ==` dividers and what are the phase names?"
**Expected**:
- NTK-10020: Detection, Evacuation Execution, Post-Incident
- NTK-10022: Dashboard Connection, Periodic Data Aggregation (every 30 seconds)
- NTK-10024: Webhook Reception, Async Processing Pipeline, Nightly Reconciliation (02:00 UTC)
- NTK-10025: Phase 1 - Duplicate Detection, Phase 2 - Merge Execution, Phase 3 - Post-Merge Notifications
**Tests**: Whether chunking preserves == divider == markers

### C2.2: Note Block Content
**Prompt**: "Find all note blocks in the test diagrams that mention specific data schemas or payload formats."
**Expected**: Must find GPS Payload Schema (NTK-10022), Webhook Payload (NTK-10024), Tier Multipliers (NTK-10023), Merge Candidate Analysis (NTK-10025), Aggregation Cycle details (NTK-10022)
**Tests**: Whether chunking preserves multi-line note blocks

---

## C3 — Arrow Type Differentiation

### C3.1: Sync vs Async
**Prompt**: "Which diagrams mix synchronous (solid) and asynchronous (dashed) arrows? Give examples of each."
**Expected**:
- NTK-10020: ->> for Kafka publish (async), -> for API calls (sync)
- NTK-10023: ->> for notify (fire-and-forget), -> for payments (sync with response)
- NTK-10024: ->> for Kafka publish and DLQ send, -> for API calls
- NTK-10025: ->> for analytics consume (async), -> for migration calls (sync)
**Tests**: Whether chunking preserves arrow type distinctions

---

## D1 — Enricher Output Validation

### D1.1: Service Discovery via Enrichment
**Prompt**: "Which NovaTrek services are involved in emergency evacuation?"
**Expected**: Answer should include svc-weather, svc-safety-compliance, svc-location-services, svc-guide-management, svc-transport-logistics, svc-notifications, svc-guest-profiles, svc-check-in, svc-reservations, svc-payments, svc-loyalty-rewards, svc-analytics
**Tests**: Whether enriched Markdown makes participant services discoverable via natural language

### D1.2: API Call Discovery
**Prompt**: "What API endpoints does svc-partner-integrations call?"
**Expected**: GET /trips (svc-trip-catalog), PATCH /trips/{id}/capacity (svc-trip-catalog), GET /reservations (svc-reservations), PATCH /reservations/{id} (svc-reservations), POST /refunds (svc-payments), POST /notifications (svc-notifications), POST /reports/partner-reconciliation (svc-analytics)
**Tests**: Whether enriched Markdown cross-references API calls with target services

### D1.3: ERD Entity Search
**Prompt**: "What tables are in the guest identity database?"
**Expected**: guests, guest_redirects, merge_audit_log, reservations, check_in_records, guest_points, points_ledger, payment_records, media_assets
**Tests**: Whether enriched ERD entities are discoverable via natural language
