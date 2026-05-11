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
| **Layer 1 — Behavioral Specification** | What the agent does, how it reasons, what constraints it obeys | `.github/copilot-instructions.md`, `.clinerules`, `.cursor/rules/*.mdc`, `.windsurfrules`, OpenSpec specs, deployed agent system prompts (`agents/<name>/system-prompt.md`) |
| **Layer 2 — Change Governance** | How Layer 1 artifacts are proposed, reviewed, versioned | OpenSpec, ADRs, hub-and-spoke replication |
| **Layer 3 — Runtime Integration** | How context and capability are delivered to the agent at inference time | MCP, RAG, vector stores, tool registries |

EaC governs Layer 1 and Layer 2. Layer 3 is a runtime concern (it has its own as-code patterns — MCP server configs, RAG index manifests — but those are operational, not behavioral).

## The Portability Problem

AI instructions reach agents via two distinct surfaces, each with its own format fragmentation problem.

### IDE Coding Assistants

Every IDE AI tool has its own instruction file format:

| Tool | Primary file | Routing mechanism |
|------|--------------|-------------------|
| GitHub Copilot | `.github/copilot-instructions.md` + `.github/instructions/*.instructions.md` | `applyTo` glob in YAML frontmatter |
| Roo Code | `.clinerules` + `.roo/rules/` + `memory-bank/` + modes | Hierarchical aggregation by active mode |
| Cursor | `.cursor/rules/*.mdc` | YAML frontmatter (Always, Auto Attached, Agent Requested, Manual) |
| Windsurf | `.windsurfrules` + `.windsurf/rules/` + `.windsurf/workflows/` | Activation modes (Always On, Model Decision, Glob, Manual) |
| Continue.dev | `config.yaml` | Explicit Models / Rules / Prompts / MCP sections |
| Aider | `.aider.conf.yml` + convention files | Convention-based |

### Deployed Agent Platforms

Deployed agents — chatbots, workflow agents, API-accessible assistants — consume behavioral instructions as system prompts set via SDK or API at deployment time, not as files read from a workspace:

| Platform | Instruction mechanism | EaC pattern |
|----------|-----------------------|-------------|
| Azure AI Foundry (Agent Service) | `instructions` field set via Azure AI Projects SDK | Store as `agents/<name>/system-prompt.md` in git; CI deploys via SDK |
| OpenAI Assistants API | `instructions` field on the Assistant object | Store as file in git; CI deploys via OpenAI SDK |
| Amazon Bedrock Agents | Instruction field in agent resource config | Store as file in git; deploy via CloudFormation / CDK |
| Google Vertex AI Agents | System instruction in agent config | Store as file in git; deploy via Terraform / gcloud |

**The key distinction:** IDE assistants read files from the workspace; deployed agents are configured via API. The EaC answer for deployed agents is to store the system prompt as a versioned text file and deploy it via CI/CD using the platform SDK — the same principle as infrastructure manifests.

If you author your behavioral rules separately for each tool and each surface, you have:

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
└──────────────────────┬──────────────────────────┘
                       │ CI assembles into:
           ┌───────────┴────────────┐
           ▼                        ▼
┌──────────────────────┐  ┌─────────────────────────┐
│ IDE ASSISTANT FILES  │  │ DEPLOYED AGENT CONFIGS   │
│ (DERIVED FILE header)│  │ (DERIVED FILE header)    │
│                      │  │                          │
│ .clinerules   (Roo)  │  │ agents/<name>/           │
│ .github/copilot-     │  │   system-prompt.md       │
│   instructions.md    │  │   config.yaml            │
│   (Copilot)          │  │                          │
│ .github/instructions/│  │ Deployed to:             │
│   *.md (Copilot)     │  │   Azure AI Foundry       │
│                      │  │   OpenAI Assistants      │
│ (future) Cursor      │  │   Bedrock / Vertex AI    │
│ (future) Windsurf    │  │                          │
└──────────────────────┘  └─────────────────────────┘
```

Every derived file MUST start with a `DERIVED FILE` header that:

1. Identifies the file as derived
2. Names the canonical source it was derived from
3. Forbids direct edits
4. Points contributors to the OpenSpec change workflow

## Deployed Agents as a Second Derivation Target

The hub-and-spoke pattern applies equally to deployed agents. The hub contains the behavioral definition once; CI assembles it into platform-specific forms for both IDE assistant files and deployed agent configs.

**Scenario: one behavioral definition, two surfaces**

You want a Solution Architect AI that knows its persona, its skills (C4 diagrams, ADRs, impact assessments), and its constraints — accessible both in VS Code (as a Copilot customization) and as a standalone Azure AI Foundry chatbot.

Without the hub, you write the persona and skills twice. Drift occurs within weeks. There is no single PR to review when "the agent's behavior" changes.

With the hub:
- `universal/personas.md` — authoritative persona definition, RFC 2119 language, no platform-specific syntax
- `skills/sequence-diagrams/SKILL.md` — skill definition
- CI assembles these into `.github/copilot-instructions.md` (VS Code surface) **and** `agents/solution-architect/system-prompt.md` (Foundry surface)
- The Foundry config is committed to git and deployed by CI — never set by hand in the portal

**Azure AI Foundry agent config (EaC form):**

```yaml
# agents/solution-architect/config.yaml
# DERIVED FILE — assembled from hub by CI. Do not edit directly.
# Source: universal/personas.md + skills/
# Governance: openspec/specs/ai-instruction-governance/
name: solution-architect
description: Solution Architect AI assistant
model: gpt-4o
system_prompt_file: agents/solution-architect/system-prompt.md
tools:
  - type: file_search
    file_search:
      vector_store_ids: ["${ARCH_DOCS_VECTOR_STORE_ID}"]
```

**CI deployment step (Azure AI Projects SDK):**

```python
# scripts/deploy-foundry-agent.py
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
import os

client = AIProjectClient.from_connection_string(
    conn_str=os.environ["AZURE_AI_FOUNDRY_CONNECTION_STRING"],
    credential=DefaultAzureCredential()
)

with open("agents/solution-architect/system-prompt.md") as f:
    system_prompt = f.read()

agent = client.agents.create_agent(
    model="gpt-4o",
    name="solution-architect",
    instructions=system_prompt,
)
```

This makes the Foundry agent's behavioral definition version-controlled, reviewable, and governed by the same OpenSpec change workflow as every other AI instruction.

**The key rule:** A deployed agent whose system prompt lives only in the cloud portal has the same problem as a VM whose configuration was applied by hand — it works until it doesn't, and no one knows why it changed.

**Scope boundary:** The Foundry agent's *tools* (file search, code interpreter, MCP servers, vector store IDs) are Layer 3 (Runtime Integration) and are configured separately via the platform SDK or Bicep. The `config.yaml` above intentionally separates the behavioral spec (`system_prompt_file`) from the runtime tool config so each can evolve independently.

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

## What OpenSpec Does and Does Not Do

OpenSpec has two distinct capabilities that operate at different levels and are frequently conflated.

**What OpenSpec DOES provide**

| Capability | Mechanism |
|-----------|----------|
| Change governance | Structured proposal/apply/archive workflow for any change to AI instructions |
| Multi-tool workflow delivery | `openspec init` generates skill files and command files in each tool's native directory for 25+ tools |
| Slash command portability | `/opsx:propose`, `/opsx:apply`, `/opsx:archive` work identically in all tools after `openspec init` |
| Audit archive | Completed changes archived as immutable records |

The multi-tool delivery is precise in scope: OpenSpec generates files that teach each tool how to run **OpenSpec's own workflows**. When you run `/opsx:propose` in Cursor, Roo Code, Copilot, or Windsurf, OpenSpec handles it the same way. Same workflow, any tool.

**What OpenSpec does NOT provide**

OpenSpec does not carry **your content** across tools. It does **not**:

- Assemble your domain rules, corporate standards, or architectural conventions into each tool's instruction files
- Unify the schemas of derived content files (each tool still has its own format for behavioral instructions)
- Provide a portable Layer 1 schema (the industry has not standardized one)
- Replace runtime context delivery (Layer 3, MCP/RAG)

Content portability — distributing your domain rules from a single canonical hub into `.github/copilot-instructions.md`, `.clinerules`, `.cursor/rules/*.mdc`, and `.windsurfrules` — is the hub-and-spoke pattern's job. OpenSpec and hub-and-spoke are complementary, not overlapping: OpenSpec governs how changes are made to the hub; hub-and-spoke CI assembly distributes hub content to each tool's native files.

True **schema portability** requires a **Layer 1 schema standard** — a formal typed format that any compliant AI tool natively parses. That standard does not yet exist. See [Deep Research Prompt — AI-Native Architecture](DEEP-RESEARCH-PROMPT-AI-NATIVE-ARCHITECTURE.md) for an investigation into emerging candidates.

## Three Tiers of Portability (today vs. future)

| Tier | Description | Achievable today? |
|------|-------------|-------------------|
| **Semantic portability** | Write rules in platform-agnostic language (RFC 2119, structured sections, no tool-specific syntax) so they can be copied across tools with minimal adaptation | YES — adopt now |
| **Structural portability** | Hub-and-spoke architecture with canonical source driving platform-specific content into derived files | YES — implemented via hub-and-spoke CI assembly; OpenSpec governs the change process but does not perform the assembly |
| **Workflow portability** | The same change governance workflows (propose, apply, archive) run identically across 25+ AI tools without per-tool configuration | YES — provided by OpenSpec: `openspec init` generates skill and command files in each tool's native directory |
| **Schema portability** | Instructions conform to a formal typed schema that any compliant tool natively parses | NO — requires industry standard (W3C / OASIS / IETF) |

We are at structural and workflow portability today. Schema portability is a future state pending standardization.

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
| OpenSpec init | COMPLETE — `.roo/` and `.github/prompts/` generated (OpenSpec workflow skill files and command files; these deliver the `/opsx:*` slash commands to each tool — they are not content derivation files) |
| Governance spec | LIVE — `openspec/specs/ai-instruction-governance/spec.md` (REQ-GOV-001 through 003) |
| Validation script | DEFERRED — see Phase 5 of the [TRANSFORMATION-PLAN.md](TRANSFORMATION-PLAN.md) |
| First end-to-end change cycle | NOT YET RUN — `openspec/changes/archive/` is empty |
| Cursor + Windsurf as derived targets | NOT YET ADDED |

## Forward Plan

Tracked in [TRANSFORMATION-PLAN.md](TRANSFORMATION-PLAN.md) Phase 5 (immediate) and Phase 11 (vendor-agnostic expansion).

## References

- [AI-INSTRUCTION-GOVERNANCE.md](AI-INSTRUCTION-GOVERNANCE.md) — governance annex: single source of truth ownership, conflict detection, baseline access, conflict resolution procedure
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
