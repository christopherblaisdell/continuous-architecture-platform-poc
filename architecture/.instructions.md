## Architecture Security Context

When working in this directory or analyzing NovaTrek architecture artifacts, always apply these security principles:

### Data Ownership Boundaries

Every service owns its data exclusively. Cross-service data access MUST go through published API endpoints. Check `architecture/metadata/cross-service-calls.yaml` for the allowed integration map. Flag any design that proposes direct database access from one service to another.

### Identity Resolution

All guest identity resolution flows through `svc-guest-profiles`. Services MUST NOT maintain shadow guest records. Any solution that stores guest data outside `svc-guest-profiles` is an anti-pattern.

### Safety Defaults

Unknown or unmapped adventure categories MUST default to Pattern 3 (Full Service), NEVER Pattern 1 (Basic). This is a safety requirement documented in ADR-005 and `config/adventure-classification.yaml`.

### API Contract Security

When reviewing or proposing API changes in `architecture/specs/`:
- All fields must have types, descriptions, and nullable annotations
- New required fields break existing consumers — check backward compatibility
- Enum values must be validated against known domain values
- Error responses must not leak internal details (stack traces, database IDs)
- Confirmation codes and reservation IDs must be validated for format and length

### Prior Art Discovery

Before creating a new solution design, ALWAYS search for prior art:
1. Check capability history: `python3 scripts/ticket-client.py --list --capability CAP-X.Y`
2. Review `architecture/metadata/capability-changelog.yaml` for overlapping L3 capabilities
3. Search `decisions/` for constraining ADRs
4. Reference prior solutions in the new solution's master document
