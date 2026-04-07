<!-- CONFLUENCE-PUBLISH -->
<!-- CONFLUENCE-URL: https://christopherblaisdell.atlassian.net/wiki/spaces/ARCH/pages/evaluation-approach -->

# Evaluation Approach

## Principle: Test Reversible Options Before Irreversible Ones

This evaluation compares three platform options for AI-assisted architecture work. A critical — and often overlooked — constraint is that **the three options are not equally testable**.

| Option | What It Takes to Test | Time to First Scenario | Approximate Evaluation Cost | Reversible? |
|--------|----------------------|------------------------|----------------------------|-------------|
| A — GitHub Copilot | Install extension, add instruction files, run scenario | Minutes | $0.48 per scenario (subscription covers it) | Yes — cancel subscription |
| B — Roo Code + Kong | Install extension, configure Kong gateway, provision API keys, run scenario | Hours | $25–100 in API tokens per scenario | Yes — stop paying for tokens |
| C — Bespoke Agent | Design agent architecture, provision Azure AI Foundry, build VS Code extension or integrate Continue/Cline, develop prompt orchestration, build context pipeline | Weeks to months | Engineering team time + Azure infrastructure | No — sunk cost |

Options A and B can be evaluated empirically: install, configure, run a real architecture scenario, measure quality and cost, compare. Option C requires **building the product before you can test it**.

This is not a minor inconvenience. It is a structural asymmetry that shapes the entire evaluation strategy.

## The Sunk Cost Trap

Option C cannot be A/B tested against Options A and B without first investing weeks of engineering effort and Azure infrastructure cost. Once that investment is made, the evaluation is no longer neutral:

- **Confirmation bias** — the team that built the bespoke agent has professional incentive to demonstrate it works
- **Sunk cost pressure** — "we've already invested X weeks, we should make it work" replaces objective comparison
- **Scope creep** — shortcomings discovered during testing are treated as "bugs to fix" rather than evidence of a wrong approach
- **Delayed feedback** — by the time the bespoke agent is testable, Options A and B have been idle for weeks, and the organization has lost the opportunity to be productive with them

The only way to avoid this trap is to **sequence the evaluation so that Option C is the last resort, not the first experiment**.

## Phased Evaluation Strategy

### Phase 1: Empirical Comparison (Options A and B)

Run both testable options against identical architecture scenarios. Measure:

- Output quality (using the [Evaluation Methodology](evaluation-methodology.md) scoring framework)
- Cost per scenario (actual, not projected)
- Time to complete each scenario
- Context awareness (does the AI find and use the right workspace evidence?)
- Workflow friction (how much manual intervention does the architect need?)

**Duration:** 1–2 weeks. **Cost:** Negligible (subscription + token spend).

**Exit criteria for Phase 1:**

- If one option scores significantly higher and costs are acceptable → **select it. Evaluation complete.**
- If both options fail to meet quality thresholds → proceed to Phase 2.

### Phase 2: Gap Analysis (Before Building Anything)

If Phase 1 results are unsatisfactory, identify **why** before committing to bespoke engineering:

1. **What specific capabilities are missing?** — Document the exact gaps with scenario evidence
2. **Can the gaps be closed with configuration?** — Additional instruction files, MCP servers, prompt templates
3. **Are the gaps in the platform or in our usage?** — Poor results may indicate incomplete customization, not platform limitations
4. **What would a bespoke agent need to do differently?** — Define concrete requirements, not aspirations

This gap analysis produces either:

- A targeted set of enhancements to the Phase 1 winner (new MCP server, better instructions, additional prompts) — much cheaper than a bespoke build
- A clear, evidence-based specification for what a bespoke agent must achieve — which justifies Phase 3

### Phase 3: Bespoke Investment (Only If Justified)

Commission a bespoke agent build **only** with:

- Documented evidence that Options A and B failed specific, measurable criteria
- A concrete specification derived from gap analysis, not aspirational architecture diagrams
- An agreed budget and timeline with explicit go/no-go checkpoints
- A plan to A/B test the bespoke agent against the Phase 1 winner once built

Without Phase 1 and Phase 2 evidence, Phase 3 is speculative engineering.

## Decision Sequencing

The phased evaluation strategy also determines the order in which toolchain decisions (DD-01 through DD-04) should be resolved:

| Decision | When to Resolve | Why This Order |
|----------|-----------------|----------------|
| DD-01 Context and Configuration | Phase 1 | If native context injection meets requirements, the largest argument for custom infrastructure disappears |
| DD-02 Billing Model | Phase 1 | Actual cost data from scenario runs replaces projections |
| DD-03 AI Provider | Phase 1 | Provider is determined by the platform that wins Phase 1 |
| DD-04 Model Routing | Phase 1 / Phase 2 | Only relevant if the winning platform supports multiple models |
| DD-05 VS Code AI Plugin | Phase 3 only | Only relevant if Option C is pursued |

**The key insight:** DD-01 through DD-04 can be resolved with empirical evidence from Phase 1. DD-05 only becomes relevant if Phase 1 and Phase 2 fail. Resolving DD-01 through DD-04 first prevents premature commitment to bespoke engineering.

## What This Means for Option C

Option C is not dismissed. It is **sequenced correctly**. If Options A and B genuinely cannot meet the architecture practice's needs — and Phase 2 gap analysis confirms this with evidence — then a bespoke agent is the right investment.

But investing in Option C before testing Options A and B is building a custom house before checking whether an existing one meets your needs. The evaluation approach ensures that the organization only pays for bespoke engineering when it has empirical proof that off-the-shelf solutions are insufficient.

See also: [Build vs Leverage](../evidence/build-vs-leverage.md) for a detailed analysis of when custom RAG pipelines are justified versus when they reinvent capabilities that already exist natively.
