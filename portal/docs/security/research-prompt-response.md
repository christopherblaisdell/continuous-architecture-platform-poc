# Authoritative Security Assessment: Docs-as-Code vs. Dynamic Wiki Platforms

This page contains the full output from an AI deep research prompt (see [Security Research Prompt](research-prompt.md)), enriched with authoritative citations from NIST, CISA, OWASP, SLSA, Gartner, and vendor security advisories. The key findings are integrated into the other security documentation pages with direct source links.

---

## 1. Executive Overview and Architectural Threat Modeling

The enterprise paradigm for knowledge management and architecture documentation is undergoing a fundamental, structural transformation driven by escalating cybersecurity threats. Historically, corporate environments have relied almost exclusively on dynamic Content Management Systems (CMS) and wiki platforms, such as Atlassian Confluence, to author, store, and distribute internal technical documentation. While these platforms offer robust out-of-the-box functionality, their underlying architectures introduce immense and perpetually expanding attack surfaces. Dynamic wikis are characterized by persistent database connections, complex server-side code execution, and expansive third-party runtime plugin ecosystems that fundamentally increase the risk of systemic compromise.[^1]

Conversely, the "Docs-as-Code" methodology utilizes a decoupled, immutable architecture. This modern paradigm relies on Git for cryptographically verifiable version control, a Static Site Generator (SSG) such as MkDocs for artifact compilation, Continuous Integration and Continuous Deployment (CI/CD) pipelines like GitHub Actions for automated security validation, and static hosting environments such as Azure Static Web Apps for content delivery.[^2]

This comprehensive research report provides an exhaustive, evidence-based security comparison between the traditional Confluence Cloud architecture and the proposed Docs-as-Code pipeline. By systematically analyzing real-world vulnerability data, historical breach patterns, cryptographic audit capabilities, and alignment with prominent cybersecurity frameworks — including NIST SP 800-53, the SLSA framework, and the OWASP guidelines — the analysis demonstrates that the Docs-as-Code model fundamentally eliminates entire classes of runtime vulnerabilities.[^1] By shifting from dynamic server-side processing to immutable static file delivery, organizations can achieve a mathematically verifiable reduction in their external attack surface while simultaneously enhancing compliance auditability through cryptographic tamper-evidence.[^6]

---

## 2. Dynamic Web Applications vs. Static Sites: Attack Surface Research

The most critical distinction between Confluence Cloud and a Docs-as-Code architecture lies in the fundamental nature of how data is processed, rendered, and delivered to the end-user. This operational distinction directly dictates the size, complexity, and severity of the platform's attack surface.[^1]

### 2.1 The Mechanics of Dynamic CMS Vulnerabilities

Dynamic platforms like Confluence operate on highly complex, multi-tiered architectures. When a user requests a Confluence page, the request is received by a web server, passed to an application server (typically a Java Virtual Machine), which then executes application logic, queries a backend relational database (such as PostgreSQL), retrieves the content, passes it through a rendering engine, integrates active third-party plugins, and finally returns an HTML response to the client.[^1] Every single layer, network hop, and processing stage in this transaction represents a distinct attack vector.[^9]

The [OWASP Attack Surface Management (ASM) Top 10](https://owasp.org/www-project-attack-surface-management-top-10/) framework explicitly highlights the profound risks of interconnected application environments, third-party SaaS tools, and exposed APIs.[^10] Because dynamic platforms process user input at runtime, they are perpetually vulnerable to severe injection attacks, insecure deserialization flaws, broken access controls, and Server-Side Request Forgery (SSRF).[^9] The inherent requirement to interpret executable code on the server side means that any flaw in the application logic — or within its vast web of dependencies — can easily result in Remote Code Execution (RCE).[^12]

### 2.2 The Static-First Security Paradigm

Conversely, the Docs-as-Code architecture utilizes a Static Site Generator. An SSG processes flat Markdown files and compiles them into plain HTML, CSS, and JavaScript during a build phase within an ephemeral, highly controlled CI/CD environment.[^1] The resulting files are completely static. When deployed to a hosting environment like Azure Static Web Apps, there is no database to query, no application server to exploit, and absolutely no runtime code evaluation.[^2]

The security implications of this architectural shift are profound and quantifiable. By eliminating the database and the server-side runtime, the architecture effectively eradicates the possibility of SQL injection, PHP/Java deserialization flaws, and traditional RCE vulnerabilities on the delivery infrastructure.[^1] Security research from Envestis focusing on the comparison between dynamic CMS solutions and static site generators concludes that SSGs present the **"smallest possible attack surface,"** resulting in a core CVE count that is historically near zero.[^1]

Furthermore, [NIST SP 800-123](https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-123.pdf) (Guide to General Server Security) and [SP 800-95](https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-95.pdf) (Guide to Secure Web Services) strongly emphasize the principle of minimizing server-side execution and reducing the footprint of web-hosted content to defend against direct and indirect exploitation.[^13] The static delivery model aligns perfectly with this federal guidance, transitioning the threat model from defending a persistently running, highly privileged application to merely serving immutable text files via a globally distributed CDN.[^15]

### 2.3 Economic and Maintenance Burden of Dynamic Platforms

The security burden of maintaining a dynamic application is not merely theoretical; it carries a substantial financial and operational cost. According to the [2024-2025 Envestis comparison](https://envestis.ch/en/blog/confronto-cms-sicurezza-2025), the five-year security maintenance cost for a dynamic CMS ranges from 10,000 to 25,000 CHF, requiring weekly minimum updates to mitigate emerging threats.[^1] By contrast, the maintenance burden for a static site generator is dramatically lower (estimated at 1,500 to 7,500 CHF over five years) and generally only requires monthly updates to local build tools, with near-zero incident response costs.[^1]

| Architectural Component | Confluence (Dynamic Wiki) | Docs-as-Code (MkDocs + Azure SWA) | Security Implication |
|------------------------|--------------------------|-----------------------------------|---------------------|
| Data Storage | Relational Database (SQL) | Git Repository (Flat Markdown) | Eliminates SQL Injection and database exfiltration risk in production |
| Content Rendering | Server-side at Runtime (Java) | Build-time in CI/CD (Python) | Eliminates production Server-Side Template Injection |
| Plugin Execution | Runtime in Application Context | Build-time in Ephemeral Runner | Prevents malicious plugins from achieving persistent RCE |
| Session Management | Stateful Server Sessions | Stateless Identity Provider Tokens | Reduces session hijacking, fixation, and memory exhaustion risks |
| Infrastructure | Application Servers and DB Clusters | Global CDN and Blob Storage | Mitigates infrastructure-level exhaustion and layer-7 DDoS attacks |

---

## 3. Confluence CVE History and Security Incidents

To objectively evaluate the security posture of an enterprise documentation platform, it is necessary to examine historical vulnerability disclosure rates, the severity of those vulnerabilities, and the frequency of active exploitation by advanced threat actors in the wild.

### 3.1 Unrelenting High-Severity Disclosures

Atlassian Confluence has been subject to a severe and sustained volume of critical security vulnerabilities over the past several years. Data from the [CISA Known Exploited Vulnerabilities (KEV) catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) reveals that Confluence has been the subject of at least **nine separate KEV alerts** for active exploitation.[^12] The severity of these vulnerabilities frequently reaches the maximum CVSS score of 10.0, indicating that they are trivial to exploit over the network, require zero authentication, and result in total system compromise.[^12]

The vulnerability disclosure rate shows no signs of slowing. In the [February 17, 2026, Atlassian Security Bulletin](https://confluence.atlassian.com/security/security-bulletin-february-17-2026-1722256046.html) alone, multiple critical and high-severity vulnerabilities were disclosed for Confluence Data Center and Server, including:[^17]

- **CVE-2025-59343** — File Inclusion vulnerability in tar-fs dependency (CVSS 8.7)
- **CVE-2025-41249** — Improper Authorization in spring-core dependency (CVSS 7.5)
- **CVE-2022-25883** and **CVE-2025-48976** — multiple Denial of Service conditions
- **CVE-2025-48734** — RCE via commons-beanutils
- **CVE-2025-12383** — Race Condition in jersey-client[^18]

### 3.2 Zero-Day Exploitation and Ransomware Syndicates

A chronological analysis of recent critical incidents demonstrates a troubling pattern of zero-day exploitation and ransomware deployment targeting Confluence environments:

**CVE-2023-22515 (CVSS 10.0):** Critical broken access control vulnerability allowing external, unauthenticated attackers to silently create unauthorized administrative accounts. According to [Microsoft Threat Intelligence](https://phoenix.security/vuln-atlassian-cve-2023-22515/), this was exploited as a zero-day by the nation-state actor Storm-0062 (DarkShadow/Oro0lxy) starting September 14, 2023 — weeks before Atlassian disclosed the vulnerability on October 4, 2023.[^16]

**CVE-2023-22518 (CVSS 9.1):** Improper authorization allowing unauthenticated attackers to wipe and restore Confluence databases. Rapidly weaponized by ransomware syndicates to deploy [C3RB3R (Cerber) ransomware](https://www.sentinelone.com/blog/c3rb3r-ransomware-ongoing-exploitation-of-cve-2023-22518-targets-unpatched-confluence-servers/) payloads across exposed enterprise instances, prompting urgent CISA warnings.[^19][^21]

**CVE-2023-22527 (CVSS 10.0):** Unauthenticated remote code execution vulnerability. Due to the complexity of patching dynamic CMS environments, threat actors routinely exploit legacy deployments, leading to its rapid addition to the [CISA KEV catalog](https://www.greenbone.net/en/blog/cisa-multiple-vulnerabilities-in-atlassian-confluence-are-being-actively-exploited/) in January 2024.[^12]

**CVE-2022-26134 (CVSS 9.8):** Unauthenticated OGNL injection vulnerability enabling complete remote code execution. Heavily utilized by the DragonForce ransomware group as an initial access vector into corporate networks.[^22]

### 3.3 The Patch Management Burden

Maintaining a dynamic CMS requires a permanent, high-velocity patch management program. A failure to apply a Confluence patch within 24 hours of release has historically resulted in devastating ransomware deployment.[^12] Conversely, a failure to update a static site generator like MkDocs poses no immediate runtime risk to the deployed site, as the generated output remains inert HTML.[^3] This architectural difference transforms security maintenance from an emergency incident response capability into a scheduled, predictable engineering task.

| CVE Identifier | CVSS Score | Vulnerability Type | Exploited in Wild? | CISA KEV Status |
|---------------|------------|-------------------|-------------------|-----------------|
| CVE-2023-22515 | 10.0 (Critical) | Broken Access Control / Privilege Escalation | Yes (Zero-Day) | Listed |
| CVE-2023-22527 | 10.0 (Critical) | Remote Code Execution (RCE) | Yes | Listed |
| CVE-2022-26134 | 9.8 (Critical) | OGNL Injection (RCE) | Yes | Listed |
| CVE-2023-22518 | 9.1 (Critical) | Improper Auth / Database Wipe | Yes (Ransomware) | Listed |
| CVE-2025-59343 | 8.7 (High) | File Inclusion (tar-fs dependency) | Unknown | Pending |
| CVE-2025-41249 | 7.5 (High) | Improper Auth (spring-core dependency) | Unknown | Pending |
| CVE-2020-28469 | 7.5 (High) | Denial of Service (DoS) | Unknown | Pending |

---

## 4. Git as an Immutable Cryptographic Audit Trail

Enterprise documentation platforms often house highly sensitive intellectual property, authoritative architecture designs, and internal security procedures. Consequently, they are subject to strict regulatory compliance frameworks, including HIPAA, GDPR, SOX, and SOC 2 trust criteria.[^6] A core foundational requirement of all these frameworks is the maintenance of an immutable, tamper-evident audit trail.

### 4.1 The Forensic Weakness of CMS Page History

Traditional wikis like Confluence provide native "page history" features, which act as a rudimentary audit trail. However, this implementation is fundamentally flawed from a forensic and regulatory compliance perspective. In Confluence Cloud, page histories, unpublished drafts, and even entire pages can be [permanently deleted or purged](https://support.atlassian.com/confluence-cloud/docs/delete-restore-or-purge-a-page/) by users with appropriate administrative or space-level permissions.[^25]

Furthermore, the platform automatically runs background automation jobs that purge unpublished drafts and empty pages. These automated deletions often appear in the organizational audit log as actions performed by an ["anonymous" actor, frequently lacking page titles or location context](https://support.atlassian.com/confluence/kb/the-organizations-audit-log-displays-anonymous-users-deleting-pages/) (a known limitation documented in Atlassian Access issue [ACCESS-2505](https://jira.atlassian.com/browse/ACCESS-2505)).[^26] Additionally, Confluence's default audit log configuration only retains events for [one year, reducible to as little as 31 days](https://support.atlassian.com/confluence-cloud/docs/view-the-audit-log/).[^28]

This profound lack of referential integrity makes it mathematically impossible to guarantee that a specific version of a Confluence document existed at a specific point in time without having been silently altered or purged.[^25]

### 4.2 Git as a Mathematically Verifiable Ledger

The Docs-as-Code architecture solves this non-repudiation problem through the inherent cryptographic properties of Git. Git constructs a Merkle tree of cryptographic hashes (utilizing SHA-1 or SHA-256 algorithms).[^6] Every single commit, author signature, timestamp, and file state is mathematically derived from the preceding commit. It is computationally impossible to alter a historical document, change an author attribution, or retroactively inject a malicious policy modification without altering the cryptographic hash of every subsequent commit, immediately triggering an integrity failure.[^6]

This tamper-evident property directly satisfies stringent federal guidelines, specifically [NIST SP 800-53](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final) Control **CM-3** (Configuration Change Control) and **AU-12** (Audit Generation).[^7] When a compliance auditor requires proof of who authorized a specific architectural change, Git provides a pristine chain of custody.[^32] Frameworks such as SOC 2 and HIPAA explicitly recognize version control hygiene — when paired with strict branch protection rules, mandatory cryptographic commit signing, and centralized logging — as a superior mechanism for establishing irrefutable data integrity.[^6]

A third-order implication of this cryptographic audit trail is its profound impact on incident response velocity. In the event of an intellectual property theft investigation or a configuration drift incident, security operations teams can rely on the Git ledger as an absolute source of truth — completely immune to the application-level data purging capabilities present in standard wiki software.[^29]

---

## 5. CI/CD Security Gates for Documentation

By systematically moving away from runtime exploitation risks, the Docs-as-Code model shifts the primary threat vector to the software supply chain and the continuous integration pipeline.[^36] This paradigm shift requires the implementation of robust, automated pipeline security gates.

### 5.1 Alignment with the SLSA Framework

In response to devastating supply chain attacks, Google introduced the [Supply-chain Levels for Software Artifacts (SLSA)](https://slsa.dev/) framework, providing an authoritative blueprint for securing CI/CD pipelines.[^36]

- **SLSA Build Level 1:** Requires fully scripted builds with provenance metadata.[^37] The entire documentation build is deterministically defined in a declarative YAML file (GitHub Actions workflow).
- **SLSA Build Level 2:** Requires builds on a hosted platform with cryptographically signed provenance.[^37] Enforcing deployments exclusively through hosted runners guarantees the documentation artifact reflects the repository source.
- **SLSA Build Level 3:** Adds hardened, ephemeral build environments.[^37] Each documentation build spins up a clean, isolated runner, executes the MkDocs build, deploys artifacts, and immediately destroys the environment — ensuring hermetic builds.[^36]

### 5.2 Mitigating OWASP Top 10 CI/CD Security Risks

The [OWASP Top 10 CI/CD Security Risks](https://owasp.org/www-project-top-10-ci-cd-security-risks/) framework identifies key pipeline threats:[^39]

| OWASP CI/CD Risk | Risk Description | Docs-as-Code Mitigation |
|-----------------|-----------------|------------------------|
| CICD-SEC-1 | Insufficient Flow Control Mechanisms | Strict branch protection rules, required PR approvals, automated status checks[^39] |
| CICD-SEC-3 | Dependency Chain Abuse | SCA blocking malicious packages; Dependabot for automated updates[^40] |
| CICD-SEC-4 | Poisoned Pipeline Execution (PPE) | Ephemeral runners, SLSA Level 2 provenance signing, immutable build environments[^37] |
| CICD-SEC-6 | Insufficient Credential Hygiene | Workload Identity Federation (OIDC) replacing long-lived deployment credentials[^40] |

### 5.3 Addressing Secret Sprawl via Push Protection

The [2025 State of Secrets Sprawl report by GitGuardian](https://www.scribd.com/document/855773866/The-State-of-Secrets-Sprawl-2025) indicates a massive **25% year-over-year rise** in credential exposure, identifying **23.77 million new hardcoded secrets** in public repositories in 2024 alone.[^42] Generic secrets now account for 58% of all detected leaks.[^42]

While Confluence relies on reactive scanning, enterprise Git platforms like GitHub provide native [Secret Scanning and Push Protection](https://docs.github.com/en/code-security/concepts/secret-security/about-push-protection). Push protection operates as a pre-receive hook; if a developer attempts to commit a document containing a live API key, the Git server intercepts and **rejects the commit entirely**, preventing the secret from ever entering the repository history.[^43][^44]

---

## 6. Separation of Duties and Least Privilege

Information security governance is predicated on the principles of separation of duties and least privilege. [NIST SP 800-53](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final) defines these requirements under controls **AC-5** (Separation of Duties) and **AC-6** (Least Privilege).[^47]

### 6.1 The Author-equals-Publisher Control Weakness

The standard operational model of a dynamic wiki natively violates the principle of separation of duties.[^1] In Confluence, the roles of "author" and "publisher" are inextricably merged. A user with edit privileges can write a document and immediately publish it by clicking "Save." There is no mandatory, system-enforced technical gate requiring secondary review. This presents a significant insider threat risk and a compliance violation in highly regulated environments.[^47]

### 6.2 PR-Based Workflows as Enforced AC-5 Compliance

The Docs-as-Code model enforces NIST SP 800-53 AC-5 by default through the Pull Request workflow.[^7] When an engineer drafts a new architecture document, they do so on an isolated, non-production branch. Branch protection rules require at least one approving review from designated code owners before merge.[^7]

This workflow physically and logically decouples content creation from publication. The author cannot unilaterally publish. The reviewer cannot publish without an author's initial commit. This dual-authorization mechanism ensures peer review is cryptographically enforced, fulfilling compliance mandates while preventing unauthorized architectural documentation from entering the organizational canon.[^7] Furthermore, it aligns with NIST AC-6 by ensuring developers only possess write access to their feature branches, while the CI/CD service principal retains exclusive deployment privilege.[^47]

---

## 7. Azure Static Web Apps Security Posture

### 7.1 Federal Compliance and Certifications

Azure Static Web Apps is comprehensively covered under major independent third-party audit reports, including ISO 27001, ISO 27018, SOC 1, SOC 2, and SOC 3.[^50]

Azure Static Web Apps is designated as compliant under the U.S. [Federal Risk and Authorization Management Program (FedRAMP)](https://learn.microsoft.com/en-us/azure/compliance/offerings/offering-fedramp) High baseline and Department of Defense Impact Level 2 (IL2).[^52] The FedRAMP High authorization incorporates **421 specific security controls** covering incident response, encryption in transit and at rest, and physical security.[^53]

### 7.2 Identity Integration and Network Edge Protection

Azure Static Web Apps natively integrates with [Microsoft Entra ID](https://learn.microsoft.com/en-us/azure/static-web-apps/authentication-custom) for robust authentication and authorization.[^54] This allows enforcement of existing Conditional Access policies, MFA, and real-time session risk evaluations natively.[^55]

From a network security perspective, Azure Static Web Apps integrates with [Enterprise-grade edge powered by Azure Front Door](https://learn.microsoft.com/en-us/azure/static-web-apps/enterprise-edge), providing layered DDoS defense across more than 118 global edge locations.[^15] The CDN caches HTML at the edge, absorbing massive traffic spikes while automatically refusing malformed dynamic application requests.[^15]

---

## 8. Content Security Policy and Header Configurability

### 8.1 The Constraints of Dynamic CMS CSP

Implementing a rigorous CSP in Confluence is notoriously difficult. Confluence Data Center 10.0 introduced a script-src CSP header, but it is implemented exclusively in [**report-only mode**](https://developer.atlassian.com/server/confluence/content-security-policy-adoption/) — the browser logs violations but fails to block malicious execution.[^59] Full enforcement is not expected until future versions.[^62]

In Confluence Cloud, Forge apps often require injection of `unsafe-hashes` or complex custom scopes.[^63] Atlassian explicitly warns that `unsafe-inline` or `unsafe-eval` weakens security, yet legacy plugin complexity often mandates these insecure workarounds.[^64]

### 8.2 Uncompromising Static CSP Enforcement

Because the Docs-as-Code architecture serves purely static files with highly predictable asset origins, administrators can deploy exceptionally strict CSP headers without breaking site functionality. A static site can enforce a baseline policy of `default-src 'self'`, ensuring the browser rejects any injected script.[^65]

[Google research](https://conf.researchr.org/track/icse-2025/icse-2025-research-track) indicates that effective nonce-based or strict hash-based CSP adoption is historically low across the internet precisely due to architectural complexities of dynamic platforms.[^66] By utilizing an SSG, security teams bypass this complexity entirely. Static deployment allows security headers to be hardcoded at the edge CDN level, resulting in a client-side security posture that Confluence cannot replicate without severe functional degradation.[^60]

---

## 9. Plugin Execution Models and Supply Chain Risk

### 9.1 The Danger of Runtime Execution

In Confluence, plugins execute at runtime directly within the application server's context. A vulnerability in a third-party plugin grants attackers direct access to the Confluence server, database credentials, and underlying file system.[^68] Atlassian's [security guidelines for Data Center apps](https://developer.atlassian.com/platform/marketplace/security-requirements-dc/) highlight the profound risks of plugins failing to sanitize untrusted data.[^69]

The catastrophic severity of this model was highlighted when threat actors utilized a malicious application (`web.shell.Plugin`) to maintain persistence during the [CVE-2023-22518 exploitation campaigns](https://confluence.atlassian.com/security/cve-2023-22518-improper-authorization-vulnerability-in-confluence-data-center-and-server-1311473907.html).[^21]

### 9.2 Build-Time Execution Isolation

In the Docs-as-Code ecosystem, extensions (MkDocs Python packages) execute **only during the CI/CD build phase**.[^1] They process flat text files and output static HTML. They are never deployed to the production web server.

If a supply chain attack compromises an MkDocs plugin, the malicious code executes inside the ephemeral GitHub Actions runner. Adoption of [OIDC Workload Identity Federation](https://docs.github.com/en/get-started/learning-about-github/about-github-advanced-security) mitigates this by eliminating long-lived credentials in the pipeline. Once HTML is generated, the runner is destroyed. The resulting static HTML cannot execute backend server commands because there is no backend server.[^1]

---

## 10. Data Sovereignty, Residency, and Privacy

As global privacy regulations (GDPR, UK GDPR, CCPA) become increasingly stringent, organizations must exert granular control over data residency.

Atlassian Cloud offers data residency capabilities, but certain data types are explicitly excluded from residency controls.[^8] Operational telemetry, user account metadata, and application analytics may continue to be routed globally.[^72]

Deploying Docs-as-Code affords absolute control over data location. The Git repository resides in a specific regional data center. Azure Static Web Apps origin storage resides exclusively in the chosen Azure region. Because there is no backend telemetry database, the organization sidesteps opaque residency exclusions inherent to managed SaaS wikis.[^15]

---

## 11. Comparative Breach Realities and Industry Analyst Perspectives

Confluence has been repeatedly targeted and successfully breached by APTs, nation-state actors (Storm-0062), and organized ransomware syndicates.[^16] These are the expected statistical outcome of operating a monolithic, dynamic Java application with a massive internet-facing attack surface.

Conversely, there is an industry-wide absence of comparable breach reports involving static site hosting platforms. While misconfigured CI/CD pipelines can lead to source code leaks, the actual static hosting environments (Azure SWA, Netlify, Vercel) are virtually immune to server-side exploitation.[^74]

Leading analyst firms, including Gartner and Forrester, have consistently highlighted the rapid transition toward decoupled, headless, and static architectures.[^75] In evaluations of Digital Experience Platforms, the move away from monolithic dynamic systems is praised specifically for dramatic improvements in both delivery speed and inherent security posture.[^76]

---

## 12. Conclusion

The transition from Confluence Cloud to a pipeline utilizing Git, MkDocs, CI/CD automation, and Azure Static Web Apps is not merely a lateral shift in tooling; it is a fundamental, structural elevation of the organization's cybersecurity posture.

By physically decoupling the authoring environment from the publishing infrastructure, the architecture enforces mandatory **separation of duties** (NIST SP 800-53 AC-5). By utilizing Git, the organization gains an **immutable, mathematically verifiable audit trail** (NIST SP 800-53 AU-12) that cannot be silently purged. By executing plugins strictly within an ephemeral, **SLSA-compliant CI/CD pipeline**, runtime supply chain risks are eradicated. Finally, by deploying immutable artifacts to an edge-optimized, **FedRAMP-certified** environment like Azure Static Web Apps, the external attack surface is reduced to zero-runtime execution.

This renders the devastating zero-day RCE vulnerabilities and ransomware campaigns that have historically plagued dynamic wikis structurally impossible.

---

## Works Cited

[^1]: [CMS Security Comparison 2025 - Envestis SA](https://envestis.ch/en/blog/confronto-cms-sicurezza-2025)
[^2]: [Azure Static Web Apps documentation - Microsoft Learn](https://learn.microsoft.com/en-us/azure/static-web-apps/)
[^3]: [How to Build Static Sites - freeCodeCamp](https://www.freecodecamp.org/news/how-to-use-jigsaw-to-quickly-and-easily-build-static-sites-8a3304c3ad7e/)
[^4]: [SLSA - Supply-chain Levels for Software Artifacts](https://slsa.dev/)
[^5]: [Introduction - OWASP Top 10:2025](https://owasp.org/Top10/2025/0x00_2025-Introduction/)
[^6]: [HIPAA Compliance in Git - hoop.dev](https://hoop.dev/blog/hipaa-compliance-in-git-preventing-phi-leaks-and-securing-your-repository/)
[^7]: [NIST 800-53 Controls Explained - Aikido](https://www.aikido.dev/learn/compliance/compliance-frameworks/nist-800-53)
[^8]: [Migrating Applications - IBM Redbooks](https://www.redbooks.ibm.com/redbooks/pdfs/sg246690.pdf)
[^9]: [Qualys SAST and IAST FAQs](https://www.qualys.com/faqs-resources-web-application-scanning)
[^10]: [OWASP Attack Surface Management Top 10](https://owasp.org/www-project-attack-surface-management-top-10/)
[^11]: [OWASP Top 10 2025 - GitLab](https://about.gitlab.com/blog/2025-owasp-top-10-whats-changed-and-why-it-matters/)
[^12]: [CISA: Multiple Vulnerabilities in Atlassian Confluence - Greenbone](https://www.greenbone.net/en/blog/cisa-multiple-vulnerabilities-in-atlassian-confluence-are-being-actively-exploited/)
[^13]: [NIST SP 800-123, Guide to General Server Security](https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-123.pdf)
[^14]: [NIST SP 800-95, Guide to Secure Web Services](https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-95.pdf)
[^15]: [Enterprise-grade edge in Azure Static Web Apps - Microsoft Learn](https://learn.microsoft.com/en-us/azure/static-web-apps/enterprise-edge)
[^16]: [Unpacking CVE-2023-22515 and CVE-2023-22518 - Phoenix Security](https://phoenix.security/vuln-atlassian-cve-2023-22515/)
[^17]: [Security Bulletin - February 17, 2026 - Atlassian](https://confluence.atlassian.com/security/security-bulletin-february-17-2026-1722256046.html)
[^18]: [Security at Atlassian: Vulnerabilities](https://www.atlassian.com/trust/data-protection/vulnerabilities)
[^19]: [Atlassian Confluence CVE-2023-22518 - ProjectDiscovery](https://projectdiscovery.io/blog/atlassian-confluence-auth-bypass)
[^20]: [2023 Top Routinely Exploited Vulnerabilities - CISA](https://www.cisa.gov/news-events/cybersecurity-advisories/aa24-317a)
[^21]: [C3RB3R Ransomware: Exploiting CVE-2023-22518 - SentinelOne](https://www.sentinelone.com/blog/c3rb3r-ransomware-ongoing-exploitation-of-cve-2023-22518-targets-unpatched-confluence-servers/)
[^22]: [May 2025 Threat Report - Greenbone](https://www.greenbone.net/en/blog/threat-report-may-2025-hack-rinse-repeat/)
[^25]: [Delete, restore, or purge a content item - Atlassian Support](https://support.atlassian.com/confluence-cloud/docs/delete-restore-or-purge-a-page/)
[^26]: [Audit log displays anonymous users - Atlassian Support](https://support.atlassian.com/confluence/kb/the-organizations-audit-log-displays-anonymous-users-deleting-pages/)
[^27]: [ACCESS-2505: Page Deletion Audit Entries Missing Titles - Atlassian JIRA](https://jira.atlassian.com/browse/ACCESS-2505)
[^28]: [View the audit log - Confluence Cloud - Atlassian Support](https://support.atlassian.com/confluence-cloud/docs/view-the-audit-log/)
[^29]: [Git and AI Coding Agents for Government Compliance - GitHub](https://github.com/brucedombrowski/WhitePaper)
[^32]: [Complete Git Commit Message Templates Guide for Regulated Industries](https://medium.com/@levente.szabo/the-complete-git-commit-message-templates-guide-for-regulated-industries-59c595b771b0)
[^36]: [What is the SLSA Framework? - JFrog](https://jfrog.com/learn/grc/slsa-framework/)
[^37]: [Is SLSA the Best Standard for CI/CD Pipelines? - CBT Nuggets](https://www.cbtnuggets.com/blog/technology/devops/is-slsa-the-best-standard-for-ci-cd-pipelines)
[^38]: [SLSA Framework - Wiz](https://www.wiz.io/academy/application-security/slsa-framework)
[^39]: [OWASP Top 10 CI/CD Security Risks](https://owasp.org/www-project-top-10-ci-cd-security-risks/)
[^40]: [CI/CD Security - OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/CI_CD_Security_Cheat_Sheet.html)
[^41]: [About GitHub Advanced Security](https://docs.github.com/en/get-started/learning-about-github/about-github-advanced-security)
[^42]: [Secrets Sprawl Report 2025 - GitGuardian (Scribd)](https://www.scribd.com/document/855773866/The-State-of-Secrets-Sprawl-2025)
[^43]: [About secret scanning - GitHub Docs](https://docs.github.com/code-security/secret-scanning/about-secret-scanning)
[^44]: [About push protection - GitHub Docs](https://docs.github.com/en/code-security/concepts/secret-security/about-push-protection)
[^47]: [AC-6: Least Privilege - CSF Tools](https://csf.tools/reference/nist-sp-800-53/r5/ac/ac-6/)
[^49]: [SP 800-53 Rev. 5 - NIST CSRC](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
[^50]: [Compliance in the Trusted Cloud - Microsoft Azure](https://azure.microsoft.com/en-us/explore/trusted-cloud/compliance)
[^51]: [Azure compliance documentation - Microsoft Learn](https://learn.microsoft.com/en-us/azure/compliance/)
[^52]: [Azure services in FedRAMP audit scope](https://learn.microsoft.com/en-us/azure/azure-government/compliance/azure-services-in-fedramp-auditscope)
[^53]: [FedRAMP - Azure Compliance](https://learn.microsoft.com/en-us/azure/compliance/offerings/offering-fedramp)
[^54]: [Configure authentication with Azure AD B2C - Microsoft](https://learn.microsoft.com/en-us/azure/active-directory-b2c/configure-authentication-in-azure-static-app)
[^55]: [Custom authentication in Azure Static Web Apps - Microsoft Learn](https://learn.microsoft.com/en-us/azure/static-web-apps/authentication-custom)
[^57]: [Configure a CDN for Azure Static Web Apps - Microsoft Learn](https://learn.microsoft.com/en-us/azure/static-web-apps/front-door-manual)
[^58]: [Azure DDoS Protection Overview - Microsoft Learn](https://learn.microsoft.com/en-us/azure/ddos-protection/ddos-protection-overview)
[^59]: [Content Security Policy adoption - Atlassian Developer](https://developer.atlassian.com/server/confluence/content-security-policy-adoption/)
[^60]: [Secure hosted pages with CSP - PingOne](https://docs.pingidentity.com/pingoneaic/tenants/content-security-policy.html)
[^62]: [Confluence 10.0 release notes - Atlassian](https://confluence.atlassian.com/doc/confluence-10-0-release-notes-1612579091.html)
[^63]: [Forge Permissions - Atlassian Developer](https://developer.atlassian.com/platform/forge/manifest-reference/permissions/)
[^64]: [AGC Developer Security Guidelines - Atlassian](https://developer.atlassian.com/platform/framework/agc/guides/agc-developer-security-guidelines/)
[^65]: [CSP Header Not Set - StackHawk](https://docs.stackhawk.com/vulnerabilities/10038/)
[^66]: [ICSE 2025 Research Track](https://conf.researchr.org/track/icse-2025/icse-2025-research-track)
[^68]: [Confluence Security Overview - Atlassian](https://confluence.atlassian.com/doc/confluence-security-overview-and-advisories-134526.html)
[^69]: [Security requirements for Data Center apps - Atlassian](https://developer.atlassian.com/platform/marketplace/security-requirements-dc/)
[^72]: [Atlassian Data Residency](https://www.atlassian.com/trust/compliance/data-residency)
[^74]: [Netlify Security Rating - Panorays](https://panorays.com/free-security-reports/netlify/)
[^75]: [Top Static Site Generators for 2026 - TestMu AI](https://www.testmuai.com/blog/top-static-site-generators/)
[^76]: [What is a Static Website? - Contentstack](https://www.contentstack.com/blog/all-about-headless/what-is-a-static-website-learn-why-its-perfect-for-speed-and-security)
