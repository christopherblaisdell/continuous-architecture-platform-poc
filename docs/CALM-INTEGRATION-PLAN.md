# CALM Integration Plan — Continuous Architecture Platform

| | |
|-----------|-------|
| **Author** | Christopher Blaisdell (Solution Architect) |
| **Date** | 2026-03-10 |
| **Status** | Draft |
| **Purpose** | Detailed plan for incorporating CALM (Common Architecture Language Model) into the NovaTrek Adventures architecture practice |
| **Prior Art** | `architecture/reminders/CALM-EVALUATION.md` (deferred evaluation from 2026-03-06) |

---

## 1. Executive Summary

The Continuous Architecture Platform already implements a sophisticated architecture-as-code practice: 13 YAML metadata files, 7 Python generators, OpenAPI/AsyncAPI specs, solution designs with capability rollup, and a portal with cross-linked artifacts. This foundation is strong, but it lacks a **formal topology layer** — there is no machine-readable definition of how services, databases, actors, and events connect at the system level.

CALM (Common Architecture Language Model) fills this gap. It provides a JSON Schema-based specification for declaring architecture topology — nodes, relationships, interfaces, and data flows — in a version-controlled, validatable format. Rather than replacing what we have, CALM **formalizes what we already model informally** across `domains.yaml`, `cross-service-calls.yaml`, `data-stores.yaml`, `events.yaml`, and `actors.yaml`.

This document lays out a phased plan to adopt CALM, mapping each phase to concrete deliverables, risk mitigation, and measurable outcomes.

---

## 2. What CALM Is (and Is Not)

### What CALM Provides

| Concept | Description | Our Equivalent Today |
|---------|-------------|---------------------|
| **Nodes** | Typed architectural building blocks (services, databases, people, systems) | Implicit in `domains.yaml`, `data-stores.yaml`, `actors.yaml` — no unified model |
| **Relationships** | Typed connections between nodes (`interacts`, `connects`, `deployed-in`, `composed-of`) | `cross-service-calls.yaml` covers synchronous REST only; events in `events.yaml` are separate |
| **Interfaces** | Declared integration points (host-port, URL, path, OAuth audience) | OpenAPI specs define endpoints; no formal interface registry |
| **Patterns** | Reusable architectural blueprints written as JSON Schema | Solution design template (`3.solution/` folder structure) — not machine-validatable |
| **Controls** | Governance policies linked to compliance frameworks (NIST, ISO 27001) | Manual review checklist in PR template |
| **Standards** | Organizational extensions to core CALM schemas | `copilot-instructions.md` rules + PR template — human-enforced |
| **Timelines** | Versioned architecture snapshots tracking evolution | `capability-changelog.yaml` — capability-scoped only, not topology-scoped |
| **Decorators** | Cross-cutting metadata (deployment, security, business context) | `pci.yaml` for PCI scope — no general decorator model |

### What CALM Does Not Replace

| Artifact | Stays As-Is | Reason |
|----------|-------------|--------|
| OpenAPI specs | Yes | CALM models topology; OpenAPI models API contracts. They are complementary |
| AsyncAPI specs | Yes | CALM references event interfaces; AsyncAPI defines schemas and channels |
| Solution designs | Yes | CALM does not prescribe the solution design lifecycle — our folder structure and content separation rules remain |
| Capability model | Yes | CALM is topology; capabilities are business alignment. Different axes |
| MADR decisions | Yes | Architectural decisions are human judgment artifacts, not topology |
| Wireframes | Yes | UI design is orthogonal to system topology |

### The Relationship

```
                    CALM Topology Layer (NEW)
                    ├── Nodes (services, DBs, actors, apps)
                    ├── Relationships (REST, events, DB connections)
                    ├── Interfaces (endpoints, Kafka channels, JDBC)
                    └── Controls (PCI, auth, data ownership)
                         │
        ┌────────────────┼────────────────┐
        │                │                │
  OpenAPI Specs    AsyncAPI Specs    Solution Designs
  (API contracts)  (Event schemas)   (Change lifecycle)
        │                │                │
        └────────────────┼────────────────┘
                         │
                  Portal Generators
                  (merge topology + contracts + solutions → pages)
```

---

## 3. Strategic Value Assessment

### 3.1 Problems CALM Solves

**Problem 1: Fragmented Topology**

Today, NovaTrek's system topology is scattered across 5+ YAML files with no cross-referencing or validation. A developer adding a new cross-service call to `cross-service-calls.yaml` gets no feedback if the target service or endpoint does not exist in specs. CALM unifies nodes, relationships, and interfaces into a single validatable document.

**Problem 2: No Automated Governance**

Architecture rules (data ownership boundaries, no shared databases, PCI scope) are enforced entirely by human review in PRs. CALM controls and patterns enable CI-enforced governance — a PR that introduces a direct database connection between services can be automatically rejected.

**Problem 3: No Architecture Drift Detection**

There is no mechanism to detect when the running system diverges from the documented architecture. CALM's validation layer can compare the declared topology against observed reality (via decorator-attached deployment metadata).

**Problem 4: Manual Diagram Maintenance**

The `generate-microservice-pages.py` script (3,400 lines) manually constructs sequence diagrams from OpenAPI specs and cross-service-call metadata. CALM's topology data could simplify this by providing a canonical graph to traverse.

**Problem 5: Solution Impact Prediction**

When a new ticket arrives, there is no way to automatically identify which services, relationships, and data flows will be affected. CALM's topology graph enables graph-based impact analysis: "If we change svc-check-in's interface, which upstream callers are affected?"

### 3.2 Risks of CALM Adoption

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Schema migration breaks existing generators | Medium | High | Parallel adoption — generators read both CALM and legacy YAML during transition |
| CALM tooling immaturity (currently v1.2+) | Low | Medium | Pin CLI version; contribute upstream if needed |
| Learning curve for JSON Schema pattern authoring | Medium | Medium | Provide NovaTrek-specific templates; document patterns in portal |
| Over-engineering — CALM adds complexity without proportional value | Medium | High | Phase 0 (pilot) proves value before committing to full migration |
| Maintenance burden of keeping CALM documents in sync with OpenAPI/AsyncAPI | Medium | Medium | Automate with generators that read specs and produce CALM topology |

---

## 4. Current State Mapping

Before building anything new, map existing metadata to CALM concepts:

### 4.1 Nodes (What We Already Model)

| Source Today | CALM Node Type | Count |
|-------------|---------------|-------|
| `domains.yaml` → services list | `service` | 22 services |
| `data-stores.yaml` → per-service DB config | `database` | 19 data stores |
| `actors.yaml` → Human actors | `actor` | ~8 actors |
| `actors.yaml` → Frontend apps | `system` (UI) | 3 applications |
| `actors.yaml` → External integrations | `system` (external) | ~4 external systems |
| `events.yaml` → Kafka channels | `system` (messaging) | 1 (Kafka broker) |

**Total nodes to model: ~57**

### 4.2 Relationships (What We Already Model)

| Source Today | CALM Relationship Type | Protocol |
|-------------|----------------------|----------|
| `cross-service-calls.yaml` → REST calls | `interacts` or `connects` | HTTPS |
| `events.yaml` → event producer/consumer | `interacts` | Kafka |
| `data-stores.yaml` → service-to-DB | `connects` | JDBC/MongoDB |
| `consumers.yaml` → app-to-service | `interacts` | HTTPS |
| `pci.yaml` → PCI data flows | `interacts` (decorated with PCI control) | HTTPS |

### 4.3 Interfaces (What We Already Model)

| Source Today | CALM Interface Type |
|-------------|-------------------|
| OpenAPI specs → endpoints | `path` (e.g., `/reservations/{id}`) |
| AsyncAPI specs → channels | `path` (e.g., `novatrek.booking.reservation.created`) |
| `data-stores.yaml` → DB connections | `host-port` + `path` (schema name) |

### 4.4 Controls (What We Already Enforce Manually)

| Rule | Enforcement Today | CALM Control |
|------|-------------------|-------------|
| No shared databases | PR review | `data-ownership` control: each database node has exactly one `connects` relationship from its owning service |
| PCI scope | `pci.yaml` manual list | `pci-dss-scope` control: flag on nodes and relationships |
| Pattern 3 default fallback | ADR-005 + PR review | `safety-default` control: validate adventure classification mappings |
| Cross-service API-only | `copilot-instructions.md` rule | `api-mediated-access` control: no `connects` relationships of type JDBC between services |

---

## 5. Phased Implementation Plan

### Phase 0: Pilot (1-2 weeks)

**Goal:** Prove CALM adds value by modeling a single bounded context and running validation in CI.

| Step | Task | Deliverable |
|------|------|-------------|
| 0.1 | Install CALM CLI (`npm install -g @finos/calm-cli`) and verify | Working `calm validate` and `calm generate` commands |
| 0.2 | Model the **Operations domain** (svc-check-in, svc-scheduling-orchestrator, their databases, Kafka topics, and cross-service calls) as a CALM architecture document | `architecture/calm/operations-domain.json` |
| 0.3 | Write a **NovaTrek microservice pattern** that enforces: each service has exactly one database, uses HTTPS for sync calls, and has a defined owner | `architecture/calm/patterns/novatrek-microservice.json` |
| 0.4 | Run `calm validate -p pattern.json -a operations-domain.json` in CI (add step to `validate-solution.yml`) | Green CI check for CALM validation |
| 0.5 | Write a **data-ownership control** that flags any database node connected to more than one service | `architecture/calm/controls/data-ownership.json` |
| 0.6 | Document findings: what worked, what did not, migration effort estimate | `architecture/reminders/CALM-PILOT-RESULTS.md` |

**Success Criteria:**
- CALM accurately represents the Operations domain topology
- `calm validate` catches a deliberately introduced violation (e.g., shared database)
- Effort to model one domain < 2 hours
- No disruption to existing generators or workflows

**File Placement:**

```
architecture/
├── calm/
│   ├── novatrek-system.json          (Phase 1 — full system)
│   ├── domains/
│   │   └── operations.json           (Phase 0 — pilot domain)
│   ├── patterns/
│   │   ├── novatrek-microservice.json
│   │   ├── novatrek-event-driven.json
│   │   └── novatrek-3tier.json
│   ├── controls/
│   │   ├── data-ownership.json
│   │   ├── pci-scope.json
│   │   └── api-mediated-access.json
│   └── standards/
│       └── novatrek-org-standard.json
├── metadata/                          (existing — unchanged during Phase 0)
├── specs/                             (existing — unchanged)
└── events/                            (existing — unchanged)
```

---

### Phase 1: Full Topology Model (2-3 weeks)

**Goal:** Model the complete NovaTrek system in CALM, all 9 domains.

| Step | Task | Deliverable |
|------|------|-------------|
| 1.1 | Model remaining 8 domains as individual CALM documents | `architecture/calm/domains/{domain}.json` (8 files) |
| 1.2 | Create the **system-level CALM document** that composes all domains using `composed-of` relationships | `architecture/calm/novatrek-system.json` |
| 1.3 | Write a **CALM-to-YAML bridge generator** that reads `novatrek-system.json` and produces the existing metadata YAML files (domains.yaml, cross-service-calls.yaml, data-stores.yaml, actors.yaml, events.yaml, consumers.yaml) | `portal/scripts/calm-to-metadata.py` |
| 1.4 | Validate that existing generators produce identical output when fed CALM-derived YAML vs. hand-maintained YAML | Diff report showing zero divergence |
| 1.5 | Write an **OpenAPI-to-CALM interface generator** that reads `architecture/specs/*.yaml` and populates CALM interface nodes automatically | `portal/scripts/openapi-to-calm-interfaces.py` |
| 1.6 | Write an **AsyncAPI-to-CALM interface generator** for event channel interfaces | `portal/scripts/asyncapi-to-calm-interfaces.py` |
| 1.7 | Add CALM validation to CI — `calm validate` for all domain documents and system document | Updated `.github/workflows/validate-solution.yml` |

**Architecture Decision Required:** ADR-012 — Single Source of Truth Direction

The central question Phase 1 must answer:

> Should CALM become the single source of truth for topology (replacing `domains.yaml`, `cross-service-calls.yaml`, etc.), or should CALM be a derived view generated from the existing YAML files?

| Option | Pros | Cons |
|--------|------|------|
| **A: CALM as source, YAML derived** | Single topology source; CALM validation catches errors; industry-standard format | Migration effort; architects learn new format; CALM tooling dependency |
| **B: YAML as source, CALM derived** | No migration; existing workflow unchanged; CALM is additive | Two representations to maintain; CALM validation may miss YAML-only issues |
| **C: Coexistence with bridge validation** | Gradual migration; both formats validated against each other | Complexity; two sources of truth during transition |

**Recommendation:** Option C for Phase 1 (coexistence), with a decision gate at Phase 1 completion to choose A or B for Phase 2+.

---

### Phase 2: Generator Integration (2-3 weeks)

**Goal:** Portal generators consume CALM topology for richer output.

| Step | Task | Deliverable |
|------|------|-------------|
| 2.1 | Update `generate-microservice-pages.py` to optionally read CALM topology for cross-service relationship data instead of `cross-service-calls.yaml` | Updated generator with `--source calm` flag |
| 2.2 | Create a **topology visualization generator** using CALM data — produces an interactive system map (D3.js or Mermaid) | `portal/scripts/generate-topology-map.py` → `portal/docs/topology/` |
| 2.3 | Create a **data flow diagram generator** that reads CALM relationships and produces C4-style data flow diagrams in PlantUML | `portal/scripts/generate-data-flows.py` → `portal/docs/topology/data-flows/` |
| 2.4 | Add a **dependency matrix** page to the portal showing service-to-service dependencies from CALM | `portal/docs/topology/dependency-matrix.md` |
| 2.5 | Enhance `generate-capability-pages.py` to show which CALM nodes and relationships each capability touches | Updated capability pages with topology cross-links |
| 2.6 | Add CALM-aware **impact analysis** to solution design workflow — when a new solution touches a service, automatically list all upstream/downstream dependencies from the CALM graph | `portal/scripts/calm-impact-analysis.py` |

**Portal Addition: Topology Section**

```yaml
# portal/mkdocs.yml (new nav entry)
nav:
  - Topology:
    - System Map: topology/system-map.md
    - Dependency Matrix: topology/dependency-matrix.md
    - Data Flows: topology/data-flows/index.md
    - PCI Scope: topology/pci-scope.md
```

---

### Phase 3: Governance Automation (2-3 weeks)

**Goal:** Replace manual PR review checks with automated CALM validation.

| Step | Task | Deliverable |
|------|------|-------------|
| 3.1 | Write CALM patterns for NovaTrek architecture rules: **no shared databases**, **API-mediated cross-service access**, **event-driven cross-domain communication** | `architecture/calm/patterns/` (3 pattern files) |
| 3.2 | Write CALM controls for: **PCI data flow scope**, **data ownership boundaries**, **safety default (Pattern 3 fallback)** | `architecture/calm/controls/` (3 control files) |
| 3.3 | Create a **NovaTrek organizational standard** extending CALM nodes with required metadata: domain, team owner, data classification, PCI flag | `architecture/calm/standards/novatrek-org-standard.json` |
| 3.4 | Integrate `calm validate` with all patterns, controls, and standards into CI — validation failures block PR merge | Updated `validate-solution.yml` |
| 3.5 | Write a **governance dashboard generator** that shows compliance status per service (which controls pass/fail/not-applicable) | `portal/scripts/generate-governance-dashboard.py` → `portal/docs/governance/` |
| 3.6 | Add Spectral custom rules for NovaTrek-specific warnings (e.g., "service has no consumer — is it orphaned?") | `.spectral.yml` or CALM-equivalent config |

**Governance Rules to Automate:**

| Rule | Current Enforcement | CALM Enforcement |
|------|-------------------|-----------------|
| No shared databases | PR reviewer reads `data-stores.yaml` | CALM pattern: each `database` node has exactly one `connects` relationship with `relationship-type: connects` |
| Cross-domain via API only | Copilot instructions text | CALM pattern: no `connects` relationships between services in different domains unless protocol is `HTTPS` or `Kafka` |
| PCI scope tracking | Manual `pci.yaml` | CALM decorator: `pci-dss-scope` attached to relevant nodes/relationships |
| Optimistic locking required | ADR-011 + PR review | CALM control: services with mutable shared entities require `@Version`/`_rev` interface metadata |
| Pattern 3 default | ADR-005 + PR review | CALM control: adventure classification mapping must include `UNKNOWN → Pattern 3` |
| Event schema required | asyncAPI spec exists | CALM pattern: every `interacts` relationship with protocol `Kafka` must reference an AsyncAPI interface |

---

### Phase 4: Solution Design Integration (1-2 weeks)

**Goal:** Integrate CALM into the solution design lifecycle so topology changes are tracked alongside capability changes.

| Step | Task | Deliverable |
|------|------|-------------|
| 4.1 | Add a `topology-changes/` subfolder to the solution design template under `3.solution/` | Updated solution template |
| 4.2 | Define a **CALM diff format** — when a solution modifies the topology (adds a node, changes a relationship, adds an interface), the diff is captured as a before/after CALM fragment | `architecture-standards/calm/topology-diff-template.json` |
| 4.3 | Update `copilot-instructions.md` to include CALM topology change requirements in the solution design checklist | Updated instructions |
| 4.4 | Write a **CALM timeline entry generator** that creates timeline moments from solution merges | `portal/scripts/calm-timeline.py` |
| 4.5 | Extend `capability-changelog.yaml` schema to include optional `topology_changes` field per entry — records which CALM nodes/relationships were added, modified, or removed | Updated YAML schema |
| 4.6 | Update `generate-solution-pages.py` to render topology change diffs on solution pages | Updated generator |

**Solution Design Topology Change Example:**

```yaml
# capability-changelog.yaml entry
entries:
  - ticket: NTK-10010
    date: 2026-04-01
    solution: _NTK-10010-real-time-adventure-tracking
    summary: Add real-time GPS tracking for active adventures
    capabilities:
      - id: CAP-2.4
        impact: new
        description: Real-time location tracking during adventures
    topology_changes:
      nodes_added:
        - id: svc-location-tracking
          type: service
          domain: Operations
      relationships_added:
        - source: svc-check-in
          target: svc-location-tracking
          type: interacts
          protocol: HTTPS
        - source: svc-location-tracking
          target: kafka-broker
          type: interacts
          protocol: Kafka
          channel: novatrek.operations.location.updated
      interfaces_added:
        - node: svc-location-tracking
          type: path
          path: /adventures/{id}/location
```

---

### Phase 5: Advanced Capabilities (3-4 weeks)

**Goal:** Leverage CALM for advanced architecture intelligence.

| Step | Task | Deliverable |
|------|------|-------------|
| 5.1 | Deploy **CALM Hub** (Java/Quarkus + MongoDB or NitriteDB) as a centralized pattern and architecture repository | Azure Container Apps deployment (next to Vikunja) |
| 5.2 | Write an **architecture drift detector** — compare CALM topology against running system metadata (e.g., Kubernetes service mesh, API gateway routes) | `portal/scripts/calm-drift-detector.py` |
| 5.3 | Create an **AI-assisted topology reviewer** — when a solution branch modifies CALM documents, the AI agent validates the change against patterns and suggests missing relationships | Copilot custom instruction update |
| 5.4 | Build a **blast radius calculator** — given a proposed change to a CALM node or relationship, compute the transitive closure of affected components | `portal/scripts/calm-blast-radius.py` |
| 5.5 | Implement **CALM timeline visualization** — show the evolution of the NovaTrek topology over time, highlighting when services, relationships, and interfaces were added or modified | `portal/docs/topology/timeline.md` (interactive) |
| 5.6 | Create **CALM-aware Confluence publishing** — extend `confluence-prepare.py` to include topology diagrams and governance dashboards in the Confluence mirror | Updated Confluence pipeline |
| 5.7 | Write **CALM templates** (Handlebars) to auto-generate architecture documentation sections from topology data — replacing manual content in solution impact assessments | `architecture/calm/templates/` |

---

## 6. CALM CLI Integration

### Installation

```bash
# Install globally
npm install -g @finos/calm-cli

# Verify
calm --version
```

### Key Commands for Our Workflow

| Command | Usage in NovaTrek |
|---------|-------------------|
| `calm generate -p pattern.json -o output.json` | Scaffold a new service topology from the NovaTrek microservice pattern |
| `calm validate -p pattern.json -a arch.json -f junit` | CI validation — produces jUnit XML for GitHub Actions test reporting |
| `calm validate -a arch.json --strict` | Strict mode — warnings become errors (use in production branches) |
| `calm template -a arch.json -d templates/ -o output/` | Generate portal pages directly from topology (Phase 2+) |
| `calm docify -a arch.json --scaffold -o docs/` | Generate documentation scaffolds from topology |
| `calm init-ai -p copilot -d .` | Configure GitHub Copilot with CALM schema awareness |

### CI Integration

```yaml
# .github/workflows/validate-solution.yml (addition)
  calm-validation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm install -g @finos/calm-cli
      - name: Validate CALM topology
        run: |
          for domain in architecture/calm/domains/*.json; do
            calm validate \
              -p architecture/calm/patterns/novatrek-microservice.json \
              -a "$domain" \
              -f junit \
              -o "test-results/calm-$(basename $domain .json).xml"
          done
      - name: Validate system composition
        run: |
          calm validate \
            -a architecture/calm/novatrek-system.json \
            --strict \
            -f junit \
            -o test-results/calm-system.xml
      - name: Publish CALM results
        uses: dorny/test-reporter@v1
        if: always()
        with:
          name: CALM Validation
          path: test-results/calm-*.xml
          reporter: java-junit
```

---

## 7. Migration Strategy

### 7.1 Parallel Operation (Phases 0-1)

During Phases 0 and 1, CALM documents coexist with the legacy YAML files. Both are maintained. A bridge validator ensures they stay in sync:

```
Architect edits YAML (existing workflow)
  → Bridge script generates CALM from YAML
  → calm validate checks CALM documents
  → Any validation failure = CI red

OR

Architect edits CALM (new workflow)
  → Bridge script generates YAML from CALM
  → Existing generators read YAML as before
  → calm validate checks CALM documents
```

### 7.2 Cutover Decision Gate (End of Phase 1)

At the end of Phase 1, a decision is made (ADR-012):

**If CALM becomes the source of truth:**
- Generators are updated to read CALM directly (Phase 2)
- Legacy YAML files are generated from CALM for backward compatibility
- New metadata changes go into CALM documents
- Legacy YAML files are eventually deprecated

**If YAML remains the source of truth:**
- CALM is treated as a derived governance layer
- A CI step generates CALM from YAML and validates it
- CALM patterns and controls add automated governance without changing the authoring workflow
- Architects never edit CALM directly

### 7.3 Metadata Mapping Reference

| Legacy YAML File | CALM Equivalent | Migration Complexity |
|-----------------|-----------------|---------------------|
| `domains.yaml` | Node groups with domain metadata | Low — direct 1:1 mapping |
| `cross-service-calls.yaml` | `interacts` relationships with `HTTPS` protocol | Low — structural translation |
| `data-stores.yaml` | `database` nodes + `connects` relationships | Medium — table details need custom metadata |
| `events.yaml` | `interacts` relationships with `Kafka` protocol | Low — channel → interface mapping |
| `actors.yaml` | `actor` and `system` nodes | Low — direct mapping |
| `consumers.yaml` | `interacts` relationships (app → service) | Low — derived from actors + services |
| `label-to-svc.yaml` | Not needed — CALM nodes have both `name` and `unique-id` | Eliminated |
| `pci.yaml` | `pci-dss-scope` decorator attached to nodes and relationships | Medium — decorator model is new |
| `capabilities.yaml` | Not migrated — CALM models topology, not business capabilities | N/A |
| `capability-changelog.yaml` | Extended with optional `topology_changes` field | Low — additive change |
| `tickets.yaml` | Not migrated — tickets are workflow, not topology | N/A |
| `applications.yaml` | `system` nodes with screen metadata in decorators | Medium — screen flows need custom decorators |
| `app-titles.yaml` | Not needed — CALM nodes have `name` | Eliminated |

---

## 8. CALM Document Examples

### 8.1 Service Node

```json
{
  "unique-id": "svc-check-in",
  "node-type": "service",
  "name": "Check-In Service",
  "description": "Manages day-of-adventure check-in workflows including identity verification, waiver validation, and equipment assignment",
  "interfaces": [
    {
      "unique-id": "svc-check-in-api",
      "type": "path",
      "path": "/check-ins"
    },
    {
      "unique-id": "svc-check-in-event-completed",
      "type": "path",
      "path": "novatrek.operations.checkin.completed"
    }
  ],
  "metadata": {
    "domain": "Operations",
    "team": "NovaTrek Operations Team",
    "data-classification": "internal",
    "pci-in-scope": false
  }
}
```

### 8.2 Database Node

```json
{
  "unique-id": "db-check-in",
  "node-type": "database",
  "name": "Check-In Database",
  "description": "PostgreSQL database storing check-in records, session data, and equipment assignments",
  "interfaces": [
    {
      "unique-id": "db-check-in-jdbc",
      "type": "host-port",
      "host": "checkin-db.novatrek.internal",
      "port": 5432
    }
  ],
  "metadata": {
    "engine": "PostgreSQL 15",
    "schema": "checkin",
    "tables": ["check_ins", "equipment_assignments", "waiver_validations"]
  }
}
```

### 8.3 Relationship (Service-to-Service REST Call)

```json
{
  "unique-id": "rel-checkin-to-reservations",
  "relationship-type": "interacts",
  "description": "Check-in service retrieves reservation details for guest verification",
  "protocol": "HTTPS",
  "source": {
    "node": "svc-check-in"
  },
  "destination": {
    "node": "svc-reservations",
    "interface": "svc-reservations-api"
  }
}
```

### 8.4 Relationship (Event-Driven)

```json
{
  "unique-id": "rel-checkin-event-completed",
  "relationship-type": "interacts",
  "description": "Check-in service publishes completion event consumed by analytics and notifications",
  "protocol": "Kafka",
  "source": {
    "node": "svc-check-in",
    "interface": "svc-check-in-event-completed"
  },
  "destination": {
    "node": "kafka-broker",
    "interface": "kafka-checkin-completed-topic"
  }
}
```

### 8.5 NovaTrek Microservice Pattern (JSON Schema)

```json
{
  "$schema": "https://calm.finos.org/release/1.2/meta/calm.json",
  "title": "NovaTrek Microservice Pattern",
  "description": "Every NovaTrek microservice must have exactly one owned database, expose an HTTPS API, and declare a team owner",
  "type": "object",
  "properties": {
    "nodes": {
      "type": "array",
      "prefixItems": [
        {
          "properties": {
            "node-type": { "const": "service" },
            "interfaces": {
              "type": "array",
              "minItems": 1
            },
            "metadata": {
              "type": "object",
              "required": ["domain", "team", "data-classification"]
            }
          },
          "required": ["unique-id", "node-type", "name", "interfaces", "metadata"]
        },
        {
          "properties": {
            "node-type": { "const": "database" }
          },
          "required": ["unique-id", "node-type", "name"]
        }
      ],
      "minItems": 2,
      "maxItems": 2
    },
    "relationships": {
      "type": "array",
      "minItems": 1,
      "items": {
        "properties": {
          "relationship-type": { "enum": ["connects", "interacts"] },
          "protocol": { "type": "string" }
        },
        "required": ["unique-id", "relationship-type", "protocol"]
      }
    }
  },
  "required": ["nodes", "relationships"]
}
```

### 8.6 Data Ownership Control

```json
{
  "$schema": "https://calm.finos.org/release/1.2/meta/control-requirement.json",
  "unique-id": "ctrl-data-ownership",
  "name": "Exclusive Data Ownership",
  "description": "Each database node must be connected to exactly one service node. No shared databases between services.",
  "control-requirement-url": "https://architecture.novatrek.example.com/standards/data-ownership",
  "severity": "error"
}
```

---

## 9. Impact on Existing Workflows

### 9.1 Solution Design Workflow (Enhanced)

```
Ticket Assigned
  |
  v
Create Branch: solution/NTK-XXXXX-slug
  |
  v
Run Prior-Art Discovery (EXISTING)
  |
  v
Create Solution in architecture/solutions/_NTK-XXXXX-slug/
  |-- (existing folders unchanged)
  |-- 3.solution/
  |   |-- t.topology/                    ← NEW
  |   |   |-- topology-changes.json      ← CALM diff fragment
  |   |   |-- topology-changes.md        ← Human-readable summary
  |
  v
Update Metadata (EXISTING + NEW):
  |-- architecture/metadata/capabilities.yaml (existing)
  |-- architecture/metadata/capability-changelog.yaml (existing, with topology_changes)
  |-- architecture/calm/domains/{domain}.json  ← NEW: topology changes
  |
  v
Open Pull Request
  |-- CI validates YAML (existing)
  |-- CI validates CALM topology (NEW)
  |-- CI runs calm validate against patterns and controls (NEW)
  |-- Reviewer applies architecture checklist (existing)
  |
  v
Merge to Main → Portal Publishes → Topology Updates → Architecture Grows
```

### 9.2 AI Agent Workflow (Enhanced)

Update `copilot-instructions.md` to include:

1. **Before proposing a solution:** Read the CALM topology document for affected domains to understand current node/relationship structure
2. **When adding cross-service calls:** Update both `cross-service-calls.yaml` and the relevant CALM domain document
3. **When proposing a new service:** Use `calm generate` to scaffold from the NovaTrek microservice pattern
4. **In impact assessments:** Reference CALM node and relationship IDs for precision
5. **Infrastructure for CALM:** `calm validate` runs locally before pushing; CI validates on PR

### 9.3 Portal Generator Workflow (Enhanced)

```
Phase 0-1 (Parallel):
  YAML files → existing generators → portal pages
  CALM files → calm validate → CI check (governance only)

Phase 2+ (Integrated):
  CALM files → topology generators → topology pages, data flow diagrams
  CALM files → bridge → YAML → existing generators → service pages
  (or)
  CALM files → updated generators → service pages (direct consumption)
```

---

## 10. Tooling Requirements

| Tool | Version | Purpose | Install |
|------|---------|---------|---------|
| CALM CLI | v1.34+ | Validate, generate, template | `npm install -g @finos/calm-cli` |
| Node.js | v20+ | CALM CLI runtime | Already available (CI runners) |
| Python 3.x | 3.10+ | Bridge scripts, generators | Already available |
| PlantUML | Latest | Topology diagram rendering | Already available (CI) |
| D3.js or Mermaid | Latest | Interactive topology visualization | Portal dependency (Phase 2) |
| CALM Hub (optional) | Latest | Centralized pattern repository | Docker or Azure Container Apps (Phase 5) |

---

## 11. Success Metrics

| Phase | Metric | Target |
|-------|--------|--------|
| 0 | Time to model one domain in CALM | < 2 hours |
| 0 | CALM catches deliberately introduced violation | 100% |
| 1 | Full system modeled in CALM | 22 services, ~57 nodes, all relationships |
| 1 | Legacy YAML ↔ CALM parity | Zero divergence in bridge validation |
| 2 | Topology visualization live on portal | Interactive system map with drill-down |
| 2 | Impact analysis available for solution designs | Automatic dependency listing per solution |
| 3 | Manual governance rules automated in CI | 6+ rules enforced by CALM patterns/controls |
| 3 | PR review time for topology changes | Reduced (quantitative measurement) |
| 4 | Solution designs include topology diffs | 100% of solutions touching cross-service boundaries |
| 5 | Architecture drift detection | Automated comparison between CALM and runtime topology |

---

## 12. Relationship to Existing Roadmap Phases

| Roadmap Phase | CALM Integration Point |
|---------------|----------------------|
| Phase 1 (Foundation) | Complete — CALM builds on the metadata backbone |
| Phase 2 (Portal Publishing) | CALM Phase 2 adds topology pages to the existing portal |
| Phase 3 (AI Integration) | CALM Phase 3 extends AI with topology-aware reasoning |
| Phase 4 (Ticketing / Vikunja) | CALM Phase 4 links tickets to topology changes |
| Phase 5 (Advanced Features) | CALM Phase 5 enables blast radius, drift detection, timeline visualization |
| Phase 6 (Confluence Publishing) | CALM topology diagrams included in Confluence mirror |

---

## 13. Open Questions

1. **CALM version pinning** — Should we pin to a specific CALM schema version (e.g., 1.2) or track latest? Pinning provides stability; latest provides features.

2. **JSON vs. YAML for CALM documents** — CALM uses JSON natively. Our architects are YAML-fluent. Should we author in YAML and transpile to JSON for validation, or adopt JSON?

3. **Granularity of domain decomposition** — Should each domain have its own CALM document, or should we model the entire system in one large document? Separate documents enable independent validation but require composition for cross-domain analysis.

4. **CALM Hub deployment** — Is the operational overhead of running CALM Hub (Java/Quarkus + MongoDB) justified, or can we achieve sufficient governance with file-based CALM documents in Git?

5. **Decorator schema design** — How many custom decorator types does NovaTrek need? Candidates: `deployment`, `pci-scope`, `cost-attribution`, `data-classification`, `team-ownership`. Each needs a JSON Schema.

6. **OpenAPI/AsyncAPI synchronization** — Should CALM interfaces be auto-generated from specs (keeping specs as source of truth for contracts), or should CALM interfaces be authored independently with specs validated against them?

7. **Community engagement** — Should NovaTrek contribute NovaTrek-specific patterns back to the CALM community as examples for the adventure/hospitality domain?

---

## 14. Appendix: CALM Resources

| Resource | URL | Purpose |
|----------|-----|---------|
| CALM Specification | `github.com/finos/architecture-as-code` | Core spec, examples, governance |
| CALM CLI | `npmjs.com/package/@finos/calm-cli` | Tooling |
| Architecture as Code Foundation | `architectureascode.org` | Community, events, blog |
| CALM Hub | Included in spec repo | Centralized governance platform |
| CALM VS Code Extension | VS Code Marketplace | Visual editing |
| Existing Evaluation | `architecture/reminders/CALM-EVALUATION.md` | Prior evaluation criteria (2026-03-06) |
