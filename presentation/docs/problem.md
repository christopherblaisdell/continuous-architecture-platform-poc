# The Problem: The Last Mile of Architecture Documentation

## Many Teams Already Do the Hard Part

Many architecture practices have achieved what most organizations struggle with:

- **OpenAPI specs are source-controlled** in a central repository
- **Diagram source files** (PlantUML, Mermaid, etc.) are version-controlled alongside specs
- **Production gating** — no API changes ship without approval in the architecture repo
- Architects work from authoritative, version-controlled artifacts

This is a strong foundation. But two critical gaps erode its value over time.

---

## Gap 1: Browsable Documentation Is Manual and Voluntary

Most teams maintain wiki pages for each microservice — the browsable reference that architects, developers, and stakeholders consult when they need to understand a service.

**Updating those pages is often voluntary and gets skipped.**

1. An architect designs a solution, updates specs and diagrams
2. Changes are checked into the architecture repository (the gate works)
3. The architect is *supposed to* update the wiki pages
4. Sometimes they do. Often they don't.

The result: **Browsable documentation falls behind the source-controlled artifacts.** When the next architect assesses the current state of a service, the wiki pages may reflect a state from two or three projects ago.

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

## Gap 2: Design Intent vs Production Reality

Architecture designs describe **intent** — how a solution *should* be built. But developers sometimes deviate from the design during implementation. When that happens:

- The spec in Git reflects the **approved design**, not the actual production behavior
- Nobody goes back to update the architecture artifacts to reflect what was **actually built**
- The next architect finds artifacts that describe a version of the system that **may never have existed in production**

There is no step in the current workflow that compares what was designed against what was deployed and reconciles the difference.

<div class="big-number red">0%</div>

**of architecture knowledge is reconciled against reality after deployment.**

---

## The Compounding Effect

These two gaps compound with every project:

```
Project 1:  Design A checked in  →  Implemented (with deviations)
                                      Confluence NOT updated
                                      Deviations NOT recorded

Project 2:  Architect reads stale Confluence + specs that may not match reality
            Re-investigates from source code + tribal knowledge
            Designs B  →  Implemented (with deviations)

Project 3:  THREE layers of drift have accumulated
            Confluence still reflects a pre-Project-1 state
            Specs show designed intent (not reality) from Projects 1 and 2
```

By Project 5, finding the **actual current state** of a service requires reading production source code, interviewing developers, and guessing at which artifacts are still accurate. The source-controlled specs — which should be the authoritative baseline — describe what was *designed*, not necessarily what *exists*.

---

## What It Costs

Production gating gives teams authoritative API contracts at design time. But the **documentation people actually browse** — wiki pages, rendered diagrams, the searchable service catalog — falls further behind with every project.

| Hidden Cost | Impact |
|------------|--------|
| Re-investigation | Architects re-read source code because wiki pages are stale |
| Stale browsable docs | Stakeholders consult wiki pages that no longer reflect the current state |
| Lost decisions | ADRs stay in ticket branches, never promoted to a searchable global log |
| Knowledge silos | The architect who did the last project is the only one who knows what changed |
| Design-reality gap | Specs describe intended design, not necessarily what was built and deployed |

The platform demonstrated here solves every one of these problems — building on the version-controlled foundation that already exists.

<div class="cta-box" markdown>

### Ready to see the solution?

[The Solution: Continuous Architecture Platform](solution.md)

</div>
