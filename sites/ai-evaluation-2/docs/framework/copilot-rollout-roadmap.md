<!-- CONFLUENCE-PUBLISH -->
<!-- CONFLUENCE-URL: https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2619671251/GitHub+Copilot+Rollout+Roadmap -->

# GitHub Copilot Rollout Roadmap

## Purpose

This roadmap defines the practical steps to roll out GitHub Copilot as the AI-assisted architecture tool for the Solution Architecture practice. It covers three workstreams:

1. **Licensing and access** — getting Copilot seats provisioned and configured
2. **Content preparation** — organizing architecture content so Copilot can index it effectively
3. **Context injection** — configuring instructions, skills, and agent definitions so Copilot understands the architecture domain

The roadmap is sequenced by dependency and value: each phase delivers usable capability before the next phase begins.

---

## Phase 0: Pilot (COMPLETE)

**Status:** Done. This is where we are today. Demonstrated using a realistic proof-of-concept workspace with synthetic services, architecture artifacts, and mock tool integrations.

| Deliverable | Status |
|-------------|--------|
| Single-architect Copilot Pro+ seat | Active |
| 1,172-line `copilot-instructions.md` with full domain model | Complete |
| Custom agent definition (Solution Architect persona) | Complete |
| 5 prompt workflows (investigation, deep-research, architecture-review, security-review, solution-verification) | Complete |
| 5 scoped instruction files (GitHub URLs, prompt-me workflow, architecture security, specs, solutions) | Complete |
| 22 OpenAPI service specs indexed in workspace | Complete |
| 14 ADRs, 6 solution designs, 37 PlantUML diagrams, 8 AsyncAPI event specs | Complete |
| 15 metadata YAML files (capabilities, tickets, domains, cross-service calls, events, data stores) | Complete |
| 18 wireframes across 3 applications (Excalidraw in pilot; team uses Figma) | Complete |
| Live architecture portal (MkDocs Material on Azure Static Web Apps) | Complete |
| Confluence publishing pipeline (automated mirror) | Complete |
| MCP server stub configured (Vikunja integration, not yet active) | Configured |

**Result:** 4 complete solution designs, 14 ADRs, and 139 generated sequence diagrams produced using this setup. The pilot validated that Copilot with declarative customization handles enterprise architecture work effectively.

---

## Phase 1: Licensing and Team Access

**Goal:** Get Copilot seats provisioned for the architecture team.

**Timeline:** Can start immediately; procurement timeline depends on existing GitHub Enterprise agreement.

### 1.1 Determine Licensing Path

The pilot ran on **GitHub Copilot Pro+** ($39/month, individual plan), which provides full agent mode capability including Claude Opus 4.6 access. For team rollout, GitHub Copilot Business or Enterprise is required — Pro+ does not support organization-level policy controls, centralized seat management, or content exclusion rules. The table below compares the team-appropriate tiers.

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
| GitHub Copilot extension | Install from VS Code marketplace (includes code completions, chat, and agent mode in a single extension) | 2 min |
| Sign in to GitHub | Authenticate with organizational or personal GitHub account | 2 min |
| Clone architecture repository | `git clone` the workspace repository | 5 min |
| Verify Copilot is active | Open a file, confirm Copilot icon in status bar, test with a chat prompt | 2 min |

**Total setup time per architect: ~18 minutes.** No infrastructure provisioning, no API keys, no gateway configuration.

### 1.3 Verify Workspace Indexing

After cloning, Copilot automatically indexes all workspace files. Verify by asking in Copilot Chat:

- "What services do we have?" (should list services from specs)
- "What does ADR-003 say?" (should return the relevant decision content)
- "Show me the OpenAPI spec for [service-name]" (should find and reference the spec file)

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

This content is already in GitHub repositories and VS Code workspaces today. Copilot indexes it automatically when an architect clones the repo.

| Data Category | What It Includes | Why It Matters for AI |
|--------------|-----------------|----------------------|
| **Company source code** | All application and service source code across the organization's GitHub repositories | Copilot can analyze code patterns, trace data flows, identify anti-patterns, cross-reference implementations against API contracts, and ground architecture recommendations in actual code rather than assumptions |
| **Architecture PlantUML diagrams** | C4 container/component diagrams, sequence diagrams, event flow diagrams | Copilot can reference existing diagrams when designing new integrations, verify that proposed changes align with documented architecture, and identify which diagrams need updating when services change |
| **Architecture Swagger/OpenAPI specs** | OpenAPI YAML specifications for all services — endpoints, schemas, request/response models | Copilot can validate that proposed API changes are backward-compatible, identify missing fields, check schema completeness, and cross-reference specs against source code to detect drift |
| **Architecture decisions (ADRs)** | MADR-formatted decision records documenting why key design choices were made | Copilot can reference prior decisions to avoid re-deciding settled questions, identify constraints that apply to new designs, and ensure new proposals do not contradict existing decisions |
| **Copilot customizations** | Instructions, agent definitions, prompt workflows, scoped rules | These ARE the context injection layer — they teach Copilot the domain model, team conventions, and workflow patterns. Every architect who clones the repo inherits identical AI behavior |

**Key insight:** Source code, architecture diagrams, and API specs are the three highest-value data categories for AI-assisted architecture work. All three are already in git and indexed automatically. This is a significant head start — most organizations would need to consolidate these before beginning.

### 2.3 Tier 2 — Migrate into Git

This content exists in a corporate system that is not indexed by Copilot. It needs to be exported and committed to the architecture repository so Copilot can see it.

| Data Category | What It Contains | Where It Lives Today | Migration Approach | Priority | Rationale |
|--------------|-----------------|---------------------|-------------------|----------|-----------|
| **Confluence pages** | Architecture documentation, design decisions, team knowledge bases, runbooks, onboarding guides, standards references | Confluence Cloud / Confluence Server | Export pages as Markdown, organize into `docs/` directory structure, commit to git. Establish git as the source of truth going forward — Confluence becomes a read-only mirror (see Phase 0 pilot for this pattern). | HIGH | Confluence pages are the single largest body of architecture knowledge not currently visible to Copilot. Architects reference these pages constantly during design work. Until they are in git, Copilot cannot use them as context, and architects must manually copy-paste relevant content into prompts. |
| **Figma design tokens** | Global design system definitions — color palettes, typography scales, spacing metrics, border radii, component variant properties | Figma (hosted on figma.com) | Automated CI/CD pipeline (GitHub Action) runs `figtree-cli` or `figma-extractor` to poll Figma API, extract design tokens as W3C DTCG-format JSON/YAML, and commit to git. Shallow key-value structure indexes flawlessly in Copilot's embedding engine. | MEDIUM | Design tokens give Copilot ambient awareness of the design system without MCP. However, tokens lack screen-specific layout data and user flow logic — the MCP server (Tier 3) fills that gap. See [Figma deep research](../research/deep-research-results-figma-chunking.md). |

**Migration considerations for Confluence:**

- **Volume:** Identify which Confluence spaces contain architecture-relevant content. Not every page needs to migrate — focus on spaces owned by the architecture team.
- **Freshness:** Some Confluence pages are living documents updated weekly; others have not been touched in years. Stale pages may still have value as historical context, but should be clearly marked.
- **Attachments:** Confluence pages often embed diagrams, spreadsheets, and PDFs as attachments. These need to be converted or referenced, not ignored.
- **Cross-links:** Confluence pages link to each other extensively. When migrating to Markdown in git, internal links need to be rewritten to relative paths.
- **Ongoing sync:** After migration, decide whether Confluence continues to exist as a read-only mirror (generated from git) or is decommissioned entirely for architecture content. The pilot already demonstrated the git-to-Confluence publishing pipeline — the same approach scales to all architecture pages.

**Recommended migration workflow — Confluence HTML export + Pandoc:**

There is no dedicated "Confluence-to-Markdown" tool in active maintenance. The most reliable approach combines Confluence's native HTML export with Pandoc for format conversion. This produces clean, Git-friendly Markdown with minimal manual cleanup.

**Step 1 — Export from Confluence:**

1. Open the Confluence space to migrate
2. Navigate to Space Settings → General → Export Space
3. Select **HTML** as the export format
4. Choose content scope — select all pages, or filter to architecture-relevant pages only
5. Click Export — Confluence produces a zip archive containing HTML files and an `attachments/` directory organized by page ID

**Step 2 — Convert HTML to Markdown with Pandoc:**

```bash
# Unzip the Confluence export
unzip confluence-export.zip -d ./confluence-html

# Convert each HTML file to GitHub-Flavored Markdown
find ./confluence-html -name "*.html" | while read f; do
  # Preserve directory structure
  outdir="./docs/confluence/$(dirname "${f#./confluence-html/}")"
  mkdir -p "$outdir"

  # Convert with Pandoc
  #   -f html           → read Confluence's HTML output
  #   -t gfm            → write GitHub-Flavored Markdown (best for git rendering)
  #   --wrap=none        → do not hard-wrap lines (let git/editors handle wrapping)
  #   --extract-media    → pull inline images into a local directory
  pandoc -f html -t gfm --wrap=none \
    --extract-media="$outdir/media" \
    "$f" -o "$outdir/$(basename "${f%.html}.md")"
done
```

**Step 3 — Post-processing:**

| Task | What to Fix | Approach |
|------|-------------|----------|
| **Rewrite internal links** | Confluence `pageId`-based links become broken | Script to replace `/pages/viewpage.action?pageId=12345` with relative Markdown paths based on page title mapping |
| **Move attachments** | Confluence stores attachments in `download/attachments/<pageId>/` | Copy to a predictable `attachments/` directory alongside each page, update image references |
| **Clean up Confluence macros** | `{code}`, `{info}`, `{warning}`, `{toc}` blocks may render as raw HTML | Pandoc handles most macro HTML correctly; remaining artifacts are typically `<div>` wrappers that can be stripped with `sed` or a simple Python script |
| **Mark stale pages** | Pages not updated in 12+ months | Add a `> NOTE: This page was last updated in Confluence on [date]. Review for accuracy.` banner at the top |
| **Remove boilerplate** | Confluence export includes navigation chrome, breadcrumbs, footer | Pandoc's `-f html` parser mostly ignores these, but spot-check output for leftover navigation markup |

**Step 4 — Commit and verify:**

```bash
# Add the converted Markdown to the architecture repository
git add docs/confluence/
git commit -m "docs: migrate Confluence architecture pages to Markdown"
git push
```

After pushing, Copilot indexes the new Markdown files automatically. Verify by asking Copilot: "What do we have in the Confluence migration docs?" — it should reference the newly committed content.

**Estimated effort:** 2-4 hours for a space with 50-200 pages. The export and conversion steps are fully automated; post-processing (link rewriting, attachment cleanup) is the manual work. A Python script to automate link rewriting based on a title-to-path mapping table can reduce this to under an hour for subsequent spaces.

### 2.4 Tier 3 — Access via MCP Server (Live Queries)

This data lives in corporate systems that change in real time. It should NOT be copied into git — it would go stale immediately. Instead, an MCP server provides live query access when Copilot needs it.

The pilot demonstrated this pattern using local mock scripts that simulate what MCP servers would do in production — proving the tool-call interface works before investing in real integrations.

| Data Category | Corporate System | What the Architect Needs | MCP Server Approach | Priority |
|--------------|-----------------|-------------------------|---------------------|----------|
| Work items and tickets | JIRA or Azure DevOps | Ticket details, status, comments, linked issues — to understand requirements before designing | MCP server calling JIRA/ADO REST API with read-only access. Query by ticket ID, filter by status/component/label. | HIGH — this is the most frequent external data need during architecture work |
| Production logs and metrics | Elasticsearch, Datadog, or Application Insights | Error logs, latency metrics, traffic patterns — to ground architecture analysis in production evidence | MCP server querying observability APIs. Filter by service, severity, time range, keyword. | HIGH — essential for investigation scenarios |
| Source control activity | GitHub or GitLab | Recent PRs/MRs, code diffs, branch status — to understand what changed and when | MCP server calling GitHub/GitLab API. List PRs by repo, get diff for specific PR, search commits. | MEDIUM — useful during investigations but architects can also browse the UI |
| CI/CD pipeline status | GitHub Actions, Azure DevOps Pipelines, or Jenkins | Build results, test failures, deployment history — to assess whether a service is stable before proposing changes | MCP server querying pipeline APIs. Get latest build status, test results for a service. | MEDIUM — valuable but not blocking architecture decisions |
| Service registry / CMDB | ServiceNow, Backstage, or internal CMDB | Service ownership, SLA targets, deployment tier, dependency graph — to validate service metadata is current | MCP server querying CMDB API. Lookup service by name, get owner/tier/dependencies. | LOW — metadata YAML in git covers this for now; MCP adds live validation |
| Incident history | PagerDuty, ServiceNow, or Opsgenie | Past incidents, root cause analysis, affected services — to identify recurring architectural weaknesses | MCP server querying incident management API. Search by service, severity, date range. | LOW — useful for pattern detection but not a daily need |
| Figma wireframes and UI designs | Figma (hosted on figma.com) | Frame layouts, component hierarchies, state variations, user flow transitions, Dev Mode annotations — to derive API data requirements and validate service orchestration against actual screen designs | Official `@figma/mcp-server` (requires paid Dev/Full seat) or community `@yhy2001/figma-mcp-server` (Smart Layout Detection, caching). Architect passes Figma frame URL into Copilot Chat; MCP server returns structured layout, component properties, and Code Connect mappings. | MEDIUM — high value for UI-facing services but not needed for pure backend architecture decisions |

**Key principle:** Each MCP server is a thin adapter — it translates Copilot's tool calls into the corporate system's API. The architecture team does not need to build indexing infrastructure. MCP servers are additive: each one extends Copilot's reach without changing anything about the workspace, instructions, or agent definitions.

### 2.5 Tier 4 — Access via Foundry IQ or Enterprise Knowledge Base

This data is large, unstructured, and spread across Microsoft 365. It cannot be moved into git (too large, wrong ownership, wrong format) and is not well-suited to real-time MCP queries (requires full-text search over large corpora, not point lookups).

This is the retrieval workload that enterprise knowledge layers like Foundry IQ are designed for. See [Foundry IQ Comparison](../evidence/foundry-iq-comparison.md) for detailed analysis.

| Data Category | Where It Lives | Why It Cannot Be in Git or MCP | How Foundry IQ / Knowledge Base Addresses It |
|--------------|---------------|-------------------------------|---------------------------------------------|
| **Office 365 documents** | Word documents, PowerPoint decks, OneNote notebooks in OneDrive and Teams channels | Binary formats not suited for git. Updated by non-technical stakeholders who do not use git. Volume is too large to clone. | Foundry IQ natively indexes Microsoft 365 content. Architects can search across Word docs and PowerPoint decks for relevant requirements, business rules, and stakeholder decisions without leaving VS Code. |
| **SharePoint spreadsheets and lists** | Excel workbooks, SharePoint lists used for tracking, capacity planning, risk registers, compliance matrices | Tabular data in binary format. Updated by multiple teams on their own schedule. Git cannot meaningfully diff or merge Excel files. | Foundry IQ indexes SharePoint content including Excel metadata. Architects search for "what are the SLA targets for payment processing?" and get relevant spreadsheet content surfaced as text. |
| **SharePoint sites and document libraries** | Team sites, project document libraries, policy repositories | Owned by other teams, updated independently, too large to clone. An MCP point-lookup requires knowing which document to fetch — but the architect often does not know what exists. | Foundry IQ indexes SharePoint sites and enables semantic search across document libraries. Architects can discover relevant content without knowing which site or folder it lives in. |
| **Teams channel conversations** | Architecture discussions, design decisions made in chat, meeting notes | Ephemeral and high-volume. Not practical to export to git. Critical decisions are often buried in chat threads. | Foundry IQ can index Teams messages, surfacing past design discussions when relevant to new work. |
| **Compliance and regulatory frameworks** | SharePoint document management, controlled distribution folders | Large corpus, controlled distribution, subject to legal review. Not appropriate for a git repository accessible to all developers. | Foundry IQ can index approved compliance documents with access controls preserved. Architects search for applicable regulations during security reviews. |
| **Vendor reference documentation** | Vendor portals, licensed PDF/HTML documentation | Licensing restrictions prevent redistribution. Content updates on vendor's schedule. | Foundry IQ can index vendor docs (where licensing permits) without the architect browsing vendor portals. |
| **Cross-team architecture content** | Other teams' Confluence spaces, SharePoint sites, git repos | Different ownership, different change cadence. Copying creates stale forks. | Foundry IQ provides cross-corpus semantic search. An architect designing a new integration can find how other teams solved similar problems. |

**Key principle:** Foundry IQ solves the "I don't know what I don't know" problem. Git and MCP work when the architect knows what to look for. Foundry IQ works when the architect needs to discover relevant content across a broad corpus — especially across Microsoft 365, where architecture-relevant information is scattered across Word docs, Excel sheets, SharePoint sites, and Teams threads.

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
| **Global instructions** | `.github/copilot-instructions.md` (1,172 lines) | Domain model, service ownership, solution design workflow, architecture standards, document formatting, portal generation. **NOTE:** Research indicates files exceeding ~1,000 lines suffer non-deterministic attention degradation ([see context injection analysis](../evidence/context-injection-controls.md#size-limits-and-degradation)). Decomposition into scoped files is recommended before team rollout. |
| **Solution Architect agent** | `.github/agents/solution-architect.agent.md` | Specialized persona scoped to architecture work — triage, design, review, ADR authoring. Tool restrictions prevent non-architecture tasks |
| **Investigation prompt** | `.github/prompts/investigation.prompt.md` | Structured workflow: JIRA context, Elastic logs, GitLab MRs, architecture analysis |
| **Deep research prompt** | `.github/prompts/deep-research.prompt.md` | Multi-source evidence synthesis with cross-referencing |
| **Architecture review prompt** | `.github/prompts/architecture-review.prompt.md` | Anti-pattern detection, ISO 25010 quality assessment |
| **Security review prompt** | `.github/prompts/security-review.prompt.md` | OWASP Top 10 + domain-specific safety rules |
| **Solution verification prompt** | `.github/prompts/solution-verification.prompt.md` | 8-gate quality check before merge |
| **GitHub URL rules** | `.github/instructions/github-urls.instructions.md` | Prevents malformed GitHub links (applies to all files) |
| **Prompt-me workflow** | `.github/instructions/prompt-me.instructions.md` | Interactive decision loop — step through plans one item at a time |
| **Architecture security** | `architecture/.instructions.md` | Data ownership, identity resolution, safety defaults (scoped to architecture files) |

### 3.2 Customizations to Add

| Customization | Type | Purpose | Priority |
|---------------|------|---------|----------|
| **Onboarding guide** | `.github/instructions/onboarding.instructions.md` | Quick-start instructions for new architects: how to use the agent, available prompts, workspace structure | HIGH |
| **Decompose global instructions** | Split `copilot-instructions.md` into scoped files | Move domain-specific rules (OpenAPI conventions, solution design workflow, diagram standards) into `applyTo`-scoped files. Keep global file under ~500 lines with core domain model and safety rules only. Scoped files are injected only when matching files are active, preventing token waste. | HIGH — mitigates attention degradation risk |
| **Team conventions** | Update `copilot-instructions.md` | Add team-specific conventions as the team grows (naming standards, review expectations, communication patterns) | MEDIUM — as team forms |
| **Additional agent personas** | `.agent.md` files | Specialized agents for specific roles (e.g., security architect, integration architect) — only if the team needs differentiated workflows | LOW — only when needed |
| **SKILL.md files** | `SKILL.md` | Package complex multi-step workflows as reusable skills (e.g., "create a solution design from scratch") — currently handled by prompt files | LOW — prompts are sufficient for now |
| **Scoped instruction for OpenAPI specs** | `.github/instructions/openapi-specs.instructions.md` | Instruct the LLM: "When analyzing OpenAPI specs, the file may be retrieved in fragments. Always retrieve both the endpoint and its `$ref` component schemas before generating analysis." Mitigates YAML chunking fragmentation. | HIGH — zero-cost mitigation for a known blind spot |
| **AGENTS.md repository map** | `AGENTS.md` at repo root | Explicit topology map for the AI agent: which directories contain specs, source code, ADRs, wireframes, and which MCP tools to use for each. Adopted by 60,000+ repositories as the standard for AI agent navigation. | MEDIUM — improves retrieval routing |

### 3.3 How Context Injection Works

For architects unfamiliar with how this works:

```
Architect opens VS Code with architecture repository
    │
    ├── Copilot reads copilot-instructions.md (always-on context)
    │     → Agent now knows the domain model, service boundaries,
    │       safety rules, workflow patterns
    │
    ├── Copilot indexes all workspace files (automatic, background)
    │     → OpenAPI specs, ADRs, metadata YAML files,
    │       solution designs — all searchable via @workspace
    │
    ├── Architect selects "Solution Architect" agent
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

!!! info "Deep dive: How chunking and retrieval actually work"
    Copilot's context injection pipeline is more nuanced than the diagram above suggests. YAML and Markdown files receive *worse* chunking treatment than source code — they fall back to generic 60-line sliding windows instead of AST-aware parsing. This affects how OpenAPI specs and ADRs are retrieved. See [Controlling What Copilot Sees](../evidence/context-injection-controls.md) for the full analysis, including the priority hierarchy, file structure optimization, and MCP as a custom chunking bypass.

---

## Phase 4: Scale and Enhance

**Goal:** Extend the setup as the team grows and new use cases emerge.

### 4.1 Team Scaling

| When | Action |
|------|--------|
| 2-5 architects | Shared repo with current customization layer. Peer review of instruction changes via PR. |
| 5-10 architects | Consider splitting instructions by domain using scoped `.instructions.md` with `applyTo` patterns. Monitor for conflicting conventions. |
| 10+ architects | Evaluate Copilot Enterprise for org-level policy controls and admin dashboards. Evaluate **Copilot Spaces** for cross-repository context sharing (replaced Knowledge Bases in Nov 2025). Note: Spaces are limited to GitHub-hosted content — external systems still require MCP. |

### 4.2 Adding External Context via MCP

When a concrete retrieval use case emerges — "I need to search across content that is NOT in this git repository" — MCP is the extension mechanism. See Section 2.4 (Tier 3) for the prioritized MCP integration list with effort estimates. Add MCP servers incrementally as concrete retrieval use cases emerge.

Each MCP server is additive — it extends Copilot's reach without replacing anything. The workspace indexing, instructions, and agent definitions continue working exactly as before.

**Critical design constraint:** Research reveals that Copilot enforces a **hard 10KB truncation limit** on MCP tool responses. Responses exceeding this threshold are silently corrupted — the LLM receives broken JSON with no warning. Extended sessions with large MCP payloads can trigger HTTP 413 errors that create unrecoverable retry loops. All MCP servers built for this team must:

- Return paginated results (10-25 items per call with cursor tokens)
- Strip non-essential metadata (internal IDs, stack traces, raw telemetry)
- Provide summary views first, with detail available on follow-up calls
- Target responses under 5KB to maintain a safety margin

See [Controlling What Copilot Sees](../evidence/context-injection-controls.md#mcp-server-design-constraints) for the full analysis.

An additional MCP use case emerged from chunking research: **OpenAPI specs receive generic token-window chunking** (not AST-aware YAML parsing), which fragments endpoint-schema relationships. An OpenAPI MCP server (e.g., `openapi-mcp` or a custom FastMCP implementation) would expose each endpoint as a discrete tool, entirely bypassing Copilot's native indexing limitation. This is a higher-value MCP use case than external system integration because it fixes a known retrieval quality problem for content already in the workspace.

See [Controlling What Copilot Sees — MCP as a Custom Chunking Layer](../evidence/context-injection-controls.md#mcp-as-a-custom-chunking-layer) for the architecture pattern.

### 4.3 BYOK Model Integration (Option D — Hybrid)

When the Foundry team has a domain-specialized model ready for architecture work, Copilot's BYOK (Bring Your Own Key) mechanism allows it to appear alongside built-in models in every architect's model picker — no IDE changes, no custom extensions.

| Step | Action | Owner | Effort |
|------|--------|-------|--------|
| 1 | Deploy fine-tuned model to Azure AI Foundry endpoint | Foundry team | Already in progress |
| 2 | Register Foundry endpoint in GitHub Copilot admin settings (Enterprise/Business) | GitHub admin | ~15 minutes (one-time) |
| 3 | Architects select custom model from model picker for domain-specialized tasks | Each architect | Zero — appears automatically |
| 4 | Establish usage guidance: when to use custom model vs built-in Opus vs 0x models | Architecture practice lead | 1-2 hours (document norms) |
| 5 | Monitor BYOK usage via Azure consumption metrics (token counts, latency, cost) | Foundry team | Ongoing |

**Key properties of BYOK integration:**

- BYOK requests do NOT consume Copilot premium request quotas — they bill at Azure consumption rates
- The custom model coexists with all built-in models (GPT-4o, GPT-4.1, Opus) — architects switch freely
- All existing Copilot customizations (instruction files, agents, prompt workflows) work identically with the BYOK model
- BYOK is GA via CLI (Feb 2026) and Public Preview in admin UI — see [Option D — Hybrid Architecture](../evidence/option-d-hybrid-architecture.md) for maturity details
- No Entra ID / managed identity support yet — static API keys only (rotate on schedule)

!!! warning "BYOK Limitations to Track"
    Three gaps require monitoring before full production reliance: (1) No Entra ID support — static API keys lack auto-refresh and managed identity integration. (2) Audit logging is provider-side (Azure), not GitHub-side — requires separate log aggregation. (3) Fine-tuned model quality is bounded by training data — a model fine-tuned on outdated architecture patterns will confidently produce outdated guidance. See [DD-06: IDE Client Selection](../decisions/dd-06-ide-client-selection.md) for the frozen customization risk.

### 4.4 Measuring Value

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
| **Phase 1** | Copilot seats for the team, verified workspace indexing | ~18 min per architect + procurement | GitHub Enterprise agreement or individual seats |
| **Phase 2** | Complete data inventory: what's in git, what moves to git, what needs MCP, what needs Foundry IQ. Tier 1-2 content fully indexed. | 2-4 hours (Tier 2 file moves) + ongoing (Tier 3-4 integrations planned here, built in Phase 4) | Phase 1 |
| **Phase 3** | Team inherits domain-aware AI behavior by cloning the repo | Already done — new architects get it for free | Phase 1 |
| **Phase 4** | MCP servers for live corporate data (Tier 3), Foundry IQ bridge for enterprise knowledge (Tier 4), BYOK custom model integration (Option D Hybrid), team scaling, value measurement | Weeks to months, as needed | Concrete retrieval use cases; Foundry model readiness for BYOK |

The critical insight: **Phases 1-3 can be completed in a single day per architect.** The customization layer already exists. Most content is already in the workspace (Tier 1). Tier 2 content moves take hours. The hardest work — teaching Copilot the architecture domain — is already done. Tiers 3 and 4 (MCP and Foundry IQ) are additive enhancements that extend reach without changing the foundation.
