#!/usr/bin/env python3
"""CALM-based impact analysis for NovaTrek architecture.

Given one or more service names, traverses the CALM topology to identify
all upstream (callers) and downstream (callees) dependencies, grouped by
protocol and domain. Useful for assessing the blast radius of a change.

Usage:
    python3 scripts/calm-impact-analysis.py svc-check-in
    python3 scripts/calm-impact-analysis.py svc-check-in svc-reservations
    python3 scripts/calm-impact-analysis.py svc-check-in --depth 2
    python3 scripts/calm-impact-analysis.py svc-check-in --format json
"""

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
CALM_PATH = WORKSPACE_ROOT / "architecture" / "calm" / "novatrek-topology.json"


def load_topology():
    with open(CALM_PATH, encoding="utf-8") as f:
        return json.load(f)


def _rel_endpoints(rel):
    """Extract (source, target) from a CALM 1.2 relationship."""
    rt = rel.get("relationship-type", {})
    if "connects" in rt:
        c = rt["connects"]
        return c["source"]["node"], c["destination"]["node"]
    if "interacts" in rt:
        it = rt["interacts"]
        if "source" in it and "destination" in it:
            return it["source"]["node"], it["destination"]["node"]
    return None


def _rel_protocol(rel):
    """Get effective protocol (checks metadata.transport for Kafka events)."""
    proto = rel.get("protocol", "")
    if proto:
        return proto
    return rel.get("metadata", {}).get("transport", "")


def build_graph(topology):
    """Build adjacency lists from CALM topology.

    Returns:
        node_map: {id: node_dict}
        downstream: {src: [(target, protocol, description)]}
        upstream:   {tgt: [(source, protocol, description)]}
    """
    node_map = {n["unique-id"]: n for n in topology["nodes"]}
    svc_ids = {n["unique-id"] for n in topology["nodes"] if n["node-type"] == "service"}

    downstream = defaultdict(list)
    upstream = defaultdict(list)

    for rel in topology["relationships"]:
        endpoints = _rel_endpoints(rel)
        if not endpoints:
            continue
        src, tgt = endpoints
        if src not in svc_ids or tgt not in svc_ids:
            continue
        proto = _rel_protocol(rel)
        desc = rel.get("description", "")
        downstream[src].append((tgt, proto, desc))
        upstream[tgt].append((src, proto, desc))

    return node_map, downstream, upstream


def walk_deps(graph, start, depth):
    """BFS walk of a dependency graph to a given depth."""
    visited = set()
    frontier = {start}
    result = {}  # depth -> set of (node, protocol)
    for d in range(1, depth + 1):
        next_frontier = set()
        for node in frontier:
            for target, proto, _ in graph.get(node, []):
                if target not in visited and target != start:
                    visited.add(target)
                    next_frontier.add(target)
                    result.setdefault(d, set()).add((target, proto))
        frontier = next_frontier
        if not frontier:
            break
    return result


def analyze(services, topology, depth=1):
    """Run impact analysis for the given services."""
    node_map, downstream, upstream = build_graph(topology)
    svc_ids = {n["unique-id"] for n in topology["nodes"] if n["node-type"] == "service"}

    results = {}
    for svc in services:
        if svc not in svc_ids:
            print(f"WARNING: {svc} not found in CALM topology", file=sys.stderr)
            continue

        node = node_map[svc]
        domain = node.get("metadata", {}).get("domain", "Unknown")
        team = node.get("metadata", {}).get("team", "Unknown")

        down = walk_deps(downstream, svc, depth)
        up = walk_deps(upstream, svc, depth)

        # Flatten for summary
        all_downstream = set()
        for deps in down.values():
            all_downstream.update(deps)
        all_upstream = set()
        for deps in up.values():
            all_upstream.update(deps)

        # Group by domain
        down_by_domain = defaultdict(list)
        for target, proto in sorted(all_downstream):
            t_domain = node_map.get(target, {}).get("metadata", {}).get("domain", "Unknown")
            down_by_domain[t_domain].append({"service": target, "protocol": proto})

        up_by_domain = defaultdict(list)
        for source, proto in sorted(all_upstream):
            s_domain = node_map.get(source, {}).get("metadata", {}).get("domain", "Unknown")
            up_by_domain[s_domain].append({"service": source, "protocol": proto})

        results[svc] = {
            "domain": domain,
            "team": team,
            "downstream": dict(down_by_domain),
            "upstream": dict(up_by_domain),
            "downstream_count": len(all_downstream),
            "upstream_count": len(all_upstream),
            "blast_radius": len(all_downstream) + len(all_upstream),
        }

    return results


def print_text(results, depth):
    """Pretty-print results as text."""
    for svc, data in results.items():
        print(f"\n{'=' * 60}")
        print(f"  Impact Analysis: {svc}")
        print(f"  Domain: {data['domain']}  |  Team: {data['team']}")
        print(f"  Blast Radius: {data['blast_radius']} services "
              f"({data['downstream_count']} downstream, {data['upstream_count']} upstream)")
        if depth > 1:
            print(f"  Traversal Depth: {depth}")
        print(f"{'=' * 60}")

        if data["downstream"]:
            print(f"\n  DOWNSTREAM (services {svc} calls):")
            for domain in sorted(data["downstream"]):
                print(f"    [{domain}]")
                for dep in data["downstream"][domain]:
                    print(f"      -> {dep['service']}  ({dep['protocol']})")
        else:
            print("\n  DOWNSTREAM: none (leaf service)")

        if data["upstream"]:
            print(f"\n  UPSTREAM (services that call {svc}):")
            for domain in sorted(data["upstream"]):
                print(f"    [{domain}]")
                for dep in data["upstream"][domain]:
                    print(f"      <- {dep['service']}  ({dep['protocol']})")
        else:
            print("\n  UPSTREAM: none (no inbound dependencies)")

        print()


def main():
    parser = argparse.ArgumentParser(
        description="CALM-based impact analysis for NovaTrek architecture"
    )
    parser.add_argument(
        "services",
        nargs="+",
        help="One or more service IDs (e.g. svc-check-in svc-reservations)",
    )
    parser.add_argument(
        "--depth",
        type=int,
        default=1,
        help="Traversal depth for transitive dependencies (default: 1)",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )
    parser.add_argument(
        "--topology",
        type=Path,
        default=CALM_PATH,
        help="Path to CALM topology JSON file",
    )
    args = parser.parse_args()

    topology = load_topology()
    results = analyze(args.services, topology, depth=args.depth)

    if not results:
        print("No valid services found.", file=sys.stderr)
        sys.exit(1)

    if args.format == "json":
        print(json.dumps(results, indent=2))
    else:
        print_text(results, args.depth)


if __name__ == "__main__":
    main()
