# OpenSpec AI Customization Blueprint — Migration Guide

This is the bootstrap guide for setting up the OpenSpec AI customization system in any workspace. Follow these steps to replicate the hub-and-spoke AI instruction architecture — where `.openspec/` is the single source of truth and all AI tool-native directories are generated outputs — in a new corporate workspace.

**Source workspace (this synthetic reference):** `$SOURCE_WORKSPACE`
**Target workspace (corporate):** `$TARGET_WORKSPACE`

---

## How This System Works

```
.openspec/                   ← Single source of truth (you own and edit this)
├── instructions/            ← AI behavior rules, globally applied or path-scoped
├── prompts/                 ← Slash commands / prompt templates
├── agents/                  ← AI agent persona definitions
└── skills/                  ← Reusable skill packages (one subdirectory per skill)

scripts/generate-tool-instructions.py   ← Generator script (distributes .openspec/ to all tools)

Generated outputs (never edit directly):
├── .github/                 ← GitHub Copilot native format
├── .cursor/                 ← Cursor native format
├── .roo/                    ← Roo Code native format
├── .windsurfrules           ← Windsurf native format (single file)
├── CLAUDE.md                ← Claude Code native format
├── GEMINI.md                ← Gemini CLI native format
└── .foundry/                ← Azure AI Foundry native format
```

When you modify a file in `.openspec/`, run the generator to propagate the change to all tool-native output directories. This ensures every AI tool gets the same instructions without maintaining separate copies.

---

## Prerequisites

- Python 3.9 or later (`python3 --version`)
- Node.js 18 or later — any installation method works (`node --version`)
- Git
- Access to the source workspace: `$SOURCE_WORKSPACE`

---

## Step 1: Declare Path Variables

```bash
export SOURCE_WORKSPACE="/path/to/continuous-architecture-platform-poc-2"
export TARGET_WORKSPACE="/path/to/your-corporate-workspace"
```

Set these once and use them in all subsequent copy commands. Adjust paths to match your actual directories.

---

## Step 2: Copy Source Files

Copy the three required elements: the `.openspec/` source directory, the generator script, and the CI validation workflow.

```bash
# .openspec/ source directory (the hub)
cp -r "$SOURCE_WORKSPACE/.openspec" "$TARGET_WORKSPACE/"

# Generator script (the distribution engine)
mkdir -p "$TARGET_WORKSPACE/scripts"
cp "$SOURCE_WORKSPACE/scripts/generate-tool-instructions.py" "$TARGET_WORKSPACE/scripts/"

# CI validation workflow
mkdir -p "$TARGET_WORKSPACE/.github/workflows"
cp "$SOURCE_WORKSPACE/.github/workflows/validate-instructions.yml" "$TARGET_WORKSPACE/.github/workflows/"
```

The generator uses `ROOT = Path(__file__).parent.parent` to locate the workspace root, so it **must** remain at `scripts/generate-tool-instructions.py` — one directory level below the workspace root.

---

## Step 3: Install the openspec CLI

```bash
npm install -g openspec@1.3.1
openspec --version   # expect: 1.3.1
```

Node.js 18 or later is required. Use nvm, fnm, or your system package manager — any installation method works.

---

## Step 4: Configure the openspec CLI

The CLI stores global configuration at `~/.config/openspec/config.json`. Run these commands to establish the correct profile:

```bash
openspec config set profile custom
openspec config set delivery both
openspec config set workflows propose,explore,apply,archive
```

Verify:

```bash
openspec config list
# Expected output:
# profile: custom
# delivery: both
# workflows: propose,explore,apply,archive
```

---

## Step 5: Initialize the openspec Workspace

Create the `openspec/` workspace directory that the CLI uses to track active changes:

```bash
cd "$TARGET_WORKSPACE"
openspec init
```

If `openspec init` is unavailable or produces errors, create the structure manually:

```bash
mkdir -p openspec/changes/archive
mkdir -p openspec/specs
```

The `openspec/` workspace directory is separate from `.openspec/` (the source of truth). The `openspec/` directory tracks active change drafts and is created at the workspace root.

---

## Step 6: Customize Instructions for Your Domain

The `.openspec/` files you copied contain NovaTrek Adventures content (a synthetic architecture workspace). Before running the generator, replace or customize the domain-specific content with your organization's context.

### 6.1 File Classification

| File | Classification | Action |
|------|---------------|--------|
| `instructions/core-instructions.md` | REPLACE | Rewrite entirely for your domain |
| `instructions/architecture.instructions.md` | REPLACE | Rewrite security context for your architecture directory |
| `instructions/architecture-solutions.instructions.md` | REPLACE | Rewrite solution design workflow for your practice |
| `instructions/architecture-specs.instructions.md` | REPLACE | Rewrite API/contract design rules for your standards |
| `agents/novatrek-solution-architect.agent.md` | REPLACE | Rename file, rewrite persona for your domain role |
| `prompts/investigation.prompt.md` | CUSTOMIZE | Swap mock tool commands for your corporate tools |
| `prompts/architecture-review.prompt.md` | CUSTOMIZE | Replace NovaTrek service names with your system names |
| `prompts/security-review.prompt.md` | CUSTOMIZE | Replace data ownership rules with your policies |
| `prompts/solution-verification.prompt.md` | CUSTOMIZE | Replace folder paths with your solution structure |
| `instructions/github-urls.instructions.md` | KEEP | Generic; copy verbatim |
| `instructions/prompt-me.instructions.md` | KEEP | Generic; copy verbatim |
| `instructions/prompt-me-copyable.md` | KEEP | Generic; copy verbatim |
| `prompts/deep-research.prompt.md` | KEEP | Generic; copy verbatim |
| `prompts/opsx-propose.prompt.md` | KEEP | Generic; copy verbatim |
| `prompts/opsx-apply.prompt.md` | KEEP | Generic; copy verbatim |
| `prompts/opsx-explore.prompt.md` | KEEP | Generic; copy verbatim |
| `prompts/opsx-archive.prompt.md` | KEEP | Generic; copy verbatim |
| `prompts/bootstrap-instance.prompt.md` | KEEP | Generic bootstrap workflow; copy verbatim |
| `skills/openspec-propose/SKILL.md` | KEEP | Generic; copy verbatim |
| `skills/openspec-apply-change/SKILL.md` | KEEP | Generic; copy verbatim |
| `skills/openspec-archive-change/SKILL.md` | KEEP | Generic; copy verbatim |
| `skills/openspec-explore/SKILL.md` | KEEP | Generic; copy verbatim |

### 6.2 REPLACE Files — Template Stubs

For each REPLACE file, delete the NovaTrek content and write your own using the structure below.

---

**`.openspec/instructions/core-instructions.md`**

This is the primary AI persona file — the largest and most important file to replace. It has no frontmatter; GitHub Copilot uses it as the root instruction file, and the generator appends its content as the first section of `CLAUDE.md`, `GEMINI.md`, and `.windsurfrules`.

```markdown
# [Your Role Title]

## [Your Domain] — READ FIRST

[Opening constraint or data isolation rule that the AI must internalize before anything else.
Example: "This workspace contains ZERO corporate data. Everything is synthetic."]

---

## Role Definition: [Role Title]

You operate as a **[Role Title]** for [Your Organization]. Your responsibilities are:

- [Responsibility 1]
- [Responsibility 2]
- [Responsibility 3]

You **DO NOT**:
- [Excluded activity 1]
- [Excluded activity 2]

---

## [Your Domain] Domain Model

### [Component Groups or Service Domains]

| Group | Components | Owner |
|-------|-----------|-------|
| [group] | [component1, component2] | [team] |

### Boundary Rules

- [Rule 1 — how components communicate across boundaries]
- [Rule 2 — what is prohibited]

### Data Ownership Boundaries

| Data Entity | Owning Component | Read Access |
|-------------|-----------------|-------------|
| [entity] | [owner] | [who can access] |

---

## Tool Usage

[If your workspace uses local mock tools, CLI scripts, or data tools, document the commands here.
Include: tool purpose, exact command, when to use, and the order to run them.]

---

## Solution Design Workflow

[Document your branching convention, solution folder structure, and any required artifact rollup steps.]

---

## Architecture Standards

[Document naming conventions, diagram standards (e.g., C4, arc42), decision record format (e.g., MADR), quality model (e.g., ISO 25010).]

---

## Document Formatting Rules

1. [Style rule 1]
2. [Style rule 2]
3. [Evidence requirement — cite file paths and line numbers]

---

## AI Workflow Patterns

### Search-First Principle

Before creating new designs or documentation, search for existing solutions:

1. [Where to look first]
2. [Where to look second]

### Research Mode

- [Read what before concluding]
- [How to form and verify hypotheses]
- [How to acknowledge gaps without fabricating data]

---

## Interaction Style

- Be direct and concise
- Lead with findings, not process descriptions
- State assumptions explicitly rather than asking for clarification
- Prioritize accuracy over comprehensiveness
```

---

**`.openspec/instructions/architecture.instructions.md`**

Path-scoped to your architecture directory (e.g., `architecture/**`). No frontmatter required — Copilot discovers this via its location at `architecture/.instructions.md`; Cursor and Roo Code scope it via globs; CLAUDE.md and GEMINI.md receive it as a labeled section.

```markdown
## [Domain Area] Security Context

> Note: These rules apply when working in the `[your-architecture-dir]/` directory.

### Data Ownership Boundaries

[List which systems own which data. Define what API-mediated access means here.
Name the metadata file or registry that defines the allowed integration map.]

### Identity Resolution

[Define the authoritative identity source. State explicitly that shadow records are prohibited.
Name the service or system that owns identity.]

### Safety Defaults

[Define safety-critical defaults. What must never fail silently?
Example pattern: unknown inputs MUST default to the highest safety level.]

### API Contract Security

When reviewing or proposing contract changes in this directory:
- [Validation rule 1 — e.g., all fields must have types and descriptions]
- [Validation rule 2 — backward compatibility requirement]
- [Validation rule 3 — what must not leak in error responses]

### Prior Art Discovery

Before creating a new solution, always:
1. [Search step 1 — e.g., check capability history with a CLI command]
2. [Search step 2 — e.g., review the changelog for overlapping changes]
3. [Search step 3 — e.g., read constraining ADRs before proposing decisions]
```

---

**`.openspec/instructions/architecture-solutions.instructions.md`**

Path-scoped to your solution designs directory (e.g., `architecture/solutions/**`). No frontmatter required.

```markdown
# Solution Design Instructions

When working in this directory, follow the architecture review process for every solution design.

## Prior-Art Discovery (Always Do First)

Before creating or modifying a solution design:

1. [Your prior-art search step 1 — what CLI/search to run]
2. [Your prior-art search step 2 — what files to read]
3. [Your prior-art search step 3 — what changelog or registry to check]

Do not skip prior-art discovery. Duplicate or conflicting changes break the architecture model.

## Architecture Review Checklist

- [ ] All data sourced from [your authoritative sources] (no fabrication)
- [ ] Every affected component identified with specific API/schema changes
- [ ] Decision records created for decisions that cross component boundaries
- [ ] At least 2 genuine options considered in each decision (not straw-man alternatives)
- [ ] Impact assessments focus on WHAT changes (not HOW to implement)
- [ ] [Your quality gate — e.g., ISO 25010 attributes assessed]
- [ ] Data ownership boundaries respected
- [ ] Backward compatibility addressed for all contract changes

## Trade-Off Documentation

For every architectural decision, document:
- Pros: concrete benefits tied to decision drivers
- Cons: honest drawbacks — do not minimize or omit
- Alternatives: at least one genuine alternative with fair analysis
- Decision: final choice with rationale tied to decision drivers

## Solution Decomposition

| Layer | Contains | Does NOT Contain |
|-------|----------|-----------------|
| Requirements | Business context, ticket report | Technical solutions |
| Analysis | Plain-language explanation | Jargon, API details |
| Assumptions | What is assumed true but not verified | Decisions |
| Capabilities | Descriptive summary referencing changelog | Duplicate capability data |
| Decisions | Decision records with options analysis | Implementation code |
| Guidance | HOW to implement — patterns, migration steps | Business justification |
| Impacts | WHAT changes — contracts, data models | Timelines, code |
| Risks | Risk register with likelihood and mitigation | Solved problems |
| User Stories | WHO benefits and WHY — acceptance criteria | Technical details |

## Anti-Pattern Detection

Flag these patterns in any solution design:

- [Anti-pattern 1]: [description] — Recommended alternative: [solution]
- [Anti-pattern 2]: [description] — Recommended alternative: [solution]
- [Anti-pattern 3]: [description] — Recommended alternative: [solution]
```

---

**`.openspec/instructions/architecture-specs.instructions.md`**

Path-scoped to your API contract files directory (e.g., `architecture/specs/**`). No frontmatter required.

```markdown
## [Your API/Contract Area] Design Rules

When creating or modifying [contract files] in this directory, follow these design patterns:

### Resource Naming

- [Naming convention 1 — e.g., nouns, plural, lowercase, kebab-case]
- [Naming convention 2 — sub-resources for relationships]
- [Naming convention 3 — query parameter conventions]

### HTTP Methods and Status Codes

| Method | Use For | Success Code |
|--------|---------|-------------|
| GET | Retrieve resources | 200 OK |
| POST | Create resources | 201 Created |
| PATCH | Partial update | 200 OK |
| DELETE | Remove resource | 204 No Content |

Error codes: 400 (validation), 401 (unauthenticated), 403 (unauthorized), 404 (not found),
409 (conflict), 422 (unprocessable), 500 (server error)

### Schema Completeness Checklist

For every schema in a contract, verify:
- [ ] All fields have `type` specified
- [ ] All fields have `description` with business meaning
- [ ] Nullable fields have null semantics documented
- [ ] Enum fields use validated domain values
- [ ] Required vs optional fields are correctly annotated
- [ ] Date fields use ISO 8601 format

### Backward Compatibility

When modifying an existing contract:
- Adding a new optional field: safe
- Adding a new required field: BREAKING — existing consumers will fail
- Removing a field: BREAKING — deprecate first
- Changing a field type: BREAKING
```

---

**`agents/{your-agent-name}.agent.md`**

Rename the file from `novatrek-solution-architect.agent.md` to reflect your domain role (e.g., `platform-architect.agent.md`). The YAML frontmatter is the Claude Code native agent format; the generator propagates it to all other tools.

```markdown
---
name: "[Your Agent Name]"
description: "[One sentence: what this agent does and when to use it. This appears in agent pickers and skill directories.]"
tools: [execute, read, edit, search, agent, web, todo]
model: "Claude Opus 4.6"
---

You are a **[Role Title]** for **[Your Organization/Domain]**.

## Core Identity

- [Communication style — e.g., direct, evidence-driven]
- [Priority rule — e.g., lead with findings, not process descriptions]
- [Evidence standard — e.g., cite workspace files with paths and line numbers]
- [Ambiguity rule — e.g., state assumptions explicitly rather than asking]

## Responsibilities

You DO:

- [Task 1]
- [Task 2]
- [Task 3]

You DO NOT:

- [Excluded task 1 — e.g., debug production code]
- [Excluded task 2 — e.g., deploy or configure infrastructure]

## Domain Knowledge

[Document the key domain concepts the agent must know:
- System names and their responsibilities
- Data ownership rules and boundary enforcement
- Safety-critical constraints
- Toolchain commands and the order to run them
- Architecture standards and required document formats]

## Interaction Style

- Be direct and concise
- Lead with findings, not process descriptions
- State assumptions explicitly rather than asking for clarification
- Prioritize accuracy over comprehensiveness
```

### 6.3 CUSTOMIZE Files — What to Update

These four prompts retain their structure but contain NovaTrek-specific references that must be replaced:

**`prompts/investigation.prompt.md`**

Replace:
- Mock tool commands (`python3 scripts/mock-jira-client.py`, `python3 scripts/mock-elastic-searcher.py`, `python3 scripts/mock-gitlab-client.py`) with your corporate tool access patterns (API clients, internal CLIs, or queries)
- The `NTK-XXXXX` ticket ID format with your ticketing system's format
- The three-phase investigation order (JIRA → Elastic → GitLab) with your toolchain's sequence

**`prompts/architecture-review.prompt.md`**

Replace:
- NovaTrek service names (e.g., `svc-check-in`, `svc-reservations`) with your system or service names
- The NovaTrek domain classification table with your component or domain groups
- Anti-pattern examples that reference NovaTrek-specific patterns (e.g., shadow guest records, Pattern 3 default) with your domain's equivalent anti-patterns
- The ISO 25010 quality attribute table — keep this if applicable to your practice

**`prompts/security-review.prompt.md`**

Replace:
- Data ownership references (`svc-guest-profiles` as the identity source) with your identity system
- NovaTrek safety default rules (Pattern 3, ADR-005) with your domain's safety-critical defaults
- OWASP Top 10 references — keep these; they are generic
- Cross-service boundary rules with your actual component boundaries

**`prompts/solution-verification.prompt.md`**

Replace:
- Solution folder paths (`architecture/solutions/_NTK-XXXXX-*/`) with your solution folder structure
- Verification gates that reference NovaTrek-specific artifacts (capability changelog, tickets.yaml, portal generators) with your equivalent artifacts
- The NovaTrek ADR numbering convention with your decision record system

---

## Step 7: Run the Generator for the First Time

```bash
cd "$TARGET_WORKSPACE"
python3 scripts/generate-tool-instructions.py
```

The generator reads `.openspec/` and writes all tool-native output directories. This is idempotent — running it again produces the same output.

To preview changes without writing files:

```bash
python3 scripts/generate-tool-instructions.py --dry-run
```

To target a single tool during development:

```bash
python3 scripts/generate-tool-instructions.py --tool copilot
python3 scripts/generate-tool-instructions.py --tool cursor
python3 scripts/generate-tool-instructions.py --tool claude
```

---

## Step 8: Wire Up CI Validation

The copied `.github/workflows/validate-instructions.yml` runs `--check` mode on every pull request that touches instruction-related files. It fails if the generated outputs are out of sync with `.openspec/`.

Review the `paths:` trigger list and update it if your workspace uses different generated output locations:

```yaml
on:
  pull_request:
    paths:
      - ".github/copilot-instructions.md"
      - ".github/instructions/*.instructions.md"
      - "architecture/.instructions.md"           # update path if different
      - "architecture/solutions/.instructions.md" # update path if different
      - "architecture/specs/.instructions.md"     # update path if different
      - "scripts/generate-tool-instructions.py"
      - ".cursor/rules/**"
      - ".roo/rules/**"
      - ".windsurfrules"
      - "CLAUDE.md"
      - "GEMINI.md"
```

For non-GitHub CI platforms (GitLab CI, Azure DevOps, Bitbucket Pipelines), the equivalent step is:

```bash
pip install --upgrade pip   # if needed
python3 scripts/generate-tool-instructions.py --check
```

Exit code 0 means all generated outputs are in sync. Exit code 1 means one or more files are out of date and the pipeline should fail.

---

## Step 9: Verify the Setup

Complete each gate in order. All six must pass before committing.

```
[ ] Gate 1: openspec CLI installed
    openspec --version
    Expect: 1.3.1

[ ] Gate 2: Global config correct
    openspec config list
    Expect: profile: custom | delivery: both | workflows: propose,explore,apply,archive

[ ] Gate 3: openspec workspace directories exist
    ls openspec/changes/ openspec/specs/
    Expect: no "No such file" errors

[ ] Gate 4: Generator passes --check (all outputs in sync)
    python3 scripts/generate-tool-instructions.py --check
    Expect: exit code 0

[ ] Gate 5: All tool output directories present
    ls .github/ .cursor/ .roo/ .foundry/ && cat .windsurfrules | head -3 && cat CLAUDE.md | head -3
    Expect: directories exist, single-file targets have content

[ ] Gate 6: CI workflow present
    cat .github/workflows/validate-instructions.yml
    Expect: file exists with validate job
```

After all gates pass:

```bash
git add -A
git commit -m "chore: bootstrap OpenSpec AI customization system"
git push
```

---

## Appendix A: .openspec/ File Inventory

All 22 source files and their roles:

### instructions/ (7 files)

| File | Role | Classification | Distributed To |
|------|------|---------------|----------------|
| `core-instructions.md` | Primary AI persona; global instructions | REPLACE | All tools |
| `github-urls.instructions.md` | Generic GitHub URL formatting rules | KEEP | All tools |
| `prompt-me.instructions.md` | Interactive decision-loop workflow | KEEP | All tools |
| `prompt-me-copyable.md` | Copyable version of prompt-me | KEEP | Copilot only |
| `architecture.instructions.md` | Path-scoped: architecture directory | REPLACE | All tools |
| `architecture-solutions.instructions.md` | Path-scoped: solutions directory | REPLACE | All tools |
| `architecture-specs.instructions.md` | Path-scoped: API contracts directory | REPLACE | All tools |

### prompts/ (10 files)

| File | Role | Classification | Distributed To |
|------|------|---------------|----------------|
| `deep-research.prompt.md` | Generic multi-source research workflow | KEEP | All tools |
| `opsx-propose.prompt.md` | OpenSpec propose workflow | KEEP | All tools |
| `opsx-apply.prompt.md` | OpenSpec apply-change workflow | KEEP | All tools |
| `opsx-explore.prompt.md` | OpenSpec explore mode | KEEP | All tools |
| `opsx-archive.prompt.md` | OpenSpec archive-change workflow | KEEP | All tools |
| `investigation.prompt.md` | Domain-specific investigation workflow | CUSTOMIZE | All tools |
| `architecture-review.prompt.md` | Domain-specific architecture review | CUSTOMIZE | All tools |
| `security-review.prompt.md` | Domain-specific security review | CUSTOMIZE | All tools |
| `solution-verification.prompt.md` | Domain-specific solution verification | CUSTOMIZE | All tools |
| `bootstrap-instance.prompt.md` | Generic OpenSpec bootstrap workflow | KEEP | All tools |

### agents/ (1 file)

| File | Role | Classification | Distributed To |
|------|------|---------------|----------------|
| `{name}.agent.md` | AI agent persona definition | REPLACE | All tools |

### skills/ (4 subdirectories, one SKILL.md each)

| Directory | Role | Classification | Distributed To |
|-----------|------|---------------|----------------|
| `openspec-propose/` | Skill: propose a new change | KEEP | All tools |
| `openspec-apply-change/` | Skill: implement tasks from a change | KEEP | All tools |
| `openspec-archive-change/` | Skill: archive a completed change | KEEP | All tools |
| `openspec-explore/` | Skill: explore mode thinking partner | KEEP | All tools |

---

## Appendix B: Generator CLI Reference

**Script location:** `scripts/generate-tool-instructions.py`
**Python requirement:** 3.9 or later (stdlib only — no pip dependencies)

### Flags

| Flag | Effect |
|------|--------|
| *(no flags)* | Generate all tool outputs from `.openspec/` |
| `--dry-run` | Print what would be written without writing files |
| `--check` | Verify generated outputs are in sync; exit 1 if not |
| `--tool {name}` | Limit output to one tool only |

### Tool names for `--tool`

`copilot` `cursor` `roocode` `windsurf` `claude` `gemini` `foundry`

### --check mode

`--check` re-generates all outputs in memory and diffs against the files on disk. If any file would change, it exits 1 and prints which files are out of date. Use this in CI to enforce that `.openspec/` is always the source of truth.

### Single-file targets

Three tools receive all their instructions as a single concatenated file. The generator appends each MANIFEST entry as a titled section:

| Tool | File |
|------|------|
| Windsurf | `.windsurfrules` |
| Claude Code | `CLAUDE.md` |
| Gemini CLI | `GEMINI.md` |

### Path-scoped instructions in CLAUDE.md and GEMINI.md

When a MANIFEST entry has a `path_scope` (e.g., `architecture/**`), the generator inserts a note before the section content:

```
> Note: These rules apply when working in the `architecture/` directory.
```

---

## Appendix C: Per-Tool Output Directory Map

### GitHub Copilot

| Source type | Output location |
|------------|----------------|
| Core instructions | `.github/copilot-instructions.md` |
| Global instruction files | `.github/instructions/*.instructions.md` |
| Path-scoped instructions | `{path-scope-dir}/.instructions.md` |
| Prompts | `.github/prompts/*.prompt.md` |
| Agents | `.github/agents/*.agent.md` |
| Skills | `.github/skills/{name}/SKILL.md` |

### Cursor

| Source type | Output location |
|------------|----------------|
| Instructions (all) | `.cursor/rules/*.mdc` |
| Prompts | `.cursor/commands/*.prompt.md` |
| Agents | `.cursor/agents/*.agent.md` |
| Skills | `.cursor/skills/{name}/SKILL.md` |

### Roo Code

| Source type | Output location |
|------------|----------------|
| Instructions (all) | `.roo/rules/*.md` |
| Prompts | `.roo/commands/*.prompt.md` |
| Agents | `.roo/agents/*.agent.md` |
| Skills | `.roo/skills/{name}/SKILL.md` |

### Windsurf

| Source type | Output location |
|------------|----------------|
| Instructions (all) | `.windsurfrules` (single concatenated file) |
| Prompts | `.windsurf/workflows/*.prompt.md` |
| Agents | `.windsurf/agents/*.agent.md` |
| Skills | `.windsurf/skills/{name}/SKILL.md` |

### Claude Code

| Source type | Output location |
|------------|----------------|
| Instructions (all) | `CLAUDE.md` (single concatenated file) |
| Prompts | `.claude/commands/opsx/*.prompt.md` |
| Agents | `.claude/agents/*.agent.md` |
| Skills | `.claude/skills/{name}/SKILL.md` |

### Gemini CLI

| Source type | Output location |
|------------|----------------|
| Instructions (all) | `GEMINI.md` (single concatenated file) |
| Prompts | `.gemini/commands/opsx/*.prompt.md` |
| Agents | `.gemini/agents/*.agent.md` |
| Skills | `.gemini/skills/{name}/SKILL.md` |

### Azure AI Foundry

| Source type | Output location |
|------------|----------------|
| Instructions (combined) | `.foundry/system-prompt.md` |
| Prompts | `.foundry/prompts/*.prompt.md` |
| Agent config | `.foundry/agent.yaml`, `.foundry/agent-metadata.yaml` |
| Skills | Not distributed to Foundry |

---

## Appendix D: openspec CLI Workflow Commands

After setup, the openspec CLI provides four workflow commands. These operate on the `openspec/changes/` workspace directory.

| Command | What it does |
|---------|-------------|
| `openspec propose` | Create a new change: generates `proposal.md`, `design.md`, `tasks.md` |
| `openspec explore` | Enter explore mode: thinking partner for clarifying requirements |
| `openspec apply` | Implement tasks from an active change |
| `openspec archive` | Archive a completed change to `openspec/changes/archive/` |

These commands are also available as prompt slash commands (e.g., `/opsx-propose`, `/opsx-apply`) via the skills and prompts distributed by the generator.

The `/opsx-propose`, `/opsx-apply`, `/opsx-explore`, and `/opsx-archive` prompts in `.openspec/prompts/` are thin wrappers that invoke the corresponding skills in `.openspec/skills/`. The skills contain the full workflow logic.
