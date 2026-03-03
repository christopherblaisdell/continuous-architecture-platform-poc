# Roo Code Execution Prompt for Phase 1 Scenario Comparison

> **Purpose**: Paste this prompt into Roo Code (Architect mode via Kong AI Gateway) to execute the same 5 architecture scenarios that GitHub Copilot completed. This enables a fair, head-to-head comparison of quality, cost, and workflow for Phase 1 of the Continuous Architecture Platform POC.

## Pre-Execution Setup

Before pasting the prompt below, complete these steps:

### 1. Reset Workspace to Pre-Execution Baseline

The workspace must match the state before Copilot executed (commit `e83f83e`). Run these commands from the workspace root (`phase-1-ai-tool-cost-comparison/workspace/`):

```bash
# Remove all Copilot-created artifacts (files that did not exist before Copilot ran)
# SC-01 artifacts (NTK-10005 — Copilot created these from scratch)
rm -f work-items/tickets/_NTK-10005-wristband-rfid-field/2.analysis/simple.explanation.md
rm -f work-items/tickets/_NTK-10005-wristband-rfid-field/3.solution/a.assumptions/assumptions.md
rm -f work-items/tickets/_NTK-10005-wristband-rfid-field/3.solution/c.current.state/investigations.md
rm -f work-items/tickets/_NTK-10005-wristband-rfid-field/3.solution/d.decisions/decisions.md
rm -f work-items/tickets/_NTK-10005-wristband-rfid-field/3.solution/g.guidance/guidance.md
rm -f work-items/tickets/_NTK-10005-wristband-rfid-field/3.solution/i.impacts/impacts.md
rm -f work-items/tickets/_NTK-10005-wristband-rfid-field/3.solution/s.user.stories/user-stories.md
rm -f work-items/tickets/_NTK-10005-wristband-rfid-field/NTK-10005-solution-design.md

# SC-03 artifacts (NTK-10004 — Copilot created new files and modified investigations.md)
rm -f work-items/tickets/_NTK-10004-guide-schedule-overwrite-bug/3.solution/d.decisions/decisions.md
rm -f work-items/tickets/_NTK-10004-guide-schedule-overwrite-bug/3.solution/g.guidance/guidance.md
rm -f work-items/tickets/_NTK-10004-guide-schedule-overwrite-bug/3.solution/i.impacts/impacts.md
rm -f work-items/tickets/_NTK-10004-guide-schedule-overwrite-bug/3.solution/r.risks/risks.md
rm -f work-items/tickets/_NTK-10004-guide-schedule-overwrite-bug/3.solution/s.user.stories/user-stories.md
rm -f work-items/tickets/_NTK-10004-guide-schedule-overwrite-bug/NTK-10004-solution-design.md

# SC-04 artifacts (NTK-10001 — Copilot created commit-message.md)
rm -f work-items/tickets/_NTK-10001-add-elevation-to-trail-response/commit-message.md

# SC-05 artifacts (NTK-10003 — Copilot created a new C4 diagram)
rm -f corporate-services/diagrams/Components/ntk10003-unregistered-checkin-components.puml

# Restore Copilot-MODIFIED files to their pre-execution state
git checkout e83f83e -- \
  corporate-services/services/svc-trail-management.yaml \
  corporate-services/diagrams/Components/novatrek-component-overview.puml \
  work-items/tickets/_NTK-10002-adventure-category-classification/3.solution/d.decisions/decisions.md \
  work-items/tickets/_NTK-10003-unregistered-guest-self-checkin/3.solution/d.decisions/decisions.md \
  work-items/tickets/_NTK-10004-guide-schedule-overwrite-bug/3.solution/c.current.state/investigations.md
```

### 2. Verify Clean State

```bash
# These ticket folders should exist with pre-populated partial content:
ls work-items/tickets/_NTK-10001-add-elevation-to-trail-response/
ls work-items/tickets/_NTK-10002-adventure-category-classification/
ls work-items/tickets/_NTK-10003-unregistered-guest-self-checkin/
ls work-items/tickets/_NTK-10004-guide-schedule-overwrite-bug/
ls work-items/tickets/_NTK-10005-wristband-rfid-field/

# NTK-10005 should only have:
#   1.requirements/NTK-10005.ticket.report.md  (pre-existing)
# NTK-10004 should only have:
#   1.requirements/NTK-10004.ticket.report.md
#   2.analysis/simple.explanation.md
#   3.solution/a.assumptions/assumptions.md
#   3.solution/c.current.state/investigations.md  (pre-existing, not Copilot-enriched)
```

### 3. Open the NovaTrek Workspace

Open `novatrek-workspace.code-workspace` in VS Code with Roo Code extension active. Ensure Roo Code is configured to use Kong AI Gateway routing to Claude Sonnet on Bedrock.

### 4. Activate Architect Mode

Roo Code should load the `.roo/rules/architect-rules.md` file automatically. Verify the rules are active before starting.

### 5. Start Kong AI Token Logging

Enable Kong Admin API logging or Bedrock CloudWatch metrics to capture per-request token counts. Record the start timestamp.

---

## The Prompt

Copy everything below the line and paste it as a single message into Roo Code chat.

---

I need you to execute 5 architecture scenarios in sequence for the NovaTrek Adventures workspace. These scenarios test your ability to perform Solution Architecture work: ticket triage, solution design, investigation, corporate artifact updates, and complex cross-service design.

**CRITICAL RULES FOR ALL SCENARIOS:**
- Use the mock tool scripts (`scripts/mock-jira-client.py`, `scripts/mock-elastic-searcher.py`, `scripts/mock-gitlab-client.py`) to gather data. These are local Python scripts reading JSON files — no network calls.
- Run them with `python3 scripts/mock-jira-client.py` (use `python3`, not `python`).
- NEVER fabricate data. Only use what the mock scripts return or what exists in workspace files.
- Follow the folder structure defined in `.ai-instructions/main-instructions.md`.
- Use MADR format for all architectural decision records (reference `architecture-standards/madr/`).
- Use C4 model notation for all PlantUML diagrams (reference `architecture-standards/c4-model/`).
- NO emojis in documentation. NO unvalidated quantified claims. NO special characters in headers.
- Separate content: impacts = WHAT changes; guidance = HOW to implement; user stories = user perspective only.
- Read ALL relevant source files and specs BEFORE writing any output.

Execute all 5 scenarios below in order without stopping between them.

---

### SCENARIO 1: New Ticket Triage (NTK-10005)

**Task**: Triage a new ticket.

1. Run `python3 scripts/mock-jira-client.py --list --status "New"` to find available tickets.
2. Run `python3 scripts/mock-jira-client.py --ticket NTK-10005` to get full details for the Wristband RFID Field ticket.
3. Create the workspace folder `work-items/tickets/_NTK-10005-wristband-rfid-field/` with the standard folder structure if any parts are missing.
4. Write `2.analysis/simple.explanation.md` — a non-technical explanation of the ticket suitable for stakeholders.
5. Write `3.solution/a.assumptions/assumptions.md` with documented assumptions.
6. Write `3.solution/c.current.state/investigations.md` with initial current state notes.
7. Write `3.solution/d.decisions/decisions.md` with initial classification.
8. Write `3.solution/g.guidance/guidance.md` with initial guidance notes.
9. Write `3.solution/i.impacts/impacts.md` with initial impact assessment.
10. Write `3.solution/s.user.stories/user-stories.md` with user stories.
11. Write `NTK-10005-solution-design.md` as the main solution design document.
12. Classify whether this ticket is architecturally relevant or a code-level task. Provide reasoning grounded in the ticket description.

**Key files to check**: The ticket report should already exist at `1.requirements/NTK-10005.ticket.report.md`.

---

### SCENARIO 2: Solution Design (NTK-10002)

**Task**: Create a full solution design for the Adventure Category Classification ticket.

1. Read the existing ticket report at `work-items/tickets/_NTK-10002-adventure-category-classification/1.requirements/NTK-10002.ticket.report.md`.
2. Read the svc-check-in Swagger spec at `corporate-services/services/svc-check-in.yaml`.
3. Read the svc-trip-catalog Swagger spec at `corporate-services/services/svc-trip-catalog.yaml`.
4. Read the AdventureCategoryClassifier source code at `source-code/svc-check-in/src/main/java/com/novatrek/checkin/service/AdventureCategoryClassifier.java`.
5. Update or create the solution design at `NTK-10002-solution-design.md` with:
   - Problem statement derived from the ticket
   - Proposed solution with architectural approach
   - Service interaction changes
   - Data model modifications
6. Update `3.solution/d.decisions/decisions.md` with MADR-formatted architecture decisions:
   - Decision on classification approach (config-driven vs hardcoded)
   - Decision on API contract changes
7. Create impact assessments in `3.solution/i.impacts/`:
   - Impact on svc-check-in (API contract changes)
   - Impact on svc-trip-catalog (data model changes)
   - Use separate `impact.1/impact.1.md` and `impact.2/impact.2.md` subdirectories
8. Update `3.solution/a.assumptions/assumptions.md`.
9. Update `3.solution/s.user.stories/user-stories.md` — user stories must be free of technical implementation details.
10. Create `3.solution/g.guidance/guidance.md` with implementation guidance.
11. Create `3.solution/r.risks/risks.md` with risk assessment.

**Key insight to test**: The config-driven vs hardcoded classification approach should be identified as a key architectural decision.

---

### SCENARIO 3: Investigation and Root Cause Analysis (NTK-10004)

**Task**: Investigate a production bug using logs, source code, and MR history.

1. Read the existing ticket report at `work-items/tickets/_NTK-10004-guide-schedule-overwrite-bug/1.requirements/NTK-10004.ticket.report.md`.
2. Run `python3 scripts/mock-elastic-searcher.py --service svc-scheduling-orchestrator --level ERROR` to retrieve production error logs.
3. Read the SchedulingService source code at `source-code/svc-scheduling-orchestrator/src/main/java/com/novatrek/scheduling/service/SchedulingService.java`.
4. Run `python3 scripts/mock-gitlab-client.py --project svc-scheduling-orchestrator --mrs` to check merge request history.
5. Update `3.solution/c.current.state/investigations.md` with:
   - Timeline of errors from Elastic logs
   - Code analysis showing the PUT vs PATCH issue
   - MR history showing when the change was introduced
6. Document the root cause — this is NOT just a code bug, it is an **architectural boundary violation**: the scheduling service uses PUT semantics that overwrite fields owned by the guest-profiles service.
7. Write `3.solution/d.decisions/decisions.md` with MADR-formatted decision on the remediation approach (PATCH semantics + data ownership boundaries).
8. Write `3.solution/g.guidance/guidance.md` with implementation guidance.
9. Write `3.solution/i.impacts/impacts.md` with impact assessment.
10. Write `3.solution/r.risks/risks.md` with risk assessment.
11. Write `3.solution/s.user.stories/user-stories.md` with user stories.
12. Write `NTK-10004-solution-design.md` as the main solution design.

**Critical insight the AI must discover**: The root cause is a data ownership boundary violation — not just "use PATCH instead of PUT". The scheduling service overwrites guest-profile-owned enrichment data because it uses full-entity replacement.

---

### SCENARIO 4: Update Corporate Architecture Artifacts (NTK-10001)

**Task**: The solution design for NTK-10001 (Add Elevation Profile Data) is approved. Update corporate artifacts.

1. Read the approved solution design at `work-items/tickets/_NTK-10001-add-elevation-to-trail-response/NTK-10001-solution-design.md`.
2. Modify the svc-trail-management Swagger spec at `corporate-services/services/svc-trail-management.yaml`:
   - Add elevation fields to the TrailDetail schema:
     - `elevationProfile` (array of elevation data points)
     - `elevationGain` (number, total elevation gain in meters)
     - `elevationLoss` (number, total elevation loss in meters)
     - `maxElevation` (number, peak elevation in meters)
     - `minElevation` (number, minimum elevation in meters)
   - Add proper types, descriptions, and examples
   - Ensure fields appear in the GET trail detail response
3. Update the PlantUML component diagram at `corporate-services/diagrams/Components/novatrek-component-overview.puml` to show the new elevation data flow.
4. Write a commit message summarizing the changes at `work-items/tickets/_NTK-10001-add-elevation-to-trail-response/commit-message.md`.

**Key constraint**: Changes must be LIMITED to what the solution design specifies. No scope creep. The OpenAPI changes must be valid OpenAPI 3.0 syntax. The PlantUML must be valid, compilable syntax.

---

### SCENARIO 5: Complex Cross-Service Design (NTK-10003)

**Task**: Create a comprehensive solution design for the Unregistered Guest Self-Service Check-In feature — a complex cross-service feature.

1. Read the existing ticket report at `work-items/tickets/_NTK-10003-unregistered-guest-self-checkin/1.requirements/NTK-10003.ticket.report.md`.
2. Read ALL relevant Swagger specs:
   - `corporate-services/services/svc-check-in.yaml`
   - `corporate-services/services/svc-guest-profiles.yaml`
   - `corporate-services/services/svc-safety-compliance.yaml`
   - `corporate-services/services/svc-reservations.yaml`
3. Read relevant source code:
   - `source-code/svc-check-in/src/main/java/com/novatrek/checkin/controller/CheckInController.java`
   - `source-code/svc-guest-profiles/` (scan for relevant files)
4. Create or update `NTK-10003-solution-design.md` with:
   - Problem statement: unregistered guests cannot self-service check-in
   - Proposed new endpoint: POST /check-in/self-service/unregistered
   - Request schema (reservation lookup fields, identity verification)
   - Response schema (temporary guest profile, check-in confirmation)
   - Orchestration flow across 4 services
   - Error handling and edge cases
5. Create or update C4 component diagram as a PlantUML file (place in `corporate-services/diagrams/Components/`) showing:
   - New self-service check-in component
   - Interactions with guest-profiles, reservations, safety-compliance
   - Data flow direction and protocols
6. Create a PlantUML sequence diagram (place in either `corporate-services/diagrams/Sequence/` or alongside the solution design) showing:
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
8. Create impact assessments for EACH affected service in separate subdirectories under `3.solution/i.impacts/`:
   - `impact.1/impact.1.md` — svc-check-in: new endpoint, new controller logic
   - `impact.2/impact.2.md` — svc-guest-profiles: temporary profile creation API
   - `impact.3/impact.3.md` — svc-safety-compliance: unregistered guest compliance flow
   - `impact.4/impact.4.md` — svc-reservations: reservation lookup by confirmation code
9. Write `3.solution/r.risks/risks.md` covering:
   - Security risk: identity verification for unregistered guests
   - Data risk: temporary profiles and data retention
   - Operational risk: increased load on check-in flow
   - Compliance risk: safety requirements for unregistered guests
10. Write `3.solution/g.guidance/guidance.md` with implementation guidance.
11. Write `3.solution/s.user.stories/user-stories.md` covering guest, staff, and system perspectives.

**Key tests**: Does the AI identify ALL 4 affected services? Are PlantUML diagrams syntactically valid? Do ADR decisions have genuine options analysis? Are security considerations front and center?

---

After completing all 5 scenarios, provide a brief summary listing:
- Total files created or modified
- Total tool calls (mock scripts executed)
- Any scenarios where you encountered issues or had to retry
- Wall-clock time if you can estimate it

---

## Post-Execution Steps

After Roo Code completes, do the following:

1. **Record Kong AI token counts** from the gateway logs or Bedrock CloudWatch
2. **Commit the results**: `git add -A && git commit -m "feat: complete Phase 1 Roo Code + Kong AI execution - all 5 scenarios"`
3. **Score each scenario** using the rubrics in the playbook files:
   - [scenario-01-new-ticket-triage.md](workspace/playbooks/scenario-01-new-ticket-triage.md) (max 25)
   - [scenario-02-solution-design.md](workspace/playbooks/scenario-02-solution-design.md) (max 35)
   - [scenario-03-investigation-analysis.md](workspace/playbooks/scenario-03-investigation-analysis.md) (max 30)
   - [scenario-04-architecture-update.md](workspace/playbooks/scenario-04-architecture-update.md) (max 25)
   - [scenario-05-complex-cross-service.md](workspace/playbooks/scenario-05-complex-cross-service.md) (max 40)
4. **Record actual token costs** and create `phase-1-roo-code-results.md` using the same format as `phase-1-copilot-results.md`
5. **Run the data isolation audit**: `./scripts/audit-data-isolation.sh`

## Quality Scoring Reference (What Copilot Achieved)

For calibration — these are the scores and observable metrics from the Copilot execution:

| Scenario | Copilot Score | Max | Key Observations |
|----------|-------------|-----|-----------------|
| SC-01 | 23 | 25 | -2: flat folder structure in some areas |
| SC-02 | 33 | 35 | -2: no separate business rules doc |
| SC-03 | 30 | 30 | Perfect: identified data ownership boundary violation |
| SC-04 | 24 | 25 | -1: PlantUML used note annotation vs structural change |
| SC-05 | 39 | 40 | -1: created new C4 file vs updating existing |
| **Total** | **149** | **155** | **96.1%** |

| Observable Metric | Copilot Value |
|------------------|---------------|
| Total tool calls | ~85 |
| Files read | 40 |
| Files created | 16 |
| Files modified | 5 |
| Wall-clock time | ~100 minutes |
| Mock scripts executed | 5 (JIRA ×2, Elastic ×1, GitLab ×1, JIRA ×1) |
