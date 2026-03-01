# Scenario 02: Create Solution Design for Medium Ticket

## Scenario Overview

| Property | Value |
|----------|-------|
| **Scenario ID** | SC-02 |
| **Task** | Create Solution Design for Medium Complexity Ticket |
| **Estimated Monthly Frequency** | 6 tickets/month |
| **Complexity** | Medium |
| **Duration Target** | 45-90 minutes |
| **Skills Tested** | Multi-source analysis, template adherence, MADR format, impact assessment |

## Pre-conditions

- NTK-10002 ticket folder exists at `work-items/tickets/_NTK-10002-adventure-category-classification/`
- Ticket report already created in `1.requirements/NTK-10002.ticket.report.md`
- Swagger specs available for svc-check-in and svc-trip-catalog in `source-code/` or `services/`
- AdventureCategoryClassifier.java source code available
- Solution design template available in workspace AI instructions

## Exact Prompt to Use

> "Work on ticket NTK-10002 (Adventure Category Classification). I need a full solution design. Review the existing ticket report, analyze the svc-check-in and svc-trip-catalog Swagger specs, review the AdventureCategoryClassifier source code, and create a complete solution design following our template. Include architecture decisions using MADR format, impact assessments for affected services, assumptions, and user stories."

## Expected AI Actions

1. Read `1.requirements/NTK-10002.ticket.report.md` for ticket context
2. Read svc-check-in Swagger spec (identify relevant endpoints and schemas)
3. Read svc-trip-catalog Swagger spec (identify category-related models)
4. Read `AdventureCategoryClassifier.java` source code (understand current logic)
5. Create `NTK-10002-solution-design.md` following template with:
   - Problem statement derived from ticket
   - Proposed solution with architectural approach
   - Service interaction changes
   - Data model modifications
6. Create architecture decision records in `3.solution/d.decisions/` using MADR format:
   - Decision on classification approach (config-driven vs hardcoded)
   - Decision on API contract changes
7. Create impact assessments in `3.solution/i.impacts/`:
   - Impact on svc-check-in (API contract changes)
   - Impact on svc-trip-catalog (data model changes)
8. Create `3.solution/a.assumptions/assumptions.md` with documented assumptions
9. Create `3.solution/s.user.stories/user-stories.md` with properly scoped stories

## What to Watch For

- Does the AI read ALL relevant sources before designing, or start writing prematurely?
- Are MADR decisions structured with Context, Decision, Options, Consequences?
- Do impact docs focus on WHAT changes (not HOW to implement)?
- Are user stories free of technical implementation details?
- Is the classification approach (config-driven vs hardcoded) identified as a key decision?
- Does the solution design cross-reference the Swagger specs?

## Quality Rubric

Score each criterion 1-5:

- [ ] **Spec Coverage**: Referenced all relevant Swagger specs accurately
- [ ] **Service Identification**: Identified correct services impacted
- [ ] **MADR Quality**: Architecture decisions are well-reasoned with proper options analysis
- [ ] **Impact Accuracy**: Impact docs cover API contract changes specifically
- [ ] **Template Adherence**: Solution design follows template structure
- [ ] **User Story Scope**: User stories are properly scoped (no tech details leaked)
- [ ] **Cross-cutting Concerns**: Identified config-driven vs hardcoded as key concern

**Maximum Score**: 35

## Token Cost Tracking

| Metric | Roo+Kong | Copilot |
|--------|----------|---------|
| Input tokens | | |
| Output tokens | | |
| Total tokens | | |
| Tool calls count | | |
| Files read | | |
| Files created | | |
| Time to complete (min) | | |
| Quality score (/35) | | |
| Cost per run ($) | | |
| Estimated monthly cost ($) | | |

## Complexity Factors

This scenario tests the AI's ability to:
- Synthesize information from multiple sources (ticket, specs, source code)
- Apply a specific document template correctly
- Use MADR format without being given the template inline
- Separate impact (WHAT) from guidance (HOW)
- Keep user stories non-technical

## Notes

- This scenario represents the most common high-value task for Solution Architecture
- Quality of MADR decisions is a strong differentiator between tools
- Watch for hallucinated API endpoints that do not exist in the Swagger specs
