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
| Wave 5-6 tests + deploy | NOT STARTED |

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

1. Write tests for Wave 5 services (svc-analytics, svc-loyalty-rewards, svc-media-gallery)
2. Build and deploy Wave 5 to ACA
3. Write tests for Wave 6 services (svc-partner-integrations, svc-weather, svc-inventory-procurement, svc-emergency-response, svc-wildlife-tracking)
4. Build and deploy Wave 6 to ACA
5. Validate health checks and Swagger UI across all deployed services

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

## Companion Document

[docs/AZURE-IMPLEMENTATION-PLAN.md](../../docs/AZURE-IMPLEMENTATION-PLAN.md)
