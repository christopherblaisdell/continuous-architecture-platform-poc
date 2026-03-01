# Scenario 04: Update Corporate Architecture Artifacts

## Scenario Overview

| Property | Value |
|----------|-------|
| **Scenario ID** | SC-04 |
| **Task** | Update Corporate Architecture Artifacts After Approved Design |
| **Estimated Monthly Frequency** | 4 per month |
| **Complexity** | Medium |
| **Duration Target** | 30-60 minutes |
| **Skills Tested** | OpenAPI editing, PlantUML syntax, consistency validation, artifact management |

## Pre-conditions

- Solution design for NTK-10001 (Add Elevation Profile Data) is complete and approved
- Solution design located at `work-items/tickets/_NTK-10001-elevation-profile-data/NTK-10001-solution-design.md`
- Swagger spec for svc-trail-management exists at `services/svc-trail-management.yaml`
- PlantUML component diagram exists in `diagrams/`
- AI understands that corporate artifacts are the source of truth

## Exact Prompt to Use

> "The solution design for NTK-10001 (Add Elevation Profile Data) is approved. Update the corporate architecture artifacts: modify the svc-trail-management Swagger spec to add the elevation fields to the TrailDetail schema and trail response endpoint. Update the relevant PlantUML component diagram to show the new data flow. Create a commit message summarizing the changes."

## Expected AI Actions

1. **Read Solution Design**: Review NTK-10001 solution design to understand:
   - What elevation fields need to be added
   - Which schema (TrailDetail) is affected
   - Which endpoint returns trail data with elevation
   - Any new dependencies or data flows

2. **Modify Swagger Spec** (`svc-trail-management.yaml`):
   - Add elevation fields to the `TrailDetail` schema:
     - `elevationProfile` (array of elevation data points)
     - `elevationGain` (number, total elevation gain in meters)
     - `elevationLoss` (number, total elevation loss in meters)
     - `maxElevation` (number, peak elevation in meters)
     - `minElevation` (number, minimum elevation in meters)
   - Add proper types, descriptions, and examples
   - Ensure fields appear in the GET trail detail response

3. **Update PlantUML Diagram**:
   - Add elevation data flow to component diagram
   - Show data source for elevation data (if new integration)
   - Ensure diagram syntax is valid

4. **Verify Consistency**:
   - Swagger changes match what solution design specified
   - No orphaned references or broken schemas
   - PlantUML diagram reflects the Swagger changes

5. **Draft Commit Message**:
   - Clear summary referencing NTK-10001
   - List of changed files
   - Brief description of what was added

## What to Watch For

- Does the AI read the solution design FIRST before making changes?
- Are the OpenAPI spec changes valid (proper types, required fields, descriptions)?
- Does the PlantUML diagram use correct syntax (compilable)?
- Are the changes LIMITED to what the solution design specified (no scope creep)?
- Does the commit message follow conventional format?

## Quality Rubric

Score each criterion 1-5:

- [ ] **OpenAPI Validity**: Swagger spec changes are valid OpenAPI 3.0 syntax
- [ ] **Field Quality**: New fields have proper types, descriptions, and examples
- [ ] **PlantUML Syntax**: Diagram compiles with valid PlantUML syntax
- [ ] **Design Consistency**: Changes match exactly what solution design specified
- [ ] **Commit Message**: Commit message is clear, references ticket, and lists changes

**Maximum Score**: 25

## Token Cost Tracking

| Metric | Roo+Kong | Copilot |
|--------|----------|---------|
| Input tokens | | |
| Output tokens | | |
| Total tokens | | |
| Tool calls count | | |
| Files read | | |
| Files modified | | |
| Time to complete (min) | | |
| Quality score (/25) | | |
| Cost per run ($) | | |
| Estimated monthly cost ($) | | |

## Validation Steps (Manual)

After the AI completes the task, manually verify:

1. **Swagger Validation**: Run the spec through an OpenAPI validator
2. **PlantUML Compilation**: Render the diagram to confirm valid syntax
3. **Diff Review**: Check that only intended fields were added (no unrelated changes)
4. **Cross-reference**: Confirm all fields in solution design appear in the spec

## Notes

- This scenario tests precision and restraint -- the AI should change only what the design specifies
- Scope creep (adding fields not in the design) should reduce the quality score
- This is a common task that is tedious for humans but should be straightforward for AI
- The commit message quality reflects the AI's understanding of change management
