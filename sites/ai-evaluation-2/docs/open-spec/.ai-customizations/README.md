# AI Customizations Hub

This directory is the canonical source of truth for AI customizations used by **Roo Code** and other AI tools. The system uses a hub-and-spoke documentation pattern to maintain consistency across all AI modes while allowing mode-specific customizations.

## System Overview

### Hub-and-Spoke Architecture
- **Hub**: This README and `core-instructions.md` serve as central references
- **Spokes**: Specialized directories containing focused customization documents
- **Mode-Aware Loading**: Instructions load dynamically based on active mode

### Directory Structure

```
.ai-customizations/
├── README.md                     # This file - system overview
├── core-instructions.md          # Base instructions for ALL modes
├── INDEX.md                      # Searchable index of all customizations
├── modes.yaml                    # Roo global mode definitions (symlinked)
├── setup-ai-tools.sh             # One-time machine setup script
│
├── universal/                    # ALWAYS loaded for ALL modes
│   ├── corporate-standards.md    # No emojis, professional tone
│   ├── effort-estimation.md      # Component/endpoint complexity, not dollars
│   ├── markdown-formatting.md    # Header rules, formatting
│   ├── file-organization.md      # Directory standards
│   └── security-uptime-basic.md  # Basic security awareness
│
├── methodologies/                # Mode-aware loading
│   ├── 4-phase-investigation.md  # SA, Orchestrator, Ask
│   ├── ticket-classification.md  # SA, Orchestrator
│   ├── guided-plan-execution.md  # All modes (paired with .github/instructions/prompt-me)
│   ├── bdd-tdd-methodology.md    # Code, Debug, VS Code Plugin
│   ├── sequence-diagrams.md      # SA, Orchestrator
│   ├── plantuml-standards.md     # SA, Orchestrator, Code
│   └── architecture-backlog.md   # SA, Orchestrator
│
├── user-prompts/                 # VS Code user-level files (symlinked globally)
│   └── jira-extract.prompt.md    # JIRA ticket extraction prompt
│
├── standards/                    # Mode-aware loading
│   ├── testing-standards.md      # Code, Debug, VS Code Plugin
│   ├── impact-organization.md    # SA, Orchestrator
│   ├── email-writing.md          # SA, Orchestrator, Ask, Compliance
│   ├── component-hierarchy.md    # SA, Code
│   ├── documentation-dates.md    # Compliance, SA
│   ├── swagger-yaml-locations.md # SA, Code, Orchestrator
│   └── plantuml-diagram-locations.md # SA, Orchestrator, Code
│
├── mode-customizations/          # Mode-specific instructions
│   ├── all-modes.md             # References universal standards
│   ├── solution-architect.md
│   ├── code.md
│   ├── debug.md
│   ├── ask.md
│   ├── corporate-compliance.md
│   ├── vscode-plugin-dev.md
│   └── orchestrator.md
│
└── project-overrides/           # Project-specific customizations
    └── .gitkeep
```

## Key Principles

### 1. Universal Standards (All Modes)
Every mode MUST follow these core standards:
- Professional communication (no emojis)
- Effort estimation by component/endpoint complexity, never dollars
- Proper markdown formatting
- Consistent file organization
- Basic security awareness

### 2. Mode-Specific Customizations
Each mode loads only relevant instructions:
- Solution Architects get architecture patterns, not coding standards
- Developers get BDD/TDD methodology, not stakeholder communication
- Modes maintain clear role boundaries

### 3. Progressive Enhancement
- Start with universal standards
- Layer mode-specific customizations
- Apply project overrides last
- Maintain clear hierarchy

## Loading Order

1. **Universal Standards** - Always loaded first
2. **Mode Customizations** - Based on active mode
3. **Relevant Methodologies** - As specified by mode
4. **Applicable Standards** - Mode-appropriate only
5. **Project Overrides** - If present

## Mode Customization Matrix

| Standard/Feature | Solution Architect | Code | Debug | Compliance | VS Code Plugin | Orchestrator | Ask |
|-----------------|-------------------|------|-------|------------|----------------|--------------|-----|
| No Emojis/Professional | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Component Complexity | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 4-Phase Investigation | ✅ | ⚠️ | ⚠️ | ❌ | ❌ | ✅ | ✅ |
| BDD/TDD Methodology | ❌ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ |
| Architecture Patterns | ✅ | ⚠️ | ❌ | ❌ | ❌ | ✅ | ❌ |
| Email Writing | ✅ | ❌ | ❌ | ✅ | ❌ | ✅ | ✅ |
| Testing Standards | ❌ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ |

**Legend**: ✅ Full application | ⚠️ Awareness only | ❌ Not applicable

## Integration with VSFlow v5

All modes integrate with UDX VSFlow v5 for execution:
- JIRA ticket extraction and management
- GitLab merge request analysis
- Production Elasticsearch queries
- Confluence page operations
- Architecture artifact management

Roo provides intelligence and guidance, VSFlow provides execution.

## Usage

### For Mode Developers
1. Check `mode-customizations/[mode-name].md` for mode-specific rules
2. Review universal standards that apply to all modes
3. Load only relevant methodologies and standards
4. Respect the loading hierarchy

### For Project Teams
1. Create project-specific overrides in `project-overrides/`
2. Never modify core standards directly
3. Document why overrides are necessary
4. Maintain compatibility with universal standards

## How to Make Changes

**All changes to AI customizations go through OpenSpec — never by editing derived files directly.**

Files in this directory (`.ai-customizations/`) are the canonical source. Five derived files are
assembled from them. Editing derived files directly causes drift and will fail pre-commit validation.

### Canonical vs. Derived Files

| Canonical — edit via OpenSpec | Derived — updated by sync script only |
|---|---|
| `.ai-customizations/**` | `.clinerules` |
| | `.github/copilot-instructions.md` |
| | `.github/instructions/prompt-me.instructions.md` |
| | `.github/instructions/prompt-mirror.instructions.md` |
| | `.github/instructions/plantuml-svg.instructions.md` |

### Workflow

1. **Propose** — Run `/opsx:propose "description of what you want to change"`
   Use the `ai-customization-change` schema: `/opsx:propose --schema ai-customization-change "..."`
   OpenSpec creates `openspec/changes/<name>/` with proposal, specs, design, tasks.

2. **Review** — Review `proposal.md` and update `design.md` to identify which canonical files change.

3. **Apply** — Run `/opsx:apply`
   The AI executes `tasks.md`. The final task always runs
   `scripts/sync-ai-customizations.sh`, which updates all derived files atomically.

4. **Validate** — `scripts/validate-ai-customizations.sh` runs automatically (or manually).
   All checks must pass before committing.

5. **Archive** — Run `/opsx:archive` to move the change to the archive.

### Governance

This system is governed by `openspec/specs/ai-customization-governance/spec.md`.
Requirements REQ-GOV-001 through REQ-GOV-004 define the enforcement rules.

## Maintenance

### Adding New Standards
1. Determine if universal or mode-specific
2. Create appropriately named file in `.ai-customizations/`
3. Update relevant mode customization files
4. Update this README's matrix
5. Propose the change via `/opsx:propose --schema ai-customization-change "..."`

### Updating Existing Standards
1. Propose the change via `/opsx:propose --schema ai-customization-change "..."`
2. Edit the canonical file(s) in `.ai-customizations/` as directed by `design.md`
3. Run `scripts/sync-ai-customizations.sh` to propagate changes
4. Validate with `scripts/validate-ai-customizations.sh` — Errors must be 0

## Key Prohibitions

### Universal (All Modes)
- ❌ No emojis in any output
- ❌ No dollar-based estimates
- ❌ No special characters in markdown headers
- ❌ No unvalidated claims or metrics

### Mode-Specific
- Solution Architects: ❌ No implementation code
- Developers: ❌ No architecture decisions
- All modes: ❌ No crossing role boundaries

## Support

For questions or issues with AI customizations:
1. Check mode-specific documentation first
2. Review universal standards
3. Consult project overrides if applicable
4. Contact architecture team for clarifications

## Cross-Tool File Map

Each customization has one canonical source and is delivered to each tool via its native mechanism.

| Canonical Source | Instruction File | Roo Sees Via |
|---|---|---|
| `core-instructions.md` + `universal/*` | `.github/copilot-instructions.md` (auto-loaded) | `.clinerules` (auto-loaded) |
| `methodologies/guided-plan-execution.md` | `.github/instructions/prompt-me.instructions.md` (auto-loaded, paired copy) | Symlinked via `~/.config/roo/ai-customizations/` |
| `user-prompts/jira-extract.prompt.md` | Symlinked to `~/Library/.../Code/User/prompts/` | Roo skill at `~/.roo/skills/jira-extraction` (from `shared-ai-customizations/`) |
| `modes.yaml` | N/A (VS Code has no modes) | Symlinked to `~/.config/roo/modes.yaml` |

### Paired Files

Files that must stay in sync (validated by `scripts/validate-ai-customizations.sh`):

| File A | File B | Why |
|---|---|---|
| `.github/copilot-instructions.md` | `.clinerules` | Same universal standards, different auto-load paths |
| `.github/instructions/prompt-me.instructions.md` | `.ai-customizations/methodologies/guided-plan-execution.md` | Same workflow, different auto-load paths |

### Drift Prevention

- **Pre-commit hook**: Automatically runs `scripts/validate-ai-customizations.sh` when any AI customization file is staged
- **Paired file headers**: Each paired file has a comment linking to its counterpart
- **Validation checks**: File existence, frontmatter validity, content sync, key rule presence, symlink health

---

*This customization system ensures consistent, professional AI assistance across all tools while maintaining appropriate role boundaries and enterprise standards.*