**Plugin:** Just Add+ | **Need:** Restore C4 diagram drill-down navigation

Confluence strips all hyperlinks from SVG files on upload (CONFCLOUD-1762 — intentional XSS protection). This breaks C4 model navigation — users cannot click through Context → Container → Component diagrams. Just Add+ renders PlantUML diagrams client-side from our Git repo, bypassing the media sanitizer so links are preserved.

**Security response to "markdown is less secure":**
- Plugin renders in the browser, not server-side — unlike Confluence's own macro engine (vector for CVE-2023-22515 CVSS 10.0, CVE-2023-22527 CVSS 10.0)
- Fetches read-only from Git — cannot modify repo content
- Renders pre-authored files from a reviewed repo, not arbitrary user input — the XSS risk Atlassian's sanitizer addresses does not apply
- Alternative (iframe embedding) is worse: requires CSP relaxation and cross-origin content loading
- Atlassian Marketplace-listed, subject to Ecoscope security assessment

**Scope:** Architecture team only. PlantUML C4 diagrams only. No markdown rendering.
