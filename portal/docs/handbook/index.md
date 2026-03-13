---
tags:
  - handbook
  - architecture
  - workflow
---

<!-- PUBLISH -->

<div class="hero" markdown>

# Architect Handbook

<p class="subtitle">Step-by-step task guides for solution architects working on the NovaTrek platform</p>

</div>

This handbook is the single reference for how solution architects get work done on the NovaTrek Continuous Architecture Platform. Every common task — from triaging a ticket to deploying a portal update — has a dedicated guide below.

The NovaTrek platform is **metadata-driven**: architects edit YAML files and OpenAPI specs, and CI regenerates all portal pages, diagrams, and documentation automatically. The handbook explains which files to touch, in what order, and what CI does next.

---

## Task Map

| I need to... | Go to |
|---|---|
| Triage a new ticket and decide if architecture work is needed | [Working a Ticket](working-a-ticket.md) |
| Create a full solution design for a ticket | [Solution Design](solution-design.md) |
| Add or change an API endpoint or schema | [API Contract Changes](api-contracts.md) |
| Add a database table, column, index, or foreign key | [Database Changes](database-changes.md) |
| Add a new microservice to the platform | [Adding a Service](adding-a-service.md) |
| Add or modify a domain event | [Events](events.md) |
| Create or update a UI wireframe | [Wireframes](wireframes.md) |
| Regenerate portal pages and deploy changes | [Publishing](publishing.md) |

---

<div class="portal-grid" markdown>

<a href="working-a-ticket/" class="portal-card" markdown>
<span class="card-icon">:material-ticket-outline:</span>

### Working a Ticket

How to assess architectural relevance, run investigations with mock tools, discover prior art, and decide whether a solution design is needed.
</a>

<a href="solution-design/" class="portal-card" markdown>
<span class="card-icon">:material-draw-pen:</span>

### Solution Design

How to create a solution design — branch naming, folder structure, master document, capability changelog, and raising the PR for review.
</a>

<a href="api-contracts/" class="portal-card" markdown>
<span class="card-icon">:material-api:</span>

### API Contract Changes

How to add endpoints, modify schemas, add fields, and handle cross-service contract impacts in OpenAPI specs.
</a>

<a href="database-changes/" class="portal-card" markdown>
<span class="card-icon">:material-database-edit:</span>

### Database Changes

How to add or modify tables, columns, indexes, and foreign key relationships — and how to keep the architectural metadata in sync.
</a>

<a href="adding-a-service/" class="portal-card" markdown>
<span class="card-icon">:material-server-plus:</span>

### Adding a Service

How to register a new microservice: OpenAPI spec, domain assignment, metadata registration, and portal generation.
</a>

<a href="events/" class="portal-card" markdown>
<span class="card-icon">:material-timeline-clock:</span>

### Events

How to add a new domain event or modify an existing one, including AsyncAPI specs and the metadata event catalog.
</a>

<a href="wireframes/" class="portal-card" markdown>
<span class="card-icon">:material-monitor-screenshot:</span>

### Wireframes

How to create and publish UI wireframes using Excalidraw, including naming conventions and how CI converts them for the portal.
</a>

<a href="publishing/" class="portal-card" markdown>
<span class="card-icon">:material-rocket-launch:</span>

### Publishing

How to regenerate all portal pages and deploy to the Azure Static Web Apps site after making architecture changes.
</a>

</div>

---

## How the Platform Works

Every architectural artifact follows the same flow:

```
Architect edits source files            CI detects push to main
(YAML, OpenAPI, Excalidraw)  ──push──►  Generators run (Python scripts)
                                         MkDocs builds the portal
                                         Site deploys to Azure SWA
                                         Confluence mirror updates
```

**Source files the architect owns:**

| File / Directory | What it models | Generator that reads it |
|---|---|---|
| `architecture/specs/*.yaml` | OpenAPI contracts for all services | `generate-microservice-pages.py`, `generate-swagger-pages.py` |
| `architecture/events/*.events.yaml` | AsyncAPI event schemas per service | `generate-event-pages.py` |
| `architecture/metadata/events.yaml` | Event catalog (channels, producers, consumers) | `generate-event-pages.py`, `generate-microservice-pages.py` |
| `architecture/metadata/data-stores.yaml` | DB schemas, tables, columns, indexes | `generate-microservice-pages.py` |
| `architecture/metadata/domains.yaml` | Service-to-domain assignments | `generate-microservice-pages.py`, `generate-topology-pages.py` |
| `architecture/metadata/capabilities.yaml` | L1/L2 capability definitions | `generate-capability-pages.py` |
| `architecture/metadata/capability-changelog.yaml` | Capability changes per solution | `generate-capability-pages.py`, `generate-solution-pages.py` |
| `architecture/metadata/tickets.yaml` | Ticket registry | `generate-ticket-pages.py` |
| `architecture/metadata/cross-service-calls.yaml` | Service-to-service integrations | `generate-microservice-pages.py` |
| `architecture/metadata/applications.yaml` | Front-end application registry | `generate-application-pages.py` |
| `architecture/wireframes/**/*.excalidraw` | UI wireframes | `generate-wireframe-pages.py` |
| `architecture/solutions/` | Solution design folders | `generate-solution-pages.py` |
| `decisions/` | ADRs | Static — served directly |
| `portal/docs/**/*.md` | Static portal pages | MkDocs |

---

## Platform Principles

These principles underpin all the workflows described in this handbook.

**Edit data, not documents.** Portal pages are generated from YAML and OpenAPI specs. Never manually edit files in `portal/docs/microservices/`, `portal/docs/solutions/`, `portal/docs/tickets/`, or `portal/docs/capabilities/` — they are overwritten by generators.

**Single source of truth.** Each fact lives in exactly one file. For example, service domain ownership lives in `domains.yaml`, not in a prose wiki page. If the same fact needs to appear in multiple places, generators produce the copies from the single source.

**Branch per solution.** All architectural work is done on a dedicated branch (`solution/NTK-XXXXX-slug`) and merged via pull request. No direct commits to `main` for solution work.

**Safety defaults.** Any unknown or unmapped adventure category must default to Pattern 3 (Full Service) — never Pattern 1. This is a safety constraint enforced by ADR-005.

**Backward compatibility.** Any change to a published OpenAPI schema is a contract change that may break consumers. Adding new required fields to response schemas requires a versioned migration path. See [API Contract Changes](api-contracts.md#versioning-considerations).

---

!!! tip "First time on the platform?"
    Start with [Working a Ticket](working-a-ticket.md) to understand how tickets flow through the architecture practice, then read [Solution Design](solution-design.md) for the full end-to-end workflow.
