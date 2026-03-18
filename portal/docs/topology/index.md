# System Topology

Auto-generated from the [CALM topology](../calm.md) — the machine-readable architecture model for NovaTrek Adventures.

!!! info "Everything on this portal is entirely fictional"
    NovaTrek Adventures is a completely fictitious company used as a synthetic workspace for the Continuous Architecture Platform proof of concept.

---

## Topology at a Glance

| Metric | Count |
|--------|-------|
| Services | 22 |
| Databases | 22 |
| REST integrations | 72 |
| Event flows (Kafka) | 55 |
| Database connections | 22 |
| Total nodes | 78 |
| Total relationships | 149 |

## Domain Summary

| Domain | Services | REST Calls | Event Flows | Total Relationships |
|--------|----------|------------|-------------|---------------------|
| Booking | 1 | 5 | 8 | 14 |
| External | 1 | 5 | 1 | 7 |
| Guest Identity | 1 | 3 | 3 | 7 |
| Guide Management | 1 | 0 | 0 | 1 |
| Logistics | 2 | 6 | 1 | 9 |
| Operations | 2 | 14 | 8 | 24 |
| Product Catalog | 2 | 3 | 1 | 6 |
| Safety | 3 | 12 | 17 | 32 |
| Support | 9 | 17 | 16 | 42 |

## Pages

| Page | Description |
|------|-------------|
| [System Map](system-map.md) | Interactive Mermaid diagram showing all 22 services grouped by domain with REST and event-driven connections |
| [Dependency Matrix](dependency-matrix.md) | Service-to-service dependency table showing which services call which, and over what protocol |
| [Domain Views](domain-views.md) | Per-domain topology details with service lists, databases, and relationship breakdowns |

## Data Source

All topology data is auto-generated from architecture metadata by `scripts/generate-calm.py` and validated by `scripts/validate-calm.py`. The CALM topology files live in `architecture/calm/`.

The generator reads 6 metadata sources:

- `architecture/metadata/domains.yaml` — service domain assignments
- `architecture/metadata/data-stores.yaml` — database configurations
- `architecture/metadata/cross-service-calls.yaml` — REST integrations
- `architecture/metadata/events.yaml` — Kafka event definitions
- `architecture/metadata/actors.yaml` — actors and frontend applications
- `architecture/specs/*.yaml` — OpenAPI specifications
