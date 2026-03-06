# Root Folder Reorganization Plan

**Date**: 2026-03-06
**Status**: Proposed
**Goal**: Reduce root folder clutter by consolidating related content into intuitive subfolders without breaking any existing functionality.

---

## Problem Statement

The repository root currently contains **20+ visible items** (excluding dotfiles), making it difficult to quickly understand the project structure. Files and folders are organized by the order they were created rather than by logical grouping. Several root-level items serve similar purposes (plans, research, documentation, configuration) but sit side-by-side with no hierarchy.

### Current Root Layout (20 items)

```
ROOT/
├── AI-TOOL-COST-COMPARISON-PLAN.md      # Plan doc (orphaned duplicate)
├── CLOSING-THE-LOOP.md                  # Narrative doc
├── LICENSE
├── README.md
├── architecture/                        # Architect source of truth (specs, metadata, events)
├── decisions/                           # 11 ADRs
├── docs/                               # Root MkDocs source (secondary site)
├── infra/                               # Azure Bicep IaC
├── mkdocs.yml                           # Root MkDocs config (secondary site)
├── phase-1-ai-tool-cost-comparison/     # Phase 1 evaluation
├── phase-2-ai-workflow/                 # Empty (.gitkeep only)
├── phase-3-vsflow-pipelines/            # Empty (.gitkeep only)
├── phase-4-artifact-graph/              # Empty (.gitkeep only)
├── phase-5-continuous-improvement/       # Empty (.gitkeep only)
├── phase-6-documentation-publishing/    # Phase 6 plan
├── portal/                              # Primary MkDocs site + generators
├── presentation/                        # Executive presentation MkDocs site
├── presentation-internal-full.pptx      # PowerPoint (loose in root)
├── presentation-internal.pptx           # PowerPoint (loose in root)
├── requirements-docs.txt                # Python deps (loose in root)
├── research/                            # Deep research docs
├── roadmap/                             # Single file folder
├── scripts/                             # Utility scripts
├── site/                                # Root MkDocs build output
├── staticwebapp.config.json             # Root site Azure config
```

---

## Proposed Structure (8 root items)

```
ROOT/
├── LICENSE
├── README.md
├── .github/                             # (unchanged, hidden)
├── architecture/                        # ARCHITECT WORKSPACE — unchanged, prominent
├── decisions/                           # ADRs — unchanged, prominent
├── docs/                                # Root MkDocs source — unchanged
├── infra/                               # Azure IaC — unchanged
├── phases/                              # NEW — all 6 phases consolidated
│   ├── phase-1-ai-tool-cost-comparison/
│   ├── phase-2-ai-workflow/
│   ├── phase-3-vsflow-pipelines/
│   ├── phase-4-artifact-graph/
│   ├── phase-5-continuous-improvement/
│   └── phase-6-documentation-publishing/
├── portal/                              # Primary site + generators — unchanged
├── presentation/                        # Presentation site — absorbs .pptx files
│   ├── docs/
│   ├── mkdocs.yml
│   ├── scripts/
│   ├── site/
│   ├── presentation-internal-full.pptx  # MOVED from root
│   └── presentation-internal.pptx       # MOVED from root
├── research/                            # Deep research — unchanged
├── mkdocs.yml                           # Root MkDocs config — stays (needed at root)
├── requirements-docs.txt                # Python deps — stays (CI references it)
└── staticwebapp.config.json             # Root site config — stays (if root site is kept)
```

### What Changes

| Item | Action | Rationale |
|------|--------|-----------|
| `phase-1-ai-tool-cost-comparison/` | Move to `phases/phase-1-ai-tool-cost-comparison/` | Group all 6 phases together |
| `phase-2-ai-workflow/` | Move to `phases/phase-2-ai-workflow/` | Group all 6 phases together |
| `phase-3-vsflow-pipelines/` | Move to `phases/phase-3-vsflow-pipelines/` | Group all 6 phases together |
| `phase-4-artifact-graph/` | Move to `phases/phase-4-artifact-graph/` | Group all 6 phases together |
| `phase-5-continuous-improvement/` | Move to `phases/phase-5-continuous-improvement/` | Group all 6 phases together |
| `phase-6-documentation-publishing/` | Move to `phases/phase-6-documentation-publishing/` | Group all 6 phases together |
| `presentation-internal-full.pptx` | Move to `presentation/` | Keep presentation assets together |
| `presentation-internal.pptx` | Move to `presentation/` | Keep presentation assets together |
| `AI-TOOL-COST-COMPARISON-PLAN.md` | Move to `phases/phase-1-ai-tool-cost-comparison/` | Duplicate/companion of the one already there |
| `CLOSING-THE-LOOP.md` | Move to `docs/` | It is source content for the root MkDocs site |
| `roadmap/` | Move to `docs/roadmap/` | Already referenced by root mkdocs.yml from docs/ context |
| `scripts/` | Move to `portal/scripts/utilities/` | Utility scripts related to the portal/build workflow |
| `site/` | Already in .gitignore | Build output, stays but confirm .gitignore |

### What Stays in Root

| Item | Reason |
|------|--------|
| `README.md` | Standard repo entry point |
| `LICENSE` | Standard repo requirement |
| `mkdocs.yml` | MkDocs requires config at project root (or docs_dir must be absolute) |
| `requirements-docs.txt` | CI workflow references it by path |
| `staticwebapp.config.json` | Root site Azure SWA config (paired with root mkdocs.yml) |
| `architecture/` | Architect source of truth — must stay prominent |
| `decisions/` | ADR log — must stay prominent for architects |
| `docs/` | Root MkDocs source directory |
| `infra/` | Infrastructure as code — common root convention |
| `portal/` | Primary documentation portal |
| `presentation/` | Presentation site |
| `research/` | Deep research documents |
| `phases/` | All phased work consolidated |

**Result**: Root goes from **20+ visible items** to **14 visible items** (7 folders, 4 config files, README, LICENSE, and the hidden .github).

---

## Detailed Execution Plan

### Step 1: Consolidate Phase Folders

```bash
mkdir -p phases
git mv phase-1-ai-tool-cost-comparison phases/
git mv phase-2-ai-workflow phases/
git mv phase-3-vsflow-pipelines phases/
git mv phase-4-artifact-graph phases/
git mv phase-5-continuous-improvement phases/
git mv phase-6-documentation-publishing phases/
```

**Files that reference phase paths and need updating:**

| File | Reference | Update |
|------|-----------|--------|
| `.github/workflows/docs-deploy.yml` | `phase-*/**` trigger path | Change to `phases/phase-*/**` |
| `mkdocs.yml` (root) | Nav entries like `phase-1-ai-tool-cost-comparison/...` | Prefix with `phases/` |
| `portal/scripts/generate-svgs.sh` | `$ROOT/phase-1-ai-tool-cost-comparison/workspace/...` | Change to `$ROOT/phases/phase-1-ai-tool-cost-comparison/workspace/...` |
| `.github/copilot-instructions.md` | Multiple references to `phase-1-ai-tool-cost-comparison/` | Prefix with `phases/` |
| `docs/` pages | Symlinks or includes from phase-1 | Update paths |

### Step 2: Move PowerPoint Files into Presentation Folder

```bash
git mv presentation-internal-full.pptx presentation/
git mv presentation-internal.pptx presentation/
```

**No cross-references** — these are standalone binary files.

The `~$presentation-internal.pptx` temp file (PowerPoint lock file) should be added to `.gitignore` and removed if tracked.

### Step 3: Move AI-TOOL-COST-COMPARISON-PLAN.md

```bash
git mv AI-TOOL-COST-COMPARISON-PLAN.md phases/phase-1-ai-tool-cost-comparison/
```

**Note**: `phases/phase-1-ai-tool-cost-comparison/AI-TOOL-COST-COMPARISON-PLAN.md` already exists. Check if root copy is identical or a different version.

**Files that reference this:**

| File | Reference | Update |
|------|-----------|--------|
| `mkdocs.yml` (root) | `phase-1-ai-tool-cost-comparison/AI-TOOL-COST-COMPARISON-PLAN.md` | Will be handled by nav path update in Step 1 |

### Step 4: Move CLOSING-THE-LOOP.md into docs/

```bash
git mv CLOSING-THE-LOOP.md docs/
```

**Files that reference this:**

| File | Reference | Update |
|------|-----------|--------|
| `mkdocs.yml` (root) | Nav entry `CLOSING-THE-LOOP.md` | No change needed — MkDocs resolves relative to docs_dir which is `docs/` at root level, and the root mkdocs.yml already uses this path meaning it was already expecting it inside `docs/` |
| `.github/workflows/docs-deploy.yml` | Trigger path `CLOSING-THE-LOOP.md` | Change to `docs/CLOSING-THE-LOOP.md` |
| `.github/copilot-instructions.md` | References in key locations table | Update path |

**Wait** — the root mkdocs.yml nav entry is just `CLOSING-THE-LOOP.md`. Since MkDocs resolves nav paths relative to the `docs_dir` (which defaults to `docs/`), and `CLOSING-THE-LOOP.md` already exists inside `docs/`, there are actually **two copies**: one at root and one in `docs/`. We need to check which is the source of truth and keep only one.

### Step 5: Move roadmap/ into docs/

```bash
git mv roadmap docs/
```

**Files that reference this:**

| File | Reference | Update |
|------|-----------|--------|
| `mkdocs.yml` (root) | Nav entry `roadmap/ROADMAP.md` | No change — MkDocs already resolves relative to docs/, so `docs/roadmap/ROADMAP.md` is correct |
| `.github/workflows/docs-deploy.yml` | Trigger path `roadmap/**` | Change to `docs/roadmap/**` |
| `.github/copilot-instructions.md` | `roadmap/ROADMAP.md` reference | Update path |

**Check**: Verify `docs/roadmap/` does not already exist before moving.

### Step 6: Move scripts/ into portal/

The root `scripts/` folder contains utility scripts (`audit-data-isolation.sh`, `cost-measurement.py`, `openrouter-cost.py`, `check-app-links.py`, `snapshots/`). These are build/analysis utilities closely related to the portal workflow.

```bash
# Move utility scripts as a subfolder within portal/scripts/
mkdir -p portal/scripts/utilities
git mv scripts/audit-data-isolation.sh portal/scripts/utilities/
git mv scripts/cost-measurement.py portal/scripts/utilities/
git mv scripts/openrouter-cost.py portal/scripts/utilities/
git mv scripts/check-app-links.py portal/scripts/utilities/
git mv scripts/snapshots portal/scripts/utilities/
rmdir scripts  # Remove empty directory
```

**Files that reference this:**

| File | Reference | Update |
|------|-----------|--------|
| `.github/copilot-instructions.md` | `scripts/audit-data-isolation.sh`, `scripts/openrouter-cost.py`, `scripts/cost-measurement.py` | Update to `portal/scripts/utilities/` |
| `phases/phase-1-ai-tool-cost-comparison/COST-MEASUREMENT-METHODOLOGY.md` | May reference `scripts/` paths | Update if present |

### Step 7: Handle Duplicate CLOSING-THE-LOOP.md

Check if `CLOSING-THE-LOOP.md` (root) and `docs/CLOSING-THE-LOOP.md` are identical:

```bash
diff CLOSING-THE-LOOP.md docs/CLOSING-THE-LOOP.md
```

- If identical: delete root copy, keep `docs/` copy (that is what MkDocs uses)
- If different: merge content, keep in `docs/`

### Step 8: Handle Duplicate AI-TOOL-COST-COMPARISON-PLAN.md

Check if `AI-TOOL-COST-COMPARISON-PLAN.md` (root) and `phase-1-ai-tool-cost-comparison/AI-TOOL-COST-COMPARISON-PLAN.md` are identical:

```bash
diff AI-TOOL-COST-COMPARISON-PLAN.md phase-1-ai-tool-cost-comparison/AI-TOOL-COST-COMPARISON-PLAN.md
```

- If identical: delete root copy after phase folder is moved
- If different: keep the more complete version inside `phases/`

### Step 9: Update .gitignore

Add PowerPoint temp files and update any paths:

```gitignore
# PowerPoint temp files
~$*.pptx
```

Remove the root `~$presentation-internal.pptx` if tracked:
```bash
git rm --cached '~$presentation-internal.pptx' 2>/dev/null || true
```

### Step 10: Update CI Workflow

Update `.github/workflows/docs-deploy.yml` trigger paths:

**Before:**
```yaml
paths:
  - 'phase-*/**'
  - 'roadmap/**'
  - 'CLOSING-THE-LOOP.md'
  - 'services/**'
```

**After:**
```yaml
paths:
  - 'phases/**'
  - 'docs/roadmap/**'
  - 'docs/CLOSING-THE-LOOP.md'
```

Also remove the `services/**` trigger (root `services/` folder does not exist).

### Step 11: Update Root mkdocs.yml Navigation

Update all nav entries that reference moved content:

**Before:**
```yaml
- Roadmap: roadmap/ROADMAP.md
- Closing the Loop: CLOSING-THE-LOOP.md
- Comparison Plan: phase-1-ai-tool-cost-comparison/AI-TOOL-COST-COMPARISON-PLAN.md
- Cost Methodology: phase-1-ai-tool-cost-comparison/COST-MEASUREMENT-METHODOLOGY.md
- Results: phase-1-ai-tool-cost-comparison/outputs/README.md
```

**After:**
```yaml
- Roadmap: roadmap/ROADMAP.md                    # No change (resolved relative to docs/)
- Closing the Loop: CLOSING-THE-LOOP.md           # No change (resolved relative to docs/)
- Comparison Plan: phases/phase-1-ai-tool-cost-comparison/AI-TOOL-COST-COMPARISON-PLAN.md
- Cost Methodology: phases/phase-1-ai-tool-cost-comparison/COST-MEASUREMENT-METHODOLOGY.md
- Results: phases/phase-1-ai-tool-cost-comparison/outputs/README.md
```

**Wait — important MkDocs behavior**: The root `mkdocs.yml` uses `docs_dir: docs` (default). Nav entries are resolved relative to `docs/`. BUT `decisions/`, `roadmap/`, `phase-1-*/`, and `services/` are NOT inside `docs/` — they work because MkDocs can reference files outside `docs_dir` **only if they are siblings or the paths are correct from the repo root**.

Let me reconsider: Actually MkDocs resolves nav paths relative to the `docs_dir`. Checking the current setup — the root mkdocs.yml references `decisions/ADR-001-*.md` etc. If `decisions/` is not inside `docs/`, the root MkDocs build would fail. Let me verify: does `docs/decisions/` exist?

**Resolution**: The `docs/` folder likely contains symlinks or copies of `decisions/`, `roadmap/`, etc. OR the root mkdocs.yml is configured with `docs_dir: .` (current directory). Need to verify before executing.

### Step 12: Update generate-svgs.sh

```bash
# Before:
SRC="$ROOT/phase-1-ai-tool-cost-comparison/workspace/corporate-services/diagrams"
WI="$ROOT/phase-1-ai-tool-cost-comparison/workspace/work-items/"

# After:
SRC="$ROOT/phases/phase-1-ai-tool-cost-comparison/workspace/corporate-services/diagrams"
WI="$ROOT/phases/phase-1-ai-tool-cost-comparison/workspace/work-items/"
```

### Step 13: Update copilot-instructions.md

Update all path references in `.github/copilot-instructions.md` to reflect new locations. Key changes:

| Old Path | New Path |
|----------|----------|
| `phase-1-ai-tool-cost-comparison/` | `phases/phase-1-ai-tool-cost-comparison/` |
| `phase-6-documentation-publishing/` | `phases/phase-6-documentation-publishing/` |
| `scripts/audit-data-isolation.sh` | `portal/scripts/utilities/audit-data-isolation.sh` |
| `scripts/openrouter-cost.py` | `portal/scripts/utilities/openrouter-cost.py` |
| `scripts/cost-measurement.py` | `portal/scripts/utilities/cost-measurement.py` |
| `roadmap/ROADMAP.md` | `docs/roadmap/ROADMAP.md` |

### Step 14: Verify Build

```bash
# Activate venv
source .venv/bin/activate

# Run full portal build
bash portal/scripts/generate-all.sh

# Run root MkDocs build (if still maintained)
python3 -m mkdocs build
```

---

## Pre-Execution Checks

Before executing, verify:

1. [ ] Are `CLOSING-THE-LOOP.md` (root) and `docs/CLOSING-THE-LOOP.md` identical?
2. [ ] Are `AI-TOOL-COST-COMPARISON-PLAN.md` (root) and `phase-1-*/AI-TOOL-COST-COMPARISON-PLAN.md` identical?
3. [ ] Does `docs/roadmap/` already exist?
4. [ ] Does `docs/decisions/` already exist (as symlink or copy)?
5. [ ] What is the effective `docs_dir` in root `mkdocs.yml`? (default `docs/` or explicit)
6. [ ] Is `~$presentation-internal.pptx` tracked in git?
7. [ ] Are there any other files referencing `phase-1-ai-tool-cost-comparison` paths?

---

## Risk Assessment

| Risk | Mitigation |
|------|------------|
| CI/CD build breaks | Update workflow trigger paths and generate-svgs.sh paths before pushing |
| Root MkDocs build breaks | Verify docs_dir resolution and nav paths with local build |
| Portal build breaks | generate-svgs.sh is the only portal script referencing phase paths; update it |
| copilot-instructions.md out of date | Bulk find-and-replace all moved paths |
| Deep links in docs break | No external links point to phase folders; internal links are in mkdocs nav only |

---

## Rollback Plan

All moves use `git mv` which preserves history. If anything breaks:

```bash
git reset --hard HEAD~1  # Undo the reorganization commit
```

---

## Final Root Structure After Execution

```
ROOT/
├── .github/
├── .gitignore
├── LICENSE
├── README.md
├── architecture/            # Architect workspace (specs, metadata, events)
├── decisions/               # Architecture Decision Records
├── docs/                    # Root MkDocs source + roadmap + narrative docs
├── infra/                   # Azure infrastructure as code
├── mkdocs.yml               # Root MkDocs config
├── phases/                  # All 6 delivery phases
├── portal/                  # Primary NovaTrek Architecture Portal
├── presentation/            # Executive presentation site + .pptx files
├── research/                # Deep research documents
├── requirements-docs.txt    # Python dependencies
└── staticwebapp.config.json # Root site Azure SWA config
```

**Visible root items: 14** (down from 20+)
**Folders: 8** (down from 14)
**Loose files: 5** (down from 7+)
