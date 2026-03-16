# The Ask

## One Test License. $39/month.

This POC was conducted on a synthetic workspace. The next step is validating against **real architecture artifacts** to produce a go/no-go recommendation.

---

## What We Need

**One test license ($39/month)** to run architecture scenarios against actual corporate artifacts:

- Corporate OpenAPI specs, ADRs, and architecture metadata
- Real JIRA tickets and service codebases
- Production Elasticsearch logs and GitLab merge requests

No custom infrastructure. No engineering effort from other teams. Cancel anytime.

---

## What We Will Produce

A validation report within 2 weeks, containing:

1. **Quality assessment** — Does the AI produce standards-compliant designs with real corporate context?
2. **Accuracy check** — Does it cite real API fields correctly, or fabricate?
3. **Workflow fit** — Does it integrate with existing architect workflows?
4. **Go/no-go recommendation** — With corporate data, not synthetic data

---

## Why Not Build Our Own Instead?

This POC evaluated that option. Short answer: no.

| | Adopt Existing | Build Custom (Foundry) |
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
| 13x cheaper than assembling alternatives | $39/mo vs $507/mo (actual billing data) |
| 243x cheaper than building custom | $39/mo vs $9,454/mo (Foundry TCO analysis) |

<div class="key-insight" markdown>
**The ask is one $39/month test license.** The risk is near zero. The validation takes 2 weeks. Cancel if it doesn't work. The evidence so far says it will.
</div>

<div class="cta-box" markdown>

### Want the full evidence?

[Cost Analysis](cost-evidence.md) | [Output Quality](quality-evidence.md) | [Foundry Analysis](foundry-analysis.md) | [Roadmap](roadmap.md)

</div>
