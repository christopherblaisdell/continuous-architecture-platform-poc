# Deep Research Prompt: DD-02 Billing Model

## Objective

Investigate every pricing figure, billing mechanism claim, and behavioral economics assertion on the DD-02 page. This page argues that per-seat fixed billing is superior to per-token billing for architecture work — a skeptic will challenge the pricing accuracy and the behavioral claims.

---

## Claims to Investigate

### 1. Copilot Pro+ at $39/month — "1,500 included premium requests per month — approximately 500 Opus-tier sessions"

**Research questions:**
- Confirm the $39/month price and 1,500 premium request allowance. Cite official GitHub pricing.
- Is "approximately 500 Opus-tier sessions" correct? This assumes 3 premium requests per session (4 prompts x 3x multiplier = 12 requests per session... wait, check the math). Clarify exactly how premium requests are consumed for Claude Opus 4.6 sessions.
- What happens when the 1,500 allowance is exceeded? What is the overage rate? Cite documentation.

### 2. GPT-4o and GPT-4.1 at "0x multiplier — free, unlimited"

**Research questions:**
- Confirm that GPT-4o and GPT-4.1 are 0x multiplier (consume zero premium requests) on Copilot Pro+. Cite documentation.
- Is this a current, stable policy or could it change? Has GitHub changed multipliers in the past?
- Are there any usage limits on 0x models (rate limits, daily caps)?

### 3. Per-Token Costs for Option B — "$5-15 per session" and "$100-300/architect" at 20 sessions/month

**Research questions:**
- Calculate the actual per-token cost for a Claude Opus 4.6 architecture session via OpenRouter:
  - Input: ~100K tokens (10-20 files of context)
  - Output: ~20K tokens (4-6 responses averaging ~4K tokens each)
  - Cite current OpenRouter pricing for Claude Opus 4.6
- Is "$5-15 per session" accurate based on these calculations?
- At 20 sessions/month, is "$100-300/month" the resulting range?

### 4. Option C — "Double variable" and "token costs, infrastructure costs, and engineering maintenance costs are all variable"

**Research questions:**
- What are Azure AI Foundry's actual pricing components? Cite the Azure pricing page.
- Are infrastructure costs truly "variable" or are some fixed (e.g., App Service plan is monthly fixed)?
- Is "step-function infra at team thresholds" accurate? What infrastructure scaling characteristics does Azure AI Foundry exhibit?

### 5. Behavioral Economics — "architects self-censor usage to stay within budgets"

**Research questions:**
- Is there academic research on how billing models affect technology adoption and usage intensity? Cite relevant studies.
- Is "usage anxiety" or "meter anxiety" a documented phenomenon in per-unit billing for enterprise tools? Cite sources from cloud computing economics, SaaS adoption, or behavioral economics.
- Are there counterexamples where per-token billing led to MORE disciplined (and therefore better) usage rather than self-censoring?

### 6. Monthly Cost Comparison Table — 1 architect vs 5 architects

**Research questions:**
- Verify: Option A at 5 architects = $195/month (5 x $39). Correct.
- Verify: Option B at 5 architects = $500-1,500 variable. Is this range accurate based on the per-session costs calculated above?
- Verify: Option C at 5 architects = same token costs + "$50-100 infra." Where does the $50-100 infrastructure figure come from? Cite Azure pricing.

---

## Expected Output Format

For each claim:
1. **Claim as stated** — exact quote from the page
2. **Verdict** — Confirmed / Partially Confirmed / Unconfirmed / Incorrect
3. **Evidence** — cited sources with URLs, dates accessed, and relevant excerpts
4. **Recommended correction** — if the claim needs updating, provide the corrected text
5. **Confidence level** — High / Medium / Low based on source quality

Include a summary table at the top with all claims and their verdicts.
