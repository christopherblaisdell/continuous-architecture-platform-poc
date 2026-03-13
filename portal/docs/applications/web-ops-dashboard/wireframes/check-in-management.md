# Operations Dashboard - Check-In Management

Staff-facing check-in queue management for a single departure gate. The left panel shows the guest queue with status badges (Ready, Waiver Pending, Gear Check, ID Check, No Waiver, Payment Issue). The right panel shows full details for the selected guest: safety checklist, wristband colour and number assignment, and action controls (Complete Check-In, Hold, Skip, Flag Issue).

## Preview

<object data="../check-in-management.svg" type="image/svg+xml" style="width: 100%; border: 1px solid #e0e0e0; border-radius: 4px;"></object>

## Interactive Viewer

**[Open Interactive Editor →](../check-in-management.html)**

Open in the interactive Excalidraw viewer to explore the wireframe with zoom and pan controls.

## Design Notes

- **App**: Web Ops Dashboard
- **Flow Position**: Gate operations view — Operations Command
- **Status**: Draft
- **Source**: `architecture/wireframes/web-ops-dashboard/check-in-management.excalidraw`

## Integration Points

### Backing Services

- **[svc-check-in](../../../microservices/svc-check-in/)** — Processes each step: verifies gear, records wristband, finalises check-in
- **[svc-reservations](../../../microservices/svc-reservations/)** — Supplies booking details and party size for each guest in the queue
- **[svc-safety-compliance](../../../microservices/svc-safety-compliance/)** — Reports waiver status and flags guests with missing signatures
- **[svc-gear-inventory](../../../microservices/svc-gear-inventory/)** — Tracks equipment issue status for Pattern 2 and Pattern 3 adventures
- **[svc-notifications](../../../microservices/svc-notifications/)** — Sends check-in complete confirmation to guest and guide
- **[svc-analytics](../../../microservices/svc-analytics/)** — Logs check-in completion events for operational reporting

### Related Tickets

[NTK-10003](../../../tickets/NTK-10003/), [NTK-10005](../../../tickets/NTK-10005/)

## Feedback

To provide feedback or propose changes to this wireframe:

1. Download the Excalidraw source file from `architecture/wireframes/web-ops-dashboard/check-in-management.excalidraw`
2. Edit at [excalidraw.com](https://excalidraw.com) or in VS Code with the Excalidraw extension
3. Submit updates via pull request

---

*This wireframe is maintained as part of NovaTrek Adventures enterprise architecture documentation.*
