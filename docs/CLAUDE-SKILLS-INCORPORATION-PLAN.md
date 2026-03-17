# Claude Skills Incorporation Plan

**Date**: 2026-03-17
**Status**: Draft
**Source Repository**: [Jeffallan/claude-skills](https://github.com/Jeffallan/claude-skills) (MIT License, 6.9K stars)
**Target**: GitHub Copilot Agent Mode with Claude Opus 4.6

---

## Executive Summary

The `Jeffallan/claude-skills` repository contains 66 specialized SKILL.md files with 365 reference documents covering full-stack development. The SKILL.md format (YAML frontmatter + structured markdown) is natively compatible with GitHub Copilot's skill system — skills can be registered in VS Code settings and loaded on demand via `copilot-skill://` URIs.

This plan identifies the 14 skills directly relevant to our NovaTrek architecture workflow, proposes an adaptation strategy that layers them beneath our existing `copilot-instructions.md`, and defines a phased rollout to avoid context window bloat.

---

## Current State

### What We Have

| Asset | Location | Size |
|-------|----------|------|
| Master instructions | `.github/copilot-instructions.md` | 718 lines (~28KB) |
| VS Code settings | `.vscode/settings.json` | Color theme + Java config only |
| MCP servers | `.vscode/mcp.json` | NovaTrek architecture MCP |
| Custom skills | None | — |

### How GitHub Copilot Skills Work

1. **SKILL.md files** are placed in the workspace (any directory)
2. **VS Code settings** registers skill directories via `github.copilot.chat.skills`
3. **YAML frontmatter** defines: name, description, triggers, related-skills, domain
4. **Copilot loads the SKILL.md** into context when the user's prompt matches trigger keywords or when explicitly referenced
5. **Reference files** (`references/*.md`) are loaded on demand when the skill's reference table directs the agent to read them

### Key Difference: Claude Code vs GitHub Copilot

| Feature | Claude Code | GitHub Copilot |
|---------|-------------|----------------|
| Skill loading | Plugin system (`/plugin install`) | VS Code settings + workspace files |
| Skill format | SKILL.md (YAML + MD) | SKILL.md (YAML + MD) — SAME format |
| Slash commands | Supported (`/common-ground`) | Not supported in Copilot |
| Reference loading | Automatic via skill engine | Agent reads files on demand |
| Context budget | ~200K tokens | ~128K tokens (model dependent) |

The SKILL.md format is identical. The main adaptation needed is:
- Remove Claude Code-specific features (slash commands, plugin refs)
- Adjust reference loading to use explicit file paths instead of relative plugin paths
- Curate skills to fit within Copilot's smaller context window

---

## Relevant Skills for NovaTrek Architecture Workflow

### Tier 1 — Core Architecture (Always Available)

These skills directly align with the Solution Architect role defined in `copilot-instructions.md`.

| Skill | Lines | References | Relevance to NovaTrek |
|-------|-------|------------|----------------------|
| `architecture-designer` | 117 | 5 files (541 lines) | ADR authoring, system design, architecture patterns — core workflow |
| `microservices-architect` | 164 | 5 files (2,972 lines) | Bounded contexts, DDD, saga patterns — matches our 19-service domain |
| `api-designer` | 217 | 5 files (2,585 lines) | OpenAPI specs, REST patterns, versioning — we maintain 19 OpenAPI specs |

### Tier 2 — Technology Stack (Load on Demand)

These match our specific technology choices (Spring Boot, PostgreSQL, Azure).

| Skill | Lines | References | Relevance to NovaTrek |
|-------|-------|------------|----------------------|
| `java-architect` | 132 | 5 files (1,963 lines) | Spring ecosystem, JPA — our services are Java/Spring Boot |
| `spring-boot-engineer` | 195 | 5 files (~2,000 lines) | Spring Boot patterns — direct match |
| `postgres-pro` | ~150 | ~5 files | PostgreSQL optimization — our primary data store |
| `cloud-architect` | ~150 | ~5 files | Azure architecture — our deployment target |
| `database-optimizer` | ~150 | ~5 files | Index strategies, query optimization |

### Tier 3 — Quality and Operations (Load on Demand)

These support specific workflow phases.

| Skill | Lines | References | Relevance to NovaTrek |
|-------|-------|------------|----------------------|
| `security-reviewer` | ~150 | ~5 files | Security analysis — required per our review checklist |
| `devops-engineer` | ~150 | ~5 files | CI/CD, GitHub Actions — we have 14 workflows |
| `code-reviewer` | ~150 | ~5 files | Code review patterns — source code analysis |
| `code-documenter` | ~150 | ~5 files | Documentation standards — portal content |
| `spec-miner` | ~150 | ~5 files | Reverse-engineering specs from code — useful for analysis |

### Tier 4 — Excluded (Not Relevant)

Skills not applicable to our architecture workflow: `angular-architect`, `react-expert`, `nextjs-developer`, `vue-expert`, `flutter-expert`, `react-native-expert`, `django-expert`, `fastapi-expert`, `nestjs-expert`, `laravel-specialist`, `rails-expert`, `dotnet-core-expert`, `python-pro`, `typescript-pro`, `golang-pro`, `rust-engineer`, `cpp-pro`, `swift-expert`, `kotlin-specialist`, `csharp-developer`, `php-pro`, `game-developer`, `embedded-systems`, `salesforce-developer`, `shopify-expert`, `wordpress-pro`, `ml-pipeline`, `pandas-pro`, `spark-engineer`, `fine-tuning-expert`, `rag-architect`, `prompt-engineer`, `the-fool`, `fullstack-guardian`, `debugging-wizard`, `playwright-expert`, `test-master`, `legacy-modernizer`, `mcp-developer`, `graphql-architect`, `websocket-engineer`, `chaos-engineer`, `cli-developer`, `sre-engineer`, `monitoring-expert`, `terraform-engineer`, `kubernetes-specialist`, `atlassian-mcp`, `feature-forge`, `sql-pro`, `javascript-pro`, `vue-expert-js`.

---

## Context Window Budget Analysis

### Current Budget

| Component | Tokens (est.) |
|-----------|--------------|
| System prompt (Copilot built-in) | ~8K |
| `copilot-instructions.md` (718 lines) | ~7K |
| Conversation history | ~20-40K |
| File context (open files, search results) | ~20-40K |
| **Available for skills** | **~30-60K** |

### Skill Loading Strategy

**Problem**: Loading all 14 relevant skills + their 70+ reference files would consume ~50K tokens — too much.

**Solution**: Tiered loading with explicit activation.

| Tier | Loading | Token Budget | Mechanism |
|------|---------|-------------|-----------|
| Tier 1 (3 skills) | SKILL.md only, auto-loaded | ~1.5K | VS Code `applyTo` + `copilot-instructions.md` reference |
| Tier 2 (5 skills) | SKILL.md on demand | ~1K when active | User mentions technology keyword |
| Tier 3 (5 skills) | SKILL.md on demand | ~1K when active | User mentions workflow keyword |
| References | Never auto-loaded | 0 base, ~2-5K when read | Agent reads specific reference file when needed |

**Total baseline overhead**: ~1.5K tokens (Tier 1 SKILL.md files only)
**Maximum when fully active**: ~10K tokens (all skills activated, 1-2 references loaded)

---

## Implementation Plan

### Phase 1: Workspace Setup (Immediate)

1. **Create skill directory structure**:
   ```
   .copilot/skills/
   ├── architecture-designer/
   │   ├── SKILL.md              (adapted from claude-skills)
   │   └── references/           (copied from claude-skills)
   ├── microservices-architect/
   │   ├── SKILL.md
   │   └── references/
   ├── api-designer/
   │   ├── SKILL.md
   │   └── references/
   └── ... (remaining Tier 2-3 skills)
   ```

2. **Adapt SKILL.md files** for each skill:
   - Replace Claude Code-specific metadata with Copilot-compatible YAML frontmatter
   - Add `applyTo` patterns where relevant (e.g., `api-designer` applies to `**/*.yaml` in specs/)
   - Remove slash command references
   - Update reference paths to use workspace-relative paths
   - Add NovaTrek-specific context to each skill's role definition

3. **Register skills in VS Code settings** (`.vscode/settings.json`):
   ```json
   {
     "github.copilot.chat.skills": [
       ".copilot/skills/architecture-designer",
       ".copilot/skills/microservices-architect",
       ".copilot/skills/api-designer"
     ]
   }
   ```

### Phase 2: NovaTrek Customization (Next)

Layer NovaTrek-specific knowledge on top of the generic skills:

1. **Create `novatrek-architect` skill** — A meta-skill that combines our domain model, bounded context rules, and service ownership boundaries from `copilot-instructions.md` into a structured SKILL.md format with references:
   - `references/domain-model.md` — Service domains, data ownership, bounded context rules
   - `references/solution-design-workflow.md` — Folder structure, capability rollup, prior-art discovery
   - `references/quality-checklist.md` — Architecture review checklist, anti-patterns

2. **Create `novatrek-openapi` skill** — Specialized API designer for our 19 services:
   - Knows the spec locations in `architecture/specs/`
   - Understands our heading slug format, deep linking conventions
   - References the OpenAPI analysis guidelines from `copilot-instructions.md`

3. **Create `novatrek-solution-designer` skill** — Solution design workflow:
   - MADR template, folder structure conventions
   - Capability changelog workflow
   - Portal generator commands

### Phase 3: Integration Testing

1. **Test skill activation** with sample prompts:
   - "Design an ADR for adding WebSocket support to svc-check-in" → Should activate `architecture-designer` + `novatrek-architect`
   - "Review the OpenAPI spec for svc-reservations" → Should activate `api-designer` + `novatrek-openapi`
   - "What microservices patterns should we use for the scheduling flow?" → Should activate `microservices-architect`

2. **Measure context window impact**:
   - Run the same architecture scenario with and without skills
   - Compare token usage and output quality
   - Verify skills don't crowd out essential file context

3. **Tune trigger keywords** to avoid false activations

### Phase 4: Optimize copilot-instructions.md

Once skills are working, refactor `copilot-instructions.md` to reduce duplication:

1. **Move domain-specific sections** to skill reference files:
   - Architecture Standards → `architecture-designer` references
   - Source Code Analysis Guidelines → `java-architect` + `code-reviewer` references
   - OpenAPI Spec Analysis → `api-designer` references
   - Service Domains table → `novatrek-architect` references

2. **Keep in copilot-instructions.md** (always-loaded context):
   - Role definition (Solution Architect)
   - Data isolation rules (critical safety guardrails)
   - Mock tool usage commands
   - Document formatting rules
   - Core workflow (branching convention, folder structure)

3. **Expected reduction**: 718 lines → ~300 lines, with rest distributed to on-demand skill references

---

## Adaptation Checklist (Per Skill)

For each skill copied from `claude-skills/`:

- [ ] Remove Claude Code plugin metadata (`allowed-tools: Read, Grep, Glob, Bash`)
- [ ] Update YAML frontmatter to Copilot format (add `applyTo`, remove `license`)
- [ ] Replace implementation examples that reference Node.js/Express with Java/Spring Boot equivalents where relevant
- [ ] Update reference file paths from relative plugin paths to workspace paths
- [ ] Add NovaTrek context to the role definition (e.g., "You operate within the NovaTrek Adventures microservices platform")
- [ ] Remove any slash command references (`/common-ground`, `/project:*`)
- [ ] Verify total SKILL.md size stays under 200 lines (for context efficiency)
- [ ] Test trigger keyword activation in Copilot Agent Mode

---

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Context window bloat | Skills crowd out file context needed for analysis | Tiered loading — only Tier 1 auto-loaded (~1.5K tokens) |
| Skill conflicts with copilot-instructions.md | Contradictory guidance confuses the agent | Phase 4 refactors instructions to defer to skills |
| Over-generic advice | Generic skills give advice that contradicts NovaTrek conventions | NovaTrek-specific skill overlays in Phase 2 |
| Maintenance burden | Skills drift from upstream updates | Pin to a specific commit; review quarterly |
| False activations | Wrong skill loads for a prompt | Tune trigger keywords in Phase 3 |

---

## File Inventory

### Source (cloned, gitignored)

```
claude-skills/                          # Cloned from Jeffallan/claude-skills (MIT)
├── skills/                             # 66 skill directories
│   ├── {skill-name}/
│   │   ├── SKILL.md                    # Skill definition
│   │   └── references/                 # Deep-dive reference materials
│   └── ...
├── SKILLS_GUIDE.md                     # Category index and workflow combos
├── QUICKSTART.md                       # Installation guide (Claude Code-specific)
└── docs/                              # Additional documentation
```

### Target (committed, workspace-owned)

```
.copilot/skills/                        # Adapted skills for GitHub Copilot
├── architecture-designer/              # Tier 1
├── microservices-architect/            # Tier 1
├── api-designer/                       # Tier 1
├── java-architect/                     # Tier 2
├── spring-boot-engineer/              # Tier 2
├── postgres-pro/                       # Tier 2
├── cloud-architect/                    # Tier 2
├── database-optimizer/                 # Tier 2
├── security-reviewer/                  # Tier 3
├── devops-engineer/                    # Tier 3
├── code-reviewer/                      # Tier 3
├── code-documenter/                    # Tier 3
├── spec-miner/                         # Tier 3
├── novatrek-architect/                 # Custom (Phase 2)
├── novatrek-openapi/                   # Custom (Phase 2)
└── novatrek-solution-designer/         # Custom (Phase 2)
```

---

## Success Criteria

1. **Skills activate correctly** for architecture-related prompts without manual invocation
2. **Context window usage** increases by less than 5K tokens at baseline
3. **Output quality improves** — ADRs, impact assessments, and API reviews reference skill knowledge
4. **copilot-instructions.md shrinks** from 718 to ~300 lines without losing functionality
5. **No regression** in existing architecture workflow (solution designs, portal generation, mock tool usage)

---

## Next Steps

1. Review and approve this plan
2. Begin Phase 1: copy and adapt Tier 1 skills (architecture-designer, microservices-architect, api-designer)
3. Test activation with a sample architecture scenario
4. Iterate on Tier 2-3 and NovaTrek custom skills
