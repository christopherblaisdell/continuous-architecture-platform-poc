# Team Topology as Code — A First-Class EaC Pillar (Blueprint)

> **BLUEPRINT DOCUMENT.** This is the portable definition of Pillar AE — Team Topology as Code.
> It describes a pattern applicable to any software architecture practice. References to NovaTrek
> Adventures teams and services are synthetic exemplar data used to validate the pattern, not
> corporate information. See [Synthetic Exemplar Status](#synthetic-exemplar-status) for details.

**Status**: This is Pillar AE of the Everything as Code framework — see [EaC Framework](EVERYTHING-AS-CODE-FRAMEWORK.md).

---

## Why Team Topology Belongs in EaC

Conway's Law (Mel Conway, 1968) states: *"Any organization that designs a system will produce a
design whose structure is a copy of the organization's communication structure."*

This is not an observation to work around — it is an architectural constraint to design with.
The organizational topology IS part of the architecture. Teams that are not allowed to communicate
directly will produce services that are not coupled. Teams that communicate constantly will produce
tightly integrated services. Teams that are restructured without updating service ownership will
produce orphaned services with unclear ownership.

Making team topology a version-controlled artifact yields structural benefits:

| Property | Requirement |
|----------|-------------|
| Legibility | Any engineer can answer "who owns this service?" without asking anyone |
| Traceability | Service ownership changes are recorded with dates and rationale |
| Alignment | Aspirational interaction modes can be declared alongside current modes, making gaps visible |
| AI legibility | AI agents can reason over ownership when generating impact assessments and routing escalations |
| Onboarding | New team members read the topology registry to understand the organizational context |

---

## The Team Topologies Vocabulary

This pillar is grounded in the Team Topologies framework (Matthew Skelton and Manuel Pais, 2019),
which provides the definitional vocabulary for team types and interaction modes.

### Team types

| Type | Purpose | Typical lifespan |
|------|---------|-----------------|
| `stream-aligned` | Delivers value directly to end users; owns a specific business subdomain end-to-end | Long-lived |
| `platform` | Provides internal capabilities as a service to stream-aligned teams; reduces cognitive load | Long-lived |
| `enabling` | Helps stream-aligned teams acquire capabilities they lack; transfers knowledge, then dissolves | Time-limited |
| `complicated-subsystem` | Owns a component requiring deep specialist knowledge (ML models, real-time processing, cryptography) | Stable |

### Interaction modes

| Mode | Description | Bandwidth |
|------|-------------|-----------|
| `collaboration` | Two teams work together closely on a shared problem. High bandwidth, temporary by intent. | High |
| `x-as-a-service` | One team provides a well-defined service that the other consumes. Low coordination overhead. | Low |
| `facilitating` | An enabling team helps a stream-aligned team acquire a capability. One-directional assistance. | Medium |

---

## The Team Registry Schema

### teams.yaml

```yaml
# architecture/metadata/teams.yaml
$schema: "./schemas/teams.schema.json"

teams:
  # --- Stream-aligned teams ---
  - id: team-booking-platform
    name: Booking Platform Team
    type: stream-aligned
    domain: Booking
    description: >
      Owns the end-to-end reservation lifecycle: search, booking, modification,
      and cancellation. Accountable for the guest booking experience and payment integration.
    services_owned:
      - svc-reservations
      - svc-payments
    members_count: 6
    communication_channels:
      - type: slack
        handle: "#team-booking-platform"
      - type: email
        address: booking-platform@novatrek.example.com
    status: active

  - id: team-guest-experience
    name: Guest Experience Team
    type: stream-aligned
    domain: Guest Identity
    description: >
      Owns all guest-facing identity, loyalty, and personalization services.
      Accountable for guest profile integrity and loyalty program execution.
    services_owned:
      - svc-guest-profiles
      - svc-loyalty-rewards
    members_count: 5
    communication_channels:
      - type: slack
        handle: "#team-guest-experience"
    status: active

  - id: team-operations
    name: NovaTrek Operations Team
    type: stream-aligned
    domain: Operations
    description: >
      Owns day-of adventure execution systems: check-in, scheduling, guide management,
      and live tracking. Accountable for the operations dashboard and guide mobile app.
    services_owned:
      - svc-check-in
      - svc-scheduling-orchestrator
      - svc-guide-management
    members_count: 7
    communication_channels:
      - type: slack
        handle: "#team-operations"
    status: active

  - id: team-product
    name: Product Team
    type: stream-aligned
    domain: Product Catalog
    description: >
      Owns adventure catalog management, trail data, and adventure classification.
      Accountable for the configuration-driven classification system (ADR-004).
    services_owned:
      - svc-trip-catalog
      - svc-trail-management
    members_count: 4
    communication_channels:
      - type: slack
        handle: "#team-product"
    status: active

  # --- Platform teams ---
  - id: team-platform-engineering
    name: Platform Engineering Team
    type: platform
    domain: Platform
    description: >
      Provides CI/CD pipelines, observability tooling, developer portal infrastructure,
      and the internal architecture metadata toolchain as internal products consumed by
      stream-aligned teams.
    services_owned:
      - svc-analytics
    members_count: 4
    communication_channels:
      - type: slack
        handle: "#platform-engineering"
    status: active

  - id: team-platform-architecture
    name: Platform Architecture Team
    type: platform
    domain: Architecture
    description: >
      Provides architecture standards, EaC framework tooling, ADR governance, and
      capability modeling as an internal product consumed by all engineering teams.
      Maintains the NovaTrek Architecture Portal.
    services_owned: []
    members_count: 2
    communication_channels:
      - type: slack
        handle: "#platform-architecture"
    status: active

  # --- Enabling teams ---
  - id: team-security-enablement
    name: Security Enablement Team
    type: enabling
    domain: Security
    description: >
      Helps stream-aligned teams adopt security-as-code practices. Time-limited:
      this team dissolves once each stream-aligned team has an established security
      review workflow and Policy as Code rules for their domain.
    services_owned: []
    members_count: 2
    communication_channels:
      - type: slack
        handle: "#security-enablement"
    status: active
    expected_dissolution: 2026-12-31

  # --- Complicated-subsystem teams ---
  - id: team-safety-compliance
    name: Safety and Compliance Team
    type: complicated-subsystem
    domain: Safety
    description: >
      Owns the safety compliance service and waiver management system. Requires deep
      domain expertise in NovaTrek safety regulations and liability management.
      Not a general software engineering team — staffed by safety domain specialists.
    services_owned:
      - svc-safety-compliance
    members_count: 3
    communication_channels:
      - type: slack
        handle: "#safety-compliance"
    status: active

interactions:
  - id: INT-001
    from_team: team-booking-platform
    to_team: team-platform-engineering
    mode: x-as-a-service
    description: >
      Booking Platform Team consumes the CI/CD pipelines and observability stack
      provided by Platform Engineering as self-service internal products.
    since: 2025-01-01
    status: active

  - id: INT-002
    from_team: team-operations
    to_team: team-guest-experience
    mode: x-as-a-service
    description: >
      Operations Team calls svc-guest-profiles (owned by Guest Experience) via its
      published API for guest identity resolution during check-in.
    since: 2025-06-01
    status: active

  - id: INT-003
    from_team: team-guest-experience
    to_team: team-booking-platform
    mode: collaboration
    description: >
      Temporary collaboration on a unified guest checkout experience that requires
      coordination between loyalty point application (Guest Experience) and reservation
      creation (Booking Platform). Collaboration ends once the integration API is stable.
    since: 2026-03-01
    until: 2026-09-30
    status: active

  - id: INT-004
    from_team: team-security-enablement
    to_team: team-booking-platform
    mode: facilitating
    description: >
      Security Enablement Team is helping Booking Platform Team adopt security-as-code
      patterns, specifically establishing Policy as Code rules for PCI-adjacent data handling.
    since: 2026-01-01
    until: 2026-06-30
    status: active
```

### JSON Schema excerpt

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Team Registry",
  "type": "object",
  "required": ["teams", "interactions"],
  "properties": {
    "teams": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "name", "type", "domain", "description", "services_owned", "status"],
        "properties": {
          "id": { "type": "string", "pattern": "^team-[a-z0-9-]+$" },
          "name": { "type": "string" },
          "type": {
            "type": "string",
            "enum": ["stream-aligned", "platform", "enabling", "complicated-subsystem"]
          },
          "domain": { "type": "string" },
          "description": { "type": "string" },
          "services_owned": {
            "type": "array",
            "items": { "type": "string" }
          },
          "members_count": { "type": "integer", "minimum": 1 },
          "status": { "type": "string", "enum": ["active", "dissolved"] },
          "expected_dissolution": { "type": "string", "format": "date" }
        }
      }
    },
    "interactions": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "from_team", "to_team", "mode", "description", "since", "status"],
        "properties": {
          "id": { "type": "string", "pattern": "^INT-[0-9]+$" },
          "from_team": { "type": "string", "pattern": "^team-" },
          "to_team": { "type": "string", "pattern": "^team-" },
          "mode": {
            "type": "string",
            "enum": ["collaboration", "x-as-a-service", "facilitating"]
          },
          "description": { "type": "string" },
          "since": { "type": "string", "format": "date" },
          "until": { "type": "string", "format": "date" },
          "status": { "type": "string", "enum": ["active", "completed", "planned"] }
        }
      }
    }
  }
}
```

---

## Backstage Compatibility

The team registry schema is designed to be compatible with the Spotify Backstage catalog format
(Kind: Group). A generator can produce Backstage-compatible `catalog-info.yaml` entries from the
team registry, enabling organizations using Backstage as their developer portal to ingest the same
source file.

The mapping between the EaC team registry and Backstage Group metadata:

| EaC field | Backstage Group field |
|-----------|----------------------|
| `id` | `metadata.name` |
| `name` | `metadata.title` |
| `type` | `spec.type` (maps to `team` with a subtype label) |
| `description` | `metadata.description` |
| `services_owned` | Derived via `spec.owns` with Component references |
| `communication_channels[slack].handle` | `metadata.annotations["slack.com/channel"]` |

Organizations using Backstage do not need to maintain separate catalog-info files for teams —
the generator produces them from the single source of truth in `teams.yaml`.

---

## Generator Architecture

### 1. Organizational topology diagram

A generated PlantUML or Mermaid diagram showing teams as nodes, colored by type, with interaction
mode arrows between them. Active collaborations are shown as solid bidirectional arrows.
X-as-a-service relationships are shown as directed arrows. Facilitating relationships are shown as
dashed arrows.

This diagram is regenerated on every change to `teams.yaml`. It is the equivalent of a Conway's
Law map: the communication structure made visible.

### 2. Service ownership index

A generated index mapping every service to its owning team:

```markdown
| Service | Owning Team | Team Type |
|---------|-------------|-----------|
| svc-check-in | NovaTrek Operations Team | stream-aligned |
| svc-guest-profiles | Guest Experience Team | stream-aligned |
| svc-reservations | Booking Platform Team | stream-aligned |
| svc-safety-compliance | Safety and Compliance Team | complicated-subsystem |
```

This index is generated from the `services_owned` fields and is the authoritative answer to "who
owns this service?".

### 3. Team profile pages

One generated page per team, rendered to `portal/docs/teams/{team-id}.md`. Each page includes
the team type, description, services owned (with links to service pages), active interactions,
and communication channel links.

---

## CI Integration

```yaml
# .github/workflows/validate-teams.yml (excerpt)

- name: Validate teams.yaml schema
  run: |
    npx ajv validate \
      --schema architecture/metadata/schemas/teams.schema.json \
      --data architecture/metadata/teams.yaml

- name: Referential integrity — services owned
  run: |
    python3 scripts/ci/check-team-service-refs.py \
      --teams architecture/metadata/teams.yaml \
      --services architecture/metadata/services.yaml

- name: Referential integrity — interaction team IDs
  run: |
    python3 scripts/ci/check-interaction-refs.py \
      --teams architecture/metadata/teams.yaml

- name: Orphaned service check
  run: |
    python3 scripts/ci/check-orphaned-services.py \
      --teams architecture/metadata/teams.yaml \
      --services architecture/metadata/services.yaml

- name: Topology diagram drift check
  run: |
    python3 portal/scripts/generate-team-topology.py --dry-run
    git diff --exit-code portal/docs/teams/
```

### Validation rules

| Rule | Description |
|------|-------------|
| Schema validation | All required fields present; type and mode values from allowed enums; IDs match prefix patterns |
| Service ownership referential integrity | Every service ID in `services_owned` must exist in the service registry (Pillar D) |
| Interaction team referential integrity | `from_team` and `to_team` IDs must exist in the teams list |
| Orphaned service check | Every service in the service registry must appear in at least one team's `services_owned` list |
| Enabling team dissolution date | Enabling teams without an `expected_dissolution` date trigger a warning |
| Topology diagram drift | Generated topology diagram must match the current registry |

The orphaned service check is the most operationally important rule. A service with no declared
owning team is an architectural liability: incidents have no escalation path, changes have no
approval process, and the service may be deprecated without notice.

---

## AI Fit

The team registry enables two AI behaviors directly relevant to architecture work:

**Impact assessment routing**: When an AI generates an impact assessment for a proposed change, it
reads the team registry to determine which team owns each affected service. The impact assessment
can then name the specific team that must review each service impact rather than leaving the routing
implicit.

**Interaction mode analysis**: When an AI is asked to evaluate a proposed integration between two
services, it reads the team registry to determine how the owning teams currently interact. If
Service A (owned by a platform team) is being asked to call Service B (owned by a stream-aligned
team) synchronously, the AI can flag that this direction of dependency violates the expected
platform → stream-aligned service model and suggest the alternative (stream-aligned calls platform,
not the reverse).

**Ownership gap detection**: An AI scanning the service registry against the team registry can
identify services with no declared owner and surface them as a governance finding.

---

## Governance Model

Team topology changes are significant architectural events. They affect Conway's Law alignment,
service ownership, and escalation paths. Changes to the team registry SHOULD follow the standard
PR review process with explicit rationale, and SHOULD reference any ADR that established the
topology change.

Specific rules:

- **Adding a team**: Requires a declared type, domain, and at least one `services_owned` entry
  or an explicit declaration of empty ownership with rationale.
- **Dissolving a team**: The team record is not deleted; `status` is set to `dissolved` with a
  date. Ownership of all services owned by the dissolved team must be transferred to an active team
  in the same PR.
- **Adding a collaboration interaction**: Because collaboration is temporary, every collaboration
  entry MUST have an `until` date. Collaboration interactions without an end date are flagged by CI.
- **Changing interaction modes**: Significant topology changes (e.g., changing a collaboration to
  x-as-a-service) SHOULD be accompanied by an ADR when the change was the result of a deliberate
  architectural decision.

---

## Recommended Practices

1. **Classify every team by type before authoring the registry.** The classification is the
   architectural claim. Getting it right requires the team to genuinely understand Team Topologies
   and whether they are stream-aligned, platform, enabling, or complicated-subsystem. Rushing
   the classification produces a registry that is technically populated but architecturally
   uninformative.

2. **Declare the current topology, not the aspirational topology.** The aspirational topology
   belongs in interactions with `status: planned` and a `since` date in the future. Mixing
   current and aspirational state in the same fields obscures what is actually true today.

3. **Enforce the orphaned service check in CI.** An orphaned service is a governance failure.
   The CI check makes it impossible to add a service without also declaring ownership.

4. **Review the topology quarterly.** Teams change. Services are transferred. Enabling teams
   dissolve. The topology is not static. Quarterly review is the minimum cadence for an active
   engineering organization.

5. **Use the git history as the organizational record.** The team registry's git history records
   every team reorganization, ownership transfer, and interaction mode change. This is the
   organizational equivalent of the architecture decision log — preserve it.

6. **Distinguish enabling teams from platform teams.** An enabling team helps other teams build
   a capability and then transfers ownership. A platform team provides a permanent internal product.
   These have fundamentally different operational models. Mislabeling an enabling team as a platform
   team produces an organization that keeps "temporary" teams permanently.

---

## Synthetic Exemplar Status

> The status below describes how Pillar AE has been implemented in the NovaTrek Adventures
> synthetic exemplar workspace. NovaTrek data is entirely fictional — no corporate systems are
> represented.

| Artifact | Status | Location |
|----------|--------|----------|
| Team registry YAML | Not yet created — planned in Transformation Wave 9 | `architecture/metadata/teams.yaml` |
| JSON Schema | Not yet created | `architecture/metadata/schemas/teams.schema.json` |
| Team topology diagram | Not yet generated | `portal/docs/teams/topology.svg` |
| Service ownership index | Not yet generated | `portal/docs/teams/ownership-index.md` |
| Team profile pages | Not yet generated | `portal/docs/teams/` |
| CI validation workflow | Not yet wired | `.github/workflows/validate-teams.yml` |
| Orphaned service check | Not yet wired | — |

Team ownership is currently implicit in the NovaTrek workspace — service-to-team assignments appear
in the copilot instructions file and in solution design documents, but not in a queryable registry.
The domain grouping in the microservice page generator (`DOMAINS` dict in
`portal/scripts/generate-microservice-pages.py`) is the closest existing equivalent.

---

## Forward Plan

Pillar AE adoption for NovaTrek is planned in **Wave 9** of the Transformation Plan, alongside
Onboarding as Code (Pillar AF) and Developer Experience as Code (Pillar AG). Wave 9 pillars are
most valuable once the technical pillars have stabilized. See
[Transformation Plan — Pillar AE](TRANSFORMATION-PLAN.md#pillar-ae--team-topology-as-code) for the
sequenced adoption checklist.

Key adoption prerequisite: Applications as Code (Pillar D) MUST be complete before the team
registry can enforce ownership, because the service references in `services_owned` must resolve
against the service registry.

---

## References

- Matthew Skelton and Manuel Pais, *Team Topologies* (2019) — the foundational vocabulary for team types and interaction modes
- Mel Conway, *How Do Committees Invent?* (1968) — the original statement of Conway's Law
- Spotify Backstage catalog-info.yaml specification — https://backstage.io/docs/features/software-catalog/descriptor-format
- Ruth Malan, *Conway's Law* (2008) — extended commentary on the organizational architecture relationship
- NovaTrek EaC Framework: [Pillar AE definition](EVERYTHING-AS-CODE-FRAMEWORK.md)
- NovaTrek Transformation Plan: [Pillar AE adoption steps](TRANSFORMATION-PLAN.md#pillar-ae--team-topology-as-code)
