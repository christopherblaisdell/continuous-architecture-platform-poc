<!-- PUBLISH -->
# NTK-10006 Risk Register

## R-1: GPS Signal Loss in Remote Terrain

| Field | Value |
|-------|-------|
| Likelihood | HIGH |
| Impact | HIGH |
| Risk Level | CRITICAL |
| Category | Technical |

**Description:** Canyons, dense forest canopy, and underground cave systems will block or degrade GPS signals. During signal loss, the guest's position is unknown to the tracking system.

**Mitigation:**
- Wristbands buffer position data locally and transmit in batches when signal resumes (POST /positions/batch)
- Last-known-position is used for emergency response — rescue teams head to the last confirmed coordinates
- Pattern 3 adventures in known dead zones could supplement GPS with BLE beacons at waypoints (future enhancement)

---

## R-2: Wristband Battery Depletion

| Field | Value |
|-------|-------|
| Likelihood | MEDIUM |
| Impact | HIGH |
| Risk Level | HIGH |
| Category | Technical |

**Description:** GPS transmission at 10-second intervals (Pattern 3) consumes significant battery. If a wristband battery depletes during an adventure, tracking is lost for that guest.

**Mitigation:**
- Battery percentage is reported with every position update — the system can alert operations when battery drops below 20%
- Pattern-based frequency optimization reduces battery drain for lower-risk adventures
- Wristband hardware spec must guarantee minimum 12-hour battery life at Pattern 3 frequency (assumption A-3)

---

## R-3: Privacy and Consent Compliance

| Field | Value |
|-------|-------|
| Likelihood | LOW |
| Impact | CRITICAL |
| Risk Level | HIGH |
| Category | Legal/Compliance |

**Description:** Continuous GPS tracking of guests constitutes collection of personal location data. Without explicit consent, this may violate privacy regulations (GDPR, CCPA, local tourism regulations).

**Mitigation:**
- GPS tracking consent is embedded in the safety waiver (assumption A-6) — guests must acknowledge tracking before check-in completes
- Position data retention is limited to 90 days (insurance compliance), then purged
- Guests can request deletion of their tracking data after adventure completion (right to deletion)
- Position data is encrypted at rest and access-logged

---

## R-4: False SOS Triggers

| Field | Value |
|-------|-------|
| Likelihood | MEDIUM |
| Impact | MEDIUM |
| Risk Level | MEDIUM |
| Category | Operational |

**Description:** Accidental SOS button presses on wristbands could trigger unnecessary emergency responses, wasting rescue team resources and causing alarm.

**Mitigation:**
- SOS confirmation period — wristband requires a 5-second press-and-hold to trigger SOS (hardware UX)
- Emergency cancellation within 60 seconds — guest can cancel via wristband or mobile app, auto-cancelling the emergency record
- Operations dashboard shows SOS with "unconfirmed" status during the cancellation window
- False SOS rate is tracked as an operational metric for hardware design feedback

---

## R-5: High Data Volume and Storage Costs

| Field | Value |
|-------|-------|
| Likelihood | HIGH |
| Impact | MEDIUM |
| Risk Level | MEDIUM |
| Category | Cost |

**Description:** At peak capacity — 500 guests tracked simultaneously at Pattern 3 frequency (10s) — the system generates approximately 50,000 position records per day. With 90-day retention, the positions table grows to approximately 4.5 million rows.

**Mitigation:**
- TimescaleDB extension (or PostgreSQL table partitioning) for time-series position data
- Positions older than 90 days are archived to cold storage (Azure Blob) before deletion
- Pattern-based frequency ensures only high-risk adventures generate high-frequency data
- Position data is compact (~200 bytes per record) — 4.5M rows is approximately 900 MB, manageable for PostgreSQL

---

## R-6: Geofence Accuracy and False Breaches

| Field | Value |
|-------|-------|
| Likelihood | MEDIUM |
| Impact | LOW |
| Risk Level | LOW |
| Category | Technical |

**Description:** GPS accuracy varies (3-15 meter horizontal accuracy in consumer devices). Guests near trail boundaries may trigger false geofence breach alerts.

**Mitigation:**
- Geofence buffer distance (default 50 meters) accounts for GPS inaccuracy
- Breach must persist for 2 consecutive position updates before triggering an alert (debouncing)
- GPS accuracy estimate is included in every position report — positions with accuracy worse than the buffer threshold are flagged as unreliable

---

## R-7: Single Point of Failure in Emergency Notification Chain

| Field | Value |
|-------|-------|
| Likelihood | LOW |
| Impact | CRITICAL |
| Risk Level | HIGH |
| Category | Architecture |

**Description:** If svc-notifications is unavailable during an emergency, critical alerts may not reach rescue teams, guides, or emergency contacts.

**Mitigation:**
- svc-emergency-response uses circuit breaker pattern for svc-notifications calls
- Fallback: if notification delivery fails, the emergency record remains in DISPATCHED status with a timeline entry marking notification failure — operations staff monitoring the dashboard will see the emergency directly
- SMS delivery via Twilio has its own retry mechanism independent of svc-notifications availability
- Emergency notifications are retried with exponential backoff for transient failures

## Risk Summary

| Risk | Level | Status |
|------|-------|--------|
| R-1: GPS Signal Loss | CRITICAL | Mitigated (batch upload, last-known-position) |
| R-2: Battery Depletion | HIGH | Mitigated (monitoring, frequency optimization) |
| R-3: Privacy Compliance | HIGH | Mitigated (waiver consent, encryption, retention) |
| R-4: False SOS | MEDIUM | Mitigated (confirmation period, cancellation) |
| R-5: Data Volume | MEDIUM | Mitigated (partitioning, archival, pattern frequency) |
| R-6: Geofence Accuracy | LOW | Mitigated (buffer, debouncing) |
| R-7: Notification Failure | HIGH | Mitigated (circuit breaker, dashboard fallback) |
