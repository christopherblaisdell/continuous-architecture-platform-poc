# CALM: Architecture Topology as Code

## What Is CALM?

CALM (Common Architecture Language Model) is a JSON specification from the [Architecture as Code Foundation](https://www.architectureascode.org/) (FINOS) for describing system topology — **nodes**, **relationships**, and **interfaces** — in a machine-readable, version-controlled format.

It answers a question that OpenAPI specs and diagrams cannot: **How does the entire system fit together?**

---

## Why Auto-Generate CALM?

NovaTrek already maintains structured YAML metadata: domain classifications, cross-service call maps, data store registries, event schemas, and 22 OpenAPI specs. This metadata is the single source of truth for the architecture portal.

Rather than writing CALM by hand (creating a second source of truth that drifts), we **auto-generate** CALM from the metadata architects already maintain:

```bash
# Generate full system topology
python3 architecture/scripts/generate-calm.py

# Generate a single domain for focused review
python3 architecture/scripts/generate-calm.py --domain Operations
```

**No new format to learn.** Architects stay in YAML and OpenAPI specs. CALM is produced as a derived artifact — like how the portal pages are generated from the same metadata.

---

## What CALM Gets Us

### Manual Governance vs. Automated Governance

| Architecture Rule | Today (Manual) | With CALM (Automated) |
|-------------------|---------------|----------------------|
| No shared databases | PR reviewer reads YAML diffs | CI rejects PRs that connect a database to multiple services |
| API-only cross-service access | Convention enforced by review | CI validates no direct JDBC relationships between services |
| Impact analysis | Architect reads cross-service-calls.yaml manually | Graph traversal shows all upstream/downstream dependencies |
| Architecture drift | Undetected until something breaks | CALM topology compared against running system metadata |

### Real Finding from Generation

Running the generator against NovaTrek's metadata immediately found an inconsistency: `svc-reviews` is referenced in `cross-service-calls.yaml` but is not listed in any domain in `domains.yaml`. This is exactly the kind of gap that manual review misses but automated topology validation catches automatically.

---

## Generated Output

The generator reads 6 metadata sources and produces a complete topology:

| Metric | Value |
|--------|-------|
| Total nodes | 74 (services, databases, actors, frontend apps) |
| Total relationships | 146 (REST calls, Kafka events, JDBC connections) |
| Domain topologies | 9 (one per bounded context) |
| Architecture patterns | 1 (microservice pattern rules) |
| Governance controls | 2 (data ownership, API-mediated access) |

All output is in `architecture/calm/` — version-controlled alongside the metadata that produces it.

---

## How It Fits the Platform

``` mermaid
flowchart LR
    A["YAML Metadata<br/>(architects maintain)"] --> B["CALM Generator<br/>(architecture/scripts/generate-calm.py)"]
    B --> C["CALM Topology JSON<br/>(architecture/calm/)"]
    C --> D["CI Validation<br/>(architecture/scripts/validate-calm.py)"]
    C --> E["Portal Pages<br/>(auto-generated)"]
    A --> E

    style A fill:#e0f2f1
    style B fill:#00897b,color:#fff
    style C fill:#ff8f00,color:#fff
    style D fill:#e53935,color:#fff
    style E fill:#1565c0,color:#fff
```

CALM is a **derived artifact** — it does not add authoring burden. Architects maintain the same YAML files they already maintain. The generator transforms them into a standard topology format that enables automated validation, impact analysis, and governance enforcement.

---

## Example: Operations Domain

```json
{
  "nodes": [
    {
      "unique-id": "svc-check-in",
      "node-type": "service",
      "name": "Check In Service",
      "interfaces": [
        { "unique-id": "svc-check-in-api-post-check-ins", "path": "/check-ins" }
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
    }
  ]
}
```

Services, databases, and their connections — expressed as a graph that tools can query, validate, and visualize.
