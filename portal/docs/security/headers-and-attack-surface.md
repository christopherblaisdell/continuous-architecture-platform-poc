# Security Headers and Attack Surface

The NovaTrek Architecture Portal is a static site — pre-rendered HTML, CSS, and JavaScript files served from a CDN with no server-side code execution. This fundamentally limits the attack surface compared to dynamic web applications like Confluence.

!!! note "Fictional Domain"
    Everything on this portal is entirely fictional. NovaTrek Adventures is a completely fictitious company. All configuration examples reference the NovaTrek proof-of-concept implementation.

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

**Historical evidence**: Confluence has had critical CVEs in recent years:

| CVE | Year | Severity | Description |
|-----|------|----------|-------------|
| CVE-2023-22515 | 2023 | 10.0 Critical | Broken access control allowing admin account creation |
| CVE-2023-22518 | 2023 | 9.1 Critical | Improper authorization leading to data destruction |
| CVE-2022-26134 | 2022 | 9.8 Critical | Remote code execution via OGNL injection |
| CVE-2021-26084 | 2021 | 9.8 Critical | Remote code execution via OGNL injection |

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
| **DDoS** | Azure DDoS Protection Basic (included) |
| **CDN** | Azure Front Door edge network (300+ points of presence) |
| **DNS** | Azure DNS with DNSSEC support |
| **Compliance** | SOC 1/2/3, ISO 27001, ISO 27018, FedRAMP, HIPAA BAA eligible |
| **Deployment tokens** | Scoped to specific Static Web App instances, rotatable |

The deployment token used by CI/CD can only upload static files to a specific Azure Static Web App. It cannot:

- Access other Azure resources
- Modify network configuration
- Read data from other services
- Modify authentication settings

This is the principle of least privilege applied to the deployment pipeline.
