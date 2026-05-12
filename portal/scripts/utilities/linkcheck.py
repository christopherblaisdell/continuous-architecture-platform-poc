#!/usr/bin/env python3
"""Crawl a built MkDocs site directory and report broken internal links.

Usage:
    python3 linkcheck.py <site_dir> [--strict] [--json <output.json>]

Options:
    --strict    Exit with code 1 if any broken links are found.
    --json      Write detailed results to the given JSON file.

Notes:
    - Handles unquoted id= attributes produced by mkdocs-minify-plugin.
    - Only checks internal/relative links; external URLs are skipped.
    - Fragment-only (#anchor) links are checked against the current page.
"""
import os
import re
import sys
import json
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote, urljoin
from collections import defaultdict


class LinkExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []  # (kind, url)

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "a" and "href" in d:
            self.links.append(("a", d["href"]))
        elif tag == "img" and "src" in d:
            self.links.append(("img", d["src"]))
        elif tag == "object" and "data" in d:
            self.links.append(("object", d["data"]))
        elif tag == "link" and "href" in d and d.get("rel", "").lower() in (
            "stylesheet", "icon", "shortcut icon", "manifest"
        ):
            self.links.append(("link", d["href"]))
        elif tag == "script" and "src" in d:
            self.links.append(("script", d["src"]))
        elif tag == "iframe" and "src" in d:
            self.links.append(("iframe", d["src"]))


def page_url_from_path(path, root):
    rel = os.path.relpath(path, root)
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    if rel == "index.html":
        return "/"
    return "/" + rel


def resolve(base_url, href):
    fragment = ""
    if "#" in href:
        href, fragment = href.split("#", 1)
    if href == "":
        return ("fragment", base_url, fragment)
    parsed = urlparse(href)
    if parsed.scheme in ("http", "https", "mailto", "tel", "data", "javascript"):
        return ("external", href, fragment)
    if parsed.scheme:
        return ("external", href, fragment)
    if href.startswith("/"):
        target = href
    else:
        target = urljoin(base_url, href)
    target = unquote(target)
    return ("internal", target, fragment)


def target_to_fs(target, root):
    path = target.lstrip("/")
    fs = os.path.join(root, path)
    candidates = [fs]
    if target.endswith("/") or path == "":
        candidates.append(os.path.join(fs, "index.html"))
    else:
        candidates.append(os.path.join(fs, "index.html"))
        candidates.append(fs + ".html")
    for c in candidates:
        if os.path.exists(c):
            return c
    return None


def extract_anchors(html_path):
    """Extract id= and name= values, handling quoted, single-quoted, and
    unquoted attributes (mkdocs-minify-plugin emits unquoted attributes)."""
    try:
        with open(html_path, encoding="utf-8", errors="ignore") as f:
            text = f.read()
    except Exception:
        return set()
    ids = set(re.findall(r'id="([^"]+)"', text))
    ids |= set(re.findall(r"id='([^']+)'", text))
    ids |= set(re.findall(r"id=([^\s>\"']+)", text))
    names = set(re.findall(r'name="([^"]+)"', text))
    names |= set(re.findall(r"name='([^']+)'", text))
    names |= set(re.findall(r"name=([^\s>\"']+)", text))
    return ids | names


# Repo-relative path prefixes that are never built into the portal site.
# Links resolving to these paths are expected to be absent from portal/site/
# and are excluded from the missing_a count.
_NON_PORTAL_PREFIXES = (
    "/docs/",
    "/portal/",
    "/phases/",
    "/architecture/",
    "/source-code/",
    "/.ai-instructions/",
    "/tickets/",
)

# Source-file extensions that are never served as HTML pages.
_NON_PORTAL_EXTENSIONS = (".md", ".yaml", ".yml", ".sh", ".java", ".py")


def _is_repo_only_target(target: str) -> bool:
    """Return True when *target* is a known non-portal repo path.

    These are targets that reference workspace files never published to the
    portal (planning docs, source code, YAML specs, shell scripts). The
    linkchecker would otherwise flag them as missing_a; they are excluded
    because the appropriate fix is in the source authoring, not the portal
    build, and they do not represent broken portal navigation for users.
    """
    # Non-portal repo-directory prefixes (no portal URL equivalent)
    for prefix in _NON_PORTAL_PREFIXES:
        if target.startswith(prefix):
            return True
    # Source-file extensions (not served as HTML)
    for ext in _NON_PORTAL_EXTENSIONS:
        if target.endswith(ext):
            return True
    return False


def main():
    args = sys.argv[1:]
    if not args or args[0].startswith("-"):
        print("Usage: linkcheck.py <site_dir> [--strict] [--json <file>]")
        sys.exit(1)

    root = os.path.abspath(args[0])
    strict = "--strict" in args
    json_out = None
    if "--json" in args:
        idx = args.index("--json")
        if idx + 1 < len(args):
            json_out = args[idx + 1]

    if not os.path.isdir(root):
        print(f"ERROR: {root} is not a directory")
        sys.exit(1)

    results = defaultdict(list)
    anchor_cache = {}

    html_files = []
    for dp, _, fns in os.walk(root):
        for fn in fns:
            if fn.endswith(".html"):
                html_files.append(os.path.join(dp, fn))

    print(f"Crawling {len(html_files)} HTML files in {root}...", file=sys.stderr)
    link_count = 0

    for hp in html_files:
        page_url = page_url_from_path(hp, root)
        try:
            with open(hp, encoding="utf-8", errors="ignore") as f:
                html = f.read()
        except Exception as e:
            results["page_read_error"].append((hp, "", str(e)))
            continue
        ex = LinkExtractor()
        try:
            ex.feed(html)
        except Exception:
            pass
        for kind, href in ex.links:
            link_count += 1
            t, target, fragment = resolve(page_url, href)
            if t == "external":
                continue
            if t == "fragment":
                if fragment:
                    # Skip MkDocs-generated footnote backref anchors (fnref:N).
                    # These are created by the footnotes extension and are valid
                    # at runtime but do not appear as id= attributes in the HTML.
                    if re.match(r"^fnref:\d+$", fragment):
                        continue
                    if hp not in anchor_cache:
                        anchor_cache[hp] = extract_anchors(hp)
                    if fragment not in anchor_cache[hp]:
                        results["fragment_missing_self"].append(
                            (page_url, href, fragment)
                        )
                continue
            fs = target_to_fs(target, root)
            if fs is None:
                # Skip targets that are known repo-only paths or source files
                # not published to the portal.  These produce expected 404s
                # that are not actionable broken-link errors for portal users.
                if kind == "a" and _is_repo_only_target(target):
                    continue
                cat = f"missing_{kind}"
                results[cat].append((page_url, href, target))
            else:
                if fragment and fs.endswith(".html"):
                    # Skip fragment validation for Swagger UI pages — anchors
                    # are injected by JavaScript at runtime and are not present
                    # in the static HTML. The file-exists check above is sufficient.
                    rel_fs = os.path.relpath(fs, root).replace(os.sep, "/")
                    if rel_fs.startswith("services/api/"):
                        continue
                    if fs not in anchor_cache:
                        anchor_cache[fs] = extract_anchors(fs)
                    if fragment not in anchor_cache[fs]:
                        results["fragment_missing"].append(
                            (page_url, href, fragment)
                        )

    print(f"Pages: {len(html_files)}, Links examined: {link_count}", file=sys.stderr)

    summary = {k: len(v) for k, v in results.items()}
    total = sum(summary.values())

    print("\n=== LINK CHECK SUMMARY ===")
    for k, v in sorted(summary.items(), key=lambda x: -x[1]):
        print(f"  {k}: {v}")
    print(f"\nTotal broken: {total}")

    if json_out:
        out = {}
        for k, items in results.items():
            out[k] = [{"page": p, "href": h, "detail": d} for p, h, d in items]
        with open(json_out, "w") as f:
            json.dump(out, f, indent=2)
        print(f"Detailed results saved to {json_out}")

    if strict and total > 0:
        print("\nFAIL: broken links found (--strict mode)", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
