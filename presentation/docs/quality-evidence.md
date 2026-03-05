# Quality Evidence: 96.1% on First Execution

## Five Scenarios. 155 Quality Checks. 149 Passed.

We didn't just measure cost. We measured **quality** — running 5 representative architecture scenarios through a structured evaluation framework with specific quality criteria per scenario.

---

## The Scorecard

**SC-01 — Ticket Triage** (Wristband RFID field addition)
<div class="score-bar"><div class="fill" style="width: 92%">23/25 — 92%</div></div>

**SC-02 — Classification Design** (Adventure category to check-in pattern mapping)
<div class="score-bar"><div class="fill" style="width: 94%">33/35 — 94%</div></div>

**SC-03 — Production Investigation** (Guide schedule overwrite bug)
<div class="score-bar"><div class="fill" style="width: 100%">30/30 — 100%</div></div>

**SC-04 — Architecture Update** (Elevation data Swagger spec modification)
<div class="score-bar"><div class="fill" style="width: 96%">24/25 — 96%</div></div>

**SC-05 — Complex Cross-Service Design** (Unregistered guest self check-in)
<div class="score-bar"><div class="fill" style="width: 98%">39/40 — 98%</div></div>

<div class="big-number">149/155</div>

**Total: 96.1% standards compliance across all scenarios.**

---

## What Was Produced

Across 5 scenarios, the AI generated **39 files** including:

| Artifact Type | Count | Standard |
|--------------|:-----:|----------|
| MADR Architecture Decision Records | 9 | Markdown Any Decision Record format |
| Solution designs | 5 | arc42 template structure |
| Impact assessments | 6 | Service-level impact analysis |
| User stories | 14 | User perspective with acceptance criteria |
| Investigation reports | 2 | Evidence-grounded with source citations |
| Implementation guidance | 5 | Code patterns and migration steps |
| Swagger spec updates | 2 | OpenAPI 3.0 modifications |
| PlantUML diagrams | 2 | C4 model notation |
| Simple explanations | 4 | Non-technical stakeholder summaries |
| Assumptions documents | 4 | Documented constraints and dependencies |

Every artifact followed the required standard — arc42 sections, MADR format, C4 notation, ISO 25010 quality attributes — with **no manual template enforcement**.

---

## Head-to-Head: Copilot vs Roo Code

Both tools used the same underlying model (Claude Opus 4.6) and the same workspace. The differences reveal that the **agent framework matters as much as the model**.

| Dimension | Copilot | Roo Code |
|-----------|:------:|:-------:|
| **Files produced** | 39 | 37 (missing 2) |
| **Accuracy** | Zero fabrication | Fabricated 4 OpenAPI fields |
| **Tool utilization** | 5 mock script calls | 3-4 mock script calls |
| **Workspace file reads** | 40+ | 22 |
| **Standards compliance** | 96.1% | Not independently scored |

### The Critical Accuracy Failure

In Scenario 4, Roo Code was asked to update a Swagger spec based on an **approved design**. It was supposed to enhance existing elevation fields with better descriptions and constraints.

Instead, it **fabricated 4 entirely new schema elements** — `max_elevation_m`, `min_elevation_m`, `elevation_profile`, and `ElevationDataPoint` — that were **not in the approved design**.

| Field | In Approved Design? | Copilot | Roo Code |
|-------|:---:|:---:|:---:|
| `elevation_gain_m` (existing) | Yes | Enhanced | Enhanced |
| `elevation_loss_m` (existing) | Yes | Enhanced | Enhanced |
| `max_elevation_m` | **No** | Not added | **FABRICATED** |
| `min_elevation_m` | **No** | Not added | **FABRICATED** |
| `elevation_profile` | **No** | Not added | **FABRICATED** |
| `ElevationDataPoint` | **No** | Not added | **FABRICATED** |

!!! warning "Why This Matters"
    In a corporate environment, merging fabricated API contract fields would **break downstream consumers**, create **false contract commitments**, and **violate architecture governance**. Roo Code's own run summary claimed "No fabricated data" — indicating it lacked self-awareness of its accuracy failure.

---

## Quality Dimensions

The evaluation covered five dimensions. Copilot won or tied in every one:

| Dimension | Winner | Evidence |
|-----------|:------:|---------|
| **Completeness** | Copilot | 39 files vs 37; Roo Code missing `simple.explanation.md` and `assumptions.md` in the hardest scenario |
| **Accuracy** | Copilot | Zero fabrication vs 4 fabricated OpenAPI fields |
| **Standards Compliance** | Copilot | 149/155 (96.1%) across all 5 scenarios |
| **Tool Utilization** | Copilot | Fetched MR-5001 detail for deeper investigation; Roo Code stopped at the list view |
| **ADR Quality** | Copilot | More detailed consequences sections with source code line references |

---

## What This Means

<div class="key-insight" markdown>
**The AI produces architecture artifacts at 96.1% quality on its first attempt** — using the same standards (arc42, MADR, C4, ISO 25010) that the architecture practice mandates. This is not a rough draft that needs heavy editing. It's production-quality output that needs a final review pass.
</div>

And the better-performing tool is also the **208x cheaper** one.

<div class="cta-box" markdown>

### How does the AI produce such accurate results?

[The Shared Workspace: AI Sees What the Architect Sees](shared-workspace.md)

</div>
