#!/usr/bin/env python3
"""
Generate Swagger UI pages for the NovaTrek Architecture Portal.

Reads all OpenAPI YAML specs from the workspace and generates one HTML page
per service under portal/docs/services/api/. Each page embeds the spec inline
and renders it with Swagger UI, themed to match the portal's corporate style.

Also generates:
  - portal/docs/services/index.md  (service catalog landing page)
  - Copies YAML specs to portal/docs/specs/ for raw download links

Usage:
    python3 portal/scripts/generate-swagger-pages.py
"""

import os
import yaml
import shutil

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SPECS_DIR = os.path.join(WORKSPACE_ROOT, "phase-1-ai-tool-cost-comparison", "workspace", "corporate-services", "services")
PORTAL_DOCS = os.path.join(WORKSPACE_ROOT, "portal", "docs")
API_OUTPUT = os.path.join(PORTAL_DOCS, "services", "api")
SPECS_OUTPUT = os.path.join(PORTAL_DOCS, "specs")

# ── Metadata loaded from YAML files (portal/docs/metadata/) ──
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from load_metadata import DOMAINS  # noqa: E402

SWAGGER_HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — API Reference</title>
  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5.11.0/swagger-ui.css">
  <style>
    /* ── NovaTrek Corporate Theme for Swagger UI ── */
    :root {{
      --nt-navy: #1a2744;
      --nt-navy-light: #2c3e6b;
      --nt-copper: #c77b30;
      --nt-copper-light: #d4945a;
      --nt-slate: #f8fafc;
      --nt-text: #1e293b;
      --nt-text-light: #475569;
      --nt-border: #e2e8f0;
    }}

    * {{ margin: 0; padding: 0; box-sizing: border-box; }}

    body {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: var(--nt-slate);
      color: var(--nt-text);
    }}

    /* Top bar */
    .nt-header {{
      background: linear-gradient(135deg, #0f172a 0%, var(--nt-navy) 60%, #1e3a5f 100%);
      padding: 1rem 2rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      box-shadow: 0 2px 8px rgba(0,0,0,0.15);
      border-bottom: 3px solid var(--nt-copper);
    }}
    .nt-header a {{
      color: #f8fafc;
      text-decoration: none;
      font-size: 0.85rem;
      opacity: 0.8;
      transition: opacity 0.2s;
    }}
    .nt-header a:hover {{ opacity: 1; }}
    .nt-header-title {{
      color: #ffffff;
      font-size: 1.1rem;
      font-weight: 600;
      letter-spacing: 0.02em;
    }}
    .nt-header-title span {{
      color: var(--nt-copper-light);
      font-weight: 400;
    }}
    .nt-header-links {{
      display: flex;
      gap: 1.5rem;
      align-items: center;
    }}
    .nt-badge {{
      background: rgba(199, 123, 48, 0.2);
      border: 1px solid rgba(199, 123, 48, 0.4);
      color: var(--nt-copper-light);
      padding: 0.2rem 0.6rem;
      border-radius: 1rem;
      font-size: 0.75rem;
      font-weight: 600;
      letter-spacing: 0.03em;
    }}

    /* Meta bar under header */
    .nt-meta {{
      background: #ffffff;
      border-bottom: 1px solid var(--nt-border);
      padding: 0.75rem 2rem;
      display: flex;
      gap: 2rem;
      font-size: 0.8rem;
      color: var(--nt-text-light);
      flex-wrap: wrap;
    }}
    .nt-meta strong {{ color: var(--nt-text); font-weight: 600; }}
    .nt-meta-item {{ display: flex; gap: 0.4rem; align-items: center; }}

    /* Swagger UI container */
    .swagger-container {{
      max-width: 1200px;
      margin: 0 auto;
      padding: 0 1rem;
    }}

    /* ── Swagger UI Overrides ── */

    /* Top bar hidden (we have our own) */
    .swagger-ui .topbar {{ display: none !important; }}

    /* Info section */
    .swagger-ui .info {{ margin: 2rem 0 1rem; }}
    .swagger-ui .info .title {{ color: var(--nt-navy) !important; font-size: 1.8rem !important; }}
    .swagger-ui .info .description p {{ color: var(--nt-text-light); line-height: 1.6; }}

    /* Operation blocks */
    .swagger-ui .opblock.opblock-get {{
      border-color: #2563eb;
      background: rgba(37, 99, 235, 0.04);
    }}
    .swagger-ui .opblock.opblock-get .opblock-summary-method {{
      background: #2563eb;
    }}
    .swagger-ui .opblock.opblock-post {{
      border-color: #059669;
      background: rgba(5, 150, 105, 0.04);
    }}
    .swagger-ui .opblock.opblock-post .opblock-summary-method {{
      background: #059669;
    }}
    .swagger-ui .opblock.opblock-put {{
      border-color: var(--nt-copper);
      background: rgba(199, 123, 48, 0.04);
    }}
    .swagger-ui .opblock.opblock-put .opblock-summary-method {{
      background: var(--nt-copper);
    }}
    .swagger-ui .opblock.opblock-patch {{
      border-color: #7c3aed;
      background: rgba(124, 58, 237, 0.04);
    }}
    .swagger-ui .opblock.opblock-patch .opblock-summary-method {{
      background: #7c3aed;
    }}
    .swagger-ui .opblock.opblock-delete {{
      border-color: #dc2626;
      background: rgba(220, 38, 38, 0.04);
    }}
    .swagger-ui .opblock.opblock-delete .opblock-summary-method {{
      background: #dc2626;
    }}

    .swagger-ui .opblock .opblock-summary-method {{
      border-radius: 4px;
      font-weight: 700;
      font-size: 0.8rem;
      min-width: 70px;
      text-align: center;
    }}

    .swagger-ui .opblock .opblock-summary-path {{
      font-family: 'JetBrains Mono', 'Fira Code', monospace;
      font-size: 0.9rem;
    }}

    /* Models section */
    .swagger-ui section.models {{
      border: 1px solid var(--nt-border);
      border-radius: 8px;
    }}
    .swagger-ui section.models h4 {{
      color: var(--nt-navy);
      font-size: 1.1rem;
    }}

    /* Tags */
    .swagger-ui .opblock-tag {{
      color: var(--nt-navy) !important;
      font-size: 1.2rem !important;
      border-bottom: 2px solid var(--nt-border);
    }}

    /* Buttons — authorize, execute */
    .swagger-ui .btn.authorize {{
      color: var(--nt-copper) !important;
      border-color: var(--nt-copper) !important;
    }}
    .swagger-ui .btn.execute {{
      background: var(--nt-navy) !important;
      border-color: var(--nt-navy) !important;
    }}

    /* Scheme container */
    .swagger-ui .scheme-container {{
      background: #ffffff;
      border: 1px solid var(--nt-border);
      border-radius: 8px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.04);
      padding: 1rem;
    }}

    /* Response codes */
    .swagger-ui .responses-table .response-col_status {{
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
    }}

    /* Footer */
    .nt-footer {{
      background: #0f172a;
      border-top: 3px solid var(--nt-copper);
      color: #94a3b8;
      text-align: center;
      padding: 1.5rem;
      font-size: 0.8rem;
      margin-top: 3rem;
    }}
    .nt-footer a {{ color: var(--nt-copper-light); text-decoration: none; }}
    .nt-footer a:hover {{ text-decoration: underline; }}

    @media (max-width: 768px) {{
      .nt-header {{ padding: 0.75rem 1rem; flex-direction: column; gap: 0.5rem; }}
      .nt-meta {{ padding: 0.5rem 1rem; gap: 1rem; }}
    }}
  </style>
</head>
<body>

  <div class="nt-header">
    <div class="nt-header-title">
      NovaTrek Architecture Portal <span>/ API Reference</span>
    </div>
    <div class="nt-header-links">
      <span class="nt-badge">v{version}</span>
      <a href="../">Service Catalog</a>
      <a href="../../">Portal Home</a>
      <a href="../../specs/{svc_name}.yaml" download>Download YAML</a>
    </div>
  </div>

  <div class="nt-meta">
    <div class="nt-meta-item"><strong>Service:</strong> {svc_name}</div>
    <div class="nt-meta-item"><strong>Owner:</strong> {owner}</div>
    <div class="nt-meta-item"><strong>Version:</strong> {version}</div>
    <div class="nt-meta-item"><strong>Domain:</strong> {domain}</div>
  </div>

  <div class="swagger-container">
    <div id="swagger-ui"></div>
  </div>

  <div class="nt-footer">
    &copy; 2026 NovaTrek Adventures &mdash; Architecture Practice
    &nbsp;|&nbsp;
    <a href="../../">Portal Home</a>
    &nbsp;|&nbsp;
    <a href="../">Service Catalog</a>
  </div>

  <script src="https://unpkg.com/swagger-ui-dist@5.11.0/swagger-ui-bundle.js"></script>
  <script>
    const spec = {spec_json};

    SwaggerUIBundle({{
      spec: spec,
      dom_id: '#swagger-ui',
      deepLinking: true,
      presets: [
        SwaggerUIBundle.presets.apis,
        SwaggerUIBundle.SwaggerUIStandalonePreset
      ],
      layout: "BaseLayout",
      defaultModelsExpandDepth: 1,
      defaultModelExpandDepth: 2,
      docExpansion: "list",
      filter: true,
      showExtensions: true,
      showCommonExtensions: true,
      tryItOutEnabled: false
    }});
  </script>
</body>
</html>
"""


def get_domain_for_service(svc_name):
    """Look up which domain a service belongs to."""
    for domain_name, domain_info in DOMAINS.items():
        if svc_name in domain_info["services"]:
            return domain_name
    return "Unknown"


def generate_swagger_page(spec_path, svc_name):
    """Generate a Swagger UI HTML page for one service."""
    with open(spec_path, 'r') as f:
        spec_data = yaml.safe_load(f)

    # Rewrite .example.com URLs that Swagger UI renders as clickable links.
    # These point to non-existent domains; replace with portal-relative paths.
    info = spec_data.get("info", {})
    contact = info.get("contact", {})
    if contact.get("url", "").endswith(".example.com") or "example.com" in contact.get("url", ""):
        contact["url"] = "../../"
    license_info = info.get("license", {})
    if "example.com" in license_info.get("url", ""):
        del license_info["url"]

    import json
    spec_json = json.dumps(spec_data, indent=2)

    title = spec_data.get("info", {}).get("title", svc_name)
    version = spec_data.get("info", {}).get("version", "0.0.0")
    owner = spec_data.get("info", {}).get("contact", {}).get("name", "Unknown")
    domain = get_domain_for_service(svc_name)

    html = SWAGGER_HTML_TEMPLATE.format(
        title=title,
        version=version,
        owner=owner,
        domain=domain,
        svc_name=svc_name,
        spec_json=spec_json
    )

    os.makedirs(API_OUTPUT, exist_ok=True)
    output_path = os.path.join(API_OUTPUT, f"{svc_name}.html")
    with open(output_path, 'w') as f:
        f.write(html)

    return {
        "name": svc_name,
        "title": title,
        "version": version,
        "owner": owner,
        "domain": domain,
        "description": spec_data.get("info", {}).get("description", "").split("\n")[0].strip()
    }


def count_endpoints(spec_path):
    """Count the number of API endpoints in a spec."""
    with open(spec_path, 'r') as f:
        spec_data = yaml.safe_load(f)
    count = 0
    for path, methods in spec_data.get("paths", {}).items():
        for method in methods:
            if method.lower() in ("get", "post", "put", "patch", "delete", "head", "options"):
                count += 1
    return count


def generate_catalog_page(services):
    """Generate the service catalog landing page as Markdown."""
    # Group services by domain
    domain_services = {}
    for svc in services:
        d = svc["domain"]
        if d not in domain_services:
            domain_services[d] = []
        domain_services[d].append(svc)

    # Domain ordering
    domain_order = [
        "Operations", "Guest Identity", "Booking", "Product Catalog",
        "Safety", "Logistics", "Guide Management", "External", "Support"
    ]

    lines = []
    lines.append("---")
    lines.append("hide:")
    lines.append("  - toc")
    lines.append("tags:")
    lines.append("  - services")
    lines.append("  - api")
    lines.append("---")
    lines.append("")
    lines.append('<div class="hero" markdown>')
    lines.append("")
    lines.append("# Service Catalog")
    lines.append("")
    lines.append('<p class="subtitle">NovaTrek Adventures — Microservice API Reference</p>')
    lines.append("")
    lines.append(f'<span class="version-badge">{len(services)} Services</span>')
    lines.append("")
    lines.append("</div>")
    lines.append("")
    lines.append("Browse the complete inventory of NovaTrek microservices. Each service links to its full, interactive **Swagger UI** API reference — styled, colored, and documented exactly like [Swagger Editor](https://editor.swagger.io/).")
    lines.append("")
    lines.append("---")
    lines.append("")

    for domain_name in domain_order:
        svcs = domain_services.get(domain_name, [])
        if not svcs:
            continue

        domain_info = DOMAINS[domain_name]
        lines.append(f"## {domain_name}")
        lines.append("")
        lines.append("| Service | Version | Owner | API Reference |")
        lines.append("|---------|---------|-------|---------------|")

        for svc in sorted(svcs, key=lambda s: s["name"]):
            spec_path = os.path.join(SPECS_DIR, f"{svc['name']}.yaml")
            endpoint_count = count_endpoints(spec_path)
            lines.append(
                f"| **{svc['title']}**<br>"
                f"<small>`{svc['name']}`</small><br>"
                f"<small>{svc['description'][:80]}{'...' if len(svc['description']) > 80 else ''}</small> "
                f"| `{svc['version']}` "
                f"| {svc['owner']} "
                f"| [:material-api: **Swagger UI** ({endpoint_count} endpoints)](api/{svc['name']}.html){{ .md-button }} |"
            )

        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("!!! tip \"Download Specs\"")
    lines.append("")
    lines.append("    Raw OpenAPI YAML files are available for download from each service's Swagger UI page, or directly from the [specs directory](../specs/).")
    lines.append("")

    catalog_path = os.path.join(PORTAL_DOCS, "services", "index.md")
    os.makedirs(os.path.dirname(catalog_path), exist_ok=True)
    with open(catalog_path, 'w') as f:
        f.write("\n".join(lines))


def copy_specs():
    """Copy raw YAML specs to the portal docs for download."""
    os.makedirs(SPECS_OUTPUT, exist_ok=True)
    for filename in os.listdir(SPECS_DIR):
        if filename.endswith(".yaml"):
            src = os.path.join(SPECS_DIR, filename)
            dst = os.path.join(SPECS_OUTPUT, filename)
            if os.path.realpath(src) == os.path.realpath(dst):
                continue
            shutil.copy2(src, dst)


def main():
    print("Generating NovaTrek Service Catalog for Architecture Portal...")
    print(f"  Specs source: {SPECS_DIR}")
    print(f"  Portal docs:  {PORTAL_DOCS}")
    print()

    # Collect all specs
    spec_files = sorted([
        f for f in os.listdir(SPECS_DIR) if f.endswith(".yaml")
    ])

    services = []
    for spec_file in spec_files:
        svc_name = spec_file.replace(".yaml", "")
        spec_path = os.path.join(SPECS_DIR, spec_file)
        print(f"  Generating Swagger UI: {svc_name}")
        info = generate_swagger_page(spec_path, svc_name)
        services.append(info)

    print()
    print(f"  Generated {len(services)} Swagger UI pages")

    print("  Generating service catalog index...")
    generate_catalog_page(services)

    print("  Copying raw YAML specs for download...")
    copy_specs()

    print()
    print(f"  Done! {len(services)} services in the catalog.")
    print(f"  HTML pages: {API_OUTPUT}/")
    print(f"  YAML specs: {SPECS_OUTPUT}/")


if __name__ == "__main__":
    main()
