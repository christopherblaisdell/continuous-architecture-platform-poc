# AI Instruction Governance

## Overview

This workspace manages AI instruction rules for two AI tools: GitHub Copilot and
Roo Code. The rules live in a canonical hub (`.ai-instructions/`) and are
propagated to tool-specific derived files. This spec defines the governance model
that ensures those files never drift and that every change is traceable.

### Hub-and-Spoke Architecture

```
.ai-instructions/              ← CANONICAL HUB (source of truth)
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

All changes to AI instruction rules MUST flow through OpenSpec:

```
/opsx:propose  →  openspec/changes/<name>/  →  /opsx:apply  →  /opsx:archive
```

After a change is accepted via OpenSpec, canonical files are edited and derived
files are updated to reflect the change. Each derived file has a
`DERIVED FILE — DO NOT EDIT DIRECTLY` header making the constraint visible to
any editor or AI tool that opens the file.

---

## Requirements

### REQ-GOV-001: No Direct Edits to Derived Files

The system SHALL prevent direct edits to derived AI instruction files.

**Derived files (MUST NOT be edited directly):**

- `.clinerules`
- `.github/copilot-instructions.md`
- `.github/instructions/prompt-me.instructions.md`
- `.github/instructions/prompt-mirror.instructions.md`
- `.github/instructions/plantuml-svg.instructions.md`

**Enforcement mechanism:**

- Each derived file has a `DERIVED FILE — DO NOT EDIT DIRECTLY` header at the top,
  making the constraint visible to any editor or AI tool that opens the file.
- `scripts/validate-ai-instructions.sh` can be run manually to confirm all headers
  are present before committing.

---

### REQ-GOV-002: OpenSpec as Change Gateway

All changes to AI instruction rules MUST be proposed via OpenSpec before any
file is modified.

**Process:**

1. Run `/opsx:propose "description of change"` to open a change.
2. Review and accept the generated `proposal.md`, `specs/`, `design.md`, and `tasks.md`.
3. Run `/opsx:apply` to execute the tasks (edit canonical files, then update all
   derived files ensuring the DERIVED FILE header is preserved in each).
4. Run `/opsx:archive` to close the change.

**This spec (`openspec/specs/ai-instruction-governance/spec.md`) MUST be
referenced in the design of every AI instruction change.**

---

### REQ-GOV-003: Validation Must Pass Before Commit

`scripts/validate-ai-instructions.sh` MUST pass (0 errors, 0 warnings) before
any AI instruction change is committed to git.

**Triggered by:**

- Manually, before committing any AI instruction change.

**Checks that must pass:**

- All 5 derived files exist.
- All 5 derived files have the `DERIVED FILE` header.
- Paired methodology files are in sync.
- Key rules are present in both base files.
- `openspec/config.yaml` exists (OpenSpec is initialized).
- This governance spec exists (`openspec/specs/ai-instruction-governance/spec.md`).

---

## Scenarios

### SCENARIO: Developer Wants to Add a New Communication Rule

```
GIVEN a developer wants to add a rule to corporate communication standards
WHEN they run /opsx:propose "add X rule to communication standards"
THEN OpenSpec creates a change folder with proposal, specs, design, and tasks
AND the design.md identifies which canonical file changes
    (.ai-instructions/universal/corporate-standards.md)
AND the change is not applied until /opsx:apply is run
AND after /opsx:apply, all 5 derived files are updated to reflect the new rule
    (with DERIVED FILE header preserved in each)
AND validate-ai-instructions.sh passes
```

### SCENARIO: Drift Is Detected

```
GIVEN a derived file was edited directly (bypassing OpenSpec)
WHEN validate-ai-instructions.sh is run manually
THEN the script reports a FAIL for the "DERIVED FILE" header check
AND the developer is directed to restore the header and use /opsx:propose
    to make future changes properly
```

---

## File Inventory

| File | Role | Governed By |
|---|---|---|
| `.ai-instructions/core-instructions.md` | Canonical base rules | REQ-GOV-002 |
| `.ai-instructions/universal/` | Canonical universal standards | REQ-GOV-002 |
| `.ai-instructions/methodologies/` | Canonical methodologies | REQ-GOV-002 |
| `.clinerules` | Derived — Roo Code | REQ-GOV-001 |
| `.github/copilot-instructions.md` | Derived — GitHub Copilot | REQ-GOV-001 |
| `.github/instructions/*.instructions.md` | Derived — Copilot scoped | REQ-GOV-001 |
| `scripts/validate-ai-instructions.sh` | Validation script | REQ-GOV-003 |
| `openspec/specs/ai-instruction-governance/spec.md` | This spec | All |
