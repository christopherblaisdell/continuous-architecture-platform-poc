<!-- PUBLISH -->
# NTK-10006 User Stories

## US-1: Real-Time Guest Position Monitoring

**As a** park safety officer,
**I want to** see the live GPS position of every guest on an active adventure on a map,
**So that** I can monitor overall safety and identify potential issues before they become emergencies.

### Acceptance Criteria

1. The operations dashboard (web-ops-dashboard) displays a map with markers for all active tracking sessions
2. Markers update at the tracking frequency for each guest (10s, 30s, or 60s based on adventure pattern)
3. Marker color indicates adventure pattern: green (Pattern 1), amber (Pattern 2), red (Pattern 3)
4. Clicking a marker shows guest name, adventure type, guide name, check-in time, and battery level
5. The map supports filtering by adventure category, guide, and geographic area

---

## US-2: Automatic Tracking Activation

**As a** park safety officer,
**I want** GPS tracking to activate automatically when a guest completes check-in,
**So that** every guest on an adventure is tracked without requiring manual setup.

### Acceptance Criteria

1. Tracking begins within 10 seconds of check-in completion — no manual trigger
2. Tracking frequency matches the adventure's safety pattern (Pattern 1: 60s, Pattern 2: 30s, Pattern 3: 10s)
3. Unknown adventure categories default to Pattern 3 frequency (10 seconds)
4. The tracking session links to the guest's reservation, wristband RFID tag, and assigned guide
5. Tracking deactivates automatically when the adventure completes

---

## US-3: SOS Emergency Response

**As a** guest on an active adventure,
**I want to** press an SOS button on my wristband to request immediate help,
**So that** a rescue team is dispatched to my exact GPS location without delay.

### Acceptance Criteria

1. Pressing and holding the SOS button for 5 seconds triggers an emergency alert
2. The system sends my GPS coordinates and identity to the emergency response service
3. The nearest available rescue team is dispatched within 30 seconds of the SOS trigger
4. My assigned guide, operations staff, and emergency contacts are notified within 60 seconds
5. I can cancel the SOS within 60 seconds of triggering it (accidental press protection)

---

## US-4: Geofence Breach Alerting

**As an** adventure guide,
**I want to** receive an alert when a guest in my group leaves the designated trail boundary,
**So that** I can locate and redirect the guest before they enter a restricted or dangerous area.

### Acceptance Criteria

1. Geofence boundaries are defined for each adventure trail with a configurable buffer (default 50 meters)
2. A breach alert is sent to the assigned guide via push notification within one GPS update cycle
3. The alert includes the guest's name, last known position, and the geofence that was breached
4. False breaches from GPS inaccuracy are minimized by requiring 2 consecutive out-of-bounds positions
5. Operations staff also receive the breach alert via the dashboard

---

## US-5: Weather-Triggered Evacuation

**As a** park safety officer,
**I want** all guests in a weather-affected area to receive evacuation notifications automatically,
**So that** no guest is left uninformed during a severe weather event.

### Acceptance Criteria

1. When svc-weather issues a WARNING or EMERGENCY alert, the system identifies all guests currently in the affected area
2. Affected guests receive SMS and push notifications with evacuation instructions within 120 seconds
3. Their assigned guides receive parallel notifications with the guest list and nearest assembly points
4. An emergency record is created for the weather event with all affected guest IDs
5. The operations dashboard highlights the affected area and guest markers

---

## US-6: Emergency Timeline and Audit

**As an** insurance compliance officer,
**I want** every emergency to have a complete, tamper-proof timeline of events,
**So that** NovaTrek can demonstrate timely response and meet insurance tracking mandates.

### Acceptance Criteria

1. Every emergency record has an append-only timeline from trigger through resolution
2. Timeline entries include: trigger event, dispatch time, team acknowledgment, route time, arrival time, and resolution
3. Timeline entries are immutable — updates add new entries, never modify existing ones
4. Timelines can be exported for insurance reporting
5. GPS tracking data for the 90 days following an emergency is retained for compliance review

---

## US-7: Rescue Team Dispatch

**As a** park safety officer,
**I want** the system to automatically identify and dispatch the nearest rescue team with the right certifications,
**So that** response times are minimized and the right expertise arrives on scene.

### Acceptance Criteria

1. svc-emergency-response selects the nearest AVAILABLE rescue team based on geographic proximity
2. If the emergency type requires specific certification (e.g., swift water rescue, technical rope), only certified teams are considered
3. The dispatch includes an ETA based on team base location and emergency coordinates
4. The dispatched team receives an URGENT SMS and push notification with emergency details and GPS coordinates
5. If no team is available, the emergency is escalated to operations staff for manual coordination
