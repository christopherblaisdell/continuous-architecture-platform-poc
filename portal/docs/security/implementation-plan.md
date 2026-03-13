# Security Implementation Plan — From Documentation to Working Demo

<!-- PUBLISH -->

| | |
|-----------|-------|
| **Author** | Architecture Practice |
| **Date** | 2026-03-13 |
| **Status** | Approved for Backlog |
| **Ticket** | NTK-10010 |
| **Purpose** | Implement the security controls documented in the Security Model section so they can be demoed as actually working in the NovaTrek platform |

!!! note "Fictional Domain"
    Everything on this portal is entirely fictional. NovaTrek Adventures is a completely fictitious company. The security controls described here reference real tools and real implementation patterns — the enterprise context is synthetic.

---

## Overview

The [Security Model](index.md) section of this portal documents a comprehensive case for why the docs-as-code architecture is more secure than Confluence. The controls are described in detail, but not all of them are fully implemented in the repository today.

This plan defines four implementation sprints — each producing something that can be demoed live. Every item maps to a specific file change that can be demonstrated in a browser, a terminal, or a GitHub Actions run.

The four sprints are:

| Sprint | Theme | Demo-able Outcome |
|--------|-------|-------------------|
| Sprint 1 | Headers and HSTS | Open DevTools, show all security headers live on the portal |
| Sprint 2 | CODEOWNERS and Branch Protection | Show that a PR touching `staticwebapp.config.json` cannot merge without security team approval |
| Sprint 3 | Snyk Token and Live Gate | Show a PR fail because of a real dependency vulnerability |
| Sprint 4 | Signed Commits and Audit Trail | Show a cryptographically verified commit chain in GitHub |

---

## Sprint 1 — Security Headers and HSTS Hardening

**Source documentation**: [Headers and Attack Surface](headers-and-attack-surface.md), CSP Hardening Roadmap

**What is missing today**: The `staticwebapp.config.json` file is missing the `Strict-Transport-Security` (HSTS) header and two defensive CSP directives (`form-action`, `base-uri`).

**Changes required**:

### 1A — Add HSTS Header

File: `portal/staticwebapp.config.json`

Add to `globalHeaders`:

```json
"Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload"
```

This tells browsers to only ever connect to `architecture.novatrek.cc` over HTTPS for the next year, even if the user types `http://`. Once the preload directive is added and the site is submitted to [hstspreload.org](https://hstspreload.org), browsers enforce this before even making a DNS request.

### 1B — Add `form-action` CSP Directive

File: `portal/staticwebapp.config.json`

Append to the `Content-Security-Policy` header value:

```
form-action 'none';
```

The portal has no forms. `form-action 'none'` prevents any form submission, eliminating a class of cross-site request forgery and data exfiltration attacks.

### 1C — Add `base-uri` CSP Directive

File: `portal/staticwebapp.config.json`

Append to the `Content-Security-Policy` header value:

```
base-uri 'self';
```

Prevents base tag injection attacks where an attacker injects a `<base>` tag to redirect all relative URLs to an attacker-controlled domain.

**Demo**: After deployment, open [https://architecture.novatrek.cc](https://architecture.novatrek.cc) in Chrome DevTools (Network tab, select any request, Headers tab). Show:
- `strict-transport-security: max-age=31536000; includeSubDomains; preload`
- `content-security-policy` includes `form-action 'none'; base-uri 'self'`

Additionally, test with [securityheaders.com](https://securityheaders.com/?q=architecture.novatrek.cc) to show the A+ rating.

**Effort**: 1 commit to `portal/staticwebapp.config.json`

**Risk**: Low. HSTS should be applied after confirming HTTPS is stable (Azure Static Web Apps handles this — managed certificates, auto-renewal). The `form-action` and `base-uri` directives are additive and do not break existing functionality.

---

## Sprint 2 — CODEOWNERS and Required Reviews

**Source documentation**: [Access Control and Audit Trail](access-control-and-audit.md), CODEOWNERS Example section

**What is missing today**: There is no `CODEOWNERS` file in the repository. This means any reviewer can approve a PR touching `portal/staticwebapp.config.json` — including one that weakens the CSP or removes HSTS.

**Changes required**:

### 2A — Create `.github/CODEOWNERS`

File: `.github/CODEOWNERS` (new file)

```
# ─── Security-relevant files require security team review ───────────────────
# Any PR touching these files must be approved by the security team before merge.

# Security headers, CSP, and routing configuration
portal/staticwebapp.config.json       @christopherblaisdell

# Azure infrastructure definitions
infra/                                @christopherblaisdell

# CI/CD pipeline definitions (including this file)
.github/                              @christopherblaisdell

# Security documentation
portal/docs/security/                 @christopherblaisdell

# Data isolation audit script
scripts/audit-data-isolation.sh       @christopherblaisdell
```

Note: In a real enterprise deployment, `@christopherblaisdell` would be replaced with a GitHub team slug (e.g., `@novatrek/security-team`). For the NovaTrek proof-of-concept, the repository owner serves as the security reviewer.

### 2B — Enable Branch Protection Rules (GitHub Settings)

This is a GitHub repository settings change, not a file change. It cannot be made via a PR. The following settings must be enabled on the `main` branch:

| Setting | Value | Purpose |
|---------|-------|---------|
| Require a pull request before merging | On | No direct pushes to main |
| Required approvals | 1 | At least one reviewer must approve |
| Dismiss stale reviews on new commits | On | Re-review required after changes |
| Require review from Code Owners | On | CODEOWNERS takes effect for restricted paths |
| Require status checks to pass | On | CI gates are enforced |
| Require branches to be up to date | On | Prevents stale branches bypassing gates |
| Restrict who can push to matching branches | On | Only CI service account can merge |

**Demo**: 
1. Open a PR that modifies `portal/staticwebapp.config.json`
2. Show that GitHub blocks merge with "Review required from CODEOWNERS" 
3. Show the specific reviewer(s) listed in the CODEOWNERS requirement
4. Show that merging without that approval is blocked even if other approvals exist

**Effort**: 1 commit to `.github/CODEOWNERS` + 1 GitHub Settings change

**Risk**: Low. CODEOWNERS only adds a reviewer requirement — it does not break anything. Test first on a non-sensitive path before applying to `portal/staticwebapp.config.json`.

---

## Sprint 3 — Snyk Live Gate with SNYK_TOKEN

**Source documentation**: [Pipeline Security Gates](pipeline-security-gates.md), Gates 4-6

**What is missing today**: The `snyk-security.yml` workflow file exists, but without the `SNYK_TOKEN` secret configured in GitHub, all three scan jobs will fail immediately with an authentication error rather than performing the scans. The gates exist in code but cannot run.

**Changes required**:

### 3A — Configure SNYK_TOKEN Secret in GitHub

This is a GitHub repository settings change. Steps:

1. Create a free Snyk account at [snyk.io](https://snyk.io)
2. Create an organization in Snyk for NovaTrek Adventures
3. Generate a service account token in Snyk organization settings
4. In GitHub repository settings → Secrets and variables → Actions, add:
   - Name: `SNYK_TOKEN`
   - Value: the Snyk service account token

### 3B — Import Repository into Snyk Dashboard

In the Snyk dashboard:
1. Connect GitHub integration
2. Import `continuous-architecture-platform-poc` repository
3. Enable continuous monitoring (Snyk will open automated PRs when new CVEs are discovered)

### 3C — Add Snyk Badge to Security Index Page

File: `portal/docs/security/index.md`

Add a Snyk vulnerability badge that shows live scan status:

```markdown
[![Known Vulnerabilities](https://snyk.io/test/github/christopherblaisdell/continuous-architecture-platform-poc/badge.svg)](https://snyk.io/test/github/christopherblaisdell/continuous-architecture-platform-poc)
```

**Demo**:

Scenario A — show a passing gate:
1. Open a PR on the branch (e.g., a documentation change to `portal/docs/security/index.md`)
2. Show the three Snyk jobs running in GitHub Actions: Snyk Dependency Scan, Snyk Code Analysis, Snyk IaC Scan
3. Show all three passing (green)
4. Show the Snyk dashboard with zero vulnerabilities

Scenario B — show a blocking gate (for maximum demo impact):
1. Temporarily add a vulnerable package to `requirements-docs.txt` (e.g., `Pillow==9.0.0`, which has known CVEs)
2. Open a PR
3. Show the Snyk Dependency Scan job failing with a specific CVE report
4. Show that the PR cannot be merged until the vulnerability is fixed
5. Remove the vulnerable package and show the gate going green

**Effort**: No code changes required for the workflow (already implemented). 1 GitHub Settings change + 1 Snyk dashboard action + optional badge commit.

**Risk**: Low. Snyk free tier supports the scans needed for this demo. The `continue-on-error: true` on the SARIF upload step means the workflow will not fail due to the security events upload — only actual vulnerabilities block the merge.

---

## Sprint 4 — Signed Commits and Immutable Audit Trail

**Source documentation**: [Access Control and Audit Trail](access-control-and-audit.md), Git as Immutable Audit Trail

**What is missing today**: The repository does not currently enforce signed commits. While Git's content-addressed object model provides tamper evidence (any change breaks the SHA chain), commit signing with GPG or SSH keys adds cryptographic proof of authorship.

**Changes required**:

### 4A — Enable Required Signed Commits (GitHub Settings)

In GitHub repository settings → Branches → Branch protection rules for `main`:

- Enable: "Require signed commits"

This means every commit that reaches `main` — including merge commits from PRs — must be signed with a GPG or SSH key.

### 4B — Enable Vigilant Mode for Commit Verification

In GitHub account settings → SSH and GPG keys:

- Enable "Vigilant mode" — this marks all unsigned commits with an "Unverified" badge in the GitHub UI, making it visually obvious which commits lack cryptographic proof of authorship.

### 4C — Document the Audit Trail Demonstration Script

File: `portal/docs/security/access-control-and-audit.md`

Add a demonstration section showing the commands that prove the audit trail is intact:

```bash
# Show the complete, cryptographically-linked commit history
git log --show-signature --oneline

# Verify a specific commit's signature
git verify-commit <commit-hash>

# Show the full audit record for a specific file change
git log --follow --patch portal/staticwebapp.config.json

# Show which PR approved a specific commit
gh pr list --search "sha:<commit-hash>"
```

**Demo**:
1. Show `git log --show-signature` output — each commit shows GPG/SSH signature and "Good signature from..."
2. Show a commit in the GitHub UI with the green "Verified" badge
3. Navigate to any page on the portal, click the "Edit" pencil → show it opens a PR workflow (not direct edit)
4. Show the commit that changed `portal/staticwebapp.config.json` — author, timestamp, approving reviewer, CI run results all visible
5. Compare with Confluence: show a Confluence page history with "Anonymous" actor entries (use a screenshot from the research report)

**Effort**: 1 GitHub Settings change + 1 GPG/SSH key configuration + optional documentation update

**Risk**: Low for the settings change. The commit signing requirement only applies to `main` — contributors can commit unsigned to feature branches and sign the merge commit.

---

## Consolidated Demo Script

The following is a structured 15-minute demo flow that shows all four sprints working together. Intended audience: security team, management, or anyone evaluating the platform's security posture.

### Demo Flow

**Opening (2 min)**

> "The NovaTrek Architecture Portal uses a docs-as-code model. Every documentation change goes through the same security controls as production code. Let me show you those controls working live."

**Step 1 — Security Headers (3 min)**

1. Open [https://architecture.novatrek.cc](https://architecture.novatrek.cc) in Chrome
2. Open DevTools → Network → select any request → Headers
3. Show `strict-transport-security`, `content-security-policy`, `x-frame-options`, `x-content-type-options`, `referrer-policy`, `permissions-policy`
4. Open [securityheaders.com](https://securityheaders.com/?q=architecture.novatrek.cc) → show the A+ rating
5. Say: "Confluence cannot show you this screen — their headers are managed by Atlassian and you have no control over them."

**Step 2 — CODEOWNERS Gate (3 min)**

1. Open a PR in GitHub that modifies `portal/staticwebapp.config.json`
2. Show the "Review required from CODEOWNERS" block on the PR
3. Show the specific file that triggered the review requirement
4. Say: "Any attempt to weaken the security headers — remove HSTS, loosen the CSP — is blocked until the security team reviews it. This is enforced by the platform, not by hoping someone notices."

**Step 3 — Snyk Live Gate (4 min)**

1. Show the `snyk-security.yml` workflow file
2. Open a recent PR and show the Snyk CI checks (three jobs)
3. Show the Snyk dashboard at [app.snyk.io](https://app.snyk.io) — zero vulnerabilities in the repo
4. If doing the advanced demo: add `Pillow==9.0.0` to requirements, show the scan fail with a CVE report, show merge blocked
5. Say: "If someone adds a dependency that has a known security vulnerability, the PR cannot merge. Confluence cannot scan its own dependencies — organizations have no visibility until Atlassian publishes a bulletin."

**Step 4 — Audit Trail (3 min)**

1. In GitHub, navigate to any committed file (e.g., `portal/staticwebapp.config.json`)
2. Click "History" — show every change, who made it, when, what was reviewed
3. Show a commit with the "Verified" badge (signed commit)
4. Run `git log --show-signature --oneline` in the terminal — show the cryptographic verification
5. Say: "This is an immutable record. Nobody — not even a repository admin — can delete this history without breaking the cryptographic chain and triggering alerts. Confluence page history can be deleted by space admins."

**Closing (1 min)**

> "Every control you just saw is documented in the Security Model section of this portal, with citations to NIST, CISA, and OWASP. The security team can review the exact configuration files, propose changes through PRs, and see every gate that protects those changes. This is a live, auditable, demonstrably secure publishing platform."

---

## Implementation Priority Order

The sprints are ordered by demo impact vs. implementation effort:

| Priority | Sprint | Effort | Demo Impact | Requires External Account |
|----------|--------|--------|-------------|--------------------------|
| 1 | Sprint 1 — HSTS + CSP hardening | 30 min | High | No |
| 2 | Sprint 2 — CODEOWNERS | 30 min | High | No |
| 3 | Sprint 3 — Snyk live gate | 1 hr (account setup) | Very High | Yes (Snyk free) |
| 4 | Sprint 4 — Signed commits | 45 min | Medium | No |

**Recommended sequence**: Execute Sprint 1 and Sprint 2 in the same PR. Execute Sprint 3 after confirming the Snyk account is set up. Execute Sprint 4 last, as it requires a one-time key configuration for each contributor.

---

## What Each Sprint Proves

| Sprint | Security Claim Demonstrated | Documentation Reference |
|--------|----------------------------|------------------------|
| 1 | Static sites can enforce strict, version-controlled security headers that dynamic CMS platforms cannot replicate | [Headers and Attack Surface](headers-and-attack-surface.md) |
| 2 | Path-level access control via CODEOWNERS enforces separation of duties at the file level | [Access Control and Audit Trail](access-control-and-audit.md) |
| 3 | Automated dependency scanning blocks vulnerable packages before they reach production | [Pipeline Security Gates](pipeline-security-gates.md), Gates 4-6 |
| 4 | Git's cryptographic commit chain provides a tamper-evident, immutable audit trail | [Access Control and Audit Trail](access-control-and-audit.md), Section 2 |
