# NTK-10005 - Assumptions

## Assumptions

| ID | Assumption | Risk if Wrong | Status |
|----|------------|---------------|--------|
| A1 | The RFID tag format is a hexadecimal string between 8 and 16 characters (regex: `^[A-F0-9]{8,16}$`), as specified in the ticket acceptance criteria. | Validation logic would need updating; kiosk firmware format may differ | Open |
| A2 | RFID uniqueness is scoped to active check-ins only (not globally unique across all historical records). Once a check-in is completed or cancelled, the RFID tag can be reassigned to a new guest. | If global uniqueness is required, the constraint and lookup logic become more complex | Open |
| A3 | The `rfid_tag` field is optional. Adventures that do not use wristband tracking will continue to work without it. | If RFID becomes mandatory, migration of existing check-in flows would be needed | Confirmed |
| A4 | Downstream services consuming check-in events (svc-guest-experience, svc-trail-management) will receive the RFID tag in the event payload but are not required to act on it in this phase. | If downstream services need immediate RFID processing, their scope increases | Open |
| A5 | Kiosk firmware supporting RFID scanning will ship in May 2026 (per Comment 1 in ticket). The API schema change should be deployed before the firmware release. | If the API is late, kiosks with new firmware will have no backend support for RFID data | Confirmed |
