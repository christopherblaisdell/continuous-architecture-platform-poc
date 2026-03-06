# Cross-Platform Comparison: Copilot Run 002 vs Roo Code Run 001

## Execution Metrics

| Metric | Copilot (run 002) | Roo Code (run 001) |
|--------|-------------------|-------------------|
| Model | Claude Opus 4.6 (standard, 3x multiplier) | Claude Opus 4.6 |
| User prompts | 4 | not reported |
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
| Cost model | Per user prompt x model multiplier x $0.04 | OpenRouter per-token (auto-top-up) |
| Day-total cost (Mar 4) | $4.80 (120 requests, entire day, all projects) | $100+ (4 x $25 auto-top-ups in 26 min) |
| Session cost | **$0.48** (4 prompts x 3x x $0.04 = 12 premium requests) | ~$75-$100 (bulk of Mar 4 top-ups) |
| Actual overage charged | $0 (within 1,500 included Pro+ allowance) | $100 (pay-per-token, no allowance) |
| Cost ratio | 1x (baseline) | ~156x-208x more expensive |

### OpenRouter Transaction Evidence (Roo Code)

OpenRouter auto-top-up charges on March 4, 2026:

| Time | Amount |
|------|--------|
| 10:11 AM | $25 |
| 10:27 AM | $25 |
| 10:32 AM | $25 |
| 10:37 AM | $25 |
| **Total** | **$100** |

These 4 charges occurred within a 26-minute window starting 5 minutes after the Copilot run 002 first file was created (10:06 AM). The Roo Code run 002 was executing concurrently. Each $25 top-up triggers when the OpenRouter balance drops below a threshold, meaning credits were being consumed continuously at a high rate.

Additional OpenRouter charges on March 3 ($75 across 3 top-ups) likely correspond to Roo Code run 001 and related work.

### Copilot Billing Details (Corrected via Deep Research)

GitHub Copilot Pro+ billing for March 4, 2026:
- 120 premium requests at $0.04 each = $4.80 notional (entire day, all projects)
- $0 overage (within 1,500/month included allowance)
- **Run 002 session: 4 user prompts x 3x multiplier = 12 premium requests = $0.48**
- Autonomous tool calls (file reads, terminal commands, sub-agents) are free -- only user prompts consume premium requests
- The remaining 108 requests ($4.32) came from other Copilot usage throughout the day

See [DEEP-RESEARCH-RESULTS-COPILOT-BILLING.md](../../../../research/DEEP-RESEARCH-RESULTS-COPILOT-BILLING.md) for the full billing model analysis with 39 cited sources.

### Key Cost Finding

For equivalent architecture work (5 identical scenarios, both producing 37 files), Roo Code via OpenRouter cost approximately **$75-$100** in direct API charges, while GitHub Copilot consumed **$0.48 notional** ($0 actual overage). Even at overage rates, Copilot is **156x-208x cheaper** per run.

Copilot has a $39/month fixed subscription cost. At $0.48 notional per run, the subscription covers approximately **125 equivalent runs per month** (1,500 included requests / 12 requests per run) at no additional cost. Beyond that, overage at $0.04/request remains dramatically cheaper than OpenRouter.

NOTE: OpenRouter exact per-generation costs should be retrieved using `python3 scripts/openrouter-cost.py` for precise figures. The $100 figure is based on auto-top-up charges and represents an upper bound for March 4 usage.

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
| Cost per quality point | pending (need scores) | pending (need scores) |
| Cost per file created | ~$0.013 ($0.48 / 37) | ~$2.70 ($100 / 37) |
| Cost per scenario | ~$0.10 ($0.48 / 5) | ~$20.00 ($100 / 5) |

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
- Roo Code wall-clock time (from Roo Code terminal history or run-metadata.md)
- Quality scores for both runs using scenario playbook rubrics
- Verified model turn count for Copilot (review chat interaction count)
- Exact OpenRouter per-generation costs via `python3 scripts/openrouter-cost.py`

### Methodology Implications (Resolved via Deep Research)

The original cost comparison methodology contained fundamental errors that have been corrected:

1. **Copilot formula corrected**: The original formula `model_turns x $0.028 x multiplier` was wrong on every parameter. Correct formula: `User Prompts x Model Multiplier x $0.04`. The $0.028 rate was a DeepSeek/Azure cached-token API rate -- never applicable to Copilot. The billing unit is user prompts, not model turns. This reduced the session cost from the original $46.20 estimate to $0.48 -- a 96x correction.
2. **OpenRouter is transparent but expensive**: Per-token billing provides exact costs but Claude Opus 4.6 via OpenRouter costs **156x-208x** more than the same model via Copilot for equivalent agent work.
3. **Per-session isolation**: OpenRouter provides exact per-request costs via generation IDs. Copilot provides only daily aggregate premium request counts with no session-level breakdown. However, user prompt counting provides a reliable session cost calculation.
4. **Fixed vs variable**: Copilot's $39/month subscription absorbs approximately 125 equivalent architecture runs per month (1,500 / 12 requests per run). OpenRouter is purely pay-per-token with no discount floor.
