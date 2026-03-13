# User Stories — NTK-10006

## US-1: Safety Officer Views Live Adventure Map

As a park safety officer,
I want to see a live map showing the current GPS location of every active adventure party,
So that I have continuous situational awareness without waiting for radio check-ins.

**Acceptance Criteria**:
- The operations dashboard displays a map with a dot per active adventure session
- Each dot shows the trip name, guide name (if assigned), party size, and time since last update
- The map refreshes positions at least every 2 minutes
- Sessions where the last update is older than 15 minutes are highlighted as stale

---

## US-2: Safety Officer Receives Automated SOS Alert

As a park safety officer,
I want to receive an automated emergency alert the moment a guest activates their SOS signal,
So that I can dispatch rescue within 2 minutes of signal receipt instead of waiting for a
radio call from the guide.

**Acceptance Criteria**:
- An SOS activation on any tracked device creates an emergency incident automatically
- The emergency alert appears on the safety officer's dashboard within 60 seconds of signal receipt
- The alert includes the guest's last known GPS coordinates and the trip details
- The safety officer receives a push notification or audio alert (not just a silent UI update)

---

## US-3: Safety Officer Receives Geofence Violation Alert

As a park safety officer,
I want to be notified when an adventure party crosses outside their designated adventure area,
So that I can investigate whether the deviation is an emergency before dispatching rescue.

**Acceptance Criteria**:
- A geofence boundary violation alert is delivered to the safety officer within 60 seconds
  of detection
- The alert includes the GPS position of the violation, the party details, and the boundary map
- The safety officer can mark the alert as a false positive (clears the alert without escalation)
- If the safety officer does not acknowledge the alert within 5 minutes, the system automatically
  escalates to an emergency incident

---

## US-4: Safety Officer Retrieves GPS Trail for Incident Investigation

As a safety compliance officer,
I want to retrieve the full GPS position history for any adventure session,
So that I can construct an accurate incident timeline for insurance claims and regulatory reports.

**Acceptance Criteria**:
- The position history for any session is retrievable for a minimum of 90 days after the adventure
- The history can be filtered by time range and by specific device
- Position records include the timestamp, coordinates, altitude (when available), and SOS flag
- The history is linkable from the incident report in svc-safety-compliance

---

## US-5: Operations Staff Configures Geofence for an Adventure Area

As an operations coordinator,
I want to define a GPS boundary for each adventure area in the system,
So that the tracking service can enforce boundaries automatically without manual configuration
for each individual adventure.

**Acceptance Criteria**:
- Operations staff can create a geofence by drawing a polygon or circle on a map
- Each geofence is associated with a specific trip type in the catalog
- The geofence is active for all future sessions of that trip type automatically
- Operations staff can update or delete a geofence without affecting sessions already in progress

---

## US-6: Guide Activates Adventure Tracking at Departure

As a trip guide,
I want to confirm adventure departure from my check-in device,
So that the tracking session activates automatically and the safety team begins monitoring
our party without any additional steps on my part.

**Acceptance Criteria**:
- A single action (marking check-in status as ADVENTURE_STARTED) activates the tracking session
- The guide receives confirmation that tracking is active before departure
- If tracking activation fails (service unavailable), the guide is notified but the departure
  is not blocked — the adventure proceeds
- The check-in record shows the tracking session ID so the guide can reference it if needed
