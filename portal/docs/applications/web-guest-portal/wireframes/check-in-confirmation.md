# Guest Portal - Check-In Confirmation

Final confirmation screen (step 4 of 4) shown after the guest completes all check-in steps. Displays adventure details, guest information, safety and compliance status, wristband assignment, loyalty points earned, and action buttons to start the adventure, print a receipt, or view the trail map.

## Preview

<object data="../check-in-confirmation.svg" type="image/svg+xml" style="width: 100%; border: 1px solid #e0e0e0; border-radius: 4px;"></object>

## Interactive Viewer

**[Open Interactive Editor →](../check-in-confirmation.html)**

Open in the interactive Excalidraw viewer to explore the wireframe with zoom and pan controls.

## Design Notes

- **App**: Web Guest Portal
- **Flow Position**: Step 4 of 4 — Confirmation
- **Status**: Draft
- **Source**: `architecture/wireframes/web-guest-portal/check-in-confirmation.excalidraw`

## Integration Points

### Backing Services

- **[svc-check-in](../../../microservices/svc-check-in/)** — Records the completed check-in with wristband and gear status
- **[svc-reservations](../../../microservices/svc-reservations/)** — Supplies booking reference and party details
- **[svc-safety-compliance](../../../microservices/svc-safety-compliance/)** — Confirms waiver signed and safety briefing completed
- **[svc-loyalty-rewards](../../../microservices/svc-loyalty-rewards/)** — Calculates and awards TrailPoints for the completed check-in
- **[svc-notifications](../../../microservices/svc-notifications/)** — Sends confirmation to guest email and guide SMS

### Related Tickets

[NTK-10003](../../../tickets/NTK-10003/), [NTK-10005](../../../tickets/NTK-10005/)

## Feedback

To provide feedback or propose changes to this wireframe:

1. Download the Excalidraw source file from `architecture/wireframes/web-guest-portal/check-in-confirmation.excalidraw`
2. Edit at [excalidraw.com](https://excalidraw.com) or in VS Code with the Excalidraw extension
3. Submit updates via pull request

---

*This wireframe is maintained as part of NovaTrek Adventures enterprise architecture documentation.*
