# Architecture Decisions — NTK-10006

## ADR-NTK10006-001: Dedicated Adventure Tracking Microservice

### Status

Accepted

### Date

2026-03-13

### Context and Problem Statement

GPS telemetry ingestion for active adventures needs a home in the NovaTrek architecture.
Options include adding telemetry endpoints to svc-check-in (which already owns adventure
sessions), to svc-safety-compliance (which owns emergency protocols), or creating a dedicated
service. The choice affects data ownership, operational isolation, and team boundaries.

### Decision Drivers

- High-frequency ingest (up to 14 events/second peak) is operationally distinct from
  transactional check-in flows
- Device authentication (long-lived API keys) must not be co-located with guest JWT flows
- Time-series telemetry has different storage, indexing, and retention requirements than
  operational records
- The Safety and Compliance Team owns both svc-safety-compliance and svc-emergency-response;
  centralising tracking in their domain makes ownership clear
- svc-check-in is owned by Operations Team; mixing telemetry ingest into it would create
  cross-team data ownership ambiguity

### Considered Options

**Option 1: New svc-adventure-tracking microservice** (SELECTED)

- (+) Isolated deployment and scaling for high-frequency write path
- (+) Device API key authentication isolated from human JWT tokens
- (+) TimescaleDB time-series storage optimised for telemetry without affecting check-in DB
- (+) Safety and Compliance Team owns the full emergency signal chain end-to-end
- (-) Additional service to deploy, monitor, and operate
- (-) Cross-service call from svc-check-in to activate sessions

**Option 2: Extend svc-check-in with tracking endpoints**

- (+) No new service; check-in already holds group and RFID data
- (-) Mixes high-frequency telemetry ingest into a transactional service; shared DB handles
  different access patterns poorly
- (-) Operations Team would own safety telemetry — cross-domain data ownership violation
- (-) Device API keys co-located with guest JWTs increase blast radius of a key compromise

**Option 3: Extend svc-safety-compliance**

- (+) Safety team already owns the service
- (-) svc-safety-compliance is compliance-record oriented (waivers, incident reports, audits);
  real-time telemetry ingest is architecturally different
- (-) High-frequency writes would compete with compliance record queries
- (-) No clean API contract for device-to-cloud telemetry in the existing spec

### Decision Outcome

Selected **Option 1: New svc-adventure-tracking microservice**. The operational and data model
differences between real-time telemetry ingest and transactional adventure operations justify
a dedicated service. The Safety and Compliance Team owns the complete emergency detection chain.

### Consequences

**Positive**: Isolated scaling for telemetry; clean data ownership; device authentication
isolated from human auth flows.

**Negative**: Additional operational surface (deployment, monitoring, alerting).

**Neutral**: Follows the NovaTrek pattern of one bounded context per service.

---

## ADR-NTK10006-002: Time-Series Storage for GPS Telemetry

### Status

Accepted

### Date

2026-03-13

### Context and Problem Statement

GPS telemetry generates append-only, timestamped records at high frequency. The query patterns
are time-range queries (give me all positions for session X between T1 and T2) and last-known
lookups (give me the current position of each device). Standard relational storage treats all
rows equally; time-series optimised storage can compress and partition by time natively.

### Decision Drivers

- Telemetry is append-only — no updates to historical records
- 90-day retention with compression after 30 days is a known requirement
- Queries are primarily time-bounded range scans, not arbitrary relational joins
- Infrastructure must be viable on Azure (managed service preferred)
- The rest of the NovaTrek platform uses PostgreSQL; diverging to a separate database engine
  has an operational cost

### Considered Options

**Option 1: TimescaleDB extension on PostgreSQL** (SELECTED)

- (+) Native PostgreSQL — same operational tooling (backups, monitoring, access control)
- (+) Automatic time-based partitioning (chunk interval configurable)
- (+) Built-in compression policies (up to 95% size reduction after 30 days)
- (+) Continuous aggregates for real-time dashboard summaries without full scans
- (+) Available as managed extension on Azure Database for PostgreSQL Flexible Server
- (-) Less specialised than a purpose-built time-series DB (e.g., InfluxDB)

**Option 2: Standard PostgreSQL without time-series extension**

- (+) No extension; familiar without additional configuration
- (-) Manual partitioning required for 90-day retention and compression
- (-) Full table scans on large telemetry tables without proper indexing
- (-) No built-in compression policies

**Option 3: Azure Data Explorer (Kusto)**

- (+) Purpose-built for high-volume time-series data at scale
- (-) Significant divergence from the PostgreSQL-centric NovaTrek platform
- (-) Separate operational tooling, security model, and access patterns
- (-) Overengineered for the 14 events/second peak load estimate

### Decision Outcome

Selected **Option 1: TimescaleDB on PostgreSQL**. The operational consistency with the existing
NovaTrek platform, combined with TimescaleDB's native compression and continuous aggregates,
provides the right balance of capability and simplicity at the current load estimate.

### Consequences

**Positive**: Single operational database family; compression keeps storage costs manageable;
continuous aggregates power the live dashboard without full-table scans.

**Negative**: Requires TimescaleDB extension provisioned on the PostgreSQL instance.

**Neutral**: If load grows beyond TimescaleDB's comfortable range, migration to Azure Data
Explorer is the documented escalation path.

---

## ADR-NTK10006-003: Automated Emergency Triggering With Human Review Gate

### Status

Accepted

### Date

2026-03-13

### Context and Problem Statement

When svc-adventure-tracking detects an SOS signal or geofence violation, it must decide
whether to create an emergency incident in svc-emergency-response automatically or require
a safety officer to manually confirm before dispatch. Fully automated triggers reduce response
time but risk false positives (GPS drift near a boundary, accidental SOS activation).
Human-gated triggers prevent false positives but reintroduce the delay this system is
designed to eliminate.

### Decision Drivers

- Rescue response time is the primary objective — automation exists to shorten it
- False positive dispatches waste resources and desensitise staff to alerts
- The SOS button is a deliberate action by the guest; geofence violations may be ambiguous
  (GPS drift within 50 metres of boundary)
- Operations must maintain accountability for emergency dispatch decisions
- The existing svc-emergency-response API already supports status transitions (active →
  dispatched → resolved); a human confirmation step fits naturally into the workflow

### Considered Options

**Option 1: Fully automated dispatch for SOS; human review gate for geofence violations** (SELECTED)

- (+) SOS is an unambiguous intent signal — automated dispatch is appropriate
- (+) Geofence violations are evaluated with a configurable distance buffer before alerting
- (+) Safety officers receive notification immediately for both; they can cancel a false positive
- (+) Response time for SOS drops to under 2 minutes
- (-) Geofence violations still have a human review step (target: 5-minute resolution window)
- (-) Requires clear UX in the ops dashboard for incident cancellation

**Option 2: All triggers require human confirmation**

- (+) Zero false positive dispatches
- (-) Reintroduces the delay this system is designed to eliminate; defeats the primary objective
- (-) No improvement on current radio-dependent workflow for SOS events

**Option 3: Fully automated dispatch for all trigger types**

- (+) Fastest possible response for all scenarios
- (-) GPS drift near geofence boundaries generates frequent false alarms during normal operation
- (-) Staff desensitisation to false alarms reduces actual emergency response quality

### Decision Outcome

Selected **Option 1: SOS triggers automated dispatch; geofence violations trigger a safety
officer review alert**. The distinction matches the intent signals: SOS is deliberate and
unambiguous; geofence proximity may be GPS drift. Geofence alerts are sent immediately to the
safety officer with a 5-minute confirmation window before auto-escalation.

### Consequences

**Positive**: SOS response target of under 2 minutes achievable; geofence violations reviewed
before dispatch reduces false positive rate.

**Negative**: Geofence violation response is still bounded by the safety officer's
acknowledgment time (target 5 minutes).

**Neutral**: Auto-escalation after 5 minutes (if no acknowledgment) preserves the safety net
for unattended consoles.
