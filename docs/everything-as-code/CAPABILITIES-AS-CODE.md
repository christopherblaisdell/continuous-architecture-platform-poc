# Capabilities as Code — A First-Class EaC Pillar (Blueprint)

> **BLUEPRINT DOCUMENT.** This is the portable definition of Pillar F — Capabilities as Code. It
> describes a pattern applicable to any software architecture practice. References to NovaTrek
> Adventures services and files are synthetic exemplar data used to validate the pattern, not
> corporate information. See [Synthetic Exemplar Status](#synthetic-exemplar-status) for details.

**Status**: This is Pillar F of the Everything as Code framework — see [EaC Framework](EVERYTHING-AS-CODE-FRAMEWORK.md).

---

## Why Capabilities Belong in EaC

Business capabilities — the things an organization *does*, independent of the specific systems,
teams, or technologies that implement them — are the most stable organizing unit in enterprise
architecture. Applications are replaced. Teams are reorganized. Technologies are retired. The
underlying capability (e.g., "Guest Identity Resolution" or "Reservation Management") survives.

Making capabilities version-controlled artifacts yields four structural advantages:

| Property | Requirement |
|----------|-------------|
| Traceability | Every delivered change must link to the capability it affects |
| Portfolio visibility | Leadership can ask "what has been built?" and get a machine-queryable answer |
| Continuity | Capabilities outlast the applications, teams, and decisions that serve them |
| AI legibility | AI agents can locate prior art by capability rather than by ticket title or service name |

The last property drives the architectural decision to make capabilities machine-readable rather
than slide-deck-resident. An AI completing a solution design reads the capability changelog and asks:
"Has this capability been touched before? What decisions were made? What L3 capabilities already
exist?" This requires a structured YAML file, not a wiki page.

---

## The Core Problem

Without a machine-readable capability map and changelog, architecture practices accumulate knowledge
silently:

- A service is enhanced to handle a new edge case — the capability it now covers is not recorded
- A new integration is added — the cross-service capability it enables is visible only by reading
  the implementation code
- A ticket is delivered — the traceability from that delivery to the business capability it
  addressed exists only in the ticket title, which no system can query semantically
- An AI generates a solution design for a new ticket — without a capability index, it cannot
  determine whether the capability has already been addressed in a prior design

The capability changelog is the architectural journal. It records, with machine-readable precision,
what was built, which capability it affected, and what decisions governed the change. It makes the
architecture's evolution legible to both humans and AI agents.

---

## The Three-Tier Capability Model

The EaC framework uses a three-tier capability hierarchy, adapted from Gartner Business Capability
Modeling practice and TOGAF Architecture Building Blocks:

| Tier | Scope | Who defines it | Example |
|------|-------|----------------|---------|
| **L1 — Domain** | The highest-level business grouping | Architecture practice leads, working with business leadership | Guest Management |
| **L2 — Capability** | A functional capability within a domain; what the business does | Solution architects | Guest Identity and Profile |
| **L3 — Feature** | An emergent, fine-grained capability delivered by a specific solution | AI agent or architect authoring the solution design | RFID Wristband Identity Verification |

L1 and L2 capabilities are declared in `capabilities.yaml` and are relatively stable — they change
when the business fundamentally changes what it does. L3 capabilities emerge from the capability
changelog: each solution design records the L3 capabilities it introduced or enhanced. L3 entries
are never pre-declared; they accumulate as solutions are delivered.

This three-tier model is the key distinction from traditional capability maps: L3 capabilities are
*discovered and recorded*, not planned upfront. The changelog is a living record of architectural
growth.

---

## The Capability Hierarchy Schema

### capabilities.yaml

```yaml
# architecture/metadata/capabilities.yaml
$schema: "./schemas/capabilities.schema.json"

capabilities:
  - id: CAP-1
    name: Guest Management
    level: L1
    description: >
      All capabilities related to knowing, serving, and managing NovaTrek guests across
      their lifecycle — from initial account creation through post-adventure loyalty.
    children:
      - id: CAP-1.1
        name: Guest Identity and Profile
        level: L2
        description: >
          Creating, maintaining, and resolving unique guest identity records.
          Includes identity verification, profile data management, and
          deduplication of guest records across channels.

      - id: CAP-1.2
        name: Guest Loyalty and Rewards
        level: L2
        description: >
          Tracking loyalty points, tier progression, and reward redemption
          across NovaTrek guest interactions.

  - id: CAP-2
    name: Adventure Operations
    level: L1
    description: >
      All capabilities required to plan, execute, and close out adventure experiences
      for guests — from scheduling and guide assignment through post-trip reporting.
    children:
      - id: CAP-2.1
        name: Guest Check-in
        level: L2
        description: >
          The end-to-end workflow of receiving a guest on arrival, verifying
          identity and reservation, assigning equipment, capturing waivers,
          and confirming the guest's participation in their scheduled adventure.

      - id: CAP-2.2
        name: Adventure Scheduling
        level: L2
        description: >
          Constructing, publishing, and updating daily adventure schedules,
          including guide assignment, capacity management, and cancellation handling.

      - id: CAP-2.3
        name: Live Adventure Tracking
        level: L2
        description: >
          Monitoring the real-time location, status, and safety of adventure groups
          during active adventures.

  - id: CAP-3
    name: Booking and Commerce
    level: L1
    description: >
      Capabilities covering the end-to-end booking lifecycle: search, selection,
      reservation, payment, and modification.
    children:
      - id: CAP-3.1
        name: Reservation Management
        level: L2
        description: >
          Creating, modifying, and cancelling guest reservations; enforcing
          capacity constraints; maintaining reservation lifecycle state.

      - id: CAP-3.2
        name: Payment Processing
        level: L2
        description: >
          Authorizing, capturing, and refunding payment transactions through
          third-party payment gateway integrations.
```

### JSON Schema excerpt

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Capability Hierarchy",
  "type": "object",
  "required": ["capabilities"],
  "properties": {
    "capabilities": {
      "type": "array",
      "items": { "$ref": "#/definitions/L1Capability" }
    }
  },
  "definitions": {
    "L1Capability": {
      "type": "object",
      "required": ["id", "name", "level", "description"],
      "properties": {
        "id": { "type": "string", "pattern": "^CAP-[0-9]+$" },
        "name": { "type": "string" },
        "level": { "type": "string", "enum": ["L1"] },
        "description": { "type": "string" },
        "children": {
          "type": "array",
          "items": { "$ref": "#/definitions/L2Capability" }
        }
      }
    },
    "L2Capability": {
      "type": "object",
      "required": ["id", "name", "level", "description"],
      "properties": {
        "id": { "type": "string", "pattern": "^CAP-[0-9]+\\.[0-9]+$" },
        "name": { "type": "string" },
        "level": { "type": "string", "enum": ["L2"] },
        "description": { "type": "string" }
      }
    }
  }
}
```

---

## The Capability Changelog Schema

The capability changelog is the second half of Pillar F. It is the journal of architectural
growth — a record of which capabilities changed, when, in which solution, and what new L3
capabilities emerged from the work.

### capability-changelog.yaml

```yaml
# architecture/metadata/capability-changelog.yaml
$schema: "./schemas/capability-changelog.schema.json"

changes:
  - ticket: NTK-10005
    date: 2026-01-15
    summary: RFID wristband tap added as an identity verification method at check-in
    capabilities:
      - id: CAP-2.1
        impact: enhanced
        description: >
          The check-in workflow now accepts NFC/RFID wristband tap as a valid identity
          verification method alongside the existing four-field form entry.
        l3_capabilities:
          - name: RFID Wristband Identity Verification
            description: >
              Guest identity confirmed by reading a pre-assigned NFC wristband at the
              check-in kiosk. The wristband ID is resolved to a guest profile via
              svc-guest-profiles before confirmation is issued.
    decisions:
      - ADR-003
      - ADR-007
    solution_design: architecture/solutions/_NTK-10005-wristband-rfid-field/NTK-10005-solution-design.md

  - ticket: NTK-10006
    date: 2026-02-01
    summary: Live adventure tracking session initiation via event-driven architecture
    capabilities:
      - id: CAP-2.3
        impact: new
        description: >
          The Live Adventure Tracking capability did not previously exist. This solution
          introduces the event-driven session initiation workflow as the foundation for
          real-time group monitoring.
        l3_capabilities:
          - name: Adventure Session Initiation
            description: >
              A check-in completion event triggers the creation of a live tracking session
              for the adventure group. The session includes guide ID, guest roster, and
              assigned adventure category.
          - name: Guide Location Event Ingestion
            description: >
              The tracking service subscribes to guide device location events published
              at configurable intervals during active adventures.
    decisions:
      - ADR-014
    solution_design: architecture/solutions/_NTK-10006-adventure-tracking/NTK-10006-solution-design.md
```

### Changelog schema structure

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Capability Changelog",
  "type": "object",
  "required": ["changes"],
  "properties": {
    "changes": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["ticket", "date", "summary", "capabilities"],
        "properties": {
          "ticket": { "type": "string", "pattern": "^[A-Z]+-[0-9]+$" },
          "date": { "type": "string", "format": "date" },
          "summary": { "type": "string" },
          "capabilities": {
            "type": "array",
            "items": {
              "type": "object",
              "required": ["id", "impact", "description"],
              "properties": {
                "id": {
                  "type": "string",
                  "pattern": "^CAP-[0-9]+(\\.[0-9]+)?$"
                },
                "impact": {
                  "type": "string",
                  "enum": ["new", "enhanced", "fixed", "deprecated"]
                },
                "description": { "type": "string" },
                "l3_capabilities": {
                  "type": "array",
                  "items": {
                    "type": "object",
                    "required": ["name", "description"],
                    "properties": {
                      "name": { "type": "string" },
                      "description": { "type": "string" }
                    }
                  }
                }
              }
            }
          },
          "decisions": {
            "type": "array",
            "items": { "type": "string", "pattern": "^ADR-[0-9]+" }
          },
          "solution_design": { "type": "string" }
        }
      }
    }
  }
}
```

### Impact taxonomy

| Impact value | Meaning |
|-------------|---------|
| `new` | The capability did not previously exist. This solution introduces it. |
| `enhanced` | The capability existed but has been improved — new methods, better coverage, additional edge cases handled. |
| `fixed` | A defect in an existing capability has been corrected. |
| `deprecated` | The capability is being retired. May be replaced by another capability. |

---

## The Canonical Source Rule

A critical governance constraint prevents the system from becoming inconsistent:

**The capability changelog is the single source of truth for delivered capability impacts. Ticket
metadata (e.g., `tickets.yaml`) MUST NOT duplicate capability mapping data for delivered tickets.**

Only unsolved tickets use a `planned_capabilities` field in the ticket registry. Once a ticket is
delivered, capability mapping is derived exclusively from the changelog. Generators read the
changelog — not the ticket registry — to produce capability pages, traceability matrices, and
coverage reports.

This rule eliminates the most common data integrity failure in capability tracking: two places that
claim to be authoritative, which diverge over time.

---

## Generator Architecture

The two capability files drive a cascade of generated outputs:

### 1. Capability profile pages

Generated to `portal/docs/capabilities/{cap-id}.md`. Each L2 capability page renders:

- Definition and L1 parent context
- All L3 capabilities delivered to date (from the changelog)
- Timeline of changes (by ticket and date)
- Linked ADRs governing this capability
- Coverage indicator: does the capability have corresponding test feature files? (cross-reference to Pillar I)

### 2. Capability summary table

An index page listing all L1/L2 capabilities with their L3 capability count and last-modified date.
This is the portfolio dashboard: leadership can see at a glance how many capabilities exist at each
level and when each was last touched.

### 3. Traceability matrix

A generated matrix cross-referencing tickets, capabilities, and ADRs:

| Ticket | Capability | Impact | ADRs |
|--------|-----------|--------|------|
| NTK-10005 | CAP-2.1 Guest Check-in | enhanced | ADR-003, ADR-007 |
| NTK-10006 | CAP-2.3 Live Adventure Tracking | new | ADR-014 |

### 4. Coverage gap report

A report listing L2 capabilities that have no delivered L3 capabilities. These are capabilities
declared in the hierarchy but not yet backed by delivered work. The gap report surfaces the planning
vs. delivery discrepancy.

---

## CI Integration

```yaml
# .github/workflows/validate-capabilities.yml (excerpt)

- name: Validate capabilities.yaml schema
  run: |
    npx ajv validate \
      --schema architecture/metadata/schemas/capabilities.schema.json \
      --data architecture/metadata/capabilities.yaml

- name: Validate capability-changelog.yaml schema
  run: |
    npx ajv validate \
      --schema architecture/metadata/schemas/capability-changelog.schema.json \
      --data architecture/metadata/capability-changelog.yaml

- name: Check changelog capability ID references
  run: |
    python3 scripts/ci/check-capability-refs.py \
      --hierarchy architecture/metadata/capabilities.yaml \
      --changelog architecture/metadata/capability-changelog.yaml

- name: Check solution design changelog completeness
  run: |
    python3 scripts/ci/check-solution-changelog.py \
      --changelog architecture/metadata/capability-changelog.yaml \
      --solutions-dir architecture/solutions/
```

### Validation rules

| Rule | Description |
|------|-------------|
| Hierarchy schema validation | All L1/L2 entries have required fields; ID patterns match their level prefix |
| Changelog schema validation | All changelog entries have required fields; impact values are from the allowed set |
| Changelog ID referential integrity | Every capability ID in the changelog must exist in the capability hierarchy YAML |
| ADR referential integrity | Every ADR reference in the changelog must resolve to an existing file in `decisions/` |
| Solution design completeness | Every folder in `architecture/solutions/` representing a delivered ticket must have a corresponding changelog entry |

The solution design completeness check is the enforcement mechanism for the cultural expectation:
every delivered solution records its capability impacts. Without CI enforcement, this convention
degrades into a manual burden that eventually stops being followed.

---

## AI Fit

Capabilities as Code is the highest-value EaC pillar for AI architecture work. It enables three
AI behaviors that are not possible without a structured capability index:

**Prior-art discovery**: Before authoring a solution design, an AI reads the capability changelog to
find all prior solutions that touched the same capability. It surfaces the ADRs, existing L3
capabilities, and prior design documents. This prevents duplicated work and ensures new solutions
build on, rather than ignore, prior decisions.

**Traceability authoring**: When an AI completes a solution design, it writes the changelog entry.
The structured schema makes this a mechanical task: read the solution design, identify the
capabilities affected, determine impact type, describe the L3 capabilities introduced. The AI
produces a changelog entry that a human reviewer can validate in seconds.

**Portfolio questioning**: Stakeholders can ask "what check-in capabilities do we have?" The AI
reads the capability hierarchy and changelog, aggregates all delivered L3 capabilities under
CAP-2.1, and presents a structured summary with dates and linked tickets.

**Gap identification**: The AI reads the hierarchy and changelog together and surfaces capabilities
that are declared but have no delivered L3 entries — the coverage gap report in natural language.

---

## Governance Model

Capability hierarchy changes (adding L1/L2 entries) MUST be reviewed by the architecture practice
lead. L1 capability additions represent a strategic claim that a new business domain exists; this
has organizational implications beyond the architecture practice.

Capability changelog entries are authored as part of solution design PRs. They are reviewed as part
of the solution design review, not as a separate process.

L3 capability names SHOULD be chosen from the domain ubiquitous language (Pillar AI). An L3
capability named "RFID Wristband Identity Verification" uses terms that must be consistent with
how those terms are defined in the glossary — and if the terms are not yet in the glossary, the
solution PR that introduces them should add glossary entries alongside the changelog entry.

---

## Recommended Practices

1. **Keep the L1/L2 hierarchy stable and small.** A hierarchy of 30-50 L2 entries is manageable
   and meaningful. A hierarchy of 200 entries is unmaintainable. If a new domain genuinely needs
   to be added at L1, it requires architecture practice lead review and should be rare.

2. **Let L3 capabilities emerge; do not plan them.** L3 capabilities are recorded after delivery,
   not planned before. Attempting to pre-declare L3 capabilities produces speculative entries that
   diverge from what is actually built.

3. **Enforce the changelog in CI.** Without CI enforcement, the changelog falls behind within one
   sprint. The check-solution-changelog.py script (or equivalent) is not optional.

4. **Never duplicate capability data between the changelog and the ticket registry.** The canonical
   source rule (see above) prevents the most common drift failure. Enforce it by removing any
   `capabilities` or `decisions` fields from ticket YAML entries that correspond to delivered work.

5. **Link L3 capabilities to test feature files.** An L3 capability without a corresponding
   Gherkin feature file (Pillar I) is a capability delivered without a behavioral specification.
   The coverage gap report should surface this.

6. **Use the capability ID as the cross-reference key, not the name.** Capability names will be
   refined over time. The ID (e.g., `CAP-2.1`) is stable and is the correct reference key in
   ADRs, solution designs, and generated artifacts.

---

## Synthetic Exemplar Status

> The status below describes how Pillar F has been implemented in the NovaTrek Adventures
> synthetic exemplar workspace. NovaTrek data is entirely fictional — no corporate systems are
> represented.

| Artifact | Status | Location |
|----------|--------|----------|
| Capability hierarchy YAML | Implemented — 34 L2 capabilities across 8 L1 domains | `architecture/metadata/capabilities.yaml` |
| JSON Schema for hierarchy | Not yet authored | `architecture/metadata/schemas/capabilities.schema.json` |
| Capability changelog YAML | Implemented — entries for all delivered solutions | `architecture/metadata/capability-changelog.yaml` |
| JSON Schema for changelog | Not yet authored | `architecture/metadata/schemas/capability-changelog.schema.json` |
| Capability portal pages | Partially generated | `portal/docs/capabilities/` |
| Traceability matrix | Not yet generated | — |
| CI schema validation | Not yet wired | `.github/workflows/validate-capabilities.yml` |
| Solution changelog completeness check | Not yet wired | — |

The capability hierarchy and changelog are the most fully realized artifacts in the NovaTrek
exemplar — they have been actively used across all solution designs. The gap is in the schema
validation infrastructure (JSON Schema files not yet authored) and CI enforcement (completeness
check not yet wired). Both are Wave 2 backlog items.

---

## Forward Plan

Pillar F adoption for NovaTrek is planned in **Wave 2** of the Transformation Plan, alongside
Decisions as Code (Pillar G) and Actors as Code (Pillar C). See
[Transformation Plan — Pillar F](TRANSFORMATION-PLAN.md#pillar-f--capabilities-as-code) for the
sequenced adoption checklist.

Key adoption prerequisite: Applications as Code (Pillar D) SHOULD be complete before the capability
changelog is used in production, because changelog entries reference service names that must resolve
against the application registry. The hierarchy itself can be authored independently of Pillar D.

---

## References

- Gartner Business Capability Modeling — methodology for constructing L1/L2 capability hierarchies
- TOGAF 10, Architecture Content Framework — Architecture Building Blocks (ABBs) as a related concept
- Wardley Mapping (Simon Wardley) — an alternative capability-evolution representation, useful for strategic planning alongside this registry-based model
- Eric Evans, *Domain-Driven Design* (2003) — Chapter 15: Distillation (core domain vs. supporting subdomain)
- NovaTrek EaC Framework: [Pillar F definition](EVERYTHING-AS-CODE-FRAMEWORK.md)
- NovaTrek Transformation Plan: [Pillar F adoption steps](TRANSFORMATION-PLAN.md#pillar-f--capabilities-as-code)
