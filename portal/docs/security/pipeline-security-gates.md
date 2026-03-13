# Pipeline Security Gates

Every piece of content published to the NovaTrek Architecture Portal passes through a series of automated security gates in the CI/CD pipeline. No content can reach production without passing all gates. This is fundamentally different from wiki-based platforms where content is published the moment an author clicks "Save."

For the complete evidence base including NIST, SLSA, and OWASP citations, see [Research Results](research-prompt-response.md).

!!! note "Fictional Domain"
    Everything on this portal is entirely fictional. NovaTrek Adventures is a completely fictitious company. All pipeline references describe the NovaTrek proof-of-concept implementation.

---

## Gate Architecture

```
Author writes content
    │
    ▼
Feature branch (git push)
    │
    ├─── GitHub Push Protection ─── blocks commits containing secrets
    │
    ▼
Pull Request opened
    │
    ├─── Gate 1: YAML Metadata Validation
    ├─── Gate 2: Solution Folder Structure Validation
    ├─── Gate 3: Data Isolation Audit
    ├─── Gate 4: Portal Build (link validation)
    ├─── Gate 5: Confluence Dry-Run (mirror validation)
    ├─── Gate 6: Snyk Security Scan (dependency, code, IaC)
    ├─── Gate 7: PR Review Approval (human gate)
    │
    ▼
Merge to main (only if ALL gates pass)
    │
    ├─── Gate 8: Production Build
    ├─── Gate 9: Snyk Security Scan (post-merge verification)
    ├─── Gate 10: Static Asset Integrity
    │
    ▼
Deploy to Azure Static Web Apps
    │
    ├─── Gate 11: Azure Platform Security (WAF, DDoS protection)
    │
    ▼
Content live on portal
```

---

## Pre-Merge Gates (PR Phase)

These gates run automatically on every pull request. All must pass before the PR can be merged. For a gate to actually block a merge, its workflow check must be added to the GitHub branch protection rules for `main` under Settings > Branches > Require status checks to pass.

### Gate 1 — YAML Metadata Validation

**What it checks**: All YAML files in `architecture/metadata/` are syntactically valid and parseable.

**Why it matters**: Malformed YAML could cause generators to produce incorrect output or fail silently, leading to missing or corrupted content on the portal.

**Implementation**: The `validate-solution.yml` workflow parses every YAML file with Python's `yaml.safe_load()` — note the use of `safe_load`, not `load`, which prevents YAML deserialization attacks.

**Blocks merge on failure**: Yes.

### Gate 2 — Solution Folder Structure Validation

**What it checks**: Every solution folder under `architecture/solutions/` contains the required artifacts:

- A master document (`*-solution-design.md`)
- A capabilities mapping (`3.solution/c.capabilities/capabilities.md`)

**Why it matters**: Incomplete solutions could reference non-existent files, causing broken links on the portal or missing capability rollup data.

**Blocks merge on failure**: Yes.

### Gate 3 — Data Isolation Audit

**What it checks**: Scans all tracked files for patterns that indicate corporate data leakage:

- Real company names or internal system identifiers
- Real domain names (only `*.novatrek.example.com` is permitted)
- Corporate email patterns
- Internal project codes or system names
- API keys, tokens, or credentials in content files

**Why it matters**: The NovaTrek workspace is synthetic by design. Any real corporate data appearing in the repository represents a data leakage incident. This gate catches it before it reaches the published site.

**Implementation**: `scripts/audit-data-isolation.sh` — a custom shell script that runs regex pattern matching against all tracked files.

**Blocks merge on failure**: Yes.

### Gate 4 — Portal Build

**What it checks**: The full MkDocs site builds successfully, including:

- All generators run (microservice pages, solution pages, capability pages, ticket pages)
- All internal links resolve to existing pages
- All referenced assets (SVGs, images) exist
- MkDocs configuration is valid

**Why it matters**: A successful build proves that the content is internally consistent. Broken links, missing files, or configuration errors are caught before they reach production.

**Blocks merge on failure**: Yes.

### Gate 5 — Confluence Dry-Run

**What it checks**: The Confluence mirror preparation script (`confluence-prepare.py`) runs successfully and the resulting Markdown passes `mark --dry-run` validation.

**Why it matters**: Even though Confluence is a read-only mirror, publishing failures there indicate content formatting issues that may also affect the primary portal.

**Blocks merge on failure**: Yes.

### Gate 6 — Snyk Security Scan

**What it checks**: Three complementary security scans run in parallel with the build:

- **Dependency scan** (`snyk test`): All Python packages in `requirements-docs.txt` are checked against the Snyk vulnerability database. Even build-time dependencies can be exploited to inject malicious content into generated HTML if compromised.
- **Code scan** (`snyk code test`): Static analysis of Python generator scripts in `portal/scripts/` detects path traversal, unsafe deserialization (generators parse YAML input), and injection risks (generators produce HTML output).
- **IaC scan** (`snyk iac test`): `portal/staticwebapp.config.json` and `.github/workflows/docs-deploy.yml` are scanned for misconfigurations — overly permissive CSP, missing security headers, and excessively broad workflow permissions.

**Why it matters**: The generator scripts are the boundary between untrusted input (YAML metadata, OpenAPI specs) and trusted output (published HTML). A misconfigured `staticwebapp.config.json` could silently strip all security headers from the production site. Snyk catches both classes of issue before they reach production.

**Implementation**: The `security-scan` job in `docs-deploy.yml` runs Snyk CLI against each target. The `security-scan` job runs in parallel with the `build` job. The `deploy` job depends on both, so deployment is blocked if any scan finds a HIGH or CRITICAL severity issue. To block PR merges, add `Security Scan` to the required status checks in branch protection rules for `main`.

**Blocks merge on failure**: Yes (HIGH or CRITICAL severity findings, when branch protection is configured).

### Gate 7 — PR Review Approval

**What it checks**: At least one designated reviewer has approved the pull request.

**Why it matters**: Automated gates catch structural and formatting issues but cannot evaluate content accuracy, architectural correctness, or appropriateness. The human review gate ensures that a second pair of eyes validates the substance of every change.

**Configuration**: GitHub branch protection rules on `main` require:

- At least 1 approving review
- Dismissal of stale approvals when new commits are pushed
- No self-approval (the PR author cannot approve their own PR)

**Blocks merge on failure**: Yes.

---

## Post-Merge Gates (Deploy Phase)

These gates run after the PR is merged to `main`, before content reaches production.

### Gate 8 — Production Build

**What it checks**: The full site builds again from the merged `main` branch. This is not redundant — it catches merge conflicts or timing issues where two PRs were individually valid but conflict when combined.

**Why it matters**: Defense in depth. Even if a PR gate was somehow bypassed, the production build catches issues before deployment.

**Blocks deployment on failure**: Yes.

### Gate 9 — Snyk Post-Merge Verification

**What it checks**: The same three Snyk scans from Gate 6 run again on the merged `main` branch before deployment proceeds.

**Why it matters**: New vulnerability advisories may have been published between the time the PR was opened and when it was merged. Running Snyk again on `main` ensures the production deployment reflects the current vulnerability landscape, not the state at PR creation time.

**Blocks deployment on failure**: Yes (the `deploy` job depends on `security-scan`).

### Gate 10 — Static Asset Integrity

**What it checks**: Non-Markdown assets (SVGs, OpenAPI specs, Swagger UI pages, `staticwebapp.config.json`) are correctly copied into the build output.

**Why it matters**: MkDocs only processes Markdown files. Static assets must be explicitly copied into the `site/` output directory. Missing assets could break diagrams, API documentation, or security headers.

**Implementation**: The `generate-all.sh` script and post-build `cp` commands handle this.

**Blocks deployment on failure**: Yes (missing `staticwebapp.config.json` would remove all security headers).

### Gate 11 — Azure Platform Security

**What it checks**: Azure Static Web Apps provides platform-level protections:

- **DDoS protection** (Azure-managed, included with the platform)
- **TLS termination** (HTTPS only, managed certificates, TLS 1.2 minimum)
- **Global CDN** (Azure Front Door edge nodes, reducing origin exposure)
- **Custom domain validation** (prevents domain spoofing)
- **Staging environments** (PR deployments go to isolated preview URLs, not production)

**Why it matters**: Even with perfect content security, the hosting platform must also be secure. Azure Static Web Apps is a managed platform with enterprise-grade security controls — the NovaTrek team does not manage web servers, load balancers, or TLS certificates.

---

## Gate Comparison with Confluence

| Gate | Docs-as-Code | Confluence Equivalent |
|------|-------------|----------------------|
| Secret scanning | Automated, blocks push | Not available |
| YAML validation | Automated, blocks merge | Not applicable |
| Data isolation audit | Automated, blocks merge | Not available |
| Dependency vulnerability scan | Snyk — automated, blocks merge (requires branch protection rule) | Atlassian-managed (no visibility) |
| Code security analysis | Snyk — automated, blocks merge (requires branch protection rule) | Not available |
| IaC misconfiguration scan | Snyk — automated, blocks merge (requires branch protection rule) | Not applicable |
| Link validation | Automated, blocks merge | Not available |
| Pre-publish review | Required PR approval | Optional (page restrictions) |
| Build integrity | Automated, blocks deploy | Not applicable |
| Security headers | Version-controlled, gated | Atlassian-managed |
| Platform security | Azure (SOC 2, ISO 27001) | Atlassian (SOC 2, ISO 27001) |

**Key difference**: Confluence has **zero automated gates** between editing and publishing. Every control is either manual (page restrictions) or managed by Atlassian (platform security). The docs-as-code model provides **9 automated gates** plus a required human review, all of which must pass before content reaches production.

---

## SLSA Framework Alignment

The [Supply-chain Levels for Software Artifacts (SLSA)](https://slsa.dev/) framework, developed by Google, provides an authoritative blueprint for securing CI/CD pipelines against supply chain attacks. The NovaTrek documentation pipeline aligns with SLSA Build Levels 1--3:

| SLSA Level | Requirement | NovaTrek Implementation |
|------------|-------------|------------------------|
| **Build L1** | Fully scripted builds with provenance metadata | Entire build defined declaratively in GitHub Actions YAML |
| **Build L2** | Hosted platform with cryptographically signed provenance | Deployments run exclusively on GitHub-hosted runners; artifacts tied to source commits |
| **Build L3** | Hardened, ephemeral build environments | Each build spins up a clean, isolated runner — executes MkDocs build, deploys, and destroys the environment |

Source: [SLSA Framework specification](https://slsa.dev/) and [JFrog SLSA analysis](https://jfrog.com/learn/grc/slsa-framework/).

---

## OWASP CI/CD Risk Mitigation

The [OWASP Top 10 CI/CD Security Risks](https://owasp.org/www-project-top-10-ci-cd-security-risks/) identifies key pipeline threat categories. The docs-as-code model addresses the most critical risks:

| OWASP Risk | Risk Description | Docs-as-Code Mitigation |
|-----------|-----------------|------------------------|
| **CICD-SEC-1** | Insufficient Flow Control | Branch protection rules, required PR approvals, automated status checks |
| **CICD-SEC-3** | Dependency Chain Abuse | Snyk SCA blocks malicious packages; Dependabot automates updates |
| **CICD-SEC-4** | Poisoned Pipeline Execution (PPE) | Ephemeral runners, SLSA Level 2 provenance, immutable build environments |
| **CICD-SEC-6** | Insufficient Credential Hygiene | Workload Identity Federation (OIDC) eliminates long-lived deployment credentials |

Source: [OWASP CI/CD Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/CI_CD_Security_Cheat_Sheet.html).

---

## Snyk Integration

Snyk provides three distinct scanning capabilities, each deployed as an active CI gate in the documentation pipeline (`security-scan` job in `docs-deploy.yml`). All three scans run on every pull request and every push to `main`. The `deploy` job depends on `security-scan`, so deployment is blocked if any scan finds a HIGH or CRITICAL finding.

### Snyk Dependency Scan (`snyk test`)

**What it checks**: All Python packages in `requirements-docs.txt` against the Snyk vulnerability database.

**Why it matters**: MkDocs, pymdownx, and other build-time dependencies may contain vulnerabilities. Even though these packages only run at build time (not in production), a compromised build dependency could inject malicious content into the generated HTML.

**Implementation** (runs from repository root):

```yaml
- name: Snyk dependency scan
  run: snyk test --severity-threshold=high --file=requirements-docs.txt --package-manager=pip
  env:
    SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
```

**Blocks merge on failure**: Yes (HIGH or CRITICAL severity).

### Snyk Code Analysis (`snyk code test`)

**What it checks**: Static analysis of Python generator scripts in `portal/scripts/` for security issues including:

- Path traversal vulnerabilities (generators process file paths from YAML input)
- Unsafe deserialization (generators parse YAML metadata)
- Injection risks (generators produce HTML output)
- Hardcoded secrets or credentials

**Why it matters**: The generator scripts are the boundary between untrusted input (YAML metadata, OpenAPI specs) and trusted output (published HTML). Security flaws in generators could allow a crafted YAML file to produce malicious portal content.

**Implementation**:

```yaml
- name: Snyk code scan
  run: snyk code test --severity-threshold=high portal/scripts/
  env:
    SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
```

**Blocks merge on failure**: Yes.

### Snyk Infrastructure-as-Code Scan (`snyk iac test`)

**What it checks**: Infrastructure and configuration files for security misconfigurations:

- `portal/staticwebapp.config.json` — overly permissive CSP, missing security headers
- `.github/workflows/docs-deploy.yml` — overly broad workflow permissions, missing pinned action versions

**Why it matters**: A misconfigured `staticwebapp.config.json` could silently remove all security headers from the production site. Snyk IaC catches these misconfigurations before they are deployed.

**Implementation**:

```yaml
- name: Snyk IaC scan
  run: snyk iac test --severity-threshold=high portal/staticwebapp.config.json .github/workflows/docs-deploy.yml
  env:
    SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
```

**Blocks merge on failure**: Yes (HIGH or CRITICAL severity).

### Required Secret

The `security-scan` job requires `SNYK_TOKEN` to be configured as a GitHub Actions secret. To obtain a token:

1. Create a free or team account at [snyk.io](https://snyk.io)
2. Navigate to Account Settings and generate an API token
3. Add it to the repository under Settings > Secrets and variables > Actions > New repository secret

Without `SNYK_TOKEN`, the security-scan job will fail and block deployment. This is intentional — the gate must be explicitly configured, not silently skipped.

### Continuous Monitoring

Beyond CI gates, Snyk's GitHub integration provides continuous monitoring:

- **New vulnerability alerts**: If a CVE is published for a dependency that was clean at merge time, Snyk opens an automated PR with the fix
- **License compliance**: Snyk can enforce that all dependencies use approved licenses (MIT, Apache-2.0, etc.)
- **Reporting dashboard**: Security team gets a single-pane view of all vulnerability findings across the repository

This is a capability that Confluence cannot match — there is no way for an organization to scan Confluence's own dependencies or receive alerts when Confluence's build toolchain has a new vulnerability.

---

## Secret Sprawl: The Scale of the Problem

The [2025 State of Secrets Sprawl report by GitGuardian](https://www.scribd.com/document/855773866/The-State-of-Secrets-Sprawl-2025) quantifies the scale of credential exposure in modern software environments:

- **23.77 million** new hardcoded secrets found in public repositories in 2024
- **25% year-over-year increase** in secret exposure
- **58% of all detected leaks** are generic secrets (API keys, passwords, connection strings)

While Confluence relies on authors to avoid pasting secrets (with no automated detection), the docs-as-code pipeline provides two layers of defence:

1. **[GitHub Push Protection](https://docs.github.com/en/code-security/concepts/secret-security/about-push-protection)** — operates as a pre-receive hook that **rejects commits** containing detected secrets before they enter the repository history
2. **[GitHub Secret Scanning](https://docs.github.com/code-security/secret-scanning/about-secret-scanning)** — continuously monitors for secrets that bypass push protection, scanning for 200+ partner patterns plus custom organization-defined patterns

---

## Adding More Gates

The pipeline is extensible. Additional gates that can be added with minimal effort:

| Gate | Tool | Purpose |
|------|------|---------|
| Markdown lint | markdownlint-cli | Enforce consistent formatting and catch common Markdown errors |
| Spell check | cspell | Catch typos and enforce terminology consistency |
| Accessibility check | pa11y-ci | Validate generated HTML meets WCAG guidelines |
| Link rot detection | lychee | Check external links still resolve (scheduled, not blocking) |
| Content policy check | Custom script | Enforce organization-specific content policies (e.g., no PII, no internal codenames) |

Each gate is a step in the GitHub Actions workflow — a YAML file that is itself version-controlled, reviewed, and auditable.
