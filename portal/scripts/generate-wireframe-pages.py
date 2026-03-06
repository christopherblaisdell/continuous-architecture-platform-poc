#!/usr/bin/env python3
"""
Generate wireframe pages from Excalidraw JSON files.

Converts .excalidraw JSON files into:
- SVG preview images (static diagrams)
- Interactive HTML viewers
- Markdown wrapper pages

The script scans portal/docs/applications/*/wireframes/ for .excalidraw files
and generates pages in the same directory.
"""

import json
from pathlib import Path


def generate_svg_from_excalidraw(excalidraw_json: dict) -> str:
    """
    Generate a basic SVG preview from Excalidraw JSON.
    
    Excalidraw JSON contains elements with coordinates, dimensions, and text.
    This generates a simple SVG that approximates the wireframe.
    """
    elements = excalidraw_json.get("elements", [])
    
    # Calculate bounding box
    if not elements:
        return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600"><rect width="800" height="600" fill="#fafafa" stroke="#ccc"/></svg>'
    
    # Simple bounds calculation
    min_x = min((e.get("x", 0) for e in elements), default=0)
    min_y = min((e.get("y", 0) for e in elements), default=0)
    max_x = max((e.get("x", 0) + e.get("width", 0) for e in elements), default=800)
    max_y = max((e.get("y", 0) + e.get("height", 0) for e in elements), default=600)
    
    width = max(max_x - min_x + 40, 800)
    height = max(max_y - min_y + 40, 600)
    
    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{min_x - 20} {min_y - 20} {width} {height}" width="100%" height="auto">'
    ]
    
    # Add background
    svg_parts.append(f'<rect x="{min_x - 20}" y="{min_y - 20}" width="{width}" height="{height}" fill="#fafafa" stroke="#e0e0e0" stroke-width="1"/>')
    
    # Draw elements
    for element in elements:
        element_type = element.get("type", "")
        x = element.get("x", 0)
        y = element.get("y", 0)
        w = element.get("width", 100)
        h = element.get("height", 50)
        
        if element_type == "rectangle":
            stroke_color = element.get("strokeColor", "#000000")
            fill_color = element.get("backgroundColor", "#ffffff")
            svg_parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill_color}" stroke="{stroke_color}" stroke-width="2" rx="4"/>')
        
        elif element_type == "ellipse":
            stroke_color = element.get("strokeColor", "#000000")
            fill_color = element.get("backgroundColor", "#ffffff")
            svg_parts.append(f'<circle cx="{x + w/2}" cy="{y + h/2}" r="{min(w, h)/2}" fill="{fill_color}" stroke="{stroke_color}" stroke-width="2"/>')
        
        elif element_type == "text":
            text_content = element.get("text", "")
            font_size = element.get("fontSize", 16)
            text_color = element.get("strokeColor", "#000000")
            svg_parts.append(f'<text x="{x}" y="{y + font_size}" font-size="{font_size}" fill="{text_color}" font-family="sans-serif">{text_content}</text>')
        
        elif element_type == "line":
            x2 = element.get("x2", x)
            y2 = element.get("y2", y)
            stroke_color = element.get("strokeColor", "#000000")
            svg_parts.append(f'<line x1="{x}" y1="{y}" x2="{x2}" y2="{y2}" stroke="{stroke_color}" stroke-width="2"/>')
    
    svg_parts.append('</svg>')
    return '\n'.join(svg_parts)


def generate_wireframe_page(wireframe_dir: Path, excalidraw_file: Path) -> None:
    """Generate markdown wrapper page for a wireframe."""
    
    with open(excalidraw_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    app_type = wireframe_dir.parent.name
    wireframe_name = excalidraw_file.stem
    
    # Get metadata from Excalidraw JSON
    app_state = data.get("appState", {})
    name = app_state.get("name", wireframe_name.replace("-", " ").title())
    
    # Generate SVG
    svg_content = generate_svg_from_excalidraw(data)
    svg_filename = f"{wireframe_name}.svg"
    svg_path = wireframe_dir / svg_filename
    
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    # Generate interactive HTML viewer
    html_filename = f"{wireframe_name}.html"
    html_path = wireframe_dir / html_filename
    
    # Excalidraw JSON is embedded for client-side rendering
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name}</title>
    <script async src="https://cdn.jsdelivr.net/npm/excalidraw@0.15.0/dist/excalidraw.production.min.js"></script>
    <style>
        body {{ margin: 0; padding: 0; font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif; }}
        #root {{ width: 100vw; height: 100vh; }}
        .header {{ position: absolute; top: 10px; left: 10px; z-index: 10; background: white; padding: 10px 15px; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .header h1 {{ margin: 0; font-size: 16px; color: #333; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{name}</h1>
    </div>
    <div id="root"></div>
    <script>
        const excalidrawAPI = window.ExcalidrawAPI;
        const excalidrawData = {json.dumps(data)};
        
        excalidrawAPI.render(
            document.getElementById("root"),
            {{
                elements: excalidrawData.elements,
                appState: {{
                    ...excalidrawData.appState,
                    readOnly: true
                }},
                onChange: () => {{}}
            }}
        );
    </script>
</body>
</html>"""
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Generate markdown page
    md_filename = f"{wireframe_name}.md"
    md_path = wireframe_dir / md_filename
    
    md_content = f"""# {name}

## Preview

<object data="{svg_filename}" type="image/svg+xml" style="width: 100%; border: 1px solid #e0e0e0; border-radius: 4px;"></object>

## Interactive Viewer

**[Open Interactive Editor →]({html_filename})**

Open in the interactive Excalidraw viewer to explore the wireframe with zoom and pan controls.

## Design Notes

- **Purpose**: {name}
- **App**: {app_type.replace("-", " ").title()}
- **Status**: Draft

## Integration Points

This wireframe represents the user interface for the {app_type.replace("-", " ")} application.

### Related Services

- Relevant microservices that power this screen can be found in the [Microservice Pages](../../microservices/)

### Design Rationale

This screen design addresses the following user needs:

- User interaction flow visualization
- Component layout and placement
- State transitions and navigation

## Feedback

To provide feedback or propose changes to this wireframe:

1. Download the Excalidraw JSON source file
2. Edit at [excalidraw.com](https://excalidraw.com)
3. Submit updates via pull request

---

*This wireframe is maintained as part of NovaTrek Adventures enterprise architecture documentation.*
"""
    
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"✓ Generated wireframe: {md_path}")


def main():
    """Generate all wireframe pages."""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    portal_dir = project_root / "portal" / "docs" / "applications"
    
    wireframe_count = 0
    
    # Scan all application directories
    for app_dir in portal_dir.iterdir():
        if not app_dir.is_dir() or app_dir.name == "puml":
            continue
        
        wireframes_dir = app_dir / "wireframes"
        if not wireframes_dir.exists():
            continue
        
        # Process all .excalidraw files
        for excalidraw_file in wireframes_dir.glob("*.excalidraw"):
            try:
                generate_wireframe_page(wireframes_dir, excalidraw_file)
                wireframe_count += 1
            except (json.JSONDecodeError, IOError, ValueError) as e:
                print(f"✗ Error processing {excalidraw_file}: {e}")
    
    print(f"\nGenerated {wireframe_count} wireframe pages")


if __name__ == "__main__":
    main()
