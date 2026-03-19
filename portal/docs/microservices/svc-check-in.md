---
tags:
  - microservice
  - svc-check-in
  - operations
---

# svc-check-in

**NovaTrek Check-In Service** &nbsp;|&nbsp; <span style="background: #2563eb15; color: #2563eb; border: 1px solid #2563eb40; padding: 0.15rem 0.6rem; border-radius: 1rem; font-size: 0.8rem; font-weight: 600;">Operations</span> &nbsp;|&nbsp; `v1.0.0` &nbsp;|&nbsp; *NovaTrek Operations Team*

> Handles day-of-adventure check-in workflow including wristband assignment,

[:material-api: Swagger UI](../services/api/svc-check-in.html){ .md-button .md-button--primary }
[:material-file-download: Download OpenAPI Spec](../specs/svc-check-in.yaml){ .md-button }
[:material-rocket-launch: Live Service (Dev)](https://ca-svc-check-in.blackwater-fd4bc06d.eastus2.azurecontainerapps.io/actuator/health){ .md-button }
[:material-microsoft-azure: Azure Portal](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.App/containerApps/ca-svc-check-in){ .md-button }
[:material-pipe: CI/CD Pipeline](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/actions/workflows/service-ci.yml){ .md-button }
[:material-source-branch: Source Code](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/tree/main/services/svc-check-in){ .md-button }
[:material-language-java: Technology Stack](../technologies.md){ .md-button }

## :material-truck-delivery: Delivery Status

**Delivery Wave:** 3 -- Day-of-Adventure Operations

| Stage | Status |
|-------|--------|
| Infrastructure (Bicep) | :white_check_mark: complete |
| Database Schema (Flyway) | :white_check_mark: complete |
| Deployed to Dev | :white_check_mark: complete |
| Smoke Tested | :white_check_mark: complete |
| Deployed to Prod | :material-circle-outline: not-started |


| Pipeline | Status |
|----------|--------|
| CI Pipeline | :white_check_mark: complete |
| CD Pipeline | :white_check_mark: complete |

**Azure Resources (Dev):**

- [:material-microsoft-azure: Container App](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.App/containerApps/ca-svc-check-in)
- [:material-database: PostgreSQL Server](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.DBforPostgreSQL/flexibleServers/pg-novatrek-dev-smwd6ded4e3so)
- [:material-text-search: Log Analytics](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.OperationalInsights/workspaces/log-novatrek-dev/logs)

---

## :material-map: Integration Context

<div class="diagram-wrap"><a href="../svg/svc-check-in--c4-context.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-check-in--c4-context.svg" type="image/svg+xml" style="max-width: 100%;">svc-check-in C4 context diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-check-in.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-check-in.yaml` + `cross-service-calls.yaml`</a>


## :material-database: Data Store { #data-store }

### Entity Relationship Diagram

<div class="diagram-wrap"><a href="../svg/svc-check-in--erd.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-check-in--erd.svg" type="image/svg+xml" style="max-width: 100%;">svc-check-in entity relationship diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/metadata/data-stores.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/metadata/data-stores.yaml`</a>

### Overview

| Property | Detail |
|----------|--------|
| **Engine** | PostgreSQL 15 |
| **Schema** | `checkin` |
| **Tables** | `check_ins`, `gear_verifications`, `wristband_assignments` |
| **Estimated Volume** | ~5,000 check-ins/day peak season |
| **Connection Pool** | min 5 / max 20 / idle timeout 10min |
| **Backup Strategy** | Continuous WAL archiving, daily base backup, 7-day PITR |

### Key Features

- Indexes on reservation_id and check_in_date
- TTL-based cleanup of stale check-ins (older than 24h)
- Composite unique constraint on (reservation_id, participant_id)

### Table Reference

#### `check_ins`

*Primary check-in records for each guest arrival*

| Column | Type | Constraints |
|--------|------|-------------|
| `check_in_id` | `UUID` | PK, DEFAULT gen_random_uuid() |
| `reservation_id` | `UUID` | NOT NULL, FK -> svc-reservations |
| `participant_id` | `UUID` | NOT NULL |
| `guest_id` | `UUID` | NOT NULL |
| `adventure_category` | `VARCHAR(50)` | NOT NULL |
| `check_in_pattern` | `SMALLINT` | NOT NULL, CHECK (1-3) |
| `status` | `VARCHAR(20)` | NOT NULL, DEFAULT 'pending' |
| `checked_in_at` | `TIMESTAMPTZ` | DEFAULT NOW() |
| `checked_in_by` | `VARCHAR(100)` | NULL (staff ID or 'self') |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT NOW() |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT NOW() |

**Indexes:**

- `idx_checkin_reservation` on `reservation_id`
- `idx_checkin_date` on `checked_in_at`
- `idx_checkin_guest` on `guest_id, checked_in_at DESC`
- `uq_checkin_participant` on `reservation_id, participant_id` (UNIQUE)

#### `gear_verifications`

*Gear assignment verification records linked to check-ins*

| Column | Type | Constraints |
|--------|------|-------------|
| `verification_id` | `UUID` | PK |
| `check_in_id` | `UUID` | NOT NULL, FK -> check_ins |
| `gear_assignment_id` | `UUID` | NOT NULL |
| `verified_by` | `VARCHAR(100)` | NOT NULL |
| `status` | `VARCHAR(20)` | NOT NULL |
| `notes` | `TEXT` | NULL |
| `verified_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT NOW() |

**Indexes:**

- `idx_gear_ver_checkin` on `check_in_id`

#### `wristband_assignments`

*Digital wristband NFC assignments for checked-in guests*

| Column | Type | Constraints |
|--------|------|-------------|
| `assignment_id` | `UUID` | PK |
| `check_in_id` | `UUID` | NOT NULL, FK -> check_ins |
| `wristband_nfc_id` | `VARCHAR(64)` | NOT NULL, UNIQUE |
| `active` | `BOOLEAN` | NOT NULL, DEFAULT TRUE |
| `assigned_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT NOW() |
| `deactivated_at` | `TIMESTAMPTZ` | NULL |

**Indexes:**

- `idx_wristband_nfc` on `wristband_nfc_id` (UNIQUE)
- `idx_wristband_checkin` on `check_in_id`


---

## :material-lightbulb: Solutions Affecting This Service

| Ticket | Solution | Capabilities | Date |
|--------|----------|-------------|------|
| NTK-10002 | [Adventure Category Classification for Check-In UI Patterns](../solutions/_NTK-10002-adventure-category-classification.md) | `CAP-2.1`, `CAP-1.2` | 2025-02-10 |
| NTK-10005 | [Add Wristband RFID Field to Check-In Record](../solutions/_NTK-10005-wristband-rfid-field.md) | `CAP-2.1` | 2025-02-08 |

---

## :material-api: Endpoints (5 total)

---

### GET `/check-ins` -- List check-ins by reservation { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-check-in.html#/Check-Ins/listCheckIns){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-check-in--get-check-ins.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-check-in--get-check-ins.svg" type="image/svg+xml" style="max-width: 100%;">GET /check-ins sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-check-in.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-check-in.yaml`</a>
<span class="diagram-source-subtitle">Auto-generated baseline — shows standard request flow. For detailed behavioral sequences, see the relevant <a href="/solutions/">solution design</a>.</span>

---

### POST `/check-ins` -- Initiate check-in for a participant { .endpoint-post }

> Begins the check-in process for a reservation participant. Validates that

[:material-open-in-new: View in Swagger UI](../services/api/svc-check-in.html#/Check-Ins/createCheckIn){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-check-in--post-check-ins.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-check-in--post-check-ins.svg" type="image/svg+xml" style="max-width: 100%;">POST /check-ins sequence diagram</object></div>
<span class="diagram-source diagram-source--override"><span class="diagram-source-icon">&#x270E;</span> Architect-authored — overrides auto-generated baseline</span>
<span class="diagram-source-subtitle">Source: <a href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/diagrams/endpoints/svc-check-in--post-check-ins.puml"><code>architecture/diagrams/endpoints/svc-check-in--post-check-ins.puml</code></a></span>

---

### GET `/check-ins/{check_in_id}` -- Get check-in details { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-check-in.html#/Check-Ins/getCheckIn){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-check-in--get-check-ins-check_in_id.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-check-in--get-check-ins-check_in_id.svg" type="image/svg+xml" style="max-width: 100%;">GET /check-ins/{check_in_id} sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-check-in.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-check-in.yaml`</a>
<span class="diagram-source-subtitle">Auto-generated baseline — shows standard request flow. For detailed behavioral sequences, see the relevant <a href="/solutions/">solution design</a>.</span>

---

### POST `/check-ins/{check_in_id}/gear-verification` -- Verify gear has been picked up and fitted { .endpoint-post }

> Records that the participant has received and been fitted with required

[:material-open-in-new: View in Swagger UI](../services/api/svc-check-in.html#/Check-Ins/verifyGear){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-check-in--post-check-ins-check_in_id-gear-verification.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-check-in--post-check-ins-check_in_id-gear-verification.svg" type="image/svg+xml" style="max-width: 100%;">POST /check-ins/{check_in_id}/gear-verification sequence diagram</object></div>
<span class="diagram-source diagram-source--override"><span class="diagram-source-icon">&#x270E;</span> Architect-authored — overrides auto-generated baseline</span>
<span class="diagram-source-subtitle">Source: <a href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/diagrams/endpoints/svc-check-in--post-check-ins-check_in_id-gear-verification.puml"><code>architecture/diagrams/endpoints/svc-check-in--post-check-ins-check_in_id-gear-verification.puml</code></a></span>

---

### POST `/check-ins/{check_in_id}/wristband-assignment` -- Assign RFID wristband to checked-in participant { .endpoint-post }

> Assigns a color-coded RFID wristband for tracking and access control

[:material-open-in-new: View in Swagger UI](../services/api/svc-check-in.html#/Check-Ins/assignWristband){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-check-in--post-check-ins-check_in_id-wristband-assignment.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-check-in--post-check-ins-check_in_id-wristband-assignment.svg" type="image/svg+xml" style="max-width: 100%;">POST /check-ins/{check_in_id}/wristband-assignment sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-check-in.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-check-in.yaml`</a>
<span class="diagram-source-subtitle">Auto-generated baseline — shows standard request flow. For detailed behavioral sequences, see the relevant <a href="/solutions/">solution design</a>.</span>

---

## :material-cellphone-link: Consuming Applications

| Application | Screens Using This Service |
|-------------|---------------------------|
| [Operations Dashboard](../../applications/web-ops-dashboard/) | Check-In Station |
| [Adventure App](../../applications/app-guest-mobile/) | Self Check-In, Digital Wristband |

---

## :material-broadcast: Events Published

| Event | Channel | Trigger | Consumers |
|-------|---------|---------|-----------|
| [`checkin.completed`](/events/#checkincompleted) | `novatrek.operations.checkin.completed` | [`POST /check-ins`](#post-check-ins-initiate-check-in-for-a-participant) | [svc-analytics](../svc-analytics/), [svc-notifications](../svc-notifications/) |
