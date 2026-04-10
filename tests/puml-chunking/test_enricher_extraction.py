#!/usr/bin/env python3
"""
Test script for validating puml-enricher.py extraction on PUML chunking test fixtures.

Runs puml-enricher.py --file on each test fixture, then validates the enriched
output against expected extraction results defined in tests/puml-chunking/expected/.

Usage:
    python3 tests/puml-chunking/test_enricher_extraction.py
    python3 tests/puml-chunking/test_enricher_extraction.py --verbose
    python3 tests/puml-chunking/test_enricher_extraction.py --fixture NTK-10020
"""

import argparse
import re
import sys
import yaml
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
FIXTURES_DIR = WORKSPACE_ROOT / "tests" / "puml-chunking" / "fixtures"
EXPECTED_DIR = WORKSPACE_ROOT / "tests" / "puml-chunking" / "expected"

# Import enricher functions directly
sys.path.insert(0, str(WORKSPACE_ROOT / "scripts"))
from importlib import import_module
puml_enricher = import_module("puml-enricher")


def load_expected():
    """Load all expected extraction YAML files."""
    expected = {}
    for yaml_file in EXPECTED_DIR.glob("*.yaml"):
        with open(yaml_file, encoding="utf-8") as f:
            data = yaml.safe_load(f)
            if data:
                expected.update(data)
    return expected


def run_enricher(fixture_path):
    """Run puml-enricher on a single fixture file by calling enrich_file directly."""
    content = fixture_path.read_text(encoding="utf-8")
    rel_path = str(fixture_path.relative_to(WORKSPACE_ROOT))
    enriched, dtype = puml_enricher.enrich_file(rel_path, content)
    return enriched, dtype, None


def validate_classification(enriched_content, expected_class):
    """Check if the enricher classified the diagram correctly."""
    type_patterns = {
        "sequence": r"sequence diagram|endpoint sequence",
        "c4-context": r"C4|integration context|container|component",
        "erd": r"entity|data model|ERD",
        "event-flow": r"event flow",
        "topology": r"topology",
        "other": r"diagram",
    }
    pattern = type_patterns.get(expected_class, r"diagram")
    return bool(re.search(pattern, enriched_content, re.IGNORECASE))


def validate_participants(enriched_content, spec):
    """Validate participant extraction."""
    errors = []
    if "participant_aliases_must_include" in spec:
        for alias in spec["participant_aliases_must_include"]:
            if alias not in enriched_content.lower():
                errors.append(f"Missing participant alias: {alias}")
    if "services_must_include" in spec:
        for svc in spec["services_must_include"]:
            if svc not in enriched_content:
                errors.append(f"Missing service: {svc}")
    if "min_participants" in spec:
        # Count participant declarations in the embedded PUML source
        count = len(re.findall(r'participant\s+"', enriched_content))
        if count < spec["min_participants"]:
            errors.append(
                f"Expected >= {spec['min_participants']} participants, found {count}"
            )
    return errors


def validate_api_calls(enriched_content, spec):
    """Validate API call extraction."""
    errors = []
    if "min_api_calls" in spec:
        call_count = len(re.findall(
            r'(?:GET|POST|PUT|PATCH|DELETE)\s+/', enriched_content
        ))
        # Divide by 2 since calls appear in both enriched section and raw PUML
        effective = call_count // 2 if call_count > spec["min_api_calls"] else call_count
        if effective < spec["min_api_calls"]:
            errors.append(
                f"Expected >= {spec['min_api_calls']} API calls, found ~{effective}"
            )
    if "api_calls_must_include" in spec:
        for call in spec["api_calls_must_include"]:
            if call not in enriched_content:
                errors.append(f"Missing API call: {call}")
    return errors


def validate_adr_references(enriched_content, spec):
    """Validate ADR reference extraction."""
    errors = []
    if "adr_references" in spec:
        for adr in spec["adr_references"]:
            if adr not in enriched_content:
                errors.append(f"Missing ADR reference: {adr}")
    return errors


def validate_notes(enriched_content, spec):
    """Validate note extraction."""
    errors = []
    if "min_notes" in spec:
        # Count notes in the Behavioral Notes section
        notes_section = re.search(
            r'## Behavioral Notes\n(.*?)(?=\n## |\Z)',
            enriched_content, re.DOTALL
        )
        if notes_section:
            note_count = notes_section.group(1).count("- ")
            if note_count < spec["min_notes"]:
                errors.append(
                    f"Expected >= {spec['min_notes']} notes, found {note_count}"
                )
        else:
            errors.append("No 'Behavioral Notes' section found")
    return errors


def validate_containers(enriched_content, spec):
    """Validate C4 container extraction."""
    errors = []
    if "containers_must_include" in spec:
        for container in spec["containers_must_include"]:
            if container not in enriched_content:
                errors.append(f"Missing container: {container}")
    if "min_containers" in spec:
        count = len(re.findall(r'Container(?:Db|Queue)?\(', enriched_content))
        if count < spec["min_containers"]:
            errors.append(
                f"Expected >= {spec['min_containers']} containers, found {count}"
            )
    return errors


def validate_relationships(enriched_content, spec):
    """Validate C4 relationship extraction."""
    errors = []
    if "min_relationships" in spec:
        count = len(re.findall(r'Rel\(', enriched_content))
        if count < spec["min_relationships"]:
            errors.append(
                f"Expected >= {spec['min_relationships']} relationships, found {count}"
            )
    return errors


def validate_entities(enriched_content, spec):
    """Validate ERD entity extraction."""
    errors = []
    if "entities_must_include" in spec:
        for entity in spec["entities_must_include"]:
            if entity not in enriched_content:
                errors.append(f"Missing entity: {entity}")
    if "min_entities" in spec:
        count = len(re.findall(r'entity\s+"', enriched_content))
        if count < spec["min_entities"]:
            errors.append(
                f"Expected >= {spec['min_entities']} entities, found {count}"
            )
    return errors


def validate_fixture(name, enriched_content, spec):
    """Run all validations for a single fixture."""
    results = {"name": name, "passed": 0, "failed": 0, "errors": []}

    # Classification
    if "classification" in spec:
        if validate_classification(enriched_content, spec["classification"]):
            results["passed"] += 1
        else:
            results["failed"] += 1
            results["errors"].append(
                f"Classification mismatch: expected {spec['classification']}"
            )

    # Title
    if spec.get("has_title"):
        if re.search(r'^#\s+.+', enriched_content, re.MULTILINE):
            results["passed"] += 1
        else:
            results["failed"] += 1
            results["errors"].append("No title found in enriched output")

    # Participants (sequence diagrams)
    participant_errors = validate_participants(enriched_content, spec)
    if participant_errors:
        results["failed"] += len(participant_errors)
        results["errors"].extend(participant_errors)
    else:
        results["passed"] += 1

    # API calls
    api_errors = validate_api_calls(enriched_content, spec)
    if api_errors:
        results["failed"] += len(api_errors)
        results["errors"].extend(api_errors)
    elif "min_api_calls" in spec or "api_calls_must_include" in spec:
        results["passed"] += 1

    # ADR references
    adr_errors = validate_adr_references(enriched_content, spec)
    if adr_errors:
        results["failed"] += len(adr_errors)
        results["errors"].extend(adr_errors)
    elif "adr_references" in spec:
        results["passed"] += 1

    # Notes
    note_errors = validate_notes(enriched_content, spec)
    if note_errors:
        results["failed"] += len(note_errors)
        results["errors"].extend(note_errors)
    elif "min_notes" in spec:
        results["passed"] += 1

    # Containers (C4 diagrams)
    container_errors = validate_containers(enriched_content, spec)
    if container_errors:
        results["failed"] += len(container_errors)
        results["errors"].extend(container_errors)
    elif "min_containers" in spec:
        results["passed"] += 1

    # Relationships (C4 diagrams)
    rel_errors = validate_relationships(enriched_content, spec)
    if rel_errors:
        results["failed"] += len(rel_errors)
        results["errors"].extend(rel_errors)
    elif "min_relationships" in spec:
        results["passed"] += 1

    # Entities (ERD diagrams)
    entity_errors = validate_entities(enriched_content, spec)
    if entity_errors:
        results["failed"] += len(entity_errors)
        results["errors"].extend(entity_errors)
    elif "min_entities" in spec:
        results["passed"] += 1

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Validate puml-enricher extraction on test fixtures"
    )
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Show detailed output for each fixture")
    parser.add_argument("--fixture", type=str,
                        help="Run only fixtures matching this pattern")
    args = parser.parse_args()

    # Load expected results
    expected = load_expected()
    if not expected:
        print("ERROR: No expected results found in tests/puml-chunking/expected/")
        sys.exit(1)

    # Find fixtures
    fixtures = sorted(FIXTURES_DIR.glob("*.puml"))
    if args.fixture:
        fixtures = [f for f in fixtures if args.fixture in f.stem]

    if not fixtures:
        print("ERROR: No fixtures found in tests/puml-chunking/fixtures/")
        sys.exit(1)

    print(f"Running enricher validation on {len(fixtures)} fixtures...")
    print(f"Expected specs loaded: {len(expected)}")
    print("=" * 70)

    total_passed = 0
    total_failed = 0
    total_skipped = 0
    all_results = []

    for fixture in fixtures:
        stem = fixture.stem
        spec = expected.get(stem)

        if spec is None:
            if args.verbose:
                print(f"  SKIP  {stem} (no expected spec)")
            total_skipped += 1
            continue

        # Run enricher
        enriched, _dtype, error = run_enricher(fixture)
        if error:
            print(f"  ERROR {stem}: enricher failed — {error}")
            total_failed += 1
            continue

        if enriched is None:
            print(f"  ERROR {stem}: no enriched output produced")
            total_failed += 1
            continue

        # Validate
        results = validate_fixture(stem, enriched, spec)
        all_results.append(results)
        total_passed += results["passed"]
        total_failed += results["failed"]

        # Print result
        status = "PASS" if results["failed"] == 0 else "FAIL"
        print(f"  [{status}] {stem} "
              f"({results['passed']} passed, {results['failed']} failed)")

        if args.verbose and results["errors"]:
            for err in results["errors"]:
                print(f"         - {err}")

    print("=" * 70)
    print(f"Total: {total_passed} passed, {total_failed} failed, "
          f"{total_skipped} skipped")

    if total_failed > 0:
        print("\nFailed fixtures:")
        for r in all_results:
            if r["failed"] > 0:
                print(f"  {r['name']}:")
                for err in r["errors"]:
                    print(f"    - {err}")
        sys.exit(1)
    else:
        print("\nAll validations passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()
