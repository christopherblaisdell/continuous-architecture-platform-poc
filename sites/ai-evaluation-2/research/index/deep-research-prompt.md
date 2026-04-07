# Deep Research Prompt: Index (Home Page)

## Objective

Investigate every factual claim, pricing figure, and architectural assertion made on the AI Toolchain Evaluation home page. Return a comprehensive, source-cited research document that either validates or corrects each claim.

---

## Claims to Investigate

### 1. GitHub Copilot Billing Model

The page states Option A uses "intent-based billing" and has "native workspace indexing" and "declarative customization via instruction files."

**Research questions:**
- Confirm GitHub Copilot Pro+ uses intent-based billing (per user prompt, not per token). Cite the official GitHub documentation or pricing page.
- What exactly counts as a "premium request" in Copilot? Does each user prompt in Agent Mode consume one premium request, or do tool calls / sub-agent invocations also consume requests?
- What is the current multiplier for Claude Opus 4.6 on Copilot? Is it 3x as claimed elsewhere on the site?
- Does Copilot perform server-side workspace indexing automatically? Cite documentation.
- What declarative customization mechanisms does Copilot support? (instruction files, skills, agent modes, hooks, MCP) — cite official docs for each.

### 2. Roo Code + Kong AI Gateway

The page states Option B is an "open-source IDE extension with token-based billing through a self-managed API gateway" that is "testable with moderate setup, requires API key provisioning and gateway configuration."

**Research questions:**
- Is Roo Code open-source? Under what license? Cite the repository.
- Does Roo Code support token-based billing through Kong or OpenRouter? How does billing work?
- What setup is actually required to get Roo Code + Kong operational? Is "moderate setup" accurate or understated/overstated?
- Does Roo Code support declarative instruction files (.clinerules)? What customization mechanisms does it offer?

### 3. Option C — Azure AI Foundry

The page states Option C is a "custom-built agent on Azure AI Foundry" that "requires weeks of engineering investment before testing can begin."

**Research questions:**
- What is Azure AI Foundry? What capabilities does it provide for building custom AI agents? Cite Microsoft documentation.
- What is the minimum viable engineering effort to build a custom architecture agent on Azure AI Foundry? Is "weeks" accurate?
- What are the infrastructure components required (Cognitive Services, App Service, etc.)?

### 4. Phased Evaluation Principle

The page states: "test reversible, low-cost options empirically before committing to irreversible, high-cost alternatives."

**Research questions:**
- Is this a recognized evaluation methodology in technology decision-making? Cite academic or industry sources that support or describe this principle (e.g., real options theory, lean startup, set-based design).
- Are there counterarguments in the literature for when investing in the more complex option first is justified?

### 5. Architecture Practice Pilot Claims

The page states the pilot "produced 4 complete solution designs, 14 architecture decision records, 139 generated sequence diagrams, and a live documentation portal" with "zero custom engineering, zero infrastructure."

**Research questions:**
- These are internal claims about a specific pilot — they cannot be externally verified. Flag this as self-reported evidence and recommend how to make it independently verifiable (e.g., link to the actual artifacts, provide before/after comparisons, include third-party review).

---

## Expected Output Format

For each claim:
1. **Claim as stated** — exact quote from the page
2. **Verdict** — Confirmed / Partially Confirmed / Unconfirmed / Incorrect
3. **Evidence** — cited sources with URLs, dates accessed, and relevant excerpts
4. **Recommended correction** — if the claim needs updating, provide the corrected text
5. **Confidence level** — High / Medium / Low based on source quality

Include a summary table at the top with all claims and their verdicts.
