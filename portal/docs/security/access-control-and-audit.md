# Access Control and Audit Trail

This page compares how access control and audit trails work in Confluence vs. the docs-as-code model. The core argument: Git's cryptographic commit chain and GitHub's branch protection rules provide stronger, more granular, and more tamper-resistant controls than Confluence's page-level permissions and page history.

For the complete evidence base with NIST SP 800-53 control mappings and forensic analysis, see [Research Results](research-prompt-response.md), Sections 4 and 6.

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

- **History can be permanently purged**: Space admins can [delete, restore, or purge](https://support.atlassian.com/confluence-cloud/docs/delete-restore-or-purge-a-page/) specific page versions, effectively erasing audit trail entries. This makes it mathematically impossible to guarantee that a specific document version existed at a specific point in time.
- **Anonymous actor bug**: Automated cleanup jobs purge unpublished drafts and empty pages, appearing in the audit log as actions by an ["anonymous" actor](https://support.atlassian.com/confluence/kb/the-organizations-audit-log-displays-anonymous-users-deleting-pages/), frequently without page titles or location context. This is a known limitation documented in Atlassian Access issue [ACCESS-2505](https://jira.atlassian.com/browse/ACCESS-2505).
- **Audit log retention is limited**: Confluence's default audit log retains events for [one year, reducible to as little as 31 days](https://support.atlassian.com/confluence-cloud/docs/view-the-audit-log/). After expiry, audit records are permanently lost.
- **Bulk operations leave minimal trace**: Confluence REST API edits, bulk imports, or automated updates may show as system-level edits without meaningful context.
- **No commit messages**: Confluence does not require editors to explain why a change was made. Changes appear as diffs without context.
- **No review record**: Page history shows who edited, but not who reviewed or approved the edit (because there is no review step).
- **Cross-page audit is fragmented**: There is no single view showing "all changes made across all pages in this time period by this user." Each page's history must be checked individually.

### Git Audit Trail

Git provides a cryptographically-linked, append-only audit log:

- **Every change has a commit hash**: A SHA-256 hash derived from the content, parent commit, author, and timestamp. Git constructs a [Merkle tree](https://en.wikipedia.org/wiki/Merkle_tree) of cryptographic hashes — altering any historical commit changes all subsequent hashes, immediately triggering an integrity failure. This tamper-evident property directly satisfies [NIST SP 800-53](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final) controls **CM-3** (Configuration Change Control) and **AU-12** (Audit Generation).
- **Every change has a commit message**: Required context explaining why the change was made.
- **Every change has a diff**: Exact line-by-line comparison with the previous state.
- **Every change has authorship**: Verified author identity (with signed commits, cryptographically verified).
- **PR records are permanent**: The PR conversation, review comments, approval records, and CI gate results are stored in GitHub and cannot be deleted by contributors.
- **Cross-repository audit is unified**: `git log` provides a single chronological view of all changes across all files. Filter by date, author, path, or content.

!!! info "Compliance Recognition"
    Frameworks such as SOC 2, HIPAA, and SOX explicitly recognize version control hygiene — when paired with strict branch protection rules, mandatory cryptographic commit signing, and centralized logging — as a [superior mechanism for establishing irrefutable data integrity](https://hoop.dev/blog/hipaa-compliance-in-git-preventing-phi-leaks-and-securing-your-repository/). When a compliance auditor requires proof of who authorized a specific architectural change, Git provides a pristine chain of custody completely immune to the application-level data purging capabilities present in wiki software.

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

### [NIST SP 800-53](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final) Alignment

| Control | Confluence | Docs-as-Code |
|---------|-----------|--------------|
| **[AC-5](https://csf.tools/reference/nist-sp-800-53/r5/ac/ac-5/) (Separation of Duties)** | Not enforced — editors = publishers. The author-equals-publisher model natively violates this control. | Enforced via PR workflow — authors, reviewers, and deployers are distinct roles. Branch protection physically decouples creation from publication. |
| **[AC-6](https://csf.tools/reference/nist-sp-800-53/r5/ac/ac-6/) (Least Privilege)** | Coarse space-level permissions | CODEOWNERS + branch protection for path-level control. Developers only possess write access to feature branches; the CI/CD service principal retains exclusive deployment privilege. |
| **AU-3 (Content of Audit Records)** | Limited — no commit messages, no reviewer records | Complete — author, reviewer, timestamp, diff, context, CI results |
| **AU-9 (Protection of Audit Information)** | Deletable by space admins; audit log retention as low as 31 days | Cryptographic chain prevents undetected tampering; append-only history |
| **AU-10 (Non-repudiation)** | No signature verification | Signed commits provide non-repudiation |
| **AU-12 (Audit Generation)** | Limited — automated deletions logged as "anonymous" | Every commit generates a complete, attributed, cryptographically linked audit record |
| **CM-3 (Configuration Change Control)** | No automated validation | CI gates validate every change before deployment |

### SOX and Regulatory Audit

For organizations subject to SOX or similar regulatory requirements, the Git audit trail provides:

- **Traceability**: Every published page can be traced to a specific commit, PR, reviewer, and CI run
- **Completeness**: No gaps in history (append-only log)
- **Integrity**: Cryptographic verification that history has not been altered
- **Timeliness**: Timestamps are part of the cryptographic chain
- **Accountability**: Author and reviewer identities are recorded for every change

### Impact on Incident Response Velocity

In the event of an intellectual property theft investigation or a configuration drift incident, the Git ledger serves as an absolute source of truth — completely immune to the application-level data purging capabilities present in wiki software. Security operations teams can deterministically trace every document version, authorship, and approval decision without relying on an audit log that may have been reduced to 31 days of retention or corrupted by anonymous actor entries.

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
