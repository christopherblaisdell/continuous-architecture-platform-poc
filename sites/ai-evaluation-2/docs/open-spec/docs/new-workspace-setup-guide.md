# New Workspace Setup Guide — AI Customization System

This guide walks through reproducing the full AI customization governance system
in a new workspace from scratch. Follow the steps in order.

Reference: `docs/ai-customization-system-inventory.md` for the full file inventory.

---

## Prerequisites

- Node.js via nvm (for OpenSpec)
- VS Code with GitHub Copilot and Roo Code extensions

---

## Step 1 — Install OpenSpec CLI

```bash
npm install -g @fission-ai/openspec@1.3.1
```

Verify:

```bash
openspec --version
# Should output: 1.3.1
```

---

## Step 2 — Copy the Canonical Hub

Copy the entire `.ai-customizations/` directory into the new workspace. This is the
full canonical source — all rules live here.

Key files that must be present:

```
.ai-customizations/
├── README.md
├── core-instructions.md
├── modes.yaml
├── setup-ai-tools.sh
├── universal/               (5 files)
├── methodologies/           (8 files)
├── standards/               (8 files)
├── mode-customizations/     (8 files)
└── user-prompts/
    └── jira-extract.prompt.md
```

**Update `setup-ai-tools.sh`:** The `SOURCE_DIR` variable at the top of the script
is hardcoded to the old workspace path. Update it to the new workspace path:

```bash
SOURCE_DIR="/path/to/new-workspace/.ai-customizations"
```

---

## Step 3 — Copy the Derived Files

Copy these files. They have `DERIVED FILE` headers — do not strip the headers.

```
.clinerules
.github/copilot-instructions.md
.github/instructions/prompt-me.instructions.md
.github/instructions/prompt-mirror.instructions.md
.github/instructions/plantuml-svg.instructions.md
```

If `.github/` does not exist in the new workspace, create it:

```bash
mkdir -p .github/instructions
```

---

## Step 4 — Run `openspec init`

```bash
cd /path/to/new-workspace
openspec init
```

This creates the `openspec/` directory and injects Copilot slash-command prompts
and skill files into `.github/`.

After `openspec init`, the following will exist:
```
openspec/config.yaml
.github/prompts/opsx-propose.prompt.md
.github/prompts/opsx-apply.prompt.md
.github/prompts/opsx-archive.prompt.md
.github/prompts/opsx-explore.prompt.md
.github/skills/openspec-propose/SKILL.md
.github/skills/openspec-apply-change/SKILL.md
.github/skills/openspec-archive-change/SKILL.md
.github/skills/openspec-explore/SKILL.md
```

---

## Step 5 — Replace `openspec/config.yaml`

After `openspec init`, replace the generated `openspec/config.yaml` with the
customized version from this workspace. The key additions are the `context:` block
and the `rules:` block.

Copy the full content from this workspace's `openspec/config.yaml`.

---

## Step 6 — Copy the Governance Spec

```
openspec/specs/ai-customization-governance/spec.md
```

Create the directory if needed:

```bash
mkdir -p openspec/specs/ai-customization-governance
```

---

## Step 7 — Fork and Customize the Schema

Either copy the schema directory directly:

```
openspec/schemas/ai-customization-change/
├── schema.yaml
└── templates/
    ├── proposal.md
    ├── tasks.md
    ├── design.md
    └── spec.md
```

Or recreate it by forking and then replacing the template files:

```bash
openspec schema fork spec-driven ai-customization-change
# Then replace templates/proposal.md and templates/tasks.md with the customized versions
```

The two customized templates are the critical files. Copy them from:
- `openspec/schemas/ai-customization-change/templates/proposal.md`
- `openspec/schemas/ai-customization-change/templates/tasks.md`

---

## Step 8 — Copy the Validation Script

```bash
mkdir -p scripts
cp scripts/validate-ai-customizations.sh /path/to/new-workspace/scripts/
chmod +x /path/to/new-workspace/scripts/validate-ai-customizations.sh
```

Run it to verify everything is in order:

```bash
scripts/validate-ai-customizations.sh
# Expected: Errors: 0, Warnings: 0
```

If checks fail, see the troubleshooting section below.

---

## Step 9 — Install the Pre-Commit Hook

```bash
cp /path/to/new-workspace/.git/hooks/pre-commit /path/to/target/.git/hooks/pre-commit
chmod +x /path/to/target/.git/hooks/pre-commit
```

Or create it manually — full content:

```sh
#!/bin/sh
# Pre-commit hook to remind about sensitive content

echo "REMINDER: Ensure you're not committing any credentials, keys, or passwords."
echo ""

# Check if AI customization files are staged — if so, run validation
AI_FILES_STAGED=$(git diff --cached --name-only | grep -E '^\.(ai-customizations|github|clinerules|roomodes)' || true)
if [ -n "$AI_FILES_STAGED" ]; then
    SCRIPT="$(git rev-parse --show-toplevel)/scripts/validate-ai-customizations.sh"
    if [ -x "$SCRIPT" ]; then
        echo "AI customization files staged — running drift validation..."
        echo ""
        if ! "$SCRIPT"; then
            echo ""
            echo "Commit blocked: AI customization drift detected. Fix the errors above."
            echo "To bypass (not recommended): git commit --no-verify"
            exit 1
        fi
        echo ""
    fi
fi

exit 0
```

---

## Step 10 — Configure `.gitignore`

The `.gitignore` in this workspace uses an allow-list pattern (ignore everything,
then explicitly allow tracked directories). If the new workspace uses a similar
approach, add these entries:

```gitignore
# Allow AI customizations
!.ai-customizations/
!.ai-customizations/**

# Allow derived AI files
!.clinerules
!.github/
!.github/**

# Allow OpenSpec
!openspec/
!openspec/**

# Allow scripts
!scripts/
!scripts/**
```

---

## Step 11 — Run the Machine Setup Script

This symlinks the canonical hub into Roo Code's global config and links
user prompts into VS Code:

```bash
chmod +x .ai-customizations/setup-ai-tools.sh
./.ai-customizations/setup-ai-tools.sh
```

After this:
- `~/.config/roo/ai-customizations` → `<workspace>/.ai-customizations/`
- `~/.config/roo/modes.yaml` → `<workspace>/.ai-customizations/modes.yaml`
- VS Code user prompts symlinked from `user-prompts/`

**Note:** Update `SOURCE_DIR` in `setup-ai-tools.sh` to the new workspace path first (see Step 2).

---

## Step 12 — Final Validation

```bash
scripts/validate-ai-customizations.sh
```

Expected output:
```
Errors:   0
Warnings: 0
RESULT: PASSED
```

If any check fails, see troubleshooting below.

---

## What Is NOT Included (Deferred)

These items were skipped in the original implementation and remain as future work:

| Item | Why Skipped | Priority |
|---|---|---|
| `scripts/sync-ai-customizations.sh` | High effort — requires scripting per-file assembly logic | High — needed before team rollout |
| Tracked pre-commit hook (`.git-hooks/pre-commit` + `core.hooksPath`) | Low value for single-developer workspace | Medium — needed for team rollout |
| Phase 10 end-to-end test | No suitable test change available at time of implementation | Low |
| Phase 11 roadmap update | Minor bookkeeping | Low |

---

## Troubleshooting

### `[FAIL] <file> is MISSING the DERIVED FILE header`

The file does not have the `DERIVED FILE — DO NOT EDIT DIRECTLY` comment at the top.
Add the appropriate header:

For `.clinerules`:
```
[//]: # (DERIVED FILE — DO NOT EDIT DIRECTLY)
[//]: # (Canonical source: .ai-customizations/core-instructions.md + .ai-customizations/universal/)
[//]: # (To make changes: /opsx:propose "description" then run scripts/sync-ai-customizations.sh)
[//]: # (Validation: scripts/validate-ai-customizations.sh)
[//]: # (Governance: openspec/specs/ai-customization-governance/spec.md)
```

For `.github/copilot-instructions.md` and `.github/instructions/*.instructions.md`:
```
<!-- ============================================================
     DERIVED FILE — DO NOT EDIT DIRECTLY
     Canonical source: .ai-customizations/core-instructions.md
                       .ai-customizations/universal/
     To make changes: /opsx:propose "description of change"
     Then run: scripts/sync-ai-customizations.sh
     Validation: scripts/validate-ai-customizations.sh
     Governance: openspec/specs/ai-customization-governance/spec.md
     ============================================================ -->
```

For `.github/instructions/*.instructions.md`, the header goes AFTER the YAML frontmatter block.

### `[FAIL] prompt-me.instructions.md and guided-plan-execution.md have DRIFTED`

The content of the two paired files has diverged. The validation script strips
multi-line HTML comment blocks before diffing (using awk, not sed — macOS sed
does not support multi-line patterns). If this check fails unexpectedly, confirm
the awk strip pattern is present in the validation script:

```bash
strip_html_blocks='BEGIN{skip=0} /^<!-- ===/{ skip=1 } skip && /-->$/{ skip=0; next } skip{ next } 1'
```

### `[FAIL] openspec/config.yaml exists (OpenSpec initialized)`

Run `openspec init` in the workspace root.

### `[FAIL] AI customization governance spec exists`

Create the directory and copy the spec:
```bash
mkdir -p openspec/specs/ai-customization-governance
# Copy openspec/specs/ai-customization-governance/spec.md from this workspace
```

---

## Change Workflow (Once Set Up)

All changes to AI customization rules go through OpenSpec:

```bash
# 1. Propose
/opsx:propose --schema ai-customization-change "description of change"

# 2. Review proposal.md, update design.md
# 3. Apply
/opsx:apply

# 4. Verify
scripts/validate-ai-customizations.sh

# 5. Archive
/opsx:archive
```

Reference: `.ai-customizations/README.md` — "How to Make Changes" section.
