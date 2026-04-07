# Deep Research Prompt: AI Toolchain Evaluation Site — Complete Fact Check

## Objective

This is a comprehensive research prompt covering every factual claim, pricing figure, competitive comparison, behavioral assertion, and architectural argument across all 12 pages of the AI Toolchain Evaluation site at https://ai.evaluation.novatrek.cc. The site recommends GitHub Copilot (Option A) over Roo Code + Kong (Option B) and a bespoke Azure AI Foundry agent (Option C) for an enterprise architecture practice.

A knowledgeable skeptic — someone familiar with AI platforms, enterprise procurement, and architecture tooling — should not be able to find an unsubstantiated or incorrect claim after this research is applied.

**For every claim investigated below, return:**

1. **Claim as stated** — exact quote or paraphrase from the page
2. **Verdict** — Confirmed / Partially Confirmed / Unconfirmed / Incorrect
3. **Evidence** — cited sources with URLs, dates accessed, and relevant excerpts
4. **Recommended correction** — if the claim needs updating, provide corrected text
5. **Confidence level** — High / Medium / Low based on source quality

**Include a summary table at the top of results with all claims and their verdicts.**

---

## Part 1: GitHub Copilot — Pricing, Billing, and Model Access

These claims appear across multiple pages (index, DD-02, DD-04, scoring-results, model-quality-at-budget, platform-landscape).

### 1.1 Copilot Pro+ Pricing

- Is GitHub Copilot Pro+ $39/month? Is Business $19/user/mo and Enterprise $39/user/mo? Cite current pricing page.
- Is the billing model "intent-based" (per user prompt, not per token)? What exactly counts as a "premium request"? Does each user prompt in Agent Mode consume one premium request, or do tool calls / sub-agent invocations also consume requests?
- Is the overage rate $0.04 per premium request? Cite documentation.
- Is 1,500 premium requests/month included? Does "~500 Opus-tier sessions" follow from 1,500 / 3 = 500?

### 1.2 Model Multipliers

- What are the current Copilot model multipliers as of mid-2026? Cite official GitHub documentation.
- Is Claude Opus 4.6 at 3x multiplier? Is GPT-4o at 0x (unlimited, free)? Is GPT-4.1 at 0x?
- Has GitHub changed multipliers since early 2026? Are there newer models with different multipliers?
- Are there any usage limits on 0x models (rate limits, daily caps)?

### 1.3 Session Cost Calculation

- Is $0.48 the correct cost for a 4-prompt Opus session? (4 prompts x 3x multiplier x $0.04 = $0.48)
- Is "$5-15 per session" on per-token platforms accurate? Calculate using current Claude Opus 4.6 per-token rates via OpenRouter and Anthropic API for ~100K input tokens + ~5-20K output tokens.
- Is "$100-200+/month per architect at 20 sessions/month" accurate for per-token billing? Show the calculation.

### 1.4 Model Transparency and Routing Opacity

- When an architect selects "Claude Opus 4.6" in Copilot, what does that selection actually control? Does Microsoft disclose which models handle tool dispatch, summarization, context assembly, or sub-agent steps within the agentic loop?
- Has Microsoft published any architecture diagrams or blog posts describing Copilot's multi-model orchestration?
- Does Copilot expose any telemetry, logs, or dashboards showing which model handled which inference? Does Enterprise/Business offer model attribution not available in Pro+?
- Are there third-party investigations (blog posts, network inspection, reverse engineering) revealing Copilot's internal model routing?
- Has GitHub indicated any plans to add per-request model attribution?

### 1.5 Financial Incentive Alignment

- Is the characterization that "Microsoft has a financial incentive to route non-critical inferences to cheaper models" accurate? Cite industry analysis of how AI SaaS providers manage costs under fixed-price subscriptions.
- Has Microsoft discussed Copilot's cost management strategy? (Investor calls, blog posts, interviews)
- Are there analogous examples of fixed-price bundling with opaque internal resource allocation? (Cell phone unlimited plans, cloud reservations)

---

## Part 2: Competing Platforms — Pricing, Capabilities, Governance

These claims primarily appear on platform-landscape, with supporting references in DD-01, DD-03, and build-vs-leverage.

### 2.1 Cursor

- Is Cursor Pro $20/mo and Pro+ $60/mo? Is Teams $40/user/mo? What quota system do they use? Cite pricing page.
- Is "3x usage at Pro+" accurate? What does that mean exactly?
- Does Cursor use `.cursor/rules/*.md` with "Always Apply"? Do they support a Skills marketplace? Cite documentation.
- Does Cursor support AGENTS.md? MCP? Sub-agents? Cite documentation for each.
- Does Cursor have SOC 2 Type II? SSO at Teams/Enterprise? Privacy Mode "enforced at team level"? Cite trust/security pages.
- What are Cursor's custom models (Tab, agent-specific fine-tunes)? Are they publicly documented? What benchmarks exist?
- Is Cursor still a VS Code fork? Do they support JetBrains? Cite documentation.
- Is "US-primary; no region selection" accurate for data residency? Cite documentation.

### 2.2 Windsurf

- Is Windsurf Pro $20/mo and Max $200/mo? Teams $40/user/mo? What is the daily/weekly refresh model? Cite pricing page.
- **CRITICAL**: Windsurf was acquired by OpenAI — has pricing, branding, or feature set changed? What is the current status?
- Does Windsurf use `.windsurf/rules/*.md` (always_on)? Support `.windsurf/skills/` with SKILL.md? Support Workflows? Cite documentation.
- Is SWE-1.5 a real, published model? What benchmarks exist? What happened to it post-acquisition?
- Is SOC 2 status truly "Not published"? Is "Automated zero retention (Teams)" accurate? Cite documentation.
- Does Windsurf still maintain a VS Code fork or has OpenAI integrated it differently? Cite current status.

### 2.3 Cline / Roo Code

- Is Cline still free and open source? Under what license? Cite repository.
- What is Roo Code's relationship to Cline? Who maintains each? What is the current project status?
- Does Cline use `.clinerules/*.md`? Support conditional rules with path globs? Custom modes? Cite documentation.
- Does Cline support MCP? AGENTS.md? Cite documentation.
- Is Cline truly VS Code only? Cite documentation.
- Does the claim "Cline is capable but lacks structured abstractions" fair? What abstractions does Cline offer?
- Does Cline's documentation use `architecture.md` as an example rule file at docs.cline.bot/customization/cline-rules? Verify this specific citation.

### 2.4 Claude Code

- Is Claude Code part of an Anthropic subscription? What are actual pricing tiers? Cite pricing page.
- Does Claude Code use `CLAUDE.md` with subdirectory support? Cite documentation.
- Is it accurate that Claude Code has no Skills, no custom agent modes, and no AGENTS.md support? Cite documentation.
- Is Claude Code truly terminal-only, or does it have VS Code integration? Cite documentation.
- Does Claude Code support MCP natively? Sub-agents? Cite documentation.

### 2.5 Kong AI Gateway

- What does Kong AI Gateway cost? Is there a free tier? What are enterprise pricing tiers? Cite documentation.
- Does Kong provide model routing capabilities, per-request logging, and enterprise governance (SOC 2, audit trails)? Cite documentation.

### 2.6 OpenRouter

- Does OpenRouter provide full per-request model attribution and token-level cost visibility? Cite documentation.
- What is OpenRouter's markup on Claude Opus 4.6 vs direct Anthropic API pricing?
- What governance controls does OpenRouter offer (rate limiting, model restrictions, usage auditing)?

---

## Part 3: Azure AI Foundry (Option C)

Claims across DD-03, model-quality-at-budget, build-vs-leverage, and platform-landscape.

### 3.1 Capabilities and Costs

- What is Azure AI Foundry? What capabilities does it provide for building custom AI agents? Cite Microsoft documentation.
- What compliance certifications does it carry? (SOC 2, ISO 27001, etc.)
- What are the per-token rates for frontier models on Azure (Claude, GPT-4o, etc.)?
- What infrastructure costs are required beyond tokens? (App Service, Cognitive Services, storage, monitoring)
- Is "weeks of engineering" accurate for minimum viable custom architecture agent? Or is this overstated/understated?

### 3.2 Characterization Fairness

- Is "custom code = custom security surface" fair? How much security surface is inherited from Azure vs custom?
- Is "every domain change requires agent update, not just a file edit" accurate? Can Azure AI Foundry agents use file-based knowledge, prompt templates, or grounding data?
- Are there Azure AI Foundry security best practices or reference architectures that mitigate the custom security concern?
- Is "full control" accurate for Option C routing, or do Azure abstractions also obscure some routing?

### 3.3 The Microsoft Quote

- The site references a Microsoft quote selecting "two of the cheapest available models." What models would those be on Azure in mid-2026?
- Is "3-5x more than Option A to deliver equivalent output" accurate when normalizing for model quality? Show the math.

---

## Part 4: Evaluation Methodology and Scoring

Claims from evaluation-methodology and scoring-results.

### 4.1 Methodology Design

- Is 12 factors a reasonable count for a technology evaluation? Cite decision analysis literature on optimal factor count.
- Is the weight distribution (36% Quality, 29% Economics, 20% Operational, 15% Strategic) reasonable? Compare against Gartner Magic Quadrant, Forrester TEI, or ISO 25010.
- Is a 1-5 ordinal scale appropriate? What does decision analysis literature say about precision? Could two independent evaluators arrive at the same scores?
- Is the "+/- 5 percentage point" one-at-a-time (OAT) sensitivity analysis a standard technique? Is OAT criticized for missing interaction effects? What are more rigorous alternatives?
- Is a "hard floor" (score of 1 = disqualification unless explicitly accepted) standard in weighted scoring models? Cite ELECTRE concordance/discordance or similar.

### 4.2 ISO 25010 Alignment

- Does the methodology actually align with ISO 25010, or merely mention it? Map each evaluation factor to its corresponding ISO 25010 quality characteristic.
- Is ISO 25010 appropriate for AI platform evaluation, or is it designed for software product quality?

### 4.3 Evidence Hierarchy

- The methodology defines four evidence types: run data, vendor documentation, POC results, reasoned analysis. Is this hierarchy standard? Compare against GRADE framework, systematic review methodologies, or technology evaluation standards.

---

## Part 5: Evaluation Approach and Decision Sequencing

Claims from evaluation-approach.

### 5.1 Phased Evaluation Principle

- "Test reversible, low-cost options empirically before committing to irreversible, high-cost alternatives." Is this a recognized methodology? Cite: real options theory, lean startup, set-based design, or other decision-making frameworks.
- Are there counterarguments for when investing in the complex option first is justified?

### 5.2 Sunk Cost and Commitment Escalation

- Is the sunk cost trap a documented risk in AI platform adoption specifically? Cite relevant studies.
- Is "commitment escalation" a recognized behavioral economics concept? Cite the academic literature (Staw 1976, etc.).

---

## Part 6: Context and Configuration (DD-01)

### 6.1 Copilot Customization Hierarchy

- Does Copilot support all five mechanisms? Cite official docs for each:
  - `copilot-instructions.md` (global)
  - `.instructions.md` with `applyTo` globs (scoped)
  - `SKILL.md` with progressive disclosure (skills)
  - `.agent.md` with tool restrictions (agent modes)
  - MCP integration
- Are there additional mechanisms not mentioned? (AGENTS.md, hooks, prompt files)
- Which are GA vs preview/experimental?

### 6.2 MCP (Model Context Protocol)

- What is MCP? Who created it? Cite the specification.
- Does Copilot natively support MCP? Since when? Cite announcement/documentation.
- Are there production-grade MCP servers for JIRA, Elasticsearch, and GitLab, or would they need custom building?
- Do all five platforms (Copilot, Cursor, Windsurf, Cline, Claude Code) support MCP natively? At what maturity level?

### 6.3 Cross-Platform Standards

- Is AGENTS.md a real standard? Who maintains it? What does it cover? Which platforms support it?
- Is agentskills.io a real site? What is the Agent Skills specification? Who maintains it?
- How much of Copilot's customization is portable via these standards vs proprietary?
- What is the actual migration effort to move from Copilot to Cursor or Windsurf? Has anyone documented this?

### 6.4 Content Taxonomy — "7 of 8 categories fully served"

- Can instruction files effectively encode arc42, C4, MADR templates?
- Does workspace indexing handle YAML files effectively?
- Is workspace retrieval reliable for large repositories with 10+ metadata files?

---

## Part 7: Billing Model Behavioral Claims (DD-02)

### 7.1 Usage Anxiety / Meter Anxiety

- Is there academic research on how billing models affect technology adoption and usage intensity? Cite studies.
- Is "usage anxiety" or "meter anxiety" documented in per-unit billing for enterprise tools? Cite from cloud computing economics, SaaS adoption, or behavioral economics.
- Are there counterexamples where per-token billing led to MORE disciplined (better) usage?

### 7.2 Budget Downgrade Pressure

- Is there research on "model downgrade pressure" in enterprise AI adoption?
- Are there documented cases of organizations switching from frontier to budget models due to cost?
- Is the "rework tax" concept documented anywhere?

---

## Part 8: Model Quality Sensitivity

Claims from model-quality-at-budget.

### 8.1 Architecture Tasks Require Frontier Models

- Is there evidence that architecture tasks (multi-file reasoning, structured document generation, cross-service analysis) require frontier models?
- Are there benchmarks comparing frontier vs mid-tier vs budget models on complex reasoning, multi-file analysis, structured document generation?
- Is "long-context fidelity" (100K+ tokens) a documented differentiator for frontier models? Cite benchmarks.
- Could a mid-tier model (Claude Sonnet, GPT-4o) produce multi-file synthesis, domain rule enforcement, and structured ADRs at comparable quality?

### 8.2 Self-Correcting Risk

- Can an architect reliably detect gradual model quality degradation?
- Is there research on human ability to detect AI output quality changes? ("Boiling frog" effects)
- Are there documented cases of AI service providers quietly downgrading model quality?

### 8.3 Abandonment Risk

- Is there evidence of enterprise AI tool abandonment due to poor model quality?
- Are there published failure rates or adoption decay curves for enterprise AI tools?
- Is the 5-step worst-case (build → budget pressure → poor output → abandonment → sunk cost) a recognized pattern?

---

## Part 9: Build vs Leverage — RAG Comparison

### 9.1 The 8-Row RAG Component Table

For each row, verify the "Native Platform Equivalent":
- **Document Ingestion → Workspace Indexing**: Do Copilot, Cursor, Windsurf do automatic incremental indexing? Does Claude Code? Is "zero-config" fair?
- **Vector Store → Built-in Semantic Search**: Quality of native semantic search vs Pinecone/Weaviate?
- **Retrieval → @workspace/@codebase**: Does each platform use these commands? How does quality compare to custom RAG with re-ranking?
- **Context Injection → Instruction Files**: Is "no code required" accurate? Limitations?
- **Behavior Config → Rules/Agents**: Workspace-as-code support per platform?
- **Tool Integration → MCP**: Maturity level per platform?
- **Multi-Agent → Sub-Agents**: Does Cursor support sub-agents? Does Claude Code? The table omits both.
- **Evaluation → Direct Observation**: Is this a weak equivalence? Do platforms offer evaluation tooling?

### 9.2 Infrastructure Tax

- Are there managed RAG services (Amazon Bedrock Knowledge Bases, Azure AI Search + OpenAI) that significantly reduce the infrastructure tax?
- Should the page acknowledge managed RAG-as-a-service as a middle ground?

### 9.3 "AI as Product vs AI as Tool"

- Is this distinction recognized in industry literature? Cite sources.
- Are there counterexamples where custom RAG is justified for internal developer tools?

---

## Part 10: Architecture Is Not Just Coding

### 10.1 Task Decomposition

- Is the claim that all architecture tasks reduce to file operations defensible?
- What architecture tasks require capabilities beyond file ops? (Whiteboard, stakeholder interviews, consensus building, visual modeling)
- Should the page acknowledge these limitations?

### 10.2 Vendor Documentation Claims

- Cline docs use `architecture.md` as example rule file — verify at docs.cline.bot/customization/cline-rules.
- Windsurf Skills examples include `code-review/` bundles — verify in Windsurf documentation. Has this changed post-OpenAI acquisition?

### 10.3 Bespoke vs Native Equivalence

- Is workspace indexing truly equivalent to a custom knowledge base? What are the limitations?
- Is instruction file injection equivalent to prompt orchestration (LangChain)? What capabilities are lost?
- Is "weeks of engineering vs hours of configuration" supportable? Are there estimates or case studies?

### 10.4 External Validation

- Are there published evaluations of AI coding platforms performing architecture work (ADR writing, trade-off analysis, impact assessment)?
- Are there independent benchmarks for non-coding tasks (documentation, architecture analysis, decision records)?

---

## Part 11: Enterprise Governance Comparison

Claims from platform-landscape governance table.

### 11.1 Per-Platform Verification

- **Copilot**: SOC 2 Type II via GitHub/Microsoft? SSO via GitHub Enterprise Cloud? Data residency controls? "No code sent for training" under Enterprise? Under Business? Under Pro+? Audit log integration? Cite trust pages and terms of service.
- **Cursor**: SOC 2 Type II? SSO at Teams/Enterprise? Privacy Mode enforcement? Admin dashboard? Model blocklists? Cite trust/security documentation.
- **Windsurf**: SOC 2 "Not published"? Zero retention? Enterprise-only features? Current status post-acquisition?
- **Claude Code**: SOC 2 via Anthropic? Organization settings? Cite documentation.

### 11.2 Governance Surface Concept

- Is "governance surface" a recognized concept in enterprise architecture? Cite TOGAF, COBIT, or equivalent frameworks.
- Does the "single governance surface" argument (Copilot inherits GitHub governance) hold under scrutiny?
- Would Cursor with SSO integration truly add a "new governance boundary" or could it integrate seamlessly?

---

## Part 12: Procurement and Organizational Fit (DD-03)

### 12.1 Procurement Friction

- Is adding Copilot seats to an existing GitHub Enterprise agreement truly friction-free? What approvals are typically required?
- Do AI tools face additional procurement scrutiny (AI governance committees, data privacy reviews) even when the platform vendor is already approved?
- Is "not a months-long vendor evaluation" accurate for most enterprises?

### 12.2 Portability

- What exactly is portable vs proprietary in Copilot's customization?
- Can `copilot-instructions.md` content be directly reused in Cursor rules, Windsurf rules, or CLAUDE.md?

---

## Part 13: Regulatory and Future Trends

### 13.1 Model Attribution Regulation

- Has any AI coding platform introduced per-request model attribution?
- Is there an industry trend toward model transparency in AI SaaS?
- Are there regulatory pressures (EU AI Act, etc.) that might force model attribution disclosure?

### 13.2 Copilot IDE Support

- Does Copilot support VS Code, JetBrains, Xcode, Neovim, Eclipse, AND Zed? Cite current IDE support page.
