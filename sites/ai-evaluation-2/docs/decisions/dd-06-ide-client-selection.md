<!-- CONFLUENCE-PUBLISH -->
<!-- CONFLUENCE-URL: -->

# DD-06: IDE Client Selection for Custom Model Consumption

| | |
|-----------|-------|
| **Status** | Decided — GitHub Copilot is the recommended client for consuming custom Foundry models |
| **Date** | 2026-04-09 |
| **Scope** | Given that the team is building a custom fine-tuned model in Azure AI Foundry, which IDE client should consume it? |
| **Depends on** | DD-03 (AI Provider), DD-04 (Model Routing), DD-05 (Model Selection Autonomy) |
| **Feeds into** | Option D Hybrid Architecture, Copilot rollout roadmap |

---

## Problem Statement

The organization is investing in a custom fine-tuned model deployed on Azure AI Foundry. This model encodes domain-specific knowledge that general-purpose frontier models lack. The question is: **how do architects interact with this model in their daily workflow?**

The answer is not obvious. Building a custom VS Code extension (the current Option C approach) is one path, but commercial IDE clients have evolved rapidly. Several now support custom model endpoints natively. If a commercial client provides superior orchestration — agent mode, tool calling, workspace indexing, instruction files — then building a bespoke extension duplicates infrastructure that already exists.

This decision evaluates six IDE clients on their ability to consume a custom Foundry model while delivering the orchestration capabilities that architecture work requires.

---

## Candidate Clients

| # | Client | Type | Custom Model Mechanism |
|---|--------|------|----------------------|
| 1 | **GitHub Copilot** | Commercial (Microsoft) | Enterprise BYOK — admin registers Foundry endpoint; model appears in picker |
| 2 | **Cursor** | Commercial (Anysphere) | API key configuration for custom OpenAI-compatible endpoints |
| 3 | **Windsurf** | Commercial (Codeium) | Custom model API configuration |
| 4 | **Cline** | Open source (VS Code extension) | Any OpenAI-compatible endpoint via settings |
| 5 | **Claude Code** | Commercial (Anthropic) | Anthropic models only — no custom endpoint support |
| 6 | **Custom VS Code Extension** | Self-built (Option C) | Direct API calls to Foundry endpoint from extension code |

---

## Evaluation Matrix

### Dimension 1: BYOK / Custom Model Support

How does each client connect to a custom model deployed on Azure AI Foundry?

| Client | Mechanism | Enterprise Admin Control | Effort to Configure |
|--------|-----------|------------------------|-------------------|
| **Copilot** | Enterprise BYOK — admin adds API key + deployment URL in AI Controls panel. Model appears in every member's picker automatically. | YES — org-level scoping, admin manages keys centrally | Minutes (admin UI, no code) |
| **Cursor** | User configures OpenAI-compatible endpoint in settings. Each user manages their own API key. | NO — per-user configuration, no central management | Minutes per user (settings file) |
| **Windsurf** | User configures custom API provider in settings. Similar to Cursor's approach. | NO — per-user configuration | Minutes per user |
| **Cline** | User configures any OpenAI-compatible endpoint in extension settings. Very flexible. | NO — per-user configuration | Minutes per user |
| **Claude Code** | No custom model support. Anthropic models only. | N/A | N/A — not possible |
| **Custom Extension** | Direct API integration in extension code. Team manages API keys, auth, retry logic, and endpoint URLs. | YES — but requires custom development | Weeks to months (engineering) |

!!! warning "The Key Differentiator"
    Only Copilot and the Custom Extension offer enterprise-administered model registration. But Copilot does it through a UI in minutes; the Custom Extension requires engineering it from scratch.

### Dimension 2: Agent Mode / Tool Calling

Can the client execute multi-step autonomous workflows — reading files, running commands, making edits — using the custom model as the reasoning engine?

| Client | Agent Mode | Tool Calling with Custom Model | Quality of Tooling |
|--------|-----------|-------------------------------|-------------------|
| **Copilot** | YES — full agent mode with 7+ built-in tools (file read/write, terminal, search, sub-agents, memory, MCP) | Expected YES — agent mode sends tool-calling requests to whichever model is selected in the picker | Production-grade, integrated into VS Code |
| **Cursor** | YES — Composer mode with multi-file editing, terminal, codebase search | YES — custom models receive tool calls | Strong, but Cursor is a forked IDE (not native VS Code) |
| **Windsurf** | YES — Cascade mode with autonomous multi-step execution | YES — custom models can drive Cascade flows | Capable, but smaller ecosystem |
| **Cline** | YES — autonomous mode with file edits, terminal, browser interaction | YES — any configured model receives tool calls | Good for individuals; lacks enterprise features |
| **Claude Code** | YES — powerful terminal-based agent | NO — Claude models only, no custom models | Excellent quality, but locked to Anthropic |
| **Custom Extension** | Must be built from scratch — tool calling, file operations, terminal integration, context management | YES — but every tool must be engineered | Quality depends entirely on engineering investment |

### Dimension 3: Workspace Indexing and Context Injection

How does the client understand the workspace and inject relevant context into prompts?

| Client | Workspace Indexing | Context Injection Mechanism | Custom Model Gets Full Context? |
|--------|-------------------|---------------------------|-------------------------------|
| **Copilot** | YES — semantic index of workspace files, automatic context assembly | Client-side retrieval injects context before sending to any model | YES — the model receives assembled context regardless of provider |
| **Cursor** | YES — full codebase indexing, @codebase queries | Client-side indexing with context injection | YES |
| **Windsurf** | YES — workspace indexing with Cascade context | Client-side context assembly | YES |
| **Cline** | LIMITED — file reads on demand, no persistent index | Reads files as tool calls during conversation | Partial — context builds incrementally via tool calls |
| **Claude Code** | YES — workspace indexing via CLAUDE.md and file reads | Combines explicit context files with tool-based reads | YES |
| **Custom Extension** | Must be built — embedding pipeline, vector store, retrieval ranking | Custom RAG implementation required | Depends on implementation quality |

### Dimension 4: Instruction File Support (Declarative Customization)

Can the client load domain-specific behavioral rules from version-controlled Markdown files?

| Client | Instruction Files | Mechanism | Composability |
|--------|------------------|-----------|---------------|
| **Copilot** | YES — `copilot-instructions.md`, `.github/instructions/*.md`, custom agents, skills | Declarative Markdown with `applyTo` glob patterns, automatic activation | Full composability — global + per-file-type + per-agent |
| **Cursor** | YES — `.cursorrules` file | Single rules file per workspace | Limited — one file, no glob-based activation |
| **Windsurf** | YES — `.windsurfrules` file | Single rules file per workspace | Limited — one file |
| **Cline** | YES — `.clinerules` file and custom instructions in settings | Single rules file + UI-configured instructions | Moderate |
| **Claude Code** | YES — `CLAUDE.md` files (workspace root and subdirectories) | Hierarchical Markdown files, auto-loaded per directory | Good — directory-scoped stacking |
| **Custom Extension** | Must be built — parse instruction files, inject into prompts | Custom implementation required | Depends on implementation |

!!! note "Why This Matters for Architecture"
    The NovaTrek pilot uses 500+ lines of `copilot-instructions.md` covering domain models, service boundaries, data ownership rules, mock tool commands, and solution design workflows. PLUS per-file instruction files, custom agents, and skills. This level of declarative customization is a proven force multiplier for architecture work. Clients that support only a single rules file cannot replicate this approach.

### Dimension 5: Client-Side Thinking / Reasoning Display

Does the client expose the model's reasoning process to the architect?

| Client | Thinking Display | With Custom Model |
|--------|-----------------|-------------------|
| **Copilot** | YES — thinking blocks shown in chat (when model supports extended thinking) | Expected YES — if the custom model returns thinking tokens, Copilot renders them |
| **Cursor** | YES — thinking mode available | YES — works with custom models that support it |
| **Windsurf** | LIMITED — some reasoning display | Varies |
| **Cline** | YES — shows raw model output including thinking | YES — raw output displayed |
| **Claude Code** | YES — extended thinking blocks | NO — Claude models only |
| **Custom Extension** | Must be built — UI for displaying reasoning chains | Depends on implementation |

### Dimension 6: MCP (Model Context Protocol) Support

Can the client connect to external tools via the open MCP standard?

| Client | MCP Support | Maturity |
|--------|-------------|----------|
| **Copilot** | YES — configure MCP servers in VS Code settings or `.vscode/mcp.json` | Production — growing ecosystem of MCP servers |
| **Cursor** | YES — MCP server configuration | Production |
| **Windsurf** | YES — MCP support added | Maturing |
| **Cline** | YES — strong MCP support, early adopter | Production — Cline was one of the first MCP adopters |
| **Claude Code** | YES — MCP support | Production |
| **Custom Extension** | Must be built — MCP client integration | Engineering effort required |

### Dimension 7: Enterprise Governance (SSO, Audit, Compliance)

Does the client meet enterprise requirements for security, audit trails, and compliance?

| Client | SSO / Identity | Audit Trail | Content Exclusion | IP Indemnity | Data Residency |
|--------|---------------|-------------|-------------------|-------------|----------------|
| **Copilot** | YES — GitHub Enterprise Cloud SSO, SAML/OIDC | YES — audit log API, usage dashboard | YES — content exclusion policies in admin | YES — for built-in models | YES — EU data residency option |
| **Cursor** | LIMITED — team features, no enterprise SSO | LIMITED — usage tracking | NO | NO | NO |
| **Windsurf** | LIMITED — team features | LIMITED | NO | NO | NO |
| **Cline** | NO — open source, no enterprise layer | NO | NO | NO | NO |
| **Claude Code** | YES — Anthropic enterprise agreements | YES — API-level logging | YES — via Anthropic policies | NO | Depends on plan |
| **Custom Extension** | Must be built — integrate with corporate identity | Must be built — logging, monitoring | Must be built | N/A (self-hosted) | YES (Foundry controls this) |

!!! warning "Non-Negotiable for Enterprise"
    SSO integration, audit trails, and content exclusion are non-negotiable for enterprise deployment. Cursor, Windsurf, and Cline fail this dimension outright. Only Copilot and Claude Code (with enterprise plans) meet these requirements natively.

### Dimension 8: Cost Model When Using Custom Model

What does it cost to use the custom Foundry model through each client?

| Client | Client License | Custom Model Cost | Total Cost Model |
|--------|---------------|-------------------|-----------------|
| **Copilot** | $19/user/month (Business) or $39/user/month (Enterprise) | Per-token via Foundry API (paid by enterprise Azure subscription) | Subscription + Foundry tokens. Built-in 0x models (GPT-4o, GPT-4.1) remain free and unlimited. |
| **Cursor** | $20/user/month (Pro) or $40/user/month (Business) | Per-token via Foundry API | Similar subscription. No free 0x model tier — all models consume from request budget. |
| **Windsurf** | $15-$60/user/month (varies by tier) | Per-token via Foundry API | Subscription + Foundry tokens. |
| **Cline** | Free (open source) | Per-token via Foundry API | Foundry tokens only — but enterprise governance costs are hidden (somebody must build SSO, audit, compliance). |
| **Claude Code** | Usage-based or Max plan ($100-200/month) | N/A — cannot use custom models | Cannot use custom Foundry model. |
| **Custom Extension** | Free (self-built) | Per-token via Foundry API | Foundry tokens + engineering cost to build and maintain the extension ($150K-$400K estimated over 18 months). |

---

## Consolidated Comparison

| Dimension | Copilot | Cursor | Windsurf | Cline | Claude Code | Custom Ext. |
|-----------|---------|--------|----------|-------|-------------|-------------|
| Custom model support | STRONG | Good | Good | Good | NONE | STRONG |
| Enterprise model admin | YES | No | No | No | No | Must build |
| Agent mode + tool calling | STRONG | Strong | Strong | Good | Strong | Must build |
| Workspace indexing | STRONG | Strong | Strong | Limited | Strong | Must build |
| Instruction files | STRONG | Limited | Limited | Moderate | Good | Must build |
| Thinking display | YES | Yes | Limited | Yes | Yes | Must build |
| MCP support | YES | Yes | Yes | Yes | Yes | Must build |
| Enterprise governance | STRONG | Weak | Weak | None | Moderate | Must build |
| Free model tier (0x) | YES | No | No | N/A | No | No |

**Legend:** STRONG = best-in-class or superior, Good = capable, Limited = basic or partial, Weak = insufficient for enterprise, None = not available, Must build = engineering effort required.

---

## The Frozen Customization Problem

The eight-dimension comparison above evaluates client capabilities. But there is a ninth dimension that does not fit neatly into a matrix — and it may be the most consequential: **what happens when a customization is wrong, incomplete, or outdated?**

### Hard-Coded vs. Declarative Customization

A custom fine-tuned model embeds domain knowledge into its weights during training. This is powerful — but it is also **frozen at training time**. When the domain changes (new services, renamed fields, updated data ownership rules, revised safety classifications), the model's embedded knowledge is wrong until it is retrained.

| Customization Type | Change Latency | Who Can Change It | Blocked Architect's Recourse |
|-------------------|---------------|-------------------|------------------------------|
| **Fine-tuned model weights** | Weeks to months (data curation → training → validation → deployment) | ML engineering team only | Submit a ticket. Wait. |
| **Declarative instruction files** (copilot-instructions.md, .instructions.md, custom agents) | Minutes (edit a Markdown file, push to Git) | Any architect with repo access | Fix it yourself in the same session. |

This asymmetry matters because architecture knowledge changes constantly. In the NovaTrek pilot alone, the `copilot-instructions.md` file was updated dozens of times — adding new service boundaries, correcting data ownership rules, refining mock tool commands, adjusting solution design workflows. Each update took minutes and was immediately effective. If those customizations had been embedded in model weights, every correction would have required a retraining cycle.

### The Blocked Architect Scenario

Consider the concrete scenario:

1. An architect is working on a solution design for a new ticket
2. The custom model confidently applies a data ownership rule that was correct three months ago but has since changed (e.g., a service boundary was redrawn, a new event schema was introduced)
3. The model produces architecturally incorrect output — wrong service identified as data owner, wrong API contract referenced, wrong event flow described
4. The architect recognizes the error but **cannot fix the underlying cause**

**With Option C (Custom Extension + fine-tuned model):**

The architect has no recourse in that session. The incorrect knowledge is baked into the model. They must:

- Abandon the AI-assisted workflow and do the analysis manually
- Submit a ticket to the ML engineering team describing the knowledge gap
- Wait for the team to curate corrective training data, retrain, validate, and redeploy
- Resume AI-assisted work weeks or months later — if they have not already abandoned the tool

**With Option D (Copilot + declarative customization):**

The architect fixes the instruction file in the same session:

- Opens `copilot-instructions.md` (or creates a targeted `.instructions.md` file)
- Corrects the data ownership rule, adds the new service boundary, updates the event schema reference
- The very next prompt uses the corrected instructions
- Submits the instruction file change as a PR for peer review
- Every architect benefits from the correction after merge

!!! warning "This Is Not a Hypothetical"
    The NovaTrek pilot's `copilot-instructions.md` evolved from ~200 lines to 500+ lines over the course of the evaluation. Every addition was a response to a real gap — the model did not know a convention, violated a boundary, or missed a workflow step. In every case, the architect corrected the instruction file and continued working. If those corrections had required model retraining, the pilot would have stalled repeatedly.

### Model Selection Lock-In Compounds the Problem

The customization problem is amplified when combined with model selection lock-in. If the custom model is the **only** model available to the architect (as in a custom extension that hard-codes its model endpoint), the architect cannot even switch to a general-purpose frontier model as a workaround.

With Copilot's model picker, an architect who encounters a domain knowledge gap in the custom Foundry model can:

1. Switch to Claude Opus 4.6 or GPT-4.1 for that specific task
2. Provide the correct domain context manually via the conversation
3. Complete the work without delay
4. File an instruction file update for the long-term fix

This is the **circuit breaker** that prevents the Help Desk Loop described in DD-05. The architect is never fully blocked because they always have alternative models available in the same picker.

---

## Customization Ownership: Who Grows the Model?

### The Staffing Question

A custom fine-tuned model is not a one-time deliverable. Domain knowledge evolves continuously — new services are added, API contracts change, architectural decisions are made, data ownership boundaries shift, safety classifications are updated. The model must evolve with them or it becomes an increasingly unreliable source of architectural guidance.

This raises an unavoidable question: **who is responsible for the ongoing curation, retraining, validation, and deployment of the custom model?**

| Ownership Model | Staffing Implication | Knowledge Gap Problem |
|----------------|---------------------|---------------------|
| **Dedicated ML team** | Must hire or allocate engineers with fine-tuning expertise, MLOps skills, and model evaluation capabilities | The ML team does not practice architecture. They cannot judge whether training data is correct, whether model output quality is acceptable, or whether a domain rule has changed. They depend entirely on architects to tell them what to train — creating a bottleneck. |
| **Architecture practice (current team)** | Architects maintain the model alongside their architecture work | Architects lack ML engineering skills. Fine-tuning workflows, training data curation, model evaluation, and deployment pipelines are not architecture competencies. |
| **Hybrid (current approach)** | Troy + Gabriel build the model; architects provide domain knowledge | Knowledge transfer is asynchronous and lossy. Architects describe domain rules in tickets; the ML team interprets and encodes them. Misinterpretations are caught only after retraining and testing. |

None of these models are self-sustaining. Each creates a dependency chain where the people who understand the domain (architects) are separated from the mechanism that encodes it (model weights).

### The Declarative Customization Alternative

Instruction files eliminate this organizational problem entirely.

| Aspect | Fine-Tuned Model | Instruction Files |
|--------|------------------|-------------------|
| **Who writes customizations?** | ML engineers (interpreting architect requirements) | Architects directly |
| **Review process** | Informal — architects may never see training data | Git PR — peer-reviewed Markdown, same as any architecture artifact |
| **Change velocity** | Weeks (retrain cycle) | Minutes (push to Git) |
| **Domain accuracy** | Filtered through ML team interpretation | First-hand — the architect who knows the rule writes the rule |
| **Experimentation** | Expensive — each experiment requires a training run | Free — edit a file, test in the next prompt, revert if wrong |
| **Institutional knowledge capture** | Opaque — embedded in model weights, not human-readable | Transparent — instruction files are documentation that happens to also configure AI behavior |
| **Onboarding new architects** | New architect gets model output with no visibility into why | New architect reads the instruction files and understands the practice's conventions immediately |

### The Contribution Model That Scales

With declarative customization, growing the AI practice's domain knowledge follows the same workflow architects already use for every other artifact:

1. **Architect encounters a gap** — the model does not know a convention, misapplies a rule, or lacks context about a service
2. **Architect writes the fix** — edits `copilot-instructions.md` or creates a targeted `.instructions.md` file
3. **Architect submits a PR** — the customization change is peer-reviewed by other architects, just like an ADR or solution design
4. **PR is merged** — every architect in the practice benefits immediately
5. **The instruction file history is the changelog** — Git log shows exactly when each customization was added, by whom, and why

This is **architecture practice knowledge management** — the instruction files are a living, version-controlled, peer-reviewed codification of how the practice works. They grow organically as architects encounter new scenarios, and they never go stale because the people who use them are the people who maintain them.

### The Decay Risk for Custom Models

Without a sustainable ownership model, a custom fine-tuned model follows a predictable decay curve:

1. **Months 1-3:** Model is current, output quality is high, enthusiasm is strong
2. **Months 4-6:** Domain knowledge starts drifting — new services added, API contracts updated, architectural decisions made that the model does not reflect. Architects notice increasing inaccuracies.
3. **Months 7-12:** Retraining happens (if budgeted), but the training data curation process is slow and the ML team is context-switching between projects. The retrained model fixes some gaps but introduces new ones because the training data was curated by someone other than the practicing architects.
4. **Month 12+:** Architects no longer trust the custom model's domain knowledge. They either abandon it for general-purpose models (making the investment wasted) or work around it (adding manual corrections that negate the productivity benefit).

Instruction files do not decay this way because **there is no separation between the knowledge maintainer and the knowledge consumer**. The architect who discovers a gap is the architect who fixes it, in the same session, with the same tools.

---

## Decision Outcome

**Selected: GitHub Copilot via BYOK.**

### Why Not the Alternatives?

| Client | Disqualifying Factor |
|--------|---------------------|
| **Cursor** | Forked IDE — not native VS Code. No enterprise SSO/audit. Single `.cursorrules` file cannot replicate the composable instruction file system. Switching the team from VS Code to Cursor introduces adoption risk with no offsetting benefit, since Copilot already provides equivalent agent capabilities natively in VS Code. |
| **Windsurf** | Same governance gap as Cursor — no enterprise SSO, audit, or content exclusion. Single rules file. Smaller ecosystem and less investment certainty than Copilot or Cursor. |
| **Cline** | Open source with no enterprise layer. Individual architects would need to manage their own API keys. No SSO, no audit trail, no content exclusion. Excellent for individual experimentation but unsuitable for enterprise deployment. |
| **Claude Code** | Cannot consume the custom Foundry model at all. Locked to Anthropic models. This alone disqualifies it for the Option D hybrid architecture. Additionally, Claude Code is terminal-based — not the IDE-integrated experience architects prefer. |
| **Custom VS Code Extension** | Every capability that Copilot delivers out of the box — agent mode, tool calling, workspace indexing, instruction files, MCP, enterprise governance — must be engineered, tested, maintained, and updated. This is a multi-month, multi-engineer effort that duplicates existing infrastructure. The extension then falls behind as Copilot adds features (sub-agents, memory, new tool integrations) that the custom extension must re-implement or forgo. |

### Why Copilot Wins

1. **Only client with enterprise-administered BYOK.** The admin registers the Foundry endpoint once; every architect sees the model in their picker. No per-user API key management, no configuration drift.

2. **Full orchestration platform, not just a chat window.** Agent mode with 7+ built-in tools, sub-agents, persistent memory, MCP connections — all of which work with the BYOK model because context injection is client-side.

3. **Composable declarative customization.** The 500+ line `copilot-instructions.md`, per-file instruction files, custom agents, and skills that power the NovaTrek pilot are not replicable in clients with single-rules-file support.

4. **Free frontier models for routine work.** The 0x multiplier models (GPT-4o, GPT-4.1, GPT-5 mini, Raptor mini) provide unlimited free usage for routine tasks. No other client offers this — Cursor, Windsurf, and Cline all consume from a request budget or per-token billing for every model.

5. **Enterprise governance built in.** SSO, audit logs, content exclusion, IP indemnity, data residency — these are table-stakes requirements that Copilot meets natively. Cursor, Windsurf, and Cline do not.

6. **Zero engineering cost for client capabilities.** The Custom Extension approach spends engineering budget rebuilding what Copilot already provides. Option D redirects that budget to model quality — where the custom Foundry model adds genuine value.

### Consequences

**Positive:**

- Architects use a single, familiar tool (VS Code + Copilot) for both frontier and custom models
- No engineering investment in client-side infrastructure; budget redirected to model fine-tuning
- Enterprise governance requirements met without custom development
- Free 0x models subsidize the cost of the overall AI practice

**Negative:**

- Dependency on GitHub/Microsoft for BYOK feature stability (currently public preview)
- No visibility into Copilot's internal orchestration routing (see DD-04 transparency caveat)
- If GitHub deprecates or restricts BYOK, the Foundry model integration path narrows

**Neutral:**

- Cursor, Windsurf, and Cline remain valid for individual experimentation — this decision applies to the enterprise-recommended client for architecture practice deployment

---

## Related Pages

- [Option D — Hybrid Architecture](../evidence/option-d-hybrid-architecture.md) — full BYOK architecture and risk assessment
- [DD-04: Model Routing](dd-04-model-routing.md) — how models are selected and routed
- [DD-05: Model Selection Autonomy](dd-05-model-selection-autonomy.md) — why architects control model choice
- [DD-03: AI Provider](dd-03-ai-provider.md) — the upstream provider decision
