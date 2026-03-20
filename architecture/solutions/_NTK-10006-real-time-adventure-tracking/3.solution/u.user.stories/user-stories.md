<!-- PUBLISH -->

# NTK-10006 User Stories

## US-1: Real-Time Guest Location Monitoring

**As a** park safety officer,
**I want** to see the current GPS location of every guest on an active adventure on a live map,
**So that** I have situational awareness of all guest positions and can identify potential issues before they escalate.

**Acceptance Criteria:**
- The ops dashboard displays a map showing all active tracking sessions with guest markers
- Each marker shows guest name, adventure type, guide name, and time since last location update
- The map updates within 30 seconds of a new GPS coordinate being received
- Guests with no location update for more than 5 minutes are highlighted in amber (warning)

---

## US-2: Automated SOS Emergency Alerting

**As a** guest on an active adventure,
**I want** my wristband's SOS button to immediately notify rescue teams with my exact GPS location,
**So that** help arrives as quickly as possible in an emergency.

**Acceptance Criteria:**
- Pressing the SOS button on the wristband triggers `POST /tracking-sessions/{id}/locations` with `source: sos`
- svc-adventure-tracking creates an anomaly event and calls `POST /emergencies` on svc-emergency-response within 10 seconds
- The emergency record includes the guest's current GPS coordinates, reservation details, and medical information (from guest profile)
- On-duty guides, dispatch team, and guest emergency contacts receive notifications within 30 seconds of the SOS signal

---

## US-3: Geofence Violation Detection

**As a** park safety officer,
**I want** the system to automatically detect when a guest leaves the designated adventure area,
**So that** I can intervene before the guest enters unsafe territory.

**Acceptance Criteria:**
- Each trail has a geofence boundary polygon defined via `POST /geofences`
- When a guest's GPS location falls outside the geofence, svc-adventure-tracking creates a `tracking.anomaly.detected` event
- The ops dashboard shows a visual alert on the map with the guest's position relative to the boundary
- If no staff acknowledges the alert within 2 minutes, the anomaly auto-escalates to an emergency

---

## US-4: Tracking Session Lifecycle

**As a** park safety officer,
**I want** tracking sessions to start automatically when a guest completes check-in and end when the adventure concludes,
**So that** I do not need to manually manage tracking for each guest.

**Acceptance Criteria:**
- When `checkin.completed` event is received, svc-adventure-tracking creates a tracking session linked to the wristband RFID tag
- The tracking session status is `active` from creation until adventure end
- When the adventure ends (scheduled time or manual check-out), the session transitions to `ended`
- Location history is retained for 1 year; audit records for 7 years
- For Pattern 2/3 adventures, ops staff receive an alert if a guest departs without an active tracking session

---

## US-5: Signal Loss Handling

**As a** park safety officer,
**I want** the system to alert me when a guest's wristband stops transmitting,
**So that** I can investigate whether the guest is in distress or if the equipment malfunctioned.

**Acceptance Criteria:**
- If no location update is received for a configurable timeout (default: 5 minutes), svc-adventure-tracking creates a signal-loss anomaly
- The ops dashboard shows the guest's last known position with a "signal lost" indicator
- If signal is not restored within a second configurable timeout (default: 15 minutes), the anomaly auto-escalates to an emergency
- The timeout values are configurable per adventure category in `config/adventure-classification.yaml` (longer for remote adventures with expected dead zones)

---

## US-6: Insurance Compliance Reporting

**As a** compliance officer,
**I want** a complete GPS location history for every guest's adventure,
**So that** NovaTrek can demonstrate continuous monitoring to insurance providers.

**Acceptance Criteria:**
- `GET /tracking-sessions/{id}/locations` returns the full coordinate history for a session
- Each location record includes timestamp, coordinates, accuracy, and source (GPS, wristband, manual)
- Tracking session records include start time, end time, total duration, and total location updates
- All anomaly events and emergency triggers linked to a session are accessible via the session API
- Data is retained for a minimum of 1 year (location history) and 7 years (audit trail)
