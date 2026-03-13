# Risks — NTK-10006

## R1: Insurance Mandate Deadline at Risk Without Hardware Decision

**Risk**: The ticket references a year-end insurance mandate for GPS audit trails. If the
wristband hardware decision (RFID-only vs. GPS-capable) is not made imminently, the software
solution cannot be tested with real devices before the deadline.

**Likelihood**: High — the hardware procurement cycle for custom wristbands is typically
8-16 weeks.

**Impact**: Critical — losing insurance coverage would halt all high-risk adventure operations.

**Mitigation**: Begin software development immediately using the mobile app as the primary
tracking device (no hardware dependency). Run a parallel hardware evaluation. Satellite
beacons (procurement lead time: 2-4 weeks) are the near-term fallback for alpine trips.

---

## R2: GPS Coverage Gaps in Adventure Zones

**Risk**: Some adventure areas (deep canyons, dense forest, underground caves) may have
insufficient cellular or GPS signal for continuous telemetry. Guests in these areas will
have position records that go stale during coverage gaps.

**Likelihood**: Medium — NovaTrek operates diverse terrain types.

**Impact**: High — stale positions could delay detection of an incident in a coverage gap.

**Mitigation**: Coverage mapping for each active trip type before go-live. Trips in known
coverage gaps require satellite beacons as mandatory equipment (not optional). A staleness
alert fires when a device has not sent a position update within a configurable window
(default: 15 minutes for active adventures).

---

## R3: False Positive Emergency Triggers from GPS Drift

**Risk**: GPS accuracy near geofence boundaries (within 20-50 metres) may cause devices
to oscillate across the boundary and generate spurious alerts.

**Likelihood**: Medium — standard GPS accuracy is ±5 metres under ideal conditions but
±30 metres in tree canopy or near cliff faces.

**Impact**: Medium — false positive dispatches waste rescue resources and erode staff trust
in the system.

**Mitigation**: Configurable distance buffer on geofence boundaries (default: 50-metre
inset from the defined boundary before alert fires). Violation must persist for 3 consecutive
updates before an alert is created (prevents momentary drift triggers). Safety officer
review gate for geofence violations (SOS remains fully automated per ADR-NTK10006-003).

---

## R4: Automated Emergency Suppression During Device Malfunction

**Risk**: A wristband that malfunctions and continuously sends SOS flags would flood
svc-emergency-response with duplicate incidents.

**Likelihood**: Low — devices are tested before issuance; malfunction rate expected to be low.

**Impact**: Medium — duplicate incidents create noise and could delay response to a real emergency.

**Mitigation**: Rate limiting on emergency creation per device (maximum 1 automated emergency
per session per 10 minutes). Duplicate suppression in svc-adventure-tracking: if an emergency
is already active for a session, subsequent triggers update the existing incident rather than
creating a new one.

---

## R5: Device API Key Compromise

**Risk**: A long-lived device API key extracted from a wristband or mobile app could be used
by a third party to inject false telemetry or SOS signals.

**Likelihood**: Low — devices are physical and require physical access to compromise.

**Impact**: High — false SOS signals would dispatch rescue resources to incorrect locations.

**Mitigation**: Per-device API keys with narrow scope (POST /telemetry only). Key rotation
procedure documented and executable within 30 minutes of a reported device compromise.
Anomaly detection on position jumps (positions more than 50 km from the previous position
in under 1 minute are flagged and quarantined for human review rather than processed
immediately).

---

## R6: Data Privacy — Guest GPS Positions Are Sensitive PII

**Risk**: Real-time GPS positions and historical telemetry constitute sensitive location PII.
A breach of the telemetry store would expose guests' precise physical locations.

**Likelihood**: Low — standard cloud security controls apply.

**Impact**: High — location PII breach triggers regulatory notification obligations and
damages guest trust.

**Mitigation**: Column-level encryption for latitude/longitude in the position_telemetry table
at rest. TLS in transit for all telemetry (device-to-API and API-to-DB). Access control: only
Safety Officer role can query position history via the API. 90-day archive policy limits the
window of historical exposure.
