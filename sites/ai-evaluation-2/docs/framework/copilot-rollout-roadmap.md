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

**Goal:** Ensure all architecture content is in the workspace so Copilot can index it. Content that lives in the workspace is automatically available as context.

### 2.1 Content Already in Workspace (No Action Needed)

| Content Type | Count | Location | Indexed? |
|-------------|-------|----------|----------|
| OpenAPI service specs | 22 | `architecture/specs/` | Yes, automatically |
| Architecture Decision Records | 14 | `decisions/` | Yes, automatically |
| Solution designs | 6 | `architecture/solutions/` | Yes, automatically |
| PlantUML diagrams | 37 | `architecture/diagrams/` | Yes, automatically |
| AsyncAPI event specs | 8 | `architecture/events/` | Yes, automatically |
| Metadata YAML | 15 | `architecture/metadata/` | Yes, automatically |
| Wireframes (Excalidraw) | 18 | `architecture/wireframes/` | Yes, automatically |

### 2.2 Content to Bring into the Workspace

| Content | Current Location | Target Location | Action | Priority |
|---------|-----------------|-----------------|--------|----------|
| Architecture standards (MADR template, C4 guide, arc42 template, ISO 25010 quality tree) | `phases/phase-1-ai-tool-cost-comparison/workspace/architecture-standards/` | `architecture-standards/` | Copy to workspace root | HIGH — referenced by copilot-instructions.md but currently only in Phase 1 isolated workspace |
| Source code examples | Not present (referenced in instructions) | `source-code/` or remove references | Either add representative Java service implementations, or remove source code analysis guidelines from instructions | MEDIUM — instructions reference analysis patterns that have no content to analyze |
| Mock tool scripts | `phases/phase-1-ai-tool-cost-comparison/workspace/scripts/` and `scripts/` | Already in `scripts/` at root | Verify `scripts/mock-jira-client.py` etc. are accessible from workspace root | LOW — already partially addressed |

### 2.3 Content That Should NOT Be in the Workspace

Not all content needs to be in the git repository. Content that belongs elsewhere:

| Content Type | Why Not in Workspace | How to Access |
|-------------|---------------------|---------------|
| Vendor documentation | Licensing restrictions, frequent updates | Future: MCP server pointing at vendor doc index |
| Regulatory/compliance docs | Controlled distribution, access restrictions | Future: MCP server with access control |
| SharePoint content from other teams | Cross-team ownership, not architecture-owned | Future: Foundry IQ knowledge base via MCP |
| Other team's git repositories | Separate ownership, separate change cadence | Future: Copilot multi-repo support or MCP |

These are retrieval workloads (see [Glossary: Retrieval Workload](../reference/glossary.md#retrieval-workload)). They require indexing infrastructure beyond workspace indexing. MCP is the bridge — when a concrete cross-repo use case emerges, an MCP server can expose external content to Copilot without moving it into the workspace.

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
| **Phase 2** | All architecture content indexed and accessible to Copilot | Hours (file moves + verification) | Phase 1 |
| **Phase 3** | Team inherits domain-aware AI behavior by cloning the repo | Already done — new architects get it for free | Phase 1 |
| **Phase 4** | External data via MCP, team scaling, value measurement | Weeks to months, as needed | Concrete retrieval use cases |

The critical insight: **Phases 1-3 can be completed in a single day per architect.** The customization layer already exists. The content is already in the workspace. The hardest work — teaching Copilot the architecture domain — is already done.
