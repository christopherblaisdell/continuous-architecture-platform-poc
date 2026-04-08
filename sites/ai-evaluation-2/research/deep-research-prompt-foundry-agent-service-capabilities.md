# Deep Research Prompt: Can Foundry Agent Service Replace IDE-Based Agents for Architecture Work?

## Research Question

Can Microsoft Azure AI Foundry Agent Service function as a replacement for IDE-based AI agents (GitHub Copilot, Cursor, Roo Code, Windsurf, Claude Code) for **solution architecture work** — specifically writing ADRs, analyzing OpenAPI specs, editing files in git repositories, producing PlantUML diagrams, running terminal commands, and iterating on workspace content?

## Context

Our team is evaluating AI toolchains for a solution architecture practice. A stakeholder has proposed using Azure AI Foundry (including Foundry IQ for retrieval and Foundry Agent Service for generation) as the platform. The alternative is GitHub Copilot running inside VS Code with workspace-local context.

The key architectural question: Foundry Agent Service solves the MCP auth gap with Foundry IQ (it has turnkey integration via `ProjectManagedIdentity`). But does it have the capabilities that make IDE agents effective for architecture work?

## Specific Questions to Answer

### 1. File System Access
- Can Foundry Agent Service read, create, edit, and delete files in a git repository?
- Does it have workspace awareness — knowledge of the full directory structure, file relationships, and project layout?
- Can it perform multi-file edits (e.g., update an OpenAPI spec AND the corresponding service page AND the capability changelog)?

### 2. Terminal / Command Execution
- Can Foundry Agent Service execute shell commands (e.g., run Python scripts, build MkDocs sites, execute PlantUML rendering)?
- Can it interact with git (commit, push, create branches)?
- Can it run arbitrary CLI tools that an architecture workflow depends on?

### 3. IDE Integration
- Does it integrate with VS Code or any IDE, or is it purely a cloud API / chat interface?
- Can it see what file the user has open, navigate to specific lines, show inline suggestions?
- Does it support the iterative "edit → review → refine" workflow that IDE agents enable?

### 4. Customization Model
- Does Foundry Agent Service support declarative behavioral customization (like Copilot's `.instructions.md`, `SKILL.md`, `.agent.md` files)?
- How do you configure domain-specific behavior (e.g., "you are a solution architect, follow MADR format, use C4 notation")?
- Is customization done via code (Python SDK), configuration (YAML/JSON), or prompt engineering?

### 5. Tool Use / MCP Support
- Can Foundry Agent Service consume MCP servers (not just expose MCP endpoints)?
- Can it call external tools — file search, grep, semantic search — the way IDE agents do?
- What is the tool integration model — function calling, code interpreter, or custom tool definitions?

### 6. Billing Model
- How is Foundry Agent Service billed? Per-token? Per-request? Per-seat?
- How does cost compare to GitHub Copilot's $39/seat/month for equivalent architecture work?

### 7. Production Readiness
- Is Foundry Agent Service GA or preview?
- What SLAs are available?
- What are the documented limitations?

## What Counts as an Authoritative Source

- Microsoft Learn documentation (learn.microsoft.com)
- Microsoft Tech Community blog posts
- Azure AI Foundry SDK documentation (GitHub repos, PyPI)
- Microsoft Build / Ignite session recordings or transcripts
- Official Azure pricing pages

Do NOT cite:
- Blog posts from non-Microsoft sources (unless they contain verifiable technical demonstrations)
- Marketing materials without technical specifics
- Reddit, StackOverflow, or forum posts

## Expected Output Format

For each question above:
1. State the finding (yes/no/partially)
2. Cite the authoritative source with a direct URL
3. Quote the relevant passage from the source
4. Note any caveats (preview status, limitations, planned features)

Then provide a summary assessment: **Can Foundry Agent Service realistically replace IDE-based agents for the daily workflow of a solution architect?**
