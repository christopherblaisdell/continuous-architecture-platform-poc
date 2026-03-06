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

<div class="diagram-wrap"><a href="../svg/svc-scheduling-orchestrator--c4-context.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-scheduling-orchestrator--c4-context.svg" type="image/svg+xml" style="max-width: 100%;">svc-scheduling-orchestrator C4 context diagram</object></div>


## :material-database: Data Store { #data-store }

### Overview

| Property | Detail |
|----------|--------|
| **Engine** | PostgreSQL 15 + Valkey 8 |
| **Schema** | `scheduling` |
| **Tables** | `schedule_requests`, `daily_schedules`, `schedule_conflicts`, `optimization_runs` |
| **Estimated Volume** | ~500 schedule requests/day |
| **Connection Pool** | min 5 / max 20 / idle timeout 10min |
| **Backup Strategy** | Continuous WAL archiving, daily base backup, 14-day PITR |

### Key Features

- Optimistic locking per ADR-011
- Valkey for schedule lock cache and optimization queue
- JSONB columns for constraint parameters

### Table Reference

#### `schedule_requests`

*Incoming requests to create or modify daily schedules*

| Column | Type | Constraints |
|--------|------|-------------|
| `request_id` | `UUID` | PK |
| `schedule_date` | `DATE` | NOT NULL |
| `requested_by` | `VARCHAR(100)` | NOT NULL |
| `status` | `VARCHAR(20)` | NOT NULL |
| `constraints` | `JSONB` | NOT NULL, DEFAULT '{}' |
| `created_at` | `TIMESTAMPTZ` | NOT NULL |

**Indexes:**

- `idx_sched_req_date` on `schedule_date`
- `idx_sched_req_status` on `status`

#### `daily_schedules`

*Published daily schedules with optimistic locking*

| Column | Type | Constraints |
|--------|------|-------------|
| `schedule_id` | `UUID` | PK |
| `schedule_date` | `DATE` | NOT NULL, UNIQUE |
| `assignments` | `JSONB` | NOT NULL |
| `_rev` | `INTEGER` | NOT NULL, DEFAULT 1 |
| `published_at` | `TIMESTAMPTZ` | NULL |
| `created_at` | `TIMESTAMPTZ` | NOT NULL |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL |

**Indexes:**

- `idx_daily_sched_date` on `schedule_date` (UNIQUE)

#### `schedule_conflicts`

*Detected conflicts during schedule optimization*

| Column | Type | Constraints |
|--------|------|-------------|
| `conflict_id` | `UUID` | PK |
| `schedule_id` | `UUID` | NOT NULL, FK -> daily_schedules |
| `conflict_type` | `VARCHAR(30)` | NOT NULL |
| `details` | `JSONB` | NOT NULL |
| `resolved` | `BOOLEAN` | NOT NULL, DEFAULT FALSE |
| `detected_at` | `TIMESTAMPTZ` | NOT NULL |

**Indexes:**

- `idx_conflict_schedule` on `schedule_id`

#### `optimization_runs`

*Execution history of schedule optimization algorithms*

| Column | Type | Constraints |
|--------|------|-------------|
| `run_id` | `UUID` | PK |
| `schedule_date` | `DATE` | NOT NULL |
| `algorithm` | `VARCHAR(30)` | NOT NULL |
| `duration_ms` | `INTEGER` | NOT NULL |
| `score` | `DECIMAL(5,2)` | NULL |
| `status` | `VARCHAR(20)` | NOT NULL |
| `started_at` | `TIMESTAMPTZ` | NOT NULL |
| `completed_at` | `TIMESTAMPTZ` | NULL |

**Indexes:**

- `idx_opt_run_date` on `schedule_date`


---

## :material-lightbulb: Solutions Affecting This Service

| Ticket | Solution | Capabilities | Date |
|--------|----------|-------------|------|
| NTK-10003 | [Support Unregistered Guest Self-Service Check-In](../solutions/_NTK-10003-unregistered-guest-self-checkin.md) | `CAP-2.1`, `CAP-1.1`, `CAP-1.3` | 2025-02-12 |
| NTK-10004 | [Guide Schedule Overwrite Bug in Scheduling Orchestrator](../solutions/_NTK-10004-guide-schedule-overwrite-bug.md) | `CAP-2.2` | 2025-02-05 |

---

## :material-api: Endpoints (5 total)

---

### POST `/schedule-requests` -- Request optimal schedule for a trip { .endpoint-post }

> Submits a scheduling request that evaluates preferred dates against

[:material-open-in-new: View in Swagger UI](../services/api/svc-scheduling-orchestrator.html){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-scheduling-orchestrator--post-schedule-requests.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-scheduling-orchestrator--post-schedule-requests.svg" type="image/svg+xml" style="max-width: 100%;">POST /schedule-requests sequence diagram</object></div>

---

### GET `/schedule-requests/{request_id}` -- Get schedule request status and result { .endpoint-get }

> Poll this endpoint to retrieve the status and, once complete, the

[:material-open-in-new: View in Swagger UI](../services/api/svc-scheduling-orchestrator.html){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-scheduling-orchestrator--get-schedule-requests-request_id.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-scheduling-orchestrator--get-schedule-requests-request_id.svg" type="image/svg+xml" style="max-width: 100%;">GET /schedule-requests/{request_id} sequence diagram</object></div>

---

### GET `/schedule-optimization` -- Run synchronous schedule optimization { .endpoint-get }

> Performs a real-time scheduling optimization for a specific trip and

[:material-open-in-new: View in Swagger UI](../services/api/svc-scheduling-orchestrator.html){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-scheduling-orchestrator--get-schedule-optimization.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-scheduling-orchestrator--get-schedule-optimization.svg" type="image/svg+xml" style="max-width: 100%;">GET /schedule-optimization sequence diagram</object></div>

---

### GET `/schedule-conflicts` -- List scheduling conflicts { .endpoint-get }

> Returns active scheduling conflicts for a given date and/or region.

[:material-open-in-new: View in Swagger UI](../services/api/svc-scheduling-orchestrator.html){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-scheduling-orchestrator--get-schedule-conflicts.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-scheduling-orchestrator--get-schedule-conflicts.svg" type="image/svg+xml" style="max-width: 100%;">GET /schedule-conflicts sequence diagram</object></div>

---

### POST `/schedule-conflicts/resolve` -- Resolve a scheduling conflict { .endpoint-post }

> Applies a resolution to an identified scheduling conflict. The resolution

[:material-open-in-new: View in Swagger UI](../services/api/svc-scheduling-orchestrator.html){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-scheduling-orchestrator--post-schedule-conflicts-resolve.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-scheduling-orchestrator--post-schedule-conflicts-resolve.svg" type="image/svg+xml" style="max-width: 100%;">POST /schedule-conflicts/resolve sequence diagram</object></div>

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
| [`emergency.triggered`](/events/#emergencytriggered) | [svc-emergency-response](../svc-emergency-response/) | `novatrek.safety.emergency.triggered` |
| [`wildlife_alert.issued`](/events/#wildlife_alertissued) | [svc-wildlife-tracking](../svc-wildlife-tracking/) | `novatrek.safety.wildlife-alert.issued` |
