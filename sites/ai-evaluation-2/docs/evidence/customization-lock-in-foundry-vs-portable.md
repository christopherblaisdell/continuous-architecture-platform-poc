<!-- CONFLUENCE-PUBLISH -->
<!-- CONFLUENCE-URL: -->

# Customization Lock-In: Foundry Native vs Portable Standards

!!! note "Context for This Analysis"
    This page examines what happens to AI customization investments if the team customizes directly within Azure AI Foundry or Foundry IQ versus maintaining customizations as portable files. It also introduces OpenSpec, an open-source framework that addresses cross-platform portability for AI agent customizations. This analysis is offered as input for the decision-makers — not as a directive.

## The Question

The existing analysis asks: [What Copilot investment could become a dead end?](foundry-iq-comparison.md#what-copilot-investment-could-become-a-dead-end) The answer is reassuring — mostly a reformatting cost, not a data loss.

But the inverse question has not been asked: **What happens to customization investments made directly in Azure AI Foundry or Foundry IQ if the team later needs to switch platforms?**

## Yes, Foundry-Native Customization Creates Lock-In

Customizing directly in Azure AI Foundry or Foundry IQ creates a qualitatively different kind of lock-in than customizing via portable files. The reason is structural: Foundry customizations are platform-specific configurations stored in Azure's control plane, not version-controlled files in a repository.

### What Gets Locked In

| Foundry Investment | Portable? | Why |
|--------------------|-----------|-----|
| **Knowledge base definitions** | No | Azure-specific constructs — knowledge source bindings, retrieval instructions, reasoning effort levels. No equivalent in other platforms. |
| **Scoring profiles and relevance tuning** | No | Azure AI Search-specific configuration (freshness functions, field weighting, boost rules). Would need to be re-created from scratch in any alternative search platform. |
| **Custom skillsets** (document cracking, enrichment) | No | Azure AI Search-specific pipeline definitions. Each skillset encodes domain-specific chunking logic (e.g., how to split PlantUML files) that has no portable representation. |
| **Agent definitions** (Foundry Agent Service) | No | Defined via Python SDK (`azure-ai-projects`) or REST API. Not AGENTS.md, not SKILL.md — Azure-proprietary format with no open standard equivalent. |
| **Integration code** (Python SDK, REST calls) | No | `azure-ai-projects` SDK, Foundry-specific connection types, `ProjectManagedIdentity` auth flows. None of this code transfers to another platform. |
| **RBAC and ACL configuration** | No | Azure Entra ID role assignments and ACL synchronization rules. Every alternative platform has its own authorization model. |
| **MCP endpoint wrappers** | Partial | MCP is an open standard, so the *protocol* is portable. But Foundry's MCP endpoints use `ProjectManagedIdentity` authentication — a Foundry-specific auth type that no IDE client natively supports. |
| **Content** (ADRs, specs, diagrams) | Always | Files in storage. Any platform can read them. |

### Contrast with Copilot Customization Lock-In

The [existing analysis](foundry-iq-comparison.md#what-copilot-investment-could-become-a-dead-end) established that Copilot's lock-in risk is a reformatting cost — the knowledge survives, only file naming changes. The contrast with Foundry is stark:

| Dimension | Copilot Lock-In | Foundry Lock-In |
|-----------|----------------|-----------------|
| **Where customizations live** | Markdown files in git | Azure control plane (portal, SDK, REST API) |
| **Version controlled by default?** | Yes — same git workflow as code | No — requires manual export or IaC discipline |
| **What survives a platform switch** | Content and knowledge (plain text) | Content only — all configuration must be rebuilt |
| **Migration effort** | Rename files, adjust syntax | Rebuild from scratch in new platform |
| **Who can modify** | Any team member with repo access | Users with Azure RBAC roles |
| **Diff and review changes** | Standard git pull request workflow | Azure Activity Log or custom auditing |
| **Cost of switching** | Hours (reformatting) | Weeks to months (re-architecture) |

The key insight: **Copilot lock-in is a formatting problem. Foundry lock-in is a rebuild problem.**

### Why This Matters for the Architecture Practice

The architecture practice's customizations are not trivial. The pilot produced over 1,100 lines of behavioral instructions, multiple scoped rule files, a custom agent definition, and skill packages — all encoding hard-won domain knowledge about service boundaries, data ownership rules, safety defaults, C4 diagram conventions, and workflow patterns.

If that knowledge were encoded in Foundry-native constructs (agent definitions via Python SDK, knowledge base retrieval instructions, custom skillsets), switching platforms would mean re-expressing all of it in whatever format the new platform requires — without the benefit of having it in portable, diffable Markdown files to work from.

## OpenSpec: A Cross-Platform Portability Layer

[OpenSpec](https://github.com/Fission-AI/OpenSpec) (by Fission AI, MIT license, 39.6k GitHub stars) is an open-source framework for spec-driven development that addresses this portability problem directly. It provides a tool-agnostic abstraction layer above the proprietary file conventions of individual AI coding platforms.

### How OpenSpec Works

OpenSpec maintains a single source of truth in an `openspec/` directory within the repository:

```
openspec/
├── specs/           # Behavioral specifications (tool-agnostic)
│   ├── auth/
│   │   └── spec.md
│   └── architecture/
│       └── spec.md
└── changes/         # Proposed modifications (delta-based)
    └── add-safety-defaults/
        ├── proposal.md
        ├── specs/
        ├── design.md
        └── tasks.md
```

When initialized, OpenSpec generates the native configuration files for whichever AI tools the team uses:

```bash
openspec init --tools github-copilot,cursor,roocode
```

This produces:

| Tool | Generated Files |
|------|----------------|
| GitHub Copilot | `.github/skills/openspec-*/SKILL.md`, `.github/prompts/opsx-*.prompt.md` |
| Cursor | `.cursor/skills/openspec-*/SKILL.md`, `.cursor/commands/opsx-*.md` |
| RooCode | `.roo/skills/openspec-*/SKILL.md`, `.roo/commands/opsx-*.md` |

Switching tools — or supporting multiple tools simultaneously — is a single command:

```bash
openspec init --tools claude,windsurf   # add new tools
openspec update                          # regenerate native files
```

### What OpenSpec Remediates (and What It Does Not)

| Risk | OpenSpec Remediation | Notes |
|------|---------------------|-------|
| **Customization format lock-in** | Full | Specs live in `openspec/` — tool-specific files are generated artifacts, not source of truth |
| **Behavioral knowledge portability** | Full | Domain rules, workflow conventions, and procedural knowledge are expressed in tool-agnostic Markdown specs |
| **Multi-tool support** | Full | 25+ supported tools including Copilot, Cursor, Windsurf, Claude Code, Cline, RooCode, Gemini CLI, Kiro, Amazon Q |
| **Knowledge base configuration lock-in** | None | OpenSpec does not address retrieval infrastructure — scoring profiles, chunking skillsets, and knowledge base bindings remain platform-specific |
| **Infrastructure lock-in** (Azure AI Search, Entra ID) | None | Infrastructure decisions are outside OpenSpec's scope |

OpenSpec addresses the **customization portability** problem specifically. It does not solve the **infrastructure lock-in** problem that comes with Foundry IQ's retrieval layer. These are separate risks that require separate mitigations.

### OpenSpec vs the Current Copilot Approach

The pilot already maintains customizations as portable Markdown files. The question is whether OpenSpec adds value beyond what the current approach provides:

| Capability | Current Copilot Approach | With OpenSpec |
|------------|------------------------|---------------|
| **Portability** | High — Markdown files converging on open standards (AGENTS.md, SKILL.md) | Higher — tool-agnostic source with automated generation for any target tool |
| **Multi-tool support** | Manual — rename/restructure files per tool's convention | Automated — `openspec init --tools` generates native files for 25+ tools |
| **Spec-driven workflow** | Not structured — instructions are freeform behavioral guidance | Structured — requirements, scenarios, Given/When/Then format, delta-based changes |
| **Change tracking** | Git history on instruction files | Git history + structured change proposals with proposal/design/tasks artifacts |
| **Learning curve** | None — just write Markdown | Moderate — learn OpenSpec's spec format, commands, and artifact workflow |
| **Overhead** | None | CLI installation, `openspec init/update` maintenance, generated file management |

## Suggested Assessment

The lock-in risk from Foundry-native customization appears significantly higher than from Copilot-native customization:

1. **Foundry customizations are a rebuild problem.** Knowledge base definitions, scoring profiles, agent definitions via SDK, and integration code are all Azure-specific. Switching platforms means re-creating this work from scratch — not reformatting files.

2. **Copilot customizations are a reformatting problem.** Instruction files, skills, and agent definitions are Markdown files in git. The content (domain knowledge, behavioral rules, workflow conventions) survives a platform switch. Only file naming and activation syntax change.

3. **OpenSpec could further reduce the reformatting cost** by providing a tool-agnostic source of truth with automated generation for 25+ platforms. If multi-platform portability or simultaneous multi-tool support becomes a requirement, OpenSpec offers a structured way to achieve it without maintaining parallel customization files manually.

4. **For the current pilot scope**, the existing Copilot customization approach already provides strong portability. The open standards convergence around AGENTS.md and SKILL.md is shrinking the reformatting cost organically. OpenSpec would add the most value if the practice needs to support multiple AI tools simultaneously or if the team anticipates frequent tool switching.

5. **If Foundry IQ is adopted for retrieval**, the analysis suggests keeping it as a retrieval-only layer and maintaining all behavioral customizations (instructions, skills, agent definitions) as portable Markdown files — whether in the current Copilot-native format or via OpenSpec. This separates the retrieval infrastructure investment (which is inherently platform-specific) from the customization knowledge investment (which can and should remain portable).

## Relationship to Other Pages

- [What Does Foundry IQ Actually Require?](foundry-iq-comparison.md) — Covers the operational requirements and "buy vs build" framing. That page asks what Copilot investment could become a dead end; this page asks the inverse for Foundry.
- [Customization Extensibility and Governance](customization-extensibility-governance.md) — Discusses who owns customizations and how they evolve. This page adds the platform portability dimension: even if governance is solved, customizations locked in a proprietary format create a different kind of risk.
- [Build vs Leverage](build-vs-leverage.md) — Analyzes custom RAG vs native platform capabilities. The lock-in risk identified here reinforces the "leverage" argument: platform-native customization formats carry less lock-in risk than custom-built alternatives.
- [DD-06: IDE Client Selection](../decisions/dd-06-ide-client-selection.md) — Evaluates the frozen customization problem from a model perspective. This page extends the analysis to the platform format level.

## Sources

- [OpenSpec — GitHub Repository](https://github.com/Fission-AI/OpenSpec) — Fission AI, MIT license, v1.3.0, 39.6k stars
- [OpenSpec Supported Tools](https://github.com/Fission-AI/OpenSpec/blob/main/docs/supported-tools.md) — Full list of 25+ supported AI coding assistants
- [OpenSpec Concepts](https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md) — Architecture and philosophy documentation
- [Agent Skills Specification](https://agentskills.io) — Open standard for SKILL.md format
- [AGENTS.md Standard](https://github.com/agentsmd/agents.md) — Cross-platform agent metadata standard
