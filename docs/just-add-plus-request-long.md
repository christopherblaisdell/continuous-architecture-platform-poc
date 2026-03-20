**Plugin:** Just Add+ (Embed Markdown, Diagrams & Code in Confluence & Git)
**Vendor:** Monocle Consulting (Atlassian Marketplace, 1000+ installs)
**URL:** https://marketplace.atlassian.com/apps/1211438

**Business Need:**
Our architecture practice publishes C4 model diagrams (System Context → Container → Component) to Confluence. The core value of C4 is clickable drill-down — clicking a system box navigates to its container diagram. Confluence Cloud's media sanitizer strips all `<a href>` tags from SVG files on ingest (CONFCLOUD-1762). This is intentional XSS protection by Atlassian, not a bug, but it destroys diagram navigation entirely. Our C4 diagrams are currently static images with no interactivity.

**Why Just Add+:**
Just Add+ renders PlantUML diagrams client-side in the browser DOM by fetching the `.puml` source file directly from our Git repository. The SVG is never ingested by the Confluence media engine, so Atlassian's sanitizer never strips the links. Diagram drill-down is restored.

**Security Argument:**
The concern that "rendering markdown/diagrams is less secure than native Confluence" inverts the actual risk profile:

1. **No new server-side code.** Just Add+ renders in the user's browser using Kroki (a diagram rendering engine). It does not execute server-side code in the Confluence application context — unlike Confluence's own macro engine, which has been the vector for multiple critical CVEs (CVE-2023-22515 CVSS 10.0, CVE-2023-22527 CVSS 10.0, CVE-2022-26134 CVSS 9.8).

2. **Read-only Git integration.** The plugin fetches `.puml` source files from Git with a read-only token. It cannot modify repository content, push code, or access other repositories. The Git repo is the same source-of-truth already secured by branch protection, PR review, and CI/CD gates.

3. **No user input processing.** The plugin renders pre-authored diagram files — it does not accept arbitrary user input. The XSS risk that Atlassian's SVG sanitizer protects against (user-uploaded SVGs containing malicious scripts) does not apply because the content comes from a reviewed, version-controlled Git repository, not from user uploads.

4. **Alternative is worse.** Without this plugin, our options are: (a) accept broken diagrams (unacceptable — defeats the purpose of C4), (b) embed via iframe from our external portal (introduces cross-origin content loading, requires CSP relaxation, and creates a dependency on an external site's availability), or (c) build a custom macro (far greater maintenance and security burden). Just Add+ is the narrowest-scope, lowest-risk solution.

5. **Atlassian Marketplace trust.** The plugin is listed on the Atlassian Marketplace, which requires vendors to complete Atlassian's security self-assessment program (Ecoscope). Marketplace apps are scanned by Atlassian for known vulnerabilities.

**Scope of use:** Architecture team only. Used exclusively for rendering PlantUML C4 diagrams from our architecture Git repository. No markdown rendering needed.
