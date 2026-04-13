<!-- CONFLUENCE-PUBLISH -->
<!-- CONFLUENCE-URL: -->

# Option D Hybrid Architecture -- Copilot Plus Custom Foundry Model via BYOK

**TL;DR:** Option D combines Option A (GitHub Copilot as the development client) with Option C's investment (a custom fine-tuned model in Azure AI Foundry) by using GitHub Copilot's BYOK feature. Architects get frontier models for everyday work at zero incremental cost, and switch to the custom Foundry model when domain specialization adds value -- all in the same model picker, with no custom extension or separate UI.

---

## What Is Option D?

Option D is not a new platform. It is a **deployment topology** that composes the strengths of Options A and C while avoiding their weaknesses.

| Component | Source | Role in Option D |
|-----------|--------|-----------------|
| IDE client and orchestration | Option A (GitHub Copilot) | Agent mode, tool calling, MCP, instruction files, workspace indexing |
| Frontier models (Claude, GPT, Gemini) | Option A (built-in) | Routine architecture tasks at zero or low multiplier cost |
| Custom fine-tuned model | Option C (Azure AI Foundry) | Domain-specialized tasks where company-specific context improves output |
| Integration bridge | BYOK (Bring Your Own Key) | Enterprise admin registers Foundry endpoint; model appears in Copilot's picker |

The key insight: Copilot is not just a model -- it is an **orchestration platform** with 7+ IDE-integrated tools (file read/write, terminal, search, memory, sub-agents, MCP). The model is swappable; the orchestration is not. Option D keeps the best orchestration layer and adds the best custom model.

## How BYOK Works

### Architecture

```
Architect (VS Code)
    |
    |  selects model from picker
    v
GitHub Copilot Client (VS Code extension)
    |
    |  orchestrates: tool calls, file reads,
    |  instruction files, workspace context
    |
    +--- Built-in model route ---> GitHub-hosted Claude/GPT/Gemini
    |                              (standard premium request billing)
    |
    +--- BYOK model route -------> Azure AI Foundry endpoint
                                   (per-token via enterprise API key)
```

### Enterprise Admin Setup (Verified)

1. Enterprise owner navigates to **Enterprise > AI Controls > Copilot > Configure allowed models > Custom models tab**
2. Clicks **Add API key**
3. Selects provider: **Microsoft Foundry**
4. Enters a display name (shown in the model picker), the API key, and the **deployment URL**
5. Adds a **Model ID** for the deployed model
6. Clicks Save

The model then appears at the bottom of every organization member's model picker, under the enterprise name. Different deployment URLs require separate API key entries.

Source: [Using your LLM provider API keys with Copilot](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-enterprise/use-your-own-api-keys)

### Organization Scoping (Verified)

Enterprise admins can control which organizations see the custom model:

- **Allow for all organizations** -- every org in the enterprise gets access
- **Choose per organization** -- check/uncheck specific orgs

This means the architecture practice can have access to the custom model without exposing it to engineering teams (or vice versa).

## Supported Providers (Verified)

Seven BYOK providers are supported as of April 2026:

| Provider | Notes |
|----------|-------|
| Anthropic | Direct API key |
| AWS Bedrock | For models deployed on Bedrock |
| Google AI Studio | Google-hosted models |
| **Microsoft Foundry** | **Our target -- custom/fine-tuned models deployed as endpoints** |
| OpenAI | Direct API key |
| OpenAI-compatible providers | Any endpoint implementing the OpenAI Chat Completions API |
| xAI | Grok models |

**Fine-tuned models are supported**, with a documented caveat: *"Fine-tuned models are also supported, but functionality and quality of results can vary depending on the fine-tuning setup."*

Source: [Enterprise BYOK docs](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-enterprise/use-your-own-api-keys)

## Feature Compatibility Matrix

| Feature | Built-in Models | BYOK Model | Notes |
|---------|----------------|------------|-------|
| Copilot Chat (ask/edit modes) | YES | **YES (verified)** | BYOK explicitly scoped to "Copilot Chat and CLI" |
| Agent mode (tool calling, file ops, terminal) | YES | **YES (verified)** | Sub-agents automatically inherit BYOK provider configuration. Model must support tool calling and streaming. |
| MCP servers | YES | **YES (verified)** | MCP operates at the client/orchestration layer. VS Code uses fully qualified tool names to prevent conflicts between built-in and MCP tools when using BYOK models. |
| Instruction files (.instructions.md, copilot-instructions.md) | YES | **YES (verified)** | Copilot coding agent reads both `copilot-instructions.md` and `.instructions.md` files. Instructions are deduplicated to save context. |
| Workspace context (indexing) | YES | **YES (verified)** | Client-side Tree-sitter AST indexing assembles context before sending to any model. BYOK models benefit from the same `#codebase` / `@workspace` retrieval as built-in models. |
| Model coexistence (switch mid-session) | YES | **YES (verified)** | Language Models editor provides centralized view of all models: built-in, extension-provided, and BYOK. |
| Copilot CLI | YES | **YES (verified, GA)** | CLI BYOK reached General Availability in February 2026. Supports offline mode (`COPILOT_OFFLINE=true`) for air-gapped environments. |
| Inline code completions | YES | **YES (verified, with caveat)** | Developers route completions via "Change Completions Model" command. Caveat: heavyweight models may introduce perceptible latency; lightweight models (e.g., GPT-4o-mini, Qwen 2.5 Coder) recommended for inline completions. |
| Copilot coding agent (cloud) | YES | **YES (verified)** | Cloud agent supports BYOK when admin registers the endpoint centrally. Prompts route from GitHub's cloud infrastructure outbound to the enterprise's Foundry endpoint. |
| Copilot code review (PR review) | YES | **YES (verified)** | Agentic code review fully supports BYOK, including closed-loop fix generation. Sub-agents inherit the BYOK configuration. |

**Verification key:** "Verified" = confirmed by GitHub Docs or official changelog primary source. All features in this table were verified via deep research (April 2026).

## Cost Model: The Hybrid Subsidy

The most common objection is: *"Why pay for Copilot AND the custom model?"*

The answer: **the Copilot subscription reduces custom model costs by 80%+.**

### The Math

Without Copilot (Option C alone):

- Every architect query hits the custom Foundry model at per-token cost
- This includes routine tasks: formatting tables, generating boilerplate, simple Q&A, code generation, refactoring
- Estimated 80%+ of daily AI interactions are routine, not domain-specialized

With Copilot (Option D):

- Routine tasks use **0x multiplier models** (GPT-4.1, GPT-4o, GPT-5 mini, Raptor mini) -- unlimited, zero incremental cost
- Domain-specialized tasks use the **custom Foundry model** (BYOK) -- per-token via enterprise API key
- Net effect: custom model token consumption drops by 80%+ because routine work never touches it

### Model Cost Tiers (April 2026)

| Model | Multiplier | Cost per prompt (Copilot) | When to use |
|-------|-----------|--------------------------|-------------|
| GPT-4.1, GPT-4o, GPT-5 mini | **0x** | **$0.00** (included) | Routine: formatting, boilerplate, simple Q&A |
| Raptor mini | **0x** | **$0.00** (included) | Routine: code generation with fine-tuned quality |
| Claude Haiku 4.5, Gemini 3 Flash, GPT-5.4 mini | 0.25-0.33x | $0.01-0.01 | Mid-tier: moderate reasoning tasks |
| Claude Sonnet 4.6, GPT-5.4 | 1x | $0.04 | Heavy reasoning, complex analysis |
| **Claude Opus 4.6** | **3x** | **$0.12** | Deep architecture analysis (current pilot model) |
| Custom Foundry Model (BYOK) | N/A | Per-token (enterprise rate) | Domain-specialized: company-specific context |

The 0x tier now includes **four models** -- meaning even more routine work can be handled at zero cost compared to earlier evaluations.

## Plan Compatibility (Verified)

BYOK is available across **all plans**, but the access method and governance model differ:

| Plan | Monthly Cost | Premium Requests | BYOK Access Method | Admin Governance |
|------|-------------|-----------------|-------------------|------------------|
| Copilot Free | $0 | 50 | VS Code extensions (e.g., AI Toolkit), CLI env vars | Individual only |
| Copilot Pro | $10/seat | 300 | VS Code extensions, CLI env vars | Individual only |
| Copilot Pro+ | $39/seat | 1,500 | VS Code extensions, CLI env vars | Individual only |
| **Copilot Business** | **$19/seat** | **300/user** | **Centralized Enterprise/Org UI + CLI + extensions** | **Organization-wide key distribution** |
| **Copilot Enterprise** | **$39/seat** | **1,000/user** | **Centralized Enterprise/Org UI + CLI + extensions** | **Enterprise-wide, cross-org scoping** |
| No subscription (SDK) | $0 | N/A | Copilot SDK direct integration | Programmatic only |

**Key insight:** Individual developers on Free, Pro, or Pro+ can use BYOK models via VS Code extensions and CLI environment variables without any enterprise overhead. The Business and Enterprise plans add **centralized administration** — the admin registers API keys once and organization members see the models automatically.

**Premium request impact:** BYOK requests **do not count against Copilot premium request quotas**. The inference cost is paid directly to the model provider, completely bypassing GitHub's SaaS billing. This means enterprises with negotiated Azure compute rates can route high-volume agentic workflows through their own Foundry endpoints without risk of throttling.

Source: [Plans for GitHub Copilot](https://docs.github.com/en/copilot/get-started/plans), [Copilot SDK BYOK docs](https://github.com/github/copilot-sdk/blob/main/docs/auth/byok.md)

## CLI BYOK: Individual-Level Access (New)

On April 7, 2026, GitHub launched **CLI BYOK** -- a separate, individual-level BYOK mechanism for Copilot CLI:

| Aspect | Enterprise BYOK (Chat) | CLI BYOK |
|--------|----------------------|----------|
| Configuration | Enterprise admin (AI controls panel) | Individual developer (environment variables) |
| Requires Enterprise Cloud | Yes | No |
| Requires GitHub auth | Yes | No (optional) |
| Offline mode | No | Yes (`COPILOT_OFFLINE=true`) |
| Supported providers | 7 (see above) | 3 (OpenAI-compatible, Azure OpenAI, Anthropic) |
| Model requirements | Not documented | Tool calling + streaming, 128k+ context recommended |

CLI BYOK means architects can use the custom Foundry model from the terminal even without Enterprise Cloud -- useful for testing and evaluation.

Source: [Copilot CLI BYOK docs](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/use-byok-models), [Changelog](https://github.blog/changelog/2026-04-07-copilot-cli-now-supports-byok-and-local-models/)

## Preview Status and Risks

### Current Status

BYOK exists in a **fragmented maturity state** as of April 2026:

| Surface | Status |
|---------|--------|
| Enterprise admin UI (Chat/IDE) | **Public Preview** — *"The ability to bring your own API keys is currently in public preview and is subject to change."* |
| Copilot CLI | **General Availability** — CLI reached GA in February 2026 with full BYOK support including offline mode. |
| Copilot SDK | **Technical Preview** — programmatic BYOK access, does not require a Copilot subscription. |

The steady cadence of announcements (SDK in January 2026, CLI GA in February 2026, CLI BYOK in April 2026) indicates deliberate maturation toward full GA across all surfaces.

### Risk Assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| Enterprise admin BYOK removed or changed during preview | Medium | Fallback: CLI BYOK is already GA. VS Code extension BYOK works on all plans. GitHub's trajectory is toward more model flexibility, not less — SDK, CLI, and IDE all trending toward BYOK support. |
| Fine-tuned model quality varies | Medium | GitHub explicitly warns: *"quality of results and functionality may vary based on your specific fine-tuning setup."* Fine-tuned models may disrupt Copilot's orchestration cadence if instruction-following capabilities are degraded. Thorough testing in agent mode is essential before production use. |
| No Entra ID / Managed Identity support | **High** | BYOK requires **static API keys only** — no Entra managed identities, no service principals, no OIDC/SAML federation. Bearer tokens are supported but cannot auto-refresh (no callback mechanism). This complicates zero-trust security postures. Mitigation: manage key rotation via Azure Key Vault; accept static keys as a preview-period limitation likely to be resolved at GA. |
| Audit logging gap | Medium | BYOK usage is **tracked by the provider, not GitHub**. GitHub's audit log API does not capture BYOK prompt contents or token consumption. Compliance teams must integrate directly with Azure AI Foundry's audit logging. |
| Inline completion latency with heavyweight models | Low | BYOK inline completions are supported but heavyweight models (Claude Opus) may introduce perceptible lag. Mitigate by routing inline completions to lightweight models (GPT-4o-mini, Qwen 2.5 Coder) optimized for low-latency streaming. |
| Enterprise Cloud required for centralized admin | Low | NBCU already uses GitHub Enterprise Cloud. Individual BYOK works on all plans without Enterprise Cloud. |
| Data transit architecture varies by surface | Medium | IDE BYOK establishes a **direct connection** to the provider, bypassing GitHub's servers. Cloud agent routes prompts **through GitHub's infrastructure** outbound to the Foundry endpoint. Assess data classification for cloud agent workflows against GitHub's DPA. |
| EMU restrictions on cloud features | Low | Enterprise Managed User environments cannot use the cloud coding agent with BYOK. Local IDE and CLI BYOK remain functional. |

### What Is NOT a Risk

- **Model availability in Foundry**: The Foundry team is actively building this. The model will exist.
- **Copilot agent mode capability**: Verified -- sub-agents automatically inherit BYOK configuration, and the full agentic loop works with custom models.
- **Instruction file and MCP support**: Verified -- both instruction files and MCP are consumed by BYOK models identically to built-in models.
- **Premium request consumption**: Verified -- BYOK requests do not count against Copilot premium request quotas.
- **Inline completions**: Verified -- BYOK models can serve inline completions via the "Change Completions Model" command.
- **Cloud coding agent and code review**: Verified -- both support BYOK when the admin registers the endpoint centrally.

## Why Not "A Absorbs C"?

This page deliberately frames the recommendation as **Option D (Hybrid)** rather than "Option A absorbs Option C" for three reasons:

1. **Credit, not conflict**: The Foundry team's investment is a valuable component of Option D, not a redundant effort that gets absorbed. The custom model is what makes Option D better than Option A alone.

2. **Complementary strengths**: Option A provides the orchestration platform and frontier models. Option C provides the domain-specialized model. Neither is complete without the other. Option D is genuinely new -- not A with C bolted on.

3. **Shared ownership**: Option D is the team's recommendation, not one group's victory over another. The architecture practice and the Foundry team both see their work validated. Everyone gets the best available tooling.

## Integration Path

See [Copilot Rollout Roadmap](../framework/copilot-rollout-roadmap.md) for the phased deployment plan. Option D adds a new phase after the initial Copilot rollout:

1. **Phase 0-2**: Roll out Copilot with built-in models (immediate value)
2. **Phase 3**: The Foundry team completes model training and deployment
3. **Phase 4**: Enterprise admin registers Foundry endpoint via BYOK
4. **Phase 5**: Architecture practice tests BYOK model in agent mode, establishes guidance for when to use custom vs built-in models
5. **Steady state**: Architects choose the right model per task from the unified picker

## Related Pages

- [DD-05: Model Selection Autonomy](../decisions/dd-05-model-selection-autonomy.md) -- how architects choose models per task
- [DD-04: Model Routing](../decisions/dd-04-model-routing.md) -- how requests route to different model providers
- [Copilot Rollout Roadmap](../framework/copilot-rollout-roadmap.md) -- phased deployment plan
- [What Does Foundry IQ Actually Require?](foundry-iq-comparison.md) -- operational requirements for Option C standalone
- [Customization Portability: Option D + OpenSpec](customization-lock-in-foundry-vs-portable.md) -- how Option D, living practice customization, and OpenSpec compose to neutralize Foundry lock-in across four layers
- [Scoring Results](../framework/scoring-results.md) -- weighted scoring matrix
