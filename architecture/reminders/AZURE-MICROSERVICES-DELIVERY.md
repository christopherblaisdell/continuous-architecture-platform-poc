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
| Wave 2 tests + deploy | IN PROGRESS |
| Wave 3-4 tests + deploy | NOT STARTED |

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

## Next Steps

1. Provision Azure subscription and configure OIDC federation
2. Deploy Wave 0 shared infrastructure via `infra-deploy.yml`
3. Verify all 22 services compile locally (`./gradlew build` per service)
4. Write baseline tests for Wave 1 services (meet 80% coverage gate)
5. Build and push Docker images for Wave 1 to ACR
6. Deploy Wave 1 services to dev ACA environment
7. Validate health checks and Swagger UI access
8. Repeat for Waves 2-6

## Companion Document

[docs/AZURE-IMPLEMENTATION-PLAN.md](../../docs/AZURE-IMPLEMENTATION-PLAN.md)
