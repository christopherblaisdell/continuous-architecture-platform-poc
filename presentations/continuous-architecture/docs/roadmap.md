# Roadmap: Six Phases to Full Platform

## Standalone Value at Every Phase

The Continuous Architecture Platform is delivered in six phases. Each phase delivers independent value — you can stop at any phase and still have a working, useful system. The full vision completes by August 2026.

---

## Timeline

<div class="timeline" markdown>

<div class="timeline-item completed" markdown>

### Phase 1: AI Toolchain Comparison — COMPLETE

**March 2026**

Compared GitHub Copilot Pro+ against Roo Code + OpenRouter across 5 architecture scenarios. Established cost advantage (208x per-run) and output completeness. Produced ADR-001 recommending Copilot Pro+.

**Delivered:** Cost comparison data, output analysis, billing model research, toolchain recommendation.

</div>

<div class="timeline-item completed" markdown>

### Phase 6: Documentation Publishing — COMPLETE

**March 2026** (accelerated from original timeline)

Built the NovaTrek Architecture Portal using MkDocs Material on Azure Static Web Apps. Generated 19 microservice pages, 184 SVG diagrams, 19 Swagger UI pages, enterprise C4 with PCI compliance zone.

**Delivered:** Live architecture portal with automated publishing pipeline.

</div>

<div class="timeline-item" markdown>

### Phase 2: AI-Integrated Workflow Design

**April - May 2026**

Formalize the AI-assisted architecture workflow into repeatable playbooks. Add the PROMOTE step as a standard workflow phase. Create scenario-specific execution prompts for common architecture tasks.

**Will deliver:** Standardized AI workflows, PROMOTE playbook, execution prompt library, workflow documentation.

</div>

<div class="timeline-item" markdown>

### Phase 3: Pipeline Integration

**May - June 2026**

Integrate architecture validation gates into CI/CD pipelines. Automated checks for: spec completeness, ADR format compliance, cross-service consistency, link integrity.

**Will deliver:** GitHub Actions workflows, validation scripts, quality gates, automated spec linting.

</div>

<div class="timeline-item" markdown>

### Phase 4: Navigable Artifact Graph

**June - July 2026**

Build bidirectional traceability between all architecture artifacts. From any ADR, navigate to the ticket, solution design, impacted specs, and service pages. From any service page, find all ADRs and designs that modified it.

**Will deliver:** Artifact graph data model, navigation UI, backlink generation, traceability reports.

</div>

<div class="timeline-item" markdown>

### Phase 5: Continuous Improvement Loop

**July - August 2026**

Measure and improve the platform's effectiveness. Track quality scores over time, identify recurring patterns, optimize AI instructions based on actual usage data.

**Will deliver:** Quality metrics dashboard, improvement recommendations, optimized instruction sets, adoption metrics.

</div>

</div>

---

## What's Already Proven vs What's Planned

| Capability | Status | Phase |
|-----------|:------:|:-----:|
| AI produces complete architecture artifacts | **Proven** | 1 |
| Copilot is 208x cheaper per run | **Proven** | 1 |
| MkDocs publishes 301 artifacts automatically | **Proven** | 6 |
| PCI compliance zones in architecture diagrams | **Proven** | 6 |
| Clickable C4 diagrams with drill-down navigation | **Proven** | 6 |
| Interactive Swagger UI for every service | **Proven** | 6 |
| PROMOTE step closes the documentation loop | **Designed** | 2 |
| CI/CD validation gates for architecture quality | Planned | 3 |
| Bidirectional artifact traceability | Planned | 4 |
| Quality metrics and continuous improvement | Planned | 5 |

---

## Risk Profile

| Risk | Mitigation |
|------|-----------|
| AI quality degrades on new scenario types | Phase 5 monitors quality scores and tunes instructions |
| Architects resist Markdown-first authoring | Phase 2 provides guided workflows; AI handles formatting |
| Copilot pricing changes | Current plan is $39/month; even at 2x would be cheaper than alternatives |
| Azure Static Web Apps limits | Free tier supports 100GB bandwidth; upgrade to Standard ($9/mo) if needed |
| Confluence sync complexity | Phase 3 includes Confluence API integration as optional pipeline step |

<div class="cta-box" markdown>

### See the AI companion presentation

[AI-Assisted Architecture — The Case for Copilot](https://ai.novatrek.cc)

</div>
