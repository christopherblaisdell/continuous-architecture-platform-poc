# Guest Portal - Reservation Lookup

Landing screen for the guest self-check-in flow. Guests enter their booking reference number and last name, or their registered email address and last name, to look up an existing reservation before proceeding to identity verification and waiver signing.

## Preview

<object data="../reservation-lookup.svg" type="image/svg+xml" style="width: 100%; border: 1px solid #e0e0e0; border-radius: 4px;"></object>

## Interactive Viewer

**[Open Interactive Editor →](../reservation-lookup.html)**

Open in the interactive Excalidraw viewer to explore the wireframe with zoom and pan controls.

## Design Notes

- **App**: Web Guest Portal
- **Flow Position**: Step 1 of 4 — Reservation Lookup
- **Status**: Draft
- **Source**: `architecture/wireframes/web-guest-portal/reservation-lookup.excalidraw`

## Integration Points

### Backing Services

- **[svc-reservations](../../../microservices/svc-reservations/)** — Searches for matching reservation by reference or guest email
- **[svc-guest-profiles](../../../microservices/svc-guest-profiles/)** — Resolves guest identity from email address

### Related Tickets

[NTK-10003](../../../tickets/NTK-10003/)

## Feedback

To provide feedback or propose changes to this wireframe:

1. Download the Excalidraw source file from `architecture/wireframes/web-guest-portal/reservation-lookup.excalidraw`
2. Edit at [excalidraw.com](https://excalidraw.com) or in VS Code with the Excalidraw extension
3. Submit updates via pull request

---

*This wireframe is maintained as part of NovaTrek Adventures enterprise architecture documentation.*
