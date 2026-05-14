# Governance as Code — A First-Class EaC Pillar (Blueprint)

> **BLUEPRINT DOCUMENT.** This is the portable definition of Pillar O — Governance as Code. It
> describes a pattern applicable to any software architecture practice. References to NovaTrek
> Adventures services and files are synthetic exemplar data used to validate the pattern, not
> corporate information. See [Synthetic Exemplar Status](#synthetic-exemplar-status) for details.

**Status**: This is Pillar O of the Everything as Code framework — see [EaC Framework](EVERYTHING-AS-CODE-FRAMEWORK.md).

---

## Why Governance Belongs in EaC

Governance — the process of controlling who can change what, under what conditions, with what
evidence — is itself an architectural concern. In most practices, governance lives in policy
documents (unversioned), Change Advisory Board (CAB) processes (undocumented or documented in
wikis), and reviewer norms (in practitioners' heads). None of these are machine-readable,
version-controlled, or automatically enforced.

Governance as Code addresses this directly:

| Property | Requirement |
|----------|-------------|
| Auditability | Every change to a governed artifact must produce an archived record |
| Consistency | The same artifact class is governed by the same rules regardless of who submits the PR |
| Traceability | Approved changes must cite the proposal artifacts that authorized them |
| Evolvability | Governance rules can themselves be changed — but only through a governed process |
| AI legibility | AI agents can author and review change proposals against declared governance schemas |

The last property is critical for AI-native architecture practices. An AI agent that generates a
solution design or proposes an API contract change must produce a change proposal artifact that
conforms to the declared governance schema. Governance as Code makes AI-authored changes auditable
by the same mechanism as human-authored changes.

---

## The Critical Distinction: Governance vs Policy

Pillar O (Governance as Code) is frequently confused with Pillar J (Policy as Code). They are
related but distinct:

**Policy as Code** (Pillar J) asks: *"Does this artifact's content conform to our rules?"*
- Mechanism: OPA Rego rules, Conftest policies
- Example: "Every OpenAPI spec must have a contact field" — a content rule
- Enforcement: Static analysis of file content on every PR

**Governance as Code** (Pillar O) asks: *"Was the process for making this change followed?"*
- Mechanism: Structured proposal artifacts, archived approval records, proposal-completeness checks
- Example: "Any change to an API spec must include a backward-compatibility assessment artifact
  signed by the owning team" — a process rule
- Enforcement: Presence and completeness of process artifacts before merge is permitted

Both are needed. Policy as Code prevents bad content from landing. Governance as Code ensures that
the process of introducing changes — including good content — was followed. A perfectly valid API
spec that was changed without a backward-compatibility assessment still violates governance.

The two pillars compose: a policy rule can verify that a governance artifact (e.g., a change
proposal) exists and is complete. This is the gate rule pattern described below.

---

## Governance Scope

Not all artifacts require formal governance. The governance scope is declared explicitly. In most
practices, the highest-governance artifact classes are:

| Artifact Class | Governance Rationale |
|----------------|---------------------|
| API contract specifications | Consumer-breaking changes require coordinated rollout |
| AI instruction files | AI behavior changes affect every AI-assisted workflow |
| Architecture decision records | Decisions govern other decisions; changing them has cascading effects |
| Policy rules | The rules that govern other artifacts must themselves be governed |
| Data schemas | Schema changes affect downstream consumers and may require migration |
| Governance specs themselves | The meta-level: changing governance requires governance |

The governance spec for each artifact class declares: what the artifact is, who owns it, what the
change workflow requires, and where completed change records are archived.

---

## The Governance Spec Schema

### governance/specs/{artifact-class}.yaml

```yaml
# governance/specs/api-contracts.yaml
$schema: "../schemas/governance-spec.schema.json"

spec_id: GOV-001
name: API Contract Governance
version: 1.1.0
governed_artifacts:
  - path_pattern: "architecture/specs/**/*.yaml"
    description: OpenAPI specification files (all services)
  - path_pattern: "architecture/events/**/*.yaml"
    description: AsyncAPI event schema files

ownership:
  owner_team: team-platform-architecture
  approvers:
    - role: Senior Architect
      minimum_required: 1
    - role: Owning Service Team Lead
      minimum_required: 1

change_workflow:
  proposal_template: governance/templates/api-contract-change-proposal.md
  required_sections:
    - motivation
    - backward_compatibility_assessment
    - consumer_impact_list
    - rollout_plan
  review_sla_days: 3
  archive_location: governance/archive/api-contracts/
  gate_rule: policies/governance/api-contract-proposal-completeness.rego

metadata:
  created: 2026-01-10
  last_reviewed: 2026-03-01
  governing_adr: ADR-007
```

```yaml
# governance/specs/ai-instructions.yaml
$schema: "../schemas/governance-spec.schema.json"

spec_id: GOV-002
name: AI Instruction Governance
version: 1.0.0
governed_artifacts:
  - path_pattern: ".github/copilot-instructions.md"
    description: Primary AI instruction file for GitHub Copilot
  - path_pattern: ".github/instructions/**/*.md"
    description: Supplementary instruction files

ownership:
  owner_team: team-platform-architecture
  approvers:
    - role: Architecture Practice Lead
      minimum_required: 1

change_workflow:
  proposal_template: governance/templates/ai-instruction-change-proposal.md
  required_sections:
    - change_scope
    - rationale
    - ai_behavior_impact_assessment
    - rollback_procedure
  review_sla_days: 2
  archive_location: governance/archive/ai-instructions/
  gate_rule: policies/governance/ai-instruction-proposal-completeness.rego

metadata:
  created: 2026-01-10
  last_reviewed: 2026-03-01
  governing_adr: ADR-009
```

### Governance spec field reference

| Field | Required | Description |
|-------|----------|-------------|
| `spec_id` | Yes | Unique identifier for this governance spec (e.g., `GOV-001`). Used in cross-references. |
| `name` | Yes | Human-readable name of the governance spec. |
| `version` | Yes | Semantic version of this spec. Changes to a governance spec increment this version. |
| `governed_artifacts` | Yes | List of path patterns that identify which files are under this governance spec. |
| `ownership.owner_team` | Yes | The team ID (from the team registry, Pillar AE) that owns governance of these artifacts. |
| `ownership.approvers` | Yes | Who must approve a change proposal. May include multiple roles with minimum counts. |
| `change_workflow.proposal_template` | Yes | Path to the Markdown template that change proposals must follow. |
| `change_workflow.required_sections` | Yes | Identifiers for the sections a proposal must contain. The gate rule verifies their presence. |
| `change_workflow.review_sla_days` | No | The maximum number of calendar days for proposal review. Exceeding this SLA triggers an alert. |
| `change_workflow.archive_location` | Yes | Directory where completed (approved or rejected) proposals are archived. |
| `change_workflow.gate_rule` | No | OPA Rego policy file that enforces proposal completeness in CI. |
| `metadata.governing_adr` | No | The ADR that established this governance spec. |

---

## The Change Proposal Format

Each governance spec references a proposal template. A completed proposal is a Markdown document
in the archive directory that serves as the permanent record of the change cycle.

### Example: API contract change proposal

```markdown
# Change Proposal: POST /check-in — Add wristband_id field

<!-- PROPOSAL-ID: CP-2026-001 -->
<!-- SPEC: GOV-001 -->
<!-- STATUS: approved -->
<!-- DATE: 2026-01-15 -->
<!-- APPROVED-BY: senior-architect-jane-doe, team-lead-checkin -->

## Motivation

NTK-10005 requires the check-in API to accept an RFID wristband tap as a verification method.
The `POST /check-in` endpoint must accept an optional `wristband_id` field. See ADR-003.

## Backward Compatibility Assessment

The `wristband_id` field is additive and optional. Existing consumers that do not send the field
will receive unchanged responses. The change is backward-compatible.

API version remains 2.0; a `2.1` bump is not required for additive optional fields per our
versioning policy (ADR-007).

## Consumer Impact List

| Consumer | Impact | Action Required |
|----------|--------|----------------|
| svc-check-in | New field accepted; no change to consumers of this endpoint | None |
| Existing kiosk clients | No change required for clients not using RFID | None |
| RFID-enabled kiosk clients | Must begin sending `wristband_id` on wristband tap | Client update required |

## Rollout Plan

1. Deploy svc-check-in with the updated spec accepting optional `wristband_id`
2. Confirm existing non-RFID check-in flows continue to pass contract tests
3. Deploy RFID-enabled kiosk firmware
4. Monitor error rates on `/check-in` for 24 hours post-deployment
```

---

## The Change Archive

Completed proposals are stored in the archive directory with a consistent naming convention:

```
governance/archive/api-contracts/
├── CP-2026-001-checkin-wristband-id.md    (approved)
├── CP-2026-002-reservations-guest-ref.md  (approved)
└── CP-2026-003-analytics-event-schema.md  (rejected — see inline rationale)
```

Proposals are never deleted from the archive. Rejected proposals are retained with the rejection
rationale recorded in the document header. The archive is the authoritative history of what was
proposed, who approved it, and why.

---

## Gate Rules

Gate rules are OPA Rego policies (Pillar J mechanism) that verify governance artifacts exist and
are complete before a governed artifact can be merged:

```rego
# policies/governance/api-contract-proposal-completeness.rego
package governance.api_contracts

import future.keywords.if
import future.keywords.in

deny[msg] if {
    # A PR touches a governed artifact path
    input.pull_request.changed_files[_].filename matches "architecture/specs/.+\\.yaml"
    
    # No completed change proposal exists for this PR
    not proposal_exists_for_pr(input.pull_request.number)
    
    msg := sprintf(
        "PR %d modifies an API spec but no completed change proposal found in governance/archive/api-contracts/. See governance/specs/api-contracts.yaml.",
        [input.pull_request.number]
    )
}

proposal_exists_for_pr(pr_number) if {
    some filename in input.governance_archive_files
    startswith(filename, "governance/archive/api-contracts/")
    contains(filename, sprintf("pr-%d", [pr_number]))
}
```

The gate rule composition:
- Policy as Code (Pillar J) enforces *what* can exist (valid content)
- Governance as Code (Pillar O) enforces *how* changes arrive (required process artifacts)

Both must pass before a PR can be merged.

---

## The Meta-Governance Rule

Governance specs are themselves governed artifacts. Any change to a governance spec — adding a
required section, changing who must approve, adjusting the review SLA — MUST go through a
change proposal process.

This is Pillar O's self-referential property: the governance spec for governance specs is
`governance/specs/governance-specs.yaml`. It is typically the most restrictive spec in the
registry: any change requires the architecture practice lead and at least one senior architect.

The meta-governance ADR (the ADR that established the governance-as-code approach itself) is the
final backstop. It records the rationale for why the practice chose structured governance over
informal review customs, and it establishes the amendment process for governance rules.

---

## CI Integration

```yaml
# .github/workflows/validate-governance.yml (excerpt)

- name: Validate governance spec schemas
  run: |
    for spec in governance/specs/*.yaml; do
      npx ajv validate \
        --schema governance/schemas/governance-spec.schema.json \
        --data "$spec"
    done

- name: Check governance proposal completeness (gate rules)
  run: |
    conftest test \
      --policy policies/governance/ \
      --input pr-metadata.json

- name: Check proposal archive completeness (SLA check)
  run: |
    python3 scripts/ci/check-governance-sla.py \
      --archive-dir governance/archive/ \
      --specs-dir governance/specs/ \
      --sla-report governance-sla-report.json

- name: Referential integrity — governance ADR references
  run: |
    python3 scripts/ci/check-governance-adrs.py \
      --specs-dir governance/specs/ \
      --decisions-dir decisions/
```

### Validation rules

| Rule | Description |
|------|-------------|
| Governance spec schema validation | All governance specs have required fields; version follows semver |
| Gate rule completeness | Every PR touching a governed artifact path must have a completed proposal in the archive |
| SLA check | Open proposals older than the declared `review_sla_days` trigger a warning |
| ADR referential integrity | ADR references in governance specs resolve to existing ADR files |
| Archive completeness | All archived proposals have a `STATUS` header set to `approved` or `rejected` |

---

## AI Fit

Governance as Code is the pillar that makes AI-authored architectural changes auditable:

**Proposal authoring**: An AI completing a solution design can generate a change proposal document
in the required format, completing all required sections from the solution design content. The human
reviewer then verifies and approves the proposal, not the free-form PR description.

**Completeness checking**: An AI reviewing a PR checks whether the PR touches any governed artifact
path and, if so, whether a completed proposal exists in the archive. It flags missing proposals
before the PR reaches human review.

**SLA monitoring**: An AI agent running on a schedule reads the archive and flags open proposals
that have exceeded their review SLA. This prevents proposals from stalling silently.

**Governance spec drafting**: When a new artifact class requires governance (e.g., a new category
of infrastructure-as-code file is added to the practice), an AI can draft the initial governance
spec YAML and proposal template, which a human then reviews.

---

## Governance Model

The governance model for Governance as Code is self-referential by design. There are three levels:

1. **The governance spec registry** (`governance/specs/`): Declares what is governed and how.
   Changes require a proposal reviewed by the architecture practice lead.

2. **Change proposals** (`governance/archive/`): The per-artifact change records. Authored following
   the template for their artifact class. Reviewed by the approvers declared in the governing spec.

3. **The meta-governance ADR**: The decision record that established the entire governance-as-code
   approach. Changing this ADR requires the same process as any other ADR (Pillar G), with the
   additional requirement that the architecture practice lead is an explicit approver.

---

## Recommended Practices

1. **Begin with one artifact class.** Start governance with the artifact class most frequently
   involved in production incidents — usually API contracts. Establish the full cycle (spec →
   template → archive → gate rule) before expanding to other artifact classes.

2. **Archive every proposal, including rejected ones.** Rejected proposals are as valuable as
   approved ones — they record what was considered and declined, and why. Do not delete them.

3. **Separate the gate rule from the content policy.** The gate rule checks that a proposal exists.
   A content policy checks that the proposal is complete (contains required sections). These are two
   distinct policy files even if they run in the same CI step.

4. **Set an SLA and enforce it.** Proposals that sit in review indefinitely are a governance
   failure. The SLA check in CI converts a cultural norm ("review proposals promptly") into an
   automated alert.

5. **Version governance specs.** When a governance spec changes, increment the version. Proposals
   filed against a spec must cite the spec version they were authored against, so that historical
   proposals are not invalidated by later spec changes.

6. **Do not govern everything.** Governance has overhead. Reserve it for artifact classes where
   unreviewed changes have caused — or could cause — significant harm. Governing too broadly
   produces a practice where everything is technically governed but nothing is actually reviewed.

---

## Synthetic Exemplar Status

> The status below describes how Pillar O has been implemented in the NovaTrek Adventures
> synthetic exemplar workspace. NovaTrek data is entirely fictional — no corporate systems are
> represented.

| Artifact | Status | Location |
|----------|--------|----------|
| Governance spec registry | Not yet created — planned in Transformation Wave 10 | `governance/specs/` |
| Governance spec schema | Not yet created | `governance/schemas/governance-spec.schema.json` |
| Change proposal templates | Not yet created | `governance/templates/` |
| Change archive directory | Not yet created | `governance/archive/` |
| Gate rule policy files | Not yet created | `policies/governance/` |
| CI governance validation workflow | Not yet wired | `.github/workflows/validate-governance.yml` |
| Meta-governance ADR | Not yet authored | `decisions/ADR-NNN-governance-as-code.md` |

The AI Instruction Governance document (`AI-INSTRUCTION-GOVERNANCE.md`) in this workspace
represents an early, informal implementation of the governance concept applied specifically to AI
instructions. It predates the Governance as Code pillar definition and does not follow the
structured spec/proposal/archive model. It will be migrated to the formal pattern as part of
Wave 10 adoption.

---

## Forward Plan

Pillar O adoption for NovaTrek is planned in **Wave 10** of the Transformation Plan, as a capstone
pillar. It benefits from the full CI pattern library established in earlier waves — particularly
Policy as Code (Pillar J) for gate rule execution and Decisions as Code (Pillar G) for governing
ADR authoring. See
[Transformation Plan — Pillar O](TRANSFORMATION-PLAN.md#pillar-o--governance-as-code) for the
sequenced adoption checklist.

---

## References

- DORA (DevOps Research and Assessment) — Change Management capability: https://dora.dev/capabilities/change-management/
- Open Policy Agent / Conftest — gate rule execution: https://www.conftest.dev
- GitOps principles (Weaveworks, 2017) — the foundation for treating operations as code, including governance operations
- ITIL 4 Change Enablement practice — the ITSM antecedent that Governance as Code replaces with machine-verifiable process
- NovaTrek AI Instruction Governance: [AI-INSTRUCTION-GOVERNANCE.md](AI-INSTRUCTION-GOVERNANCE.md) (early informal implementation)
- NovaTrek EaC Framework: [Pillar O definition](EVERYTHING-AS-CODE-FRAMEWORK.md)
- NovaTrek Transformation Plan: [Pillar O adoption steps](TRANSFORMATION-PLAN.md#pillar-o--governance-as-code)
