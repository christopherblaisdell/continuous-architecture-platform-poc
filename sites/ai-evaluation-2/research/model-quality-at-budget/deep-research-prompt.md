# Deep Research Prompt: Model Quality at Budget

## Objective

This page makes the central economic argument of the evaluation: Copilot's fixed pricing delivers frontier models while per-token alternatives either cost more or force downgrades. Every cost figure, model tier claim, and behavioral prediction must be verified.

---

## Claims to Investigate

### 1. Copilot Cost Claims

**Research questions:**
- Is $39/mo still the Copilot Pro+ price? Cite the current pricing page.
- Is $0.48 the correct cost for a 4-prompt Opus session? (4 x 3 x $0.04 = $0.48) Verify the multiplier and per-request rate.
- Is "1,500/month supports ~500 Opus-tier sessions" accurate? (1,500 / 3 = 500 — math check)
- Is GPT-4o truly 0x multiplier (unlimited, free) for routine tasks? Cite documentation.

### 2. "If you paid for Claude Opus 4.6 at market per-token rates... the monthly token bill would be $100-200+ per architect"

**Research questions:**
- What are the current per-token rates for Claude Opus 4.6 via Anthropic API and via OpenRouter?
- For 20 architecture sessions per month, with an estimated context of ~100K input tokens and ~5K output tokens per session, what is the actual monthly cost?
- Is $100-200+ a reasonable estimate, or is it too high or too low? Show the calculation.
- How does token cost vary between providers (Anthropic direct, OpenRouter, AWS Bedrock, Google Vertex)?

### 3. Option B Cost Estimate — "$100-200/month per architect at 20 sessions/month"

**Research questions:**
- Is $100-200/month a reasonable estimate for Roo Code + OpenRouter using Claude Opus 4.6?
- What is OpenRouter's markup on Claude Opus 4.6 vs direct API pricing?
- What does Kong AI Gateway cost? Is there a free tier? What are the enterprise pricing tiers?
- Total Option B cost = OpenRouter tokens + Kong infrastructure. What is the realistic total?

### 4. Option C Cost Estimate — "$100-200+/month per architect (tokens only, before infrastructure)"

**Research questions:**
- What are Azure AI Foundry's per-token rates for frontier models (Claude, GPT-4o, etc.)?
- What Azure infrastructure costs are required beyond tokens? (App Service, Cognitive Services, storage, monitoring)
- Is the claim "3-5x more than Option A" accurate when normalizing for model quality? Show the math.
- What did the actual "Microsoft quote" reference? (The page describes it as selecting "two of the cheapest available models" — what models would those be on Azure?)

### 5. "Budget pressure will push toward cheaper models over time"

**Research questions:**
- Is there research or industry evidence on "model downgrade pressure" in enterprise AI adoption?
- Are there documented cases of organizations switching from frontier to budget models due to cost?
- Is this a well-known pattern in SaaS/cloud economics? Cite relevant literature or case studies.
- Is the "rework tax" concept (cheap models create rework that exceeds the cost savings) documented anywhere?

### 6. Architecture Work Model Quality Sensitivity

**Research questions:**
- Is there evidence that architecture tasks (multi-file reasoning, structured document generation, cross-service analysis) require frontier models?
- Are there benchmarks comparing frontier vs mid-tier vs budget models on complex reasoning, multi-file analysis, or structured document generation?
- Is "long-context fidelity" (maintaining accuracy across 100K+ tokens) truly a differentiator for frontier models? Cite benchmarks.
- The page claims budget models "produce shallow analysis, miss domain rules, generate generic boilerplate" — is there empirical evidence for this?

### 7. The Abandonment Risk Scenario

**Research questions:**
- Is there evidence of enterprise AI tool abandonment due to poor model quality?
- Are there published failure rates or adoption decay curves for enterprise AI tools?
- Is the "negative value" concept (tool produces output so poor it wastes time) documented in AI adoption literature?
- Is the 5-step worst-case scenario (build → budget pressure → poor output → abandonment → sunk cost) a recognized pattern?

---

## Expected Output Format

For each claim:
1. **Claim as stated** — exact quote from the page
2. **Verdict** — Confirmed / Partially Confirmed / Unconfirmed / Incorrect
3. **Evidence** — cited sources with URLs, dates accessed, and relevant excerpts
4. **Recommended correction** — if the claim needs updating, provide the corrected text
5. **Confidence level** — High / Medium / Low based on source quality

Include a summary table at the top with all claims and their verdicts.
