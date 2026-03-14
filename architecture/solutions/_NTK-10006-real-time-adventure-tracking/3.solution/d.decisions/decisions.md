<!-- PUBLISH -->
# NTK-10006 Architecture Decisions

## ADR-012: Two New Services for Tracking and Emergency Response

### Status

Proposed

### Date

2026-03-14

### Context and Problem Statement

NTK-10006 requires real-time GPS tracking of guests on active adventures and automated emergency alerting with rescue dispatch. This functionality does not exist in any current service. The system must ingest high-frequency GPS position updates (estimated 50,000/day at peak), evaluate geofences, detect emergencies, and coordinate rescue responses. Where should this functionality live?

### Decision Drivers

- **Separation of concerns** — tracking (high-frequency data ingestion) and emergency response (low-frequency, high-criticality workflow) have fundamentally different performance and reliability profiles
- **Data ownership** — the NovaTrek architecture mandates that each service owns its data exclusively; mixing tracking data with emergency records in a single service creates ownership ambiguity
- **Scaling independence** — GPS position ingestion must scale horizontally with guest count; emergency response must prioritize reliability over throughput
- **Domain alignment** — tracking is an operational concern (Operations domain); emergency response is a safety concern (Safety domain)
- **Existing infrastructure** — svc-emergency-response already has a data store schema and AsyncAPI event spec defined in the metadata; svc-adventure-tracking is entirely new

### Considered Options

**Option A: Two new services (svc-adventure-tracking + svc-emergency-response)**

Separate services with distinct responsibilities, data stores, and scaling profiles.

| Aspect | Assessment |
|--------|-----------|
| Separation of concerns | Each service has one job: tracking ingests positions, emergency-response manages emergencies |
| Scaling | Tracking scales horizontally for GPS volume; emergency-response scales for reliability |
| Data ownership | Clean ownership: tracking owns position data, emergency-response owns emergency records |
| Complexity | Two services to deploy, monitor, and maintain |
| Domain alignment | Tracking in Operations, emergency-response in Safety — matches domain boundaries |

**Option B: Single combined service (svc-adventure-safety)**

One service handles both GPS tracking and emergency response.

| Aspect | Assessment |
|--------|-----------|
| Separation of concerns | Mixed: high-frequency data ingestion and critical emergency workflows in one codebase |
| Scaling | Cannot scale tracking throughput independently of emergency reliability |
| Data ownership | Single owner, but the data model mixes operational telemetry with safety-critical records |
| Complexity | One service to deploy — simpler operations |
| Domain alignment | Crosses the Operations/Safety domain boundary — violates bounded context |

**Option C: Extend existing services (svc-check-in + svc-safety-compliance)**

Add tracking to svc-check-in (which already handles check-in orchestration) and emergency response to svc-safety-compliance (which already handles incidents).

| Aspect | Assessment |
|--------|-----------|
| Separation of concerns | Overloads svc-check-in with high-frequency GPS ingestion unrelated to check-in; overloads svc-safety-compliance with dispatch workflow unrelated to waivers |
| Scaling | svc-check-in would need to handle both check-in bursts AND continuous GPS streams — fundamentally different load patterns |
| Data ownership | Tracking data stored alongside check-in records muddies the data model |
| Complexity | No new services — minimal infrastructure change |
| Domain alignment | Stays within existing domains, but violates single responsibility |

### Decision Outcome

**Chosen option: Option A — Two new services.**

The ticket itself specifies `svc-adventure-tracking` and `svc-emergency-response` as new services. The two-service approach aligns with NovaTrek's bounded context rules: tracking is an Operations concern (data ingestion, geofence evaluation) while emergency response is a Safety concern (dispatch, compliance, audit trail). The fundamentally different performance profiles (high-throughput GPS vs. high-reliability emergency) make independent scaling essential.

svc-emergency-response already has data store schema and event definitions in the architecture metadata, confirming prior architectural intent.

### Consequences

**Positive:**
- Clean domain boundaries maintained
- Each service can be scaled, deployed, and monitored independently
- Failure in tracking does not cascade to emergency response and vice versa
- Clear data ownership for compliance and audit

**Negative:**
- Two additional services to operate (deploy, monitor, alert on)
- Cross-service latency between tracking detection and emergency creation (mitigated by async events with SLA)
- Additional network hops for the SOS-to-dispatch flow

**Neutral:**
- Event-driven integration (not synchronous REST) between the two services, consistent with cross-domain communication patterns

---

## ADR-013: Event-Driven Tracking Activation via Check-In Completion

### Status

Proposed

### Date

2026-03-14

### Context and Problem Statement

GPS tracking must begin when a guest starts their adventure. The system needs a reliable trigger to activate tracking for the correct guest with the correct adventure classification. When and how should tracking be activated?

### Decision Drivers

- **No manual triggers** — tracking must activate automatically (acceptance criteria 2)
- **Wristband identity** — the RFID tag assigned during check-in is the link between guest and GPS device
- **Adventure classification** — tracking frequency depends on adventure pattern (Pattern 1/2/3)
- **Existing event contracts** — the `checkin.completed` event already carries `rfid_tag`, `adventure_category`, and `check_in_pattern`
- **Loose coupling** — svc-check-in should not need to know about svc-adventure-tracking

### Considered Options

**Option A: Consume the existing checkin.completed event**

svc-adventure-tracking subscribes to the `novatrek.operations.checkin.completed` event. The event payload already contains all required fields (rfid_tag, adventure_category, check_in_pattern, guest_id, trip_id).

| Aspect | Assessment |
|--------|-----------|
| Coupling | Zero coupling — svc-check-in does not change |
| Data availability | Event already carries rfid_tag, adventure_category, check_in_pattern |
| Reliability | At-least-once delivery via message broker ensures no missed activations |
| Timing | Slight delay (event propagation) between check-in completion and tracking start — acceptable since guests are still at the check-in desk |

**Option B: Synchronous API call from svc-check-in to svc-adventure-tracking**

svc-check-in calls `POST /tracking-sessions` on svc-adventure-tracking during the check-in completion workflow.

| Aspect | Assessment |
|--------|-----------|
| Coupling | Tight — svc-check-in must know about svc-adventure-tracking |
| Data availability | Check-in has all required data at call time |
| Reliability | If svc-adventure-tracking is down, check-in either fails or silently skips tracking — both are bad |
| Timing | Immediate, but adds latency to the check-in completion path |

**Option C: Scheduled batch activation**

A periodic job queries svc-check-in for recently completed check-ins and creates tracking sessions.

| Aspect | Assessment |
|--------|-----------|
| Coupling | Loose — polling-based |
| Data availability | Available via API |
| Reliability | Delay between check-in and tracking activation (polling interval) |
| Timing | Unacceptable latency for safety-critical system — guests could be on trail before tracking starts |

### Decision Outcome

**Chosen option: Option A — Consume checkin.completed event.**

The event already exists, carries all required data (rfid_tag, adventure_category, check_in_pattern), and requires zero changes to svc-check-in. This follows the established cross-domain communication pattern (event-driven between domains) and ensures tracking activation is decoupled from the check-in workflow.

### Consequences

**Positive:**
- Zero changes to svc-check-in
- Event contract already proven in production (NTK-10005)
- At-least-once delivery guarantees no missed activations
- New event consumers can be added without modifying the producer

**Negative:**
- Small propagation delay between check-in completion and tracking activation (typically under 1 second)
- svc-adventure-tracking must handle duplicate events (idempotent session creation)

**Neutral:**
- Tracking deactivation uses the same pattern: consume `reservation.status-changed` event with status COMPLETED

---

## ADR-014: Pattern-Based Tracking Frequency with Pattern 3 Default

### Status

Proposed

### Date

2026-03-14

### Context and Problem Statement

GPS tracking frequency affects battery life, data volume, position accuracy, and emergency response time. Higher-risk adventures need more frequent position updates for safety. How should tracking frequency be determined, and what should the default be for unknown categories?

### Decision Drivers

- **Safety-first principle** (ADR-005) — unknown categories must default to the highest safety level
- **Battery optimization** — lower-risk adventures do not need 10-second GPS updates
- **Configuration-driven approach** (ADR-004) — tracking frequency should be configurable, not hardcoded
- **Insurance compliance** — Pattern 2 and 3 adventures require sufficient tracking granularity for compliance records
- **Data volume** — 10-second updates for all guests would generate excessive storage and processing load

### Considered Options

**Option A: Pattern-based frequency matrix (configuration-driven)**

| Pattern | Frequency | Rationale |
|---------|-----------|-----------|
| 1 (Basic) | 60 seconds | Low risk, self-guided — periodic position sufficient |
| 2 (Guided) | 30 seconds | Moderate risk, guide-led — balance of detail and efficiency |
| 3 (Full Service) | 10 seconds | High risk — near-real-time for safety and compliance |
| Unknown/default | 10 seconds | ADR-005 safety-first — treat unknown as highest risk |

Frequency matrix stored in YAML configuration (adventure-classification.yaml extension), changeable without code deployment.

**Option B: Uniform frequency for all adventures**

All adventures tracked at 30-second intervals regardless of classification.

| Aspect | Assessment |
|--------|-----------|
| Simplicity | Maximum — one frequency for all |
| Safety | Pattern 3 adventures are under-tracked (30s vs needed 10s) |
| Efficiency | Pattern 1 adventures are over-tracked (30s vs sufficient 60s) |
| Battery | Single frequency is a poor trade-off between battery life and accuracy |

**Option C: Guest-configurable frequency**

Allow guests to choose their tracking frequency via the mobile app.

| Aspect | Assessment |
|--------|-----------|
| Guest autonomy | Maximum — guest chooses |
| Safety | Guests may choose minimal tracking on high-risk adventures, creating liability |
| Compliance | Insurance mandates cannot be met if guests opt for infrequent tracking |
| Complexity | High — UI, validation, and policy enforcement needed |

### Decision Outcome

**Chosen option: Option A — Pattern-based frequency matrix (configuration-driven).**

This extends the established configuration-driven pattern from ADR-004 (adventure classification YAML) to include tracking parameters. The safety-first default from ADR-005 applies: unknown or unmapped categories get Pattern 3 frequency (10 seconds). The matrix is stored in YAML configuration, allowing operations to tune frequencies based on field experience without code changes.

### Consequences

**Positive:**
- Tracking intensity matches risk level — efficient use of battery, bandwidth, and storage
- Safety-first default for unknown categories (ADR-005 consistency)
- Configurable without code deployment (ADR-004 consistency)
- Clear insurance compliance story: Pattern 2 and 3 meet frequency requirements

**Negative:**
- Three frequency tiers add complexity to the tracking session management
- Configuration drift risk if the frequency matrix is changed without reviewing battery life implications

**Neutral:**
- The frequency matrix becomes part of the adventure-classification configuration, extending an existing pattern rather than introducing a new one
