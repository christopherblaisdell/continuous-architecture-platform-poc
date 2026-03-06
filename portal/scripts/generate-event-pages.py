#!/usr/bin/env python3
"""
Generate AsyncAPI UI pages for the NovaTrek Architecture Portal.

Reads AsyncAPI YAML specs from architecture/events/ and generates one HTML page
per producing service under portal/docs/events-ui/. Each page embeds the spec
inline and renders it with the AsyncAPI React component (CDN-loaded).

Usage:
    python3 portal/scripts/generate-event-pages.py
"""

import json
import os

import yaml

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EVENTS_DIR = os.path.join(WORKSPACE_ROOT, "architecture", "events")
EVENTS_UI_DIR = os.path.join(WORKSPACE_ROOT, "portal", "docs", "events-ui")

ASYNCAPI_HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — Event Specification</title>
  <link rel="stylesheet" href="https://unpkg.com/@asyncapi/react-component@1.4.10/styles/default.min.css">
  <style>
    :root {{
      --nt-navy: #1a2744;
      --nt-copper: #c77b30;
      --nt-slate: #f8fafc;
      --nt-text: #1e293b;
      --nt-border: #e2e8f0;
    }}
    body {{
      margin: 0;
      padding: 0;
      font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
      background: var(--nt-slate);
      color: var(--nt-text);
    }}
    .nt-header {{
      background: var(--nt-navy);
      color: white;
      padding: 1rem 2rem;
      display: flex;
      align-items: center;
      gap: 1rem;
    }}
    .nt-header h1 {{
      margin: 0;
      font-size: 1.25rem;
      font-weight: 600;
    }}
    .nt-header a {{
      color: var(--nt-copper);
      text-decoration: none;
      font-size: 0.9rem;
    }}
    .nt-header a:hover {{
      text-decoration: underline;
    }}
    .nt-breadcrumb {{
      background: white;
      border-bottom: 1px solid var(--nt-border);
      padding: 0.5rem 2rem;
      font-size: 0.85rem;
      color: #64748b;
    }}
    .nt-breadcrumb a {{
      color: var(--nt-copper);
      text-decoration: none;
    }}
    .nt-breadcrumb a:hover {{
      text-decoration: underline;
    }}
    #asyncapi-container {{
      max-width: 1200px;
      margin: 2rem auto;
      padding: 0 2rem;
    }}
  </style>
</head>
<body>
  <div class="nt-header">
    <h1>{title} — Event Specification</h1>
    <a href="/events/">Back to Event Catalog</a>
    <a href="/microservices/{svc_name}/">Service Page</a>
  </div>
  <div class="nt-breadcrumb">
    <a href="/">Portal</a> &rsaquo;
    <a href="/events/">Event Catalog</a> &rsaquo;
    {title}
  </div>
  <div id="asyncapi-container">
    <asyncapi-component
      schemaFetchError="Failed to load AsyncAPI specification"
      cssImportPath="https://unpkg.com/@asyncapi/react-component@1.4.10/styles/default.min.css">
    </asyncapi-component>
  </div>
  <script src="https://unpkg.com/@asyncapi/react-component@1.4.10/browser/standalone/index.js"></script>
  <script>
    const schema = {spec_json};
    AsyncApiStandalone.render({{ schema: schema, config: {{ show: {{ sidebar: true }} }} }}, document.getElementById('asyncapi-container'));
  </script>
</body>
</html>
"""


def main():
    os.makedirs(EVENTS_UI_DIR, exist_ok=True)

    if not os.path.isdir(EVENTS_DIR):
        print(f"  No events directory found at {EVENTS_DIR}")
        return

    spec_files = sorted(f for f in os.listdir(EVENTS_DIR) if f.endswith(".events.yaml"))
    if not spec_files:
        print("  No AsyncAPI spec files found")
        return

    print(f"Generating AsyncAPI UI pages from {len(spec_files)} specs...")

    for spec_file in spec_files:
        svc_name = spec_file.replace(".events.yaml", "")
        spec_path = os.path.join(EVENTS_DIR, spec_file)

        with open(spec_path, encoding="utf-8") as f:
            spec = yaml.safe_load(f)

        title = spec.get("info", {}).get("title", svc_name)
        spec_json = json.dumps(spec, indent=2)

        html = ASYNCAPI_HTML_TEMPLATE.format(
            title=title,
            svc_name=svc_name,
            spec_json=spec_json,
        )

        output_path = os.path.join(EVENTS_UI_DIR, f"{svc_name}.html")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"  {svc_name}: {output_path}")

    print(f"\n  Done! {len(spec_files)} AsyncAPI UI pages generated")
    print(f"  Output: {EVENTS_UI_DIR}/")


if __name__ == "__main__":
    main()
