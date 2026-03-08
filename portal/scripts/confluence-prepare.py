#!/usr/bin/env python3
"""Prepare portal Markdown files for Confluence publishing via `mark`.

Reads portal/docs/ Markdown files, applies transformations to make them
compatible with Confluence Storage Format, and writes the results to
portal/confluence/ as a staging directory for `mark` to publish.

Transformations (applied in order):
  1. Inject `mark` metadata headers (Space, Parent, Title, Label)
  2. Insert do-not-edit banner
  3. Add portal link callout for interactive pages
  4. Convert MkDocs admonitions to Confluence macros
  5. Convert <object> SVG tags to Markdown images
  6. Convert MkDocs content tabs to H3 sections
  7. Rewrite internal links (relative paths -> Confluence page titles)
  8. Strip MkDocs-specific syntax (attribute lists, Material emoji, etc.)

Usage:
    python3 portal/scripts/confluence-prepare.py
    python3 portal/scripts/confluence-prepare.py --dry-run
"""

import os
import re
import shutil
import sys
import yaml

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PORTAL_DIR = os.path.join(WORKSPACE_ROOT, "portal")
DOCS_DIR = os.path.join(PORTAL_DIR, "docs")
CONFLUENCE_DIR = os.path.join(PORTAL_DIR, "confluence")
MKDOCS_YML = os.path.join(PORTAL_DIR, "mkdocs.yml")

PORTAL_BASE_URL = "https://mango-sand-083b8ce0f.4.azurestaticapps.net"
CONFLUENCE_SPACE = "ARCH"

# Directories to exclude from publishing
EXCLUDE_DIRS = {
    "services/api",
    "specs",
    "search",
    "microservices/svg",
    "microservices/puml",
    "events-ui",
}

# Files to exclude
EXCLUDE_FILES = {"tags.md"}

# Admonition type -> Confluence macro mapping
ADMONITION_MAP = {
    "note": "note",
    "warning": "warning",
    "danger": "warning",
    "tip": "tip",
    "hint": "tip",
    "info": "info",
    "abstract": "info",
    "summary": "info",
    "example": "panel",
    "question": "note",
    "quote": "quote",
    "bug": "warning",
    "success": "info",
    "failure": "warning",
}


# ── Nav Parsing ──

def parse_mkdocs_nav():
    """Parse portal/mkdocs.yml nav to build file -> (title, parent) mapping."""
    # Use a custom loader that ignores Python-specific YAML tags
    # (e.g., !!python/name:material.extensions.emoji.twemoji)
    class _PermissiveLoader(yaml.SafeLoader):
        pass

    _PermissiveLoader.add_multi_constructor(
        "tag:yaml.org,2002:python/",
        lambda loader, suffix, node: None,
    )

    with open(MKDOCS_YML, encoding="utf-8") as f:
        config = yaml.load(f, Loader=_PermissiveLoader)  # noqa: S506

    nav = config.get("nav", [])
    file_map = {}  # rel_path -> {"title": ..., "parent": ...}
    _walk_nav(nav, None, file_map)
    return file_map


def _walk_nav(items, parent_title, file_map, grandparent_title=None):
    """Recursively walk the nav tree."""
    for item in items:
        if isinstance(item, str):
            # Plain file reference (no title)
            file_map[item] = {"title": _title_from_path(item), "parent": parent_title,
                              "grandparent": grandparent_title}
        elif isinstance(item, dict):
            for key, val in item.items():
                if isinstance(val, str):
                    # "Title: path.md"
                    file_map[val] = {"title": key, "parent": parent_title,
                                     "grandparent": grandparent_title}
                elif isinstance(val, list):
                    # "Section Title: [children]"
                    _walk_nav(val, key, file_map, grandparent_title=parent_title)


def _title_from_path(path):
    """Derive a title from a file path when none is given in nav."""
    basename = os.path.splitext(os.path.basename(path))[0]
    if basename == "index":
        parent_dir = os.path.basename(os.path.dirname(path))
        return parent_dir.replace("-", " ").title() if parent_dir else "Home"
    return basename.replace("-", " ").title()


# ── Link Rewriting ──

def build_link_map(file_map):
    """Build a path -> Confluence page title map for link rewriting."""
    link_map = {}
    for path, info in file_map.items():
        link_map[path] = info["title"]
        # Also index without .md extension
        if path.endswith(".md"):
            link_map[path[:-3]] = info["title"]
        # Index files can be referenced by directory
        if path.endswith("/index.md"):
            dir_path = path[:-len("/index.md")]
            link_map[dir_path] = info["title"]
            link_map[dir_path + "/"] = info["title"]
    return link_map


def rewrite_internal_links(content, link_map, current_file):
    """Rewrite relative Markdown links to Confluence page titles."""
    current_dir = os.path.dirname(current_file)

    def _replace_link(match):
        text = match.group(1)
        href = match.group(2)

        # Skip external links
        if href.startswith(("http://", "https://", "mailto:", "#")):
            return match.group(0)

        # Split off anchor
        anchor = ""
        if "#" in href:
            href, anchor = href.split("#", 1)
            anchor = "#" + anchor

        # Resolve relative path
        if href:
            resolved = os.path.normpath(os.path.join(current_dir, href))
            # Try with and without .md
            title = link_map.get(resolved)
            if not title and not resolved.endswith(".md"):
                title = link_map.get(resolved + ".md")
            if not title and resolved.endswith("/"):
                title = link_map.get(resolved + "index.md")

            if title:
                return f"[{text}]({title}{anchor})"

        return match.group(0)

    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', _replace_link, content)


# ── Admonition Conversion ──

def convert_admonitions(content):
    """Convert MkDocs admonitions (!!! type) to Confluence macros ({type})."""
    lines = content.split("\n")
    result = []
    i = 0

    while i < len(lines):
        # Match admonition start: !!! type "title" or !!! type
        adm_match = re.match(r'^(!{3}|^\?{3}\+?)\s+(\w+)\s*(?:"([^"]*)")?', lines[i])
        if adm_match:
            is_collapsible = lines[i].startswith("???")
            adm_type = adm_match.group(2).lower()
            adm_title = adm_match.group(3) or adm_type.title()
            macro = ADMONITION_MAP.get(adm_type, "info")

            # Collect indented body lines
            body_lines = []
            i += 1
            while i < len(lines):
                if lines[i] == "":
                    # Blank line could be part of the body or end of it
                    if i + 1 < len(lines) and re.match(r'^    ', lines[i + 1]):
                        body_lines.append("")
                        i += 1
                        continue
                    break
                if re.match(r'^    ', lines[i]):
                    body_lines.append(lines[i][4:])  # strip 4-space indent
                    i += 1
                else:
                    break

            body = "\n".join(body_lines).strip()

            if is_collapsible:
                result.append(f"{{expand:title={adm_title}}}")
                result.append(body)
                result.append("{expand}")
            else:
                result.append(f"{{{macro}:title={adm_title}}}")
                result.append(body)
                result.append(f"{{{macro}}}")
            result.append("")
        else:
            result.append(lines[i])
            i += 1

    return "\n".join(result)


# ── SVG Object Tag Conversion ──

def convert_object_tags(content):
    """Convert <object> SVG tags to Markdown image syntax."""
    def _replace_object(match):
        data = match.group(1)
        alt = match.group(2) or "Diagram"
        return f"![{alt}]({data})"

    # Match <object data="..." ...>alt text</object>
    # Also handle <div class="diagram-wrap">...<object>...</object>...</div>
    content = re.sub(
        r'<div class="diagram-wrap">.*?<object\s+data="([^"]+)"[^>]*>(.*?)</object>.*?</div>',
        lambda m: f"![{m.group(2) or 'Diagram'}]({m.group(1)})",
        content,
        flags=re.DOTALL,
    )
    # Standalone <object> tags
    content = re.sub(
        r'<object\s+data="([^"]+)"[^>]*>(.*?)</object>',
        _replace_object,
        content,
        flags=re.DOTALL,
    )
    return content


# ── Content Tab Conversion ──

def convert_content_tabs(content):
    """Convert MkDocs Material content tabs (=== "Tab") to H3 sections."""
    lines = content.split("\n")
    result = []
    i = 0

    while i < len(lines):
        tab_match = re.match(r'^===\s+"([^"]+)"', lines[i])
        if tab_match:
            tab_name = tab_match.group(1)
            result.append(f"### {tab_name}")
            result.append("")

            # Collect indented body lines
            i += 1
            while i < len(lines):
                if lines[i] == "":
                    if i + 1 < len(lines) and re.match(r'^    ', lines[i + 1]):
                        result.append("")
                        i += 1
                        continue
                    result.append("")
                    i += 1
                    break
                if re.match(r'^    ', lines[i]):
                    result.append(lines[i][4:])
                    i += 1
                else:
                    break

            result.append("---")
            result.append("")
        else:
            result.append(lines[i])
            i += 1

    return "\n".join(result)


# ── MkDocs Syntax Stripping ──

def strip_mkdocs_syntax(content):
    """Remove MkDocs-specific syntax not supported by Confluence."""
    # Attribute lists: { .class } { #id } { .md-button }
    content = re.sub(r'\{\s*[:.#][^}]*\}', '', content)

    # Material Design emoji shortcodes: :material-xxx:  (clean up extra spaces)
    content = re.sub(r':material-[a-z0-9-]+:\s*', '', content)

    # YAML frontmatter (already handled by mark, remove to avoid duplication)
    content = re.sub(r'^---\n.*?\n---\n', '', content, count=1, flags=re.DOTALL)

    # HTML comments (preserve mark headers: <!-- Space: -->, etc.)
    content = re.sub(
        r'<!--(?!\s*(?:Space|Parent|Title|Label|Macro)\s*:).*?-->',
        '',
        content,
        flags=re.DOTALL,
    )

    # Clean up multiple blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)

    return content


# ── Header Injection ──

def inject_headers(content, title, parent, labels=None):
    """Inject mark metadata headers at the top of the file."""
    if labels is None:
        labels = ["auto-generated", "do-not-edit"]

    header_lines = [
        f"<!-- Space: {CONFLUENCE_SPACE} -->",
        f"<!-- Parent: {parent} -->",
        f"<!-- Title: {title} -->",
        f'<!-- Label: {",".join(labels)} -->',
        "",
    ]
    return "\n".join(header_lines) + content


# ── Banner Insertion ──

DO_NOT_EDIT_BANNER = (
    "> **This page is auto-generated from Git. Do not edit here.**\n"
    f"> Source: [NovaTrek Architecture Portal]({PORTAL_BASE_URL})\n"
    "> Any changes made on this Confluence page will be overwritten on the next deploy.\n"
    "\n"
)


def insert_banner(content):
    """Insert do-not-edit banner after mark headers, before first content."""
    # Find the end of mark headers (lines starting with <!--)
    lines = content.split("\n")
    insert_pos = 0
    for i, line in enumerate(lines):
        if line.startswith("<!--") or line.strip() == "":
            insert_pos = i + 1
        else:
            break

    lines.insert(insert_pos, DO_NOT_EDIT_BANNER)
    return "\n".join(lines)


def add_portal_link(content, rel_path):
    """Add interactive portal link callout for pages with SVG diagrams."""
    # Only add for microservice, application, and event pages
    page_dir = rel_path.split("/")[0] if "/" in rel_path else ""
    if page_dir not in ("microservices", "applications", "events"):
        return content

    # Derive portal URL from relative path
    url_path = rel_path.replace(".md", "/").replace("index/", "")
    portal_url = f"{PORTAL_BASE_URL}/{url_path}"

    callout = (
        f"{{info:title=Interactive Version Available}}"
        f"View the full interactive version with clickable SVG diagrams at: "
        f"[NovaTrek Architecture Portal]({portal_url})"
        f"{{info}}\n\n"
    )

    # Insert after banner
    banner_end = content.find("\n> Any changes made")
    if banner_end >= 0:
        next_line = content.find("\n\n", banner_end) + 2
        content = content[:next_line] + callout + content[next_line:]
    else:
        content += callout

    return content


# ── Path Resolution ──

def should_exclude(rel_path):
    """Check if a file should be excluded from Confluence publishing."""
    rel_str = str(rel_path).replace(os.sep, "/")

    if rel_str in EXCLUDE_FILES:
        return True

    for excl in EXCLUDE_DIRS:
        if rel_str.startswith(excl + "/") or rel_str == excl:
            return True

    return False


def derive_labels(rel_path, title):
    """Derive Confluence labels from the file path and title."""
    labels = ["auto-generated", "do-not-edit"]
    parts = rel_path.replace(os.sep, "/").split("/")

    if parts[0] == "microservices" and len(parts) > 1:
        svc = parts[1].replace(".md", "")
        if svc.startswith("svc-"):
            labels.extend(["microservice", svc])
    elif parts[0] == "solutions":
        labels.append("solution")
        # Extract ticket ID
        ticket_match = re.search(r'NTK-\d+', rel_path)
        if ticket_match:
            labels.append(ticket_match.group(0))
    elif parts[0] == "tickets":
        labels.append("ticket")
        ticket_match = re.search(r'NTK-\d+', rel_path)
        if ticket_match:
            labels.append(ticket_match.group(0))
    elif parts[0] == "capabilities":
        labels.append("capability")
    elif parts[0] == "standards":
        labels.append("standard")
        if len(parts) > 1:
            slug = parts[1].replace(".md", "")
            if slug != "index":
                labels.append(slug)
    elif parts[0] == "applications":
        labels.append("application")
    elif parts[0] == "events":
        labels.append("event")
    elif parts[0] == "actors":
        labels.append("actor")
    elif parts[0] == "services":
        labels.append("service-catalog")

    return labels


# ── Main Pipeline ──

def process_all_files(dry_run=False):
    """Main entry point: transform all portal docs for Confluence."""
    nav_map = parse_mkdocs_nav()
    link_map = build_link_map(nav_map)

    # Clean staging directory
    if not dry_run:
        if os.path.exists(CONFLUENCE_DIR):
            shutil.rmtree(CONFLUENCE_DIR)
        os.makedirs(CONFLUENCE_DIR, exist_ok=True)

    processed = 0
    skipped = 0

    for root, _dirs, files in os.walk(DOCS_DIR):
        for filename in sorted(files):
            filepath = os.path.join(root, filename)
            rel_path = os.path.relpath(filepath, DOCS_DIR).replace(os.sep, "/")

            if not filename.endswith(".md"):
                continue

            if should_exclude(rel_path):
                skipped += 1
                continue

            # Look up nav metadata
            nav_info = nav_map.get(rel_path, {})
            title = nav_info.get("title", _title_from_path(rel_path))
            parent = nav_info.get("parent", "NovaTrek Architecture Portal")
            grandparent = nav_info.get("grandparent")

            if parent is None:
                parent = "NovaTrek Architecture Portal"

            # Index pages whose title matches the parent section name (case-insensitive)
            # ARE the landing page for that section. Promote them: use the exact
            # section name as title and the grandparent section as parent.
            if title.lower() == parent.lower():
                title = parent  # Use exact section name casing
                parent = grandparent if grandparent else "NovaTrek Architecture Portal"

            labels = derive_labels(rel_path, title)

            with open(filepath, encoding="utf-8") as f:
                content = f.read()

            # Apply transformations in order
            content = strip_mkdocs_syntax(content)
            content = convert_admonitions(content)
            content = convert_object_tags(content)
            content = convert_content_tabs(content)
            content = rewrite_internal_links(content, link_map, rel_path)
            content = inject_headers(content, title, parent, labels)
            content = insert_banner(content)
            content = add_portal_link(content, rel_path)

            if dry_run:
                print(f"  [DRY RUN] {rel_path}")
                print(f"            Title: {title}")
                print(f"            Parent: {parent}")
                print(f"            Labels: {', '.join(labels)}")
            else:
                dst = os.path.join(CONFLUENCE_DIR, rel_path)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                with open(dst, "w", encoding="utf-8") as f:
                    f.write(content)

            processed += 1

    # Copy image assets (SVGs, PNGs)
    if not dry_run:
        images_copied = 0
        for ext in ("*.svg", "*.png"):
            for root, _dirs, files in os.walk(DOCS_DIR):
                for filename in files:
                    if not filename.endswith(ext.lstrip("*")):
                        continue
                    src = os.path.join(root, filename)
                    rel = os.path.relpath(src, DOCS_DIR)
                    dst = os.path.join(CONFLUENCE_DIR, rel)
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    shutil.copy2(src, dst)
                    images_copied += 1

        print(f"  Copied {images_copied} image assets")

    print(f"\n  Confluence preparation complete:")
    print(f"    Processed: {processed} pages")
    print(f"    Skipped:   {skipped} files (excluded paths)")
    if not dry_run:
        print(f"    Output:    {CONFLUENCE_DIR}")


if __name__ == "__main__":
    dry = "--dry-run" in sys.argv
    if dry:
        print("  Running in dry-run mode (no files written)\n")
    process_all_files(dry_run=dry)
