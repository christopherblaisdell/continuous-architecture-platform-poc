# Actors as Code — A First-Class EaC Pillar (Blueprint)

> **BLUEPRINT DOCUMENT.** This is the portable definition of Pillar C — Actors as Code. It describes
> a pattern applicable to any software architecture practice. References to NovaTrek Adventures
> services and files are synthetic exemplar data used to validate the pattern, not corporate
> information. See [Synthetic Exemplar Status](#synthetic-exemplar-status) for details.

**Status**: This is Pillar C of the Everything as Code framework — see [EaC Framework](EVERYTHING-AS-CODE-FRAMEWORK.md).

---

## Why Actors Belong in EaC

Actors — the human roles, teams, external systems, partner organizations, and automated agents that
interact with your architecture — are first-class architectural concepts. They appear in C4 context
diagrams, ADRs, user stories, API documentation, event schemas, and test specifications. Without a
single version-controlled source of truth, actor identity fragments:

| Property | Requirement |
|----------|-------------|
| Consistency | Every diagram, ADR, and user story must use the same actor name for the same real entity |
| Discoverability | Stakeholders must be able to ask "what systems does the Payment Gateway interact with?" |
| Traceability | Every actor reference in every artifact must resolve to a declared, described entity |
| Evolvability | Actors are renamed, merged, and retired; history must be preserved |
| AI legibility | AI agents must not hallucinate actor names when generating architecture artifacts |

The last property is the forcing function for machine-readable actor registries. An AI generating a
C4 Person diagram from a YAML actor registry cannot invent a name that does not exist. An AI
populating a user story format reads the actor's declared responsibilities. The registry closes the
most common class of AI hallucination in architecture work: inconsistent naming.

---

## The Core Problem

Without an actor registry, actor definitions live in whatever artifact first introduced them. A
`Guest Member` is named in slide 7 of a capabilities deck. An `Integration Partner` appears in an
OpenAPI tag description. An `External System` is labeled in a PlantUML diagram. A `Customer` is
what the JIRA ticket says. A `User` is what the test specification says.

These are all the same entity. No machine can resolve that equivalence. No AI agent can either.
The result is:

- Sequence diagrams have actor labels that do not match the labels in ADRs
- User stories use actor names that do not match the labels in the API documentation
- New solution designs introduce actors that silently duplicate existing ones with slightly
  different names
- AI agents asked to "generate a user story for the check-in flow" produce "As a Customer,..."
  when the canonical term established in three ADRs is "Guest Member"

The actor registry solves this by making actor identity an authoritative source rather than an
inference.

---

## Actor Types

An actor in the EaC sense is any external entity that initiates, receives, or participates in
system behavior. The taxonomy is deliberately broad:

| Type | Description | C4 Notation |
|------|-------------|-------------|
| `human` | A person in a defined role (customer, operator, administrator) | `Person` |
| `team` | An organizational team that operates or integrates with the system | `Person` (group) |
| `external_system` | A third-party system that sends or receives data | `SoftwareSystem` |
| `automated_agent` | An internal or external system operating without direct human involvement | `SoftwareSystem` |
| `iot_device` | A physical device emitting events into the system | `SoftwareSystem` |

The `team` type is distinct from the Team Registry (Pillar AE). Actors describe who the *users and
integrators* of the architecture are. The team registry describes who *builds and owns* it. A
`Platform Engineering Team` is both an actor (it integrates with developer tooling APIs) and a team
in the organizational topology.

---

## The Actor Registry Schema

### actors.yaml

```yaml
# architecture/metadata/actors.yaml
$schema: "./schemas/actors.schema.json"

actors:
  # --- Human roles ---
  - id: actor-guest-member
    name: Guest Member
    type: human
    domain: Guest Identity
    description: >
      A NovaTrek customer who has made a reservation and is arriving at a NovaTrek
      location to begin their adventure. The primary subject of the check-in workflow.
    responsibilities:
      - Presents identity credentials at the check-in kiosk
      - Signs digital liability waivers
      - Receives adventure confirmation and guide assignment
    c4_type: Person
    bounded_context: Guest Identity
    status: active

  - id: actor-operations-staff
    name: Operations Staff
    type: human
    domain: Operations
    description: >
      NovaTrek ground operations employee responsible for managing day-of adventure
      execution, monitoring live tracking, and handling exceptions.
    responsibilities:
      - Monitors the live adventure tracking dashboard
      - Manages check-in exceptions and waitlists
      - Coordinates with guides during active adventures
    c4_type: Person
    bounded_context: Operations
    status: active

  - id: actor-adventure-guide
    name: Adventure Guide
    type: human
    domain: Guide Management
    description: >
      Certified NovaTrek guide who leads guest groups during adventures. Receives
      rosters and schedule information via the guide mobile application.
    responsibilities:
      - Confirms guest check-in via handheld device
      - Leads the adventure and manages in-field safety
      - Submits post-adventure completion reports
    c4_type: Person
    bounded_context: Guide Management
    status: active

  # --- External systems ---
  - id: actor-payment-gateway
    name: Payment Gateway
    type: external_system
    domain: Payments
    description: >
      Third-party payment processing network (e.g., Stripe). Receives payment
      authorization requests from svc-payments and returns authorization confirmations.
    c4_type: SoftwareSystem
    bounded_context: Payments
    status: active
    integrations:
      - service: svc-payments
        direction: inbound
        protocol: HTTPS/REST

  - id: actor-weather-provider
    name: Weather Data Provider
    type: external_system
    domain: External Data
    description: >
      External API providing real-time conditions and multi-day forecast data used
      by the scheduling and safety compliance services to assess adventure viability.
    c4_type: SoftwareSystem
    bounded_context: External Data
    status: active
    integrations:
      - service: svc-weather
        direction: inbound
        protocol: HTTPS/REST

  - id: actor-partner-operator
    name: Partner Operator
    type: external_system
    domain: External Partners
    description: >
      Third-party adventure operator with whom NovaTrek shares reservation data
      and receives confirmation callbacks through the partner integrations gateway.
    c4_type: SoftwareSystem
    bounded_context: External Partners
    status: active
    integrations:
      - service: svc-partner-integrations
        direction: bidirectional
        protocol: HTTPS/Webhook

  # --- Automated agents ---
  - id: actor-scheduling-engine
    name: Scheduling Orchestrator
    type: automated_agent
    domain: Operations
    description: >
      Internal automated system responsible for computing daily adventure schedules,
      assigning guides, and publishing the daily schedule to consuming services.
    c4_type: SoftwareSystem
    bounded_context: Operations
    status: active
    integrations:
      - service: svc-scheduling-orchestrator
        direction: inbound

  # --- IoT devices ---
  - id: actor-rfid-reader
    name: RFID Check-in Reader
    type: iot_device
    domain: Operations
    description: >
      NFC/RFID reader installed at NovaTrek check-in kiosks. Reads guest wristband
      identifiers and forwards them to the check-in service for identity verification.
    c4_type: SoftwareSystem
    bounded_context: Operations
    status: active
    integrations:
      - service: svc-check-in
        direction: inbound
        protocol: NFC/RFID
```

### JSON Schema excerpt

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Actor Registry",
  "type": "object",
  "required": ["actors"],
  "properties": {
    "actors": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "name", "type", "domain", "description", "c4_type", "status"],
        "properties": {
          "id": {
            "type": "string",
            "pattern": "^actor-[a-z0-9-]+$",
            "description": "Kebab-case unique identifier; used as the key in all cross-references"
          },
          "name": { "type": "string" },
          "type": {
            "type": "string",
            "enum": ["human", "team", "external_system", "automated_agent", "iot_device"]
          },
          "domain": { "type": "string" },
          "description": { "type": "string" },
          "responsibilities": {
            "type": "array",
            "items": { "type": "string" }
          },
          "c4_type": {
            "type": "string",
            "enum": ["Person", "SoftwareSystem"]
          },
          "bounded_context": { "type": "string" },
          "status": {
            "type": "string",
            "enum": ["active", "deprecated"]
          },
          "deprecated_in": { "type": "string", "format": "date" },
          "superseded_by": { "type": "string", "pattern": "^actor-" },
          "integrations": {
            "type": "array",
            "items": {
              "type": "object",
              "required": ["service", "direction"],
              "properties": {
                "service": { "type": "string" },
                "direction": {
                  "type": "string",
                  "enum": ["inbound", "outbound", "bidirectional"]
                },
                "protocol": { "type": "string" }
              }
            }
          }
        }
      }
    }
  }
}
```

### Field reference

| Field | Required | Description |
|-------|----------|-------------|
| `id` | Yes | Kebab-case identifier prefixed with `actor-`. Used as the canonical reference key in all cross-referencing YAML, ADRs, and generated artifacts. |
| `name` | Yes | Human-readable display name. This is the canonical name used in diagrams, user stories, and documentation. |
| `type` | Yes | Actor type from the fixed taxonomy. Determines C4 rendering and generator behavior. |
| `domain` | Yes | The business or organizational domain this actor belongs to. |
| `description` | Yes | Plain-language description of who or what this actor is and their role in the architecture. |
| `responsibilities` | No | Bulleted list of what this actor does in the context of the system. Used in generated actor profile pages and user-story scaffolds. |
| `c4_type` | Yes | C4 notation element type: `Person` or `SoftwareSystem`. Used by diagram generators. |
| `bounded_context` | No | The DDD bounded context this actor most naturally inhabits. |
| `status` | Yes | `active` or `deprecated`. Deprecated actors retain their entry with history; they are not deleted. |
| `deprecated_in` | Conditional | ISO 8601 date when the actor was deprecated. Required when `status: deprecated`. |
| `superseded_by` | No | The `id` of the actor that replaces a deprecated actor, if one exists. |
| `integrations` | No | List of services this actor directly integrates with, including directionality. Consumed by C4 diagram generators to draw relationships. |

---

## Generator Architecture

The actor registry is the source for three categories of generated artifact:

### 1. Portal actor pages

One page per actor entry, generated to `portal/docs/actors/{actor-id}.md`. Each page renders:

- Name, type, domain, description, and bounded context
- Responsibilities list (if declared)
- Integration diagram: a C4 context excerpt showing only this actor and the services it touches
- Back-links: ADRs that reference this actor ID, solution designs that mention this actor

### 2. C4 PlantUML macro library

Generated file: `portal/docs/actors/actors.puml`

```plantuml
' Auto-generated — do not edit. Source: architecture/metadata/actors.yaml
!define ACTOR_GUEST_MEMBER(alias) Person(alias, "Guest Member", "NovaTrek customer arriving for check-in")
!define ACTOR_OPERATIONS_STAFF(alias) Person(alias, "Operations Staff", "NovaTrek ground operations employee")
!define ACTOR_PAYMENT_GATEWAY(alias) System_Ext(alias, "Payment Gateway", "Third-party payment processor")
```

Any C4 diagram author includes this file and uses the macros — the actor names cannot diverge from the registry.

### 3. Actor inventory table

A summary page listing all active actors with their type, domain, and linked services. This becomes
the "stakeholder catalog" that architects reference when writing impact assessments.

---

## CI Integration

```yaml
# .github/workflows/validate-actors.yml (excerpt)
- name: Validate actors.yaml schema
  run: |
    npx ajv validate \
      --schema architecture/metadata/schemas/actors.schema.json \
      --data architecture/metadata/actors.yaml

- name: Check actor ID referential integrity
  run: |
    python3 scripts/ci/check-actor-refs.py \
      --registry architecture/metadata/actors.yaml \
      --scan-dirs architecture/solutions/ decisions/ architecture/specs/

- name: Check generated actor macros drift
  run: |
    python3 portal/scripts/generate-actor-pages.py --dry-run
    git diff --exit-code portal/docs/actors/
```

### Validation rules

| Rule | Trigger | Description |
|------|---------|-------------|
| Schema validation | Every PR touching `actors.yaml` | All required fields present; types from allowed enums; IDs match the `actor-` prefix pattern |
| Referential integrity | Every PR touching `decisions/`, `architecture/solutions/`, or `architecture/specs/` | Any actor ID appearing in those files must exist in the registry |
| Deprecation hygiene | Every PR marking an actor `deprecated` | Deprecated entries must include `deprecated_in` date |
| C4 macro drift | Every PR touching `actors.yaml` | Generated `actors.puml` must match source after regeneration |

---

## AI Fit

The actor registry is high-value input for AI architecture work because it eliminates a class of
hallucination that is otherwise undetectable:

**Diagram generation**: An AI generating a C4 context diagram reads `actors.yaml` to populate
`Person` nodes and external system boundaries. It cannot invent an actor name that does not exist.
The generated diagram will use `Actor-guest-member` → `"Guest Member"` exactly as declared.

**User story generation**: AI populates the "As a [actor]" slot from the registry's `name` field
and uses the `responsibilities` list to constrain plausible story bodies.

**ADR authoring**: When an AI generates an ADR that involves stakeholder impact, it reads the actor
registry to enumerate affected parties and verify that all referenced actors are declared.

**Impact assessment**: When an AI is asked "which stakeholders are affected by this API change?", it
joins the change's service references against the actor integration map to produce a prioritized
list of impacted actors.

**Consistency enforcement**: AI agents checking PRs for consistency flag any actor name in a
document that does not resolve to a registry ID.

---

## Governance Model

The actor registry is a governed artifact. Changes follow the standard PR review process with the
following additional constraints:

- **Adding a new actor**: Any contributor may add an actor via PR. Requires all mandatory fields.
  The PR must not introduce an actor whose `name` or `description` overlaps significantly with an
  existing active actor without acknowledgment of the distinction.

- **Renaming an actor**: Name changes propagate to all generated artifacts. The PR must include
  evidence (grep output or CI report) that the old name has been retired from all cross-referencing
  files, or that those files are being updated in the same PR.

- **Deprecating an actor**: Deprecated actors retain their entry. The PR must set `status:
  deprecated`, supply a `deprecated_in` date, and optionally supply a `superseded_by` reference. Do
  not delete entries — history matters.

- **Merging two actors** (determining two entries describe the same entity): Requires an ADR if the
  actors appear in published API specifications or ADRs, because API consumers may depend on the
  distinction. The ADR records the rationale for treating the two as the same entity.

---

## Recommended Practices

1. **Establish the actor registry before authoring C4 diagrams.** The registry is the source; diagrams
   are derived outputs. Diagrams authored before the registry are technical debt.

2. **Use the `id` field as the canonical cross-reference key.** Never reference an actor by name
   alone in YAML files — use the `id`. Display names change; IDs must be stable.

3. **Distinguish actors from services.** An actor is an external entity that interacts with the
   system. A service is part of the system. The same organization can be both an actor (as a
   consumer of your APIs) and an owner of services internally.

4. **Keep responsibilities concrete.** Responsibilities should describe what the actor does in the
   context of the architecture, not generic job duties. "Monitors the live tracking dashboard" is
   a responsibility. "Manages the operations team" is not.

5. **Do not delete deprecated actors.** Deprecated actors may still appear in historical ADRs,
   archived solution designs, and git history. Deleting them breaks referential integrity of the
   historical record. Set `status: deprecated` and preserve the entry.

6. **Review the registry when new external integrations are onboarded.** Every integration partner
   or third-party system that sends or receives data MUST have an actor entry before any API spec
   or ADR references it.

---

## Synthetic Exemplar Status

> The status below describes how Pillar C has been implemented in the NovaTrek Adventures
> synthetic exemplar workspace. NovaTrek data is entirely fictional — no corporate systems are
> represented.

| Artifact | Status | Location |
|----------|--------|----------|
| Actor registry YAML | Not yet created — planned in Transformation Wave 2 | `architecture/metadata/actors.yaml` |
| JSON Schema | Not yet created | `architecture/metadata/schemas/actors.schema.json` |
| Actor portal pages | Not yet generated | `portal/docs/actors/` |
| C4 PlantUML macro library | Not yet generated | `portal/docs/actors/actors.puml` |
| CI schema validation | Not yet wired | `.github/workflows/validate-actors.yml` |

Actors are implicitly declared in the existing OpenAPI tags, PlantUML diagrams, and ADRs (e.g.,
ADR-007 references a guest identity verification flow involving a "Guest" actor). The backlog item
is to extract these implicit declarations into an authoritative `actors.yaml` and retire all ad-hoc
actor references in favor of registry-keyed IDs.

---

## Forward Plan

Pillar C adoption for NovaTrek is planned in **Wave 2** of the Transformation Plan, alongside
Capabilities as Code (Pillar F) and Decisions as Code (Pillar G). See
[Transformation Plan — Pillar C](TRANSFORMATION-PLAN.md#pillar-c--actors-as-code) for the
sequenced adoption checklist.

Key adoption prerequisite: Applications as Code (Pillar D) SHOULD be complete before Actors as
Code, because the actor `integrations` field references service names from the application registry.
Authoring actors without a stable service registry produces dangling references.

---

## References

- Simon Brown, *C4 model for software architecture* — https://c4model.com (Person and SoftwareSystem elements)
- Eric Evans, *Domain-Driven Design* (2003) — Chapter 2: Communication and the Use of Language (bounded contexts)
- TOGAF 10 — Part IV: Architecture Content Framework, Catalog: Actor/Role
- NovaTrek EaC Framework: [Pillar C definition](EVERYTHING-AS-CODE-FRAMEWORK.md)
- NovaTrek Transformation Plan: [Pillar C adoption steps](TRANSFORMATION-PLAN.md#pillar-c--actors-as-code)
