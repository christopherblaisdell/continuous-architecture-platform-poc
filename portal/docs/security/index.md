# Security Model

This section documents the security architecture of the NovaTrek Architecture Portal — a static documentation site built with MkDocs Material, source-controlled in Git, deployed through gated CI/CD pipelines to Azure Static Web Apps. It demonstrates that a docs-as-code publishing model provides **stronger security controls** than wiki-based platforms like Confluence.

---

## Why This Matters

Security teams are right to scrutinize any new publishing platform. The question is not "Is MkDocs secure?" but rather **"Does the docs-as-code model provide security controls that are equal to or stronger than our current Confluence-based workflow?"**

The answer is: the docs-as-code model is **demonstrably more secure** than wiki-based publishing. This section explains why, with specific evidence from the NovaTrek platform implementation.

---

## Section Overview

| Page | Purpose |
|------|---------|
| [Security Comparison](security-comparison.md) | Side-by-side comparison of Confluence vs. docs-as-code security controls across 12 dimensions |
| [Pipeline Security Gates](pipeline-security-gates.md) | Detailed walkthrough of every CI/CD gate that content passes through before reaching production |
| [Security Headers and Attack Surface](headers-and-attack-surface.md) | HTTP security headers, Content Security Policy, and why static sites have a fundamentally smaller attack surface |
| [Access Control and Audit Trail](access-control-and-audit.md) | How Git + branch protection + PR reviews provide stronger access control and more complete audit trails than wiki page-level permissions |
| [Data Protection](data-protection.md) | Secret scanning, data isolation auditing, and content validation gates that prevent sensitive data from reaching the published site |
| [Security Research Prompt](research-prompt.md) | AI deep-research prompt used to gather authoritative sources for this security assessment |
