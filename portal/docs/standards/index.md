---
tags:
  - standards
  - architecture
---

<div class="hero" markdown>

# Design Standards

<p class="subtitle">Templates, guidelines, and quality models for consistent architecture documentation</p>

</div>

The NovaTrek Architecture Practice maintains a curated set of design standards that ensure consistency, quality, and traceability across all architectural work. These standards are organized into seven categories.

---

<div class="portal-grid" markdown>

<a href="arc42/" class="portal-card" markdown>
<span class="card-icon">:material-file-document-outline:</span>

### arc42 Template

The 12-section documentation framework for software architecture. Provides a proven structure for capturing system context, building blocks, runtime behavior, deployment, decisions, and quality requirements.
</a>

<a href="c4-model/" class="portal-card" markdown>
<span class="card-icon">:material-sitemap:</span>

### C4 Model

Hierarchical diagramming approach with four zoom levels — System Context, Container, Component, and Code. Includes notation guide, PlantUML macros, and a review checklist.
</a>

<a href="madr/" class="portal-card" markdown>
<span class="card-icon">:material-scale-balance:</span>

### MADR

Markdown Any Decision Records — the standard format for documenting architecture decisions. Full and short templates plus worked examples.
</a>

<a href="adr-templates/" class="portal-card" markdown>
<span class="card-icon">:material-clipboard-text:</span>

### ADR Templates

Three alternative ADR formats for different contexts: Nygard (minimal), Alexandrian (pattern-based), and Tyree-Akerman (business-oriented).
</a>

<a href="openapi-contracts/" class="portal-card" markdown>
<span class="card-icon">:material-api:</span>

### OpenAPI Contracts

Machine-readable API specifications in YAML for all 22 NovaTrek microservices. The single source of truth for endpoints, schemas, and cross-service contracts — powering Swagger UI, sequence diagrams, and portal generation.
</a>

<a href="metadata-registry/" class="portal-card" markdown>
<span class="card-icon">:material-database-cog:</span>

### Metadata Registry

15 YAML files that model the entire architecture — domains, capabilities, integrations, data stores, actors, events, and tickets. Portal pages are generated from this data, not maintained by hand.
</a>

<a href="quality-model/" class="portal-card" markdown>
<span class="card-icon">:material-shield-check:</span>

### ISO 25010 Quality Model

The international standard for software product quality. Eight quality characteristics with sub-characteristics, definitions, and example quality scenarios for architecture evaluation.
</a>

</div>

---

## How These Standards Work Together

| Activity | Primary Standard | Supporting Standards |
|----------|-----------------|---------------------|
| **New service documentation** | arc42 template (Sections 01-12) | C4 Model for diagrams, OpenAPI Contracts, ISO 25010 for quality requirements |
| **Architecture decision** | MADR full template | ISO 25010 for quality attribute assessment |
| **Quick design spike** | MADR short template | C4 Model (Level 2 Container diagram) |
| **Business-facing decision** | Tyree-Akerman ADR template | ISO 25010 for stakeholder quality concerns |
| **Diagram review** | C4 diagram checklist | C4 notation guide, C4-PlantUML guide |
| **Quality assessment** | ISO 25010 quality tree | arc42 Section 10 (Quality Requirements) |

---

!!! tip "Getting Started"

    **First time writing architecture documentation?** Start with the [arc42 template](arc42/index.md) for full system documentation or the [MADR short template](madr/adr-template-short.md) for a quick decision record.

    **Need to create a diagram?** The [C4-PlantUML guide](c4-model/c4-plantuml-guide.md) has ready-to-use code examples for System Context, Container, and Component diagrams.
