# AI Instruction Governance — Source of Truth, Conflict Resolution, and Baseline Access (Blueprint)

> **BLUEPRINT DOCUMENT.** This document defines the governance pattern for AI instructions across all derivation targets — IDE coding assistants and deployed agents. It is target-agnostic and intended for export to a corporate **EaC Adoption Instance** workspace. See [Blueprint Overview](README.md) for the Blueprint vs Instance distinction. See [AI Instructions as Code](AI-INSTRUCTIONS-AS-CODE.md) for the hub-and-spoke architecture this document extends.

**Status**: Pillar 11 governance annex — see [EaC Framework](EVERYTHING-AS-CODE-FRAMEWORK.md).

## Overview

The hub-and-spoke architecture defined in [AI Instructions as Code](AI-INSTRUCTIONS-AS-CODE.md) establishes that a canonical hub in git is the single source of truth for AI behavioral instructions, with derived files assembled by CI/CD for each target platform. This governance annex addresses three problems that arise once that pattern is in production:

1. **Source of truth fragmentation** — the hub is canonical, but the deployed agent's system prompt is also visible and editable in the cloud portal. Without explicit governance, the canonical source and the deployed artifact drift. Someone edits the portal. Nobody notices. The next CI run overwrites it. Or it doesn't, and now two versions of the instructions exist with no audit trail.

2. **Instruction conflict** — personas, skills, and corporate standards are authored independently and assembled together at deployment time. They can contradict each other. CI/CD assembles without checking for behavioral coherence. A passing pipeline means the instructions were delivered — not that they are coherent.

3. **Baseline access** — resolving a conflict requires understanding what the model does without any instructions applied. Deployed agents always have instructions. Without an explicit baseline environment, conflict resolution has no ground truth. The question "is this behavior from the model or from the instruction?" cannot be answered.

These are not edge cases. They are the predictable failure modes of any AI instruction governance system operating at scale.

---

## Problem 1 — Single Source of Truth

### The ownership hierarchy

```
 ┌────────────────────────────────────────────────────────────────┐
 │  CANONICAL HUB (git)  ← THE SINGLE SOURCE OF TRUTH            │
 │                                                                │
 │  hub/                                                          │
 │    universal/                                                  │
 │      personas.md              ← who the agent is              │
 │      corporate-standards.md   ← non-negotiable constraints     │
 │      workflows.md             ← how to approach tasks          │
 │    skills/                                                     │
 │      <skill>/SKILL.md         ← task-specific capability       │
 │  agents/governance/                                            │
 │    baseline-config.yaml       ← authored directly (not CI)     │
 │    staging-config.yaml        ← authored directly (not CI)     │
 └───────────────────────────────────┬────────────────────────────┘
                                     │
                        CI/CD assembles on every merge to main
                                     │
                  ┌──────────────────┴──────────────────┐
                  ▼                                      ▼
 ┌───────────────────────────────┐  ┌───────────────────────────────────┐
 │   IDE ASSISTANT FILES         │  │   DEPLOYED AGENT CONFIGS          │
 │   (same repository)           │  │   (cloud platform)                │
 │                               │  │                                   │
 │   DERIVED — READ ONLY         │  │   DERIVED — READ ONLY             │
 │                               │  │                                   │
 │   .github/copilot-            │  │   agents/<name>/                  │
 │     instructions.md           │  │     system-prompt.md              │
 │   .clinerules                 │  │     config.yaml                   │
 │   .cursor/rules/*.mdc         │  │                                   │
 │   .windsurfrules              │  │   Deployed to:                    │
 │                               │  │     Azure AI Foundry              │
 │   Do not edit directly.       │  │     OpenAI Assistants API         │
 │   Change the hub.             │  │     Bedrock / Vertex AI           │
 └───────────────────────────────┘  │                                   │
                                    │   Do not edit in the portal.      │
                                    │   Change the hub.                 │
                                    └───────────────────────────────────┘
```

### Portal edits vs. hub-based changes

Cloud platforms expose the deployed agent's system prompt in a web UI. It is possible to edit it directly. There are two valid positions on whether to allow this, and they suit different teams at different maturity levels.

| Approach | How it works | Trade-offs |
|---|---|---|
| **Portal edits allowed** | Behavioral changes are made directly in the cloud platform UI | Fast and low-friction; no tooling required; changes are immediate — but there is no version history, no review record, no rollback path, and no audit trail. If CI re-deploys, the edit is silently overwritten. Works for solo practitioners or early-stage teams where speed matters more than traceability. |
| **Hub-based changes only** | The portal field is treated as a read-only deployment artifact; all changes flow through the canonical hub via a governed change workflow | Full version history, peer review, rollback, and audit trail for every behavioral change. Requires CI infrastructure and team discipline. Suited to teams where AI agent behavior is a shared, governed asset. |

**Recommendation — hub-based changes**: Once an AI agent's behavior materially affects your team's work or your users' experience, portal edits become a liability. A change no one reviewed, no one can trace, and no one can roll back is the same governance problem that EaC solves for infrastructure and configuration. The hub-based approach applies the same discipline to agent behavior.

If your team is not yet ready for full hub-based governance, a practical middle path is: allow portal edits during initial development, but commit each working state back to the hub before sharing the agent with others. This preserves the feedback loop without requiring full CI infrastructure from day one.

### Ownership table

| Artifact | Owner | Change mechanism |
|----------|-------|-----------------|
| `universal/personas.md` | Architecture Practice Lead | OpenSpec change workflow (PR + review) |
| `universal/corporate-standards.md` | Architecture Practice Lead | OpenSpec change workflow (PR + review) |
| `universal/workflows.md` | Architecture Practice Lead | OpenSpec change workflow (PR + review) |
| `skills/<skill>/SKILL.md` | Named skill owner | OpenSpec change workflow (PR + review) |
| `agents/<name>/system-prompt.md` | CI — DO NOT EDIT | Assembled from hub by CI pipeline |
| `agents/<name>/config.yaml` | CI — DO NOT EDIT | Assembled from hub by CI pipeline |
| Portal system prompt field | CI — DO NOT EDIT | Overwritten on every CI deployment |
| `agents/governance/baseline-config.yaml` | Governance team | Direct authoring — NOT assembled by CI |
| `agents/governance/staging-config.yaml` | Governance team | Direct authoring — NOT assembled by CI |

### Version traceability

Every deployed agent config MUST embed the source commit it was assembled from. This makes it possible to answer: "what instructions is this agent running right now, and when were they last updated?"

```yaml
# agents/solution-architect/config.yaml
# DERIVED FILE — assembled from hub by CI. Do not edit directly.
# Source commit: ${GIT_COMMIT_SHA}
# Assembled:     ${CI_TIMESTAMP}
# Hub version:   ${HUB_SEMVER}
name: solution-architect
description: Solution Architect AI assistant
model: gpt-4o
system_prompt_file: agents/solution-architect/system-prompt.md
```

---

## Problem 2 — Instruction Conflict

### Conflict taxonomy

Instructions assembled from multiple independently authored source files can conflict in four ways:

```
CONFLICT TYPE 1 — DIRECT CONTRADICTION
──────────────────────────────────────────────────────────────────────
  corporate-standards.md:       "MUST use Mermaid for all diagrams"
  skills/sequence/SKILL.md:     "MUST use PlantUML for sequence diagrams"
                                              ↑
                                 Model receives both rules. Result:
                                 unpredictable. One rule wins based on
                                 position in the assembled prompt, not intent.

CONFLICT TYPE 2 — SCOPE OVERLAP
──────────────────────────────────────────────────────────────────────
  skills/architecture-docs/SKILL.md:   "When producing architecture documents..."
  skills/solution-design/SKILL.md:     "When producing architecture documents..."
                                              ↑
                                 Two skills both claim authority over
                                 the same output type. Model may blend
                                 them inconsistently or unpredictably.

CONFLICT TYPE 3 — PRIORITY AMBIGUITY
──────────────────────────────────────────────────────────────────────
  universal/personas.md:               "SHOULD be concise"
  skills/impact-analysis/SKILL.md:     "MUST provide full context for
                                        every finding, including all evidence"
                                              ↑
                                 MUST outranks SHOULD by RFC 2119, but
                                 the model may not apply precedence
                                 rules correctly across file boundaries.
                                 No explicit priority declaration exists.

CONFLICT TYPE 4 — TEMPORAL DRIFT
──────────────────────────────────────────────────────────────────────
  corporate-standards v2.0:            "use ADR format Y"    ← updated 2026-03
  skills/adr-authoring/SKILL.md:       references ADR format X  ← not updated
                                              ↑
                                 Skill is internally consistent but now
                                 contradicts the updated corporate standard.
                                 CI deploys the contradiction silently.
```

### The CI/CD gap

CI/CD solves the *delivery* problem. It does not solve the *coherence* problem.

```
WHAT CI/CD PROVIDES                  WHAT CI/CD DOES NOT PROVIDE
─────────────────────────────────    ─────────────────────────────────────────────
Assembles hub files into targets     Detects contradictions between rules
Validates file structure and syntax  Tests behavioral coherence of combined instructions
Deploys to all target platforms      Verifies which rule wins when two rules conflict
Maintains full git audit history     Detects scope overlap between skills
Produces deployment audit trail      Warns when a skill references outdated standards
Rolls back on pipeline failure       Catches Type 3 (priority ambiguity) conflicts
```

A passing CI pipeline means: the instructions were delivered correctly. It does NOT mean: the instructions are coherent.

### Conflict detection strategy — three layers

**Layer A — Static analysis (in CI)**

Add a validation step to the CI pipeline that:

- Scans all canonical files for MUST / MUST NOT pairs covering the same topic
- Flags any two skills whose trigger conditions overlap (e.g., both say "when producing architecture documents")
- Reports when a skill file references a standard version older than the current `corporate-standards.md` version header
- Blocks deployment on any detected Type 1 or Type 4 violation

**Layer B — Behavioral test suite**

Maintain a set of "conflict probe" prompts — scenarios specifically designed to trigger each potential conflict area. Run these against the staging environment after every hub change:

```
Probe ID:       diagram-format
Source:         Potential conflict between corporate-standards.md (Mermaid)
                and skills/sequence/SKILL.md (PlantUML)
Prompt:         "Create a sequence diagram showing the check-in flow."
Expected:       Response uses [defined expected format]
Fail condition: Response uses a format other than the expected format
Run against:    agent-staging, after every change to diagram-related files
```

This catches Type 2 and Type 3 conflicts that static analysis cannot see.

**Layer C — Periodic cross-skill review**

Quarterly (or triggered on any change to `universal/`): a human review of all skill files against the current corporate standards. This governance ritual catches temporal drift before it produces user-visible inconsistency. The review is tracked as an OpenSpec change proposal even when no changes result — the review itself is the audit artifact.

---

## Problem 3 — Baseline Access

### Why you need it

When a conflict is detected in a deployed agent, the resolution process requires answering three questions in sequence:

1. What does the model do with NO instructions applied? (baseline behavior)
2. What does the model do with ONLY the first rule applied? (isolated Rule A behavior)
3. What does the model do with ONLY the second rule applied? (isolated Rule B behavior)

Without answers to these questions, it is impossible to determine whether observed behavior is:

- The model's built-in default (the instructions are irrelevant to this scenario)
- Correct behavior driven by Rule A (Rule B is redundant or directly contradictory)
- Correct behavior driven by Rule B (Rule A is the problem)
- Neither (both rules are producing wrong behavior and both need to change)

**In a standard production deployment, the production agent always has the full assembled system prompt applied.** There is no way to ask it questions 1 or 2 without a separate environment. This makes conflict resolution a process of guessing against a black box.

### The three-environment pattern

```
 ┌──────────────────────────────────────────────────────────────────┐
 │  ENVIRONMENT 1: BASELINE                                         │
 │                                                                  │
 │  Agent:         agent-baseline                                   │
 │  System prompt: [none] or "You are a helpful assistant."         │
 │  Purpose:       Understand raw model behavior — no instructions  │
 │  Access:        Governance team ONLY — not for general use       │
 │  Lifecycle:     Permanent fixture — never deleted or modified    │
 │                                                                  │
 │  Use for:  "Is this behavior from the model or the instruction?" │
 └──────────────────────────────────────────────────────────────────┘

 ┌──────────────────────────────────────────────────────────────────┐
 │  ENVIRONMENT 2: STAGING / CONFLICT TEST                          │
 │                                                                  │
 │  Agent:         agent-staging                                    │
 │  System prompt: Loaded on demand — single rule file or pair      │
 │  Purpose:       Isolate and test individual instructions         │
 │  Access:        Governance team ONLY                             │
 │  Lifecycle:     Ephemeral — system prompt replaced per test run  │
 │                                                                  │
 │  Use for:  "What does Rule A alone produce?"                     │
 │            "What does Rule A + Rule B together produce?"         │
 └──────────────────────────────────────────────────────────────────┘

 ┌──────────────────────────────────────────────────────────────────┐
 │  ENVIRONMENT 3: PRODUCTION                                       │
 │                                                                  │
 │  Agent:         solution-architect (or domain-specific name)     │
 │  System prompt: Full assembled instructions (CI-deployed)        │
 │  Purpose:       Live agent for authorized users                  │
 │  Access:        Standard access controls for authorized users    │
 │  Lifecycle:     Updated by CI on every merge to main             │
 │                                                                  │
 │  Use for:  Live work. Do not use for governance testing.         │
 └──────────────────────────────────────────────────────────────────┘
```

### Conflict resolution workflow

```
 CONFLICT DETECTED
 (source: user report, behavioral test failure, or static analysis)
         │
         ▼
 STEP 1 — Reproduce in production
          Open:    Production environment
          Prompt:  The scenario that exposed the conflict
          Record:  What the agent actually does
         │
         ▼
 STEP 2 — Establish baseline
          Open:    BASELINE environment (no instructions)
          Prompt:  Same scenario
          Record:  What the model does with no instructions
          Answer:  Is this the model's default, or is an instruction driving it?
         │
         ▼
 STEP 3 — Isolate Rule A
          Open:    STAGING environment
          Apply:   ONLY the first candidate instruction file
          Prompt:  Same scenario
          Record:  Behavior with only Rule A
         │
         ▼
 STEP 4 — Isolate Rule B
          Open:    STAGING environment
          Apply:   ONLY the second candidate instruction file
          Prompt:  Same scenario
          Record:  Behavior with only Rule B
         │
         ▼
 STEP 5 — Combine
          Open:    STAGING environment
          Apply:   Rule A + Rule B together
          Prompt:  Same scenario
          Record:  Which rule wins; what the agent actually does
         │
         ▼
 STEP 6 — Decide
          With evidence from steps 1–5, determine:
            - Which behavior is correct for this scenario?
            - Which rule needs to be updated or made more specific?
            - Does an explicit priority declaration need to be added?
         │
         ▼
 STEP 7 — Update the canonical hub
          Edit the relevant file(s) in the hub
          Propose via OpenSpec change workflow (proposal + review + apply)
          Merge to main
         │
         ▼
 STEP 8 — Verify resolution
          CI deploys updated instructions to all environments
          Re-run the conflict probe in STAGING
          Confirm production agent exhibits the resolved behavior
          Record the conflict and resolution in the OpenSpec archive
```

### Provisioning the governance environments as code

The baseline and staging environments are declared as code — not created by hand in the portal:

```yaml
# agents/governance/baseline-config.yaml
# This file is authored directly — NOT assembled by CI.
# It is a permanent governance fixture. Do not modify the system_prompt field.
name: agent-baseline
description: >
  Permanent governance fixture. Minimal behavioral instructions applied.
  Used exclusively for conflict resolution and baseline testing.
  Do not use for production purposes.
model: gpt-4o
system_prompt: "You are a helpful assistant."
access_policy: governance-team-only
deployed_by: manual or separate governance CI step — NOT the instruction assembly pipeline
```

```yaml
# agents/governance/staging-config.yaml
# This file is authored directly — NOT assembled by CI.
# System prompt is loaded on demand by the governance test harness, not by CI.
name: agent-staging
description: >
  Ephemeral conflict test environment.
  System prompt replaced per test run by the governance test harness.
  Used exclusively for conflict resolution and skill validation.
  Do not use for production purposes.
model: gpt-4o
system_prompt: null
access_policy: governance-team-only
deployed_by: manual or separate governance CI step — NOT the instruction assembly pipeline
```

**Critical constraint**: The baseline and staging agent configs MUST NOT be processed by the same CI pipeline that assembles and deploys production instructions. They are governance fixtures — their behavior is intentionally decoupled from the instruction assembly process.

---

## Governance Architecture — Complete Picture

```
 CANONICAL HUB (git — single source of truth)
 ┌──────────────────────────────────────────────────────────────────────┐
 │  hub/universal/personas.md                                           │
 │  hub/universal/corporate-standards.md                                │
 │  hub/universal/workflows.md                                          │
 │  hub/skills/<skill>/SKILL.md  (one file per skill)                   │
 │  agents/governance/baseline-config.yaml  ← authored, not CI-derived  │
 │  agents/governance/staging-config.yaml   ← authored, not CI-derived  │
 └──────────────────────────────────┬───────────────────────────────────┘
                                    │
                       ┌────────────▼────────────────┐
                       │   CI/CD PIPELINE             │
                       │                              │
                       │  Phase 1: Static conflict    │
                       │    scan (Type 1 + 4)         │
                       │  Phase 2: Assemble derived   │
                       │    files from hub            │
                       │  Phase 3: Run behavioral     │
                       │    probe suite in staging    │
                       │  Phase 4: Deploy on pass     │
                       │  Phase 5: Fail and alert     │
                       │    on any conflict detected  │
                       └────────┬──────────────┬──────┘
                                │              │
             ┌──────────────────▼───┐ ┌────────▼──────────────────────────┐
             │  IDE ASSISTANT FILES │ │  DEPLOYED AGENT ENVIRONMENTS       │
             │                      │ │                                    │
             │  DERIVED — READ ONLY │ │  PRODUCTION (CI-managed)           │
             │                      │ │    system-prompt: [full assembled] │
             │  .github/copilot-    │ │    access: authorized users        │
             │    instructions.md   │ │                                    │
             │  .clinerules         │ │  BASELINE (governance fixture)     │
             │  .cursor/rules/*.mdc │ │    system-prompt: [minimal]        │
             │  .windsurfrules      │ │    access: governance team only    │
             │                      │ │    managed: separately from CI     │
             │  Change via hub.     │ │                                    │
             └──────────────────────┘ │  STAGING (governance fixture)      │
                                      │    system-prompt: [on demand]      │
                                      │    access: governance team only    │
                                      │    managed: separately from CI     │
                                      └────────────────────────────────────┘
```

---

## Implementation Checklist

Before declaring AI instruction governance operational:

- [ ] Canonical hub location declared and documented in repository README
- [ ] All IDE-assistant derived files carry `DERIVED FILE` headers
- [ ] All deployed agent configs carry `DERIVED FILE` headers with source commit SHA
- [ ] CI pipeline static conflict scan active (catches Type 1 and Type 4)
- [ ] Behavioral probe suite authored with at least one probe per potential conflict area
- [ ] CI pipeline runs behavioral probe suite against staging on every merge
- [ ] Baseline agent deployed, access-restricted to governance team
- [ ] Staging agent deployed, access-restricted to governance team
- [ ] Baseline and staging configs committed to git (not portal-managed)
- [ ] Ownership table populated with named owners for every canonical file
- [ ] Conflict resolution workflow documented and team has run through it at least once
- [ ] Quarterly cross-skill review scheduled on team calendar
- [ ] OpenSpec change workflow active for all hub modifications
- [ ] Conflict resolution records archived in OpenSpec after each resolved conflict

---

## Synthetic Exemplar Status (May 2026)

> The table below describes the synthetic exemplar in this blueprint workspace. It is **not** a corporate status. Replace this table when instantiating in the corporate workspace.

| | |
|---|---|
| Canonical hub | LIVE — `sites/ai-evaluation-2/docs/open-spec/.ai-instructions/` |
| Derived IDE files | LIVE — 5 derived files with DERIVED FILE headers |
| Deployed agent configs | NOT YET — no agents/ directory in this workspace |
| Baseline environment | NOT YET — no Foundry deployment in this synthetic workspace |
| Staging environment | NOT YET — no Foundry deployment in this synthetic workspace |
| Static conflict scan | NOT YET — see SYNTHETIC-EXEMPLAR-BACKLOG.md |
| Behavioral probe suite | NOT YET — see SYNTHETIC-EXEMPLAR-BACKLOG.md |
| Quarterly review process | NOT YET — governance ritual not yet scheduled |

---

## References

- [AI Instructions as Code](AI-INSTRUCTIONS-AS-CODE.md) — hub-and-spoke architecture, derivation chain, OpenSpec change governance and multi-tool workflow delivery
- [EaC Framework](EVERYTHING-AS-CODE-FRAMEWORK.md) — Pillar 11 definition and maturity model
- [Transformation Plan](TRANSFORMATION-PLAN.md) — Pillar 11 adoption phases
- OpenSpec — https://github.com/Fission-AI/OpenSpec
- Azure AI Foundry Agent Service — https://learn.microsoft.com/en-us/azure/ai-studio/
- Anthropic Constitutional AI — https://arxiv.org/abs/2212.08073
- Instruction Hierarchy paper (OpenAI) — https://arxiv.org/abs/2404.13208
