# OpenSpec Customization Guide

<!-- PUBLISH -->

OpenSpec is a spec-driven development workflow framework for AI coding agents, created by Fission AI. It structures AI-assisted change work using folder-based artifacts, YAML dependency schemas, behavioral specifications, and slash commands. This guide covers how OpenSpec works, its file structure, capabilities, and limitations.

For how GitHub Copilot's native customization system works, see [GitHub Copilot Customization Guide](github-copilot-customization-guide.md). For a side-by-side comparison and recommendation, see [Copilot vs OpenSpec Comparison](index.md).

---

## Quick Reference

| Attribute | Value |
|-----------|-------|
| Creator | Fission AI |
| Version evaluated | v1.2.0 |
| License | MIT |
| GitHub stars | 31.5k |
| Foundation governance | None (startup-backed) |
| Primary value | Multi-tool portability across 20+ AI coding tools |
| Primary limitation | No security enforcement, no content validation |

---

## Core Concept

OpenSpec replaces free-form AI prompting with a **structured artifact workflow**. Instead of asking an AI agent to "design a solution," you run `/opsx:propose NTK-10005: Add RFID wristband tracking` and OpenSpec guides the agent through a defined sequence of artifacts: proposal, behavioral specs, design, and implementation tasks.

The artifacts live in a folder structure. A YAML schema defines the dependency order (proposal before design, design before tasks). The AI agent generates each artifact in sequence, and you can review, roll back, or fast-forward through the workflow.

---

## 1. File Structure and Folder Layout

### Core Folder Architecture

```
openspec/
├── specs/                           # Behavioral source of truth (baseline)
│   ├── operations/spec.md
│   ├── booking/spec.md
│   └── logistics/spec.md
├── changes/                         # Active work (one folder per change)
│   └── NTK-10005-wristband-rfid/
│       ├── proposal.md              # Why is this change needed?
│       ├── analysis.md              # Investigation findings
│       ├── specs/                   # Delta specs (ADDED/MODIFIED/REMOVED)
│       ├── design.md                # How will it be implemented?
│       └── tasks.md                 # Implementation checklist
├── config.yaml                      # Project configuration and AI context
└── schemas/
    └── custom-schema/
        └── schema.yaml              # Custom artifact dependency schema
```

### Artifact Types

| Artifact | File | Purpose |
|----------|------|---------|
| Proposal | `proposal.md` | Problem statement, motivation, affected services, success criteria |
| Analysis | `analysis.md` | Investigation findings, evidence gathering |
| Specs | `specs/*.md` | Behavioral specifications (Given/When/Then) with delta tracking |
| Design | `design.md` | Proposed approach, architecture changes, trade-offs |
| Tasks | `tasks.md` | Implementation checklist with acceptance criteria |

### Naming Conventions

- Change folders: `ID-slug` in kebab-case (e.g., `NTK-10005-wristband-rfid`)
- Schema names: kebab-case (e.g., `novatrek-architecture`)
- Spec files: organized by logical domain (e.g., `operations/spec.md`, `booking/spec.md`)

---

## 2. YAML Schema System

### What Schemas Do

Schemas define the **dependency order** of artifacts. They specify which files must exist and in what sequence they should be generated.

### Schema Definition

```yaml
# openspec/schemas/novatrek-architecture/schema.yaml
name: novatrek-architecture
version: 1.0
description: Architecture solution design workflow

artifacts:
  - id: requirements
    generates: requirements.md
    requires: []
    description: "Ticket-sourced requirements"

  - id: analysis
    generates: analysis.md
    requires: [requirements]
    description: "Investigation and findings"

  - id: specs
    generates: specs/**/*.md
    requires: [requirements]
    description: "Behavioral specifications"

  - id: decisions
    generates: decisions.md
    requires: [specs]
    description: "Architecture decisions"

  - id: impacts
    generates: impacts/impact.*/index.md
    requires: [specs, decisions]
    description: "Per-service impact assessments"

  - id: tasks
    generates: tasks.md
    requires: [specs, decisions, impacts]
    description: "Implementation checklist"
```

### Dependency Graph Rules

| Rule | Example | Meaning |
|------|---------|---------|
| Linear | `requires: [requirements]` | Requirements must be complete first |
| Multiple | `requires: [specs, decisions]` | Both specs AND decisions must be complete |
| Glob patterns | `generates: specs/**/*.md` | Matches any depth subdirectories |
| Variable subdirs | `generates: impacts/impact.*/index.md` | Matches `impact.1/`, `impact.2/`, etc. |
| No circular deps | Schema validation rejects cycles | A cannot require B if B requires A |

### Critical Limitation: File Existence Only

Schemas validate that **files exist at the expected paths**. They do NOT validate:

- Internal structure (e.g., MADR format within `decisions.md`)
- Content completeness (e.g., "must have 2+ options")
- Section presence (e.g., "must include Consequences")
- Field values (e.g., "Status must be Proposed or Accepted")
- Cross-file consistency (e.g., specs matching OpenAPI contracts)
- Cardinality (e.g., "exactly one decisions file")

A `decisions.md` containing a single sentence passes schema validation because the file exists.

---

## 3. Configuration (config.yaml)

The configuration file provides project context to the AI agent and optional rule hints:

```yaml
schema: novatrek-architecture

context: |
  NovaTrek Adventures is a fictional adventure tourism platform with
  19 microservices across 9 bounded domains. Architecture decisions
  follow MADR format. All work is ticket-driven (NTK-XXXXX).

rules:
  requirements:
    template: requirements-template.md
    source: "Extract from JIRA ticket via mock tool"
    validation:
      - must_include: ["Ticket ID", "Problem Statement", "Acceptance Criteria"]

  specs:
    format: "Given/When/Then (RFC 2119 keywords: MUST, SHOULD, MAY)"
    organization: "By affected service domain"

  decisions:
    format: "MADR (Markdown Any Decision Record)"
    validation:
      - must_include: ["Status", "Date", "Context", "Decision Drivers", "Options"]
      - min_options: 2
```

IMPORTANT: The `rules` section is **advisory guidance** for the AI agent. It is NOT enforced programmatically. The AI agent reads the rules and *should* follow them, but there is no runtime validation that it did.

---

## 4. Slash Commands

OpenSpec provides commands that the AI agent interprets in chat:

### Core Workflow Commands

| Command | Purpose |
|---------|---------|
| `/opsx:propose` | Initiate a change with a ticket description |
| `/opsx:continue` | Resume artifact generation from where left off |
| `/opsx:ff` | Fast-forward to next artifact phase (skip current) |
| `/opsx:apply` | Apply a proposed design (merge delta specs) |
| `/opsx:archive` | Merge deltas into main specs, lock the change |
| `/opsx:validate` | Check artifacts against schema |
| `/opsx:status` | Show current artifact generation status |

### Navigation and Review Commands

| Command | Purpose |
|---------|---------|
| `/opsx:show` | Display a specific artifact |
| `/opsx:list` | List all open changes |
| `/opsx:diff` | Show delta between current and archived specs |
| `/opsx:compare` | Side-by-side comparison of two artifacts |

### Control Commands

| Command | Purpose |
|---------|---------|
| `/opsx:rollback` | Undo a phase (e.g., rollback design) |
| `/opsx:revert` | Hard reset change to last archive point |
| `/opsx:decide` | Lock a decision (mark as final) |
| `/opsx:template` | Generate an artifact template for manual editing |

### Integration Commands

| Command | Purpose |
|---------|---------|
| `/opsx:export` | Export change to JSON/YAML |
| `/opsx:import` | Import external change definition |
| `/opsx:sync` | Align schema versions after update |
| `/opsx:merge` | Manually merge speculative versions |
| `/opsx:discuss` | Multi-turn AI discussion of a change |

### Example Workflow

```
/opsx:propose NTK-10005: Add RFID wristband tracking field to check-in
  → AI creates proposal.md

/opsx:continue
  → AI generates specs/ with Given/When/Then scenarios

/opsx:continue
  → AI generates design.md

/opsx:validate
  → Schema checks: all required files exist

/opsx:archive
  → Deltas merged into main specs/, change folder locked
```

---

## 5. Behavioral Specs (Given/When/Then)

### Format

OpenSpec uses Gherkin-like behavioral language with RFC 2119 keywords:

```gherkin
Feature: Check-in workflow for adventure type classification

  Scenario: Pattern 1 (Basic) adventure auto-detects check-in flow
    Given an adventure with category TECHNICAL_HIKING (Pattern 1)
    And the adventure has elevation_gain < 1000m
    And guest_age >= 18
    When the guest initiates check-in via mobile
    Then the system SHALL present the "Basic" check-in flow
    And the check-in form SHALL NOT require waiver signature

  Scenario: Unknown category defaults to Pattern 3 (Full Service)
    Given an adventure with unknown or unmapped category
    When the system determines the category classification
    Then the system MUST default to Pattern 3 (Full Service)
    And the check-in flow SHALL require all safety protocols
```

### RFC 2119 Keywords

| Keyword | Meaning |
|---------|---------|
| MUST / MUST NOT | Absolute requirement, non-negotiable |
| SHOULD / SHOULD NOT | Strong recommendation, deviation allowed with justification |
| MAY | Optional, implementation choice |
| SHALL | Synonym for MUST (formal style) |

### Spec File Structure

```markdown
# Specification: Check-in Pattern Classification

## Feature Overview
[Narrative description]

## Entry Points
- `svc-check-in POST /check-in/start`
- `svc-check-in GET /adventures/{adventure_id}/classification`

## Behavioral Scenarios
[Given/When/Then scenarios]

## Data Schema Changes (Delta Specs)
[ADDED/MODIFIED/REMOVED sections]

## Integration Points
[Cross-service calls affected]

## Backward Compatibility
[How existing clients are unaffected]
```

---

## 6. Delta/Diff Tracking

### How Delta Tracking Works

1. **Baseline**: Main `specs/` folder contains the current behavioral contracts
2. **Change deltas**: New specs in `changes/NTK-XXXXX/specs/` describe what changes
3. **Explicit markers**: Changes use ADDED/MODIFIED/REMOVED labels
4. **Merge**: `/opsx:archive` applies deltas to the baseline

### Delta Spec Format

```markdown
## Delta Spec: Adventure Classification Schema

### ADDED Fields
- `classification_pattern: enum(PATTERN_1, PATTERN_2, PATTERN_3)`

### MODIFIED Fields
- `category: string` -- Now links to classification config for mapping

### REMOVED Fields
- None

### Dependent Services Affected
- svc-check-in (reads pattern for flow selection)
- svc-trip-catalog (stores pattern metadata)
```

### Benefits

- Changes are explicit -- no need to diff full spec files
- REMOVED fields highlight backward compatibility risks
- Archive points enable rollback
- Review is focused on what changed, not the full document

---

## 7. Archival Workflow

### What Archive Does

```
Active Change (NTK-10005)           /opsx:archive           Main Specs
├── proposal.md              ──────────────────>    ├── specs/operations.md (updated)
├── specs/ (deltas)                                 └── specs/...
├── design.md
└── tasks.md                                        Archive (read-only)
                                                    └── changes/NTK-10005-slug/
```

1. Merges delta specs into the main `specs/` folder
2. Locks the change folder as read-only reference
3. Preserves original proposal, design, and tasks
4. Creates a snapshot (git commit is manual or CI-driven)

### Post-Archive Manual Steps

OpenSpec does NOT automate post-archive workflows. These must be done manually or via separate CI:

- Update capability-changelog.yaml
- Regenerate portal documentation pages
- Update ticket status in the tracking system
- Commit and push to version control

---

## 8. Multi-Tool Portability

### Supported Tools

| Tool | Integration | Slash Commands |
|------|------------|---------------|
| Claude Code | Native | Full |
| Cursor | Native | Full |
| GitHub Copilot | Instructions + Skills | Full |
| Windsurf | Native | Full |
| JetBrains Copilot | Native | Full |
| Roo Code | Custom | Full |
| Zed AI | Limited | Partial |
| Continue.dev | Local models | Partial |
| LM Studio / Ollama | Local models | Limited |

### How Portability Works

**For native tools** (Claude Code, Cursor, Windsurf): OpenSpec installs as a native extension. Slash commands work in the chat interface. Workspace context is shared automatically.

**For GitHub Copilot**: OpenSpec generates skill files or instruction content. Slash commands work in Agent Mode. May conflict with existing `copilot-instructions.md` -- must verify during setup.

**For non-native tools**: OpenSpec provides a CLI wrapper that translates slash commands to tool-specific calls.

### When Portability Matters

Portability is OpenSpec's primary value proposition. It matters when:

- Your team uses multiple AI coding tools simultaneously
- You are evaluating tools and want to avoid vendor lock-in
- You want workflows that survive a tool migration

It does NOT matter when:

- You are committed to a single AI tool
- Your workflow is tool-specific by design
- Portability overhead exceeds switching cost

---

## 9. Security and Enforcement

### What OpenSpec Does NOT Provide

| Capability | Status |
|-----------|--------|
| Permission system / role-based access | None |
| Tool access control (restrict operations) | None |
| Sandboxing / execution boundaries | None |
| Lifecycle hooks (block operations, require approval) | None |
| Audit trail | None |
| Content validation (beyond file existence) | None |
| Cross-file consistency checking | None |
| External system integration hooks | None |

OpenSpec is a **workflow guidance framework**. It has no enforcement mechanisms. The AI agent follows OpenSpec's structure because the instructions tell it to, not because the runtime prevents deviation.

### Comparison to GitHub Copilot Native Enforcement

GitHub Copilot's native customization system provides multiple enforcement layers that OpenSpec lacks entirely:

- **Agent tool restrictions** (`tools` field in `.agent.md`) -- runtime filtering of available tools
- **PreToolUse hooks** -- deterministic shell commands that can block operations
- **User-level hooks** -- outside the repository, cannot be modified by workspace changes
- **GitHub org admin settings** -- platform-level governance

For detailed enforcement comparison, see [Copilot vs OpenSpec Comparison](index.md).

---

## 10. Limitations Summary

### Content Validation

| Gap | Impact | Workaround |
|-----|--------|-----------|
| Schemas validate file existence only | MADR format cannot be enforced | Manual review or separate linter |
| No template injection | Schemas do not auto-populate sections | Include templates in `config.yaml` context |
| No section validation | Cannot verify required content sections | Custom CI script |
| No cardinality enforcement | Cannot require "exactly 1 decisions file" | Convention documentation |

### Workflow Integration

| Gap | Impact | Workaround |
|-----|--------|-----------|
| Archive does not trigger metadata updates | Capability changelog requires manual update | Post-commit CI hook |
| No portal regeneration hook | Documentation pages not auto-updated | Separate CI job |
| No cross-file consistency checks | APIs can drift from behavioral specs | Custom lint rule |
| No external data access | Cannot validate against service catalog | Custom validator |

### Architecture-Specific Gaps

| Gap | Impact |
|-----|--------|
| No MADR decision template enforcement | Free-form decisions hard to compare |
| No capability model | L3 capability emergence not tracked |
| No per-service impact assessment structure | Unclear which services are affected |
| No assumptions register | Trade-offs not documented separately |
| No risk register with quality attributes | ISO 25010 not systematized |
| No user story tracking | Customer value disconnected from architecture |

### Maturity Risks

| Concern | Impact |
|---------|--------|
| v1.2.0, pre-v2.0 | Breaking changes possible |
| Startup-backed (Fission AI) | Unknown sustainability |
| No foundation governance | No IP protection; forking risk |
| Limited architecture case studies | Unclear if anyone uses it for architecture vs. feature dev |
| npm dependency | Adds build dependency to workspace |

---

## 11. When OpenSpec Makes Sense

OpenSpec is a good fit when:

- Your team **uses multiple AI coding tools** and needs portable workflow definitions
- You are doing **feature development** (proposal, spec, design, tasks maps well to features)
- Your workflow is **relatively flat** (no deep artifact hierarchies like MADR + impacts + capabilities)
- You value **behavioral specs** (Given/When/Then) as a primary deliverable
- You want a **standardized change lifecycle** across diverse tooling

OpenSpec is a poor fit when:

- You are committed to **a single AI tool** (portability is unused overhead)
- You need **architecture-specific artifacts** (MADR decisions, per-service impacts, capability tracking, risk registers)
- You need **content validation** beyond file existence
- You need **enforcement** (tool restrictions, lifecycle hooks, approval gates)
- You need **metadata integration** (capability changelog updates, portal regeneration)

---

## Further Reading

- [GitHub Copilot Customization Guide](github-copilot-customization-guide.md) -- how Copilot's native customization system works
- [Copilot vs OpenSpec Comparison](index.md) -- side-by-side comparison with recommendation
- [OpenSpec Analysis and Decision](research/OPENSPEC-ANALYSIS.md) -- full research findings from this workspace
- [OpenSpec Evaluation Plan](research/OPENSPEC-EVALUATION-PLAN.md) -- PoC evaluation criteria (not executed)
