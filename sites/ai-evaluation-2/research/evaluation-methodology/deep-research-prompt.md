# Deep Research Prompt: Evaluation Methodology

## Objective

Investigate every methodological claim, scoring rubric definition, and weight assignment on the Evaluation Methodology page. This page defines the framework used to produce the scoring results — its academic and professional rigor determines whether the entire evaluation is defensible.

---

## Claims to Investigate

### 1. Weighted Scoring Model as Methodology

**Research questions:**
- Is the weighted scoring model (also called weighted factor analysis or multi-criteria decision analysis) a recognized and respected methodology for technology selection? Cite academic and industry sources (e.g., Saaty's AHP, TOPSIS, ELECTRE, or simpler weighted scoring).
- What are the documented weaknesses of weighted scoring models? (e.g., sensitivity to weight selection, anchoring bias in scoring, false precision)
- What safeguards does the literature recommend? (e.g., sensitivity analysis, independent scoring, calibration meetings). Does this methodology include those safeguards?

### 2. Factor Count and Category Organization

The methodology uses 12 factors across 4 categories: Economics (29%), Quality and Capability (36%), Operational Fitness (20%), Strategic and Risk (15%).

**Research questions:**
- Is 12 factors a reasonable number for a technology evaluation? Cite guidance from decision analysis literature on optimal factor count (too few = oversimplified, too many = diminishing marginal insight).
- Are the four categories well-chosen? Compare against established enterprise technology evaluation frameworks (e.g., Gartner's Magic Quadrant dimensions: Completeness of Vision + Ability to Execute; Forrester's Total Economic Impact framework; ISO 25010 quality model).
- Is the weight distribution (36% on Quality, 29% on Economics, 20% on Operational, 15% on Strategic) reasonable? Are there benchmarks for how enterprises typically weight these concerns?

### 3. EF-01 Total Cost of Ownership — Rubric and Weight (15%)

**Research questions:**
- Is 15% weight for TCO standard in enterprise technology evaluations? Cite benchmarks.
- The rubric uses $50/seat/month as the threshold for a score of 5. Is this calibrated to the AI platform market? What do competing platforms actually cost?
- Is "amortized over 24 months" a standard amortization period for engineering investment in technology evaluations?

### 4. EF-04 Architecture Output Quality at Operating Budget — Weight (20%)

The methodology gives 20% weight to output quality, making it the single heaviest factor. It explicitly links budget to model quality.

**Research questions:**
- Is it standard practice to weight output quality as the single highest factor in AI platform evaluations? Cite comparable evaluations.
- Is the concept of "budget-constrained model selection" — scoring based on the model you can afford, not the best available — documented in AI evaluation literature?
- What external benchmarks exist for measuring AI architecture output quality? (e.g., SWE-bench, HumanEval, architecture-specific benchmarks)

### 5. Scoring Rubrics (1-5 Scale)

**Research questions:**
- Is a 1-5 ordinal scale appropriate for this type of evaluation? What are the alternatives (e.g., 1-10, binary pass/fail, continuous)?
- What does decision analysis literature say about the precision of ordinal scales? Is a 1-point difference between scores (e.g., 3 vs 4) meaningful?
- Are the rubric definitions sufficiently operational (i.e., could two independent evaluators arrive at the same score)? This is a critical question for defensibility.

### 6. ISO 25010 Alignment

The methodology references ISO 25010 quality characteristics.

**Research questions:**
- Does this methodology actually align with ISO 25010, or does it merely mention it? Map each evaluation factor to the ISO 25010 quality characteristic it corresponds to.
- Is ISO 25010 appropriate for evaluating AI platforms, or is it designed for software product quality? Are there AI-specific quality models emerging?

### 7. Sensitivity Analysis Method — "+/- 5 Percentage Points"

**Research questions:**
- Is the "+/- 5 percentage point shift on one factor at a time" a standard sensitivity analysis technique? Cite sources.
- What are more rigorous alternatives? (e.g., Monte Carlo simulation, pairwise weight sensitivity, full factorial analysis)
- Is one-at-a-time (OAT) sensitivity analysis considered sufficient in academic decision analysis, or is it criticized for missing interaction effects?

### 8. Critical Failure Check (Score of 1)

**Research questions:**
- Is a "hard floor" (any factor scored 1 disqualifies the option unless explicitly accepted) a standard feature of weighted scoring models?
- In multi-criteria decision analysis, how are absolute thresholds typically handled? Cite the ELECTRE method's concordance/discordance thresholds or similar approaches.
- Is this a reasonable safeguard or does it introduce bias by allowing low-weight factors to disqualify otherwise strong options?

### 9. Evidence Source Categories

The methodology defines four evidence source types: run data, vendor documentation, POC results, reasoned analysis.

**Research questions:**
- Is this evidence hierarchy standard in technology evaluation? Cite comparable frameworks.
- Should there be a weighting or confidence adjustment based on evidence type (e.g., run data > vendor docs > reasoned analysis)?
- Are there evidence quality standards from systematic review methodologies (e.g., GRADE framework from medicine) that could be adapted?

---

## Expected Output Format

For each claim:
1. **Claim as stated** — exact quote from the page
2. **Verdict** — Confirmed / Partially Confirmed / Unconfirmed / Incorrect
3. **Evidence** — cited sources with URLs, dates accessed, and relevant excerpts
4. **Recommended correction** — if the claim needs updating, provide the corrected text
5. **Confidence level** — High / Medium / Low based on source quality

Include a summary table at the top with all claims and their verdicts.
