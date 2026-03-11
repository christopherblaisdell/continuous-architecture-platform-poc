---
tags:
  - standards
  - metadata
  - architecture
---

<div class="hero" markdown>

# Architecture Metadata Registry

<p class="subtitle">The 15 YAML files that define the entire NovaTrek architecture — and why everything is modeled as structured data</p>

</div>

## What Is the Metadata Registry?

The `architecture/metadata/` directory contains **15 YAML files** that together form a complete, machine-readable model of the NovaTrek platform. Every service, domain, capability, integration, data store, actor, event, application, ticket, and deployment status is captured as structured data.

This is **not documentation** in the traditional sense. These files are the **single source of truth** that portal pages, CALM topology, sequence diagrams, and capability maps are all generated from. Editing a YAML file and pushing to `main` triggers CI to regenerate the entire architecture portal automatically.

---

## Why YAML Instead of Documentation?

### The problem with prose

Traditional architecture documentation is a collection of wiki pages, Word documents, and diagrams maintained by hand. This approach has well-known failure modes:

- **Drift** — documentation falls behind reality within weeks of being written
- **Duplication** — the same fact (e.g., "svc-payments is in the Support domain") appears in 12 places and is updated in 3 of them
- **No validation** — a wiki page can claim anything; there is no way to lint or test it
- **No generation** — every downstream artifact (diagrams, capability maps, service catalogs) must be manually maintained in parallel

### The metadata-driven alternative

By encoding architecture facts as structured YAML, NovaTrek gains:

| Property | Prose Documentation | YAML Metadata |
|----------|-------------------|---------------|
| **Single source of truth** | Facts scattered across wikis | One file per concern, all derived from it |
| **Machine-readable** | Humans only | Parsed by generators, linters, CALM exporters |
| **Diffable in PRs** | Ambiguous prose changes | Structural changes reviewable field-by-field |
| **Generates everything** | Manual upkeep for each artifact | Portal pages, diagrams, topology — all auto-generated |
| **Validatable** | Cannot verify consistency | Scripts can check referential integrity across files |
| **Version-controlled** | Wiki history is opaque | Full git history with blame, diff, and revert |

The core principle: **edit the data, not the documents. Documents are generated outputs.**

---

## File Reference

### Domain and Service Model

| File | Purpose | Key Fields |
|------|---------|------------|
| **domains.yaml** | Groups all 22 services into 9 business domains with display colors and icons | domain name, color, light (pastel), icon, services list |
| **label-to-svc.yaml** | Maps human-readable labels (e.g., "Reservations") to service identifiers (e.g., `svc-reservations`) | flat key-value pairs |
| **data-stores.yaml** | Database engine, schema, tables, columns, constraints, and features for every service | engine, schema, tables (with column-level detail), volume, backup policy |
| **cross-service-calls.yaml** | Complete REST integration map — which endpoint calls which endpoint on which service | source endpoint, target service, target method/path, sync/async flag |
| **pci.yaml** | PCI DSS compliance scope — which services handle payment data and the data flow paths | in-scope services, external systems, data flow pairs |

### Business Capabilities

| File | Purpose | Key Fields |
|------|---------|------------|
| **capabilities.yaml** | L1/L2 business capability definitions organized by domain (34 capabilities across 9 domains) | domain id/name, capability id/name, status, owning services |
| **capability-changelog.yaml** | **Single source of truth** for all capability changes per solution — L3 capabilities emerge here | ticket, date, solution folder, affected capabilities, L3 sub-capabilities, ADR references |

!!! note "Capability Data Ownership"
    For solved tickets, capability mappings live exclusively in `capability-changelog.yaml`. The `tickets.yaml` file only carries `planned_capabilities` for unsolved tickets (planning estimates). This avoids duplication.

### Actors and Applications

| File | Purpose | Key Fields |
|------|---------|------------|
| **actors.yaml** | External systems, frontend applications, and human actors that interact with the platform | actor name, type (person/system/app), description, domain |
| **applications.yaml** | Frontend app definitions with screen-by-screen user flows | app id, title, type, technology, team, screens with step-by-step service calls |
| **app-titles.yaml** | Short display names for applications used in portal UI rendering | flat key-value pairs |
| **consumers.yaml** | Maps each service to the application screens that consume it | service name, list of (app, screen) pairs |

### Events

| File | Purpose | Key Fields |
|------|---------|------------|
| **events.yaml** | Domain event catalog — channels, producers, consumers, and triggers | event key, channel name, producing service, trigger endpoint, consuming services, domain |

### Tickets and Delivery

| File | Purpose | Key Fields |
|------|---------|------------|
| **tickets.yaml** | Ticket registry with service mappings, priority, status, and capability links | ticket key, summary, status, priority, assignee, solution folder, user story, planned capabilities |
| **delivery-status.yaml** | Deployment progress across 6 delivery waves with Azure resource tracking | wave number, name, status, deployed date, resource list |
| **pipeline-registry.yaml** | Central CI/CD pipeline registry — GitHub workflows and per-service CI patterns | repository, global pipelines, per-service pipeline templates |

---

## How These Files Power the Portal

Every portal page is a **generated output** of these metadata files. Nothing is maintained by hand in the portal.

```
architecture/metadata/*.yaml
        │
        ▼
  Generator Scripts
  (portal/scripts/)
        │
        ├──► Microservice deep-dive pages (22 pages, 139 sequence diagrams)
        ├──► Application pages with screen flows
        ├──► Service Catalog with Swagger UI links
        ├──► Business Capability map
        ├──► Solution design pages
        ├──► Ticket pages
        ├──► CALM topology JSON (74 nodes, 146 relationships)
        └──► Event Catalog
```

### Which scripts consume which files

| Generator Script | Metadata Files Used |
|-----------------|---------------------|
| `generate-microservice-pages.py` | domains, data-stores, cross-service-calls, label-to-svc, applications, capabilities |
| `generate-application-pages.py` | applications, consumers, label-to-svc |
| `generate-swagger-pages.py` | domains, data-stores |
| `generate-capability-pages.py` | capabilities, capability-changelog |
| `generate-ticket-pages.py` | tickets, capabilities |
| `generate-solution-pages.py` | capability-changelog, tickets |
| `generate-calm.py` | domains, data-stores, cross-service-calls, events, actors |
| `ticket-client.py` | tickets, capabilities |

All generators use the shared `load_metadata.py` module which validates and caches metadata on load.

---

## Who Edits These Files — and How?

### The architect workflow

Architects **do not typically edit YAML metadata by hand**. Instead, the AI agent (GitHub Copilot or Roo Code) modifies these files as part of executing the solution design workflow. Here is the typical flow:

```
Architect receives ticket (e.g., NTK-10005)
        │
        ▼
Architect prompts AI agent to design a solution
        │
        ▼
AI agent reads ticket, specs, and metadata
        │
        ▼
AI agent produces solution design documents AND
updates YAML files as a side effect:
  • capability-changelog.yaml  (new capability entries)
  • tickets.yaml               (status → Solved, solution link)
  • cross-service-calls.yaml   (new integration points)
  • OpenAPI specs              (new/modified endpoints)
  • data-stores.yaml           (new tables or columns)
        │
        ▼
Architect reviews YAML changes in PR diff
        │
        ▼
Merge to main → CI regenerates portal
```

The architect's role is to **prompt, review, and approve** — not to author YAML by hand. The AI agent understands the file formats, referential integrity rules, and naming conventions, so it produces structurally correct updates that the architect validates in a pull request diff.

### When would an architect edit YAML manually?

Rarely, but it happens for **structural or bootstrapping changes**:

| Scenario | Example | Why Manual? |
|----------|---------|-------------|
| **Initial setup** | Creating `domains.yaml` with all 9 domains | One-time bootstrap — no prior data to derive from |
| **Domain restructuring** | Splitting "Support" into "Payments" and "Communication" | Strategic decision requiring human judgment about taxonomy |
| **Fixing a typo** | Correcting a team name in `actors.yaml` | Faster to fix directly than to prompt an AI agent |
| **Adding a new service** | New entry in `domains.yaml`, `data-stores.yaml`, `label-to-svc.yaml` | Minimal, predictable changes — may be manual or AI-assisted |

For anything involving analysis, cross-referencing, or producing multiple coordinated changes (the common case during solution design), the AI agent handles the updates.

### Are these files generated from code?

**No.** These metadata files are **authored data**, not generated outputs. They are not extracted from running services, source code, or infrastructure. The flow is:

```
Authored inputs:                    Generated outputs:
─────────────────                   ───────────────────
architecture/metadata/*.yaml   ──►  portal/docs/ (Markdown pages)
architecture/specs/*.yaml      ──►  portal/docs/microservices/ (deep-dive pages)
                               ──►  portal/docs/microservices/svg/ (sequence diagrams)
                               ──►  architecture/calm/ (CALM topology JSON)
                               ──►  portal/docs/services/api/ (Swagger UI)
```

The YAML files are inputs. The portal pages, diagrams, and CALM topology are outputs. This is the opposite of many "docs-as-code" approaches that extract documentation from source code — here, the architecture model is the primary artifact, and everything else is derived from it.

### CI/CD integration

1. **Edit** YAML files (typically via AI agent during solution design, occasionally by hand)
2. **Commit** and push to `main`
3. **CI regenerates** all portal pages automatically via `generate-all.sh`

For local preview before pushing:

```bash
# Regenerate all portal pages from metadata
bash portal/scripts/generate-all.sh

# Build the portal locally
cd portal && python3 -m mkdocs build

# Or serve locally for preview
cd portal && python3 -m mkdocs serve
```

### Validation rules

- **Referential integrity**: Service names in `cross-service-calls.yaml` must exist in `domains.yaml`
- **No duplication**: Solved ticket capabilities go in `capability-changelog.yaml` only, never duplicated in `tickets.yaml`
- **Consistent identifiers**: Service names use `svc-` prefix everywhere (e.g., `svc-check-in`, never `check-in`)
- **ISO 8601 dates**: All date fields use `YYYY-MM-DD` format

---

## Relationship Between Metadata and OpenAPI Specs

The metadata registry and the [OpenAPI specs](../openapi-contracts/index.md) are complementary:

| Concern | Where It Lives |
|---------|---------------|
| What endpoints does a service expose? | `architecture/specs/svc-*.yaml` (OpenAPI) |
| What domain does the service belong to? | `architecture/metadata/domains.yaml` |
| What database does it use? | `architecture/metadata/data-stores.yaml` |
| Which other services does it call? | `architecture/metadata/cross-service-calls.yaml` |
| Who publishes/subscribes to events? | `architecture/metadata/events.yaml` |
| What business capability does it support? | `architecture/metadata/capabilities.yaml` |

OpenAPI specs define the **contract surface** (endpoints, schemas, parameters). Metadata files define the **architecture topology** (how services relate to each other, to domains, to capabilities, and to actors). Together they form the complete architecture model.

---

!!! tip "Quick Reference"

    **Adding a new service**: Add entries to `domains.yaml`, `data-stores.yaml`, and `label-to-svc.yaml` at minimum. Create the OpenAPI spec in `architecture/specs/`. Run `bash portal/scripts/generate-all.sh` to regenerate portal pages.

    **Recording a solved ticket's capability impact**: Add an entry to `capability-changelog.yaml` — not to `tickets.yaml`. Update the ticket's `status` in `tickets.yaml` only.

    **Checking what calls what**: Open `cross-service-calls.yaml` for the full REST integration map, or `events.yaml` for async pub-sub relationships.
