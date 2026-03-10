# Continuous Architecture — Closing the Loop

## From Design-and-Forget to Design-Build-Verify-Publish

<div class="hero-grid" markdown>

<div class="hero-card" markdown>
<div class="metric">0%</div>
<div class="label">of architecture knowledge reconciled after deployment today</div>
</div>

<div class="hero-card accent" markdown>
<div class="metric">301</div>
<div class="label">Architecture artifacts auto-published from a single git push</div>
</div>

<div class="hero-card dark" markdown>
<div class="metric">$0</div>
<div class="label">Publishing infrastructure cost (MkDocs + Azure Free Tier)</div>
</div>

</div>

---

## The Vision in 60 Seconds

Architecture practices already gate production deployments through version-controlled specs. But two gaps compound with every project: **browsable documentation falls behind** because manual wiki updates get skipped, and **design intent diverges from production reality** because nobody reconciles the difference after deployment.

The **Continuous Architecture Platform** closes both gaps — replacing the manual wiki step with automated publishing, and adding a **PROMOTE step** that verifies what was built matches what was designed. The result: architecture knowledge that stays current, searchable, and trustworthy.

<div class="key-insight" markdown>
**This is not theoretical.** A live architecture portal with 301 auto-published artifacts demonstrates the publishing pipeline. The PROMOTE step and CALM integration are designed and ready for Phase 2 implementation.
</div>

---

## What This Presentation Covers

| Section | Question It Answers |
|---------|-------------------|
| [The Problem](the-problem.md) | Why does architecture knowledge decay after every project? |
| [Markdown-First](markdown-first.md) | How do we extend our Git-first practice beyond specs? |
| [Automated Publishing](publishing-pipeline.md) | How do we replace the manual Confluence step? |
| [Closing the Loop](closing-the-loop.md) | What's the PROMOTE step and why does it matter? |
| [CALM Integration](calm-integration.md) | How does CALM formalize our architecture topology? |
| [Roadmap](roadmap.md) | What comes next? |

---

<div class="key-insight" markdown>
**See also:** [AI-Assisted Architecture](https://ai.novatrek.cc) — the companion presentation on how AI powers the architecture workflows at 208x lower cost.
</div>
