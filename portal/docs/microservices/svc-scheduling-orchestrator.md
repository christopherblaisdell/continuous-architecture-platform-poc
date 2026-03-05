---
tags:
  - microservice
  - svc-scheduling-orchestrator
  - operations
---

# svc-scheduling-orchestrator

**NovaTrek Scheduling Orchestrator API** &nbsp;|&nbsp; <span style="background: #2563eb15; color: #2563eb; border: 1px solid #2563eb40; padding: 0.15rem 0.6rem; border-radius: 1rem; font-size: 0.8rem; font-weight: 600;">Operations</span> &nbsp;|&nbsp; `v3.0.1` &nbsp;|&nbsp; *NovaTrek Platform Engineering*

> Central orchestration service for NovaTrek trip scheduling. Coordinates guide

[:material-api: Swagger UI](../services/api/svc-scheduling-orchestrator.html){ .md-button .md-button--primary }
[:material-file-download: Download OpenAPI Spec](../specs/svc-scheduling-orchestrator.yaml){ .md-button }

---

## :material-database: Data Store

| Property | Detail |
|----------|--------|
| **Engine** | PostgreSQL 15 + Redis 7 |
| **Schema** | `scheduling` |
| **Primary Tables** | `schedule_requests`, `daily_schedules`, `schedule_conflicts`, `optimization_runs` |
| **Key Features** | Optimistic locking per ADR-011 | Redis for schedule lock cache and optimization queue | JSONB columns for constraint parameters |
| **Estimated Volume** | ~500 schedule requests/day |

---

## :material-api: Endpoints (5 total)

---

### POST `/schedule-requests` -- Request optimal schedule for a trip { .endpoint-post }

> Submits a scheduling request that evaluates preferred dates against

[:material-open-in-new: View in Swagger UI](../services/api/svc-scheduling-orchestrator.html){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-scheduling-orchestrator--post-schedule-requests.svg" type="image/svg+xml" style="max-width: 100%;">POST /schedule-requests sequence diagram</object></div>

---

### GET `/schedule-requests/{request_id}` -- Get schedule request status and result { .endpoint-get }

> Poll this endpoint to retrieve the status and, once complete, the

[:material-open-in-new: View in Swagger UI](../services/api/svc-scheduling-orchestrator.html){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-scheduling-orchestrator--get-schedule-requests-request_id.svg" type="image/svg+xml" style="max-width: 100%;">GET /schedule-requests/{request_id} sequence diagram</object></div>

---

### GET `/schedule-optimization` -- Run synchronous schedule optimization { .endpoint-get }

> Performs a real-time scheduling optimization for a specific trip and

[:material-open-in-new: View in Swagger UI](../services/api/svc-scheduling-orchestrator.html){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-scheduling-orchestrator--get-schedule-optimization.svg" type="image/svg+xml" style="max-width: 100%;">GET /schedule-optimization sequence diagram</object></div>

---

### GET `/schedule-conflicts` -- List scheduling conflicts { .endpoint-get }

> Returns active scheduling conflicts for a given date and/or region.

[:material-open-in-new: View in Swagger UI](../services/api/svc-scheduling-orchestrator.html){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-scheduling-orchestrator--get-schedule-conflicts.svg" type="image/svg+xml" style="max-width: 100%;">GET /schedule-conflicts sequence diagram</object></div>

---

### POST `/schedule-conflicts/resolve` -- Resolve a scheduling conflict { .endpoint-post }

> Applies a resolution to an identified scheduling conflict. The resolution

[:material-open-in-new: View in Swagger UI](../services/api/svc-scheduling-orchestrator.html){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-scheduling-orchestrator--post-schedule-conflicts-resolve.svg" type="image/svg+xml" style="max-width: 100%;">POST /schedule-conflicts/resolve sequence diagram</object></div>
