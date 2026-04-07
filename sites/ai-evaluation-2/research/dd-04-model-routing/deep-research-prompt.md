# Deep Research Prompt: DD-04 Model Routing

## Objective

DD-04 is a brief stub page that declares the model routing decision "Resolved by DD-03." Investigate the specific claims about model multipliers and the assertion that model routing is subsumed by the provider decision.

---

## Claims to Investigate

### 1. "Model routing matters only under Option B or C — Copilot handles it natively"

**Research questions:**
- Does Copilot allow users to select models, or is model selection automatic? What models are currently available in Copilot?
- Does Copilot's model selection constitute "model routing" in the same sense as OpenRouter or Azure AI Foundry routing?
- Is it accurate that model routing is a non-decision under Option A, or are there routing choices even within Copilot (e.g., choosing Claude vs GPT-4o)?

### 2. Model Multiplier Table — "GPT-4o: 1x, Claude Sonnet: 1x, Claude Opus: 3x"

**Research questions:**
- What are the current Copilot model multipliers as of mid-2026? Cite the official GitHub documentation page.
- Has GitHub changed multipliers since the page was written? Are there newer models with different multipliers?
- What is the 0x multiplier claim for GPT-4.1 and GPT-4o? When was this introduced? Cite the announcement.
- Is "no per-token cost visibility" accurate for Copilot? Are there any usage dashboards or reporting tools?

### 3. "Under Option B, model routing is a procurement and governance exercise"

**Research questions:**
- How does OpenRouter handle model routing? Can organizations restrict which models are available?
- Does Kong AI Gateway provide model routing capabilities? Cite documentation.
- What governance controls does OpenRouter offer (rate limiting, model restrictions, usage auditing)?

### 4. "Under Option C, routing is a full engineering concern"

**Research questions:**
- Does Azure AI Foundry provide built-in model routing, or must it be custom-built?
- What is Azure AI Foundry's model catalog and deployment model? Can routing be configured without custom code?
- Is "full engineering concern" an overstatement given Azure's managed services?

---

## Expected Output Format

For each claim:
1. **Claim as stated** — exact quote from the page
2. **Verdict** — Confirmed / Partially Confirmed / Unconfirmed / Incorrect
3. **Evidence** — cited sources with URLs, dates accessed, and relevant excerpts
4. **Recommended correction** — if the claim needs updating, provide the corrected text
5. **Confidence level** — High / Medium / Low based on source quality

Include a summary table at the top with all claims and their verdicts.
