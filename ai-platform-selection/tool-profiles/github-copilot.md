# GitHub Copilot Pro+

## Tool Profile

| | |
|---|---|
| **Type** | Commercial AI assistant (SaaS) |
| **IDE Integration** | VS Code (native), JetBrains, Neovim |
| **Agent Mode** | Yes -- autonomous multi-step execution |
| **Pricing** | $39/month (Pro+), includes 1,500 premium requests |
| **Model Used** | Claude Opus 4.6 (3x multiplier) |
| **Workspace Indexing** | Server-side vector database (automatic) |
| **Vendor** | Microsoft / GitHub |

---

## Architecture

GitHub Copilot operates as a fully managed SaaS platform. The key architectural characteristics that drive its cost advantage:

### Server-Side Workspace Indexing

Copilot automatically indexes the entire workspace into a server-side vector database. When the AI needs context, it performs semantic retrieval -- pulling only the relevant snippets from specs, source code, and decision history. The developer does not need to manually select files or configure external infrastructure.

| Characteristic | Detail |
|---------------|--------|
| Index location | GitHub servers (not local) |
| Index trigger | Automatic on workspace open |
| Retrieval method | Semantic search against vector embeddings |
| Context selection | Server-side -- sends curated snippets, not full files |
| Infrastructure required | None -- fully managed |

### Intent-Based Billing

Copilot charges per **user prompt**, not per model invocation. In Agent Mode, the autonomous tool-call loop is entirely free -- absorbed by GitHub's infrastructure.

**What is billed:** Each time a human types a prompt and presses Enter, one base request is consumed, multiplied by the model's rate.

**What is NOT billed:**

- File reads and workspace searches
- Terminal command executions
- Sub-agent invocations
- Context summarization (when approaching token limits)
- Parallel tool calls

This means a 4-prompt session that triggers 50+ autonomous tool calls costs exactly:
`4 prompts x 3x (Claude Opus 4.6) x $0.04 = $0.48`

See [Copilot Billing Mechanics](../research/copilot-billing.md) for the full analysis.

---

## Pricing

### Copilot Pro+ Plan

| Parameter | Value |
|-----------|-------|
| Monthly subscription | $39 |
| Included premium requests | 1,500/month |
| Overage rate | $0.04 per premium request |
| Reset cycle | 1st of calendar month, 00:00 UTC |
| Unused requests | Do not roll over |

### Model Multipliers (March 2026)

| Model | Multiplier | Cost per Prompt |
|-------|-----------|-----------------|
| GPT-4.1, GPT-4o | 0x | $0 (unlimited) |
| Claude Sonnet 4, o4-mini, Gemini 2.5 Pro | 1x | $0.04 |
### Monthly Capacity at Pro+

At 12 premium requests per run (4 prompts x 3x multiplier):

- **125 runs/month** within the included 1,500 allowance
- **$0 overage** for typical architecture workloads (38 runs/month)
- Effective cost per run: **$0.48 notional** ($0 actual, absorbed by subscription)

---

## Evaluation Results

### Quality Scores (Run 001)

| Scenario | Score | Max | Percentage |
|----------|-------|-----|-----------|
| SC-01: Ticket Triage | 23 | 25 | 92% |
| SC-02: Solution Design | 33 | 35 | 94% |
| SC-03: Investigation | 30 | 30 | 100% |
| SC-04: Architecture Update | 24 | 25 | 96% |
| SC-05: Publishing Prep | 39 | 40 | 98% |
| **Total** | **149** | **155** | **96.1%** |

### Demonstrated Capabilities

- Autonomous multi-step execution -- all 5 scenarios completed in a single session
- Correct architectural reasoning (data ownership violation identification in SC-03)
- MADR-compliant ADR generation (9 ADRs created/formatted)
- Valid PlantUML diagram generation (2 diagrams created/modified)
- All 3 mock tools used appropriately across scenarios
- Scope discipline in SC-04 (limited changes to approved solution design)
- Source code gap analysis in SC-05 (4 specific code gaps identified)

### Cost Evidence (March 4, 2026)

| Metric | Value |
|--------|-------|
| User prompts in session | 4 |
| Premium requests consumed | 12 (4 x 3x multiplier) |
| Notional session cost | $0.48 |
| Day-total premium requests | 120 (all projects) |
| Day-total notional cost | $4.80 |
| Actual overage charged | $0 (within 1,500 included) |

---

## Strengths

1. **Cost predictability** -- $39/month flat fee regardless of usage volume within the included allowance
2. **Zero infrastructure** -- no gateway, no vector database, no embedding provider to maintain
3. **Workspace awareness** -- automatic server-side indexing means the AI has full context without manual file selection
4. **GitHub ecosystem** -- PR reviews, code suggestions, repository context, issue integration
5. **Agent mode maturity** -- autonomous loop handles complex multi-step architecture tasks reliably
6. **Sub-agent delegation** -- can spawn isolated sub-agents for deep research without polluting the primary session

---

## Limitations

1. **No per-request token visibility** -- cost estimates are approximations based on prompt counting; no generation-level billing data
2. **Context summarization** -- long sessions trigger lossy context compression, which may degrade quality across extended interactions
3. **Model selection constrained** -- limited to models GitHub offers; cannot bring arbitrary models
4. **Fixed cost floor** -- light months still cost $39/seat regardless of actual usage
5. **Telemetry opacity** -- no way to export the exact cost of a single Agent Mode session from native tooling
6. **Sub-agent model routing** -- sub-agents may default to zero-multiplier models instead of the requested premium model (documented bug)

---

## Customization

Copilot supports a layered customization system:

| Mechanism | Scope | File |
|-----------|-------|------|
| Workspace instructions | Always loaded for repo | `.github/copilot-instructions.md` |
| Folder instructions | Loaded when working in directory | `.instructions.md` |
| Reusable prompts | On-demand slash commands | `.prompt.md` |
| Custom agents | Specialized agent behaviors | Agent definitions |

The NovaTrek workspace uses a 700+ line `copilot-instructions.md` that encodes the full domain model, architecture standards, mock tool usage patterns, and solution design workflow. See the [AI Instruction site](https://ai.customization.novatrek.cc) for detailed customization guidance.
