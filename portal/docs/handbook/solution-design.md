---
tags:
  - handbook
  - workflow
  - solution-design
---

<!-- PUBLISH -->

<div class="hero" markdown>

# Solution Design

<p class="subtitle">How to create a complete solution design — from branch creation to merged PR</p>

</div>

A solution design is the primary deliverable of a solution architect. It captures what needs to change, why, and the architectural implications — without specifying how implementation is done.

This guide walks through every step from creating the branch to merging the PR.

---

## End-to-End Workflow

```
1. Create branch            solution/NTK-XXXXX-slug
2. Discover prior art       ticket-client, capability-changelog.yaml
3. Create folder            architecture/solutions/_NTK-XXXXX-slug/
4. Gather requirements      1.requirements/
5. Write analysis           2.analysis/
6. Write solution           3.solution/ (assumptions, capabilities, decisions,
                                        guidance, impacts, risks, user stories)
7. Update capability log    architecture/metadata/capability-changelog.yaml
8. Run generators           bash portal/scripts/generate-all.sh
9. Raise PR                 PR to main, link ticket
```

---

## Step 1 — Create the Branch

All solution design work happens on a dedicated branch. Never commit solution work directly to `main`.

```bash
git checkout main
git pull
git checkout -b solution/NTK-10005-wristband-rfid-field
```

Branch naming convention: `solution/NTK-XXXXX-slug`

- `NTK-XXXXX` — the ticket number
- `slug` — kebab-case description of the change (3-5 words)

---

## Step 2 — Discover Prior Art

Before creating any files, search for related prior work.

```bash
# Find tickets that affected the same capabilities
python3 architecture/scripts/ticket-client.py --list --capability CAP-2.1

# Find tickets affecting the same service
python3 architecture/scripts/ticket-client.py --list --service svc-check-in

# Review the capability changelog for overlapping L3 capabilities
cat architecture/metadata/capability-changelog.yaml
```

Browse existing solution folders for related work:

```bash
ls architecture/solutions/
```

Document what you find in the **Related Solutions** section of your master document.

---

## Step 3 — Create the Solution Folder

Create the folder with the full prescribed structure:

```bash
# From repo root
TICKET=NTK-10005
SLUG=wristband-rfid-field
FOLDER="architecture/solutions/_${TICKET}-${SLUG}"

mkdir -p "$FOLDER/1.requirements"
mkdir -p "$FOLDER/2.analysis"
mkdir -p "$FOLDER/3.solution/a.assumptions"
mkdir -p "$FOLDER/3.solution/c.capabilities"
mkdir -p "$FOLDER/3.solution/d.decisions"
mkdir -p "$FOLDER/3.solution/g.guidance"
mkdir -p "$FOLDER/3.solution/i.impacts"
mkdir -p "$FOLDER/3.solution/r.risks"
mkdir -p "$FOLDER/3.solution/u.user.stories"
```

The full folder structure:

```
architecture/solutions/_NTK-XXXXX-slug/
├── NTK-XXXXX-solution-design.md          ← master document (primary deliverable)
├── 1.requirements/
│   └── requirements.md                   ← ticket report / requirement summary
├── 2.analysis/
│   └── analysis.md                       ← simple explanation for non-technical stakeholders
└── 3.solution/
    ├── a.assumptions/
    │   └── assumptions.md                ← what is assumed true but not verified
    ├── c.capabilities/
    │   └── capabilities.md               ← narrative; references capability-changelog.yaml
    ├── d.decisions/
    │   └── decisions.md                  ← MADR-format ADRs (one or more)
    ├── g.guidance/
    │   └── guidance.1/
    │       └── guidance.1.md             ← optional implementation guidance
    ├── i.impacts/
    │   └── impact.1/
    │       └── impact.1.md               ← per-service impact assessment
    ├── r.risks/
    │   └── risks.md                      ← risk register
    └── u.user.stories/
        └── user-stories.md               ← user stories with acceptance criteria
```

---

## Step 4 — Write the Requirements Document

`1.requirements/requirements.md` is a clean statement of what the ticket asks for — written in the architect's voice, not copied verbatim from the ticket.

Include:
- Ticket reference and summary
- Business context
- Stated requirements (numbered list)
- Out of scope items

---

## Step 5 — Write the Analysis

`2.analysis/analysis.md` is a plain-language explanation of the problem and proposed approach, written for non-technical stakeholders. No jargon, no API references, no code snippets.

---

## Step 6 — Write the Solution Components

### 6a. Assumptions (`a.assumptions/assumptions.md`)

List everything that is assumed true but not yet verified. Assumptions are inputs to decisions — they are not decisions themselves.

```markdown
1. The wristband RFID reader communicates via REST to svc-check-in.
2. Existing wristband IDs are globally unique UUIDs.
3. No back-fill of historical check-in records is required.
```

### 6b. Capabilities (`c.capabilities/capabilities.md`)

Write a narrative summary of which capabilities this solution affects. Reference the `capability-changelog.yaml` — do not duplicate data here.

```markdown
This solution enhances **CAP-2.1 (Check-In Orchestration)** by adding RFID
wristband assignment to the check-in flow. A new L3 capability, "RFID
Wristband Assignment", emerges from this solution.

See `architecture/metadata/capability-changelog.yaml` entry for NTK-10005
for the full capability mapping.
```

### 6c. Decisions (`d.decisions/decisions.md`)

Write all ADRs in MADR format. Use H2 separators between multiple decisions in the same file.

Every ADR must include:
1. **Status** — Proposed / Accepted / Deprecated / Superseded
2. **Date** — ISO 8601 (YYYY-MM-DD)
3. **Context and Problem Statement** — 2-3 sentences
4. **Decision Drivers** — minimum 3 criteria
5. **Considered Options** — minimum 2 genuine options with pros/cons
6. **Decision Outcome** — selected option with justification
7. **Consequences** — Positive, Negative, and Neutral sections (all three required)

See the [MADR template](../standards/madr/adr-template.md) for the full format.

Cross-domain decisions should be copied to `decisions/` as a new global ADR (numbering follows the sequence in that directory).

### 6d. Guidance (`g.guidance/`)

Guidance is optional. Use it when implementation teams need specific patterns, configuration examples, or migration steps. Keep it separate from impact assessments — guidance says **how to implement**, not what changes architecturally.

### 6e. Impact Assessments (`i.impacts/`)

One impact assessment per affected service. Name subdirectories `impact.1/`, `impact.2/`, etc.

Each impact assessment focuses on **what changes architecturally**:

- API contract changes (endpoint additions/modifications, schema changes)
- Data model modifications (new tables, columns, indexes)
- Integration point changes (new cross-service calls, event subscriptions)
- Security implications

Impact assessments do NOT contain implementation code, deployment steps, or timelines.

If multiple services are affected, create a separate subdirectory for each:

```
i.impacts/
  impact.1/impact.1.md       ← svc-check-in impact
  impact.2/impact.2.md       ← svc-reservations impact
```

### 6f. Risks (`r.risks/risks.md`)

Document risks using a register format:

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Wristband ID collision with legacy system | Low | High | UUID v4 generation in svc-check-in |

### 6g. User Stories (`u.user.stories/user-stories.md`)

Write from the user's perspective. Include acceptance criteria. No technical implementation details.

```markdown
## US-001 — Staff can assign a wristband during check-in

**As** an operations staff member checking in a guest,
**I want** to scan an RFID wristband and have it assigned to the guest's check-in record,
**So that** the guest can access gated adventure areas without showing ID.

**Acceptance Criteria:**
- Staff can scan a wristband using the handheld RFID reader
- The system confirms the wristband is unassigned before assigning it
- An error is shown if the wristband is already assigned to another guest
- The check-in record updates to show the wristband ID
```

---

## Step 7 — Write the Master Document

`NTK-XXXXX-solution-design.md` is the primary deliverable. It provides an executive summary and ties together all the subcomponents.

Required header table:

```markdown
| | |
|---|---|
| **Solution Architect** | [Name] |
| **Solution Name** | [Descriptive name] |
| **Ticket** | NTK-XXXXX |
| **Capabilities** | CAP-X.Y (enhances), CAP-X.Y (new) |
| **Status** | DRAFT |
| **Impacted Services** | svc-check-in, svc-reservations |
| **Related ADRs** | ADR-006 |
| **Supersedes** | — |
```

Version the document: `# Solution Name v1.0`, bumping to `v1.1` on revisions.

---

## Step 8 — Update the Capability Changelog

`architecture/metadata/capability-changelog.yaml` is the **single source of truth** for capability changes. Every solution design must add an entry here.

```yaml
entries:
  # ... existing entries ...

  - ticket: NTK-10005
    date: 2026-03-15
    solution: _NTK-10005-wristband-rfid-field
    summary: Add RFID wristband field to check-in record
    capabilities:
      - id: CAP-2.1
        impact: enhanced
        description: Check-in record now supports RFID wristband assignment
        l3_capabilities:
          - name: RFID Wristband Assignment
            description: Staff can assign an RFID wristband to a guest check-in record during the check-in flow
    decisions:
      - ADR-006    # only if a new global ADR was created
```

**Impact values:**

| Value | Meaning |
|---|---|
| `new` | A new capability is introduced |
| `enhanced` | An existing capability gains new scope or depth |
| `fixed` | A broken capability is restored to intended behavior |

**Do NOT** add `planned_capabilities` to `tickets.yaml` for solved tickets — capability mappings are derived from the changelog by generators.

---

## Step 9 — Register the Ticket (if New)

If the ticket does not yet exist in `architecture/metadata/tickets.yaml`, add it:

```yaml
- id: NTK-10005
  title: Add RFID wristband field to check-in wristband assignment
  status: In Progress
  priority: medium
  type: enhancement
  services:
    - svc-check-in
  domains:
    - Operations
  description: >
    The wristband_id field is missing from the check-in record. Staff
    cannot associate an RFID wristband with a guest check-in.
  created: 2026-03-01
  updated: 2026-03-15
```

---

## Step 10 — Run Portal Generators

After all files are written, regenerate the portal to include the new solution:

```bash
# From repo root
bash portal/scripts/generate-all.sh
```

This runs all generators, builds MkDocs, and copies assets. Review the output for errors.

If you only want to regenerate solution and ticket pages (faster):

```bash
python3 portal/scripts/generate-solution-pages.py
python3 portal/scripts/generate-ticket-pages.py
python3 portal/scripts/generate-capability-pages.py
```

---

## Step 11 — Raise the Pull Request

```bash
git add .
git commit -m "solution: NTK-10005 — RFID wristband field"
git push -u origin solution/NTK-10005-wristband-rfid-field
```

Open a PR against `main`. PR title convention: `solution: NTK-XXXXX — [short description]`.

In the PR description include:
- Link to the ticket
- Summary of architectural changes
- List of affected services
- Any new ADRs
- Confirmation that generators have been run

---

## Architecture Review Checklist

Before submitting the PR, verify:

- [ ] All data sourced from tools or workspace files — nothing fabricated
- [ ] Every affected service identified with specific API/schema changes
- [ ] MADR ADRs created for decisions that cross service boundaries or change data semantics
- [ ] At least 2 options genuinely considered in each ADR
- [ ] Impact assessments say WHAT changes (not HOW to implement)
- [ ] User stories written from user perspective without implementation details
- [ ] C4 notation used for any diagrams, with relationship labels
- [ ] ISO 25010 quality attributes considered (minimum: reliability, maintainability, compatibility)
- [ ] No quantified claims without evidence
- [ ] Cross-service data ownership boundaries respected
- [ ] Backward compatibility addressed for all API contract changes
- [ ] Error handling and fallback paths defined for new integration points
- [ ] Security implications assessed for any data flow involving PII or authentication
- [ ] `capability-changelog.yaml` updated
- [ ] Generators run successfully

---

!!! tip "Related guides"
    - [Working a Ticket](working-a-ticket.md) — triage before starting a solution design
    - [API Contract Changes](api-contracts.md) — when the solution changes an OpenAPI spec
    - [Database Changes](database-changes.md) — when the solution changes a data store
    - [Writing ADRs](../standards/madr/index.md) — MADR format reference
    - [Solution Design Template](../standards/solution-design/solution-design-template.md) — master document template
