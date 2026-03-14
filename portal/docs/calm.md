---
tags:
  - topology
  - governance
  - automation
---

# CALM — Architecture Topology Layer

| | |
|-----------|-------|
| **Status** | Pilot |
| **Spec** | [Architecture as Code — CALM](https://github.com/finos/architecture-as-code) |
| **Generator** | `python3 scripts/generate-calm.py` |
| **Output** | `architecture/calm/` |

---

## What is CALM?

CALM (Common Architecture Language Model) is a JSON specification from the [Architecture as Code Foundation](https://www.architectureascode.org/) (FINOS) for declaring system topology — **nodes**, **relationships**, and **interfaces** — in a machine-readable, version-controlled format.

It answers the question: *How does the system fit together?*

```
    CALM Topology Layer
    ├── Nodes       (services, databases, actors, frontend apps)
    ├── Relationships  (REST calls, Kafka events, JDBC connections)
    ├── Interfaces     (API endpoints, event channels, DB schemas)
    └── Controls       (governance rules enforced in CI)
         │
    ┌────┼────────────────┐
    │    │                │
  OpenAPI Specs    AsyncAPI Specs    Solution Designs
  (API contracts)  (Event schemas)   (Change lifecycle)
```

CALM does **not** replace OpenAPI, AsyncAPI, or solution designs. It sits above them as a **topology map** that shows how all the pieces connect.

---

## Why Auto-Generate CALM?

NovaTrek already models its architecture in structured YAML: `domains.yaml`, `cross-service-calls.yaml`, `data-stores.yaml`, `events.yaml`, `actors.yaml`, and 22 OpenAPI specs. This is the single source of truth for the portal.

Rather than writing CALM by hand (creating a second source of truth), we **auto-generate** CALM from the metadata architects already maintain:

```bash
# Generate full system topology (74 nodes, 146 relationships)
python3 scripts/generate-calm.py

# Generate a single domain for focused review
python3 scripts/generate-calm.py --domain Operations

# Validate topology against architecture patterns
python3 scripts/validate-calm.py
```

**Why auto-generate instead of hand-author?**

1. **No new format to learn** — architects stay in YAML and OpenAPI specs
2. **No drift by construction** — one source of truth feeds both portal pages and CALM topology
3. **Incremental adoption** — existing workflows are unchanged; CALM is additive
4. **Validation is the value, not authoring** — CALM patterns and controls catch violations regardless of how the CALM document was produced

---

## What CALM Gets Us

### Today vs. With CALM

| Capability | Today (Manual) | With CALM (Automated) |
|-----------|---------------|----------------------|
| No shared databases | PR reviewer reads YAML | CI rejects PRs that connect a database to multiple services |
| API-only cross-service access | Rule text in copilot-instructions.md | CI validates no JDBC relationships exist between services |
| PCI scope tracking | Manual list in `pci.yaml` | CALM decorator flags PCI-scoped nodes and relationships |
| Impact analysis | Architect reads cross-service-calls.yaml | Graph traversal shows all upstream/downstream dependencies |
| Architecture drift | Undetected | CALM topology compared against running system metadata |
| Topology visualization | Static PlantUML diagrams | Interactive system map generated from CALM graph |

### Example: Automated Governance

Today, if someone introduces a shared database between two services, the only protection is a human reviewer catching it in a PR. With CALM, a CI step runs:

```bash
calm validate --pattern novatrek-microservice.json --architecture novatrek-topology.json
```

If the pattern says "each database node must have exactly one `connects` relationship," the PR is automatically blocked.

---

## Generated Topology Summary

The generator reads 6 metadata sources and produces a complete topology:

| Source File | CALM Output |
|------------|------------|
| `domains.yaml` (22 services across 9 domains) | 22 service nodes with domain/team metadata |
| `data-stores.yaml` (21 databases) | 21 database nodes + 21 `connects` relationships |
| `cross-service-calls.yaml` (REST integrations) | `interacts` relationships with endpoint-level detail |
| `events.yaml` (7 Kafka events) | `interacts` relationships with channel metadata |
| `actors.yaml` (actors + frontend apps) | actor/system nodes + `interacts` relationships |
| `architecture/specs/*.yaml` (OpenAPI) | Interface definitions on each service node |

**Current output:** 74 nodes (21 services, 21 databases, 12 external systems, 20 actors/apps), 146 relationships across the full NovaTrek platform.

---

## Per-Domain Topology

All 9 domains are generated individually for focused review:

| Domain | Services | Nodes | Relationships | File |
|--------|----------|-------|---------------|------|
| Operations | svc-check-in, svc-scheduling-orchestrator | 17 | 28 | `architecture/calm/domains/operations.json` |
| Guest Identity | svc-guest-profiles | 12 | 18 | `architecture/calm/domains/guest-identity.json` |
| Booking | svc-reservations | 14 | 23 | `architecture/calm/domains/booking.json` |
| Product Catalog | svc-trip-catalog, svc-trail-management | 13 | 16 | `architecture/calm/domains/product-catalog.json` |
| Safety | svc-safety-compliance, svc-emergency-response, svc-wildlife-tracking | 17 | 36 | `architecture/calm/domains/safety.json` |
| Logistics | svc-transport-logistics, svc-gear-inventory | 12 | 11 | `architecture/calm/domains/logistics.json` |
| Guide Management | svc-guide-management | 5 | 8 | `architecture/calm/domains/guide-management.json` |
| External | svc-partner-integrations | 7 | 7 | `architecture/calm/domains/external.json` |
| Support | 8 services (payments, notifications, etc.) | 36 | 77 | `architecture/calm/domains/support.json` |

**Full system:** `architecture/calm/novatrek-topology.json`

---

## Automated Validation

The validator (`scripts/validate-calm.py`) checks the generated topology against 6 architecture rules:

| Rule | What it Catches | Severity |
|------|----------------|----------|
| No shared databases | Database node connected to more than one service | Error |
| API-mediated access | JDBC relationship between two service nodes | Error |
| Service metadata required | Service missing domain or team in metadata | Error |
| Relationship integrity | Relationship referencing a non-existent node | Error |
| No orphan services | Service with zero relationships | Warning |
| PCI scope | PCI-scoped service missing `pci-in-scope: true` metadata | Error |

These rules are also documented as formal CALM pattern, control, and standard files:

- `architecture/calm/patterns/novatrek-microservice.json` — microservice pattern rules
- `architecture/calm/controls/data-ownership.json` — single-owner database control
- `architecture/calm/controls/api-mediated-access.json` — no cross-service JDBC control
- `architecture/calm/controls/pci-scope.json` — PCI DSS cardholder data environment scope
- `architecture/calm/standards/novatrek-org-standard.json` — organizational metadata requirements and governance rules

### Validation in Action

Running `python3 scripts/validate-calm.py` immediately caught a real finding: `svc-reviews` is referenced in `cross-service-calls.yaml` but is not listed in any domain in `domains.yaml`. This is exactly the kind of inconsistency that manual review misses but automated topology validation catches automatically.

```
[FAIL] architecture/calm/domains/booking.json (14 nodes, 23 relationships)
  ERROR: [relationship-integrity] Relationship references unknown source: 'svc-reviews'
```

---

## Generated Files

```
architecture/calm/
├── novatrek-topology.json                 # Full system (76 nodes, 147 relationships)
├── domains/
│   ├── operations.json                    # Operations domain
│   ├── guest-identity.json                # Guest Identity domain
│   ├── booking.json                       # Booking domain
│   ├── product-catalog.json               # Product Catalog domain
│   ├── safety.json                        # Safety domain
│   ├── logistics.json                     # Logistics domain
│   ├── guide-management.json              # Guide Management domain
│   ├── external.json                      # External domain
│   └── support.json                       # Support domain
├── patterns/
│   └── novatrek-microservice.json         # Microservice architecture pattern
├── controls/
│   ├── data-ownership.json                # Single-owner database control
│   ├── api-mediated-access.json           # No cross-service JDBC control
│   └── pci-scope.json                     # PCI DSS cardholder data environment scope
└── standards/
    └── novatrek-org-standard.json         # Organizational metadata requirements (6 governance rules)
```

---

## Example Output (Operations Domain)

Generated with `python3 scripts/generate-calm.py --domain Operations`:

```json
{
  "$schema": "https://raw.githubusercontent.com/finos/architecture-as-code/main/calm/schema/calm.json",
  "metadata": {
    "name": "NovaTrek Adventures — Operations Domain Topology",
    "version": "1.0.0"
  },
  "nodes": [
    {
      "unique-id": "svc-check-in",
      "node-type": "service",
      "name": "Check In Service",
      "interfaces": [
        { "unique-id": "svc-check-in-api-post-check-ins", "type": "path", "path": "/check-ins" },
        { "unique-id": "svc-check-in-event-checkin-completed", "type": "path", "path": "novatrek.operations.checkin.completed" }
      ],
      "metadata": { "domain": "Operations", "team": "NovaTrek Operations Team" }
    },
    {
      "unique-id": "svc-check-in-db",
      "node-type": "database",
      "name": "Check In Database",
      "metadata": { "engine": "PostgreSQL 15", "schema": "checkin" }
    }
  ],
  "relationships": [
    {
      "unique-id": "rel-svc-check-in-to-db",
      "relationship-type": "connects",
      "parties": { "source": "svc-check-in", "target": "svc-check-in-db" },
      "protocol": "JDBC"
    },
    {
      "unique-id": "rel-svc-check-in-post--check-ins-to-svc-reservations",
      "relationship-type": "interacts",
      "parties": { "source": "svc-check-in", "target": "svc-reservations" },
      "protocol": "HTTPS",
      "metadata": { "action": "Verify reservation exists" }
    }
  ]
}
```

14 nodes (2 Operations services + databases + 10 external services referenced by cross-service calls), 28 relationships.

---

## Roadmap

| Phase | Description | Status |
|-------|-------------|--------|
| **Phase 0: Pilot** | Auto-generate CALM from metadata; validate all 9 domains; patterns + controls | Complete |
| **Phase 1: CI Integration** | Add `validate-calm.py` to CI pipeline; block PRs on validation failures | Complete |
| **Phase 2: Generator Integration** | Portal generators consume CALM for topology views, dependency matrix | Complete |
| **Phase 3: Governance Automation** | PCI scope control, org standard, governance dashboard, FINOS `calm validate` CLI | In Progress |
| Phase 4: Solution Integration | Track topology changes per solution design | Planned |
| Phase 5: Advanced | Blast radius analysis, drift detection, timeline visualization | Planned |

See the full plan: [CALM Integration Plan](../../docs/CALM-INTEGRATION-PLAN.md)
