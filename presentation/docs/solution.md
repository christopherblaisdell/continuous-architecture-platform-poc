# The Solution: A Shared Workspace for the Architecture Practice

## Build on What Already Exists

Many architecture practices already source-control OpenAPI specs and diagrams. They already gate production deployments through an architecture repository. **That foundation is the hardest part — and many teams have already achieved it.**

The shared solution adds four capabilities on top of that foundation, closing the two gaps that erode its value over time. No MCP servers to build. No custom infrastructure. Copilot indexes the workspace automatically.

---

## The Four Pillars

### 1. AI-Assisted Architecture Workflows

An AI assistant in VS Code that reads the architecture Git repo — the same specs, diagrams, and source code architects already maintain — and produces compliant artifacts automatically.

**What it does:**

- Triages tickets for architectural significance
- Investigates production issues using logs, source code, and API specs
- Generates MADR-formatted Architecture Decision Records
- Creates solution designs following arc42 structure
- Updates Swagger/OpenAPI specs from approved designs
- Produces PlantUML and C4 model diagrams

---

### 2. Enhanced Architecture Workspace

The architecture repository is enhanced with **AI-readable context** — architecture standards (MADR, C4, arc42), domain knowledge, anti-pattern checklists, and a growing library of solution designs — so the AI agent operates with the same expertise as a senior architect.

**Why this matters:**

- The AI reads the actual OpenAPI specs already version-controlled (no hallucination)
- A `copilot-instructions.md` file encodes 500+ lines of domain knowledge, loaded into every AI session
- Previous architectural decisions inform new ones — automatically
- The workspace gets richer with every project — each design becomes context for the next

---

### 3. Solution Designs in Markdown (Extending Git-First)

The platform extends the Git-first practice to **solution designs, ADRs, impact assessments, and service documentation** — all authored in Markdown, all version-controlled in the shared architecture repository.

**What this enables:**

- **Pull request reviews** on architecture decisions, not just specs
- **AI-readable history** — the agent can analyze and cross-reference past designs
- **Searchable decision log** — ADRs indexed and discoverable, not buried in ticket branches
- **Publishable everywhere** — MkDocs portal, Confluence API sync, PDF export from one source

---

### 4. Automated Publishing (Replacing the Manual Wiki Step)

The voluntary wiki update — the step that gets skipped — is replaced by a `git push` that automatically publishes a browsable architecture portal. No manual copy-paste. No "I'll update the documentation later."

**What gets published automatically:**

- Microservice deep-dive pages with endpoint sequence diagrams
- Interactive Swagger UI for every service
- Clickable C4 system context diagrams
- Global ADR decision log
- Service architecture baselines

---

## How It All Fits Together

``` mermaid
flowchart LR
    A[Architecture Ticket] --> B[AI-Assisted Design\nin VS Code]
    B --> C[Markdown Artifacts +\nUpdated Specs in Git]
    C --> D[git push]
    D --> E[Automated Build\n+ Publishing Pipeline]
    E --> F[Living Architecture\nPortal]
    E --> G[Confluence Sync\noptional]
    F --> H[Next AI Session\nricher context]
    H --> B

    style B fill:#00897b,color:#fff
    style F fill:#ff8f00,color:#fff
    style H fill:#37474f,color:#fff
```

<div class="key-insight" markdown>
**Compounding returns:** Every artifact the AI produces becomes context for the next session. The workspace grows richer. The AI gets more accurate. The documentation stays current — not because someone remembers to update the wiki, but because publishing is automated.
</div>

---

## Demonstrated Capabilities

This POC demonstrates a complete architecture platform using NovaTrek Adventures as a synthetic case study. Everything described here **exists and is deployed**:

| Component | Status | Evidence |
|-----------|--------|----------|
| AI-assisted workflow | Proven | 5 scenarios executed, 39 files produced |
| Enhanced architecture workspace | Built | Existing specs + AI instructions + standards + domain model |
| Markdown-first artifacts | Produced | 39 files across 5 scenarios |
| Automated publishing pipeline | Live | Architecture portal deployed at Azure Static Web Apps |
| Cost comparison | Definitive | Actual billing data from both toolchains |

<div class="cta-box" markdown>

### See the cost evidence

[Cost Evidence: Toolchain Comparison](cost-evidence.md)

</div>
