# Continuous Architecture Platform

Welcome to the **Continuous Architecture Platform** documentation — the living architecture knowledge base for NovaTrek Adventures.

## What Is This?

This platform replaces point-in-time architecture documentation with **living, interconnected architecture artifacts** powered by AI-assisted workflows.

All content is authored in Markdown, stored in Git, and published automatically on every push to `main`.

## Quick Navigation

| Section | Description |
|---------|-------------|
| **[Decisions](decisions/README.md)** | Architecture Decision Records (ADR-001 through ADR-011) |
| **[Phase 1](phase-1-ai-tool-cost-comparison/AI-TOOL-COST-COMPARISON-PLAN.md)** | AI toolchain cost and quality comparison (Copilot vs Roo Code) |
| **[Roadmap](roadmap/ROADMAP.md)** | Phased delivery plan from Phase 1 through Phase 6 |
| **[Research](research/CONTEXT-WINDOW-UTILIZATION-ANALYSIS.md)** | Deep research findings on AI tooling and billing |

## Architecture at a Glance

NovaTrek Adventures operates **19 microservices** across 10 bounded contexts:

- **Operations**: svc-check-in, svc-scheduling-orchestrator
- **Guest Identity**: svc-guest-profiles
- **Booking**: svc-reservations
- **Product Catalog**: svc-trip-catalog, svc-trail-management
- And 13 more supporting services

## How This Site Is Built

This documentation site is built with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) and deployed to [Azure Static Web Apps](https://learn.microsoft.com/en-us/azure/static-web-apps/) via GitHub Actions. See [ADR-002](decisions/ADR-002-documentation-publishing-platform.md) for the platform selection rationale.

!!! info "Data Isolation"
    This workspace contains **zero corporate data**. The entire NovaTrek Adventures domain is fictional. All JIRA, Elasticsearch, and GitLab integrations are local mock Python scripts reading JSON files — no network calls, no credentials.
