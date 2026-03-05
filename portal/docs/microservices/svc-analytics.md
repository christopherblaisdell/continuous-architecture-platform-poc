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

---

## :material-database: Data Store

| Property | Detail |
|----------|--------|
| **Engine** | Oracle Database 19c |
| **Schema** | `ANALYTICS` |
| **Primary Tables** | `BOOKING_METRICS`, `REVENUE_METRICS`, `UTILIZATION_METRICS`, `SATISFACTION_SCORES`, `SAFETY_METRICS`, `GUIDE_PERFORMANCE` |
| **Key Features** | Oracle Partitioning for time-series data (range partitioning by month) | Materialized views with fast refresh for real-time dashboards | Oracle Advanced Analytics (DBMS_PREDICTIVE_ANALYTICS) for trend forecasting |
| **Estimated Volume** | ~50K metric inserts/day (event-driven) |

---

## :material-api: Endpoints (6 total)

---

### GET `/analytics/bookings` -- Get booking analytics for a period { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-analytics.html#/Bookings/getBookingAnalytics){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-analytics--get-analytics-bookings.svg" type="image/svg+xml" style="max-width: 100%;">GET /analytics/bookings sequence diagram</object></div>

---

### GET `/analytics/revenue` -- Get revenue analytics for a period { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-analytics.html#/Revenue/getRevenueAnalytics){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-analytics--get-analytics-revenue.svg" type="image/svg+xml" style="max-width: 100%;">GET /analytics/revenue sequence diagram</object></div>

---

### GET `/analytics/utilization` -- Get resource utilization analytics { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-analytics.html#/Utilization/getUtilizationAnalytics){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-analytics--get-analytics-utilization.svg" type="image/svg+xml" style="max-width: 100%;">GET /analytics/utilization sequence diagram</object></div>

---

### GET `/analytics/guest-satisfaction` -- Get guest satisfaction metrics { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-analytics.html#/Guest%20Experience/getGuestSatisfaction){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-analytics--get-analytics-guest-satisfaction.svg" type="image/svg+xml" style="max-width: 100%;">GET /analytics/guest-satisfaction sequence diagram</object></div>

---

### GET `/analytics/safety-metrics` -- Get safety and incident metrics { .endpoint-get }

> Aggregates data from svc-safety-compliance incident reports.

[:material-open-in-new: View in Swagger UI](../services/api/svc-analytics.html#/Safety/getSafetyMetrics){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-analytics--get-analytics-safety-metrics.svg" type="image/svg+xml" style="max-width: 100%;">GET /analytics/safety-metrics sequence diagram</object></div>

---

### GET `/analytics/guide-performance/{guide_id}` -- Get performance metrics for a specific guide { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-analytics.html#/Staff/getGuidePerformance){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-analytics--get-analytics-guide-performance-guide_id.svg" type="image/svg+xml" style="max-width: 100%;">GET /analytics/guide-performance/{guide_id} sequence diagram</object></div>

---

## :material-cellphone-link: Consuming Applications

| Application | Screens Using This Service |
|-------------|---------------------------|
| [Operations Dashboard](../applications/web-ops-dashboard/) | Analytics Dashboard |
