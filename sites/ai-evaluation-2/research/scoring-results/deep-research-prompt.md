# Deep Research Prompt: Scoring Results

## Objective

Investigate every factual claim, pricing figure, scoring justification, and methodological assertion on the Scoring Results page. This page is the bottom-line output of the evaluation — every score must be defensible to a knowledgeable skeptic.

---

## Claims to Investigate

### 1. Option A Pricing — "$39/seat/month, zero engineering"

**Research questions:**
- Confirm the current GitHub Copilot Pro+ price is $39/month. Cite the official pricing page.
- Is there a Business or Enterprise tier with different pricing? What are those prices?
- Is it accurate to say "zero engineering" for Copilot setup? Does configuration of instruction files count as engineering?

### 2. Option A Model — "Claude Opus 4.6 included at $39 flat — frontier model, proven 96%+ quality"

**Research questions:**
- Is Claude Opus 4.6 available on GitHub Copilot Pro+? Cite documentation.
- What is the multiplier for Claude Opus 4.6 on Copilot? How many premium requests does it consume per prompt?
- What does "96%+ quality" refer to? Is this an internal benchmark or an external one? If internal, flag as self-reported.
- Is Claude Opus 4.6 considered a "frontier model" by industry standards? What defines frontier-tier?

### 3. Option B Pricing — "$100-200/month tokens + gateway infra"

**Research questions:**
- What are the actual per-token rates for Claude Opus 4.6 on OpenRouter? Calculate the cost of 20 architecture sessions (each reading 10-20 files, ~100K context tokens, generating ~5K output tokens).
- What does Kong AI Gateway cost? Is there a free tier? What are enterprise pricing tiers?
- Is "$100-200/month" a reasonable estimate for an architect using Claude Opus 4.6 via OpenRouter at 20 sessions/month?

### 4. Option C Pricing — "$100-200/month tokens + Cognitive Services + App Service + engineering amortization"

**Research questions:**
- What are Azure Cognitive Services pricing tiers relevant to AI agent deployment? Cite Azure pricing pages.
- What does Azure App Service cost for hosting a custom AI agent? Cite pricing.
- Is the "$100-200/month tokens" figure reasonable for Azure-hosted model calls at 20 sessions/month?
- What engineering effort would need to be amortized? Is "significant engineering investment (6-12 dev-months)" a reasonable estimate for building a custom architecture agent?

### 5. EF-02 Cost Predictability — "Fixed $39/month regardless of usage" (Score: 5 for A)

**Research questions:**
- Is Copilot Pro+ truly fixed regardless of usage, or are there overage charges beyond the premium request allowance?
- If overages exist, does this change the score from 5 to 4 ("Fixed base with small, bounded variable component")?

### 6. EF-05 Domain Context Awareness — "500+ line instructions, scoped rules, workspace indexing — proven with 4 solution designs" (Score: 5 for A)

**Research questions:**
- Does Copilot support scoped `.instructions.md` files with `applyTo` glob patterns? Cite documentation.
- Does Copilot support workspace indexing (semantic search across the repository)? How does it work?
- The "4 solution designs" claim is internal — flag as self-reported evidence.

### 7. EF-08 Time to Value — "6+ months" for Option C (Score: 1)

**Research questions:**
- Are there examples of organizations building custom AI agents on Azure AI Foundry? How long did they take?
- Is "6+ months" a reasonable estimate or overstated? What would a minimum viable agent look like and how long to build?
- Could an organization use Azure AI Foundry's no-code/low-code agent builder to reduce this timeline?

### 8. EF-11 Vendor Lock-in — "AGENTS.md emerging as standard" (Score: 4 for A)

**Research questions:**
- What is the AGENTS.md standard? Who created it? Which platforms support it? Cite sources.
- Is there a formal specification or is it an informal convention?
- Does AGENTS.md provide enough portability to justify a score of 4 rather than 3?

### 9. Sensitivity Analysis Methodology

**Research questions:**
- Is the "+/- 5 percentage point shift" a standard sensitivity analysis technique for weighted scoring models? Cite decision analysis literature.
- Are there more rigorous sensitivity analysis methods (e.g., Monte Carlo simulation, tornado diagrams) that a skeptic might demand?
- Is a 1.84-point margin on a 1-5 scale genuinely "enormous" as claimed? What margins are typically considered decisive in multi-criteria decision analysis?

### 10. Critical Failure Check — "4 critical failures" for Option C

**Research questions:**
- Is the "any factor scored 1 is grounds for rejection" rule a standard practice in weighted scoring models, or is it an added criterion specific to this evaluation?
- In multi-criteria decision analysis literature, how are critical thresholds typically handled?

---

## Expected Output Format

For each claim:
1. **Claim as stated** — exact quote from the page
2. **Verdict** — Confirmed / Partially Confirmed / Unconfirmed / Incorrect
3. **Evidence** — cited sources with URLs, dates accessed, and relevant excerpts
4. **Recommended correction** — if the claim needs updating, provide the corrected text
5. **Confidence level** — High / Medium / Low based on source quality

Include a summary table at the top with all claims and their verdicts.
