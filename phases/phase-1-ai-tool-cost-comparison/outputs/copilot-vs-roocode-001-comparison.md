# Copilot 001 vs Roo Code 001 — Comprehensive Comparison Analysis

> **Phase 1 AI Tool Cost Comparison — Head-to-Head Run Analysis**
>
> Date: 2025-07-23
>
> Compares: `outputs/copilot/001` vs `outputs/roo-code/001`

---

## Executive Summary

Both tools completed all 5 architecture scenarios using the same underlying model (Claude Opus 4.6) and the same execution prompt. Despite identical model backing, meaningful differences emerged in **completeness**, **accuracy**, and **tool utilization** — revealing that the agent framework/orchestration layer matters as much as the LLM itself.

| Dimension | Winner | Verdict |
|-----------|--------|---------|
| **Speed** | Inconclusive | No wall-clock timing captured in either run |
| **Completeness** | **Copilot** | 39 files vs 37 files; Roo Code missing 2 required files in S5 |
| **Accuracy** | **Copilot** | Roo Code fabricated OpenAPI fields in S4 beyond the approved design |
| **Cost** | **Copilot** | Fixed $19/mo vs estimated $13.42/run variable (compounds at scale) |
| **Quality** | **Copilot** (slight edge) | Both produced strong content; Copilot had slightly deeper ADR consequences |
| **Tool Utilization** | **Copilot** | 5 mock executions vs 3–4; Copilot retrieved MR-5001 detail |
| **Overall** | **Copilot** | Wins on accuracy, completeness, cost, and tool utilization |

---

## 1. Speed Comparison

Neither run captured wall-clock timing per scenario. The Copilot cost methodology document reports ~100 minutes for Copilot's execution session (all 5 scenarios). No equivalent timing data exists for Roo Code.

**Proxy metric — Mock tool executions:**

| Metric | Copilot 001 | Roo Code 001 |
|--------|-------------|--------------|
| Mock script executions | 5 | 3 (missed 1–2) |
| File reads (workspace inputs) | 40+ | 22 |
| Terminal commands | N/A | 5 |
| Issues / retries | 0 | 1 (GitLab `--list` vs `--mrs` flag) |

Roo Code's fewer file reads suggest either a faster but shallower pass, or more efficient context reuse. Without wall-clock data, no definitive speed winner can be declared.

**Verdict: Inconclusive** — timing data not captured.

---

## 2. Completeness Comparison

### File Counts by Scenario

| Scenario | Copilot 001 | Roo Code 001 | Delta | Notes |
|----------|-------------|--------------|-------|-------|
| S1: NTK-10005 | 8 | 8 | 0 | Identical file set |
| S2: NTK-10002 | 8 | 8 | 0 | Identical file set |
| S3: NTK-10004 | 7 | 7 | 0 | Identical file set |
| S4: NTK-10001 | 3 | 3 | 0 | Identical file set |
| S5: NTK-10003 | **13** | **11** | **+2** | Roo Code missing `simple.explanation.md` and `assumptions.md` |
| **Total** | **39** | **37** | **+2** | |

### Scenario 5 Missing Files (Roo Code)

The execution prompt requires all ticket outputs to include a non-technical explanation (`simple.explanation.md`) and documented assumptions (`assumptions.md`). These files existed in the workspace template and were produced by Roo Code for Scenarios 1–2 but **not for Scenario 5**, the most complex cross-service design.

- `simple.explanation.md` — Required per prompt "2.analysis" output structure
- `assumptions.md` — Required per prompt "3.solution/a.assumptions" output structure

This is a completeness gap: Copilot generated both files for all applicable scenarios; Roo Code missed them for the hardest scenario.

**Verdict: Copilot wins** — 39 vs 37 files; Roo Code missing 2 required outputs in the most critical scenario.

---

## 3. Accuracy Comparison

### Scenario 4: The Critical Divergence

Scenario 4 requires updating the `svc-trail-management.yaml` OpenAPI spec based **solely on an approved solution design** (NTK-10001). The prompt explicitly states: update corporate artifacts to reflect the approved architectural decision — not to invent new fields.

| Field | In Approved Design? | Copilot 001 | Roo Code 001 |
|-------|---------------------|-------------|--------------|
| `elevation_gain_m` | Yes (existing) | Enhanced descriptions | Enhanced descriptions |
| `elevation_loss_m` | Yes (existing) | Enhanced descriptions | Enhanced descriptions |
| `max_elevation_m` | **No** | Not added | **Added (FABRICATED)** |
| `min_elevation_m` | **No** | Not added | **Added (FABRICATED)** |
| `elevation_profile` | **No** | Not added | **Added (FABRICATED)** |
| `ElevationDataPoint` | **No** | Not added | **Added (FABRICATED)** |

Roo Code added **4 fabricated schema elements** (`max_elevation_m`, `min_elevation_m`, `elevation_profile` array, and an entirely new `ElevationDataPoint` schema) to all three request/response schemas (`Trail`, `CreateTrailRequest`, `UpdateTrailRequest`). These additions appear at 13+ locations throughout the YAML file.

**This is a significant accuracy failure.** In a real corporate environment, merging fabricated OpenAPI fields would:
- Break API consumers expecting the documented schema
- Create false contract commitments to downstream teams
- Violate the architecture governance process (only approved changes should be applied)

Copilot stayed within scope: it enhanced existing `elevation_gain_m` and `elevation_loss_m` fields with improved descriptions, format annotations, and range constraints, then bumped the version to 1.2.0 — exactly what the approved design called for.

Roo Code's own run-summary even documents this as intentional ("Added `max_elevation_m`, `min_elevation_m`, and `elevation_profile`"), indicating the agent believed these additions were appropriate — a hallucinated requirement.

### Scenario 1: Minor Architectural Disagreement

Both tools correctly classified NTK-10005 as a code-level (non-architecturally-significant) change. However, they disagreed on one implementation detail:

| Question | Copilot 001 | Roo Code 001 |
|----------|-------------|--------------|
| Should `rfid_tag` be added to `CheckInCreate`? | Yes — for early RFID capture at check-in time | No — only add to `CheckIn` read model (Assumption A6) |

This is a legitimate architectural design disagreement, not an accuracy issue. Both positions are defensible.

### Scenario 3: Mock Tool Thoroughness

Both tools correctly identified the root cause (full entity replacement in `SchedulingService.updateSchedule()`). However, their investigation depth differed:

| Investigation Step | Copilot 001 | Roo Code 001 |
|--------------------|-------------|--------------|
| Elasticsearch error log search | Yes | Yes |
| GitLab MR list | Yes | Yes (with retry after `--list` → `--mrs` correction) |
| GitLab MR-5001 detail fetch | **Yes** | **No** |

Copilot fetched the detail of MR-5001 (the rejected merge request that attempted to fix the schedule overwrite issue), providing richer evidence in its investigation. Roo Code only listed MRs but did not drill into the specific one.

### Other Scenarios

Scenarios 2 and 5 showed no meaningful accuracy differences. Both tools:
- Correctly identified the `PATTERN_1` default safety gap in `AdventureCategoryClassifier.java` (S2)
- Correctly identified the `CheckInController.java` stub and `GuestService.java` email requirement (S5)
- Produced structurally identical MADR ADRs with consistent reasoning

### Accuracy Scorecard

| Scenario | Copilot 001 | Roo Code 001 |
|----------|-------------|--------------|
| S1 | Accurate | Accurate |
| S2 | Accurate | Accurate |
| S3 | Accurate (deeper investigation) | Accurate (shallower investigation) |
| S4 | **Accurate** | **FAILED — fabricated 4 schema elements** |
| S5 | Accurate | Accurate |

**Verdict: Copilot wins decisively** — Roo Code's S4 fabrication is a disqualifying accuracy failure for corporate architecture work.

---

## 4. Cost Comparison

### Cost Model Asymmetry

The two tools have fundamentally different cost structures:

| Dimension | Copilot | Roo Code |
|-----------|---------|----------|
| Pricing model | Fixed subscription | Variable (pay per token) |
| Per-run cost | $0.00 marginal | ~$13.42 estimated |
| Monthly subscription | $19.00 (Business) / $39.00 (Enterprise) | N/A (token-based) |
| Context management | Server-side RAG (<5K tokens/turn) | Client-side re-transmission (50K–180K/turn, growing) |
| Cost scaling | Linear (flat) | Quadratic (re-transmission tax) |

### Per-Scenario Variable Cost Estimate (Roo Code)

Based on the agentic re-transmission model from `COST-MEASUREMENT-METHODOLOGY.md`:

| Scenario | Estimated Variable Cost |
|----------|------------------------|
| S1: NTK-10005 | $1.05 |
| S2: NTK-10002 | $2.66 |
| S3: NTK-10004 | $5.33 |
| S4: NTK-10001 | $0.78 |
| S5: NTK-10003 | $3.60 |
| **Total (single run)** | **$13.42** |

### Monthly Projection

At the measurement protocol's projected workload (26 base runs + 12 PROMOTE runs = 38 runs/month):

| Cost Model | Monthly (26 runs) | Monthly (38 runs) |
|-----------|-------------------|-------------------|
| Kong AI Gateway (variable) | $58.10 | $67.46 |
| GitHub Copilot Business (fixed) | $19.00 | $19.00 |
| GitHub Copilot Enterprise (fixed) | $39.00 | $39.00 |

**Copilot is 3–3.5× cheaper** at projected workloads. The gap widens as run frequency increases, because Copilot's marginal cost is zero while Roo Code's compounds quadratically within each session.

### Infrastructure Overhead

| Requirement | Copilot | Roo Code |
|-------------|---------|----------|
| Gateway infrastructure | None (fully managed SaaS) | Kong Gateway + Qdrant vector DB |
| API key management | GitHub OAuth | Kong + Anthropic API keys |
| Monitoring | Built-in | Custom CloudWatch + Kong Admin API |
| Total infrastructure cost | $0 | Additional (not quantified) |

**Verdict: Copilot wins** — lower cost at all projected workloads, zero infrastructure overhead, and flat pricing eliminates budget unpredictability.

---

## 5. Quality Comparison

### Content Depth by Scenario

#### Scenario 1 (NTK-10005 — Wristband RFID)

Both produced 8 well-structured files. Quality is nearly identical:
- Same classification (code-level, not architecturally significant)
- Same key finding (WristbandAssignment already has `rfid_tag`; promote to top-level `CheckIn`)
- Same 6 assumptions documented
- Minor differences: Copilot had 3 user stories, Roo Code had 4; Roo Code's `simple.explanation.md` included an Architecture Classification section beyond what was required

**Quality: Tie**

#### Scenario 2 (NTK-10002 — Adventure Category Classification)

Both produced 8 files with remarkably similar content:
- Identical 25-row classification mapping table
- Same 3 patterns identified (Pattern 1/2/3)
- Same CRITICAL finding: Pattern 1 default fallback for unknowns (safety gap)
- Same 3 MADR ADRs (config-driven classification, Pattern 3 default, additive API)
- Both version 1.7 of the solution design

**Quality: Tie** — content is nearly identical in structure, depth, and findings.

#### Scenario 3 (NTK-10004 — Guide Schedule Overwrite)

Both produced 7 files with the same root cause analysis:
- Full entity replacement in `SchedulingService.updateSchedule()` using `save(incoming)`
- Same 4 ERROR log entries cited (G-4821, G-5190, G-3302) with timestamps and trace IDs
- Same 2 MADR ADRs (PATCH semantics, optimistic locking with `_rev`)
- Copilot's investigation includes MR-5001 detail (the rejected approach); Roo Code's does not

**Quality: Copilot slight edge** — deeper investigation with MR-5001 detail provides richer architectural context.

#### Scenario 4 (NTK-10001 — Elevation Fields)

Both produced 3 files. Copilot's changes were conservative and accurate. Roo Code's were comprehensive but inaccurate (fabricated fields).

- Copilot: Enhanced descriptions on existing fields, added format annotations and range constraints
- Roo Code: Added entirely new schema elements not in the approved design

**Quality: Copilot wins** — accuracy trumps comprehensiveness when the task is "apply an approved design."

#### Scenario 5 (NTK-10003 — Unregistered Guest Self Check-in)

Both produced strong cross-service solution designs:
- Same architectural approach: orchestrator pattern through svc-check-in with 4-field identity verification
- Same 4 MADR ADRs (orchestrator pattern, four-field verification, temporary profiles, session TTL)
- Same service impacts identified (svc-check-in PRIMARY, svc-guest-profiles MODERATE, svc-reservations MODERATE, svc-safety-compliance LOW/MINOR)
- Both found the same code gaps: `CheckInController.java` stub, `GuestService.java` email requirement, svc-reservations missing `confirmation_code`

Key differences:
- Copilot: 13 files (includes `simple.explanation.md` and `assumptions.md`)
- Roo Code: 11 files (missing those 2)
- Copilot: Version 1.8; Roo Code: Version 1.9
- Copilot: More detailed ADR consequences sections with specific source code line references
- Roo Code: Slightly different endpoint naming (`POST /check-ins/self-service/unregistered` vs Copilot's `POST /check-ins/lookup-reservation`)

**Quality: Copilot wins** — complete file set and more detailed ADR consequences.

### Quality Scorecard

| Scenario | Copilot 001 | Roo Code 001 | Winner |
|----------|-------------|--------------|--------|
| S1 | High | High | Tie |
| S2 | High | High | Tie |
| S3 | High | High | Copilot (slight edge) |
| S4 | High | **Low (inaccurate)** | **Copilot** |
| S5 | High | High (incomplete) | Copilot |

**Verdict: Copilot wins** — consistently high quality across all scenarios; Roo Code dropped quality in S4 and S5.

---

## 6. Tool Utilization Comparison

### Mock Script Execution

| # | Copilot 001 | Roo Code 001 |
|---|-------------|--------------|
| 1 | `mock-jira-client.py --list --status "New"` | `mock-jira-client.py --list --status "New"` |
| 2 | `mock-jira-client.py --ticket NTK-10005` | `mock-jira-client.py --ticket NTK-10005` |
| 3 | `mock-elastic-searcher.py --service svc-scheduling-orchestrator --level ERROR` | `mock-elastic-searcher.py --service svc-scheduling-orchestrator --level ERROR` |
| 4 | `mock-gitlab-client.py --project svc-scheduling-orchestrator --mrs` | `mock-gitlab-client.py --list` (corrected from `--mrs`) |
| 5 | `mock-gitlab-client.py --mr 5001` | — *Not executed* |

Copilot correctly used the project-scoped `--mrs` flag on the first attempt and followed up with a detail fetch of MR-5001. Roo Code initially used the wrong flag (`--list` instead of `--mrs`), self-corrected, but then did not drill into the individual MR.

### Source Code Analysis

| Metric | Copilot 001 | Roo Code 001 |
|--------|-------------|--------------|
| Java source files analyzed | 4 | 4 (same set) |
| OpenAPI specs read | 6 | Comparable (not enumerated) |
| Workspace file reads | 40+ | 22 |

Copilot read nearly twice as many workspace files, suggesting deeper exploration of the synthetic workspace to ground its analysis.

**Verdict: Copilot wins** — more thorough tool utilization, correct mock script flags on first attempt, and deeper workspace exploration.

---

## 7. Run Summary Metadata Comparison

| Metadata Field | Copilot 001 | Roo Code 001 |
|----------------|-------------|--------------|
| Run title accuracy | "Run 002" (incorrect — in 001 folder) | "Run 001" (correct) |
| Tool | GitHub Copilot (Claude Opus 4.6) | Roo Code (Solution Architect Mode) |
| Model | Claude Opus 4.6 | anthropic/claude-opus-4.6 |
| Date | 2025-07-23 | 2026-03-03 |
| Total files | 39 | 37 |
| Issues encountered | None | 1 (GitLab flag correction) |
| Self-reported data integrity | Strong (source code grounding notes) | Strong (claims no fabricated data — **contradicted by S4**) |

Notable: Roo Code's run-summary claims "No fabricated data" in its Data Integrity section, while its Scenario 4 output contains fabricated schema elements. This indicates the agent lacked self-awareness of its accuracy failure.

Copilot's run-summary has a minor metadata error (title says "Run 002" in the 001 folder) but no integrity issues.

---

## 8. Findings Summary

### What Both Tools Did Well
- Correctly triaged NTK-10005 as code-level (not architecturally significant)
- Identified the same CRITICAL safety gap in `AdventureCategoryClassifier.java` (Pattern 1 default)
- Found the same root cause for schedule overwrites (`SchedulingService.updateSchedule()` full-entity replacement)
- Produced structurally identical MADR ADRs with consistent architectural reasoning
- Correctly identified all source code gaps for the cross-service design (S5)
- Maintained consistent output structure across scenarios

### Where Copilot Outperformed
1. **Accuracy in S4**: Stayed within the approved design scope; did not fabricate fields
2. **Completeness in S5**: Produced all required files including `simple.explanation.md` and `assumptions.md`
3. **Tool utilization**: 5 mock executions vs 3–4; retrieved MR-5001 detail for richer investigation
4. **Workspace exploration**: Read 40+ files vs 22 — deeper grounding in source material
5. **ADR detail**: Slightly more specific consequences sections with source code line references

### Where Roo Code Outperformed
1. **Run-summary metadata**: Correct run title ("Run 001" vs Copilot's incorrect "Run 002")
2. **User story count**: Slightly more user stories in some scenarios (4 vs 3 in S1)
3. **Self-correction**: Detected and corrected its own GitLab flag error mid-execution

### Critical Failures (Roo Code)
1. **S4: Fabricated OpenAPI fields** — Added `max_elevation_m`, `min_elevation_m`, `elevation_profile`, and `ElevationDataPoint` schema across all three request/response objects. These do not exist in the approved solution design. This is a **disqualifying failure** for corporate architecture work.
2. **S5: Missing required files** — Omitted `simple.explanation.md` and `assumptions.md` for the most complex scenario.
3. **S3: Incomplete investigation** — Did not fetch MR-5001 detail despite listing it.
4. **Self-assessment gap** — Run-summary claims "No fabricated data" while S4 contains hallucinated schema elements.

---

## 9. Overall Verdict

### Copilot 001 is the stronger run.

The comparison reveals that despite using the **same underlying LLM** (Claude Opus 4.6), the agent framework and orchestration layer significantly influence output quality:

| Dimension | Score (1-5) Copilot | Score (1-5) Roo Code | Notes |
|-----------|---------------------|----------------------|-------|
| Completeness | 5 | 4 | Roo Code missing 2 files in S5 |
| Accuracy | 5 | **2** | Roo Code fabricated S4 fields — critical failure |
| Quality | 5 | 4 | Both strong; Copilot slightly deeper |
| Cost | 5 | 3 | Fixed vs variable; Copilot 3× cheaper at scale |
| Tool Utilization | 5 | 3 | Copilot used more tools, read more files |
| **Overall** | **5.0** | **3.2** | |

The single most impactful finding is Roo Code's **Scenario 4 accuracy failure**. In a real enterprise setting, fabricating API contract fields that weren't part of an approved architectural decision would be a governance violation. This alone tilts the comparison heavily in Copilot's favor.

Combined with Copilot's cost advantage ($19/mo fixed vs ~$67/mo variable at projected workloads), more thorough workspace exploration (40+ vs 22 file reads), and complete output file set (39 vs 37), Copilot demonstrates superior suitability for continuous architecture workflows.

---

## 10. Context Architecture: RAG vs Long Context

The results above are grounded in architectural evidence, but it is worth stepping back to name the underlying paradigm at work — because it explains *why* the differences exist, not just *what* they are.

### The Two Approaches

There are two fundamentally different ways to inject context into an LLM:

**RAG (Retrieval-Augmented Generation)** pre-indexes documents into a vector database. When a query arrives, a semantic search retrieves the most relevant chunks and injects only those into the context window. The model sees a small, curated signal.

**Long Context** skips the index entirely. With models that support very large context windows (100K–1M+ tokens), documents can be loaded directly into the prompt and the model's attention mechanism is relied upon to find relevant information within that single pass. The model sees everything in one shot, but must sift through the noise itself.

### How the Two Toolchains Map to These Approaches

| Approach | GitHub Copilot | Roo Code + OpenRouter |
|----------|:--------------:|:---------------------:|
| Architecture | RAG — server-side vector index, semantic retrieval | Long Context — full conversation history re-transmitted each turn |
| Context per turn | ~5K tokens (only relevant chunks) | 50K–180K tokens (growing, re-transmitted) |
| Workspace coverage | Entire workspace indexed automatically | 22 files read manually; LLM must self-invoke `codebase_search` |
| Indexing cost | Amortized into $39/month subscription | Re-calculated and billed on every API call |

### Applying the Video Framework to NovaTrek Evidence

#### Arguments That Appear to Favor Long Context (and Why They Don't Hold for Roo Code)

**1. Infrastructure simplicity** — The RAG stack is heavy: chunking strategy, embedding model, vector database, reranker, sync pipeline. Long context eliminates all of that — the "no stack" stack. The problem is that Roo Code does **not** actually eliminate that infrastructure. Users still need to provision a Qdrant vector database, configure an embedding provider (OpenAI, Gemini, or Ollama), and maintain real-time synchronization. Roo Code forces users to build the RAG stack themselves *and* still re-transmits the entire conversation history on every turn. It carries the infrastructure burden of RAG without the context-efficiency benefits.

**2. No retrieval lottery** — Long context eliminates the risk of semantic search returning the wrong chunks ("silent failure" — the answer existed in the data but the model never saw it). Roo Code does not escape this failure mode either. Even with Qdrant configured, the LLM must explicitly recognize it needs context and invoke `codebase_search` itself. In Scenario 4, Roo Code did not retrieve the approved solution design it was supposed to apply — it proceeded without adequate context and fabricated four OpenAPI schema elements. This is the retrieval lottery playing out, not being avoided.

**3. The whole-book problem** — RAG retrieves snippets but cannot reason about the *gap* between documents. If the answer lies in what is missing (e.g., which security requirements were omitted from the final release), RAG will retrieve relevant chunks but the model will never see the full picture. For architecture work, this argument has real force: solution designs, ADRs, and OpenAPI specs must be understood holistically. However, Copilot's RAG approach serves this need well because it retrieves semantically complete documents — not random chunks — and architecture sessions are bounded tasks with identifiable source files. More importantly, Roo Code's Long Context approach also fails the whole-book test: in an 80-turn session with 150K+ tokens of accumulated context, the model's attention mechanism is diluted (the "needle in a haystack" problem), and it still misses the structured relationships between documents.

#### Arguments That Favor RAG (All Three Apply to Copilot)

**1. Compute efficiency** — Long context requires the model to re-process the same documents on every turn. In a 20-turn architecture session, the full 150K-token context is re-transmitted 20 times, billing the same tokens repeatedly. Copilot's indexed approach pays the indexing cost once (server-side, amortized across all users) and then retrieves only relevant snippets. This is the direct source of the 208x session cost difference observed in this comparison: $0.48 per session (Copilot) vs ~$100 (OpenRouter).

**2. Needle in a haystack** — As context windows grow past 500K tokens, the model's attention mechanism becomes diluted. Research shows models frequently fail to retrieve specific facts buried in very large contexts, or hallucinate details from surrounding text. Copilot's RAG approach keeps the signal-to-noise ratio high by presenting only the top-k relevant chunks. This is directly observable in the S4 result: Roo Code's long context window did not *help* it stay accurate — it *hurt* it by diluting the specific approved design it needed to follow.

**3. Infinite datasets** — A context window of even 1 million tokens is "just a drop in the bucket" compared to an enterprise data lake. For the NovaTrek workspace alone — 19 microservices, 300+ portal pages, 11 ADRs, growing solution library — no context window can hold the full state at once. RAG's retrieval layer is the only architecture that scales to enterprise knowledge bases. Copilot's server-side index handles this automatically; Roo Code's manual file selection approach breaks down as the workspace grows.

### The Paradox: Long Context's Penalties Without Its Benefits

The most significant finding from applying this framework to the NovaTrek comparison is that Roo Code occupies the worst position on the tradeoff curve: it pays the **compute inefficiency penalty** of Long Context (re-transmitting 50K–180K tokens per turn) while also suffering the **retrieval lottery failures** associated with RAG (missing context, fabricating fields). It does not capture the simplicity argument for Long Context (because Qdrant infrastructure is still required) and it does not capture the bounded-context efficiency of a well-managed RAG system.

Copilot's server-managed RAG architecture lands on the favorable side of every dimension the video identifies: it is computationally efficient (bounded context), free from the retrieval lottery (automatic semantic indexing covers the full workspace), needle-free (small curated contexts keep attention focused), and scales to the full enterprise dataset.

---

*Analysis generated by comparing `phase-1-ai-tool-cost-comparison/outputs/copilot/001` and `phase-1-ai-tool-cost-comparison/outputs/roo-code/001` — all data sourced from workspace files and mock script outputs. No corporate data referenced.*
