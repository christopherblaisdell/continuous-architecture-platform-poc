# Assumptions — NTK-10006

## A1: Wristband RFID Devices Support GPS Telemetry Transmission

**Assumption**: The wristband hardware issued at check-in (introduced by NTK-10005) includes
or will include a GPS chipset and cellular/LoRaWAN connectivity capable of transmitting
position updates to the svc-adventure-tracking API at a configurable interval (default: every
2 minutes for normal operation, every 30 seconds when SOS is active).

**Risk if invalid**: The existing RFID-only wristbands cannot transmit GPS. A hardware upgrade
or supplementary GPS device (e.g., satellite beacon for alpine trips) would be required.

**Mitigation**: Mobile app tracking is the fallback for guests who carry smartphones.
Satellite beacons (spot devices) are the fallback for trips without cellular coverage.
Both alternatives use the same `/telemetry` API endpoint with a different `device_type`.

## A2: Cellular or LoRaWAN Coverage Exists in All Active Adventure Zones

**Assumption**: At least one of cellular data, LoRaWAN gateway, or satellite uplink is
available within adventure areas to deliver telemetry updates within 3 minutes of capture.

**Risk if invalid**: Adventures in deep canyons or dense forest may have multi-hour coverage
gaps. Telemetry batching with local storage and delayed upload would be needed.

**Mitigation**: Trips with known coverage gaps require satellite beacons as primary device.
The system handles batched telemetry (multiple position records submitted in one call)
without any API changes — the `recorded_at` field on each position preserves original timing.

## A3: svc-check-in Exposes an ADVENTURE_STARTED Status Transition

**Assumption**: svc-check-in supports (or can be extended to support) an
`ADVENTURE_STARTED` status on check-in records, triggered when the guide initiates
the adventure departure. This is the event that activates a tracking session.

**Risk if invalid**: Without a departure trigger, svc-adventure-tracking cannot know when
to expect telemetry. Sessions would need to be activated manually by safety officers.

**Mitigation**: If ADVENTURE_STARTED status does not exist, svc-check-in can be extended
with minimal API surface: a `PATCH /check-ins/{id}` call with `status: ADVENTURE_STARTED`.
This change is within the check-in impact assessment.

## A4: geofence Boundaries Are Pre-Configured Per Trip Type

**Assumption**: Operations staff will define geofence boundaries for each trip type in
advance using the `POST /geofences` endpoint. Geofences do not need to be created in real
time at session start.

**Risk if invalid**: Trips without configured geofences cannot enforce boundary violations.
This creates a safety gap for newly added trip types.

**Mitigation**: Per ADR-005 (safe defaults), if no geofence is configured for a trip, the
system defaults to logging a warning every 10 minutes rather than skipping boundary checks
entirely. Safety officers are alerted that a trip is running without a configured geofence.

## A5: svc-emergency-response API Is Available for Programmatic Calls

**Assumption**: The existing svc-emergency-response `POST /emergencies` endpoint accepts
machine-generated requests (not just human-submitted SOS forms). The `triggered_by` field
in the request body can indicate the source as `system` (automated) vs. `guest` or `staff`.

**Risk if invalid**: If the endpoint validates that caller is human, automated emergency
creation will fail. The fallback is an asynchronous event (Kafka topic
`novatrek.tracking.emergency.triggered`) consumed by svc-emergency-response.

## A6: 90-Day Telemetry Retention Is Sufficient for Insurance

**Assumption**: The liability insurer requires GPS audit trails retained for at least 90 days
from adventure date. Longer retention (e.g., for litigation hold) is handled by manual
export to cold storage, not by the live telemetry API.

**Risk if invalid**: If the insurer requires 1+ years of hot storage, the TimescaleDB
compression configuration and storage budget will need revision.

**Mitigation**: TimescaleDB chunk compression after 30 days reduces storage cost by up to 95%.
Data beyond 90 days is archived to Azure Blob Storage via a scheduled job.

## A7: 200 Concurrent Adventures Is the Peak Load for the Next 12 Months

**Assumption**: NovaTrek's maximum concurrent adventure load in the next 12 months is
200 parties with an average party size of 8 guests, each transmitting every 2 minutes.
This yields approximately 1,600 telemetry events per 2-minute window (under 14 events/second).

**Risk if invalid**: If NovaTrek expands rapidly or acquires another operator, load could
exceed this estimate. The TimescaleDB time-series approach scales horizontally.

**Mitigation**: Horizontal scaling of the ingest worker is the primary scaling path.
Load testing should be performed before production launch.
