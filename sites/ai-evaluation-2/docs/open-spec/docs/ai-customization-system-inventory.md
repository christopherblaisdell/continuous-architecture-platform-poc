# AI Customization System — Complete Inventory

This document captures the full state of the AI customization governance system
as of 2026-05-05 (commit `1b1a3ca`). Use this as the authoritative reference when
setting up a new workspace.

---

## System Overview

The system enforces a hub-and-spoke architecture for AI customization rules:

- **Canonical hub**: `.ai-customizations/` — the only place rules are authored
- **Derived files**: 5 tool-specific files assembled from the hub
- **Change gateway**: OpenSpec (`@fission-ai/openspec@1.3.1`) — every change goes through `/opsx:propose`
- **Validation**: `scripts/validate-ai-customizations.sh` — 32 checks, runs on pre-commit
- **Governance spec**: `openspec/specs/ai-customization-governance/spec.md`

---

## File Inventory

### Canonical Hub — `.ai-customizations/`

These are the only files that should ever be edited directly (via OpenSpec).

| File | Purpose |
|---|---|
| `README.md` | System overview, how-to-make-changes guide, canonical vs. derived table |
| `core-instructions.md` | Base rules for ALL AI modes (communication, estimation, security, commits, etc.) |
| `INDEX.md` | Searchable index of all customizations |
| `GLOBAL-CONFIGURATION.md` | Global configuration reference |
| `IMPLEMENTATION-SUMMARY.md` | Implementation notes |
| `VALIDATION-REPORT.md` | Last validation snapshot |
| `modes.yaml` | Roo Code global mode definitions (symlinked from `~/.config/roo/modes.yaml`) |
| `setup-ai-tools.sh` | One-time machine setup: symlinks to Roo config + VS Code prompts |

#### `.ai-customizations/universal/` — Always loaded for all modes

| File | Purpose |
|---|---|
| `corporate-standards.md` | No emojis, professional tone |
| `effort-estimation.md` | Component/endpoint complexity table, never dollars |
| `markdown-formatting.md` | Header rules, formatting |
| `file-organization.md` | Directory naming standards |
| `security-uptime-basic.md` | Basic security awareness |

#### `.ai-customizations/methodologies/` — Workflow instructions

| File | Purpose | Modes |
|---|---|---|
| `guided-plan-execution.md` | Guided plan execution loop (paired with `.github/instructions/prompt-me`) | All |
| `prompt-mirror.md` | Prompt mirror context capture (paired with `.github/instructions/prompt-mirror`) | All |
| `4-phase-investigation.md` | 4-phase investigation methodology | SA, Orchestrator, Ask |
| `ticket-classification.md` | Ticket classification workflow | SA, Orchestrator |
| `bdd-tdd-methodology.md` | BDD/TDD development approach | Code, Debug, VS Code Plugin |
| `sequence-diagrams.md` | Sequence diagram standards | SA, Orchestrator |
| `plantuml-standards.md` | PlantUML standards | SA, Orchestrator, Code |
| `architecture-backlog.md` | Architecture backlog management | SA, Orchestrator |

#### `.ai-customizations/standards/` — Domain standards

| File | Purpose | Modes |
|---|---|---|
| `testing-standards.md` | Test coverage, BDD, test approach documentation | Code, Debug, VS Code Plugin |
| `impact-organization.md` | Impact analysis organization | SA, Orchestrator |
| `email-writing.md` | Email writing standards | SA, Orchestrator, Ask, Compliance |
| `component-hierarchy.md` | Component hierarchy standards | SA, Code |
| `documentation-dates.md` | ISO 8601 date standards | Compliance, SA |
| `swagger-yaml-locations.md` | OpenAPI spec file locations | SA, Code, Orchestrator |
| `plantuml-diagram-locations.md` | PlantUML diagram locations | SA, Orchestrator, Code |
| `solution-design-terminology.md` | Solution design terminology | SA |

#### `.ai-customizations/mode-customizations/` — Per-mode instructions

| File | Purpose |
|---|---|
| `all-modes.md` | References universal standards |
| `solution-architect.md` | Solution Architect mode |
| `code.md` | Code mode |
| `debug.md` | Debug mode |
| `ask.md` | Ask mode |
| `corporate-compliance.md` | Corporate Compliance mode |
| `vscode-plugin-dev.md` | VS Code Plugin Dev mode |
| `orchestrator.md` | Orchestrator mode |

#### `.ai-customizations/user-prompts/` — VS Code user-level prompts

| File | Purpose |
|---|---|
| `jira-extract.prompt.md` | JIRA ticket extraction prompt (symlinked to VS Code user prompts) |

---

### Derived Files — Never Edit Directly

These 5 files are assembled from the canonical hub. Each has a `DERIVED FILE — DO NOT EDIT DIRECTLY` header.

| File | Tool | Canonical Source | Header Format |
|---|---|---|---|
| `.clinerules` | Roo Code | `core-instructions.md` + `universal/` | Markdown comment `[//]: #` |
| `.github/copilot-instructions.md` | GitHub Copilot | `core-instructions.md` + `universal/` | HTML comment `<!-- -->` |
| `.github/instructions/prompt-me.instructions.md` | Copilot (scoped) | `methodologies/guided-plan-execution.md` | HTML comment (after YAML frontmatter) |
| `.github/instructions/prompt-mirror.instructions.md` | Copilot (scoped) | `methodologies/prompt-mirror.md` | HTML comment (after YAML frontmatter) |
| `.github/instructions/plantuml-svg.instructions.md` | Copilot (scoped) | `methodologies/plantuml-svg-workflow.md` | HTML comment (after YAML frontmatter) |

**Note:** `sync-ai-customizations.sh` is the script that regenerates these files. It does not yet exist (Phase 4 was skipped). Regeneration is currently done manually by the AI agent during apply.

---

### OpenSpec Files — `openspec/`

| File | Purpose |
|---|---|
| `openspec/config.yaml` | OpenSpec workspace config — context block + rules block |
| `openspec/specs/ai-customization-governance/spec.md` | Governance spec — REQ-GOV-001 through REQ-GOV-004 |
| `openspec/schemas/ai-customization-change/schema.yaml` | Custom schema forked from `spec-driven` |
| `openspec/schemas/ai-customization-change/templates/proposal.md` | Proposal template — canonical/derived file inventory + governance checklist |
| `openspec/schemas/ai-customization-change/templates/tasks.md` | Tasks template — edit canonical → sync → verify → commit |
| `openspec/schemas/ai-customization-change/templates/design.md` | Design template (from spec-driven fork, not customized) |
| `openspec/schemas/ai-customization-change/templates/spec.md` | Spec template (from spec-driven fork, not customized) |

#### `openspec/config.yaml` — key content

```yaml
schema: spec-driven

context: |
  Hub-and-spoke architecture:
    Canonical hub: .ai-customizations/
    Derived files (NEVER edit directly — use /opsx:propose):
      - .clinerules
      - .github/copilot-instructions.md
      - .github/instructions/prompt-me.instructions.md
      - .github/instructions/prompt-mirror.instructions.md
      - .github/instructions/plantuml-svg.instructions.md

  Change process:
    1. /opsx:propose "description"
    2. /opsx:apply
    3. /opsx:archive

  Governance spec: openspec/specs/ai-customization-governance/spec.md

rules:
  proposal:
    - Reference the governance spec
    - Identify which canonical file(s) will change
    - Identify which derived files will be regenerated
  design:
    - Show before/after diff for each canonical file
    - Confirm no derived files are edited directly
  tasks:
    - Always include a task to run scripts/sync-ai-customizations.sh
    - Always include a task to verify scripts/validate-ai-customizations.sh passes
```

---

### Scripts — `scripts/`

| File | Purpose | Status |
|---|---|---|
| `scripts/validate-ai-customizations.sh` | 32-check validation: file existence, YAML frontmatter, paired sync, key rules, derived headers, OpenSpec checks | Active — runs on pre-commit |
| `scripts/sync-ai-customizations.sh` | Regenerates all 5 derived files from canonical hub atomically | **NOT YET CREATED** (Phase 4 skipped) |
| `scripts/check-conversation-size.sh` | Conversation token size utility | Unrelated to AI customizations |
| `scripts/clone-external-repos.sh` | External repo cloning | Unrelated to AI customizations |
| `scripts/export-conversation-context.sh` | Conversation context export | Unrelated to AI customizations |

---

### GitHub Copilot Prompts — `.github/prompts/`

These are Copilot slash-command prompt files injected by `openspec init`.

| File | Copilot Command |
|---|---|
| `.github/prompts/opsx-propose.prompt.md` | `/opsx:propose` |
| `.github/prompts/opsx-apply.prompt.md` | `/opsx:apply` |
| `.github/prompts/opsx-archive.prompt.md` | `/opsx:archive` |
| `.github/prompts/opsx-explore.prompt.md` | `/opsx:explore` |

### GitHub Copilot Skills — `.github/skills/`

These are skill files injected by `openspec init`.

| File | Purpose |
|---|---|
| `.github/skills/openspec-propose/SKILL.md` | Propose skill |
| `.github/skills/openspec-apply-change/SKILL.md` | Apply skill |
| `.github/skills/openspec-archive-change/SKILL.md` | Archive skill |
| `.github/skills/openspec-explore/SKILL.md` | Explore skill |

---

### Git Infrastructure

| Item | Location | Status |
|---|---|---|
| Pre-commit hook | `.git/hooks/pre-commit` | Active (untracked — not in git) |
| Hook trigger | Runs `validate-ai-customizations.sh` when AI customization files are staged | Working |
| `.gitignore` | Explicitly un-ignores `.ai-customizations/**`, `openspec/**`, `.clinerules` | Configured |

#### Pre-commit hook behavior

The hook at `.git/hooks/pre-commit`:
1. Prints a LOCAL-ONLY air-gapped reminder
2. Detects staged files matching `^\.(ai-customizations|github|clinerules|roomodes)`
3. If any match, runs `scripts/validate-ai-customizations.sh`
4. Blocks the commit if validation fails (exit 1)

---

### Plans — `plans/`

| File | Purpose |
|---|---|
| `plans/openspec-ai-customization-governance-plan.md` | 11-phase integration plan — the master plan for this governance system |

---

## Phase Completion Status

| Phase | Description | Status |
|---|---|---|
| Phase 1 | Install OpenSpec v1.3.1, `openspec init`, fix `.gitignore` | Complete (`b127748`) |
| Phase 2 | Create governance spec + populate `openspec/config.yaml` | Complete (`8566b19`) |
| Phase 3 | Add `DERIVED FILE` headers to all 5 derived files | Complete (`abc5337`) |
| Phase 4 | Create `scripts/sync-ai-customizations.sh` | **Skipped** (defer to team rollout) |
| Phase 5 | Add derived-header checks + governance-spec check to validation script | Complete (`5ed20fa`) |
| Phase 6 | Create tracked `.git-hooks/pre-commit` | **Skipped** (defer to team rollout) |
| Phase 7 | Create `openspec/schemas/ai-customization-change/` custom schema | Complete (`169bdc7`) |
| Phase 8 | Add "How to Make Changes" section to `.ai-customizations/README.md` | Complete (`1b1a3ca`) |
| Phase 9 | Update `setup-ai-tools.sh` to auto-install hook via `core.hooksPath` | **Skipped** (defer to team rollout) |
| Phase 10 | End-to-end test with a real change via `/opsx:propose` | **Deferred** |
| Phase 11 | Update roadmap status to Complete | Not started |

---

## Key Technical Decisions

### Derived File Header Formats

Different formats are required per tool:

- **HTML comment** (`<!-- ... -->`) — used in `.github/copilot-instructions.md` and all `.github/instructions/*.instructions.md` files (after YAML frontmatter if present)
- **Markdown comment** (`[//]: # (...)`) — used in `.clinerules` (Roo does not support HTML comments at file root)

### BSD sed Incompatibility

macOS sed does not support the `:a; N; ba` label/branch syntax for multi-line patterns. The validation script uses portable `awk` instead:

```bash
strip_html_blocks='BEGIN{skip=0} /^<!-- ===/{ skip=1 } skip && /-->$/{ skip=0; next } skip{ next } 1'
```

This strips multi-line `DERIVED FILE` header blocks before diffing paired files.

### `sync-ai-customizations.sh` — Not Yet Created

Phase 4 (creating the sync script) was skipped. Derived files are currently regenerated manually by the AI agent during an `/opsx:apply` cycle. The sync script is the largest remaining gap in the governance system. It should be created before sharing the system with a team.

---

## Validation Script — 32 Checks

The `scripts/validate-ai-customizations.sh` runs 32 checks in 7 sections:

| Section | Checks |
|---|---|
| File Existence | 10 checks — all canonical, derived, and paired files exist |
| YAML Frontmatter | 3 checks — `.instructions.md` files have valid frontmatter with `applyTo` |
| Paired File Sync | 2 checks — paired methodology files are in sync |
| Key Rule Presence | 6 checks — critical rules present in both `.clinerules` and `copilot-instructions.md` |
| Derived File Headers | 5 checks — all 5 derived files have `DERIVED FILE` header |
| Symlink Health | 3 checks — Roo symlinks valid, VS Code prompts linked |
| OpenSpec Checks | 3 checks — `openspec/config.yaml` exists, Copilot slash commands installed, governance spec exists |

---

## Roo Code Integration

Roo Code loads AI customizations via symlinks created by `setup-ai-tools.sh`:

```
~/.config/roo/ai-customizations  →  <workspace>/.ai-customizations/
~/.config/roo/modes.yaml          →  <workspace>/.ai-customizations/modes.yaml
```

This means the canonical hub in this workspace is the live source for ALL Roo instances on this machine. No duplication, no drift.

---

## OpenSpec Global Config

```
Package:    @fission-ai/openspec@1.3.1
Install:    npm install -g @fission-ai/openspec@1.3.1
Profile:    core
Delivery:   both
Config:     ~/.config/openspec/config.json
Workflows:  propose, explore, apply, archive
```
