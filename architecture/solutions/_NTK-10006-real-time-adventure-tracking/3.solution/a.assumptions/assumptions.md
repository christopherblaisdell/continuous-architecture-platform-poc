<!-- PUBLISH -->

# NTK-10006 Assumptions

| ID | Assumption | Impact if Wrong |
|----|-----------|----------------|
| A1 | Wristband hardware can transmit GPS coordinates via cellular or LoRa at 30-second intervals | Architecture must accommodate alternative ingestion methods (batch upload, relay stations) |
| A2 | NTK-10005 (wristband RFID field) is implemented — `checkin.completed` event includes `wristband_nfc_id` | Cannot correlate tracking sessions to guests without this field; blocker |
| A3 | Trail boundary data is available in svc-location-services as polygon geometry | Geofence monitoring requires machine-readable boundaries; without them, geofencing is not possible |
| A4 | Peak concurrent active adventures is 500 guests simultaneously | Database and ingestion pipeline sized accordingly; higher volume requires infrastructure scaling review |
| A5 | Guest consent for GPS tracking is obtained during the check-in waiver signing process (svc-safety-compliance) | Legal and privacy review required if consent is obtained through a separate mechanism |
| A6 | The web-ops-dashboard can consume WebSocket connections for real-time map updates | If the frontend is polling-only, the real-time map will need a different delivery mechanism |
| A7 | Insurance tracking mandates require GPS-level precision (not just check-in/check-out timestamps) | If timestamp-only tracking satisfies the mandate, the GPS infrastructure is over-engineered |
