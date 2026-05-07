# AI Instructions as Code — A First-Class EaC Pillar (Blueprint)

> **BLUEPRINT DOCUMENT.** This is the portable definition of Pillar 11. The patterns (three-layer model, hub-and-spoke, OpenSpec governance, RFC 2119 authoring) are the durable contributions. The "Operational Status" table near the end describes the **synthetic exemplar** in this workspace and is illustrative only — when the blueprint is exported to a corporate instance, that table is replaced with the real corporate status.

**Status**: This is Pillar 11 of the Everything as Code framework — see [EVERYTHING-AS-CODE-FRAMEWORK.md](EVERYTHING-AS-CODE-FRAMEWORK.md).

## Why AI Instructions Belong in EaC

AI instructions — the files that govern how AI coding agents reason, what personas they adopt, what constraints they obey, what skills they have — are now **first-class architectural artifacts**. They define the behavior of the agents that build the system. Treating them as ad-hoc Markdown notes is the same mistake organizations made treating infrastructure as ad-hoc shell scripts before IaC matured.

Every property of an EaC artifact applies to AI instructions:

| Property | AI instruction file requirement |
|----------|---------------------------------|
| Declarative | Describes *what* the agent should do, not *how* to retrieve it at runtime |
| Text-based | Markdown + YAML frontmatter (no proprietary formats) |
| Version-controlled | Lives in git, every change is a reviewed PR |
| Machine-readable | AI tools parse the file at session start |
| Human-readable | Engineers can read and edit it in any text editor |
| Testable | Validated by `validate-ai-instructions.sh` and rendered through governance gates |
| Reviewable | Every change flows through `/opsx:propose → /opsx:apply → /opsx:archive` |
| Reproducible | Hub source deterministically produces all derived files |

## The Three-Layer Model (from prior research)

AI behavior governance breaks into three distinct layers. AI Instructions as Code lives in Layer 1.

| Layer | Concern | Examples |
|-------|---------|----------|
| **Layer 1 — Behavioral Specification** | What the agent does, how it reasons, what constraints it obeys | `.github/copilot-instructions.md`, `.clinerules`, `.cursor/rules/*.mdc`, `.windsurfrules`, OpenSpec specs |
| **Layer 2 — Change Governance** | How Layer 1 artifacts are proposed, reviewed, versioned | OpenSpec, ADRs, hub-and-spoke replication |
| **Layer 3 — Runtime Integration** | How context and capability are delivered to the agent at inference time | MCP, RAG, vector stores, tool registries |

EaC governs Layer 1 and Layer 2. Layer 3 is a runtime concern (it has its own as-code patterns — MCP server configs, RAG index manifests — but those are operational, not behavioral).

## The Portability Problem

Every AI tool has its own instruction format:

| Tool | Primary file | Routing mechanism |
|------|--------------|-------------------|
| GitHub Copilot | `.github/copilot-instructions.md` + `.github/instructions/*.instructions.md` | `applyTo` glob in YAML frontmatter |
| Roo Code | `.clinerules` + `.roo/rules/` + `memory-bank/` + modes | Hierarchical aggregation by active mode |
| Cursor | `.cursor/rules/*.mdc` | YAML frontmatter (Always, Auto Attached, Agent Requested, Manual) |
| Windsurf | `.windsurfrules` + `.windsurf/rules/` + `.windsurf/workflows/` | Activation modes (Always On, Model Decision, Glob, Manual) |
| Continue.dev | `config.yaml` | Explicit Models / Rules / Prompts / MCP sections |
| Aider | `.aider.conf.yml` + convention files | Convention-based |

If you author your behavioral rules separately for each tool, you have:

- N copies of the same intent
- N opportunities for drift
- N different review processes
- No single source of truth for "what does my AI do?"

This is exactly the problem IaC solved for cloud providers. The answer is the same: **canonical source + derived files**.

## Hub-and-Spoke Architecture

The pattern this workspace adopts:

```
┌─────────────────────────────────────────────────┐
│   CANONICAL HUB                                 │
│   sites/ai-evaluation-2/docs/open-spec/         │
│     .ai-instructions/                           │
│       universal/                                │
│         corporate-standards.md                  │
│         personas.md                             │
│         workflows.md                            │
│       skills/                                   │
│         <skill>/SKILL.md                        │
└─────────────────────┬───────────────────────────┘
                      │ replicated to
                      ▼
┌─────────────────────────────────────────────────┐
│   DERIVED FILES (each has DERIVED FILE header)  │
│                                                 │
│   .clinerules                          (Roo)    │
│   .github/copilot-instructions.md      (Copilot)│
│   .github/instructions/                         │
│     prompt-me.instructions.md          (Copilot)│
│     prompt-mirror.instructions.md      (Copilot)│
│     plantuml-svg.instructions.md       (Copilot)│
│                                                 │
│   (future) .cursor/rules/*.mdc         (Cursor) │
│   (future) .windsurfrules              (Windsurf)│
└─────────────────────────────────────────────────┘
```

Every derived file MUST start with a `DERIVED FILE` header that:

1. Identifies the file as derived
2. Names the canonical source it was derived from
3. Forbids direct edits
4. Points contributors to the OpenSpec change workflow

## Governance via OpenSpec

Layer 2 — change governance — is implemented in this workspace via [OpenSpec](https://github.com/Fission-AI/OpenSpec).

The change workflow:

1. **`/opsx:propose`** — agent or human creates a change folder under `openspec/changes/<change-name>/` with `proposal.md`, `spec.md` (delta), `design.md`, `tasks.md`
2. **Review** — PR review focuses on the proposal artifacts before any code changes
3. **`/opsx:apply`** — agent executes the tasks in `tasks.md`, modifying both the canonical hub and the derived files
4. **Validation** — `scripts/validate-ai-instructions.sh` runs in CI, asserting:
   - Canonical files exist and are well-formed
   - Every derived file has a `DERIVED FILE` header
   - Derived content matches canonical (no drift)
   - YAML frontmatter is valid
   - Required rules are present
5. **`/opsx:archive`** — completed change moved to `openspec/changes/archive/<date>-<change-name>/`, becoming an immutable audit record

This is the same Codify-Validate-Generate (CVG) loop that every EaC pillar implements.

## What OpenSpec Does NOT Do

OpenSpec governs the *process* of changing AI instructions. It does **not**:

- Unify the schemas of the derived files (each tool still has its own format)
- Provide a portable Layer 1 schema (the industry has not standardized one)
- Replace runtime context delivery (Layer 3, MCP/RAG)

True portability requires a **Layer 1 schema standard** — a typed, declarative format for behavioral instructions that any compliant AI tool could parse natively. That standard does not yet exist. See [DEEP-RESEARCH-PROMPT-AI-NATIVE-ARCHITECTURE.md](DEEP-RESEARCH-PROMPT-AI-NATIVE-ARCHITECTURE.md) for an investigation into emerging candidates.

## Three Tiers of Portability (today vs. future)

| Tier | Description | Achievable today? |
|------|-------------|-------------------|
| **Semantic portability** | Write rules in platform-agnostic language (RFC 2119, structured sections, no tool-specific syntax) so they can be copied across tools with minimal adaptation | YES — adopt now |
| **Structural portability** | Hub-and-spoke architecture with canonical source driving platform-specific derived files | YES — implemented in this workspace via OpenSpec |
| **Schema portability** | Instructions conform to a formal typed schema that any compliant tool natively parses | NO — requires industry standard (W3C / OASIS / IETF) |

We are at structural portability today. Schema portability is a future state pending standardization.

## Recommended Practices for Authoring AI Instructions

Based on Constitutional AI, the Instruction Hierarchy paper, and OpenSpec governance:

1. **Use RFC 2119 language**: MUST, SHALL, SHOULD, MAY — gives the model unambiguous priority signals
2. **Separate concerns by file**: corporate standards, personas, skills, workflows — each in its own canonical file
3. **Define explicit negative constraints**: forbid actions explicitly (e.g., "MUST NOT generate fake URLs")
4. **Anchor every rule in evidence**: cite ADRs, capability specs, or domain rules — never assert rules without source
5. **Mark privilege tiers explicitly**: distinguish system rules (cannot be overridden) from project rules from session rules
6. **Version the canonical hub semantically**: changes to behavior get version bumps (semver)
7. **Ship every change through OpenSpec**: never edit derived files directly — even for "tiny" fixes
8. **Validate in CI**: failed validation blocks the merge
9. **Test the rules**: include exemplars showing positive and negative behaviors
10. **Audit quarterly**: rules accumulate; periodically refactor the hub to remove obsolete or contradictory rules

## Synthetic Exemplar Status (May 2026)

> The table below describes the synthetic exemplar in this blueprint workspace. It is **not** a corporate status. Replace this table when instantiating in the corporate workspace.

| | |
|---|---|
| Canonical hub | LIVE — `sites/ai-evaluation-2/docs/open-spec/.ai-instructions/` |
| Derived files | LIVE — 5 derived files with DERIVED FILE headers |
| OpenSpec init | COMPLETE — `.roo/` and `.github/prompts/` generated |
| Governance spec | LIVE — `openspec/specs/ai-instruction-governance/spec.md` (REQ-GOV-001 through 003) |
| Validation script | DEFERRED — see Phase 5 of the [TRANSFORMATION-PLAN.md](TRANSFORMATION-PLAN.md) |
| First end-to-end change cycle | NOT YET RUN — `openspec/changes/archive/` is empty |
| Cursor + Windsurf as derived targets | NOT YET ADDED |

## Forward Plan

Tracked in [TRANSFORMATION-PLAN.md](TRANSFORMATION-PLAN.md) Phase 5 (immediate) and Phase 11 (vendor-agnostic expansion).

## References

- OpenSpec — https://github.com/Fission-AI/OpenSpec
- Anthropic Constitutional AI — https://arxiv.org/abs/2212.08073
- Instruction Hierarchy paper (OpenAI) — https://arxiv.org/abs/2404.13208
- PROMPTPRISM (semantic prompt structure) — see academic search
- Model Context Protocol — https://modelcontextprotocol.io/
- W3C AI Agent Protocol Community Group — https://www.w3.org/community/agentprotocol/
- GitHub Copilot custom instructions — https://docs.github.com/en/copilot/customizing-copilot
- Cursor Rules — https://docs.cursor.com/context/rules
- Roo Code Rules — https://docs.roocode.com/features/rules
- Windsurf Rules — https://docs.windsurf.com/windsurf/cascade/rules
- Continue.dev Configuration — https://docs.continue.dev/customize/overview
