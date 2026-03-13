#!/usr/bin/env python3
"""Validate CALM topology documents against NovaTrek architecture patterns.

Checks the generated CALM topology for architecture rule violations that
would normally require manual PR review. This is a lightweight Python
validator — a stepping stone to the full CALM CLI (`calm validate`).

Usage:
    python3 architecture/scripts/validate-calm.py                              # validate all
    python3 architecture/scripts/validate-calm.py architecture/calm/domains/operations.json
    python3 architecture/scripts/validate-calm.py --patterns architecture/calm/patterns/

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
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CALM_DIR = ROOT / "architecture" / "calm"


def load_calm(path):
    with open(path) as f:
        return json.load(f)


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
        if rel.get("relationship-type") == "connects" and rel["parties"]["target"] in db_nodes:
            target = rel["parties"]["target"]
            db_connections.setdefault(target, []).append(rel["parties"]["source"])

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
            src = rel["parties"]["source"]
            tgt = rel["parties"]["target"]
            if src in service_ids and tgt in service_ids:
                result.error("api-mediated-access", f"JDBC connection between services: {src} -> {tgt} (must use API)")


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
        src = rel["parties"]["source"]
        tgt = rel["parties"]["target"]
        if src not in node_ids:
            result.error("relationship-integrity", f"Relationship '{rel['unique-id']}' references unknown source: '{src}'")
        if tgt not in node_ids:
            result.error("relationship-integrity", f"Relationship '{rel['unique-id']}' references unknown target: '{tgt}'")


def validate_no_orphan_services(calm, result):
    """Rule 5: Every service should participate in at least one relationship."""
    service_ids = {n["unique-id"] for n in calm.get("nodes", []) if n.get("node-type") == "service"}
    connected = set()

    for rel in calm.get("relationships", []):
        connected.add(rel["parties"]["source"])
        connected.add(rel["parties"]["target"])

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


def main():
    parser = argparse.ArgumentParser(description="Validate CALM topology against NovaTrek architecture patterns")
    parser.add_argument("files", nargs="*", help="CALM JSON files to validate (default: all in architecture/calm/)")
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

    print(f"\n{'='*60}")
    print(f"Validated {len(paths)} file(s): {total_errors} error(s), {total_warnings} warning(s)")

    if total_errors > 0:
        print("VALIDATION FAILED")
        sys.exit(1)
    else:
        print("ALL CHECKS PASSED")
        sys.exit(0)


if __name__ == "__main__":
    main()
