# Deep Research Prompt: OpenSpec Evaluation for Architecture Solution Design Workflow

## Research Objective

I need a technically precise analysis of **OpenSpec** (by Fission AI) evaluated as a potential workflow framework for my architecture solution design process. I am NOT comparing OpenSpec to CALM — they are completely different categories of tool. CALM is an architecture topology specification (nodes, relationships, interfaces). OpenSpec is a development workflow framework (specs, changes, AI agent workflow). Do NOT compare OpenSpec to CALM in your research.

The question is: **Should I adopt OpenSpec to improve my existing custom solution design workflow?**

## My Exact Setup

I have a **Continuous Architecture Platform** for a microservices-based system (19 services, 9 domains) with a custom solution design workflow:

- **Solution folder structure**: `architecture/solutions/_NTK-XXXXX-slug/` with subfolders for requirements, analysis, assumptions, capabilities, decisions (MADR format), guidance, per-service impacts, risks, and user stories
- **Workflow enforcement**: Convention-based — documented in an ~800-line `copilot-instructions.md` file that the AI agent reads and interprets
- **AI tooling**: GitHub Copilot Agent Mode (Claude Opus 4.6) — single tool, Copilot-specific instructions
- **Capability tracking**: YAML-based capability changelog records L3 capability emergence per solution
- **Decision format**: MADR (Markdown Any Decision Record) with required sections (Status, Date, Context, Decision Drivers, 2+ Options, Outcome, Consequences)
- **Portal**: MkDocs Material site with generators that consume metadata YAML
- **CI/CD**: GitHub Actions validating solution folder structure, YAML schema, and portal generation

## Specific Questions to Research

### 1. OpenSpec's Workflow Model vs My Custom Workflow

OpenSpec structures work as "changes" containing artifacts (proposal, specs, design, tasks) with a dependency graph schema. My workflow uses a richer artifact set (requirements, analysis, assumptions, capabilities, MADR decisions, guidance, per-service impacts, risks, user stories).

- Can OpenSpec's custom schema system accommodate my artifact types?
- Can schemas enforce artifact-internal structure (e.g., MADR format within a decisions artifact)?
- Can schemas handle variable-count subdirectories (e.g., `impacts/impact.1/`, `impacts/impact.2/`)?
- Can the schema dependency graph trigger metadata rollups (e.g., updating capability-changelog.yaml on archive)?

### 2. Enterprise Evidence and Production Use

- Who is actually using OpenSpec at scale? What is Comcast's specific use case?
- What industries or organization types are adopting it?
- Are there documented case studies beyond the marketing claims?
- What does the community activity look like (GitHub issues, PR velocity, Discord/forum activity)?

### 3. Custom Schema Capabilities

- What are the actual limits of OpenSpec's custom schemas?
- Can I inject templates into generated artifacts (e.g., pre-populate MADR sections)?
- How does the schema validation work — does it check artifact content or just file existence?
- Can schemas define artifact-specific rules (e.g., "decisions.md MUST contain at minimum 2 options")?

### 4. AI Agent Integration Mechanics

- What exactly does OpenSpec generate for GitHub Copilot integration?
- Does it create copilot-instructions.md content, skill files, or something else?
- Would OpenSpec's generated Copilot integration conflict with my existing copilot-instructions.md?
- How do the slash commands (/opsx:propose, /opsx:apply, etc.) work in Copilot Agent Mode specifically?
- Does the AI agent quality actually improve with OpenSpec's structured guidance vs. a well-written instruction file?

### 5. Risks and Maturity

- OpenSpec is v1.2.0 from a startup (Fission AI). What is Fission AI's funding, team size, and sustainability trajectory?
- Is there any indication of foundation governance (e.g., joining FINOS, Linux Foundation, Apache)?
- What is the breaking change history between versions?
- How does the MIT license interact with custom schema IP?

### 6. Minimum Viable Evaluation

- What is the smallest possible PoC to test whether OpenSpec improves my workflow?
- Can I run a single architecture scenario through OpenSpec and compare output quality?
- What are the concrete setup steps for a GitHub Copilot + OpenSpec integration?

## Output Format Requested

1. **Direct answers** to each numbered question above with source citations
2. **A clear verdict** on whether OpenSpec is worth evaluating for architecture solution design (not just feature development)
3. **Specific risks** that would make adoption inadvisable
4. **If recommending evaluation**: concrete next steps with expected effort

## Important Constraints

- Do NOT compare OpenSpec to CALM. They are different categories of tool.
- Do NOT assume OpenSpec is designed for architecture work — verify whether anyone uses it for architecture governance vs. feature development
- Do NOT rely on marketing claims — look for independent usage evidence
- Do cite specific GitHub issues, commits, or documentation pages where possible
