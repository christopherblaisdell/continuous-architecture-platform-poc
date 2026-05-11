# Azure AI Foundry Customization Guide

<!-- PUBLISH -->

Azure AI Foundry is a cloud-hosted platform for deploying and running AI agents. Unlike VS Code Copilot — which discovers customization files from the local filesystem — Foundry agents receive their instructions, prompts, agents, and skills through deployment-time configuration and server-side code. This guide documents every intake mechanism and maps them to the equivalent OpenSpec concepts.

---

## Quick Reference

| OpenSpec Category | Foundry Mechanism | Where It Lives |
|---|---|---|
| `instructions/` | System prompt | `agent.yaml` `instructions:` field, or a file loaded at agent startup |
| `prompts/` | Prompt templates | Foundry Prompt Management (portal/SDK) or template strings in agent code |
| `agents/` | Deployment configuration | `.foundry/agent-metadata.yaml` per environment |
| `skills/` | MCP tool definitions | `agent.yaml` `tools:` block or Agent Framework tool registration |

---

## Key Difference from Local AI Assistants

VS Code Copilot discovers customization files by scanning the local filesystem (`copilot-instructions.md`, `*.instructions.md`, `*.prompt.md`, etc.) at the start of each session. Changes take effect immediately with no deployment step.

Foundry agents have no file-discovery mechanism. Every customization is either:

- Embedded in the agent's **system prompt** (static, set at deployment)
- Provided by a **connected MCP server** (dynamic, called at runtime)
- Stored in **Foundry Prompt Management** and fetched via SDK at startup

A deployment step is always required to push changes to a running Foundry agent.

---

## 1. Instructions

### What it is

The system prompt — always-on context that shapes the agent's persona, domain knowledge, and behavioral rules. Equivalent to `copilot-instructions.md` in Copilot or `core-instructions.md` in OpenSpec.

### Prompt agents (LLM-based, no custom code)

System prompt is declared directly in `agent.yaml` and deployed via the Foundry MCP `agent_update` tool:

```yaml
# agent.yaml
type: prompt
model: gpt-4o
instructions: |
  You are a NovaTrek Solution Architect. Your responsibilities are:
  - Assess architectural relevance of tickets
  - Produce MADR-formatted architecture decision records
  ...
```

### Hosted agents (containerized code)

System prompt is a string in Python or C# source code. Best practice is to load it from a file at startup so it can be maintained separately:

```python
# agent.py
import os
from agent_framework import Agent

instructions = open("system-prompt.md").read()
# Or from environment variable: os.environ["SYSTEM_PROMPT"]

agent = Agent(
    model=model_client,
    instructions=instructions,
)
```

The `system-prompt.md` file is bundled into the container image at build time, or injected via environment variable from Azure Key Vault at runtime.

### What OpenSpec generates for this

The `generate_foundry()` function in `generate-tool-instructions.py` would extract content from `.openspec/instructions/core-instructions.md` and write it to `.foundry/system-prompt.md` for use by hosted agents, or inline it into a generated `agent.yaml` for prompt agents.

---

## 2. Prompts

### What it is

Reusable input templates the agent can use when invoked. Equivalent to `.github/prompts/*.prompt.md` slash commands in Copilot.

### Foundry Prompt Management

Foundry has a built-in prompt catalog hosted in the project. Templates are versioned, tagged, and fetched via the Azure AI Projects SDK at agent startup or on-demand:

```python
from azure.ai.projects import AIProjectClient

client = AIProjectClient(endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"])
template = client.prompts.get("architecture-review", version="latest")
rendered = template.render(ticket_id="NTK-10007", service="svc-check-in")
```

Templates in Foundry Prompt Management are uploaded via the portal or SDK — they are not auto-discovered from local files.

### Embedded templates

For simpler agents, prompt templates are Python f-strings or Jinja2 templates embedded in source code:

```python
ARCHITECTURE_REVIEW_TEMPLATE = """
Review the following ticket and identify all affected services.
Ticket: {ticket_id}
Description: {description}
"""
```

### What OpenSpec generates for this

`.openspec/prompts/*.prompt.md` files would be bundled into the container as named template files, or uploaded to Foundry Prompt Management as a pre-deployment step.

---

## 3. Agents

### What it is

Deployment configuration — which project endpoint, which ACR registry, which agent name, per environment. Equivalent to `.github/agents/*.agent.md` definitions in Copilot, but focused on infrastructure rather than persona.

### `.foundry/agent-metadata.yaml`

Every Foundry agent source folder contains a `.foundry/` directory with a metadata file that records environments, container registry, and evaluation suites:

```yaml
# .foundry/agent-metadata.yaml
defaultEnvironment: dev
environments:
  dev:
    projectEndpoint: https://contoso.services.ai.azure.com/api/projects/novatrek-dev
    agentName: novatrek-solution-architect-dev
    azureContainerRegistry: contosoregistry.azurecr.io
    observability:
      applicationInsightsResourceId: /subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.Insights/components/novatrek-dev-ai
    evaluationSuites:
      - id: smoke-core
        tags:
          tier: smoke
        dataset: novatrek-arch-eval-seed
        datasetVersion: v1
        evaluators:
          - name: task_adherence
            threshold: 4
```

For production, a sidecar file isolates that environment:

```yaml
# .foundry/agent-metadata.prod.yaml
defaultEnvironment: prod
environments:
  prod:
    projectEndpoint: https://contoso.services.ai.azure.com/api/projects/novatrek-prod
    agentName: novatrek-solution-architect-prod
    azureContainerRegistry: contosoregistry.azurecr.io
```

### Naming rules

Agent names must start and end with alphanumeric characters, may contain hyphens in the middle, and have a maximum length of 63 characters. Examples: `novatrek-solution-architect-dev`. Invalid: `-agent`, `agent_1`.

### What OpenSpec generates for this

`.openspec/agents/*.agent.md` files would be transformed into `.foundry/agent-metadata.yaml` stubs by `generate_foundry()`, with placeholder values for `projectEndpoint` and `azureContainerRegistry` that the operator fills in per environment.

---

## 4. Skills

### What it is

Domain-specific capabilities the agent can invoke. Equivalent to `.github/skills/*/SKILL.md` in Copilot. In Foundry, skills are exposed as **MCP servers** or registered tool functions.

### MCP tool definitions in `agent.yaml`

Prompt agents declare MCP servers in `agent.yaml`. The Foundry runtime calls these servers when the agent invokes the tool:

```yaml
# agent.yaml
type: prompt
model: gpt-4o
instructions: "..."
tools:
  - type: mcp
    server: novatrek-arch-mcp
    endpoint: https://mcp.novatrek.example.com
    auth:
      type: managed_identity
```

### Agent Framework tool registration (hosted agents)

For hosted agents, tools are registered directly in Python or C# code using the Agent Framework SDK:

```python
from agent_framework import Agent, tool

@tool
def get_ticket(ticket_id: str) -> dict:
    """Retrieve a NovaTrek ticket by ID."""
    ...

agent = Agent(
    model=model_client,
    instructions=instructions,
    tools=[get_ticket],
)
```

### What OpenSpec generates for this

`.openspec/skills/*/SKILL.md` files contain narrative instructions consumed by the agent at inference time. In Foundry, this content would be bundled into the system prompt (large skills) or uploaded to Foundry Prompt Management (reusable sub-prompts). The actual tool functions (code) are separate from the skill documentation and must be implemented in the agent source.

---

## Comparison with VS Code Copilot

| Dimension | VS Code Copilot | Azure AI Foundry |
|---|---|---|
| Instructions intake | File on disk (auto-discovered) | System prompt in `agent.yaml` or loaded at startup |
| Prompts intake | File on disk (`*.prompt.md`, slash command) | Foundry Prompt Management or embedded template strings |
| Agent definitions | File on disk (`*.agent.md`, agent picker) | `.foundry/agent-metadata.yaml` + portal deployment |
| Skills intake | File on disk (`SKILL.md`, auto-loaded) | MCP server registration or Agent Framework `@tool` decorator |
| Change propagation | Immediate (file save) | Requires container rebuild and redeploy |
| Scope | Single developer workstation | Shared, multi-user, cloud-hosted |
| Governance | None (file permissions only) | Azure RBAC, Managed Identity, Key Vault |

---

## OpenSpec Generation Target: `.foundry/`

The `generate-tool-instructions.py` script already writes to `.github/`, `.cursor/`, `.roo/`, `.windsurf/`, `CLAUDE.md`, and `GEMINI.md`. A `generate_foundry()` function would add a `.foundry/` output with:

| Output File | Source | Purpose |
|---|---|---|
| `.foundry/system-prompt.md` | `.openspec/instructions/core-instructions.md` | System prompt for hosted agents |
| `.foundry/agent.yaml` | `.openspec/agents/*.agent.md` + core-instructions | Ready-to-deploy prompt agent config |
| `.foundry/agent-metadata.yaml` | `.openspec/agents/*.agent.md` | Deployment config stub (fill in endpoints) |
| `.foundry/prompts/<name>.md` | `.openspec/prompts/*.prompt.md` | Prompt templates for Foundry Prompt Management |

This would make `.foundry/` a generated output directory — never edited directly, always regenerated from `.openspec/` — consistent with how every other tool output directory is managed.
