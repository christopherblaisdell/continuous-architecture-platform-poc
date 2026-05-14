# Ubiquitous Language as Code — A First-Class EaC Pillar (Blueprint)

> **BLUEPRINT DOCUMENT.** This is the portable definition of Pillar AI — Ubiquitous Language as
> Code. It describes a pattern applicable to any software architecture practice. References to
> NovaTrek Adventures services and files are synthetic exemplar data used to validate the pattern,
> not corporate information. See [Synthetic Exemplar Status](#synthetic-exemplar-status) for
> details.

**Status**: This is Pillar AI of the Everything as Code framework — see [EaC Framework](EVERYTHING-AS-CODE-FRAMEWORK.md).

---

## Why Ubiquitous Language Belongs in EaC

Eric Evans introduced the concept of Ubiquitous Language in *Domain-Driven Design* (2003): a
shared vocabulary between domain experts and software engineers, expressed consistently in all
artifacts — conversations, documents, models, and code. The language is "ubiquitous" because
it should appear the same way everywhere.

In practice, the ubiquitous language degrades. The booking domain uses "reservation". The
operations domain uses "booking". The analytics service schema uses "trip". The event payload
uses "journey". The guest mobile app uses "adventure". These are all the same concept. Each
inconsistency creates a translation tax: every developer working across domains must maintain
a mental mapping, every API integration requires a field-level mapping document, every new hire
must learn the unofficial glossary by making mistakes.

Making the domain vocabulary a version-controlled artifact addresses this directly:

| Property | Requirement |
|----------|-------------|
| Consistency | One canonical form per concept; synonyms and deprecated aliases declared explicitly |
| Traceability | Terms link to the services that use them, the ADRs that formalized them, and the bounded contexts they belong to |
| Evolvability | Renaming a term is a PR with reviewers and a deprecation trail |
| AI legibility | AI agents read the glossary to use correct terminology in generated artifacts |
| Naming governance | Optional CI lint checks verify that new API fields and event names use canonical forms |

---

## The Core Problem: Naming Inconsistency as an Architectural Defect

Terminology inconsistency is not merely a style problem. It is an architectural defect with
observable consequences:

**Data mapping bugs**: A service that refers to `customer_id` in its database sends `guestIdentifier`
in its events. A downstream consumer queries for `guest_id`. These three refer to the same thing,
but the inconsistency causes silent mapping failures when a new integration is built.

**Bounded context confusion**: When the operations team and the product team both define "adventure"
differently (the operations team's definition includes scheduling constraints; the product team's
definition includes pricing) and neither definition is documented, the check-in service receives
conflicting requirements about which definition to implement.

**AI hallucination vector**: An AI assistant asked to write a migration from the reservations schema
to the analytics schema must guess that `guest_id` and `customer_id` are the same. If the glossary
makes this mapping explicit, the AI does not guess.

**Onboarding friction**: New engineers spend weeks discovering that "member" in the loyalty service
means something slightly different from "guest" in the profiles service. The glossary makes this
visible on day one.

---

## Bounded Contexts in the Glossary

The glossary is not a flat list of terms. Each term is owned by a bounded context (Eric Evans,
DDD Chapter 14). Within its bounded context, a term has a precise definition. Across bounded
contexts, the same real-world concept may carry a different name and a slightly different meaning —
and this divergence is intentional and legitimate.

The glossary records:
- The canonical form within each bounded context
- The cross-context translations (where the same concept has different names in different contexts)
- Deprecated aliases that remain in legacy code

---

## The Glossary Schema

### glossary.yaml

```yaml
# architecture/metadata/glossary.yaml
$schema: "./schemas/glossary.schema.json"

terms:
  # --- Guest Identity bounded context ---
  - id: term-guest
    term: Guest
    bounded_context: Guest Identity
    definition: >
      A NovaTrek customer who has a verified account with the platform. A Guest has a
      persistent identity record in svc-guest-profiles with a stable `guest_id`. Guests
      are distinguished from anonymous visitors (who have not created an account) and
      from historical reservation records that predate the guest profile system.
    canonical_form: guest
    canonical_field_name: guest_id
    synonyms:
      - customer
      - member
      - traveler
    deprecated_aliases:
      - passenger
      - client
    cross_context_equivalents:
      - context: Loyalty and Rewards
        term: Member
        note: >
          In the Loyalty context, a Guest becomes a Member when enrolled in the rewards
          program. Not all Guests are Members. Member-specific data (tier, points balance)
          is owned by svc-loyalty-rewards.
    used_in:
      - svc-guest-profiles
      - svc-check-in
      - svc-reservations
      - svc-safety-compliance
      - svc-notifications
    adrs:
      - ADR-007
      - ADR-008
    created: 2025-08-01
    last_reviewed: 2026-01-01

  # --- Product Catalog bounded context ---
  - id: term-adventure
    term: Adventure
    bounded_context: Product Catalog
    definition: >
      A NovaTrek product offering: a scheduled, guided outdoor experience. An Adventure
      has a catalog definition (svc-trip-catalog: type, duration, difficulty, price) and
      one or more scheduled instances (svc-scheduling-orchestrator: date, guide, capacity).
      A Reservation is a Guest's commitment to attend a specific Adventure instance.
    canonical_form: adventure
    canonical_field_name: adventure_id
    synonyms:
      - trip
      - tour
      - experience
      - outing
    deprecated_aliases: []
    cross_context_equivalents:
      - context: Operations
        term: Schedule Item
        note: >
          In the Operations context, an Adventure becomes a Schedule Item when it has been
          assigned a guide and a date. The operational view emphasizes guide assignment and
          capacity; the catalog view emphasizes product definition and pricing.
    used_in:
      - svc-trip-catalog
      - svc-check-in
      - svc-reservations
      - svc-trail-management
      - svc-safety-compliance
    adrs: []
    created: 2025-08-01
    last_reviewed: 2026-01-01

  # --- Booking bounded context ---
  - id: term-reservation
    term: Reservation
    bounded_context: Booking
    definition: >
      A Guest's confirmed commitment to attend a specific Adventure instance on a specific
      date. A Reservation has a lifecycle: pending payment -> confirmed -> checked-in ->
      completed -> cancelled. A Reservation is not the same as a payment — a Reservation
      can exist in pending state before payment clears.
    canonical_form: reservation
    canonical_field_name: reservation_id
    synonyms:
      - booking
    deprecated_aliases:
      - order
    cross_context_equivalents:
      - context: Operations
        term: Check-in Record
        note: >
          When a Guest with a confirmed Reservation arrives on the day of the adventure,
          the check-in process creates a Check-in Record (owned by svc-check-in). The
          Reservation is the pre-adventure artifact; the Check-in Record is the
          day-of-adventure artifact.
    used_in:
      - svc-reservations
      - svc-check-in
      - svc-scheduling-orchestrator
      - svc-payments
    adrs:
      - ADR-007
    created: 2025-08-01
    last_reviewed: 2026-01-01

  # --- Operations bounded context ---
  - id: term-check-in
    term: Check-in
    bounded_context: Operations
    definition: >
      The day-of-adventure process by which a Guest's identity is verified, their waiver
      status is confirmed, and they are formally marked as present for their reserved
      Adventure. Check-in may be performed via kiosk self-service (Patterns 1 and 2) or
      with full staff assistance (Pattern 3). The check-in record is the operational
      confirmation that a Guest has physically arrived.
    canonical_form: check-in
    canonical_field_name: checkin_id
    synonyms:
      - arrival
      - registration
    deprecated_aliases: []
    used_in:
      - svc-check-in
      - svc-scheduling-orchestrator
      - svc-notifications
    adrs:
      - ADR-005
      - ADR-006
      - ADR-007
    created: 2025-09-01
    last_reviewed: 2026-01-01

  - id: term-check-in-pattern
    term: Check-in Pattern
    bounded_context: Operations
    definition: >
      One of three standardized check-in workflows, differentiated by the level of staff
      involvement and equipment verification required. Pattern 1 (Basic): self-service kiosk
      with minimal equipment. Pattern 2 (Guided): guide-assisted with moderate equipment
      verification. Pattern 3 (Full Service): full staff-assisted with extensive safety
      gear and waiver review. Unknown adventure categories MUST default to Pattern 3.
    canonical_form: check-in pattern
    canonical_field_name: checkin_pattern
    synonyms:
      - check-in flow
      - check-in mode
    deprecated_aliases: []
    used_in:
      - svc-check-in
      - svc-trip-catalog
    adrs:
      - ADR-004
      - ADR-005
    created: 2025-09-15
    last_reviewed: 2026-01-01

  - id: term-daily-schedule
    term: Daily Schedule
    bounded_context: Operations
    definition: >
      The master operational plan for a single date, owned exclusively by
      svc-scheduling-orchestrator. A Daily Schedule contains zero or more Schedule Entries
      (each representing one Adventure instance), guide assignments, capacity allocations,
      and status (draft, published, locked). Only svc-scheduling-orchestrator may mutate a
      Daily Schedule.
    canonical_form: daily schedule
    canonical_field_name: schedule_id
    synonyms:
      - schedule
      - run sheet
    deprecated_aliases: []
    used_in:
      - svc-scheduling-orchestrator
      - svc-guide-management
      - svc-check-in
    adrs:
      - ADR-010
      - ADR-011
    created: 2025-11-01
    last_reviewed: 2026-01-01

  # --- Safety bounded context ---
  - id: term-waiver
    term: Waiver
    bounded_context: Safety
    definition: >
      A digitally signed legal document in which a Guest acknowledges the risks of a
      specific Adventure category and releases NovaTrek from liability. Waivers are owned
      by svc-safety-compliance. A valid, current waiver is a prerequisite for completing
      check-in for Pattern 2 and Pattern 3 adventures.
    canonical_form: waiver
    canonical_field_name: waiver_id
    synonyms:
      - liability waiver
      - release form
    deprecated_aliases:
      - consent form
    used_in:
      - svc-safety-compliance
      - svc-check-in
    adrs: []
    created: 2025-09-01
    last_reviewed: 2026-01-01
```

### JSON Schema excerpt

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Domain Glossary",
  "type": "object",
  "required": ["terms"],
  "properties": {
    "terms": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "term", "bounded_context", "definition", "canonical_form", "used_in", "created"],
        "properties": {
          "id": { "type": "string", "pattern": "^term-[a-z0-9-]+$" },
          "term": { "type": "string" },
          "bounded_context": { "type": "string" },
          "definition": { "type": "string" },
          "canonical_form": { "type": "string" },
          "canonical_field_name": { "type": "string", "pattern": "^[a-z][a-z0-9_]*$" },
          "synonyms": { "type": "array", "items": { "type": "string" } },
          "deprecated_aliases": { "type": "array", "items": { "type": "string" } },
          "cross_context_equivalents": {
            "type": "array",
            "items": {
              "type": "object",
              "required": ["context", "term"],
              "properties": {
                "context": { "type": "string" },
                "term": { "type": "string" },
                "note": { "type": "string" }
              }
            }
          },
          "used_in": { "type": "array", "items": { "type": "string" } },
          "adrs": { "type": "array", "items": { "type": "string", "pattern": "^ADR-[0-9]+" } },
          "created": { "type": "string", "format": "date" },
          "last_reviewed": { "type": "string", "format": "date" }
        }
      }
    }
  }
}
```

### Field reference

| Field | Required | Description |
|-------|----------|-------------|
| `id` | Yes | Unique identifier following `term-{kebab-slug}` pattern |
| `term` | Yes | The canonical display name of the term (Title Case) |
| `bounded_context` | Yes | The domain bounded context that owns this definition |
| `definition` | Yes | The precise, substantive definition of the term within its bounded context |
| `canonical_form` | Yes | The single approved spelling and casing for use in all new artifacts (lowercase) |
| `canonical_field_name` | No | The exact field name format (snake_case) for use in API contracts, database schemas, and events |
| `synonyms` | No | Alternative terms that mean the same thing and are acceptable (but not preferred) |
| `deprecated_aliases` | No | Terms that were previously used, may appear in legacy code, but MUST NOT be used in new artifacts |
| `cross_context_equivalents` | No | Mappings to equivalent terms in other bounded contexts, with explanatory notes |
| `used_in` | Yes | Service IDs where this term appears in API contracts, schemas, or event payloads |
| `adrs` | No | ADR IDs that formalized or constrained the use of this term |
| `created` | Yes | ISO 8601 date when the term was first declared |
| `last_reviewed` | No | ISO 8601 date of most recent review |

---

## Generator Architecture

### 1. Searchable glossary portal page

Generated to `portal/docs/glossary/index.md`. The page renders terms grouped by bounded context,
with each entry showing the canonical form, definition, synonyms, deprecated aliases, service
usage, and ADR links. A cross-reference section shows each term's equivalents in other bounded
contexts.

### 2. Bounded context translation matrix

A generated table showing, for each pair of bounded contexts that share concepts, the term
mappings. This is the machine-readable version of the "context map" from Domain-Driven Design —
the explicit record of how concepts translate across context boundaries.

### 3. Deprecated alias report

A generated report listing every deprecated alias, the service or event that most recently used it
(if detectable), and a recommendation to migrate to the canonical form. This report drives naming
cleanup backlog items.

---

## CI Integration

### Schema and referential integrity validation

```yaml
# .github/workflows/validate-glossary.yml (excerpt)

- name: Validate glossary.yaml schema
  run: |
    npx ajv validate \
      --schema architecture/metadata/schemas/glossary.schema.json \
      --data architecture/metadata/glossary.yaml

- name: Referential integrity — service references
  run: |
    python3 scripts/ci/check-glossary-service-refs.py \
      --glossary architecture/metadata/glossary.yaml \
      --services architecture/metadata/services.yaml

- name: Referential integrity — ADR references
  run: |
    python3 scripts/ci/check-glossary-adr-refs.py \
      --glossary architecture/metadata/glossary.yaml \
      --decisions-dir decisions/
```

### Optional: Naming linter

The naming linter is an optional CI step that checks new or modified OpenAPI spec files, AsyncAPI
event schemas, and database migration scripts for field names that match deprecated aliases or
synonym forms where a canonical field name has been declared.

```yaml
- name: Naming lint (optional)
  run: |
    python3 scripts/ci/naming-lint.py \
      --glossary architecture/metadata/glossary.yaml \
      --check-files "architecture/specs/**/*.yaml" \
      --check-files "architecture/events/**/*.yaml" \
      --report naming-lint-report.json
```

The naming linter does not block PRs by default — it reports findings as warnings. Promoting it to
a blocking check requires a governance decision: naming lint errors must be triaged to distinguish
legitimate bounded-context-appropriate variation from genuine canonical form violations.

---

## AI Fit

A machine-readable glossary enables AI behaviors that significantly improve generated artifact
quality:

**Terminology consistency in generated artifacts**: When an AI generates an OpenAPI spec, impact
assessment, ADR, or user story, it reads the glossary to use canonical forms. Instead of writing
"customer" or "traveler" in a new API spec, it writes "guest". Instead of "order", it writes
"reservation".

**Bounded context awareness in solution design**: When an AI proposes a solution that crosses
bounded context boundaries, it reads the cross_context_equivalents fields to identify where
explicit translation is needed. "The check-in service calls the reservations API using `booking_id`
— note that the canonical form in the Booking context is `reservation_id`. This mapping should be
made explicit in the contract."

**Deprecated alias detection**: When an AI reviews a PR that adds new API fields, it reads the
glossary and flags any field names that match deprecated aliases. "The new field `customer_id` in
`svc-notifications` appears to be a deprecated alias for `guest_id`. See glossary term `term-guest`."

**Onboarding Q&A**: An AI assistant can answer "what is the difference between a Guest and a
Member?" from the glossary, with accurate bounded-context-aware definitions rather than
synthesizing an answer from codebase context.

---

## Governance Model

The domain glossary is one of the highest-authority artifacts in the practice. Terminology changes
ripple through all layers of the stack: API contracts, database schemas, event payloads, test
fixtures, and documentation.

Governance rules for the glossary:

- **Adding a term**: PR review required. New terms must have a precise definition, a canonical
  form, and at least one service in `used_in`. Terms that represent new domain concepts should be
  accompanied by or reference the ADR that introduced the concept.

- **Changing a term's canonical form**: This is a breaking change. It requires a deprecation
  migration plan: the old canonical form becomes a deprecated alias, CI/CD lint warnings fire until
  the old form is replaced in all artifacts, and the migration is tracked as a backlog item.

- **Adding a deprecated alias**: Permitted at any time. Deprecated aliases record what was used
  before; they do not authorize using the alias in new artifacts.

- **Cross-context equivalent changes**: Treated like other term changes. Adding a new cross-context
  equivalent is additive and non-breaking. Removing one (because the contexts merged or separated)
  requires the same PR review as a term change.

---

## Recommended Practices

1. **Audit the current terminology before authoring the first glossary entry.** Scan existing API
   specs, event schemas, and database schemas for the same real-world concept expressed differently.
   The audit output is the list of synonyms, deprecated aliases, and cross-context equivalents to
   declare. Do not start with an empty glossary — start with the terms that have already diverged.

2. **Assign each term to exactly one bounded context.** If a term spans multiple bounded contexts
   with identical meaning, this is a signal that the contexts may not be properly separated. If the
   meanings genuinely differ across contexts, they are different terms that happen to share a name —
   and that ambiguity is the most dangerous kind. Separate them.

3. **The canonical field name drives API contracts.** When `canonical_field_name: guest_id` is
   declared, all new API endpoints MUST use `guest_id` for this concept. The naming linter enforces
   this automatically. If the canonical form differs from the most common current usage, plan for a
   phased migration rather than a flag day.

4. **Preserve deprecated aliases forever.** A deprecated alias may appear in a log entry, a
   database column, a legacy API that cannot be changed, or an integration test fixture. Deleting
   it from the glossary makes the alias invisible — but it does not make it disappear from the
   codebase. Preservation with a `deprecated_aliases` flag is the correct approach.

5. **The glossary is a design artifact, not a documentation artifact.** It should be authored
   during domain modeling, not written after the software ships. If the glossary is being written
   after the fact, that is fine — but recognize that the naming inconsistencies already embedded
   in the code are technical debt that the glossary is documenting, not resolving.

6. **Review the glossary when new bounded contexts are introduced.** Every new service is an
   opportunity to introduce new terminology. Require every new service's first PR to include a
   glossary contribution for any domain terms introduced.

---

## Synthetic Exemplar Status

> The status below describes how Pillar AI has been implemented in the NovaTrek Adventures
> synthetic exemplar workspace. NovaTrek data is entirely fictional — no corporate systems are
> represented.

| Artifact | Status | Location |
|----------|--------|----------|
| Domain glossary YAML | Not yet created — planned in Transformation Wave 2 | `architecture/metadata/glossary.yaml` |
| JSON Schema | Not yet created | `architecture/metadata/schemas/glossary.schema.json` |
| Glossary portal page | Not yet generated | `portal/docs/glossary/index.md` |
| Naming linter script | Not yet created | `scripts/ci/naming-lint.py` |
| CI schema validation | Not yet wired | `.github/workflows/validate-glossary.yml` |

The NovaTrek workspace exhibits several pre-glossary naming inconsistencies that the glossary would
resolve: "guest" vs "customer" across specs; "adventure" vs "trip" in some event payload names;
"check-in" vs "checkin" (hyphenation) in field names across services. These inconsistencies are the
primary motivation for Wave 2 Ubiquitous Language adoption.

---

## Forward Plan

Pillar AI adoption for NovaTrek is planned in **Wave 2** of the Transformation Plan, alongside
Architecture Principles as Code (Pillar AH) and Capabilities as Code (Pillar F). Wave 2 establishes
the vocabulary and governance infrastructure that make all later pillars interpretable by AI agents.
See [Transformation Plan — Pillar AI](TRANSFORMATION-PLAN.md#pillar-ai--ubiquitous-language-as-code)
for the sequenced adoption checklist.

---

## References

- Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software* (2003) — the origin of Ubiquitous Language as a design concept
- Eric Evans and Martin Fowler, *Domain Driven Design Reference* (2015) — Context Maps and Bounded Context vocabulary
- Vaughn Vernon, *Implementing Domain-Driven Design* (2013) — Chapter 2: Domains, Subdomains, and Bounded Contexts
- Sam Newman, *Building Microservices* (2021, 2nd ed.) — Chapter 2: How to Model Services (bounded context as the primary driver of service boundaries)
- NovaTrek EaC Framework: [Pillar AI definition](EVERYTHING-AS-CODE-FRAMEWORK.md)
- NovaTrek Transformation Plan: [Pillar AI adoption steps](TRANSFORMATION-PLAN.md#pillar-ai--ubiquitous-language-as-code)
