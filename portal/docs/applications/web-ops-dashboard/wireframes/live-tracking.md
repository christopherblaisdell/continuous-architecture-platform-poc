# Operations Dashboard - Live Tracking

Real-time GPS tracking of all active adventure groups. Displays a map with colour-coded group markers, an alert banner for SOS or delayed groups, a right-side panel listing all active adventures and their status, and a stats bar showing guests on trail, active alerts, guides on duty, and average emergency response time.

## Preview

<object data="../live-tracking.svg" type="image/svg+xml" style="width: 100%; border: 1px solid #e0e0e0; border-radius: 4px;"></object>

## Interactive Viewer

**[Open Interactive Editor →](../live-tracking.html)**

Open in the interactive Excalidraw viewer to explore the wireframe with zoom and pan controls.

## Design Notes

- **App**: Web Ops Dashboard
- **Flow Position**: Primary view — Operations Command
- **Status**: Draft
- **Source**: `architecture/wireframes/web-ops-dashboard/live-tracking.excalidraw`

## Integration Points

### Backing Services

- **[svc-location-services](../../../microservices/svc-location-services/)** — Provides real-time GPS coordinates for each active group
- **[svc-scheduling-orchestrator](../../../microservices/svc-scheduling-orchestrator/)** — Supplies the list of scheduled departures and guide assignments
- **[svc-safety-compliance](../../../microservices/svc-safety-compliance/)** — Flags groups with overdue waypoints or triggered SOS alerts
- **[svc-guide-management](../../../microservices/svc-guide-management/)** — Resolves guide name and contact from assignment records

### Related Tickets

[NTK-10006](../../../tickets/NTK-10006/)

## Feedback

To provide feedback or propose changes to this wireframe:

1. Download the Excalidraw source file from `architecture/wireframes/web-ops-dashboard/live-tracking.excalidraw`
2. Edit at [excalidraw.com](https://excalidraw.com) or in VS Code with the Excalidraw extension
3. Submit updates via pull request

---

*This wireframe is maintained as part of NovaTrek Adventures enterprise architecture documentation.*
