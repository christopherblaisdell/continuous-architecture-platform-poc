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

## :material-map: Integration Context

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-scheduling-orchestrator--c4-context.svg" type="image/svg+xml" style="max-width: 100%;">svc-scheduling-orchestrator C4 context diagram</object></div>

<p style="text-align: right; margin-top: -0.5em;"><a href="../svg/svc-scheduling-orchestrator--c4-context.svg" target="_blank" title="Open diagram in full screen">:material-fullscreen: View full screen</a></p>

| Property | Detail |
|----------|--------|
| **Engine** | PostgreSQL 15 + Valkey 8 |
| **Schema** | `scheduling` |
| **Primary Tables** | `schedule_requests`, `daily_schedules`, `schedule_conflicts`, `optimization_runs` |
| **Key Features** | Optimistic locking per ADR-011 | Valkey for schedule lock cache and optimization queue | JSONB columns for constraint parameters |
| **Estimated Volume** | ~500 schedule requests/day |

---

## :material-api: Endpoints (5 total)

---

### POST `/schedule-requests` -- Request optimal schedule for a trip { .endpoint-post }

> Submits a scheduling request that evaluates preferred dates against

[:material-open-in-new: View in Swagger UI](../services/api/svc-scheduling-orchestrator.html){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-scheduling-orchestrator--post-schedule-requests.svg" type="image/svg+xml" style="max-width: 100%;">POST /schedule-requests sequence diagram</object></div>

<p style="text-align: right; margin-top: -0.5em;"><a href="../svg/svc-scheduling-orchestrator--post-schedule-requests.svg" target="_blank" title="Open diagram in full screen">:material-fullscreen: View full screen</a></p>

---

### GET `/schedule-requests/{request_id}` -- Get schedule request status and result { .endpoint-get }

> Poll this endpoint to retrieve the status and, once complete, the

[:material-open-in-new: View in Swagger UI](../services/api/svc-scheduling-orchestrator.html){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-scheduling-orchestrator--get-schedule-requests-request_id.svg" type="image/svg+xml" style="max-width: 100%;">GET /schedule-requests/{request_id} sequence diagram</object></div>

<p style="text-align: right; margin-top: -0.5em;"><a href="../svg/svc-scheduling-orchestrator--get-schedule-requests-request_id.svg" target="_blank" title="Open diagram in full screen">:material-fullscreen: View full screen</a></p>

---

### GET `/schedule-optimization` -- Run synchronous schedule optimization { .endpoint-get }

> Performs a real-time scheduling optimization for a specific trip and

[:material-open-in-new: View in Swagger UI](../services/api/svc-scheduling-orchestrator.html){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-scheduling-orchestrator--get-schedule-optimization.svg" type="image/svg+xml" style="max-width: 100%;">GET /schedule-optimization sequence diagram</object></div>

<p style="text-align: right; margin-top: -0.5em;"><a href="../svg/svc-scheduling-orchestrator--get-schedule-optimization.svg" target="_blank" title="Open diagram in full screen">:material-fullscreen: View full screen</a></p>

---

### GET `/schedule-conflicts` -- List scheduling conflicts { .endpoint-get }

> Returns active scheduling conflicts for a given date and/or region.

[:material-open-in-new: View in Swagger UI](../services/api/svc-scheduling-orchestrator.html){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-scheduling-orchestrator--get-schedule-conflicts.svg" type="image/svg+xml" style="max-width: 100%;">GET /schedule-conflicts sequence diagram</object></div>

<p style="text-align: right; margin-top: -0.5em;"><a href="../svg/svc-scheduling-orchestrator--get-schedule-conflicts.svg" target="_blank" title="Open diagram in full screen">:material-fullscreen: View full screen</a></p>

---

### POST `/schedule-conflicts/resolve` -- Resolve a scheduling conflict { .endpoint-post }

> Applies a resolution to an identified scheduling conflict. The resolution

[:material-open-in-new: View in Swagger UI](../services/api/svc-scheduling-orchestrator.html){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-scheduling-orchestrator--post-schedule-conflicts-resolve.svg" type="image/svg+xml" style="max-width: 100%;">POST /schedule-conflicts/resolve sequence diagram</object></div>

<p style="text-align: right; margin-top: -0.5em;"><a href="../svg/svc-scheduling-orchestrator--post-schedule-conflicts-resolve.svg" target="_blank" title="Open diagram in full screen">:material-fullscreen: View full screen</a></p>

---

## :material-cellphone-link: Consuming Applications

| Application | Screens Using This Service |
|-------------|---------------------------|
| [Operations Dashboard](../../applications/web-ops-dashboard/) | Daily Schedule Board, Guide Assignment |
| [Adventure App](../../applications/app-guest-mobile/) | Live Trip Map |

---

## :material-broadcast: Events Published

| Event | Channel | Trigger | Consumers |
|-------|---------|---------|-----------|
| [`schedule.published`](/events/#schedulepublished) | `novatrek.operations.schedule.published` | [`POST /schedule-requests`](#post-schedule-requests-request-optimal-schedule-for-a-trip) | [svc-guide-management](../svc-guide-management/), [svc-notifications](../svc-notifications/) |

---

## :material-broadcast-off: Events Consumed

| Event | Producer | Channel |
|-------|----------|---------|
| [`reservation.created`](/events/#reservationcreated) | [svc-reservations](../svc-reservations/) | `novatrek.booking.reservation.created` |
