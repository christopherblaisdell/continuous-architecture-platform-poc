<!-- PUBLISH -->
# NTK-10006 Simple Explanation

## What is this about?

NovaTrek Adventures currently has no way to know where guests are once they leave the check-in desk and head out on their adventure. If a guest gets lost, injured, or encounters dangerous weather, there is no automated system to locate them or alert rescue teams.

## What is the problem?

1. **No visibility** — Safety officers cannot see where guests are on the trail in real time
2. **Slow response** — If something goes wrong, the first step is to figure out where the guest is, wasting critical minutes
3. **Insurance gaps** — NovaTrek's insurance requires GPS tracking records for high-risk adventures, and this data does not currently exist
4. **No automation** — Weather alerts and wildlife sightings require manual coordination to determine which guests are affected

## What is the proposed solution?

Two new services work together to solve this:

**svc-adventure-tracking** — Receives GPS signals from guest wristbands (the same RFID wristbands already assigned during check-in). It knows where every guest is at all times during their adventure. It also checks if guests wander outside their trail boundaries (geofencing).

**svc-emergency-response** — When something goes wrong (guest presses SOS, weather turns dangerous, guest leaves the safe zone), this service coordinates the response: creating an emergency record, finding the nearest rescue team, and sending alerts to guides, staff, and emergency contacts.

## How does it connect to what already exists?

The system builds on infrastructure from three previous tickets:

- **NTK-10005** added RFID wristband tracking IDs to the check-in record — that wristband ID is now the key that links a guest to their GPS position
- **NTK-10002** established the adventure classification system (Pattern 1/2/3) — tracking frequency scales with risk level
- **NTK-10003** established svc-check-in as the orchestrator — check-in completion is the trigger that activates tracking

## Who benefits?

- **Safety officers** see every active guest on a live map and get instant alerts when something goes wrong
- **Guides** receive immediate notification of emergencies in their group without relying on radio communication
- **Guests** have a safety net — pressing an SOS button on their wristband triggers an automatic rescue response
- **NovaTrek** meets insurance tracking mandates and reduces liability exposure

## What does this NOT include?

- Building the mobile app tracking UI (app-guest-mobile already has a "live trip maps" concept — this solution provides the backend data)
- Trail condition sensors or IoT infrastructure — GPS wristband hardware is assumed to exist
- Changes to the check-in flow itself — svc-check-in already emits the event that triggers tracking
