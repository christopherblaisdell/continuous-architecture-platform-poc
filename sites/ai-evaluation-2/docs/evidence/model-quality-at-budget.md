<!-- CONFLUENCE-PUBLISH -->
<!-- CONFLUENCE-URL: https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2616459316/Model+Quality+at+Budget -->

# Model Quality at Budget

## The Hidden Variable

Every AI platform evaluation focuses on features, integration, and total cost. But there is a variable that determines whether any option actually delivers value: **the quality of the AI model you can afford to run.**

Budget constrains model selection. Model selection determines output quality. A platform with every feature in the world is useless if it runs a model that cannot perform the task.

This page examines what model tier each option delivers at its actual operating cost — not the theoretical best model, but the one you will use day-to-day based on real budget constraints.

---

## What Each Option Actually Delivers

### Option A: GitHub Copilot — Frontier Model, Fixed Cost

| Parameter | Value |
|-----------|-------|
| Monthly cost | $39 per seat (fixed) |
| Architecture model | Claude Opus 4.6 (frontier-tier) |
| Cost per architecture session | ~$0.48 (4 prompts x 3x multiplier x $0.04) |
| Included premium requests | 1,500/month (supports ~500 Opus-tier sessions) |
| Routine task model | GPT-4o, GPT-4.1 (0x multiplier — free, unlimited) |

Copilot bundles a frontier model at a fixed price. Intent-based billing (per user prompt, not per token) means the actual model cost is absorbed by Microsoft. An architect gets Claude Opus 4.6 for solution design AND GPT-4o for routine tasks, all within $39/month.

**The key insight:** If you paid for Claude Opus 4.6 at market per-token rates for the same volume of architecture work, the monthly token bill would be $100-200+ per architect. Copilot's fixed pricing makes frontier models accessible at a fraction of their raw cost.

!!! info "Model Transparency Caveat"
    Selecting Claude Opus 4.6 in Copilot governs the primary reasoning model, but Microsoft's orchestration layer routes internal agentic steps (tool dispatch, summarization, context assembly) to models of its choosing — with no per-inference visibility. This is a real trade-off: you get frontier-model access at fixed cost, but you trade away per-request model attribution. The architecture practice pilot's output quality demonstrates that frontier reasoning is applied where it matters. See [DD-04: Model Routing](../decisions/dd-04-model-routing.md) for the full analysis of this trade-off.

### Option B: Roo Code + Kong AI Gateway — Pay-Per-Token, Operator Chooses

| Parameter | Value |
|-----------|-------|
| Monthly cost | Variable (token-based) |
| Architecture model | Operator's choice (any model via OpenRouter or Kong) |
| Claude Opus 4.6 estimated cost | ~$100-200/month per architect at 20 sessions/month |
| Budget fallback | Cheaper models available but degrade output quality |

Option B gives full model flexibility — the operator chooses which model to route through the gateway. But this is a double-edged sword: choosing Claude Opus 4.6 means paying market per-token rates with no bulk discount. Budget pressure will push toward cheaper models over time.

### Option C: Bespoke Agent (Azure AI Foundry) — Per-Token, Budget-Driven

| Parameter | Value |
|-----------|-------|
| Monthly cost | Variable (infrastructure + tokens) |
| Architecture model | Whatever the budget allows |
| Frontier model on Azure | $100-200+/month per architect (tokens only, before infrastructure) |
| Microsoft quote model tier | Budget-tier models (cheapest available) |
| Infrastructure overhead | Cognitive Services, App Service, storage, monitoring, engineering maintenance |

Option C's cost structure forces a choice: **use a frontier model and spend significantly more than Option A, or use a budget model and get significantly worse output.** There is no fixed-price bundling to subsidize model quality.

---

## The Microsoft Quote: Apples to Oranges

Microsoft recently provided a projected monthly AI token cost estimate for Option C. The estimate appeared competitive — but it achieved that price point by selecting two of the cheapest available models.

This is not an apples-to-apples comparison with Option A.

| Comparison Dimension | Option A (Copilot) | Option C (Microsoft Quote) |
|---------------------|-------------------|---------------------------|
| Model quality tier | Frontier (Claude Opus 4.6) | Budget (cheapest available) |
| Architecture reasoning capability | Deep, multi-file, context-aware | Shallow, generic, requires significant rework |
| Monthly cost | $39 fixed | Appears competitive at budget-tier models |
| Cost to match Option A's model quality | $39 | $100-200+ per seat (tokens only) + infrastructure |

**When you normalize for model quality, Option C costs 3-5x more than Option A to deliver equivalent output.** The quote looks affordable because it assumes models that cannot do the job at the level Option A delivers.

!!! warning "The Comparison Trap"
    Comparing Option C's budget-model token estimate against Option A's subscription is like comparing the fuel cost of a bicycle to a car. The bicycle is cheaper to fuel — but it cannot complete the journey. The relevant question is: **what does it cost to run Option C with a model that produces comparable output to what Option A already includes?**

---

## The Model Quality Cliff

Architecture work is disproportionately sensitive to model quality compared to routine code completion. Unlike suggesting the next line of code (where a fast, cheap model often suffices), architecture analysis requires:

| Capability | Why It Needs a Frontier Model |
|-----------|-------------------------------|
| Multi-file reasoning | Reading 10-20 files (specs, source code, ADRs, metadata) and synthesizing coherent analysis |
| Domain rule enforcement | Applying specific constraints (safety defaults, data ownership, naming conventions) consistently |
| Structured document generation | Producing MADR-formatted ADRs, impact assessments, and solution designs that follow precise templates |
| Cross-service impact analysis | Tracing how a change to one service affects contracts, data flows, and event schemas across the system |
| Nuanced trade-off evaluation | Weighing options with genuine pros and cons, not strawman alternatives |
| Long-context fidelity | Maintaining accuracy across 100K+ token contexts without losing instructions or domain rules |

Budget-tier models struggle with all of these. They produce shallow analysis, miss domain rules, generate generic boilerplate, and fail to trace cross-service impacts. The output looks plausible on first read but requires extensive rework — effectively making the "cheap" model more expensive in architect time than a frontier model that gets it right the first time.

!!! note "The Rework Tax"
    A frontier model that costs $39/month and produces output requiring 10 minutes of review saves more architect time than a budget model that costs $15/month but produces output requiring 2 hours of rework. The model cost is noise compared to the architect's hourly rate.

---

## The Risk: Spending More for Less

The worst-case scenario is not picking the wrong platform. It is this:

1. The organization invests weeks of engineering building Option C
2. Budget constraints force the use of a budget-tier model to keep costs "reasonable"
3. Architecture output quality is so poor that architects stop using it
4. The platform is abandoned, leaving the practice with **no AI assistance at all**
5. The engineering investment is unrecoverable sunk cost

This is not hypothetical — it is the natural consequence of per-token pricing combined with budget pressure. Every month, someone will ask "can we use a cheaper model?" The answer will always be yes, technically. But each step down the model ladder degrades output quality until the platform provides negative value.

Option A eliminates this risk entirely:

- Frontier model is included — no per-token budget pressure to downgrade
- Zero engineering investment — nothing to lose if the practice evolves
- Same-day deployment — value begins immediately
- Monthly subscription — cancel anytime with no sunk cost

---

**See also:**

- [Evaluation Methodology](../framework/evaluation-methodology.md) — EF-04 (Architecture Output Quality) scores each option based on the model tier it will actually use at its operating budget
- [Evaluation Approach](../framework/evaluation-approach.md) — Why testing reversible options before committing to irreversible ones matters
- [Build vs Leverage](build-vs-leverage.md) — The cost of building infrastructure that platforms already provide
