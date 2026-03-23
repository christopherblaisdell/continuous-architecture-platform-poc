# Copilot Billing Mechanics

## Deep Research Results: GitHub Copilot Premium Request Billing

This page summarizes the findings of a deep research analysis conducted on March 4, 2026, investigating the exact billing mechanics of GitHub Copilot Pro+ Agent Mode. The research resolved a critical methodological error that overstated Copilot's cost by 96x -- from an estimated $46.20/session to the actual $0.48/session.

---

## The Core Discovery: Intent-Based Billing

GitHub Copilot uses **intent-based billing**, not token-based billing. The billing unit is the **user prompt** -- each time a human types a message and presses Enter. All autonomous agent activity that follows is free.

### What Is Billed

Each user prompt consumes one base premium request, multiplied by the selected model's rate:

`Session Cost = User Prompts x Model Multiplier x $0.04`

### What Is NOT Billed

- File reads and workspace searches executed by the agent
- Terminal command executions
- Sub-agent invocations (runSubagent)
- Context summarization (when approaching token limits)
- Parallel tool calls
- Internal reasoning and planning tokens
- Error recovery and retry attempts

This means a 4-prompt session triggering 50+ autonomous tool calls costs:
`4 x 3 (Claude Opus 4.6) x $0.04 = $0.48`

---

## Model Multipliers (March 2026)

| Model | Multiplier | Cost per Prompt | Notes |
|-------|-----------|-----------------|-------|
| GPT-4.1, GPT-4o | 0x | $0 | Unlimited, included |
| Claude Opus 4.6 | 3x | $0.12 | Standard inference speed |
| Claude Opus 4.6 fast (preview) | 30x | $1.20 | 2.5x faster inference; 9x promotional rate expired Feb 16, 2026 |

### Auto Model Selection Discount

When VS Code's "Auto Model Selection" is enabled, a 10% multiplier discount applies (e.g., a 1x model is billed at 0.9x).

---

## The 78-Request Reconciliation

The research resolved why a full day of heavy Agent Mode usage (including a 50-iteration autonomous session) resulted in only 78 premium requests total:

- **4 user prompts** x 3x (Claude Opus 4.6 standard) = **12 premium requests** for the architecture session
- Remaining **66 requests** = other Copilot usage across projects throughout the day (~22 additional prompts on a 3x model)

The 50-iteration autonomous loop consumed **zero additional premium requests** beyond the 4 human prompts that initiated it.

### Why Not 30x?

If the session had used Claude Opus 4.6 fast (30x), 4 prompts would consume 120 requests -- but only 78 were recorded. The evidence confirms the session ran on the standard 3x model, not the 30x fast variant. Several factors explain this:

1. **Standard model execution:** 3x multiplier confirmed by daily total reconciliation
2. **Quota fallback protocols:** Copilot automatically falls back to 0x models when approaching rate limits
3. **LLM self-identification unreliability:** The system prompt may identify one model while the backend routes to another

---

## The $0.04 Standard vs. the $0.028 Artifact

The original methodology used $0.028/request, producing wildly inflated cost estimates. The research identified:

- **$0.04** is the official GitHub Copilot premium request overage rate (documented)
- **$0.028** is a DeepSeek/Azure cached-token API rate that was erroneously cross-applied to Copilot's abstracted billing unit

A Copilot premium request is an arbitrary enterprise-defined unit, completely unrelated to per-million-token API rates. Mapping one onto the other is mathematically invalid.

---

## Quota Mechanics

### Pro+ Allowance

| Parameter | Value |
|-----------|-------|
| Included requests | 1,500/month |
| Reset | 1st of calendar month, 00:00 UTC |
| Rollover | None -- unused requests expire |
| Overage rate | $0.04/request (if enabled) |
| Overage disabled behavior | Falls back to 0x models (GPT-4.1) |

### Capacity at Architecture Workload

At 12 premium requests per run (4 prompts x 3x):

- 1,500 / 12 = **125 runs/month** within included allowance
- Typical architecture workload: ~38 runs/month
- Headroom: ~87 unused runs/month

---

## Per-Session Cost Isolation

GitHub provides no native tool to export the cost of a single Agent Mode session. The deep research recommends a differential polling methodology:

1. **Pre-session baseline:** Close all other VS Code instances. Record the exact premium request count from the GitHub Billing dashboard.
2. **Execute session:** Run the architecture prompts. Wait 15-30 minutes for backend synchronization.
3. **Post-session polling:** Record the new premium request count.
4. **Differential calculation:** Subtract baseline from post-session count.
5. **Financial translation:** Multiply delta by $0.04 for notional cost.

---

## Comparative Economics

### Why Copilot Is 208x Cheaper Per Run

| Factor | Copilot | OpenRouter |
|--------|---------|-----------|
| **Billing unit** | User prompt (intent) | Token (compute) |
| **Agent loop cost** | $0 (absorbed by GitHub) | Full token cost per turn |
| **Context cost** | Amortized via server-side index | Re-transmitted every turn |
| **Session of 50 turns** | $0.48 (4 prompts x 3x x $0.04) | ~$100 (accumulated tokens) |

GitHub absorbs the financial penalty of the expanding context window. Even when the underlying model is Claude Opus 4.6 at 3x, the user pays $0.12 per prompt for an extensive autonomous operation that would cost orders of magnitude more on an unprotected API.

### When OpenRouter Is Cheaper

OpenRouter is economically superior when the workflow consists of hundreds of very short, one-shot queries with minimal context history. In this scenario, Copilot's per-prompt multiplier would rapidly exhaust the 1,500-request quota, while OpenRouter would charge fractions of a penny for small token payloads.

For architecture work (long, multi-step sessions with deep context), Copilot's model is dramatically cheaper.

---

## Sub-Agent Billing Anomalies

The research identified two documented issues with sub-agent billing:

1. **Telemetry bug (early 2026):** `runSubagent` erroneously triggered a premium request deduction per invocation, contradicting stated policy. Identified as a software defect, flagged for remediation.

2. **Model routing failure:** The `runSubagent` runtime schema lacks parameters to route to specific premium models. When requesting Claude Opus, the parameter is dropped, and the sub-agent defaults to a 0x model (GPT-5 mini/GPT-4o). This effectively functions as an accidental cost-containment mechanism.

---

## Source

This analysis was produced from deep research with 39 cited sources including GitHub official documentation, community discussions, billing API endpoints, and VS Code extension diagnostics. Full citations: `docs/research/DEEP-RESEARCH-RESULTS-COPILOT-BILLING.md`.
