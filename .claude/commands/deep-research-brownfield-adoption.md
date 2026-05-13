---
name: "Deep Research Brownfield Adoption"
description: Deep research prompt for OpenSpec brownfield adoption — covers discovery methodology, instruction consolidation patterns, and migration strategy for workspaces with existing AI instruction files.
category: Workflow
tags: [workflow]
---

# OpenSpec Brownfield Adoption: Deep Research

Use this prompt when you need to go deeper on brownfield-specific challenges beyond what `GREENFIELD-VS-BROWNFIELD.md` covers. This is most useful when:

- You have a complex existing instruction ecosystem to audit (many files, multiple tools, inconsistent conventions)
- You are unsure how to map an unusual existing toolchain into OpenSpec CUSTOMIZE files
- You are dealing with conflicting instructions across tool-native files
- You need to plan a phased migration that minimizes team disruption

---

## Research Questions to Investigate

Break your brownfield research into these sub-questions. Investigate each with evidence from the workspace.

### 1. What existing AI instructions are in place?

Search for all instruction files currently in use:

```bash
# Find all existing tool-native instruction files
find . -name "copilot-instructions.md" -o -name ".cursorrules" -o -name "*.cursorrules" \
       -o -name ".windsurfrules" -o -name "CLAUDE.md" -o -name "GEMINI.md" | grep -v ".openspec" | grep -v node_modules

# Find all Copilot prompt files
find .github/prompts/ -name "*.prompt.md" 2>/dev/null

# Find all Cursor rule files
find .cursor/rules/ -name "*.mdc" 2>/dev/null

# Find all Roo Code rules
find .roo/rules/ -name "*.md" 2>/dev/null

# Find slash commands and skills
find . \( -name "SKILL.md" -o -name "*.agent.md" \) | grep -v ".openspec" | grep -v node_modules
```

For each file found: read it, extract all rules and conventions, and classify them into:
- Domain knowledge (service names, data ownership, safety rules)
- Process rules (how to investigate, what order to run tools)
- Standards (naming conventions, document formats, review checklists)
- Tool commands (how to query JIRA, Splunk, GitHub, etc.)

### 2. What conventions exist but are not in any instruction file?

These are the hardest to find. Search documentation sources:

```bash
# Check README files for conventions
find . -name "README.md" | head -20

# Check onboarding docs
find . -path "*/docs/onboarding*" -o -path "*/docs/contributing*" -o -path "*/CONTRIBUTING.md"

# Check architecture standards
find . -path "*/architecture-standards/*" -name "*.md"

# Check existing ADRs for implicit standards
ls decisions/ADR-*.md 2>/dev/null || find . -name "ADR-*.md" | head -20
```

Read these files and extract any conventions the AI should know. Particularly look for:
- Folder structure rules (where things live, how they are named)
- Review process steps (what gates must be passed)
- Anti-patterns the team actively avoids
- Data or security constraints

### 3. What is the existing toolchain?

Identify the concrete commands for each tool the team uses:

| Category | Question | Where to Look |
|---------|---------|-------------|
| Ticketing | What system? What project key format? | `.env` files, CI scripts, existing prompts |
| Log platform | Splunk? Elastic? Datadog? CloudWatch? | `docker-compose.yml`, infra configs, existing prompts |
| Source control | GitHub? GitLab? ADO? Which org/project? | `git remote -v`, CI config |
| Internal CLIs | Any custom scripts that query internal systems? | `scripts/`, `Makefile`, `package.json` scripts |
| Architecture metadata | Any capability registries, service catalogs? | `architecture/metadata/`, `services/`, `infra/` |

### 4. What conflicts exist between existing instruction files?

If multiple tool-native instruction files exist, compare them:

- Does `.github/copilot-instructions.md` say something different from `.cursorrules`?
- Are there rules that contradict each other (e.g., one file says "always add types", another says "prefer inference")?
- Are there rules that are outdated (reference systems or processes that no longer exist)?

### 5. What is the migration risk?

Assess the risk of replacing existing instruction files with generator output:

- Are any existing prompt files used in CI or automated workflows? (If yes, deleting them breaks automation)
- Do any team members have local overrides or personal instruction files that depend on the current structure?
- Are there instructions that reference secrets or environment-specific values? (These cannot go in `.openspec/` as-is)

---

## Research Report Format

After investigating the above, produce:

```markdown
# OpenSpec Brownfield Discovery Report
*Workspace: [repo name] | Date: [YYYY-MM-DD]*

## Existing Instruction Ecosystem

### Files Found
| File | Lines | Key Content Summary |
|------|-------|-------------------|
| .github/copilot-instructions.md | N | [summary] |
| ... | | |

### Conventions Inventory
| Convention | Source File | Classification | Goes Into |
|-----------|------------|---------------|----------|
| [rule text] | [file] | Domain/Process/Standard/Tool | core-instructions / CUSTOMIZE prompt |

### Toolchain Map
| Tool | System | Example Command | CUSTOMIZE File |
|------|--------|----------------|---------------|
| Ticketing | [JIRA/ADO/Linear] | [command] | investigation.prompt.md |
| Logs | [Splunk/Elastic] | [command] | investigation.prompt.md |
| Source control | [GitHub/GitLab] | [command] | investigation.prompt.md |

### Conflicts Identified
| Conflict | File A | File B | Resolution |
|---------|--------|--------|-----------|

### Migration Risks
| Risk | Severity | Mitigation |
|------|---------|-----------|

## Migration Plan

### Phase 1: Consolidation (before running generator)
1. [Specific action: which file to read, what to extract, where it goes]
2. ...

### Phase 2: Generator run and reconciliation
1. Run `--dry-run` and list files that would change
2. For each changed file: [reconciliation action]

### Phase 3: Cutover
1. [When to delete old files]
2. [How to communicate to team]

### Phase 4: Validation
1. Verify gate 4 passes: `python3 scripts/generate-tool-instructions.py --check`
2. Test one proposal end-to-end to confirm AI uses new instructions correctly
3. [Any team-specific validation steps]

## Gaps and Unknowns
- [Convention or rule that could not be determined from available sources]
- [Assumption made due to missing data]
```

---

## When to Use External Research

If workspace evidence is insufficient to answer any of the above questions (e.g., the toolchain CLI commands are not documented anywhere in the repo), use `#deep-research` with web sources to find:

- Official API documentation for the toolchain (e.g., Jira REST API, Splunk search API)
- OpenSpec documentation at the project's official source
- Patterns for consolidating AI instruction files from the broader AI-assisted development community

Always cite external sources with URLs and retrieval date.
