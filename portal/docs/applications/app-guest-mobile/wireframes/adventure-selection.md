# Mobile App - Adventure Selection

Adventure discovery screen for the NovaTrek mobile guest app. Shows a horizontally scrollable row of activity category filter chips (All, Hiking, Kayaking, Climbing, Wildlife, Cycling) above a vertical list of adventure cards. Each card shows the adventure name, location, star rating, duration, difficulty, price per person, and slot availability. Fully booked adventures show a 'Join Waitlist' button.

## Preview

<object data="../adventure-selection.svg" type="image/svg+xml" style="width: 100%; border: 1px solid #e0e0e0; border-radius: 4px;"></object>

## Interactive Viewer

**[Open Interactive Editor →](../adventure-selection.html)**

Open in the interactive Excalidraw viewer to explore the wireframe with zoom and pan controls.

## Design Notes

- **App**: App Guest Mobile
- **Flow Position**: Discover tab — Mobile Guest App
- **Status**: Draft
- **Source**: `architecture/wireframes/app-guest-mobile/adventure-selection.excalidraw`

## Integration Points

### Backing Services

- **[svc-trip-catalog](../../../microservices/svc-trip-catalog/)** — Provides adventure listings, descriptions, pricing, and activity types
- **[svc-scheduling-orchestrator](../../../microservices/svc-scheduling-orchestrator/)** — Supplies real-time slot availability and remaining capacity
- **[svc-trail-management](../../../microservices/svc-trail-management/)** — Provides trail difficulty, distance, and location data
- **[svc-weather](../../../microservices/svc-weather/)** — Optionally surfaces weather advisories for each adventure location

## Feedback

To provide feedback or propose changes to this wireframe:

1. Download the Excalidraw source file from `architecture/wireframes/app-guest-mobile/adventure-selection.excalidraw`
2. Edit at [excalidraw.com](https://excalidraw.com) or in VS Code with the Excalidraw extension
3. Submit updates via pull request

---

*This wireframe is maintained as part of NovaTrek Adventures enterprise architecture documentation.*
