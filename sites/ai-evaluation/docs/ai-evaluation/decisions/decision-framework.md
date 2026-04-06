<!-- CONFLUENCE-PUBLISH -->

# Decision Framework

> **You are reading:** Layer 2 — Toolchain Decision Framework | [Home](../../index.md)
>
> This document structures the four toolchain decisions (what to buy/build). For the practice-level operating model (how the team works with AI), see [Practice Strategy](../practice-strategy.md) (Layer 1).

## Toolchain Decisions for AI Platform Selection

Selecting an AI platform for architecture practice is not a single decision — it is four interconnected but independently analyzable decisions. This framework decomposes the monolithic "which toolchain?" question into its constituent architectural concerns, analyzes each on its own merits, and then composes the results into evaluated platform options.

---

## Why Decompose?

The original evaluation compared three toolchains as monolithic options: GitHub Copilot, Roo Code + Kong AI, and Claude Code. But this conflated several independent architectural questions:

| Conflated Question | Independent Decision |
|-------------------|---------------------|
| "Should we build custom MCP servers?" | [DD-01: Content Injection Strategy](dd-01-content-injection.md) |
| "Where does context injection happen?" | [DD-02: Injection Location](dd-02-injection-location.md) |
| "How should we pay for AI processing?" | [DD-03: Billing Model](dd-03-billing-model.md) |
| "Who do we buy AI from?" | [DD-04: AI Processing Provider](dd-04-ai-provider.md) |

A stakeholder who says "we should use Roo Code + Kong with custom MCP servers" is actually expressing preferences on all four questions simultaneously. Decomposing them allows each to be evaluated with precision.

---

## The Reinventing-the-Wheel Question

One approach to enterprise context injection is building custom MCP servers to inject proprietary context (Confluence knowledge bases, CMDB data, ServiceNow tickets, internal APIs) into AI workflows.

The critical question is whether this **reinvents capabilities that native toolchains already provide**:

| Capability | Custom MCP Approach | Native Copilot Approach |
|-----------|-------------------|----------------------|
| Workspace context | Custom RAG pipeline with Qdrant | Built-in semantic indexing (server-side, free) |
| Architecture standards | Custom MCP server serving rules | `copilot-instructions.md` loaded automatically |
| Ticket access | Custom MCP server for JIRA API | Local MCP server (already built) or file-based |
| Code analysis | Custom embedding + retrieval | Native file reads + workspace search |

DD-01 addresses this directly: for each content type, is the gap caused by a toolchain limitation (justifying custom MCP) or by an investment gap (the instruction/metadata file has not been written yet)?

---

## Decision Dependency Map

The four decisions are not fully independent — they have directional dependencies:

```
DD-04: AI Provider
  ↓ constrains
DD-03: Billing Model (some providers only offer one model)
  ↓ influences
DD-02: Injection Location (server-side injection adds infrastructure cost)
  ↓ scoped by
DD-01: Content Injection (what to inject determines where/how)
```

**Read order recommendation:** DD-01 first (establishes what context injection is needed), then DD-02 (where it happens), then DD-03 (how you pay), then DD-04 (from whom).

---

## How Decisions Map to Decision Points

These decision documents map to the existing [Decision Points](https://architecture.novatrek.cc) framework:

| Decision Document | Maps to Decision Points |
|-------------------|------------------------|
| DD-01: Content Injection Strategy | DP-09 (Context Enrichment), DP-19 (Hybrid MCP) |
| DD-02: Injection Location | DP-19 (MCP Location), DP-01 (Buy vs Build) |
| DD-03: Billing Model | DP-02 (Intent-Based vs Token) |
| DD-04: AI Processing Provider | DP-03 (Toolchain Selection), DP-10 (Vendor Lock-In) |

---

## How Decisions Compose Into Platform Options

After analyzing each decision independently, the results compose into [Platform Options](../platform-options.md) — side-by-side configurations evaluated against systematic criteria. Each platform option represents a coherent combination of choices across all four decisions.

| | Option A: Lean | Option B: Hybrid | Option C: Full Build |
|---|---|---|---|
| DD-01 Content Injection | Native workspace + instructions | Native + targeted MCP for external data | Full custom MCP pipeline + RAG |
| DD-02 Location | Workstation only | Workstation + selective server | Server-hosted AI orchestration |
| DD-03 Billing | Intent-based (fixed) | Intent-based + consumption | Token-based (variable) |
| DD-04 Provider | GitHub | GitHub + Azure AI Foundry | Azure AI Foundry or Anthropic direct |
| **Monthly cost/seat** | **~$39-50** | **~$70-130** | **~$150-350** |
| **Engineering investment** | None | 2-4 dev-months | 6-12 dev-months |
| **Time to value** | Now | 3-6 months | 6-18 months |

See [Platform Options](../platform-options.md) for the full scored comparison.

---

## Decision Documents

<div class="grid cards" markdown>

-   **DD-01: Content Injection Strategy**

    ---

    Do we need custom MCP servers to inject enterprise context, or does native workspace indexing and instructions suffice?

    [:octicons-arrow-right-24: Read DD-01](dd-01-content-injection.md)

-   **DD-02: Injection Location**

    ---

    Should content injection happen on the developer workstation or on a server?

    [:octicons-arrow-right-24: Read DD-02](dd-02-injection-location.md)

-   **DD-03: Billing Model**

    ---

    Intent-based billing vs token-based billing vs subscription ceiling — what economic model fits?

    [:octicons-arrow-right-24: Read DD-03](dd-03-billing-model.md)

-   **DD-04: AI Processing Provider**

    ---

    GitHub, Anthropic, Microsoft Azure AI Foundry, or Kong/OpenRouter — who do we buy AI from?

    [:octicons-arrow-right-24: Read DD-04](dd-04-ai-provider.md)

</div>
