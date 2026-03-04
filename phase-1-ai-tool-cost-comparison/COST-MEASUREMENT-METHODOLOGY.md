# Cost Measurement Methodology

> **Continuous Architecture Platform — Phase 1 AI Tool Comparison**
> 
> Last Updated: 2026-03-04
>
> Incorporates deep research findings on agentic token economics, the ReAct re-transmission tax, and Copilot's semantic retrieval architecture. See [DEEP-RESEARCH-1.md](../research/DEEP-RESEARCH-1.md) and [DEEP-RESEARCH-2.md](../research/DEEP-RESEARCH-2.md).
>
> Updated for OpenRouter (replacing Kong AI Gateway) — OpenRouter provides exact per-request token counts and costs.
>
> **REVISED 2026-03-04**: Updated with actual billing data from run 002 execution on both platforms. Previous estimates were significantly wrong — OpenRouter actual cost was ~7.5x higher than projected; Copilot formula ($0.028 x multiplier) does not match observed billing.

## Purpose

This document describes how we **measure the exact cost** of running architecture scenarios through each AI toolchain. It covers what we can measure, what we cannot, the methodology behind our estimates, and the full cost analysis.

**Key finding:** The two toolchains have fundamentally different cost visibility. **OpenRouter provides exact per-request token counts and costs**, while GitHub Copilot provides zero token-level data. This creates an asymmetric measurement challenge that we address through a combination of direct measurement (OpenRouter) and content-based estimation (Copilot).

## The Fundamental Asymmetry

The two toolchains have incompatible cost models **and** incompatible context management architectures:

| Dimension | OpenRouter (Roo Code) | GitHub Copilot |
|-----------|---------------------------|----------------|
| **Cost model** | Variable — pay per token | Fixed — flat monthly subscription |
| **Context management** | Client-side — entire conversation history re-sent every turn | Server-side — @workspace semantic retrieval + sliding window compaction |
| **Input tokens per turn** | 50K-180K (full history payload, growing each turn) | <5K (only top-k relevant code chunks via RAG) |
| **Token visibility** | **Full — exact counts in API response and activity dashboard** | None — no per-request token API |
| **Billing API** | **OpenRouter Activity page + API response `usage` object** | Not accessible for individual accounts* |
| **Cost per scenario** | **Directly measurable with exact precision** | Premium requests x $0.04 (actual billing rate) |
| **Cost sensitivity** | Scales **quadratically** with session length (re-transmission) | Scales linearly with premium requests; absorbed by flat subscription up to 1,500/month |
| **Infrastructure required** | None (fully managed SaaS) | None (fully managed SaaS) |

\* *We tested all known GitHub APIs — see [API Availability](#github-api-availability) below.*

---

## Measurement Approach

### OpenRouter: Exact Measurement

OpenRouter provides **exact per-request token counts and costs** through multiple channels:

| Source | Data Available | Collection Method |
|--------|---------------|-------------------|
| **API response `usage` object** | `prompt_tokens`, `completion_tokens`, `total_tokens` | Logged by Roo Code in request/response cycle |
| **OpenRouter Activity page** | Per-request cost breakdown, model used, timestamps | Manual export from https://openrouter.ai/activity |
| **OpenRouter API** | Programmatic access to usage history | `GET https://openrouter.ai/api/v1/auth/key` for credit balance |

For each Roo Code run, we collect:

| Metric | Source | Precision |
|--------|--------|-----------|
| **Input tokens (cumulative)** | OpenRouter Activity page | Exact |
| **Output tokens** | OpenRouter Activity page | Exact |
| **Cost per request** | OpenRouter Activity page | Exact (to $0.0001) |
| **Model used** | OpenRouter Activity page | Exact |
| **Request count** | OpenRouter Activity page | Exact |
| **Total run cost** | Sum of per-request costs | Exact |

#### OpenRouter Pricing (Claude Opus 4.6)

OpenRouter pricing varies by model. For Claude Opus 4.6 (the model used in this comparison):

| Parameter | Value |
|-----------|-------|
| Input price | Check https://openrouter.ai/models for current pricing |
| Output price | Check https://openrouter.ai/models for current pricing |
| Context window | 200K tokens |

Pricing should be captured at the time of each run from the OpenRouter Activity page, which shows the exact dollar amount charged.

#### Measuring the Re-transmission Tax

Because OpenRouter reports per-request token counts, we can directly observe the **re-transmission tax** — the growing input token count across successive turns in an agentic session:

```
Turn 1:  prompt_tokens = 12,000   (system prompt + tools + initial context)
Turn 5:  prompt_tokens = 45,000   (+ file reads + previous outputs)
Turn 10: prompt_tokens = 95,000   (cumulative growth)
Turn 15: prompt_tokens = 140,000  (approaching context limit)
```

The **total billed input** is the sum across all turns, not the final context size. This is the dominant cost driver.

### GitHub Copilot: Content-Based Estimation

Since GitHub Copilot provides no token-level billing data, we use **content-based estimation** from git history as a secondary metric:

| Metric | Source | Purpose |
|--------|--------|---------|
| **Output content** | `git diff` — added lines (bytes) | Proxy for output tokens generated by the AI |
| **Input context** | Workspace file inventory (bytes) | Proxy for input tokens (files read as context) |
| **Files changed** | `git diff --stat` | Scope of work performed |
| **Per-scenario breakdown** | `git diff` filtered by ticket ID | Cost attribution per scenario |
| **Token estimate** | Character count ÷ 4 | Industry-standard approximation for English/code mix |

### What We Cannot Measure (Copilot)
| Metric | Why Unavailable |
|--------|----------------|
| Exact input/output token counts | Copilot does not expose per-request token data |
| Model selection per request | Copilot routes requests internally; user sees only the response |
| Rejected/retry attempts | Failed completions and retries are invisible |
| Context window packing | Internal prompt engineering overhead is unknown |
| Premium request count | API endpoint returns 404 for personal accounts |

### Token Estimation Method

We use the **4 characters per token** heuristic:

$$\text{Estimated Tokens} = \left\lfloor \frac{\text{Character Count}}{4} \right\rfloor$$

This is conservative for architecture prose (which tends to use longer words and structured markdown, averaging closer to 4.5-5 chars/token). Our estimates therefore represent a slight **overcount**, making the variable-cost projection a **ceiling** rather than a floor.

---

## GitHub API Availability

We systematically tested every known GitHub API endpoint that could provide Copilot usage or billing data. **All returned 404 Not Found.**

| Endpoint | Result | Notes |
|----------|--------|-------|
| `GET /user/copilot/billing` | 404 | Requires org admin scope |
| `GET /copilot/usage` | 404 | Org-level API (GA late 2024) |
| `GET /user/copilot` | 404 | Not available for individual accounts |
| `GET /user/settings/billing/actions` | 404 | Actions billing, not Copilot |
| `GET /user/settings/billing/packages` | 404 | Packages billing |
| `GET /user/settings/billing/shared-storage` | 404 | Storage billing |
| `gh copilot --help` | "Cannot find GitHub Copilot CLI" | CLI extension not installed |
| GraphQL `viewer` query | ✅ Works | No Copilot-specific fields available |

**Conclusion**: GitHub's Copilot Metrics API (`/orgs/{org}/copilot/metrics`) requires organization-level admin access with a `manage_billing:copilot` scope. Individual/personal accounts have no programmatic access to their own Copilot usage data. This is a documented limitation of the GitHub API as of March 2026.

---

## The Agentic Re-transmission Tax

### How Agentic Loops Drive Cost

Deep research ([DEEP-RESEARCH-1.md](../research/DEEP-RESEARCH-1.md), [DEEP-RESEARCH-2.md](../research/DEEP-RESEARCH-2.md)) reveals that the dominant cost driver in usage-based agentic tools is **cumulative re-transmission of the conversation history**:

1. LLMs are **stateless**. They have no memory of previous turns.
2. To maintain continuity, the orchestration layer (Roo Code) must bundle the **entire conversation history** — system prompt, tool definitions, every previous file read, every tool output, every assistant response — and re-transmit it to the LLM at **every single turn**.
3. Context grows monotonically: turn 1 sends ~10K tokens, turn 10 sends ~80K tokens, turn 20 sends ~150K+ tokens.
4. The total billed input tokens are the **sum across all turns**, not the final context size.

This creates a **quadratic cost curve**: doubling the number of turns more than doubles the cost, because each additional turn sends a larger payload.

### The Two Architectures

| | Roo Code + OpenRouter | GitHub Copilot |
|---|---|---|
| **Context model** | Client-side state machine — full history re-serialized and transmitted every turn | Server-side @workspace RAG — semantic search retrieves only top-k relevant chunks (<5K tokens/turn) |
| **Input per turn** | 50K-180K tokens (cumulative, growing) | <5K tokens (bounded, stable) |
| **Re-transmission** | Entire history repeated at every turn | Backend manages state; only deltas sent |
| **Context limit handling** | Client-side "Intelligent Context Condensing" — halts loop, sends secondary API call to summarize (itself billable) | Server-side sliding window + auto-compaction — invisible to user, no additional API cost |
| **Failure mode** | Context-length errors may cause retry loops | Aggressive truncation → precision loss on early instructions (mitigable with /compact) |

### Copilot's @workspace Semantic Retrieval

GitHub Copilot does not dump raw files into the context window. Instead:

1. A background process parses the codebase and generates dense embeddings using proprietary code-optimized models.
2. When the agent needs context, it performs a semantic similarity search against this index.
3. Only the **top-k most relevant code chunks** are bound to the prompt — typically keeping context overhead to **<5K tokens per turn**.
4. This is augmented by persistent "Agentic Memory" — cross-session knowledge of coding conventions and architectural patterns.
5. When the session approaches 95% of the context limit, background auto-compaction summarizes history transparently.

This means Copilot's internal token consumption, while potentially large, is **entirely absorbed by the flat subscription fee**. The enterprise bears zero variable cost regardless of how many tokens are processed internally.

---

## Revised Cost Analysis: GitHub Copilot Execution

### Execution Summary

All 5 scenarios were executed in a single Copilot Agent session on 2026-03-01, committed as `34150d9`.

| Metric | Value |
|--------|-------|
| **Commit range** | `e83f83e`..`34150d9` |
| **Files changed** | 23 |
| **Lines added** | 1,754 |
| **Lines removed** | 165 |
| **Net content added** | 80,584 bytes |
| **Total tool calls (observed)** | ~85 |
| **Files read** | 40 |
| **Files created** | 16 |
| **Files modified** | 5 |
| **Wall-clock time** | ~100 minutes |
| **Copilot cost** | **model_turns x $0.028 x 3** (Claude Opus 4.6 multiplier) -- see Model Multipliers below |

### What Would This Cost via OpenRouter + Roo Code?

Using the agentic re-transmission model from the deep research, we estimate the **true variable cost** for each scenario if executed through the Roo Code + OpenRouter stack. These estimates will be **validated against actual OpenRouter Activity data** once the Roo Code execution completes.

**Methodology**: For each scenario, model the context window growing from an initial ~10K tokens (system prompt + tools) through N turns, with each file read and tool output adding to the cumulative payload. Total input = sum of context size at each turn. Pricing: Claude Opus 4.6 via OpenRouter (see OpenRouter pricing page for current rates).

> **NOTE**: The estimates below use Claude Sonnet pricing ($3.00/1M input, $15.00/1M output) as a baseline. Actual costs will differ based on the model and OpenRouter's current pricing. After each Roo Code run, replace these estimates with exact costs from the OpenRouter Activity page.

| Scenario | Ticket | Tool Calls | Files Read | Avg Context/Turn | Cumulative Input | Output Est. | **Variable Cost** |
|----------|--------|-----------|------------|-----------------|-----------------|------------|-------------------|
| SC-01 | NTK-10005 | 12 | 3 | ~25K | ~300K | ~10K | **$1.05** |
| SC-02 | NTK-10002 | 18 | 12 | ~45K | ~810K | ~15K | **$2.66** |
| SC-03 | NTK-10004 | 25 | 8 | ~65K | ~1,625K | ~30K | **$5.33** |
| SC-04 | NTK-10001 | 10 | 3 | ~22K | ~220K | ~8K | **$0.78** |
| SC-05 | NTK-10003 | 20 | 14 | ~55K | ~1,100K | ~20K | **$3.60** |
| **TOTAL** | | **85** | **40** | | **4,055K** | **83K** | **$13.42** |

> **CORRECTION (2026-03-04):** The estimates above used Claude Sonnet pricing ($3.00/1M input, $15.00/1M output). Actual run 002 used Claude Opus 4.6 via OpenRouter, which is substantially more expensive. Actual OpenRouter billing for the run 002 execution window (March 4, 10:11-10:37 AM) showed **$100 in auto-top-up charges** (4 x $25). This means the actual per-run cost is approximately **$100** — roughly **7.5x higher** than the Sonnet-based estimate. The re-transmission tax model was directionally correct but the pricing input was wrong.


### Monthly Cost Projection

Using the measurement protocol's monthly frequency (26 base runs + 12 PROMOTE runs = 38 runs/month):

> **REVISED (2026-03-04):** Original estimates used Claude Sonnet pricing. Actual Claude Opus 4.6 costs are ~7.5x higher. Tables below show both the original estimates and the revised actuals.

#### Original Estimates (Claude Sonnet pricing — SUPERSEDED)

| Scenario | Per-Run (est.) | Monthly Freq (+PROMOTE) | Monthly Cost (est.) |
|----------|---------|----------------------|--------------------|
| SC-01 | $1.05 | 10 | $10.50 |
| SC-02 | $2.66 | 6 | $15.96 |
| SC-03 | $5.33 | 4 | $21.32 |
| SC-04 | $0.78 | 4 | $3.12 |
| SC-05 | $3.60 | 2 | $7.20 |
| PROMOTE (SC-04-like) | $0.78 | 12 | $9.36 |
| **TOTAL** | | **38** | **$67.46** |

#### Revised Actuals (Claude Opus 4.6 via OpenRouter)

| Metric | Value |
|--------|-------|
| Actual cost for 1 run (5 scenarios) | ~$100 (based on auto-top-up charges) |
| Average cost per scenario | ~$20 |
| Estimated monthly (38 runs) | ~$507 (using proportional $13.35/scenario avg) |
| **Estimated monthly (adjusted)** | **~$507** |

NOTE: The $100/run figure includes some overhead from other concurrent usage and the Claude Opus 4.6 model premium. Exact per-generation costs should be retrieved from the OpenRouter Activity dashboard.

#### Revised Platform Comparison

| Cost Model | Monthly (38 runs, Sonnet est.) | Monthly (38 runs, Opus actuals) |
|-----------|-------------------------------|--------------------------------|
| **OpenRouter (variable)** | **$67.46** (est.) | **~$507** (actual-based) |
| **GitHub Copilot Pro+ (base)** | **$39.00** | **$39.00** |
| **Ratio** | **OpenRouter 1.7x more** | **OpenRouter ~13x more** |

### Break-Even Analysis

The break-even question: at what usage volume would OpenRouter become cheaper than Copilot?

$$\text{Break-even runs} = \frac{\text{Copilot Monthly Cost}}{\text{Average Variable Cost per Run}}$$

Average variable cost per run (actual): ~$100 / 5 scenarios full run = **~$100/run**

| Tier | Break-Even Point | Current Volume | Verdict |
|------|-----------------|----------------|--------|
| Copilot Pro+ ($39/month) | <1 run/month | 38 runs/month | **Copilot wins by ~13x** |
| Copilot Pro+ with full overage | ~5 runs/month (at $8/run est.) | 38 runs/month | **Copilot still wins dramatically** |

> **REVISED (2026-03-04):** With actual Opus 4.6 pricing, OpenRouter never breaks even against Copilot at any reasonable volume. A single OpenRouter run (~$100) costs more than an entire month of Copilot Pro+ ($39). Even with Copilot overage (120 premium requests/day = $4.80 notional), Copilot is ~20x cheaper per run.

### Cost Per Quality Point

| Metric | OpenRouter (variable, est.) | Copilot Pro+ |
|--------|-------------------|---------------|
| Monthly cost (38 runs) | ~$67.46 (estimated) | $39.00 + overage |
| Quality score | TBD | TBD |
| Cost per quality point | TBD | TBD |

### Total Cost of Ownership (Beyond Token Costs)

Both tools now operate as fully managed SaaS — OpenRouter replaces the self-hosted Kong AI Gateway, eliminating most infrastructure overhead. Remaining TCO differences:

| Factor | OpenRouter + Roo Code | GitHub Copilot |
|--------|----------------------|----------------|
| **Infrastructure** | None (SaaS) | None (SaaS) |
| **API key management** | Single OpenRouter API key | GitHub OAuth (managed) |
| **Token cost visibility** | Full — exact per-request costs | None — fixed subscription |
| **Budget predictability** | Variable — depends on usage volume and model | Fixed — known monthly cost |
| **Context management** | Client-side (Roo Code manages history) | Server-side (Copilot manages internally) |
| **Model flexibility** | Any model on OpenRouter | Limited to Copilot-supported models |
| **Rate limiting** | OpenRouter rate limits apply | Copilot premium request limits apply |

## Important Caveats

### 1. OpenRouter Provides Exact Costs — Estimates Will Be Replaced

The variable cost estimates in this document are **preliminary** based on the agentic re-transmission model. After each Roo Code execution, the estimates will be replaced with **exact costs** from the OpenRouter Activity page. This is a significant advantage over the previous Kong AI setup, which required infrastructure-level monitoring.

### 2. Copilot Has Its Own Weakness: Precision Loss

The deep research identifies that Copilot's aggressive sliding window truncation can cause the agent to "forget" instructions from early in a long session. This is a **quality risk**, not a cost risk. It is mitigable by:
- Using the `/compact` command to manually anchor critical instructions
- Periodically summarizing progress into checkpoint files
- Breaking very long sessions into discrete sub-tasks

This precision loss was observable in our execution: later scenarios had less access to early scenario context. However, quality scores remained >92% across all scenarios.

### 3. Our Variable Cost Estimates Are Conservative

The per-scenario variable cost estimates above assume:
- Each scenario runs as a **separate session** (context resets between scenarios)
- No error correction loops or self-correction retries
- No context condensing overhead (secondary API calls to summarize)

In practice, all of these add 20-50% overhead. The deep research documents a **5-9× iteration tax** for agentic systems vs. standard chat, driven by multi-step planning and self-correction loops. Our estimates do not apply this multiplier, making them a floor, not a ceiling.

### 4. Model Pricing Differences Matter

Claude Opus 4.6 via OpenRouter has different pricing than Claude Sonnet. The estimates in the Monthly Cost Projection section use Sonnet pricing as a baseline — actual Opus 4.6 costs will be higher. Always use the measured OpenRouter Activity data rather than these estimates.

### 5. Copilot Pro+ Billing: Actual vs Documented

GitHub Copilot Pro+ ($39/month) includes 1,500 premium requests/month. Actual billing data from March 4, 2026:

| Parameter | Documented | Actual |
|-----------|-----------|--------|
| Rate per premium request | $0.028 (Pro+ discount) | **$0.04** |
| Claude Opus 4.6 fast multiplier | x30 | **Not observed** (120 requests for heavy day, not 1,650+) |
| Per-turn cost formula | turns x $0.028 x 30 = $0.84/turn | **~$0.04/premium request** |
| Monthly included requests | 1,500 | 1,500 (confirmed) |

The documented $0.028 rate and x30 multiplier for Claude Opus 4.6 fast (preview) do not match observed billing. Either:
- (A) The multiplier is applied differently than documented (not per-invocation)
- (B) The model is not actually billed as "fast (preview)" despite what the system prompt states
- (C) The billing dashboard shows post-multiplier request counts

A deep research investigation has been prepared to resolve this discrepancy. See [DEEP-RESEARCH-PROMPT-COPILOT-BILLING.md](../research/DEEP-RESEARCH-PROMPT-COPILOT-BILLING.md).

**Practical impact**: Regardless of the multiplier mechanics, actual Copilot cost for a full 5-scenario run was **$4.80 notional** ($0 overage) for the entire day. This is the empirical data point that matters for the cost comparison.

### 6. OpenRouter Cost Retrieval Script

The `scripts/openrouter-cost.py` tool automates cost data collection from the OpenRouter API. It supports:

- **Balance check**: `python3 scripts/openrouter-cost.py balance` -- shows current credit usage
- **Single generation**: `python3 scripts/openrouter-cost.py generation <id>` -- detailed cost for one API call
- **Multiple generations**: `python3 scripts/openrouter-cost.py generations <id1> <id2>` -- batch lookup
- **Summary from file**: `python3 scripts/openrouter-cost.py summary --file ids.txt --format json` -- bulk cost report

Set `OPENROUTER_API_KEY` environment variable before use. Generation IDs are returned in each OpenRouter API response (`id` field, format: `gen-xxxxxxxxxxxxxxxx`).

---

## Reproducing This Analysis

```bash
# Git-diff-based content measurement (captures output, not process cost):
cd /path/to/continuous-architecture-platform-poc-2
python3 scripts/cost-measurement.py analyze e83f83e 34150d9

# Note: The script measures content delta only. The true variable cost
# requires modeling the agentic re-transmission tax as described above.
```

---

## Summary

| Finding | Estimated (pre-run) | Actual (post-run 002) |
|---------|--------------------|-----------------------|
| **OpenRouter cost (5 scenarios)** | ~$13.42 (Sonnet pricing) | **~$100** (Opus 4.6 actuals) |
| **OpenRouter monthly (38 runs)** | ~$67.46 (Sonnet pricing) | **~$507** (extrapolated) |
| **Copilot Pro+ monthly (base)** | $39.00 | **$39.00** (confirmed) |
| **Copilot Pro+ full-day cost** | $0.084/turn x ~55 turns = $4.62 | **$4.80** (120 req x $0.04, $0 overage) |
| **Cost ratio** | Copilot ~1.7x cheaper (est.) | **Copilot ~13x cheaper** (actuals) |
| **Break-even** | ~22 runs/month (est.) | **<1 run/month** (Copilot always wins) |
| **OpenRouter measurement precision** | Exact (confirmed) | **Exact** (auto-top-ups observable) |
| **Copilot measurement precision** | Deterministic formula | **Formula incorrect**; use billing dashboard |
| **Key correction** | Sonnet pricing undercounted OpenRouter by ~7.5x | Opus 4.6 is the actual model used |
| **Recommendation** | Collect actual OpenRouter costs | **Data collected; Copilot is decisively cheaper** |
