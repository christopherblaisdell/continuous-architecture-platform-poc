#!/usr/bin/env python3
"""
generate-tool-instructions.py
Distributes canonical AI instruction content from .github/ source files to
per-tool native formats for Cursor, RooCode, Windsurf, Claude Code, and Gemini CLI.

Usage:
  python3 scripts/generate-tool-instructions.py            # write all files
  python3 scripts/generate-tool-instructions.py --dry-run  # print what would be written
  python3 scripts/generate-tool-instructions.py --check    # exit 1 if any file is out of sync
  python3 scripts/generate-tool-instructions.py --tool cursor  # write one tool only
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Source manifest
# Each entry describes one source file and where its content goes.
# ---------------------------------------------------------------------------

ROOT = Path(__file__).parent.parent

MANIFEST = [
    {
        "source": ".github/copilot-instructions.md",
        "section_title": "Core Architecture Instructions",
        "path_scope": None,
        "cursor": {
            "path": ".cursor/rules/novatrek-architecture.mdc",
            "description": "NovaTrek Adventures Solution Architect — full persona, domain model, workflow rules",
            "always_apply": True,
            "globs": None,
        },
        "roocode": {
            "path": ".roo/rules/novatrek-architecture.md",
        },
        "windsurf_section": "Core Architecture Instructions",
        "claude_section": "Core Architecture Instructions",
        "gemini_section": "Core Architecture Instructions",
    },
    {
        "source": ".github/instructions/github-urls.instructions.md",
        "section_title": "GitHub URL Formatting Rules",
        "path_scope": None,
        "cursor": {
            "path": ".cursor/rules/github-urls.mdc",
            "description": "GitHub URL formatting rules — correct paths, no spurious fragments",
            "always_apply": True,
            "globs": None,
        },
        "roocode": {
            "path": ".roo/rules/github-urls.md",
        },
        "windsurf_section": "GitHub URL Formatting Rules",
        "claude_section": "GitHub URL Formatting Rules",
        "gemini_section": "GitHub URL Formatting Rules",
    },
    {
        "source": ".github/instructions/prompt-me.instructions.md",
        "section_title": "Prompt Me — Interactive Decision Loop",
        "path_scope": None,
        "cursor": {
            "path": ".cursor/rules/prompt-me.mdc",
            "description": "Prompt Me — interactive decision-loop workflow triggered when the user says 'prompt me'",
            "always_apply": True,
            "globs": None,
        },
        "roocode": {
            "path": ".roo/rules/prompt-me.md",
        },
        "windsurf_section": "Prompt Me — Interactive Decision Loop",
        "claude_section": "Prompt Me — Interactive Decision Loop",
        "gemini_section": "Prompt Me — Interactive Decision Loop",
    },
    {
        "source": "architecture/.instructions.md",
        "section_title": "Path-Scoped: architecture/** — Security Context",
        "path_scope": "architecture/**",
        "path_scope_note": "These rules apply when working in the `architecture/` directory.",
        "cursor": {
            "path": ".cursor/rules/architecture-context.mdc",
            "description": "NovaTrek architecture security context — data ownership, identity resolution, safety defaults",
            "always_apply": False,
            "globs": "architecture/**",
        },
        "roocode": {
            "path": ".roo/rules/architecture-context.md",
        },
        "windsurf_section": "Path-Scoped: architecture/** — Security Context",
        "claude_section": "Path-Scoped: architecture/** — Security Context",
        "gemini_section": "Path-Scoped: architecture/** — Security Context",
    },
    {
        "source": "architecture/solutions/.instructions.md",
        "section_title": "Path-Scoped: architecture/solutions/** — Solution Design",
        "path_scope": "architecture/solutions/**",
        "path_scope_note": "These rules apply when working in `architecture/solutions/`.",
        "cursor": {
            "path": ".cursor/rules/architecture-solutions.mdc",
            "description": "NovaTrek solution design workflow — prior-art discovery, review checklist, anti-pattern detection",
            "always_apply": False,
            "globs": "architecture/solutions/**",
        },
        "roocode": {
            "path": ".roo/rules/architecture-solutions.md",
        },
        "windsurf_section": "Path-Scoped: architecture/solutions/** — Solution Design",
        "claude_section": "Path-Scoped: architecture/solutions/** — Solution Design",
        "gemini_section": "Path-Scoped: architecture/solutions/** — Solution Design",
    },
    {
        "source": "architecture/specs/.instructions.md",
        "section_title": "Path-Scoped: architecture/specs/** — OpenAPI Rules",
        "path_scope": "architecture/specs/**",
        "path_scope_note": "These rules apply when working in `architecture/specs/`.",
        "cursor": {
            "path": ".cursor/rules/architecture-specs.mdc",
            "description": "NovaTrek OpenAPI spec design rules — resource naming, HTTP methods, schema completeness, backward compatibility",
            "always_apply": False,
            "globs": "architecture/specs/**",
        },
        "roocode": {
            "path": ".roo/rules/architecture-specs.md",
        },
        "windsurf_section": "Path-Scoped: architecture/specs/** — OpenAPI Rules",
        "claude_section": "Path-Scoped: architecture/specs/** — OpenAPI Rules",
        "gemini_section": "Path-Scoped: architecture/specs/** — OpenAPI Rules",
    },
]

SINGLE_FILE_TARGETS = {
    "windsurf": ".windsurfrules",
    "claude": "CLAUDE.md",
    "gemini": "GEMINI.md",
}

SINGLE_FILE_HEADER = """\
# NovaTrek Architecture Platform — AI Instructions

This file is auto-generated. Do not edit manually.
Source: .github/copilot-instructions.md and .github/instructions/*.instructions.md
Regenerate: python3 scripts/generate-tool-instructions.py

"""

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_FRONTMATTER_RE = re.compile(r"^---\s*\n.*?\n---\s*\n", re.DOTALL)


def strip_frontmatter(content: str) -> str:
    """Remove YAML frontmatter block if present."""
    return _FRONTMATTER_RE.sub("", content, count=1).lstrip("\n")


def read_source(relative_path: str) -> str:
    path = ROOT / relative_path
    if not path.exists():
        print(f"ERROR: source file not found: {path}", file=sys.stderr)
        sys.exit(1)
    return strip_frontmatter(path.read_text(encoding="utf-8"))


def cursor_frontmatter(description: str, always_apply: bool, globs: Optional[str]) -> str:
    lines = ["---"]
    lines.append(f'description: "{description}"')
    if globs:
        lines.append(f"globs: \"{globs}\"")
    lines.append(f"alwaysApply: {str(always_apply).lower()}")
    lines.append("---\n")
    return "\n".join(lines)


def roocode_scope_comment(path_scope: Optional[str], note: Optional[str]) -> str:
    if path_scope and note:
        return f"<!-- Path scope: {path_scope} — {note} -->\n\n"
    return ""


def write_or_check(path: Path, content: str, dry_run: bool, check: bool) -> bool:
    """
    Write content to path. Returns True if the file was (or would be) changed.
    In check mode, returns True if the file is out of sync.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_text(encoding="utf-8") if path.exists() else None
    changed = existing != content

    if check:
        if changed:
            print(f"OUT OF SYNC: {path.relative_to(ROOT)}")
        return changed

    if dry_run:
        status = "WRITE" if changed else "unchanged"
        print(f"  [{status}] {path.relative_to(ROOT)}")
        return changed

    path.write_text(content, encoding="utf-8")
    status = "wrote" if changed else "unchanged"
    print(f"  [{status}] {path.relative_to(ROOT)}")
    return changed


# ---------------------------------------------------------------------------
# Generators
# ---------------------------------------------------------------------------

def generate_cursor(entries: list, dry_run: bool, check: bool) -> list[bool]:
    results = []
    for entry in entries:
        cfg = entry["cursor"]
        content = read_source(entry["source"])
        fm = cursor_frontmatter(cfg["description"], cfg["always_apply"], cfg["globs"])
        output = fm + "\n" + content
        results.append(write_or_check(ROOT / cfg["path"], output, dry_run, check))
    return results


def generate_roocode(entries: list, dry_run: bool, check: bool) -> list[bool]:
    results = []
    for entry in entries:
        cfg = entry["roocode"]
        content = read_source(entry["source"])
        scope_comment = roocode_scope_comment(
            entry.get("path_scope"), entry.get("path_scope_note")
        )
        output = scope_comment + content
        results.append(write_or_check(ROOT / cfg["path"], output, dry_run, check))
    return results


def generate_single_file(
    tool_key: str, section_key: str, output_path: str,
    entries: list, dry_run: bool, check: bool
) -> bool:
    sections = [SINGLE_FILE_HEADER]
    for entry in entries:
        content = read_source(entry["source"])
        section_title = entry[section_key]
        scope_note = entry.get("path_scope_note")

        sections.append(f"## {section_title}\n")
        if scope_note:
            sections.append(f"> Note: {scope_note}\n")
        sections.append(content)
        sections.append("\n---\n")

    # Remove trailing separator
    if sections and sections[-1] == "\n---\n":
        sections.pop()

    output = "\n".join(sections)
    return write_or_check(ROOT / output_path, output, dry_run, check)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Generate per-tool instruction files from canonical sources.")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be written without writing")
    parser.add_argument("--check", action="store_true", help="Exit 1 if any file is out of sync")
    parser.add_argument("--tool", choices=["cursor", "roocode", "windsurf", "claude", "gemini"], help="Generate for one tool only")
    args = parser.parse_args()

    dry_run = args.dry_run
    check = args.check
    tool_filter = args.tool

    if dry_run:
        print("Dry run — no files will be written.\n")

    all_changed: list[bool] = []

    if not tool_filter or tool_filter == "cursor":
        print("Cursor (.cursor/rules/*.mdc)")
        all_changed += generate_cursor(MANIFEST, dry_run, check)

    if not tool_filter or tool_filter == "roocode":
        print("RooCode (.roo/rules/*.md)")
        all_changed += generate_roocode(MANIFEST, dry_run, check)

    if not tool_filter or tool_filter == "windsurf":
        print("Windsurf (.windsurfrules)")
        result = generate_single_file(
            "windsurf", "windsurf_section", ".windsurfrules",
            MANIFEST, dry_run, check
        )
        all_changed.append(result)

    if not tool_filter or tool_filter == "claude":
        print("Claude Code (CLAUDE.md)")
        result = generate_single_file(
            "claude", "claude_section", "CLAUDE.md",
            MANIFEST, dry_run, check
        )
        all_changed.append(result)

    if not tool_filter or tool_filter == "gemini":
        print("Gemini CLI (GEMINI.md)")
        result = generate_single_file(
            "gemini", "gemini_section", "GEMINI.md",
            MANIFEST, dry_run, check
        )
        all_changed.append(result)

    if check and any(all_changed):
        print("\nERROR: Tool instruction files are out of sync.")
        print("Run: python3 scripts/generate-tool-instructions.py")
        sys.exit(1)
    elif check:
        print("All tool instruction files are up to date.")

    if not check and not dry_run:
        changed_count = sum(1 for c in all_changed if c)
        print(f"\nDone. {changed_count} file(s) written.")


if __name__ == "__main__":
    main()
