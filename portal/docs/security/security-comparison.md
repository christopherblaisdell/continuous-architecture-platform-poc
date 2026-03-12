# Security Comparison — Docs-as-Code vs. Confluence

A side-by-side evaluation of security controls across 12 dimensions. For each dimension, we assess whether Confluence or the docs-as-code model (Git + MkDocs + CI/CD + Azure Static Web Apps) provides stronger guarantees.

!!! note "Fictional Domain"
    Everything on this portal is entirely fictional. NovaTrek Adventures is a completely fictitious company. All examples reference synthetic NovaTrek systems only.

---

## Summary Scorecard

| Dimension | Confluence | Docs-as-Code | Advantage |
|-----------|-----------|--------------|-----------|
| 1. Change Authorization | Page-level edit permissions | Branch protection + PR approval | Docs-as-Code |
| 2. Audit Trail | Page history (editable) | Git log (immutable) | Docs-as-Code |
| 3. Pre-publish Validation | None (direct publish) | CI/CD gates block merge | Docs-as-Code |
| 4. Secret Scanning | Not available | Automated in CI pipeline | Docs-as-Code |
| 5. Attack Surface | Full web application (Java, DB, plugins) | Static HTML files (no server-side code) | Docs-as-Code |
| 6. Content Security Policy | Atlassian-managed (limited control) | Fully controlled via `staticwebapp.config.json` | Docs-as-Code |
| 7. Dependency Scanning | Atlassian-managed (no visibility) | OWASP + Trivy scans in CI | Docs-as-Code |
| 8. Rollback | Page-by-page version restore | `git revert` (atomic, full-site rollback) | Docs-as-Code |
| 9. Data Sovereignty | Atlassian Cloud (US/EU regions) | Azure region of your choice | Docs-as-Code |
| 10. Plugin/Extension Risk | Marketplace plugins run with full permissions | No plugins at runtime (build-time only) | Docs-as-Code |
| 11. Authentication | Atlassian account or SSO | Azure AD / Entra ID integration | Tie |
| 12. Separation of Duties | Editors = publishers (no separation) | Authors, reviewers, and deployers are distinct roles | Docs-as-Code |

**Result: Docs-as-Code is stronger in 11 of 12 dimensions.**

---

## Detailed Analysis

### 1. Change Authorization

**Confluence**: Any user with "Edit" permission on a page can modify and immediately publish content. There is no staging, no review, and no approval required. Space-level permissions are coarse — granting edit access to a space grants edit access to all pages within it. Restricted pages exist but must be manually applied page-by-page and are routinely forgotten.

**Docs-as-Code**: Content changes follow the same workflow as code changes:

1. Author creates a branch and makes changes
2. Author opens a pull request
3. Required reviewers must approve the PR (enforced by branch protection rules)
4. CI/CD pipeline must pass all gates (YAML validation, data isolation audit, portal build)
5. Only after approval AND passing gates can the PR be merged to `main`
6. Merge to `main` triggers the deploy pipeline — authors never directly publish

This means no single person can both write and publish content without at least one other person reviewing it.

### 2. Audit Trail

**Confluence**: Page history shows who edited what, but:

- Page history can be pruned or deleted by space admins
- Bulk changes (e.g., search-and-replace across pages) leave minimal trace
- API-based edits may not show meaningful diffs
- There is no record of who read a page (without Atlassian Analytics premium)

**Docs-as-Code**: Git provides a cryptographically-linked, append-only audit log:

- Every change has: author, timestamp, commit message, exact diff, and reviewer approvals
- Git history cannot be altered without force-push (which branch protection rules block)
- PR conversations, review comments, and approval records are permanently stored
- CI/CD pipeline logs record every gate that was checked for every deploy

### 3. Pre-publish Validation

**Confluence**: There are no automated gates between editing and publishing. Content is live the moment "Publish" is clicked. The only safeguard is page restrictions, which prevent editing but not publishing mistakes by authorized editors.

**Docs-as-Code**: The NovaTrek portal enforces the following gates before any content reaches production (see [Pipeline Security Gates](pipeline-security-gates.md) for details):

- YAML metadata validation (syntax correctness)
- Solution folder structure validation (completeness)
- Data isolation audit (prevents corporate data leakage)
- Full portal build (catches broken links, missing files)
- Confluence dry-run validation (for the read-only mirror)
- PR review approval (human gate)

If any gate fails, the PR cannot be merged.

### 4. Secret Scanning

**Confluence**: No built-in secret scanning. If someone pastes an API key, database password, or access token into a Confluence page, it is immediately published. There is no mechanism to detect or prevent this.

**Docs-as-Code**: GitHub provides:

- **Push protection**: Blocks pushes containing detected secrets (API keys, tokens, passwords)
- **Secret scanning**: Continuously monitors the repository for accidentally committed secrets
- **Custom patterns**: Organizations can define regex patterns for internal secret formats
- **Data isolation audit**: The NovaTrek platform runs a custom audit script that scans for corporate identifiers, real domain names, and other sensitive patterns before every merge

### 5. Attack Surface

**Confluence**: Confluence Cloud is a full Java web application with:

- Server-side code execution
- PostgreSQL database with stored procedures
- Plugin runtime environment (third-party code runs with application permissions)
- Rich text editor with XSS vectors
- REST API with authentication endpoints
- File upload and attachment processing
- Macro rendering engine

Each component is a potential attack vector. Atlassian has experienced security incidents (e.g., CVE-2023-22515, CVE-2023-22518) that allowed remote code execution on Confluence instances.

**Docs-as-Code**: The published portal is a collection of static HTML, CSS, and JavaScript files. There is:

- No server-side code execution
- No database
- No file upload capability
- No user input processing
- No authentication endpoints (authentication is handled at the Azure platform level, entirely separate from content)
- No plugin runtime

The attack surface of a static site is fundamentally smaller. The only vectors are the HTTP headers (which are fully controlled) and the content itself (which is validated before publish).

### 6. Content Security Policy

**Confluence**: CSP headers are managed by Atlassian. Organizations have limited ability to customize them. The CSP must accommodate the Confluence editor, macro engine, and all installed marketplace plugins, which inherently requires a permissive policy.

**Docs-as-Code**: The NovaTrek portal defines its CSP explicitly in `staticwebapp.config.json`:

```json
{
  "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://unpkg.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://unpkg.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https:; connect-src 'self'"
}
```

This CSP is version-controlled, reviewed in PRs, and can be tightened progressively. The security team can see exactly what is permitted and propose changes through the same PR workflow.

### 7. Dependency Scanning

**Confluence**: Organizations have no visibility into Confluence Cloud's dependency tree. Atlassian manages patching on their own schedule. When a vulnerability is discovered in a Confluence dependency, organizations must wait for Atlassian to release and deploy a fix.

**Docs-as-Code**: The NovaTrek platform runs dependency scanning at multiple levels:

- **Snyk**: Scans Python dependencies (`requirements-docs.txt`), generator source code (`portal/scripts/`), and infrastructure-as-code (`staticwebapp.config.json`, Bicep templates) for vulnerabilities and misconfigurations. Runs in CI as a merge-blocking gate and continuously monitors the repository for newly disclosed vulnerabilities
- **OWASP Dependency Check**: Scans Gradle dependencies in service builds
- **Trivy**: Scans Docker container images for known CVEs, failing the build on CRITICAL or HIGH severity
- **Dependabot / Renovate**: Automated PRs for dependency updates

All scan results are visible in CI logs and can block deployment. Snyk adds continuous monitoring — if a new CVE is published for a dependency that was clean at merge time, Snyk opens an automated PR with the fix.

### 8. Rollback

**Confluence**: Rolling back a change requires:

1. Identifying which pages were affected
2. Navigating to each page individually
3. Finding the correct version in page history
4. Restoring each page one at a time

For bulk changes (e.g., a generator that updated 19 service pages), this is impractical.

**Docs-as-Code**: Rolling back any change is a single command:

```bash
git revert <commit-hash>
```

This creates a new commit that undoes the entire change atomically, triggers the CI/CD pipeline, and deploys the reverted version. The rollback itself goes through the same audit trail and review process. For emergencies, a previously-built artifact can be redeployed in seconds.

### 9. Data Sovereignty

**Confluence Cloud**: Data is stored in Atlassian's infrastructure. While Atlassian offers data residency options (US, EU, Australia), organizations have limited control over exactly where data resides, how it is replicated, and who at Atlassian can access it.

**Docs-as-Code**: The published site lives in an Azure Static Web App in the region of your choice. The source lives in your GitHub organization. Both are within your organization's existing cloud governance boundary, covered by existing Azure and GitHub enterprise agreements.

### 10. Plugin and Extension Risk

**Confluence**: Marketplace plugins are a significant risk vector:

- Plugins run with the same permissions as Confluence itself
- Plugin code is not reviewed by your security team
- Plugins can access all page content, user data, and space configurations
- Plugin vulnerabilities have led to data breaches (e.g., CVE-2022-26134 was exploited via a plugin vector)

**Docs-as-Code**: MkDocs extensions (plugins) run only at **build time** in the CI/CD pipeline. They:

- Never run on the production server (there is no server)
- Cannot access production data
- Are listed in `requirements-docs.txt` (version-pinned, auditable)
- Can be scanned by dependency tools like any other Python package
- Run in ephemeral CI containers that are destroyed after each build

### 11. Authentication

**Confluence Cloud**: Supports Atlassian accounts and SAML SSO integration. Well-established but requires trusting Atlassian's identity management.

**Docs-as-Code (Azure Static Web Apps)**: Supports Azure AD / Entra ID natively, plus custom authentication providers. If the portal needs restricted access, Azure Static Web Apps supports built-in authentication with role-based access control configured in `staticwebapp.config.json`. This integrates with the same identity provider your organization already uses.

For public architecture portals (like NovaTrek's), authentication is not required because the content is intentionally public. This is a deliberate design choice, not a security gap.

### 12. Separation of Duties

**Confluence**: The person who writes content is the same person who publishes it. There is no separation between the "author" and "publisher" roles. A space admin can both write and approve their own content.

**Docs-as-Code**: Roles are naturally separated:

| Role | Responsibility | Cannot Do |
|------|---------------|-----------|
| **Author** | Create branches, write content, open PRs | Merge to `main`, deploy |
| **Reviewer** | Review PRs, approve changes | Bypass CI gates, self-approve |
| **CI Pipeline** | Run security gates, build, deploy | Approve PRs, modify content |
| **Admin** | Configure branch protection rules | Bypass rules without audit trail |

Branch protection rules enforce these boundaries at the platform level. GitHub audit logs record any changes to branch protection settings, providing oversight on the oversight.

---

## Common Objections

### "But Confluence has page restrictions"

Page restrictions prevent editing, but they must be manually applied to each page and are easily forgotten. They do not provide pre-publish validation, secret scanning, or audit trail immutability. They are a single control where docs-as-code provides defense in depth.

### "Our team is not technical enough for Git"

Architecture documentation is already written by technical staff (architects, engineers). The PR workflow is simpler than it appears: write Markdown, commit, open PR, get review, merge. Many organizations have successfully adopted this workflow for documentation. The GitHub web editor allows editing without command-line Git knowledge.

### "We lose real-time collaboration"

MkDocs Material supports `mkdocs serve` for local preview and PR preview environments for shared review. For real-time co-editing (rare for architecture documentation), the source files can be edited in VS Code Live Share or GitHub Codespaces. Architecture documents are typically authored by one person and reviewed by a group — the PR model fits this workflow naturally.

### "We cannot control who accesses the site"

Azure Static Web Apps supports built-in authentication with Entra ID. Access can be restricted to specific groups, roles, or individuals using the same `staticwebapp.config.json` that controls security headers. This is often more granular than Confluence space permissions.
