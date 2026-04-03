# DD-02: Content Injection Location

## Workstation vs Server

| | |
|-----------|-------|
| **Status** | Under Evaluation |
| **Date** | 2026-04-03 |
| **Category** | Architecture |
| **Maps to** | DP-19 (Hybrid MCP Location), DP-01 (Buy vs Build) |
| **Depends on** | DD-01 (Content Injection Strategy) |

---

## Context and Problem Statement

Once the practice determines **what** to inject (DD-01), the next question is **where** the injection happens. Content injection can occur at three architectural locations:

1. **Developer workstation** — the AI tool reads local files, local MCP servers, and workspace content directly from the developer's machine
2. **Server** — a centralized server hosts MCP services, RAG pipelines, or AI orchestration that provides context remotely
3. **Hybrid** — local for workspace-scoped content, server for enterprise-scoped content

This decision affects security (where does enterprise data flow?), latency (network round-trips vs local file reads), cost (infrastructure overhead), multi-team scalability (do teams share a context layer?), and offline capability.

---

## Current State

Today, all content injection happens on the developer workstation:

| Injection Point | Location | Mechanism |
|----------------|----------|-----------|
| Architecture standards | Local | `copilot-instructions.md` loaded by IDE |
| Domain model metadata | Local | `architecture/metadata/*.yaml` read from filesystem |
| OpenAPI specs | Local | `architecture/specs/*.yaml` read from filesystem |
| Source code | Local | Java files read from filesystem |
| Tickets | Local | Vikunja MCP server running on localhost |
| Mock tools (JIRA, Elastic, GitLab) | Local | Python scripts reading local JSON files |
| Workspace indexing | Server (Copilot) | Copilot indexes workspace server-side, retrieves on demand |

The one exception is Copilot's workspace indexing, which processes files server-side — but this is transparent to the developer and managed entirely by the vendor.

---

## Options

### Option A: Workstation Only

**Description:** All content injection stays on the developer workstation. The AI reads local files, local MCP servers, and the toolchain's native indexing. No enterprise servers are built for context injection.

**Architecture:**

```
┌──────────────────────────────────────────┐
│  Developer Workstation                   │
│                                          │
│  ┌────────────────────────────────────┐  │
│  │  AI Toolchain                      │  │
│  │  - Native workspace indexing       │  │
│  │  - Instructions (local files)      │  │
│  │  - File reads (local filesystem)   │  │
│  └──────────┬─────────────────────────┘  │
│             │                            │
│  ┌──────────▼──────────┐                 │
│  │  Local MCP Servers  │                 │
│  │  - Vikunja tickets  │                 │
│  │  - Mock tools       │                 │
│  └─────────────────────┘                 │
│                                          │
│  Enterprise data accessed manually       │
│  (browser, copy-paste, manual export)    │
└──────────────────────────────────────────┘
```

**Evaluation:**

| Criterion | Assessment |
|-----------|-----------|
| **Latency** | Excellent — all reads are local filesystem or localhost |
| **Security** | Strong — enterprise data never leaves the developer's machine (except through the AI vendor's cloud processing) |
| **Infrastructure cost** | Zero — no servers to provision |
| **Operational complexity** | Minimal — local MCP servers are developer-managed |
| **Multi-team scalability** | Poor — each developer maintains their own workspace copy; no shared context |
| **Offline capability** | Full — all context available without network |
| **Enterprise data access** | None — enterprise systems require manual interaction |
| **Context freshness** | Depends on developer pulling latest workspace changes |

**Best for:** Solo practitioners or small teams working within a self-contained workspace.

---

### Option B: Workstation + Selective Server (Hybrid)

**Description:** Workstation handles all workspace-scoped content (specs, code, metadata, tickets) using native capabilities. Confluence content is migrated to repository markdown and published via CI, making it natively indexable. A small number of server-hosted MCP services provide access to remaining enterprise data sources that cannot be replicated locally (CMDB, cross-team ADRs).

**Architecture:**

```
┌──────────────────────────────────────────┐
│  Developer Workstation                   │
│                                          │
│  ┌────────────────────────────────────┐  │
│  │  AI Toolchain                      │  │
│  │  - Native workspace indexing       │  │
│  │  - Instructions (local)            │  │
│  │  - MCP client (local + remote)     │  │
│  └──────┬──────────────┬──────────────┘  │
│         │              │                 │
│  ┌──────▼──────┐       │                 │
│  │ Local MCP   │       │                 │
│  │ - Vikunja   │       │                 │
│  └─────────────┘       │                 │
└────────────────────────┼─────────────────┘
                         │ HTTPS (MCP)
                         │ Auth: Entra ID
┌────────────────────────▼─────────────────┐
│  Azure (Selective MCP Services)          │
│  ┌─────────────────────────────────────┐ │
│  │  CMDB Lookup MCP                    │ │
│  │  Cross-Team ADR Index MCP           │ │
│  └─────────────────────────────────────┘ │
│  ┌─────────────────────────────────────┐ │
│  │  Entra ID (auth) + Key Vault       │ │
│  │  Azure Monitor (usage tracking)     │ │
│  └─────────────────────────────────────┘ │
└──────────────────────────────────────────┘
```

**Evaluation:**

| Criterion | Assessment |
|-----------|-----------|
| **Latency** | Good — workspace reads are local; enterprise reads add network round-trip (~50-200ms per MCP call) |
| **Security** | Moderate — enterprise data flows through centralized, RBAC-controlled servers; network boundary exists |
| **Infrastructure cost** | Low-moderate — 2-3 lightweight MCP servers on Azure (~$50-150/month shared) |
| **Operational complexity** | Moderate — server MCP services need monitoring, auth management, uptime |
| **Multi-team scalability** | Good — multiple teams share the same server-side MCP services |
| **Offline capability** | Degraded — workspace context available offline; enterprise MCP calls fail gracefully |
| **Enterprise data access** | Targeted — specific high-value sources only |
| **Context freshness** | Server-side: real-time API calls to enterprise systems; local: pull-based |

**Best for:** Teams that have validated specific enterprise data needs (DD-01, Option B) and have engineering capacity to build and maintain a small number of MCP services.

---

### Option C: Server-Hosted AI Orchestration

**Description:** The server owns the context layer. A centralized AI orchestration service on Azure AI Foundry manages all context injection — workspace content is synced to the server, enterprise data is pre-indexed in a vector store, and the AI agent runs server-side. The developer workstation is a thin client or the server provides context to the local agent via comprehensive MCP services.

**Architecture:**

```
┌──────────────────────────────────────────┐
│  Developer Workstation (Thin Client)     │
│  ┌────────────────────────────────────┐  │
│  │  AI Toolchain (or browser client)  │  │
│  │  - Sends prompts to server         │  │
│  │  - Displays results                │  │
│  └──────────┬─────────────────────────┘  │
└─────────────┼────────────────────────────┘
              │ HTTPS
┌─────────────▼────────────────────────────┐
│  Azure AI Foundry (Full Server)          │
│  ┌─────────────────────────────────────┐ │
│  │  AI Orchestrator Agent              │ │
│  │  - Custom system prompt             │ │
│  │  - RAG pipeline                     │ │
│  │  - All context injection            │ │
│  │  - Full tool calling                │ │
│  └──────────┬──────────────────────────┘ │
│             │                            │
│  ┌──────────▼──────────────────────────┐ │
│  │  Context Layer                      │ │
│  │  - Vector DB (workspace + Confluence│ │
│  │  - CMDB integration                 │ │
│  │  - Cross-team ADR index             │ │
│  │  - Production log aggregator        │ │
│  │  - Workspace sync (git clone)       │ │
│  └─────────────────────────────────────┘ │
│                                          │
│  ┌─────────────────────────────────────┐ │
│  │  Infrastructure                     │ │
│  │  - Azure AI Search / Qdrant         │ │
│  │  - Cosmos DB (state management)     │ │
│  │  - Entra ID + RBAC                  │ │
│  │  - Azure Monitor                    │ │
│  └─────────────────────────────────────┘ │
└──────────────────────────────────────────┘
```

**Evaluation:**

| Criterion | Assessment |
|-----------|-----------|
| **Latency** | Poor — every interaction goes through network; agent execution on server adds round-trips |
| **Security** | Complex — enterprise data centralized (good); developer prompts flow to server (DLP concern); full RBAC possible |
| **Infrastructure cost** | High — $150-350/month per seat; Azure AI Foundry compute, vector DB, App Service |
| **Operational complexity** | High — full application stack to monitor, scale, patch |
| **Multi-team scalability** | Excellent — centralized platform serves all teams with shared indexing |
| **Offline capability** | None — requires network connectivity for all operations |
| **Enterprise data access** | Comprehensive — all data sources indexed centrally |
| **Context freshness** | Centralized sync — can be near-real-time but adds pipeline complexity |

**Best for:** Large organizations with dedicated platform engineering teams, extensive enterprise data integration requirements, and the engineering budget to build and maintain a custom AI platform.

---

## Comparative Analysis

| Factor | Option A: Workstation | Option B: Hybrid | Option C: Server |
|--------|:---:|:---:|:---:|
| Latency | Excellent | Good | Poor |
| Security simplicity | High | Moderate | Complex |
| Infrastructure cost | $0 | $50-150/mo | $500-1,500/mo |
| Engineering investment | 0 months | 2-4 months | 6-12 months |
| Operational burden (ongoing) | None | 0.25 FTE | 1-2 FTE |
| Multi-team scalability | Poor | Good | Excellent |
| Offline capability | Full | Degraded | None |
| Enterprise data breadth | Manual only | Targeted | Comprehensive |
| Risk | Low | Moderate | High |

---

## Decision Drivers

1. **Current team size**: For a practice with 1-5 architects, workstation-only or hybrid is sufficient. Server-first is over-engineered.
2. **Enterprise data urgency**: If architects rarely need CMDB or cross-team ADR data during AI sessions, server infrastructure is premature. Confluence content should be migrated to repository markdown rather than accessed via MCP.
3. **Security posture**: Server-side centralizes governance but adds attack surface. Workstation-side reduces data exposure but limits sharing.
4. **Engineering capacity**: Server options divert engineering effort from architecture work to platform engineering.
5. **Offline requirement**: Field architects or those on unreliable networks need local-first operation.

---

## Preliminary Recommendation

!!! tip "Working Recommendation: Option A now, evolve to Option B when enterprise data needs are validated"
    Start with workstation-only (proven, zero infrastructure). When DD-01 validates specific enterprise data gaps, build targeted server-side MCP services incrementally (Option B). Do not build a server-first platform (Option C) unless the organization has 20+ architects with deep enterprise data integration requirements.

### Rationale

- The current workstation-only approach delivers 96.1% quality — the baseline is already high
- Enterprise data access needs are not yet validated with usage data
- The hybrid path (A to B) is incremental — each MCP server addition is a small, reversible investment
- The server-first path (A to C) requires a large upfront commitment before any value is delivered

### Evolution Path

```
Phase 1 (Now):    Option A — workstation only
Phase 2 (3-6mo):  Option B — add first server MCP when usage data validates the need
Phase 3 (12mo+):  Option B+ — expand server MCP services based on demonstrated value
Phase N (if ever): Option C — only if 20+ architects across multiple teams need shared orchestration
```

---

## Consequences

### If Option A is selected (with path to B)

**Positive:**

- Zero infrastructure cost or operational burden today
- Proven quality (96.1%) with zero server dependencies
- Engineering effort stays focused on architecture work
- Incremental evolution path preserves optionality

**Negative:**

- Enterprise data (CMDB) requires manual access until MCP servers are built; Confluence content is addressable by migrating to repository markdown
- No shared context layer across teams
- Depends on the toolchain vendor for workspace indexing quality

**Neutral:**

- This is not a permanent decision — it is a starting position with a defined evolution path

---

## Links

- [DD-01: Content Injection Strategy](dd-01-content-injection.md) — What context to inject (prerequisite for location decision)
- [DD-03: Billing Model](dd-03-billing-model.md) — Server-side adds infrastructure cost that affects billing analysis
- [Platform Options](../platform-options.md) — How location choice maps to platform options
