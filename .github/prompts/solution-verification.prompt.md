---
agent: "agent"
description: "Verify a NovaTrek solution design for completeness, consistency, and quality before merge. Checks all required sections, capability rollup, content separation, metadata consistency, and cross-references."
---

# Solution Design Verification — NovaTrek Architecture

You are performing a quality gate verification on a NovaTrek Adventures solution design before it is merged to main. This verification ensures the solution meets all architecture practice standards.

## Verification Target

Identify the solution to verify. If not specified, ask for the ticket ID (e.g., NTK-10005).

Read ALL files in: `architecture/solutions/_NTK-XXXXX-*/`

## Verification Gates

Work through each gate sequentially. A solution must pass all gates to be merge-ready.

### Gate 1: Structure Completeness

Check that all required directories and files exist:

| Required Path | Purpose | Status |
|---------------|---------|--------|
| `NTK-XXXXX-solution-design.md` | Master document | PRESENT/MISSING |
| `1.requirements/` | Ticket report | PRESENT/MISSING |
| `2.analysis/` | Simple explanation | PRESENT/MISSING |
| `3.solution/a.assumptions/` | Documented assumptions | PRESENT/MISSING |
| `3.solution/c.capabilities/capabilities.md` | Capability mapping | PRESENT/MISSING |
| `3.solution/d.decisions/decisions.md` | MADR decisions | PRESENT/MISSING |
| `3.solution/i.impacts/` | Per-service impacts | PRESENT/MISSING |
| `3.solution/r.risks/` | Risk register | PRESENT/MISSING |
| `3.solution/u.user.stories/` | User stories | PRESENT/MISSING |

Flag: MISSING files are blockers. PRESENT but empty files are warnings.

### Gate 2: Master Document Quality

Check the master document (`NTK-XXXXX-solution-design.md`):

- [ ] Has metadata header (ticket, status, capabilities, services)
- [ ] Has Overview section with problem statement
- [ ] Has Component Architecture section
- [ ] References all impacted services
- [ ] Lists capability IDs (CAP-X.Y)
- [ ] Has no placeholder content ("TODO", "TBD", "[fill in]")

### Gate 3: Capability Rollup (REQUIRED)

This is the most critical gate — capability rollup is what makes architecture continuous.

- [ ] `3.solution/c.capabilities/capabilities.md` exists and has substantive content
- [ ] CAP-X.Y IDs are declared and match valid capabilities from `architecture/metadata/capabilities.yaml`
- [ ] Impact type is specified for each capability (enhanced / fixed / new)
- [ ] Check `architecture/metadata/capability-changelog.yaml` for an entry matching this ticket
  - If missing: FLAG as blocker — "Capability changelog entry required"
  - If present: verify the capabilities listed match the solution's capability mapping

### Gate 4: Decision Quality (MADR)

For each decision in `3.solution/d.decisions/decisions.md`:

- [ ] Uses MADR format (Status, Date, Context, Decision Drivers, Options, Outcome, Consequences)
- [ ] Has at least 2 genuinely considered options (not straw-man alternatives)
- [ ] Decision drivers are listed (minimum 3)
- [ ] Consequences section has Positive, Negative, AND Neutral subsections
- [ ] Decision outcome references the decision drivers

### Gate 5: Content Separation

Verify that document types contain the right content:

| Document | Should Answer | Should NOT Contain |
|----------|-------------|-------------------|
| Impact assessments | WHAT changes | Implementation code, deployment steps |
| Decisions (MADR) | WHY this approach | Code samples, deployment procedures |
| Guidance | HOW to implement | Business justification |
| User stories | WHO benefits, WHY | Technical implementation details |
| Simple explanation | Plain language summary | Jargon, code, API references |

Flag violations by specific file and section.

### Gate 6: Metadata Consistency

Cross-reference the solution against metadata files:

- [ ] Services mentioned in the solution match entries in `architecture/metadata/domains.yaml`
- [ ] Cross-service calls in the solution are reflected in `architecture/metadata/cross-service-calls.yaml`
- [ ] Capability IDs used exist in `architecture/metadata/capabilities.yaml`
- [ ] If new ADRs are documented, check if they should be promoted to `decisions/` (cross-boundary decisions)

### Gate 7: Prior Art Reference

- [ ] Check if `architecture/metadata/capability-changelog.yaml` has prior entries for the same capabilities
- [ ] If prior solutions exist for the same capabilities, are they referenced in the master document?
- [ ] Run: `python3 scripts/ticket-client.py --list --capability CAP-X.Y` for each affected capability

### Gate 8: Anti-Pattern Detection

Check for known architecture anti-patterns:

- [ ] No shared database access (services must use API-mediated access)
- [ ] No entity replacement (PATCH semantics, not PUT for updates — ADR-010)
- [ ] No shadow guest records (all identity goes through svc-guest-profiles)
- [ ] No unsafe defaults (unknown categories must default to Pattern 3 — ADR-005)
- [ ] No missing concurrency control on mutable entities (ADR-011)

## Output Format

```markdown
# Solution Design Verification: NTK-XXXXX — [Solution Title]

**Verifier**: AI Verification Gate (ECC-adapted)
**Date**: [today]
**Solution**: [solution folder path]
**Overall Status**: PASS / PASS WITH WARNINGS / FAIL

## Gate Results

| # | Gate | Status | Findings |
|---|------|--------|----------|
| 1 | Structure Completeness | PASS/FAIL | [summary] |
| 2 | Master Document Quality | PASS/FAIL | [summary] |
| 3 | Capability Rollup | PASS/FAIL | [summary] |
| 4 | Decision Quality (MADR) | PASS/FAIL | [summary] |
| 5 | Content Separation | PASS/FAIL | [summary] |
| 6 | Metadata Consistency | PASS/FAIL | [summary] |
| 7 | Prior Art Reference | PASS/FAIL | [summary] |
| 8 | Anti-Pattern Detection | PASS/FAIL | [summary] |

## Blockers (Must Fix Before Merge)

1. [Gate X] [Description of blocking issue]
2. ...

## Warnings (Should Address)

1. [Gate X] [Description of warning]
2. ...

## Observations (Informational)

1. [Gate X] [Observation]
2. ...

## Merge Recommendation

[APPROVE / APPROVE WITH CONDITIONS / REQUEST CHANGES]

[1-2 sentence justification]
```

## Rules

- ALWAYS read every file in the solution directory before producing the report
- ALWAYS cross-reference with the actual metadata YAML files — do not assume consistency
- NEVER fabricate findings — only report issues found in the actual files
- If a gate passes cleanly, say "PASS — no issues found" — do not invent warnings
- Blockers must be genuine quality gaps, not style preferences
