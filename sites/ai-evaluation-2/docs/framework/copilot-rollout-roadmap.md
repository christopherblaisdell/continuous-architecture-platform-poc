<!-- CONFLUENCE-PUBLISH -->

# GitHub Copilot Rollout Roadmap

## Purpose

This roadmap defines the practical steps to roll out GitHub Copilot as the AI-assisted architecture tool for the Solution Architecture practice. It covers three workstreams:

1. **Licensing and access** — getting Copilot seats provisioned and configured
2. **Content preparation** — organizing architecture content so Copilot can index it effectively
3. **Context injection** — configuring instructions, skills, and agent definitions so Copilot understands the architecture domain

The roadmap is sequenced by dependency and value: each phase delivers usable capability before the next phase begins.

---

## Phase 0: Pilot (COMPLETE)

**Status:** Done. This is where we are today.

| Deliverable | Status |
|-------------|--------|
| Single-architect Copilot Pro+ seat | Active |
| 1,172-line `copilot-instructions.md` with full NovaTrek domain model | Complete |
| Custom agent definition (`Novatrek Solution Architect`) | Complete |
| 5 prompt workflows (investigation, deep-research, architecture-review, security-review, solution-verification) | Complete |
| 5 scoped instruction files (GitHub URLs, prompt-me workflow, architecture security, specs, solutions) | Complete |
| 22 OpenAPI service specs indexed in workspace | Complete |
| 14 ADRs, 6 solution designs, 37 PlantUML diagrams, 8 AsyncAPI event specs | Complete |
| 15 metadata YAML files (capabilities, tickets, domains, cross-service calls, events, data stores) | Complete |
| 18 Excalidraw wireframes across 3 applications | Complete |
| Live architecture portal (MkDocs Material on Azure Static Web Apps) | Complete |
| Confluence publishing pipeline (automated mirror) | Complete |
| MCP server stub configured (Vikunja integration, not yet active) | Configured |

**Result:** 4 complete solution designs, 14 ADRs, and 139 generated sequence diagrams produced using this setup. The pilot validated that Copilot with declarative customization handles enterprise architecture work effectively.

---

## Phase 1: Licensing and Team Access

**Goal:** Get Copilot seats provisioned for the architecture team.

**Timeline:** Can start immediately; procurement timeline depends on existing GitHub Enterprise agreement.

### 1.1 Determine Licensing Path

| Path | When to Use | Action |
|------|-------------|--------|
| **Extend existing GitHub Enterprise agreement** | Organization already has GitHub Enterprise Cloud with Copilot Business or Enterprise | Request additional Copilot Enterprise seats through existing MSA. Fastest path — no new vendor onboarding. |
| **Add Copilot Business to existing GitHub org** | Organization has GitHub Enterprise but no Copilot add-on | Enable Copilot Business ($19/user/month) or Enterprise ($39/user/month) at org level. Requires GitHub org admin approval. |
| **Individual Copilot Pro+ seats (interim)** | While enterprise licensing is in procurement | Architects use individual Pro+ seats ($39/month each). Full agent mode capability, but no org-level policy controls. |

**Recommendation:** If enterprise licensing takes more than 2 weeks, start with individual Pro+ seats to avoid blocking progress. Transition to enterprise seats when available.

### 1.2 VS Code Configuration

Each architect needs:

| Component | Action | Time |
|-----------|--------|------|
| VS Code | Install or update to latest stable | 5 min |
| GitHub Copilot extension | Install from VS Code marketplace | 2 min |
| GitHub Copilot Chat extension | Install from VS Code marketplace | 2 min |
| Sign in to GitHub | Authenticate with organizational or personal GitHub account | 2 min |
| Clone architecture repository | `git clone` the workspace repository | 5 min |
| Verify Copilot is active | Open a file, confirm Copilot icon in status bar, test with a chat prompt | 2 min |

**Total setup time per architect: ~20 minutes.** No infrastructure provisioning, no API keys, no gateway configuration.

### 1.3 Verify Workspace Indexing

After cloning, Copilot automatically indexes all workspace files. Verify by asking in Copilot Chat:

- "What services does NovaTrek have?" (should list services from specs)
- "What does ADR-005 say?" (should return Pattern 3 safety default)
- "Show me the OpenAPI spec for svc-check-in" (should find and reference the spec file)

If Copilot returns accurate answers, indexing is working. No configuration needed.

---

## Phase 2: Content Preparation

**Goal:** Identify every category of data an architecture practice needs for AI-assisted work, determine where it lives today, decide whether it belongs in git or requires a different access mechanism, and execute the moves.

Copilot can only use what it can see. Content in the workspace is indexed automatically. Content outside the workspace requires an integration (MCP server) or an enterprise knowledge layer (Foundry IQ). This section inventories all data categories, classifies their delivery mechanism, and sequences the work.

### 2.1 Data Inventory — Master View

Every data source an architecture practice needs falls into one of four tiers:

| Tier | Delivery Mechanism | When Copilot Sees It | Effort to Enable |
|------|-------------------|---------------------|-----------------|
| **Tier 1** | Already in git | Immediately on clone | None — already done |
| **Tier 2** | Move into git | After copy + commit | Hours (file moves) |
| **Tier 3** | MCP server (live queries) | When MCP server is running | Days to weeks per integration |
| **Tier 4** | Foundry IQ / knowledge base | When index is built + MCP bridge configured | Weeks to months |

The following sections detail what falls into each tier and why.

### 2.2 Tier 1 — Already in Git (No Action Needed)

This content is in the architecture repository today. Copilot indexes it automatically when an architect clones the repo.

| Data Category | Examples | Count | Location |
|--------------|----------|-------|----------|
| API contracts | OpenAPI YAML specs for all 19+ services | 22 | `architecture/specs/` |
| Event schemas | AsyncAPI YAML specs for event-driven integrations | 8 | `architecture/events/` |
| Architecture decisions | MADR-formatted ADRs (ADR-001 through ADR-014) | 14 | `decisions/` |
| Solution designs | Complete solution packages (requirements, analysis, impacts, guidance, user stories) | 6 | `architecture/solutions/` |
| Service metadata | Domain classifications, data stores, cross-service calls, actors, capabilities, tickets | 15 | `architecture/metadata/` |
| Architecture diagrams | C4 container/component diagrams, sequence diagrams, event flows | 37 | `architecture/diagrams/` |
| UI wireframes | Excalidraw designs for guest portal, ops dashboard, mobile app | 18 | `architecture/wireframes/` |
| Copilot customizations | Instructions, agent definitions, prompt workflows, scoped rules | 9 | `.github/` |
| Portal source | MkDocs pages, generators, deployment configs | ~50 | `portal/` |
| Configuration schemas | Adventure classification rules, test standards | 2 | `config/` |

**Total: ~180 files providing architecture context on clone.**

### 2.3 Tier 2 — Move into Git

This content exists but is not in the right location for Copilot to index it, or it exists outside the repository and should be brought in.

| Data Category | What It Contains | Where It Lives Today | Where It Should Go | Priority | Rationale |
|--------------|-----------------|---------------------|-------------------|----------|-----------|
| Architecture standards | MADR template, C4 model guide, arc42 template structure, ISO 25010 quality tree, quality model reference | `phases/phase-1-ai-tool-cost-comparison/workspace/architecture-standards/` (58 files) | `architecture-standards/` at workspace root | HIGH | `copilot-instructions.md` references these templates by path. Copilot currently cannot find them because they are buried in the Phase 1 evaluation workspace. |
| Source code examples | Representative Java service implementations showing patterns (controller/service/repository, entity models, event handlers) | Not present — `copilot-instructions.md` references `source-code/` analysis patterns | `source-code/` with 2-3 representative services, OR remove source code analysis section from instructions | MEDIUM | Instructions teach Copilot how to analyze Java code, but there is no code to analyze. Either provide examples or remove the dead reference. |
| Team runbooks | How to run generators, deploy the portal, execute mock tools, perform architecture reviews | Scattered across README files and copilot-instructions.md | `docs/runbooks/` or consolidate into a single operations guide | MEDIUM | An architect joining the team needs a single place to learn operational procedures, and Copilot needs this to answer "how do I..." questions. |
| Reference architectures | Canonical patterns the team has adopted (saga, CQRS, event sourcing, API gateway) with rationale | Implicit in ADRs and solution designs — no standalone reference | `architecture/patterns/` as short pattern cards (1 page each) | LOW | Gives Copilot explicit pattern vocabulary to draw from when recommending designs. Currently it infers patterns from ADRs, which works but is indirect. |
| Environment topology | Which services run where, what databases back them, network topology between environments | Partially in `architecture/metadata/data-stores.yaml` | Expand metadata YAML or add `architecture/metadata/environments.yaml` | LOW | Useful for impact assessments that need to reference deployment boundaries, but not blocking current work. |

### 2.4 Tier 3 — Access via MCP Server (Live Queries)

This data lives in corporate systems that change in real time. It should NOT be copied into git — it would go stale immediately. Instead, an MCP server provides live query access when Copilot needs it.

The pilot demonstrated this pattern using local mock scripts (`mock-jira-client.py`, `mock-elastic-searcher.py`, `mock-gitlab-client.py`) that simulate what MCP servers would do in production.

| Data Category | Corporate System | What the Architect Needs | MCP Server Approach | Priority |
|--------------|-----------------|-------------------------|---------------------|----------|
| Work items and tickets | JIRA or Azure DevOps | Ticket details, status, comments, linked issues — to understand requirements before designing | MCP server calling JIRA/ADO REST API with read-only access. Query by ticket ID, filter by status/component/label. | HIGH — this is the most frequent external data need during architecture work |
| Production logs and metrics | Elasticsearch, Datadog, or Application Insights | Error logs, latency metrics, traffic patterns — to ground architecture analysis in production evidence | MCP server querying observability APIs. Filter by service, severity, time range, keyword. | HIGH — essential for investigation scenarios |
| Source control activity | GitHub or GitLab | Recent PRs/MRs, code diffs, branch status — to understand what changed and when | MCP server calling GitHub/GitLab API. List PRs by repo, get diff for specific PR, search commits. | MEDIUM — useful during investigations but architects can also browse the UI |
| CI/CD pipeline status | GitHub Actions, Azure DevOps Pipelines, or Jenkins | Build results, test failures, deployment history — to assess whether a service is stable before proposing changes | MCP server querying pipeline APIs. Get latest build status, test results for a service. | MEDIUM — valuable but not blocking architecture decisions |
| Service registry / CMDB | ServiceNow, Backstage, or internal CMDB | Service ownership, SLA targets, deployment tier, dependency graph — to validate service metadata is current | MCP server querying CMDB API. Lookup service by name, get owner/tier/dependencies. | LOW — metadata YAML in git covers this for now; MCP adds live validation |
| Incident history | PagerDuty, ServiceNow, or Opsgenie | Past incidents, root cause analysis, affected services — to identify recurring architectural weaknesses | MCP server querying incident management API. Search by service, severity, date range. | LOW — useful for pattern detection but not a daily need |

**Key principle:** Each MCP server is a thin adapter — it translates Copilot's tool calls into the corporate system's API. The architecture team does not need to build indexing infrastructure. MCP servers are additive: each one extends Copilot's reach without changing anything about the workspace, instructions, or agent definitions.

### 2.5 Tier 4 — Access via Foundry IQ or Enterprise Knowledge Base

This data is large, unstructured, and owned by other teams. It cannot be moved into git (too large, wrong ownership) and is not well-suited to real-time MCP queries (requires full-text search over large corpora, not point lookups).

This is the retrieval workload that enterprise knowledge layers like Foundry IQ are designed for. See [Foundry IQ Comparison](../evidence/foundry-iq-comparison.md) for detailed analysis.

| Data Category | Where It Lives | Why It Cannot Be in Git or MCP | How Foundry IQ / Knowledge Base Addresses It |
|--------------|---------------|-------------------------------|---------------------------------------------|
| Cross-team documentation | SharePoint, Confluence, Google Docs | Owned by other teams, updated independently, too large to clone. An MCP point-lookup requires knowing which document to fetch — but the architect often does not know what exists. | Foundry IQ indexes SharePoint/Confluence sites and enables semantic search. Copilot asks "what has the payments team documented about PCI compliance?" and gets relevant passages. |
| Compliance and regulatory frameworks | SharePoint, internal wiki, or document management system | Large corpus, controlled distribution, subject to legal review. Not appropriate for a git repository accessible to all developers. | Foundry IQ can index approved compliance documents with access controls preserved. Architects search for applicable regulations during security reviews. |
| Vendor reference documentation | Vendor portals, licensed PDF/HTML documentation | Licensing restrictions prevent redistribution. Content updates on vendor's schedule. | Foundry IQ can index vendor docs (where licensing permits) to answer "what does the Azure Service Bus SLA guarantee?" without the architect browsing vendor portals. |
| Enterprise reference architectures from other teams | Other teams' git repos, architecture wikis, Confluence spaces | Different ownership, different change cadence. Copying creates stale forks. | Foundry IQ provides cross-repo semantic search. An architect designing an event-driven integration can find how other teams solved similar problems. |
| Historical decision records from other domains | Confluence, SharePoint, email threads, meeting recordings | Scattered across systems, often not in structured format. | Foundry IQ indexes unstructured content and surfaces relevant prior decisions during new design work. |
| Onboarding and training materials | LMS, SharePoint, internal wiki | Owned by HR/L&D, updated on their schedule. | Foundry IQ makes institutional knowledge searchable. New architects can ask Copilot questions that draw from training materials they have not read yet. |

**Key principle:** Foundry IQ solves the "I don't know what I don't know" problem. Git and MCP work when the architect knows what to look for. Foundry IQ works when the architect needs to discover relevant content across a broad corpus.

**Bridge to Copilot:** Foundry IQ does not natively integrate with VS Code / Copilot today. An MCP server calling the Foundry IQ retrieval API would bridge the gap — the architect's tool call flows through MCP to Foundry IQ's search index and returns relevant passages as context. See the [MCP Bridge Analysis](../evidence/foundry-iq-comparison.md#can-mcp-bridge-the-gap) for feasibility assessment.

### 2.6 Decision Framework: Git vs. MCP vs. Foundry IQ

When new data sources are identified, use this framework to classify them:

| Question | If Yes → | If No → |
|----------|----------|---------|
| Does the architecture team own this content? | Consider git | Move to next question |
| Is the content small enough for git (< 100 MB, < 1,000 files)? | Git | Move to next question |
| Does the content change with architecture decisions (not independently)? | Git | Move to next question |
| Is the content in a system with a REST API? | MCP server | Move to next question |
| Does the architect know exactly what to query (point lookup)? | MCP server | Move to next question |
| Is the content a large unstructured corpus requiring semantic search? | Foundry IQ | Evaluate case-by-case |

**Rules of thumb:**

- **If you wrote it, git it.** Architecture artifacts, standards, templates, decisions — these belong in the repository.
- **If you query it, MCP it.** Live systems (tickets, logs, pipelines) that change in real time need an API adapter, not a static copy.
- **If you search it, index it.** Large knowledge bases where the architect does not know which specific document to fetch need an indexing layer.
- **When in doubt, start with git.** Moving a document into the repository is the simplest possible action. Only reach for MCP or Foundry IQ when git genuinely cannot serve the need.

---

## Phase 3: Context Injection via Customizations

**Goal:** Configure Copilot so it understands the architecture domain, follows team conventions, and produces consistent output — without each architect manually explaining the context every session.

### 3.1 What's Already Configured

The pilot produced a complete customization layer. New architects inherit all of this by cloning the repository:

| Customization | File | What It Does |
|---------------|------|-------------|
| **Global instructions** | `.github/copilot-instructions.md` (1,172 lines) | Domain model, service ownership, data isolation rules, solution design workflow, architecture standards, document formatting, mock tool commands, portal generation |
| **Solution Architect agent** | `.github/agents/novatrek-solution-architect.agent.md` | Specialized persona scoped to architecture work — triage, design, review, ADR authoring. Tool restrictions prevent non-architecture tasks |
| **Investigation prompt** | `.github/prompts/investigation.prompt.md` | Structured workflow: JIRA context, Elastic logs, GitLab MRs, architecture analysis |
| **Deep research prompt** | `.github/prompts/deep-research.prompt.md` | Multi-source evidence synthesis with cross-referencing |
| **Architecture review prompt** | `.github/prompts/architecture-review.prompt.md` | Anti-pattern detection, ISO 25010 quality assessment |
| **Security review prompt** | `.github/prompts/security-review.prompt.md` | OWASP Top 10 + NovaTrek-specific safety rules |
| **Solution verification prompt** | `.github/prompts/solution-verification.prompt.md` | 8-gate quality check before merge |
| **GitHub URL rules** | `.github/instructions/github-urls.instructions.md` | Prevents malformed GitHub links (applies to all files) |
| **Prompt-me workflow** | `.github/instructions/prompt-me.instructions.md` | Interactive decision loop — step through plans one item at a time |
| **Architecture security** | `architecture/.instructions.md` | Data ownership, identity resolution, safety defaults (scoped to architecture files) |

### 3.2 Customizations to Add

| Customization | Type | Purpose | Priority |
|---------------|------|---------|----------|
| **Onboarding guide** | `.github/instructions/onboarding.instructions.md` | Quick-start instructions for new architects: how to use the agent, available prompts, workspace structure | HIGH |
| **Team conventions** | Update `copilot-instructions.md` | Add team-specific conventions as the team grows (naming standards, review expectations, communication patterns) | MEDIUM — as team forms |
| **Additional agent personas** | `.agent.md` files | Specialized agents for specific roles (e.g., security architect, integration architect) — only if the team needs differentiated workflows | LOW — only when needed |
| **MCP server for external data** | `.vscode/mcp.json` + server implementation | Connect Copilot to external data sources (ticket systems, monitoring, document stores) when a concrete retrieval use case emerges | LOW — defer until retrieval workload is defined |
| **SKILL.md files** | `SKILL.md` | Package complex multi-step workflows as reusable skills (e.g., "create a solution design from scratch") — currently handled by prompt files | LOW — prompts are sufficient for now |

### 3.3 How Context Injection Works

For architects unfamiliar with how this works:

```
Architect opens VS Code with architecture repository
    │
    ├── Copilot reads copilot-instructions.md (always-on context)
    │     → Agent now knows the NovaTrek domain, service boundaries,
    │       safety rules, workflow patterns
    │
    ├── Copilot indexes all workspace files (automatic, background)
    │     → 22 OpenAPI specs, 14 ADRs, 15 metadata YAML files,
    │       6 solution designs — all searchable via @workspace
    │
    ├── Architect selects "Novatrek Solution Architect" agent
    │     → Scoped to architecture tasks, inherits global instructions
    │
    ├── Architect types a prompt or invokes #investigation
    │     → Agent uses workspace context + instructions + prompt
    │       workflow to produce structured output
    │
    └── Output follows team conventions automatically
          → MADR format for ADRs, C4 notation for diagrams,
            ISO 25010 for quality assessment — because the
            instructions define these standards
```

No infrastructure. No API keys. No pipeline. Every architect who clones the repo gets identical AI behavior, because the customizations are files in git.

---

## Phase 4: Scale and Enhance

**Goal:** Extend the setup as the team grows and new use cases emerge.

### 4.1 Team Scaling

| When | Action |
|------|--------|
| 2-5 architects | Shared repo with current customization layer. Peer review of instruction changes via PR. |
| 5-10 architects | Consider splitting instructions by domain (operations, booking, safety) using scoped `.instructions.md` with `applyTo` patterns. Monitor for conflicting conventions. |
| 10+ architects | Evaluate Copilot Enterprise for org-level policy controls, knowledge bases, and admin dashboards. |

### 4.2 Adding External Context via MCP

When a concrete retrieval use case emerges — "I need to search across content that is NOT in this git repository" — MCP is the extension mechanism:

| Use Case | MCP Server | Effort |
|----------|-----------|--------|
| Search JIRA/Azure DevOps tickets | MCP server calling JIRA REST API | Days (standard HTTP integration) |
| Search Confluence/SharePoint docs | MCP server with document search | Days to weeks (depending on auth) |
| Search other git repos | MCP server with multi-repo index | Weeks (requires indexing infrastructure) |
| Search via Foundry IQ knowledge base | MCP server calling Foundry IQ API | Weeks (requires Foundry IQ setup + auth bridge — see [MCP Bridge Analysis](../evidence/foundry-iq-comparison.md#can-mcp-bridge-the-gap)) |

Each MCP server is additive — it extends Copilot's reach without replacing anything. The workspace indexing, instructions, and agent definitions continue working exactly as before.

### 4.3 Measuring Value

| Metric | How to Measure | Baseline (Pilot) |
|--------|---------------|-------------------|
| Architecture artifacts produced per month | Count ADRs, solution designs, impact assessments | 14 ADRs + 6 solutions in pilot |
| Time from ticket to solution design | Timestamp comparison | Not measured in pilot — establish baseline |
| Consistency of output format | Peer review compliance rate | 96%+ in pilot (self-assessed) |
| Copilot usage intensity | Premium requests consumed / month | Track via GitHub billing dashboard |
| Customization evolution | Git commits to instruction/agent/prompt files | Track via git log |

---

## Summary

| Phase | What You Get | Effort | Dependencies |
|-------|-------------|--------|-------------|
| **Phase 0** (DONE) | Proven single-architect setup with full customization layer | Complete | None |
| **Phase 1** | Copilot seats for the team, verified workspace indexing | ~20 min per architect + procurement | GitHub Enterprise agreement or individual seats |
| **Phase 2** | Complete data inventory: what's in git, what moves to git, what needs MCP, what needs Foundry IQ. Tier 1-2 content fully indexed. | Hours for Tier 2 file moves; Tier 3-4 are future-phase planning | Phase 1 |
| **Phase 3** | Team inherits domain-aware AI behavior by cloning the repo | Already done — new architects get it for free | Phase 1 |
| **Phase 4** | MCP servers for live corporate data (Tier 3), Foundry IQ bridge for enterprise knowledge (Tier 4), team scaling, value measurement | Weeks to months, as needed | Concrete retrieval use cases |

The critical insight: **Phases 1-3 can be completed in a single day per architect.** The customization layer already exists. Most content is already in the workspace (Tier 1). Tier 2 content moves take hours. The hardest work — teaching Copilot the architecture domain — is already done. Tiers 3 and 4 (MCP and Foundry IQ) are additive enhancements that extend reach without changing the foundation.
