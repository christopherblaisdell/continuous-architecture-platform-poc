# Service Architecture Pages

| | |
|-----------|-------|
| **Owner** | Architecture Practice |
| **Created** | 2026-03-03 |
| **Last Updated** | 2026-03-03 |
| **Services Documented** | 6 |

---

## Overview

Service architecture pages provide a consolidated view of each service's architectural identity — its purpose, integration points, active architecture decisions, and recent changes. These pages are the **corporate architecture baseline** for each service, maintained as a living document that is updated whenever a ticket-level solution design affects the service.

This is the artifact that the [PROMOTE step](../CLOSING-THE-LOOP.md) updates after each deployment.

---

## Service Index

| Service | Domain | Architecture Decisions | Last Updated |
|---------|--------|----------------------|--------------|
| [svc-check-in](svc-check-in.md) | Operations | 6 | 2026-03-03 |
| [svc-guest-profiles](svc-guest-profiles.md) | Guest Identity | 2 | 2026-03-03 |
| [svc-reservations](svc-reservations.md) | Booking | 2 | 2026-03-03 |
| [svc-scheduling-orchestrator](svc-scheduling-orchestrator.md) | Scheduling | 2 | 2026-03-03 |
| [svc-trail-management](svc-trail-management.md) | Trail Operations | 1 | 2026-03-03 |
| [svc-trip-catalog](svc-trip-catalog.md) | Product Catalog | 1 | 2026-03-03 |

---

## Services Referenced but Not Yet Documented

These services were referenced as dependencies in Phase 1 work but do not yet have architecture pages:

| Service | Referenced In | Role |
|---------|--------------|------|
| svc-gear-inventory | NTK-10003 | Equipment assignment during check-in |
| svc-guide-management | NTK-10004 | Guide schedule and preference data owner |
| svc-partner-integrations | NTK-10003 | External booking source fallback |
| svc-safety-compliance | NTK-10003 | Waiver validation during check-in |

These pages will be created when tickets directly modify these services.
