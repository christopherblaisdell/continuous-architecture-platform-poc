# The Ask

## One Test Seat to Validate the Shared Solution

This POC was conducted on a synthetic workspace. The next step is validating the shared workspace approach against **real architecture artifacts** to produce a go/no-go recommendation for the practice.

---

## What We Need

**One Copilot Pro+ subscription ($39/month)** to assemble a shared workspace from actual corporate artifacts and validate the approach:

- Corporate OpenAPI specs, ADRs, and architecture metadata in a shared Git repo
- Real architecture scenarios against actual service codebases
- Copilot indexes the workspace automatically — no MCP servers, no custom integrations

No custom infrastructure. No engineering effort from other teams. Cancel anytime.

---

## What We Will Produce

A validation report within 2 weeks, containing:

1. **Quality assessment** — Does the AI produce standards-compliant designs with real corporate context?
2. **Accuracy check** — Does it cite real API fields correctly, or fabricate?
3. **Shared workspace viability** — Can the practice operate from a single shared Git repo?
4. **Go/no-go recommendation** — With corporate data, not synthetic data

---

## Why Not Build Our Own Instead?

This POC evaluated that option. Short answer: no. Copilot already indexes the entire workspace into a vector database automatically — no MCP servers, no custom RAG pipelines, no engineering project.

| | Shared Solution ($39/seat/mo) | Build Custom (Foundry) |
|-|:-:|:-:|
| Year 1 cost | $468 | $113,450 |
| Time to first output | Immediate | 10-14 weeks |
| Engineering headcount | 0 | 2-3 engineers ongoing |
| Reads full workspace context | Yes | No (chunked RAG) |
| Risk of project failure | None (already proven) | High (RAG quality, 5-call limit) |

See [Microsoft Foundry Analysis](foundry-analysis.md) for the full build-vs-buy breakdown.

---

## Summary of POC Evidence

| Claim | Evidence |
|-------|---------|
| Works for architecture, not just code | 39 architecture files across 5 scenarios |
| Standards compliant | MADR, arc42, C4 notation throughout |
| Zero fabrication | Head-to-head comparison: 0 vs 4 fabricated fields |
| Enables automated publishing | 301 portal artifacts, live at [architecture.novatrek.cc](https://architecture.novatrek.cc) |
| No MCP servers or custom infrastructure | Copilot indexes the workspace automatically |
| 13x cheaper than assembling alternatives | $39/mo vs $507/mo (actual billing data) |
| 243x cheaper than building custom | $39/mo vs $9,454/mo (Foundry TCO analysis) |

<div class="key-insight" markdown>
**The ask is one $39/month test seat.** The risk is near zero. The validation takes 2 weeks. Cancel if it doesn't work. The evidence so far says it will.
</div>

<div class="cta-box" markdown>

### Want the full evidence?

[Cost Analysis](cost-evidence.md) | [Output Quality](quality-evidence.md) | [Foundry Analysis](foundry-analysis.md) | [Roadmap](roadmap.md)

</div>
