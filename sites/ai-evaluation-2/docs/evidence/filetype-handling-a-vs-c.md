<!-- CONFLUENCE-PUBLISH -->

# File-Type Handling: Option A vs Option C

!!! abstract "TL;DR"
    Azure AI Search (Option C) does not provide meaningfully better chunking than GitHub Copilot (Option A) for most architecture file types out of the box. For the two file types where Option C *can* deliver better results — Markdown and OpenAPI YAML — one requires only a configuration toggle (Markdown) and the other requires a custom Azure Functions skillset (OpenAPI). For source code, Copilot is strictly superior. The engineering investment to bring Option C up to parity with Option A's workarounds exceeds the benefit for a team of this size.

## Why This Comparison Matters

The [File-Type Chunking Strategy](../framework/filetype-chunking-strategy.md) thoroughly documents where GitHub Copilot's native indexer struggles — PlantUML diagrams get 60-line sliding windows, OpenAPI `$ref` pointers are severed, YAML key hierarchies are ignored. But documenting Option A's weaknesses is not the same as demonstrating Option C's strengths. A stakeholder could reasonably ask:

> "You say PlantUML chunks poorly in Copilot — but would a custom Foundry IQ pipeline actually chunk it better?"

This page answers that question with evidence. For each architecture file type, it compares what both platforms deliver by default, what workarounds each requires, and whether the engineering investment for Option C produces a meaningfully better outcome.

**Research basis:** [Deep research on Azure AI Search chunking mechanics](../research/deep-research-results-azure-ai-search-chunking-fast.md) — covering document cracking, Text Split cognitive skill, integrated vectorization, custom skillsets, Foundry IQ agentic retrieval, and file-type-specific analysis across 49 sources including Microsoft Learn documentation.

---

## Option C File-Type Decision Matrix

This matrix mirrors the structure of the [existing Copilot matrix](../framework/filetype-chunking-strategy.md#file-type-decision-matrix) but evaluates Azure AI Search (the retrieval engine behind Foundry IQ).

| File Type | Default Azure AI Search Behavior | Chunking Quality (Default) | Available Customization | Custom Skillset Required? | Engineering Effort | Target State |
|-----------|----------------------------------|---------------------------|------------------------|--------------------------|-------------------|-------------|
| **Java / TypeScript / Python source code** | Plain text, token-window chunking. No AST awareness, no function-level boundaries. | LOW — no code structure recognition; a function crossing the token limit is split mid-body | Custom Azure Functions skillset implementing Tree-sitter or similar AST parsing | Yes — must build AST-based chunking from scratch | HIGH (weeks) | Parity with Copilot's native AST chunking — but Copilot does this for free |
| **Markdown ADRs and solution designs** | Header-aware parsing via `parsingMode: markdown`. Splits by H1/H2/H3 into separate search documents. | HIGH — recognizes heading hierarchy and keeps section content together | Built-in; no custom skill needed. Configuration change only. | No | LOW (hours) | Each MADR section (Context, Decision Drivers, Decision Outcome) indexed as a discrete, retrievable unit |
| **OpenAPI YAML specs (small, <150 lines)** | Plain text extraction. YAML structure ignored; `$ref` pointers treated as opaque strings. | LOW — same quality as any plain text file under the token limit; no schema awareness | Custom skillset to parse YAML and chunk by endpoint definition | Yes — YAML-aware OpenAPI parser in Azure Functions | HIGH (days-weeks) | Per-endpoint chunks with resolved schemas — semantically complete |
| **OpenAPI YAML specs (large, >150 lines)** | Plain text, token-window split. A 500-line spec is split into ~3-4 chunks with no regard for endpoint boundaries. `$ref` pointers severed. | VERY LOW — endpoint definitions separated from their schemas; worse than Copilot because no Jaccard overlap scoring | Custom skillset to dereference `$ref` pointers and produce per-endpoint chunks | Yes — full OpenAPI spec resolution logic | HIGH (weeks) | Fully dereferenced endpoint chunks with complete schemas |
| **AsyncAPI event specs** | Plain text. Same limitations as OpenAPI — channel definitions separated from message schemas. | LOW — no event-specific awareness | Custom skillset for channel-aware chunking | Yes — AsyncAPI parser in Azure Functions | HIGH (days-weeks) | Per-channel chunks linking event schema to producer |
| **YAML metadata files (capabilities, tickets, domains)** | Single chunk if file is under the token limit (~5,000 characters default). YAML key hierarchy is ignored. | MEDIUM — small files indexed as single units (adequate); large files split without structure awareness | Custom skillset for hierarchy-aware chunking (only needed for large files) | No (small files) / Yes (large files) | LOW (small) / MEDIUM (large) | Adequate for small files; large files need custom parsing |
| **PlantUML diagrams (.puml)** | Not recognized as structured content. Treated as unknown text. `!include` directives ignored — external components invisible. | VERY LOW — participant declarations severed from message flows; raw syntax is poor for vector embedding | Custom skillset to parse PlantUML syntax and "verbalize" diagrams into structured text (participants, relationships, message flows) | Yes — PlantUML parser or LLM-based verbalization in Azure Functions | HIGH (weeks) | Verbalized diagram descriptions that are retrievable by architectural concept |
| **Figma wireframes** | Not indexable — hosted on figma.com. No direct connector for external URLs (Bing indexing is public web only). Design token JSON exports treated as flat text. | NONE (external) / LOW (JSON exports) | Custom skillset to parse design token JSON hierarchy | Yes — JSON structure parser for design tokens | MEDIUM (days) | Design token values linked to their component categories |
| **Configuration YAML (small files)** | Single chunk for files under ~100 lines. Structure ignored but content is complete. | MEDIUM — adequate for small files; entire file fits in one chunk | None needed for small files | No | NONE | Already adequate |
| **Confluence-migrated Markdown** | Header-aware parsing (same as regular Markdown if properly structured). | MEDIUM-HIGH — heading-aware if Pandoc output has clean hierarchy | Built-in Markdown parsing. May need post-migration heading cleanup. | No | LOW | Clean heading hierarchy enables section-level retrieval |

### Key Observations

1. **Markdown is the only file type where Azure AI Search provides a clear built-in advantage** — heading-aware parsing produces semantically coherent section chunks without any custom engineering.

2. **For every other architecture file type, Azure AI Search requires the same kind of workaround as Copilot** — custom skillsets (Option C) vs companion Markdown / MCP servers / scoped instructions (Option A).

3. **For source code, Copilot is strictly superior** — Tree-sitter AST-aware chunking is built in. Azure AI Search would require building equivalent AST parsing from scratch in Azure Functions.

4. **`$ref` resolution is unsolved by both platforms** — neither Copilot nor Azure AI Search natively dereferences YAML `$ref` pointers in OpenAPI/AsyncAPI specs. Both require external tooling (CLI bundling for Copilot, custom skillset for Azure AI Search).

---

## A-vs-C Comparison Matrix

For each file type, this table puts Options A and C side by side — comparing default behavior, required workarounds, engineering effort, and net advantage.

| File Type | Option A Default | Option A Workaround | Option A Effort | Option C Default | Option C Workaround | Option C Effort | Net Advantage | Verdict |
|-----------|-----------------|--------------------|-----------------|-----------------|--------------------|-----------------|--------------|---------|
| **Source code (Java/TS/Python)** | HIGH — Tree-sitter AST-aware, function-level chunks | None needed | None | LOW — plain text, token-window split | Custom AST skillset in Azure Functions | HIGH (weeks) | Option A is categorically better | **A wins** |
| **Markdown (ADRs, solutions)** | MEDIUM — heading-aware chunking but no semantic anchoring for nested sections | Heading structure discipline + scoped instructions | LOW (hours) | HIGH — `parsingMode: markdown` splits by H1/H2/H3 into separate documents | Config change only | LOW (hours) | Option C has a slight edge in section isolation; Option A compensates with direct file access | **Draw** |
| **OpenAPI YAML (<150 lines)** | LOW — generic YAML chunking, no schema awareness | File decomposition + scoped instructions | LOW (hours) | LOW — plain text extraction, no YAML structure | Custom OpenAPI parser skillset | HIGH (days-weeks) | Both start equally bad; A's workaround is cheaper | **A wins** |
| **OpenAPI YAML (>150 lines)** | VERY LOW — `$ref` severed, 60-line Jaccard windows | CLI bundling (`swagger-cli bundle --dereference`) + MCP server | LOW-MEDIUM (hours for CLI; days for MCP) | VERY LOW — token-window split, `$ref` severed, no overlap scoring | Custom skillset with full `$ref` resolution | HIGH (weeks) | Both need external tooling; A's CLI bundling is a one-line CI hook vs weeks of Azure Functions development | **A wins** |
| **AsyncAPI event specs** | LOW — generic YAML chunking | File decomposition + scoped instructions | LOW (hours) | LOW — plain text, no channel awareness | Custom AsyncAPI parser skillset | HIGH (days-weeks) | Same pattern as OpenAPI — A's workarounds are simpler | **A wins** |
| **YAML metadata (small)** | LOW — 60-line windows break key hierarchies | File decomposition (keep under 150 lines) | LOW (hours) | MEDIUM — fits in single chunk if under token limit | None needed for small files | None | Option C slightly better for small files (single chunk vs sliding window) | **Draw** |
| **PlantUML (.puml)** | LOW — no Tree-sitter grammar, 60-line Jaccard fallback, `!include` opaque | Companion Markdown generation + structured comments + MCP server | MEDIUM (1-3 days) | VERY LOW — unknown text format, `!include` ignored, raw syntax poorly embedded | Custom skillset to verbalize diagrams into structured text | HIGH (weeks) | Both require custom tooling; A's companion Markdown is simpler than C's verbalization skillset | **A wins** |
| **Figma wireframes** | NONE — external, not in git | Figma MCP server + design token CI export | MEDIUM-HIGH (phased) | NONE — no external URL indexing; JSON exports are flat text | Custom JSON structure skillset for design tokens | MEDIUM (days) | Both need external bridges; A's MCP approach is more direct | **Draw** |
| **Config YAML (small)** | LOW — 60-line windows | File decomposition if >150 lines | LOW | MEDIUM — single chunk for small files | None needed | None | Negligible difference for small files | **Draw** |
| **Confluence-migrated Markdown** | MEDIUM — heading-aware if structured | Post-migration heading cleanup | LOW | MEDIUM-HIGH — built-in Markdown parsing | Post-migration heading cleanup | LOW | Nearly identical outcomes | **Draw** |

### Verdict Summary

| Verdict | Count | File Types |
|---------|-------|-----------|
| **A wins** | 5 | Source code, OpenAPI (small), OpenAPI (large), AsyncAPI, PlantUML |
| **Draw** | 5 | Markdown, YAML metadata (small), Figma, Config YAML, Confluence-migrated Markdown |
| **C wins** | 0 | — |

**Option C does not win on any file type.** It draws on five file types (mostly because both platforms handle them similarly) and loses on five — including the three most problematic file types for architecture teams (OpenAPI specs, PlantUML diagrams, and source code).

---

## Analysis: Where Does Custom Infrastructure Actually Help?

### The custom skillset trap

The research reveals a pattern: Azure AI Search's default chunking is no better than Copilot's for structured technical files. The claimed advantage of Option C is the ability to build *custom skillsets* — Azure Functions that implement domain-specific parsing.

But this creates a paradox:

1. **If the file type is simple enough for default chunking to work** (Markdown, small config files), both platforms handle it adequately — no custom infrastructure needed.

2. **If the file type requires custom parsing** (OpenAPI, PlantUML, AsyncAPI), the engineering effort for Option C (Azure Functions skillsets) is *higher* than Option A's workarounds (Markdown companion files, CLI bundling, MCP servers) — while achieving similar outcomes.

3. **If the file type has native IDE support** (source code), Option A is categorically better because Copilot's Tree-sitter integration is free and automatic, while Option C would require rebuilding AST parsing from scratch.

### The direct-access factor

The comparison matrices above evaluate *retrieval quality* — how well each platform finds the right chunk when searching. But Copilot has a capability that Azure AI Search fundamentally lacks: **direct file access**.

When a Copilot agent needs to understand an OpenAPI spec, it can:

1. **Read the entire file** — no chunking, no retrieval, no embedding. The agent opens the file and reads it.
2. **Follow `$ref` pointers manually** — the agent reads the referenced file in a separate operation.
3. **Cross-reference with other files** — the agent reads metadata, source code, and ADRs in the same session.

Azure AI Search is retrieval-only. Every query returns chunks, not files. The agent cannot say "show me the full OpenAPI spec for svc-reservations" — it gets fragments ranked by relevance.

This distinction matters most for architecture work, where the architect frequently needs to read *entire* files in context rather than search for fragments. The File-Type Chunking Strategy's workarounds (scoped instructions, companion Markdown) exist for the `@workspace` search path — but the agent also reads files directly via `#file` references and tool invocations, bypassing chunking entirely.

**For file types where the agent reads the whole file (which is most architecture scenarios), chunking quality is irrelevant — and Option A provides this for free.**

### The "platform vs product" reality

The deep research confirms what the [Foundry IQ comparison page](foundry-iq-comparison.md) identified: Azure AI Search is a *platform*, not a product. Its value proposition is the modular enrichment pipeline — but that modularity requires engineering to activate.

For the architecture practice's 200-file workspace:

| What you get for free | Option A (Copilot) | Option C (Azure AI Search) |
|----------------------|--------------------|-----------------------------|
| Workspace indexing | Automatic, zero config | Requires provisioning Azure AI Search service ($74+/month), configuring data source, defining index schema, creating skillset, scheduling indexer |
| Source code awareness | Tree-sitter AST chunking (10+ languages) | Plain text token windows |
| Markdown awareness | Heading-level chunking | Heading-level chunking (comparable) |
| YAML awareness | Generic (poor) | Generic (poor) |
| PlantUML awareness | Generic (poor) | Generic (poor) |
| Direct file access | Yes — agent reads files from workspace | No — retrieval only |
| Cost | $39/seat/month (included) | $74/month base + embedding costs + custom skillset development |

### The cost-effort equation

Even if Option C delivered marginally better retrieval for some file types, the cost comparison is stark:

| Investment | Option A Workarounds | Option C Custom Skillsets |
|-----------|---------------------|--------------------------|
| **Markdown (ADRs)** | Heading discipline (hours) | Config toggle (hours) — **parity** |
| **OpenAPI specs** | `swagger-cli bundle` CI hook (hours) | Custom Azure Functions parser (weeks) |
| **PlantUML** | Companion Markdown CI script (1-3 days) | Custom verbalization skillset (weeks) |
| **Source code** | Nothing (already optimal) | Custom AST skillset (weeks) |
| **Infrastructure** | None | Azure AI Search Basic tier ($74/month) + Azure Functions + Azure OpenAI embeddings |
| **Maintenance** | Markdown files in git | Azure services requiring monitoring, scaling, cost management |
| **Total effort** | ~1 sprint, zero infrastructure | Multi-sprint, ongoing Azure operations |

---

## Conclusion

The evaluation's core question was: *does Option C's chunking advantage (if any) justify its engineering cost?*

The answer is **no**, for three reasons:

1. **There is no chunking advantage.** Azure AI Search's default chunking is no better than Copilot's for the architecture file types that matter most (OpenAPI, PlantUML, AsyncAPI, source code). For Markdown, both platforms offer heading-aware chunking.

2. **Option C's workarounds are more expensive than Option A's.** Where both platforms need help (OpenAPI `$ref` resolution, PlantUML parsing), Option A's workarounds (CI hooks, companion files, MCP servers) are simpler, cheaper, and maintainable as Markdown files in git — while Option C requires Azure Functions, index management, and ongoing operational overhead.

3. **Direct file access bypasses chunking entirely.** The architect's most common workflow — reading specific files in context — does not involve retrieval at all. Copilot reads files directly from the workspace. Azure AI Search cannot do this; it only returns search results.

The "maybe Option C is better at chunking" hypothesis does not survive contact with the evidence. Both platforms handle architecture files poorly by default. The difference is in the cost of the workaround — and Option A's workarounds are categorically cheaper.

---

**See also:**

- [File-Type Chunking Strategy](../framework/filetype-chunking-strategy.md) — Option A decision matrix with implementation sequencing
- [Build vs Leverage](build-vs-leverage.md) — Why native capabilities replace custom RAG for most use cases
- [What Does Foundry IQ Actually Require?](foundry-iq-comparison.md) — Operational requirements comparison
- [Controlling What Copilot Sees](context-injection-controls.md) — How Copilot's context pipeline works
