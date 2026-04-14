<!-- CONFLUENCE-PUBLISH -->
<!-- CONFLUENCE-URL: https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2614526429/DD-05+Architect+Model+Selection+Autonomy -->

# DD-05: Architect Model Selection Autonomy

| | |
|-----------|-------|
| **Status** | Decided — guided freedom; architect selects from platform-provided model set |
| **Date** | 2026-04-07 |
| **Scope** | Should architects control which AI model is used for their tasks, or should model selection be locked down by a central team? |
| **Depends on** | DD-03 (AI Provider), DD-04 (Model Routing) |
| **Feeds into** | DD-06 (IDE Client Selection), Governance roadmap, adoption strategy |

---

## Problem Statement

When rolling out an AI-assisted architecture practice, organizations must decide how much control the architect has over model selection. This decision has significant implications for output quality, cost management, troubleshooting workflows, and practice adoption.

The tension is real: giving architects unrestricted model access risks cost overruns and inconsistent outputs, while locking model selection behind a central team creates friction, delays, and learned helplessness.

## Three Governance Models

### Option 1: Full Lock-Down (Central Team Controls Model Selection)

A platform team or AI governance committee pre-selects the model. Architects cannot change it.

**Purported benefits:**

- Consistent output quality across all architects
- Predictable cost envelope — no surprise overages
- Central oversight of model usage patterns

**Why this fails for architecture work:**

| Failure Mode | Impact |
|-------------|--------|
| **Model behavior issues become ticket queue problems** | Architect encounters a hallucination, context loss, or domain rule violation. Cannot switch models to work around it. Must file a ticket to a platform team that cannot reproduce the issue because they lack architecture domain context. Resolution time: days to weeks. |
| **The platform team cannot evaluate architecture output quality** | A support ticket reading "the ADR reasoning was shallow" is meaningless to a team that does not practice solution architecture. The architect is the only person who can judge output quality for their task. |
| **Learned helplessness kills adoption** | After two or three experiences where a model behavior issue blocks their work and the ticket queue offers no timely resolution, architects stop using the AI tool entirely. This is the single most common cause of enterprise AI tool abandonment. |
| **One model does not fit all tasks** | A frontier model (Claude Opus 4.6, 3x multiplier) is necessary for complex multi-service impact analysis. It is wasteful for routine tasks like reformatting tables or generating boilerplate. Lock-down forces the organization to either overpay or underperform. |
| **New model releases require change management** | When a better model becomes available, deploying it to the locked-down environment requires a change request, testing cycle, and rollout — adding weeks of latency to capability improvements that should be immediate. |

!!! warning "Anti-Pattern: The Help Desk Loop"
    Architect hits a model behavior issue → files ticket to platform team → platform team cannot reproduce (lacks architecture workspace context) → ticket bounces back asking for more details → architect spends more time documenting the issue than the original task would have taken → architect abandons the AI tool and returns to manual work. This pattern is well-documented in enterprise tool standardization failures.

### Option 2: Guided Freedom (Architect Selects from Platform-Provided Models)

The platform offers a curated set of models. Architects choose the appropriate model for each session or task based on complexity and cost awareness.

**How this works in practice with Copilot (Option A):**

| Task Type | Recommended Model | Multiplier | Cost Per Prompt |
|-----------|------------------|------------|-----------------|
| Routine tasks (formatting, boilerplate, simple queries) | GPT-4o / GPT-4.1 | 0x | $0 (unlimited) |
| Architecture analysis, solution design, ADR generation | Claude Opus 4.6 | 3x | $0.12 |
| Quick exploration, brainstorming | GPT-4.1 | 0x | $0 (unlimited) |
| Domain-specialized analysis (custom enterprise model) | Custom Foundry Model (BYOK) | Per-token (enterprise rate) | Azure consumption-based |

!!! note "Option D — Hybrid Architecture"
    The guided freedom model extends naturally to BYOK (Bring Your Own Key) models. GitHub Copilot allows organizations to register custom Azure AI Foundry endpoints alongside the built-in model set. This means an architect can switch between a free 0x model for routine work, a frontier model (Opus) for complex design, and a domain-specialized Foundry model for enterprise-specific analysis — all within the same IDE session, with no infrastructure changes. See [Option D — Hybrid Architecture](../evidence/option-d-hybrid-architecture.md) for the full BYOK analysis.

**Why this works:**

- **Architect matches model to task** — no overpaying for routine work, no underpowering for complex analysis
- **Self-correcting quality feedback** — if a model produces poor output, the architect switches immediately instead of filing a ticket
- **Cost awareness without anxiety** — architects understand the multiplier system and self-regulate. The 0x models provide an unlimited baseline; frontier models are reserved for high-value tasks
- **Zero ticket queue friction** — behavior issues are resolved in seconds (switch model) not days (wait for platform team)
- **New models are available immediately** — when GitHub adds a new model, architects can try it in their next session

**Guardrails that prevent abuse:**

| Guardrail | Mechanism |
|-----------|-----------|
| Budget caps | GitHub Copilot subscription includes 1,500 premium requests/month. Overages are visible and billable at $0.04/request. Enterprise admins can set spending limits. |
| Usage monitoring | Copilot usage dashboard shows per-user consumption patterns. Outliers are identifiable without restricting the majority. |
| Team norms | Architecture practice establishes guidelines (not mandates): "Use 0x models for routine tasks, save Opus for design work." Social norms are more effective than technical locks for professional teams. |
| Model availability | GitHub curates the model set — only production-ready, compliance-cleared models appear in the selector. Architects cannot route to arbitrary endpoints. |

### Option 3: Unrestricted Access (Any Model, Any Provider)

Architects can use any model from any provider, including self-provisioned API keys and custom endpoints.

**Why this is unnecessary:**

- The curated model set in Option A already includes frontier models from multiple providers (Anthropic, OpenAI, Google)
- Unrestricted access introduces ungovernable cost exposure and compliance risk
- Self-provisioned API keys bypass enterprise audit trails
- This is the Option B (Roo Code + OpenRouter) model — and the evaluation already demonstrates its cost and governance disadvantages

## Decision Outcome

**Selected: Option 2 — Guided Freedom.**

The architect selects the model per session from the platform's curated set. No central approval is required. Cost guardrails operate at the subscription and spending limit level, not at the model selection level.

### Rationale

1. **Architecture output quality is observable only by the architect.** No platform team can evaluate whether an ADR's reasoning chains are sound or whether a cross-service impact analysis is complete. The architect must have the agency to select the tool configuration that produces acceptable output for each specific task.

2. **The ticket-to-another-team model is incompatible with architecture work cadence.** Architecture sessions are time-sensitive — a solution design blocker cannot wait in a ticket queue. The architect who encounters a model behavior issue needs to resolve it in seconds (switch model), not days (wait for another team).

3. **Guided freedom aligns cost incentives without creating anxiety.** The 0x/3x multiplier system makes the cost trade-off explicit and transparent. Architects self-regulate because they understand the economics — not because a system prevents them from making choices.

4. **Lock-down creates the adoption failure loop.** The most dangerous outcome is not a cost overrun — it is architects abandoning the AI tool because friction exceeds value. Every lock-down mechanism that adds friction to the workflow increases the probability of this outcome.

### Consequences

**Positive:**

- Architects adopt and sustain AI usage because they control their own experience
- Model behavior issues are self-resolved, eliminating an entire category of support tickets
- Cost optimization happens naturally — architects use free models for routine tasks
- New model capabilities are available immediately without change management

**Negative:**

- Individual cost variance — some architects will consume more premium requests than others
- No central enforcement of "always use the cheapest model" — but this is intentional, because the cheapest model produces the worst architecture output

**Neutral:**

- Usage monitoring is still recommended to identify outliers, but as an observability practice, not as an enforcement mechanism

---

## Beyond Model Selection: Declarative Agent Customization

Model selection autonomy — choosing which model runs a task — is the first dimension of architect control. But a second, equally important dimension is emerging: **behavioral customization** — controlling *how* the model works, not just *which* model works.

GitHub Copilot supports declarative agent customization through Markdown files checked into the repository. This is not prompt engineering in the traditional sense (crafting one-off system prompts). It is a **version-controlled, peer-reviewed, composable configuration system** that shapes AI behavior without writing code.

### What Declarative Agent Customization Provides

| Mechanism | File Convention | What It Controls |
|-----------|----------------|-----------------|
| **Custom agents** | `.github/agents/*.md` | Define specialized AI personas with scoped instructions, tool restrictions, and domain knowledge. An architect invokes a specific agent for a specific task type. |
| **Instruction files** | `.github/instructions/*.md` with `applyTo` glob patterns | Inject context rules that activate automatically based on which files the architect is working with. No manual invocation required. |
| **Skills** | `SKILL.md` files | Package domain-specific workflows as reusable capabilities that agents can invoke. A skill defines *how* to perform a multi-step task. |
| **Global instructions** | `.github/copilot-instructions.md` | Establish baseline behavior for every interaction — domain model, data ownership rules, coding standards, safety constraints. |

### Why This Matters for the Autonomy Decision

Declarative agent customization is the **middle ground** between two extremes that stakeholders often debate:

| Extreme | Problem | Middle Ground |
|---------|---------|---------------|
| "Every architect uses the AI differently" | Inconsistent outputs, no shared standards, no institutional knowledge capture | Custom agents encode best practices into versioned, shared configuration. Every architect gets the same starting point. |
| "We need a bespoke agent platform to control AI behavior" | Multi-month engineering, ML infrastructure expertise, ongoing maintenance | Markdown files checked into Git achieve behavioral control with zero infrastructure — the customization files ARE the control mechanism. |

This is **behavioral autonomy via declarative configuration**:

- The organization defines the agents, instructions, and skills (governance)
- The architect selects which agent to use for each task (autonomy)
- Everything is version-controlled in Git (auditability)
- Changes go through pull requests (peer review)
- No infrastructure to provision, no pipelines to maintain (zero operational cost)

### Concrete Example: The Architecture Practice Pilot

The pilot that produced this evaluation uses declarative agent customization extensively:

| Configuration | Purpose | Effect |
|---------------|---------|--------|
| `copilot-instructions.md` (500+ lines) | Domain model, service ownership boundaries, data isolation rules, mock tool commands, solution design workflow | Every AI interaction understands the NovaTrek domain, respects service boundaries, and follows the established workflow — without the architect repeating context |
| `.github/instructions/prompt-me.instructions.md` | Interactive decision-loop workflow | When an architect says "prompt me," the agent presents each issue with lettered options, a recommendation, and waits for a decision before proceeding |
| `.github/agents/Novatrek Solution Architect.md` | Specialized architecture agent | Scoped to architecture work — solution design, ticket triage, API contract review, impact assessments, ADR authoring. Tool restrictions prevent it from performing unrelated tasks |

These files are checked into Git. Every architect who clones the repository gets identical AI behavior customization. Changes are reviewed via pull request. No platform team ticket required.

### The Build-vs-Configure Spectrum

The stakeholder argument for self-managed embeddings often assumes that behavioral customization requires engineering a bespoke platform. Declarative agent customization demonstrates a third path:

| Approach | Effort | Control | Maintenance |
|----------|--------|---------|-------------|
| **No customization** (use platform defaults) | Zero | None | None |
| **Declarative configuration** (instruction files, custom agents, skills) | Hours to days | Behavioral control over domain knowledge, workflows, tool usage, output format | Git-managed Markdown files — same workflow as any other code artifact |
| **Bespoke agent platform** (custom RAG, embedding pipelines, orchestration framework) | Months | Full control over retrieval, ranking, model routing, embedding strategy | ML infrastructure team, vector DB operations, pipeline monitoring |

The middle row — declarative configuration — captures the majority of the behavioral control benefits at a fraction of the cost and complexity. It is the recommended path for scaling the architecture practice.

### Recommendation

Declarative agent customization should be adopted as a core capability alongside model selection autonomy. Specifically:

1. **Pilot phase (current):** The `copilot-instructions.md` and custom agent definitions already in use should be treated as first-class architecture artifacts — reviewed, versioned, and maintained with the same rigor as ADRs and OpenAPI specs.

2. **Team adoption phase:** As additional architects join the practice, shared agent definitions become the primary mechanism for ensuring consistent AI behavior across the team. New architects receive the same behavioral customization by cloning the repository — no onboarding configuration required.

3. **Scaled adoption phase:** Teams develop domain-specific agents and skills for their service domains. An instruction file governance process (code review for `.instructions.md` and agent definitions) ensures quality without central bottleneck.

This is not a future aspiration — it is a working capability demonstrated in the pilot. The 4 solution designs, 14 ADRs, and 139 diagrams produced during the evaluation were all generated under declarative behavioral configuration that any architect on the team can inherit, modify, and extend through standard Git workflows.

---

## Governance Roadmap

As the architecture AI practice scales from pilot to team-wide adoption, governance decisions should be resolved in sequence — each triggered by an observable need, not a speculative concern:

| Phase | Governance Decision | Trigger | Resolution Approach |
|-------|--------------------|---------|---------------------|
| **Pilot (current)** | Model selection autonomy (this decision) | Initial rollout | Guided freedom — architect selects per session |
| **Pilot (current)** | Declarative agent customization | Demonstrated in pilot | Custom agents, instruction files, and skills checked into Git — behavioral control with zero infrastructure |
| **Team adoption** | Cost monitoring and alerting | Monthly spend exceeds expected range | Usage dashboard review; spending limits if needed |
| **Team adoption** | Quality baselines | Multiple architects using the tool | Define minimum output quality expectations; peer review of AI-assisted deliverables |
| **Scaled adoption** | Model standardization for shared workflows | Team needs reproducible outputs across architects | Recommend (not mandate) specific models for specific workflow types |
| **Scaled adoption** | Instruction file governance | Multiple teams contributing to shared instruction files | Code review process for `.instructions.md` and agent definitions |
| **Scaled adoption** | Domain-specific agents and skills | Teams need task-specific AI behavior for their service domains | Teams develop and maintain their own agents and skills within shared governance framework |
| **Enterprise rollout** | Compliance and audit | Regulatory or security requirement | Enterprise Copilot tier with data residency, SSO, audit logs |

!!! note "Governance Principle"
    Add governance in response to observed problems, not in anticipation of hypothetical ones. Every governance mechanism that adds friction before demonstrating value reduces adoption — and an unused AI tool provides zero value regardless of how well-governed it is.

---

**See also:**

- [DD-04: Model Routing](dd-04-model-routing.md) — How model routing works mechanically (complements this governance-level decision)
- [DD-06: IDE Client Selection](dd-06-ide-client-selection.md) — Which IDE client consumes the custom Foundry model and how customization is distributed
- [DD-02: Billing Model](dd-02-billing-model.md) — Why intent-based billing eliminates meter anxiety that would otherwise complicate model selection
- [Scoring Results](../framework/scoring-results.md) — EF-07 (Multi-Model Flexibility) scores each option on model selection capabilities
- [Model Quality at Budget](../evidence/model-quality-at-budget.md) — Why restricting architects to budget models degrades output quality
