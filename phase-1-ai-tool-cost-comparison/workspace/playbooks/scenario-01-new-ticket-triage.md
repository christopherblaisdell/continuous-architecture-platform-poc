# Scenario 01: New Ticket Triage and Classification

## Scenario Overview

| Property | Value |
|----------|-------|
| **Scenario ID** | SC-01 |
| **Task** | New Ticket Triage and Classification |
| **Estimated Monthly Frequency** | 10 tickets/month |
| **Complexity** | Low |
| **Duration Target** | 15-30 minutes |
| **Skills Tested** | Tool usage, folder creation, data extraction, classification |

## Pre-conditions

- Workspace open with all folders visible
- No existing work-item folder for NTK-10005
- Mock JIRA client script available at `scripts/mock-jira-client.py`
- Virtual environment activated

## Exact Prompt to Use

> "I need to work on a new ticket. Query our JIRA board for new tickets, find NTK-10005 (Wristband RFID Field), and create the initial workspace with ticket report and simple explanation. Classify whether this is architecturally relevant or a code-level task."

## Expected AI Actions

1. Run `python scripts/mock-jira-client.py --list --status "New"` to list available tickets
2. Run `python scripts/mock-jira-client.py --ticket NTK-10005` to extract full ticket details
3. Create folder structure:
   ```
   work-items/tickets/_NTK-10005-wristband-rfid-field/
   ├── NTK-10005-solution-design.md
   ├── 1.requirements/
   │   └── NTK-10005.ticket.report.md
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
4. Generate ticket report from JIRA mock data (not fabricated)
5. Write simple explanation suitable for non-technical stakeholders
6. Classify the ticket as architecturally relevant or code-level task with reasoning

## What to Watch For

- Does the AI run the mock scripts or fabricate data?
- Does the folder name start with underscore and use kebab-case?
- Does the ticket report faithfully reflect mock data?
- Is classification reasoning grounded in the ticket description?
- Does the simple explanation avoid technical jargon?

## Quality Rubric

Score each criterion 1-5:

- [ ] **Tool Usage**: Correctly used mock tool scripts (not guessed data)
- [ ] **Folder Structure**: Created proper folder structure (underscore prefix, kebab-case)
- [ ] **Data Accuracy**: Ticket report matches mock data accurately
- [ ] **Classification**: Classification reasoning is sound and justified
- [ ] **Clarity**: Simple explanation is clear and non-technical friendly

**Maximum Score**: 25

## Token Cost Tracking

| Metric | Roo+Kong | Copilot |
|--------|----------|---------|
| Input tokens | | |
| Output tokens | | |
| Total tokens | | |
| Tool calls count | | |
| Time to complete (min) | | |
| Quality score (/25) | | |
| Cost per run ($) | | |
| Estimated monthly cost ($) | | |

## Notes

- This is the simplest scenario and serves as a baseline
- If an AI tool cannot handle this scenario well, more complex scenarios are unlikely to succeed
- Pay attention to whether the AI follows the naming conventions without being reminded
