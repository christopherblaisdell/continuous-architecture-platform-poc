# Scenario 03: Investigate Production Bug from Elastic Logs

## Scenario Overview

| Property | Value |
|----------|-------|
| **Scenario ID** | SC-03 |
| **Task** | Investigate Production Bug Using Logs and Source Code |
| **Estimated Monthly Frequency** | 4 per month |
| **Complexity** | High |
| **Duration Target** | 60-120 minutes |
| **Skills Tested** | Log analysis, root cause identification, multi-tool orchestration, diagnostic reasoning |

## Pre-conditions

- NTK-10004 ticket folder exists at `work-items/tickets/_NTK-10004-guide-schedule-overwrite-bug/`
- Ticket report already created in `1.requirements/NTK-10004.ticket.report.md`
- Source code for svc-scheduling-orchestrator available (including SchedulingService.java)
- Mock Elastic Search script available at `scripts/mock-elastic-searcher.py`
- Mock GitLab client available at `scripts/mock-gitlab-client.py`

## Exact Prompt to Use

> "Investigate ticket NTK-10004 (Guide Schedule Overwrite Bug). Query production logs for errors from svc-scheduling-orchestrator in the last 48 hours. Review the source code of the SchedulingService.java to find the root cause. Check the GitLab MR history. Document your findings with root cause analysis, current state investigation, and recommendations."

## Expected AI Actions

1. Run `python scripts/mock-elastic-searcher.py --service svc-scheduling-orchestrator --level ERROR`
   - Retrieve error logs showing schedule overwrite patterns
2. Read `SchedulingService.java` source code
   - Identify the PUT endpoint that replaces entire schedule entity
   - Find that guide enrichment data is lost on full replacement
3. Run `python scripts/mock-gitlab-client.py --project svc-scheduling-orchestrator --mrs`
   - Check recent merge requests for related changes
   - Identify when the bug was introduced
4. Update `3.solution/c.current.state/investigations.md` with:
   - Timeline of errors from Elastic logs
   - Code analysis showing the PUT vs PATCH issue
   - MR history showing when the change was introduced
5. Document root cause:
   - Full entity replacement (PUT) overwrites guide-specific enrichments
   - Data ownership boundary violation: scheduling service overwrites guest-profile-owned data
6. Propose remediation:
   - Switch to PATCH semantics for partial updates
   - Establish clear data ownership boundaries between services
   - Add validation to prevent overwrite of enrichment fields

## What to Watch For

- Does the AI use all three mock tools (JIRA, Elastic, GitLab) or skip some?
- Does it correctly identify PUT vs PATCH as the root cause from the source code?
- Does it connect the Elastic log evidence to the code-level issue?
- Does it identify the data ownership boundary problem (architectural concern)?
- Are recommendations actionable and specific?
- Does it distinguish between the immediate fix and the architectural improvement?

## Quality Rubric

Score each criterion 1-5:

- [ ] **Tool Usage**: Used all three mock tools (JIRA, Elastic, GitLab) appropriately
- [ ] **Root Cause**: Correctly identified PUT vs PATCH as root cause
- [ ] **Data Ownership**: Identified data ownership boundary issue (architectural concern)
- [ ] **Remediation**: Proposed actionable and specific remediation steps
- [ ] **Document Structure**: Investigation document follows proper structure
- [ ] **Evidence-Based**: Diagnosis is supported by evidence from logs and code

**Maximum Score**: 30

## Token Cost Tracking

| Metric | Roo+Kong | Copilot |
|--------|----------|---------|
| Input tokens | | |
| Output tokens | | |
| Total tokens | | |
| Tool calls count | | |
| Scripts executed | | |
| Files read | | |
| Files created/updated | | |
| Time to complete (min) | | |
| Quality score (/30) | | |
| Cost per run ($) | | |
| Estimated monthly cost ($) | | |

## Complexity Factors

This scenario is rated High because it requires:
- Orchestrating multiple external tools in sequence
- Correlating data across sources (logs + code + MR history)
- Distinguishing symptoms (errors) from root cause (PUT semantics)
- Elevating from code-level bug to architectural concern (data ownership)
- Providing both tactical fix and strategic recommendation

## Key Insight the AI Must Discover

The critical insight is that this is NOT just a code bug -- it is an **architectural boundary violation**. The scheduling service is using PUT semantics that overwrite fields owned by the guest-profiles service. The fix is not just changing PUT to PATCH, but establishing proper data ownership contracts between services.

An AI that only identifies "use PATCH instead of PUT" scores lower than one that identifies the data ownership boundary issue.

## Notes

- This scenario tests the AI's ability to reason about distributed system concerns
- The mock Elastic data is designed to provide enough evidence to trace the issue
- Watch for whether the AI asks clarifying questions vs investigates autonomously
