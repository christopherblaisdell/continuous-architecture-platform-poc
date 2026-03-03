# Copilot Instructions for Continuous Architecture Platform POC

## Data Isolation — READ FIRST

**This repository contains ZERO corporate data.** Everything is synthetic.

- The entire **NovaTrek Adventures** domain is fictional — services, tickets, logs, architecture decisions, and all supporting data
- JIRA, Elasticsearch, and GitLab integrations are **local mock Python scripts** that read JSON files from disk — no network calls, no credentials, no corporate system access
- Mock scripts use **Python stdlib only** (no `requests`, no API clients, no external dependencies)
- All 19 microservice OpenAPI specs and Java source code are synthetic
- Architecture decisions (ADR-003 through ADR-011) describe synthetic services only

### Rules for All AI Interactions

1. **Never imply real corporate connections.** When referencing JIRA, Elastic, or GitLab tools, always clarify they are local mock scripts
2. **Never fabricate data.** Only use data returned by the mock scripts or present in workspace files
3. **Never introduce corporate identifiers.** Run `./scripts/audit-data-isolation.sh` to verify before committing
4. **Always use the NovaTrek Adventures domain** for any new synthetic data

## Repository Purpose

This is a proof of concept for a **Continuous Architecture Platform** — replacing point-in-time documentation with living, interconnected architecture artifacts powered by AI-assisted workflows.

### Phase 1 (Current)

Compare AI toolchains (GitHub Copilot vs Roo Code + Kong AI) by executing 5 architecture scenarios against a synthetic workspace. The mock tools simulate the corporate tool environment so the AI agent's behavior can be evaluated realistically without any corporate data exposure.

### Key Locations

| Path | Purpose |
|------|---------|
| `decisions/` | Global architecture decision log (11 ADRs) |
| `services/` | Service architecture baseline pages (6 services) |
| `phase-1-ai-tool-cost-comparison/workspace/` | Synthetic workspace for Phase 1 evaluation (reset between runs) |
| `phase-1-ai-tool-cost-comparison/workspace/scripts/` | Mock JIRA, Elastic, GitLab tools (local JSON, no network) |
| `phase-1-ai-tool-cost-comparison/outputs/` | Run-by-run results for Copilot and Roo Code executions |
| `phase-1-ai-tool-cost-comparison/scripts/capture-run.sh` | Script to snapshot workspace into outputs after a run |
| `scripts/audit-data-isolation.sh` | Pre-commit audit for corporate data leakage |
| `roadmap/ROADMAP.md` | Phased delivery roadmap |
