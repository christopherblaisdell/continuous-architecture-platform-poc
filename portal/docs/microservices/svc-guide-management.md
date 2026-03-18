---
tags:
  - microservice
  - svc-guide-management
  - guide-management
---

# svc-guide-management

**NovaTrek Guide Management Service** &nbsp;|&nbsp; <span style="background: #4f46e515; color: #4f46e5; border: 1px solid #4f46e540; padding: 0.15rem 0.6rem; border-radius: 1rem; font-size: 0.8rem; font-weight: 600;">Guide Management</span> &nbsp;|&nbsp; `v2.4.0` &nbsp;|&nbsp; *NovaTrek Platform Engineering*

> Manages adventure guides for NovaTrek Adventures, including guide profiles,

[:material-api: Swagger UI](../services/api/svc-guide-management.html){ .md-button .md-button--primary }
[:material-file-download: Download OpenAPI Spec](../specs/svc-guide-management.yaml){ .md-button }
[:material-rocket-launch: Live Service (Dev)](https://ca-svc-guide-management.blackwater-fd4bc06d.eastus2.azurecontainerapps.io/actuator/health){ .md-button }
[:material-microsoft-azure: Azure Portal](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.App/containerApps/ca-svc-guide-management){ .md-button }
[:material-pipe: CI/CD Pipeline](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/actions/workflows/service-ci.yml){ .md-button }
[:material-source-branch: Source Code](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/tree/main/services/svc-guide-management){ .md-button }
[:material-language-java: Technology Stack](../technologies.md){ .md-button }

## :material-truck-delivery: Delivery Status

**Delivery Wave:** 4 -- Guide and Transport Operations

| Stage | Status |
|-------|--------|
| Infrastructure (Bicep) | :white_check_mark: complete |
| Database Schema (Flyway) | :white_check_mark: complete |
| Deployed to Dev | :white_check_mark: complete |
| Smoke Tested | :white_check_mark: complete |
| Deployed to Prod | :material-circle-outline: not-started |

!!! info "Deployment Method"
    This service was deployed manually via Azure CLI. Automated CI/CD pipelines are not yet configured.

**Azure Resources (Dev):**

- [:material-microsoft-azure: Container App](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.App/containerApps/ca-svc-guide-management)
- [:material-database: PostgreSQL Server](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.DBforPostgreSQL/flexibleServers/pg-novatrek-dev-smwd6ded4e3so)
- [:material-text-search: Log Analytics](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.OperationalInsights/workspaces/log-novatrek-dev/logs)

---

## :material-map: Integration Context

<div class="diagram-wrap"><a href="../svg/svc-guide-management--c4-context.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-guide-management--c4-context.svg" type="image/svg+xml" style="max-width: 100%;">svc-guide-management C4 context diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-guide-management.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-guide-management.yaml` + `cross-service-calls.yaml`</a>


## :material-database: Data Store { #data-store }

### Entity Relationship Diagram

<div class="diagram-wrap"><a href="../svg/svc-guide-management--erd.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-guide-management--erd.svg" type="image/svg+xml" style="max-width: 100%;">svc-guide-management entity relationship diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/metadata/data-stores.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/metadata/data-stores.yaml`</a>

### Overview

| Property | Detail |
|----------|--------|
| **Engine** | PostgreSQL 15 |
| **Schema** | `guides` |
| **Tables** | `guides`, `certifications`, `guide_schedules`, `availability_windows`, `ratings` |
| **Estimated Volume** | ~100 schedule updates/day, ~500 availability queries/day |
| **Connection Pool** | min 3 / max 15 / idle timeout 10min |
| **Backup Strategy** | Daily pg_dump, 30-day retention |

### Key Features

- Certification expiry tracking with automated alerts
- Availability window overlap detection constraints
- Weighted rating aggregation with recency bias

### Table Reference

#### `guides`

*Adventure guide profiles and qualifications*

| Column | Type | Constraints |
|--------|------|-------------|
| `guide_id` | `UUID` | PK |
| `first_name` | `VARCHAR(100)` | NOT NULL |
| `last_name` | `VARCHAR(100)` | NOT NULL |
| `email` | `VARCHAR(255)` | NOT NULL, UNIQUE |
| `phone` | `VARCHAR(30)` | NOT NULL |
| `hire_date` | `DATE` | NOT NULL |
| `status` | `VARCHAR(20)` | NOT NULL, DEFAULT 'active' |
| `avg_rating` | `DECIMAL(3,2)` | NULL |
| `total_trips` | `INTEGER` | NOT NULL, DEFAULT 0 |

**Indexes:**

- `idx_guide_email` on `email` (UNIQUE)
- `idx_guide_status` on `status`
- `idx_guide_rating` on `avg_rating DESC NULLS LAST`

#### `certifications`

*Guide adventure certifications with expiry tracking*

| Column | Type | Constraints |
|--------|------|-------------|
| `cert_id` | `UUID` | PK |
| `guide_id` | `UUID` | NOT NULL, FK -> guides |
| `cert_type` | `VARCHAR(50)` | NOT NULL |
| `level` | `VARCHAR(20)` | NOT NULL |
| `issued_date` | `DATE` | NOT NULL |
| `expiry_date` | `DATE` | NOT NULL |
| `verified` | `BOOLEAN` | NOT NULL, DEFAULT FALSE |

**Indexes:**

- `idx_gcert_guide` on `guide_id`
- `idx_gcert_expiry` on `expiry_date`

#### `availability_windows`

*Time blocks when a guide is available for scheduling*

| Column | Type | Constraints |
|--------|------|-------------|
| `window_id` | `UUID` | PK |
| `guide_id` | `UUID` | NOT NULL, FK -> guides |
| `start_time` | `TIMESTAMPTZ` | NOT NULL |
| `end_time` | `TIMESTAMPTZ` | NOT NULL |
| `recurrence` | `VARCHAR(20)` | NULL |

**Indexes:**

- `idx_avail_guide_time` on `guide_id, start_time`

#### `ratings`

*Guest ratings and reviews for guides*

| Column | Type | Constraints |
|--------|------|-------------|
| `rating_id` | `UUID` | PK |
| `guide_id` | `UUID` | NOT NULL, FK -> guides |
| `guest_id` | `UUID` | NOT NULL |
| `trip_id` | `UUID` | NOT NULL |
| `score` | `SMALLINT` | NOT NULL, CHECK (1-5) |
| `comment` | `TEXT` | NULL |
| `rated_at` | `TIMESTAMPTZ` | NOT NULL |

**Indexes:**

- `idx_rating_guide` on `guide_id, rated_at DESC`


---

## :material-api: Endpoints (12 total)

---

### GET `/guides` -- Search guides with filters { .endpoint-get }

> Returns a paginated list of guides matching the specified filter criteria.

[:material-open-in-new: View in Swagger UI](../services/api/svc-guide-management.html#/Guides/searchGuides){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-guide-management--get-guides.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-guide-management--get-guides.svg" type="image/svg+xml" style="max-width: 100%;">GET /guides sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-guide-management.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-guide-management.yaml`</a>

---

### POST `/guides` -- Create a new guide profile { .endpoint-post }

> Registers a new adventure guide in the system.

[:material-open-in-new: View in Swagger UI](../services/api/svc-guide-management.html#/Guides/createGuide){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-guide-management--post-guides.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-guide-management--post-guides.svg" type="image/svg+xml" style="max-width: 100%;">POST /guides sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-guide-management.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-guide-management.yaml`</a>

---

### GET `/guides/{guide_id}` -- Get guide by ID { .endpoint-get }

> Retrieves the full profile for a specific guide.

[:material-open-in-new: View in Swagger UI](../services/api/svc-guide-management.html#/Guides/getGuide){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-guide-management--get-guides-guide_id.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-guide-management--get-guides-guide_id.svg" type="image/svg+xml" style="max-width: 100%;">GET /guides/{guide_id} sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-guide-management.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-guide-management.yaml`</a>

---

### PATCH `/guides/{guide_id}` -- Update guide profile { .endpoint-patch }

> Partially updates a guide profile. Only provided fields are modified.

[:material-open-in-new: View in Swagger UI](../services/api/svc-guide-management.html#/Guides/updateGuide){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-guide-management--patch-guides-guide_id.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-guide-management--patch-guides-guide_id.svg" type="image/svg+xml" style="max-width: 100%;">PATCH /guides/{guide_id} sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-guide-management.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-guide-management.yaml`</a>

---

### GET `/guides/{guide_id}/certifications` -- List guide certifications { .endpoint-get }

> Returns all certifications held by the specified guide.

[:material-open-in-new: View in Swagger UI](../services/api/svc-guide-management.html#/Certifications/getGuideCertifications){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-guide-management--get-guides-guide_id-certifications.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-guide-management--get-guides-guide_id-certifications.svg" type="image/svg+xml" style="max-width: 100%;">GET /guides/{guide_id}/certifications sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-guide-management.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-guide-management.yaml`</a>

---

### POST `/guides/{guide_id}/certifications` -- Add a certification to a guide { .endpoint-post }

> Records a new certification for the specified guide.

[:material-open-in-new: View in Swagger UI](../services/api/svc-guide-management.html#/Certifications/addGuideCertification){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-guide-management--post-guides-guide_id-certifications.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-guide-management--post-guides-guide_id-certifications.svg" type="image/svg+xml" style="max-width: 100%;">POST /guides/{guide_id}/certifications sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-guide-management.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-guide-management.yaml`</a>

---

### GET `/guides/{guide_id}/schedule` -- Get upcoming trip assignments { .endpoint-get }

> Returns the guide's upcoming scheduled trip assignments.

[:material-open-in-new: View in Swagger UI](../services/api/svc-guide-management.html#/Scheduling/getGuideSchedule){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-guide-management--get-guides-guide_id-schedule.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-guide-management--get-guides-guide_id-schedule.svg" type="image/svg+xml" style="max-width: 100%;">GET /guides/{guide_id}/schedule sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-guide-management.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-guide-management.yaml`</a>

---

### GET `/guides/{guide_id}/availability` -- Get guide availability windows { .endpoint-get }

> Returns the availability windows configured for this guide.

[:material-open-in-new: View in Swagger UI](../services/api/svc-guide-management.html#/Availability/getGuideAvailability){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-guide-management--get-guides-guide_id-availability.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-guide-management--get-guides-guide_id-availability.svg" type="image/svg+xml" style="max-width: 100%;">GET /guides/{guide_id}/availability sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-guide-management.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-guide-management.yaml`</a>

---

### POST `/guides/{guide_id}/availability` -- Set availability windows { .endpoint-post }

> Creates or updates availability windows for the guide.

[:material-open-in-new: View in Swagger UI](../services/api/svc-guide-management.html#/Availability/setGuideAvailability){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-guide-management--post-guides-guide_id-availability.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-guide-management--post-guides-guide_id-availability.svg" type="image/svg+xml" style="max-width: 100%;">POST /guides/{guide_id}/availability sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-guide-management.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-guide-management.yaml`</a>

---

### GET `/guides/{guide_id}/ratings` -- Get guest ratings and reviews { .endpoint-get }

> Returns paginated guest ratings and reviews for the specified guide.

[:material-open-in-new: View in Swagger UI](../services/api/svc-guide-management.html#/Ratings/getGuideRatings){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-guide-management--get-guides-guide_id-ratings.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-guide-management--get-guides-guide_id-ratings.svg" type="image/svg+xml" style="max-width: 100%;">GET /guides/{guide_id}/ratings sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-guide-management.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-guide-management.yaml`</a>

---

### POST `/guides/{guide_id}/ratings` -- Submit a guest rating { .endpoint-post }

> Records a guest rating and optional review for a guide.

[:material-open-in-new: View in Swagger UI](../services/api/svc-guide-management.html#/Ratings/submitGuideRating){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-guide-management--post-guides-guide_id-ratings.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-guide-management--post-guides-guide_id-ratings.svg" type="image/svg+xml" style="max-width: 100%;">POST /guides/{guide_id}/ratings sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-guide-management.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-guide-management.yaml`</a>

---

### GET `/guides/available` -- Find available guides for a date, activity, and region { .endpoint-get }

> Searches for guides who are available on the specified date, hold relevant

[:material-open-in-new: View in Swagger UI](../services/api/svc-guide-management.html#/Availability/findAvailableGuides){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-guide-management--get-guides-available.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-guide-management--get-guides-available.svg" type="image/svg+xml" style="max-width: 100%;">GET /guides/available sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-guide-management.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-guide-management.yaml`</a>

---

## :material-cellphone-link: Consuming Applications

| Application | Screens Using This Service |
|-------------|---------------------------|
| [Operations Dashboard](../../applications/web-ops-dashboard/) | Daily Schedule Board, Guide Assignment, Safety Incident Board |

---

## :material-broadcast-off: Events Consumed

| Event | Producer | Channel |
|-------|----------|---------|
| [`schedule.published`](/events/#schedulepublished) | [svc-scheduling-orchestrator](../svc-scheduling-orchestrator/) | `novatrek.operations.schedule.published` |
