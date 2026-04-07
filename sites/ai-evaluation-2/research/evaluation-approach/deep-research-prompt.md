# Deep Research Prompt: Evaluation Approach

## Objective

Investigate every factual claim, methodological assertion, and decision-theory principle on the Evaluation Approach page. This page establishes the evaluation sequencing strategy — its credibility depends on the underlying principles being well-supported by decision science literature.

---

## Claims to Investigate

### 1. Testability Asymmetry — "Minutes / $0.48" for Option A

**Research questions:**
- Confirm that GitHub Copilot can be installed and producing output within minutes. Is there any provisioning delay for enterprise organizations?
- Is $0.48 per scenario accurate? This assumes 4 prompts x 3x multiplier x $0.04. Verify the $0.04 per premium request rate and the 3x Claude Opus 4.6 multiplier from official sources.
- Does "install extension, add instruction files, run scenario" accurately describe the setup process? Are there additional steps (e.g., GitHub organization approval, license assignment)?

### 2. Testability Asymmetry — "$25-100 in API tokens per scenario" for Option B

**Research questions:**
- Calculate the actual token cost for a single architecture scenario using Claude Opus 4.6 via OpenRouter. Assume: 10-20 file reads (~100K input tokens), 4-6 user prompts, ~5K output tokens per response.
- What are the current OpenRouter per-token rates for Claude Opus 4.6? Cite the pricing page.
- Is "$25-100 per scenario" accurate, or is it overstated/understated?

### 3. Testability Asymmetry — "Weeks to months" for Option C, "No — sunk cost"

**Research questions:**
- What does Azure AI Foundry offer for building custom agents? Does it have low-code/no-code options that could reduce the timeline?
- Are there reference architectures or quickstarts from Microsoft that could accelerate Option C below "weeks"?
- Is it accurate to call Option C's investment "sunk cost" (not reversible)? Could any components (e.g., prompt designs, knowledge bases) be reused if Option C is abandoned?

### 4. The Sunk Cost Trap — Confirmation Bias and Scope Creep

**Research questions:**
- Cite academic sources on sunk cost fallacy in technology investment decisions (e.g., Arkes & Blumer 1985, Staw 1976 "Knee-deep in the big muddy").
- Is "confirmation bias" a documented risk in technology evaluation when the evaluation team built one of the options? Cite organizational behavior or IT governance literature.
- Is "scope creep" during evaluation testing a documented phenomenon? Cite relevant sources.

### 5. Phased Evaluation Strategy

**Research questions:**
- Is the "test cheap/reversible first, then expensive/irreversible" approach supported by decision theory? Cite real options theory (e.g., Dixit & Pindyck 1994), set-based concurrent engineering, or lean startup methodology.
- Are there established frameworks for sequencing technology evaluations (e.g., Gartner, Forrester, ThoughtWorks Technology Radar approach)?
- What are the counterarguments? When is it justified to invest in the most complex option first?

### 6. Phase 2 Gap Analysis Before Building

**Research questions:**
- Is root cause analysis before build commitment a standard practice in enterprise architecture? Cite TOGAF, Zachman, or other framework guidance on evaluation before implementation.
- Are there case studies of organizations that skipped gap analysis and went straight to bespoke builds, with documented outcomes?

### 7. Decision Sequencing — "DD-01 through DD-04 can be resolved with empirical evidence from Phase 1"

**Research questions:**
- Is decision decomposition (breaking a large decision into smaller, sequenced decisions) a recognized technique in decision analysis? Cite sources (e.g., Howard & Abbas, Keeney's value-focused thinking).
- Is the claim that resolving DD-01 first "makes the largest argument for custom infrastructure disappear" logically sound? Could a skeptic argue that DD-01 should be decided after DD-03?

---

## Expected Output Format

For each claim:
1. **Claim as stated** — exact quote from the page
2. **Verdict** — Confirmed / Partially Confirmed / Unconfirmed / Incorrect
3. **Evidence** — cited sources with URLs, dates accessed, and relevant excerpts
4. **Recommended correction** — if the claim needs updating, provide the corrected text
5. **Confidence level** — High / Medium / Low based on source quality

Include a summary table at the top with all claims and their verdicts.
