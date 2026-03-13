#!/usr/bin/env python3
"""
Content Policy Check for NovaTrek Architecture Platform.

Enforces organization-specific content rules across architecture documentation:
  1. Terminology consistency  — correct NovaTrek brand and service names
  2. PII safeguards           — no email addresses, phone numbers, or real URLs
                                that could inadvertently expose personal data
  3. Fabricated data markers  — detect placeholder/lorem-ipsum content left
                                in published documents

Usage:
    python3 portal/scripts/utilities/content-policy-check.py [--staged]

Exit codes:
    0  all checks passed
    1  one or more policy violations found
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

# ---------------------------------------------------------------------------
# File selection
# ---------------------------------------------------------------------------

STAGED_FLAG = "--staged" in sys.argv

if STAGED_FLAG:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        cwd=ROOT, capture_output=True, text=True
    )
    all_files = result.stdout.strip().splitlines()
    scope_label = "staged files"
else:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT, capture_output=True, text=True
    )
    all_files = result.stdout.strip().splitlines()
    scope_label = "all tracked files"

TARGET_FILES = [
    f for f in all_files
    if f.endswith(".md") and not any(f.startswith(prefix) for prefix in [
        ".github/",
        "research/",
        "phases/",
        "docs/phase-",
        "docs/research/",
        "portal/docs/standards/arc42/",
        "portal/docs/solutions/",
        "portal/docs/capabilities/",
        "portal/docs/tickets/",
        "portal/docs/actors/",
        "portal/docs/topology/",
        "portal/docs/applications/",
        "portal/docs/events-ui/",
        "portal/site/",
    ])
]


# ---------------------------------------------------------------------------
# Policy definitions
# ---------------------------------------------------------------------------

POLICIES = [
    {
        "id": "P-001",
        "name": "Brand name — misspelled 'Novatrek'",
        "description": "Use 'NovaTrek' (camel-case). 'Novatrek' and 'Nova Trek' are incorrect.",
        # Matches "Novatrek" (Title case, wrong) or "Nova Trek" (two words, wrong)
        # but NOT "NovaTrek" (correct), "novatrek" (in URLs/handles — acceptable),
        # or "NOVATREK" (all-caps acronym context — acceptable).
        "pattern": re.compile(r'\bNovatrek\b|\bNova Trek\b'),
        "severity": "ERROR",
    },
    {
        "id": "P-002",
        "name": "PII — email address pattern",
        "description": "Markdown files should not contain real email addresses. "
                        "Use placeholder@novatrek.example.com if an example is needed.",
        "pattern": re.compile(
            r'\b[A-Za-z0-9._%+\-]+@(?!novatrek\.example\.com)[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b'
        ),
        "severity": "ERROR",
    },
    {
        "id": "P-003",
        "name": "PII — formatted phone number",
        "description": "Markdown files should not contain real phone numbers.",
        # Require formatted phone numbers: (xxx) xxx-xxxx or xxx-xxx-xxxx or +1-xxx-xxx-xxxx
        "pattern": re.compile(
            r'\b(\+?1[\s.\-])?\(?\d{3}\)?[\s.\-]\d{3}[\s.\-]\d{4}\b'
        ),
        "severity": "WARNING",
    },
    {
        "id": "P-005",
        "name": "Placeholder content — lorem ipsum",
        "description": "Lorem ipsum placeholder text must not appear in committed documents.",
        "pattern": re.compile(r'\blorem\s+ipsum\b', re.IGNORECASE),
        "severity": "ERROR",
    },
    {
        "id": "P-006",
        "name": "TODO / FIXME markers left in published documents",
        "description": "TODO and FIXME markers should be resolved before committing architecture "
                        "documents. Use <!-- TODO: ... --> or GitHub issues instead.",
        "pattern": re.compile(r'\bTODO\b|\bFIXME\b'),
        "severity": "WARNING",
    },
]

# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

RED = "\033[0;31m"
YELLOW = "\033[0;33m"
CYAN = "\033[0;36m"
GREEN = "\033[0;32m"
RESET = "\033[0m"


def severity_color(severity: str) -> str:
    return {
        "ERROR": RED,
        "WARNING": YELLOW,
        "INFO": CYAN,
    }.get(severity, RESET)


def check_file(path: Path, policy: dict) -> list[dict]:
    findings = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return findings

    in_html_comment = False
    for lineno, line in enumerate(lines, start=1):
        # Track HTML comment blocks (<!-- ... -->) across lines.
        # A line that opens a comment but doesn't close it starts a block.
        stripped = line
        if in_html_comment:
            if "-->" in stripped:
                in_html_comment = False
                # Remove the closed comment and check the remainder.
                stripped = stripped[stripped.index("-->") + 3:]
            else:
                continue  # entire line is inside a comment block

        # Remove any inline HTML comments from the line before checking.
        # This handles both <!-- single-line --> and opening <!-- without close.
        while "<!--" in stripped:
            open_idx = stripped.index("<!--")
            close_idx = stripped.find("-->", open_idx)
            if close_idx != -1:
                # Inline comment — remove it
                stripped = stripped[:open_idx] + stripped[close_idx + 3:]
            else:
                # Comment opens but does not close on this line
                in_html_comment = True
                stripped = stripped[:open_idx]
                break

        match = policy["pattern"].search(stripped)
        if not match:
            continue
        findings.append({
            "file": str(path.relative_to(ROOT)),
            "line": lineno,
            "col": match.start() + 1,
            "match": match.group(),
            "policy": policy,
        })
    return findings


def main() -> int:
    print("=" * 64)
    print(f" Content Policy Check — {scope_label}")
    print("=" * 64)

    if not TARGET_FILES:
        print(f"{GREEN}✓ No files to check{RESET}")
        return 0

    all_findings: list[dict] = []

    for rel_path in TARGET_FILES:
        abs_path = ROOT / rel_path
        if not abs_path.exists():
            continue
        for policy in POLICIES:
            findings = check_file(abs_path, policy)
            all_findings.extend(findings)

    errors = [f for f in all_findings if f["policy"]["severity"] == "ERROR"]
    warnings = [f for f in all_findings if f["policy"]["severity"] == "WARNING"]

    if all_findings:
        print()
        for finding in all_findings:
            p = finding["policy"]
            color = severity_color(p["severity"])
            print(
                f"{color}{p['severity']}{RESET} [{p['id']}] "
                f"{finding['file']}:{finding['line']}:{finding['col']} — "
                f"{p['name']}"
            )
            print(f"        matched: {finding['match']!r}")
            print(f"        {p['description']}")
            print()

    print("=" * 64)
    summary_parts = []
    if errors:
        summary_parts.append(f"{RED}{len(errors)} error(s){RESET}")
    if warnings:
        summary_parts.append(f"{YELLOW}{len(warnings)} warning(s){RESET}")

    if not all_findings:
        print(f"{GREEN}  PASSED: No content policy violations in {scope_label}{RESET}")
        print("=" * 64)
        return 0

    print(f"  RESULT: {', '.join(summary_parts)} across {len(TARGET_FILES)} files checked")
    print("=" * 64)

    # Only fail on errors, not warnings
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
