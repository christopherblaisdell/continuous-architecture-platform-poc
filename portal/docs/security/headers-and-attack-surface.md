# Security Headers and Attack Surface

The NovaTrek Architecture Portal is a static site — pre-rendered HTML, CSS, and JavaScript files served from a CDN with no server-side code execution. This fundamentally limits the attack surface compared to dynamic web applications like Confluence.

[NIST SP 800-123](https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-123.pdf) (Guide to General Server Security) and [SP 800-95](https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-95.pdf) (Guide to Secure Web Services) strongly emphasize minimizing server-side execution and reducing the footprint of web-hosted content. The static delivery model aligns directly with this federal guidance, transitioning the threat model from defending a persistently running application to serving immutable files via a CDN.

For the complete evidence base, see [Research Results](research-prompt-response.md).

---

## HTTP Security Headers

All security headers are defined in `staticwebapp.config.json` and are version-controlled, reviewed in PRs, and deployed through the CI/CD pipeline. The security team can propose changes to these headers through the same PR workflow as any other content change.

### Current Headers

| Header | Value | Purpose |
|--------|-------|---------|
| `X-Frame-Options` | `SAMEORIGIN` | Prevents clickjacking by blocking embedding in cross-origin frames. Set to `SAMEORIGIN` (not `DENY`) because the portal uses `<object>` tags for interactive SVG sequence diagrams. |
| `X-Content-Type-Options` | `nosniff` | Prevents MIME-type sniffing, ensuring browsers respect declared content types. |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | Limits referrer information sent to external sites, preventing URL leakage. |
| `Permissions-Policy` | `camera=(), microphone=(), geolocation=()` | Explicitly disables browser APIs that the portal does not use, preventing abuse if the site were compromised. |
| `X-XSS-Protection` | `1; mode=block` | Legacy XSS protection for older browsers. Modern browsers rely on CSP instead. |

### Content Security Policy

The CSP is the most important security header. It controls exactly which resources the browser is allowed to load:

```
default-src 'self';
script-src 'self' 'unsafe-inline' 'unsafe-eval' https://unpkg.com;
style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://unpkg.com;
font-src 'self' https://fonts.gstatic.com;
img-src 'self' data: https:;
connect-src 'self'
```

| Directive | Allows | Rationale |
|-----------|--------|-----------|
| `default-src 'self'` | Only resources from the same origin | Baseline lockdown — everything else must be explicitly allowed |
| `script-src 'self' 'unsafe-inline' 'unsafe-eval' https://unpkg.com` | Scripts from self and unpkg CDN | MkDocs Material uses inline scripts for search and navigation; Mermaid.js loaded from unpkg |
| `style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://unpkg.com` | Styles from self, Google Fonts, unpkg | MkDocs Material uses inline styles and Google Fonts for typography |
| `font-src 'self' https://fonts.gstatic.com` | Fonts from self and Google Fonts | Inter and JetBrains Mono font loading |
| `img-src 'self' data: https:` | Images from self, data URIs, any HTTPS source | SVG diagrams may reference external HTTPS resources |
| `connect-src 'self'` | XHR/fetch only to same origin | Search index is loaded from the same domain; no external API calls |

### CSP Hardening Roadmap

The current CSP includes `'unsafe-inline'` and `'unsafe-eval'` for MkDocs Material compatibility. These can be progressively tightened:

| Phase | Change | Impact |
|-------|--------|--------|
| 1 | Add `Strict-Transport-Security: max-age=31536000; includeSubDomains` | Enforce HTTPS for all future visits |
| 2 | Replace `'unsafe-inline'` with nonce-based script loading | Eliminate inline script injection vector |
| 3 | Remove `'unsafe-eval'` when MkDocs Material adds CSP-safe Mermaid rendering | Eliminate eval-based code execution |
| 4 | Add `form-action 'none'` | Prevent form submissions (the portal has no forms) |
| 5 | Add `base-uri 'self'` | Prevent base tag injection attacks |

Each phase is a change to `staticwebapp.config.json` — reviewed, tested, and deployed through the same pipeline.

### Confluence CSP Limitations

By contrast, implementing a rigorous CSP in Confluence is significantly constrained:

- Confluence Data Center [10.0 introduced a `script-src` CSP header](https://developer.atlassian.com/server/confluence/content-security-policy-adoption/), but it operates exclusively in **report-only mode** — the browser logs violations but does not block malicious execution. Full enforcement is not expected until future versions ([Confluence 10.0 Release Notes](https://confluence.atlassian.com/doc/confluence-10-0-release-notes-1612579091.html)).
- In Confluence Cloud, [Forge apps](https://developer.atlassian.com/platform/forge/manifest-reference/permissions/) often require injection of `unsafe-hashes` or complex custom scopes, weakening the CSP that Atlassian can enforce.
- Legacy plugin complexity frequently mandates `unsafe-inline` or `unsafe-eval`, which Atlassian [explicitly warns](https://developer.atlassian.com/platform/framework/agc/guides/agc-developer-security-guidelines/) weakens security.

Because the docs-as-code architecture serves purely static files with predictable asset origins, administrators can enforce strict CSP headers without breaking functionality. A static site can lock down to `default-src 'self'` as a baseline, rejecting any injected script — a posture Confluence cannot replicate without severe functional degradation.

---

## Attack Surface Comparison

### Static Site (MkDocs on Azure Static Web Apps)

```
┌─────────────────────────────────────────┐
│           Attack Surface                 │
│                                          │
│  ┌──────────┐   ┌──────────────────┐    │
│  │   CDN    │   │  Static Files    │    │
│  │ (Azure   │──▶│  HTML, CSS, JS   │    │
│  │  Front   │   │  SVG, JSON       │    │
│  │  Door)   │   │                  │    │
│  └──────────┘   └──────────────────┘    │
│                                          │
│  No database                             │
│  No server-side code                     │
│  No file uploads                         │
│  No user input processing                │
│  No authentication endpoints (*)         │
│  No plugin runtime                       │
│  No session management                   │
│                                          │
│  (*) Auth handled by Azure platform      │
│      layer, separate from content        │
└─────────────────────────────────────────┘
```

**Potential attack vectors**: DNS hijacking, CDN compromise, TLS downgrade, CSP bypass. All managed at the Azure platform level with enterprise-grade protections.

### Dynamic Site (Confluence Cloud)

```
┌─────────────────────────────────────────┐
│           Attack Surface                 │
│                                          │
│  ┌──────────┐   ┌──────────────────┐    │
│  │   Load   │   │  Java App Server │    │
│  │ Balancer │──▶│  (Spring/Tomcat)  │    │
│  └──────────┘   │                  │    │
│                  │  ┌────────────┐  │    │
│  ┌──────────┐   │  │ Plugin     │  │    │
│  │ Database │◀──│  │ Runtime    │  │    │
│  │ (Postgres)│   │  └────────────┘  │    │
│  └──────────┘   │                  │    │
│                  │  ┌────────────┐  │    │
│  ┌──────────┐   │  │ Rich Text  │  │    │
│  │  File    │◀──│  │ Editor     │  │    │
│  │ Storage  │   │  └────────────┘  │    │
│  └──────────┘   │                  │    │
│                  │  ┌────────────┐  │    │
│  ┌──────────┐   │  │ REST API   │  │    │
│  │ Session  │◀──│  │ Endpoints  │  │    │
│  │  Store   │   │  └────────────┘  │    │
│  └──────────┘   └──────────────────┘    │
│                                          │
│  Database injection                      │
│  Server-side code execution              │
│  File upload exploitation                │
│  XSS via rich text editor                │
│  Plugin vulnerabilities                  │
│  Session hijacking                       │
│  API authentication bypass               │
│  Deserialization attacks                  │
└─────────────────────────────────────────┘
```

**Historical evidence**: Confluence has been the subject of at least [nine CISA KEV alerts](https://www.greenbone.net/en/blog/cisa-multiple-vulnerabilities-in-atlassian-confluence-are-being-actively-exploited/) for active exploitation. Critical CVEs include:

| CVE | Year | Severity | Description | Exploited By |
|-----|------|----------|-------------|-------------|
| [CVE-2023-22515](https://phoenix.security/vuln-atlassian-cve-2023-22515/) | 2023 | 10.0 Critical | Broken access control — admin account creation | Storm-0062 (nation-state zero-day) |
| CVE-2023-22527 | 2023-24 | 10.0 Critical | Remote code execution | Multiple threat actors |
| CVE-2022-26134 | 2022 | 9.8 Critical | Remote code execution via OGNL injection | [DragonForce ransomware](https://www.greenbone.net/en/blog/threat-report-may-2025-hack-rinse-repeat/) |
| [CVE-2023-22518](https://www.sentinelone.com/blog/c3rb3r-ransomware-ongoing-exploitation-of-cve-2023-22518-targets-unpatched-confluence-servers/) | 2023 | 9.1 Critical | Improper auth — database wipe | C3RB3R (Cerber) ransomware |
| CVE-2021-26084 | 2021 | 9.8 Critical | Remote code execution via OGNL injection | Multiple threat actors |
| [CVE-2025-59343](https://confluence.atlassian.com/security/security-bulletin-february-17-2026-1722256046.html) | 2026 | 8.7 High | File inclusion (tar-fs dependency) | Pending |
| [CVE-2025-41249](https://confluence.atlassian.com/security/security-bulletin-february-17-2026-1722256046.html) | 2026 | 7.5 High | Improper auth (spring-core dependency) | Pending |

A static site is immune to all of these attack categories because the attack vectors (server-side code execution, database access, plugin runtime) do not exist.

---

## Caching and Performance Security

The portal uses differentiated caching policies:

| Path | Cache Policy | Rationale |
|------|-------------|-----------|
| `/assets/*` | `public, max-age=31536000, immutable` | Hashed asset filenames — content changes produce new URLs |
| `/search/*` | `public, max-age=3600` | Search index updates on each deploy |
| All other paths | CDN default (short-lived) | Content pages may change on each deploy |

The `immutable` directive on hashed assets prevents cache poisoning attacks — once an asset is cached, it cannot be replaced without changing the URL.

---

## Infrastructure Security

Azure Static Web Apps provides:

| Control | Detail |
|---------|--------|
| **TLS** | Managed certificates, TLS 1.2 minimum, automatic HTTPS redirect |
| **DDoS** | [Azure DDoS Protection](https://learn.microsoft.com/en-us/azure/ddos-protection/ddos-protection-overview) Basic (included) |
| **CDN** | [Enterprise-grade edge powered by Azure Front Door](https://learn.microsoft.com/en-us/azure/static-web-apps/enterprise-edge) — 118+ global edge locations for layered DDoS defense |
| **DNS** | Azure DNS with DNSSEC support |
| **Compliance** | SOC 1/2/3, ISO 27001, ISO 27018, [FedRAMP High](https://learn.microsoft.com/en-us/azure/compliance/offerings/offering-fedramp) (421 security controls), DoD IL2 |
| **Identity** | Native [Microsoft Entra ID](https://learn.microsoft.com/en-us/azure/static-web-apps/authentication-custom) integration — Conditional Access, MFA, and real-time session risk evaluation |
| **Deployment tokens** | Scoped to specific Static Web App instances, rotatable |

The deployment token used by CI/CD can only upload static files to a specific Azure Static Web App. It cannot:

- Access other Azure resources
- Modify network configuration
- Read data from other services
- Modify authentication settings

This is the principle of least privilege applied to the deployment pipeline.
