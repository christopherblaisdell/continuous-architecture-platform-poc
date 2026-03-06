# Capability Mapping — NTK-10004

## Affected Capabilities

| Capability | Impact | Description |
|-----------|--------|-------------|
| CAP-2.2 Schedule Planning and Optimization | Fixed | Schedule updates use PATCH semantics with optimistic locking to prevent concurrent overwrites |

## Emergent L3 Capabilities

- **Optimistic Locking on Daily Schedule** — Version-based concurrency control (_rev field) prevents concurrent overwrites
- **PATCH Semantics for Schedule Updates** — Field-level merge replaces full entity replacement on schedule endpoints

## Related Decisions

- ADR-010: PATCH Semantics for Schedule Updates
- ADR-011: Optimistic Locking on Daily Schedule
