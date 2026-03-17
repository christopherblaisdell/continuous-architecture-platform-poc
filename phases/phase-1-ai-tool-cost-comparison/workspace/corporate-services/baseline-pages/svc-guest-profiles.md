# svc-guest-profiles — Service Architecture Page

| | |
|-----------|-------|
| **Service** | svc-guest-profiles |
| **Domain** | Guest Identity |
| **API Version** | 1.0.0 |
| **Base URL** | `https://api.novatrek.example.com/guests/v1` |
| **Last Updated** | 2026-03-03 |

---

## Purpose

Manages guest identity records including full registered accounts and temporary kiosk profiles. Provides profile CRUD, identity lookup, and profile merge capabilities. Serves as the system of record for guest identity across the NovaTrek platform.

---

## Architecture Decisions

| ADR | Title | Status | Impact |
|-----|-------|--------|--------|
| [ADR-008](../decisions/ADR-008-temporary-guest-profile.md) | Temporary Guest Profile | Accepted | New `TEMPORARY` profile type with minimal required fields, 90-day auto-anonymization |

---

## Integration Points

| Direction | Service | Purpose |
|-----------|---------|---------|
| ← Called by | svc-check-in | Profile lookup, temporary profile creation |
| ← Called by | svc-reservations | Guest identity validation |
| Calls → | (none currently) | — |

---

## Sequence Diagrams


Shows the guest profile lookup and temporary profile creation flow during self-service check-in.

<object data="diagrams/lookup-orchestration.svg" type="image/svg+xml" style="width: 100%; max-width: 100%; overflow-x: auto;">Lookup Orchestration diagram</object>

---

## Key Patterns

- **Temporary Profile Lifecycle**: `TEMPORARY` profiles are created with minimal data (last name + reservation ID) and auto-anonymized after 90 days. If the guest later registers, the temporary profile is merged into the full account, preserving check-in history.
- **Profile Type Enum**: `REGISTERED`, `TEMPORARY` — governs required field validation and retention policies.

---

## Recent Changes

| Ticket | Change | Date |
|--------|--------|------|

---

## Source Code

- [svc-guest-profiles](../phase-1-ai-tool-cost-comparison/workspace/source-code/svc-guest-profiles/)
- [OpenAPI Spec](../phase-1-ai-tool-cost-comparison/workspace/corporate-services/services/svc-guest-profiles.yaml)

---

## Technical Debt and Open Questions

- Profile merge edge cases: multiple temporary profiles for the same guest across visits need deduplication logic
- Background anonymization job monitoring and alerting needs operational runbook
- `TEMPORARY` profile type may need additional fields if kiosk features expand (e.g., dietary preferences for catered adventures)
