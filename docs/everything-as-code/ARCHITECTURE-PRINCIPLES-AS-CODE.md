# Architecture Principles as Code — A First-Class EaC Pillar (Blueprint)

> **BLUEPRINT DOCUMENT.** This is the portable definition of Pillar 33 — Architecture Principles
> as Code. It describes a pattern applicable to any software architecture practice. References to
> NovaTrek Adventures services and files are synthetic exemplar data used to validate the pattern,
> not corporate information. See [Synthetic Exemplar Status](#synthetic-exemplar-status) for
> details.

**Status**: This is Pillar 33 of the Everything as Code framework — see [EaC Framework](EVERYTHING-AS-CODE-FRAMEWORK.md).

---

## Why Principles Belong in EaC

Architecture principles are the standing heuristics that guide design decisions below the level of
a specific Architecture Decision Record. An ADR records what was decided for a specific problem.
A principle records the general rule that informed that decision — and will inform future decisions
the same way.

Without version control, principles live in slide decks, wiki pages, and the mental models of
senior practitioners. They drift, contradict each other, and become invisible to new team members.
More critically, they become invisible to AI agents.

Making principles version-controlled artifacts yields structural advantages:

| Property | Requirement |
|----------|-------------|
| Authority | Principles are reviewed, approved, and have a declared enforcement status |
| Traceability | Every principle is linked to the ADRs and policy rules that give it teeth |
| Evolvability | Principles are promoted, retired, and superseded through a PR process |
| AI legibility | AI agents can check proposed solutions against declared principles during design review |
| Consistency | The same principles apply to all teams — not informally applied by whoever happens to review a PR |

The last two properties are the forcing functions for machine-readable principles. An AI reviewing
a proposed solution design can read `principles.yaml` and flag decisions that appear to violate
standing principles. An AI generating an ADR can cite the relevant principles as decision drivers.

---

## The Core Problem

Without a principles registry, architectural principles exist in the following fragile forms:

- **Embedded in ADRs**: The principle is stated once in one ADR and never elevated to a standing
  commitment. New ADRs on related topics cannot easily discover or cite it.
- **In onboarding slides**: Presented to new team members once, then never referenced again.
- **In reviewer memory**: "We don't do direct database access" is enforced by whoever happens to
  be reviewing the PR, applied inconsistently across reviewers.
- **Nowhere**: The principle exists as a shared assumption that practitioners have never stated
  explicitly and therefore cannot evaluate, debate, or evolve.

The principles registry makes the implicit explicit. It forces the practice to be specific: not
"prefer simple solutions" (untestable) but "Services MUST NOT maintain local copies of data owned
by another service" (testable against a codebase).

---

## Enforcement Status Taxonomy

The key architectural contribution of a principles-as-code registry is the enforcement status
taxonomy. Not all principles can or should be enforced mechanically. The taxonomy makes the
enforcement gap visible:

| Status | Meaning | Enforcement Mechanism |
|--------|---------|----------------------|
| `aspirational` | The practice agrees with this principle but enforces compliance through reviewer discipline alone | None (PR review only) |
| `adr-mandated` | A specific ADR records a decision that implements this principle. The ADR is the primary enforcement artifact. | ADR reference; reviewer required to cite the ADR on violations |
| `policy-enforced` | A CI policy rule (Pillar 10) automatically verifies this principle on every PR | Rego/Conftest policy rule; violations block merge |
| `deprecated` | The principle is retired. It is preserved for historical context. | None |

The enforcement status reveals which principles are genuinely binding and which are aspirational.
A practice with 15 principles all marked `aspirational` has declared principles but no enforcement.
A practice with 8 principles — 3 `policy-enforced`, 3 `adr-mandated`, 2 `aspirational` — has a
credible, graduated enforcement model.

---

## The Principles Schema

### principles.yaml

```yaml
# architecture/metadata/principles.yaml
$schema: "./schemas/principles.schema.json"

principles:
  - id: PRIN-001
    name: API-Mediated Data Access
    statement: >
      Services MUST access data owned by another service exclusively through that service's
      published API. Direct database access across service boundaries is prohibited.
    rationale: >
      Direct database access couples services at the schema level. Schema changes in one service
      silently break other services. API-mediated access provides a stable contract that permits
      independent schema evolution and enforces data ownership semantics.
    enforcement_status: policy-enforced
    policy_rule: policies/data-access/cross-service-db-access.rego
    governing_adrs:
      - ADR-003
    tags:
      - data
      - coupling
      - data-ownership
    created: 2025-09-01
    last_reviewed: 2026-01-01

  - id: PRIN-002
    name: Fail-Safe Defaults
    statement: >
      When the system cannot determine the correct safety classification for an adventure
      category, it MUST default to the most restrictive classification (Pattern 3). Unknown
      inputs MUST NOT default to the least restrictive level.
    rationale: >
      Defaulting to the least restrictive classification when the input is unknown optimizes
      for throughput at the cost of safety. NovaTrek's liability and duty-of-care obligations
      require the opposite optimization: err on the side of caution.
    enforcement_status: adr-mandated
    governing_adrs:
      - ADR-005
    tags:
      - safety
      - defaults
    created: 2025-09-15
    last_reviewed: 2026-01-01

  - id: PRIN-003
    name: Single Source of Guest Identity
    statement: >
      svc-guest-profiles is the exclusive source of truth for guest identity data. No
      service MAY maintain a local copy of guest identity fields. Cross-service reads MUST
      go through svc-guest-profiles at runtime.
    rationale: >
      Shadow guest records cause identity divergence: guest name changes in one place,
      contact preferences change in another, loyalty tier is stale in a third. A single
      source eliminates the class of data integrity failures caused by stale local copies.
    enforcement_status: adr-mandated
    governing_adrs:
      - ADR-008
    tags:
      - data
      - guest-identity
      - data-integrity
    created: 2025-10-01
    last_reviewed: 2026-01-01

  - id: PRIN-004
    name: Schedule Mutation Ownership
    statement: >
      Only svc-scheduling-orchestrator MAY mutate daily schedule data. Other services MUST
      NOT directly modify schedule records, even if they have database access.
    rationale: >
      The scheduling orchestrator implements the schedule lifecycle state machine including
      conflict detection, capacity enforcement, and guide assignment constraints. Services
      mutating schedule data directly bypass this logic, producing invalid schedule states
      that are difficult to detect and correct.
    enforcement_status: adr-mandated
    governing_adrs:
      - ADR-010
      - ADR-011
    tags:
      - data-ownership
      - scheduling
    created: 2025-11-01
    last_reviewed: 2026-01-01

  - id: PRIN-005
    name: Configuration-Driven Classification
    statement: >
      Business classification rules (adventure category to check-in pattern mapping) MUST
      be declared in configuration files, not hardcoded in application source code. New
      classification categories MUST NOT require a code deployment to take effect.
    rationale: >
      Hardcoded classification creates a deployment bottleneck for business rule changes.
      Configuration-driven classification separates business rule evolution from software
      deployment cycles and allows non-engineering teams to manage classification rules.
    enforcement_status: adr-mandated
    governing_adrs:
      - ADR-004
    tags:
      - configuration
      - extensibility
    created: 2025-10-15
    last_reviewed: 2026-01-01

  - id: PRIN-006
    name: Backward-Compatible API Evolution
    statement: >
      Published API contracts MUST evolve in a backward-compatible manner. New optional
      fields may be added without a version increment. Breaking changes require a new API
      version and a migration window for consumers.
    rationale: >
      Services have independent deployment cycles. A breaking API change without a migration
      window forces coordinated deployments across multiple services, reintroducing the
      coupling that service decomposition was designed to eliminate.
    enforcement_status: aspirational
    governing_adrs:
      - ADR-007
    tags:
      - api
      - compatibility
    created: 2025-09-01
    last_reviewed: 2026-01-01

  - id: PRIN-007
    name: Optimistic Concurrency on Shared Mutable State
    statement: >
      Any entity that is concurrently modified by multiple services or clients MUST use
      optimistic locking (a `_rev` or `@Version` field) with a 409 Conflict response on
      version mismatch.
    rationale: >
      Pessimistic locking (database row locks) couples services at the transaction level
      and is incompatible with a distributed architecture. Optimistic locking provides
      conflict detection without coupling services at the lock level.
    enforcement_status: adr-mandated
    governing_adrs:
      - ADR-011
    tags:
      - concurrency
      - data-integrity
    created: 2025-12-01
    last_reviewed: 2026-01-01

  - id: PRIN-008
    name: Test-First Behavioral Specification
    statement: >
      New capabilities MUST have executable behavioral specifications (Gherkin feature files)
      authored alongside the implementation, not after. Capabilities without feature files
      are not considered complete.
    rationale: >
      Post-implementation specification writing produces specifications that describe what
      was built rather than what was required. Test-first specification forces explicit
      thinking about acceptance criteria before implementation begins.
    enforcement_status: aspirational
    governing_adrs:
      - ADR-012
    tags:
      - testing
      - quality
    created: 2026-01-15
    last_reviewed: 2026-01-15

  # --- Deprecated principles ---
  - id: PRIN-D01
    name: REST-Only External APIs
    statement: >
      All external-facing API endpoints MUST use REST/HTTP. GraphQL and gRPC are not
      permitted for external-facing endpoints.
    rationale: >
      Superseded: ADR-015 permits GraphQL for the guest mobile app BFF, which requires
      flexible field selection not suited to REST. The blanket REST-only rule has been
      replaced with a per-context decision process.
    enforcement_status: deprecated
    deprecated_in: 2026-02-01
    superseded_by: PRIN-006
    governing_adrs:
      - ADR-015
    tags:
      - api
      - deprecated
```

### JSON Schema excerpt

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Architecture Principles Registry",
  "type": "object",
  "required": ["principles"],
  "properties": {
    "principles": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "name", "statement", "rationale", "enforcement_status", "tags", "created"],
        "properties": {
          "id": {
            "type": "string",
            "pattern": "^PRIN(-D)?-[0-9]+$"
          },
          "name": { "type": "string" },
          "statement": { "type": "string" },
          "rationale": { "type": "string" },
          "enforcement_status": {
            "type": "string",
            "enum": ["aspirational", "adr-mandated", "policy-enforced", "deprecated"]
          },
          "policy_rule": { "type": "string" },
          "governing_adrs": {
            "type": "array",
            "items": { "type": "string", "pattern": "^ADR-[0-9]+" }
          },
          "deprecated_in": { "type": "string", "format": "date" },
          "superseded_by": { "type": "string", "pattern": "^PRIN-" },
          "tags": {
            "type": "array",
            "items": { "type": "string" }
          },
          "created": { "type": "string", "format": "date" },
          "last_reviewed": { "type": "string", "format": "date" }
        },
        "if": {
          "properties": { "enforcement_status": { "const": "policy-enforced" } }
        },
        "then": {
          "required": ["policy_rule"]
        }
      }
    }
  }
}
```

### Field reference

| Field | Required | Description |
|-------|----------|-------------|
| `id` | Yes | Identifier prefixed with `PRIN-`. Deprecated principles use `PRIN-D-` prefix convention. |
| `name` | Yes | Short, action-oriented principle name. Used as the heading in generated pages. |
| `statement` | Yes | The normative statement using RFC 2119 language (MUST, MUST NOT, SHOULD, MAY). |
| `rationale` | Yes | The "why" behind the principle. Should explain what failure mode the principle prevents. |
| `enforcement_status` | Yes | One of the four enforcement status values (see taxonomy above). |
| `policy_rule` | Conditional | Required when `enforcement_status: policy-enforced`. Path to the Rego/Conftest policy file. |
| `governing_adrs` | No | ADR IDs that established or constrain this principle. Required for `adr-mandated` principles. |
| `deprecated_in` | Conditional | Date the principle was deprecated. Required when `enforcement_status: deprecated`. |
| `superseded_by` | No | The ID of the principle that replaces a deprecated principle, if one exists. |
| `tags` | Yes | One or more topic tags for filtering and grouping in the generated portal page. |
| `created` | Yes | ISO 8601 date when the principle was first declared. |
| `last_reviewed` | No | ISO 8601 date of the most recent annual review. |

---

## Generator Architecture

### 1. Principles portal page

Generated to `portal/docs/principles/index.md`. The page groups principles by tag, renders each
principle's statement and rationale, shows the enforcement status (with a badge or indicator), and
links each principle to its governing ADRs and policy rules.

A summary table at the top of the page shows the enforcement status distribution:

```markdown
| Status | Count |
|--------|-------|
| Policy-enforced | 1 |
| ADR-mandated | 5 |
| Aspirational | 2 |
| Deprecated | 1 |
```

This summary is the enforcement credibility indicator: a practice that can show 6 of 8 active
principles are mechanically enforced has a fundamentally different governance posture from one with
all principles aspirational.

### 2. ADR back-links

The principles generator enriches generated ADR pages with a "Governing principle" annotation:
when an ADR is referenced by a principle, the generated ADR page links back to that principle.

---

## CI Integration

```yaml
# .github/workflows/validate-principles.yml (excerpt)

- name: Validate principles.yaml schema
  run: |
    npx ajv validate \
      --schema architecture/metadata/schemas/principles.schema.json \
      --data architecture/metadata/principles.yaml

- name: Referential integrity — ADR references
  run: |
    python3 scripts/ci/check-principle-adr-refs.py \
      --principles architecture/metadata/principles.yaml \
      --decisions-dir decisions/

- name: Referential integrity — policy rule files
  run: |
    python3 scripts/ci/check-principle-policy-refs.py \
      --principles architecture/metadata/principles.yaml

- name: Deprecation hygiene
  run: |
    python3 scripts/ci/check-principle-deprecations.py \
      --principles architecture/metadata/principles.yaml
```

### Validation rules

| Rule | Description |
|------|-------------|
| Schema validation | All required fields present; enforcement status from allowed enum; ID pattern matches |
| ADR referential integrity | Every ADR cited in `governing_adrs` must resolve to an existing file in `decisions/` |
| Policy rule referential integrity | Every `policy_rule` path must resolve to an existing Rego/Conftest file |
| `policy-enforced` completeness | Principles with `enforcement_status: policy-enforced` must have a `policy_rule` field |
| `adr-mandated` completeness | Principles with `enforcement_status: adr-mandated` must have at least one entry in `governing_adrs` |
| Deprecation completeness | Deprecated principles must have a `deprecated_in` date |

---

## AI Fit

A machine-readable principles registry enables two AI behaviors that significantly improve
architecture work quality:

**Design review**: When an AI reviews a proposed solution design or ADR, it reads `principles.yaml`
and checks the proposal against each active principle. It flags specific potential violations with
the principle ID and statement. This produces a structured review comment rather than a subjective
opinion.

Example AI output: "PRIN-001 (API-Mediated Data Access): The proposed implementation in
`ReservationService.java` lines 87–92 queries the `guest_profiles` table directly. This appears to
violate PRIN-001. Consider calling `GET /guests/{guest_id}` via svc-guest-profiles instead."

**ADR authoring**: When an AI generates an ADR, it reads the principles registry to populate the
"Decision Drivers" section with relevant active principles. An ADR about a data schema change will
automatically cite PRIN-001 (API-Mediated Data Access) and PRIN-003 (Single Source of Guest
Identity) as relevant drivers.

**Principle gap detection**: An AI can read the principles registry, analyze the ADR archive, and
identify patterns in decisions that suggest an undeclared standing principle. "ADR-003, ADR-008,
and ADR-010 all reference data ownership boundaries — these suggest an undeclared principle about
service data exclusivity that could be elevated."

---

## Governance Model

Principles are high-authority artifacts. Changes to the principles registry require:

- **Adding a principle**: PR review by the architecture practice lead. New principles must include
  a concrete, testable statement (not a vague heuristic), a rationale explaining what failure mode
  it prevents, and an initial enforcement status.

- **Promoting a principle** (e.g., from `aspirational` to `policy-enforced`): Requires a
  corresponding policy rule to be authored and merged in the same PR. The principle statement
  may be refined as part of the promotion to match the precise semantics of the policy rule.

- **Deprecating a principle**: Requires an explanation of why the principle no longer applies (or
  was superseded), a `deprecated_in` date, and a reference to any superseding principle or ADR.

- **Annual review**: The full principles registry is reviewed annually. Each principle's
  `last_reviewed` date is updated. Principles not reviewed in two years are marked `aspirational`
  (if previously `adr-mandated` without recent use) or deprecated.

---

## Recommended Practices

1. **Write principle statements in RFC 2119 language.** "Services MUST NOT query databases owned
   by other services" is enforceable. "Services should avoid unnecessary coupling" is not. The
   normative keyword (MUST, SHOULD, MAY, MUST NOT) signals the strength of the principle and
   anchors enforcement status decisions.

2. **Keep the registry small and high-signal.** Ten principles that are actually followed and
   enforceable are more valuable than forty principles that exist to make the registry look
   comprehensive. Err toward fewer, stronger principles.

3. **Every `aspirational` principle is a debt item.** Aspirational principles are enforced only
   by reviewer diligence, which degrades over time. The backlog should include a task to either
   promote each aspirational principle to `adr-mandated` or `policy-enforced`, or to deprecate it
   if it is not worth the enforcement investment.

4. **Rationale is as important as the statement.** A principle without a rationale will be
   challenged and overridden by the next developer who does not know why it exists. The rationale
   is the institutional memory that prevents the principle from being silently eroded.

5. **Do not delete deprecated principles.** A deprecated principle is evidence that the practice
   tried this approach and moved away from it. Future architects should be able to read that
   history. Set `enforcement_status: deprecated` and preserve the entry.

6. **Link principles to policy rules bidirectionally.** The principle references the policy rule.
   The policy rule (via a comment header) references the principle ID. This bidirectional linkage
   makes it possible to navigate from "what does this policy rule enforce?" to "what principle
   established this rule?" and back.

---

## Synthetic Exemplar Status

> The status below describes how Pillar 33 has been implemented in the NovaTrek Adventures
> synthetic exemplar workspace. NovaTrek data is entirely fictional — no corporate systems are
> represented.

| Artifact | Status | Location |
|----------|--------|----------|
| Principles YAML | Not yet created — planned in Transformation Wave 2 | `architecture/metadata/principles.yaml` |
| JSON Schema | Not yet created | `architecture/metadata/schemas/principles.schema.json` |
| Principles portal page | Not yet generated | `portal/docs/principles/index.md` |
| CI schema validation | Not yet wired | `.github/workflows/validate-principles.yml` |
| ADR referential integrity check | Not yet wired | — |

The NovaTrek workspace has 14 ADRs that each contain an implicit principle statement in their
"Decision Outcome" section. The backlog item is to extract these implicit principles into an
explicit `principles.yaml` registry, assign enforcement statuses, and wire CI validation. This is a
Wave 2 adoption item that will be completed alongside Decisions as Code (Pillar 7) infrastructure
improvements.

---

## Forward Plan

Pillar 33 adoption for NovaTrek is planned in **Wave 2** of the Transformation Plan, alongside
Capabilities as Code (Pillar 6), Decisions as Code (Pillar 7), and Ubiquitous Language as Code
(Pillar 34). Wave 2 establishes the governance and language infrastructure that all later pillars
depend on. See
[Transformation Plan — Pillar 33](TRANSFORMATION-PLAN.md#pillar-33--architecture-principles-as-code)
for the sequenced adoption checklist.

---

## References

- IEEE Std 42010:2011, *Systems and software engineering — Architecture description* — Section 5.4: Architecture decisions and rationale
- TOGAF 10 — Part II: Architecture Development Method, Section 3.3: Architecture Principles
- Gregor Hohpe, *The Architect Elevator* (2020) — Chapters on standing architecture principles vs. tactical decisions
- RFC 2119 — Key words for use in RFCs to indicate requirement levels (MUST, SHOULD, MAY)
- NovaTrek EaC Framework: [Pillar 33 definition](EVERYTHING-AS-CODE-FRAMEWORK.md)
- NovaTrek Transformation Plan: [Pillar 33 adoption steps](TRANSFORMATION-PLAN.md#pillar-33--architecture-principles-as-code)
