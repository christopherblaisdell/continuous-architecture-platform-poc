# Metadata and Artifacts

Architecture at NovaTrek is modeled as structured data, not prose. This page explains the metadata-driven approach, what files you edit, and how those edits flow through to the portal.

---

## The Metadata-Driven Approach

Instead of writing free-form documentation, architects maintain **15 YAML metadata files** that describe the architecture. Generator scripts read these files and produce portal pages, diagrams, topology views, and capability maps.

This approach provides:

- **Consistency** — every service page follows the same structure because a script generates them all
- **Cross-linking** — generators create links between services, events, actors, and capabilities automatically
- **Validation** — YAML schema can be validated; prose cannot
- **Drift prevention** — the portal always reflects what's in the YAML; there's no way for documentation to silently diverge from the architecture
- **Automation** — CI/CD regenerates everything on every push to `main`

---

## Metadata Files Reference

All files live in [`architecture/metadata/`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/tree/main/architecture/metadata).

### Domain and Service Structure

| File | What It Defines | When to Edit |
|------|----------------|--------------|
| [`domains.yaml`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/metadata/domains.yaml) | 9 service domain groupings, colors, team ownership | Adding a new service or changing domain structure |
| [`cross-service-calls.yaml`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/metadata/cross-service-calls.yaml) | All inter-service API calls (the arrows in C4 diagrams) | Adding or changing how services interact |
| [`data-stores.yaml`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/metadata/data-stores.yaml) | Database engine, schema, tables, indexes, and features per service | Adding tables, indexes, or changing database structure |
| [`label-to-svc.yaml`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/metadata/label-to-svc.yaml) | Display label to service name mappings (e.g., "Reservations" -> "svc-reservations") | Adding a new service |
| [`delivery-status.yaml`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/metadata/delivery-status.yaml) | Service delivery waves (GA, beta, planning) | Changing a service's delivery status |

### People and Systems

| File | What It Defines | When to Edit |
|------|----------------|--------------|
| [`actors.yaml`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/metadata/actors.yaml) | Human actors, frontend apps, infrastructure, and external systems (39 total) | Adding new actor types or external integrations |
| [`applications.yaml`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/metadata/applications.yaml) | Frontend applications, screens, user journey steps | Adding screens or user flows |
| [`consumers.yaml`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/metadata/consumers.yaml) | Which frontend apps consume which services | Changing which apps call which services |
| [`app-titles.yaml`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/metadata/app-titles.yaml) | Frontend application display names | Updating app display names |

### Events and Integration

| File | What It Defines | When to Edit |
|------|----------------|--------------|
| [`events.yaml`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/metadata/events.yaml) | Kafka event producers, consumers, and topic mappings | Adding or changing domain events |

### Capabilities and Tickets

| File | What It Defines | When to Edit |
|------|----------------|--------------|
| [`capabilities.yaml`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/metadata/capabilities.yaml) | Business capability hierarchy — 7 L1 domains, 34 L2 capabilities | Defining new business capabilities |
| [`capability-changelog.yaml`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/metadata/capability-changelog.yaml) | Per-solution capability changes (L3 emergence and decisions) | After completing any solution design (REQUIRED) |
| [`tickets.yaml`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/metadata/tickets.yaml) | Ticket registry with service and capability mappings | Adding new tickets or updating ticket status |

### Operations and Compliance

| File | What It Defines | When to Edit |
|------|----------------|--------------|
| [`pci.yaml`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/metadata/pci.yaml) | PCI DSS compliance scope (services, externals, data flows) | Changing payment or card data handling |
| [`pipeline-registry.yaml`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/metadata/pipeline-registry.yaml) | CI/CD pipeline configurations per service | Updating deployment pipelines |

---

## Hand-Authored vs. Generated Artifacts

Understanding this distinction is critical. **Never edit generated files** — they will be overwritten on the next build.

### You Edit (Source of Truth)

| Category | Location | Examples |
|----------|----------|----------|
| Metadata YAML | [`architecture/metadata/`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/tree/main/architecture/metadata) | `domains.yaml`, `events.yaml`, `capabilities.yaml` |
| OpenAPI specs | [`architecture/specs/`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/tree/main/architecture/specs) | `svc-check-in.yaml` (23 specs total) |
| AsyncAPI event specs | [`architecture/events/`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/tree/main/architecture/events) | `svc-check-in.events.yaml` (8 specs total) |
| Solution designs | [`architecture/solutions/`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/tree/main/architecture/solutions) | `_NTK-10005-wristband-rfid-field/` |
| Global ADRs | [`decisions/`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/tree/main/decisions) | `ADR-005-pattern3-default-fallback.md` |
| Hand-authored diagrams | [`architecture/diagrams/`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/tree/main/architecture/diagrams) | C4 system context, component, and sequence diagrams |
| Wireframes | [`architecture/wireframes/`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/tree/main/architecture/wireframes) | Excalidraw `.excalidraw` files |
| Configuration | [`config/`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/tree/main/config) | `adventure-classification.yaml`, `test-standards.yaml` |
| Portal hand-authored pages | `portal/docs/` (selected files) | `platform-operations.md`, `security/*.md` |

### Scripts Generate (Do Not Edit)

| Output | Generator | Source |
|--------|-----------|--------|
| Microservice pages (19) | [`generate-microservice-pages.py`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/portal/scripts/generate-microservice-pages.py) | OpenAPI specs + all metadata YAML |
| Application pages (3) | [`generate-application-pages.py`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/portal/scripts/generate-application-pages.py) | `applications.yaml` + specs |
| Swagger UI pages (23) | [`generate-swagger-pages.py`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/portal/scripts/generate-swagger-pages.py) | OpenAPI specs |
| Endpoint sequence SVGs (139) | [`generate-microservice-pages.py`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/portal/scripts/generate-microservice-pages.py) | OpenAPI specs + cross-service-calls |
| Event catalog pages | [`generate-event-pages.py`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/portal/scripts/generate-event-pages.py) | AsyncAPI specs |
| Solution pages | [`generate-solution-pages.py`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/portal/scripts/generate-solution-pages.py) | Solution design master documents |
| Capability pages | [`generate-capability-pages.py`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/portal/scripts/generate-capability-pages.py) | `capabilities.yaml` + `capability-changelog.yaml` |
| Ticket pages | [`generate-ticket-pages.py`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/portal/scripts/generate-ticket-pages.py) | `tickets.yaml` + changelog |
| Topology pages | [`generate-topology-pages.py`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/portal/scripts/generate-topology-pages.py) | CALM JSON + metadata YAML |
| CALM topology JSON | [`generate-calm.py`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/scripts/generate-calm.py) | All metadata YAML + OpenAPI specs |
| Actor catalog | [`generate-microservice-pages.py`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/portal/scripts/generate-microservice-pages.py) | `actors.yaml` |

### The Central Loader

All generators import from [`portal/scripts/load_metadata.py`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/portal/scripts/load_metadata.py), which loads all 15 metadata YAML files into Python data structures. If you add a new metadata file, it needs a loader function here.

---

## How to Add a New Service

This is the most common metadata operation. Follow these steps in order:

1. **Add to `domains.yaml`** — assign the service to a domain and team
2. **Create the OpenAPI spec** — `architecture/specs/svc-new-service.yaml`
3. **Add to `data-stores.yaml`** — define the database, schema, and tables
4. **Add to `cross-service-calls.yaml`** — document all API calls to/from other services
5. **Add to `label-to-svc.yaml`** — map display label to service name
6. **Add to `events.yaml`** — if the service produces or consumes events
7. **Add nav entry** — add the service to `mkdocs.yml` under Microservices
8. **Regenerate** — run `bash portal/scripts/generate-all.sh`

---

## How to Add a New Event

1. **Create or update the AsyncAPI spec** — `architecture/events/svc-producer.events.yaml`
2. **Add to `events.yaml`** — declare the producer, consumers, topic, and event name
3. **Regenerate** — run `bash portal/scripts/generate-all.sh`

---

## How Schema Changes Flow to Production

Database index and schema changes follow a specific workflow from architecture metadata to production deployment. See the [Database Index Change Workflow](../database-change-workflow.md) for the complete 5-step process.

---

## Validation

### CALM topology validation

After changing metadata, validate the generated CALM topology:

```bash
python3 scripts/validate-calm.py
```

This checks referential integrity — every service referenced in cross-service calls exists in domains, every event producer exists, etc.

### Portal build validation

```bash
cd portal && python3 -m mkdocs build --strict
```

The `--strict` flag treats warnings as errors, catching broken links and missing references.

---

## For More Detail

- [Artifact Registry](../artifact-registry.md) — complete inventory with actor ownership
- [Metadata Registry Standard](../standards/metadata-registry/index.md) — why YAML, not prose
- [Portal Publishing](portal-publishing.md) — build and deploy workflow
