# Your Role as Solution Architect

This page defines what a solution architect does at NovaTrek Adventures — and equally important, what falls outside the role.

---

## What You Do

As a solution architect, you are responsible for the **structural integrity** of the NovaTrek platform. Your work shapes how services interact, how data flows, and how the system evolves.

### Core Responsibilities

| Responsibility | Description | Key Artifacts |
|---------------|-------------|---------------|
| **Triage tickets** | Assess whether a ticket has architectural relevance — does it cross service boundaries, change data semantics, or affect integration patterns? | Ticket annotations in `tickets.yaml` |
| **Design solutions** | Produce complete solution designs for architecturally significant tickets, including impact assessments, decisions, risks, and user stories | Solution folders in `architecture/solutions/` |
| **Record decisions** | Write MADR-formatted architecture decision records for any choice that crosses service boundaries or changes data semantics | ADRs in `decisions/` |
| **Maintain API contracts** | Author and evolve OpenAPI specs and AsyncAPI event schemas as the machine-readable contracts between services | Specs in `architecture/specs/` and `architecture/events/` |
| **Model the architecture** | Maintain the 15 metadata YAML files that define domains, services, data stores, actors, events, capabilities, and cross-service calls | YAML files in `architecture/metadata/` |
| **Create diagrams** | Author C4 diagrams (System Context, Container, Component) and sequence diagrams using PlantUML | PUML files in `architecture/diagrams/` |
| **Design wireframes** | Create UI/UX wireframes for guest-facing and operations screens using Excalidraw | `.excalidraw` files in `architecture/wireframes/` |
| **Write guidance** | Produce implementation guidance documents that help developers understand HOW to implement approved designs | Guidance docs in solution `g.guidance/` folders |
| **Assess quality** | Evaluate solutions against ISO 25010 quality attributes — reliability, maintainability, security, performance, compatibility | Quality analysis in solution designs |
| **Identify risks** | Flag architectural risks, anti-patterns, and technical debt in proposed and existing designs | Risk registers in solution `r.risks/` folders |

### What You Produce

Every solution design creates a structured folder with these deliverables:

```
architecture/solutions/_NTK-XXXXX-slug/
  NTK-XXXXX-solution-design.md          # Master document
  1.requirements/                        # Ticket analysis
  2.analysis/                            # Plain-language explanation
  3.solution/
    a.assumptions/                       # What is assumed true
    c.capabilities/capabilities.md       # Capability mappings
    d.decisions/decisions.md             # MADR decisions
    g.guidance/                          # Implementation advice (optional)
    i.impacts/                           # Per-service impact assessments
    r.risks/                             # Risk register
    u.user.stories/                      # User stories with acceptance criteria
```

---

## What You Do NOT Do

This boundary is critical. Crossing it creates confusion about ownership and accountability.

| NOT Your Responsibility | Who Owns It | Why |
|------------------------|-------------|-----|
| Debug code or fix bugs | Software Developer | Architects design; developers implement and troubleshoot |
| Write production code | Software Developer | Solution designs describe WHAT changes, not the code itself |
| Execute or reproduce issues | Software Developer / QA | Architects analyze from logs, specs, and source — not by running services |
| Deploy or configure infrastructure | Platform Engineer | Architects document deployment requirements; engineers implement them |
| Perform code reviews on implementation PRs | Tech Lead / Senior Developer | Architects review API contract PRs, not implementation details |
| Write unit tests | Software Developer | Architects specify acceptance criteria; developers write tests (see [Testing Guide](testing-guide.md)) |

---

## Content Separation

Different document types serve different purposes. Mixing them creates confusion.

| Document Type | Contents | Does NOT Contain |
|---------------|----------|-----------------|
| **Impact assessment** | WHAT changes architecturally — API contracts, data models, integration points | Implementation code, deployment steps, timelines |
| **Guidance** | HOW to implement — code patterns, configuration examples, migration steps | Business justification, architectural rationale |
| **User stories** | WHO benefits and WHY — user perspective, acceptance criteria | Technical implementation details, code references |
| **Decision (ADR)** | WHY this approach — context, options analysis, trade-offs | Code samples, deployment procedures |
| **Investigation** | WHAT was found — evidence from logs, source code, specs | Proposed solutions (those go in the solution design) |
| **Simple explanation** | Plain-language summary for non-technical stakeholders | Jargon, code snippets, API references |
| **Assumptions** | What is assumed true but not verified — dependencies, constraints | Decisions (assumptions inform decisions; they are not decisions) |

---

## Working with Developers

The architect-developer relationship is collaborative, not hierarchical.

### Handoff Points

1. **Architect produces a solution design** — the developer receives a clear picture of what needs to change, why, and what the acceptance criteria are
2. **Developer proposes API contract changes** — when implementation reveals gaps in the OpenAPI spec, the developer submits a PR. The architect reviews and approves.
3. **Architect writes guidance** — optional implementation advice in `g.guidance/` folders. Developers may follow or propose alternatives.
4. **Developer writes tests from user stories** — acceptance criteria in user stories drive BDD scenarios (see [Testing Guide](testing-guide.md))

### Shared Ownership

Some artifacts have dual ownership:

| Artifact | Primary Owner | Secondary Owner |
|----------|--------------|-----------------|
| OpenAPI specs | Solution Architect | Developer (via PR for implementation-discovered gaps) |
| AsyncAPI event specs | Solution Architect | Developer (via PR) |
| [`config/test-standards.yaml`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/config/test-standards.yaml) | Solution Architect | Developer (proposes threshold changes) |
| Database migrations (Flyway) | Developer | Architect (designs schema in `data-stores.yaml`) |

---

## How to Get Started

1. **Read the [Domain Model](domain-model.md)** — understand the NovaTrek business domain, the 19 services, and how they interact
2. **Study an existing solution** — read through [NTK-10005 Wristband RFID](../solutions/_NTK-10005-wristband-rfid-field.md) as a complete worked example
3. **Learn the [Solution Design Workflow](solution-design-workflow.md)** — the step-by-step process for creating your first design
4. **Familiarize yourself with the [Quick Reference](quick-reference.md)** — commands, file locations, and naming conventions
