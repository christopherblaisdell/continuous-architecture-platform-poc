# AI Agent Instruction Governance — A Practical Guide

**Audience**: Architects, platform engineers, and engineering leads evaluating how to govern AI agent behavior across multiple surfaces — IDE coding assistants, deployed chatbots, and workflow agents.

**Purpose**: This document addresses where AI agent instructions should live, who owns them, how conflicts between instructions are detected and resolved, and what infrastructure is required to do that resolution correctly.

---

## The Problem in Plain Language

An AI agent's behavior is determined by its instructions — the system prompt, persona definition, skill descriptions, and constraint rules that tell the model who it is and how it should behave.

Once you move beyond a single AI tool in a single context, those instructions need to reach multiple surfaces:

| Surface | How instructions are consumed |
|---------|------------------------------|
| IDE coding assistants (GitHub Copilot, Cursor, Windsurf, Roo Code) | Files in the repository, read at session start |
| Deployed chatbots (Azure AI Foundry, OpenAI Assistants) | System prompt set via API or portal at deployment time |
| Workflow agents (Bedrock Agents, Vertex AI) | Instruction field in the agent resource config |

If you write the instructions separately for each surface, you have:

- Multiple copies of the same intent
- Multiple opportunities for drift
- Multiple change processes with no shared audit trail
- No single answer to the question "what does my AI actually do?"

This is the exact problem Infrastructure as Code solved for cloud configuration. The answer is the same: **one canonical source, derived targets**.

But choosing a single source is just the beginning. Three governance problems emerge immediately.

---

## Problem 1 — Where Does the Single Source of Truth Live?

### The answer

The canonical source MUST live in git — version-controlled, reviewable, and auditable. A specific location in the repository is declared as the hub, and every other copy of those instructions is a derived artifact.

```
 GIT REPOSITORY — canonical (the single source of truth)
 ┌────────────────────────────────────────────────────────────────┐
 │  hub/                                                          │
 │    universal/                                                  │
 │      personas.md              ← who the agent is              │
 │      corporate-standards.md   ← non-negotiable rules          │
 │      workflows.md             ← how to approach tasks         │
 │    skills/                                                     │
 │      <skill-name>/SKILL.md    ← one file per capability       │
 └──────────────────────────────────┬─────────────────────────────┘
                                    │
                   CI/CD assembles on every merge to main
                                    │
             ┌──────────────────────┴──────────────────────┐
             ▼                                             ▼
 ┌─────────────────────────────┐  ┌──────────────────────────────────┐
 │  IDE ASSISTANT FILES        │  │  DEPLOYED AGENT CONFIGS          │
 │  (same repository)          │  │  (cloud platform)                │
 │                             │  │                                  │
 │  DERIVED — READ ONLY        │  │  DERIVED — READ ONLY             │
 │                             │  │                                  │
 │  .github/copilot-           │  │  agents/<name>/                  │
 │    instructions.md          │  │    system-prompt.md              │
 │  .clinerules (Roo Code)     │  │    config.yaml                   │
 │  .cursor/rules/*.mdc        │  │                                  │
 │  .windsurfrules             │  │  Deployed to:                    │
 │                             │  │    Azure AI Foundry              │
 │  Do not edit directly.      │  │    OpenAI Assistants API         │
 │  Change the hub.            │  │    Bedrock / Vertex AI           │
 └─────────────────────────────┘  │                                  │
                                  │  Do not edit in the portal.      │
                                  │  Change the hub.                 │
                                  └──────────────────────────────────┘
```

### The portal-edit trap

Every cloud platform that hosts deployed agents exposes the system prompt in a web UI. It is possible to edit it there directly — and it feels fast and productive. This is the most common governance failure:

- The portal edit is not version-controlled
- The portal edit is not reviewed or approved
- The portal edit is overwritten on the next CI deployment, or silently persists if CI is not re-run
- Nobody else knows it happened

**Rule without exception**: The system prompt visible in the cloud portal is a read-only audit artifact. It is never the change mechanism. All behavioral changes flow through the canonical hub via the standard change workflow.

### Ownership must be explicit

Every file in the hub needs a declared owner who is accountable for its accuracy and coherence with the rest of the hub:

| File | Owner | How changes are made |
|------|-------|---------------------|
| `universal/personas.md` | Architecture Practice Lead | Pull request with human review |
| `universal/corporate-standards.md` | Architecture Practice Lead | Pull request with human review |
| `skills/<skill>/SKILL.md` | Named skill owner | Pull request with human review |
| `agents/<name>/system-prompt.md` | CI pipeline | Assembled automatically — do not edit |
| `agents/<name>/config.yaml` | CI pipeline | Assembled automatically — do not edit |
| Portal system prompt | CI pipeline | Overwritten on every deployment — do not edit |

### Version traceability

Every deployed agent configuration must embed the source commit it was assembled from. This answers the question "what instructions is this agent running right now?" at any point in time:

```yaml
# agents/solution-architect/config.yaml
# DERIVED FILE — assembled from hub by CI. Do not edit directly.
# Source commit: a3f7c92
# Assembled:     2026-05-07T14:32:00Z
# Hub version:   2.1.0
name: solution-architect
model: gpt-4o
system_prompt_file: agents/solution-architect/system-prompt.md
```

---

## Problem 2 — Instruction Conflicts and the Limits of CI/CD

### Instructions authored independently will conflict

Personas, skills, and corporate standards are written separately and assembled together. When the assembled combination is incoherent, the model receives contradictory instructions and produces unpredictable behavior. There are four conflict patterns:

```
TYPE 1 — DIRECT CONTRADICTION
  corporate-standards.md:     "MUST use Mermaid for all diagrams"
  skills/sequence/SKILL.md:   "MUST use PlantUML for sequence diagrams"
                                           ↑
                              Both rules apply. One wins based on
                              where it appears in the assembled prompt.
                              The outcome is not deterministic.

TYPE 2 — SCOPE OVERLAP
  skills/architecture-docs/SKILL.md:   "When producing architecture documents..."
  skills/solution-design/SKILL.md:     "When producing architecture documents..."
                                           ↑
                              Two skills claim the same territory.
                              The model blends them inconsistently
                              across different sessions.

TYPE 3 — PRIORITY AMBIGUITY
  universal/personas.md:              "SHOULD be concise"
  skills/impact-analysis/SKILL.md:    "MUST provide full context
                                       for every finding"
                                           ↑
                              MUST outranks SHOULD, but the model
                              may not apply this precedence correctly
                              across separately authored files.

TYPE 4 — TEMPORAL DRIFT
  corporate-standards.md v2.0:    "use ADR format Y"   ← updated March 2026
  skills/adr-authoring/SKILL.md:  references format X  ← not updated
                                           ↑
                              Skill is internally correct but now
                              contradicts the updated standard.
                              The contradiction is deployed silently.
```

### What CI/CD does not do

This is the critical gap:

```
WHAT CI/CD PROVIDES                  WHAT CI/CD DOES NOT PROVIDE
─────────────────────────────────    ─────────────────────────────────────────────
Assembles hub files into targets     Detects contradictions between rules
Validates file syntax and structure  Tests behavioral coherence of combined rules
Deploys to all target platforms      Verifies which rule wins when two conflict
Maintains full git audit history     Detects scope overlap between skills
Rolls back on pipeline failure       Warns when a skill is outdated relative to
                                     an updated corporate standard
```

A passing CI pipeline means: the instructions were delivered. It does NOT mean: the instructions are coherent.

### How to detect conflicts before users find them

Three layers of defense, applied together:

**Layer 1 — Static analysis in CI**

Add a validation step that scans all canonical files for contradictory MUST / MUST NOT pairs on the same topic, flags skills whose trigger conditions overlap, and reports skills that reference an older version of corporate standards than the current one. This catches Type 1 and Type 4 conflicts before deployment.

**Layer 2 — Behavioral probe suite**

Maintain a set of "conflict probe" prompts — scenarios specifically designed to trigger each potential conflict area. Run them automatically in a staging environment after every hub change:

```
Probe: diagram-format
Prompt: "Create a sequence diagram showing the check-in flow."
Expected: Response uses [defined format per current corporate-standards]
Fail: Response uses a different format
Run: After every change touching any diagram-related instruction file
```

This catches Type 2 and Type 3 conflicts that static analysis cannot see.

**Layer 3 — Periodic cross-skill review**

Once per quarter (or triggered on any change to the universal/ files): a human review of all skill files against the current corporate standards. This catches temporal drift (Type 4) before it accumulates into user-visible inconsistency. The review is documented even when no changes result — the review record is the governance artifact.

---

## Problem 3 — You Need Baseline Access to Resolve Conflicts

### Why this is non-obvious

When a conflict is detected, the resolution process requires answering three questions:

1. What does the model do with NO instructions applied?
2. What does the model do with ONLY Rule A applied?
3. What does the model do with ONLY Rule B applied?

Without these answers, it is impossible to know whether the observed behavior is:

- The model's built-in default (the instructions are irrelevant to this scenario)
- Correct per Rule A, with Rule B being redundant or wrong
- Correct per Rule B, with Rule A being the problem
- Wrong under both rules, which both need to change

In a standard deployed agent, the production system prompt is always applied. You cannot ask questions 1 or 2 without a separate environment. Without this, conflict resolution is guesswork.

### The three-environment pattern

```
 ┌──────────────────────────────────────────────────────────────────┐
 │  BASELINE                                                        │
 │  System prompt: none (or "You are a helpful assistant.")         │
 │  Purpose:  Raw model behavior — no instructions applied          │
 │  Access:   Governance team ONLY                                  │
 │  Rule:     This environment's system prompt is NEVER changed.    │
 │            It is a permanent reference point.                    │
 └──────────────────────────────────────────────────────────────────┘

 ┌──────────────────────────────────────────────────────────────────┐
 │  STAGING / CONFLICT TEST                                         │
 │  System prompt: loaded on demand — one rule file at a time       │
 │  Purpose:  Isolate individual instructions for testing           │
 │  Access:   Governance team ONLY                                  │
 │  Rule:     System prompt is replaced per test run.               │
 │            This environment is ephemeral by design.              │
 └──────────────────────────────────────────────────────────────────┘

 ┌──────────────────────────────────────────────────────────────────┐
 │  PRODUCTION                                                      │
 │  System prompt: full assembled instructions (CI-deployed)        │
 │  Purpose:  Live agent for authorized users                       │
 │  Access:   Standard access controls                              │
 │  Rule:     Only CI updates this environment.                     │
 │            Never used for governance testing.                    │
 └──────────────────────────────────────────────────────────────────┘
```

### The conflict resolution procedure

When a conflict is detected — from user report, a failing behavioral probe, or static analysis — follow this procedure:

```
 1. REPRODUCE
    Use the production environment.
    Prompt: the scenario that exposed the conflict.
    Record: what the deployed agent actually does.

 2. ESTABLISH BASELINE
    Use the baseline environment (no instructions).
    Prompt: same scenario.
    Record: what the model does with no instructions at all.
    Question: Is this the model's default, or is an instruction driving it?

 3. ISOLATE RULE A
    Use the staging environment.
    Apply: only the first candidate instruction file.
    Prompt: same scenario.
    Record: behavior with only Rule A.

 4. ISOLATE RULE B
    Use the staging environment.
    Apply: only the second candidate instruction file.
    Prompt: same scenario.
    Record: behavior with only Rule B.

 5. COMBINE
    Use the staging environment.
    Apply: Rule A + Rule B together.
    Prompt: same scenario.
    Record: which rule wins; what the agent does.

 6. DECIDE
    With evidence from steps 1–5:
      - Which behavior is correct for this scenario?
      - Which rule needs to be updated, narrowed, or made more specific?
      - Does an explicit priority declaration need to be added?

 7. UPDATE THE HUB
    Edit the relevant canonical file(s).
    Submit via the standard change workflow (pull request + review).
    Merge to main.

 8. VERIFY
    CI deploys updated instructions to all environments.
    Re-run the conflict probe in staging.
    Confirm production agent exhibits the resolved behavior.
    Record the conflict and resolution for future reference.
```

### These environments must themselves be governed as code

The governance environments are not created by hand in the portal. They are declared as versioned config files in git and deployed by a separate governance pipeline — intentionally isolated from the CI pipeline that assembles and deploys production instructions:

```yaml
# agents/governance/baseline-config.yaml
# Authored directly — NOT assembled by the instruction CI pipeline.
# The system_prompt field MUST NOT be changed. It is a permanent reference.
name: agent-baseline
description: Permanent governance fixture. No behavioral instructions.
             Governance team only. Not for production use.
model: gpt-4o
system_prompt: "You are a helpful assistant."
access_policy: governance-team-only
```

```yaml
# agents/governance/staging-config.yaml
# Authored directly — NOT assembled by the instruction CI pipeline.
# System prompt is replaced on demand by the governance test harness.
name: agent-staging
description: Ephemeral conflict test environment. Governance team only.
             System prompt loaded per test run. Not for production use.
model: gpt-4o
system_prompt: null
access_policy: governance-team-only
```

**Critical isolation rule**: The baseline and staging configs MUST NOT be processed by the same CI pipeline that assembles production instructions. They are governance fixtures. Their behavior is intentionally decoupled from the instruction assembly process. If the production CI pipeline overwrites the baseline system prompt, the baseline is no longer a baseline.

---

## What Good Governance Looks Like — The Full Picture

```
 CANONICAL HUB (git — single source of truth)
 ┌──────────────────────────────────────────────────────────────────────┐
 │  hub/universal/personas.md                                           │
 │  hub/universal/corporate-standards.md                                │
 │  hub/skills/<skill>/SKILL.md                                         │
 │  agents/governance/baseline-config.yaml  ← authored directly         │
 │  agents/governance/staging-config.yaml   ← authored directly         │
 └────────────────────────────────┬─────────────────────────────────────┘
                                  │
                     ┌────────────▼────────────────────┐
                     │   INSTRUCTION CI PIPELINE        │
                     │                                  │
                     │  Phase 1: Static conflict scan   │
                     │    (Type 1 + Type 4 detection)   │
                     │  Phase 2: Assemble derived files │
                     │  Phase 3: Behavioral probe suite │
                     │    (Type 2 + Type 3 detection)   │
                     │  Phase 4: Deploy on pass         │
                     │  Phase 5: Block and alert on any │
                     │    conflict detected              │
                     └─────────┬─────────────┬──────────┘
                               │             │
          ┌────────────────────▼──┐ ┌────────▼──────────────────────────┐
          │  IDE ASSISTANT FILES  │ │  DEPLOYED AGENT ENVIRONMENTS       │
          │  DERIVED — READ ONLY  │ │                                    │
          │                       │ │  PRODUCTION                        │
          │  .github/copilot-     │ │    system-prompt: [full]           │
          │    instructions.md    │ │    access: authorized users        │
          │  .clinerules          │ │    updated: by instruction CI      │
          │  .cursor/rules/*.mdc  │ │                                    │
          │  .windsurfrules       │ │  BASELINE (governance)             │
          │                       │ │    system-prompt: [minimal, fixed] │
          │  Change via hub only. │ │    access: governance team only    │
          └───────────────────────┘ │    updated: NEVER by instruction CI│
                                    │                                    │
                                    │  STAGING (governance)              │
                                    │    system-prompt: [on demand]      │
                                    │    access: governance team only    │
                                    │    updated: by test harness        │
                                    └────────────────────────────────────┘
```

---

## Getting Started Checklist

| Step | Action |
|------|--------|
| 1 | Declare the canonical hub location and document it in the repository README |
| 2 | Establish the ownership table — name an owner for every hub file |
| 3 | Tag all derived files with a DERIVED FILE header referencing the hub |
| 4 | Add version traceability (source commit SHA) to all deployed agent configs |
| 5 | Add static conflict analysis to CI (catches Type 1 + Type 4) |
| 6 | Author a behavioral probe suite (one probe per potential conflict area) |
| 7 | Deploy a baseline agent with minimal/no instructions, governance team access only |
| 8 | Deploy a staging agent for on-demand conflict testing, governance team access only |
| 9 | Document both governance environments as code — not portal-managed |
| 10 | Run a cross-skill review before the first production deployment |
| 11 | Schedule a quarterly cross-skill review on the team calendar |
| 12 | Train the governance team on the conflict resolution procedure |

---

## Key Principles (Summary)

1. **The canonical hub in git is always authoritative.** The portal-visible system prompt is a read-only audit artifact.

2. **CI/CD delivers instructions. It does not validate coherence.** Behavioral coherence requires a separate test suite and human review.

3. **Every deployed agent config must be traceable to a source commit.** If you cannot answer "what instructions is this agent running right now?", the governance is incomplete.

4. **Baseline access is a non-negotiable governance requirement.** You cannot resolve instruction conflicts without an environment where no instructions are applied.

5. **Governance environments must themselves be governed as code.** If the baseline agent's system prompt can be changed in the portal, there is no baseline.

6. **Skill ownership must be explicit.** Skills without named owners drift. Someone must be accountable for each file in the hub.
