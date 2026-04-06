<!-- CONFLUENCE-PUBLISH -->

# DD-01: Content Injection Strategy

> **You are reading:** Layer 2 — Toolchain Decision 1 of 4 | [Decision Framework](decision-framework.md) | [Home](../../index.md)
>
> This is a toolchain decision (what to buy/build). For the practice-level operating model, see [Practice Strategy](../practice-strategy.md) (Layer 1).

## Do We Need Custom MCP Servers?

| | |
|-----------|-------|
| **Status** | Under Evaluation |
| **Date** | 2026-04-03 |
| **Category** | Architecture |
| **Maps to** | DP-09 (Context Enrichment Strategy), DP-19 (Hybrid MCP) |
| **Stakeholder Input Required** | Yes |

---

## Context and Problem Statement

The architecture practice needs AI to reason about enterprise context — architecture standards, domain models, OpenAPI specs, ticket history, production logs, code patterns, and organizational knowledge. The question is not whether to inject context, but **how**.

One approach is to build **custom MCP (Model Context Protocol) servers** to inject proprietary enterprise context (Confluence knowledge bases, CMDB data, ServiceNow tickets, internal APIs) into AI workflows.

An alternative approach is to leverage **native toolchain capabilities** — Copilot's workspace semantic indexing, the `copilot-instructions.md` instruction system, and lightweight local MCP servers — which already achieve context injection without custom infrastructure. For content sources like Confluence, the architecture practice can **migrate content to markdown files in the repository**, published to both MkDocs portals and Confluence via CI — eliminating the need for a Confluence MCP server entirely.

**This decision must be made independently of toolchain selection.** Regardless of which tool wins, the practice needs a principled framework for when custom content injection is justified vs when native capabilities are sufficient.

---

## Content Injection Taxonomy

Before evaluating options, classify all content types the AI consumes and assess how well each is served by existing capabilities:

### Content Type Classification

| # | Content Type | Volatility | Size | Current Source | Native Coverage | Gap |
|---|-------------|-----------|------|---------------|----------------|-----|
| C1 | Architecture standards (arc42, C4, MADR) | Static — evolves quarterly | ~10K tokens | `copilot-instructions.md` | FULL — loaded every session | None |
| C2 | Domain model (services, APIs, data ownership) | Semi-static — evolves per solution | ~15K tokens | `architecture/metadata/*.yaml`, OpenAPI specs | FULL — workspace indexed | None |
| C3 | Solution design templates and conventions | Static — evolves slowly | ~5K tokens | `copilot-instructions.md` + `.instructions.md` files | FULL — loaded contextually | None |
| C4 | Current ticket context (active work items) | Dynamic — changes per session | ~2K tokens | Vikunja MCP server (local) | FULL — MCP already built | None |
| C5 | Production evidence (logs, metrics, traces) | Real-time | Variable | Mock scripts (synthetic) | PARTIAL — synthetic only | Real production data not accessible |
| C6 | Source code and OpenAPI specs | Semi-static | ~200K tokens (full workspace) | Workspace files | FULL — Copilot indexes natively | None |
| C7 | Prior solution designs (completed work) | Static post-completion | ~50K tokens total | `architecture/solutions/` directory | FULL — workspace indexed | None |
| C8 | Enterprise Confluence knowledge base | Semi-static, large corpus | Millions of tokens | Not connected | NONE | Migrate to repository markdown; publish to Confluence + MkDocs via CI |
| C9 | CMDB / ServiceNow service registry | Dynamic | ~50K tokens | Not connected | NONE | Requires integration |
| C10 | Cross-team architecture decisions (other teams) | Semi-static | ~100K+ tokens | Not connected | NONE | Requires integration |

### Gap Analysis Summary

| Coverage Level | Content Types | Custom MCP Justified? |
|---------------|--------------|----------------------|
| FULL — native capabilities sufficient | C1, C2, C3, C4, C6, C7 | No — already working |
| PARTIAL — synthetic gap | C5 | Maybe — depends on production data access strategy |
| NONE — enterprise data not accessible | C9, C10 | Possibly — but only if the use case justifies the cost |
| NONE — but solvable by content migration | C8 | No — migrate Confluence content to repository markdown published via CI |

**Key finding:** 7 of 10 content types are already fully served by native capabilities. C8 (Confluence) is solvable by migrating content to markdown files in the repository, published to Confluence and MkDocs portals via CI — bringing it into the workspace where native indexing covers it. The remaining 2 gaps (C9, C10) are enterprise data sources that require integration regardless of which AI tool is selected.

---

## Options

### Option A: Native Only — No Custom MCP Servers

**Description:** Rely entirely on the toolchain's native context management. Copilot's workspace semantic indexing handles code and specs. The `copilot-instructions.md` provides architecture standards. Local MCP servers handle ticketing. Confluence content (C8) is migrated to markdown files in the repository and published to Confluence via CI, making it natively indexable. Remaining enterprise data sources (C9-C10) are accessed manually when needed.

**Architecture:**

```
┌──────────────────────────────────────┐
│  Developer Workstation               │
│  ┌────────────────────────────────┐  │
│  │  AI Toolchain (Copilot/Claude) │  │
│  │  - Native workspace indexing   │  │
│  │  - Instructions (always-on)    │  │
│  │  - File reads (on-demand)      │  │
│  └──────────┬─────────────────────┘  │
│             │                        │
│  ┌──────────▼──────────┐             │
│  │  Local MCP Servers  │             │
│  │  - Vikunja tickets  │             │
│  │  - Mock tools       │             │
│  └─────────────────────┘             │
│                                      │
│  ┌─────────────────────────────────┐ │
│  │  Workspace Files                │ │
│  │  - OpenAPI specs (19 services)  │ │
│  │  - Metadata YAML (10 files)    │ │
│  │  - Solution designs            │ │
│  │  - Java source code            │ │
│  └─────────────────────────────────┘ │
└──────────────────────────────────────┘
```

**Strengths:**

- Zero additional infrastructure
- Zero engineering investment
- Already proven: 96.1% quality with native context
- No operational burden
- Content types C1-C4, C6-C7 all fully covered

**Weaknesses:**

- No access to enterprise data (C8-C10) without manual copy-paste
- Single-player mode — no shared enterprise context across teams
- If the workspace grows beyond indexing capacity, quality may degrade

**When this is the right choice:** When the architecture practice operates within a self-contained workspace and enterprise knowledge base access is either unnecessary or manageable through manual lookup.

---

### Option B: Native + Targeted MCP — Selective Integration

**Description:** Keep native capabilities for all currently-served content types (C1-C7). Migrate Confluence content (C8) to repository markdown published via CI. Build targeted MCP servers only for the 1-2 enterprise data sources that represent genuine gaps (CMDB service registry, cross-team ADR index). No RAG pipeline, no vector database — each MCP server is a thin API adapter.

**Architecture:**

```
┌──────────────────────────────────────┐
│  Developer Workstation               │
│  ┌────────────────────────────────┐  │
│  │  AI Toolchain (Native Context) │  │
│  │  + MCP client                  │  │
│  └──────────┬──────────┬──────────┘  │
│             │          │             │
│  ┌──────────▼──────┐   │             │
│  │  Local MCP      │   │             │
│  │  - Vikunja      │   │             │
│  │  - Mock tools   │   │             │
│  └─────────────────┘   │             │
└────────────────────────┼─────────────┘
                         │  MCP (HTTPS)
                         │
┌────────────────────────▼─────────────┐
│  Targeted MCP Servers (1-2 only)     │
│  - CMDB/ServiceNow lookup            │
│  - (Optional: cross-team ADR index)  │
│  Auth: Entra ID / API tokens         │
└──────────────────────────────────────┘
```

**Strengths:**

- Fills genuine gaps (C8-C10) without disrupting what works
- Each MCP server is a thin, maintainable adapter (not a RAG pipeline)
- Incremental — build one at a time, validate value before building the next
- Native context remains the primary source — MCP supplements, not replaces
- MCP is an open standard — servers work with any MCP-compatible client

**Weaknesses:**

- Engineering investment (1-2 months per MCP server)
- Operational burden for hosted MCP servers (monitoring, auth, uptime)
- Latency for remote MCP calls vs local file reads
- Risk of scope creep — "just one more MCP server" pressure

**When this is the right choice:** When the practice has identified specific, high-value enterprise data sources that the AI cannot access natively, and the expected benefit justifies the per-server engineering cost.

---

### Option C: Full Custom MCP Pipeline — Comprehensive Content Injection

**Description:** Build a comprehensive custom MCP pipeline that handles all content injection: workspace context, architecture standards, enterprise knowledge, and production data. Includes a vector database for semantic retrieval, embedding pipeline for knowledge ingestion, and custom RAG orchestration.

**Architecture:**

```
┌──────────────────────────────────────┐
│  Developer Workstation               │
│  ┌────────────────────────────────┐  │
│  │  Roo Code + Kong AI Gateway   │  │
│  │  + MCP client                  │  │
│  └──────────┬─────────────────────┘  │
└─────────────┼────────────────────────┘
              │  MCP (HTTPS)
              │
┌─────────────▼────────────────────────┐
│  Custom MCP Server Farm              │
│  ┌─────────────────────────────────┐ │
│  │  Content Services               │ │
│  │  - Workspace indexer (Qdrant)   │ │
│  │  - Standards server             │ │
│  │  - Ticket server (JIRA API)     │ │
│  │  - Confluence RAG pipeline      │ │
│  │  - CMDB integration             │ │
│  │  - Production log aggregator    │ │
│  │  - Cross-team ADR index         │ │
│  └──────────┬──────────────────────┘ │
│             │                        │
│  ┌──────────▼──────────────────────┐ │
│  │  Infrastructure                 │ │
│  │  - Qdrant vector database       │ │
│  │  - Embedding pipeline           │ │
│  │  - Kong AI Gateway              │ │
│  │  - Auth (Entra ID)              │ │
│  │  - Monitoring + alerting        │ │
│  └─────────────────────────────────┘ │
└──────────────────────────────────────┘
```

**Strengths:**

- Complete control over all context injection
- Full enterprise data access regardless of AI toolchain
- Can optimize retrieval quality with custom embeddings and re-ranking
- Toolchain-agnostic — works with any MCP client (Roo Code, Claude Code, Copilot)

**Weaknesses:**

- **Reinvents native capabilities**: workspace indexing, instruction loading, and file retrieval are rebuilt from scratch
- Estimated 4-8 developer-months to build, 1-2 FTE to operate
- Qdrant + embedding pipeline adds $75-250/month infrastructure cost
- Custom workspace indexer replicates what Copilot provides for free
- Custom standards server replicates what `copilot-instructions.md` provides for free
- Custom ticket server replicates the already-built Vikunja MCP server
- Operational complexity: 7+ services to monitor, scale, and maintain
- Latency: every context retrieval goes through network calls vs local file reads

**When this is the right choice:** When the organization has deep, custom knowledge management requirements that cannot be served by targeted servers, AND has the engineering capacity to build and maintain the full pipeline, AND the AI toolchain does not provide native workspace indexing.

---

## The "Reinventing the Wheel" Analysis

For each capability that custom MCP would provide, does a native equivalent already exist?

| Capability | Custom MCP Approach | Native Equivalent | Verdict |
|-----------|-------------------|-------------------|---------|
| Workspace file search | Qdrant vector index | Copilot semantic search | REINVENTION — native is better (server-side, free) |
| Architecture standards injection | MCP server serving rules | `copilot-instructions.md` (auto-loaded) | REINVENTION — native is simpler |
| OpenAPI spec context | Embedding + retrieval pipeline | Workspace files (indexed natively) | REINVENTION — native covers this |
| Ticket access | Custom JIRA MCP server | Vikunja MCP server (already built) | REINVENTION — already solved |
| Source code analysis | Custom code indexer | Native file reads + search | REINVENTION — native is adequate |
| Solution design templates | Custom template server | `.instructions.md` + SKILL.md | REINVENTION — native mechanism exists |
| Confluence knowledge base | Confluence MCP + RAG | Migrate to repository markdown; CI publishes to Confluence + MkDocs | SOLVABLE — migrate content to repo, no MCP needed |
| CMDB / service registry | CMDB API MCP server | No native equivalent | GENUINE GAP — custom server justified |
| Cross-team ADR repository | Federated ADR MCP server | No native equivalent | GENUINE GAP — custom server justified |
| Production logs (real) | Log aggregator MCP server | Mock scripts (synthetic only) | GENUINE GAP — but dependency on production access |

**Result:** 6 of 10 capabilities are reinventions of native features. Only 4 represent genuine gaps — and of those, C8 (Confluence) is solvable by migrating content to repository markdown. The remaining 2 enterprise data sources (C9-C10) could be addressed by targeted MCP servers (Option B) without a full pipeline.

---

## Cost-Benefit Analysis by Content Type

| Content Type | Custom MCP Cost | Native Cost | Marginal Value of Custom | Recommendation |
|-------------|----------------|------------|------------------------|----------------|
| C1: Architecture standards | 1 month build + ongoing | $0 (already in instructions) | Negative — adds complexity for no benefit | USE NATIVE |
| C2: Domain model | 2 months build + Qdrant | $0 (workspace indexed) | Negative — native indexing is superior | USE NATIVE |
| C3: Templates | 0.5 months build | $0 (SKILL.md files) | Negative | USE NATIVE |
| C4: Tickets | 1 month build | $0 (Vikunja MCP exists) | Negative — already solved | USE NATIVE |
| C5: Production logs | 1 month build + log access | $0 (synthetic mock) | Positive IF real data access is approved | EVALUATE when real data available |
| C6: Source code / specs | 2 months build + Qdrant | $0 (native indexing) | Negative — native is better | USE NATIVE |
| C7: Prior solutions | 0.5 months build | $0 (workspace indexed) | Negative | USE NATIVE |
| C8: Confluence KB | 2 months build + embedding | Migrate to repo markdown; CI publishes to Confluence | Positive — but migration is simpler and cheaper than MCP | MIGRATE content to repository markdown |
| C9: CMDB | 1 month build | Not available natively | Positive — genuine gap | BUILD if justified by use frequency |
| C10: Cross-team ADRs | 1 month build | Not available natively | Positive — genuine gap | BUILD if other teams adopt |

---

## Decision Drivers

1. **Engineering cost vs marginal value**: Each custom MCP server costs 1-2 months of engineering. Is the marginal context improvement worth diverting engineering from architecture work?
2. **Native coverage**: 7 of 10 content types are fully covered. Building custom infrastructure for them adds cost and complexity with zero benefit.
3. **Genuine gaps**: C8 (Confluence) is solvable by content migration to repository markdown. C9-C10 are the only areas where custom MCP adds new capability beyond native tooling.
4. **Operational sustainability**: Every custom MCP server requires monitoring, auth management, and maintenance — ongoing cost disproportionate to benefit if native alternatives exist.
5. **Reinvention risk**: Building a custom workspace indexer when Copilot already provides one is engineering waste — it will always be inferior to the vendor's first-party implementation.

---

## Preliminary Recommendation

!!! tip "Working Recommendation: Option B — Native + Targeted MCP"
    Rely on native toolchain capabilities for all currently-served content types (C1-C7). Migrate Confluence content (C8) to markdown files in the repository, published to Confluence and MkDocs portals via CI — this eliminates the Confluence MCP gap entirely. Build targeted MCP servers only for validated enterprise data gaps (C9-C10), and only when the specific use case has been demonstrated to justify the per-server engineering investment. Do not build a full custom pipeline that replicates native capabilities.

### Rationale

- 7 of 10 content types are fully served by native capabilities — no MCP needed
- Confluence (C8) is solvable by migrating content to repository markdown published via CI — no MCP needed
- The 2 remaining gaps (CMDB, cross-team ADRs) can be addressed incrementally with thin MCP adapters if validated
- The full pipeline approach (Option C) reinvents 6 native capabilities at a cost of 4-8 developer-months
- The 96.1% quality score was achieved entirely with native context — the baseline is already high

### Validation Criteria

Before building any MCP server, require:

1. **Usage frequency**: Will the AI access this data source more than 3 times per week?
2. **Manual alternative cost**: How many minutes does it take to manually find and paste the same information?
3. **Quality impact**: Has the lack of this data source caused a documented quality gap in AI outputs?
4. **Maintenance commitment**: Is there an owner committed to maintaining the MCP server for at least 12 months?

---

## Consequences

### If Option B is selected

**Positive:**

- Native capabilities continue to provide proven quality (96.1%)
- Engineering effort focused on genuine gaps, not reinventing existing features
- Incremental approach limits risk — each MCP server is validated before the next is built
- No disruption to current workflow

**Negative:**

- Enterprise data (C9-C10) remains inaccessible until targeted MCP servers are built (Confluence is addressed by content migration)
- The practice remains dependent on the toolchain vendor for workspace indexing quality

**Neutral:**

- This decision is revisitable — if enterprise data access becomes critical, Option B can evolve toward targeted servers without the waste of Option C's full pipeline

---

## Open Questions

1. What Confluence content should be prioritized for migration to repository markdown? (Determines the migration backlog for C8)
2. Does the CMDB contain data that is not already captured in `architecture/metadata/` YAML files? (Deduplication check for C9)
3. Are other architecture teams willing to share their ADR repositories via a federated index? (Prerequisite for C10)

---

## Links

- [Context Management Research](../research/context-management.md) — How native vs custom context injection drives the 208x cost difference
- [Platform Options](../platform-options.md) — How this decision composes with DD-02, DD-03, DD-04
- [DD-02: Injection Location](dd-02-injection-location.md) — Where the injection happens (workstation vs server)
