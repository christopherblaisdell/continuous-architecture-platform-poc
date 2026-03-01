# NTK-10002: Architecture Decisions

## ADR-001: Configuration-Driven Classification over Database-Driven

**Status**: ACCEPTED

**Context**: The adventure category classification system requires a mapping from 25 categories to 3 check-in patterns. This mapping needs to be maintainable and performant. Two approaches were considered:

- **Option A - Database-driven**: Store the mapping in a database table, build an admin UI for operations staff to edit it, query the table during check-in.
- **Option B - Configuration-driven**: Define the mapping in a YAML configuration file managed through Spring Cloud Config, loaded into memory at startup.

**Decision**: Use configuration-driven classification (Option B) with YAML config in Spring Cloud Config.

**Rationale**:
- The mapping is expected to change infrequently (less than once per sprint).
- YAML config files are version-controlled in Git, providing full audit trail and PR-based review.
- No new database table, schema migration, or admin UI is required, reducing implementation scope.
- In-memory cache provides sub-millisecond lookup performance with no per-request I/O.
- Spring `@Cacheable` with configurable TTL provides automatic refresh.
- The `/actuator/refresh` endpoint enables on-demand reload for urgent changes.

**Consequences**:
- Configuration changes require a commit and push to the config repository followed by a service refresh.
- Operations staff cannot self-service mapping changes through a UI; they must request changes through the development team.
- If category changes become frequent (more than once per sprint), this decision should be revisited.

---

## ADR-002: Pattern 3 as Default Fallback for Unknown Categories

**Status**: ACCEPTED

**Context**: Edge cases exist where the `adventure_category` field may be null, empty, or contain a value not recognized by the classification table. This could occur with legacy reservations that predate the feature, or when a new category is added to `svc-trip-catalog` before the classification config is updated. The system needs a defined behavior for these cases.

**Decision**: Default to Pattern 3 (Full Service) for any null, empty, or unrecognized adventure category.

**Rationale**:
- **Safety-first principle**: Pattern 3 includes all possible check-in steps including gear verification, safety briefing, and medical clearance. An incorrectly over-serviced guest experiences a few extra minutes of check-in. An incorrectly under-serviced guest may miss critical safety procedures.
- **Operational alignment**: Operations staff confirmed that providing the full check-in experience is always safe, while skipping steps can create liability.
- **Guest experience**: A guest who goes through unnecessary steps has a minor inconvenience. A guest who misses necessary steps may face safety risks or arrive at their activity unprepared.

**Consequences**:
- Guests with unmapped categories will experience the longest check-in flow, which may cause minor frustration if their activity is actually low-complexity.
- Monitoring should track how often the fallback is triggered (metric: `checkin.classification.fallback.count`) to identify categories that need to be added to the mapping.
- Operations teams should be aware that new categories require a corresponding classification config update to avoid unnecessary Pattern 3 assignments.
