# Markdown-First: Extending What We Already Do

## We Already Author in Text Formats — Now We Complete the Picture

Our architects already author OpenAPI specs in YAML and diagrams in PlantUML — text formats checked into Git. The platform extends this practice to **solution designs, ADRs, and impact assessments** in Markdown, completing the set of version-controlled architecture artifacts.

---

## What We Have vs What We Add

| Artifact | Today | With the Platform |
|----------|:---:|:---:|
| **OpenAPI specs** | In Git (gated) | In Git (same) + AI-assisted updates |
| **PlantUML diagrams** | In Git | In Git (same) + auto-rendered to portal |
| **Solution designs** | Confluence (manual) or ticket attachments | Markdown in Git + auto-published |
| **Architecture Decision Records** | In ticket branches (not discoverable) | Markdown in Git + global searchable log |
| **Impact assessments** | Confluence or email | Markdown in Git + version-controlled |
| **Service documentation** | Confluence (voluntary updates) | Auto-generated from specs in Git |
| **Cross-service links** | Manually maintained in Confluence | Auto-generated from dependency graph |

---

## What Changes in Practice

### Current Workflow

```
1. Architect updates OpenAPI specs and PlantUML diagrams in Git
2. Changes are checked into master (governance gate — this works well)
3. Architect is supposed to update Confluence service pages manually
4. Sometimes this happens, often it doesn't
5. Solution design lives in a ticket branch or Confluence — not discoverable later
6. ADRs stay in ticket context, never promoted to a global log
7. After deployment, nobody reconciles design intent vs actual implementation
```

### Enhanced Workflow

```
1. AI reads the existing Git repo (specs, diagrams, previous designs)
2. AI scaffolds solution design from template in VS Code
3. Architect reviews and refines (with AI assistance)
4. Specs, diagrams, and solution design committed together
5. Pull request for architecture review with line-by-line diffs
6. Merge to main triggers automated publishing to browsable portal
7. Optionally synced to Confluence via API (no manual step)
8. AI reads the design in future sessions (full context)
9. PROMOTE step reconciles design intent with actual implementation
```

---

## Every Design Artifact in This POC is Markdown

The proof of concept produced 39 files across 5 scenarios — all in Markdown, all version-controlled alongside the specs and diagrams already in Git:

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

!!! info "This replaces the manual Confluence step — not Confluence itself"
    The platform can publish to **both** MkDocs and Confluence from the same source. The difference: updates happen automatically on `git push` instead of relying on a voluntary manual step.

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

The key difference: **publishing is automated**, not voluntary. Git remains the source of truth (as it already is for specs), and Confluence becomes a read-only mirror. This means:

- Architecture changes go through pull request review (extending what we already do for specs)
- The AI reads the Git version (always available, always current)
- Confluence stays up to date automatically (no manual step to skip)
- Browsable documentation always reflects the latest checked-in artifacts

---

## Migration Path

This builds on what architects already do — **no disruption required**:

| Phase | Action | Disruption |
|-------|--------|:---:|
| **Already done** | Specs and diagrams are in Git | None — this is the existing process |
| **Start** | New solution designs and ADRs authored in Markdown in the same repo | None — same content, text format |
| **Automatic** | Browsable portal generated from Git on every push | None — replaces a manual step that was often skipped |
| **Optional** | Confluence sync from the same Markdown source | None — additive, not replacement |
| **Never required** | Converting all historical Confluence content | Not needed — only active designs matter |

<div class="key-insight" markdown>
**The migration cost is near zero.** Architects already author in text formats (YAML specs, PlantUML). Markdown is the same skill. And the AI handles formatting automatically.
</div>

<div class="cta-box" markdown>

### How does publishing work?

[Automated Publishing: Replace the Manual Confluence Step](publishing-pipeline.md)

</div>
