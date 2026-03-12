# Access Control and Audit Trail

This page compares how access control and audit trails work in Confluence vs. the docs-as-code model. The core argument: Git's cryptographic commit chain and GitHub's branch protection rules provide stronger, more granular, and more tamper-resistant controls than Confluence's page-level permissions and page history.

!!! note "Fictional Domain"
    Everything on this portal is entirely fictional. NovaTrek Adventures is a completely fictitious company. All examples reference the NovaTrek proof-of-concept implementation.

---

## Access Control Comparison

### Confluence Permission Model

Confluence uses a hierarchical permission model:

| Level | Controls | Granularity |
|-------|----------|-------------|
| Global | Site admin, user management | Entire instance |
| Space | View, edit, delete, export, admin | All pages in a space |
| Page | View restriction, edit restriction | Single page (manual, per-page) |

**Weaknesses**:

- **Space permissions are coarse**: Granting "Edit" on a space grants edit on all pages. There is no way to say "this user can edit architecture decisions but not service specs" within a single space.
- **Page restrictions are opt-in and forgettable**: Each page must be individually restricted. New pages inherit space permissions with no restrictions by default. It is easy to create a page with sensitive content and forget to restrict it.
- **Editors are publishers**: Any user with edit permission can modify and immediately publish content. There is no review step between editing and publishing.
- **Restrictions can be removed**: A space admin can remove page restrictions at any time, granting themselves access. This is sometimes necessary (e.g., when a page owner leaves the organization) but creates a bypass path.
- **No conditional access**: Permissions cannot be conditioned on content validation, security scanning, or approval workflows.

### Docs-as-Code Permission Model

The docs-as-code model uses Git repository permissions and branch protection rules:

| Level | Controls | Granularity |
|-------|----------|-------------|
| Repository | Read, write, admin | Entire repository |
| Branch protection | Required reviews, status checks, restrictions | Per-branch rules |
| CODEOWNERS | Required reviewers per path | File or directory pattern |
| Environment protection | Approval gates, wait timers | Per-deployment environment |

**Strengths**:

- **CODEOWNERS provides path-level review requirements**: A `CODEOWNERS` file can require different reviewers for different paths. For example:

    ```
    # Architecture decisions require architect approval
    decisions/                        @architecture-team

    # Security headers require security team approval
    portal/staticwebapp.config.json   @security-team

    # OpenAPI specs require API governance approval
    architecture/specs/               @api-governance-team
    ```

    This means the security team can require their own approval for any change to security headers, CSP configuration, or authentication settings — without needing to review every documentation change.

- **Branch protection enforces separation of duties**: The `main` branch requires:
    - At least 1 approving review (no self-approval)
    - All CI status checks to pass
    - No force pushes (prevents history tampering)
    - No branch deletion

- **Environment protection adds a second gate**: Even after a PR is merged, the deployment to production can require additional approval from a designated team. This creates a two-gate workflow: PR approval for content correctness, environment approval for deployment authorization.

- **Conditional access**: Merge is conditional on automated gates passing. Unlike Confluence, where the only gate is "does this person have edit permission," docs-as-code requires both authorization (PR approval) AND validation (CI gates).

---

## Audit Trail Comparison

### Confluence Page History

Confluence maintains a page history showing:

- Who edited the page
- When the edit occurred
- A diff of what changed

**Limitations**:

- **History can be pruned**: Space admins can delete old page versions, removing audit trail entries. This is sometimes done for storage management but creates gaps in the audit record.
- **Bulk operations leave minimal trace**: Confluence REST API edits, bulk imports, or automated updates may show as system-level edits without meaningful context.
- **No commit messages**: Confluence does not require editors to explain why a change was made. Changes appear as diffs without context.
- **No review record**: Page history shows who edited, but not who reviewed or approved the edit (because there is no review step).
- **Cross-page audit is fragmented**: There is no single view showing "all changes made across all pages in this time period by this user." Each page's history must be checked individually.

### Git Audit Trail

Git provides a cryptographically-linked, append-only audit log:

- **Every change has a commit hash**: A SHA-256 hash that depends on the content, parent commit, author, and timestamp. Altering any prior commit changes all subsequent hashes, making tampering detectable.
- **Every change has a commit message**: Required context explaining why the change was made.
- **Every change has a diff**: Exact line-by-line comparison with the previous state.
- **Every change has authorship**: Verified author identity (with signed commits, cryptographically verified).
- **PR records are permanent**: The PR conversation, review comments, approval records, and CI gate results are stored in GitHub and cannot be deleted by contributors.
- **Cross-repository audit is unified**: `git log` provides a single chronological view of all changes across all files. Filter by date, author, path, or content.

**Tamper resistance**:

| Property | Confluence | Git |
|----------|-----------|-----|
| History deletable? | Yes (by space admins) | No (branch protection blocks force-push) |
| Individual versions deletable? | Yes | No (without force-push, which is blocked and audited) |
| Cryptographic integrity? | No | Yes (SHA-256 commit chain) |
| Change context required? | No (no commit messages) | Yes (commit message + PR description) |
| Reviewer identity recorded? | No (no review step) | Yes (PR approval records) |
| CI gate results recorded? | N/A | Yes (status check logs) |
| Exportable? | Manual (page-by-page) | `git clone` (complete history in seconds) |

---

## Compliance Implications

### NIST SP 800-53 Alignment

| Control | Confluence | Docs-as-Code |
|---------|-----------|--------------|
| **AC-5 (Separation of Duties)** | Not enforced — editors = publishers | Enforced — authors, reviewers, deployers are distinct roles |
| **AC-6 (Least Privilege)** | Coarse space-level permissions | CODEOWNERS + branch protection for path-level control |
| **AU-3 (Content of Audit Records)** | Limited — no commit messages, no reviewer records | Complete — author, reviewer, timestamp, diff, context, CI results |
| **AU-9 (Protection of Audit Information)** | Deletable by space admins | Cryptographic chain prevents undetected tampering |
| **AU-10 (Non-repudiation)** | No signature verification | Signed commits provide non-repudiation |
| **CM-3 (Configuration Change Control)** | No automated validation | CI gates validate every change before deployment |

### SOX and Regulatory Audit

For organizations subject to SOX or similar regulatory requirements, the Git audit trail provides:

- **Traceability**: Every published page can be traced to a specific commit, PR, reviewer, and CI run
- **Completeness**: No gaps in history (append-only log)
- **Integrity**: Cryptographic verification that history has not been altered
- **Timeliness**: Timestamps are part of the cryptographic chain
- **Accountability**: Author and reviewer identities are recorded for every change

---

## CODEOWNERS Example for Security Team Oversight

The security team can maintain visibility and approval authority over security-relevant files without reviewing every documentation change:

```
# ─── Security-relevant files ───────────────────────────
# These require security team approval for any change

# Security headers and CSP
portal/staticwebapp.config.json       @security-team

# Azure infrastructure
infra/                                @security-team @platform-team

# CI/CD pipeline definitions
.github/workflows/                    @security-team @devops-team

# Authentication configuration
portal/docs/security/                 @security-team

# Data isolation audit script
scripts/audit-data-isolation.sh       @security-team
```

This gives the security team a **veto** on security-relevant changes while allowing the architecture team to move quickly on documentation content. Confluence has no equivalent mechanism — space permissions are all-or-nothing.
