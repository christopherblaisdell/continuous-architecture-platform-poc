# CALM Evaluation Reminder

**Date**: 2026-03-06
**Updated**: 2026-03-14
**Status**: Implemented — Phases 0, 1, and 2 complete

See `architecture/reminders/CALM-PILOT-RESULTS.md` for the full Phase 0 pilot results.

## Summary of What Was Built

CALM integration is now live in three phases:

- **Phase 0 (Pilot)**: Auto-generate CALM from metadata YAML, custom validator, Operations domain
- **Phase 1 (Full Topology)**: All 9 domains + full system topology, CI integration
- **Phase 2 (Portal)**: Topology pages (system map, dependency matrix, domain views, governance dashboard)

## What Remains

- Phase 3: Governance automation (FINOS `calm validate` CLI, Spectral rules)
- Phase 4: Solution design topology integration
- Phase 5: Blast radius analysis, drift detection

See `docs/CALM-INTEGRATION-PLAN.md` for the full plan.

---

## Original Evaluation Notes (2026-03-06)

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

## Evaluation criteria (results from pilot)

1. Does CALM add value beyond what our existing metadata YAML files already provide? **Yes — automated governance and topology visualization**
2. Can our generators consume CALM documents instead of/alongside custom YAML? **Yes — topology pages generated from CALM**
3. Is the CALM tooling ecosystem mature enough for production use? **Custom Python validator is sufficient; FINOS CLI still being evaluated**
4. Would CALM enable governance features we can't achieve with current metadata? **Yes — automated shared database detection, PCI scope tracking**
5. Cost of migration from current metadata format to CALM: **Low — auto-generate from existing YAML, no migration needed**

## Related

- Current metadata: `architecture/metadata/*.yaml`
- Current generators: `portal/scripts/generate-*.py`
- CALM generator: `scripts/generate-calm.py`
- CALM validator: `scripts/validate-calm.py`

