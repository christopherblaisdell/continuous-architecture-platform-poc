<!-- PUBLISH -->

# NTK-10006 Simple Explanation

## What is changing?

NovaTrek Adventures currently has no way to know where guests are once they leave the check-in station. If a guest gets lost, injured, or encounters wildlife, the safety team relies on phone calls and manual search — which is slow and unreliable in backcountry areas with poor cell coverage.

This ticket adds a **real-time GPS tracking system** that monitors every guest during their adventure. When a guest checks in and receives their wristband, the system starts tracking their location automatically. The operations team can see all active guests on a live map, and if something goes wrong, the system detects it and alerts the right people immediately.

## Why does it matter?

1. **Guest safety** — faster rescue response times when guests trigger SOS or go off-trail
2. **Insurance compliance** — tracking mandates require proof of location monitoring during high-risk adventures
3. **Operational visibility** — safety officers see all active guests in real time instead of relying on radio check-ins

## What is new?

- **svc-adventure-tracking** — a new service that receives GPS coordinates from guest wristbands, manages tracking sessions (start at check-in, end at adventure completion), monitors geofences, and detects anomalies (guest stopped moving, exited trail boundary)
- **Integration with svc-emergency-response** — when the tracking system detects an emergency (SOS button pressed, geofence violation, guest unresponsive), it automatically triggers the existing emergency alerting workflow: dispatches rescue teams, notifies guides, and contacts the guest's emergency contacts

## What stays the same?

- The check-in process is unchanged — guests still check in with their reservation, get their wristband, and receive a safety briefing
- The emergency response workflow already exists (svc-emergency-response has a complete API) — this ticket connects it to real-time location data
- Notifications still go through the existing svc-notifications channels (SMS, email, push)
- All existing safety compliance features (waivers, incident reporting, audit logging) continue operating as-is
