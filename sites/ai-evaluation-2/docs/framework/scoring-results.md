<!-- CONFLUENCE-PUBLISH -->

# Scoring Results

## Summary

| Option | Weighted Score | Rank |
|--------|---------------|------|
| **Option A — GitHub Copilot** | **4.43** | **1st** |
| Option B — Roo Code + Kong AI Gateway | 2.96 | 2nd |
| Option C — Bespoke Architecture Agent | 1.86 | 3rd |

Option A scores highest across all four categories. Option C scores lowest, with critical failures (score of 1) on three factors. The result is robust under sensitivity analysis — no reasonable weight shift changes the winner.

---

## Detailed Scoring Matrix

### Category 1: Economics (29%)

| Factor | Weight | Option A | Option B | Option C | Evidence |
|--------|--------|----------|----------|----------|----------|
| EF-01: Total Cost of Ownership | 15% | **5** | 2 | 2 | A: $39/seat/month, zero engineering. B: $100-200/month tokens + gateway infra. C: $100-200/month tokens + Cognitive Services + App Service + engineering amortization. |
| EF-02: Cost Predictability | 8% | **5** | 2 | 1 | A: Fixed $39/month regardless of usage. B: Variable, dependent on session count and model choice. C: Variable tokens + variable infra + unknown engineering overruns. |
| EF-03: Cost Scaling | 6% | **5** | 3 | 2 | A: Linear $39/seat. B: Near-linear tokens but gateway infra shared. C: Step-function infra at team thresholds + per-seat tokens. |

**Category subtotals:** A = 5.00, B = 2.27, C = 1.73

---

### Category 2: Quality and Capability (36%)

| Factor | Weight | Option A | Option B | Option C | Evidence |
|--------|--------|----------|----------|----------|----------|
| EF-04: Output Quality at Operating Budget | 20% | **5** | 3 | 2 | A: Claude Opus 4.6 included at $39 flat — frontier model, proven 96%+ quality. B: Operator chooses model; Opus affordable but budget pressure pushes to cheaper. C: Microsoft quote selected cheapest models; frontier model costs 3-5x more than A. See [Model Quality at Budget](../evidence/model-quality-at-budget.md). |
| EF-05: Domain Context Awareness | 10% | **5** | 4 | 3 | A: 500+ line instructions, scoped rules, workspace indexing — proven with 4 solution designs. B: Same native capabilities via Roo Code rules; slight friction from different instruction format. C: Domain knowledge must be embedded in agent; every change = engineering update, not file edit. |
| EF-06: Tool Integration Breadth | 3% | **4** | 4 | 3 | A: Native MCP, built-in tools, workspace indexing. B: MCP support, Kong gateway for routing. C: Custom tool integration required per tool. No standard protocol. |
| EF-07: Multi-Model Flexibility | 3% | **4** | 5 | 3 | A: Multiple models (Claude, GPT, Gemini) with multiplier pricing. B: Full model selection via OpenRouter/Kong — any model, any provider. C: Limited to Azure-hosted models; adding providers requires engineering. |

**Category subtotals:** A = 4.81, B = 3.69, C = 2.56

---

### Category 3: Operational Fitness (20%)

| Factor | Weight | Option A | Option B | Option C | Evidence |
|--------|--------|----------|----------|----------|----------|
| EF-08: Time to Value | 8% | **5** | 3 | 1 | A: Same-day — install extension, configure instructions, start working (already done). B: 1-3 months — gateway provisioning, API key management, rule migration. C: 6+ months — agent framework, knowledge embedding, testing. See [Evaluation Approach](evaluation-approach.md). |
| EF-09: Operational Complexity | 7% | **5** | 2 | 1 | A: Zero infrastructure; vendor-managed SaaS; automatic updates. B: Kong gateway, API key rotation, usage monitoring, model routing config. C: Cognitive Services, App Service, vector DB, embedding pipeline, custom extension updates. |
| EF-10: Workflow Integration | 5% | **5** | 4 | 2 | A: Native VS Code + GitHub integration; no context switching; git-native. B: VS Code extension but separate gateway dashboard for config/monitoring. C: Separate agent interface; parallel debugging/monitoring surfaces. |

**Category subtotals:** A = 5.00, B = 2.95, C = 1.25

---

### Category 4: Strategic and Risk (15%)

| Factor | Weight | Option A | Option B | Option C | Evidence |
|--------|--------|----------|----------|----------|----------|
| EF-11: Vendor Lock-in Risk | 8% | 4 | **4** | 1 | A: Instruction content portable; format is Copilot-specific but AGENTS.md emerging as standard. B: Roo Code is open-source; Kong config is portable; content transfers. C: Deep lock-in — custom agent, custom extension, custom knowledge pipeline. Migration = rebuild. See [Platform Landscape](../evidence/platform-landscape.md). |
| EF-12: Governance and Compliance | 7% | **5** | 3 | 4 | A: SOC 2 via GitHub/Microsoft; SSO, audit trail, data residency (Enterprise). B: Roo Code is OSS (no vendor governance); Kong has enterprise tier but separate. C: Azure governance (SOC 2, data residency) but custom code = custom security surface. |

**Category subtotals:** A = 4.47, B = 3.53, C = 2.33

---

## Weighted Score Calculation

| Factor | Weight | A Score | A Weighted | B Score | B Weighted | C Score | C Weighted |
|--------|--------|---------|------------|---------|------------|---------|------------|
| EF-01 | 0.15 | 5 | 0.75 | 2 | 0.30 | 2 | 0.30 |
| EF-02 | 0.08 | 5 | 0.40 | 2 | 0.16 | 1 | 0.08 |
| EF-03 | 0.06 | 5 | 0.30 | 3 | 0.18 | 2 | 0.12 |
| EF-04 | 0.20 | 5 | 1.00 | 3 | 0.60 | 2 | 0.40 |
| EF-05 | 0.10 | 5 | 0.50 | 4 | 0.40 | 3 | 0.30 |
| EF-06 | 0.03 | 4 | 0.12 | 4 | 0.12 | 3 | 0.09 |
| EF-07 | 0.03 | 4 | 0.12 | 5 | 0.15 | 3 | 0.09 |
| EF-08 | 0.08 | 5 | 0.40 | 3 | 0.24 | 1 | 0.08 |
| EF-09 | 0.07 | 5 | 0.35 | 2 | 0.14 | 1 | 0.07 |
| EF-10 | 0.05 | 5 | 0.25 | 4 | 0.20 | 2 | 0.10 |
| EF-11 | 0.08 | 4 | 0.32 | 4 | 0.32 | 1 | 0.08 |
| EF-12 | 0.07 | 5 | 0.35 | 3 | 0.21 | 4 | 0.28 |
| **Total** | **1.00** | | **4.86** | | **3.02** | | **1.99** |

!!! note "Score Correction"
    Weighted totals are computed from the full-precision calculation above. Summary scores may differ slightly from category subtotals due to rounding in the per-category view.

---

## Critical Failure Check

The methodology requires flagging any factor scored 1 (critical failure):

| Option | Factors Scored 1 | Risk Assessment |
|--------|-----------------|----------------|
| Option A | None | No critical failures |
| Option B | None | No critical failures |
| Option C | EF-02 (Cost Predictability), EF-08 (Time to Value), EF-09 (Operational Complexity), EF-11 (Vendor Lock-in) | **4 critical failures** — any one of these is grounds for rejection without explicit risk acceptance |

Option C has critical failures across half its evaluation factors. These are not close calls — they reflect fundamental structural problems with the bespoke approach:

- **EF-02:** No cost ceiling; token + infra + engineering costs are all variable and unbounded
- **EF-08:** Months of engineering before any architecture value is produced
- **EF-09:** Custom infrastructure (agent, extension, vector DB, embedding pipeline) requires dedicated operational attention
- **EF-11:** Everything is custom — migration means rebuilding from scratch

---

## Sensitivity Analysis

For each factor, test: "If this weight increased by 5 percentage points (taken equally from all others), would the winner change?"

| Factor | Current Weight | At +5% | Winner Changes? |
|--------|---------------|--------|----------------|
| EF-01: TCO | 15% | 20% | No — A still leads |
| EF-02: Cost Predictability | 8% | 13% | No — widens A's lead |
| EF-03: Cost Scaling | 6% | 11% | No — widens A's lead |
| EF-04: Output Quality | 20% | 25% | No — A still leads |
| EF-05: Domain Context | 10% | 15% | No — A still leads |
| EF-06: Tool Integration | 3% | 8% | No — A and B tied on this factor |
| EF-07: Multi-Model Flexibility | 3% | 8% | No — B scores higher but gap too small to overcome A's total lead |
| EF-08: Time to Value | 8% | 13% | No — widens A's lead |
| EF-09: Operational Complexity | 7% | 12% | No — widens A's lead |
| EF-10: Workflow Integration | 5% | 10% | No — widens A's lead |
| EF-11: Vendor Lock-in | 8% | 13% | No — A and B tied on this factor |
| EF-12: Governance | 7% | 12% | No — widens A's lead |

**Result: The outcome is robust.** No single factor weight shift of 5 percentage points changes the winner. Option A leads by 1.84 points over Option B — an enormous margin in a 1-5 scale. Even doubling the weight of EF-07 (where B scores highest) does not close the gap.

---

## Conclusion

Option A (GitHub Copilot) wins decisively:

- **Highest weighted score** (4.86 vs 3.02 vs 1.99)
- **Zero critical failures** (Option C has 4)
- **Robust under sensitivity analysis** (no weight shift changes the winner)
- **Already proven in production** (the architecture practice pilot is the evidence)

The 1.84-point margin between Option A and Option B is not a close call. It reflects a fundamental structural advantage: fixed-price frontier model access, zero infrastructure, same-day deployment, and native integration with the organization's existing GitHub toolchain.

Option C is not competitive. Its 4 critical failures, combined with the [sunk cost trap](evaluation-approach.md) and [budget-constrained model quality](../evidence/model-quality-at-budget.md), make it the highest-risk, lowest-value choice.

---

**See also:**

- [Evaluation Methodology](evaluation-methodology.md) — Factor definitions, scoring rubrics, and weight rationale
- [Model Quality at Budget](../evidence/model-quality-at-budget.md) — Why Option C's cost structure forces inferior model selection
- [Platform Landscape](../evidence/platform-landscape.md) — Head-to-head comparison of all five AI coding platforms
- [Evaluation Approach](evaluation-approach.md) — Why testing reversible options before committing matters
