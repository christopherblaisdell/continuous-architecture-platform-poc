# System Topology

Auto-generated from the [CALM topology](../calm.md) — the machine-readable architecture model for NovaTrek Adventures.

---

## Topology at a Glance

| Metric | Count |
|--------|-------|
| Services | 22 |
| Databases | 22 |
| REST integrations | 80 |
| Event flows (Kafka) | 57 |
| Database connections | 22 |
| Total nodes | 92 |
| Total relationships | 159 |

## Domain Summary

| Domain | Services | REST Calls | Event Flows | Total Relationships |
|--------|----------|------------|-------------|---------------------|
| Booking | 1 | 6 | 9 | 16 |
| External | 1 | 5 | 1 | 7 |
| Guest Identity | 1 | 3 | 3 | 7 |
| Guide Management | 1 | 0 | 0 | 1 |
| Logistics | 2 | 7 | 1 | 10 |
| Operations | 2 | 14 | 8 | 24 |
| Product Catalog | 2 | 6 | 1 | 9 |
| Safety | 3 | 13 | 17 | 33 |
| Support | 9 | 19 | 17 | 45 |

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
