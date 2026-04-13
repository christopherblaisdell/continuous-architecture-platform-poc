<!-- CONFLUENCE-PUBLISH -->
<!-- CONFLUENCE-URL: -->

# Cost Offset -- How Free Models Subsidize the Custom Model Investment

**TL;DR:** Option D costs less than Option C alone. Copilot's 0x multiplier models (GPT-4.1, GPT-4o, GPT-5 mini, Raptor mini) handle routine work at zero cost — work that Option C routes through the custom Foundry model at per-token cost. BYOK requests do not consume Copilot premium request quotas. The net effect: an architect's custom model token consumption drops by 80%+ because only domain-specialized tasks touch it. The Copilot subscription is not an added expense — it is a cost reduction mechanism.

---

## The Objection

> *"Why would we pay for Copilot AND the custom model? That's two costs instead of one."*

This objection assumes that every AI interaction requires the custom model. It does not. Architecture work falls into two distinct tiers:

| Tier | Examples | % of Daily AI Interactions | Requires Domain-Specific Knowledge? |
|------|----------|---------------------------|-------------------------------------|
| **Routine** | Reformatting tables, generating boilerplate, writing SQL, converting data formats, creating placeholder files, summarizing documents, generating test scaffolding, Markdown cleanup | ~80% | No — any capable model handles these |
| **Domain-specialized** | Cross-service impact analysis, solution design with company-specific service boundaries, data ownership enforcement, ADR generation with organization-specific patterns, safety classification reasoning | ~20% | Yes — benefits from fine-tuned domain knowledge |

Option C routes **all** interactions through the custom model — routine and specialized alike. Every table reformatted, every boilerplate generated, every Markdown file cleaned up costs per-token against the Foundry endpoint.

Option D routes routine work to **free** models and reserves the custom model for work where it adds genuine value.

---

## The Math

### Option C Standalone: Every Token Costs Money

| Parameter | Value |
|-----------|-------|
| Architecture model | Custom Foundry model (fine-tuned) |
| Routine task model | Custom Foundry model (same endpoint) |
| Per-token cost | Enterprise Azure rate (all tokens billable) |
| Engineering cost | Custom VS Code extension: build, test, maintain ($150K-$400K over 18 months) |
| Infrastructure | Cognitive Services, App Service, storage, monitoring, key management |
| Monthly per-architect token estimate at moderate usage | $50-150 (varies by model size and usage volume) |

Every AI interaction — whether it is a multi-service impact analysis or reformatting a YAML table — hits the same billing meter.

### Option D Hybrid: Routine Work Is Free

| Parameter | Value |
|-----------|-------|
| Architecture model | Claude Opus 4.6 (3x, $0.12/prompt) or custom Foundry model (BYOK, per-token) |
| Routine task model | **GPT-4.1, GPT-4o, GPT-5 mini, Raptor mini (0x — $0.00, unlimited)** |
| Copilot subscription | $19/seat (Business) or $39/seat (Enterprise) |
| Engineering cost | $0 — Copilot orchestration is built-in. No custom extension to build. |
| Infrastructure | $0 — Copilot is SaaS. Only the Foundry endpoint requires infrastructure. |
| Custom model token cost | 80%+ lower than Option C — routine work never touches the Foundry endpoint |

### Monthly Cost Comparison Per Architect

The following table models three usage profiles. "Sessions" means a meaningful AI interaction (averaging 4-6 user prompts). Token costs use illustrative rates — actual Azure pricing varies by model size and negotiated contract.

| Usage Profile | Option C (All Custom Model) | Option D (Hybrid) | Savings |
|--------------|---------------------------|-------------------|---------|
| **Light user** (10 sessions/month, 60% routine) | $30-60 (all tokens to Foundry) | $19-39 subscription + $6-12 Foundry tokens (specialized only) = $25-51 | 15-35% lower |
| **Moderate user** (30 sessions/month, 80% routine) | $90-180 (all tokens to Foundry) | $19-39 subscription + $18-36 Foundry tokens = $37-75 | **58-68% lower** |
| **Heavy user** (60 sessions/month, 85% routine) | $180-360 (all tokens to Foundry) | $19-39 subscription + $27-54 Foundry tokens = $46-93 | **74-75% lower** |

!!! note "The Heavier the Usage, the Greater the Savings"
    Option D's advantage compounds with usage volume because more sessions means more routine work shifted to free models. Option C's cost scales linearly with every interaction. Option D's cost scales only with *specialized* interactions.

### The Engineering Cost Offset

The cost comparison above covers only token and subscription expenses. Option C also requires a **custom VS Code extension** — the client that connects the architect to the Foundry model. This is engineering investment:

| Engineering Cost | Option C | Option D |
|-----------------|----------|----------|
| Initial extension build | $50K-$100K (agent mode, tool calling, workspace indexing, instruction files, MCP) | $0 (Copilot provides all orchestration natively) |
| Annual maintenance | $50K-$100K (feature parity with evolving IDE capabilities, bug fixes, security patches) | $0 (GitHub maintains Copilot) |
| Feature gap risk | Every new Copilot capability (sub-agents, memory, new tools) must be re-implemented or forgone | New capabilities arrive automatically with VS Code updates |
| 18-month total | $150K-$400K | $0 |

The engineering budget saved by Option D can be redirected to **model quality** — additional training data curation, fine-tuning iterations, and evaluation — where the custom Foundry model genuinely adds value.

---

## Premium Request Bypass (Verified)

A critical economic advantage confirmed by deep research: **BYOK requests do not count against Copilot premium request quotas.**

> *"Premium requests: Do not count against Copilot premium request quotas"*
> — [Copilot SDK BYOK docs](https://github.com/github/copilot-sdk/blob/main/docs/auth/byok.md)

This means:

1. **No throttling risk.** High-volume agentic workflows through the Foundry model do not consume the monthly premium request allowance.
2. **Cost isolation.** The Copilot subscription covers the orchestration layer and free models. The Foundry endpoint is billed separately by Azure. Each cost is independently manageable and auditable.
3. **Incentive alignment.** Enterprises with negotiated Azure compute rates benefit most — bulk token pricing through Azure is typically cheaper than GitHub's per-prompt premium request pricing at equivalent model quality. The more you use the custom model, the more the direct Azure billing advantage compounds.

---

## The 0x Model Subsidy in Detail

The zero-cost models are not compromise models. They are current-generation frontier models that GitHub offers at no incremental cost as a competitive strategy.

| Model | Multiplier | Capability Level | Architecture Use Cases |
|-------|-----------|-----------------|----------------------|
| **GPT-4.1** | 0x | Strong general reasoning, 1M token context | Document summarization, spec analysis, code generation, refactoring, long-context workspace queries |
| **GPT-4o** | 0x | Strong multimodal, fast response | Quick Q&A, diagram interpretation, Markdown generation, table formatting |
| **GPT-5 mini** | 0x | Compact frontier reasoning | Brainstorming, rapid iteration on ideas, lightweight analysis |
| **Raptor mini** | 0x | Fine-tuned code generation | Code scaffolding, test generation, boilerplate creation |

These models would cost $50-150/month per architect at market per-token rates (via OpenRouter or direct API). Copilot includes them for $0 because Microsoft subsidizes their cost to drive GitHub platform adoption. Option D captures this subsidy.

### What "Free" Actually Means for Workflow

In a typical architecture session, an architect might:

1. **Search and read files** — free (client-side operations, no model invoked)
2. **Ask "summarize this OpenAPI spec"** — free (GPT-4.1 at 0x)
3. **Ask "reformat this table as Markdown"** — free (GPT-4o at 0x)
4. **Ask "generate test scaffolding for this service"** — free (Raptor mini at 0x)
5. **Ask "analyze the cross-service impact of adding this field"** — $0.12 (Claude Opus at 3x) or per-token (Foundry BYOK)
6. **Ask "generate the ADR for this decision"** — $0.12 (Claude Opus at 3x) or per-token (Foundry BYOK)
7. **Ask "clean up the formatting of this document"** — free (GPT-4o at 0x)

Steps 1-4 and 7 are routine. Steps 5-6 are domain-specialized. In Option C, all seven steps would be billed to the Foundry endpoint. In Option D, only steps 5-6 reach the custom model — the rest are free.

---

## Why Option C Cannot Replicate This

Option C cannot offer free routine models because:

1. **No free model tier exists.** The custom VS Code extension connects to one endpoint — the Foundry deployment. There is no "free model picker" in a custom extension unless someone builds one.
2. **Building a multi-model router is engineering scope.** Adding model routing (route routine tasks to a cheap endpoint, specialized tasks to Foundry) requires building what Copilot already provides. This is the DD-04 model routing decision reinvented as custom infrastructure.
3. **No intent-based billing.** Copilot's 0x tier works because Microsoft absorbs the cost as a platform subsidy. An organization running its own endpoints pays for every token, regardless of task complexity.

The only way to get free routine models in the architecture workflow is to use a platform that offers them as part of its business model. GitHub Copilot is that platform.

---

## Team-Level Cost Projection

For a 5-architect team at moderate usage (30 sessions/month each):

| Cost Component | Option C (Annual) | Option D (Annual) |
|---------------|-------------------|-------------------|
| Token/subscription | $54K-$108K | $22K-$45K |
| Engineering (extension) | $100K-$200K | $0 |
| Infrastructure (hosting, monitoring) | $12K-$24K | $6K-$12K (Foundry only, reduced) |
| **Total** | **$166K-$332K** | **$28K-$57K** |
| **Savings** | — | **$138K-$275K (83%)** |

!!! warning "These Are Directional Estimates"
    Exact costs depend on Foundry model size, negotiated Azure rates, usage volume, and engineering team rates. The structural advantage — free routine models, no extension engineering, reduced infrastructure — holds regardless of the specific numbers.

---

## The Redirect Argument

The savings from Option D are not just cost avoidance — they are **budget available for model quality improvement.**

| What Option C Spends On | What Option D Redirects That Budget To |
|------------------------|---------------------------------------|
| Custom extension engineering ($150K-$400K) | Additional training data curation for the Foundry model |
| Routine task token costs ($40K-$80K/year) | Fine-tuning iterations and model evaluation cycles |
| Multi-model routing infrastructure | Experimentation with different fine-tuning strategies |
| Extension maintenance (ongoing) | Continuous model improvement as domain knowledge evolves |

The custom Foundry model is the valuable investment. The custom VS Code extension is the expensive distraction. Option D eliminates the distraction and doubles down on the investment.

---

## Related Pages

- [Option D — Hybrid Architecture](option-d-hybrid-architecture.md) — full BYOK architecture and feature compatibility matrix
- [Model Quality at Budget](model-quality-at-budget.md) — why model tier determines output quality
- [DD-06: IDE Client Selection](../decisions/dd-06-ide-client-selection.md) — why Copilot is the best client for consuming the custom model
- [DD-02: Billing Model](../decisions/dd-02-billing-model.md) — intent-based vs. token-based billing comparison
