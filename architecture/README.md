# Architecture Source Files

**This is where architects work.** Edit the YAML files below, commit, push — the portal rebuilds automatically.

## Folder Structure

| Folder | What's Inside | When to Edit |
|--------|---------------|--------------|
| `specs/` | 19 OpenAPI YAML files — one per microservice | Adding/changing API endpoints, request/response schemas, or error codes |
| `events/` | 6 AsyncAPI YAML files — one per event-producing service | Adding/changing domain events, channels, or message schemas |
| `metadata/` | 10 YAML files — domain classifications, data stores, integrations, actors, and more | Adding a new service, changing cross-service integrations, updating database schemas, or modifying domain groupings |

## Quick Start

1. **Find the file** you need in one of the three folders above
2. **Edit the YAML** using your preferred editor
3. **Commit and push** to `main`
4. **CI rebuilds the portal** automatically — Swagger UI pages, microservice deep-dive pages, sequence diagrams, and event catalog all regenerate

## What Gets Generated From These Files

```
architecture/specs/*.yaml       -->  Swagger UI pages + sequence diagrams + microservice pages
architecture/events/*.yaml      -->  AsyncAPI interactive viewers + event catalog
architecture/metadata/*.yaml    -->  Domain classifications, data store docs, cross-service
                                     integration maps, actor definitions, PCI annotations
```

## Metadata File Reference

| File | Purpose |
|------|---------|
| `metadata/domains.yaml` | Groups services into domains (Operations, Booking, Safety, etc.) with colors |
| `metadata/data-stores.yaml` | Database engine, schema, tables, columns, and indexes for each service |
| `metadata/cross-service-calls.yaml` | Maps every cross-service API call (who calls whom, which endpoint) |
| `metadata/events.yaml` | Event catalog — producers, channels, event names, and consumers |
| `metadata/actors.yaml` | Human and system actors that interact with services |
| `metadata/applications.yaml` | Frontend applications — tech stack, screens, API dependencies |
| `metadata/consumers.yaml` | Which services consume each event |
| `metadata/pci.yaml` | PCI-DSS scope — compliant services and sensitive data flows |
| `metadata/label-to-svc.yaml` | Display label to service name mapping (e.g., "Reservations" to "svc-reservations") |
| `metadata/app-titles.yaml` | Application display titles |

## Do NOT Edit These Locations

Generated output lives under `portal/` — these files are overwritten on every build:

- `portal/docs/microservices/*.md` — generated microservice pages
- `portal/docs/microservices/puml/` and `svg/` — generated diagrams
- `portal/docs/applications/*.md` — generated application pages
- `portal/docs/services/api/*.html` — generated Swagger UI pages
- `portal/docs/events-ui/*.html` — generated AsyncAPI viewers
- `portal/site/` — MkDocs build output

## Local Build

To test your changes locally before pushing:

```bash
bash portal/scripts/generate-all.sh
```

This runs all generators and builds the MkDocs site. Open `portal/site/index.html` to preview.
