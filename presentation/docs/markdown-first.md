# Markdown-First: Write Once, Publish Everywhere

## Why Markdown Instead of Word or Confluence?

The format you author in determines what you can do with the output. Markdown unlocks capabilities that Word and Confluence cannot match.

---

## The Comparison

| Capability | Markdown (git) | Word | Confluence |
|-----------|:---:|:---:|:---:|
| **Version control** | Full git history with diffs | Binary file — no meaningful diffs | Page history (limited) |
| **AI-readable** | Native — AI reads and writes Markdown directly | Requires doc parsing | Requires API + HTML conversion |
| **Pull request reviews** | Line-by-line review on architecture changes | File-level comments | Comment threads |
| **Diffable** | Character-level diffs in git | "Track changes" mode | Side-by-side page comparison |
| **Publish to website** | MkDocs, Hugo, Docusaurus | Manual export | Already in Confluence |
| **Publish to Confluence** | API sync from Markdown source | Copy-paste or upload | Native |
| **Publish to PDF** | Automated via build pipeline | Native | Plugin required |
| **Searchable in IDE** | Full-text search across all designs | Not in IDE | Not in IDE |
| **AI can update** | Direct file edit | Complex doc manipulation | API calls required |
| **Works offline** | Yes | Yes | No |

---

## What Markdown-First Looks Like in Practice

### Before: Confluence-First Workflow

```
1. Open Confluence → Create page from template
2. Write solution design in the browser editor
3. Copy-paste diagrams as screenshots
4. Share link for review via comments
5. Design is now locked in Confluence
6. AI cannot access it for future sessions
7. Nobody updates it after deployment
```

### After: Markdown-First Workflow

```
1. AI scaffolds solution design from template in VS Code
2. Architect reviews and refines (with AI assistance)
3. Diagrams generated as PlantUML code (version-controlled)
4. Pull request for architecture review with line-by-line diffs
5. Merge to main triggers automated publishing
6. Published to MkDocs site (always current)
7. Optionally synced to Confluence via API
8. AI reads the design in future sessions (full context)
9. PROMOTE step updates baselines after deployment
```

---

## Every Artifact in This POC is Markdown

The proof of concept produced 39 files across 5 scenarios. Every one is Markdown:

- **Solution designs** — arc42-structured Markdown with embedded PlantUML
- **Architecture Decision Records** — MADR format (Markdown Any Decision Record)
- **Impact assessments** — service-level analysis in Markdown tables
- **User stories** — acceptance criteria in Markdown lists
- **Investigation reports** — evidence-grounded analysis with code block citations
- **Implementation guidance** — code patterns in fenced code blocks
- **Simple explanations** — non-technical summaries for stakeholders

None of these required Word. None required Confluence. All are version-controlled, AI-readable, and auto-publishable.

---

## Confluence Compatibility

!!! info "Markdown-first does not mean Confluence-never"
    For organizations that require Confluence as the architecture documentation platform, Markdown-first authoring is fully compatible. The pipeline publishes to **both** MkDocs and Confluence from the same source.

``` mermaid
flowchart LR
    A[Markdown in Git\nsingle source of truth] --> B[MkDocs Build]
    A --> C[Confluence API Sync]
    B --> D[Architecture Portal\nalways current]
    C --> E[Confluence Pages\nalways current]

    style A fill:#00897b,color:#fff
    style D fill:#ff8f00,color:#fff
    style E fill:#1565c0,color:#fff
```

The key difference: **git is the source of truth**, not Confluence. Confluence becomes a read-only mirror. This means:

- Architecture changes go through pull request review (not Confluence comment threads)
- The AI reads the git version (always available, always current)
- Confluence stays up to date automatically (no manual publishing step)
- You never lose content because "someone edited the Confluence page directly"

---

## Migration Path

Moving to Markdown-first is **incremental, not disruptive**:

| Phase | Action | Disruption |
|-------|--------|:---:|
| **Start** | New solution designs written in Markdown | None — same content, different format |
| **Gradual** | Existing Confluence templates recreated as Markdown templates | None — templates already exist in workspace |
| **Optional** | High-value existing designs exported from Confluence to Markdown | Low — export tools available |
| **Never required** | Converting all historical Confluence content | Not needed — only active designs matter |

<div class="key-insight" markdown>
**The migration cost is near zero.** Architects already write structured text with tables and code blocks. Markdown is the same skill with a different syntax. The AI handles formatting automatically.
</div>

<div class="cta-box" markdown>

### How does publishing work?

[CI/CD Publishing: Living Documentation](publishing-pipeline.md)

</div>
