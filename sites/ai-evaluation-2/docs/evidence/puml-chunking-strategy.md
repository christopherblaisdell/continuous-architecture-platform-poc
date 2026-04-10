<!-- CONFLUENCE-PUBLISH -->

# The PlantUML Problem: Why Architecture Diagrams Break AI Context

!!! abstract "TL;DR"
    PlantUML is the single worst file type for AI-assisted architecture work. It has no Tree-sitter grammar in any AI coding platform, its symbolic syntax confuses embedding models, and its `!include` directives are completely opaque to retrieval pipelines. Both Option A (GitHub Copilot) and Option C (Azure AI Search / Foundry IQ) require custom workarounds — but they take fundamentally different approaches. Option A generates companion Markdown files via CI/CD that Copilot indexes natively. Option C pre-processes PUML into enriched Markdown with type-specific metadata extraction, uploads to blob storage, and retrieves via agentic search. This page documents both approaches with evidence from our POC.

---

## Why This Page Exists

The [File-Type Chunking Strategy](../framework/filetype-chunking-strategy.md) and the [A-vs-C comparison](filetype-handling-a-vs-c.md) both address PlantUML as one row in a multi-file-type matrix. But PlantUML deserves its own page for three reasons:

1. **It is the hardest file type for AI.** Source code has Tree-sitter. Markdown has heading-aware chunking. YAML has key-value parsing. PlantUML has *nothing* — every AI platform treats it as generic plain text.

2. **It is central to architecture work.** This workspace contains 314 canonical PUML files across 6 diagram types (sequence, C4, ERD, event flow, topology, application). These diagrams are the primary artifacts that document service interactions, data models, and system boundaries.

3. **We built and tested a solution.** The POC includes a working `puml-enricher.py` that pre-processes all 314 files into search-optimized Markdown — providing concrete evidence of what Option C's workaround actually looks like, instead of theoretical analysis.

**Research basis:** Two independent deep research rounds — [PlantUML Diagram Chunking](../research/deep-research-results-plantuml-chunking.md) (detailed analysis of Copilot's native PUML behavior, Tree-sitter gaps, and workaround strategies) and [PlantUML and OpenAPI Combined](../research/deep-research-results-puml-openapi-chunking.md) (strategy comparison and ranking).

---

## The Fundamental Problem

### No Tree-sitter Grammar

GitHub Copilot relies on [Tree-sitter](https://tree-sitter.github.io/) to parse source code into Abstract Syntax Trees (ASTs). For Java, Python, TypeScript, and 170+ other languages, Tree-sitter identifies function boundaries, class definitions, and scope blocks — enabling semantic chunking that preserves logical relationships.

**PlantUML is completely absent from the Tree-sitter ecosystem.** Two experimental community grammars exist (`lyndsysimon/tree-sitter-plantuml` and `Decodetalkers/tree_sitter_plantuml`), but both are abandoned or pre-release. The Tree-sitter grammar organization is not currently accepting new language submissions.

This means every AI coding platform — Copilot, Cursor, Windsurf, Claude Code — treats `.puml` files as generic, unstructured text.

### The 60-Line Sliding Window

Without a Tree-sitter AST, Copilot falls back to the `FixedWindowJaccardMatcher` — a 60-line sliding window with Jaccard similarity scoring. This algorithm slices the file into overlapping 60-line chunks, computes the intersection-over-union of lexical tokens between each chunk and the query, and ranks results.

This is catastrophic for architecture diagrams. In a typical sequence diagram:

- **Lines 1-20**: Participant and actor declarations — the *nouns* of the system
- **Lines 70-150**: Runtime interactions, API calls, response flows — the *verbs* of the system

A 60-line window physically isolates interactions from the entities they connect. The chunk containing `svc_check_in -> svc_reservations : GET /reservations` completely lacks the earlier declarations that define what those services are, what protocols they use, or which domain they belong to.

**The model receives the action but not the actors.**

### Embedding Model Failure

Even if the right chunks are retrieved, the vector similarity computation fails on PlantUML syntax. Embedding models (OpenAI `text-embedding-3-small`, Azure `text-embedding-ada-002`) are trained primarily on natural language prose and structured programming languages.

PlantUML's symbolic operators create noise in the embedding space:

| Syntax | Meaning | Embedding Quality |
|--------|---------|-------------------|
| `-->` | Asynchronous call | Noise |
| `->` | Synchronous call | Noise |
| `-[#red]>o` | Optional error path | Noise |
| `->>` | Return response | Noise |
| `activate svc` | Start activation scope | Noise |
| `alt condition` | Conditional branch | Low |
| `note right` | Annotation | Low |

A natural language query like "which services does svc-check-in call?" has low cosine similarity against the dense symbolic syntax `svc_check_in -> svc_reservations : GET /reservations/{id}`. The literal tokens barely overlap — "services," "does," and "call" appear nowhere in the PUML line.

### !include Opacity

Enterprise architecture teams use `!include` directives to standardize diagrams, particularly with the C4 model macro library:

```plantuml
!include https://raw.githubusercontent.com/.../C4_Component.puml
Container(api, "API Gateway", "Spring Boot")
Rel(api, db, "Reads from", "JDBC")
```

Copilot treats `!include` as an opaque string literal. It does not fetch the remote URL, does not resolve local file paths, and does not inject macro definitions. The LLM sees `Container()` and `Rel()` as undefined function calls with no semantic meaning.

Azure AI Search has the same limitation amplified: blob indexers operate on isolated blobs with no file system context. They cannot follow `!include` references at all — each blob is processed in complete isolation.

### SVG Exclusion

PlantUML renders to SVG, which contains highly structured XML `<text>` nodes with the diagram's exact content. These nodes are more searchable than the raw PUML syntax. However, Copilot explicitly excludes `**/*.svg` from its workspace index. Azure AI Search can index SVGs but treats them as XML text without understanding the diagram semantics.

The rendered output — which is actually more parseable than the source — is invisible to both platforms.

---

## What an Ideal Parser Would Extract

Before comparing workarounds, it is useful to define what a perfect PlantUML parser would produce — the gold standard against which our workarounds are measured.

| PUML Element | Architectural Purpose | What Plain Text Loses | Ideal Extraction |
|-------------|----------------------|----------------------|-----------------|
| `participant`, `actor`, `database` | System entities — the nouns | Alias mapping lost; entity type classification lost | Global entity registry with aliases resolved to full service names |
| `->`, `-->`, `->>` | Call relationships — the verbs | Directionality confused by embeddings; dense punctuation is noise | Directed adjacency list: `source -> target via protocol` |
| `Container()`, `System()`, `Rel()` | C4 model abstractions | Opaque function calls — parameters have no meaning without `!include` | Structured objects: `{type: "Container", name: "API", tech: "Java"}` |
| `activate`, `alt`, `loop`, `opt` | Control flow and error paths | 60-line chunks split `alt` from `else` — execution path context destroyed | Nested execution tree isolating happy path from error handling |
| `note right`, `note over` | Design rationale — why an interaction exists | Multi-line notes truncated at chunk boundaries | Note text bound as property of the specific relationship or actor |
| `!include`, `!define` | Modularity and standards enforcement | Dead references; external dependencies never fetched | Recursively resolved definitions injected into the knowledge graph |
| `entity`, `--`, `*--` | ERD relationships and cardinality | Cardinality symbols are embedding noise | Structured entity-relationship tuples with cardinality labels |

**The gap is structural.** Plain-text lexical search treats an architecture diagram as a flat, linear sequence of words. In PlantUML, physical proximity in the text does *not* equate to logical proximity. A participant defined on line 5 might not interact with another system until line 120.

---

## Option A: GitHub Copilot Native Workarounds

Option A cannot change how Copilot chunks `.puml` files — there are no configuration controls for chunking behavior. Instead, it uses four layered strategies to compensate.

### Strategy 1: CI/CD Companion Markdown Generation (Primary)

The highest-ranked non-MCP approach in both deep research rounds. A CI pipeline parses `.puml` files and generates structured Markdown summaries that Copilot indexes with near-perfect accuracy.

**How it works:**

1. A CI script (GitHub Actions, pre-commit hook) triggers on any commit containing `.puml` modifications
2. The script parses each PUML file — extracting participants, relationships, call flows, and error paths
3. It generates a companion file (e.g., `svc-check-in-sequence.summary.md`) containing a human-readable summary
4. The companion file is committed to the repository alongside the PUML source
5. Copilot indexes the Markdown file using its heading-aware chunker — the entire architectural context is preserved

**Example output:**

```markdown
## Diagram: svc-check-in POST /check-ins

### Participants
- MobileClient (actor)
- svc-check-in (service)
- svc-reservations (external dependency)

### Call Flow
1. MobileClient sends POST /check-ins to svc-check-in
2. svc-check-in validates the reservation via GET /reservations/{id} from svc-reservations
3. svc-reservations returns 200 with reservation details
4. svc-check-in creates the check-in record and returns 201
```

**Limitations:**

- Companion files must be kept in sync with PUML sources — drift is the primary operational risk
- The parsing script must be maintained as PUML conventions evolve
- Generated files consume repository storage and Git history
- The parser operates on text patterns, not a true AST — complex diagrams may be incompletely parsed
- CI pipeline adds build time

### Strategy 2: Structured Embedded Comments

Embedding natural-language comment blocks at the top of each PUML file improves the quality of Copilot's 60-line window retrieval:

```plantuml
' @architecture-summary
' This sequence diagram illustrates the check-in orchestration process.
' Primary actors: MobileClient, WebFrontend.
' Core services: svc-check-in, svc-reservations.
' Flow: Client authenticates, calls check-in, which validates the reservation.
@startuml
...
```

The comment block is physically adjacent to the participant declarations, increasing the probability that both appear in the same 60-line chunk. Copilot's embedding model handles the natural language in the comments far better than the symbolic PUML syntax.

**Limitations:** Manual authoring, risk of comment-to-diagram drift, does not help with diagrams whose interactions span beyond line 60.

### Strategy 3: Scoped Instructions

A `.github/instructions/plantuml.instructions.md` file with `applyTo: "**/*.puml"` teaches Copilot how to interpret PUML syntax:

```markdown
When analyzing .puml files:
- Treat `->` as a synchronous HTTP call
- Treat `-->` as an asynchronous event
- When encountering `Rel(A, B, ...)`, map this to a dependency where A relies on B
- Always search for the corresponding OpenAPI spec in architecture/specs/ to verify payloads
```

**Limitations:** Instructions guide the LLM's reasoning but do not fix the underlying retrieval problem. If the right chunks are not retrieved, no instruction can compensate.

### Strategy 4: PlantUML MCP Server (Future)

The Infobip PlantUML MCP server enables the LLM to generate, validate, and render PlantUML code on demand — bypassing the native indexing pipeline entirely. Community implementations exist but require evaluation for enterprise suitability.

**Limitations:** MCP servers are dynamic tools for diagram generation and validation, not for bulk architectural search. They complement retrieval but do not replace it.

### Option A Cost Summary

| Component | Effort | Ongoing Cost |
|-----------|--------|-------------|
| Companion Markdown CI script | 1-3 days initial development | CI build time; script maintenance |
| Structured comments convention | Hours (documentation + team adoption) | Manual authoring discipline |
| Scoped instructions file | Hours | Near zero |
| MCP server evaluation | Days | Server hosting + maintenance |
| **Total** | **~1 sprint** | **Low** |

---

## Option C: Foundry IQ with PUML Enricher (POC Evidence)

Option C takes a fundamentally different approach. Instead of compensating for poor retrieval at the instruction or CI layer, it **pre-processes PUML files into enriched Markdown documents** that are uploaded to Azure Blob Storage and indexed by Azure AI Search. The Foundry IQ knowledge base then retrieves these enriched documents via agentic search.

### The puml-enricher.py Pipeline

Built and tested during this POC, `puml-enricher.py` is a purpose-built pre-processor that converts raw PUML files into search-optimized Markdown documents with type-specific metadata extraction.

**Pipeline architecture:**

```
314 canonical PUML files
    ↓ classify_diagram() — 6 type classifiers
    ↓ type-specific enrichment function
    ↓ structured Markdown with metadata headers
    ↓ .enriched-puml/ output directory (311 files)
    ↓ sync-content-to-blob.py uploads to Azure Blob
    ↓ Azure AI Search indexer processes blobs
    ↓ Foundry IQ KB retrieves via agentic search
```

### Type-Specific Extraction

Unlike Option A's generic companion file approach, the enricher classifies each diagram and applies type-specific extraction logic:

| Diagram Type | Count | Extraction Logic |
|-------------|-------|-----------------|
| **Sequence** | 243 | Participant list, API call inventory (method + path), cross-service dependencies, response codes, activation scopes, error paths (alt/else blocks), ADR references, inline notes |
| **C4 Context** | 36 | System/container definitions with technology annotations, relationship graph with protocol labels, boundary groupings, external system declarations |
| **ERD** | 23 | Entity names, field lists with types, relationship cardinalities (one-to-many, many-to-many), primary/foreign key identification |
| **Event Flow** | 6 | Kafka topic names, producer/consumer pairs, event types, cross-domain event routing |
| **Topology** | 2 | Domain-to-service mappings, inter-domain communication paths |
| **Other** | 1 | Generic participant and relationship extraction |

### Enriched Output Structure

Each enriched Markdown document contains three sections:

**1. Structured metadata header** — machine-readable key-value pairs:

```markdown
# Sequence Diagram: svc-check-in POST /check-ins

- **Service**: svc-check-in
- **Endpoint**: POST /check-ins
- **Diagram type**: sequence
- **Source file**: portal/docs/microservices/puml/svc-check-in--post-check-ins.puml
```

**2. Natural-language description** — search-optimized prose:

```markdown
## Participants

This diagram involves 4 participants:
- **MobileClient** (actor) — the mobile application initiating check-in
- **svc-check-in** — the check-in orchestrator service
- **svc-reservations** — validates reservation existence
- **db-check-ins** (database) — persists check-in records

## API Calls

This flow makes the following API calls:
1. POST /check-ins — initiated by MobileClient to svc-check-in
2. GET /reservations/{id} — svc-check-in validates with svc-reservations

## Cross-Service Dependencies

svc-check-in depends on: svc-reservations (synchronous REST)
```

**3. Raw PUML source** — preserved for reference and exact-match queries:

```markdown
## Raw PlantUML Source

    ```plantuml
    @startuml
    participant MobileClient
    participant "svc-check-in" as checkin
    ...
    @enduml
    ```
```

### POC Results

| Metric | Value |
|--------|-------|
| Files processed | 311 of 314 canonical PUML files |
| Input size | 590 KB total raw PUML |
| Output size | 846 KB enriched Markdown |
| Enrichment ratio | 1.4x (additional context generated per file) |
| Largest output | Under 32 KB (Lucene single-document limit) |
| Processing time | Under 5 seconds for all 311 files |
| Type coverage | 6 diagram types with dedicated extractors |

### Why Enrichment Works for Search

The enrichment transforms symbolic PUML syntax into the format that embedding models handle best — natural language prose with structured metadata:

| Query | Raw PUML Match Quality | Enriched Match Quality |
|-------|----------------------|----------------------|
| "which services does svc-check-in call?" | LOW — `svc_check_in -> svc_reservations` has poor cosine similarity to the query | HIGH — "svc-check-in depends on: svc-reservations (synchronous REST)" directly matches |
| "what tables does the reservation service use?" | VERY LOW — `entity reservations` buried in ERD syntax | HIGH — "Entity: reservations" with field list in structured format |
| "how does check-in validate waivers?" | LOW — arrow syntax `checkin -> safety : GET /waivers` is opaque | HIGH — "svc-check-in validates waivers via GET /waivers from svc-safety-compliance" |
| "which events does svc-check-in publish?" | LOW — Kafka topic references scattered across event flow diagrams | HIGH — "Producer: svc-check-in publishes check-in.completed to topic check-in-events" |

### Option C Cost Summary

| Component | Effort | Ongoing Cost |
|-----------|--------|-------------|
| `puml-enricher.py` development | 1 day (built in POC) | Script maintenance |
| Blob upload pipeline integration | Hours (added to existing `sync-content-to-blob.py`) | Azure Blob storage (~$0.01/month for 846 KB) |
| Azure AI Search indexing | Zero (uses existing indexer) | Included in existing S1 tier (~$250/month) |
| Foundry IQ KB configuration | Zero (uses existing KB) | Included in existing Azure OpenAI deployment |
| **Total incremental** | **~1 day** | **Negligible** (infrastructure already provisioned) |

!!! warning "Infrastructure Context"
    The "negligible" ongoing cost assumes the Azure AI Search S1 tier and Azure OpenAI deployment already exist for other purposes. If PUML enrichment were the *only* reason to provision this infrastructure, the cost would be ~$250/month for AI Search alone — making Option A's CI/CD approach more cost-effective. The low incremental cost is only realized because Option C's infrastructure serves the entire architecture knowledge base, not just PUML files.

---

## Head-to-Head Comparison

| Dimension | Option A (Copilot + CI/CD) | Option C (Foundry IQ + Enricher) |
|-----------|---------------------------|----------------------------------|
| **Enrichment approach** | Companion Markdown generated by CI script | Enriched Markdown generated by `puml-enricher.py` |
| **Type awareness** | Generic parsing — no diagram-type-specific logic | 6 dedicated extractors (sequence, C4, ERD, event flow, topology, app) |
| **Metadata extraction** | Participant list + call flow summary | Structured metadata headers + natural-language descriptions + raw source preservation |
| **Retrieval mechanism** | Copilot native workspace indexer (heading-aware Markdown chunking) | Azure AI Search with semantic ranker and agentic retrieval |
| **Query capability** | `@workspace` full-text + vector search; agent can also read files directly | KB retrieve API with answer synthesis mode; agent cannot read source files |
| **!include resolution** | Not resolved — companion file must include the resolved information manually | Not resolved — enricher extracts macro *usage* but does not resolve definitions |
| **Maintenance model** | CI pipeline must regenerate on every PUML commit | Enricher runs as a sync step; blob upload pipeline handles distribution |
| **Staleness prevention** | CI validation check — fail build if companion is stale | Sync script re-uploads on every run; index auto-rebuilds |
| **Direct file access** | YES — Copilot agent can read the raw PUML file directly via workspace tools | NO — only retrieves indexed chunks from the knowledge base |
| **Infrastructure cost** | Zero (CI/CD is free in GitHub Actions) | ~$250/month for Azure AI Search S1 (shared with other content types) |
| **Development effort** | 1-3 days for CI script | 1 day for enricher (demonstrated in POC) |
| **File count overhead** | 1 companion file per PUML = 311 extra files in git | 311 enriched files in blob storage only (not in git — `.enriched-puml/` is gitignored) |

### Where Option A Wins

1. **Direct file access.** When the architect asks about a specific diagram, Copilot can read the entire raw PUML file — no chunking, no retrieval, no embedding. This bypasses all indexing limitations for targeted queries.

2. **Zero infrastructure.** Companion files live in git. There is nothing to provision, monitor, or pay for.

3. **Cheaper at small scale.** For a team with 50 PUML files, a simple CI script is clearly the right approach.

### Where Option C Wins

1. **Type-specific extraction.** The enricher applies different extraction logic for sequence diagrams (API calls, response codes), ERDs (entities, cardinalities), C4 diagrams (container definitions, technology annotations), and event flows (topics, producers, consumers). Option A's companion script would need to implement the same logic — and if it does, the approaches converge.

2. **Separation of concerns.** Enriched files are not committed to git — they exist only in blob storage. The repository stays clean. Option A adds 311 companion files to the git history.

3. **Search quality.** Azure AI Search with semantic ranker and BM25 hybrid retrieval is purpose-built for document search. Copilot's `@workspace` search is good but optimized for code, not architecture documentation.

4. **Scalability.** As the workspace grows beyond Copilot's index limits (currently generous but not unlimited), having a dedicated search index becomes valuable.

### Where They Converge

Both approaches ultimately do the same thing: **convert opaque PUML syntax into searchable Markdown.** The difference is where the Markdown lives (git vs blob), how it is retrieved (Copilot indexer vs AI Search), and how sophisticated the extraction logic is (generic vs type-specific).

If Option A's CI script implements type-specific extraction (sequence-aware, ERD-aware, C4-aware), the quality gap narrows substantially. The remaining difference is infrastructure cost vs git clutter.

---

## Strategy Ranking

Based on both deep research rounds and POC evidence, here is the consolidated ranking of PlantUML context injection strategies:

| Rank | Strategy | Quality | Effort | Automation | Best For |
|------|----------|---------|--------|------------|----------|
| 1 | **CI/CD companion Markdown** (Option A) or **Enricher + Blob** (Option C) | HIGH | LOW-MEDIUM | Full | Production use — either approach works; choose based on infrastructure posture |
| 2 | **Structured embedded comments** | MEDIUM | LOW | Manual | Quick improvement with zero tooling; complements Strategy 1 |
| 3 | **PlantUML MCP server** (Infobip) | HIGH | MEDIUM | Dynamic | Interactive diagram generation and validation; does not replace retrieval |
| 4 | **Scoped `.instructions.md`** | LOW-MEDIUM | LOW | Automatic | Baseline improvement; always deploy regardless of other strategies |
| 5 | **File naming conventions** | LOW | LOW | Manual | Improves lexical search fallback; always deploy |
| 6 | **Direct file read** (Option A only) | HIGH | Zero | On-demand | When the architect knows which diagram to examine |
| 7 | **Raw PUML indexing** (either platform) | VERY LOW | Zero | Automatic | Last resort — unreliable for anything beyond exact string matches |

---

## Recommendation

For teams evaluating Option A vs Option C specifically for PlantUML handling:

**If you are already using Copilot and have no Azure AI Search infrastructure:** Implement companion Markdown generation via CI/CD (Strategy 1, Option A variant). Add structured comments and scoped instructions as baseline improvements. The total effort is 1-3 days and the ongoing cost is zero.

**If you already have Azure AI Search provisioned for other purposes:** The enricher approach (Strategy 1, Option C variant) is incrementally cheap (~1 day of development, negligible ongoing cost) and produces higher-quality retrieval due to type-specific extraction and purpose-built search infrastructure. But it only makes sense if the infrastructure is already justified by other use cases.

**PlantUML alone does not justify provisioning Azure AI Search.** The $250/month S1 tier cost is not warranted for 311 files that could be served by a free CI/CD companion script. Option C's PUML handling is a *benefit* of infrastructure provisioned for the full architecture knowledge base — not a reason to provision it.

---

**See also:**

- [File-Type Chunking Strategy](../framework/filetype-chunking-strategy.md) — full file-type decision matrix for Copilot
- [File-Type Handling: A vs C](filetype-handling-a-vs-c.md) — multi-file-type comparison across platforms
- [Deep Research: PlantUML Chunking](../research/deep-research-results-plantuml-chunking.md) — detailed analysis of Copilot's native PUML behavior
- [Deep Research: PlantUML and OpenAPI Combined](../research/deep-research-results-puml-openapi-chunking.md) — strategy ranking and comparison tables
- [Controlling What Copilot Sees](context-injection-controls.md) — how Copilot's context pipeline works
- [Build vs Leverage](build-vs-leverage.md) — the broader platform vs product analysis
