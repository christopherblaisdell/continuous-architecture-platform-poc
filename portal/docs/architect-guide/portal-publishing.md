# Portal Publishing

This page covers how the NovaTrek Architecture Portal is built, previewed, and deployed.

---

## Architecture

The portal is a [MkDocs Material](https://squidfun.github.io/mkdocs-material/) site deployed to Azure Static Web Apps. Content flows through three stages:

```
Hand-authored YAML + Markdown
  -> Generator scripts (Python)
    -> MkDocs build (HTML/CSS/JS)
      -> Azure Static Web Apps (deployment)
```

---

## The Build Pipeline

All generation runs through a single entry point:

```bash
bash portal/scripts/generate-all.sh
```

This executes 11 stages in order:

| Stage | Generator | Output |
|-------|-----------|--------|
| 1 | `generate-swagger-pages.py` | Swagger UI HTML pages (23 services) |
| 2 | `generate-microservice-pages.py` | Service pages + PlantUML + SVG (139 diagrams) |
| 3 | `generate-application-pages.py` | App pages + user journey SVGs |
| 4 | `generate-wireframe-pages.py` | Wireframe SVG + HTML + Markdown |
| 5 | `generate-event-pages.py` | AsyncAPI event catalog |
| 6 | `generate-solution-pages.py` | Solution index + detail pages |
| 7 | `generate-capability-pages.py` | Capability hierarchy + timeline |
| 8 | `generate-ticket-pages.py` | Ticket index + detail pages |
| 9 | `generate-topology-pages.py` + CALM | System map, dependency matrix, domain views |
| 10 | `generate-svgs.sh` | Hand-authored PlantUML diagram SVGs |
| 11 | `mkdocs build` + asset copy | Complete HTML site in `portal/site/` |

### Why Asset Copy?

MkDocs does not copy non-Markdown assets automatically. Stage 11 copies these into the `site/` output:

```bash
cp -r docs/services/api site/services/       # Swagger UI pages
cp -r docs/specs site/                        # OpenAPI YAML files
cp -r docs/microservices/svg site/microservices/  # SVG diagram files
cp staticwebapp.config.json site/             # Azure routing config
```

---

## Local Preview

### Full rebuild and preview

```bash
# Generate all pages and diagrams
bash portal/scripts/generate-all.sh

# Start local dev server
cd portal && python3 -m mkdocs serve
```

Open `http://localhost:8000`. The dev server auto-reloads when you edit Markdown files.

### Quick preview (skip generation)

If you only changed hand-authored Markdown (not metadata YAML), skip the generators:

```bash
cd portal && python3 -m mkdocs serve
```

### Strict build (catch errors)

```bash
cd portal && python3 -m mkdocs build --strict
```

The `--strict` flag treats warnings as errors — catches broken links, missing references, and nav mismatches.

---

## Deployment

### Automated (CI/CD)

On every push to `main`, the GitHub Action `.github/workflows/docs-deploy.yml`:

1. Runs `generate-all.sh`
2. Builds the MkDocs site
3. Copies non-Markdown assets
4. Deploys to Azure Static Web Apps

### Manual deployment

```bash
cd portal
python3 -m mkdocs build
cp -r docs/services/api site/services/
cp -r docs/specs site/
cp -r docs/microservices/svg site/microservices/
cp staticwebapp.config.json site/
npx swa deploy site --deployment-token "<token>" --env production
```

### Deployment Targets

| Site | URL | Purpose |
|------|-----|---------|
| Portal (primary) | `https://architecture.novatrek.cc` | Main architecture portal |
| AI Customization | `https://ai.customization.novatrek.cc` | Copilot vs OpenSpec comparison |
| Docs | `https://victorious-mud-06704740f.4.azurestaticapps.net` | Documentation site |

---

## MkDocs Configuration

The portal configuration lives in `mkdocs.yml` at the workspace root. Key settings:

### Navigation

The `nav:` section defines the left sidebar and top tabs. When adding new pages, update the nav to include them.

### Theme Features

```yaml
features:
  - navigation.tabs          # Top-level tabs
  - navigation.tabs.sticky   # Tabs stay visible on scroll
  - navigation.sections      # Expandable sidebar sections
  - navigation.expand        # Sections start expanded
  - navigation.indexes       # Section index pages
  - navigation.top           # Back-to-top button
  - search.suggest           # Search suggestions
  - content.code.copy        # Copy button on code blocks
```

### Plugins

- **search** — full-text search
- **tags** — content tagging
- **exclude** — exclude paths from build
- **git-revision-date-localized** — show last-updated dates
- **git-committers** — show page contributors
- **minify** — HTML minification

---

## Azure Static Web App Configuration

The `staticwebapp.config.json` controls routing, headers, and CSP for the deployed site.

!!! warning "Critical Setting"
    `X-Frame-Options` MUST be `SAMEORIGIN`, not `DENY`. `DENY` blocks browsers from rendering content inside `<object>` tags, causing all SVG diagrams to silently disappear.

---

## Confluence Mirror

The portal is mirrored to Confluence as a read-only copy. See [Platform Operations](../platform-operations.md) for details.

### Key Scripts

| Script | Purpose |
|--------|---------|
| `portal/scripts/confluence-prepare.py` | Transforms MkDocs Markdown to Confluence format |
| `portal/scripts/confluence-lock-pages.py` | Locks auto-generated pages |
| `portal/scripts/confluence-drift-check.py` | Detects unauthorized Confluence edits |

---

## Multi-Site Content Sync

Some documentation is published to multiple sites. A manifest-driven sync system handles this.

| File | Purpose |
|------|---------|
| `sites/manifest.yaml` | Declares which docs go to which sites |
| `sites/sync-sites.py` | Copies with per-site link rewrites |

**Workflow:**

1. Edit in `docs/` (single source of truth)
2. Run `python3 sites/sync-sites.py` to distribute
3. Build and deploy each affected site
4. Commit source + synced copies together

**Drift check:** `python3 sites/sync-sites.py --check` (exits 1 if out of sync)

---

## Troubleshooting

### SVG diagrams not appearing

- Check that `X-Frame-Options` in `staticwebapp.config.json` is `SAMEORIGIN`, not `DENY`
- Verify SVG files were copied to `site/microservices/svg/` (Stage 11)
- Check relative paths — pages at `/microservices/svc-check-in/` need `../svg/` not `svg/`

### Broken links after build

- Run `python3 -m mkdocs build --strict` to identify which links are broken
- Check that new pages are listed in the `nav:` section of `mkdocs.yml`
- Verify file names match nav references exactly (case-sensitive)

### Generated pages show stale data

- Re-run `bash portal/scripts/generate-all.sh` — generators always read from current metadata
- Check that you saved changes to the source YAML files before running generators

### Local preview differs from deployed site

- Ensure you ran the asset copy commands after `mkdocs build`
- Check that `staticwebapp.config.json` is in the `site/` directory
