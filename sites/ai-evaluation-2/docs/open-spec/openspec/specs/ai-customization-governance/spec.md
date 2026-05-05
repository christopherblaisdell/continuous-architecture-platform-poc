# AI Customization Governance

## Overview

This workspace manages AI customization rules for two AI tools: GitHub Copilot and
Roo Code. The rules live in a canonical hub (`.ai-customizations/`) and are
propagated to tool-specific derived files. This spec defines the governance model
that ensures those files never drift and that every change is traceable.

### Hub-and-Spoke Architecture

```
.ai-customizations/              ← CANONICAL HUB (source of truth)
├── core-instructions.md         ← base rules for ALL modes
├── universal/                   ← always-loaded standards (5 files)
├── methodologies/               ← workflows (8 files)
├── standards/                   ← domain standards (7 files)
├── mode-customizations/         ← per-mode instructions (8 files)
└── modes.yaml                   ← Roo global mode definitions

Derived files (assembled from canonical hub):
├── .clinerules                             ← Roo Code base instructions
├── .github/copilot-instructions.md         ← GitHub Copilot base instructions
├── .github/instructions/prompt-me.instructions.md
├── .github/instructions/prompt-mirror.instructions.md
└── .github/instructions/plantuml-svg.instructions.md
```

### Change Gateway

All changes to AI customization rules MUST flow through OpenSpec:

```
/opsx:propose  →  openspec/changes/<name>/  →  /opsx:apply  →  /opsx:archive
```

The `scripts/sync-ai-customizations.sh` script propagates accepted changes from
the canonical hub to all derived files atomically. It is always called as the
final task in any AI customization change.

---

## Requirements

### REQ-GOV-001: No Direct Edits to Derived Files

The system SHALL prevent direct edits to derived AI customization files.

**Derived files (MUST NOT be edited directly):**

- `.clinerules`
- `.github/copilot-instructions.md`
- `.github/instructions/prompt-me.instructions.md`
- `.github/instructions/prompt-mirror.instructions.md`
- `.github/instructions/plantuml-svg.instructions.md`

**Enforcement mechanisms:**

- Each derived file has a `DERIVED FILE — DO NOT EDIT DIRECTLY` header at the top.
- `scripts/validate-ai-customizations.sh` checks for this header on every staged commit.
- A git pre-commit hook (`.git/hooks/pre-commit`) blocks commits that stage a derived
  file without the header, or that show the header was removed.

---

### REQ-GOV-002: OpenSpec as Change Gateway

All changes to AI customization rules MUST be proposed via OpenSpec before any
file is modified.

**Process:**

1. Run `/opsx:propose "description of change"` to open a change.
2. Review and accept the generated `proposal.md`, `specs/`, `design.md`, and `tasks.md`.
3. Run `/opsx:apply` to execute the tasks (which include editing canonical files and
   running `scripts/sync-ai-customizations.sh`).
4. Run `/opsx:archive` to close the change.

**This spec (`openspec/specs/ai-customization-governance/spec.md`) MUST be
referenced in the design of every AI customization change.**

---

### REQ-GOV-003: Sync Script Atomicity

The sync script (`scripts/sync-ai-customizations.sh`) SHALL update ALL derived
files in a single atomic operation each time it is run.

**Requirements:**

- The script reads from `.ai-customizations/` canonical sources only.
- The script writes all derived files in a single pass.
- The script runs `scripts/validate-ai-customizations.sh` as its final step.
- The script exits non-zero if validation fails, leaving the working tree unchanged.
- The script is idempotent: running it twice produces the same result.

---

### REQ-GOV-004: Validation Must Pass Before Commit

`scripts/validate-ai-customizations.sh` MUST pass (0 errors, 0 warnings) before
any AI customization change is committed to git.

**Triggered by:**

- The git pre-commit hook (automatic, for any staged AI customization file).
- The sync script (automatic, as its final step).
- Manually at any time.

**Checks that must pass:**

- All 5 derived files exist.
- All 5 derived files have the `DERIVED FILE` header.
- Paired methodology files are in sync.
- Key rules are present in both base files.
- `openspec/config.yaml` exists (OpenSpec is initialized).
- This governance spec exists (`openspec/specs/ai-customization-governance/spec.md`).

---

## Scenarios

### SCENARIO: Developer Wants to Add a New Communication Rule

```
GIVEN a developer wants to add a rule to corporate communication standards
WHEN they run /opsx:propose "add X rule to communication standards"
THEN OpenSpec creates a change folder with proposal, specs, design, and tasks
AND the design.md identifies which canonical file changes
    (.ai-customizations/universal/corporate-standards.md)
AND the tasks.md includes a task to run scripts/sync-ai-customizations.sh
    after the canonical file is edited
AND the change is not applied until /opsx:apply is run
AND after /opsx:apply, all 5 derived files reflect the new rule
AND validate-ai-customizations.sh passes
```

### SCENARIO: Drift Is Detected

```
GIVEN a derived file was edited directly (bypassing OpenSpec)
WHEN validate-ai-customizations.sh runs (pre-commit or manually)
THEN the script reports a FAIL for the "DERIVED FILE" header check
     (or for content divergence from the canonical source)
AND the commit is blocked by the pre-commit hook
AND the developer is directed to use /opsx:propose to make the change properly
```

### SCENARIO: Sync Script Runs After a Canonical Change

```
GIVEN a canonical file in .ai-customizations/ was updated via /opsx:apply
WHEN scripts/sync-ai-customizations.sh is run
THEN all 5 derived files are regenerated from canonical sources
AND all 5 derived files have the DERIVED FILE header
AND validate-ai-customizations.sh passes with 0 errors
AND no manual edits to derived files are required
```

---

## File Inventory

| File | Role | Governed By |
|---|---|---|
| `.ai-customizations/core-instructions.md` | Canonical base rules | REQ-GOV-002 |
| `.ai-customizations/universal/` | Canonical universal standards | REQ-GOV-002 |
| `.ai-customizations/methodologies/` | Canonical methodologies | REQ-GOV-002 |
| `.clinerules` | Derived — Roo Code | REQ-GOV-001 |
| `.github/copilot-instructions.md` | Derived — GitHub Copilot | REQ-GOV-001 |
| `.github/instructions/*.instructions.md` | Derived — Copilot scoped | REQ-GOV-001 |
| `scripts/sync-ai-customizations.sh` | Sync script | REQ-GOV-003 |
| `scripts/validate-ai-customizations.sh` | Validation script | REQ-GOV-004 |
| `openspec/specs/ai-customization-governance/spec.md` | This spec | All |
