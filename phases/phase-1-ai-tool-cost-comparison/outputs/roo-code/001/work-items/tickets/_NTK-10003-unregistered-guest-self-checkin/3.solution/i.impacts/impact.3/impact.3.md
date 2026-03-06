# NTK-10003: Impact 3 - svc-safety-compliance (MINOR)

## Service

**svc-safety-compliance** -- Manages safety waivers, certifications, and compliance requirements for adventures.

## Impact Level

MINOR -- Existing endpoint extended with a new query parameter.

## Changes Required

### Endpoint Extension

The existing `GET /safety-compliance/waivers` endpoint currently supports lookup by `guest_id`. It must be extended to also support lookup by `reservation_id` query parameter.

**New query parameter**:
```yaml
- name: reservation_id
  in: query
  required: false
  schema:
    type: string
    format: uuid
  description: Look up waiver status for all participants on a reservation
```

### Response Extension

When queried by `reservation_id`, the response should include waiver status for all participants on the reservation, not just a single guest. The response includes:

- `waiver_complete` (boolean) -- true only if ALL participants have completed waivers
- `waiver_url` (string, nullable) -- URL for digital waiver signing if any waiver is incomplete
- `pending_participants` (array) -- list of participants with incomplete waivers

### Compliance Flow for Unregistered Guests

When an unregistered guest checks in via kiosk and their waiver is incomplete:

1. The kiosk displays the digital waiver signing interface
2. The guest reads and signs the waiver on the kiosk touchscreen
3. The waiver is associated with the temporary guest profile ID
4. If the guest later creates a full account, the waiver transfers with the profile merge

## Estimated Effort

1 day (Wei Zhang, svc-safety-compliance)
