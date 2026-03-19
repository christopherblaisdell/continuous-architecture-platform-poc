# Architecture Decision Log

| | |
|-----------|-------|
| **Owner** | Architecture Practice |
| **Created** | 2026-03-01 |
| **Last Updated** | 2026-03-03 |
| **Total Decisions** | 13 |

---

## Overview

This is the global architecture decision log for the NovaTrek Adventures platform. Each ADR follows the [MADR](../phase-1-ai-tool-cost-comparison/workspace/architecture-standards/madr/README.md) (Markdown Any Decision Record) format and is numbered sequentially.

Decisions originate in ticket-level solution designs and are **promoted** to this global log when they affect corporate architecture baselines — service contracts, data models, integration patterns, or cross-cutting concerns.

---

## Decision Index

| ADR | Title | Status | Date | Services Affected | Origin |
|-----|-------|--------|------|-------------------|--------|
| [ADR-001](ADR-001-ai-toolchain-selection.md) | AI Toolchain Selection for Architecture Practice | Proposed | 2026-03-01 | — (practice-level) | Phase 1 |
| [ADR-002](ADR-002-documentation-publishing-platform.md) | Documentation Publishing Platform Selection | Proposed | 2025-01-27 | — (practice-level) | Phase 6 |
| [ADR-003](ADR-003-nullable-elevation-fields.md) | Use Nullable Fields for Elevation Data | Accepted | 2026-02-15 | svc-trail-management | NTK-10001 |
| [ADR-004](ADR-004-configuration-driven-classification.md) | Configuration-Driven Classification over Database-Driven | Accepted | 2024-08-14 | svc-check-in, svc-trip-catalog | NTK-10002 |
| [ADR-005](ADR-005-pattern3-default-fallback.md) | Pattern 3 as Default Fallback for Unknown Categories | Accepted | 2024-08-19 | svc-check-in | NTK-10002 |
| [ADR-006](ADR-006-orchestrator-pattern-checkin.md) | Orchestrator Pattern for Self-Service Check-In | Accepted | 2025-01-28 | svc-check-in, svc-reservations, svc-guest-profiles, svc-safety-compliance | NTK-10003 |
| [ADR-007](ADR-007-four-field-identity-verification.md) | Four-Field Identity Verification for Unregistered Guests | Accepted | 2025-01-28 | svc-check-in, svc-reservations | NTK-10003 |
| [ADR-008](ADR-008-temporary-guest-profile.md) | Temporary Guest Profile for Unregistered Check-In | Accepted | 2025-01-28 | svc-guest-profiles, svc-check-in | NTK-10003 |
| [ADR-009](ADR-009-session-scoped-kiosk-access.md) | Session-Scoped Kiosk Access for Self-Service Check-In | Accepted | 2025-01-28 | svc-check-in | NTK-10003 |
| [ADR-010](ADR-010-patch-semantics-schedule-updates.md) | Switch from PUT to PATCH Semantics for Schedule Updates | Proposed | 2026-02-28 | svc-scheduling-orchestrator | NTK-10004 |
| [ADR-011](ADR-011-optimistic-locking-daily-schedule.md) | Add Optimistic Locking to DailySchedule Entity | Proposed | 2026-02-28 | svc-scheduling-orchestrator | NTK-10004 |

---

## Decisions by Service

| Service | Decisions |
|---------|-----------|
| svc-check-in | [ADR-004](ADR-004-configuration-driven-classification.md), [ADR-005](ADR-005-pattern3-default-fallback.md), [ADR-006](ADR-006-orchestrator-pattern-checkin.md), [ADR-007](ADR-007-four-field-identity-verification.md), [ADR-008](ADR-008-temporary-guest-profile.md), [ADR-009](ADR-009-session-scoped-kiosk-access.md) |
| svc-guest-profiles | [ADR-006](ADR-006-orchestrator-pattern-checkin.md), [ADR-008](ADR-008-temporary-guest-profile.md) |
| svc-reservations | [ADR-006](ADR-006-orchestrator-pattern-checkin.md), [ADR-007](ADR-007-four-field-identity-verification.md) |
| svc-scheduling-orchestrator | [ADR-010](ADR-010-patch-semantics-schedule-updates.md), [ADR-011](ADR-011-optimistic-locking-daily-schedule.md) |
| svc-trail-management | [ADR-003](ADR-003-nullable-elevation-fields.md) |
| svc-trip-catalog | [ADR-004](ADR-004-configuration-driven-classification.md) |

---

## Decisions by Status

| Status | Count | ADRs |
|--------|-------|------|
| Accepted | 7 | ADR-003 through ADR-009 |
| Proposed | 4 | ADR-001, ADR-002, ADR-010, ADR-011 |
| Deprecated | 0 | — |
| Superseded | 0 | — |

---

## Promotion Process

Decisions are promoted from ticket-level `3.solution/d.decisions/decisions.md` to this global log when:

1. The decision affects a service's **public API contract** (endpoints, schemas, error codes)
2. The decision changes a service's **data model** (new entities, schema migrations)
3. The decision establishes a **cross-service integration pattern** (orchestration, events, shared contracts)
4. The decision introduces a **cross-cutting architectural pattern** (caching strategy, locking, authentication)

Each promoted ADR is normalized to MADR format and linked back to its originating ticket.
