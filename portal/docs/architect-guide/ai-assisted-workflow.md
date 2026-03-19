# AI-Assisted Architecture Workflow

This platform is designed for AI-assisted architecture work. This page covers how to use GitHub Copilot effectively and how the workspace is configured to support AI workflows.

---

## How AI Fits In

The AI agent acts as an accelerator for the solution architect — not a replacement. The agent can:

- **Research** — query mock tools (JIRA, Elastic, GitLab), read specs and source code, search for prior art
- **Analyze** — identify anti-patterns, trace data flows, cross-reference specs with source code
- **Draft** — produce solution designs, impact assessments, decisions, and user stories
- **Generate** — rebuild portal pages, render diagrams, validate CALM topology
- **Publish** — commit, push, build, and deploy the portal

The architect provides direction, reviews output, and makes final decisions. The agent handles the mechanical work.

---

## Workspace Configuration

The workspace is pre-configured for AI-assisted work through several customization layers:

### Copilot Instructions (`.github/copilot-instructions.md`)

This file tells the AI agent everything about its role, the domain model, mock tools, solution design workflow, architecture standards, and documentation rules. It is loaded automatically into every Copilot session.

Key sections the agent follows:

- **Role Definition** — the agent operates as a Solution Architect
- **Mock Tool Usage** — how to query JIRA, Elastic, and GitLab (local Python scripts)
- **Solution Design Workflow** — branching, folder structure, capability rollup
- **Architecture Standards** — MADR, C4, arc42, ISO 25010
- **Document Formatting Rules** — no emojis, no unvalidated claims, evidence-based
- **Anti-Patterns** — what to flag in existing architecture

### AI Agent Capabilities

The agent can run terminal commands, read and edit files, search the codebase, and manage tasks. Common operations:

```bash
# Query tickets
python3 scripts/ticket-client.py --list --capability CAP-2.1

# Check production logs
python3 scripts/mock-elastic-searcher.py --service svc-check-in --level ERROR

# Review recent changes
python3 scripts/mock-gitlab-client.py --project svc-check-in --mrs

# Regenerate portal
bash portal/scripts/generate-all.sh

# Deploy portal
cd portal && npx swa deploy site --deployment-token "<token>" --env production
```

---

## Working with the AI Agent

### Research Mode

When investigating a ticket or analyzing architecture, the agent follows a structured research process:

1. **JIRA first** — get the authoritative ticket description
2. **Elastic second** — check production logs for symptoms and usage data
3. **GitLab third** — review recent merge requests for related changes
4. **Specs and source** — read OpenAPI specs and Java source to understand current behavior
5. **Prior art** — search existing solutions, capability history, and ADRs

### Design Mode

When creating a solution design:

1. The agent creates the branch and folder structure
2. Populates each section following the template
3. Records capability changes in the changelog
4. Generates portal pages
5. Commits, pushes, and deploys

### Review Mode

The agent can review existing designs against the architecture review checklist, checking for:

- Data ownership violations
- Missing ADRs for cross-boundary decisions
- Anti-patterns in proposed changes
- Backward compatibility issues
- Missing quality attribute analysis

---

## Copilot Customization Deep Dive

For a detailed reference on GitHub Copilot's customization primitives, see the [Copilot Customization Guide](../github-copilot-customization-guide.md). It covers:

- The 6 customization primitives (workspace instructions, file instructions, prompts, agents, skills, hooks)
- Decision matrix for choosing primitives
- Tool restrictions and permissions
- Troubleshooting

For a comparison with OpenSpec (an alternative AI workflow framework), see [Copilot vs OpenSpec](../copilot-vs-openspec-comparison.md).

---

## Data Isolation

!!! warning "Synthetic Data Only"
    This workspace contains ZERO corporate data. Everything is synthetic — the NovaTrek Adventures domain, all services, tickets, logs, and architecture decisions are fictional.

### Mock Tools

JIRA, Elasticsearch, and GitLab integrations are **local mock Python scripts** that read JSON files from disk. No network calls, no credentials, no corporate system access.

| Tool | Script | Data Source |
|------|--------|-------------|
| JIRA | `scripts/mock-jira-client.py` | `scripts/mock-data/jira-tickets.json` |
| Elastic | `scripts/mock-elastic-searcher.py` | `scripts/mock-data/elastic-logs.json` |
| GitLab | `scripts/mock-gitlab-client.py` | `scripts/mock-data/gitlab-mrs.json` |

### Isolation Rules

1. Never imply real corporate connections
2. Never fabricate data — only use what mock tools or workspace files return
3. Never introduce corporate identifiers
4. Always use the NovaTrek Adventures domain for new synthetic data
5. Never generate fake URLs that resolve to real domains — use `*.novatrek.example.com`
6. Run `./portal/scripts/utilities/audit-data-isolation.sh` to verify before committing

---

## Cost Awareness

### GitHub Copilot Billing

Copilot bills per **user prompt**, not per model invocation. In Agent Mode, the autonomous loop (tool calls, file reads, terminal commands) is free — only your typed prompts consume premium requests.

| Model | Multiplier | Cost per Prompt |
|-------|-----------|----------------|
| GPT-4.1, GPT-4o | 0x | Free (unlimited) |
| Claude Opus 4.6 | 3x | $0.12 |
| Claude Opus 4.6 fast | 30x | $1.20 |

**Implication**: Longer, more detailed prompts are more cost-effective than many short ones. Front-load context in your prompt to minimize back-and-forth.

---

## Search-First Principle

Before creating new designs, always search for existing solutions:

1. Check `architecture/solutions/` for prior art
2. Run `python3 scripts/ticket-client.py --list --capability CAP-X.Y` for capability history
3. Review `architecture/metadata/capability-changelog.yaml` for L3 changes
4. Reference existing ADRs in `decisions/` — do not re-decide settled questions

Only create new artifacts when no existing solution covers the need.
