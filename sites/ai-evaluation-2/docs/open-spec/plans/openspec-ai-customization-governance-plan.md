# OpenSpec AI Customization Governance — Integration Plan

## Objective

Integrate OpenSpec as the mandatory change management gateway for all AI customization
files in this workspace. After this plan is fully executed:

- **No AI customization file is ever edited directly** — not `.clinerules`, not
  `.github/copilot-instructions.md`, not any `.github/instructions/*.md`, not any
  `.ai-customizations/` canonical file.
- **Every change goes through an OpenSpec change proposal** — proposal, spec,
  design, and task list are created before any file is touched.
- **A sync script propagates accepted changes** from the canonical hub
  (`.ai-customizations/`) to all derived/tool-specific files atomically.
- **Validation and git hooks enforce** the "no direct edit" rule so drift is
  structurally impossible, not just a convention.

---

## Current State

### Canonical Hub (source of truth)

```
.ai-customizations/
├── core-instructions.md          ← base rules for ALL modes
├── universal/                    ← always-loaded standards (5 files)
├── methodologies/                ← workflows (8 files, some with paired files)
├── standards/                    ← domain standards (7 files)
├── mode-customizations/          ← per-mode instructions (8 files)
└── modes.yaml                    ← Roo global mode definitions
```

### Derived / Tool-Specific Files (currently edited by hand or by convention)

| Derived File | Source |
|---|---|
| `.clinerules` | Summarized from `.ai-customizations/core-instructions.md` + `universal/` |
| `.github/copilot-instructions.md` | Summarized from `.ai-customizations/core-instructions.md` + `universal/` |
| `.github/instructions/prompt-me.instructions.md` | Paired with `.ai-customizations/methodologies/guided-plan-execution.md` |
| `.github/instructions/prompt-mirror.instructions.md` | Paired with `.ai-customizations/methodologies/prompt-mirror.md` |
| `.github/instructions/plantuml-svg.instructions.md` | Scoped instruction, currently standalone |

### Existing Validation Infrastructure

- `scripts/validate-ai-customizations.sh` — checks file existence, YAML frontmatter,
  paired file sync, and key rule presence.
- `<!-- PAIRED FILE -->` comments in paired methodology files reference this script.

### Gap

There is no workflow enforcement. Any developer (or AI agent) can open
`.clinerules` and edit it directly. The `validate-ai-customizations.sh` script
detects drift after the fact, but nothing prevents the direct edit from happening.
OpenSpec fills this gap by making every change go through a structured proposal
cycle before touching any file.

---

## Target State

```
Developer intent
       │
       ▼
/opsx:propose "description of change"
       │
       ▼
openspec/changes/<change-name>/
├── proposal.md    ← WHY: intent, rationale, affected files
├── specs/         ← WHAT: requirements and scenarios (BDD-style)
├── design.md      ← HOW: which canonical files change and what they say after
└── tasks.md       ← CHECKLIST: atomic tasks the AI executes
       │
       ▼
/opsx:apply  (AI executes tasks.md)
       │  Every task that touches AI customizations calls:
       │  scripts/sync-ai-customizations.sh
       │
       ▼
Canonical files updated (.ai-customizations/)
Derived files regenerated atomically
Validation script passes
       │
       ▼
/opsx:archive
       │
       ▼
Change archived. No drift. One audit trail.
```

---

## Complexity Assessment

| Component | Change | Complexity |
|---|---|---|
| OpenSpec CLI install | `npm install -g @fission-ai/openspec@latest` | LOW |
| `openspec init` | New `openspec/` directory + injected agent guidance | LOW |
| `openspec/specs/ai-customization-governance/spec.md` | New governance spec | MEDIUM |
| `.clinerules` | Add "DERIVED FILE — DO NOT EDIT DIRECTLY" header block | LOW |
| `.github/copilot-instructions.md` | Add "DERIVED FILE — DO NOT EDIT DIRECTLY" header block | LOW |
| `.github/instructions/prompt-me.instructions.md` | Add "DERIVED FILE" header | LOW |
| `.github/instructions/prompt-mirror.instructions.md` | Add "DERIVED FILE" header | LOW |
| `.github/instructions/plantuml-svg.instructions.md` | Add "DERIVED FILE" header | LOW |
| `scripts/sync-ai-customizations.sh` | New script: assembles derived files from canonical sources | HIGH |
| `scripts/validate-ai-customizations.sh` | Add check: derived files have "DO NOT EDIT" header | MEDIUM |
| `.git/hooks/pre-commit` | New hook: warns when derived files are edited without sync script | MEDIUM |
| `.ai-customizations/README.md` | Add "How to make changes" section referencing OpenSpec | MEDIUM |
| OpenSpec change template | `openspec/schemas/ai-customization-change/` custom template | MEDIUM |

**Total components**: 13
**Breakdown**: 6 LOW, 4 MEDIUM, 1 HIGH

---

## Implementation Phases

---

### Phase 1 — Install and Initialize OpenSpec ✓ COMPLETE

**Goal**: OpenSpec is installed and initialized in the workspace. Agent guidance is
injected into the Copilot instruction system.

#### Tasks

1.1 Install OpenSpec CLI globally:

```bash
npm install -g @fission-ai/openspec@latest
```

1.2 Initialize OpenSpec in the workspace root:

```bash
cd /path/to/workspace
openspec init
```

This creates:

```
openspec/
├── AGENTS.md          ← slash command reference for AI agents
└── changes/           ← each change gets a folder here
```

It also injects a reference into `.github/copilot-instructions.md` (or a
`.github/instructions/` file). Review what is injected and decide whether to
accept it as-is or relocate it to `.ai-customizations/` as a canonical instruction.

1.3 Run `git status` and review all new/modified files before committing.

1.4 Update `scripts/validate-ai-customizations.sh` to check that `openspec/AGENTS.md`
exists (confirming OpenSpec is initialized).

**Exit criterion**: `openspec --version` succeeds; `openspec/` directory exists in
workspace; `validate-ai-customizations.sh` passes.

---

### Phase 2 — Define the Governance Spec

**Goal**: The authoritative spec that describes how AI customizations are managed
lives in OpenSpec. All future changes reference this spec.

#### Files to Create

**`openspec/specs/ai-customization-governance/spec.md`**

Content structure:

```
# AI Customization Governance

## Overview
The workspace AI customization system uses a canonical hub (.ai-customizations/)
and derived tool-specific files. This spec defines the governance model.

## Requirements

### REQ-GOV-001: No Direct Edits to Derived Files
The system SHALL prevent direct edits to derived AI customization files.
Derived files: .clinerules, .github/copilot-instructions.md,
               .github/instructions/*.md

### REQ-GOV-002: OpenSpec as Change Gateway
All changes to AI customization rules MUST be proposed via OpenSpec
(/opsx:propose) before any file is modified.

### REQ-GOV-003: Sync Script Atomicity
The sync script (scripts/sync-ai-customizations.sh) SHALL update all
derived files in a single atomic operation after a canonical change is applied.

### REQ-GOV-004: Validation Must Pass Before Commit
The validate-ai-customizations.sh script MUST pass before any AI
customization change is committed.

## Scenarios

### SCENARIO: Developer wants to add a new communication rule
GIVEN a developer wants to add a rule to corporate communication standards
WHEN they run /opsx:propose "add X rule to communication standards"
THEN OpenSpec creates a change folder with proposal, specs, design, and tasks
AND the design.md identifies which canonical file changes (.ai-customizations/universal/corporate-standards.md)
AND the tasks.md includes a task to run scripts/sync-ai-customizations.sh after the edit
AND the change is not applied until /opsx:apply is run

### SCENARIO: Drift is detected
GIVEN a derived file was edited directly (bypassing OpenSpec)
WHEN validate-ai-customizations.sh runs (pre-commit or CI)
THEN the script reports a FAIL for the "DO NOT EDIT DIRECTLY" header
AND the commit is blocked by the pre-commit hook
```

**Exit criterion**: Spec file exists, is committed, is referenced from
`openspec/AGENTS.md` or equivalent agent guidance.

---

### Phase 3 — Add "Derived File" Headers to All Derived Files

**Goal**: Every derived file has a machine-readable and human-readable header
that identifies it as derived, names the canonical source, and prohibits direct edits.

#### Header Block Standard

Add to the **top** of each derived file (before any existing content):

```
<!-- ============================================================
     DERIVED FILE — DO NOT EDIT DIRECTLY
     Canonical source: .ai-customizations/<path>
     To make changes: /opsx:propose "description of change"
     Then run: scripts/sync-ai-customizations.sh
     Validation: scripts/validate-ai-customizations.sh
     ============================================================ -->
```

For `.clinerules` (no HTML comments — use a markdown comment at top):

```
[//]: # (DERIVED FILE — DO NOT EDIT DIRECTLY)
[//]: # (Canonical source: .ai-customizations/core-instructions.md + universal/)
[//]: # (To make changes: /opsx:propose "description" then run scripts/sync-ai-customizations.sh)
```

#### Files to Update

| File | Canonical Source |
|---|---|
| `.clinerules` | `.ai-customizations/core-instructions.md` + `universal/` |
| `.github/copilot-instructions.md` | `.ai-customizations/core-instructions.md` + `universal/` |
| `.github/instructions/prompt-me.instructions.md` | `.ai-customizations/methodologies/guided-plan-execution.md` |
| `.github/instructions/prompt-mirror.instructions.md` | `.ai-customizations/methodologies/prompt-mirror.md` |
| `.github/instructions/plantuml-svg.instructions.md` | `.ai-customizations/` (to be designated) |

**Exit criterion**: All 5 derived files have the header; `grep -r "DERIVED FILE" .github/instructions .clinerules .github/copilot-instructions.md` returns 5 matches.

---

### Phase 4 — Create the Sync Script

**Goal**: A single script assembles all derived files from their canonical sources.
This is what OpenSpec tasks call as the final step of any AI customization change.

#### File: `scripts/sync-ai-customizations.sh`

The script performs:

1. **Assemble `.clinerules`**:
   - Header block (DERIVED FILE warning)
   - Content of `.ai-customizations/core-instructions.md`
   - Summary references to `universal/` files (same content currently in `.clinerules`)

2. **Assemble `.github/copilot-instructions.md`**:
   - Header block
   - Content of `.ai-customizations/core-instructions.md` (the shared base)
   - Architecture source locations section
   - Commit policy
   - AI Customization Awareness section

3. **Sync paired methodology files**:
   - Copy `.ai-customizations/methodologies/guided-plan-execution.md` body into
     `.github/instructions/prompt-me.instructions.md` (preserving YAML frontmatter)
   - Copy `.ai-customizations/methodologies/prompt-mirror.md` body into
     `.github/instructions/prompt-mirror.instructions.md` (preserving YAML frontmatter)

4. **Run `scripts/validate-ai-customizations.sh`** as a final check. Exit non-zero
   if validation fails.

```bash
#!/bin/bash
# scripts/sync-ai-customizations.sh
# Assembles all derived AI customization files from canonical sources.
# Called by OpenSpec tasks after any change to .ai-customizations/.
# DO NOT call directly — use /opsx:propose to initiate a change.

set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# ... (full implementation as a phase 4 task)

echo "Running validation..."
"$REPO_ROOT/scripts/validate-ai-customizations.sh"
echo "Sync complete."
```

**Exit criterion**: Running `scripts/sync-ai-customizations.sh` produces identical
content to the current derived files (no change on first run); `validate-ai-customizations.sh`
passes after the sync.

---

### Phase 5 — Update the Validation Script

**Goal**: `validate-ai-customizations.sh` enforces the "DERIVED FILE" invariant so
drift is detected immediately.

#### New Checks to Add

**Check 5A**: Every derived file has the "DERIVED FILE — DO NOT EDIT DIRECTLY" header.

```bash
echo ""
echo "=== Derived File Header Checks ==="
echo ""

derived_files=(
    ".github/copilot-instructions.md"
    ".clinerules"
    ".github/instructions/prompt-me.instructions.md"
    ".github/instructions/prompt-mirror.instructions.md"
    ".github/instructions/plantuml-svg.instructions.md"
)

for f in "${derived_files[@]}"; do
    if grep -q "DERIVED FILE" "$REPO_ROOT/$f" 2>/dev/null; then
        pass "$f has DERIVED FILE header"
    else
        fail "$f is MISSING the DERIVED FILE header — was it edited directly?"
    fi
done
```

**Check 5B**: `openspec/AGENTS.md` exists (OpenSpec is initialized).

```bash
if [ -f "$REPO_ROOT/openspec/AGENTS.md" ]; then
    pass "openspec/AGENTS.md exists (OpenSpec initialized)"
else
    fail "openspec/AGENTS.md missing — run: openspec init"
fi
```

**Check 5C**: The governance spec exists.

```bash
if [ -f "$REPO_ROOT/openspec/specs/ai-customization-governance/spec.md" ]; then
    pass "AI customization governance spec exists"
else
    fail "openspec/specs/ai-customization-governance/spec.md missing"
fi
```

**Exit criterion**: `validate-ai-customizations.sh` passes with the new checks present.

---

### Phase 6 — Add a Pre-Commit Git Hook

**Goal**: A git pre-commit hook warns when derived files are staged for commit without
being accompanied by a sync script run. This is the structural enforcement layer.

#### File: `.git/hooks/pre-commit`

The hook:
1. Checks the git staged diff for changes to derived files.
2. If any derived file is staged AND the sync script has not been run in this
   session (detected by a `.sync-lock` temp file or by checking whether the
   staged content has the DERIVED FILE header), it emits a warning and exits 1.
3. Always runs `validate-ai-customizations.sh` before allowing the commit.

```bash
#!/bin/bash
# .git/hooks/pre-commit
# Prevents direct edits to derived AI customization files.

REPO_ROOT="$(git rev-parse --show-toplevel)"

DERIVED_FILES=(
    ".github/copilot-instructions.md"
    ".clinerules"
    ".github/instructions/prompt-me.instructions.md"
    ".github/instructions/prompt-mirror.instructions.md"
    ".github/instructions/plantuml-svg.instructions.md"
)

blocked=0
for f in "${DERIVED_FILES[@]}"; do
    if git diff --cached --name-only | grep -qF "$f"; then
        # File is staged — check that it has the DERIVED FILE header
        if ! git show ":$f" 2>/dev/null | grep -q "DERIVED FILE"; then
            echo "[ERROR] $f is staged but is MISSING the DERIVED FILE header."
            echo "        Do not edit derived files directly."
            echo "        Use: /opsx:propose 'description of change'"
            echo "        Then run: scripts/sync-ai-customizations.sh"
            blocked=1
        fi
    fi
done

if [ "$blocked" -eq 1 ]; then
    exit 1
fi

# Always run validation before committing AI customization changes
if git diff --cached --name-only | grep -qE '\.ai-customizations/|\.clinerules|copilot-instructions|\.instructions\.md'; then
    echo "AI customization files staged — running validation..."
    "$REPO_ROOT/scripts/validate-ai-customizations.sh"
fi

exit 0
```

Note: `.git/hooks/` is not tracked by git. After cloning, the hook must be installed
via `scripts/setup-ai-tools.sh` (update that script to copy the hook).

**Exit criterion**: Attempting to commit a direct edit to `.clinerules` without
the DERIVED FILE header is blocked. A clean sync-then-commit succeeds.

---

### Phase 7 — Create OpenSpec Change Template for AI Customizations

**Goal**: When a developer runs `/opsx:propose "change X in AI customizations"`, a
specialized template is used that pre-populates the correct artifacts for AI
customization changes specifically — including identifying canonical vs. derived
files and always including the sync script task.

#### File: `openspec/schemas/ai-customization-change/template.md`

This is a community schema / custom template that OpenSpec uses when the change
description contains "customization", "instruction", "mode", "rule", "standard",
or "clinerules".

Template structure:

```markdown
# Proposal: {{change-name}}

## Intent
<!-- What rule, standard, or methodology is changing and why -->

## Affected Canonical Files
<!-- List the .ai-customizations/ files that need to change -->
- [ ] .ai-customizations/...

## Affected Derived Files (do not edit directly)
<!-- These are updated by scripts/sync-ai-customizations.sh -->
- .clinerules
- .github/copilot-instructions.md
- .github/instructions/...

## Rationale
<!-- Why this change is needed, what problem it solves -->

## Related Specs
<!-- openspec/specs/ai-customization-governance/spec.md -->
```

```markdown
# Tasks: {{change-name}}

- [ ] 1. Edit canonical file(s) in .ai-customizations/ as specified in design.md
- [ ] 2. Run `scripts/sync-ai-customizations.sh` to propagate changes to derived files
- [ ] 3. Run `scripts/validate-ai-customizations.sh` — confirm all checks pass
- [ ] 4. Stage all changed files (canonical + derived)
- [ ] 5. Commit with message: `feat(ai-customizations): {{change-name}}`
```

**Exit criterion**: A test `/opsx:propose` for an AI customization change produces
a tasks.md that includes the sync script step.

---

### Phase 8 — Update `.ai-customizations/README.md`

**Goal**: The README becomes the primary "how to make changes" document and
explicitly directs developers and AI agents to use OpenSpec.

#### Section to Add

Add a new top-level section **"How to Make Changes"** immediately after the
System Overview section:

```markdown
## How to Make Changes

**All changes to AI customizations go through OpenSpec — never directly.**

### Workflow

1. **Propose**: Run `/opsx:propose "description of what you want to change"`
   OpenSpec creates `openspec/changes/<name>/` with proposal, specs, design, tasks.

2. **Review**: Review `proposal.md` and `specs/` to confirm the intent is correct.
   Update `design.md` to identify exactly which canonical files change.

3. **Apply**: Run `/opsx:apply`
   The AI executes `tasks.md`. The final task always runs
   `scripts/sync-ai-customizations.sh`, which updates all derived files atomically.

4. **Validate**: `scripts/validate-ai-customizations.sh` runs automatically.
   All checks must pass before the commit is made.

5. **Archive**: Run `/opsx:archive` to move the change to the archive.

### Which Files Are Canonical vs. Derived

| Canonical (edit via OpenSpec) | Derived (updated by sync script) |
|---|---|
| `.ai-customizations/**` | `.clinerules` |
| | `.github/copilot-instructions.md` |
| | `.github/instructions/prompt-me.instructions.md` |
| | `.github/instructions/prompt-mirror.instructions.md` |
| | `.github/instructions/plantuml-svg.instructions.md` |

### Why OpenSpec

The previous system relied on manual conventions (`<!-- PAIRED FILE -->` comments,
`validate-ai-customizations.sh` drift detection). Drift still happened because
nothing prevented direct edits. OpenSpec makes the change proposal step
structurally mandatory — you can't apply a change without first creating the
artifacts that describe what changed and why.
```

**Exit criterion**: README contains the "How to Make Changes" section with the
canonical/derived table and the 5-step OpenSpec workflow.

---

### Phase 9 — Install the Pre-Commit Hook Automatically

**Goal**: `scripts/setup-ai-tools.sh` (the one-time machine setup script) also
installs the pre-commit hook, so new developers get enforcement automatically.

#### Change to `scripts/setup-ai-tools.sh` (or `.ai-customizations/setup-ai-tools.sh`)

Add:

```bash
# --- Install pre-commit hook ---
HOOK_SRC="$REPO_ROOT/.git-hooks/pre-commit"
HOOK_DST="$REPO_ROOT/.git/hooks/pre-commit"

if [ -f "$HOOK_SRC" ]; then
    cp "$HOOK_SRC" "$HOOK_DST"
    chmod +x "$HOOK_DST"
    echo "Installed pre-commit hook"
else
    echo "WARNING: .git-hooks/pre-commit not found — hook not installed"
fi
```

Move the hook source from `.git/hooks/pre-commit` (untracked) to
`.git-hooks/pre-commit` (tracked) so it is version-controlled and
`setup-ai-tools.sh` can install it.

**Exit criterion**: A fresh clone + `setup-ai-tools.sh` results in a working
pre-commit hook.

---

### Phase 10 — Validate End-to-End with a Real Change

**Goal**: Prove the full workflow works by making a real (but small) AI
customization change through OpenSpec.

#### Test Change

Add a new rule to `.ai-customizations/universal/corporate-standards.md`:

```
- Never use "leverage" as a verb — use "use" or "apply"
```

#### Workflow Verification Steps

1. `/opsx:propose "add no-leverage-verb rule to corporate communication standards"`
2. Review generated `openspec/changes/add-no-leverage-verb-rule/`
3. Verify `design.md` correctly identifies `universal/corporate-standards.md` as
   the canonical file
4. Verify `tasks.md` includes `scripts/sync-ai-customizations.sh` as a task
5. `/opsx:apply` — confirm the AI edits the canonical file and runs sync
6. Confirm `.clinerules` and `.github/copilot-instructions.md` are updated
7. `scripts/validate-ai-customizations.sh` passes
8. Attempt to commit a direct edit to `.clinerules` — confirm the hook blocks it
9. `/opsx:archive`

**Exit criterion**: All 9 verification steps complete successfully. Change is
committed and pushed.

---

### Phase 11 — Update the Roadmap

**Goal**: Mark the OpenSpec roadmap item as complete and document what was
integrated.

Update `ai-platform-selection/roadmap/ROADMAP.md`:

```markdown
### 1. Integrate OpenSpec into the Solution / Workspace

**Status**: Complete

**What was integrated**:
OpenSpec is now the mandatory change management gateway for all AI customization
files. See `openspec/specs/ai-customization-governance/spec.md` for the governance
spec and `.ai-customizations/README.md` for the "How to Make Changes" workflow.
```

---

## Execution Order

The phases are designed to be executed sequentially. Each phase has a clear exit
criterion that must be met before the next phase begins.

```
Phase 1  → Install + Init OpenSpec
Phase 2  → Define Governance Spec
Phase 3  → Add Derived File Headers
Phase 4  → Create Sync Script
Phase 5  → Update Validation Script
Phase 6  → Add Pre-Commit Hook (source file)
Phase 7  → Create OpenSpec Change Template
Phase 8  → Update .ai-customizations/README.md
Phase 9  → Install Hook via setup-ai-tools.sh
Phase 10 → End-to-End Validation with Real Change
Phase 11 → Update Roadmap
```

Phases 3, 4, and 5 can be executed in parallel (they touch different files).
All other phases are sequential.

---

## Files Changed / Created by This Plan

| File | Action | Phase |
|---|---|---|
| `openspec/` (directory) | Created by `openspec init` | 1 |
| `openspec/specs/ai-customization-governance/spec.md` | New | 2 |
| `.clinerules` | Add DERIVED FILE header | 3 |
| `.github/copilot-instructions.md` | Add DERIVED FILE header | 3 |
| `.github/instructions/prompt-me.instructions.md` | Add DERIVED FILE header | 3 |
| `.github/instructions/prompt-mirror.instructions.md` | Add DERIVED FILE header | 3 |
| `.github/instructions/plantuml-svg.instructions.md` | Add DERIVED FILE header | 3 |
| `scripts/sync-ai-customizations.sh` | New | 4 |
| `scripts/validate-ai-customizations.sh` | Add 3 new checks | 5 |
| `.git-hooks/pre-commit` | New (tracked) | 6 |
| `openspec/schemas/ai-customization-change/template.md` | New | 7 |
| `.ai-customizations/README.md` | Add "How to Make Changes" section | 8 |
| `.ai-customizations/setup-ai-tools.sh` | Add hook install step | 9 |
| `ai-platform-selection/roadmap/ROADMAP.md` | Update status | 11 |

**Total**: 15 files (3 new directories, 5 new files, 7 modified files)

---

## Non-Goals

- This plan does not refactor or consolidate the content of existing AI customization
  files — only the change process changes.
- This plan does not migrate historical changes retroactively into OpenSpec. Only
  future changes go through the new workflow.
- This plan does not change how OpenSpec itself works — we use it as-is, with a
  custom template and governance spec layered on top.
