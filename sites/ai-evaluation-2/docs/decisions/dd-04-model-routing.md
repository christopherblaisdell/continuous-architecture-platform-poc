<!-- CONFLUENCE-PUBLISH -->
<!-- CONFLUENCE-URL: https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2614724648/DD-04+Model+Routing -->

# DD-04: Model Routing

| | |
|-----------|-------|
| **Status** | Decided — model routing is platform-native; transparency trade-off accepted |
| **Date** | 2026-04-07 |
| **Scope** | How are different AI models selected and routed for different task types? |
| **Depends on** | DD-03 (AI Provider) |

---

## Problem Statement

Architecture work spans a range of task complexity — from quick triage and formatting to deep multi-service analysis and solution design. Different model tiers are appropriate for different tasks. The question is whether model routing requires custom infrastructure or is handled natively by the selected platform.

## How Each Option Handles Model Routing

| Option | Model Routing Mechanism | Infrastructure Required |
|--------|------------------------|------------------------|
| **Option A (Copilot)** | Architect selects model per session. GPT-4o/4.1 (0x — free, unlimited) for routine tasks; Claude Opus 4.6 (3x) for architecture work. Built-in. | None |
| **Option B (Roo Code + Kong)** | Kong gateway routes requests to configured model providers. Operator configures routing rules. Full per-request model attribution and token-level cost visibility. | Kong gateway provisioning and maintenance |
| **Option C (Bespoke Agent)** | Custom routing logic in the agent framework. Engineering team configures model tiers. Complete control over which model handles every inference. | Custom development and ongoing maintenance |
| **Option D (Hybrid — BYOK)** | All of Option A, plus: organization registers a custom Azure AI Foundry endpoint via BYOK. Architect selects the custom model alongside built-in models in the same model picker. BYOK requests bypass premium quotas and bill at Azure consumption rates. | Foundry endpoint provisioning + admin registration (one-time). No IDE infrastructure. |

With Option A, the architect chooses the model when starting a session — frontier model for design work, routine model for everyday tasks. With Option D, the architect gains an additional choice: a domain-specialized custom model trained on enterprise architecture patterns. With Options B and C, the operator or engineer controls routing at a finer granularity.

---

## Model Transparency: What You Control vs What You Don't

This is the most important honest caveat in the evaluation.

### The Criticism

When an architect selects "Claude Opus 4.6" in Copilot, that selection governs the **primary reasoning model** for the session. However, Copilot's agentic loop involves many inferences beyond the primary reasoning step — tool call dispatch, file read summarization, context assembly, sub-agent coordination, and response synthesis. Microsoft's orchestration layer decides which model handles each of these internal steps. The architect has no visibility into or control over these per-inference routing decisions.

This means:

- **You select the frontier model**, but Microsoft determines how much of the agentic loop actually runs on it
- **You cannot verify** which model handled which part of your session — Copilot provides no per-request model attribution
- **Microsoft has a financial incentive** to route non-critical inferences to cheaper models — this is standard practice across all AI platforms offering bundled pricing, not unique to Microsoft

### Why This Is a Real Trade-Off, Not a Flaw

The criticism is valid but incomplete. The question is not "does Copilot use Opus for every inference?" — no reasonable person would expect or want that. The question is: **does the output quality reflect frontier-model reasoning where it matters?**

The evidence from the architecture practice pilot suggests it does:

- Solution designs demonstrate multi-file reasoning across 10-20 workspace files
- Domain rules from `copilot-instructions.md` are enforced consistently (safety defaults, data ownership boundaries, MADR format)
- Cross-service impact analysis traces changes through OpenAPI specs, source code, and metadata
- Long-context fidelity is maintained across sessions with 100K+ token contexts

If Microsoft were routing the primary reasoning to a budget model, these outputs would not be achievable — budget models demonstrably fail at multi-file synthesis, domain rule enforcement, and structured document generation (see [Model Quality at Budget](../evidence/model-quality-at-budget.md)).

### The Transparency Spectrum

Each option occupies a different position on the visibility-vs-convenience spectrum:

| Dimension | Option A (Copilot) | Option B (Roo Code + Kong) | Option C (Bespoke Agent) | Option D (Hybrid — BYOK) |
|-----------|-------------------|---------------------------|--------------------------|--------------------------|
| Model selection | Per-session | Per-request | Per-request | Per-session (built-in) + per-session (custom BYOK) |
| Per-inference visibility | None — opaque | Full — every API call logged with model, tokens, cost | Full — custom code, full control | Opaque for built-in models; full visibility for BYOK requests (Azure logs token usage, cost, latency) |
| Cost attribution | Per user prompt (3x multiplier for Opus) | Per token, per request | Per token, per request | Per user prompt for built-in; per token for BYOK (Azure consumption) |
| Routing control | Microsoft's orchestration | Operator-configured rules | Engineer-written logic | Microsoft's orchestration for built-in; organization controls BYOK endpoint and model version |
| Financial incentive alignment | Microsoft absorbs cost overruns (good for user); Microsoft optimizes routing to manage cost (industry-standard practice for bundled pricing, opaque to user) | Operator pays exactly what they use (full alignment) | Engineer controls everything (full alignment) | Built-in models: same as A. BYOK: organization pays Azure consumption directly (full alignment on custom model) |

### Why the Trade-Off Is Acceptable for This Practice

Three factors make Copilot's opacity an acceptable trade-off rather than a disqualifying flaw:

1. **Output quality is the observable metric, not model attribution.** The evaluation scores each option on EF-04 (Architecture Output Quality at Operating Budget). If Copilot's output quality degrades — regardless of the reason — the score drops and the recommendation changes. The architect does not need to know which model produced which inference; they need to know the final output meets their quality bar.

2. **The alternative costs more and delivers less convenience.** Option B provides full transparency but at $100-200/month per architect for equivalent model quality. Option C provides full control but requires weeks of engineering. The transparency premium is real — the question is whether it is worth 3-5x the cost.

3. **The risk is self-correcting.** If Microsoft degrades Copilot's model routing to the point where architecture output quality drops noticeably, the architect observes this directly in their work. Unlike a backend system where degradation can go undetected, architecture output is reviewed by a human every session. Quality degradation triggers an immediate re-evaluation — and Options B and C remain available as fallbacks.

!!! note "What Would Change This Assessment"
    If GitHub introduced per-request model attribution (which model handled which inference), this caveat would be eliminated entirely. If a future Copilot update visibly degraded architecture output quality, this evaluation would need to be re-scored. Both are observable events.

---

**See also:**

- [DD-03: AI Provider](dd-03-ai-provider.md) — Provider selection that determines model routing
- [DD-05: Model Selection Autonomy](dd-05-model-selection-autonomy.md) — How guided freedom extends to BYOK models
- [DD-06: IDE Client Selection](dd-06-ide-client-selection.md) — Which IDE client consumes the custom Foundry model
- [Option D — Hybrid Architecture](../evidence/option-d-hybrid-architecture.md) — Full BYOK analysis including feature compatibility and risk assessment
- [Model Quality at Budget](../evidence/model-quality-at-budget.md) — Why the model tier matters more than the routing mechanism
- [Platform Landscape](../evidence/platform-landscape.md) — Multi-model flexibility comparison (EF-07) across five platforms
