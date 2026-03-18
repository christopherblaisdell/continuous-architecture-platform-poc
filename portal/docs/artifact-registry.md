# Artifact Registry

This page documents every artifact in the NovaTrek Architecture Platform -- what is hand-authored (source of truth), what is generated, and how each actor changes and publishes them.

---

## Actors

| Actor | Role | Primary Artifacts |
|-------|------|-------------------|
| **Solution Architect** | Owns architecture metadata, API contracts, solution designs, decisions, and diagrams. Proposes and documents architectural changes. | Metadata YAML, OpenAPI specs, AsyncAPI specs, solution designs, ADRs, PlantUML diagrams, wireframes |
| **Software Developer** | Implements approved designs in service source code, writes tests, and proposes API contract updates when implementation reveals contract gaps. | Service source code, test suites, contract tests. Proposes changes to OpenAPI specs and metadata YAML via pull request. |

---

## Defined Artifacts (Source of Truth)

These files are hand-authored. All generated pages, diagrams, and portal content derive from them.

### Architecture Metadata

| File | Defines | Edited By |
|------|---------|-----------|
| `architecture/metadata/domains.yaml` | Service domain groupings (9 domains), colors, team ownership | Solution Architect |
| `architecture/metadata/cross-service-calls.yaml` | All inter-service API calls (the arrows in C4 diagrams) | Solution Architect |
| `architecture/metadata/data-stores.yaml` | Database engine, schema, tables, and features per service | Solution Architect |
| `architecture/metadata/applications.yaml` | Frontend applications, screens, user journey steps | Solution Architect |
| `architecture/metadata/actors.yaml` | Human actors, frontend apps, infrastructure, and external systems | Solution Architect |
| `architecture/metadata/events.yaml` | Kafka event producers, consumers, and topic mappings | Solution Architect |
| `architecture/metadata/consumers.yaml` | Which frontend apps consume which services | Solution Architect |
| `architecture/metadata/capabilities.yaml` | Business capability hierarchy (L1 domains, L2 capabilities) | Solution Architect |
| `architecture/metadata/capability-changelog.yaml` | Per-solution capability changes (L3 emergence, decisions) | Solution Architect |
| `architecture/metadata/tickets.yaml` | Ticket registry with service and capability mappings | Solution Architect |
| `architecture/metadata/pci.yaml` | PCI DSS compliance scope (services, externals, data flows) | Solution Architect |
| `architecture/metadata/label-to-svc.yaml` | Display label to service name mappings | Solution Architect |
| `architecture/metadata/delivery-status.yaml` | Service delivery waves (GA, beta, planning) | Solution Architect |
| `architecture/metadata/pipeline-registry.yaml` | CI/CD pipeline configurations per service | Solution Architect |
| `architecture/metadata/app-titles.yaml` | Frontend application display names and metadata | Solution Architect |

### API Contracts

| File | Defines | Edited By |
|------|---------|-----------|
| `architecture/specs/*.yaml` (23 files) | OpenAPI 3.x REST API contracts for every microservice | Solution Architect (primary), Software Developer (via PR) |
| `architecture/events/*.events.yaml` (8 files) | AsyncAPI event schemas, producers, and consumers | Solution Architect (primary), Software Developer (via PR) |

### Solution Designs

| File | Defines | Edited By |
|------|---------|-----------|
| `architecture/solutions/_NTK-XXXXX-slug/` | Complete architecture change proposals per ticket | Solution Architect |
| `NTK-XXXXX-solution-design.md` | Master solution document | Solution Architect |
| `1.requirements/` | Ticket requirements report | Solution Architect |
| `2.analysis/` | Plain-language explanation of the problem | Solution Architect |
| `3.solution/a.assumptions/` | Assumptions not yet verified | Solution Architect |
| `3.solution/c.capabilities/capabilities.md` | Capability mappings (references changelog) | Solution Architect |
| `3.solution/d.decisions/decisions.md` | MADR-formatted architecture decisions | Solution Architect |
| `3.solution/g.guidance/` | Implementation guidance for developers | Solution Architect |
| `3.solution/i.impacts/` | Per-service impact assessments | Solution Architect |
| `3.solution/r.risks/` | Risk register | Solution Architect |
| `3.solution/u.user.stories/` | User stories with acceptance criteria | Solution Architect |

### Architecture Decisions

| File | Defines | Edited By |
|------|---------|-----------|
| `decisions/ADR-*.md` (9 files) | Global architecture decisions in MADR format | Solution Architect |

### Hand-Authored Diagrams

| File | Defines | Edited By |
|------|---------|-----------|
| `architecture/diagrams/System/*.puml` | C4 System Context diagrams | Solution Architect |
| `architecture/diagrams/Components/*.puml` | C4 Component diagrams per domain | Solution Architect |
| `architecture/diagrams/Sequence/*.puml` | Cross-service sequence diagrams | Solution Architect |
| `architecture/diagrams/Tickets/*.puml` | Ticket-specific diagrams | Solution Architect |
| `architecture/diagrams/endpoints/*.puml` | Per-endpoint diagram overrides (replace generated versions) | Solution Architect |
| `architecture/diagrams/theme.puml` | PlantUML color theme (derived from domains.yaml) | Solution Architect |
| `architecture/diagrams/include.puml` | Shared PlantUML macros and skinparams | Solution Architect |
| `architecture/diagrams/templates.puml` | Reusable diagram templates | Solution Architect |

### Wireframes

| File | Defines | Edited By |
|------|---------|-----------|
| `architecture/wireframes/web-guest-portal/*.excalidraw` | Guest portal screen designs | Solution Architect |
| `architecture/wireframes/web-ops-dashboard/*.excalidraw` | Operations dashboard screen designs | Solution Architect |
| `architecture/wireframes/app-guest-mobile/*.excalidraw` | Mobile app screen designs | Solution Architect |

### Configuration

| File | Defines | Edited By |
|------|---------|-----------|
| `config/adventure-classification.yaml` | 25 adventure categories mapped to UX patterns (1/2/3) | Solution Architect |
| `config/test-standards.yaml` | TDD/BDD testing conventions (ADR-012) | Solution Architect |
| `config/sonar-project.properties` | SonarQube analysis configuration | Software Developer |

### Service Source Code

| File | Defines | Edited By |
|------|---------|-----------|
| `services/svc-*/` (19 services) | Java/Spring Boot microservice implementations | Software Developer |
| `services/template/` | Service scaffold template | Software Developer |

### Portal Configuration

| File | Defines | Edited By |
|------|---------|-----------|
| `portal/mkdocs.yml` | MkDocs Material navigation and theme | Solution Architect |
| `staticwebapp.config.json` | Azure Static Web App routing, headers, CSP | Solution Architect |
| `requirements-docs.txt` | Python dependencies for portal generators | Solution Architect |

### Infrastructure

| File | Defines | Edited By |
|------|---------|-----------|
| `infra/main.bicep` | Azure Static Web App resource | Software Developer |
| `infra/platform.bicep` | Platform-level Azure resources | Software Developer |
| `infra/deploy.sh` | Portal deployment script | Software Developer |
| `infra/db/` | Database schemas and migrations | Software Developer |

### Hand-Authored Documentation

| File | Defines | Edited By |
|------|---------|-----------|
| `docs/*.md` (20+ files) | Guides, research, phase outputs, comparisons | Solution Architect |
| `portal/docs/platform-operations.md` | Platform operations overview | Solution Architect |
| `portal/docs/security/*.md` | Security model documentation | Solution Architect |
| `portal/docs/standards/**/*.md` | arc42, C4, MADR, OpenAPI, quality model standards | Solution Architect |

### CI/CD Workflows

| File | Defines | Edited By |
|------|---------|-----------|
| `.github/workflows/docs-deploy.yml` | Portal build and deployment pipeline | Software Developer |
| `.github/workflows/validate-solution.yml` | Solution design validation checks | Software Developer |
| `.github/copilot-instructions.md` | AI agent instructions for this workspace | Solution Architect |

---

## Generated Artifacts

These are produced by scripts from the defined artifacts above. Never edit generated files directly -- they will be overwritten on the next build.

### Portal Pages (Markdown)

| Generator Script | Reads From | Writes To | Output |
|------------------|-----------|-----------|--------|
| `portal/scripts/generate-swagger-pages.py` | `architecture/specs/*.yaml` | `portal/docs/services/api/` | Swagger UI HTML pages (23 services) |
| `portal/scripts/generate-microservice-pages.py` | `architecture/specs/*.yaml` + all metadata YAML | `portal/docs/microservices/` + `puml/` + `svg/` | Service pages, endpoint sequence SVGs, C4 context SVGs, ERD SVGs, enterprise diagram, event flow diagram, actor catalog |
| `portal/scripts/generate-application-pages.py` | `architecture/metadata/applications.yaml` + specs | `portal/docs/applications/` + `puml/` + `svg/` | App pages, user journey SVGs, C4 app context SVGs |
| `portal/scripts/generate-wireframe-pages.py` | `architecture/wireframes/**/*.excalidraw` | `portal/docs/applications/*/wireframes/` | SVG previews, HTML viewers, Markdown wrappers |
| `portal/scripts/generate-event-pages.py` | `architecture/events/*.events.yaml` | `portal/docs/events/` | AsyncAPI event catalog pages |
| `portal/scripts/generate-solution-pages.py` | `architecture/solutions/*/NTK-*-solution-design.md` | `portal/docs/solutions/` | Solution index + detail pages |
| `portal/scripts/generate-capability-pages.py` | `capabilities.yaml` + `capability-changelog.yaml` | `portal/docs/capabilities/` | Capability hierarchy + timeline pages |
| `portal/scripts/generate-ticket-pages.py` | `tickets.yaml` + `capability-changelog.yaml` | `portal/docs/tickets/` | Ticket index + detail pages |
| `portal/scripts/generate-topology-pages.py` | `architecture/calm/*.json` + metadata YAML | `portal/docs/topology/` | System map, dependency matrix, domain views |
| `portal/scripts/generate-svgs.sh` | `architecture/diagrams/**/*.puml` | `portal/docs/diagrams/svg/` | Standalone C4 and sequence diagram SVGs |

### CALM Topology

| Generator Script | Reads From | Writes To | Output |
|------------------|-----------|-----------|--------|
| `scripts/generate-calm.py` | All metadata YAML + OpenAPI specs | `architecture/calm/novatrek-topology.json` + per-domain JSON | CALM-formatted system topology |
| `scripts/validate-calm.py` | `architecture/calm/*.json` | stdout (validation report) | Topology integrity check |

### Metadata Loader

| Module | Purpose |
|--------|---------|
| `portal/scripts/load_metadata.py` | Central Python module that loads all 15 metadata YAML files into Python data structures. All generators import from this module. |

### Confluence Mirror

| Generator Script | Reads From | Writes To | Output |
|------------------|-----------|-----------|--------|
| `portal/scripts/confluence-prepare.py` | `portal/docs/**/*.md` (generated + hand-authored) | `portal/confluence/` | Confluence-compatible Markdown with `mark` headers |
| `portal/scripts/confluence-lock-pages.py` | Confluence REST API | Confluence page restrictions | Edit locks on auto-generated pages |
| `portal/scripts/confluence-drift-check.py` | Confluence REST API + `portal/confluence/` | stdout (drift report) | Detects unauthorized edits |

### Multi-Site Sync

| Tool | Reads From | Writes To | Output |
|------|-----------|-----------|--------|
| `sites/sync-sites.py` | `docs/*.md` + `sites/manifest.yaml` | `portal/docs/` + `sites/ai-customization/docs/` | Copies shared docs with per-site link rewrites |

### MkDocs HTML Site

| Tool | Reads From | Writes To | Output |
|------|-----------|-----------|--------|
| `python3 -m mkdocs build` (from `portal/`) | All `portal/docs/**/*.md` | `portal/site/` | Complete HTML portal |

---

## Build Pipeline

All generation runs through a single entry point:

```
bash portal/scripts/generate-all.sh
```

This executes 11 stages in order:

1. Swagger UI pages
2. Microservice pages (Markdown + PlantUML + SVG)
3. Application pages (Markdown + PlantUML + SVG)
4. Wireframe pages (Excalidraw to SVG + HTML + Markdown)
5. AsyncAPI event pages
6. Solution design pages
7. Business capability pages
8. Ticket pages
9. CALM topology generation + validation + domain subsets
10. Standalone PlantUML diagram SVGs
11. MkDocs build + asset copy to `site/`

After building, deployment uses:

```
swa deploy site --deployment-token "<token>" --env production
```

Or via CI: the `docs-deploy.yml` GitHub Action handles build + deployment automatically on push to `main`.

---

## How to Change and Publish: Solution Architect

### Change architecture metadata

1. Edit the relevant YAML file in `architecture/metadata/`
2. Commit and push to `main`
3. CI runs `generate-all.sh` automatically, regenerates all affected portal pages, and deploys

**Local preview (optional):**

```bash
bash portal/scripts/generate-all.sh
cd portal && python3 -m mkdocs serve
```

### Change an API contract

1. Edit the OpenAPI spec in `architecture/specs/{svc-name}.yaml`
2. Verify backward compatibility (new required fields break consumers)
3. Commit and push to `main`
4. CI regenerates Swagger UI pages, microservice deep-dive pages, and sequence diagrams

### Add a new service

1. Add the service to `architecture/metadata/domains.yaml` (assign to a domain)
2. Create `architecture/specs/{svc-name}.yaml` (OpenAPI spec)
3. Add entries to `data-stores.yaml`, `cross-service-calls.yaml`, and `label-to-svc.yaml`
4. Add entries to `events.yaml` if the service produces or consumes events
5. Add nav entry to `portal/mkdocs.yml` under Services > Microservices
6. Commit and push -- CI generates the new microservice page, diagrams, and Swagger UI

### Create a solution design

1. Create branch: `git checkout -b solution/NTK-XXXXX-slug`
2. Create folder: `architecture/solutions/_NTK-XXXXX-slug/`
3. Populate the standard folder structure (see Solution Designs table above)
4. Add entry to `architecture/metadata/capability-changelog.yaml`
5. Update `architecture/metadata/tickets.yaml` if needed
6. Push branch, open PR, merge to `main`
7. CI generates the solution page and updates capability/ticket pages

### Add or update a diagram

**Hand-crafted diagram:**

1. Edit or create `.puml` file in `architecture/diagrams/{System,Components,Sequence,Tickets}/`
2. Follow C4 notation (use `!include <c4/C4_Container>` or `!include ../theme.puml`)
3. Commit and push -- CI renders to SVG via `generate-svgs.sh`

**Endpoint diagram override:**

1. Create `.puml` file in `architecture/diagrams/endpoints/` matching the generated filename
2. The generator checks this directory first and uses the override instead of auto-generating
3. Commit and push -- CI uses the override

### Add an architecture decision

1. Determine the next ADR number from `decisions/`
2. Create `decisions/ADR-{NNN}-{slug}.md` using MADR format from `standards/madr/adr-template.md`
3. If the decision belongs to a solution, also add it to `3.solution/d.decisions/decisions.md`
4. Commit and push

### Update a wireframe

1. Edit the `.excalidraw` file in `architecture/wireframes/{app}/` using the VS Code Excalidraw extension or excalidraw.com
2. Commit only the `.excalidraw` source file
3. Push -- CI generates SVG + HTML + Markdown wrapper automatically

### Add an event

1. Add the event to the producer's AsyncAPI spec in `architecture/events/{svc-name}.events.yaml`
2. Add the event to `architecture/metadata/events.yaml` (producer, consumers, topic)
3. Commit and push -- CI regenerates event catalog pages and updates microservice pages

### Update portal navigation

1. Edit `portal/mkdocs.yml` under the `nav:` section
2. Commit and push

---

## How to Change and Publish: Software Developer

### Change service source code

1. Edit files in `services/{svc-name}/`
2. Run tests locally: `cd services/{svc-name} && ./mvnw test`
3. Commit and push -- CI runs `service-ci.yml` (build + test)

NOTE: Source code changes do not affect the architecture portal. If the implementation reveals an API contract gap (missing field, new endpoint, changed behavior), propose the contract change separately.

### Propose an API contract change

1. Create a branch
2. Edit the OpenAPI spec in `architecture/specs/{svc-name}.yaml`
3. If the change affects cross-service calls, update `architecture/metadata/cross-service-calls.yaml`
4. Push the branch and open a pull request
5. The Solution Architect reviews and approves the contract change
6. On merge, CI regenerates all affected portal pages

### Propose a metadata change

1. Create a branch
2. Edit the relevant file in `architecture/metadata/`
3. Push and open a pull request for Solution Architect review
4. On merge, CI regenerates affected portal pages

### Add a new service implementation

1. Copy `services/template/` to `services/{svc-name}/`
2. Implement the API contract defined in `architecture/specs/{svc-name}.yaml`
3. Write contract tests against the OpenAPI spec (ADR-013)
4. Add database migrations to `infra/db/` if needed
5. Push and open a pull request

### Update infrastructure

1. Edit Bicep files in `infra/`
2. Test locally: `az deployment group what-if`
3. Push -- CI runs `infra-deploy.yml`

### Update CI/CD workflows

1. Edit `.github/workflows/*.yml`
2. Push to a branch and verify via GitHub Actions "dry run" or test workflow

### Run the portal build locally

```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies (first time only)
pip install -r requirements-docs.txt

# Generate all artifacts and build
bash portal/scripts/generate-all.sh

# Serve locally for preview
cd portal && python3 -m mkdocs serve
```

### Regenerate a single artifact type

```bash
# Only microservice pages
python3 portal/scripts/generate-microservice-pages.py

# Only capability pages
python3 portal/scripts/generate-capability-pages.py

# Only CALM topology
python3 scripts/generate-calm.py

# Only hand-crafted diagram SVGs
bash portal/scripts/generate-svgs.sh
```

---

## Key Rules

1. **Never edit generated files.** They live in `portal/docs/microservices/`, `portal/docs/applications/`, `portal/docs/solutions/`, `portal/docs/capabilities/`, `portal/docs/tickets/`, `portal/docs/topology/`, `portal/docs/services/api/`, `portal/docs/events/`, `portal/docs/actors/`, and `portal/docs/diagrams/svg/`. Edit the source files instead.

2. **Solution Architects own all architecture metadata.** Software Developers propose changes via pull request.

3. **One push rebuilds everything.** The CI pipeline runs the full `generate-all.sh` on every push to `main` that touches architecture or documentation files.

4. **Capability changes go in the changelog.** Every solution that affects capabilities must add an entry to `architecture/metadata/capability-changelog.yaml` -- this is the single source of truth for L3 capability emergence.

5. **API contracts are the shared boundary.** Solution Architects define the contract (OpenAPI spec). Software Developers implement it. Contract tests (ADR-013) verify alignment.
