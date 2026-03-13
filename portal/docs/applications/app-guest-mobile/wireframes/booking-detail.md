# Mobile App - Booking Detail

Mobile booking detail screen accessed from the My Trips tab. Displays a confirmed booking status badge, adventure name and departure time, a large QR code for day-of check-in at the gate kiosk, booking reference, guide name, meeting point, duration, what-to-bring list, cancellation policy, and loyalty points that will be earned. Also accessible from the push notification sent 24 hours before the adventure.

## Preview

<object data="../booking-detail.svg" type="image/svg+xml" style="width: 100%; border: 1px solid #e0e0e0; border-radius: 4px;"></object>

## Interactive Viewer

**[Open Interactive Editor →](../booking-detail.html)**

Open in the interactive Excalidraw viewer to explore the wireframe with zoom and pan controls.

## Design Notes

- **App**: App Guest Mobile
- **Flow Position**: My Trips tab — Mobile Guest App
- **Status**: Draft
- **Source**: `architecture/wireframes/app-guest-mobile/booking-detail.excalidraw`

## Integration Points

### Backing Services

- **[svc-reservations](../../../microservices/svc-reservations/)** — Provides booking status, reference, and party details
- **[svc-trip-catalog](../../../microservices/svc-trip-catalog/)** — Supplies adventure metadata including guide, meeting point, and what-to-bring
- **[svc-loyalty-rewards](../../../microservices/svc-loyalty-rewards/)** — Calculates estimated points to be earned on completion
- **[svc-notifications](../../../microservices/svc-notifications/)** — Pre-departure reminder links to this screen

### Related Tickets

[NTK-10003](../../../tickets/NTK-10003/)

## Feedback

To provide feedback or propose changes to this wireframe:

1. Download the Excalidraw source file from `architecture/wireframes/app-guest-mobile/booking-detail.excalidraw`
2. Edit at [excalidraw.com](https://excalidraw.com) or in VS Code with the Excalidraw extension
3. Submit updates via pull request

---

*This wireframe is maintained as part of NovaTrek Adventures enterprise architecture documentation.*
