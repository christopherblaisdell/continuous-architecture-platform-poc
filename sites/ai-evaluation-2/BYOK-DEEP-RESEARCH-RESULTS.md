# BYOK Deep Research Results

**Date:** 2026-04-09
**Researcher:** AI Agent (Claude Opus 4.6 via GitHub Copilot)
**Purpose:** Validate BYOK claims before publishing Option D (Hybrid) content

## Key Discovery: Two Distinct BYOK Features

GitHub Copilot now has **two separate BYOK mechanisms**, not one:

| Feature | Enterprise BYOK (Chat) | CLI BYOK |
|---------|----------------------|----------|
| Launch date | Public preview (date not pinpointed) | April 7, 2026 |
| Scope | Copilot Chat in IDEs + github.com | Copilot CLI only |
| Configuration by | Enterprise admin (AI controls panel) | Individual developer (env vars) |
| Requires Enterprise Cloud | Yes | No |
| Requires GitHub auth | Yes (enterprise membership) | No (optional) |
| Offline mode | No | Yes (`COPILOT_OFFLINE=true`) |

**For Option D, we primarily care about Enterprise BYOK (Chat)**, since that's the VS Code agent mode workflow. CLI BYOK is a bonus but not the core argument.

---

## Answers to 34 Research Questions

### Feature Status and Timeline (Q1-4)

**Q1. Current status?**
**PUBLIC PREVIEW.** Docs state: *"The ability to bring your own API keys to GitHub Copilot is in public preview and subject to change."*
- Source: https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-enterprise/use-your-own-api-keys

**Q2. Which plans support BYOK?**
Enterprise-level feature. The docs page is under "Manage for enterprise" → "Use your own API keys." It says *"make them available for organizations in your enterprise account."* This means **Copilot Business or Copilot Enterprise under a GitHub Enterprise Cloud account.** Individual Pro/Pro+ plans do NOT have this feature (though CLI BYOK works for anyone).
- Source: Same URL as Q1

**Q3. Historical trajectory?**
- NOT VERIFIED — no specific changelog entry found for when Enterprise BYOK launched. The CLI BYOK was announced April 7, 2026.
- CLI BYOK changelog: https://github.blog/changelog/2026-04-07-copilot-cli-now-supports-byok-and-local-models/

**Q4. GA timeline or roadmap?**
- NOT VERIFIED — no GA date or roadmap published in any source fetched.

### Supported Providers and Models (Q5-8)

**Q5. Supported providers as of April 2026?**
Seven providers confirmed:
1. Anthropic
2. AWS Bedrock
3. Google AI Studio
4. Microsoft Foundry
5. OpenAI
6. OpenAI-compatible providers
7. xAI

Source: Enterprise BYOK docs page (Q1 URL)

**Q6. Fine-tuned models on Azure AI Foundry?**
**YES, with caveats.** Docs state: *"Fine-tuned models are also supported, but functionality and quality of results can vary depending on the fine-tuning setup. You should test your model and review its outputs carefully before using it in production."*
- Source: Enterprise BYOK docs page

**Q7. Foundry Model Catalog models (Llama, Mistral, Phi)?**
NOT EXPLICITLY VERIFIED. However, "Microsoft Foundry" is a supported provider, and the setup requires a deployment URL + model ID. Any model deployed as an endpoint behind a URL should work. The docs show a Foundry-specific setup flow with deployment URL field.
- Source: Enterprise BYOK docs page (screenshot reference: `byok-add-foundry.webp`)

**Q8. Model capability declarations?**
NOT VERIFIED in enterprise BYOK docs. However, CLI BYOK docs state models must support **tool calling (function calling) and streaming**. This is likely a requirement for enterprise BYOK too but is not explicitly stated.
- CLI source: https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/use-byok-models#model-requirements

### Feature Compatibility (Q9-16)

**Q9. Agent mode (VS Code)?**
NOT EXPLICITLY CONFIRMED for BYOK models. The docs say BYOK models work with *"GitHub Copilot Chat and GitHub Copilot CLI."* Agent mode is a mode of Copilot Chat in VS Code. Inference: agent mode should work since it's part of Chat, but no explicit confirmation. Tool calling, file reads, terminal commands, and multi-step loops are agent mode features — if the BYOK model supports tool calling (which CLI BYOK requires), these should work.
- ASSESSMENT: **Likely works**, but NOT VERIFIED with primary source citation.

**Q10. MCP servers?**
NOT EXPLICITLY VERIFIED for BYOK models. MCP is a Copilot Chat feature available on all plans including Free. Since BYOK models appear in the Chat model picker, MCP should work — but no docs confirm this specifically.
- ASSESSMENT: **Likely works**, but NOT VERIFIED.

**Q11. Instruction files?**
NOT EXPLICITLY VERIFIED for BYOK models. Custom instructions (personal, repository, organization) are a Copilot Chat feature. Since BYOK models are used through Copilot Chat, they should receive instruction files — but no docs confirm this specifically.
- ASSESSMENT: **Likely works**, but NOT VERIFIED.

**Q12. Workspace context from indexing?**
NOT EXPLICITLY VERIFIED for BYOK models.
- ASSESSMENT: **Likely works** (Copilot's client-side orchestration sends context regardless of model), but NOT VERIFIED.

**Q13. Inline code completions?**
**NO.** The docs explicitly scope BYOK to *"GitHub Copilot Chat and GitHub Copilot CLI."* Inline code completions are a separate feature. The model picker for chat and the model picker for completions are separate. BYOK models do NOT appear in the completions model picker.
- Source: Enterprise BYOK docs page. Also confirmed by: *"Changing the model used by Copilot Chat does not affect the model used for Copilot inline suggestions."* (https://docs.github.com/en/copilot/how-tos/use-ai-models/change-the-chat-model)

**Q14. Copilot coding agent (cloud)?**
NOT VERIFIED. The cloud-based coding agent (works from GitHub issues) is a separate feature with its own premium request SKU. No docs mention BYOK support for it.
- ASSESSMENT: **Likely NOT supported** — cloud agent runs on GitHub's infrastructure, not the user's IDE.

**Q15. Copilot code review?**
NOT VERIFIED. Code review runs on an "agentic architecture" (March 2026 changelog) but no docs mention BYOK model support for it.
- ASSESSMENT: **Likely NOT supported.**

**Q16. Model coexistence (switch between built-in and custom)?**
**YES — CONFIRMED.** Docs state: *"Your models will appear at the bottom of the model picker, under the enterprise name."* This explicitly confirms coexistence — BYOK models appear alongside built-in models in the same picker. Users can switch between Claude Opus, GPT-4.1, and the custom Foundry model within the same session.
- Source: Enterprise BYOK docs page

### Enterprise Administration (Q17-21)

**Q17. Registration process?**
**CONFIRMED — detailed step-by-step:**
1. Enterprise owner navigates to enterprise → AI controls → Copilot → Configure allowed models → Custom models tab
2. Click "Add API key"
3. Select provider (e.g., Microsoft Foundry)
4. Enter name (shown in model picker), API key
5. For Foundry: enter deployment URL + model ID
6. Note: *"If your models have different deployment URLs, they cannot be added to the same API key. Create a separate API key for each deployment URL."*
7. Click Save
- Source: Enterprise BYOK docs page

**Q18. Organization scoping?**
**YES — CONFIRMED.** Enterprise admins can:
- Allow for all organizations
- Choose per organization (check/uncheck specific orgs)
Full per-organization access control documented.
- Source: Enterprise BYOK docs "Managing availability of custom models in your organizations" section

**Q19. Token limits (max input/output)?**
NOT VERIFIED — not mentioned in any fetched docs.

**Q20. Audit logging?**
Audit logs are available on Pro+ ($39/mo individual), Business, and Enterprise plans. Whether BYOK-specific events appear in audit logs is NOT EXPLICITLY VERIFIED.
- Source: https://docs.github.com/en/copilot/get-started/plans (plan comparison table)

**Q21. Data transit path?**
NOT EXPLICITLY VERIFIED. The docs don't describe whether prompts flow through GitHub's servers to the Foundry endpoint or connect directly. The enterprise BYOK docs note: *"We highly recommend adhering to the principle of least privilege by assigning only the minimum necessary scopes to your API keys."* This implies GitHub's servers hold and use the API key, meaning **prompts likely route through GitHub's infrastructure to the provider endpoint.**
- ASSESSMENT: GitHub acts as intermediary (holds API key, routes requests). NOT VERIFIED with explicit statement.

### Cost and Billing (Q22-24)

**Q22. What does the user pay?**
The user pays:
1. **Copilot subscription** (Business $19/seat or Enterprise $39/seat per month)
2. **Provider API costs** — the docs say: *"Align with your existing payment methods, contracts, credits, or negotiated rates."*
- Source: Enterprise BYOK docs (Why bring your own API keys section)

**Q23. BYOK and premium requests?**
NOT EXPLICITLY VERIFIED — critical gap. The docs don't state whether BYOK model requests consume premium requests from the Copilot subscription or are tracked separately.
- ASSESSMENT: Given that BYOK uses your own API key (and your own money for tokens), it would be logical that BYOK requests do NOT consume premium requests — but this is an assumption.

**Q24. Subscription requirement?**
**YES — Enterprise Cloud required.** BYOK is an enterprise admin feature requiring GitHub Enterprise Cloud with Copilot Business ($19/seat) or Copilot Enterprise ($39/seat).
- Source: Enterprise BYOK docs page (under "Manage for enterprise")

### Limitations and Risks (Q25-28)

**Q25. Documented limitations?**
1. **Public preview** — subject to change
2. **Chat and CLI only** — not inline completions
3. **Fine-tuned model quality varies** — explicit warning
4. **Foundry deployment URL constraint** — different deployment URLs require separate API key entries
5. **Enterprise Cloud required** — not available on individual plans or GitHub Enterprise Server
- Source: Enterprise BYOK docs page

**Q26. Models that explicitly don't work?**
NOT EXPLICITLY DOCUMENTED for enterprise BYOK. For CLI BYOK: model must support tool calling + streaming, 128k+ context recommended.
- Source: CLI BYOK docs (model requirements section)

**Q27. Deprecation/change risk?**
Generic preview disclaimer: *"in public preview and subject to change."* No specific migration or fallback path documented.

**Q28. Quality/performance issues?**
*"Fine-tuned models are also supported, but functionality and quality of results can vary depending on the fine-tuning setup."*
- Source: Enterprise BYOK docs page

### Competitor Comparison (Q29-31)

**Q29. Can competitors consume a Foundry model?**
NOT VERIFIED from these sources. Would require separate research on Cursor, Windsurf, Cline, Claude Code APIs.
- ASSESSMENT: Most competitors support OpenAI-compatible endpoints. Cursor and Windsurf support custom API keys. Cline (open source) supports any OpenAI-compatible endpoint. Claude Code is Anthropic-only. However, none provide the same enterprise admin governance (org scoping, audit logs) as Copilot.

**Q30. Feature comparison with custom model?**
NOT VERIFIED from these sources.

**Q31. Better BYOK from any competitor?**
NOT VERIFIED from these sources.

### Enterprise Readiness (Q32-34)

**Q32. Compliance certifications?**
NOT EXPLICITLY VERIFIED for BYOK specifically. GitHub Enterprise Cloud has SOC 2, FedRAMP Tailored LI-SaaS, etc., but whether BYOK inherits these is not documented in fetched pages.

**Q33. Enterprise Managed Users (EMU)?**
NOT VERIFIED. Copilot metrics docs mention EMU (*"consistent usernames for Enterprise Managed Users"*), but BYOK + EMU specifically is not documented.

**Q34. GovCloud / FedRAMP?**
NOT VERIFIED.

---

## Scorecard Summary

| Category | Verified | Partially Verified | Not Verified |
|----------|----------|--------------------|--------------|
| Feature Status (Q1-4) | Q1, Q2 | Q3 | Q4 |
| Providers & Models (Q5-8) | Q5, Q6 | Q7 | Q8 |
| Feature Compatibility (Q9-16) | Q13, Q16 | Q9, Q10, Q11, Q12 | Q14, Q15 |
| Enterprise Admin (Q17-21) | Q17, Q18 | Q20, Q21 | Q19 |
| Cost & Billing (Q22-24) | Q22, Q24 | | Q23 |
| Limitations (Q25-28) | Q25, Q27, Q28 | | Q26 |
| Competitor (Q29-31) | | | Q29, Q30, Q31 |
| Enterprise Readiness (Q32-34) | | | Q32, Q33, Q34 |

**Totals: 13 verified, 8 partially verified, 13 not verified**

---

## Critical Findings for Option D

### CONFIRMED (safe to publish)

1. BYOK is in **public preview** for Enterprise Cloud
2. **7 providers** supported including **Microsoft Foundry**
3. **Fine-tuned models supported** (with quality caveat)
4. Models appear in the **same model picker** as built-in models — users switch freely
5. Enterprise admin has **per-organization access control**
6. **Foundry setup** uses deployment URL + model ID
7. **NOT for inline completions** — Chat and CLI only
8. **CLI BYOK** (April 7, 2026) adds individual-level BYOK with offline mode

### LIKELY TRUE but NOT VERIFIED (publish with caveat)

9. Agent mode works with BYOK models (it's part of Chat, which is confirmed)
10. MCP, instruction files, workspace context work (they're Chat features)
11. BYOK requests don't consume premium requests (users pay provider directly)
12. Prompts route through GitHub infrastructure to provider endpoint

### NOT VERIFIED (do NOT publish as fact)

13. GA timeline
14. Cloud coding agent support
15. Code review support
16. Specific compliance certifications for BYOK
17. Token limit configuration
18. EMU / GovCloud / FedRAMP support
19. Competitor feature comparison specifics

---

## Showstopper Assessment

**No showstoppers found.** The core Option D thesis holds:

1. Troy's Foundry model CAN be registered via BYOK (Microsoft Foundry is a supported provider)
2. It WILL appear in the model picker alongside built-in models (confirmed)
3. Enterprise admin CAN control which orgs see it (confirmed)
4. It works with Chat and CLI (confirmed)
5. It likely works with agent mode, MCP, instruction files (not confirmed but logical given architecture)
6. Inline completions are NOT supported — but this is acceptable since completions use GitHub's optimized models anyway

**The only significant risk is preview status** — BYOK could change or be withdrawn. Mitigation: present this risk explicitly, note that GitHub's trajectory is toward more model flexibility (not less), and include CLI BYOK as a fallback path.

---

## Authoritative Sources

| Source | URL |
|--------|-----|
| Enterprise BYOK docs | https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-enterprise/use-your-own-api-keys |
| CLI BYOK docs | https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/use-byok-models |
| CLI BYOK changelog | https://github.blog/changelog/2026-04-07-copilot-cli-now-supports-byok-and-local-models/ |
| Supported models | https://docs.github.com/en/copilot/reference/ai-models/supported-models |
| Premium requests | https://docs.github.com/en/copilot/concepts/billing/copilot-requests |
| Plans comparison | https://docs.github.com/en/copilot/get-started/plans |
| Changing chat model | https://docs.github.com/en/copilot/how-tos/use-ai-models/change-the-chat-model |
| Enterprise policies | https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-enterprise/manage-enterprise-policies |
| About Copilot Chat | https://docs.github.com/en/copilot/concepts/chat |
| Copilot changelog | https://github.blog/changelog/label/copilot/ |

---

## Updated Model Multiplier Reference (April 2026)

| Model | Paid Plan Multiplier | Free Plan |
|-------|---------------------|-----------|
| GPT-4.1 | **0x** (included, free) | 1x |
| GPT-4o | **0x** (included, free) | 1x |
| GPT-5 mini | **0x** (included, free) | 1x |
| Raptor mini | **0x** (included, free) | 1x |
| Grok Code Fast 1 | 0.25x | 1x |
| Claude Haiku 4.5 | 0.33x | 1x |
| Gemini 3 Flash | 0.33x | N/A |
| GPT-5.4 mini | 0.33x | N/A |
| Claude Sonnet 4 / 4.5 / 4.6 | 1x | N/A |
| Gemini 2.5 Pro / 3.1 Pro | 1x | N/A |
| GPT-5.1 / 5.2 / 5.2-Codex / 5.3-Codex / 5.4 | 1x | N/A |
| **Claude Opus 4.5 / 4.6** | **3x** | N/A |
| Claude Opus 4.6 (fast mode) | 30x | N/A |
| Custom Foundry (BYOK) | **Unknown** (likely not counted — user pays provider) | N/A |

Key update: There are now **four 0x models** (GPT-4.1, GPT-4o, GPT-5 mini, Raptor mini), not two. This strengthens the cost offset argument — even more routine tasks can be handled at zero incremental cost.
