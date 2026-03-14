# Security Implementation Status

<!-- PUBLISH -->

This page tracks the current implementation state of every security control described in the [Security Model](index.md) section. It distinguishes controls that are **live and enforced** from those that are **planned** or **aspirational**, so the security team can assess actual posture rather than intended posture.

!!! note "Fictional Domain"
    Everything on this portal is entirely fictional. NovaTrek Adventures is a completely fictitious company. All pipeline and security references describe the NovaTrek proof-of-concept implementation.

---

## Summary

| Control | Status | Where Enforced |
|---------|--------|----------------|
| YAML metadata validation | IMPLEMENTED | `validate-solution.yml` |
| Solution folder structure validation | IMPLEMENTED | `validate-solution.yml` |
| Data isolation audit | IMPLEMENTED | `validate-solution.yml` |
| Portal build (link + generator validation) | IMPLEMENTED | `validate-solution.yml`, `docs-deploy.yml` |
| Confluence dry-run validation | IMPLEMENTED | `docs-deploy.yml` |
| PR review approval (branch protection) | IMPLEMENTED | GitHub branch protection rules |
| Production build (post-merge) | IMPLEMENTED | `docs-deploy.yml` |
| Static asset integrity | IMPLEMENTED | `generate-all.sh` + `docs-deploy.yml` |
| Azure platform security (DDoS, TLS, CDN) | IMPLEMENTED | Azure Static Web Apps (managed) |
| HTTP security headers (CSP, HSTS, etc.) | IMPLEMENTED | `portal/staticwebapp.config.json` |
| GitHub Push Protection (secret scanning) | IMPLEMENTED | GitHub organisation settings |
| Dependabot (automated dependency updates) | IMPLEMENTED | `.github/dependabot.yml` |
| Snyk dependency scan | CONFIGURED | `docs-security.yml` (requires `SNYK_TOKEN` secret) |
| Snyk code analysis | CONFIGURED | `docs-security.yml` (requires `SNYK_TOKEN` secret) |
| Snyk IaC scan | CONFIGURED | `docs-security.yml` (requires `SNYK_TOKEN` secret) |
| mark binary version-pinned | IMPLEMENTED | `docs-deploy.yml` — pinned to `10.1.0` |
| OIDC / Workload Identity Federation | PLANNED | Replace `AZURE_STATIC_WEB_APPS_API_TOKEN` with federated identity |

**Status key:**
- **IMPLEMENTED** — active, enforced, blocks merge or deploy on failure
- **CONFIGURED** — workflow and gate exist; requires a secret or external service to be active
- **PLANNED** — identified as a next step; not yet implemented

---

## Implemented Controls Detail

### Gate 1 — YAML Metadata Validation

**Workflow**: `validate-solution.yml`
**Trigger**: PRs touching `architecture/solutions/**` or `architecture/metadata/**`
**Evidence**: Runs `yaml.safe_load()` against every file in `architecture/metadata/*.yaml`

### Gate 2 — Solution Folder Structure Validation

**Workflow**: `validate-solution.yml`
**Trigger**: Same as Gate 1
**Evidence**: Checks for `*-solution-design.md` and `3.solution/c.capabilities/capabilities.md` in every `_NTK-*` folder

### Gate 3 — Data Isolation Audit

**Workflow**: `validate-solution.yml`
**Trigger**: Same as Gate 1
**Evidence**: Runs `scripts/audit-data-isolation.sh` — regex patterns catch real company names, domains, and credentials

### Gate 4 — Portal Build

**Workflow**: `validate-solution.yml`, `docs-deploy.yml`
**Trigger**: All PRs (via `docs-deploy.yml`); solution PRs additionally via `validate-solution.yml`
**Evidence**: `bash portal/scripts/generate-all.sh` — runs all generators and `mkdocs build`

### Gate 5 — Confluence Dry-Run

**Workflow**: `docs-deploy.yml` (`validate-confluence` job)
**Trigger**: PRs to `main`
**Evidence**: Runs `mark --dry-run` against prepared Confluence Markdown output

### Gate 6 — PR Review Approval

**Configuration**: GitHub branch protection rules on `main`
**Evidence**: Requires at least 1 approving review; stale reviews dismissed on new commits; self-approval blocked

### Gates 7-8 — Production Build and Static Asset Integrity

**Workflow**: `docs-deploy.yml` (`build` then `deploy` jobs)
**Trigger**: Push to `main`
**Evidence**: Full rebuild from `main` before deploy; `generate-all.sh` copies SVGs, OpenAPI specs, and `staticwebapp.config.json` into `portal/site/`

### Gate 9 — Azure Platform Security

**Platform**: Azure Static Web Apps
**Evidence**: TLS 1.2 minimum (managed certificates), Azure Front Door CDN edge, DDoS protection included, staging environments isolated from production

### HTTP Security Headers

**File**: `portal/staticwebapp.config.json`
**Evidence**: `X-Frame-Options: SAMEORIGIN`, `X-Content-Type-Options: nosniff`, `Referrer-Policy`, `Permissions-Policy`, `Content-Security-Policy` — all version-controlled and deployed as part of Gate 8

### Dependabot

**File**: `.github/dependabot.yml`
**Evidence**: Weekly PRs for GitHub Actions version bumps and Python package updates in `requirements-docs.txt`. PRs pass through the normal CI gate stack before merge.

---

## Configured Controls — Activation Required

### Snyk Scanning (dependency, code, IaC)

**Workflow**: `docs-security.yml`
**Status**: Workflow is committed and will run; results are informational until `SNYK_TOKEN` is added as a repository secret.

**To activate**:

1. Create a free or team Snyk account at [snyk.io](https://snyk.io)
2. Generate an API token from Snyk settings
3. Add it as a repository secret: `Settings → Secrets and variables → Actions → SNYK_TOKEN`
4. The three jobs (`snyk-deps`, `snyk-code`, `snyk-iac`) will then enforce HIGH/CRITICAL thresholds on every relevant PR

**What each job checks**:

| Job | Target | Blocks merge on |
|-----|--------|-----------------|
| `snyk-deps` | `requirements-docs.txt` | HIGH or CRITICAL CVE in any Python build dependency |
| `snyk-code` | `portal/scripts/` | Snyk Code finding in generator scripts (path traversal, unsafe deserialization, injection) |
| `snyk-iac` | `portal/staticwebapp.config.json`, `.github/workflows/` | HIGH or CRITICAL IaC misconfiguration |

---

## Planned Controls

### OIDC / Workload Identity Federation

**Current state**: `docs-deploy.yml` authenticates to Azure Static Web Apps using `AZURE_STATIC_WEB_APPS_API_TOKEN` — a long-lived secret stored in GitHub Actions secrets.

**Why it matters**: Long-lived credentials can leak and do not automatically rotate. OWASP CICD-SEC-6 cites insufficient credential hygiene as a top CI/CD risk.

**Planned approach**: Replace the API token with Azure Workload Identity Federation (OIDC). The GitHub Actions runner authenticates directly to Azure using a short-lived, automatically rotated OIDC token — no secret is stored.

**Implementation steps** (when ready):

1. Create an App Registration in Azure Entra ID for the repository
2. Add a Federated Identity Credential linking `repo:christopherblaisdell/continuous-architecture-platform-poc:ref:refs/heads/main` to the app registration
3. Assign `Static Web Apps Contributor` role to the app registration on the SWA resource
4. Update `docs-deploy.yml` to use `azure/login@v2` with OIDC and remove `azure_static_web_apps_api_token`

---

## What Changed in This Update

The following items moved from aspirational to implemented or configured in this update:

| Item | Before | After |
|------|--------|-------|
| Dependabot | Not configured | IMPLEMENTED — `.github/dependabot.yml` added |
| Snyk scanning workflow | No workflow file | CONFIGURED — `docs-security.yml` added; awaiting `SNYK_TOKEN` |
| `mark` binary version | Unpinned (`latest`) | IMPLEMENTED — pinned to `10.1.0` in `docs-deploy.yml` |
