# ADR-001: AI Toolchain Selection for Architecture Practice

| | |
|-----------|-------|
| **Status** | PROPOSED |
| **Date** | 2026-03-01 |
| **Decision Makers** | Christopher Blaisdell, Architecture Practice |
| **Phase** | Phase 1 - AI Tool Cost Comparison |

## Context and Problem Statement

The Architecture Practice needs AI-assisted tooling to accelerate solution architecture workflows — from ticket triage and investigation through solution design, review, and publishing. Two viable options exist. We need to select one as the standard toolchain for the practice, balancing cost, quality, standards compliance, and operational fit.

**Which AI toolchain should the Architecture Practice adopt for AI-assisted solution architecture work?**

## Decision Drivers

- **Monthly cost per architect seat**: The practice has multiple architects; per-seat cost must be defensible to leadership
- **Architecture output quality**: AI-generated artifacts must meet arc42, C4, and MADR standards without excessive manual correction
- **Standards compliance**: The toolchain must be configurable to enforce organizational architecture standards automatically
- **Workflow integration**: The toolchain must integrate with the existing VS Code-based architecture workflow (DocFlow, PlantUML, Markdown)
- **Extensibility**: The toolchain must support future pipeline integration (Phase 3) and custom tooling
- **Model flexibility**: The ability to select and switch between LLM models as pricing and capabilities evolve
- **Corporate governance**: The toolchain must operate within corporate security, procurement, and data handling policies

## Considered Options

### Option A: Roo Code + Kong AI Gateway

**Description:** Roo Code is a free, open-source VS Code extension that provides AI-assisted coding and architecture support through configurable modes and custom instructions. Kong AI Gateway routes LLM API requests through an enterprise API gateway to backend model providers (AWS Bedrock with Claude models).

**Pricing model:** Usage-based. Cost is determined by actual token consumption routed through Kong AI to AWS Bedrock. No per-seat software license fee.

**Cost formula:**
```
Monthly Cost Per Seat =
  (Monthly Input Tokens x Bedrock Input Token Price)
  + (Monthly Output Tokens x Bedrock Output Token Price)
  + Kong AI Gateway operational cost allocation (if any)
```

**Strengths:**
- Cost scales with actual usage — light months cost less
- Full model flexibility — can switch between Claude Sonnet, Haiku, Opus, or other providers
- Custom instruction system (`.roo/rules/`) enables fine-grained standards enforcement per mode
- Open source — no vendor lock-in on the extension
- Kong AI Gateway already exists in the corporate infrastructure
- Supports MCP (Model Context Protocol) for custom tool integration

**Weaknesses:**
- Cost is unpredictable — heavy months could exceed flat-rate alternatives
- Requires internal Kong AI team to maintain the gateway
- No built-in ecosystem (no GitHub integration, no PR review, no code suggestions outside of chat)
- Configuration complexity — custom instructions require ongoing maintenance

### Option B: GitHub Copilot (Business or Enterprise)

**Description:** GitHub Copilot is a commercial AI assistant integrated into VS Code with chat, inline suggestions, agent mode, and extensions. Available at two tiers: Business ($19/seat/month) and Enterprise ($39/seat/month).

**Pricing model:** Flat per-seat monthly subscription. Includes a base allocation of premium model requests (Claude Sonnet, GPT-4o) with potential overage charges.

**Cost formula:**
```
Monthly Cost Per Seat =
  Subscription fee ($19 or $39 per seat)
  + Premium model request overage (if applicable)
```

**Strengths:**
- Predictable monthly cost — easy to budget
- Deep GitHub integration (PR reviews, code suggestions, repository context)
- Large ecosystem (extensions, agent mode, workspace instructions via `.github/copilot-instructions.md`)
- Minimal setup — works out of the box with VS Code
- Enterprise tier includes organization-wide policy controls
- Backed by Microsoft/GitHub — enterprise support and compliance

**Weaknesses:**
- Per-seat cost applies regardless of usage volume — light users pay the same as heavy users
- Model selection limited to what GitHub offers (currently Claude Sonnet, GPT-4o, and Copilot's own models)
- Customization limited to workspace instructions and prompt engineering — no mode-based instruction system
- Premium model request limits may require overage tracking
- Vendor lock-in to the GitHub ecosystem

## Evaluation Criteria

Phase 1 will evaluate both options across 5 representative architecture scenarios using the synthetic NovaTrek Adventures workspace. Each scenario will be scored on the following criteria:

| Criterion | Weight | Measurement Method |
|-----------|--------|--------------------|
| Monthly cost per seat | 30% | Token usage extrapolated to monthly volume at current pricing |
| Architecture output quality | 25% | Architect-scored rubric (1-5) per scenario |
| Standards compliance rate | 20% | Pass/fail checklist against arc42, C4, MADR rules |
| Manual corrections required | 15% | Count of edits needed after AI generation |
| Workflow integration friction | 10% | Qualitative assessment of setup, configuration, and daily use |

### Evaluation Scenarios

| Scenario | What It Tests |
|----------|---------------|
| Ticket intake and classification | AI's ability to parse a ticket, classify architectural relevance, scaffold workspace |
| Current state investigation | AI's ability to analyze Swagger specs, source code, and logs to produce investigation docs |
| Solution design creation | AI's ability to produce arc42-compliant designs with impacts, decisions, and diagrams |
| Merge request review | AI's ability to validate spec/diagram changes against a solution design |
| Publishing preparation | AI's ability to validate cross-references, formatting, and standards compliance |

See [phase-1-ai-tool-cost-comparison/AI-TOOL-COST-COMPARISON-PLAN.md](../phase-1-ai-tool-cost-comparison/AI-TOOL-COST-COMPARISON-PLAN.md) for full scenario playbook details.

## Decision Outcome

**Selected option:** TBD — pending Roo Code + Kong AI execution for comparison

GitHub Copilot (Claude Opus 4.6, Agent Mode) Phase 1 execution is complete. Roo Code + Kong AI execution is pending. The Copilot column is populated below based on Phase 1 results.

| | Roo Code + Kong AI | GitHub Copilot Business | GitHub Copilot Enterprise |
|---|---|---|---|
| Monthly input tokens per architect | TBD | ~350,000 (est.) | ~350,000 (est.) |
| Monthly output tokens per architect | TBD | ~100,000 (est.) | ~100,000 (est.) |
| Token/usage cost | TBD | $0 (flat rate) | $0 (flat rate) |
| Platform/gateway cost | TBD | $19/seat | $39/seat |
| Tool license cost | $0 (open source) | (included) | (included) |
| **Total monthly per seat** | **TBD** | **$19** | **$39** |
| SC-01 quality (/25) | TBD | 23 (92%) | — |
| SC-02 quality (/35) | TBD | 33 (94%) | — |
| SC-03 quality (/30) | TBD | 30 (100%) | — |
| SC-04 quality (/25) | TBD | 24 (96%) | — |
| SC-05 quality (/40) | TBD | 39 (98%) | — |
| **Total quality (/155)** | **TBD** | **149 (96.1%)** | **—** |
| **Avg quality (normalized /5)** | **TBD** | **4.81** | **—** |
| Cost per quality point | TBD | $3.95 | $8.11 |
| Scenarios with quality >= 80% | TBD | 5/5 | — |
| Total tool calls (est.) | TBD | 85 | — |
| Average time per scenario (min) | TBD | 20 | — |
| Breakeven runs vs. Kong AI | — | ~37/month | ~76/month |

### Revised Cost at Realistic Workload (Including PROMOTE Step)

| Metric | Roo Code + Kong AI | Copilot Business | Copilot Enterprise |
|--------|-------------------|-----------------|-------------------|
| Monthly runs (with PROMOTE) | ~38 | ~38 | ~38 |
| Monthly cost | ~$19.40 | $19.00 | $39.00 |
| Cost per run | ~$0.51 | ~$0.50 | ~$1.03 |
| Cost trend as volume grows | 📈 Increases linearly | 📊 Flat | 📊 Flat |

The PROMOTE step (updating corporate baselines after deployment) adds ~12 runs/month to the workload. At this revised volume, Copilot Business and Kong AI are cost-equivalent, but Copilot offers budget predictability. See [CLOSING-THE-LOOP.md](../CLOSING-THE-LOOP.md) for the full analysis of why the PROMOTE step is essential.

### Preliminary Observations (Copilot Completed, Kong AI Pending)

**GitHub Copilot demonstrated:**
- 96.1% quality score across all 5 scenarios (149/155)
- Autonomous multi-step execution — all scenarios completed in a single session
- Correct architectural reasoning (data ownership violation identification in SC-03)
- MADR-compliant ADR generation (9 ADRs created/formatted)
- Valid PlantUML diagram generation (2 diagrams created/modified)
- All 3 mock tools used appropriately across scenarios

**Limitations:**
- No per-request token visibility — cost estimates are approximations
- Context window management summarized early context during long session
- Fixed cost model is cost-effective at current usage (~26 runs/month) but becomes relatively less attractive if Kong AI achieves comparable quality at estimated ~$13/month

**Revised Workload Analysis (PROMOTE Step):**

The original 26 runs/month workload calculation only covered ticket intake through solution design. A critical gap analysis (see [CLOSING-THE-LOOP.md](../CLOSING-THE-LOOP.md)) identified that the architecture practice never "closes the loop" — target states documented in solution designs are never promoted back to the corporate architecture baseline. Adding the PROMOTE step (updating corporate artifacts, promoting ADRs to the global log, refreshing service architecture pages) adds ~12 additional AI-assisted runs/month, bringing the realistic workload to **~38 runs/month**.

At 38 runs/month:
- Kong AI estimated cost: ~$19.40/month (exceeds Copilot Business)
- Copilot Business: $19.00/month (fixed, unaffected)
- **The PROMOTE step neutralizes Kong AI's cost advantage and favors flat-rate pricing**

This revised workload must be used when making the final tool selection. The original 26 runs/month understates real-world usage by omitting the essential baseline-update workflow.

### Positive Consequences

- Copilot demonstrated production-ready architecture artifact generation (96.1% quality)
- 9 MADR-formatted ADRs created across 5 scenarios — minimal manual correction expected
- Autonomous multi-step execution reduces architect time investment per scenario
- Flat-rate pricing provides budget predictability for practice leadership

### Negative Consequences

- No per-request token visibility limits cost optimization opportunities
- Fixed cost regardless of usage — light months still cost $19-$39/seat
- Model selection limited to what GitHub Copilot offers (currently Claude Opus 4.6 for agent mode)
- Single-session context window management may degrade quality across very long sessions

## Additional Considerations

### Future Phase Impact

The selected toolchain will be used throughout all subsequent phases:
- **Phase 2**: AI instructions and workflow design will be built for the selected tool
- **Phase 3**: Pipeline integration may leverage tool-specific APIs (e.g., Roo Code MCP servers, Copilot extensions)
- **Phase 4**: Artifact graph generation may use AI for relationship discovery
- **Phase 5**: Continuous improvement metrics will be tool-specific

A toolchain switch after Phase 2 would require significant rework. This makes Phase 1's evaluation critical.

### Hybrid Approach

It is possible that the evaluation reveals complementary strengths (e.g., Copilot for code-level suggestions, Roo Code + Kong AI for architecture-level generation). If the data supports it, a hybrid recommendation may be appropriate, though this increases operational complexity.

## Links

- [Project Vision](../README.md)
- [Roadmap](../roadmap/ROADMAP.md)
- [Phase 1 Plan](../phase-1-ai-tool-cost-comparison/AI-TOOL-COST-COMPARISON-PLAN.md)
