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
| **Engine** | Valkey 8 + PostgreSQL 15 |
| **Schema** | `weather` |
| **Primary Tables** | `weather_stations`, `forecast_cache`, `alert_history` |
| **Key Features** | Valkey TTL cache for current conditions (5-min TTL) | External weather API response caching and aggregation | Severe weather alert deduplication |
| **Estimated Volume** | ~10K weather reads/day, ~100 external API fetches/day |

---

## :material-api: Endpoints (5 total)

---

### GET `/weather/current` -- Get current weather conditions { .endpoint-get }

> Returns the latest weather data from the specified station, typically updated every 15 minutes.

[:material-open-in-new: View in Swagger UI](../services/api/svc-weather.html#/Weather/getCurrentWeather){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-weather--get-weather-current.svg" type="image/svg+xml" style="max-width: 100%;">GET /weather/current sequence diagram</object></div>

---

### GET `/weather/forecast` -- Get weather forecast { .endpoint-get }

> Returns a multi-day forecast for the area covered by the specified weather station. Maximum 10-day lookahead.

[:material-open-in-new: View in Swagger UI](../services/api/svc-weather.html#/Weather/getWeatherForecast){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-weather--get-weather-forecast.svg" type="image/svg+xml" style="max-width: 100%;">GET /weather/forecast sequence diagram</object></div>

---

### GET `/weather/alerts` -- Get active weather alerts for a region { .endpoint-get }

> Returns all active weather alerts for the specified region.

[:material-open-in-new: View in Swagger UI](../services/api/svc-weather.html#/Alerts/getWeatherAlerts){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-weather--get-weather-alerts.svg" type="image/svg+xml" style="max-width: 100%;">GET /weather/alerts sequence diagram</object></div>

---

### POST `/weather/alerts` -- Create a weather alert (internal) { .endpoint-post }

> Internal endpoint used by automated monitoring systems or operations staff

[:material-open-in-new: View in Swagger UI](../services/api/svc-weather.html#/Alerts/createWeatherAlert){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-weather--post-weather-alerts.svg" type="image/svg+xml" style="max-width: 100%;">POST /weather/alerts sequence diagram</object></div>

---

### GET `/trail-conditions` -- Get current trail conditions { .endpoint-get }

> Returns real-time condition data for the specified trail, combining weather station

[:material-open-in-new: View in Swagger UI](../services/api/svc-weather.html#/Trail%20Conditions/getTrailConditions){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-weather--get-trail-conditions.svg" type="image/svg+xml" style="max-width: 100%;">GET /trail-conditions sequence diagram</object></div>

---

## :material-cellphone-link: Consuming Applications

| Application | Screens Using This Service |
|-------------|---------------------------|
| [Guest Portal](../../applications/web-guest-portal/) | Trip Browser |
| [Operations Dashboard](../../applications/web-ops-dashboard/) | Daily Schedule Board |
| [Adventure App](../../applications/app-guest-mobile/) | Live Trip Map, Weather and Trail Alerts |
