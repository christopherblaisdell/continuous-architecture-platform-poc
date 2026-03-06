# Portal Separation of Concerns Plan

**Date**: 2026-03-06
**Status**: Proposed
**Author**: Architecture Practice

---

## Problem Statement

The NovaTrek Architecture Portal currently embeds all service metadata (data stores, cross-service integrations, event catalogs, PCI flows, application screens, actor definitions) inside Python generator scripts. This creates several problems:

1. **Architects must edit Python code** to change metadata -- a 3,400-line script for microservices, an 844-line script for applications
2. **No incremental builds** -- changing one spec regenerates all 19 services
3. **Generated artifacts are committed to git** -- Swagger HTML, microservice markdown, SVGs, and application markdown are all checked in, creating noisy diffs and merge conflicts
4. **CI does not run generators** -- the GitHub Actions pipeline only runs `mkdocs build`; architects must manually run 3 generators + PlantUML rendering before committing
5. **6-step manual process** -- forgetting any step produces silent failures (blank diagrams, stale HTML)
6. **AI is not mandatory but practically required** -- the system was designed for AI-driven workflows, not human architects

---

## Design Principles

1. **Source artifacts are what architects edit** -- YAML specs, PUML diagrams, metadata YAML files
2. **Generated artifacts are what the pipeline produces** -- HTML, rendered SVGs, Markdown pages
3. **CI handles ALL generation** -- architects edit, commit, push; the pipeline does the rest
4. **No hand-coded HTML required** -- all HTML (Swagger UI, AsyncAPI) is generated from templates
5. **Both AI and human architects can use it** -- editing a YAML file should be all that is needed
6. **Git contains source of truth only** -- generated artifacts are excluded from version control

---

## Current Architecture (Before)

```
portal/
  docs/
    specs/                    <-- SOURCE: OpenAPI YAML (19 files)
    events/                   <-- SOURCE: AsyncAPI YAML (6 files) + GENERATED: index.md
    services/api/             <-- GENERATED: Swagger HTML (19 files) -- committed to git
    microservices/            <-- GENERATED: Markdown pages (19 files) -- committed to git
    microservices/puml/       <-- GENERATED: PlantUML files (185 files) -- committed to git
    microservices/svg/        <-- GENERATED: SVG diagrams (185 files) -- committed to git
    applications/             <-- GENERATED: Markdown pages (3 files) -- committed to git
    applications/puml/        <-- GENERATED: PlantUML files -- committed to git
    applications/svg/         <-- GENERATED: SVG diagrams -- committed to git
    actors/index.md           <-- GENERATED -- committed to git
  scripts/
    generate-microservice-pages.py   <-- 3,408 lines (metadata + generation logic)
    generate-swagger-pages.py        <-- 547 lines (metadata + HTML template)
    generate-application-pages.py    <-- 844 lines (metadata + generation logic)
    generate-event-pages.py          <-- 155 lines (HTML template)
    generate-svgs.sh                 <-- 35 lines (hardcoded file list)
```

### Current Workflow (6 Manual Steps)

```
Architect edits spec
    |
    v
Run generate-swagger-pages.py       <-- manual, regenerates ALL 19 HTML files
    |
    v
Run generate-microservice-pages.py   <-- manual, regenerates ALL 19 MD + 185 PUML + 185 SVG
    |
    v
Run generate-application-pages.py    <-- manual, regenerates ALL 3 app pages + diagrams
    |
    v
mkdocs serve (verify locally)        <-- manual
    |
    v
git add + commit + push              <-- must remember to add ALL generated files
    |
    v
CI runs mkdocs build + deploy        <-- only builds static site, no generation
```

---

## Target Architecture (After)

```
portal/
  docs/
    specs/                    <-- SOURCE: OpenAPI YAML (19 files)
    events/                   <-- SOURCE: AsyncAPI YAML (6 files)
    metadata/
      domains.yaml            <-- SOURCE: Domain classification + colors
      data-stores.yaml        <-- SOURCE: Database schemas for all 19 services
      cross-service-calls.yaml <-- SOURCE: Integration map between services
      events.yaml             <-- SOURCE: Event catalog (channel, producer, consumers)
      actors.yaml             <-- SOURCE: External systems, apps, infrastructure
      pci.yaml                <-- SOURCE: PCI compliance scope and data flows
      applications.yaml       <-- SOURCE: Application definitions + screen flows
      consumers.yaml          <-- SOURCE: Per-service consuming application map
    diagrams/                 <-- SOURCE: Hand-crafted PUML diagrams (optional overrides)
    services/api/             <-- GENERATED (gitignored)
    microservices/            <-- GENERATED (gitignored)
    applications/             <-- GENERATED (gitignored, except custom content)
    actors/                   <-- GENERATED (gitignored)
  scripts/
    generate-microservice-pages.py   <-- Reads metadata from YAML, generates pages + PUML + SVG
    generate-swagger-pages.py        <-- Reads specs, generates Swagger HTML
    generate-application-pages.py    <-- Reads applications.yaml, generates pages + PUML + SVG
    generate-event-pages.py          <-- Reads AsyncAPI specs, generates HTML
    generate-all.sh                  <-- Single entry point: runs all generators in order
```

### Target Workflow (2 Steps)

```
Architect edits source artifact (YAML spec, metadata YAML, or PUML diagram)
    |
    v
git commit + push
    |
    v
CI runs generate-all.sh + mkdocs build + deploy   <-- fully automated
```

---

## Implementation Plan

### Phase 1: Extract Metadata into YAML Files

Create `portal/docs/metadata/` with the following YAML files extracted from the Python generators.

#### 1.1 domains.yaml

Extract `DOMAINS` dict from `generate-microservice-pages.py` (lines 30-62) and `generate-swagger-pages.py` (lines 28-77).

```yaml
# portal/docs/metadata/domains.yaml
Operations:
  color: "#2563eb"
  icon: clipboard-check
  services:
    - svc-check-in
    - svc-scheduling-orchestrator

Guest Identity:
  color: "#7c3aed"
  icon: account-group
  services:
    - svc-guest-profiles
# ... all 9 domains
```

#### 1.2 data-stores.yaml

Extract `DATA_STORES` dict from `generate-microservice-pages.py` (lines 93-1068). Approximately 975 lines of Python dict become a clean YAML file.

```yaml
# portal/docs/metadata/data-stores.yaml
svc-check-in:
  engine: PostgreSQL 15
  schema: checkin
  tables:
    - check_ins
    - gear_verifications
    - wristband_assignments
  features:
    - Row-level security per location
    - Partitioned by check_in_date (monthly)
  volume: ~2,000 check-ins/day peak season
  connection_pool:
    min: 5
    max: 20
    idle_timeout: 300
  backup: Continuous WAL archiving, 30-day PITR
  table_details:
    check_ins:
      columns:
        - name: check_in_id
          type: UUID
          pk: true
          default: gen_random_uuid()
        # ... all columns
      indexes:
        - name: idx_checkins_reservation
          columns: [reservation_id]
        # ... all indexes
# ... all 19 services
```

#### 1.3 cross-service-calls.yaml

Extract `CROSS_SERVICE_CALLS` dict from `generate-microservice-pages.py` (lines 1069-1323).

```yaml
# portal/docs/metadata/cross-service-calls.yaml
svc-check-in:
  POST /check-ins:
    - alias: GP
      label: Guest Profiles
      action: Verify guest identity
      async: false
      target:
        method: GET
        path: /guests/{guest_id}
    - alias: Res
      label: Reservations
      action: Validate reservation
      async: false
      target:
        method: GET
        path: /reservations/{reservation_id}
    # ... remaining integrations
# ... all services with cross-service calls
```

#### 1.4 events.yaml

Extract `EVENT_CATALOG` dict from `generate-microservice-pages.py` (lines 1328-1356).

```yaml
# portal/docs/metadata/events.yaml
reservation.created:
  channel: novatrek.booking.reservation.created
  producer: svc-reservations
  trigger:
    method: POST
    path: /reservations
  consumers:
    - svc-scheduling-orchestrator
    - svc-analytics
  domain: Booking
  summary: Published when a new reservation is confirmed
# ... all 7 events
```

#### 1.5 actors.yaml

Extract `ACTORS` dict from `generate-microservice-pages.py` (lines 1433-1546).

```yaml
# portal/docs/metadata/actors.yaml
human:
  - name: Guest
    icon: person
    description: End-user who books and participates in NovaTrek adventures
    interactions:
      - svc-guest-profiles
      - svc-reservations
      - svc-check-in
    # ...
frontend:
  - name: web-guest-portal
    label: NovaTrek Guest Portal
    tech: React 18, TypeScript, Vite
    # ...
infrastructure:
  - name: API Gateway
    label: Azure API Management
    # ...
external:
  - name: Payment Gateway
    label: Stripe
    pci: true
    # ...
```

#### 1.6 pci.yaml

Extract PCI configuration from `generate-microservice-pages.py` (lines 79-89).

```yaml
# portal/docs/metadata/pci.yaml
services:
  - svc-payments
externals:
  - Payment Gateway
  - Stripe API
  - Fraud Detection API
data_flows:
  - [svc-reservations, svc-payments]
  - [svc-partner-integrations, svc-payments]
  - [svc-loyalty-rewards, svc-payments]
  - [svc-inventory-procurement, svc-payments]
  - [svc-payments, Payment Gateway]
  - [svc-payments, Stripe API]
  - [svc-payments, Fraud Detection API]
```

#### 1.7 applications.yaml

Extract `APPLICATIONS` dict from `generate-application-pages.py` (lines 66-560).

```yaml
# portal/docs/metadata/applications.yaml
web-guest-portal:
  title: NovaTrek Guest Portal
  type: Web
  type_icon: ":material-web:"
  tech: React 18, TypeScript, Vite, Tailwind CSS
  team: Guest Experience Team
  color: "#2563eb"
  description: Public-facing website where guests browse adventures...
  client_label: Browser
  client_icon: browser
  screens:
    Trip Browser:
      description: Search and explore available adventures...
      steps:
        - alias: TC
          service: svc-trip-catalog
          action: Search available trips
          method: GET
          path: /trips
          async: false
        # ... remaining steps
    # ... remaining screens
# ... remaining applications
```

#### 1.8 consumers.yaml

Extract `APP_CONSUMERS` dict from `generate-microservice-pages.py` (lines 1368-1423).

```yaml
# portal/docs/metadata/consumers.yaml
svc-trip-catalog:
  - app: web-guest-portal
    screen: Trip Browser
  - app: web-guest-portal
    screen: Booking Flow
  - app: app-guest-mobile
    screen: My Reservations
# ... all 19 services
```

### Phase 2: Refactor Generators to Read YAML Metadata

Modify all generator scripts to load metadata from `portal/docs/metadata/*.yaml` instead of hardcoded Python dictionaries.

#### 2.1 generate-microservice-pages.py

- Remove inline `DOMAINS`, `DATA_STORES`, `CROSS_SERVICE_CALLS`, `EVENT_CATALOG`, `ACTORS`, `APP_CONSUMERS`, `PCI_*` dicts
- Add `load_metadata()` function that reads from `portal/docs/metadata/`
- Convert loaded YAML structures into the internal format the generator already expects
- Keep all generation logic (PUML building, markdown rendering, PlantUML invocation) unchanged
- Expected reduction: ~1,500 lines removed from Python, replaced by ~20 lines of YAML loading

#### 2.2 generate-swagger-pages.py

- Remove inline `DOMAINS` dict
- Load from `portal/docs/metadata/domains.yaml`
- Keep HTML template and generation logic unchanged

#### 2.3 generate-application-pages.py

- Remove inline `APPLICATIONS` dict
- Load from `portal/docs/metadata/applications.yaml`
- Convert YAML step format to the tuple format the generator expects internally
- Keep all diagram generation and page rendering unchanged

#### 2.4 generate-event-pages.py

- No metadata changes needed (already reads AsyncAPI YAML directly)
- No refactoring required

### Phase 3: Create Unified Build Script

Create `portal/scripts/generate-all.sh` as a single entry point.

```bash
#!/bin/bash
# Generate all portal artifacts from source files.
# This is the ONLY script architects need to know about.
# CI runs this automatically -- manual execution is optional for local preview.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PORTAL_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== NovaTrek Architecture Portal - Full Build ==="
echo ""

# Step 1: Generate Swagger UI HTML pages from OpenAPI specs
echo "[1/5] Generating Swagger UI pages..."
python3 "$SCRIPT_DIR/generate-swagger-pages.py"

# Step 2: Generate AsyncAPI UI pages from event specs
echo "[2/5] Generating AsyncAPI pages..."
python3 "$SCRIPT_DIR/generate-event-pages.py"

# Step 3: Generate microservice pages + PUML + SVG from specs + metadata
echo "[3/5] Generating microservice pages and diagrams..."
python3 "$SCRIPT_DIR/generate-microservice-pages.py"

# Step 4: Generate application pages + PUML + SVG from metadata
echo "[4/5] Generating application pages and diagrams..."
python3 "$SCRIPT_DIR/generate-application-pages.py"

# Step 5: Build MkDocs site
echo "[5/5] Building MkDocs site..."
cd "$PORTAL_DIR"
python3 -m mkdocs build --strict

# Copy non-markdown assets into site output (MkDocs does not copy these)
cp -r docs/services/api site/services/ 2>/dev/null || true
cp -r docs/specs site/ 2>/dev/null || true
cp -r docs/microservices/svg site/microservices/ 2>/dev/null || true
cp -r docs/applications/svg site/applications/ 2>/dev/null || true
cp -r docs/events-ui site/ 2>/dev/null || true
cp -r docs/diagrams/svg site/diagrams/ 2>/dev/null || true
cp staticwebapp.config.json site/ 2>/dev/null || true

echo ""
echo "=== Build complete ==="
echo "Output: $PORTAL_DIR/site/"
```

### Phase 4: Update CI Pipeline

Modify `.github/workflows/docs-deploy.yml` to run the full generation pipeline.

#### Changes:

1. **Add PlantUML installation** -- install Java + PlantUML in the CI runner
2. **Add path triggers** for portal source artifacts:
   - `portal/docs/specs/**`
   - `portal/docs/events/**`
   - `portal/docs/metadata/**`
   - `portal/docs/diagrams/**`
   - `portal/scripts/**`
3. **Replace `mkdocs build --strict`** with `bash portal/scripts/generate-all.sh`
4. **Remove manual `cp` commands** -- they are now inside `generate-all.sh`

#### New CI Build Steps:

```yaml
- name: Install PlantUML
  run: |
    sudo apt-get update -qq
    sudo apt-get install -y -qq plantuml

- name: Generate all portal artifacts and build site
  working-directory: portal
  run: bash scripts/generate-all.sh
```

### Phase 5: Update .gitignore

Add generated artifacts to `.gitignore` so only source files are tracked.

```gitignore
# Portal generated artifacts (produced by CI from source YAML/PUML)
portal/docs/services/api/*.html
portal/docs/services/index.md
portal/docs/microservices/*.md
portal/docs/microservices/puml/
portal/docs/microservices/svg/
portal/docs/microservices/index.md
portal/docs/applications/*.md
portal/docs/applications/puml/
portal/docs/applications/svg/
portal/docs/applications/index.md
portal/docs/events/index.md
portal/docs/events-ui/
portal/docs/actors/index.md
portal/docs/diagrams/svg/
portal/site/
```

### Phase 6: Remove Generated Artifacts from Git History

After adding `.gitignore` entries, remove the now-ignored files from git tracking:

```bash
git rm --cached portal/docs/services/api/*.html
git rm --cached portal/docs/services/index.md
git rm --cached portal/docs/microservices/*.md
git rm --cached -r portal/docs/microservices/puml/
git rm --cached -r portal/docs/microservices/svg/
git rm --cached portal/docs/microservices/index.md
git rm --cached portal/docs/applications/*.md
git rm --cached -r portal/docs/applications/puml/
git rm --cached -r portal/docs/applications/svg/
git rm --cached portal/docs/applications/index.md
git rm --cached portal/docs/events/index.md
git rm --cached -r portal/docs/events-ui/ 2>/dev/null || true
git rm --cached portal/docs/actors/index.md
git rm --cached -r portal/docs/diagrams/svg/ 2>/dev/null || true
```

---

## Target Architect Workflows

### Workflow A: Change an OpenAPI Spec

```
1. Edit portal/docs/specs/svc-gear-inventory.yaml
2. git commit -m "Add rfid_tag field to gear assignments"
3. git push
4. CI automatically:
   - Regenerates Swagger HTML for svc-gear-inventory
   - Regenerates microservice page + sequence diagrams
   - Rebuilds MkDocs site
   - Deploys to Azure
```

### Workflow B: Change Service Metadata (e.g., Add a Database Table)

```
1. Edit portal/docs/metadata/data-stores.yaml
2. git commit -m "Add audit_log table to svc-gear-inventory"
3. git push
4. CI automatically regenerates affected service page
```

### Workflow C: Add a Cross-Service Integration

```
1. Edit portal/docs/metadata/cross-service-calls.yaml
2. git commit -m "svc-gear-inventory now calls svc-safety-compliance for hazmat check"
3. git push
4. CI automatically regenerates sequence diagrams with new integration arrow
```

### Workflow D: Add or Modify an Event

```
1. Edit portal/docs/metadata/events.yaml
2. Optionally edit portal/docs/events/svc-gear-inventory.events.yaml (AsyncAPI spec)
3. git commit -m "Add gear.assigned event"
4. git push
5. CI automatically regenerates event catalog page + AsyncAPI UI
```

### Workflow E: Change an Application Screen Flow

```
1. Edit portal/docs/metadata/applications.yaml
2. git commit -m "Add gear return screen to web-ops-dashboard"
3. git push
4. CI automatically regenerates application page + user journey diagram
```

### Workflow F: Add a Custom PUML Diagram

```
1. Create portal/docs/diagrams/my-custom-flow.puml
2. git commit -m "Add custom data migration flow diagram"
3. git push
4. CI automatically renders PUML to SVG
```

### Workflow G: Local Preview (Optional)

```
1. Edit any source artifact
2. bash portal/scripts/generate-all.sh  (runs full build locally)
3. cd portal && mkdocs serve             (preview at localhost:8000)
```

---

## Files Changed Summary

| File | Action | Description |
|------|--------|-------------|
| `portal/docs/metadata/domains.yaml` | CREATE | Domain classification extracted from Python |
| `portal/docs/metadata/data-stores.yaml` | CREATE | Database schemas extracted from Python |
| `portal/docs/metadata/cross-service-calls.yaml` | CREATE | Integration map extracted from Python |
| `portal/docs/metadata/events.yaml` | CREATE | Event catalog extracted from Python |
| `portal/docs/metadata/actors.yaml` | CREATE | Actor definitions extracted from Python |
| `portal/docs/metadata/pci.yaml` | CREATE | PCI scope extracted from Python |
| `portal/docs/metadata/applications.yaml` | CREATE | Application definitions extracted from Python |
| `portal/docs/metadata/consumers.yaml` | CREATE | Consumer map extracted from Python |
| `portal/scripts/generate-microservice-pages.py` | MODIFY | Remove inline dicts, add YAML loading |
| `portal/scripts/generate-swagger-pages.py` | MODIFY | Remove inline DOMAINS, add YAML loading |
| `portal/scripts/generate-application-pages.py` | MODIFY | Remove inline APPLICATIONS, add YAML loading |
| `portal/scripts/generate-all.sh` | CREATE | Unified build entry point |
| `.github/workflows/docs-deploy.yml` | MODIFY | Add PlantUML, run generate-all.sh |
| `.gitignore` | MODIFY | Exclude generated artifacts |

---

## Risk Assessment

| Risk | Mitigation |
|------|------------|
| YAML metadata format errors break build | CI runs `--strict` mode; YAML schema validation can be added later |
| PlantUML not available on CI runner | Install via `apt-get install plantuml` in pipeline |
| Existing generated files conflict with gitignore | `git rm --cached` removes from tracking without deleting locally |
| Generator refactoring introduces bugs | Run full build locally before committing; compare output against current artifacts |
| YAML loading slower than Python dicts | Negligible -- metadata files are small (< 100KB total) |
| Merge conflicts during migration | Single commit handles all changes atomically |

---

## Success Criteria

1. An architect can change an OpenAPI spec and have it published by editing ONE file and pushing
2. An architect can change service metadata by editing a YAML file (no Python knowledge required)
3. CI handles all generation -- no manual steps between edit and deploy
4. Generated artifacts are not in git -- clean diffs, no merge conflicts on generated files
5. Local preview works with a single command (`bash portal/scripts/generate-all.sh`)
6. Both AI agents and human architects can use the same workflow
