# Closing the Loop: The PROMOTE Step

## The Innovation That Makes Architecture Continuous

Our architecture practice has two gaps that compound over time: Confluence pages that fall behind Git because updating them is voluntary, and a design-to-reality divergence that no one reconciles after deployment. The first gap is closed by automated publishing. The second requires something new.

**The PROMOTE step closes the design-to-reality gap — verifying what was built matches what was designed, and recording the actual state as the new baseline.**

---

## The Two Gaps

### Gap 1: Browsable Documentation Falls Behind (Solved by Automated Publishing)

Specs and diagrams are checked into Git — but the browsable Confluence pages that architects and stakeholders actually consult are updated manually and voluntarily. The automated publishing pipeline (Pillar 4) closes this gap: a `git push` generates an always-current portal.

### Gap 2: Design Intent vs Production Reality (Solved by PROMOTE)

This is the harder problem. Architecture designs describe *intent*. But developers sometimes deviate during implementation. After deployment:

| Metric | Current State |
|--------|:-----:|
| ADRs created during projects | Created in ticket branches |
| ADRs promoted to a discoverable global log | 0 |
| Specs reconciled against actual production behavior | 0 |
| Service documentation updated to reflect what was actually built | 0 |

<div class="big-number red">0%</div>

**of architecture knowledge is reconciled against reality after deployment.**

This isn't a discipline failure — it's a structural one. There is no step in the workflow for it.

---

## What Gets Lost Without PROMOTE

Consider a real scenario from our proof of concept — the guide schedule overwrite bug (NTK-10004):

**During the project, we captured:**

- 4 ERROR log entries with timestamps and trace IDs
- Root cause analysis: `SchedulingService.java` using `save(incoming)` instead of field-level merge
- A previously rejected MR (MR-5001) that attempted an insufficient fix
- 2 ADRs: PATCH semantics and optimistic locking with `_rev` field
- A 3-phase remediation plan

**After the fix ships:**

- Nobody verifies whether the developer actually implemented PATCH semantics as designed
- Nobody records what was *actually built* vs what was *designed*
- The ADRs sit in a ticket branch, never promoted to a searchable global log
- The next architect investigating a scheduling issue **starts from scratch**

This happens for **every project**. The specs in Git describe intended designs. Confluence (when updated at all) describes an older state. And the actual production code may differ from both.

---

## The Fix: PROMOTE

We've added a step that every architecture workflow was missing:

```
INTAKE → INVESTIGATE → DESIGN → BUILD → DEPLOY → PROMOTE → DONE
```

The PROMOTE step, executed by the same AI assistant that did the design work:

| Action | What It Does |
|--------|-------------|
| **Reconcile specs against reality** | Compares designed API contracts with actual implementation and records the true state |
| **Update OpenAPI specs** | Reflects what was *actually built*, not just what was designed |
| **Promote ADRs** | Copies ticket-level decisions to the global decision log with cross-references |
| **Refresh service pages** | Updates service architecture baselines with new integration points and current state |
| **Mark design as PROMOTED** | Adds date, version, and status to the solution design — closing the loop |
| **Trigger portal rebuild** | A `git push` publishes the updated baselines to the architecture portal |

---

## Why AI Makes This Possible

The PROMOTE step wasn't practical before AI assistance because it required:

1. Reading the solution design to understand what was intended
2. Comparing against actual production code or behavior to find deviations
3. Cross-referencing with current specs to identify what needs updating
4. Updating multiple files across the workspace consistently
5. Promoting ADRs from ticket branches to the global log

This is exactly the kind of work the AI excels at — reading context, cross-referencing files, identifying discrepancies, and producing consistent updates. And with Copilot's fixed pricing, the PROMOTE step adds **zero marginal cost**.

---

## Cost Impact

Adding the PROMOTE step increases the architecture practice's workload from 26 to 38 runs per month:

| | Without PROMOTE | With PROMOTE |
|---|:---:|:---:|
| Monthly runs | 26 | 38 |
| Copilot Pro+ cost | $39 | **$39** |
| OpenRouter cost | ~$347 | ~$507 |

<div class="key-insight" markdown>
**PROMOTE is free on Copilot.** The fixed subscription absorbs any additional runs. On per-token models, PROMOTE adds ~$160/month in variable costs — widening Copilot's cost advantage from 9x to 13x.
</div>

---

## The Compounding Value

Without PROMOTE, specs describe design intent but not reality:

```
Project 1:  Design A checked in  →  Built with deviations  →  Drift begins
Project 2:  Architect reads specs that may not match production  →  More drift
Project 3:  Three layers of design-vs-reality gap accumulated
```

With PROMOTE, each project records what was actually built:

```
Project 1:  Design A  →  Built  →  PROMOTED (actual state recorded)
Project 2:  Actual State 1  →  Design B  →  Built  →  PROMOTED
Project 3:  Accurate baseline  →  Confident design  →  Accurate result
```

After 10 projects, the architecture workspace contains a comprehensive picture of how the system **actually exists in production** — not just how it was designed. Every AI session benefits from this accumulated knowledge — at zero additional cost.

<div class="cta-box" markdown>

### What's the timeline?

[Roadmap: What Comes Next](roadmap.md)

</div>
