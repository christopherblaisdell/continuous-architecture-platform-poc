# Architecture Decisions

Every significant architectural choice at NovaTrek is recorded as an Architecture Decision Record (ADR). This page covers when to create one, the required format, and how to publish it.

---

## When to Create an ADR

Create an ADR when a decision:

- **Crosses service boundaries** — affects how two or more services interact
- **Changes data semantics** — modifies what a field means, adds nullable fields, or changes data ownership
- **Introduces a new pattern** — new integration approach, new technology, new security model
- **Has at least 2 genuinely viable alternatives** — if there's only one reasonable option, it's not a decision; it's a requirement

Do NOT create an ADR for:

- Implementation choices within a single service (method naming, internal refactoring)
- Trivial configuration decisions
- Decisions already settled by an existing ADR (reference the existing one instead)

---

## MADR Format (Required)

All ADRs use the [Markdown Any Decision Record (MADR)](../standards/madr/index.md) format. Every ADR MUST include these sections:

### 1. Status

One of: `Proposed`, `Accepted`, `Deprecated`, `Superseded`

### 2. Date

ISO 8601 format: `YYYY-MM-DD`

### 3. Context and Problem Statement

2-3 sentences establishing the architectural concern. State the problem neutrally without pre-judging the solution.

### 4. Decision Drivers

Bullet list of evaluation criteria. Minimum 3 drivers. These are the criteria used to evaluate options.

### 5. Considered Options

At least 2 options with genuine pros and cons analysis. Do not include straw-man alternatives that exist only to make the preferred option look good.

For each option:

```markdown
### Option N: [Name]

[Description of the approach]

**Pros:**
- [Advantage 1]
- [Advantage 2]

**Cons:**
- [Disadvantage 1]
- [Disadvantage 2]
```

### 6. Decision Outcome

Selected option with justification explicitly tied to the decision drivers.

### 7. Consequences

All three subsections are required:

- **Positive** — benefits gained
- **Negative** — trade-offs accepted
- **Neutral** — side effects that are neither positive nor negative

---

## Where ADRs Live

### Global ADRs

ADRs that apply across the platform live in `decisions/`:

```
decisions/
  ADR-001-ai-toolchain-selection.md
  ADR-002-documentation-publishing-platform.md
  ADR-003-nullable-elevation-fields.md
  ...
```

**Numbering**: Sequential. Check the highest existing number in `decisions/` and increment.

**Naming**: `ADR-{NNN}-{kebab-case-slug}.md`

### Solution-Level ADRs

ADRs that belong to a specific solution design go in the solution's decisions folder:

```
architecture/solutions/_NTK-XXXXX-slug/
  3.solution/d.decisions/decisions.md
```

This is a combined document with clear H2 separators between decisions. Solution-level ADRs do not get separate files — they are grouped in one document.

---

## ADR Template

Use the template at [standards/madr/adr-template.md](../standards/madr/adr-template.md). A shortened version is also available at [standards/madr/adr-template-short.md](../standards/madr/adr-template-short.md).

### Worked Example

```markdown
# ADR-014: Event Schema Versioning Strategy

## Status

Proposed

## Date

2026-03-19

## Context and Problem Statement

As NovaTrek evolves, event schemas will change. Consumers currently have no
mechanism to handle schema evolution gracefully. We need a versioning strategy
that allows producers to evolve schemas without breaking existing consumers.

## Decision Drivers

- Consumer backward compatibility — existing consumers must not break
- Producer flexibility — producers must be able to add fields
- Operational simplicity — minimize schema registry complexity
- Auditability — changes to schemas must be traceable

## Considered Options

### Option 1: Semantic Versioning with Schema Registry

Use a Confluent-compatible schema registry with semantic versioning.

**Pros:**
- Industry standard approach
- Automated compatibility checking
- Clear upgrade path

**Cons:**
- Additional infrastructure (schema registry)
- Operational complexity for small team
- Learning curve

### Option 2: Additive-Only Schema Evolution

Allow only additive changes (new optional fields). Breaking changes require
a new event type entirely.

**Pros:**
- Simple to understand and enforce
- No additional infrastructure
- Naturally backward compatible

**Cons:**
- Cannot remove or rename fields without a new event
- May lead to schema bloat over time

## Decision Outcome

**Option 2: Additive-Only Schema Evolution**

Chosen because it satisfies backward compatibility and operational simplicity
without introducing infrastructure overhead. The 7-event domain (current
scale) does not justify a schema registry. If event count exceeds 20, this
decision should be revisited.

## Consequences

### Positive
- Zero additional infrastructure
- Every schema change is inherently backward compatible
- Simple review criteria: "does this add a new optional field or create a new event?"

### Negative
- Cannot rename or remove fields from existing events
- Old optional fields accumulate over time

### Neutral
- Existing AsyncAPI specs already follow this pattern implicitly
```

---

## Referencing Existing ADRs

Before creating a new ADR, search `decisions/` for existing decisions that may constrain or overlap with your proposal. If a decision has already been settled, reference it — do not re-decide.

```markdown
This design follows [ADR-005](../decisions/ADR-005-pattern3-default-fallback.md),
which requires unknown adventure categories to default to Pattern 3.
```

---

## Alternative ADR Formats

While MADR is the required format at NovaTrek, the platform documents three alternative formats for reference:

- [Nygard Template](../standards/adr-templates/nygard-template.md) — minimal format (Title, Status, Context, Decision, Consequences)
- [Tyree-Akerman Template](../standards/adr-templates/tyree-akerman-template.md) — business-oriented with stakeholder impact
- [Alexandrian Template](../standards/adr-templates/alexandrian-template.md) — pattern-based with forces and resulting context

---

## Quality Attributes in Decisions

When evaluating options, assess impact against [ISO 25010 quality attributes](../standards/quality-model/iso-25010-quality-tree.md):

| Attribute | Assess When |
|-----------|-------------|
| Functional Suitability | Every decision — does it meet stated requirements? |
| Performance Efficiency | Any change touching API contracts or data models |
| Compatibility | Any cross-service change or data format modification |
| Reliability | Any change to error handling, fallback paths, or data integrity |
| Security | Any change involving authentication, authorization, or PII |
| Maintainability | Every decision — is the outcome modular and testable? |
| Portability | Only when infrastructure or deployment model changes |
