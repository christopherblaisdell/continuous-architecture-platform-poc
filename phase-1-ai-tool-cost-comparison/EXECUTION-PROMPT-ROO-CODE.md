# Phase 1 Execution Prompt: Roo Code (Architect Mode)

> **Purpose**: Self-contained prompt for executing all 5 Phase 1 architecture scenarios in a single, fresh Roo Code Architect Mode session. Paste the prompt section into a brand-new Roo Code chat with zero prior context.

---

## Pre-Execution Checklist (Human Steps)

### 1. Reset Workspace to Baseline

Run from the **repository root** (`continuous-architecture-platform-poc-2/`):

```bash
# Restore all modified workspace files to baseline state
git checkout e83f83e -- phase-1-ai-tool-cost-comparison/workspace/

# Remove all files that were added after baseline
git diff --name-only --diff-filter=A e83f83e..HEAD -- phase-1-ai-tool-cost-comparison/workspace/ | xargs rm -f

# Verify clean state
git diff --stat e83f83e -- phase-1-ai-tool-cost-comparison/workspace/
# Should show 0 files changed
```

### 2. Open Workspace

Open `phase-1-ai-tool-cost-comparison/workspace/novatrek-workspace.code-workspace` in VS Code. Roo Code will auto-load `.roo/rules/architect-rules.md`.

### 3. Start Fresh Chat

Open a **new** Roo Code Architect Mode chat. Do NOT reuse an existing conversation. Ensure the model is routed through Kong AI Gateway as configured.

### 4. Record Start Time

Note the wall-clock time before pasting the prompt.

### 5. Paste Everything Below the Line

Copy from `BEGIN PROMPT` to `END PROMPT` and paste as a single message.

---

<!-- ============================================================ -->
<!-- BEGIN PROMPT -->
<!-- ============================================================ -->

You are a Solution Architect for NovaTrek Adventures. You will execute 5 architecture scenarios in sequence against this workspace. Execute all 5 without stopping, asking for confirmation, or waiting for feedback between scenarios.

## Workspace Context

This workspace contains synthetic architecture artifacts for NovaTrek Adventures, a fictional outdoor adventure company. All data is synthetic — no corporate connections.

**Repository structure:**

| Folder | Purpose |
|--------|---------|
| `work-items/tickets/` | Active ticket investigations, analysis, solution designs |
| `corporate-services/services/` | Official OpenAPI/Swagger specs (19 microservices) |
| `corporate-services/diagrams/` | PlantUML architecture diagrams |
| `source-code/` | Microservice Java source code (read-only reference) |
| `architecture-standards/` | arc42, MADR, C4, ADR, ISO 25010 templates |
| `scripts/` | Mock tool scripts (local Python, no network calls) |

**Ticket folder convention** (underscore prefix, kebab-case):
```
_[TICKET-ID-BRIEF-TITLE]/
├── [TICKET-ID]-solution-design.md
├── 1.requirements/
│   └── [TICKET-ID].ticket.report.md
├── 2.analysis/
│   └── simple.explanation.md
└── 3.solution/
    ├── a.assumptions/assumptions.md
    ├── c.current.state/investigations.md
    ├── d.decisions/decisions.md
    ├── g.guidance/guidance.md
    ├── i.impacts/impacts.md
    └── s.user.stories/user-stories.md
```

**Mock tools** (all local Python scripts — use `python3`):

| Tool | Command |
|------|---------|
| JIRA — list tickets | `python3 scripts/mock-jira-client.py --list` |
| JIRA — filter by status | `python3 scripts/mock-jira-client.py --list --status "New"` |
| JIRA — get ticket | `python3 scripts/mock-jira-client.py --ticket NTK-10005` |
| Elastic — query logs | `python3 scripts/mock-elastic-searcher.py --service svc-scheduling-orchestrator --level ERROR` |
| GitLab — list MRs | `python3 scripts/mock-gitlab-client.py --project svc-scheduling-orchestrator --mrs` |

## Rules for All Scenarios

1. **NEVER fabricate data.** Only use data returned by mock scripts or found in workspace files.
2. **Read ALL relevant source files and specs BEFORE writing output.**
3. Use **MADR format** for all architecture decision records (reference `architecture-standards/madr/`).
4. Use **C4 model notation** for all PlantUML diagrams (reference `architecture-standards/c4-model/`).
5. **NO emojis** in documentation. Use "COMPLETE", "CRITICAL", "WARNING" etc.
6. **NO unvalidated quantified claims.** Use "significant improvement" not "99.9% cost reduction".
7. **NO special characters in Markdown headers** — letters, numbers, spaces only.
8. **Content separation**: impacts = WHAT changes architecturally; guidance = HOW to implement; user stories = user perspective only (no technical details).
9. If a file already exists, **read it first**, then update or enhance it. Do not create a duplicate.
10. Use impact subdirectories (`impact.1/impact.1.md`, `impact.2/impact.2.md`) when there are multiple affected services.

---

## SCENARIO 1 of 5: New Ticket Triage (NTK-10005)

**Working directory**: `work-items/tickets/_NTK-10005-wristband-rfid-field/`

**Starting state**: Only `1.requirements/NTK-10005.ticket.report.md` exists. Everything else must be created.

**Task**: Triage a new ticket — create the full workspace, classify architectural relevance.

**Steps**:
1. Run `python3 scripts/mock-jira-client.py --list --status "New"` to find available tickets.
2. Run `python3 scripts/mock-jira-client.py --ticket NTK-10005` to get the full Wristband RFID Field ticket details.
3. Read the existing ticket report at `1.requirements/NTK-10005.ticket.report.md`.
4. Create the following files:
   - `2.analysis/simple.explanation.md` — non-technical explanation suitable for stakeholders
   - `3.solution/a.assumptions/assumptions.md` — documented assumptions
   - `3.solution/c.current.state/investigations.md` — initial current state notes
   - `3.solution/d.decisions/decisions.md` — initial classification decision
   - `3.solution/g.guidance/guidance.md` — initial guidance notes
   - `3.solution/i.impacts/impacts.md` — initial impact assessment
   - `3.solution/s.user.stories/user-stories.md` — user stories
   - `NTK-10005-solution-design.md` — main solution design document
5. Classify whether this ticket is architecturally relevant or a code-level task. Ground your reasoning in the ticket description data.

---

## SCENARIO 2 of 5: Solution Design (NTK-10002)

**Working directory**: `work-items/tickets/_NTK-10002-adventure-category-classification/`

**Starting state**: Most files exist with initial content. Key file to enhance: `3.solution/d.decisions/decisions.md`.

**Task**: Create a full solution design for the Adventure Category Classification ticket.

**Steps**:
1. Read `1.requirements/NTK-10002.ticket.report.md` for ticket context.
2. Read `corporate-services/services/svc-check-in.yaml` (Swagger spec).
3. Read `corporate-services/services/svc-trip-catalog.yaml` (Swagger spec).
4. Read `source-code/svc-check-in/src/main/java/com/novatrek/checkin/service/AdventureCategoryClassifier.java`.
5. Review existing files in the ticket folder to understand current state.
6. Update `NTK-10002-solution-design.md` with:
   - Problem statement derived from ticket
   - Proposed solution with architectural approach
   - Service interaction changes
   - Data model modifications
7. Update `3.solution/d.decisions/decisions.md` with MADR-formatted architecture decisions:
   - Decision on classification approach (config-driven vs hardcoded) — this is a key architectural concern
   - Decision on API contract changes
8. Update impact assessments in `3.solution/i.impacts/` (use `impact.1/impact.1.md` and `impact.2/impact.2.md` subdirectories):
   - Impact on svc-check-in (API contract changes)
   - Impact on svc-trip-catalog (data model changes)
9. Update `3.solution/a.assumptions/assumptions.md`.
10. Update `3.solution/s.user.stories/user-stories.md` or `3.solution/u.user.stories/user-stories.md` — user stories must be free of technical implementation details.
11. Update `3.solution/g.guidance/guidance.md` with implementation guidance.
12. Update or create `3.solution/r.risks/risks.md` with risk assessment.

---

## SCENARIO 3 of 5: Investigation and Root Cause Analysis (NTK-10004)

**Working directory**: `work-items/tickets/_NTK-10004-guide-schedule-overwrite-bug/`

**Starting state**: Ticket report, analysis, assumptions, and a basic `investigations.md` exist. Solution design, decisions, guidance, impacts, risks, and user stories must be created.

**Task**: Investigate a production bug using logs, source code, and MR history. Document root cause and remediation.

**Steps**:
1. Read `1.requirements/NTK-10004.ticket.report.md` for ticket context.
2. Run `python3 scripts/mock-elastic-searcher.py --service svc-scheduling-orchestrator --level ERROR` to retrieve production error logs.
3. Read `source-code/svc-scheduling-orchestrator/src/main/java/com/novatrek/scheduling/service/SchedulingService.java` to find the root cause in code.
4. Run `python3 scripts/mock-gitlab-client.py --project svc-scheduling-orchestrator --mrs` to check merge request history.
5. Update `3.solution/c.current.state/investigations.md` with:
   - Timeline of errors from Elastic logs (cite the mock data)
   - Code analysis showing the PUT vs PATCH issue
   - MR history showing when the change was introduced
6. Identify and document the root cause. The critical insight: this is NOT just a code bug — it is an **architectural boundary violation**. The scheduling service uses PUT semantics (full entity replacement) that overwrites fields owned by the guest-profiles service. The fix requires both PATCH semantics AND establishing proper data ownership boundaries between services.
7. Create `3.solution/d.decisions/decisions.md` with MADR-formatted decision on remediation approach.
8. Create `3.solution/g.guidance/guidance.md` with implementation guidance.
9. Create `3.solution/i.impacts/impacts.md` with impact assessment.
10. Create `3.solution/r.risks/risks.md` with risk assessment.
11. Create `3.solution/s.user.stories/user-stories.md` with user stories.
12. Create `NTK-10004-solution-design.md` as the main solution design.

---

## SCENARIO 4 of 5: Update Corporate Architecture Artifacts (NTK-10001)

**Working directory**: `work-items/tickets/_NTK-10001-add-elevation-to-trail-response/`

**Starting state**: Full solution design exists and is approved. Corporate artifacts (Swagger spec, PlantUML diagram) need updating.

**Task**: The solution design for NTK-10001 (Add Elevation Profile Data) is approved. Update the corporate architecture artifacts to reflect it.

**Steps**:
1. Read the approved solution design at `NTK-10001-solution-design.md` to understand exactly what changes are needed.
2. Modify `corporate-services/services/svc-trail-management.yaml`:
   - Add elevation fields to the TrailDetail schema:
     - `elevationProfile` (array of elevation data points)
     - `elevationGain` (number, total elevation gain in meters)
     - `elevationLoss` (number, total elevation loss in meters)
     - `maxElevation` (number, peak elevation in meters)
     - `minElevation` (number, minimum elevation in meters)
   - Add proper types, descriptions, and examples
   - Ensure fields appear in the GET trail detail response
   - Changes must be **valid OpenAPI 3.0 syntax**
3. Update `corporate-services/diagrams/Components/novatrek-component-overview.puml`:
   - Add elevation data flow to the component diagram
   - Must be **valid, compilable PlantUML syntax**
4. Create `commit-message.md` in the ticket folder with a clear commit message referencing NTK-10001.

**Key constraint**: Changes must be LIMITED to what the solution design specifies. No scope creep — do not add fields or flows that are not in the approved design.

---

## SCENARIO 5 of 5: Complex Cross-Service Design (NTK-10003)

**Working directory**: `work-items/tickets/_NTK-10003-unregistered-guest-self-checkin/`

**Starting state**: Most files exist with initial content. Key files to enhance: `3.solution/d.decisions/decisions.md` (needs full MADR ADRs). A new C4 component diagram must be created.

**Task**: Create a comprehensive cross-service solution design for the Unregistered Guest Self-Service Check-In feature.

**Steps**:
1. Read `1.requirements/NTK-10003.ticket.report.md` for requirements.
2. Read ALL relevant Swagger specs:
   - `corporate-services/services/svc-check-in.yaml`
   - `corporate-services/services/svc-guest-profiles.yaml`
   - `corporate-services/services/svc-safety-compliance.yaml`
   - `corporate-services/services/svc-reservations.yaml`
3. Read relevant source code:
   - `source-code/svc-check-in/src/main/java/com/novatrek/checkin/controller/CheckInController.java`
   - Scan `source-code/svc-guest-profiles/` for relevant service files
4. Update `NTK-10003-solution-design.md` with:
   - Problem statement: unregistered guests cannot self-service check-in
   - Proposed new endpoint: POST /check-in/self-service/unregistered
   - Request schema with reservation lookup fields and identity verification
   - Response schema with temporary guest profile and check-in confirmation
   - Orchestration flow across the 4 affected services
   - Error handling and edge cases
5. Create a new C4 PlantUML component diagram at `corporate-services/diagrams/Components/ntk10003-unregistered-checkin-components.puml` showing:
   - New self-service check-in component
   - Interactions with guest-profiles, reservations, safety-compliance
   - Data flow direction and protocols
6. Create a PlantUML sequence diagram (place in `corporate-services/diagrams/Sequence/` or alongside the solution design) showing:
   - Guest initiates self-service check-in
   - Reservation lookup by confirmation code
   - Identity verification step
   - Temporary guest profile creation
   - Safety compliance check
   - Check-in confirmation
7. Update `3.solution/d.decisions/decisions.md` with MADR-formatted ADRs:
   - ADR: Identity Verification Approach (options: confirmation code only, confirmation + ID scan, confirmation + biometric)
   - ADR: Temporary Guest Profiles (options: full profile, ephemeral profile, linked-to-reservation profile)
   - ADR: Orchestration Pattern (options: choreography, orchestration, hybrid)
8. Update impact assessments using separate subdirectories under `3.solution/i.impacts/`:
   - `impact.1/impact.1.md` — svc-check-in: new endpoint, new controller logic
   - `impact.2/impact.2.md` — svc-guest-profiles: temporary profile creation API
   - `impact.3/impact.3.md` — svc-safety-compliance: unregistered guest compliance flow
   - `impact.4/impact.4.md` — svc-reservations: reservation lookup by confirmation code
9. Update `3.solution/r.risks/risks.md` covering security risk (identity verification), data risk (temporary profiles), operational risk (check-in load), compliance risk (safety for unregistered guests).
10. Update `3.solution/g.guidance/guidance.md` with implementation guidance.
11. Update `3.solution/s.user.stories/user-stories.md` or `3.solution/u.user.stories/user-stories.md` covering guest, staff, and system perspectives.

---

## Post-Execution Summary

After completing all 5 scenarios, provide a brief summary listing:
- Total files created and modified
- Total mock script executions (count each `python3 scripts/mock-*.py` invocation)
- Total tool calls (file reads, file creates, terminal commands)
- Any scenarios where you encountered issues, retried, or made corrections

<!-- ============================================================ -->
<!-- END PROMPT -->
<!-- ============================================================ -->

---

## Post-Execution Steps (Human)

1. **Record wall-clock time** (start to completion).
2. **Capture the run** (from repository root):
   ```bash
   # Auto-assigns next run number (001, 002, ...)
   ./phase-1-ai-tool-cost-comparison/scripts/capture-run.sh roo-code
   ```
   This snapshots all workspace changes into `outputs/roo-code/<RUN>/`, including:
   - `workspace-diff.patch` — full git diff from baseline
   - `workspace-snapshot/` — copy of all changed/created files
   - `run-metadata.md` — template for timing and cost data
   - `results.md` — copy of results file (if present in workspace)
3. **Fill in `run-metadata.md`** with start time, end time, wall-clock duration, and cost.
4. **Score each scenario** using the rubrics in:
   - `playbooks/scenario-01-new-ticket-triage.md` (max 25)
   - `playbooks/scenario-02-solution-design.md` (max 35)
   - `playbooks/scenario-03-investigation-analysis.md` (max 30)
   - `playbooks/scenario-04-architecture-update.md` (max 25)
   - `playbooks/scenario-05-complex-cross-service.md` (max 40)
5. **Create or update `results.md`** in the run folder documenting scores, observable metrics, and notes.
6. **Run data isolation audit**: `../../scripts/audit-data-isolation.sh`
7. **Commit the captured run**:
   ```bash
   git add -A && git commit -m 'feat: capture Phase 1 Roo Code run <RUN>'
   ```
8. **Reset workspace** before the next run:
   ```bash
   git checkout e83f83e -- phase-1-ai-tool-cost-comparison/workspace/
   git diff --name-only --diff-filter=A e83f83e..HEAD -- phase-1-ai-tool-cost-comparison/workspace/ | xargs rm -f
   ```
