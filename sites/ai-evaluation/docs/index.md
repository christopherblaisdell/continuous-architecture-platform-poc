# AI Toolchain Evaluation

## Comparative Evaluation for Enterprise Architecture Work

This site documents the NovaTrek Adventures Continuous Architecture Platform's evaluation of AI toolchains for solution architecture workflows. Three toolchains were assessed using the same AI model (Claude Opus 4.6), the same synthetic workspace, and the same 5 architecture scenarios.

---

## Key Findings

| | GitHub Copilot Pro+ | Roo Code + OpenRouter | Claude Code |
|---|:---:|:---:|:---:|
| **Cost per run** | **$0.48** | ~$100 | Spike pending |
| **Monthly cost (38 runs)** | **$39** (fixed) | ~$507 (variable) | TBD |
| **Quality score** | **149/155 (96.1%)** | TBD (scoring pending) | TBD |
| **Per-run cost ratio** | **1x** | ~208x | TBD |
| **Infrastructure required** | None (SaaS) | Kong Gateway + vector DB | Terminal only |
| **Pricing model** | Fixed subscription | Pay-per-token | Pay-per-token |

!!! note "208x Cost Advantage"
    Using the same underlying AI model (Claude Opus 4.6), GitHub Copilot costs $0.48 per architecture run compared to ~$100 via OpenRouter. This difference is architectural, not promotional -- it stems from intent-based billing vs. token-based billing and server-side workspace indexing vs. client-side context accumulation.

---

## What Was Evaluated

Five representative architecture scenarios were executed against a fully synthetic workspace containing 19 microservice OpenAPI specs, Java source code, architecture decision records, and mock tool integrations:

| Scenario | What It Tests |
|----------|---------------|
| SC-01: Ticket Triage | Parse a ticket, classify architectural relevance, scaffold workspace |
| SC-02: Solution Design | Produce arc42-compliant designs with impacts, decisions, and diagrams |
| SC-03: Investigation | Analyze specs, source code, and logs to identify root causes |
| SC-04: Architecture Update | Modify OpenAPI specs and PlantUML diagrams per approved design |
| SC-05: Publishing Prep | Validate cross-references, formatting, and standards compliance |

Both Copilot and Roo Code completed all 5 scenarios, producing 37 files each with comparable structure. The critical differences emerged in cost, quality, and architectural reliability.

---

## Three Toolchains Compared

### GitHub Copilot Pro+ (Selected)

VS Code-integrated AI assistant with agent mode, workspace indexing, and flat-rate subscription billing. Deep GitHub ecosystem integration. Intent-based billing charges per user prompt only -- autonomous tool calls are free.

[GitHub Copilot Profile](tools/github-copilot.md){ .md-button }

### Roo Code + Kong AI Gateway

Open-source VS Code extension routing through Kong API Gateway to OpenRouter/AWS Bedrock. Pay-per-token billing with full cost transparency but exponential context accumulation costs. Three architectural limitations identified during evaluation.

[Roo Code + Kong Profile](tools/roo-code-kong.md){ .md-button }

### Claude Code (Spike Pending)

Anthropic's official CLI-based coding agent. Terminal-native with direct Anthropic API access. Evaluated as a potential complement or alternative based on the Everything Claude Code (ECC) community harness. A limited 1-2 scenario spike is planned to gather real cost and quality data.

[Claude Code Profile](tools/claude-code.md){ .md-button }

---

## How to Navigate This Site

| Section | What You Will Find |
|---------|-------------------|
| [Evaluation Framework](evaluation-framework.md) | Methodology, scoring rubrics, scenario definitions |
| [Tools](tools/github-copilot.md) | Per-tool profiles with architecture, pricing, strengths, and limitations |
| [Comparisons](comparisons/copilot-vs-roocode.md) | Head-to-head results with evidence from actual runs |
| [Research](research/copilot-billing.md) | Deep research findings on billing mechanics, gateway failures, context management |
| [Data Isolation](data-isolation.md) | How this evaluation uses zero corporate data |
| [Decision Log](decision-log.md) | ADR-001: the formal architecture decision record |

---

## Data Isolation Statement

This evaluation contains **zero corporate data**. The entire NovaTrek Adventures domain is fictional. All JIRA, Elasticsearch, and GitLab integrations are local mock Python scripts reading JSON files from disk -- no network calls, no credentials, no corporate system access. See [Data Isolation](data-isolation.md) for the full policy.
