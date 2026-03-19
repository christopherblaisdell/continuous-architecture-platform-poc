---
tags:
  - operations
  - platform
---

# Operations

The Operations section covers everything about **how the Continuous Architecture Platform itself works** — CI/CD pipelines, deployment infrastructure, security posture, governance tooling, AI workflow customization, and delivery planning.

---

## Platform Infrastructure

How services are built, tested, deployed, and kept running.

| Page | What You Will Find |
|------|--------------------|
| [Platform Operations](../platform-operations.md) | CI/CD pipeline catalog (14 workflows), deployment targets (prod/dev/ephemeral), Azure resources, cost controls, secrets management |
| [Technology Stack](../technologies.md) | Java 21, Spring Boot 3.3, PostgreSQL 15, Docker, Azure Container Apps, Kafka, Redis — the full runtime stack |
| [Database Change Workflow](../database-change-workflow.md) | How a schema change flows from `data-stores.yaml` through Flyway migrations to production |
| [Platform Roadmap](../roadmap.md) | Phased delivery plan — capability mapping, portal publishing, ticketing integration, AI integration, and advanced features |

---

## Architecture Governance

Artifacts, decisions, and automated controls that keep the architecture consistent.

| Page | What You Will Find |
|------|--------------------|
| [Artifact Registry](../artifact-registry.md) | Every artifact in the platform — what is hand-authored vs. generated, who owns each, and how edits flow through generators |
| [Decision Log](../decisions/README.md) | All architecture decision records (ADRs) — global decisions that constrain the design space across all services |

---

## Security Model

The platform's security posture — how the portal, pipelines, and infrastructure are secured.

| Page | What You Will Find |
|------|--------------------|
| [Security Overview](../security/index.md) | Security model summary and approach |
| [Security Comparison](../security/security-comparison.md) | Docs-as-code vs. Confluence security trade-offs |
| [Pipeline Security Gates](../security/pipeline-security-gates.md) | OWASP dependency checks, Trivy container scans, SonarQube analysis |
| [Headers and Attack Surface](../security/headers-and-attack-surface.md) | HTTP security headers, CSP policy, attack surface analysis |
| [Access Control and Audit](../security/access-control-and-audit.md) | GitHub branch protection, role-based access, audit trails |
| [Data Protection](../security/data-protection.md) | PII handling, encryption, data classification |

---

## AI Workflow

How AI coding agents are configured, customized, and evaluated for architecture work.

| Page | What You Will Find |
|------|--------------------|
| [Copilot vs OpenSpec Comparison](../copilot-vs-openspec-comparison.md) | Side-by-side evaluation — philosophy, features, enforcement, and recommendation |
| [GitHub Copilot Customization](../github-copilot-customization-guide.md) | 6 customization primitives — instructions, prompts, agents, skills, hooks — with file patterns and activation rules |
| [OpenSpec Customization](../openspec-customization-guide.md) | Spec-driven workflow framework — folder structure, YAML schemas, slash commands |
| [OpenSpec Research](../research/OPENSPEC-ANALYSIS.md) | Evaluation analysis, decision rationale, and deep research prompt |
