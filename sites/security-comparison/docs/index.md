!!! danger "DISCLAIMER -- Synthetic Environment"
    This security comparison was produced within a **proof-of-concept workspace** using entirely synthetic data. The "NovaTrek Adventures" domain is fictional. All JIRA, Elasticsearch, and GitLab references are local mock scripts -- no real corporate systems were accessed. The security analysis, citations, and framework references (NIST, CISA, OWASP, SLSA) are **real and independently verifiable**, but the platform implementation described is a demonstration, not a production deployment.

# Security Model: Docs-as-Code vs. Confluence

An evidence-based security assessment demonstrating that a **docs-as-code publishing pipeline** (Git + MkDocs + CI/CD + Azure Static Web Apps) provides stronger security controls than Confluence Cloud across 12 measurable dimensions.

---

## Why This Matters

Security teams are right to scrutinize any new publishing platform. The question is not "Is MkDocs secure?" but rather **"Does the docs-as-code model provide security controls that are equal to or stronger than our current Confluence-based workflow?"**

The answer is: the docs-as-code model is **demonstrably more secure** than wiki-based publishing. This site explains why, with specific evidence from a reference implementation and 78 authoritative citations from NIST, CISA, OWASP, SLSA, Gartner, and vendor security advisories.

---

## Quick Result

**Docs-as-Code is stronger in 11 of 12 security dimensions.**

| Dimension | Advantage |
|-----------|-----------|
| Change Authorization | Docs-as-Code |
| Audit Trail | Docs-as-Code |
| Pre-publish Validation | Docs-as-Code |
| Secret Scanning | Docs-as-Code |
| Attack Surface | Docs-as-Code |
| Content Security Policy | Docs-as-Code |
| Dependency Scanning | Docs-as-Code |
| Rollback | Docs-as-Code |
| Data Sovereignty | Docs-as-Code |
| Plugin/Extension Risk | Docs-as-Code |
| Authentication | Tie |
| Separation of Duties | Docs-as-Code |

---

## Site Contents

| Page | Description |
|------|-------------|
| [Security Comparison](security-comparison.md) | Side-by-side comparison across all 12 dimensions with detailed analysis |
| [Pipeline Security Gates](pipeline-security-gates.md) | Walkthrough of every CI/CD gate content passes through before reaching production |
| [Security Headers and Attack Surface](headers-and-attack-surface.md) | HTTP security headers, Content Security Policy, and why static sites have a fundamentally smaller attack surface |
| [Access Control and Audit Trail](access-control-and-audit.md) | How Git + branch protection + PR reviews provide stronger controls than wiki page-level permissions |
| [Data Protection](data-protection.md) | Secret scanning, data isolation auditing, and content validation gates |
| [Research Results](research/research-prompt-response.md) | Full research output with 78 authoritative citations |

---

## Methodology

This assessment was produced using AI-assisted deep research (GitHub Copilot with Claude Opus 4.6) to systematically gather authoritative sources across 10 research dimensions. Every claim is supported by citations from:

- **NIST** (SP 800-53, SP 800-123, SP 800-95) -- federal security standards
- **CISA** -- Known Exploited Vulnerabilities catalog
- **OWASP** -- Attack Surface Management Top 10, security guidelines
- **SLSA** -- Supply-chain Levels for Software Artifacts framework
- **Atlassian** -- official security advisories and CVE disclosures
- **Microsoft** -- Azure Static Web Apps security documentation
- **Gartner, Forrester** -- industry analyst recommendations

The full evidence base with all citations is available in [Research Results](research/research-prompt-response.md).
