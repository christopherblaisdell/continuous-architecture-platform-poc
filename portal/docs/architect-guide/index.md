# Architect's Guide

Welcome to the NovaTrek Continuous Architecture Platform. This guide is your starting point for understanding how architecture works here and how to contribute.

!!! tip "New here?"
    Start with [Your Role](your-role.md) to understand what a solution architect does, then follow the [Solution Design Workflow](solution-design-workflow.md) to learn how to contribute your first design.

---

## Learning Path

Follow these pages in order for a complete onboarding experience, or jump to any topic.

### 1. Understand the Role

| Page | What You'll Learn |
|------|-------------------|
| [Your Role](your-role.md) | What a solution architect does and does not do at NovaTrek |
| [Domain Model](domain-model.md) | The NovaTrek business domain — services, bounded contexts, data ownership, safety rules |

### 2. Learn the Workflow

| Page | What You'll Learn |
|------|-------------------|
| [Solution Design Workflow](solution-design-workflow.md) | Step-by-step guide to creating a complete solution design from ticket to approval |
| [Architecture Decisions](decisions.md) | How to write MADR-formatted ADRs and when to create them |
| [API Contracts](api-contracts.md) | Working with OpenAPI and AsyncAPI specs — editing, versioning, backward compatibility |

### 3. Master the Tools

| Page | What You'll Learn |
|------|-------------------|
| [Metadata and Artifacts](metadata-and-artifacts.md) | The metadata-driven architecture — what YAML files to edit, what gets generated |
| [Diagrams and Wireframes](diagrams-and-wireframes.md) | Creating C4 diagrams, sequence diagrams, and Excalidraw wireframes |
| [Testing Guide](testing-guide.md) | BDD authoring, test methodology, and how architecture drives test design |
| [Portal Publishing](portal-publishing.md) | Building, previewing, and deploying the documentation portal |

### 4. Go Deeper

| Page | What You'll Learn |
|------|-------------------|
| [AI-Assisted Workflow](ai-assisted-workflow.md) | Using GitHub Copilot and AI tools effectively for architecture work |
| [Anti-Patterns](anti-patterns.md) | Common architectural mistakes and how to avoid them |
| [Quick Reference](quick-reference.md) | Commands, file locations, naming conventions — all in one place |

---

## How This Portal Works

This is a **living architecture portal** — not a static wiki. Every page you see is either:

- **Hand-authored** by an architect (solution designs, decisions, metadata YAML files), or
- **Auto-generated** by scripts from those hand-authored sources (microservice pages, sequence diagrams, capability maps, topology views)

The key insight: **you edit metadata and contracts, and the portal regenerates itself**. When you change an OpenAPI spec, 139 sequence diagrams update. When you add a capability to the changelog, the capability map rebuilds. When you create a solution design folder, a portal page appears.

See the [Artifact Registry](../artifact-registry.md) for the complete inventory of what is hand-authored vs. generated.

---

## Key Principles

1. **Metadata is the source of truth.** Architecture is modeled as 15 YAML files, not prose documents. Generators read YAML and produce portal pages, diagrams, and topology views.

2. **Contracts before code.** OpenAPI specs and AsyncAPI event schemas are designed by the architect before developers write implementations. The spec is the contract.

3. **Decisions are recorded.** Every architectural choice that crosses service boundaries or changes data semantics gets a MADR decision record.

4. **Safety defaults to strict.** Unknown adventure categories always default to Pattern 3 (Full Service) — the highest safety level. This is non-negotiable (ADR-005).

5. **Services own their data.** No shared databases. Every service has exclusive ownership of its data. Cross-service access goes through published APIs.

6. **Everything is version-controlled.** Metadata, specs, designs, decisions, diagrams — all in Git. CI/CD regenerates and deploys the portal on every push to `main`.
