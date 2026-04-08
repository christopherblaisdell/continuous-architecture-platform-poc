<!-- CONFLUENCE-PUBLISH -->
<!-- CONFLUENCE-URL: https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2614854155/DD-02+Billing+Model -->

# DD-02: Billing Model

| | |
|-----------|-------|
| **Status** | Under Evaluation |
| **Date** | 2026-04-07 |
| **Scope** | How is AI usage billed — per-seat, per-token, or hybrid? |
| **Feeds into** | EF-01 (TCO), EF-02 (Cost Predictability), EF-03 (Cost Scaling) |

---

## Problem Statement

AI platforms bill for usage in fundamentally different ways. The billing model is not a line-item detail — it determines whether the organization can predict costs, whether architects self-censor usage to stay within budgets, and whether model quality degrades over time as cost pressure mounts.

The three options under evaluation use three different billing models. The question is: **which billing model best supports sustained, high-quality architecture work without creating perverse incentives to reduce usage or downgrade model quality?**

---

## Options

### Option A: Per-Seat Fixed (Copilot Pro+)

$39/month per architect. Routine model usage (GPT-4o, GPT-4.1 at 0x multiplier) is included without consuming premium requests, though subject to GitHub's fair-use rate limits. Frontier model usage (Claude Opus 4.6 at 3x multiplier) draws from 1,500 included premium requests per month — approximately 500 Opus-tier sessions.

- **Predictable** — cost is known before the month starts
- **No usage anxiety** — architects use the tool freely without watching a meter
- **Frontier model included** — no budget pressure to downgrade to a cheaper model
- **Billing unit is intent, not consumption** — each user prompt costs one request regardless of how many files the agent reads or how many tool calls it makes
- **Agentic loop caveat:** In Agent Mode, each autonomous loop iteration (tool call, file read, sub-agent dispatch) may consume additional premium requests beyond the initial user prompt. A single user prompt that triggers a long agentic chain can consume more than 1 premium request. The 0x multiplier for routine models and 3x multiplier for frontier models apply per billable request, not strictly per user prompt. Actual consumption depends on session complexity.
- **Limitation:** If an architect exceeds 1,500 premium requests, overages cost $0.04 per request ($0.12 per Opus prompt). At 20 sessions/month with 4 prompts each, usage is ~240 premium requests — well within the allowance, though complex agentic sessions with many tool calls may consume more.

### Option B: Per-Token Variable (Roo Code + Kong)

Pay-per-token at market rates, routed through a Kong AI Gateway. The organization pays for every input and output token consumed. Cost varies by model, context size, and session length.

- **Transparent** — exact cost per request is visible via OpenRouter or Kong analytics
- **Flexible** — any model at any time, priced at its actual token rate
- **Budget pressure is structural** — every prompt has a visible cost, creating incentive to use shorter contexts, cheaper models, or fewer sessions
- **Architecture sessions are expensive** — a single solution design session reading 10-20 files with Claude Opus 4.6 can cost $5-15 in tokens. At 20 sessions/month, that is $100-300/architect.
- **No ceiling** — an unexpectedly complex month can produce an unexpectedly large bill

### Option C: Per-Token + Infrastructure (Azure AI Foundry)

Pay-per-token for model calls plus fixed infrastructure costs (Cognitive Services, App Service, storage, monitoring). The organization pays both variable token costs and fixed platform overhead.

- **Double variable** — token costs fluctuate with usage AND infrastructure costs step up at team thresholds
- **Budget-driven model degradation** — see [Model Quality at Budget](../evidence/model-quality-at-budget.md) for why cost pressure forces cheaper models over time
- **Infrastructure amortization** — fixed costs only become efficient at scale (5+ architects), but the practice is starting with 1-2
- **Least predictable** — token costs, infrastructure costs, and engineering maintenance costs are all variable

---

## The Behavioral Economics Factor

Billing models do not just determine cost — they shape behavior:

| Billing Model | Architect Behavior | Quality Consequence |
|---------------|-------------------|---------------------|
| Per-seat fixed | Use freely; no cost awareness per session | Frontier model used consistently; no self-censoring |
| Per-token variable | Watch costs; shorten sessions; consider cheaper models | Gradual model downgrade as budget scrutiny increases |
| Per-token + infrastructure | Same as above, with added pressure from visible infrastructure line items | Strongest pressure to cut model costs; "can we use a cheaper model?" becomes a monthly question |

The architecture practice needs architects to use AI confidently and frequently — not to ration prompts or avoid complex, multi-file analysis because it costs more. A billing model that penalizes thorough architecture work undermines the entire value proposition.

---

## Assessment

| Criterion | Option A (Per-Seat) | Option B (Per-Token) | Option C (Per-Token + Infra) |
|-----------|--------------------|--------------------|----------------------------|
| Monthly cost (1 architect) | $39 fixed | $100-300 variable | $100-300 tokens + $50-100 infra |
| Monthly cost (5 architects) | $195 fixed | $500-1,500 variable | $500-1,500 tokens + $50-100 infra |
| Cost predictability | Known in advance | Varies 3x month-to-month | Varies 3x+ with step-function infra |
| Model quality pressure | None — frontier included | Moderate — visible per-token cost | Severe — visible on two cost dimensions |
| Scaling behavior | Linear ($39/seat) | Linear (tokens) | Sublinear infra amortizes, but tokens remain linear |

---

## Recommendation

**Per-seat fixed billing (Option A)** is the clear winner for DD-02. It eliminates the behavioral economics problem entirely — architects never face a trade-off between doing thorough work and managing costs. The $39/seat/month price point with frontier model access is lower than what any per-token approach delivers at equivalent model quality and usage volume.

The per-token model is appropriate when usage is light and sporadic. Architecture work is neither — it is session-heavy, context-heavy, and model-sensitive. Fixed billing aligns the cost model with the usage pattern.

---

**See also:**

- [Model Quality at Budget](../evidence/model-quality-at-budget.md) — Why per-token billing creates pressure to downgrade model quality
- [Scoring Results](../framework/scoring-results.md) — EF-01, EF-02, and EF-03 scores for each option
- [Platform Landscape](../evidence/platform-landscape.md) — Pricing comparison across five platforms
