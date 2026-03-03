# ADR-004: Configuration-Driven Classification over Database-Driven

## Status

Accepted

## Date

2024-08-14

## Context and Problem Statement

The adventure category classification system requires a mapping from 25 adventure categories to 3 check-in UI patterns. This mapping must be maintainable by the team, performant at runtime (no per-request latency penalty), and auditable over time. How should the category-to-pattern mapping be stored and maintained?

## Decision Drivers

- Change frequency is low (less than once per sprint)
- Mapping changes must be auditable and reviewable
- Runtime lookup must add near-zero latency to the check-in request
- Implementation scope should be minimized
- Operations team needs visibility into current mapping

## Considered Options

1. **Database-driven** — Store mapping in a database table with an admin UI
2. **Configuration-driven** — Define mapping in YAML via Spring Cloud Config
3. **Code-driven** — Hardcode the mapping in the Java source code

## Decision Outcome

**Chosen Option**: "Configuration-driven", because it provides version-controlled, reviewable mapping changes with sub-millisecond runtime performance and minimal implementation scope.

### Confirmation

- Classification config file exists in Spring Cloud Config repository
- `ClassificationService` loads config at startup and refreshes on TTL expiry
- `/actuator/refresh` endpoint triggers immediate reload

## Consequences

### Positive

- YAML config is version-controlled in Git, providing full audit trail and PR-based review
- No new database table, schema migration, or admin UI required
- In-memory `ConcurrentHashMap` provides sub-millisecond lookup performance
- Spring `@Cacheable` with configurable TTL (default 5 min) handles refresh transparently

### Negative

- Configuration changes require a commit, push, and service refresh — not self-service
- Operations staff must request changes through the development team
- If change frequency increases beyond once per sprint, this approach should be revisited

### Neutral

- Requires Spring Cloud Config infrastructure (already in place)

## Pros and Cons of the Options

### Database-driven

- **Good**, because operations can modify mappings through an admin UI without developer involvement
- **Good**, because changes are immediate (no cache TTL)
- **Neutral**, because requires database connection for every lookup (mitigated by application-level caching)
- **Bad**, because introduces new database table, migration, and admin UI development effort
- **Bad**, because changes bypass code review — no audit trail in Git

### Configuration-driven

- **Good**, because changes are version-controlled and require PR review
- **Good**, because no additional infrastructure required
- **Good**, because sub-millisecond in-memory lookup with automatic refresh
- **Neutral**, because requires Spring Cloud Config refresh for changes to take effect
- **Bad**, because not self-service for operations staff

### Code-driven

- **Good**, because simplest implementation — just a Java Map constant
- **Bad**, because mapping changes require a code deployment
- **Bad**, because mixes configuration data with application logic

## More Information

- Origin: [NTK-10002 Solution Design](../phase-1-ai-tool-cost-comparison/workspace/work-items/tickets/_NTK-10002-adventure-category-classification/NTK-10002-solution-design.md)
- Services: [svc-check-in](../services/svc-check-in.md), [svc-trip-catalog](../services/svc-trip-catalog.md)
