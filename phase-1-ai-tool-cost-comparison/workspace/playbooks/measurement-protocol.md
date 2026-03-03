# AI Tool Comparison Measurement Protocol

## Purpose

Standardized methodology for comparing **Roo Code + Kong AI Gateway** vs **GitHub Copilot** for solution architecture tasks. This protocol ensures fair, repeatable measurements that produce actionable cost and quality comparisons.

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

### Kong AI Gateway (Roo Code)

Kong AI Gateway provides per-request token counts in response headers:

```
X-Kong-LLM-Input-Tokens: <count>
X-Kong-LLM-Output-Tokens: <count>
X-Kong-LLM-Model: <model_name>
```

Collect for each scenario:
- `input_tokens` -- total input tokens across all requests
- `output_tokens` -- total output tokens across all requests
- `model_used` -- which model handled the request
- `latency_ms` -- total latency across all requests
- `request_count` -- number of API calls made

**Backup**: AWS Bedrock CloudWatch metrics (per-invocation token counts)

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

### Kong AI (Variable Cost Model)

```
Kong AI Monthly Cost = SUM over all scenarios:
  (scenario_cumulative_input_tokens * input_price_per_token
   + scenario_output_tokens * output_price_per_token)
  * scenario_monthly_frequency
```

Current pricing reference (update with actual contracted rates):
- Claude Sonnet input: $3.00 / 1M tokens
- Claude Sonnet output: $15.00 / 1M tokens

Include Kong Gateway operational cost if applicable (infrastructure, licensing).

> **⚠️ Agentic Re-transmission Tax (Revision 2)**
>
> The formula above uses `cumulative_input_tokens`, not `single_pass_input_tokens`. This is critical for accurate cost modeling. Roo Code's client-side architecture re-transmits the **entire conversation history** at every turn of the agentic loop. For a scenario with `T` turns where context grows from `C₀` to `C_T` tokens:
>
> ```
> cumulative_input_tokens = Σ(t=1 to T) C_t   ≈  T × (C₀ + C_T) / 2
> ```
>
> For a 20-turn scenario starting at 10K and growing to 120K context, this yields ~1.3M cumulative input tokens — not the 120K that a single-pass measurement would suggest. This "agentic re-transmission tax" made the original cost estimate **14× too low**. See [COST-MEASUREMENT-METHODOLOGY.md](../../../phase-1-ai-tool-cost-comparison/COST-MEASUREMENT-METHODOLOGY.md) Revision 2 and [DEEP-RESEARCH-1.md](../../../../research/DEEP-RESEARCH-1.md) for the full analysis.
>
> Additionally, Roo Code + Kong AI has a documented failure mode where Kong Gateway obfuscates Anthropic's `context_length_exceeded` error, causing infinite retry loops with unbounded token consumption. See [DEEP-RESEARCH-2.md](../../../../research/DEEP-RESEARCH-2.md) for the root cause analysis.

### GitHub Copilot (Fixed Cost Model)

```
Copilot Business Monthly Cost  = $19 / seat / month
Copilot Enterprise Monthly Cost = $39 / seat / month
```

Fixed cost regardless of usage volume.

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

| Metric | Roo+Kong | Copilot Business | Copilot Enterprise |
|--------|----------|-------------------|---------------------|
| Monthly cost per seat | *Calculated* | $19 | $39 |
| SC-01 quality (/25) | | | |
| SC-02 quality (/35) | | | |
| SC-03 quality (/30) | | | |
| SC-04 quality (/25) | | | |
| SC-05 quality (/40) | | | |
| Average quality (normalized /5) | | | |
| Cost per quality point | | | |
| Scenarios with quality >= 80% | /5 | /5 | /5 |
| Total tool calls successful | | | |
| Average time per scenario (min) | | | |

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
