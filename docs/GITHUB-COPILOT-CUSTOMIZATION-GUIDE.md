# GitHub Copilot Customization Guide

<!-- PUBLISH -->

GitHub Copilot supports six distinct customization primitives, each serving a different purpose. This guide covers every type, how they work, when to use each, where the files live, how to switch between them, and how tool restrictions are enforced.

---

## Quick Reference

| Primitive | File Pattern | Location | Activation | Purpose |
|-----------|-------------|----------|------------|---------|
| Workspace Instructions | `copilot-instructions.md` or `AGENTS.md` | `.github/` or repo root | Always on | Project-wide standards |
| File Instructions | `*.instructions.md` | `.github/instructions/` or any folder | Automatic (glob match or description) | Context-specific guidance |
| Prompts | `*.prompt.md` | `.github/prompts/` | On-demand (`/` slash command) | Reusable task templates |
| Custom Agents | `*.agent.md` | `.github/agents/` | Agent picker dropdown | Role-based personas with tool restrictions |
| Skills | `SKILL.md` + folder | `.github/skills/<name>/` | On-demand (`/` or auto-detected) | Multi-step workflows with bundled assets |
| Hooks | `*.json` | `.github/hooks/` | Automatic at lifecycle events | Deterministic enforcement |

**User-level customizations** (personal, roam across workspaces) can also be placed at:

```
~/Library/Application Support/Code/User/prompts/
```

This location supports `.prompt.md`, `.instructions.md`, and `.agent.md` files (not skills or hooks).

---

## 1. Workspace Instructions (Always-On Baseline)

### What They Do

Workspace instructions are **automatically loaded into every Copilot chat interaction**. They define project-wide knowledge, coding standards, role definitions, and workflows. Every message you send to Copilot includes this content in its context window.

### Files (Choose One, Not Both)

| File | Location | Best For |
|------|----------|----------|
| `copilot-instructions.md` | `.github/` | Single-file projects, cross-editor compatibility |
| `AGENTS.md` | Repo root or subfolders | Monorepos with hierarchical overrides |

Using both simultaneously causes conflicts. Pick one approach.

### AGENTS.md Hierarchy (Monorepos)

For monorepos, the closest `AGENTS.md` in the directory tree takes precedence:

```
/AGENTS.md                    # Root defaults
/frontend/AGENTS.md           # Frontend overrides root
/backend/AGENTS.md            # Backend overrides root
/backend/services/AGENTS.md   # Service-level overrides backend
```

### Template

```markdown
# Project Guidelines

## Role
{What expertise the AI should bring to this project}

## Architecture
{Components, boundaries, service ownership rules}

## Code Style
{Language and formatting preferences -- reference exemplar files}

## Build and Test
{Commands that the agent will attempt to run}

## Conventions
{Patterns that differ from common practices -- include specific examples}
```

### What to Include

- Role definitions and domain expertise
- Domain model and bounded context rules
- Coding standards and anti-patterns
- Build, test, and deploy commands
- Mock tool commands and available scripts
- Documentation standards (MADR, arc42, etc.)

### What NOT to Include

- Content already enforced by linters or formatters (redundant)
- Entire READMEs (link instead: "See docs/TESTING.md for test conventions")
- Rarely-needed content that wastes context tokens on every interaction

### This Workspace

This project uses `.github/copilot-instructions.md` (500+ lines) containing:

- Solution Architect role definition for NovaTrek Adventures
- 19-service microservice domain model with ownership boundaries
- Mock JIRA, Elastic, and GitLab tool commands
- Solution design workflow and folder structure conventions
- MADR, C4 Model, and arc42 standards
- Architecture review checklist and anti-pattern catalog

---

## 2. File Instructions (.instructions.md) -- Contextual Guidance

### What They Do

File instructions provide **scoped guidance** that loads only when relevant, rather than consuming context on every interaction. They activate through glob pattern matching or keyword-based discovery.

### Locations

| Path | Scope |
|------|-------|
| `.github/instructions/*.instructions.md` | Workspace (team-shared) |
| `<any-folder>/.instructions.md` | Folder-scoped (applies when working in that folder) |
| `~/Library/Application Support/Code/User/prompts/*.instructions.md` | User profile (personal) |

### Frontmatter

```yaml
---
description: "<required for on-demand discovery>"
applyTo: "**/*.py"    # Optional: auto-attach when matching files are in context
---
```

### Three Discovery Modes

| Mode | Trigger | Example Use Case |
|------|---------|------------------|
| **On-demand** | Agent detects relevance from `description` keywords | Task-based: "Use when writing database migrations" |
| **Explicit** | Files matching `applyTo` glob are in context | File-based: all Python files, all YAML specs |
| **Manual** | User clicks `Add Context` then `Instructions` | Ad-hoc attachment |

### applyTo Glob Patterns

```yaml
applyTo: "**"                     # ALWAYS included (use with extreme caution)
applyTo: "**/*.py"                # All Python files
applyTo: ["src/**", "lib/**"]     # Multiple patterns (OR logic)
applyTo: "src/api/**/*.ts"        # Specific folder + extension
```

WARNING -- `applyTo: "**"` loads the instruction into the context window on **every interaction**, even when irrelevant. Use specific globs unless the content truly applies universally.

### Template

```markdown
---
description: "Use when writing database migrations, schema changes, or data
  transformations. Covers safety checks and rollback patterns."
---
# Migration Guidelines

- Always create reversible migrations
- Test rollback before merging
- Never drop columns in the same release as code removal
```

The "Use when..." pattern in the description is critical for on-demand discovery. Without specific trigger words, the agent will not find the instruction.

### This Workspace

| File | Purpose |
|------|---------|
| `architecture/.instructions.md` | General architecture workspace rules |
| `architecture/specs/.instructions.md` | OpenAPI spec editing standards |
| `architecture/solutions/.instructions.md` | Solution design checklist, prior-art discovery, trade-off documentation |

---

## 3. Prompts (.prompt.md) -- Reusable Task Templates

### What They Do

Prompts are **single-focused task templates** you invoke on demand. They define a structured workflow that the agent follows, optionally with a pinned model, specific tools, and a target agent mode.

### Location

| Path | Scope |
|------|-------|
| `.github/prompts/*.prompt.md` | Workspace (team-shared) |
| `~/Library/Application Support/Code/User/prompts/*.prompt.md` | User profile (personal) |

### Frontmatter

```yaml
---
description: "Generate test cases for selected code"     # Recommended
agent: "agent"                                           # Optional: ask, agent, plan, or custom agent name
model: "Claude Opus 4.6 (copilot)"                        # Optional: pin to a model
tools: [search, read, execute]                           # Optional: available tools
argument-hint: "Service name or ticket ID"               # Optional: hint shown in input
---
```

**Model fallback** (use first available):

```yaml
model: ['Claude Opus 4.6 (copilot)', 'Claude Sonnet 4.5 (copilot)']
```

### How to Invoke

1. **Slash command**: Type `/` in chat, then select from the list of prompts and skills
2. **Command palette**: `Chat: Run Prompt...`
3. **Editor**: Open the `.prompt.md` file directly, click the play button

### Context References

Use Markdown links to attach files and `#tool:<name>` to reference tools:

```markdown
Review the API spec [svc-check-in](../../architecture/specs/svc-check-in.yaml)
using #tool:search to find related services.
```

### Tool Priority

When both a prompt and a custom agent define tools, the resolution order is:

1. Tools declared in the prompt file
2. Tools from the referenced custom agent
3. Default tools for the selected agent mode

### This Workspace

| Prompt | Purpose |
|--------|---------|
| `architecture-review.prompt.md` | Structured 3-phase architecture review with anti-pattern detection |
| `deep-research.prompt.md` | Multi-source evidence-gathering workflow producing cited reports |
| `investigation.prompt.md` | Incident/issue investigation using logs, specs, and source code |
| `security-review.prompt.md` | Security-focused review against OWASP Top 10 |
| `solution-verification.prompt.md` | Post-design verification of solution completeness |

---

## 4. Custom Agents (.agent.md) -- Specialized Personas

### What They Do

Custom agents define **personas with specific tools, instructions, and behavioral constraints**. Each agent is effectively a different "mode" with its own tool restrictions, model preferences, and instructions. This is the primary mechanism for **role-based tool restrictions**.

### Location

| Path | Scope |
|------|-------|
| `.github/agents/*.agent.md` | Workspace (team-shared) |
| `~/Library/Application Support/Code/User/prompts/*.agent.md` | User profile (personal) |

### Frontmatter

```yaml
---
description: "<required>"                    # For agent picker and subagent discovery
tools: [read, search]                        # Tool restrictions (see below)
model: "Claude Sonnet 4"                     # Optional: pin model
agents: [researcher, reviewer]               # Optional: restrict which subagents this agent can invoke
user-invocable: true                         # Show in agent picker (default: true)
disable-model-invocation: false              # Prevent other agents from invoking as subagent
handoffs: [...]                              # Optional: transitions to other agents
---
```

### How to Switch

Use the **agent selector dropdown** in the chat panel. It appears where you see "Ask", "Agent", or a custom agent name. Your custom agents appear alongside the built-in modes.

### Tool Restrictions (Core Feature)

The `tools` field is the primary mechanism for controlling what an agent can and cannot do. By limiting the tool set, you create agents that are **structurally constrained** to their role.

#### Tool Aliases

| Alias | What It Allows |
|-------|---------------|
| `execute` | Run shell commands in the terminal |
| `read` | Read file contents |
| `edit` | Create and modify files |
| `search` | Search files and text across the workspace |
| `agent` | Invoke other custom agents as subagents |
| `web` | Fetch URLs and perform web searches |
| `todo` | Manage task lists |

#### Common Restriction Patterns

```yaml
tools: [read, search]             # Read-only research -- cannot edit files or run commands
tools: [read, edit, search]       # Can edit files but cannot run terminal commands
tools: [myserver/*]               # MCP server tools only -- no local file or terminal access
tools: []                         # Conversational only -- no tools at all
```

**What omitting `tools` means**: If you omit the `tools` field entirely, the agent gets **all default tools**. To restrict, you must explicitly list only what you want.

**What `tools: []` means**: The agent has **zero tool access** -- it can only converse based on what is in its context window. Useful for pure advisory or explanation agents.

#### MCP Server Tool Access

Reference tools from MCP (Model Context Protocol) servers:

```yaml
tools: [myserver/*]              # All tools from one MCP server
tools: [jira/*, elastic/*]       # Tools from multiple MCP servers
tools: [read, myserver/query]    # Mix built-in aliases with specific MCP tools
```

### Invocation Control

| Attribute | Default | Effect |
|-----------|---------|--------|
| `user-invocable: true` | `true` | Appears in the agent picker dropdown |
| `user-invocable: false` | `true` | Hidden from picker -- only accessible as a subagent |
| `disable-model-invocation: true` | `false` | Other agents cannot invoke this agent as a subagent |
| `agents: [name1, name2]` | all | Restrict which subagents this agent can delegate to |
| `agents: []` | all | Cannot delegate to any subagent |

### Subagent Delegation

Agents can invoke other agents as subagents. The parent agent reads the child's `description` to decide when to delegate. This enables multi-agent workflows:

```
Orchestrator Agent (all tools)
  ├── Researcher Agent (read, search only)
  ├── Reviewer Agent (read, search only)
  └── Writer Agent (read, edit, search)
```

### Template

```markdown
---
description: "Read-only research agent for codebase exploration and evidence gathering.
  Use when investigating architecture, analyzing specs, or reviewing source code."
tools: [read, search]
user-invocable: false
---
You are a research specialist. Your job is to gather evidence from the codebase.

## Constraints
- DO NOT edit any files
- DO NOT run terminal commands
- ONLY read files and search the codebase

## Approach
1. Identify relevant files from the user's question
2. Read specs, source code, and metadata files
3. Cross-reference findings across sources

## Output Format
Return a structured report with file path citations for every claim.
```

---

## 5. Skills (SKILL.md) -- On-Demand Workflow Packages

### What They Do

Skills are **folders of instructions, scripts, templates, and reference docs** that the agent loads progressively when a relevant task is detected. They are heavier than prompts -- designed for repeatable multi-step workflows with bundled assets.

### Location

| Path | Scope |
|------|-------|
| `.github/skills/<name>/` | Workspace (team-shared) |
| `.agents/skills/<name>/` | Workspace (alternative) |
| `.claude/skills/<name>/` | Workspace (Claude-specific) |
| `~/.copilot/skills/<name>/` | User profile (personal) |
| `~/.agents/skills/<name>/` | User profile (alternative) |

### Structure

```
.github/skills/webapp-testing/
├── SKILL.md              # Required entry point (name must match folder)
├── scripts/              # Executable code the agent can run
├── references/           # Docs loaded on demand
└── assets/               # Templates, boilerplate files
```

### SKILL.md Format

```yaml
---
name: webapp-testing            # Required: must match folder name (lowercase, hyphens)
description: 'Test web applications using Playwright. Use for verifying
  frontend behavior, debugging UI issues, and capturing screenshots.'
argument-hint: 'URL or component name'
user-invocable: true            # Show as slash command (default: true)
disable-model-invocation: false # Allow auto-detection (default: false)
---

# Web Application Testing

## When to Use
- Verify frontend functionality after changes
- Debug UI rendering issues

## Procedure
1. Start the web server using [start script](./scripts/start.sh)
2. Run [test suite](./scripts/test.js)
3. Review screenshots in `./screenshots/`
```

### Progressive Loading (Context Efficiency)

Skills load in three stages to minimize context window usage:

| Stage | What Loads | Token Cost |
|-------|-----------|------------|
| 1. Discovery | `name` + `description` only | ~100 tokens |
| 2. Instructions | Full `SKILL.md` body | < 5,000 tokens |
| 3. Resources | Referenced files (`./scripts/`, `./references/`) | On demand |

The agent only advances to the next stage when the skill is actually relevant. This is far more context-efficient than putting everything in workspace instructions.

### How to Invoke

- **Slash command**: Type `/` in chat -- skills appear alongside prompts
- **Auto-detected**: Agent reads the `description` and loads the skill when the task matches

### Visibility Control

| Configuration | Slash Command | Auto-Loaded by Agent |
|---|---|---|
| Default (both omitted) | Yes | Yes |
| `user-invocable: false` | No | Yes |
| `disable-model-invocation: true` | Yes | No |
| Both set | No | No |

### Skills vs Prompts

Both appear as `/` commands. The distinction:

| Aspect | Prompt | Skill |
|--------|--------|-------|
| Complexity | Single focused task | Multi-step workflow |
| Assets | None (just the markdown) | Scripts, templates, reference docs |
| Loading | Entire file loaded at once | Progressive (3-stage) |
| Use case | "Generate tests for this code" | "Run the full QA pipeline" |

---

## 6. Hooks (.json) -- Deterministic Enforcement

### What They Do

Hooks are **shell commands that run automatically at specific lifecycle events** during an agent session. Unlike all other primitives (which are guidance the agent *may* follow), hooks are **deterministic and enforced** -- they execute regardless of what the agent thinks.

This is the only customization type that provides hard guarantees.

### Location

| Path | Scope |
|------|-------|
| `.github/hooks/*.json` | Workspace (team-shared, version-controlled) |
| `~/.claude/settings.json` | User profile (personal) |

Hooks from all locations are collected and executed -- workspace and user hooks do not override each other.

### Hook Events

| Event | When It Fires | Example Use |
|-------|--------------|-------------|
| `SessionStart` | First prompt of a new session | Inject environment context |
| `UserPromptSubmit` | User submits a message | Validate or transform prompts |
| `PreToolUse` | Before any tool invocation | Block dangerous commands, require approval |
| `PostToolUse` | After successful tool invocation | Auto-format files, run linters |
| `PreCompact` | Before context window compaction | Preserve critical context |
| `SubagentStart` | Subagent begins execution | Audit subagent invocations |
| `SubagentStop` | Subagent finishes | Log subagent results |
| `Stop` | Agent session ends | Cleanup, summary generation |

### Configuration Format

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "type": "command",
        "command": "./scripts/validate-tool.sh",
        "timeout": 15
      }
    ],
    "PostToolUse": [
      {
        "type": "command",
        "command": "./scripts/auto-format.sh",
        "timeout": 10
      }
    ]
  }
}
```

Each hook supports:
- `command`: The shell command to execute (default, cross-platform)
- `windows`, `linux`, `osx`: Platform-specific overrides
- `cwd`: Working directory
- `env`: Environment variables
- `timeout`: Maximum execution time in seconds

### Input / Output Contract

Hooks receive **JSON on stdin** with context about the event (tool name, parameters, session state). They return **JSON on stdout** to control agent behavior.

**PreToolUse permission control:**

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Destructive operation blocked by policy"
  }
}
```

| Permission | Effect |
|-----------|--------|
| `allow` | Tool invocation proceeds |
| `ask` | User is prompted for confirmation |
| `deny` | Tool invocation is blocked |

**Exit codes:**

| Code | Effect |
|------|--------|
| `0` | Success -- continue normally |
| `2` | Blocking error -- stops the agent |
| Other | Non-blocking warning |

### Hooks vs Instructions

| Primitive | Nature | Guarantee |
|-----------|--------|-----------|
| Instructions, Prompts, Skills, Agents | Guidance (non-deterministic) | Agent *should* follow, but might not |
| Hooks | Enforcement (deterministic) | Runs regardless -- cannot be overridden by the agent |

Use hooks when behavior **must be guaranteed**: blocking destructive commands, forcing validation, auto-running formatters after edits.

---

## Tool Restrictions -- Deep Dive

### What Tool Restrictions Are For

Tool restrictions (the `tools` field in `.agent.md` files) control **what actions an agent can perform within that agent's session**. They are the primary mechanism for implementing:

- **Least privilege**: Agents only get the tools they need for their role
- **Workflow optimization**: Make the right thing easy -- a research agent does not need edit tools cluttering its focus
- **Role separation**: Research agents that only read, review agents that only analyze, writer agents that edit
- **Accidental damage prevention**: Reduce the chance of unintended edits or command execution
- **Workflow integrity**: Force agents to delegate to specialized subagents instead of doing everything themselves

IMPORTANT: Agent tool restrictions are **workflow guardrails, not security boundaries**. See the section below on what prevents developers from simply switching agents.

### Practical Examples

**Read-only architecture reviewer** -- can analyze but not change anything:

```yaml
---
description: "Architecture reviewer. Analyzes specs and source code for anti-patterns."
tools: [read, search]
---
```

**Documentation writer** -- can edit docs but not run commands or touch code:

```yaml
---
description: "Documentation writer. Generates and updates markdown documentation."
tools: [read, edit, search]
applyTo: "**/*.md"
---
```

**Infrastructure agent** -- can only use Terraform MCP tools:

```yaml
---
description: "Infrastructure provisioning agent. Manages Terraform resources."
tools: [terraform/*]
---
```

**Pure advisor** -- no tool access at all, just conversation:

```yaml
---
description: "Architecture advisor. Provides guidance without making changes."
tools: []
---
```

### What Prevents Developers from Switching to a Different Agent?

This is the most important governance question. A developer who is using a read-only custom agent can simply **switch to the default "Agent" mode** (which has all tools) using the agent selector dropdown. Nothing in the `.agent.md` system prevents this.

This means agent tool restrictions are fundamentally **opt-in guardrails** -- they make the right workflow convenient, but they do not enforce security policy. They are analogous to creating a `read-only` VS Code workspace profile: helpful for focus, but anyone can switch profiles.

**If you need hard enforcement, use hooks.** Hooks run at lifecycle events regardless of which agent is selected. A `PreToolUse` hook fires before ANY tool invocation in ANY agent mode -- the default Agent, a custom agent, or even Ask mode. The developer cannot bypass a hook by switching agents.

Here is the honest breakdown:

| Mechanism | Enforcement Level | Can Be Bypassed by Switching Agents? |
|-----------|-------------------|--------------------------------------|
| Agent `tools` field | Opt-in guardrail | YES -- switch to default Agent |
| Workspace hooks (`.github/hooks/`) | Deterministic | NO -- fires in all agent modes |
| User-level hooks (`~/.claude/settings.json`) | Deterministic | NO -- lives outside workspace |
| GitHub org admin settings | Platform policy | NO -- outside developer control |

The practical guidance:

- **Use agent tool restrictions for workflow optimization** -- making the right thing easy, reducing cognitive load, preventing accidental damage
- **Use hooks for security enforcement** -- blocking destructive commands, requiring approval for sensitive operations, enforcing policy
- **Use org-level settings for platform governance** -- controlling model access, disabling features, audit logging

### What Prevents Developers from Deleting Tool Restriction Files?

Even though agent restrictions are opt-in, deleting or modifying the `.agent.md` files themselves is governed through standard software engineering controls.

#### Layer 1: Version Control and Code Review

`.agent.md` files live in `.github/agents/` and are committed to the repository. Any change -- including removing tool restrictions -- shows up in a pull request diff and goes through the normal code review process. Teams can:

- Require PR approval for changes to `.github/agents/` and `.github/hooks/`
- Use GitHub CODEOWNERS to assign security reviewers to customization files
- Set up branch protection rules that require specific reviewers for these paths

```
# .github/CODEOWNERS
/.github/agents/    @security-team @architecture-team
/.github/hooks/     @security-team
/.github/instructions/ @architecture-team
```

#### Layer 2: Hooks as Hard Enforcement

While agent tool restrictions are guidance (the agent respects the `tools` field), **hooks are deterministic**. A `PreToolUse` hook runs as a shell command *before* any tool invocation, regardless of what the agent file says. Even if someone deletes an `.agent.md` file, hooks still execute.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "type": "command",
        "command": "./scripts/enforce-tool-policy.sh",
        "timeout": 10
      }
    ]
  }
}
```

The hook script can inspect the tool being invoked and return `deny` to block it. This provides a **defense-in-depth layer** that operates independently of agent definitions.

#### Layer 3: User-Level Hooks (Cannot Be Overridden by Workspace)

User-level hooks at `~/.claude/settings.json` are **outside the repository** and cannot be modified by workspace changes, other developers, or the agent itself. An organization can distribute user-level hook configurations through device management policies:

- Hooks from all locations (workspace + user) are collected and ALL execute
- A workspace cannot suppress a user-level hook
- The agent cannot edit user-level configuration files

#### Layer 4: Organizational Policy (GitHub Organization Settings)

GitHub Copilot admins at the organization level can:

- Restrict which models are available
- Control whether Agent Mode is enabled
- Manage MCP server access
- Audit Copilot usage and tool invocations

These controls exist outside the repository entirely and cannot be modified by individual developers.

#### Layer 5: The Agent Runtime

Within a given agent session, the `tools` field is enforced by the Copilot runtime infrastructure. The model literally does not have access to tools not listed in the `tools` field -- a developer cannot bypass this by prompting "ignore tool restrictions." However, the developer CAN switch to a different agent that has more tools. The restriction is per-agent, not per-developer.

#### Summary of Governance Layers

| Layer | What It Protects | Can Developer Bypass? | How? |
|-------|-----------------|----------------------|------|
| Agent `tools` field | Tools within that agent session | YES | Switch to default Agent mode |
| CODEOWNERS | File change review | NO | Requires admin override |
| Branch protection | Merge requirements | NO | Requires admin override |
| Workspace hooks | Tool invocations in ALL modes | PARTIALLY | Edit hook files (visible in PR) |
| User-level hooks | Tool invocations in ALL modes | NO | Lives outside repo |
| GitHub org settings | Platform-level controls | NO | Only org admins |

#### The Bottom Line

**Agent tool restrictions = workflow optimization.** They make the right path easy and prevent accidental damage.

**Hooks = security enforcement.** They run regardless of which agent is active and cannot be bypassed by agent switching.

If you need to **guarantee** that a developer cannot run destructive commands via Copilot, use a `PreToolUse` hook -- not an agent restriction.

---

## Decision Matrix -- Which Primitive to Use

| Need | Primitive | Why |
|------|-----------|-----|
| Rules that apply to **every interaction** | Workspace Instructions | Always loaded automatically |
| Rules for **specific file types** (Python, YAML, etc.) | File Instructions with `applyTo` | Loads only when matching files are in context |
| Rules for **specific tasks** (migrations, reviews) | File Instructions with `description` | Agent detects relevance from keywords |
| **Reusable one-shot tasks** (generate tests, create docs) | Prompts | Invoked on demand via `/` command |
| **Role-based modes** with tool restrictions | Custom Agents | Different tool sets per persona |
| **Multi-step workflows** with scripts and templates | Skills | Progressive loading, bundled assets |
| **Hard enforcement** (block commands, auto-format) | Hooks | Deterministic, runs regardless of agent behavior |

---

## Switching Between Customizations

### Switching Agents

Use the **agent selector dropdown** in the VS Code chat panel. It shows:

- Built-in modes: Ask, Agent
- Custom agents from `.github/agents/` (those with `user-invocable: true`)

Click the dropdown and select the agent you want. Each agent brings its own tool set, model preference, and instructions.

### Invoking Prompts and Skills

Type `/` in the chat input. Both prompts and skills appear in the same list. Select the one you want. You can also:

- Use the command palette: `Chat: Run Prompt...`
- Open a `.prompt.md` file and click the play button

### Attaching Instructions Manually

Click `Add Context` in the chat panel, then select `Instructions`. This shows all available `.instructions.md` files. Select the ones relevant to your current task.

### Switching Models

Models can be selected:

1. **Per-session**: Use the model picker in the chat panel
2. **Per-prompt**: Set `model:` in the prompt frontmatter
3. **Per-agent**: Set `model:` in the agent frontmatter
4. **Fallback chains**: `model: ['Claude Opus 4.6 (copilot)', 'Claude Sonnet 4.5 (copilot)']`

---

## Context References in Chat

| Reference | What It Does |
|-----------|-------------|
| `#file:path/to/file.ts` | Attaches a specific file to context |
| `#folder:src/api/` | Attaches folder contents |
| `#selection` | Attaches current editor selection |
| `#codebase` | Searches the indexed codebase |
| `#tool:<name>` | References a specific tool (in prompt/agent body) |
| `[label](./path)` | Markdown link to attach file (in prompt/skill body) |

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Using both `copilot-instructions.md` and `AGENTS.md` | Conflicts and unpredictable behavior | Pick one approach |
| `applyTo: "**"` on narrow instructions | Burns context tokens on every interaction | Use specific globs |
| Vague `description` fields | Agent cannot discover the customization | Use "Use when..." with specific keywords |
| Kitchen-sink workspace instructions | Exceeds useful context, dilutes important rules | Move specialized content to file instructions or skills |
| Swiss-army agents with all tools | Defeats the purpose of tool restrictions | Minimal tool set per role |
| Duplicating content across files | Divergence over time | Link to a single source of truth |
| Multi-task prompts | Unclear focus, inconsistent results | One prompt = one task |
| Letting agents edit hook scripts | Undermines enforcement guarantees | Protect hooks with CODEOWNERS |

---

## Troubleshooting

### Instructions Not Loading

1. Verify file location (`.github/copilot-instructions.md` or `.github/instructions/`)
2. Check YAML frontmatter syntax -- unescaped colons, tabs instead of spaces, and missing `---` delimiters cause silent failures
3. Ensure `description` contains trigger keywords for on-demand discovery
4. Restart VS Code if changes are not picked up

### Agent Not Appearing in Picker

1. Confirm file is in `.github/agents/` with `.agent.md` extension
2. Check that `user-invocable` is not set to `false`
3. Verify YAML frontmatter is valid
4. Ensure `description` field is present (required for agents)

### Skill Not Discovered

1. Verify folder name matches the `name` field in `SKILL.md`
2. Check that `description` contains the keywords from the user's task
3. Ensure `SKILL.md` is under 500 lines (move details to `references/`)
4. Confirm `disable-model-invocation` is not set to `true` if you want auto-detection

### Hook Not Executing

1. Check JSON syntax in the hook configuration file
2. Verify the shell script has execute permissions (`chmod +x`)
3. Check that the `timeout` is long enough for the script to complete
4. Review exit codes: `0` = success, `2` = blocking error, other = warning

---

## Examples from This Workspace

### Workspace Instructions

`.github/copilot-instructions.md` -- 500+ lines defining the NovaTrek Adventures domain model, 19-service architecture, mock tool commands, solution design workflow, and documentation standards.

### File Instructions

| File | Purpose |
|------|---------|
| `architecture/.instructions.md` | General architecture workspace rules |
| `architecture/specs/.instructions.md` | OpenAPI spec editing standards |
| `architecture/solutions/.instructions.md` | Solution design checklist with prior-art discovery, trade-off documentation, and content separation rules |

### Reusable Prompts

| Prompt | Purpose |
|--------|---------|
| `architecture-review.prompt.md` | 3-phase architecture review: current state analysis, anti-pattern detection, quality attribute assessment |
| `deep-research.prompt.md` | Multi-source evidence-gathering workflow with structured citation format |
| `investigation.prompt.md` | Incident/issue investigation using logs, specs, and source code |
| `security-review.prompt.md` | Security-focused review against OWASP Top 10 |
| `solution-verification.prompt.md` | Post-design completeness verification |

---

## Further Reading

### Internal References

- [OpenSpec Customization Guide](OPENSPEC-CUSTOMIZATION-GUIDE.md) -- how OpenSpec's spec-driven workflow framework works
- [Copilot vs OpenSpec Comparison](COPILOT-VS-OPENSPEC-COMPARISON.md) -- side-by-side comparison with recommendation

### Official Documentation

- [VS Code: Custom Instructions](https://code.visualstudio.com/docs/copilot/customization/custom-instructions)
- [VS Code: Prompt Files](https://code.visualstudio.com/docs/copilot/customization/prompt-files)
- [VS Code: Custom Agents](https://code.visualstudio.com/docs/copilot/customization/custom-agents)
- [VS Code: Agent Skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- [VS Code: Hooks](https://code.visualstudio.com/docs/copilot/customization/hooks)