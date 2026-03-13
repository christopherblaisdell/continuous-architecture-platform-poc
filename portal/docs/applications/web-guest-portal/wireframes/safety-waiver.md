# Guest Portal - Safety Waiver

Digital liability waiver and safety acknowledgment screen (step 3 of 4). Presents the adventure-specific waiver text, a risk acknowledgment checklist, emergency contact confirmation, and a digital signature field. Submission records the signed waiver against the guest's reservation in svc-safety-compliance.

## Preview

<object data="../safety-waiver.svg" type="image/svg+xml" style="width: 100%; border: 1px solid #e0e0e0; border-radius: 4px;"></object>

## Interactive Viewer

**[Open Interactive Editor →](../safety-waiver.html)**

Open in the interactive Excalidraw viewer to explore the wireframe with zoom and pan controls.

## Design Notes

- **App**: Web Guest Portal
- **Flow Position**: Step 3 of 4 — Safety and Waiver
- **Status**: Draft
- **Source**: `architecture/wireframes/web-guest-portal/safety-waiver.excalidraw`

## Integration Points

### Backing Services

- **[svc-safety-compliance](../../../microservices/svc-safety-compliance/)** — Stores the signed waiver and marks check-in step as complete
- **[svc-guest-profiles](../../../microservices/svc-guest-profiles/)** — Pre-fills emergency contact information from the guest profile
- **[svc-reservations](../../../microservices/svc-reservations/)** — Provides adventure context (name, date, guide) for the waiver header

### Related Tickets

[NTK-10003](../../../tickets/NTK-10003/)

## Feedback

To provide feedback or propose changes to this wireframe:

1. Download the Excalidraw source file from `architecture/wireframes/web-guest-portal/safety-waiver.excalidraw`
2. Edit at [excalidraw.com](https://excalidraw.com) or in VS Code with the Excalidraw extension
3. Submit updates via pull request

---

*This wireframe is maintained as part of NovaTrek Adventures enterprise architecture documentation.*
