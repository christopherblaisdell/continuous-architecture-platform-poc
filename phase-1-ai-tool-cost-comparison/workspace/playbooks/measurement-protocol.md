# AI Tool Comparison Measurement Protocol

## Purpose

Standardized methodology for comparing **Roo Code + OpenRouter** vs **GitHub Copilot** for solution architecture tasks. This protocol ensures fair, repeatable measurements that produce actionable cost and quality comparisons.

## Test Environment Requirements

| Requirement | Details |
|-------------|---------|
| **Machine** | Same machine for both tools |
| **Workspace** | Same VS Code workspace with identical folder structure |
| **VS Code Version** | Same version for both test runs |
| **Network** | Same network conditions (wired preferred) |
| **Context State** | Clear AI context/history between runs |
| **Run Order** | Alternate which tool goes first across scenarios |

### Context Reset Procedure

Before each scenario run:
1. Close all editor tabs
2. Clear AI chat history (new conversation)
3. Restart VS Code if needed to ensure clean state
4. Delete any files created by the previous tool's run of the same scenario
5. Confirm mock scripts return consistent data

## Token Cost Collection

### OpenRouter (Roo Code)

OpenRouter provides exact per-request token counts and costs through multiple channels:

1. **API response `usage` object**: Each response includes `prompt_tokens`, `completion_tokens`, and `total_tokens`
2. **OpenRouter Activity page**: https://openrouter.ai/activity shows per-request cost breakdown, model used, and timestamps
3. **OpenRouter API**: `GET https://openrouter.ai/api/v1/auth/key` for credit balance

Collect for each scenario:
- `input_tokens` -- total input tokens across all requests (exact from Activity page)
- `output_tokens` -- total output tokens across all requests (exact from Activity page)
- `model_used` -- which model handled the request
- `total_cost` -- exact dollar amount from Activity page
- `request_count` -- number of API calls made

**NOTE**: OpenRouter provides exact costs. No estimation needed.

### GitHub Copilot

Copilot does not expose per-request token counts. Collection methods:

1. **Primary**: GitHub Copilot usage dashboard (if available at enterprise tier)
2. **Secondary**: Count observable interactions:
   - Number of chat turns (user messages sent)
   - Number of inline completions accepted
   - Number of tool calls executed (visible in chat)
   - Wall-clock time per scenario
3. **Estimate**: Use published model pricing and estimated context window usage

## Monthly Cost Calculation

### OpenRouter (Variable Cost Model)

OpenRouter provides exact per-request token counts and costs. Use the Activity page for actual costs.

```
OpenRouter Monthly Cost = SUM over all scenarios:
  (scenario_total_cost_from_activity_page)
  * scenario_monthly_frequency
```

For estimation before runs are complete, use the token-based formula:
```
Estimated Cost = (cumulative_input_tokens * input_price_per_token
                 + output_tokens * output_price_per_token)
```

Check https://openrouter.ai/models for current model pricing.

> **Agentic Re-transmission Tax**
>
> The formula above uses `cumulative_input_tokens`, not `single_pass_input_tokens`. This is critical for accurate cost modeling. Roo Code's client-side architecture re-transmits the **entire conversation history** at every turn of the agentic loop. For a scenario with `T` turns where context grows from `C_0` to `C_T` tokens:
>
> ```
> cumulative_input_tokens = SUM(t=1 to T) C_t   approximately  T * (C_0 + C_T) / 2
> ```
>
> For a 20-turn scenario starting at 10K and growing to 120K context, this yields ~1.3M cumulative input tokens -- not the 120K that a single-pass measurement would suggest. See [COST-MEASUREMENT-METHODOLOGY.md](../../COST-MEASUREMENT-METHODOLOGY.md) for the full analysis.

### GitHub Copilot Pro+ (Subscription + Overage Model)

```
Copilot Pro+ Base Cost = $39 / month
Included Premium Requests = 1500 / month
Overage Cost = $0.04 per premium request beyond 1500

Total Monthly Cost = $39 + max(0, premium_requests_used - 1500) * $0.04
```

Copilot Pro+ is NOT purely fixed-cost. When included premium requests (1500/month) are exhausted, each additional request using models like Claude Opus 4.6 costs $0.04. The user assumes all included requests are consumed and overage pricing applies.

## Quality Scoring

Each scenario has a quality rubric with specific criteria. Score each criterion 1-5:

| Score | Meaning | Description |
|-------|---------|-------------|
| 1 | Failed | Not attempted or completely wrong |
| 2 | Poor | Partially correct with significant issues |
| 3 | Acceptable | Functional with minor issues |
| 4 | Good | Solid result with minor improvements possible |
| 5 | Excellent | Production-ready output |

### Scoring Rules

- Score independently for each tool (do not compare during scoring)
- Score immediately after scenario completion (do not wait for all scenarios)
- Two evaluators score independently, then reconcile if scores differ by more than 1
- Document specific evidence for scores of 1-2 or 5 (outliers need justification)

## Scenario Summary

| ID | Scenario | Monthly Freq | Max Score | Weight |
|----|----------|-------------|-----------|--------|
| SC-01 | New Ticket Triage | 10 | 25 | High (volume) |
| SC-02 | Solution Design | 6 | 35 | High (value) |
| SC-03 | Investigation Analysis | 4 | 30 | Medium |
| SC-04 | Architecture Update | 4 | 25 | Medium |
| SC-05 | Complex Cross-Service | 2 | 40 | High (complexity) |

## Final Comparison Table

| Metric | Roo+OpenRouter | Copilot Pro+ |
|--------|----------|-------------------|
| Monthly cost per seat | *From OpenRouter Activity* | $39 base + $0.04/request overage |
| SC-01 quality (/25) | | |
| SC-02 quality (/35) | | |
| SC-03 quality (/30) | | |
| SC-04 quality (/25) | | |
| SC-05 quality (/40) | | |
| Average quality (normalized /5) | | |
| Cost per quality point | | |
| Scenarios with quality >= 80% | /5 | /5 |
| Total tool calls successful | | |
| Average time per scenario (min) | | |

## Weighted Monthly Cost-Quality Score

```
Weighted Score = SUM over scenarios:
  (quality_percentage * monthly_frequency) / total_monthly_runs

Cost Efficiency = Weighted Score / Monthly Cost
```

Higher cost efficiency = better value.

## Re-run Policy

- **Re-run trigger**: If quality score differs by >= 2 points on any single criterion between runs
- **Re-run limit**: Maximum 2 re-runs per scenario per tool
- **Discard rule**: If all 3 runs produce different results, use the median score
- **Documentation**: Note all re-runs and reasons in the final report

## Final Report Template

The final comparison report must include:

1. **Executive Summary**: One-page recommendation with confidence level
2. **Cost Comparison Table**: Monthly costs under different usage patterns
3. **Quality Comparison by Scenario**: Radar chart or bar chart by scenario
4. **Detailed Scenario Results**: Full rubric scores with evidence
5. **Token Usage Analysis**: Breakdown of where tokens are spent (reading vs writing)
6. **Scalability Projection**: Cost at 1x, 2x, 3x current workload
7. **Risk Factors**: What could change the recommendation (model pricing, feature additions)
8. **Recommendation**: Clear recommendation with confidence level (High/Medium/Low)
