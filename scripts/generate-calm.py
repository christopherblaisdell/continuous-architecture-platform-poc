#!/usr/bin/env python3
"""Generate a CALM (Common Architecture Language Model) topology document
from NovaTrek's existing metadata YAML files.

Produces CALM 1.2-compliant JSON validated by `calm validate` (FINOS calm-cli).

Usage:
    python3 scripts/generate-calm.py                        # all domains + system
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
    architecture/calm/novatrek-topology.json  (full system)
    architecture/calm/domains/{domain}.json   (per-domain files)
"""

import argparse
import json
import sys
from pathlib import Path

import yaml

CALM_SCHEMA = "https://calm.finos.org/release/1.2/meta/calm.json"

ROOT = Path(__file__).resolve().parent.parent
META = ROOT / "architecture" / "metadata"
SPECS = ROOT / "architecture" / "specs"

# Maps actor names (from actors.yaml) to CALM node IDs for external systems
# and infrastructure. Must stay in sync with label_to_svc in
# build_cross_service_relationships().
ACTOR_TO_EXT_ID = {
    "API Gateway": "ext-api-gateway",
    "Event Bus": "ext-kafka-broker",
    "Object Store": "ext-object-store",
    "Payment Gateway": "ext-payment-gateway",
    "Stripe API": "ext-stripe",
    "Fraud Detection API": "ext-fraud-detection",
    "DocuSign API": "ext-docusign",
    "IDVerify API": "ext-idverify",
    "Google Maps Platform": "ext-google-maps",
    "OpenWeather API": "ext-openweather",
    "Firebase Cloud Messaging": "ext-firebase-fcm",
    "SendGrid API": "ext-sendgrid",
    "Twilio API": "ext-twilio",
    "Snowflake Data Cloud": "ext-snowflake",
    "National Parks Permit API": "ext-national-parks-permit",
    "Travel Insurance API": "ext-travel-insurance",
    "Search and Rescue Dispatch API": "ext-sar-dispatch",
    "Instagram Graph API": "ext-instagram",
    "Currency Exchange API": "ext-currency-exchange",
    "Fleet GPS Tracking API": "ext-fleet-gps",
    "Supplier Procurement Portal": "ext-supplier-procurement",
}


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


def build_service_node(svc, domains, data_stores, events_data):
    domain = domain_for_service(domains, svc)
    spec = load_openapi_spec(svc)

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
                        "method": method.upper(),
                        "path": path,
                        "summary": summary,
                    })

    # Extract event interfaces (produced events)
    if events_data:
        for event_key, event in events_data.items():
            if event.get("producer") == svc:
                interfaces.append({
                    "unique-id": f"{svc}-event-{event_key.replace('.', '-')}",
                    "channel": event["channel"],
                    "protocol": "Kafka",
                    "role": "producer",
                })

    description = ""
    if spec and "info" in spec:
        description = spec["info"].get("description", "").strip().split("\n")[0]

    return {
        "unique-id": svc,
        "node-type": "service",
        "name": svc.replace("svc-", "").replace("-", " ").title() + " Service",
        "description": description or f"NovaTrek {svc} microservice",
        "interfaces": interfaces,
        "metadata": {
            "domain": domain,
            "team": team_for_domain(domain),
        },
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
                "host": f"{svc.replace('svc-', '')}-db.novatrek.internal",
                "port": 5432 if "Postgres" in engine else 27017,
            }
        ],
        "metadata": {
            "domain": domain,
            "engine": engine,
            "schema": schema,
            "tables": tables,
        },
    }


def build_actor_node(name, actor_data):
    actor_type = actor_data.get("type", "Human")
    node_type = "actor" if actor_type == "Human" else "system"

    # Use ext-* ID for external systems / infrastructure to match label_to_svc
    node_id = ACTOR_TO_EXT_ID.get(name, name.lower().replace(" ", "-"))

    node = {
        "unique-id": node_id,
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


# --- CALM 1.2 relationship builders ---

def build_service_to_db_relationship(svc):
    return {
        "unique-id": f"rel-{svc}-to-db",
        "description": f"{svc} connects to its owned database",
        "relationship-type": {
            "connects": {
                "source": {"node": svc},
                "destination": {"node": f"{svc}-db"},
            }
        },
        "protocol": "JDBC",
    }


def build_cross_service_relationships(cross_calls):
    relationships = []
    label_to_svc = {
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
        "Guide Mgmt": "svc-guide-management",
        "Trail Mgmt": "svc-trail-management",
        "Weather Svc": "svc-weather",
        "Location Svc": "svc-location-services",
        "Payments Svc": "svc-payments",
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
        "National Parks Permit API": "ext-national-parks-permit",
        "Travel Insurance API": "ext-travel-insurance",
        "Search and Rescue Dispatch API": "ext-sar-dispatch",
        "Instagram Graph API": "ext-instagram",
        "Currency Exchange API": "ext-currency-exchange",
        "Fleet GPS Tracking API": "ext-fleet-gps",
        "Supplier Procurement Portal": "ext-supplier-procurement",
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
                action = call.get("action", "")

                rel_id = f"rel-{source_svc}-{endpoint.replace(' ', '-').replace('/', '-')}-to-{target_svc}".lower()

                relationships.append({
                    "unique-id": rel_id,
                    "description": action or f"{source_svc} calls {target_svc} ({endpoint})",
                    "relationship-type": {
                        "connects": {
                            "source": {"node": source_svc},
                            "destination": {"node": target_svc},
                        }
                    },
                    "protocol": "HTTPS",
                    "metadata": {
                        "source-endpoint": endpoint,
                        "target-endpoint": f"{target_info.get('method', 'GET')} {target_info.get('path', '')}",
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
                "description": event.get("summary", f"{producer} publishes {event_key} consumed by {consumer}"),
                "relationship-type": {
                    "connects": {
                        "source": {"node": producer},
                        "destination": {"node": consumer},
                    }
                },
                "metadata": {
                    "event": event_key,
                    "channel": event.get("channel", ""),
                    "transport": "Kafka",
                },
            })
    return relationships


def build_actor_relationships(actors_data):
    relationships = []
    if not actors_data:
        return relationships

    for actor_name, actor_data in actors_data.items():
        actor_id = ACTOR_TO_EXT_ID.get(actor_name, actor_name.lower().replace(" ", "-"))
        targets = actor_data.get("interacts_with", [])
        if targets:
            rel_id = f"rel-{actor_id}-interacts"
            relationships.append({
                "unique-id": rel_id,
                "description": f"{actor_name} interacts with NovaTrek services",
                "relationship-type": {
                    "interacts": {
                        "actor": actor_id,
                        "nodes": targets,
                    }
                },
                "protocol": "HTTPS",
            })
    return relationships


def get_relationship_nodes(rel):
    """Extract source and target node IDs from a CALM 1.2 relationship."""
    rt = rel["relationship-type"]
    nodes = set()
    if "connects" in rt:
        nodes.add(rt["connects"]["source"]["node"])
        nodes.add(rt["connects"]["destination"]["node"])
    elif "interacts" in rt:
        nodes.add(rt["interacts"]["actor"])
        nodes.update(rt["interacts"]["nodes"])
    elif "deployed-in" in rt:
        nodes.add(rt["deployed-in"]["container"])
        nodes.update(rt["deployed-in"]["nodes"])
    elif "composed-of" in rt:
        nodes.add(rt["composed-of"]["container"])
        nodes.update(rt["composed-of"]["nodes"])
    return nodes


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
        rel_nodes = get_relationship_nodes(rel)
        if rel_nodes & domain_node_ids:
            filtered_rels.append(rel)
            external_node_ids.update(rel_nodes - domain_node_ids)

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

    nodes = []
    relationships = []

    # Build service nodes and database nodes
    all_services = set()
    for domain_name, domain_data in domains.items():
        for svc in domain_data.get("services", []):
            all_services.add(svc)
            nodes.append(build_service_node(svc, domains, data_stores, events_data))

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
        for nid in get_relationship_nodes(rel):
            if nid.startswith("ext-") and nid not in node_ids:
                ext_systems.add(nid)

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
        "ext-national-parks-permit": ("National Parks Permit API", "Government parks and forestry trail access permit system"),
        "ext-travel-insurance": ("Travel Insurance API", "Third-party adventure trip insurance quoting and binding"),
        "ext-sar-dispatch": ("Search and Rescue Dispatch API", "Regional SAR team emergency dispatch coordination"),
        "ext-instagram": ("Instagram Graph API", "Social media photo sharing to guest Instagram accounts"),
        "ext-currency-exchange": ("Currency Exchange API", "Real-time foreign currency exchange rate conversion"),
        "ext-fleet-gps": ("Fleet GPS Tracking API", "Vehicle telematics and real-time fleet GPS tracking"),
        "ext-supplier-procurement": ("Supplier Procurement Portal", "External vendor ordering platform for gear and supplies"),
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

    # Assemble CALM 1.2 document
    title = "Full System" if not domain_filter else f"{domain_filter} Domain"
    calm_doc = {
        "$schema": CALM_SCHEMA,
        "nodes": nodes,
        "relationships": relationships,
        "metadata": [
            {
                "novatrek": {
                    "name": f"NovaTrek Adventures — {title} Topology",
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
                }
            }
        ],
    }

    return calm_doc


def main():
    parser = argparse.ArgumentParser(description="Generate CALM topology from NovaTrek metadata")
    parser.add_argument("--domain", help="Generate for a single domain (e.g., Operations)")
    parser.add_argument("--output", "-o", help="Output file path (default: architecture/calm/novatrek-topology.json)")
    parser.add_argument("--all-domains", action="store_true", help="Generate per-domain files for all domains")
    parser.add_argument("--compact", action="store_true", help="Compact JSON output")
    args = parser.parse_args()

    indent = None if args.compact else 2

    if args.all_domains:
        domains = load_domains()
        for domain_name in domains:
            calm = generate_calm(domain_filter=domain_name)
            slug = domain_name.lower().replace(" ", "-")
            out_path = ROOT / "architecture" / "calm" / "domains" / f"{slug}.json"
            out_path.parent.mkdir(parents=True, exist_ok=True)
            with open(out_path, "w") as f:
                json.dump(calm, f, indent=indent, ensure_ascii=False)
            print(f"  Domain: {domain_name} -> {out_path}")

        # Also generate full system topology
        calm = generate_calm()
        out_path = ROOT / "architecture" / "calm" / "novatrek-topology.json"
        with open(out_path, "w") as f:
            json.dump(calm, f, indent=indent, ensure_ascii=False)
        _print_summary(calm, out_path)
    else:
        calm = generate_calm(domain_filter=args.domain)

        if args.output:
            out_path = Path(args.output)
        elif args.domain:
            out_path = ROOT / "architecture" / "calm" / "domains" / f"{args.domain.lower().replace(' ', '-')}.json"
        else:
            out_path = ROOT / "architecture" / "calm" / "novatrek-topology.json"

        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w") as f:
            json.dump(calm, f, indent=indent, ensure_ascii=False)
        _print_summary(calm, out_path)


def _print_summary(calm, out_path):
    n_services = sum(1 for n in calm["nodes"] if n["node-type"] == "service")
    n_databases = sum(1 for n in calm["nodes"] if n["node-type"] == "database")
    n_actors = sum(1 for n in calm["nodes"] if n["node-type"] in ("actor", "system") and not n["unique-id"].startswith("svc-"))
    n_rels = len(calm["relationships"])

    print(f"CALM topology generated: {out_path}")
    print(f"  Nodes: {len(calm['nodes'])} ({n_services} services, {n_databases} databases, {n_actors} actors/systems)")
    print(f"  Relationships: {n_rels}")


if __name__ == "__main__":
    main()
