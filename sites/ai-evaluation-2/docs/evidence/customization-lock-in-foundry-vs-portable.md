<!-- CONFLUENCE-PUBLISH -->
<!-- CONFLUENCE-URL: -->

# Customization Portability: How Option D and OpenSpec Neutralize Foundry Lock-In

!!! note "Context for This Analysis"
    This page examines the lock-in risk of customizing AI agents within Azure AI Foundry or Foundry IQ — and how the evaluation's recommended architecture (Option D + living practice customization + OpenSpec) neutralizes that risk by separating concerns across layers. This analysis is offered as input for the decision-makers — not as a directive.

## The Question

The existing analysis asks: [What Copilot investment could become a dead end?](foundry-iq-comparison.md#what-copilot-investment-could-become-a-dead-end) The answer is reassuring — mostly a reformatting cost, not a data loss.

But the inverse question has not been asked: **What happens to customization investments made directly in Azure AI Foundry or Foundry IQ if the team later needs to switch platforms?**

The short answer: it depends on which layer the customization lives in. The longer answer — and the recommended architecture for making the risk acceptable — is what this page covers.

## Yes, Foundry-Native Customization Creates Lock-In

Customizing directly in Azure AI Foundry or Foundry IQ creates a qualitatively different kind of lock-in than customizing via portable files. The reason is structural: Foundry customizations are platform-specific configurations stored in Azure's control plane, not version-controlled files in a repository.

### What Gets Locked In

| Foundry Investment | Portable? | Why |
|--------------------|-----------|-----|
| **Knowledge base definitions** | No | Azure-specific constructs — knowledge source bindings, retrieval instructions, reasoning effort levels. No equivalent in other platforms. |
| **Scoring profiles and relevance tuning** | No | Azure AI Search-specific configuration (freshness functions, field weighting, boost rules). Would need to be re-created from scratch in any alternative search platform. |
| **Custom skillsets** (document cracking, enrichment) | No | Azure AI Search-specific pipeline definitions. Each skillset encodes domain-specific chunking logic (e.g., how to split PlantUML files) that has no portable representation. |
| **Agent definitions** (Foundry Agent Service) | No | Defined via Python SDK (`azure-ai-projects`) or REST API. Not AGENTS.md, not SKILL.md — Azure-proprietary format with no open standard equivalent. |
| **Integration code** (Python SDK, REST calls) | No | `azure-ai-projects` SDK, Foundry-specific connection types, `ProjectManagedIdentity` auth flows. None of this code transfers to another platform. |
| **RBAC and ACL configuration** | No | Azure Entra ID role assignments and ACL synchronization rules. Every alternative platform has its own authorization model. |
| **MCP endpoint wrappers** | Partial | MCP is an open standard, so the *protocol* is portable. But Foundry's MCP endpoints use `ProjectManagedIdentity` authentication — a Foundry-specific auth type that no IDE client natively supports. |
| **Content** (ADRs, specs, diagrams) | Always | Files in storage. Any platform can read them. |

### Contrast with Copilot Customization Lock-In

The [existing analysis](foundry-iq-comparison.md#what-copilot-investment-could-become-a-dead-end) established that Copilot's lock-in risk is a reformatting cost — the knowledge survives, only file naming changes. The contrast with Foundry is stark:

| Dimension | Copilot Lock-In | Foundry Lock-In |
|-----------|----------------|-----------------|
| **Where customizations live** | Markdown files in git | Azure control plane (portal, SDK, REST API) |
| **Version controlled by default?** | Yes — same git workflow as code | No — requires manual export or IaC discipline |
| **What survives a platform switch** | Content and knowledge (plain text) | Content only — all configuration must be rebuilt |
| **Migration effort** | Rename files, adjust syntax | Rebuild from scratch in new platform |
| **Who can modify** | Any team member with repo access | Users with Azure RBAC roles |
| **Diff and review changes** | Standard git pull request workflow | Azure Activity Log or custom auditing |
| **Cost of switching** | Hours (reformatting) | Weeks to months (re-architecture) |

The key insight: **Copilot lock-in is a formatting problem. Foundry lock-in is a rebuild problem.**

## Why This Lock-In Is Manageable: The Three-Layer Separation

The lock-in described above is real — but it is not a reason to avoid Foundry. It is a reason to **architect the investment correctly** so that the non-portable parts are limited to infrastructure that is inherently platform-specific anyway, while the valuable domain knowledge remains portable.

Option D (Copilot + BYOK), combined with the [living practice customization model](customization-extensibility-governance.md) and OpenSpec, achieves exactly this separation:

| Layer | What Lives Here | Who Controls It | Lock-In Risk | Portable? |
|-------|----------------|-----------------|--------------|-----------|
| **Content** | Architecture artifacts (ADRs, specs, diagrams, YAML) | Architecture practice | None | Always — files in git |
| **Behavioral customization** | Instruction files, skills, agent definitions, scoped rules, workflow conventions | Architecture practice (via inner source PR review) | Reformatting cost only — eliminated entirely by OpenSpec | Yes — tool-agnostic source of truth generates native files for 25+ tools |
| **Model selection** | Which model handles each task (frontier, custom, or free-tier) | Individual architect (guided freedom per DD-05) | None — Option D provides multiple models in the same picker | Yes — BYOK is one model among many; architects are never locked to it |
| **Retrieval infrastructure** | Knowledge bases, scoring profiles, skillsets, indexers | Platform/ML team | High — Azure-specific | No — but derived from portable content, so switching = rebuilding the index, not losing data |

The critical insight is that **each layer's lock-in risk is proportional to its replaceability**:

- Content is always portable — zero risk.
- Behavioral customization *should* be portable — and Option D + OpenSpec makes it so.
- Model selection *should* be flexible — and Option D's multi-model picker makes it so.
- Retrieval infrastructure is inherently platform-specific — but that is acceptable because (a) it is derived from portable content and (b) it is the one layer where Foundry adds genuine value that no IDE-native tool provides (cross-repository search, agentic retrieval, custom chunking).

**This means Foundry lock-in only exists in the layer where Foundry is actually doing something that justifies the investment.** Everything else stays portable.

### How Option D Prevents Model Lock-In

A common concern with custom models is that the team becomes dependent on them. Option D eliminates this risk structurally:

| Scenario | What Happens |
|----------|-------------|
| Custom Foundry model is unavailable | Architects switch to built-in Claude Opus, GPT-4.1, or any other model in the picker. No workflow disruption. |
| Custom model quality degrades | Architects route tasks to frontier models. The custom model is available but not required. |
| Foundry relationship changes | Architects lose the custom model but retain the full Copilot platform with all built-in models. No capability loss for routine work. |
| Better custom model becomes available elsewhere | BYOK supports 7 providers (Anthropic, OpenAI, AWS Bedrock, Google AI Studio, xAI, and OpenAI-compatible). Register the new endpoint; it appears in the picker alongside the old one. |

The key principle from DD-05: **model selection is an architect decision, not an infrastructure constraint.** Option D ensures no architect is ever locked into a single model — the custom Foundry model is an option, not a requirement.

### How Living Practice Customization Prevents Knowledge Lock-In

The [customization extensibility analysis](customization-extensibility-governance.md) establishes that AI customizations are living artifacts that evolve continuously with the practice. The recommended governance model (Option G — Hybrid Inner Source) keeps all behavioral customization in the hands of the architecture practice:

| Property | How It Prevents Lock-In |
|----------|------------------------|
| **Practitioners modify customizations directly** | Domain knowledge is encoded by the people who have it — in Markdown files, not model weights or platform configurations that require ML engineering to change |
| **Changes are reviewable via PR** | Every customization change is versioned, diffable, and auditable. The customization layer is its own documentation. |
| **New practitioners inherit everything** | Clone the repo = inherit 1,100+ lines of accumulated domain knowledge. No per-user configuration, no platform account provisioning. |
| **Customizations compose without conflict** | Global rules + domain-specific overrides + file-type-specific rules compose automatically. No central coordinator required. |

If the customization layer were embedded in Foundry-native constructs (agent definitions via Python SDK, retrieval instructions in knowledge base configs), every one of these properties would be lost. The living practice model depends on customizations being **files that architects can edit** — not configurations stored in a platform's control plane.

## OpenSpec: Cross-Platform Portability for the Customization Layer

[OpenSpec](https://github.com/Fission-AI/OpenSpec) (by Fission AI, MIT license, 39.6k GitHub stars) addresses the remaining portability gap in the customization layer. Even with Copilot's native Markdown files, switching to a different AI tool requires understanding that tool's file conventions. OpenSpec eliminates this friction entirely.

### How OpenSpec Works

OpenSpec maintains a single source of truth in an `openspec/` directory within the repository:

```
openspec/
├── specs/           # Behavioral specifications (tool-agnostic)
│   ├── auth/
│   │   └── spec.md
│   └── architecture/
│       └── spec.md
└── changes/         # Proposed modifications (delta-based)
    └── add-safety-defaults/
        ├── proposal.md
        ├── specs/
        ├── design.md
        └── tasks.md
```

When initialized, OpenSpec generates the native configuration files for whichever AI tools the team uses:

```bash
openspec init --tools github-copilot,cursor,roocode
```

This produces:

| Tool | Generated Files |
|------|----------------|
| GitHub Copilot | `.github/skills/openspec-*/SKILL.md`, `.github/prompts/opsx-*.prompt.md` |
| Cursor | `.cursor/skills/openspec-*/SKILL.md`, `.cursor/commands/opsx-*.md` |
| RooCode | `.roo/skills/openspec-*/SKILL.md`, `.roo/commands/opsx-*.md` |

Switching tools — or supporting multiple tools simultaneously — is a single command:

```bash
openspec init --tools claude,windsurf   # add new tools
openspec update                          # regenerate native files
```

### What OpenSpec Adds to Option D + Living Practice

The pilot already maintains customizations as portable Markdown files. OpenSpec adds value at the **platform abstraction** layer — it makes the customization investment tool-agnostic by design rather than tool-agnostic by convention:

| Capability | Option D + Living Practice (Current) | With OpenSpec Added |
|------------|--------------------------------------|---------------------|
| **Portability** | High — Markdown files converging on open standards (AGENTS.md, SKILL.md) | Maximum — tool-agnostic source with automated generation for any target tool |
| **Multi-tool support** | Manual — rename/restructure files per tool's convention | Automated — `openspec init --tools` generates native files for 25+ tools |
| **Spec-driven workflow** | Not structured — instructions are freeform behavioral guidance | Structured — requirements, scenarios, Given/When/Then format, delta-based changes |
| **Change tracking** | Git history on instruction files | Git history + structured change proposals with proposal/design/tasks artifacts |
| **Learning curve** | None — just write Markdown | Moderate — learn OpenSpec's spec format, commands, and artifact workflow |
| **Overhead** | None | CLI installation, `openspec init/update` maintenance, generated file management |

### What OpenSpec Does Not Address

| Risk | OpenSpec Coverage | Why |
|------|------------------|-----|
| **Knowledge base configuration lock-in** | None | OpenSpec governs behavioral customization, not retrieval infrastructure. Scoring profiles, chunking skillsets, and knowledge base bindings remain platform-specific. |
| **Infrastructure lock-in** (Azure AI Search, Entra ID) | None | Infrastructure decisions are outside OpenSpec's scope — and outside the scope of any customization portability tool. |
| **Model lock-in** | None (not needed) | Option D already solves this — architects choose models from the picker, never locked to one. |

These gaps are acceptable because each is handled by a different component of the recommended architecture:

- Knowledge base and infrastructure lock-in → **accepted as the cost of Foundry's genuine value** (cross-repository search, agentic retrieval). Content is portable; only the index is platform-specific.
- Model lock-in → **eliminated by Option D's BYOK + multi-model picker**.
- Customization lock-in → **eliminated by OpenSpec + living practice model**.

## The Complete Architecture: How the Pieces Compose

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     RECOMMENDED ARCHITECTURE                                │
│                                                                             │
│   ┌──────────────────────────────────────────────────────────────────────┐  │
│   │  LAYER 1: CONTENT (always portable)                                  │  │
│   │  ADRs, OpenAPI specs, PlantUML, YAML metadata — files in git         │  │
│   └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│   ┌──────────────────────────────────────────────────────────────────────┐  │
│   │  LAYER 2: BEHAVIORAL CUSTOMIZATION (portable via OpenSpec)           │  │
│   │  openspec/ specs → generates native files for Copilot, Cursor, etc.  │  │
│   │  Governed by architecture practice via inner source PR review         │  │
│   │  Living artifacts: 1,100+ lines, updated continuously                │  │
│   └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│   ┌──────────────────────────────────────────────────────────────────────┐  │
│   │  LAYER 3: MODEL SELECTION (portable via Option D)                    │  │
│   │  Architect picks per task: 0x free models | frontier | custom BYOK   │  │
│   │  Never locked to one model — BYOK supports 7 providers               │  │
│   └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│   ┌──────────────────────────────────────────────────────────────────────┐  │
│   │  LAYER 4: RETRIEVAL (platform-specific — accepted trade-off)         │  │
│   │  Foundry IQ for cross-repo search IF the workload justifies it       │  │
│   │  Lock-in accepted: indexes are derived from portable content          │  │
│   │  Switching = rebuilding the index, not losing data                    │  │
│   └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

Each layer has a clear owner, a clear portability posture, and a clear lock-in remediation:

| Layer | Owner | Lock-In Risk | Remediation |
|-------|-------|--------------|-------------|
| Content | Architecture practice | None | Files in git — always portable |
| Behavioral customization | Architecture practice (inner source) | Eliminated | OpenSpec generates native files for any tool from tool-agnostic specs |
| Model selection | Individual architect | Eliminated | Option D's multi-model picker — 7 BYOK providers + built-in frontier models |
| Retrieval infrastructure | Platform/ML team | Accepted | Foundry IQ adds genuine value here. Content is portable; only the index is platform-specific. Switching = rebuild cost, not data loss. |

## Suggested Assessment

The lock-in risk from Foundry is real but **fully manageable** when the investment is architected correctly:

1. **Separate what is inherently platform-specific from what should be portable.** Retrieval infrastructure (knowledge bases, scoring profiles, skillsets) is inherently platform-specific — every search platform has its own configuration model. Behavioral customization (instructions, skills, agents) is not inherently platform-specific and should not be locked into any platform.

2. **Keep all behavioral customization as portable Markdown files governed by the architecture practice.** The [living practice model](customization-extensibility-governance.md) ensures customizations evolve at practice speed — minutes, not months. OpenSpec ensures they survive any platform switch.

3. **Give architects full model autonomy.** Option D's multi-model picker means no architect is ever locked to the custom Foundry model. It is an option for domain-specialized tasks, not a requirement for daily work. Built-in models handle 80%+ of routine work at zero incremental cost.

4. **Accept Foundry lock-in only in the retrieval layer — where Foundry adds genuine value.** Cross-repository search, agentic retrieval, and custom chunking are capabilities that no IDE-native tool provides. The lock-in is the cost of that value. It is acceptable because (a) the content being indexed is always portable and (b) rebuilding an index in a new platform is an operational cost, not a knowledge loss.

5. **OpenSpec provides an additional insurance policy.** If the practice needs to support multiple AI tools simultaneously or anticipates tool switching, OpenSpec provides a structured path to portability without maintaining parallel customization files manually. For the current pilot scope, Copilot's native format is already highly portable via open standards convergence (AGENTS.md, SKILL.md), but OpenSpec eliminates the remaining reformatting cost entirely.

The combination of Option D (model portability) + living practice customization (knowledge portability) + OpenSpec (format portability) means that **every layer of the AI investment is either portable or acceptably platform-specific**. Foundry lock-in exists — but only in the one layer where Foundry's value justifies the trade-off.

## Relationship to Other Pages

- [What Does Foundry IQ Actually Require?](foundry-iq-comparison.md) — Covers the operational requirements and "buy vs build" framing. That page asks what Copilot investment could become a dead end; this page asks the inverse for Foundry and shows how Option D + OpenSpec makes the answer acceptable.
- [Customization Extensibility and Governance](customization-extensibility-governance.md) — Establishes that AI customizations are living artifacts requiring practitioner control. This page shows why that living practice model is also a lock-in remediation: customizations that architects maintain in portable files cannot be locked into any single platform.
- [Option D — Hybrid Architecture](option-d-hybrid-architecture.md) — Defines the deployment topology (Copilot + BYOK). This page shows how Option D's multi-model picker eliminates model lock-in as a separate concern from customization lock-in.
- [Build vs Leverage](build-vs-leverage.md) — Argues against building custom infrastructure when native capabilities exist. This page reinforces the pattern: leverage Foundry where it adds unique value (retrieval), keep everything else portable.
- [DD-05: Model Selection Autonomy](../decisions/dd-05-model-selection-autonomy.md) — Establishes that model selection is an architect decision. This page shows how that autonomy also serves as a lock-in prevention mechanism.
- [DD-06: IDE Client Selection](../decisions/dd-06-ide-client-selection.md) — Evaluates the frozen customization problem from a model perspective. This page extends the analysis to the platform format level and shows how OpenSpec resolves it.

## Sources

- [OpenSpec — GitHub Repository](https://github.com/Fission-AI/OpenSpec) — Fission AI, MIT license, v1.3.0, 39.6k stars
- [OpenSpec Supported Tools](https://github.com/Fission-AI/OpenSpec/blob/main/docs/supported-tools.md) — Full list of 25+ supported AI coding assistants
- [OpenSpec Concepts](https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md) — Architecture and philosophy documentation
- [Agent Skills Specification](https://agentskills.io) — Open standard for SKILL.md format
- [AGENTS.md Standard](https://github.com/agentsmd/agents.md) — Cross-platform agent metadata standard
