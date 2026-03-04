# Cross-Platform Comparison: Copilot Run 002 vs Roo Code Run 001

## Execution Metrics

| Metric | Copilot (run 002) | Roo Code (run 001) |
|--------|-------------------|-------------------|
| Model | Claude Opus 4.6 fast (preview) | Claude Opus 4.6 |
| Model turns | 55 (estimated) | not reported |
| Files created | 37 | 37 |
| Mock script executions | 5 | 4 |
| Workspace file reads | 35 (approx) | 22 |
| Terminal commands | 8 | 5 |
| Scenarios completed | 5 of 5 | 5 of 5 |
| Issues or retries | 2 | 1 |
| Wall-clock time | pending human entry | pending |

## Cost Comparison

| Metric | Copilot | Roo Code |
|--------|---------|----------|
| Cost model | $0.04 per premium request (actual billing) | OpenRouter exact (per-token) |
| Day-total cost | $3.12 (78 requests, entire day, all projects) | pending (no run-metadata.md) |
| Session-isolated cost | Not available (no per-session breakdown) | pending |
| Overage charges | $0 (within 1,500 included Pro+ allowance) | N/A |

NOTE: GitHub Copilot does not provide per-session cost isolation. The $3.12 represents the full day of Copilot usage across multiple projects and VS Code instances. The execution prompt's x30 multiplier and $0.028 rate were incorrect — actual billing shows $0.04 per premium request and only 78 total requests for the day (inconsistent with a x30 multiplier on 55 model turns). Roo Code cost requires `run-metadata.md` which has not been created yet for run 001.

## Quality Comparison (if scores available)

| Scenario | Copilot Score | Roo Code Score | Max |
|----------|--------------|----------------|-----|
| SC-01 NTK-10005 | pending human scoring | pending | 25 |
| SC-02 NTK-10002 | pending human scoring | pending | 35 |
| SC-03 NTK-10004 | pending human scoring | pending | 30 |
| SC-04 NTK-10001 | pending human scoring | pending | 25 |
| SC-05 NTK-10003 | pending human scoring | pending | 40 |
| TOTAL | pending | pending | 155 |

## Cost Efficiency

| Metric | Copilot | Roo Code |
|--------|---------|----------|
| Cost per quality point | pending | pending |

## Observations

### File Output Parity

Both runs produced 37 files across 5 scenarios with identical scenario coverage. The file structures are closely aligned:

- SC-01 (NTK-10005): Both produced 8 files with matching structure
- SC-02 (NTK-10002): Both produced 8 files; Copilot used `u.user.stories/` folder, Roo Code also used `u.user.stories/`
- SC-03 (NTK-10004): Both produced 7 files
- SC-04 (NTK-10001): Both produced 3 files (YAML, PlantUML, commit message)
- SC-05 (NTK-10003): Both produced 11 files with matching impact subdirectory structure

### Approach Differences

1. **SC-04 Scope Discipline**: Copilot (run 002) limited elevation field changes to the 2 fields specified in the approved solution design (elevation_gain_meters, elevation_loss_meters), rejecting the 5 fields suggested in the execution prompt as scope creep. Roo Code (run 001) added 3 additional fields (max_elevation_m, min_elevation_m, elevation_profile array) — this difference may affect SC-04 scoring depending on whether the rubric rewards strict design adherence or comprehensive implementation.

2. **Mock Script Usage**: Copilot made 5 mock script invocations (including 1 failed GitLab call that was retried). Roo Code made 4 (including the same GitLab retry pattern). Both encountered the same `--mrs` flag issue.

3. **Solution Design Versioning**: Copilot advanced NTK-10002 to v1.8 and NTK-10003 to v1.9. Roo Code used v1.7 and v1.9 respectively.

4. **Source Code Gap Analysis**: Both runs identified the same 4 source code gaps in SC-05 (Map<String,String> stub, email dedup requirement, guest_id waiver lookup, missing confirmation_code). This suggests the findings are grounded in the workspace evidence and not model-dependent.

### Pending Human Actions

The following data is required from the human reviewer to complete this comparison:

- Copilot wall-clock time (start to completion)
- Roo Code `run-metadata.md` (OpenRouter cost, wall-clock time)
- Quality scores for both runs using scenario playbook rubrics
- Verified model turn count for Copilot (review chat interaction count)
- Confirmed model multiplier (x3 for Claude Opus 4.6 or x30 for fast preview — impacts cost significantly)
