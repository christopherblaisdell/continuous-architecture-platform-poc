# ADR-002: Documentation Publishing Platform Selection

## Status

PROPOSED

## Date

2025-01-27

## Context and Problem Statement

The Continuous Architecture Platform POC produces extensive markdown-based architecture documentation including arc42 templates, MADR decision records, C4 model descriptions, PlantUML diagrams, solution designs, investigation reports, and quality assessments. These documents currently exist only as raw markdown files in a git repository, accessible only to users who clone the repository and navigate the file system.

The Architecture Practice needs to publish this documentation as a rich, searchable, professionally styled web experience that:

- Renders markdown with full formatting, tables, and code highlighting
- Displays PlantUML and Mermaid diagrams inline
- Provides full-text search across all architecture documentation
- Deploys automatically on push to the main branch
- Hosts on Azure infrastructure (organizational standard)
- Costs minimal or zero additional infrastructure spend
- Requires no custom application code or runtime infrastructure

## Decision Drivers

- **Adoption breadth**: Must be the most widely adopted solution to ensure long-term community support, plugin availability, and hiring familiarity
- **Documentation-first**: Must be purpose-built for documentation (not a general-purpose static site generator requiring theme configuration)
- **Markdown-native**: Must work directly with existing markdown files without requiring format conversion
- **Diagram support**: Must render PlantUML (`.puml`) and Mermaid diagrams natively or via established plugins
- **Architecture documentation features**: Must support admonitions, content tabs, code annotations, tagging, and structured navigation
- **Azure compatibility**: Must produce static output deployable to Azure Static Web Apps
- **Operational simplicity**: Must build via a single CLI command with no JavaScript bundling, webpack configuration, or framework-specific tooling
- **Open source**: Core functionality must be MIT/Apache licensed with no vendor lock-in

## Considered Options

1. **Material for MkDocs** - Python-based MkDocs with the Material theme
2. **Docusaurus** - React-based documentation framework by Meta
3. **Hugo with Docsy theme** - Go-based static site generator with documentation theme
4. **VitePress** - Vue-powered static site generator by the Vue.js team
5. **Starlight (Astro)** - Astro-based documentation framework

## Decision Outcome

**Chosen option: Material for MkDocs**, because it is the most widely adopted documentation-specific framework, works natively with markdown, supports all required architecture documentation features, and produces static HTML deployable to Azure Static Web Apps with zero runtime infrastructure.

### Consequences

#### Positive

- **Zero-effort markdown compatibility**: All existing `.md` files render immediately without modification
- **Architecture documentation native**: Admonitions map to ADR status badges, content tabs show service comparisons, navigation maps to arc42 sections
- **PlantUML + Mermaid support**: Both diagram formats render inline via established plugins
- **Massive adoption**: Used by Google Cloud, Microsoft, AWS CDK, FastAPI, Kubernetes, Netflix, Stripe, Cloudflare - ensures longevity and community support
- **2M+ monthly PyPI downloads**: Active, well-maintained project with dedicated full-time maintainer
- **150+ community plugins**: git-revision-date, git-committers, tags, PDF export, link checking, etc.
- **Python toolchain**: Aligns with existing mock scripts (Python 3.10+) - no additional runtime needed
- **`mkdocs build` produces static HTML**: Perfect fit for Azure Static Web Apps (free tier)
- **Built-in search**: lunr.js-based client-side search requires no search infrastructure
- **Dark mode, responsive design, mobile-first**: Professional appearance out of the box

#### Negative

- **Python dependency**: Requires Python in CI (trivially available via `actions/setup-python`)
- **Insiders features require sponsorship**: Some premium features (social cards, privacy plugin) require $15/month sponsorship - but all core features are MIT-licensed
- **Not React/Vue**: Cannot embed interactive JavaScript components without custom overrides (not needed for architecture documentation)
- **PlantUML rendering requires server**: PlantUML diagrams render via the public PlantUML server or a self-hosted instance (acceptable for non-confidential architecture diagrams)

## Pros and Cons of the Options

### Material for MkDocs

- **Good**: 21K+ GitHub stars, 2M+ PyPI downloads/month - most adopted documentation framework
- **Good**: Used by Google, Microsoft, AWS, FastAPI, Kubernetes, Netflix, Stripe, Cloudflare
- **Good**: Full-time dedicated maintainer (squidfunk) since 2016
- **Good**: Markdown-first, zero conversion needed for existing files
- **Good**: PlantUML plugin, Mermaid support, admonitions, content tabs, code annotations
- **Good**: Python ecosystem aligns with existing mock scripts
- **Good**: Single `pip install mkdocs-material` + `mkdocs build` - operational simplicity
- **Good**: Produces static HTML - perfect for Azure Static Web Apps free tier
- **Neutral**: Insiders tier ($15/mo) for premium features
- **Bad**: PlantUML requires server-side rendering (public server is acceptable)

### Docusaurus

- **Good**: 57K+ GitHub stars - highest raw star count
- **Good**: Backed by Meta (large organization support)
- **Good**: MDX support allows React components in docs
- **Good**: Built-in versioning and i18n
- **Bad**: General-purpose (blog + docs + landing page) - not documentation-specific
- **Bad**: React dependency adds complexity (node_modules, webpack bundling)
- **Bad**: Heavier build process - `npm install` + `npm run build` vs `pip install` + `mkdocs build`
- **Bad**: Stars inflated by React ecosystem - many stars from people building product sites, not documentation
- **Bad**: Configuration complexity for pure documentation use case

### Hugo with Docsy Theme

- **Good**: 77K+ GitHub stars - most starred static site generator
- **Good**: Fastest build times (Go binary)
- **Good**: Docsy theme provides documentation structure
- **Bad**: General-purpose SSG requiring theme selection and configuration
- **Bad**: Docsy theme has 2.8K stars vs Material's 21K - far less adopted
- **Bad**: Go template syntax has steep learning curve
- **Bad**: Documentation-specific features require manual configuration
- **Bad**: Weaker admonition/tab/annotation support compared to Material

### VitePress

- **Good**: 13K+ GitHub stars, growing community
- **Good**: Fast, modern, Vue-powered
- **Good**: Good default theme for documentation
- **Bad**: Vue.js dependency
- **Bad**: Smaller plugin ecosystem than MkDocs Material
- **Bad**: Less mature for large documentation sites
- **Bad**: Limited PlantUML support

### Starlight (Astro)

- **Good**: Modern framework with excellent performance
- **Good**: Framework-agnostic component support
- **Bad**: Only 5K stars - too young for enterprise adoption
- **Bad**: Limited plugin ecosystem
- **Bad**: Unproven at scale for architecture documentation
- **Bad**: Smallest community of all options considered

## More Information

- [Material for MkDocs Documentation](https://squidfunk.github.io/mkdocs-material/)
- [Azure Static Web Apps Documentation](https://learn.microsoft.com/en-us/azure/static-web-apps/)
- Implementation plan: [PUBLISHING-PLATFORM-PLAN.md](../phase-6-documentation-publishing/PUBLISHING-PLATFORM-PLAN.md)
- This ADR follows the MADR format adopted by the Architecture Practice
