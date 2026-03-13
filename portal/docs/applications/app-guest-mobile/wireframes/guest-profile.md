# Mobile App - Guest Profile

Guest profile screen showing loyalty tier status, points balance, and progress to the next tier (Bronze → Silver → Gold → Platinum). Below the loyalty card, a stats row shows total adventures, trail kilometres, and countries visited. The Upcoming Adventures section previews the next confirmed booking. The Account Settings section links to personal details, payment methods, notification preferences, and adventure preferences.

## Preview

<object data="../guest-profile.svg" type="image/svg+xml" style="width: 100%; border: 1px solid #e0e0e0; border-radius: 4px;"></object>

## Interactive Viewer

**[Open Interactive Editor →](../guest-profile.html)**

Open in the interactive Excalidraw viewer to explore the wireframe with zoom and pan controls.

## Design Notes

- **App**: App Guest Mobile
- **Flow Position**: Profile tab — Mobile Guest App
- **Status**: Draft
- **Source**: `architecture/wireframes/app-guest-mobile/guest-profile.excalidraw`

## Integration Points

### Backing Services

- **[svc-guest-profiles](../../../microservices/svc-guest-profiles/)** — Provides name, contact details, and profile metadata
- **[svc-loyalty-rewards](../../../microservices/svc-loyalty-rewards/)** — Supplies tier, points balance, and transaction history
- **[svc-reservations](../../../microservices/svc-reservations/)** — Provides upcoming and past booking records

## Feedback

To provide feedback or propose changes to this wireframe:

1. Download the Excalidraw source file from `architecture/wireframes/app-guest-mobile/guest-profile.excalidraw`
2. Edit at [excalidraw.com](https://excalidraw.com) or in VS Code with the Excalidraw extension
3. Submit updates via pull request

---

*This wireframe is maintained as part of NovaTrek Adventures enterprise architecture documentation.*
