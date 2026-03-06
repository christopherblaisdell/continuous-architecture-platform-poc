# Capability Mapping — NTK-10002

## Affected Capabilities

| Capability | Impact | Description |
|-----------|--------|-------------|
| CAP-2.1 Day-of-Adventure Check-In | Enhanced | Check-in UI renders different flows based on adventure category (Pattern 1/2/3) |
| CAP-1.2 Adventure Discovery and Browsing | Enhanced | Adventure catalog exposes category classification for consumer services |

## Emergent L3 Capabilities

- **Pattern-Based Check-In Flows** — Three distinct check-in UI patterns (Basic, Guided, Full Service) driven by adventure category
- **Safe Default Classification** — Unknown or unmapped categories default to Pattern 3 (Full Service) for safety
- **Adventure Category Taxonomy** — YAML-driven classification of 25 adventure types into 3 check-in patterns

## Related Decisions

- ADR-004: Configuration-Driven Classification
- ADR-005: Pattern 3 Default Fallback
