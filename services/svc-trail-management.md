# svc-trail-management — Service Architecture Page

| | |
|-----------|-------|
| **Service** | svc-trail-management |
| **Domain** | Trail Operations |
| **Team** | NovaTrek Platform Team |
| **API Version** | 1.0.0 |
| **Base URL** | `https://api.novatrek.example.com/trails/v1` |
| **Last Updated** | 2026-03-03 |

---

## Purpose

Manages trail definitions, waypoints, difficulty ratings, closures, and real-time condition status for all NovaTrek Adventures trail networks. Serves as the system of record for trail geography and operational state.

---

## Architecture Decisions

| ADR | Title | Status | Impact |
|-----|-------|--------|--------|
| [ADR-003](../decisions/ADR-003-nullable-elevation-fields.md) | Nullable Elevation Fields | Accepted | `elevation_gain_meters` and `elevation_loss_meters` are nullable — `null` means no data, `0` means flat |

---

## Integration Points

| Direction | Service | Purpose |
|-----------|---------|---------|
| ← Called by | svc-scheduling-orchestrator | Trail conditions for schedule optimization |
| ← Called by | svc-trip-catalog | Trail data for trip definitions |

---

## Key Patterns

- **Nullable Data Fields**: New data fields added to trail responses use nullable semantics to avoid blocking deployment on data backfill. Consumers must handle `null` explicitly. See [ADR-003](../decisions/ADR-003-nullable-elevation-fields.md).
- **Incremental Data Population**: Trail elevation data is populated incrementally as surveys complete — no big-bang backfill required.

---

## Recent Changes

| Ticket | Change | Date |
|--------|--------|------|
| NTK-10001 | Added `elevation_gain_meters` and `elevation_loss_meters` nullable fields to trail response | Phase 1 |

---

## Source Code

- [OpenAPI Spec](../phase-1-ai-tool-cost-comparison/workspace/corporate-services/services/svc-trail-management.yaml)

---

## Technical Debt and Open Questions

- No source code in the workspace for this service (API spec only) — source code location TBD
- Elevation data population status: unknown percentage of trails have elevation data populated
