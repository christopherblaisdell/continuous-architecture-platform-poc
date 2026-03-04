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

---

## :material-database: Data Store

| Property | Detail |
|----------|--------|
| **Engine** | Redis 7 + PostgreSQL 15 |
| **Schema** | `weather` |
| **Primary Tables** | `weather_stations`, `forecast_cache`, `alert_history` |
| **Key Features** | Redis TTL cache for current conditions (5-min TTL) · External weather API response caching and aggregation · Severe weather alert deduplication |
| **Estimated Volume** | ~10K weather reads/day, ~100 external API fetches/day |

---

## :material-api: Endpoints (5 total)

---

### GET `/weather/current` — Get current weather conditions { .endpoint-get }

> Returns the latest weather data from the specified station, typically updated every 15 minutes.

[:material-open-in-new: View in Swagger UI](../services/api/svc-weather.html#/Weather/getCurrentWeather){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant ExtWx as Weather API
    participant Repo as Repository
    participant DB as Redis

    C->>+GW: GET /weather/current
    GW->>+Ctrl: Route request
    Ctrl->>+Svc: getCurrentWeather()

    rect rgba(199, 123, 48, 0.08)
        Note over Svc,ExtWx: Cross-service integration
        Svc->>+ExtWx: Fetch current conditions
        ExtWx-->>-Svc: OK
    end

    Svc->>+Repo: findByFilters(criteria)
    Repo->>+DB: SELECT ... WHERE filters
    DB-->>-Repo: ResultSet
    Repo-->>-Svc: Page of results

    Svc-->>-Ctrl: Result
    Ctrl-->>-GW: Response
    GW-->>-C: 200 OK
```

---

### GET `/weather/forecast` — Get weather forecast { .endpoint-get }

> Returns a multi-day forecast for the area covered by the specified weather station. Maximum 10-day lookahead.

[:material-open-in-new: View in Swagger UI](../services/api/svc-weather.html#/Weather/getWeatherForecast){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant ExtWx as Weather API
    participant Repo as Repository
    participant DB as Redis

    C->>+GW: GET /weather/forecast
    GW->>+Ctrl: Route request
    Ctrl->>+Svc: getWeatherForecast()

    rect rgba(199, 123, 48, 0.08)
        Note over Svc,ExtWx: Cross-service integration
        Svc->>+ExtWx: Fetch multi-day forecast
        ExtWx-->>-Svc: OK
    end

    Svc->>+Repo: findByFilters(criteria)
    Repo->>+DB: SELECT ... WHERE filters
    DB-->>-Repo: ResultSet
    Repo-->>-Svc: Page of results

    Svc-->>-Ctrl: Result
    Ctrl-->>-GW: Response
    GW-->>-C: 200 OK
```

---

### GET `/weather/alerts` — Get active weather alerts for a region { .endpoint-get }

> Returns all active weather alerts for the specified region.

[:material-open-in-new: View in Swagger UI](../services/api/svc-weather.html#/Alerts/getWeatherAlerts){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant ExtWx as Weather API
    participant Repo as Repository
    participant DB as Redis

    C->>+GW: GET /weather/alerts
    GW->>+Ctrl: Route request
    Ctrl->>+Svc: getWeatherAlerts()

    rect rgba(199, 123, 48, 0.08)
        Note over Svc,ExtWx: Cross-service integration
        Svc->>+ExtWx: Fetch active alerts
        ExtWx-->>-Svc: OK
    end

    Svc->>+Repo: findByFilters(criteria)
    Repo->>+DB: SELECT ... WHERE filters
    DB-->>-Repo: ResultSet
    Repo-->>-Svc: Page of results

    Svc-->>-Ctrl: Result
    Ctrl-->>-GW: Response
    GW-->>-C: 200 OK
```

---

### POST `/weather/alerts` — Create a weather alert (internal) { .endpoint-post }

> Internal endpoint used by automated monitoring systems or operations staff

[:material-open-in-new: View in Swagger UI](../services/api/svc-weather.html#/Alerts/createWeatherAlert){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as Redis

    C->>+GW: POST /weather/alerts
    GW->>+Ctrl: Route request
    Note right of Ctrl: Validate request body
    Ctrl->>+Svc: createWeatherAlert()

    Svc->>+Repo: save(entity)
    Repo->>+DB: INSERT INTO ...
    DB-->>-Repo: Created row
    Repo-->>-Svc: Persisted entity

    Svc-->>-Ctrl: Result
    Ctrl-->>-GW: Response
    GW-->>-C: 201 Created
```

---

### GET `/trail-conditions` — Get current trail conditions { .endpoint-get }

> Returns real-time condition data for the specified trail, combining weather station

[:material-open-in-new: View in Swagger UI](../services/api/svc-weather.html#/Trail%20Conditions/getTrailConditions){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as Redis

    C->>+GW: GET /trail-conditions
    GW->>+Ctrl: Route request
    Ctrl->>+Svc: getTrailConditions()

    Svc->>+Repo: findByFilters(criteria)
    Repo->>+DB: SELECT ... WHERE filters
    DB-->>-Repo: ResultSet
    Repo-->>-Svc: Page of results

    Svc-->>-Ctrl: Result
    Ctrl-->>-GW: Response
    GW-->>-C: 200 OK
```
