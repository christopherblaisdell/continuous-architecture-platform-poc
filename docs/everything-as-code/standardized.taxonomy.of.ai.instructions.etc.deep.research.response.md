# Standardized Taxonomy of AI Instructions: Frameworks, Architectures, and Governance

> **BLUEPRINT DOCUMENT.** This file is part of the portable EaC Blueprint and is exported to corporate Instance workspaces. It is a deep-research response supporting Pillar 11 (AI Instructions as Code) — it is target-agnostic and contains no NovaTrek-specific content.

## Executive Summary: The Three-Layer Framework for AI Governance

As large language models transition from chat interfaces into autonomous, agentic software engineering systems, the industry is grappling with how to govern machine behavior. Currently, AI platforms aggregate constraints, project contexts, and procedural rules into monolithic, platform-specific markdown files (e.g., `.cursorrules`, `.clinerules`). This lack of standardization leads to "context drift," unpredictable execution, and severe security vulnerabilities.

A primary source of confusion in the industry is the conflation of behavioral rules, lifecycle management, and runtime data transport. To achieve true portability and governance, AI instruction architectures must be distinctly separated into three operational layers:

- **Layer 1 — Behavioral Specification:** The authored instructions, schemas, and typologies that define how an AI reasons, the constraints governing its behavior, the personas it adopts, and the structural standards it must follow.
- **Layer 2 — Change Governance:** The workflow and lifecycle processes by which Layer 1 artifacts are proposed, reviewed, versioned, synchronized, and archived.
- **Layer 3 — Runtime Integration:** The transport mechanisms and ecosystem integrations that deliver context and capabilities to the model at inference time (e.g., RAG pipelines, tool registries, and RPC protocols).

This research evaluates the current state of these three layers, analyzing existing vendor routing models, the emerging security implications of agentic execution, and the path toward a unified, cross-platform portability strategy.

---

## Layer 1: Behavioral Specification (The Taxonomic Void)

Layer 1 defines what the AI should do and how it should behave. Currently, most platforms rely on raw, unstructured markdown. While academic researchers have attempted to map the semantic structures of prompts, a formal, machine-readable schema for behavioral specifications remains the largest portability gap in the industry.

### Academic Foundations and Industry Frameworks

Academic research has proposed frameworks like PROMPTPRISM, a linguistically-inspired taxonomy that decomposes instructions into Structural roles (System, User, Assistant, Tools), Semantic intents (Task, Chain of Thought, Behavioral/Safety Guidelines, Output Constraints), and Syntactic markers [1]. Similarly, the Instruction Hierarchy establishes a privilege-based security architecture, mandating that System Messages hold the highest privilege, followed by User Messages, with Tool Outputs holding the lowest privilege [2].

In the industry, Anthropic's Constitutional AI represents an early attempt at formalizing behavioral rules. However, rather than using a universally portable schema, its principles are currently structured during the training phase as `CritiqueRequest` and `RevisionRequest` pairs, or as multiple-choice evaluations to generate reinforcement learning preference datasets [3]. While these frameworks identify the types of instructions that exist, they do not provide a transportable file schema.

### Emerging Standards and Working Drafts

Several standards bodies and industry coalitions are actively working to fill the Layer 1 schema gap:

- **IEEE P3394 (Large Language Model Agent Interface):** This standard introduces Agent Behavioral Contracts (ABC), which formalizes Design-by-Contract principles for AI agents. An ABC contract specifies Preconditions, Invariants, Governance policies, and Recovery mechanisms as first-class, runtime-enforceable components, bounding behavioral drift across long-horizon executions.
- **OASIS Coalition for Secure AI (CoSAI):** The CoSAI working group is drafting the Universal Agentic Skill Format (v1.0), a cross-platform YAML standard designed to define task understanding, multi-step planning, tool orchestration, and safety guardrails, superseding platform-specific formats like `.clinerules` or `.cursorrules`.
- **W3C AI Agent Protocol Community Group:** This group focuses on inter-agent communication protocols and agent identity models, developing open standards for how agents negotiate roles and exchange capability information across domains [4].
- **OASIS-CG (Ontologies for Agents, Systems, and Integration of Services):** This group focuses on standardizing semantic models for representing agents, their actions, and responsibilities using Semantic Web technologies [5].

---

## Layer 2: Change Governance (The OpenSpec Model)

Layer 2 answers the question: How do these behavioral specifications safely evolve alongside a codebase? Treating AI instructions as unstructured, append-only text files inevitably leads to context window bloat and conflicting rules.

### The OpenSpec Architecture

To solve this, OpenSpec operates strictly at Layer 2, introducing Spec-Driven Development (SDD) to manage the lifecycle of AI instructions [6]. OpenSpec enforces alignment between human intent and AI execution before any code is generated.

OpenSpec manages state through a canonical hub-and-spoke directory architecture:

- **Source of Truth (`openspec/specs/`):** The master documentation of the system's current behavior, organized by domain [6].
- **Isolated Changes (`openspec/changes/`):** In-progress modifications are isolated, allowing parallel development without context contamination [6].

The framework replaces probabilistic chat interactions with a deterministic, phase-gated execution pipeline:

- **`/opsx:propose`:** The AI generates a change portfolio consisting of four artifacts: `proposal.md` (scope/boundaries), a Delta Spec (identifying exact requirements as ADDED, MODIFIED, or REMOVED), `design.md` (architectural decisions), and `tasks.md` (a granular implementation checklist) [6].
- **`/opsx:apply`:** The AI executes the work rigidly against the `tasks.md` checklist, ensuring execution atomicity [6].
- **`/opsx:archive`:** Once completed, OpenSpec atomically merges the Delta Spec into the master `openspec/specs/` source of truth and archives the execution trace to form an immutable evolution record [6].

### Linguistic Enforcement and Portability Limitations

OpenSpec bridges the gap between natural language and structured schemas by enforcing RFC 2119 linguistic standards. By requiring AI agents to use keywords like MUST, SHALL, SHOULD, and MAY, it provides unambiguous priority signals to the model.

**The Distinction for Portability:** OpenSpec is a highly effective governance tool, but it is not a Layer 1 schema solution. OpenSpec does not abstract away platform-specific instruction formats; the downstream files it orchestrates are still platform-specific (e.g., `.clinerules` for Roo Code, `.mdc` for Cursor). OpenSpec achieves platform-agnostic governance over platform-specific instructions. True portability requires OpenSpec's governance workflows to operate on top of a future, standardized Layer 1 schema.

---

## Layer 3: Runtime Integration (The Transport Ecosystem)

Layer 3 defines the transport mechanisms and integrations that deliver context and execution capabilities to the model at inference time. It answers: "What data and tools can the AI access right now?"

### The Model Context Protocol (MCP)

Previous analyses commonly miscategorized the Model Context Protocol (MCP) alongside behavioral instruction files like Cursor's `.mdc`. This is an architectural error. MCP is a runtime integration protocol — an RPC transport layer utilizing JSON-RPC over stdio or Server-Sent Events (SSE).

MCP standardizes three distinct primitives:

- **Resources (Nouns):** Application-controlled data streams (e.g., file contents, database schemas) providing context.
- **Tools (Verbs):** Model-controlled executable functions (e.g., API calls, script execution).
- **Prompts (Templates):** User-controlled parameterized templates injected at runtime.

**Architectural Clarification:** Suggesting that MCP be extended with a core "Instruction Content block" to handle complex behavioral specifications conflates the transport layer with the specification layer. MCP is designed to transport JSON-RPC messages obliviously. Complex behavioral contracts, personas, and safety boundaries belong in Layer 1 schemas (like IEEE P3394) which are carried over Layer 3 protocols, not baked into the transport protocol's core primitives.

### The Broader Layer 3 Ecosystem

Beyond MCP, the runtime integration layer consists of:

- **Retrieval-Augmented Generation (RAG) Pipelines:** Coupling the LLM with vector-enabled datastores (like Elasticsearch) to create semantic long-term memory, injecting relevant facts into the prompt dynamically.
- **Tool Registries:** Dynamic catalogs where agents discover execution capabilities dynamically at runtime, mapped against their authorized identity.

---

## Cross-Platform Instruction Routing Analysis

At the intersection of Layer 1 (Specifications) and Layer 3 (Runtime), integrated development environments must determine when to load specific behavioral instructions. A formal comparison of vendor routing models reveals significant fragmentation:

| Platform | Activation Triggers | Conflict Resolution & Precedence | Scope Model |
|----------|--------------------|---------------------------------|-------------|
| **Cursor** | `alwaysApply: true`, Glob match (auto Attached), Semantic Match (agent Requested), Manual (`@rule`) | Last-writer-wins (rules loaded last in context take precedence). | Global User settings, Project `.cursor/rules/*.mdc`. |
| **GitHub Copilot** [7] | Always-on for repo, Path-specific glob matching (`applyTo`) | Flat aggregation. Relies on internal prompt assembly logic. | Global (`.github/copilot-instructions.md`), Path-specific (`.instructions.md`). |
| **Windsurf** | Always On, Glob match, Model Decision (semantic evaluation of rule description), Manual | Hierarchical: Evaluates descriptions to determine relevance before injecting full rule context. | Global (`~/.windsurf`), Workspace (`.windsurf/rules/`), recursive directory discovery. |
| **Roo Code** [8] | Persona/Mode activation (Code, Architect, Debug), Intent-based regex triggers | Strict cascading priority: Language > Global > Mode-Specific > AGENTS.md > General rules. | Global (`~/.roo`), Workspace (`.roo/rules/`), Mode-specific (`rules-{modeSlug}`). |
| **Continue.dev** [9] | Configuration-bound via `config.yaml`, Model Roles | Explicit assignment (e.g., binding specific rules/prompts to Chat vs Autocomplete roles). | Global/User (`~/.continue/config.yaml`), Workspace context providers. |

**Common Primitives:** All platforms support a form of Global/Always-On loading, Path/Glob-based targeting, and Manual inclusion. These form the intersection set that a portable routing specification can target.

**Non-Portable Features:** Roo Code's deep binding of rules to specific operational modes/personas (e.g., isolating file access restrictions to "Architect Mode") lacks direct equivalents in Copilot or Continue.dev.

---

## Security Model of Behavioral Instructions

Because AI instructions in enterprise settings define safety boundaries, access controls, and prohibited actions, they represent a critical attack surface.

### 1. Prompt Injection via Instruction Files

Behavioral specification files (Layer 1) are highly vulnerable to prompt injections. Security research has documented the "Zero-Click Config" attack chain: an attacker places a malicious payload containing invisible Unicode characters or zero-width sequences inside a `.cursorrules` or `.clinerules` file. When a developer clones the repository and opens the AI IDE, the IDE automatically parses the rules file as a trusted configuration. The injected instructions can immediately execute arbitrary shell commands (e.g., CVE-2026-22708, involving manipulation of shell environment variables to hijack execution).

### 2. Privilege Escalation via MCP Tools

If an MCP Tool (Layer 3) delivers a prompt or data payload that contradicts a behavioral instruction (Layer 1), it creates a privilege escalation risk. The Instruction Hierarchy dictates that System Messages (Layer 1) must take absolute precedence over Tool Outputs (Layer 3) [2]. However, many current AI tools lack strict architectural segregation, allowing "Tool Poisoning" — where a malicious instruction embedded in an external API response overrides the repository's safety guardrails, resulting in unauthorized operations.

### 3. Instruction Integrity and Verification

To prevent the silent modification of AI rules by malicious actors or rogue agents, integrity mechanisms are required. OpenSpec mitigates this through its immutable archive design; because Delta Specs are generated during the `/opsx:propose` phase and merged via `/opsx:archive`, all changes to system behavior generate a deterministic, version-controlled execution trace [10].

### 4. OWASP AI Security Top 10 Mapping

- **LLM01: Prompt Injection:** Directly maps to the exploitation of `.cursorrules`/`.clinerules` files via hidden markdown or malicious repository cloning.
- **LLM06: Excessive Agency:** Maps to the failure of Layer 1 constraints to properly bound the tools exposed at Layer 3 (MCP).
- **AST10 (Agentic Skills Top 10):** Specifically addresses vulnerabilities in reusable behavioral contracts, highlighting the need for secure parsers and sandboxed loading of skills and rule files.

---

## Actionable Portability Strategy

Achieving true AI instruction portability across fragmented tools requires a phased, layered approach.

### Tier 1: Semantic Portability (Achievable Today)

Writing instructions in a platform-agnostic, standardized semantic format.

- **Strategy:** Utilize the RFC 2119 specification (MUST, SHOULD, MAY) to clearly delineate absolute behavioral constraints from optional guidelines. Avoid tool-specific XML tags or proprietary routing descriptions.
- **Support:** Universally supported by all LLMs, as it relies on linguistic comprehension rather than platform routing engines.

### Tier 2: Structural Portability (Achievable Today)

Using a hub-and-spoke architecture where a canonical source of truth drives the generation of platform-specific files.

- **Strategy:** Implement OpenSpec as the Layer 2 governance framework. Maintain behavior contracts in `openspec/specs/`. When migrating a team from GitHub Copilot to Cursor, the development team uses an agent to read the OpenSpec source of truth and automatically generate corresponding `.cursor/rules/*.mdc` files with the correct YAML frontmatter.
- **Blockers:** The generation of the downstream platform files remains a manual orchestration step (e.g., executing a script or prompt to translate the spec into `.clinerules`).

### Tier 3: Schema Portability (Future State)

A standardized, machine-readable schema for Layer 1 that any compliant AI tool can natively parse.

- **Strategy:** The adoption of standards like the CoSAI Universal Agentic Skill Format or IEEE P3394 Agent Behavioral Contracts.
- **Target Architecture:** A developer writes a single behavioral specification using a strictly typed schema (e.g., YAML mapping Preconditions, Invariants, and Routing). OpenSpec governs the lifecycle of this schema via Delta proposals, and the IDE (whether Cursor, Roo Code, or Copilot) natively ingests the schema without translation.

---

## Gap Analysis and Standardization Roadmap

| Identified Gap | Current Best Mitigation | Responsible Standards Body / Initiative |
|---------------|------------------------|----------------------------------------|
| No Formal Layer 1 Schema for behavioral instructions and constraints. | Anthropic's Constitutional AI principles [3]; OpenSpec's RFC 2119 enforcement. | IEEE P3394 (Agent Behavioral Contracts); **OASIS CoSAI** (Universal Agentic Skill Format). |
| Fragmented Routing Models (YAML vs Globs vs Modes). | Structural portability via OpenSpec hub-and-spoke derived file generation. | W3C AI Agent Protocol CG (Agent description and discovery standards) [11]. |
| Prompt Injection via Rule Files (`.cursorrules` Zero-Click Config). | Instruction Hierarchy (System Message prioritization) [2]; Sandboxed file loading. | OWASP GenAI Security Project (LLM01 / AST10 frameworks). |
| Lack of Instruction Integrity and auditability across sessions. | OpenSpec immutable archiving and phase-gated `/opsx:verify` validation [6]. | ISO/IEC JTC 1/SC 42 (ISO/IEC 42001 AI Management System Standards). |
| Privilege Escalation via MCP Tool output poisoning. | Context isolation; strict parsing of MCP Tool execution payloads. | Model Context Protocol (MCP) specification governance. |