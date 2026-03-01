# ADR-001: AI Toolchain Selection for Architecture Practice

| | |
|-----------|-------|
| **Status** | PROPOSED |
| **Date** | 2026-03-01 |
| **Decision Makers** | Christopher Blaisdell, UDX Architecture Practice |
| **Phase** | Phase 1 - AI Tool Cost Comparison |

## Context and Problem Statement

The UDX Architecture Practice needs AI-assisted tooling to accelerate solution architecture workflows — from ticket triage and investigation through solution design, review, and publishing. Two viable options exist. We need to select one as the standard toolchain for the practice, balancing cost, quality, standards compliance, and operational fit.

**Which AI toolchain should the UDX Architecture Practice adopt for AI-assisted solution architecture work?**

## Decision Drivers

- **Monthly cost per architect seat**: The practice has multiple architects; per-seat cost must be defensible to leadership
- **Architecture output quality**: AI-generated artifacts must meet arc42, C4, and MADR standards without excessive manual correction
- **Standards compliance**: The toolchain must be configurable to enforce organizational architecture standards automatically
- **Workflow integration**: The toolchain must integrate with the existing VS Code-based architecture workflow (UDX VSFlow, PlantUML, Markdown)
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

**Selected option:** TBD — pending Phase 1 execution results

This decision will be finalized after completing the Phase 1 cost comparison. The comparison data will populate the following table:

| | Roo Code + Kong AI | GitHub Copilot Business | GitHub Copilot Enterprise |
|---|---|---|---|
| Monthly input tokens per architect | TBD | (included in seat) | (included in seat) |
| Monthly output tokens per architect | TBD | (included in seat) | (included in seat) |
| Token/usage cost | TBD | $0 (flat rate) | $0 (flat rate) |
| Platform/gateway cost | TBD | $19/seat | $39/seat |
| Tool license cost | $0 (open source) | (included) | (included) |
| **Total monthly per seat** | **TBD** | **$19** | **$39** |
| Quality score (avg) | TBD | TBD | - |
| Standards compliance rate | TBD | TBD | - |
| Manual corrections (avg) | TBD | TBD | - |
| Workflow integration | TBD | TBD | - |

### Positive Consequences

_To be documented after decision is made._

### Negative Consequences

_To be documented after decision is made._

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
