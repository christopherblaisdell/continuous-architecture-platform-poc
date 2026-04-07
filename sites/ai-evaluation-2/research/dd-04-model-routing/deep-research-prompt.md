# Deep Research Prompt: DD-04 Model Routing

## Objective

DD-04 now contains the evaluation's most important honest caveat: that Copilot's model routing is opaque and Microsoft controls which model handles each inference in the agentic loop. Every claim about this opacity — and every argument for why the trade-off is acceptable — must be verified.

---

## Claims to Investigate

### 1. "Selecting Claude Opus 4.6 governs the primary reasoning model, but Microsoft's orchestration layer routes internal agentic steps to models of its choosing"

**Research questions:**
- What is publicly documented about Copilot's internal model routing? Does Microsoft disclose which models handle tool dispatch, summarization, or context assembly?
- Has Microsoft published any architecture diagrams or blog posts describing Copilot's multi-model orchestration?
- Are there any third-party investigations (blog posts, research papers, reverse engineering) that reveal Copilot's internal model routing?
- Is "primary reasoning model" an accurate characterization of what the user's model selection controls?

### 2. "Copilot provides no per-request model attribution"

**Research questions:**
- Does Copilot expose any telemetry, logs, or dashboards showing which model handled a request?
- Does Copilot Enterprise or Business offer any model attribution features not available in Pro+?
- Are there VS Code developer tools, network inspection, or extension APIs that reveal model routing information?
- Has GitHub indicated any plans to add model attribution or transparency features?

### 3. "Microsoft has a financial incentive to route non-critical inferences to cheaper models — this is how fixed-price bundling works economically"

**Research questions:**
- Is this characterization of the economic incentive accurate? Cite any industry analysis of how AI SaaS providers manage model costs under fixed-price subscriptions.
- Has Microsoft discussed its cost management strategy for Copilot? (Investor calls, blog posts, interviews)
- Are there analogous examples in other industries of fixed-price bundling where the provider optimizes internal resource allocation? (e.g., cell phone unlimited plans, cloud compute reservations)

### 4. "If Microsoft were routing the primary reasoning to a budget model, these outputs would not be achievable"

**Research questions:**
- Is this inference valid? Could a mid-tier model (e.g., Claude Sonnet, GPT-4o) produce the claimed outputs (multi-file reasoning, domain rule enforcement, structured document generation)?
- What are the documented capability differences between frontier models (Opus) and mid-tier models (Sonnet) for complex reasoning tasks?
- Are there benchmarks comparing Opus vs Sonnet on multi-file synthesis, instruction following, or structured document generation?

### 5. Model Multiplier Table — "GPT-4o: 0x, Claude Sonnet: 1x, Claude Opus: 3x"

**Research questions:**
- What are the current Copilot model multipliers as of mid-2026? Cite the official GitHub documentation.
- Has GitHub changed multipliers since the page was written?
- What is the 0x multiplier for GPT-4o and GPT-4.1? When was this introduced?
- Is "no per-token cost visibility" accurate for Copilot?

### 6. "The risk is self-correcting — if Microsoft degrades Copilot's model routing, the architect observes this directly"

**Research questions:**
- Is this argument sound? Can an architect reliably detect gradual model quality degradation in their own work?
- Is there research on human ability to detect AI output quality changes? (Studies on "boiling frog" effects in AI-assisted work)
- Are there documented cases of AI service providers quietly downgrading model quality? How were they detected?
- Could Microsoft gradually shift routing without users noticing a discrete quality drop?

### 7. Option B and C Transparency Claims

**Research questions:**
- Does OpenRouter provide full per-request model attribution and token-level cost visibility? Cite documentation.
- Does Kong AI Gateway provide per-request logging with model attribution? Cite documentation.
- Is "full control" accurate for Option C, or are there Azure AI Foundry abstractions that also obscure routing?

### 8. "What Would Change This Assessment" — per-request model attribution

**Research questions:**
- Has any AI coding platform introduced per-request model attribution?
- Is there an industry trend toward model transparency in AI SaaS products?
- Are there regulatory pressures (EU AI Act, etc.) that might force model attribution?

---

## Expected Output Format

For each claim:
1. **Claim as stated** — exact quote from the page
2. **Verdict** — Confirmed / Partially Confirmed / Unconfirmed / Incorrect
3. **Evidence** — cited sources with URLs, dates accessed, and relevant excerpts
4. **Recommended correction** — if the claim needs updating, provide the corrected text
5. **Confidence level** — High / Medium / Low based on source quality

Include a summary table at the top with all claims and their verdicts.
