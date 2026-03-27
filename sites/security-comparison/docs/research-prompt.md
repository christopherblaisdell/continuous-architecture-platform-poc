# Security Research Prompt

This page contains the AI deep-research prompt used to gather authoritative, citable sources for the NovaTrek Architecture Portal security assessment. The prompt was designed to query across government agencies, standards bodies, vendor documentation, and industry analysts to build an evidence-based security comparison.

---

## Purpose

The security team needs authoritative evidence — not opinions — that the docs-as-code publishing model (Git + MkDocs + CI/CD + Azure Static Web Apps) provides stronger security controls than Confluence Cloud. This prompt was used to systematically gather that evidence across 10 research dimensions.

---

## Research Prompt

The following prompt was submitted to an AI deep research agent to gather authoritative sources:

---

**Deep Research Prompt: Authoritative Security Evidence for Docs-as-Code vs. Wiki-Based Documentation Platforms**

I am building a security comparison document to convince a corporate security team that publishing architecture documentation via a docs-as-code pipeline (Git + MkDocs + GitHub Actions CI/CD + Azure Static Web Apps) is MORE secure than using Confluence Cloud as a documentation platform.

I need authoritative, citable sources for the following areas. For each area, I need: the source organization/author, publication date, URL, and the specific finding or recommendation that supports the docs-as-code security argument.

### 1. Confluence CVE History and Security Incidents

- Find all Critical and High severity CVEs for Atlassian Confluence from 2020 to present (March 2026)
- Include CVSS scores, attack vectors, and whether they were exploited in the wild
- Note any that were zero-day exploits (exploited before patch was available)
- Find any Atlassian security advisories or post-incident reports
- Find any CISA (Cybersecurity and Infrastructure Security Agency) advisories or Known Exploited Vulnerabilities (KEV) catalog entries for Confluence

### 2. Static Sites vs. Dynamic Web Applications — Security Research

- Find OWASP guidance on attack surface reduction through static site generation
- Find NIST publications (SP 800-series) on minimizing attack surface for web-hosted content
- Find CIS (Center for Internet Security) benchmarks relevant to static web hosting
- Find academic or industry research comparing the attack surface of static sites vs. dynamic CMS/wiki platforms
- Find any security framework guidance (ISO 27001, SOC 2, NIST CSF) that favors immutable deployments or infrastructure-as-code for documentation

### 3. Git as an Immutable Audit Trail

- Find authoritative sources on Git's SHA-1/SHA-256 cryptographic commit chain as a tamper-evident log
- Find compliance framework guidance (SOX, GDPR, HIPAA) that accepts Git history as an audit trail
- Compare Git audit trail properties vs. wiki page history audit trail properties (e.g., can Confluence page history be deleted? Can Git history be deleted without detection?)
- Find guidance from NIST or similar bodies on version control systems as audit mechanisms

### 4. CI/CD Security Gates for Documentation

- Find SLSA (Supply-chain Levels for Software Artifacts) framework guidance and how it applies to documentation pipelines
- Find OWASP CI/CD Security guidance (OWASP Top 10 CI/CD Security Risks)
- Find GitHub's documentation on branch protection rules, push protection, and secret scanning detection rates
- Find industry research on the effectiveness of automated pre-publish validation vs. manual access controls for preventing unauthorized content publication

### 5. Azure Static Web Apps Security Posture

- Find Microsoft's official security documentation for Azure Static Web Apps
- Find Azure compliance certifications that cover Static Web Apps (SOC 1/2/3, ISO 27001, FedRAMP, etc.)
- Find Microsoft's documentation on the authentication/authorization model for Static Web Apps (Entra ID integration, custom auth providers)
- Find Azure's TLS, DDoS, and CDN security specifications for Static Web Apps

### 6. Content Security Policy (CSP) Best Practices

- Find Mozilla MDN guidance on CSP headers for static sites
- Find OWASP CSP cheat sheet recommendations
- Find Google's research on CSP adoption and effectiveness
- Compare CSP configurability: self-hosted static sites vs. Atlassian Cloud (what CSP does Confluence Cloud use? Can customers customize it?)

### 7. Plugin and Extension Security Risk

- Find security incidents caused by Confluence Marketplace plugins or Atlassian Connect apps
- Find Atlassian's own documentation on plugin/app permission models and security review process
- Compare: runtime plugins (execute in production) vs. build-time plugins (execute only in CI, never in production)
- Find industry guidance on third-party plugin risk assessment

### 8. Separation of Duties and Least Privilege

- Find NIST SP 800-53 controls related to separation of duties (AC-5) and least privilege (AC-6) and how they apply to documentation publishing
- Find guidance from security frameworks on why "author = publisher" is a control weakness
- Find research or case studies on PR-based approval workflows as a separation-of-duties control

### 9. Data Sovereignty and Residency

- Find Atlassian's data residency documentation — what regions are available, what data is covered, what data is excluded from residency controls
- Find Azure Static Web Apps regional deployment options
- Find guidance from GDPR, UK GDPR, or industry bodies on data residency requirements for documentation platforms

### 10. Comparative Breach Data

- Find any public reports of organizations breached through their Confluence instance (not just CVEs, but actual breach reports)
- Find whether any static site hosting platform (Netlify, Vercel, Azure SWA, GitHub Pages, Cloudflare Pages) has had a comparable security incident
- Find any Gartner, Forrester, or industry analyst research comparing the security of wiki/CMS platforms vs. static site generators

### Output Format

For each source found, provide:

- **Source**: Organization or author name
- **Title**: Document or publication title
- **Date**: Publication or last-updated date
- **URL**: Direct link
- **Key Finding**: 1-3 sentence summary of the relevant finding
- **Relevance**: Which of the 10 areas above it supports

Prioritize: government sources (NIST, CISA), standards bodies (OWASP, CIS, ISO), vendor documentation (Microsoft, Atlassian, GitHub), and peer-reviewed research. Deprioritize blog posts unless from recognized security researchers.

---

## Research Results

*Pending — results will be incorporated into the security comparison pages once the deep research is complete.*

---

## How Results Were Used

Once the research completes, findings will be integrated into:

| Page | What Gets Added |
|------|----------------|
| [Security Comparison](security-comparison.md) | CVE citations, framework references, comparative data |
| [Pipeline Security Gates](pipeline-security-gates.md) | SLSA framework alignment, OWASP CI/CD references |
| [Security Headers and Attack Surface](headers-and-attack-surface.md) | OWASP and NIST surface reduction guidance, CSP best practices |
| [Access Control and Audit Trail](access-control-and-audit.md) | NIST SP 800-53 controls, Git audit trail compliance references |
| [Data Protection](data-protection.md) | Data sovereignty guidance, GDPR considerations |
