# The Problem: Architecture Knowledge Decays After Every Project

## Two Gaps That Compound Over Time

Many architecture practices have achieved what most organizations struggle with: **OpenAPI specs source-controlled, diagram source files version-controlled, production changes gated through an architecture repository.** This is a strong foundation. But two critical gaps erode its value with every project.

---

## Gap 1: Browsable Documentation Falls Behind

Architects update specs and diagrams in version control. Then they are *supposed to* update the wiki pages that stakeholders actually browse. Sometimes they do. Often they don't.

The result: **the artifacts in version control are current, but the documentation people consult is not.**

| What's Source-Controlled (Current) | What's Manual and Voluntary (Falls Behind) |
|-----------------------------------|-------------------------------------------|
| OpenAPI/Swagger specs (gated) | Wiki service pages |
| Diagram source files (PlantUML, etc.) | Rendered diagram updates in wiki |
| Cross-service dependency mappings | Interactive navigation and linking |
| Architecture decision rationale (in branches) | ADR promotion to a discoverable global log |

<div class="key-insight" markdown>
**The artifacts are current in version control. The documentation that people actually browse is not.**
</div>

---

## Gap 2: Design Intent Diverges from Production Reality

Architecture designs describe **intent** — how a solution *should* be built. But developers sometimes deviate during implementation. When that happens:

- The spec in Git reflects the **approved design**, not the actual production behavior
- Nobody goes back to update the architecture artifacts to reflect what was **actually built**
- The next architect finds artifacts that describe a version of the system that **may never have existed in production**

<div class="big-number red">0%</div>

**of architecture knowledge is reconciled against reality after deployment.**

This isn't a discipline failure — it's a structural one. There is no step in the workflow for it.

---

## The Compounding Effect

These two gaps compound with every project:

```
Project 1:  Design A checked in  →  Implemented (with deviations)
                                      Wiki NOT updated
                                      Deviations NOT recorded

Project 2:  Architect reads stale wiki + specs that may not match reality
            Re-investigates from source code + tribal knowledge
            Designs B  →  Implemented (with deviations)

Project 3:  THREE layers of drift have accumulated
            Wiki still reflects a pre-Project-1 state
            Specs show designed intent (not reality) from Projects 1 and 2
```

By Project 5, finding the **actual current state** of a service requires reading production source code, interviewing developers, and guessing at which artifacts are still accurate.

---

## What It Costs

| Hidden Cost | Impact |
|------------|--------|
| Re-investigation | Architects re-read source code because wiki pages are stale |
| Stale browsable docs | Stakeholders consult wiki pages that no longer reflect the current state |
| Lost decisions | ADRs stay in ticket branches, never promoted to a searchable global log |
| Knowledge silos | The architect who did the last project is the only one who knows what changed |
| Design-reality gap | Specs describe intended design, not necessarily what was built |

The Continuous Architecture Platform closes both gaps — automated publishing eliminates Gap 1, and the PROMOTE step eliminates Gap 2.

<div class="cta-box" markdown>

### How do we extend what we already do?

[Markdown-First: Extending Our Git-First Practice](markdown-first.md)

</div>
