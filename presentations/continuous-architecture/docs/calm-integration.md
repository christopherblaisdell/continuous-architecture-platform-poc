# CALM Integration: Machine-Readable Architecture Topology

## Formalizing What We Already Model

The Continuous Architecture Platform already maintains rich architecture metadata: 13 YAML files describing services, domains, cross-service calls, data stores, events, actors, and PCI scope. But this metadata is **informal** — there is no schema validation, no cross-referencing, and no automated governance.

**CALM (Common Architecture Language Model)** is a FINOS open-source standard that provides exactly this: a JSON Schema-based specification for declaring architecture topology in a version-controlled, validatable format.

---

## What CALM Adds

``` mermaid
flowchart TD
    subgraph today ["Today (Informal Metadata)"]
        Y1[domains.yaml]
        Y2[cross-service-calls.yaml]
        Y3[data-stores.yaml]
        Y4[events.yaml]
        Y5[actors.yaml]
        Y6[pci.yaml]
    end

    subgraph calm ["With CALM (Formal Topology)"]
        C1[Unified Node Graph]
        C2[Typed Relationships]
        C3[Validatable Patterns]
        C4[Enforceable Controls]
    end

    today --> |"Migrate + Unify"| calm
    calm --> V[CI Validation]
    calm --> G[Auto-Generated Diagrams]
    calm --> I[Impact Analysis]

    style today fill:#ede7f6
    style calm fill:#e8f5e9
    style V fill:#5e35b1,color:#fff
    style G fill:#5e35b1,color:#fff
    style I fill:#5e35b1,color:#fff
```

---

## CALM in One Table

| CALM Concept | What It Models | Our Equivalent Today |
|-------------|---------------|---------------------|
| **Nodes** | Services, databases, actors, applications | Scattered across 5+ YAML files with no unified model |
| **Relationships** | REST calls, events, DB connections | `cross-service-calls.yaml` (REST only) + separate `events.yaml` |
| **Interfaces** | Endpoints, Kafka channels, JDBC connections | OpenAPI specs (endpoints only) — no interface registry |
| **Patterns** | Reusable architectural blueprints | Solution design template — not machine-validatable |
| **Controls** | Governance policies (PCI, data ownership, API-only access) | Manual PR review — no automated enforcement |

---

## What CALM Does NOT Replace

CALM is a **topology layer** — it models how things connect, not what they do or why.

| Artifact | Stays As-Is | Why |
|----------|:-----------:|-----|
| OpenAPI specs | Yes | CALM models topology; OpenAPI models API contracts |
| AsyncAPI specs | Yes | CALM references events; AsyncAPI defines schemas |
| Solution designs | Yes | Change lifecycle is orthogonal to topology |
| MADR decisions | Yes | Human judgment artifacts, not topology |
| Capability model | Yes | Business alignment, different axis |

---

## Why It Matters: Automated Governance

Today, architecture rules are enforced by **human reviewers reading PRs**. CALM enables CI-enforced governance:

| Rule | Enforcement Today | With CALM |
|------|:---:|:---:|
| No shared databases | PR review | CI rejects any DB node connected to 2+ services |
| PCI scope boundaries | Manual `pci.yaml` list | CALM control flags PCI data flows automatically |
| API-mediated access only | `copilot-instructions.md` rule | CI rejects direct JDBC between services |
| Data ownership boundaries | PR review | Formally declared and validated |

<div class="key-insight" markdown>
**CALM turns architecture rules into automated tests.** A PR that introduces a shared database connection fails CI — before any human reviewer needs to notice it.
</div>

---

## Phased Adoption

| Phase | Scope | Timeline | Outcome |
|-------|-------|----------|---------|
| **0: Pilot** | Model one bounded context (Operations domain) | 1-2 weeks | Prove CALM validation catches violations |
| **1: Full Topology** | Model all 19 services, 57 nodes, all relationships | 2-3 weeks | Single source of truth for system topology |
| **2: CI Integration** | CALM validation in GitHub Actions on every PR | 1-2 weeks | Automated governance enforcement |
| **3: Generator Evolution** | Portal generators read CALM topology instead of ad-hoc YAML | 3-4 weeks | Simpler, more accurate diagram generation |

The pilot is designed to prove value at minimal cost — model one domain, run one validation, decide whether to proceed.

---

## Impact on the Continuous Architecture Loop

CALM strengthens every step of the continuous architecture workflow:

| Step | Without CALM | With CALM |
|------|:---:|:---:|
| **INVESTIGATE** | Read multiple YAML files to understand topology | Query one CALM document for the full topology graph |
| **DESIGN** | Hope the AI reads the right metadata files | AI reads a canonical, validated topology model |
| **REVIEW** | Reviewers check rules manually | CI validates patterns and controls automatically |
| **PUBLISH** | Generators scrape 5+ YAML files | Generators traverse a formal graph model |
| **PROMOTE** | Manually verify what was built matches what was designed | Compare CALM topology snapshot before vs after |

---

## The Bigger Picture

CALM is the missing **formalization layer** between our informal metadata and our CI/CD pipeline:

``` mermaid
flowchart LR
    A[Architecture Ticket] --> B[AI-Assisted Design]
    B --> C[Updated CALM Topology\n+ OpenAPI Specs]
    C --> D[git push]
    D --> E[CI: CALM Validation\n+ Spec Linting]
    E --> F[Auto-Published Portal]
    F --> G[PROMOTE: Reconcile\ntopology vs reality]
    G --> C

    style B fill:#5e35b1,color:#fff
    style E fill:#e91e63,color:#fff
    style G fill:#ff8f00,color:#fff
```

<div class="key-insight" markdown>
**CALM completes the automation story.** Automated publishing eliminates the manual wiki step. The PROMOTE step eliminates the design-reality gap. CALM validation eliminates the manual governance step. Together, they make architecture truly continuous.
</div>

<div class="cta-box" markdown>

### Full technical plan

The detailed CALM integration plan — with file structures, CLI commands, and migration strategy — is available in the [architecture repository](https://github.com/christopherblaisdell/continuous-architecture-platform-poc-2/blob/main/docs/CALM-INTEGRATION-PLAN.md).

</div>

<div class="cta-box" markdown>

### What comes next?

[Roadmap: Six Phases to Full Platform](roadmap.md)

</div>
