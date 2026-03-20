# CALM Evaluation Reminder

**Date**: 2026-03-06
**Status**: Active (TOP, In Progress) — Phase 0+1 complete, see `docs/CALM-INTEGRATION-PLAN.md`

## What is CALM?

CALM (Cloud Architecture Language Model) is a JSON/YAML specification from the **Architecture as Code Foundation** for declaring architecture topology — nodes, relationships, interfaces, data flows — in a machine-readable, version-controllable format.

- Specification: https://github.com/architecture-as-code/calm
- Foundation: https://www.architectureascode.org/

## Why consider it?

- Declares structural topology (nodes, relationships, interfaces) in a standard format
- Machine-readable — enables validation, drift detection, automated governance
- Complements OpenAPI (contract) and metadata YAML (choreography) with a formal topology layer
- Growing community adoption for "architecture as code" practices

## What it does NOT solve

- Endpoint-level behavioral sequences (what happens inside a service call)
- Sequence diagram generation (our override model handles this)
- UI wireframe management

## Evaluation criteria when we revisit

1. Does CALM add value beyond what our existing metadata YAML files already provide?
2. Can our generators consume CALM documents instead of/alongside custom YAML?
3. Is the CALM tooling ecosystem mature enough for production use?
4. Would CALM enable governance features we can't achieve with current metadata?
5. Cost of migration from current metadata format to CALM

## Related

- Current metadata: `architecture/metadata/*.yaml`
- Current generators: `portal/scripts/generate-*.py`
- Separation of concerns: `portal/SEPARATION-OF-CONCERNS-PLAN.md`
