# Shared Workspace: AI Sees What the Architect Sees

## The Secret to 96.1% Quality: Full Context

The AI doesn't hallucinate when it can **read the actual source material**. The key architectural decision in this platform is simple: put everything in the workspace.

---

## What Lives in the Workspace

The architecture workspace is a git repository containing every artifact an architect needs:

| Artifact Type | Count | Purpose |
|--------------|:-----:|---------|
| OpenAPI specs | 19 | Authoritative API contracts for every microservice |
| Architecture Decision Records | 11 | Global decision log with rationale and consequences |
| Service architecture pages | 6 | Living baselines per service (current state, integrations, decisions) |
| Java source code | 8 files | Key service implementations for analysis |
| Mock tool scripts | 3 | JIRA, Elasticsearch, GitLab simulation (local JSON, no network) |
| Architecture standards | 4 | arc42 template, MADR format, C4 model guide, ISO 25010 tree |
| copilot-instructions.md | 1 | 500+ lines of domain knowledge loaded into every AI session |

---

## The Instructions File: 500+ Lines of Domain Knowledge

The `copilot-instructions.md` file is loaded automatically into every AI session. It contains:

- **Role definition** — the AI operates as a Solution Architect, not a developer
- **Domain model** — 19 services across 9 domains with bounded context rules
- **Data ownership** — which service owns which data entities, and who has read access
- **Mock tool commands** — exact syntax for running JIRA, Elastic, and GitLab tools
- **Architecture standards** — MADR format, C4 notation, arc42 sections, ISO 25010 attributes
- **Anti-pattern checklist** — 8 common patterns to flag (shared databases, entity replacement, unsafe defaults, etc.)
- **Document formatting rules** — no emojis, no placeholder content, present tense for current state
- **Content separation policy** — what goes in an ADR vs an impact assessment vs guidance

!!! info "Why This Works"
    When the AI analyzes a ticket, it doesn't guess what services exist or how they interact. It reads the actual OpenAPI specs. When it creates an ADR, it follows the MADR template from the workspace. When it identifies anti-patterns, it checks against the documented checklist. **The quality comes from context, not from the model being "smarter."**

---

## Evidence: How Context Drove Quality

### Scenario 3: Production Investigation

The AI was investigating a guide schedule overwrite bug. Here's what it read from the workspace:

1. **Elasticsearch logs** (via mock tool) — found 4 ERROR entries with timestamps and trace IDs
2. **Java source code** (`SchedulingService.java`) — identified `save(incoming)` full-entity replacement at a specific line number
3. **GitLab MR-5001** (via mock tool) — found a previously rejected fix attempt and analyzed why it was insufficient
4. **OpenAPI spec** (`svc-scheduling-orchestrator.yaml`) — verified the `PUT` endpoint lacked optimistic locking

**Result:** 100% quality score. The AI traced the problem from production symptoms through code to a root cause, citing specific lines and log entries — because all of that evidence was in the workspace.

### Scenario 5: Cross-Service Design

The AI designed an unregistered guest self check-in flow spanning 6 services. It identified:

- A stub controller in `CheckInController.java` (specific line)
- A missing email field requirement in `GuestService.java` (specific line)
- A missing `confirmation_code` field in the reservations API spec
- Bounded context violations that would occur if services shared databases

All of this came from **reading workspace files** — not from prior training data or guesswork.

---

## The Flywheel Effect

Here's why a shared workspace keeps getting more valuable:

``` mermaid
flowchart TD
    A[Project 1 produces artifacts] --> B[Artifacts added to workspace]
    B --> C[AI context gets richer]
    C --> D[Project 2 produces better artifacts]
    D --> B

    style A fill:#e0f2f1
    style B fill:#00897b,color:#fff
    style C fill:#ff8f00,color:#fff
    style D fill:#e0f2f1
```

- After **Project 1**: 11 ADRs, 6 service pages, 19 specs in the workspace
- After **Project 5**: 20+ ADRs, more service pages, updated specs, richer decision history
- After **Project 20**: A comprehensive architecture knowledge base that informs every new design

And with Copilot's **fixed pricing**, richer context costs nothing extra. The AI reads more files, analyzes more specs, cross-references more decisions — all for $39/month.

!!! warning "This Is Impossible with Confluence-First Authoring"
    If architecture designs live in Confluence, the AI cannot read them during a design session. The architect must manually copy-paste relevant context. The workspace-first approach eliminates this friction entirely — the AI reads everything automatically.

---

## Comparison: Workspace-First vs Confluence-First

| Capability | Workspace-First | Confluence-First |
|-----------|:---:|:---:|
| AI reads previous designs | Automatic | Manual copy-paste |
| AI reads API specs | Automatic | Not available |
| AI reads source code | Automatic | Not available |
| AI reads decision history | Automatic | Manual copy-paste |
| Version-controlled changes | Yes (git) | Limited (page history) |
| Pull request reviews | Yes | No |
| Cross-reference accuracy | High (real files) | Low (stale links) |
| Context cost (per-token models) | Grows with workspace | Grows with copy-paste |
| Context cost (Copilot) | **$0** | **$0** (but less context available) |

<div class="cta-box" markdown>

### Why Markdown specifically?

[Markdown-First: Write Once, Publish Everywhere](markdown-first.md)

</div>
