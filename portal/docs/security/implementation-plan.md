<!-- PUBLISH -->
# Security Implementation Plan

This page describes the concrete steps needed to implement the security controls documented in this section as **live, working demonstrations** — not just documentation. The goal is a 15-minute demo that a security team can watch and verify in real time.

Each sprint is self-contained and produces a specific demo artifact. Sprints can be executed in order or in parallel.

---

## Sprint 1 — Harden HTTP Security Headers

**Goal**: Add the remaining HTTPS and injection-prevention headers documented in the [CSP Hardening Roadmap](headers-and-attack-surface.md#csp-hardening-roadmap).

**File changed**: `portal/staticwebapp.config.json`

**Changes**:

```json
"Strict-Transport-Security": "max-age=31536000; includeSubDomains",
"form-action": "none",
"base-uri": "self"
```

Add these three headers to the `globalHeaders` block alongside the existing CSP.

**Demo**: Open [securityheaders.com](https://securityheaders.com), enter `https://architecture.novatrek.cc`, and show the A or A+ grade. Each header appears in the scan results with its value and an explanation of what it protects against.

**Effort**: 30 minutes (1 PR, 3 lines of JSON).

**Risk**: None — adding headers is additive and backward-compatible. HSTS has a 1-year max-age, so the header should only be enabled once HTTPS is confirmed stable.

---

## Sprint 2 — CODEOWNERS for Security-Sensitive Files

**Goal**: Require a designated security reviewer on any PR that touches security-critical files.

**File created**: `.github/CODEOWNERS`

**Content**:

```
# Security-sensitive files — require security review on any change
portal/staticwebapp.config.json         @christopherblaisdell
portal/docs/security/                   @christopherblaisdell
.github/workflows/                      @christopherblaisdell
```

**Demo**: Open a PR that modifies `portal/staticwebapp.config.json`. GitHub automatically adds the CODEOWNERS reviewer to the PR and blocks merge until they approve. The PR review page shows "Review required from CODEOWNERS" in the status checks.

**Effort**: 15 minutes (1 new file, 3 lines).

**Risk**: None — CODEOWNERS only adds a review requirement. It does not remove any existing permissions.

---

## Sprint 3 — Snyk Live Scanning

**Goal**: Wire up the Snyk CI workflow so the three scanning gates (dependency, code, IaC) actually run and block merges on findings.

**Prerequisites**: `SNYK_TOKEN` secret must be added to the repository.

**Steps**:

1. Create a free Snyk account at [snyk.io](https://snyk.io)
2. Import the repository into the Snyk dashboard
3. Generate a Snyk API token from Account Settings
4. Add the token as a GitHub Actions secret: `Settings > Secrets and variables > Actions > New repository secret`, name `SNYK_TOKEN`
5. The `.github/workflows/snyk-security.yml` workflow is already in the repository — it activates automatically once the secret is present

**Demo**:

Show Snyk running in a PR:

1. Open a PR on any branch — the three Snyk jobs appear in the checks section
2. Open the Snyk dashboard at [app.snyk.io](https://app.snyk.io) — the repository appears with its dependency tree and vulnerability count
3. To demo a blocking failure: temporarily add a known-vulnerable package version to `requirements-docs.txt` (e.g., an old `cryptography` version with a published CVE), open a PR, and show the Snyk dependency scan failing with the CVE details

**Effort**: 1 hour (account setup, token configuration, demo run).

**Risk**: Low — the workflow only reports findings. The blocking threshold is HIGH/CRITICAL, so informational findings do not fail the build.

---

## Sprint 4 — Signed Commits on Main

**Goal**: Require that all commits merged to `main` are cryptographically signed, providing a verifiable chain of custody for every published artifact.

**Steps**:

1. Enable signed commits enforcement: `Settings > Branches > main > Require signed commits`
2. Each contributor configures GPG or SSH signing locally:

```bash
# GPG approach
gpg --gen-key
git config --global user.signingkey <KEY_ID>
git config --global commit.gpgsign true

# SSH approach (Git 2.34+)
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true
```

3. Add the public key to GitHub: `Settings > SSH and GPG keys > New signing key`

**Demo**:

Two verification paths:

1. **GitHub UI**: Navigate to any commit on `main`. Look for the green "Verified" badge next to the commit hash. Clicking it shows the signing key fingerprint, the key owner, and the signing algorithm.

2. **CLI verification**:

```bash
git log --show-signature -1
```

Output shows:

```
gpg: Signature made Mon 14 Mar 2026
gpg: using RSA key ABCD1234...
gpg: Good signature from "Christopher Blaisdell <chris@novatrek.example.com>"
commit a1b2c3d...
Author: Christopher Blaisdell <chris@novatrek.example.com>
```

**Effort**: 2 hours (key setup per contributor, branch protection rule change).

**Risk**: Medium — contributors who have not set up signing cannot merge to `main` until they configure their keys. Schedule this sprint when the team has a maintenance window.

---

## Consolidated 15-Minute Demo Script

This script assumes Sprints 1-4 are complete. It is structured as a live walkthrough for a security team audience.

### Opening (1 minute)

"The question is not whether MkDocs is secure, but whether the docs-as-code model provides controls that are at least as strong as Confluence. We are going to walk through five live demonstrations that answer that question."

### Demo 1 — Security Headers (2 minutes)

1. Open `https://securityheaders.com`
2. Enter `https://architecture.novatrek.cc`
3. Show the A/A+ grade
4. Point to each header: CSP, HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy
5. "These headers are defined in a JSON file that is version-controlled, reviewed in PRs, and deployed through the same pipeline as every other content change. No one can modify them without a PR review."

### Demo 2 — Pipeline Gates (3 minutes)

1. Open the repository on GitHub
2. Open a recent PR — show the status checks list
3. Point to each automated gate: YAML validation, data isolation audit, Snyk dependency, Snyk code, Snyk IaC, portal build, Confluence dry-run
4. "Every one of these must pass before the PR can merge. Compare this to Confluence where there are zero automated gates between editing and publishing."
5. Open the `validate-solution.yml` workflow — show that it uses `yaml.safe_load()`, not `yaml.load()` — "this prevents YAML deserialization attacks"

### Demo 3 — Snyk Results (3 minutes)

1. Open [app.snyk.io](https://app.snyk.io)
2. Show the repository imported — zero HIGH/CRITICAL vulnerabilities
3. Switch to the GitHub PR checks tab — show the three Snyk jobs passing
4. "Snyk monitors the repository continuously. If a CVE is published for a dependency that was clean today, Snyk opens an automated PR with the fix. Confluence cannot do this — Atlassian manages their dependencies and you have no visibility into their vulnerability status."

### Demo 4 — CODEOWNERS Enforcement (2 minutes)

1. Open a PR that modifies `portal/staticwebapp.config.json`
2. Show the CODEOWNERS review requirement in the PR checks
3. "Any change to security-sensitive files — the CSP configuration, security documentation, CI workflows — requires explicit approval from a designated reviewer. This is not optional."

### Demo 5 — Signed Commits (2 minutes)

1. Navigate to the latest commit on `main`
2. Show the green "Verified" badge
3. Click it — show the signing key owner and algorithm
4. Run `git log --show-signature -1` in the terminal
5. "Every commit on main is cryptographically signed. If someone tried to inject a commit — tamper with the pipeline, modify a deployed file — the signature would be absent or invalid. This is a complete chain of custody from author to production."

### Closing (2 minutes)

"What we have just demonstrated: version-controlled security headers with automated scanning, nine automated pipeline gates that block bad content before it reaches production, live Snyk vulnerability scanning on every PR, CODEOWNERS enforcement on security-critical files, and signed commits with a verifiable chain of custody. This is not documentation about security controls — these are the controls running live."

---

## Status Tracker

| Sprint | Description | Status | Demo Ready |
|--------|-------------|--------|------------|
| 1 | Harden HTTP headers (HSTS, form-action, base-uri) | Pending | No |
| 2 | CODEOWNERS for security-sensitive files | Pending | No |
| 3 | Snyk live scanning (SNYK_TOKEN secret) | Pending | No |
| 4 | Signed commits on main | Pending | No |

Update this table as each sprint is completed.
