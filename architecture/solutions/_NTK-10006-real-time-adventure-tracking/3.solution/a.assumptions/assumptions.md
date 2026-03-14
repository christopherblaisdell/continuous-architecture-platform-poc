<!-- PUBLISH -->
# NTK-10006 Assumptions

## Hardware and Infrastructure

| ID | Assumption | Risk if Wrong | Mitigation |
|----|-----------|---------------|-----------|
| A-1 | RFID wristbands already assigned at check-in (NTK-10005) are capable of transmitting GPS coordinates at configurable intervals | HIGH — no tracking without GPS hardware | Validate wristband hardware spec; if current wristbands lack GPS, a hardware procurement step is required before this solution can be deployed |
| A-2 | GPS signal is available in all adventure zones, including canyons, dense forest, and underground caves | MEDIUM — signal loss creates tracking gaps | Design for intermittent connectivity: buffer positions locally on the wristband and transmit in batches when signal resumes; use last-known-position for emergency response |
| A-3 | Wristband battery life supports GPS transmission for the maximum adventure duration (12 hours at Pattern 3 frequency of 10-second intervals) | HIGH — dead batteries mean no tracking | Battery requirements must be validated against the tracking frequency matrix; Pattern 1 minimal frequency (60s) extends battery life |
| A-4 | A message broker (Kafka or equivalent) is available for event-driven communication between services | LOW — the architecture already uses async events | Verify infrastructure supports the volume of GPS position events (estimated 50,000 position updates/day at peak) |

## Data and Compliance

| ID | Assumption | Risk if Wrong | Mitigation |
|----|-----------|---------------|-----------|
| A-5 | Insurance mandates require GPS tracking records for Pattern 2 and Pattern 3 adventures, with 90-day retention | MEDIUM — over-engineering if insurance does not mandate this | Confirm insurance contract requirements; even without mandate, tracking improves safety outcomes |
| A-6 | Guest consent for GPS tracking is collected as part of the safety waiver (svc-safety-compliance) | HIGH — tracking without consent violates privacy regulations | Add GPS tracking consent clause to the waiver form; make it mandatory for Pattern 2 and 3 adventures |
| A-7 | Position data is PII (personally identifiable information) because it is linked to a specific guest | HIGH — PII classification affects storage, access controls, and data retention | Apply standard PII protections: encryption at rest, access logging, retention limits, right-to-deletion support |

## Service Architecture

| ID | Assumption | Risk if Wrong | Mitigation |
|----|-----------|---------------|-----------|
| A-8 | svc-location-services PostGIS database already contains geofence boundaries (trail routes, restricted zones, assembly points) for all adventure trails | MEDIUM — geofences must be created before geofence breach detection works | Add geofence management endpoints to svc-location-services or maintain geofences as static configuration seeded from trail data |
| A-9 | svc-emergency-response data store schema (already defined in data-stores.yaml) is correct and sufficient for the emergency lifecycle | LOW — schema exists and was designed for this use case | Review schema against the full emergency workflow before implementation |
| A-10 | The operations dashboard (web-ops-dashboard) can consume a WebSocket or Server-Sent Events (SSE) stream for live position updates | MEDIUM — if the dashboard is purely REST-based, real-time display requires additional work | Design the API to support both polling (REST) and streaming (WebSocket/SSE); the frontend team chooses the integration pattern |
| A-11 | svc-adventure-tracking will be assigned to the Operations domain, not Safety, because tracking is an operational concern that feeds into safety systems | LOW — domain assignment is a governance decision | Confirm with domain model review; the service consumes check-in events (Operations) but feeds emergency-response (Safety), making it a cross-domain bridge |
