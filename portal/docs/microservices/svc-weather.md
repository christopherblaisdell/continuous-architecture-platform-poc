---
tags:
  - microservice
  - svc-weather
  - support
---

# svc-weather

**NovaTrek Weather Service** &nbsp;|&nbsp; <span style="background: #64748b15; color: #64748b; border: 1px solid #64748b40; padding: 0.15rem 0.6rem; border-radius: 1rem; font-size: 0.8rem; font-weight: 600;">Support</span> &nbsp;|&nbsp; `v1.0.0` &nbsp;|&nbsp; *NovaTrek Platform Team*

> Integrates with on-site weather stations and third-party providers to deliver

[:material-api: Swagger UI](../services/api/svc-weather.html){ .md-button .md-button--primary }
[:material-file-download: Download OpenAPI Spec](../specs/svc-weather.yaml){ .md-button }
[:material-rocket-launch: Live Service (Dev)](https://ca-svc-weather.blackwater-fd4bc06d.eastus2.azurecontainerapps.io/actuator/health){ .md-button }
[:material-microsoft-azure: Azure Portal](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.App/containerApps/ca-svc-weather){ .md-button }
[:material-pipe: CI/CD Pipeline](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/actions/workflows/service-ci.yml){ .md-button }
[:material-source-branch: Source Code](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/tree/main/services/svc-weather){ .md-button }
[:material-language-java: Technology Stack](../technologies.md){ .md-button }

## :material-truck-delivery: Delivery Status

**Delivery Wave:** 6 -- External Integrations

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

- [:material-microsoft-azure: Container App](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.App/containerApps/ca-svc-weather)
- [:material-database: PostgreSQL Server](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.DBforPostgreSQL/flexibleServers/pg-novatrek-dev-smwd6ded4e3so)
- [:material-text-search: Log Analytics](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.OperationalInsights/workspaces/log-novatrek-dev/logs)

---

## :material-map: Integration Context

<div class="diagram-wrap"><a href="../svg/svc-weather--c4-context.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-weather--c4-context.svg" type="image/svg+xml" style="max-width: 100%;">svc-weather C4 context diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-weather.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-weather.yaml` + `cross-service-calls.yaml`</a>


## :material-database: Data Store { #data-store }

### Entity Relationship Diagram

<div class="diagram-wrap"><a href="../svg/svc-weather--erd.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-weather--erd.svg" type="image/svg+xml" style="max-width: 100%;">svc-weather entity relationship diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/metadata/data-stores.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/metadata/data-stores.yaml`</a>

### Overview

| Property | Detail |
|----------|--------|
| **Engine** | Valkey 8 + PostgreSQL 15 |
| **Schema** | `weather` |
| **Tables** | `weather_stations`, `forecast_cache`, `alert_history` |
| **Estimated Volume** | ~10K weather reads/day, ~100 external API fetches/day |
| **Connection Pool** | min 3 / max 10 / idle timeout 10min |
| **Backup Strategy** | Daily pg_dump, 7-day retention (cache data is ephemeral) |

### Key Features

- Valkey TTL cache for current conditions (5-min TTL)
- External weather API response caching and aggregation
- Severe weather alert deduplication

### Table Reference

#### `weather_stations`

*Registered weather station locations for data sourcing*

| Column | Type | Constraints |
|--------|------|-------------|
| `station_id` | `UUID` | PK |
| `name` | `VARCHAR(100)` | NOT NULL |
| `latitude` | `DECIMAL(9,6)` | NOT NULL |
| `longitude` | `DECIMAL(9,6)` | NOT NULL |
| `provider` | `VARCHAR(50)` | NOT NULL |
| `active` | `BOOLEAN` | NOT NULL, DEFAULT TRUE |

**Indexes:**

- `idx_ws_provider` on `provider`

#### `alert_history`

*Archived severe weather alerts with deduplication*

| Column | Type | Constraints |
|--------|------|-------------|
| `alert_id` | `UUID` | PK |
| `station_id` | `UUID` | NOT NULL, FK -> weather_stations |
| `alert_type` | `VARCHAR(50)` | NOT NULL |
| `severity` | `VARCHAR(20)` | NOT NULL |
| `message` | `TEXT` | NOT NULL |
| `external_id` | `VARCHAR(100)` | NOT NULL, UNIQUE (dedup key) |
| `issued_at` | `TIMESTAMPTZ` | NOT NULL |
| `expires_at` | `TIMESTAMPTZ` | NOT NULL |

**Indexes:**

- `idx_alert_station` on `station_id, issued_at DESC`
- `idx_alert_dedup` on `external_id` (UNIQUE)


---

## :material-api: Endpoints (5 total)

---

### GET `/weather/current` -- Get current weather conditions { .endpoint-get }

> Returns the latest weather data from the specified station, typically updated every 15 minutes.

[:material-open-in-new: View in Swagger UI](../services/api/svc-weather.html#/Weather/getCurrentWeather){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-weather--get-weather-current.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-weather--get-weather-current.svg" type="image/svg+xml" style="max-width: 100%;">GET /weather/current sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-weather.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-weather.yaml`</a>

---

### GET `/weather/forecast` -- Get weather forecast { .endpoint-get }

> Returns a multi-day forecast for the area covered by the specified weather station. Maximum 10-day lookahead.

[:material-open-in-new: View in Swagger UI](../services/api/svc-weather.html#/Weather/getWeatherForecast){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-weather--get-weather-forecast.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-weather--get-weather-forecast.svg" type="image/svg+xml" style="max-width: 100%;">GET /weather/forecast sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-weather.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-weather.yaml`</a>

---

### GET `/weather/alerts` -- Get active weather alerts for a region { .endpoint-get }

> Returns all active weather alerts for the specified region.

[:material-open-in-new: View in Swagger UI](../services/api/svc-weather.html#/Alerts/getWeatherAlerts){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-weather--get-weather-alerts.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-weather--get-weather-alerts.svg" type="image/svg+xml" style="max-width: 100%;">GET /weather/alerts sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-weather.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-weather.yaml`</a>

---

### POST `/weather/alerts` -- Create a weather alert (internal) { .endpoint-post }

> Internal endpoint used by automated monitoring systems or operations staff

[:material-open-in-new: View in Swagger UI](../services/api/svc-weather.html#/Alerts/createWeatherAlert){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-weather--post-weather-alerts.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-weather--post-weather-alerts.svg" type="image/svg+xml" style="max-width: 100%;">POST /weather/alerts sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-weather.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-weather.yaml`</a>

---

### GET `/trail-conditions` -- Get current trail conditions { .endpoint-get }

> Returns real-time condition data for the specified trail, combining weather station

[:material-open-in-new: View in Swagger UI](../services/api/svc-weather.html#/Trail%20Conditions/getTrailConditions){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-weather--get-trail-conditions.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-weather--get-trail-conditions.svg" type="image/svg+xml" style="max-width: 100%;">GET /trail-conditions sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-weather.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-weather.yaml`</a>

---

## :material-cellphone-link: Consuming Applications

| Application | Screens Using This Service |
|-------------|---------------------------|
| [Guest Portal](../../applications/web-guest-portal/) | Trip Browser |
| [Operations Dashboard](../../applications/web-ops-dashboard/) | Daily Schedule Board |
| [Adventure App](../../applications/app-guest-mobile/) | Live Trip Map, Weather and Trail Alerts |
