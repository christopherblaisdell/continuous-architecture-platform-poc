# Closing the Loop: The PROMOTE Step

## The Innovation That Makes Architecture Continuous

Every architecture practice in the world has the same gap: projects produce high-quality design artifacts, then abandon them after deployment. The target state becomes reality — but nobody records it as the new baseline.

**We identified this gap. We designed the fix. And we've proven the AI can automate it.**

---

## The Gap

Our Phase 1 execution produced 9 Architecture Decision Records across 5 scenarios. Here's what happened to them:

| Metric | Count |
|--------|:-----:|
| ADRs created during projects | 9 |
| ADRs promoted to global decision log | 0 |
| Service architecture pages updated | 0 |
| Solution designs marked as "promoted" | 0 |
| Swagger specs linked back to the design that drove them | 0 |

<div class="big-number red">0%</div>

**of architecture knowledge produced during projects was promoted to the corporate baseline.**

This isn't unique to us. It's industry-wide. Architecture practices invest heavily in the "design" step and completely skip the "record the result" step.

---

## What Gets Lost

Consider a real scenario from our proof of concept — the guide schedule overwrite bug (NTK-10004):

**During the project, we captured:**

- 4 ERROR log entries with timestamps and trace IDs
- Root cause analysis: `SchedulingService.java` using `save(incoming)` instead of field-level merge
- A previously rejected MR (MR-5001) that attempted an insufficient fix
- 2 ADRs: PATCH semantics and optimistic locking with `_rev` field
- A 3-phase remediation plan

**After the fix ships:**

- Nobody records that the scheduling service now uses PATCH semantics with optimistic locking
- The next architect investigating a scheduling issue **starts from scratch**
- The ADRs sit in a ticket folder, never indexed, never searchable

This happens for **every project**. Multiply by 26 architecture efforts per month, and the knowledge destruction is enormous.

---

## The Fix: PROMOTE

We've added a step that every architecture workflow was missing:

```
INTAKE → INVESTIGATE → DESIGN → BUILD → DEPLOY → PROMOTE → DONE
```

The PROMOTE step, executed by the same AI assistant that did the design work:

| Action | What It Does |
|--------|-------------|
| **Update OpenAPI specs** | Reflects implemented changes in the authoritative API contracts |
| **Promote ADRs** | Copies ticket-level decisions to the global decision log with cross-references |
| **Refresh service pages** | Updates service architecture baselines with new integration points and current state |
| **Mark design as PROMOTED** | Adds date, version, and status to the solution design — closing the loop |
| **Trigger portal rebuild** | A `git push` publishes the updated baselines to the architecture portal |

---

## Why AI Makes This Possible

The PROMOTE step wasn't practical before AI assistance because it required:

1. Reading the solution design to understand what changed
2. Cross-referencing with current Swagger specs to identify what needs updating
3. Updating multiple files across the workspace
4. Maintaining consistency across ADRs, service pages, and specs

This is exactly the kind of work the AI excels at — reading context, cross-referencing files, and producing consistent updates. And with Copilot's fixed pricing, the PROMOTE step adds **zero marginal cost**.

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

Without PROMOTE, each project starts from zero context:

```
Project 1:  State A → State B   (designed, shipped, forgotten)
Project 2:  ??? → State C       (re-investigate from scratch)
Project 3:  ??? → State D       (compounding uncertainty)
```

With PROMOTE, each project builds on the last:

```
Project 1:  State A → State B   (designed, shipped, PROMOTED)
Project 2:  State B → State C   (full context from previous PROMOTE)
Project 3:  State C → State D   (rich baseline, accurate analysis)
```

After 10 projects, the architecture workspace contains a comprehensive, accurate, up-to-date picture of the system. Every AI session benefits from this accumulated knowledge — at zero additional cost.

<div class="cta-box" markdown>

### What's the timeline?

[Roadmap: What Comes Next](roadmap.md)

</div>
