# Output Analysis: What the AI Produced

## Five Scenarios. 39 Architecture Files. Head-to-Head Comparison.

We didn't just measure cost. We measured **what was actually produced** — running 5 representative architecture scenarios and comparing Copilot's output against Roo Code's on completeness, accuracy, and adherence to standards.

---

## The Five Scenarios

**SC-01 — Ticket Triage** (Wristband RFID field addition)  
Produced: Solution design, 2 ADRs, impact assessment, user stories, assumptions  
**Outcome**: Identified cross-service impacts, proposed phased rollout

**SC-02 — Classification Design** (Adventure category to check-in pattern mapping)  
Produced: Solution design with configuration-driven approach, 2 ADRs, implementation guidance  
**Outcome**: Recommended YAML-based classification with Pattern 3 fallback for safety

**SC-03 — Production Investigation** (Guide schedule overwrite bug)  
Produced: Investigation report citing specific log entries and source code lines, 2 ADRs, 3-phase remediation plan  
**Outcome**: Root cause traced to entity replacement anti-pattern, recommended PATCH semantics + optimistic locking

**SC-04 — Architecture Update** (Elevation data Swagger spec modification)  
Produced: Updated OpenAPI spec, impact assessment, implementation guidance  
**Outcome**: Enhanced existing fields with better descriptions and constraints

**SC-05 — Complex Cross-Service Design** (Unregistered guest self check-in)  
Produced: Solution design spanning 6 services, 3 ADRs, 14 user stories, PlantUML diagrams  
**Outcome**: Designed session-scoped temporary guest profile with bounded context enforcement

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
| **Accuracy** | Copilot | Zero fabrication vs 4 fabricated OpenAPI fields (see below) |
| **Standards Adherence** | Copilot | Followed MADR format, arc42 structure, C4 notation across all scenarios |
| **Tool Utilization** | Copilot | Fetched MR-5001 detail for deeper investigation; Roo Code stopped at the list view |
| **ADR Quality** | Copilot | More detailed consequences sections with source code line references |

---

## What This Demonstrates

<div class="key-insight" markdown>
Across 5 scenarios, the AI produced 39 complete architecture artifacts following corporate standards (arc42, MADR, C4, ISO 25010). These are structured documents that follow templates, cite specific source code lines, and cross-reference actual workspace files. The toolchain that produced higher-quality output also had the lower cost profile.
</div>

<div class="cta-box" markdown>

### How does the AI produce such accurate results?

[The Shared Workspace: AI Sees What the Architect Sees](shared-workspace.md)

</div>
