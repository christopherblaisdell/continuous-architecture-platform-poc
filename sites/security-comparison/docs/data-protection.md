# Data Protection

This page documents the data protection controls in the NovaTrek docs-as-code pipeline — how sensitive data is prevented from reaching the published site, how secrets are detected and blocked, and how data sovereignty is maintained.

For the complete evidence base including GitGuardian statistics and data residency analysis, see [Research Results](research-prompt-response.md), Sections 5 and 10.

---

## Defense-in-Depth: Four Layers of Data Protection

The docs-as-code pipeline prevents sensitive data from reaching the published portal through four independent layers. Each layer catches what the previous layers missed.

```
Layer 1: GitHub Push Protection ─── blocks secrets at push time
    │
Layer 2: GitHub Secret Scanning ─── continuous monitoring of committed content
    │
Layer 3: Data Isolation Audit ─── custom patterns for domain-specific data
    │
Layer 4: Snyk Code Analysis ─── static analysis of generator scripts
    │
    ▼
Content reaches production (only if all layers pass)
```

### Layer 1 — GitHub Push Protection

**What it does**: Blocks `git push` operations that contain detected secrets before they enter the repository.

!!! warning "The Scale of Secret Sprawl"
    The [2025 State of Secrets Sprawl report by GitGuardian](https://www.scribd.com/document/855773866/The-State-of-Secrets-Sprawl-2025) found **23.77 million new hardcoded secrets** in public repositories in 2024 — a **25% year-over-year increase**. Generic secrets (API keys, passwords, connection strings) account for 58% of all detected leaks. [GitHub Push Protection](https://docs.github.com/en/code-security/concepts/secret-security/about-push-protection) operates as a pre-receive hook that **rejects commits** containing detected secrets before they enter repository history.

**What it catches**:

- API keys (AWS, Azure, GCP, GitHub, etc.)
- Database connection strings
- OAuth tokens and refresh tokens
- Private keys (SSH, PGP, TLS)
- Cloud provider credentials
- Service account keys

**Why it matters**: This is the earliest possible interception point. The secret never enters the repository history, so there is nothing to clean up. In Confluence, if someone pastes an API key into a page, it is immediately published and visible to all space viewers — there is no equivalent of push protection.

**Configuration**: Enabled at the GitHub organization level. No per-repository configuration required.

### Layer 2 — GitHub Secret Scanning

**What it does**: Continuously monitors the repository for secrets that bypass push protection (e.g., secrets committed before push protection was enabled, or secrets in patterns not yet recognized by push protection).

**What it catches**: Same categories as push protection, plus:

- Custom secret patterns defined by the organization
- Secrets committed in the past (historical scanning)
- Secrets in pull request diffs

**Remediation**: When a secret is detected, GitHub creates a security alert visible to repository admins. The alert includes the file, line number, and commit where the secret was found, along with recommended remediation steps.

### Layer 3 — Data Isolation Audit

**What it does**: Scans all tracked files for patterns that indicate corporate data leakage. This is a custom control specific to the NovaTrek platform, implemented as a shell script (`scripts/audit-data-isolation.sh`) that runs in the CI pipeline.

**What it catches**:

- Real company names or internal system identifiers
- Real domain names (only `*.novatrek.example.com` is permitted)
- Corporate email patterns
- Internal project codes or system names
- References to real tools, products, or platforms that should not appear in the synthetic workspace

**Why this layer exists**: GitHub's secret scanning catches credentials, but it does not catch non-credential sensitive data like internal project names, team names, or system identifiers that could leak through documentation content. The data isolation audit fills this gap with domain-specific pattern matching.

**Implementation**: The script runs `grep` with regex patterns against all tracked files. It excludes itself and other audit-related files from scanning. Exit code 0 means clean; non-zero means violations were found.

**Blocks merge on failure**: Yes — the `validate-solution.yml` workflow includes this as a required status check.

### Layer 4 — Snyk Code Analysis

**What it does**: Static analysis of the Python generator scripts that transform YAML metadata and OpenAPI specs into published HTML pages.

**What it catches**:

- Path traversal vulnerabilities that could read files outside the expected directories
- Unsafe YAML deserialization (use of `yaml.load()` instead of `yaml.safe_load()`)
- Template injection risks in generated HTML
- Hardcoded credentials or tokens in script files

**Why this layer exists**: The generator scripts are the trust boundary — they read input (YAML, JSON, OpenAPI specs) and produce output (HTML, SVG). A vulnerability in a generator script could allow a crafted input file to exfiltrate data, inject content, or read files it should not access.

---

## Comparison with Confluence Data Protection

| Control | Docs-as-Code | Confluence |
|---------|-------------|-----------|
| Secret detection at write time | GitHub Push Protection (blocks push) | Not available |
| Continuous secret monitoring | GitHub Secret Scanning | Not available |
| Custom data pattern scanning | Data isolation audit (CI gate) | Not available |
| Code analysis of publishing tools | Snyk code analysis | Not applicable (Atlassian-managed) |
| Content review before publish | PR review (required) | Not required (edit = publish) |
| Revocation of exposed secrets | Automated alerts with remediation steps | Manual (if noticed) |

**Key difference**: Confluence provides **zero automated data protection controls** at the content level. If an author pastes a database connection string, an internal system name, or a customer's PII into a Confluence page, it is immediately published and visible to all space viewers. The only protection is the author's own judgment.

The docs-as-code pipeline provides four independent automated layers, each of which can catch data that the author inadvertently included. The content is never published until all layers pass.

---

## Data Sovereignty

As global privacy regulations (GDPR, UK GDPR, CCPA) become increasingly stringent, organizations must exert granular control over data residency.

### Where Data Lives

| Component | Location | Control |
|-----------|----------|---------|
| Source repository | GitHub (organization-selected region) | Organization controls repository visibility, access, and retention |
| CI/CD pipeline | GitHub Actions (ephemeral runners) | Runners are destroyed after each job; no persistent state |
| Published site | Azure Static Web Apps (customer-selected region) | Organization controls deployment region and access |
| CDN edge cache | Azure Front Door (global edge network) | Cached copies at edge nodes; TTL-controlled, no persistent storage |

### Confluence Data Sovereignty

| Component | Location | Control |
|-----------|----------|---------|
| Page content | Atlassian Cloud (US, EU, or AU realm) | Organization selects realm at setup; migration between realms is manual |
| Attachments | Atlassian Cloud (same realm) | Same realm as content |
| Search index | Atlassian Cloud (may differ from content realm) | Limited visibility into index location |
| Analytics data | Atlassian Cloud (may differ from content realm) | Limited visibility into analytics data location |
| Backup / DR | Atlassian-managed | Organization has no visibility into backup location or retention |

!!! warning "Atlassian Data Residency Exclusions"
    Atlassian Cloud offers [data residency](https://www.atlassian.com/trust/compliance/data-residency) capabilities, but certain data types are **explicitly excluded** from residency controls. Operational telemetry, user account metadata, and application analytics may continue to be routed globally regardless of the selected realm. Organizations subject to GDPR, UK GDPR, or CCPA requirements should evaluate whether these exclusions create compliance gaps.

**Key difference**: With docs-as-code, the organization controls exactly where every component lives and can verify it through Azure and GitHub dashboards. Because there is no backend telemetry database, the organization sidesteps the opaque residency exclusions inherent to managed SaaS wikis. With Confluence Cloud, the organization selects a realm but has limited visibility into where all data components actually reside, especially for supporting services like search and analytics.

---

## Incident Response Comparison

### Scenario: Sensitive Data Published Accidentally

**In Confluence**:

1. Author notices (or is alerted) that sensitive data is on a published page
2. Author or admin edits the page to remove the data
3. **The sensitive data remains in page history** — anyone with page view access can see previous versions
4. A space admin must manually delete the specific page version containing the sensitive data
5. If the page was cached by browsers, CDNs, or search engines, the sensitive data may persist outside Confluence
6. There is no automated notification or audit when sensitive data is published

**In Docs-as-Code**:

1. In most cases, the sensitive data **never reaches production** — it is caught by push protection, secret scanning, or the data isolation audit
2. If it somehow passes all gates, the remediation is:
    - Revert the commit: `git revert <hash>` (removes from published site within minutes)
    - Force-remove from Git history if needed: `git filter-branch` or BFG Repo-Cleaner
    - Rotate any exposed credentials (GitHub secret scanning provides remediation steps)
    - Azure CDN cache can be purged immediately
3. The incident itself is fully traceable: which PR introduced it, who approved it, which CI gates it passed (and why), and when it was remediated
4. Post-incident: add a new pattern to the data isolation audit to prevent recurrence

**Key difference**: The docs-as-code model prevents the incident in most cases and provides complete traceability when it does not. Confluence relies entirely on manual detection and manual remediation, with sensitive data persisting in page history unless manually purged.
