<!-- CONFLUENCE-PUBLISH -->
<!-- CONFLUENCE-URL: -->

# Option D -- Hybrid Architecture (Copilot + Custom Foundry Model via BYOK)

!!! abstract "TL;DR"
    Option D combines Option A (GitHub Copilot as the development client) with Option C's investment (a custom fine-tuned model in Azure AI Foundry) by using GitHub Copilot's BYOK feature. Architects get frontier models for everyday work at zero incremental cost, and switch to the custom Foundry model when domain specialization adds value -- all in the same model picker, with no custom extension or separate UI.

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
| Agent mode (tool calling, file ops, terminal) | YES | **Expected YES** | Agent mode is a mode of Copilot Chat; model receives tool-calling requests from the client. Requires model to support function calling. |
| MCP servers | YES | **Expected YES** | MCP is a Chat feature; the client orchestrates MCP calls and injects results into model context. |
| Instruction files (.instructions.md, copilot-instructions.md) | YES | **Expected YES** | Instructions are injected by the client before sending to any model. |
| Workspace context (indexing) | YES | **Expected YES** | Client-side retrieval; the model receives context regardless of source. |
| Model coexistence (switch mid-session) | YES | **YES (verified)** | BYOK models appear in the same picker as built-in models. |
| Copilot CLI | YES | **YES (verified)** | CLI BYOK launched April 7, 2026 with additional offline mode. |
| Inline code completions | YES | **NO** | BYOK is explicitly scoped to Chat and CLI only. |
| Copilot coding agent (cloud) | YES | **Likely NO** | Cloud agent runs on GitHub infrastructure, not the user's IDE. |
| Copilot code review (PR review) | YES | **Not verified** | No documentation confirms or denies. |

**Verification key:** "Verified" = confirmed by GitHub Docs primary source. "Expected YES" = logically follows from confirmed architecture (client-side orchestration sends context to whichever model is selected). "Not verified" = no documentation found either way.

### Why "Expected YES" Is a Reasonable Inference

Copilot's architecture separates **client orchestration** from **model routing**. The VS Code extension handles:

- Tool definitions and tool-call dispatch (file read, terminal, search, etc.)
- Instruction file discovery and injection
- Workspace context retrieval and chunking
- MCP server connection and result injection

All of this happens **before** the prompt reaches any model. The model receives a fully-assembled prompt with tool definitions, context, and instructions -- then returns a response that may include tool calls. This is the same pattern regardless of whether the model is Claude Opus (built-in) or a custom Foundry model (BYOK). The only requirement is that the BYOK model supports **tool calling / function calling** and **streaming** -- which are documented requirements for CLI BYOK and are implied for Chat BYOK.

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

BYOK is an enterprise-level feature:

| Plan | Monthly Cost | Premium Requests | BYOK Support |
|------|-------------|-----------------|--------------|
| Copilot Free | $0 | 50 | NO |
| Copilot Student | Free | 300 | NO |
| Copilot Pro | $10/seat | 300 | NO |
| Copilot Pro+ | $39/seat | 1,500 | NO |
| **Copilot Business** | **$19/seat** | **300/user** | **YES (enterprise admin)** |
| **Copilot Enterprise** | **$39/seat** | **1,000/user** | **YES (enterprise admin)** |

BYOK requires **GitHub Enterprise Cloud** with a Business or Enterprise Copilot plan. The enterprise admin registers API keys; organization members see the models in their picker.

Source: [Plans for GitHub Copilot](https://docs.github.com/en/copilot/get-started/plans)

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

BYOK is in **public preview** as of April 2026. The docs state: *"The ability to bring your own API keys to GitHub Copilot is in public preview and subject to change."*

### Risk Assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| BYOK removed or changed during preview | Medium | Fallback: CLI BYOK (individual, launched April 7 2026). Alternative: use custom model via separate tool outside Copilot. GitHub's trajectory is toward more model flexibility, not less. |
| Fine-tuned model quality varies | Low | GitHub warns about this explicitly. Mitigate with thorough testing before production use. |
| Inline completions not supported | Low | Acceptable -- inline completions use GitHub's optimized models and benefit from their fine-tuning. Domain context is more valuable in chat/agent mode. |
| Enterprise Cloud required | Low | NBCU already uses GitHub Enterprise Cloud. |
| Data transit through GitHub | Medium | Prompts likely route through GitHub's infrastructure (GitHub holds the API key). Assess data classification of prompt content against GitHub's DPA and data residency policies. |
| Premium request billing for BYOK unclear | Low | Not documented whether BYOK requests consume premium requests. Logically, users pay the provider directly, so premium requests should not be consumed -- but verify before budgeting. |

### What Is NOT a Risk

- **Model availability in Foundry**: Troy's team is actively building this. The model will exist.
- **Copilot agent mode capability**: Extensively proven in this evaluation's NovaTrek pilot.
- **Instruction file and MCP support**: Proven in production use during the pilot.

## Why Not "A Absorbs C"?

This page deliberately frames the recommendation as **Option D (Hybrid)** rather than "Option A absorbs Option C" for three reasons:

1. **Credit, not conflict**: Troy's Foundry investment is a valuable component of Option D, not a redundant effort that gets absorbed. The custom model is what makes Option D better than Option A alone.

2. **Complementary strengths**: Option A provides the orchestration platform and frontier models. Option C provides the domain-specialized model. Neither is complete without the other. Option D is genuinely new -- not A with C bolted on.

3. **Shared ownership**: Option D is the team's recommendation, not one person's victory over another. Matt and Greg see collaboration. Troy and James see their work validated. Architecture practice gets the best available tooling.

## Integration Path

See [Copilot Rollout Roadmap](../framework/copilot-rollout-roadmap.md) for the phased deployment plan. Option D adds a new phase after the initial Copilot rollout:

1. **Phase 0-2**: Roll out Copilot with built-in models (immediate value)
2. **Phase 3**: Troy's team completes Foundry model training and deployment
3. **Phase 4**: Enterprise admin registers Foundry endpoint via BYOK
4. **Phase 5**: Architecture practice tests BYOK model in agent mode, establishes guidance for when to use custom vs built-in models
5. **Steady state**: Architects choose the right model per task from the unified picker

## Related Pages

- [DD-05: Model Selection Autonomy](../decisions/dd-05-model-selection-autonomy.md) -- how architects choose models per task
- [DD-04: Model Routing](../decisions/dd-04-model-routing.md) -- how requests route to different model providers
- [Copilot Rollout Roadmap](../framework/copilot-rollout-roadmap.md) -- phased deployment plan
- [What Does Foundry IQ Actually Require?](foundry-iq-comparison.md) -- operational requirements for Option C standalone
- [Scoring Results](../framework/scoring-results.md) -- weighted scoring matrix
