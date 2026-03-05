# Architecture Artifact File Structure

An inventory and analysis of every architecture artifact in this workspace — where it lives, what generates it, and whether the layout is ideal.

## Current File Structure

```
continuous-architecture-platform-poc-2/
│
├── decisions/                              # ADR source of truth
│   ├── ADR-001-ai-toolchain-selection.md       # 11 Architecture Decision Records
│   ├── ADR-002-documentation-publishing-platform.md
│   ├── ...ADR-003 through ADR-011...
│   └── README.md
│
├── (services/ removed — legacy content archived to phase-1/.../baseline-pages/)
│
├── docs/                                   # GitHub Pages root (minimal — redirects to portal)
│   └── index.md
│
├── research/                               # Deep research prompts and results
│   ├── DEEP-RESEARCH-*.md
│   └── CONTEXT-WINDOW-UTILIZATION-ANALYSIS.md
│
├── portal/                                 # MkDocs Material portal — PRIMARY PUBLISHING TARGET
│   ├── mkdocs.yml
│   ├── staticwebapp.config.json
│   │
│   ├── scripts/                                # GENERATORS (Python)
│   │   ├── generate-microservice-pages.py          # Generates 19 service pages + 160 PUMLs + event catalog
│   │   ├── generate-swagger-pages.py               # Generates 19 Swagger UI HTML pages
│   │   ├── generate-event-pages.py                 # Generates 6 AsyncAPI UI HTML pages
│   │   ├── generate-application-pages.py           # Generates 3 application pages + 25 PUMLs
│   │   └── generate-svgs.sh                        # Shell wrapper for PlantUML rendering
│   │
│   ├── docs/                                   # MkDocs source directory
│   │   ├── index.md                                # Portal home page
│   │   ├── tags.md                                 # Tags index
│   │   │
│   │   ├── specs/                                  # OpenAPI YAML specs (19 files)
│   │   │   ├── svc-check-in.yaml                       # Source of truth for API contracts
│   │   │   ├── svc-reservations.yaml
│   │   │   └── ...(19 total)
│   │   │
│   │   ├── events/                                 # AsyncAPI YAML specs + generated index
│   │   │   ├── index.md                                # GENERATED — Event Catalog page
│   │   │   ├── svc-check-in.events.yaml                # Source of truth for event schemas
│   │   │   ├── svc-reservations.events.yaml
│   │   │   └── ...(6 producers, 7 events)
│   │   │
│   │   ├── events-ui/                              # GENERATED — AsyncAPI interactive HTML pages
│   │   │   ├── svc-check-in.html
│   │   │   └── ...(6 total)
│   │   │
│   │   ├── microservices/                          # GENERATED — service deep-dive pages
│   │   │   ├── index.md                                # Microservice index page
│   │   │   ├── svc-check-in.md                         # 19 generated Markdown pages
│   │   │   ├── svc-reservations.md
│   │   │   ├── ...
│   │   │   ├── puml/                                   # GENERATED — 160 PlantUML source files
│   │   │   │   ├── svc-check-in--post-check-ins.puml       # 139 endpoint sequence diagrams
│   │   │   │   ├── svc-check-in--c4-context.puml           # 19 C4 context diagrams
│   │   │   │   ├── enterprise-c4-context.puml              # 1 enterprise rollup diagram
│   │   │   │   └── event-flow.puml                         # 1 event flow diagram
│   │   │   └── svg/                                    # GENERATED — 160 rendered SVG files
│   │   │       ├── svc-check-in--post-check-ins.svg
│   │   │       ├── enterprise-c4-context.svg
│   │   │       └── ...(160 total)
│   │   │
│   │   ├── services/                               # Service catalog landing + Swagger UI
│   │   │   ├── index.md                                # GENERATED — service catalog page
│   │   │   └── api/                                    # GENERATED — Swagger UI HTML pages
│   │   │       ├── svc-check-in.html                       # 19 interactive API reference pages
│   │   │       └── ...(19 total)
│   │   │
│   │   ├── applications/                           # Application pages + diagrams
│   │   │   ├── index.md                                # GENERATED — application index
│   │   │   ├── web-guest-portal.md                     # 3 application pages
│   │   │   ├── web-ops-dashboard.md
│   │   │   ├── app-guest-mobile.md
│   │   │   ├── puml/                                   # GENERATED — 25 PlantUML source files
│   │   │   └── svg/                                    # GENERATED — 25 rendered SVGs
│   │   │
│   │   ├── standards/                              # Architecture standards reference
│   │   │   ├── index.md
│   │   │   ├── arc42/         (14 files)               # arc42 template sections
│   │   │   ├── c4-model/      (4 files)                # C4 model guides
│   │   │   ├── madr/          (5 files)                # MADR templates and examples
│   │   │   ├── adr-templates/ (4 files)                # Additional ADR templates
│   │   │   └── quality-model/ (2 files)                # ISO 25010 quality tree
│   │   │
│   │   ├── javascripts/                            # Custom JS
│   │   │   └── site-name-link.js
│   │   └── stylesheets/                            # Custom CSS
│   │       └── extra.css
│   │
│   ├── drafts/                                 # Unpublished planning docs
│   │   ├── PLAN-frontend-applications.md
│   │   └── api-gateway-architecture-modernization.md
│   │
│   └── site/                                   # BUILD OUTPUT (deployed to Azure)
│       └── ...(not checked in)
│
├── phase-1-ai-tool-cost-comparison/
│   └── workspace/
│       └── corporate-services/
│           ├── services/                           # Symlinks to portal/docs/specs/ (single source of truth)
│           │   ├── svc-check-in.yaml -> ../../../../portal/docs/specs/svc-check-in.yaml
│           │   └── ...(19 symlinks)
│           ├── baseline-pages/                     # ARCHIVED legacy service pages (pre-portal)
│           │   ├── svc-check-in.md                     # 6 original hand-written pages
│           │   └── README.md
│           └── diagrams/                           # ORIGINAL hand-crafted diagrams (pre-generator)
│               ├── include.puml                        # Shared PlantUML includes
│               ├── templates.puml                      # Template definitions
│               ├── Components/                         # 4 component diagrams (PUML + SVG)
│               ├── Sequence/                           # 4 sequence diagrams (PUML + SVG)
│               └── System/                             # 1 system context diagram (PUML + SVG)
│
└── presentation/                               # Separate MkDocs site (12-slide presentation)
    └── ...(self-contained, not relevant to artifact layout)
```

## Artifact Inventory Summary

| Artifact Type | Count | Location | Source/Generated | Format |
|---------------|-------|----------|-----------------|--------|
| ADRs | 11 | `decisions/` | Hand-written | Markdown |
| OpenAPI specs | 19 | `portal/docs/specs/` | Hand-written | YAML |
| OpenAPI specs (symlinks) | 19 | `phase-1/.../services/` | Symlink to portal/docs/specs/ | YAML |
| AsyncAPI specs | 6 | `portal/docs/events/` | Hand-written | YAML |
| Sequence diagrams (PUML) | 139 | `portal/docs/microservices/puml/` | Generated | PlantUML |
| Sequence diagrams (SVG) | 139 | `portal/docs/microservices/svg/` | Generated | SVG |
| C4 context diagrams (PUML) | 19 | `portal/docs/microservices/puml/` | Generated | PlantUML |
| C4 context diagrams (SVG) | 19 | `portal/docs/microservices/svg/` | Generated | SVG |
| Enterprise C4 diagram | 1 | `portal/docs/microservices/puml/` | Generated | PlantUML/SVG |
| Event flow diagram | 1 | `portal/docs/microservices/puml/` | Generated | PlantUML/SVG |
| Application screen diagrams (PUML) | 25 | `portal/docs/applications/puml/` | Generated | PlantUML |
| Application screen diagrams (SVG) | 25 | `portal/docs/applications/svg/` | Generated | SVG |
| Microservice pages | 19 | `portal/docs/microservices/` | Generated | Markdown |
| Event Catalog page | 1 | `portal/docs/events/index.md` | Generated | Markdown |
| Service Catalog page | 1 | `portal/docs/services/index.md` | Generated | Markdown |
| Application pages | 3+1 | `portal/docs/applications/` | Generated | Markdown |
| Swagger UI pages | 19 | `portal/docs/services/api/` | Generated | HTML |
| AsyncAPI UI pages | 6 | `portal/docs/events-ui/` | Generated | HTML |
| Standards reference | 29 | `portal/docs/standards/` | Hand-written | Markdown |
| Legacy service pages | 6 | `phase-1/.../baseline-pages/` | Archived | Markdown |
| Hand-crafted diagrams | 9+2 | `phase-1/.../diagrams/` | Hand-written | PlantUML/SVG |
| **TOTAL** | **~480** | | | |

## Analysis: Is This Layout Ideal?

### VERDICT: RESOLVED — all issues fixed (2026-03-05)

The portal layout itself (`portal/docs/`) is **well-organized**. Generated content is cleanly separated by artifact type, specs are adjacent to what consumes them, and the generator scripts share a consistent pattern. However, there are problems with **artifact duplication**, **orphaned legacy content**, and **generated output mixing with source**.

---

### ISSUE 1: OpenAPI Specs Are Duplicated — RESOLVED

**Resolution:** Phase-1 specs replaced with symlinks to `portal/docs/specs/`. Single source of truth established.

~~**Problem:** The 19 OpenAPI YAML specs exist in two places:~~

- `portal/docs/specs/` (used by generators, served on portal)
- `phase-1-ai-tool-cost-comparison/workspace/corporate-services/services/` (original location)

Both copies are byte-for-byte identical. This creates a maintenance risk — if someone edits the Phase 1 copy or the portal copy independently, they silently diverge.

**Severity:** Medium. No divergence today, but it will happen eventually.

**Root cause:** The specs were originally authored in the Phase 1 workspace for AI tool evaluation. When the portal was built, they were copied to `portal/docs/specs/` so generators could find them and the portal could serve them for download. Neither location was deprecated.

### ISSUE 2: Legacy `services/` Directory is Stale and Redundant — RESOLVED

**Resolution:** Legacy pages archived to `phase-1/.../baseline-pages/`. Orphaned SVGs reunited with PUML sources. Root `services/` directory removed. Copilot instructions updated.

~~**Problem:** The root `services/` directory contains:~~

- 6 hand-written service pages (svc-check-in.md, etc.) — **superseded** by the 19 generated microservice pages in `portal/docs/microservices/`
- 5 SVG files in `services/diagrams/` with **no corresponding PUML source** — orphaned rendered output
- The SVGs in `services/diagrams/` are the same diagrams whose PUML sources exist in `phase-1/.../diagrams/Sequence/` — they were copied here at some point without their sources

**Severity:** Medium. New contributors will be confused about which pages are canonical. The `.github/copilot-instructions.md` still references `services/` as the "Service architecture baseline pages" — misleading.

### ISSUE 3: Generated Output is Checked Into Source

**Problem:** All generated files live in the same repo alongside their sources:

- 160 PUMLs + 160 SVGs in `portal/docs/microservices/puml/` and `svg/`
- 25 PUMLs + 25 SVGs in `portal/docs/applications/puml/` and `svg/`
- 19 Swagger UI HTML pages in `portal/docs/services/api/`
- 6 AsyncAPI UI HTML pages in `portal/docs/events-ui/`
- Generated Markdown pages in `portal/docs/microservices/`, `portal/docs/events/index.md`

This is **370+ generated files** tracked in git alongside ~50 hand-authored source files.

**Severity:** Low for a POC. In a production repo, this would cause noisy diffs, merge conflicts on generated files, and unclear ownership. However, since we don't have CI/CD generating on deploy yet, checking them in is the pragmatic choice.

**Recommendation:** Acceptable for now. When a CI pipeline is added, generated files should be `.gitignore`d and produced during the build step. No action needed today.

### ISSUE 4: The Event Flow Diagram Lives in `microservices/puml/` Instead of `events/`

**Problem:** The `event-flow.puml` and `event-flow.svg` are generated into `portal/docs/microservices/puml/` and `portal/docs/microservices/svg/` because the microservice generator creates them. But they're an event catalog artifact, not a microservice artifact. The event catalog page references them via `../microservices/svg/event-flow.svg` — a cross-directory reference that breaks the locality principle.

**Severity:** Low. Works fine, just semantically misplaced.

---

## Remediation Plan

Only Issues 1 and 2 need action. Issue 3 is acceptable for a POC. Issue 4 is cosmetic.

### Plan: Fix Issue 1 — Eliminate OpenAPI Spec Duplication

**Approach:** Make `portal/docs/specs/` the single source of truth. Update the Phase 1 workspace to **symlink or reference** the portal specs instead of maintaining a copy.

**Steps:**
1. Delete `phase-1-ai-tool-cost-comparison/workspace/corporate-services/services/*.yaml`
2. Replace with symlinks: `ln -s ../../../../portal/docs/specs/*.yaml .`
3. Verify the Phase 1 mock tools still work with symlinked specs (the mock scripts already reference them by path)

**Impact on publishing:** None. The portal generators already read from `portal/docs/specs/`. The Swagger page generator reads from `phase-1/.../services/` but only to copy them *to* `portal/docs/specs/` — this step becomes a no-op since the files are already there.

**Risk:** Low. Git handles symlinks on macOS/Linux. If Windows compatibility is needed, a copy script with a single-source marker would work instead.

### Plan: Fix Issue 2 — Archive Legacy `services/` Directory

**Approach:** Move the legacy content under `phase-1/` where it belongs (it was part of the Phase 1 evaluation baseline) and update the copilot-instructions reference.

**Steps:**
1. Move `services/*.md` to `phase-1-ai-tool-cost-comparison/workspace/corporate-services/baseline-pages/`
2. Move `services/diagrams/*.svg` to `phase-1-ai-tool-cost-comparison/workspace/corporate-services/diagrams/Sequence/` (reuniting them with their PUML sources)
3. Remove `services/README.md` or replace with a redirect note pointing to `portal/docs/microservices/`
4. Update `.github/copilot-instructions.md` Key Locations table: change `services/` description from "Service architecture baseline pages" to point to `portal/docs/microservices/`

**Impact on publishing:** None. The portal does not reference anything in root `services/`. The root `docs/` GitHub Pages site does not link to `services/` either.

**Risk:** Very low. These files are not consumed by any generator or build process.

### No Action: Issue 3 — Generated Files in Git

Acceptable for a POC. When CI is added, add to `.gitignore`:
```
portal/docs/microservices/puml/
portal/docs/microservices/svg/
portal/docs/microservices/*.md
portal/docs/applications/puml/
portal/docs/applications/svg/
portal/docs/services/api/
portal/docs/events-ui/
portal/docs/events/index.md
```

### No Action: Issue 4 — Event Flow Diagram Location

Leave as-is. Moving it would require changing the PlantUML render pipeline to output to a different SVG directory, and the cross-directory reference works correctly.
