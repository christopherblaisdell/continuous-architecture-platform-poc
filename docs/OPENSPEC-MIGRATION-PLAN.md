# OpenSpec Migration Plan

**Date**: 2026-05-11
**Status**: In Progress

This plan migrates the workspace AI instructions from GitHub Copilot-only native format to a dual-track system:

- **Track 1 — Workflow portability**: OpenSpec's `/opsx:*` slash commands installed per tool via `openspec init`
- **Track 2 — Content portability**: Canonical instruction content distributed to every tool's native format via a generator script

These two tracks are independent and complementary. Track 1 delivers workflow mechanics. Track 2 delivers architecture domain rules.

---

## Current State

### Canonical Instruction Files (Hub)

| File | Scope | Contents |
|------|-------|----------|
| `.github/copilot-instructions.md` | Global — all files | Full Solution Architect persona: EaC blueprint constraint, data isolation, role definition, NovaTrek domain model, mock tools, solution design workflow, architecture standards, document formatting, portal deployment |
| `.github/instructions/github-urls.instructions.md` | Global — all files | GitHub URL formatting rules (correct paths, no spurious fragments) |
| `.github/instructions/prompt-me.instructions.md` | Global — all files | Interactive decision-loop workflow (lettered options, one step at a time) |
| `architecture/.instructions.md` | `architecture/**` | Security context: data ownership boundaries, identity resolution, safety defaults, API contract security, prior art discovery |
| `architecture/solutions/.instructions.md` | `architecture/solutions/**` | Prior-art discovery, architecture review checklist, trade-off documentation, solution decomposition layers, anti-pattern detection, capability rollup |
| `architecture/specs/.instructions.md` | `architecture/specs/**` | OpenAPI design rules: resource naming, HTTP methods/status codes, schema completeness checklist, backward compatibility, pagination, NovaTrek-specific patterns |

### Current Tool Coverage

| Tool | Global Instructions | Path-Scoped Instructions |
|------|--------------------|-----------------------------|
| GitHub Copilot | `.github/copilot-instructions.md` + `.github/instructions/*.instructions.md` | `architecture/*.instructions.md` |
| Cursor | None | None |
| RooCode | None | None |
| Windsurf | None | None |
| Claude Code | None | None |
| Gemini CLI | None | None |

---

## Track 1 — OpenSpec Workflow Portability

OpenSpec installs its own workflow mechanics (`/opsx:propose`, `/opsx:apply`, `/opsx:archive`) into each tool's native directory. This is separate from instruction content — it delivers the change-governance workflow.

### What `openspec init` generates

| Tool | Generated File Location |
|------|------------------------|
| GitHub Copilot | `.github/skills/openspec-*/SKILL.md` + `.github/prompts/opsx-*.prompt.md` |
| Cursor | `.cursor/skills/` + `.cursor/commands/` |
| RooCode | `.roo/skills/` + `.roo/commands/` |
| Windsurf | `.windsurf/skills/` + `.windsurf/commands/` |
| Claude Code | `~/.claude/skills/` or local `.claude/` directory |
| Gemini CLI | Local Gemini skills directory |

### Steps

1. Install OpenSpec globally: `npm install -g @fission-ai/openspec@latest`
2. Run init for target tools: `openspec init --tools copilot,cursor,roocode,windsurf,claude,gemini`
3. Review generated files — verify no conflicts with existing `.github/` instruction files
4. Commit all generated OpenSpec files

### Conflict Risk: GitHub Copilot

OpenSpec generates files under `.github/skills/` and `.github/prompts/`. This workspace already has `.github/copilot-instructions.md` and `.github/instructions/*.instructions.md`. These are different paths — no direct conflict expected — but the generated prompt files must be reviewed to confirm they do not contradict or duplicate the existing instructions.

---

## Track 2 — Content Portability (Hub-and-Spoke Distribution)

The canonical hub (`.github/copilot-instructions.md` + scoped `.instructions.md` files) must be derived into each tool's native format. A generator script reads the canonical sources and writes the per-tool files.

### Target File Map

#### Global Instructions (all-files scope)

| Source | Cursor | RooCode | Windsurf | Claude Code | Gemini CLI |
|--------|--------|---------|----------|-------------|------------|
| `.github/copilot-instructions.md` | `.cursor/rules/novatrek-architecture.mdc` | `.roo/rules/novatrek-architecture.md` | `.windsurfrules` (section) | `CLAUDE.md` (section) | `GEMINI.md` (section) |
| `.github/instructions/github-urls.instructions.md` | `.cursor/rules/github-urls.mdc` | `.roo/rules/github-urls.md` | `.windsurfrules` (append) | `CLAUDE.md` (append) | `GEMINI.md` (append) |
| `.github/instructions/prompt-me.instructions.md` | `.cursor/rules/prompt-me.mdc` | `.roo/rules/prompt-me.md` | `.windsurfrules` (append) | `CLAUDE.md` (append) | `GEMINI.md` (append) |

#### Path-Scoped Instructions

| Source | Copilot native scope | Cursor | RooCode | Windsurf | Claude/Gemini |
|--------|----------------------|--------|---------|----------|---------------|
| `architecture/.instructions.md` | `architecture/**` | `.cursor/rules/architecture-context.mdc` (globs: `architecture/**`) | `.roo/rules/architecture-context.md` | Not natively supported — merged into root file | Not natively supported — merged into root file |
| `architecture/solutions/.instructions.md` | `architecture/solutions/**` | `.cursor/rules/architecture-solutions.mdc` (globs: `architecture/solutions/**`) | `.roo/rules/architecture-solutions.md` | Merged into root file | Merged into root file |
| `architecture/specs/.instructions.md` | `architecture/specs/**` | `.cursor/rules/architecture-specs.mdc` (globs: `architecture/specs/**`) | `.roo/rules/architecture-specs.md` | Merged into root file | Merged into root file |

### Format Specifications by Tool

#### Cursor (`.cursor/rules/*.mdc`)

Cursor rules use YAML frontmatter followed by markdown content:

```yaml
---
description: "Brief description shown in Cursor's rule picker"
globs: "path/pattern/**"        # omit for always-apply rules
alwaysApply: true               # true for global rules; false for path-scoped
---

# Rule content here (markdown)
```

- Global rules (no path restriction): `alwaysApply: true`, no `globs`
- Path-scoped rules: `alwaysApply: false`, `globs: "architecture/**"`
- One file per source instruction file — do not merge into a single giant file
- Filename convention: kebab-case, descriptive

#### RooCode (`.roo/rules/*.md`)

RooCode supports multiple rule files under `.roo/rules/`. Plain markdown, no frontmatter.

- One file per source instruction file
- RooCode applies all files in the directory globally — path-scoping is not natively supported; note the scope intent in a comment at the top of the file
- Filename convention: matches Cursor convention for consistency

#### Windsurf (`.windsurfrules`)

Single file at the workspace root. Plain markdown. No frontmatter. All rules merged into one file with clear section headers.

Structure:
```markdown
# NovaTrek Architecture Platform — AI Instructions

## Core Architecture Instructions
[content from copilot-instructions.md]

---

## GitHub URL Formatting Rules
[content from github-urls.instructions.md]

---

## Prompt Me — Interactive Decision Loop
[content from prompt-me.instructions.md]

---

## Path-Scoped: architecture/** — Security Context
> Note: These rules apply when working in the `architecture/` directory.
[content from architecture/.instructions.md]

---

## Path-Scoped: architecture/solutions/** — Solution Design
> Note: These rules apply when working in `architecture/solutions/`.
[content from architecture/solutions/.instructions.md]

---

## Path-Scoped: architecture/specs/** — OpenAPI Rules
> Note: These rules apply when working in `architecture/specs/`.
[content from architecture/specs/.instructions.md]
```

#### Claude Code (`CLAUDE.md`)

Single `CLAUDE.md` at workspace root. Same structure as Windsurf. Plain markdown.

Claude Code reads `CLAUDE.md` automatically when present. No frontmatter required.

#### Gemini CLI (`GEMINI.md`)

Single `GEMINI.md` at workspace root. Same structure as Windsurf and Claude. Plain markdown.

---

## Generator Script

**Location**: `scripts/generate-tool-instructions.py`

**Purpose**: Reads the canonical hub files and writes derived per-tool instruction files. Idempotent — safe to run repeatedly.

### Script Design

```
MANIFEST (inline config in script):
  - source: .github/copilot-instructions.md
    targets:
      cursor: .cursor/rules/novatrek-architecture.mdc
        frontmatter: { alwaysApply: true, description: "NovaTrek Solution Architect instructions" }
      roocode: .roo/rules/novatrek-architecture.md
      windsurf: .windsurfrules (section: "Core Architecture Instructions")
      claude: CLAUDE.md (section: "Core Architecture Instructions")
      gemini: GEMINI.md (section: "Core Architecture Instructions")

  - source: .github/instructions/github-urls.instructions.md
    targets:
      cursor: .cursor/rules/github-urls.mdc
        frontmatter: { alwaysApply: true, description: "GitHub URL formatting rules" }
      roocode: .roo/rules/github-urls.md
      windsurf: .windsurfrules (append section)
      claude: CLAUDE.md (append section)
      gemini: GEMINI.md (append section)

  - source: .github/instructions/prompt-me.instructions.md
    targets: (same pattern)

  - source: architecture/.instructions.md
    targets:
      cursor: .cursor/rules/architecture-context.mdc
        frontmatter: { alwaysApply: false, globs: "architecture/**", description: "..." }
      roocode: .roo/rules/architecture-context.md
      windsurf: .windsurfrules (append section with path note)
      claude: CLAUDE.md (append section with path note)
      gemini: GEMINI.md (append section with path note)

  - source: architecture/solutions/.instructions.md
    targets: (same pattern, globs: "architecture/solutions/**")

  - source: architecture/specs/.instructions.md
    targets: (same pattern, globs: "architecture/specs/**")
```

### Transformations Applied

| Transformation | When |
|---------------|------|
| Strip existing frontmatter from source | Source `.instructions.md` files have YAML frontmatter — remove it before embedding |
| Inject Cursor frontmatter | For all `.mdc` targets — add description, globs, alwaysApply |
| Merge into single file | For Windsurf, Claude, Gemini — concatenate sections with `---` separators and `## Section Name` headers |
| Add path-scope note | For path-scoped rules in single-file targets — prepend `> Note: applies when working in X directory` |
| Strip `.github/copilot-instructions.md` header | The main file's H1 is workspace-specific — keep it |

### Running the Script

```bash
# Generate all tool instruction files
python3 scripts/generate-tool-instructions.py

# Dry-run (print what would be written, no file changes)
python3 scripts/generate-tool-instructions.py --dry-run

# Generate for a specific tool only
python3 scripts/generate-tool-instructions.py --tool cursor
```

---

## CI / Maintenance Automation

### Pre-Commit Hook (`.githooks/pre-commit`)

Run the generator before every commit and fail if generated files are out of sync with sources:

```bash
#!/bin/bash
python3 scripts/generate-tool-instructions.py --dry-run --check
if [ $? -ne 0 ]; then
  echo "ERROR: Tool instruction files are out of sync. Run: python3 scripts/generate-tool-instructions.py"
  exit 1
fi
```

Activate: `git config core.hooksPath .githooks`

### GitHub Actions (`.github/workflows/validate-instructions.yml`)

Run on every PR that touches any source instruction file:

```yaml
on:
  pull_request:
    paths:
      - '.github/copilot-instructions.md'
      - '.github/instructions/**'
      - 'architecture/**/.instructions.md'
      - 'architecture/.instructions.md'
```

Job: Run `python3 scripts/generate-tool-instructions.py --check` and fail if drift detected.

---

## Implementation Sequence

| Step | Action | Track | Deliverable |
|------|--------|-------|-------------|
| 1 | Confirm target tools | Both | Decision recorded in this document |
| 2 | Install OpenSpec | 1 | `openspec` available on PATH |
| 3 | Run `openspec init` | 1 | Per-tool workflow files generated |
| 4 | Review OpenSpec files for conflicts | 1 | Sign-off or conflict resolution |
| 5 | Commit OpenSpec files | 1 | Committed + pushed |
| 6 | Write generator script | 2 | `scripts/generate-tool-instructions.py` |
| 7 | Generate Cursor `.mdc` files | 2 | `.cursor/rules/*.mdc` |
| 8 | Generate RooCode rule files | 2 | `.roo/rules/*.md` |
| 9 | Generate Windsurf `.windsurfrules` | 2 | `.windsurfrules` |
| 10 | Generate Claude `CLAUDE.md` | 2 | `CLAUDE.md` |
| 11 | Generate Gemini `GEMINI.md` | 2 | `GEMINI.md` |
| 12 | Review all generated content | 2 | Sign-off |
| 13 | Write pre-commit hook | 2 | `.githooks/pre-commit` |
| 14 | Write GitHub Actions workflow | 2 | `.github/workflows/validate-instructions.yml` |
| 15 | Commit all content portability files | 2 | Committed + pushed |

---

## Decisions

| Step | Decision | Choice | Date |
|------|----------|--------|------|
| 1 | Target tools | A — All six: Copilot, Cursor, RooCode, Windsurf, Claude Code, Gemini CLI | 2026-05-11 |

## Decisions Deferred to Prompt-Me Loop

- Whether to write the generator script manually or generate the files statically (Step 6 scope)
- Whether to include the pre-commit hook (Step 13)
- Whether to include the GitHub Actions workflow (Step 14)
