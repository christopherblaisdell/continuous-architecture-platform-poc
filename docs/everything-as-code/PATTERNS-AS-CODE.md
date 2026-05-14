# Patterns and Anti-patterns as Code — A First-Class EaC Pillar (Blueprint)

> **BLUEPRINT DOCUMENT.** This is the portable definition of Pillar AK — Patterns and
> Anti-patterns as Code. It describes a pattern applicable to any software architecture practice.
> References to NovaTrek Adventures services and files are synthetic exemplar data used to validate
> the pattern, not corporate information. See [Synthetic Exemplar Status](#synthetic-exemplar-status)
> for details.

**Status**: This is Pillar AK of the Everything as Code framework — see [EaC Framework](EVERYTHING-AS-CODE-FRAMEWORK.md).

---

## Why Patterns and Anti-patterns Belong in EaC

Design patterns are reusable solutions to recurring design problems (Gang of Four, 1994;
Fowler's Patterns of Enterprise Application Architecture, 2002; microservice patterns, Richardson
2018). Anti-patterns are recurring design mistakes with known harmful effects and known remediation
paths (Brown et al., *AntiPatterns*, 1998).

In most architecture practices, patterns and anti-patterns exist in informal channels:
onboarding presentations, internal wiki pages, ADR prose, and reviewer intuition. The result:

- Different reviewers apply different standards — one flags the shared database anti-pattern,
  another does not notice it
- New engineers repeatedly introduce the same anti-patterns that senior engineers have seen and
  solved before
- There is no machine-readable inventory of which patterns are approved, which are rejected, and
  which are currently under remediation
- AI agents have no structured catalog to consult when evaluating architectural proposals

Making the pattern catalog version-controlled and machine-readable produces a shared, consistent,
queryable knowledge base that improves both human and AI architectural reasoning.

---

## The Fundamental Distinction: Pattern vs Anti-pattern

A **pattern** is a named, reusable solution to a specific category of design problem. Patterns are
declared with `type: pattern` in the registry and have an `approved` status when they represent
the practice's preferred approach.

An **anti-pattern** is a named, recognized design mistake: an approach that initially appears
reasonable but produces known harmful effects in certain contexts. Anti-patterns are declared with
`type: anti-pattern` in the registry and have a `rejected` status. Crucially, every anti-pattern
entry includes:

- **The harm it causes** (not just a prohibition — engineers need to understand why)
- **A remediation path** (how to replace it with an approved approach)
- **Known occurrences** (which services currently exhibit this pattern, and their remediation status)
- **An approved alternative** (the pattern that should replace it)

The known occurrences field is the most operationally valuable field in the registry. It converts
the anti-pattern catalog from a reference document into a living remediation backlog.

---

## The Patterns Registry Schema

### patterns.yaml

```yaml
# architecture/metadata/patterns.yaml
$schema: "./schemas/patterns.schema.json"

entries:
  # =========================================================================
  # APPROVED PATTERNS
  # =========================================================================

  - id: PAT-001
    name: Saga Pattern
    type: pattern
    category: distributed-transactions
    status: approved
    problem: >
      Maintaining data consistency across multiple services without distributed transactions
      (2PC). Distributed transactions couple services at the commit level and are incompatible
      with independent service deployment.
    solution: >
      Decompose the business transaction into a sequence of local transactions, one per service.
      Each local transaction publishes an event or message that triggers the next step.
      Two implementation styles: choreography (services react to events) and orchestration
      (a central orchestrator issues commands to each service and handles failures).
      Failed steps trigger compensating transactions that undo the preceding steps.
    consequences:
      positive:
        - No distributed transaction coordinator required
        - Services remain loosely coupled and can be deployed independently
        - Failures are handled by compensating transactions without global rollback
      negative:
        - Rollback requires explicitly authored compensating transactions for each step
        - Saga state is eventually consistent — intermediate states are visible
        - Debugging is harder than in a synchronous transactional model
    governing_adrs:
      - ADR-006
    applied_in:
      - service: svc-check-in
        note: >
          The check-in orchestration flow (identity verification -> waiver check ->
          schedule slot claim -> check-in record creation) is implemented as an
          orchestrated saga with svc-check-in as the coordinator.
      - service: svc-scheduling-orchestrator
        note: >
          Schedule publishing uses an orchestrated saga: draft -> guide notification ->
          capacity lock -> published.
    related_patterns:
      - PAT-003
    tags:
      - consistency
      - distributed-systems
      - event-driven
    created: 2025-09-01
    last_reviewed: 2026-01-01

  - id: PAT-002
    name: API-Mediated Data Access
    type: pattern
    category: data-ownership
    status: approved
    problem: >
      Services need to read data owned by another service. Direct database access couples
      the services at the schema level and violates the service ownership boundary.
    solution: >
      The owning service exposes a read API (REST GET endpoint). All consumers call this
      API; no consumer accesses the owning service's database directly. The owning service
      controls access, enforces business rules on reads, and is free to change its schema
      without breaking consumers.
    consequences:
      positive:
        - Schema changes in the owning service do not break consumers
        - The owning service can add access control, rate limiting, and audit logging
        - Consumer code is independent of the owning service's persistence technology
      negative:
        - Runtime latency for cross-service reads (network hop vs. local query)
        - Requires the owning service to design and maintain a stable read API
        - Cache invalidation complexity when consumers cache read results
    governing_adrs:
      - ADR-003
    applied_in:
      - service: svc-check-in
        note: >
          Reads guest profiles via GET /guests/{guest_id} (svc-guest-profiles API).
          Never queries the guest_profiles database directly.
      - service: svc-reservations
        note: >
          Reads adventure catalog data via svc-trip-catalog API, not the catalog database.
    related_patterns: []
    tags:
      - data-ownership
      - coupling
      - service-boundary
    created: 2025-09-01
    last_reviewed: 2026-01-01

  - id: PAT-003
    name: Transactional Outbox
    type: pattern
    category: event-reliability
    status: approved
    problem: >
      A service must write to its database and publish an event atomically. If the database
      write succeeds but the event publish fails, the system is in an inconsistent state.
      If the event is published before the database write, consumers may react to an event
      that was never committed.
    solution: >
      Write the event to an outbox table in the same local transaction as the primary data
      change. A separate relay process (Debezium CDC, a polling forwarder, or the Outbox
      Event Publisher pattern) reads committed outbox entries and publishes them to the
      message broker. The outbox table is the durable staging area that guarantees at-least-once
      event delivery.
    consequences:
      positive:
        - Event publication is guaranteed for every committed database write
        - No two-phase commit between database and message broker
        - At-least-once delivery with deduplication possible via idempotency keys
      negative:
        - Adds operational complexity: the relay process must be monitored and maintained
        - Small latency increase between database commit and event publication
        - Requires database support for transactional outbox table
    governing_adrs: []
    applied_in: []
    related_patterns:
      - PAT-001
    tags:
      - event-driven
      - reliability
      - consistency
    created: 2025-12-01
    last_reviewed: 2026-01-01

  - id: PAT-004
    name: PATCH Semantics for Partial Updates
    type: pattern
    category: api-design
    status: approved
    problem: >
      A service needs to update a subset of fields on a resource. Using PUT semantics
      (full resource replacement) risks overwriting fields owned by other services or
      set by other processes since the client last read the resource.
    solution: >
      Use PATCH with a sparse payload containing only the fields to be updated. The server
      applies only the provided fields; unspecified fields are unchanged. Combine with
      optimistic locking (PAT-005) when concurrent modification is possible.
    consequences:
      positive:
        - Prevents data overwrite for fields not included in the update payload
        - Clients do not need to fetch the full resource before updating
        - Multiple services can update different subsets of a resource's fields safely
      negative:
        - PATCH semantics are more complex to implement than PUT replacement
        - Requires the server to implement field-level merge logic
        - Partial updates are harder to audit than full resource replacements
    governing_adrs:
      - ADR-010
    applied_in:
      - service: svc-scheduling-orchestrator
        note: >
          Schedule entry updates use PATCH semantics so guide assignment, capacity, and
          status can be updated independently without risk of overwriting concurrent changes.
    related_patterns:
      - PAT-005
    tags:
      - api-design
      - data-integrity
      - http
    created: 2025-11-01
    last_reviewed: 2026-01-01

  - id: PAT-005
    name: Optimistic Locking
    type: pattern
    category: concurrency
    status: approved
    problem: >
      Multiple clients or services may concurrently modify the same resource. Without
      concurrency control, the last write wins — earlier writes are silently overwritten.
    solution: >
      Include a version field (_rev or _version) on every mutable resource. When a client
      reads a resource, it receives the current version. When the client updates the
      resource, it must include the version it read. The server rejects the update with
      HTTP 409 Conflict if the current version does not match — indicating that another
      write has occurred since the client read.
    consequences:
      positive:
        - No database-level locking required
        - Highly concurrent reads with no contention
        - Conflicts are detected at the application level with a precise error response
      negative:
        - Clients must handle 409 Conflict and implement retry-with-re-read logic
        - High contention on frequently written resources increases conflict rate
        - Requires the version field to be propagated to all clients
    governing_adrs:
      - ADR-011
    applied_in:
      - service: svc-scheduling-orchestrator
        note: >
          Daily schedule records carry a `_rev` field. All update operations check `_rev`
          and return 409 on mismatch.
    related_patterns:
      - PAT-004
    tags:
      - concurrency
      - data-integrity
    created: 2025-12-01
    last_reviewed: 2026-01-01

  # =========================================================================
  # REJECTED ANTI-PATTERNS
  # =========================================================================

  - id: ANTI-001
    name: Shared Database
    type: anti-pattern
    category: data-ownership
    status: rejected
    problem: >
      Multiple services read and write the same database tables, typically because they
      were originally part of a monolith or because sharing a database was perceived as
      simpler than defining API contracts.
    harm: >
      Creates tight coupling at the data layer. Services cannot evolve their schemas
      independently — a column rename in one service breaks all other services querying
      that column. Deployments must be coordinated. Data ownership is ambiguous: which
      service is responsible for data integrity when any service can write? This
      anti-pattern undermines the core isolation benefit of service decomposition.
    remediation: >
      Each service takes exclusive ownership of its data. Cross-service reads go through
      the owning service's published API (PAT-002). This migration requires identifying
      the authoritative owner, adding an API, migrating consumers to use the API, and
      removing direct database access from non-owning services.
    approved_alternative: PAT-002
    governing_adrs:
      - ADR-003
    known_occurrences: []
    tags:
      - data-ownership
      - coupling
    created: 2025-09-01
    last_reviewed: 2026-01-01

  - id: ANTI-002
    name: Hardcoded Business Classification
    type: anti-pattern
    category: extensibility
    status: rejected
    problem: >
      Business classification rules (e.g., which adventure categories map to which check-in
      patterns) are embedded as switch statements, if-else chains, or constant maps in
      application source code rather than in externalized configuration.
    harm: >
      Adding a new category or changing a classification requires a code change, test cycle,
      and deployment. The classification becomes invisible to non-engineering stakeholders
      who cannot read source code. The risk of an unmapped category defaulting to an unsafe
      value is higher because the mapping is not inspectable without reading the code.
    remediation: >
      Extract classification rules to a configuration file (YAML, database table, or
      configuration service). The application reads the configuration at startup or on
      a defined refresh cycle. New classifications require only a configuration change —
      no code deployment. Implement safe defaults (PRIN-002) in the loading layer to
      handle unmapped categories.
    approved_alternative: PAT-006
    governing_adrs:
      - ADR-004
      - ADR-005
    known_occurrences:
      - service: svc-check-in
        status: resolved
        resolved_in: ADR-004
        note: >
          The hardcoded switch statement for adventure category to check-in pattern mapping
          was replaced with the configuration-driven classification system in the NTK-10002
          solution design. See config/adventure-classification.yaml.
    tags:
      - extensibility
      - configuration
      - safety
    created: 2025-10-01
    last_reviewed: 2026-01-01

  - id: ANTI-003
    name: Shadow Guest Records
    type: anti-pattern
    category: data-integrity
    status: rejected
    problem: >
      A service maintains its own local copy of guest identity fields (name, contact
      preferences, loyalty tier) instead of delegating to svc-guest-profiles as the
      single source of truth.
    harm: >
      Creates data divergence: the local copy becomes stale as guests update their profiles.
      Guest name changes, contact preference updates, and tier changes are not reflected in
      services maintaining shadow records. This produces incorrect notifications, stale
      personalizations, and loyalty calculation errors. The identity divergence is often
      invisible until a guest complains about the discrepancy.
    remediation: >
      Remove local guest identity fields from the non-owning service. Replace reads from
      local tables with runtime API calls to svc-guest-profiles. For performance-sensitive
      paths, introduce a time-bounded cache with explicit invalidation on guest profile
      update events.
    approved_alternative: PAT-002
    governing_adrs:
      - ADR-007
      - ADR-008
    known_occurrences: []
    tags:
      - data-integrity
      - guest-identity
      - coupling
    created: 2025-10-01
    last_reviewed: 2026-01-01

  - id: ANTI-004
    name: Entity Replacement (PUT as Full Overwrite)
    type: anti-pattern
    category: api-design
    status: rejected
    problem: >
      A service uses PUT semantics with a full entity payload to update a resource, even
      when the client only intends to change a subset of fields. The server replaces the
      entire resource with the client's payload.
    harm: >
      If another process has updated fields not included in the client's payload since the
      client last read the resource, those fields are silently overwritten. This is especially
      dangerous when multiple services update different subsets of a shared resource — each
      service's PUT call undoes the other service's changes.
    remediation: >
      Replace PUT operations with PATCH operations for partial updates (PAT-004). When a
      PUT is semantically correct (the client owns the entire resource and intends to replace
      it), combine it with optimistic locking (PAT-005) to prevent concurrent write conflicts.
    approved_alternative: PAT-004
    governing_adrs:
      - ADR-010
    known_occurrences:
      - service: svc-scheduling-orchestrator
        status: resolved
        resolved_in: ADR-010
        note: >
          The schedule update endpoint was originally implemented as PUT. ADR-010 mandated
          a migration to PATCH semantics with field-level merge logic.
    tags:
      - api-design
      - data-integrity
    created: 2025-11-01
    last_reviewed: 2026-01-01

  - id: ANTI-005
    name: Unsafe Classification Default
    type: anti-pattern
    category: safety
    status: rejected
    problem: >
      When an adventure category cannot be mapped to a check-in pattern (unknown category,
      null input, or configuration error), the system defaults to the least restrictive
      pattern (Pattern 1) rather than the most restrictive.
    harm: >
      Guests assigned to Pattern 1 (self-service kiosk) skip the staff-assisted safety
      checks and waiver verification required for higher-risk adventures. An unmapped
      category that belongs to a high-risk adventure type will receive inadequate safety
      processing. This is a safety liability and a potential duty-of-care failure.
    remediation: >
      The classification loader MUST default all unmapped and null inputs to Pattern 3
      (Full Service). This is the safe conservative default: a low-risk adventure receiving
      Pattern 3 processing causes minor inconvenience; a high-risk adventure receiving
      Pattern 1 processing creates a safety liability. The default is enforced at the
      classification layer, not at the check-in UI layer.
    approved_alternative: PAT-007
    governing_adrs:
      - ADR-005
    known_occurrences: []
    tags:
      - safety
      - defaults
      - classification
    created: 2025-10-15
    last_reviewed: 2026-01-01

  - id: ANTI-006
    name: Distributed Monolith
    type: anti-pattern
    category: service-decomposition
    status: rejected
    problem: >
      Services are deployed independently but are tightly coupled through synchronous
      call chains, shared deployment pipelines, or coordinated release schedules. The
      system has the operational overhead of a distributed system (network failures,
      eventual consistency) without the autonomy benefits of service decomposition.
    harm: >
      A failure or deployment of any service in the call chain propagates to all upstream
      services. Services cannot be deployed independently because they depend on specific
      versions of their downstream callers being available. The system has the worst
      properties of both monoliths and distributed systems.
    remediation: >
      Identify the synchronous call chains and determine which are genuinely synchronous
      requirements (requiring a response in the same request) versus those that could be
      decoupled with event-driven communication (PAT-001, PAT-003). Apply the Strangler Fig
      pattern to progressively decouple tight synchronous dependencies. Consider Saga-based
      orchestration (PAT-001) to replace multi-service synchronous transaction chains.
    approved_alternative: PAT-001
    governing_adrs:
      - ADR-006
    known_occurrences: []
    tags:
      - service-decomposition
      - coupling
      - distributed-systems
    created: 2026-01-01
    last_reviewed: 2026-01-01
```

### JSON Schema excerpt

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Pattern Catalog",
  "type": "object",
  "required": ["entries"],
  "properties": {
    "entries": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "name", "type", "category", "status", "problem", "tags", "created"],
        "properties": {
          "id": {
            "type": "string",
            "pattern": "^(PAT|ANTI)-[0-9]+$"
          },
          "name": { "type": "string" },
          "type": {
            "type": "string",
            "enum": ["pattern", "anti-pattern"]
          },
          "category": { "type": "string" },
          "status": {
            "type": "string",
            "enum": ["approved", "approved-with-conditions", "deprecated", "rejected", "under-evaluation"]
          },
          "problem": { "type": "string" },
          "tags": { "type": "array", "items": { "type": "string" } },
          "governing_adrs": { "type": "array", "items": { "type": "string" } },
          "created": { "type": "string", "format": "date" },
          "last_reviewed": { "type": "string", "format": "date" }
        },
        "if": { "properties": { "type": { "const": "pattern" } } },
        "then": { "required": ["solution", "consequences"] },
        "else": { "required": ["harm", "remediation"] }
      }
    }
  }
}
```

### Field reference

| Field | Applies to | Required | Description |
|-------|-----------|----------|-------------|
| `id` | Both | Yes | `PAT-NNN` for patterns; `ANTI-NNN` for anti-patterns |
| `name` | Both | Yes | The recognized name of the pattern or anti-pattern |
| `type` | Both | Yes | `pattern` or `anti-pattern` |
| `category` | Both | Yes | The design problem category (e.g., `data-ownership`, `concurrency`, `api-design`) |
| `status` | Both | Yes | `approved`, `approved-with-conditions`, `deprecated`, `rejected`, `under-evaluation` |
| `problem` | Both | Yes | The design problem this entry addresses |
| `solution` | Patterns | Yes | The recommended approach (patterns only) |
| `consequences` | Patterns | Yes | Positive and negative consequences (patterns only) |
| `harm` | Anti-patterns | Yes | The specific harmful effects of this approach (anti-patterns only) |
| `remediation` | Anti-patterns | Yes | How to replace the anti-pattern with an approved approach (anti-patterns only) |
| `approved_alternative` | Anti-patterns | No | The `PAT-NNN` ID of the recommended replacement pattern |
| `governing_adrs` | Both | No | ADR IDs that established or constrain this pattern entry |
| `applied_in` | Patterns | No | Services where this pattern is intentionally applied |
| `known_occurrences` | Anti-patterns | No | Services where this anti-pattern was or is present, with remediation status |
| `related_patterns` | Both | No | IDs of related patterns that compose with or follow from this entry |
| `tags` | Both | Yes | Topic tags for filtering and grouping |
| `created` | Both | Yes | ISO 8601 date when the entry was added |
| `last_reviewed` | Both | No | ISO 8601 date of most recent review |

---

## Generator Architecture

### 1. Patterns catalog portal page

Generated to `portal/docs/patterns/index.md`. The page renders approved patterns and rejected
anti-patterns in separate sections, grouped by category. Each entry shows the problem, solution
or harm, consequences, governing ADR links, and service application or occurrence links.

A remediation backlog section lists all anti-pattern entries with `known_occurrences` entries that
have `status: active` (not yet resolved). This section drives the architecture improvement backlog.

### 2. Pattern cross-reference in service pages

The service page generator enriches each service page with a "Patterns applied" section that lists
the approved patterns applied in that service and a "Known anti-patterns" section for any active
known occurrences.

---

## CI Integration

```yaml
# .github/workflows/validate-patterns.yml (excerpt)

- name: Validate patterns.yaml schema
  run: |
    npx ajv validate \
      --schema architecture/metadata/schemas/patterns.schema.json \
      --data architecture/metadata/patterns.yaml

- name: Referential integrity — ADR references
  run: |
    python3 scripts/ci/check-pattern-adr-refs.py \
      --patterns architecture/metadata/patterns.yaml \
      --decisions-dir decisions/

- name: Referential integrity — service references
  run: |
    python3 scripts/ci/check-pattern-service-refs.py \
      --patterns architecture/metadata/patterns.yaml \
      --services architecture/metadata/services.yaml

- name: Anti-pattern completeness check
  run: |
    python3 scripts/ci/check-antipattern-completeness.py \
      --patterns architecture/metadata/patterns.yaml
```

### Validation rules

| Rule | Description |
|------|-------------|
| Schema validation | Required fields present; type and status from enums; ID pattern matches |
| ADR referential integrity | All `governing_adrs` entries resolve to existing files in `decisions/` |
| Service referential integrity | All service IDs in `applied_in` and `known_occurrences` resolve to the service registry |
| Anti-pattern completeness | Every anti-pattern entry must have `harm` and `remediation` fields |
| Approved alternative referential integrity | `approved_alternative` IDs must resolve to existing pattern entries |
| Related pattern referential integrity | `related_patterns` IDs must resolve to existing pattern entries |

---

## AI Fit

A machine-readable pattern catalog enables AI behaviors across the architecture workflow:

**Solution design review**: When an AI reviews a proposed solution design, it reads the patterns
catalog to identify whether the proposal applies any approved patterns correctly and whether it
inadvertently introduces any known anti-patterns. "The proposed implementation in section 3.b
has the characteristics of ANTI-001 (Shared Database): both svc-check-in and svc-reservations
would query the `schedule_entries` table directly. ANTI-001 is rejected. See PAT-002 for the
recommended approach."

**Pattern recommendation**: When an AI is helping design a new capability, it reads the patterns
catalog to recommend applicable patterns for the problem category. "For the distributed transaction
across check-in and payments, consider PAT-001 (Saga Pattern), which is marked approved and
applied in svc-check-in and svc-scheduling-orchestrator."

**Known occurrence tracking**: An AI conducting an architecture review can scan the service
registry and source code indicators against known anti-pattern occurrences and report on
remediation progress. This converts the anti-pattern catalog from a static reference into an
active remediation tracker.

**ADR authoring**: When an AI generates an ADR, it reads the patterns catalog to cite relevant
approved patterns in the "Decision Drivers" section and anti-patterns to avoid in the "Considered
Options" section.

---

## Governance Model

The pattern catalog is a shared reference that all engineering teams use when making design
decisions. Changes require careful governance:

- **Adding a pattern**: PR review by the architecture practice. New patterns must have a concrete
  `problem` statement (not abstract), a `solution` that is actionable (not vague), and at least
  one real `applied_in` service or a prior art reference showing the pattern is valid. Patterns
  proposed without implementation evidence are marked `under-evaluation` until a first application
  is complete.

- **Adding an anti-pattern**: PR review by the architecture practice. Anti-patterns must have a
  specific `harm` description (not "bad" or "avoid this"), a concrete `remediation` path, and an
  `approved_alternative`. Anti-pattern entries without a remediation path are not useful — they
  identify problems without providing solutions.

- **Updating known occurrences**: Any engineer can add a `known_occurrences` entry for an
  anti-pattern they observe in a service. This is encouraged as a lightweight way to build the
  remediation backlog. Updating `status: resolved` requires a reference to the ADR or PR that
  resolved the occurrence.

- **Deprecating a pattern**: A previously approved pattern may be deprecated when the practice
  determines it is no longer preferred (e.g., a better alternative was adopted). Deprecated
  patterns are preserved with `status: deprecated` — not deleted.

---

## Recommended Practices

1. **Write patterns and anti-patterns from evidence, not aspiration.** An anti-pattern entry
   is most valuable when it describes something that actually happened in your codebase and
   caused harm. Abstract anti-patterns without concrete harm descriptions are unpersuasive.
   Write the harm section from incident reports and production failures.

2. **Every anti-pattern MUST have an approved alternative.** An architecture team that prohibits
   an approach without providing a better one creates frustration without resolution. The
   `approved_alternative` field and the `remediation` section are the constructive obligation
   that accompanies every prohibition.

3. **Keep known occurrences current.** The known occurrences list is the remediation backlog.
   If it is not kept current — entries that have been resolved are not marked resolved; new
   occurrences are not added — it becomes misleading. Assign ownership of the patterns catalog
   to the architecture team with a quarterly review obligation.

4. **Distinguish `approved-with-conditions` from `approved`.** Some patterns are valid in
   specific contexts but harmful in others. The Event Sourcing pattern, for example, is valid
   for audit-heavy domains but significantly increases operational complexity for simple CRUD
   services. `approved-with-conditions` with an explicit conditions note is more honest than
   blanket approval.

5. **Link every anti-pattern to its origin ADR.** When an anti-pattern was identified and
   rejected in an ADR, that ADR is the authoritative record of why it was rejected. The pattern
   catalog entry is the indexed, searchable pointer; the ADR contains the full reasoning.

6. **Review the catalog annually.** Technology and the codebase change. A pattern that was
   approved five years ago may be superseded. An anti-pattern that was identified but never
   had a known occurrence may be hypothetical rather than practical. Annual review keeps the
   catalog signal-high.

---

## Synthetic Exemplar Status

> The status below describes how Pillar AK has been implemented in the NovaTrek Adventures
> synthetic exemplar workspace. NovaTrek data is entirely fictional — no corporate systems are
> represented.

| Artifact | Status | Location |
|----------|--------|----------|
| Pattern catalog YAML | Not yet created — planned in Transformation Wave 2 | `architecture/metadata/patterns.yaml` |
| JSON Schema | Not yet created | `architecture/metadata/schemas/patterns.schema.json` |
| Patterns catalog portal page | Not yet generated | `portal/docs/patterns/index.md` |
| CI schema validation | Not yet wired | `.github/workflows/validate-patterns.yml` |
| Service page pattern cross-reference | Not yet generated | — |

The NovaTrek ADR archive contains rich pattern and anti-pattern evidence: ADR-003 (shared database
anti-pattern), ADR-004 and ADR-005 (hardcoded classification and unsafe defaults), ADR-006 (saga
pattern for orchestration), ADR-010 (PATCH semantics), ADR-011 (optimistic locking), and ADR-007
and ADR-008 (shadow guest records anti-pattern). The Wave 2 adoption item is to extract this
implicit knowledge into the formal patterns registry.

---

## Forward Plan

Pillar AK adoption for NovaTrek is planned in **Wave 2** of the Transformation Plan, alongside
Architecture Principles as Code (Pillar AH), Ubiquitous Language as Code (Pillar AI), and Actors
as Code (Pillar C). Wave 2 establishes the governance and domain knowledge infrastructure that AI
agents need to produce consistent, context-aware architecture artifacts. See
[Transformation Plan — Pillar AK](TRANSFORMATION-PLAN.md#pillar-ak--patterns-and-anti-patterns-as-code)
for the sequenced adoption checklist.

---

## References

- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns: Elements of Reusable Object-Oriented Software* (Gang of Four, 1994)
- William Brown, Raphael Malveau, Hays McCormick, Tom Mowbray, *AntiPatterns: Refactoring Software, Architectures, and Projects in Crisis* (1998)
- Martin Fowler, *Patterns of Enterprise Application Architecture* (2002)
- Chris Richardson, *Microservices Patterns* (2018) — the primary reference for Saga, Transactional Outbox, and related distributed systems patterns
- Sam Newman, *Building Microservices* (2021, 2nd ed.) — Chapter 4: Microservice Communication Styles
- NovaTrek EaC Framework: [Pillar AK definition](EVERYTHING-AS-CODE-FRAMEWORK.md)
- NovaTrek Transformation Plan: [Pillar AK adoption steps](TRANSFORMATION-PLAN.md#pillar-ak--patterns-and-anti-patterns-as-code)
