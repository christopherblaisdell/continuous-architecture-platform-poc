#!/usr/bin/env python3
"""
Pre-process PlantUML diagrams into search-optimized Markdown documents.

Each PUML file is a natural semantic unit (one diagram). This script extracts
structured metadata (services, endpoints, relationships, ADR references, etc.)
and generates enriched Markdown documents that combine a natural-language
description with the raw PUML source. These are then uploaded to blob storage
and indexed by Azure AI Search.

PUML syntax is terrible for search — "Svc -> Res : GET /reservations/{id}"
won't match "how does check-in validate reservations." This script bridges
that gap by translating diagram syntax into searchable text.

Diagram types handled:
  - Sequence diagrams (endpoint behavior, cross-service calls)
  - C4 Context diagrams (service integration maps)
  - ERD diagrams (database schema)
  - Event flow diagrams (Kafka event producers/consumers)
  - Topology diagrams (domain-level service maps)
  - Application C4 diagrams (app-to-service dependencies)

Usage:
    python3 scripts/puml-enricher.py                    # Enrich all PUMLs
    python3 scripts/puml-enricher.py --dry-run           # Preview output
    python3 scripts/puml-enricher.py --output-dir /tmp   # Custom output dir
    python3 scripts/puml-enricher.py --file portal/docs/microservices/puml/svc-check-in--post-check-ins.puml
"""

import argparse
import os
import re
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent

# Canonical PUML source directories (excludes site/, phases/, .venv/)
PUML_SOURCES = [
    "portal/docs/microservices/puml",
    "portal/docs/topology/puml",
    "portal/docs/applications/puml",
    "architecture/diagrams",
    "architecture/solutions",
]

DEFAULT_OUTPUT_DIR = WORKSPACE_ROOT / ".enriched-puml"


def classify_diagram(filename, content):
    """Classify a PUML file by diagram type."""
    name = filename.lower()
    if "--erd" in name:
        return "erd"
    if "--c4-context" in name or "c4_container" in content.lower():
        return "c4-context"
    if "event-flow" in name:
        return "event-flow"
    if "topology-" in name:
        return "topology"
    if "enterprise-c4" in name:
        return "enterprise-c4"
    if "@startuml" in content and ("participant" in content or "->" in content):
        return "sequence"
    return "other"


def extract_service_from_filename(filename):
    """Extract the primary service name from a PUML filename."""
    base = Path(filename).stem
    # svc-check-in--post-check-ins → svc-check-in
    if "--" in base:
        return base.split("--")[0]
    return base


def extract_endpoint_from_filename(filename):
    """Extract the endpoint hint from a PUML filename."""
    base = Path(filename).stem
    # svc-check-in--post-check-ins → post-check-ins
    if "--" in base:
        parts = base.split("--", 1)
        slug = parts[1]
        # Convert slug back to method + path hint
        for method in ["get", "post", "put", "patch", "delete"]:
            if slug.startswith(method + "-"):
                path_hint = slug[len(method) + 1:]
                return f"{method.upper()} /{path_hint.replace('-', '/')}"
        return slug
    return None


def extract_title(content):
    """Extract the title from PUML content."""
    match = re.search(r'^title\s+(.+?)(?:\n|\\n)', content, re.MULTILINE)
    if match:
        # Clean up multi-line titles
        title = match.group(1).strip()
        title = re.sub(r'\\n.*', '', title)  # Take first line of multi-line
        title = re.sub(r'<[^>]+>', '', title)  # Strip HTML tags
        return title.strip()
    return None


def extract_participants(content):
    """Extract participant declarations from sequence diagrams."""
    participants = []
    for match in re.finditer(
        r'participant\s+"([^"]+)"\s+as\s+(\w+)(?:\s+\[\[([^\]]+)\]\])?',
        content
    ):
        label, alias, link = match.group(1), match.group(2), match.group(3)
        svc = None
        if link:
            # Extract service name from link like /microservices/svc-check-in/
            svc_match = re.search(r'/microservices/(svc-[^/]+)', link)
            if svc_match:
                svc = svc_match.group(1)
        participants.append({"label": label, "alias": alias, "service": svc})
    return participants


def extract_api_calls(content):
    """Extract cross-service API calls from sequence diagrams."""
    calls = []
    # Match patterns like: Svc -> Res : [[link GET /reservations/{id}]]
    # or: Svc -> Res : GET /path
    for match in re.finditer(
        r'(\w+)\s+->+\s+(\w+)\s*:\s*(?:\[\[.*?\]\]\s*)?'
        r'((?:GET|POST|PUT|PATCH|DELETE)\s+/[^\n]*)',
        content
    ):
        caller, target, call = match.group(1), match.group(2), match.group(3)
        calls.append({"from": caller, "to": target, "call": call.strip()})

    # Also match [[/microservices/svc-X/#anchor VERB /path]] patterns
    for match in re.finditer(
        r'\[\[/microservices/(svc-[^\s#]+)[^\]]*\s+'
        r'(GET|POST|PUT|PATCH|DELETE)\s+(/[^\]]+)\]\]',
        content
    ):
        svc, method, path = match.group(1), match.group(2), match.group(3)
        calls.append({"to_service": svc, "call": f"{method} {path}"})

    return calls


def extract_relationships(content):
    """Extract Rel() declarations from C4 diagrams."""
    rels = []
    for match in re.finditer(
        r'Rel\((\w+),\s*(\w+),\s*"([^"]*)"(?:,\s*"([^"]*)")?\)',
        content
    ):
        source, target, desc, tech = (
            match.group(1), match.group(2),
            match.group(3), match.group(4) or ""
        )
        rels.append({
            "source": source, "target": target,
            "description": desc, "technology": tech
        })
    return rels


def extract_containers(content):
    """Extract Container/ContainerDb declarations from C4 diagrams."""
    containers = []
    for match in re.finditer(
        r'Container(?:Db)?\((\w+),\s*"([^"]*)"(?:,\s*"([^"]*)")?'
        r'(?:,\s*"([^"]*)")?',
        content
    ):
        alias, name, tech, desc = (
            match.group(1), match.group(2),
            match.group(3) or "", match.group(4) or ""
        )
        containers.append({
            "alias": alias, "name": name,
            "technology": tech, "description": desc
        })
    return containers


def extract_entities(content):
    """Extract entity declarations and fields from ERD diagrams."""
    entities = []
    current_entity = None
    fields = []
    for line in content.split("\n"):
        entity_match = re.match(r'entity\s+"([^"]+)"', line)
        if entity_match:
            if current_entity:
                entities.append({
                    "name": current_entity, "fields": list(fields)
                })
            current_entity = entity_match.group(1)
            fields = []
        elif current_entity:
            field_match = re.match(
                r'\s+[*\s]*(\w+)\s*:\s*(\w+(?:\([^)]*\))?)', line
            )
            if field_match:
                name, ftype = field_match.group(1), field_match.group(2)
                markers = []
                if "<<PK>>" in line:
                    markers.append("PK")
                if "<<FK" in line:
                    markers.append("FK")
                if "<<NN>>" in line:
                    markers.append("NOT NULL")
                if "<<UQ>>" in line:
                    markers.append("UNIQUE")
                fields.append({
                    "name": name, "type": ftype, "markers": markers
                })
    if current_entity:
        entities.append({"name": current_entity, "fields": list(fields)})
    return entities


def extract_fk_relationships(content):
    """Extract FK relationships from ERD diagrams."""
    rels = []
    for match in re.finditer(
        r'(\w+)\s+\}?\|?--\|?\|?\s+(\w+)\s*:\s*(\w+)',
        content
    ):
        child, parent, fk = match.group(1), match.group(2), match.group(3)
        rels.append({"child": child, "parent": parent, "fk_column": fk})
    return rels


def extract_events(content):
    """Extract event flow arrows from event-flow diagrams."""
    events = []
    for match in re.finditer(
        r'(\w+)\s+-->+\s+(\w+)\s*:\s*([^\n]+)', content
    ):
        source, target, event = (
            match.group(1), match.group(2), match.group(3).strip()
        )
        events.append({"source": source, "target": target, "event": event})
    return events


def extract_adr_references(content):
    """Extract ADR references from PUML content."""
    adrs = set()
    for match in re.finditer(r'ADR-(\d+)', content):
        adrs.add(f"ADR-{match.group(1)}")
    return sorted(adrs)


def extract_notes(content):
    """Extract note blocks from sequence diagrams."""
    notes = []
    for match in re.finditer(
        r'note\s+(?:right|left|over)\s+(?:of\s+)?\w+[^\n]*\n(.*?)end note',
        content, re.DOTALL
    ):
        text = match.group(1).strip()
        text = re.sub(r'\[\[.*?\]\]', '', text)  # Remove links
        if text:
            notes.append(text)
    # Also single-line notes
    for match in re.finditer(
        r'note\s+(?:right|left)\s+(?:of\s+)?\w+\s*:\s*(.+)', content
    ):
        text = match.group(1).strip()
        text = re.sub(r'\\n', ' ', text)
        if text:
            notes.append(text)
    return notes


def enrich_sequence(filepath, content):
    """Generate enriched document for a sequence diagram."""
    service = extract_service_from_filename(filepath)
    endpoint = extract_endpoint_from_filename(filepath)
    title = extract_title(content) or endpoint or Path(filepath).stem
    participants = extract_participants(content)
    api_calls = extract_api_calls(content)
    adrs = extract_adr_references(content)
    notes = extract_notes(content)

    lines = [f"# Sequence Diagram: {title}",
             f"**Service**: {service}",
             f"**Diagram type**: Endpoint sequence diagram"]
    if endpoint:
        lines.append(f"**Endpoint**: {endpoint}")
    lines.append(f"**Source file**: {filepath}")
    lines.append("")

    # Natural language description
    lines.append("## What This Diagram Shows")
    if endpoint:
        lines.append(
            f"This sequence diagram shows the internal behavior of "
            f"{service} when handling a {endpoint} request."
        )

    if participants:
        svc_names = [p["service"] or p["label"] for p in participants
                     if p["alias"] not in ("Client", "GW", "Cache", "DB")]
        if svc_names:
            lines.append(
                f"Services involved: {', '.join(svc_names)}."
            )

    lines.append("")

    if api_calls:
        lines.append("## Cross-Service API Calls")
        for call in api_calls:
            if "to_service" in call:
                lines.append(f"- Calls {call['to_service']}: {call['call']}")
            else:
                lines.append(
                    f"- {call['from']} calls {call['to']}: {call['call']}"
                )
        lines.append("")

    if adrs:
        lines.append("## Architecture Decision References")
        for adr in adrs:
            lines.append(f"- {adr}")
        lines.append("")

    if notes:
        lines.append("## Behavioral Notes")
        for note in notes:
            lines.append(f"- {note}")
        lines.append("")

    # Raw PUML for evidence
    lines.append("## PlantUML Source")
    lines.append("```plantuml")
    lines.append(content)
    lines.append("```")

    return "\n".join(lines)


def enrich_c4(filepath, content):
    """Generate enriched document for a C4 context diagram."""
    service = extract_service_from_filename(filepath)
    title = extract_title(content) or f"{service} Integration Context"
    containers = extract_containers(content)
    rels = extract_relationships(content)

    lines = [f"# C4 Integration Context: {title}",
             f"**Primary service**: {service}",
             f"**Diagram type**: C4 Container / Integration Context",
             f"**Source file**: {filepath}",
             ""]

    lines.append("## What This Diagram Shows")
    lines.append(
        f"This C4 context diagram shows all services that {service} "
        f"integrates with, including the direction and purpose of each "
        f"integration."
    )
    lines.append("")

    if containers:
        lines.append("## Components")
        for c in containers:
            desc = f" — {c['description']}" if c['description'] else ""
            tech = f" ({c['technology']})" if c['technology'] else ""
            lines.append(f"- **{c['name']}**{tech}{desc}")
        lines.append("")

    if rels:
        lines.append("## Relationships")
        for r in rels:
            tech = f" via {r['technology']}" if r['technology'] else ""
            lines.append(
                f"- {r['source']} → {r['target']}: "
                f"{r['description']}{tech}"
            )
        lines.append("")

    lines.append("## PlantUML Source")
    lines.append("```plantuml")
    lines.append(content)
    lines.append("```")

    return "\n".join(lines)


def enrich_erd(filepath, content):
    """Generate enriched document for an ERD diagram."""
    service = extract_service_from_filename(filepath)
    title = extract_title(content) or f"{service} Entity Relationship Diagram"
    entities = extract_entities(content)
    fk_rels = extract_fk_relationships(content)

    # Extract schema/DB info from title
    schema_info = ""
    schema_match = re.search(r'schema:\s*(\w+)\s*\((\d+)\s*tables?\)', content)
    if schema_match:
        schema_info = (f"Schema: {schema_match.group(1)}, "
                       f"{schema_match.group(2)} tables")

    lines = [f"# Database Schema: {title}",
             f"**Service**: {service}",
             f"**Diagram type**: Entity Relationship Diagram (ERD)"]
    if schema_info:
        lines.append(f"**{schema_info}**")
    lines.append(f"**Source file**: {filepath}")
    lines.append("")

    lines.append("## What This Diagram Shows")
    lines.append(
        f"This ERD shows the database schema for {service}, including "
        f"all tables, columns, types, and foreign key relationships."
    )
    lines.append("")

    if entities:
        lines.append("## Tables and Columns")
        for entity in entities:
            lines.append(f"### Table: {entity['name']}")
            for field in entity["fields"]:
                markers = ""
                if field["markers"]:
                    markers = f" [{', '.join(field['markers'])}]"
                lines.append(
                    f"- `{field['name']}`: {field['type']}{markers}"
                )
            lines.append("")

    if fk_rels:
        lines.append("## Foreign Key Relationships")
        for rel in fk_rels:
            lines.append(
                f"- {rel['child']}.{rel['fk_column']} → {rel['parent']}"
            )
        lines.append("")

    lines.append("## PlantUML Source")
    lines.append("```plantuml")
    lines.append(content)
    lines.append("```")

    return "\n".join(lines)


def enrich_event_flow(filepath, content):
    """Generate enriched document for an event flow diagram."""
    title = extract_title(content) or Path(filepath).stem
    events = extract_events(content)

    # Extract domain from filename: event-flow-operations → Operations
    domain = Path(filepath).stem.replace("event-flow-", "").replace("-", " ").title()

    lines = [f"# Event Flow: {title}",
             f"**Domain**: {domain}",
             f"**Diagram type**: Kafka event flow diagram",
             f"**Source file**: {filepath}",
             ""]

    lines.append("## What This Diagram Shows")
    lines.append(
        f"This event flow diagram shows Kafka event producers and consumers "
        f"in the {domain} domain, including which events are published and "
        f"which services subscribe to them."
    )
    lines.append("")

    # Group events by type
    produced = {}
    consumed = {}
    for evt in events:
        if evt["source"].startswith("p_") or "kafka" not in evt["source"]:
            produced.setdefault(evt["source"], []).append(evt["event"])
        if evt["target"].startswith("c_") or "kafka" not in evt["target"]:
            consumed.setdefault(evt["target"], []).append(evt["event"])

    if produced:
        lines.append("## Events Produced")
        for producer, evts in produced.items():
            name = producer.replace("p_", "").replace("_", "-")
            for e in evts:
                lines.append(f"- **{name}** produces: `{e}`")
        lines.append("")

    if consumed:
        lines.append("## Events Consumed")
        for consumer, evts in consumed.items():
            name = consumer.replace("c_", "").replace("_", "-")
            for e in evts:
                lines.append(f"- **{name}** consumes: `{e}`")
        lines.append("")

    lines.append("## PlantUML Source")
    lines.append("```plantuml")
    lines.append(content)
    lines.append("```")

    return "\n".join(lines)


def enrich_topology(filepath, content):
    """Generate enriched document for a topology diagram."""
    title = extract_title(content) or Path(filepath).stem
    containers = extract_containers(content)
    rels = extract_relationships(content)

    domain = Path(filepath).stem.replace("topology-", "").replace("-", " ").title()

    lines = [f"# Service Topology: {title}",
             f"**Domain**: {domain}",
             f"**Diagram type**: Domain-level service topology",
             f"**Source file**: {filepath}",
             ""]

    lines.append("## What This Diagram Shows")
    lines.append(
        f"This topology diagram shows the service-level architecture "
        f"of the {domain} domain, including all services grouped by "
        f"bounded context and their inter-service communication paths."
    )
    lines.append("")

    if containers:
        lines.append("## Services")
        for c in containers:
            desc = f" — {c['description']}" if c['description'] else ""
            lines.append(f"- **{c['name']}**{desc}")
        lines.append("")

    if rels:
        lines.append("## Communication Paths")
        for r in rels:
            tech = f" ({r['technology']})" if r['technology'] else ""
            lines.append(
                f"- {r['source']} → {r['target']}: "
                f"{r['description']}{tech}"
            )
        lines.append("")

    lines.append("## PlantUML Source")
    lines.append("```plantuml")
    lines.append(content)
    lines.append("```")

    return "\n".join(lines)


def enrich_generic(filepath, content):
    """Fallback enrichment for unclassified diagrams."""
    title = extract_title(content) or Path(filepath).stem
    adrs = extract_adr_references(content)

    lines = [f"# Architecture Diagram: {title}",
             f"**Diagram type**: PlantUML diagram",
             f"**Source file**: {filepath}",
             ""]

    if adrs:
        lines.append("## Architecture Decision References")
        for adr in adrs:
            lines.append(f"- {adr}")
        lines.append("")

    lines.append("## PlantUML Source")
    lines.append("```plantuml")
    lines.append(content)
    lines.append("```")

    return "\n".join(lines)


def enrich_file(filepath, content):
    """Route to the appropriate enricher based on diagram type."""
    filename = Path(filepath).name
    diagram_type = classify_diagram(filename, content)

    if diagram_type == "sequence":
        return enrich_sequence(filepath, content), diagram_type
    elif diagram_type == "c4-context":
        return enrich_c4(filepath, content), diagram_type
    elif diagram_type == "erd":
        return enrich_erd(filepath, content), diagram_type
    elif diagram_type == "event-flow":
        return enrich_event_flow(filepath, content), diagram_type
    elif diagram_type == "topology":
        return enrich_topology(filepath, content), diagram_type
    elif diagram_type == "enterprise-c4":
        return enrich_c4(filepath, content), diagram_type
    else:
        return enrich_generic(filepath, content), diagram_type


def find_puml_files():
    """Find all canonical PUML files."""
    files = []
    for source_dir in PUML_SOURCES:
        source_path = WORKSPACE_ROOT / source_dir
        if source_path.exists():
            for puml in source_path.rglob("*.puml"):
                # Skip theme files
                if puml.name == "theme.puml":
                    continue
                # Use relative path from workspace root
                rel_path = str(puml.relative_to(WORKSPACE_ROOT))
                files.append((rel_path, puml))
    return sorted(files, key=lambda x: x[0])


def main():
    parser = argparse.ArgumentParser(
        description="Pre-process PlantUML into search-optimized documents"
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview without writing files")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR,
                        help="Output directory for enriched files")
    parser.add_argument("--file", type=str,
                        help="Process a single PUML file")
    parser.add_argument("--stats", action="store_true",
                        help="Show statistics only")
    args = parser.parse_args()

    if args.file:
        filepath = Path(args.file)
        if not filepath.is_absolute():
            filepath = WORKSPACE_ROOT / filepath
        content = filepath.read_text(encoding="utf-8")
        rel_path = str(filepath.relative_to(WORKSPACE_ROOT))
        enriched, dtype = enrich_file(rel_path, content)
        print(f"Type: {dtype}")
        print(f"Output length: {len(enriched)} chars")
        print("---")
        print(enriched[:2000])
        if len(enriched) > 2000:
            print(f"\n... ({len(enriched) - 2000} chars truncated)")
        return

    files = find_puml_files()
    print(f"Found {len(files)} canonical PUML files")

    if args.stats:
        type_counts = {}
        total_input = 0
        total_output = 0
        for rel_path, abs_path in files:
            content = abs_path.read_text(encoding="utf-8")
            total_input += len(content)
            enriched, dtype = enrich_file(rel_path, content)
            total_output += len(enriched)
            type_counts[dtype] = type_counts.get(dtype, 0) + 1
        print(f"\nDiagram types:")
        for dtype, count in sorted(type_counts.items(),
                                    key=lambda x: -x[1]):
            print(f"  {dtype}: {count}")
        print(f"\nTotal input:  {total_input:,} chars ({total_input/1024:.0f} KB)")
        print(f"Total output: {total_output:,} chars ({total_output/1024:.0f} KB)")
        print(f"Enrichment ratio: {total_output/total_input:.1f}x")
        return

    # Process all files
    output_dir = args.output_dir
    if not args.dry_run:
        output_dir.mkdir(parents=True, exist_ok=True)

    type_counts = {}
    for rel_path, abs_path in files:
        content = abs_path.read_text(encoding="utf-8")
        enriched, dtype = enrich_file(rel_path, content)
        type_counts[dtype] = type_counts.get(dtype, 0) + 1

        # Output filename: flatten path with double-dashes
        out_name = rel_path.replace("/", "--").replace(".puml", ".md")
        out_path = output_dir / out_name

        if args.dry_run:
            print(f"  [{dtype:12}] {rel_path} → {out_name} "
                  f"({len(enriched)} chars)")
        else:
            out_path.write_text(enriched, encoding="utf-8")

    print(f"\nProcessed {len(files)} files:")
    for dtype, count in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"  {dtype}: {count}")

    if not args.dry_run:
        print(f"\nOutput directory: {output_dir}")
    else:
        print("\n(dry run — no files written)")


if __name__ == "__main__":
    main()
