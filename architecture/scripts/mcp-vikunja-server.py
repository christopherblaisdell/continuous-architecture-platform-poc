#!/usr/bin/env python3
"""MCP server for NovaTrek Architecture Platform.

Exposes Vikunja ticket data and architecture metadata to AI agents
via the Model Context Protocol (MCP) over stdio.

Tools provided:
  - list_tickets: List tickets with optional filtering by status, capability, or service
  - get_ticket: Get full ticket detail by key (e.g., NTK-10003)
  - search_tickets: Full-text search across ticket summaries and descriptions
  - get_capability_tickets: Find all tickets that affect a specific capability
  - list_capabilities: List all capabilities with health metrics
  - get_capability: Get capability detail with solution timeline

Data sources (in priority order):
  1. Vikunja API (live, if VIKUNJA_URL and VIKUNJA_TOKEN are set)
  2. tickets.yaml (fallback, always available)

Usage:
    # With Vikunja (live data):
    export VIKUNJA_URL="https://ca-vikunja-prod.greendune-28870689.eastus2.azurecontainerapps.io"
    export VIKUNJA_TOKEN="your-token"
    python3 scripts/mcp-vikunja-server.py

    # Without Vikunja (YAML-only fallback):
    python3 scripts/mcp-vikunja-server.py

MCP Configuration (add to VS Code settings.json or .vscode/mcp.json):
    {
      "servers": {
        "novatrek-architecture": {
          "command": "python3",
          "args": ["scripts/mcp-vikunja-server.py"],
          "env": {
            "VIKUNJA_URL": "https://ca-vikunja-prod...",
            "VIKUNJA_TOKEN": "..."
          }
        }
      }
    }
"""

import json
import os
import re
import sys
import urllib.request
import urllib.error
import yaml

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
METADATA_DIR = os.path.join(REPO_ROOT, "architecture", "metadata")
TICKETS_PATH = os.path.join(METADATA_DIR, "tickets.yaml")
CAPABILITIES_PATH = os.path.join(METADATA_DIR, "capabilities.yaml")
CHANGELOG_PATH = os.path.join(METADATA_DIR, "capability-changelog.yaml")

VIKUNJA_URL = os.environ.get("VIKUNJA_URL", "").rstrip("/")
VIKUNJA_TOKEN = os.environ.get("VIKUNJA_TOKEN", "")


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_yaml(path):
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def vikunja_api(method, path, data=None):
    """Make authenticated Vikunja API request. Returns None on failure."""
    if not VIKUNJA_URL or not VIKUNJA_TOKEN:
        return None
    url = f"{VIKUNJA_URL}/api/v1{path}"
    headers = {
        "Authorization": f"Bearer {VIKUNJA_TOKEN}",
        "Content-Type": "application/json",
    }
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except (urllib.error.URLError, OSError):
        return None


def get_vikunja_project_id():
    """Find NovaTrek Adventures project ID."""
    projects = vikunja_api("GET", "/projects")
    if not projects:
        return None
    for p in projects:
        if p.get("title") == "NovaTrek Adventures":
            return p["id"]
    return None


def get_vikunja_tasks():
    """Fetch all tasks from Vikunja."""
    pid = get_vikunja_project_id()
    if not pid:
        return []
    tasks = []
    page = 1
    while True:
        result = vikunja_api("GET", f"/projects/{pid}/tasks?page={page}")
        if not result:
            break
        tasks.extend(result)
        if len(result) < 50:
            break
        page += 1
    return tasks


def extract_ticket_key(title):
    match = re.match(r"\[([A-Z]+-\d+)\]", title)
    return match.group(1) if match else None


def get_task_status_label(task):
    for label in task.get("labels", []) or []:
        title = label.get("title", "")
        if title.startswith("Status: "):
            return title.replace("Status: ", "")
    return None


def get_task_cap_labels(task):
    caps = []
    for label in task.get("labels", []) or []:
        title = label.get("title", "")
        if re.match(r"CAP-\d+\.\d+:", title):
            caps.append(title.split(":")[0])
    return caps


def merge_ticket_data(yaml_tickets, vikunja_tasks):
    """Merge YAML tickets with live Vikunja data (Vikunja wins for status/priority)."""
    task_by_key = {}
    for task in vikunja_tasks:
        key = extract_ticket_key(task.get("title", ""))
        if key:
            task_by_key[key] = task

    merged = []
    for ticket in yaml_tickets:
        key = ticket["key"]
        t = dict(ticket)  # copy
        if key in task_by_key:
            task = task_by_key[key]
            vikunja_status = get_task_status_label(task)
            if vikunja_status:
                t["status"] = vikunja_status
            prio_map = {1: "Low", 2: "Medium", 3: "High", 4: "Critical"}
            t["priority"] = prio_map.get(task.get("priority", 2), t.get("priority", "Medium"))
            t["vikunja_id"] = task.get("id")
            t["source"] = "vikunja+yaml"
        else:
            t["source"] = "yaml"
        merged.append(t)

    return merged


# ---------------------------------------------------------------------------
# Tool implementations
# ---------------------------------------------------------------------------

def tool_list_tickets(arguments):
    yaml_data = load_yaml(TICKETS_PATH)
    yaml_tickets = yaml_data.get("tickets", [])
    vikunja_tasks = get_vikunja_tasks()
    tickets = merge_ticket_data(yaml_tickets, vikunja_tasks) if vikunja_tasks else yaml_tickets

    status_filter = arguments.get("status")
    capability_filter = arguments.get("capability")
    service_filter = arguments.get("service")

    results = []
    for t in tickets:
        if status_filter and t.get("status", "").lower() != status_filter.lower():
            continue
        if service_filter and service_filter not in t.get("components", []):
            continue
        if capability_filter:
            caps = t.get("planned_capabilities", [])
            cap_ids = [c.get("id", c) if isinstance(c, dict) else c for c in caps]
            changelog = load_yaml(CHANGELOG_PATH)
            for entry in changelog.get("entries", []):
                if entry.get("ticket") == t["key"]:
                    cap_ids.extend(c["id"] for c in entry.get("capabilities", []))
            if capability_filter not in cap_ids:
                continue
        results.append({
            "key": t["key"],
            "summary": t.get("summary", ""),
            "status": t.get("status", ""),
            "priority": t.get("priority", ""),
            "components": t.get("components", []),
            "solution": t.get("solution", ""),
        })

    source = "Vikunja + YAML" if vikunja_tasks else "YAML only"
    return json.dumps({"tickets": results, "count": len(results), "source": source}, indent=2)


def tool_get_ticket(arguments):
    key = arguments.get("key", "")
    yaml_data = load_yaml(TICKETS_PATH)
    yaml_tickets = yaml_data.get("tickets", [])
    vikunja_tasks = get_vikunja_tasks()
    tickets = merge_ticket_data(yaml_tickets, vikunja_tasks) if vikunja_tasks else yaml_tickets

    for t in tickets:
        if t.get("key") == key:
            return json.dumps(t, indent=2, default=str)

    return json.dumps({"error": f"Ticket {key} not found"})


def tool_search_tickets(arguments):
    query = arguments.get("query", "").lower()
    yaml_data = load_yaml(TICKETS_PATH)
    yaml_tickets = yaml_data.get("tickets", [])
    vikunja_tasks = get_vikunja_tasks()
    tickets = merge_ticket_data(yaml_tickets, vikunja_tasks) if vikunja_tasks else yaml_tickets

    results = []
    for t in tickets:
        searchable = f"{t.get('key', '')} {t.get('summary', '')} {t.get('user_story', '')} {' '.join(t.get('components', []))}".lower()
        if query in searchable:
            results.append({
                "key": t["key"],
                "summary": t.get("summary", ""),
                "status": t.get("status", ""),
                "priority": t.get("priority", ""),
            })

    return json.dumps({"results": results, "count": len(results), "query": query}, indent=2)


def tool_get_capability_tickets(arguments):
    cap_id = arguments.get("capability_id", "")
    changelog = load_yaml(CHANGELOG_PATH)
    yaml_data = load_yaml(TICKETS_PATH)

    solved = []
    for entry in changelog.get("entries", []):
        for cap in entry.get("capabilities", []):
            if cap["id"] == cap_id:
                solved.append({
                    "ticket": entry["ticket"],
                    "solution": entry.get("solution", ""),
                    "date": str(entry.get("date", "")),
                    "impact": cap.get("impact", ""),
                    "description": cap.get("description", ""),
                })
                break

    planned = []
    for t in yaml_data.get("tickets", []):
        for pc in t.get("planned_capabilities", []):
            pc_id = pc.get("id", pc) if isinstance(pc, dict) else pc
            if pc_id == cap_id:
                planned.append({
                    "ticket": t["key"],
                    "status": t.get("status", ""),
                    "summary": t.get("summary", ""),
                })
                break

    return json.dumps({
        "capability": cap_id,
        "solved": solved,
        "planned": planned,
        "total": len(solved) + len(planned),
    }, indent=2)


def tool_list_capabilities(arguments):
    caps_data = load_yaml(CAPABILITIES_PATH)
    changelog = load_yaml(CHANGELOG_PATH)

    changelog_by_cap = {}
    for entry in changelog.get("entries", []):
        for cap in entry.get("capabilities", []):
            cap_id = cap["id"]
            if cap_id not in changelog_by_cap:
                changelog_by_cap[cap_id] = 0
            changelog_by_cap[cap_id] += 1

    results = []
    for domain in caps_data.get("domains", []):
        for cap in domain.get("capabilities", []):
            results.append({
                "id": cap["id"],
                "name": cap["name"],
                "domain": domain["name"],
                "status": cap.get("status", ""),
                "solution_count": changelog_by_cap.get(cap["id"], 0),
                "services": cap.get("services", []),
            })

    status_filter = arguments.get("status")
    if status_filter:
        results = [r for r in results if r["status"] == status_filter]

    return json.dumps({"capabilities": results, "count": len(results)}, indent=2)


def tool_get_capability(arguments):
    cap_id = arguments.get("capability_id", "")
    caps_data = load_yaml(CAPABILITIES_PATH)
    changelog = load_yaml(CHANGELOG_PATH)

    cap_info = None
    domain_name = ""
    for domain in caps_data.get("domains", []):
        for cap in domain.get("capabilities", []):
            if cap["id"] == cap_id:
                cap_info = cap
                domain_name = domain["name"]
                break

    if not cap_info:
        return json.dumps({"error": f"Capability {cap_id} not found"})

    timeline = []
    for entry in changelog.get("entries", []):
        for cap in entry.get("capabilities", []):
            if cap["id"] == cap_id:
                timeline.append({
                    "ticket": entry["ticket"],
                    "date": str(entry.get("date", "")),
                    "solution": entry.get("solution", ""),
                    "impact": cap.get("impact", ""),
                    "description": cap.get("description", ""),
                    "l3_capabilities": cap.get("l3_capabilities", []),
                    "decisions": entry.get("decisions", []),
                })
                break

    return json.dumps({
        "id": cap_info["id"],
        "name": cap_info["name"],
        "domain": domain_name,
        "status": cap_info.get("status", ""),
        "description": cap_info.get("description", ""),
        "services": cap_info.get("services", []),
        "solution_count": len(timeline),
        "timeline": timeline,
    }, indent=2, default=str)


# ---------------------------------------------------------------------------
# MCP protocol handler (JSON-RPC over stdio)
# ---------------------------------------------------------------------------

TOOLS = [
    {
        "name": "list_tickets",
        "description": "List NovaTrek architecture tickets with optional filtering. Returns tickets from Vikunja (if available) merged with YAML metadata.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "status": {"type": "string", "description": "Filter by status: New, In Progress, Ready for Dev, Closed"},
                "capability": {"type": "string", "description": "Filter by capability ID (e.g., CAP-2.1)"},
                "service": {"type": "string", "description": "Filter by service name (e.g., svc-check-in)"},
            },
        },
    },
    {
        "name": "get_ticket",
        "description": "Get full details of a specific NovaTrek ticket by key.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "key": {"type": "string", "description": "Ticket key (e.g., NTK-10003)"},
            },
            "required": ["key"],
        },
    },
    {
        "name": "search_tickets",
        "description": "Full-text search across ticket summaries, user stories, and components.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query text"},
            },
            "required": ["query"],
        },
    },
    {
        "name": "get_capability_tickets",
        "description": "Find all tickets (solved and planned) that affect a specific capability.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "capability_id": {"type": "string", "description": "Capability ID (e.g., CAP-2.1)"},
            },
            "required": ["capability_id"],
        },
    },
    {
        "name": "list_capabilities",
        "description": "List all NovaTrek business capabilities with solution counts and health metrics.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "status": {"type": "string", "description": "Filter by status: implemented, partial, not-implemented"},
            },
        },
    },
    {
        "name": "get_capability",
        "description": "Get full detail of a specific capability including solution timeline and L3 emergent capabilities.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "capability_id": {"type": "string", "description": "Capability ID (e.g., CAP-2.1)"},
            },
            "required": ["capability_id"],
        },
    },
]

TOOL_HANDLERS = {
    "list_tickets": tool_list_tickets,
    "get_ticket": tool_get_ticket,
    "search_tickets": tool_search_tickets,
    "get_capability_tickets": tool_get_capability_tickets,
    "list_capabilities": tool_list_capabilities,
    "get_capability": tool_get_capability,
}


def handle_request(request):
    """Handle a JSON-RPC request and return a response."""
    method = request.get("method", "")
    req_id = request.get("id")
    params = request.get("params", {})

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {
                    "name": "novatrek-architecture",
                    "version": "1.0.0",
                },
            },
        }

    if method == "notifications/initialized":
        return None  # No response for notifications

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"tools": TOOLS},
        }

    if method == "tools/call":
        tool_name = params.get("name", "")
        arguments = params.get("arguments", {})

        handler = TOOL_HANDLERS.get(tool_name)
        if not handler:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": f"Unknown tool: {tool_name}"}],
                    "isError": True,
                },
            }

        try:
            result_text = handler(arguments)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": result_text}],
                },
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": f"Error: {e}"}],
                    "isError": True,
                },
            }

    # Unknown method
    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": f"Method not found: {method}"},
    }


def main():
    """Run the MCP server over stdio."""
    source = "Vikunja + YAML" if (VIKUNJA_URL and VIKUNJA_TOKEN) else "YAML only"
    sys.stderr.write(f"NovaTrek MCP Server started (source: {source})\n")

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
        except json.JSONDecodeError:
            continue

        response = handle_request(request)
        if response is not None:
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
