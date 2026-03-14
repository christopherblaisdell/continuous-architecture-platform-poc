#!/usr/bin/env python3
"""Generate a CALM (Common Architecture Language Model) topology document
from NovaTrek's existing metadata YAML files.

Usage:
    python3 scripts/generate-calm.py                        # all domains
    python3 scripts/generate-calm.py --domain Operations    # single domain
    python3 scripts/generate-calm.py --output path/out.json # custom output

Reads:
    architecture/metadata/domains.yaml
    architecture/metadata/data-stores.yaml
    architecture/metadata/cross-service-calls.yaml
    architecture/metadata/events.yaml
    architecture/metadata/actors.yaml
    architecture/specs/*.yaml  (OpenAPI — for interface extraction)

Produces:
    architecture/calm/novatrek-topology.json  (or per-domain file)
"""

import argparse
import json
import os
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
META = ROOT / "architecture" / "metadata"
SPECS = ROOT / "architecture" / "specs"


def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)


def load_domains():
    return load_yaml(META / "domains.yaml")


def load_data_stores():
    return load_yaml(META / "data-stores.yaml")


def load_cross_service_calls():
    return load_yaml(META / "cross-service-calls.yaml")


def load_events():
    return load_yaml(META / "events.yaml")


def load_actors():
    return load_yaml(META / "actors.yaml")


def load_pci():
    pci_path = META / "pci.yaml"
    if pci_path.exists():
        return load_yaml(pci_path)
    return {}


def load_openapi_spec(svc_name):
    spec_path = SPECS / f"{svc_name}.yaml"
    if spec_path.exists():
        return load_yaml(spec_path)
    return None


# --- CALM node builders ---

def domain_for_service(domains, svc):
    for domain_name, domain_data in domains.items():
        if svc in domain_data.get("services", []):
            return domain_name
    return "Unknown"


def team_for_domain(domain_name):
    team_map = {
        "Operations": "NovaTrek Operations Team",
        "Guest Identity": "Guest Experience Team",
        "Booking": "Booking Platform Team",
        "Product Catalog": "Product Team",
        "Safety": "Safety and Compliance Team",
        "Logistics": "Logistics Team",
        "Guide Management": "Guide Operations Team",
        "External": "Integration Team",
        "Support": "Support Services Team",
        "Analytics": "Data and Analytics Team",
        "Communication": "Communication Team",
    }
    return team_map.get(domain_name, f"{domain_name} Team")


def build_service_node(svc, domains, data_stores, events_data, pci_services=None):
    domain = domain_for_service(domains, svc)
    spec = load_openapi_spec(svc)
    pci_services = pci_services or set()

    interfaces = []

    # Extract REST interfaces from OpenAPI spec
    if spec and "paths" in spec:
        for path, methods in spec["paths"].items():
            for method in methods:
                if method in ("get", "post", "put", "patch", "delete"):
                    summary = ""
                    if isinstance(methods[method], dict):
                        summary = methods[method].get("summary", "")
                    interfaces.append({
                        "unique-id": f"{svc}-api-{method}-{path.replace('/', '-').strip('-')}",
                        "type": "path",
                        "path": path,
                        "metadata": {"method": method.upper(), "summary": summary},
                    })

    # Extract event interfaces (produced events)
    if events_data:
        for event_key, event in events_data.items():
            if event.get("producer") == svc:
                interfaces.append({
                    "unique-id": f"{svc}-event-{event_key.replace('.', '-')}",
                    "type": "path",
                    "path": event["channel"],
                    "metadata": {"protocol": "Kafka", "role": "producer"},
                })

    description = ""
    if spec and "info" in spec:
        description = spec["info"].get("description", "").strip().split("\n")[0]

    metadata = {
        "domain": domain,
        "team": team_for_domain(domain),
    }
    if svc in pci_services:
        metadata["pci-in-scope"] = True

    return {
        "unique-id": svc,
        "node-type": "service",
        "name": svc.replace("svc-", "").replace("-", " ").title() + " Service",
        "description": description or f"NovaTrek {svc} microservice",
        "interfaces": interfaces,
        "metadata": metadata,
    }


def build_database_node(svc, ds_config, domains):
    domain = domain_for_service(domains, svc)
    engine = ds_config.get("engine", "Unknown")
    schema = ds_config.get("schema", svc.replace("svc-", ""))
    tables = ds_config.get("tables", [])

    return {
        "unique-id": f"{svc}-db",
        "node-type": "database",
        "name": f"{svc.replace('svc-', '').replace('-', ' ').title()} Database",
        "description": f"{engine} database for {svc} ({schema} schema)",
        "interfaces": [
            {
                "unique-id": f"{svc}-db-jdbc",
                "type": "host-port",
                "metadata": {"engine": engine, "schema": schema},
            }
        ],
        "metadata": {
            "domain": domain,
            "engine": engine,
            "tables": tables,
        },
    }


def build_actor_node(name, actor_data):
    actor_type = actor_data.get("type", "Human")
    node_type = "actor" if actor_type == "Human" else "system"

    node = {
        "unique-id": name.lower().replace(" ", "-"),
        "node-type": node_type,
        "name": name,
        "description": actor_data.get("description", ""),
        "interfaces": [],
        "metadata": {
            "actor-type": actor_type,
            "domain": actor_data.get("domain", "External"),
        },
    }
    if actor_data.get("technology"):
        node["metadata"]["technology"] = actor_data["technology"]
    return node


# --- CALM relationship builders ---

def build_service_to_db_relationship(svc):
    return {
        "unique-id": f"rel-{svc}-to-db",
        "relationship-type": "connects",
        "parties": {
            "source": svc,
            "target": f"{svc}-db",
        },
        "protocol": "JDBC",
        "metadata": {"description": f"{svc} connects to its database"},
    }


def build_cross_service_relationships(cross_calls):
    relationships = []
    # Map display labels to service/system names
    label_to_svc = {
        # Internal services — full names
        "Reservations": "svc-reservations",
        "Guest Profiles": "svc-guest-profiles",
        "Trip Catalog": "svc-trip-catalog",
        "Safety Compliance": "svc-safety-compliance",
        "Notifications": "svc-notifications",
        "Gear Inventory": "svc-gear-inventory",
        "Scheduling Orchestrator": "svc-scheduling-orchestrator",
        "Check-In": "svc-check-in",
        "Guide Management": "svc-guide-management",
        "Trail Management": "svc-trail-management",
        "Transport Logistics": "svc-transport-logistics",
        "Payments": "svc-payments",
        "Loyalty Rewards": "svc-loyalty-rewards",
        "Media Gallery": "svc-media-gallery",
        "Analytics": "svc-analytics",
        "Weather": "svc-weather",
        "Location Services": "svc-location-services",
        "Partner Integrations": "svc-partner-integrations",
        "Inventory Procurement": "svc-inventory-procurement",
        "Emergency Response": "svc-emergency-response",
        "Reviews": "svc-reviews",
        "Wildlife Tracking": "svc-wildlife-tracking",
        # Internal services — abbreviated labels from cross-service-calls.yaml
        "Guide Mgmt": "svc-guide-management",
        "Trail Mgmt": "svc-trail-management",
        "Weather Svc": "svc-weather",
        "Location Svc": "svc-location-services",
        "Payments Svc": "svc-payments",
        # External systems (not NovaTrek services)
        "Event Bus": "ext-kafka-broker",
        "DocuSign API": "ext-docusign",
        "IDVerify API": "ext-idverify",
        "SendGrid API": "ext-sendgrid",
        "Twilio API": "ext-twilio",
        "Firebase Cloud Messaging": "ext-firebase-fcm",
        "Fraud Detection API": "ext-fraud-detection",
        "Payment Gateway": "ext-payment-gateway",
        "Object Store": "ext-object-store",
        "Google Maps Platform": "ext-google-maps",
        "OpenWeather API": "ext-openweather",
        "Snowflake Data Cloud": "ext-snowflake",
    }

    for source_svc, endpoints in (cross_calls or {}).items():
        for endpoint, calls in (endpoints or {}).items():
            for call in (calls or []):
                label = call.get("label", "")
                target_svc = label_to_svc.get(label, label.lower().replace(" ", "-"))
                if not target_svc.startswith("svc-") and not target_svc.startswith("ext-"):
                    target_svc = f"svc-{target_svc}"

                target_info = call.get("target", {})
                is_async = call.get("async", False)

                rel_id = f"rel-{source_svc}-{endpoint.replace(' ', '-').replace('/', '-')}-to-{target_svc}".lower()

                relationships.append({
                    "unique-id": rel_id,
                    "relationship-type": "interacts",
                    "parties": {
                        "source": source_svc,
                        "target": target_svc,
                    },
                    "protocol": "Kafka" if is_async else "HTTPS",
                    "metadata": {
                        "source-endpoint": endpoint,
                        "target-endpoint": f"{target_info.get('method', 'GET')} {target_info.get('path', '')}",
                        "action": call.get("action", ""),
                        "async": is_async,
                    },
                })
    return relationships


def build_event_relationships(events_data):
    relationships = []
    if not events_data:
        return relationships

    for event_key, event in events_data.items():
        producer = event.get("producer", "")
        for consumer in event.get("consumers", []):
            rel_id = f"rel-event-{event_key.replace('.', '-')}-{producer}-to-{consumer}"
            relationships.append({
                "unique-id": rel_id,
                "relationship-type": "interacts",
                "parties": {
                    "source": producer,
                    "target": consumer,
                },
                "protocol": "Kafka",
                "metadata": {
                    "event": event_key,
                    "channel": event.get("channel", ""),
                    "summary": event.get("summary", ""),
                    "async": True,
                },
            })
    return relationships


def build_actor_relationships(actors_data):
    relationships = []
    if not actors_data:
        return relationships

    for actor_name, actor_data in actors_data.items():
        actor_id = actor_name.lower().replace(" ", "-")
        for target in actor_data.get("interacts_with", []):
            rel_id = f"rel-{actor_id}-to-{target}"
            relationships.append({
                "unique-id": rel_id,
                "relationship-type": "interacts",
                "parties": {
                    "source": actor_id,
                    "target": target,
                },
                "protocol": "HTTPS",
                "metadata": {"description": f"{actor_name} uses {target}"},
            })
    return relationships


def filter_by_domain(nodes, relationships, domains, target_domain):
    """Filter nodes and relationships to a single domain."""
    domain_services = set()
    for domain_name, domain_data in domains.items():
        if domain_name == target_domain:
            domain_services = set(domain_data.get("services", []))
            break

    if not domain_services:
        print(f"ERROR: Domain '{target_domain}' not found.", file=sys.stderr)
        print(f"Available domains: {', '.join(domains.keys())}", file=sys.stderr)
        sys.exit(1)

    # Include service nodes, their databases, and any actors that interact with them
    domain_node_ids = set()
    filtered_nodes = []
    for node in nodes:
        nid = node["unique-id"]
        if nid in domain_services:
            domain_node_ids.add(nid)
            filtered_nodes.append(node)
        elif nid.replace("-db", "") in domain_services and node["node-type"] == "database":
            domain_node_ids.add(nid)
            filtered_nodes.append(node)

    # Include relationships where at least one party is in the domain
    filtered_rels = []
    external_node_ids = set()
    for rel in relationships:
        src = rel["parties"]["source"]
        tgt = rel["parties"]["target"]
        if src in domain_node_ids or tgt in domain_node_ids:
            filtered_rels.append(rel)
            if src not in domain_node_ids:
                external_node_ids.add(src)
            if tgt not in domain_node_ids:
                external_node_ids.add(tgt)

    # Pull in external nodes referenced by relationships
    for node in nodes:
        if node["unique-id"] in external_node_ids and node not in filtered_nodes:
            filtered_nodes.append(node)

    return filtered_nodes, filtered_rels


def generate_calm(domain_filter=None):
    """Generate the full CALM topology document."""
    domains = load_domains()
    data_stores = load_data_stores()
    cross_calls = load_cross_service_calls()
    events_data = load_events()
    actors_data = load_actors()
    pci_data = load_pci()
    pci_services = set(pci_data.get("services", []))

    nodes = []
    relationships = []

    # Build service nodes and database nodes
    all_services = set()
    for domain_name, domain_data in domains.items():
        for svc in domain_data.get("services", []):
            all_services.add(svc)
            nodes.append(build_service_node(svc, domains, data_stores, events_data, pci_services=pci_services))

            # Add database node if service has a data store
            if data_stores and svc in data_stores:
                nodes.append(build_database_node(svc, data_stores[svc], domains))
                relationships.append(build_service_to_db_relationship(svc))

    # Build actor nodes
    if actors_data:
        for actor_name, actor_data in actors_data.items():
            nodes.append(build_actor_node(actor_name, actor_data))
        relationships.extend(build_actor_relationships(actors_data))

    # Build cross-service call relationships
    relationships.extend(build_cross_service_relationships(cross_calls))

    # Build event-driven relationships
    relationships.extend(build_event_relationships(events_data))

    # Collect external system IDs referenced in relationships but not yet nodes
    node_ids = {n["unique-id"] for n in nodes}
    ext_systems = set()
    for rel in relationships:
        for party in (rel["parties"]["source"], rel["parties"]["target"]):
            if party.startswith("ext-") and party not in node_ids:
                ext_systems.add(party)

    # Build external system nodes
    ext_descriptions = {
        "ext-kafka-broker": ("Kafka Event Bus", "Apache Kafka message broker for asynchronous event-driven integration"),
        "ext-docusign": ("DocuSign API", "Electronic signature platform for waiver signing"),
        "ext-idverify": ("IDVerify API", "Third-party identity verification service"),
        "ext-sendgrid": ("SendGrid API", "Email delivery platform"),
        "ext-twilio": ("Twilio API", "SMS and voice communication platform"),
        "ext-firebase-fcm": ("Firebase Cloud Messaging", "Push notification delivery for mobile apps"),
        "ext-fraud-detection": ("Fraud Detection API", "Third-party payment fraud screening"),
        "ext-payment-gateway": ("Payment Gateway", "PCI-compliant payment processing gateway"),
        "ext-object-store": ("Object Store", "Cloud blob storage for media assets"),
        "ext-google-maps": ("Google Maps Platform", "Geolocation, routing, and map rendering"),
        "ext-openweather": ("OpenWeather API", "Weather forecast and alert data provider"),
        "ext-snowflake": ("Snowflake Data Cloud", "Cloud data warehouse for analytics"),
    }
    for ext_id in sorted(ext_systems):
        name, desc = ext_descriptions.get(ext_id, (ext_id, "External system"))
        nodes.append({
            "unique-id": ext_id,
            "node-type": "system",
            "name": name,
            "description": desc,
            "interfaces": [],
            "metadata": {"domain": "External", "external": True},
        })

    # Filter to single domain if requested
    if domain_filter:
        nodes, relationships = filter_by_domain(nodes, relationships, domains, domain_filter)

    # Assemble CALM document
    calm_doc = {
        "$schema": "https://raw.githubusercontent.com/finos/architecture-as-code/main/calm/schema/calm.json",
        "metadata": {
            "name": f"NovaTrek Adventures — {'Full System' if not domain_filter else domain_filter + ' Domain'} Topology",
            "description": "Auto-generated from NovaTrek metadata YAML files and OpenAPI specs. DO NOT EDIT — regenerate with: python3 scripts/generate-calm.py",
            "version": "1.0.0",
            "generated-from": [
                "architecture/metadata/domains.yaml",
                "architecture/metadata/data-stores.yaml",
                "architecture/metadata/cross-service-calls.yaml",
                "architecture/metadata/events.yaml",
                "architecture/metadata/actors.yaml",
                "architecture/specs/*.yaml",
            ],
        },
        "nodes": nodes,
        "relationships": relationships,
    }

    return calm_doc


def main():
    parser = argparse.ArgumentParser(description="Generate CALM topology from NovaTrek metadata")
    parser.add_argument("--domain", help="Generate for a single domain (e.g., Operations)")
    parser.add_argument("--output", "-o", help="Output file path (default: architecture/calm/novatrek-topology.json)")
    parser.add_argument("--pretty", action="store_true", default=True, help="Pretty-print JSON (default)")
    parser.add_argument("--compact", action="store_true", help="Compact JSON output")
    args = parser.parse_args()

    calm = generate_calm(domain_filter=args.domain)

    # Determine output path
    if args.output:
        out_path = Path(args.output)
    elif args.domain:
        out_path = ROOT / "architecture" / "calm" / "domains" / f"{args.domain.lower().replace(' ', '-')}.json"
    else:
        out_path = ROOT / "architecture" / "calm" / "novatrek-topology.json"

    out_path.parent.mkdir(parents=True, exist_ok=True)

    indent = None if args.compact else 2
    with open(out_path, "w") as f:
        json.dump(calm, f, indent=indent, ensure_ascii=False)

    # Print summary
    n_services = sum(1 for n in calm["nodes"] if n["node-type"] == "service")
    n_databases = sum(1 for n in calm["nodes"] if n["node-type"] == "database")
    n_actors = sum(1 for n in calm["nodes"] if n["node-type"] in ("actor", "system") and not n["unique-id"].startswith("svc-"))
    n_rels = len(calm["relationships"])

    print(f"CALM topology generated: {out_path}")
    print(f"  Nodes: {len(calm['nodes'])} ({n_services} services, {n_databases} databases, {n_actors} actors/systems)")
    print(f"  Relationships: {n_rels}")
    if args.domain:
        print(f"  Domain filter: {args.domain}")


if __name__ == "__main__":
    main()
