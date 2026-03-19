# Solution Design Workflow

This is the most important page for a new architect. It walks through the complete process of creating a solution design — from receiving a ticket to delivering an approved, published design.

---

## Overview

A solution design is the architect's primary deliverable. It documents what needs to change across the platform to satisfy a ticket's requirements, why specific approaches were chosen, and what developers need to know to implement the changes.

Every solution design follows this lifecycle:

```
Ticket received → Research → Prior-art discovery → Solution folder created →
  Analysis → Impact assessments → Decisions → Risks → User stories →
    Capability mapping → Master document → Portal generation → Review → Approval
```

---

## Step 1: Receive and Triage the Ticket

Start with the ticket. Read it thoroughly.

### Gather ticket data

```bash
# List all tickets
python3 scripts/ticket-client.py --list

# Get a specific ticket
python3 scripts/ticket-client.py --list --status "New"

# For Phase 1 mock environment, use mock JIRA
python3 scripts/mock-jira-client.py --ticket NTK-10005
```

### Assess architectural relevance

Not every ticket needs a solution design. A ticket is architecturally significant if it:

- Crosses service boundaries (requires changes to multiple services)
- Changes data semantics (modifies what a field means or how it's used)
- Introduces new integration patterns (new API calls, new events)
- Affects safety or security workflows
- Requires a new service or data store
- Changes an existing API contract in a breaking way

If the ticket is purely an implementation concern (performance tuning within one service, UI styling changes, bug fix with no architectural impact), it does not need a solution design.

---

## Step 2: Research and Investigation

Before designing, gather evidence. Never guess what the current state is.

### Run tools in this order

1. **JIRA first** — get the authoritative ticket description and comments
2. **Elastic second** — check production logs for symptoms, error patterns, and usage data
3. **GitLab third** — review recent merge requests for related code changes
4. **Specs and source code** — read the OpenAPI specs and Java source to understand current behavior

```bash
# Production logs
python3 scripts/mock-elastic-searcher.py --service svc-scheduling-orchestrator --level ERROR
python3 scripts/mock-elastic-searcher.py --query "timeout"

# Recent merge requests
python3 scripts/mock-gitlab-client.py --project svc-scheduling-orchestrator --mrs
python3 scripts/mock-gitlab-client.py --mr 5001
```

### Read the OpenAPI specs

The specs in `architecture/specs/` are the definitive API contracts. Read the relevant ones:

```bash
# Example: understanding the check-in API
cat architecture/specs/svc-check-in.yaml
```

### Analyze source code (when available)

When source code is available in `services/`, read it to understand current behavior:

1. Trace the flow: controller -> service -> repository
2. Check for anti-patterns (see [Anti-Patterns](anti-patterns.md))
3. Note specific line numbers for all findings
4. Cross-reference source behavior with the OpenAPI spec

---

## Step 3: Prior-Art Discovery (REQUIRED)

Before creating anything new, search for existing work that overlaps.

### Check capability history

```bash
# Find tickets that touched the same capabilities
python3 scripts/ticket-client.py --list --capability CAP-2.1

# Filter by affected service
python3 scripts/ticket-client.py --list --service svc-check-in
```

### Review existing solutions

Browse `architecture/solutions/` for related work. Read the capability mappings in each solution's `3.solution/c.capabilities/capabilities.md`.

### Check the changelog

Review `architecture/metadata/capability-changelog.yaml` for L3 capabilities that may overlap with your design.

### Reference prior decisions

Search `decisions/` for ADRs that constrain the design space. If a decision has already been made about the pattern you're considering, reference it — do not re-decide settled questions.

### Document findings

Reference prior solutions in your master document under a "Prior Art" or "Related Solutions" section.

---

## Step 4: Create the Solution Branch and Folder

### Branch naming convention

```bash
git checkout -b solution/NTK-XXXXX-slug
```

Examples: `solution/NTK-10005-wristband-rfid-field`, `solution/NTK-10008-guest-reviews`

### Create the folder structure

```bash
TICKET="NTK-XXXXX"
SLUG="short-description"

mkdir -p "architecture/solutions/_${TICKET}-${SLUG}"/{1.requirements,2.analysis,3.solution/{a.assumptions,c.capabilities,d.decisions,g.guidance,i.impacts,r.risks,u.user.stories}}
```

### Populate initial files

Create the master document using the [Solution Design Template](../standards/solution-design/solution-design-template.md) as your starting point.

---

## Step 5: Write the Analysis

### Requirements report (`1.requirements/`)

Capture the ticket's requirements. This is a factual report of what the ticket asks for, not your analysis.

### Simple explanation (`2.analysis/`)

Write a plain-language explanation of the problem that a non-technical stakeholder could understand. No jargon, no API references, no code snippets.

---

## Step 6: Design the Solution

### Impact assessments (`3.solution/i.impacts/`)

For each affected service, create an impact assessment documenting:

- WHAT changes (API contract modifications, new endpoints, data model changes)
- Schema diffs (before/after for changed fields)
- Sequence diagrams showing the modified workflow

Impact assessments focus on WHAT changes, not HOW to implement. If you find yourself writing code, you've crossed into guidance territory.

When multiple services are affected, use subdirectories: `impact.1/impact.1.md`, `impact.2/impact.2.md`.

### Decisions (`3.solution/d.decisions/decisions.md`)

Write MADR-formatted decisions for every choice that:

- Crosses service boundaries
- Changes data semantics
- Introduces a new pattern
- Has at least 2 genuinely viable alternatives

See [Architecture Decisions](decisions.md) for the MADR format and requirements.

### Assumptions (`3.solution/a.assumptions/`)

Document conditions assumed true but not verified. Each assumption has:

- A clear premise (WHAT is assumed)
- A rationale (WHY the assumption is reasonable)
- A status (VALIDATED or PROPOSED)
- A priority (CRITICAL / HIGH / MEDIUM / LOW)

### Risks (`3.solution/r.risks/`)

Identify what could go wrong. Each risk has:

- A risk statement (WHAT could happen)
- A risk level (VERY LOW / LOW / MEDIUM / HIGH / CRITICAL)
- A mitigation status (FULLY MITIGATED / ACCEPTED / MONITORING)

### User stories (`3.solution/u.user.stories/`)

Write user stories from the user's perspective with acceptance criteria. These directly drive BDD test scenarios (see [Testing Guide](testing-guide.md)).

```
As a [actor]
I want to [action]
So that [benefit]

Acceptance Criteria:
1. [Criterion 1]
2. [Criterion 2]
3. [Criterion 3]
```

### Capabilities (`3.solution/c.capabilities/capabilities.md`)

Map the solution to affected business capabilities. This file is descriptive — it references `architecture/metadata/capability-changelog.yaml`, which is the single source of truth.

### Guidance (`3.solution/g.guidance/`) — optional

Implementation guidance helps developers understand HOW to implement the design. Include code patterns, configuration examples, and migration steps. This is separate from the impact assessment (WHAT) and decisions (WHY).

---

## Step 7: Capability Rollup (REQUIRED)

Every solution MUST record capability changes in the single source of truth.

### Add to capability-changelog.yaml

```yaml
# architecture/metadata/capability-changelog.yaml
- ticket: NTK-XXXXX
  date: "2026-03-19"
  summary: One-line summary of the architectural change
  capabilities:
    - id: CAP-2.1
      impact: enhanced
      description: What changed for this capability
      l3_capabilities:
        - name: Descriptive L3 Capability Name
          description: What this emergent capability does
  decisions:
    - id: ADR-NNN
      title: Decision title
```

### Update capabilities.md

Write a narrative summary in `3.solution/c.capabilities/capabilities.md` listing affected CAP-X.Y IDs. This file is descriptive only — generators read from the changelog.

!!! warning "Do NOT duplicate"
    Do not duplicate capability or decision data in `tickets.yaml`. For solved tickets, capability mappings and decisions are derived from the changelog by generators. Only unsolved tickets use `planned_capabilities` in `tickets.yaml`.

---

## Step 8: Write the Master Document

The master document (`NTK-XXXXX-solution-design.md`) is the top-level summary. Use the [Solution Design Template](../standards/solution-design/solution-design-template.md).

Key sections:

- Metadata table (architect, ticket, capabilities, status, impacted services, related ADRs)
- Overview with problem statement and solution summary
- Component architecture with affected components table
- Per-component modification sections with sequence diagrams
- Assumptions, decisions, and risks summary tables
- Links to detailed sub-documents

---

## Step 9: Generate and Publish

### Regenerate portal pages

```bash
bash portal/scripts/generate-all.sh
```

This generates solution pages, capability pages, and ticket pages from your new content.

### Preview locally

```bash
cd portal && python3 -m mkdocs serve
```

Open `http://localhost:8000` and verify your solution page renders correctly.

### Push and merge

```bash
git add .
git commit -m "feat(solution): NTK-XXXXX short description"
git push origin solution/NTK-XXXXX-slug
```

Open a pull request. CI runs `validate-solution` checks. After review and approval, merge to `main`. CI deploys the updated portal automatically.

---

## Checklist Before Finalizing

Use this checklist before submitting your solution for review:

- [ ] All data sourced from mock tools or workspace files (no fabrication)
- [ ] Every affected service identified with specific API/schema changes
- [ ] MADR ADRs created for decisions that cross service boundaries or change data semantics
- [ ] At minimum 2 options genuinely considered in each ADR (not straw-man alternatives)
- [ ] Impact assessments focus on WHAT changes (not HOW to implement)
- [ ] User stories written from user perspective without technical implementation details
- [ ] C4 notation used for all diagrams with relationship labels
- [ ] ISO 25010 quality attributes considered (at minimum: reliability, maintainability, compatibility)
- [ ] No quantified claims without evidence
- [ ] Cross-service data ownership boundaries respected
- [ ] Backward compatibility addressed for all API contract changes
- [ ] Error handling and fallback paths defined for new integration points
- [ ] Security implications assessed for any data flow involving PII or authentication
- [ ] Capability changelog updated in `capability-changelog.yaml`
- [ ] Prior-art discovery completed and documented

---

## Worked Example

For a complete example of this workflow applied to a real ticket, read the [NTK-10005 Wristband RFID](../solutions/_NTK-10005-wristband-rfid-field.md) solution design. It demonstrates:

- Ticket analysis and research findings
- Prior-art discovery
- Multi-service impact assessments with sequence diagrams
- MADR decisions with genuine alternatives
- Risk identification and mitigation
- User stories with acceptance criteria
- Capability mapping and changelog entry
