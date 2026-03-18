---
tags:
  - microservice
  - svc-analytics
  - support
---

# svc-analytics

**NovaTrek Analytics Service** &nbsp;|&nbsp; <span style="background: #64748b15; color: #64748b; border: 1px solid #64748b40; padding: 0.15rem 0.6rem; border-radius: 1rem; font-size: 0.8rem; font-weight: 600;">Support</span> &nbsp;|&nbsp; `v1.3.0` &nbsp;|&nbsp; *NovaTrek Data & Insights Team*

> Provides operational analytics, reporting dashboards, and key performance

[:material-api: Swagger UI](../services/api/svc-analytics.html){ .md-button .md-button--primary }
[:material-file-download: Download OpenAPI Spec](../specs/svc-analytics.yaml){ .md-button }
[:material-rocket-launch: Live Service (Dev)](https://ca-svc-analytics.blackwater-fd4bc06d.eastus2.azurecontainerapps.io/actuator/health){ .md-button }
[:material-microsoft-azure: Azure Portal](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.App/containerApps/ca-svc-analytics){ .md-button }
[:material-pipe: CI/CD Pipeline](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/actions/workflows/service-ci.yml){ .md-button }
[:material-source-branch: Source Code](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/tree/main/services/svc-analytics){ .md-button }
[:material-language-java: Technology Stack](../technologies.md){ .md-button }

## :material-truck-delivery: Delivery Status

**Delivery Wave:** 5 -- Analytics, Loyalty, and Media

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

- [:material-microsoft-azure: Container App](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.App/containerApps/ca-svc-analytics)
- [:material-database: PostgreSQL Server](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.DBforPostgreSQL/flexibleServers/pg-novatrek-dev-smwd6ded4e3so)
- [:material-text-search: Log Analytics](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.OperationalInsights/workspaces/log-novatrek-dev/logs)

---

## :material-map: Integration Context

<div class="diagram-wrap"><a href="../svg/svc-analytics--c4-context.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-analytics--c4-context.svg" type="image/svg+xml" style="max-width: 100%;">svc-analytics C4 context diagram</object></div>


## :material-database: Data Store { #data-store }

### Entity Relationship Diagram

<div class="diagram-wrap"><a href="../svg/svc-analytics--erd.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-analytics--erd.svg" type="image/svg+xml" style="max-width: 100%;">svc-analytics entity relationship diagram</object></div>

### Overview

| Property | Detail |
|----------|--------|
| **Engine** | Oracle Database 19c |
| **Schema** | `ANALYTICS` |
| **Tables** | `BOOKING_METRICS`, `REVENUE_METRICS`, `UTILIZATION_METRICS`, `SATISFACTION_SCORES`, `SAFETY_METRICS`, `GUIDE_PERFORMANCE` |
| **Estimated Volume** | ~50K metric inserts/day (event-driven) |
| **Connection Pool** | min 5 / max 20 / idle timeout 10min |
| **Backup Strategy** | Oracle RMAN incremental backup, 90-day retention |

### Key Features

- Oracle Partitioning for time-series data (range partitioning by month)
- Materialized views with fast refresh for real-time dashboards
- Oracle Advanced Analytics (DBMS_PREDICTIVE_ANALYTICS) for trend forecasting

### Table Reference

#### `BOOKING_METRICS`

*Aggregated booking KPIs partitioned by month*

| Column | Type | Constraints |
|--------|------|-------------|
| `METRIC_ID` | `NUMBER(19)` | PK |
| `METRIC_DATE` | `DATE` | NOT NULL |
| `REGION_ID` | `VARCHAR2(36)` | NOT NULL |
| `BOOKINGS_COUNT` | `NUMBER(10)` | NOT NULL |
| `CANCELLATION_COUNT` | `NUMBER(10)` | NOT NULL, DEFAULT 0 |
| `TOTAL_REVENUE` | `NUMBER(12,2)` | NOT NULL |
| `AVG_PARTY_SIZE` | `NUMBER(4,1)` | NULL |
| `CREATED_AT` | `TIMESTAMP WITH TIME ZONE` | NOT NULL |

**Indexes:**

- `IDX_BM_DATE_REGION` on `METRIC_DATE, REGION_ID`

#### `REVENUE_METRICS`

*Daily revenue aggregation across payment channels*

| Column | Type | Constraints |
|--------|------|-------------|
| `METRIC_ID` | `NUMBER(19)` | PK |
| `METRIC_DATE` | `DATE` | NOT NULL |
| `CHANNEL` | `VARCHAR2(30)` | NOT NULL |
| `GROSS_REVENUE` | `NUMBER(12,2)` | NOT NULL |
| `REFUND_TOTAL` | `NUMBER(12,2)` | NOT NULL, DEFAULT 0 |
| `NET_REVENUE` | `NUMBER(12,2)` | GENERATED ALWAYS AS (GROSS_REVENUE - REFUND_TOTAL) |
| `TRANSACTION_COUNT` | `NUMBER(10)` | NOT NULL |

**Indexes:**

- `IDX_RM_DATE` on `METRIC_DATE`

#### `GUIDE_PERFORMANCE`

*Guide performance metrics for scheduling optimization*

| Column | Type | Constraints |
|--------|------|-------------|
| `METRIC_ID` | `NUMBER(19)` | PK |
| `GUIDE_ID` | `VARCHAR2(36)` | NOT NULL |
| `METRIC_DATE` | `DATE` | NOT NULL |
| `TRIPS_LED` | `NUMBER(5)` | NOT NULL |
| `AVG_RATING` | `NUMBER(3,2)` | NULL |
| `INCIDENTS_COUNT` | `NUMBER(5)` | NOT NULL, DEFAULT 0 |
| `UTILIZATION_PCT` | `NUMBER(5,2)` | NULL |

**Indexes:**

- `IDX_GP_GUIDE_DATE` on `GUIDE_ID, METRIC_DATE`


---

## :material-lightbulb: Solutions Affecting This Service

| Ticket | Solution | Capabilities | Date |
|--------|----------|-------------|------|
| NTK-10009 | [Refund and Dispute Management Workflows](../solutions/_NTK-10009-refund-dispute-management.md) | `CAP-5.5`, `CAP-5.4` | 2026-03-06 |

---

## :material-api: Endpoints (6 total)

---

### GET `/analytics/bookings` -- Get booking analytics for a period { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-analytics.html#/Bookings/getBookingAnalytics){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-analytics--get-analytics-bookings.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-analytics--get-analytics-bookings.svg" type="image/svg+xml" style="max-width: 100%;">GET /analytics/bookings sequence diagram</object></div>

---

### GET `/analytics/revenue` -- Get revenue analytics for a period { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-analytics.html#/Revenue/getRevenueAnalytics){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-analytics--get-analytics-revenue.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-analytics--get-analytics-revenue.svg" type="image/svg+xml" style="max-width: 100%;">GET /analytics/revenue sequence diagram</object></div>

---

### GET `/analytics/utilization` -- Get resource utilization analytics { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-analytics.html#/Utilization/getUtilizationAnalytics){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-analytics--get-analytics-utilization.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-analytics--get-analytics-utilization.svg" type="image/svg+xml" style="max-width: 100%;">GET /analytics/utilization sequence diagram</object></div>

---

### GET `/analytics/guest-satisfaction` -- Get guest satisfaction metrics { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-analytics.html#/Guest%20Experience/getGuestSatisfaction){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-analytics--get-analytics-guest-satisfaction.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-analytics--get-analytics-guest-satisfaction.svg" type="image/svg+xml" style="max-width: 100%;">GET /analytics/guest-satisfaction sequence diagram</object></div>

---

### GET `/analytics/safety-metrics` -- Get safety and incident metrics { .endpoint-get }

> Aggregates data from svc-safety-compliance incident reports.

[:material-open-in-new: View in Swagger UI](../services/api/svc-analytics.html#/Safety/getSafetyMetrics){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-analytics--get-analytics-safety-metrics.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-analytics--get-analytics-safety-metrics.svg" type="image/svg+xml" style="max-width: 100%;">GET /analytics/safety-metrics sequence diagram</object></div>

---

### GET `/analytics/guide-performance/{guide_id}` -- Get performance metrics for a specific guide { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-analytics.html#/Staff/getGuidePerformance){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-analytics--get-analytics-guide-performance-guide_id.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-analytics--get-analytics-guide-performance-guide_id.svg" type="image/svg+xml" style="max-width: 100%;">GET /analytics/guide-performance/{guide_id} sequence diagram</object></div>

---

## :material-cellphone-link: Consuming Applications

| Application | Screens Using This Service |
|-------------|---------------------------|
| [Operations Dashboard](../../applications/web-ops-dashboard/) | Analytics Dashboard |

---

## :material-broadcast-off: Events Consumed

| Event | Producer | Channel |
|-------|----------|---------|
| [`reservation.created`](/events/#reservationcreated) | [svc-reservations](../svc-reservations/) | `novatrek.booking.reservation.created` |
| [`reservation.status_changed`](/events/#reservationstatus_changed) | [svc-reservations](../svc-reservations/) | `novatrek.booking.reservation.status-changed` |
| [`guest.registered`](/events/#guestregistered) | [svc-guest-profiles](../svc-guest-profiles/) | `novatrek.guest-identity.guest.registered` |
| [`checkin.completed`](/events/#checkincompleted) | [svc-check-in](../svc-check-in/) | `novatrek.operations.checkin.completed` |
| [`incident.reported`](/events/#incidentreported) | [svc-safety-compliance](../svc-safety-compliance/) | `novatrek.safety.incident.reported` |
| [`emergency.triggered`](/events/#emergencytriggered) | [svc-emergency-response](../svc-emergency-response/) | `novatrek.safety.emergency.triggered` |
| [`wildlife_alert.issued`](/events/#wildlife_alertissued) | [svc-wildlife-tracking](../svc-wildlife-tracking/) | `novatrek.safety.wildlife-alert.issued` |
