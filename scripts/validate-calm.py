#!/usr/bin/env python3
"""Validate CALM topology documents against NovaTrek architecture patterns.

Checks the generated CALM topology for architecture rule violations that
would normally require manual PR review. Also invokes `calm validate`
(FINOS calm-cli) for JSON Schema validation when available.

Usage:
    python3 scripts/validate-calm.py                              # validate all
    python3 scripts/validate-calm.py architecture/calm/domains/operations.json
    python3 scripts/validate-calm.py --patterns architecture/calm/patterns/

Rules enforced:
    1. No shared databases — each database node has exactly one incoming
       'connects' relationship
    2. API-mediated access — no JDBC relationships between services (only
       service-to-its-own-database)
    3. Every service node must have a domain and team in metadata
    4. Every relationship must have both source and target referencing
       existing nodes
    5. No orphan services — every service must have at least one relationship
"""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CALM_DIR = ROOT / "architecture" / "calm"


def load_calm(path):
    with open(path) as f:
        return json.load(f)


def get_relationship_nodes(rel):
    """Extract all node IDs referenced by a CALM 1.2 relationship."""
    rt = rel.get("relationship-type", {})
    nodes = set()
    if "connects" in rt:
        nodes.add(rt["connects"]["source"]["node"])
        nodes.add(rt["connects"]["destination"]["node"])
    elif "interacts" in rt:
        nodes.add(rt["interacts"]["actor"])
        nodes.update(rt["interacts"].get("nodes", []))
    elif "deployed-in" in rt:
        nodes.add(rt["deployed-in"]["container"])
        nodes.update(rt["deployed-in"].get("nodes", []))
    elif "composed-of" in rt:
        nodes.add(rt["composed-of"]["container"])
        nodes.update(rt["composed-of"].get("nodes", []))
    return nodes


def get_connects_pair(rel):
    """Return (source, destination) for a 'connects' relationship, or None."""
    rt = rel.get("relationship-type", {})
    if "connects" in rt:
        return (rt["connects"]["source"]["node"], rt["connects"]["destination"]["node"])
    return None


class ValidationResult:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def error(self, rule, msg):
        self.errors.append(f"[{rule}] {msg}")

    def warning(self, rule, msg):
        self.warnings.append(f"[{rule}] {msg}")

    @property
    def passed(self):
        return len(self.errors) == 0


def validate_no_shared_databases(calm, result):
    """Rule 1: Each database node must have exactly one 'connects' relationship."""
    db_nodes = {n["unique-id"] for n in calm.get("nodes", []) if n.get("node-type") == "database"}
    db_connections = {}

    for rel in calm.get("relationships", []):
        pair = get_connects_pair(rel)
        if pair and pair[1] in db_nodes:
            db_connections.setdefault(pair[1], []).append(pair[0])

    for db_id in db_nodes:
        sources = db_connections.get(db_id, [])
        if len(sources) == 0:
            result.warning("no-shared-databases", f"Database '{db_id}' has no connecting service")
        elif len(sources) > 1:
            result.error("no-shared-databases", f"SHARED DATABASE: '{db_id}' is connected by multiple services: {sources}")


def validate_api_mediated_access(calm, result):
    """Rule 2: No JDBC relationships between two service nodes."""
    service_ids = {n["unique-id"] for n in calm.get("nodes", []) if n.get("node-type") == "service"}

    for rel in calm.get("relationships", []):
        if rel.get("protocol") == "JDBC":
            pair = get_connects_pair(rel)
            if pair and pair[0] in service_ids and pair[1] in service_ids:
                result.error("api-mediated-access", f"JDBC connection between services: {pair[0]} -> {pair[1]} (must use API)")


def validate_service_metadata(calm, result):
    """Rule 3: Every service must have domain and team metadata."""
    for node in calm.get("nodes", []):
        if node.get("node-type") != "service":
            continue
        meta = node.get("metadata", {})
        if not meta.get("domain"):
            result.error("service-metadata", f"Service '{node['unique-id']}' missing 'domain' in metadata")
        if not meta.get("team"):
            result.error("service-metadata", f"Service '{node['unique-id']}' missing 'team' in metadata")


def validate_relationship_integrity(calm, result):
    """Rule 4: All relationship parties must reference existing nodes."""
    node_ids = {n["unique-id"] for n in calm.get("nodes", [])}

    for rel in calm.get("relationships", []):
        for nid in get_relationship_nodes(rel):
            if nid not in node_ids:
                result.error("relationship-integrity",
                             f"Relationship '{rel['unique-id']}' references unknown node: '{nid}'")


def validate_no_orphan_services(calm, result):
    """Rule 5: Every service should participate in at least one relationship."""
    service_ids = {n["unique-id"] for n in calm.get("nodes", []) if n.get("node-type") == "service"}
    connected = set()

    for rel in calm.get("relationships", []):
        connected.update(get_relationship_nodes(rel))

    for svc in service_ids:
        if svc not in connected:
            result.warning("no-orphan-services", f"Service '{svc}' has no relationships (orphan)")


def validate_calm(calm_doc):
    """Run all validation rules against a CALM document."""
    result = ValidationResult()
    validate_no_shared_databases(calm_doc, result)
    validate_api_mediated_access(calm_doc, result)
    validate_service_metadata(calm_doc, result)
    validate_relationship_integrity(calm_doc, result)
    validate_no_orphan_services(calm_doc, result)
    return result


def run_calm_cli(path):
    """Run `calm validate` if the CLI is installed. Returns (passed, output)."""
    calm_bin = shutil.which("calm")
    if not calm_bin:
        return None, "calm CLI not installed — skipping schema validation"

    try:
        proc = subprocess.run(
            [calm_bin, "validate", "-a", str(path), "-f", "pretty"],
            capture_output=True, text=True, timeout=60,
        )
        output = (proc.stdout + proc.stderr).strip()
        # calm validate exits 0 on success (warnings ok), non-zero on errors
        return proc.returncode == 0, output
    except subprocess.TimeoutExpired:
        return False, "calm validate timed out"


def main():
    parser = argparse.ArgumentParser(description="Validate CALM topology against NovaTrek architecture patterns")
    parser.add_argument("files", nargs="*", help="CALM JSON files to validate (default: all in architecture/calm/)")
    parser.add_argument("--skip-cli", action="store_true", help="Skip calm CLI schema validation")
    args = parser.parse_args()

    # Collect files to validate
    if args.files:
        paths = [Path(f) for f in args.files]
    else:
        paths = sorted(CALM_DIR.rglob("*.json"))
        # Exclude pattern files
        paths = [p for p in paths if "patterns" not in p.parts and "controls" not in p.parts]

    if not paths:
        print("No CALM files found to validate.")
        sys.exit(1)

    total_errors = 0
    total_warnings = 0
    cli_failures = 0

    for path in paths:
        calm = load_calm(path)
        result = validate_calm(calm)
        rel_path = path.relative_to(ROOT)

        status = "PASS" if result.passed else "FAIL"
        n_nodes = len(calm.get("nodes", []))
        n_rels = len(calm.get("relationships", []))

        print(f"[{status}] {rel_path} ({n_nodes} nodes, {n_rels} relationships)")

        for err in result.errors:
            print(f"  ERROR: {err}")
        for warn in result.warnings:
            print(f"  WARN:  {warn}")

        total_errors += len(result.errors)
        total_warnings += len(result.warnings)

    # Run calm CLI schema validation on the system topology
    if not args.skip_cli:
        system_topology = CALM_DIR / "novatrek-topology.json"
        if system_topology.exists():
            print(f"\n--- CALM CLI Schema Validation ---")
            passed, output = run_calm_cli(system_topology)
            if passed is None:
                print(f"  SKIP: {output}")
            elif passed:
                print(f"  PASS: calm validate found no schema errors")
            else:
                print(f"  FAIL: calm validate reported errors:")
                for line in output.split("\n"):
                    print(f"    {line}")
                cli_failures = 1

    print(f"\n{'='*60}")
    print(f"Validated {len(paths)} file(s): {total_errors} error(s), {total_warnings} warning(s)")

    if total_errors > 0 or cli_failures > 0:
        print("VALIDATION FAILED")
        sys.exit(1)
    else:
        print("ALL CHECKS PASSED")
        sys.exit(0)


if __name__ == "__main__":
    main()
