---
tags:
  - handbook
  - publishing
  - portal
  - ci-cd
---

<!-- PUBLISH -->

<div class="hero" markdown>

# Publishing

<p class="subtitle">How to regenerate portal pages and deploy architecture changes to the live site</p>

</div>

The NovaTrek Architecture Portal is built by CI on every push to `main`. As an architect you rarely need to deploy manually — pushing your changes triggers the full build and deploy pipeline automatically.

This guide explains when to run generators locally (for verification), how the CI pipeline works, and how to deploy manually when needed.

---

## The Normal Workflow

```
Architect edits YAML, OpenAPI, or Excalidraw files
     │
     git push to solution/NTK-XXXXX branch
     │
     ▼
PR opened → validate-solution workflow runs
  ├── YAML lint
  ├── Folder structure check
  ├── Data isolation audit
  └── Portal build (validate only — does not deploy)
     │
     PR merged to main
     │
     ▼
docs-deploy workflow runs
  ├── All generators (Python scripts)
  ├── MkDocs build
  ├── Azure Static Web Apps deploy (primary portal)
  └── Confluence mirror update (optional)
```

The portal at [architecture.novatrek.cc](https://architecture.novatrek.cc) updates within minutes of merging.

---

## Running Generators Locally

Always run generators locally before pushing to verify your changes render correctly. Do not rely on CI to catch rendering errors.

### Full regeneration (recommended)

```bash
# From repo root
bash portal/scripts/generate-all.sh
```

This runs all 11 generator steps in sequence:
1. Swagger UI pages from OpenAPI specs
2. Microservice pages (MD + PUML + SVG)
3. Application pages
4. Wireframe pages from Excalidraw JSON
5. AsyncAPI event pages
6. Solution design pages
7. Business capability pages
8. Ticket pages
9. CALM topology
10. Standalone PlantUML diagrams
11. MkDocs site build

Output is in `portal/site/`. Total run time: 3-8 minutes depending on the number of PlantUML diagrams to render.

### Targeted regeneration (faster)

When only specific files have changed, run individual generators:

| Change | Generator to run |
|---|---|
| OpenAPI spec (`architecture/specs/`) | `python3 portal/scripts/generate-swagger-pages.py` then `python3 portal/scripts/generate-microservice-pages.py` |
| Data stores or cross-service calls | `python3 portal/scripts/generate-microservice-pages.py` |
| Events | `python3 portal/scripts/generate-event-pages.py` |
| Solution design | `python3 portal/scripts/generate-solution-pages.py` |
| Capabilities or changelog | `python3 portal/scripts/generate-capability-pages.py` |
| Tickets | `python3 portal/scripts/generate-ticket-pages.py` |
| Wireframes | `python3 portal/scripts/generate-wireframe-pages.py` |
| Topology / domains | `python3 portal/scripts/generate-topology-pages.py` |

After running targeted generators, build MkDocs to catch any cross-reference errors:

```bash
cd portal
python3 -m mkdocs build
```

---

## Reviewing the Built Site Locally

After running `generate-all.sh`, the built site is in `portal/site/`. You can serve it locally to review:

```bash
cd portal
python3 -m mkdocs serve
```

Then open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

!!! note "SVGs and assets"
    When using `mkdocs serve`, SVG diagrams and Swagger UI pages may not load because the asset copy steps only run during `mkdocs build`. Run `bash portal/scripts/generate-all.sh` and inspect `portal/site/` for a complete preview.

---

## CI Pipeline Details

### Validation pipeline (PRs)

Workflow: `.github/workflows/validate-solution.yml`

Triggered on every PR touching `architecture/`, `portal/docs/`, or `decisions/` paths.

Steps:
1. YAML lint on all metadata files
2. Solution folder structure check
3. Data isolation audit (`portal/scripts/utilities/audit-data-isolation.sh`)
4. Portal build (same as production — verifies generators run without error)

A failing validation pipeline blocks merge.

### Deployment pipeline (push to main)

Workflow: `.github/workflows/docs-deploy.yml`

Triggered on every push to `main` that touches documentation or architecture paths.

Steps:
1. All portal generators
2. `mkdocs build`
3. Asset copies (SVG, Swagger HTML, staticwebapp.config.json)
4. `swa deploy` to Azure Static Web Apps (production)
5. Confluence staging + publish (if `CONFLUENCE_BASE_URL` secret is set)
6. Confluence page locking

---

## Adding a New Page to Navigation

When adding a new static Markdown page to the portal, add it to `portal/mkdocs.yml` under the appropriate section:

```yaml
nav:
  - Architect Handbook:
    - handbook/index.md
    - Working a Ticket: handbook/working-a-ticket.md
    # ... existing entries ...
    - My New Guide: handbook/my-new-guide.md    # ← add here
```

MkDocs will warn if a page exists but is not in the nav, or if a nav entry points to a missing file. Both are caught by the validation pipeline.

---

## Manual Deployment

Manual deployment is rarely needed — use it only when CI is unavailable or you need to deploy a hotfix urgently.

### Prerequisites

- Azure CLI installed and logged in
- Azure Static Web Apps CLI installed: `npm install -g @azure/static-web-apps-cli`
- Deployment token (from Azure portal or repository secrets)

### Deployment commands

```bash
# From repo root — build the full site
bash portal/scripts/generate-all.sh

# Deploy to production
cd portal
swa deploy site \
  --deployment-token "<token>" \
  --env production
```

### Deployment targets

| Site | URL |
|---|---|
| Primary portal | [architecture.novatrek.cc](https://architecture.novatrek.cc) |
| Docs site (secondary) | [victorious-mud-06704740f.4.azurestaticapps.net](https://victorious-mud-06704740f.4.azurestaticapps.net) |

---

## Confluence Mirror

On every push to `main`, the portal is mirrored to Confluence Cloud (read-only). The Confluence pages are automatically locked after publishing to prevent manual edits.

If a Confluence page appears out of date, check the `docs-deploy` workflow run for that push — Confluence publishing is the last step and may have failed independently.

To check Confluence drift manually:

```bash
export CONFLUENCE_BASE_URL="https://novatrek.atlassian.net/wiki"
export CONFLUENCE_USERNAME="..."
export CONFLUENCE_API_TOKEN="..."
export CONFLUENCE_SPACE="ARCH"

python3 portal/scripts/confluence-drift-check.py --staging-dir portal/confluence
```

---

## Common Issues

**Generator fails with `KeyError`**

A YAML metadata file references a service or capability that does not exist. Check the error message for the missing key, then verify the referenced value exists in the source file.

**MkDocs warns about missing page**

A nav entry in `mkdocs.yml` points to a file that has not been generated yet. Run the appropriate generator first, then retry `mkdocs build`.

**SVGs not rendering in portal**

The portal uses `<object>` tags for SVGs to support clickable links. If SVGs appear blank, check that `staticwebapp.config.json` has `X-Frame-Options: SAMEORIGIN` (not `DENY`). `DENY` blocks `<object>` rendering entirely.

**Confluence pages showing stale content**

The Confluence mirror updates on every push to `main`. Check the `publish-confluence` job in the `docs-deploy` workflow run. If the job succeeded but pages look stale, check whether Confluence caching is the cause — refresh the page or clear the browser cache.

---

!!! tip "Related guides"
    - [Platform Operations](../platform-operations.md) — full CI/CD pipeline reference
    - [Metadata Registry](../standards/metadata-registry/index.md) — YAML files that drive generation
    - [Database Change Workflow](../database-change-workflow.md) — how database changes reach production
