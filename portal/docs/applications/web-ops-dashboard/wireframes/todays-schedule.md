# Operations Dashboard - Today's Schedule

Full daily adventure schedule table, organized into Morning, Afternoon, and Evening sections. Each row shows departure time, adventure name, guide assignment, guest count, check-in pattern (1-3), current status, and departure gate. Staff can filter by status, navigate to adjacent dates, and add or edit departure slots.

## Preview

<object data="../todays-schedule.svg" type="image/svg+xml" style="width: 100%; border: 1px solid #e0e0e0; border-radius: 4px;"></object>

## Interactive Viewer

**[Open Interactive Editor →](../todays-schedule.html)**

Open in the interactive Excalidraw viewer to explore the wireframe with zoom and pan controls.

## Design Notes

- **App**: Web Ops Dashboard
- **Flow Position**: Daily planning view — Operations Command
- **Status**: Draft
- **Source**: `architecture/wireframes/web-ops-dashboard/todays-schedule.excalidraw`

## Integration Points

### Backing Services

- **[svc-scheduling-orchestrator](../../../microservices/svc-scheduling-orchestrator/)** — Owns the schedule — all departure slots, timings, and guide assignments
- **[svc-guide-management](../../../microservices/svc-guide-management/)** — Supplies guide name, certification level, and availability
- **[svc-reservations](../../../microservices/svc-reservations/)** — Provides guest count and booking status per departure slot
- **[svc-trip-catalog](../../../microservices/svc-trip-catalog/)** — Supplies adventure name, duration, difficulty, and check-in pattern

## Feedback

To provide feedback or propose changes to this wireframe:

1. Download the Excalidraw source file from `architecture/wireframes/web-ops-dashboard/todays-schedule.excalidraw`
2. Edit at [excalidraw.com](https://excalidraw.com) or in VS Code with the Excalidraw extension
3. Submit updates via pull request

---

*This wireframe is maintained as part of NovaTrek Adventures enterprise architecture documentation.*
