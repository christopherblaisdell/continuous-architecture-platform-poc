---
tags:
  - roadmap
  - planning
  - calm
---

# Platform Roadmap

**Living Architecture Platform** &nbsp;|&nbsp; All foundational phases complete &nbsp;|&nbsp; Last updated: 2026-03-11

> The Continuous Architecture Platform replaces point-in-time architecture documentation with a living, interconnected knowledge base that grows with every ticket.

---

## Completed Phases

All 7 foundational phases are **COMPLETE**:

| Phase | Deliverables | Portal Links |
|-------|-------------|--------------|
| **Phase 0: Data Isolation** | Corporate identifiers removed, audit script enforced | [Platform Operations](platform-operations.md) |
| **Phase 1: Foundation** | Solution design workflow, metadata backbone, branch rules, 34 L2 capabilities | [Business Capabilities](capabilities/index.md) &middot; [Design Standards](standards/index.md) |
| **Phase 2: Portal Publishing** | Solution, capability, and ticket page generators with cross-links | [Solutions](solutions/index.md) &middot; [Tickets](tickets/index.md) |
| **Phase 3: AI Integration** | AI agent produces capability-mapped solutions on dedicated branches | [Solution Design Template](standards/solution-design/index.md) |
| **Phase 4: Ticketing** | Vikunja deployed, ticket sync, MCP server for AI access | [Tickets](tickets/index.md) |
| **Phase 5: Advanced Features** | Capability health dashboard, related solutions, branch status sync | [Business Capabilities](capabilities/index.md) |
| **Phase 6: Confluence Publishing** | Read-only Confluence mirror, mark CLI, 4-layer drift prevention | [Platform Operations](platform-operations.md) |

---

## Next: CALM — Automated Architecture Governance { #calm }

!!! tip "Top Priority Initiative"
    CALM is the next major evolution of the platform — adding machine-enforced architecture governance to CI/CD.

### What is CALM?

[CALM (Common Architecture Language Model)](https://github.com/architecture-as-code/calm) is a JSON Schema-based specification from the Architecture as Code Foundation for declaring architecture topology — nodes, relationships, interfaces, and data flows — in a machine-readable, version-controllable, validatable format.

### Key Design Decision: CALM is Auto-Generated

**Architects do not write CALM.** CALM documents are automatically generated from the artifacts architects already maintain:

```
Architect edits (what they know today)
  ├── OpenAPI specs           → architecture/specs/*.yaml
  ├── AsyncAPI specs          → architecture/events/*.yaml
  ├── Metadata YAML           → architecture/metadata/*.yaml
  │     ├── domains.yaml
  │     ├── cross-service-calls.yaml
  │     ├── data-stores.yaml
  │     ├── events.yaml
  │     └── actors.yaml
  │
  ▼  Bridge scripts (automated)
CALM topology documents
  │
  ▼  calm validate (CI)
Architecture rule enforcement
  ├── No shared databases
  ├── API-only cross-service access
  ├── PCI scope tracking
  ├── Team ownership required
  └── Event schema required
```

**Why auto-generate instead of hand-author?**

1. **No new format to learn** — architects stay in YAML and OpenAPI specs
2. **Validation is the value, not authoring** — CALM patterns catch violations regardless of how CALM was produced
3. **No drift by construction** — single source of truth feeds both portal generators and CALM topology
4. **Incremental adoption** — existing workflows unchanged; CALM is a CI-layer addition

### What CALM Delivers

| Capability | Today (Manual) | With CALM (Automated) |
|-----------|---------------|----------------------|
| No shared databases | PR reviewer reads YAML | CI rejects PRs that connect a DB to multiple services |
| API-only cross-service access | Rule text in instructions | CI validates no JDBC relationships between services |
| PCI scope tracking | Manual list in pci.yaml | CALM decorator flags PCI-scoped nodes and relationships |
| Impact analysis | Architect reads cross-service-calls.yaml | Graph traversal: all upstream/downstream dependencies |
| Architecture drift | Undetected | CALM topology compared against running system |
| Topology visualization | Static PlantUML | Interactive system map from CALM graph |

### Rollout Phases

| Phase | Goal | Key Deliverable |
|-------|------|----------------|
| **0: Pilot** | Prove value on 1 domain | Model Operations domain, validate in CI |
| **1: Full Topology** | All 22 services (~57 nodes) | System-level CALM document, YAML-CALM bridge |
| **2: Generator Integration** | Portal consumes CALM | Interactive topology map, dependency matrix |
| **3: Governance Automation** | 6+ CI-enforced rules | Patterns, controls, governance dashboard |
| **4: Solution Design Integration** | Topology changes per ticket | CALM diffs in capability changelog |
| **5: Advanced** | Blast radius, drift detection | Architecture intelligence layer |

**Related:** [Microservices](microservices/index.md) (22 services to model) &middot; [Event Catalog](events/index.md) (event topology) &middot; [Business Capabilities](capabilities/index.md) (complementary axis)

---

## Future Initiatives

### HIGH Priority

| Initiative | Status | Summary | Related Pages |
|-----------|--------|---------|---------------|
| **Test Methodology** | Proposed | TDD/BDD practice, 80% line coverage, contract testing, automated regression gates | [Microservices](microservices/index.md) (services under test) |
| **Fix Deploy Failures** | Backlog | Audit and fix CI/CD pipeline failures — prerequisite for reliable delivery | [Platform Operations](platform-operations.md) |
| **Azure Implementation** | Draft | Full NovaTrek microservices in Azure with IaC, ephemeral environments, deep links | [Service Catalog](services/index.md) &middot; all [Microservice Pages](microservices/index.md) |

### MEDIUM Priority

| Initiative | Status | Summary | Related Pages |
|-----------|--------|---------|---------------|
| **Separation of Concerns** | Proposed | Extract metadata from generators to YAML; CI handles generation | [Platform Operations](platform-operations.md) |
| **Figma Wireframes** | Proposed | Embed Figma wireframes in application pages | [Applications](applications/index.md) |
| **Event Catalog Expansion** | Proposed | Formalize domain events with AsyncAPI specs and portal pages | [Event Catalog](events/index.md) |
| **Presentation Site** | Draft | Executive pitch deck as MkDocs Material site | |

### LOW Priority

| Initiative | Status | Summary | Related Pages |
|-----------|--------|---------|---------------|
| **Root Folder Reorganization** | Proposed | Reduce root clutter to intuitive subfolder hierarchy | |
| **Frontend Applications** | Draft | Extend 3 application pages | [Applications](applications/index.md) |

---

## Cross-Linking Philosophy

Every artifact in this portal connects to every related artifact:

```
Microservice Page ←→ Swagger UI ←→ OpenAPI Spec
       ↕                                ↕
  Solution Page ←→ Capability Page ←→ Ticket Page
       ↕                                ↕
   ADR Decision ←→ Service Catalog ←→ Event Catalog
       ↕                                ↕
  Azure Portal  ←→   Source Code   ←→ CI/CD Pipeline
```

- **Microservice pages** link to: Swagger UI, OpenAPI spec download, Azure Portal, CI/CD pipeline, source code, technology stack, impacting solutions, capability IDs
- **Swagger UI pages** link back to: microservice deep-dive page, service catalog, portal home, OpenAPI spec download
- **Solution pages** link to: impacted services, capability changelong entries, related solutions
- **Capability pages** link to: timeline of solutions, L3 capabilities, owning services
- **Ticket pages** link to: solution designs, affected services, capability mappings

---

## Architecture Review Checklist

Applied during PR review of every solution design:

- [ ] All impacted services identified with specific API/schema changes
- [ ] MADR ADRs created for cross-boundary or data-semantic decisions
- [ ] Impact assessments focus on WHAT changes (not HOW)
- [ ] User stories written from user perspective (no technical details)
- [ ] Capability IDs declared in master document header
- [ ] `capability-changelog.yaml` entry drafted
- [ ] Backward compatibility addressed for all API changes
- [ ] Cross-service data ownership boundaries respected

---

## Success Criteria

An architect picking up a new ticket should be able to:

1. Open the **capability page** in the portal and see a timeline of every prior solution
2. Click through to any **solution design** to understand what was decided and why
3. See which **ADRs** shaped the domain
4. Read the **microservice page** with all impacting solutions cross-linked
5. Open **Swagger UI** and click back to the architecture deep-dive
6. Find the same content in **Confluence** — always in sync, never diverged
7. Start their new solution with **full context** — not from a blank page, but from accumulated knowledge
