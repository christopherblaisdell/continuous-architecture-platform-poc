# Azure Microservices Delivery

**Date**: 2026-03-17
**Priority**: High (Priority #3)
**Status**: Active

## Goal

Code, test, and deploy all 22 NovaTrek microservices to Azure Container Apps. Every resource scales to zero when idle — this is a POC running on personal Azure credits.

## Current State

| Layer | Status |
|-------|--------|
| OpenAPI specs (22) | COMPLETE — `architecture/specs/` |
| Service scaffolds (22) | COMPLETE — `services/svc-*` with controllers, entities, repos, Flyway, Dockerfile |
| Bicep modules (13) | COMPLETE — `infra/modules/` (container-app, postgresql, redis, service-bus, key-vault, acr, monitoring, etc.) |
| CI/CD workflows (14) | COMPLETE — `service-ci.yml`, `service-cd.yml`, `infra-deploy.yml`, `ephemeral-env.yml`, nightly start/stop, etc. |
| Test methodology | COMPLETE — ADR-012, ADR-013, Cucumber, BDD, coverage gates (80%/70%) |
| Wave 0 infrastructure | COMPLETE — rg-novatrek-dev (eastus2), ACA env, ACR, PostgreSQL, Key Vault, Service Bus |
| Wave 1 tests (3 svc) | COMPLETE — 27 tests, H2 in-memory, all green |
| Wave 1 deployed | COMPLETE — container apps running, scale-to-zero, latest images in ACR |
| Wave 2 tests (3 svc) | COMPLETE — 34 tests, H2 in-memory, all green |
| Wave 2 deployed | COMPLETE — ca-svc-reservations, ca-svc-payments, ca-svc-notifications |
| Wave 3 tests (4 svc) | COMPLETE — 44 tests (check-in 10, scheduling 9, gear-inventory 11, safety-compliance 15) |
| Wave 3 deployed | COMPLETE — ca-svc-check-in, ca-svc-scheduling-orchestrator, ca-svc-gear-inventory, ca-svc-safety-compliance |
| Wave 4 tests (3 svc) | COMPLETE — 45 tests (guide-management 13, transport-logistics 16, location-services 16) |
| Wave 4 deployed | COMPLETE — ca-svc-guide-management, ca-svc-transport-logistics, ca-svc-location-services |
| Wave 5 tests (3 svc) | COMPLETE — 31 tests (analytics 9, loyalty-rewards 11, media-gallery 11) |
| Wave 5 deployed | COMPLETE — ca-svc-analytics, ca-svc-loyalty-rewards, ca-svc-media-gallery |
| Wave 6 tests (5 svc) | COMPLETE — 62 tests (partner-integrations 13, weather 7, inventory-procurement 13, emergency-response 13, wildlife-tracking 16) |
| Wave 6 deployed | COMPLETE — ca-svc-partner-integrations, ca-svc-weather, ca-svc-inventory-procurement, ca-svc-emergency-response, ca-svc-wildlife-tracking |

## Delivery Waves

| Wave | Services | Dependencies |
|------|----------|-------------|
| 0 — Foundation | Shared infra only (ACA env, ACR, PostgreSQL, Key Vault, Service Bus, monitoring) | Azure subscription, OIDC federation |
| 1 — Guest + Catalog | svc-guest-profiles, svc-trip-catalog, svc-trail-management | Wave 0 |
| 2 — Booking + Payments | svc-reservations, svc-payments, svc-notifications | Wave 1 |
| 3 — Operations | svc-check-in, svc-scheduling-orchestrator, svc-gear-inventory, svc-safety-compliance | Wave 2 |
| 4 — Guides + Transport | svc-guide-management, svc-transport-logistics, svc-location-services | Wave 1 |
| 5 — Analytics + Loyalty | svc-analytics, svc-loyalty-rewards, svc-media-gallery | Wave 1 |
| 6 — External + Safety | svc-partner-integrations, svc-weather, svc-inventory-procurement, svc-emergency-response, svc-wildlife-tracking | Wave 1 |
| 7 — New Capabilities | svc-reviews, svc-adventure-tracking, svc-referral-engine, svc-campaign-management | Solution designs |

## Cost Shield

- All Container Apps: `minReplicas: 0` (scale to zero)
- PostgreSQL: Burstable B1ms only, stopped nightly in dev
- Redis: Basic C0 or skip entirely in dev (use in-memory)
- Service Bus: Basic tier in dev
- ACR: Basic tier ($5/mo — only always-on cost)
- Budget alerts: $30/mo dev, $50/mo prod
- Target idle cost: $5/mo (ACR only)
- Target light-usage cost: $25-30/mo

## Post-Deployment Validation (2026-03-20)

### Health Check Results

All 21 services validated healthy via `/actuator/health` endpoint (21/21 PASS).

### Issues Found and Resolved

1. **Password authentication failure** — All 21 services were in crash loop. Root cause: per-service DB users from `infra/db/setup-schema-isolation.sql` were never created, and the admin password in Key Vault was out of sync with the PostgreSQL server.
2. **Fix applied** — Reset admin password via `az postgres flexible-server update --admin-password`, then updated all 21 Container Apps to use admin credentials (`novatrekadmin`) instead of per-service users. All services confirmed healthy after fix.
3. **Swagger UI** — Returns 404 on all services. No SpringDoc dependency in any `build.gradle.kts`. This is a separate enhancement if desired.

### Known Technical Debt

| Item | Status | Notes |
|------|--------|-------|
| Per-service DB users | NOT CREATED | `setup-schema-isolation.sql` never executed. All services use admin credentials. Port 5432 blocked by ISP — use Azure Cloud Shell to run SQL. |
| Temp firewall rule | ACTIVE | `temp-admin-access` (50.230.6.6) on PostgreSQL server. Can be removed. |
| SpringDoc/Swagger UI | MISSING | No `springdoc-openapi-starter-webmvc-ui` dependency in any service |
| service-cd.yml | FRAGILE | CD workflow does not preserve `SPRING_DATASOURCE_USERNAME`/`SPRING_DATASOURCE_PASSWORD` env vars on redeploy |

## Next Steps

1. Create per-service DB users (run `setup-schema-isolation.sql` via Azure Cloud Shell)
2. Update Container Apps to use per-service credentials
3. Fix `service-cd.yml` to preserve DB credential env vars on deploy
4. Write tests for Wave 7 services (svc-reviews, svc-adventure-tracking, svc-referral-engine, svc-campaign-management)
5. Build and deploy Wave 7 to ACA

## Deployed Container Apps

All apps: 0.25 CPU, 0.5Gi memory, min 0 / max 2, external ingress, port 8080.

| App | FQDN | Wave |
|-----|------|------|
| ca-svc-guest-profiles | ca-svc-guest-profiles.blackwater-fd4bc06d.eastus2.azurecontainerapps.io | 1 |
| ca-svc-trip-catalog | ca-svc-trip-catalog.blackwater-fd4bc06d.eastus2.azurecontainerapps.io | 1 |
| ca-svc-trail-management | ca-svc-trail-management.blackwater-fd4bc06d.eastus2.azurecontainerapps.io | 1 |
| ca-svc-reservations | ca-svc-reservations.blackwater-fd4bc06d.eastus2.azurecontainerapps.io | 2 |
| ca-svc-payments | ca-svc-payments.blackwater-fd4bc06d.eastus2.azurecontainerapps.io | 2 |
| ca-svc-notifications | ca-svc-notifications.blackwater-fd4bc06d.eastus2.azurecontainerapps.io | 2 |
| ca-svc-check-in | ca-svc-check-in.blackwater-fd4bc06d.eastus2.azurecontainerapps.io | 3 |
| ca-svc-scheduling-orchestrator | ca-svc-scheduling-orchestrator.blackwater-fd4bc06d.eastus2.azurecontainerapps.io | 3 |
| ca-svc-gear-inventory | ca-svc-gear-inventory.blackwater-fd4bc06d.eastus2.azurecontainerapps.io | 3 |
| ca-svc-safety-compliance | ca-svc-safety-compliance.blackwater-fd4bc06d.eastus2.azurecontainerapps.io | 3 |
| ca-svc-guide-management | ca-svc-guide-management.blackwater-fd4bc06d.eastus2.azurecontainerapps.io | 4 |
| ca-svc-transport-logistics | ca-svc-transport-logistics.blackwater-fd4bc06d.eastus2.azurecontainerapps.io | 4 |
| ca-svc-location-services | ca-svc-location-services.blackwater-fd4bc06d.eastus2.azurecontainerapps.io | 4 |
| ca-svc-analytics | ca-svc-analytics.blackwater-fd4bc06d.eastus2.azurecontainerapps.io | 5 |
| ca-svc-loyalty-rewards | ca-svc-loyalty-rewards.blackwater-fd4bc06d.eastus2.azurecontainerapps.io | 5 |
| ca-svc-media-gallery | ca-svc-media-gallery.blackwater-fd4bc06d.eastus2.azurecontainerapps.io | 5 |
| ca-svc-partner-integrations | ca-svc-partner-integrations.blackwater-fd4bc06d.eastus2.azurecontainerapps.io | 6 |
| ca-svc-weather | ca-svc-weather.blackwater-fd4bc06d.eastus2.azurecontainerapps.io | 6 |
| ca-svc-inventory-procurement | ca-svc-inventory-procurement.blackwater-fd4bc06d.eastus2.azurecontainerapps.io | 6 |
| ca-svc-emergency-response | ca-svc-emergency-response.blackwater-fd4bc06d.eastus2.azurecontainerapps.io | 6 |
| ca-svc-wildlife-tracking | ca-svc-wildlife-tracking.blackwater-fd4bc06d.eastus2.azurecontainerapps.io | 6 |

## Companion Document

[docs/AZURE-IMPLEMENTATION-PLAN.md](../../docs/AZURE-IMPLEMENTATION-PLAN.md)
