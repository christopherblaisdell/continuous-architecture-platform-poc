"""Load portal metadata from YAML files.

All portal generators import metadata from this module instead of
embedding large Python dictionaries inline. The YAML files under
architecture/metadata/ are the single source of truth.

Architects edit the YAML files, commit, push -- CI rebuilds everything.
"""

import os
import yaml

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
METADATA_DIR = os.path.join(WORKSPACE_ROOT, "architecture", "metadata")


def _load(filename):
    """Load a YAML metadata file."""
    path = os.path.join(METADATA_DIR, filename)
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


# ── Domain Classification ──
DOMAINS = _load("domains.yaml")

# Derive ALL_SERVICES from domains
ALL_SERVICES = set()
for _info in DOMAINS.values():
    ALL_SERVICES.update(_info["services"])

# Service → domain light color lookup
_SVC_TO_LIGHT = {}
for _dname, _dinfo in DOMAINS.items():
    for _svc in _dinfo["services"]:
        _SVC_TO_LIGHT[_svc] = _dinfo["light"]

def get_service_light_color(svc_name):
    """Return the pastel background color for a service's domain."""
    return _SVC_TO_LIGHT.get(svc_name, "#F1F5F9")

# ── Label Mappings ──
LABEL_TO_SVC = _load("label-to-svc.yaml")

# ── PCI Compliance ──
_pci = _load("pci.yaml")
PCI_SERVICES = set(_pci["services"])
PCI_EXTERNALS = set(_pci["externals"])
PCI_DATA_FLOWS = {tuple(pair) for pair in _pci["data_flows"]}


def is_pci_flow(from_name, to_name):
    """Check whether a relationship carries PCI-sensitive data."""
    return (from_name, to_name) in PCI_DATA_FLOWS


# ── Data Stores ──
_raw_stores = _load("data-stores.yaml")

def _convert_data_stores(raw):
    """Convert YAML data-stores back to the tuple-based format generators expect."""
    result = {}
    for svc, info in raw.items():
        svc_data = {}
        for key, val in info.items():
            if key == "table_details":
                tables = {}
                for tbl_name, tbl_info in val.items():
                    tbl_data = {"description": tbl_info["description"]}
                    tbl_data["columns"] = [
                        (c["name"], c["type"], c["constraints"])
                        for c in tbl_info["columns"]
                    ]
                    tbl_data["indexes"] = [
                        (i["name"], i["columns"]) if "type" not in i
                        else (i["name"], i["columns"], i["type"])
                        for i in tbl_info["indexes"]
                    ]
                    tables[tbl_name] = tbl_data
                svc_data["table_details"] = tables
            else:
                svc_data[key] = val
        result[svc] = svc_data
    return result

DATA_STORES = _convert_data_stores(_raw_stores)


# ── Cross-Service Calls ──
_raw_calls = _load("cross-service-calls.yaml")

def _convert_cross_service_calls(raw):
    """Convert YAML cross-service-calls back to the keyed format generators expect."""
    result = {}
    for svc, endpoints in raw.items():
        for endpoint_key, calls in endpoints.items():
            method, path = endpoint_key.split(" ", 1)
            targets = []
            for c in calls:
                target = None
                if "target" in c:
                    target = (c["target"]["method"], c["target"]["path"])
                targets.append((c["alias"], c["label"], c["action"], c["async"], target))
            result[(svc, method, path)] = targets
    return result

CROSS_SERVICE_CALLS = _convert_cross_service_calls(_raw_calls)


# ── Event Catalog ──
_raw_events = _load("events.yaml")

def _convert_events(raw):
    """Convert YAML events back to the tuple-based format generators expect."""
    result = {}
    for evt_name, evt_info in raw.items():
        result[evt_name] = {
            "channel": evt_info["channel"],
            "producer": evt_info["producer"],
            "trigger": (evt_info["trigger"]["method"], evt_info["trigger"]["path"]),
            "consumers": evt_info["consumers"],
            "domain": evt_info["domain"],
            "summary": evt_info["summary"],
        }
    return result

EVENT_CATALOG = _convert_events(_raw_events)

# Derived lookups
EVENTS_BY_PRODUCER = {}
EVENTS_BY_CONSUMER = {}
for _evt_name, _evt_info in EVENT_CATALOG.items():
    EVENTS_BY_PRODUCER.setdefault(_evt_info["producer"], []).append(_evt_name)
    for _consumer in _evt_info["consumers"]:
        EVENTS_BY_CONSUMER.setdefault(_consumer, []).append(_evt_name)


# ── App Consumers ──
_raw_consumers = _load("consumers.yaml")

def _convert_consumers(raw):
    """Convert YAML consumers back to the tuple-based format generators expect."""
    result = {}
    for svc, apps in raw.items():
        result[svc] = [(a["app"], a["screen"]) for a in apps]
    return result

APP_CONSUMERS = _convert_consumers(_raw_consumers)


# ── App Titles ──
APP_TITLES = _load("app-titles.yaml")


# ── Actors ──
ACTORS = _load("actors.yaml")

# Build reverse index: which services reference which actors
ACTOR_SERVICE_USAGE = {}
for (_caller, _method, _path), _targets in CROSS_SERVICE_CALLS.items():
    for _t in _targets:
        _label = _t[1]
        if _label in ACTORS:
            ACTOR_SERVICE_USAGE.setdefault(_label, set()).add(_caller)

for _svc, _apps in APP_CONSUMERS.items():
    for _app_name, _ in _apps:
        if _app_name in ACTORS:
            ACTOR_SERVICE_USAGE.setdefault(_app_name, set()).add(_svc)


# ── Applications ──
_raw_apps = _load("applications.yaml")

def _convert_applications(raw):
    """Convert YAML applications back to the tuple-based format generators expect."""
    result = {}
    for app_id, app_info in raw.items():
        app_data = {}
        for key, val in app_info.items():
            if key == "screens":
                screens = {}
                for screen_name, screen_info in val.items():
                    screen_data = {"description": screen_info["description"]}
                    steps = []
                    for s in screen_info["steps"]:
                        steps.append((
                            s["alias"],
                            s["label"],
                            s.get("service"),  # None for external systems
                            s["action"],
                            s.get("method"),   # None for external systems
                            s.get("path"),     # None for external systems
                            s.get("async", False),
                        ))
                    screen_data["steps"] = steps
                    screens[screen_name] = screen_data
                app_data["screens"] = screens
            else:
                app_data[key] = val
        result[app_id] = app_data
    return result

APPLICATIONS = _convert_applications(_raw_apps)


# ── Solutions by Service ──
# Build a mapping: service_name -> list of solutions affecting that service
# Sources: tickets.yaml (components) + capability-changelog.yaml (solution metadata)

_tickets_data = _load("tickets.yaml")
_changelog_data = _load("capability-changelog.yaml")

# Build solution metadata from changelog
_SOLUTION_META = {}
for _entry in (_changelog_data or {}).get("entries", []):
    _SOLUTION_META[_entry["solution"]] = {
        "ticket": _entry["ticket"],
        "date": str(_entry.get("date", "")),
        "summary": _entry.get("summary", ""),
        "capabilities": [c["id"] for c in _entry.get("capabilities", [])],
    }

# Build service -> solutions mapping from tickets
SOLUTIONS_BY_SERVICE = {}
for _t in (_tickets_data or {}).get("tickets", []):
    _sol = _t.get("solution")
    if not _sol:
        continue
    _meta = _SOLUTION_META.get(_sol, {})
    _sol_info = {
        "folder": _sol,
        "ticket": _t["key"],
        "summary": _t.get("summary", _meta.get("summary", "")),
        "date": _meta.get("date", ""),
        "capabilities": _meta.get("capabilities", []),
    }
    for _comp in _t.get("components", []):
        SOLUTIONS_BY_SERVICE.setdefault(_comp, []).append(_sol_info)

# Sort each service's solutions by date (newest first)
for _svc in SOLUTIONS_BY_SERVICE:
    SOLUTIONS_BY_SERVICE[_svc].sort(key=lambda s: s["date"], reverse=True)


# ── Delivery Status ──
_raw_delivery = _load("delivery-status.yaml")

DELIVERY_STATUS = _raw_delivery.get("services", {})
DELIVERY_WAVES = _raw_delivery.get("waves", {})


# ── Pipeline Registry ──
_raw_pipelines = _load("pipeline-registry.yaml")

PIPELINE_REGISTRY = _raw_pipelines
PIPELINE_REPO_URL = _raw_pipelines.get("repository", {}).get("base_url", "")
PIPELINE_AZURE = _raw_pipelines.get("azure", {})
PIPELINE_PORTAL_LINKS = _raw_pipelines.get("portal_links", {})
PIPELINE_PER_SERVICE = _raw_pipelines.get("pipelines", {}).get("per-service", {})
PIPELINE_GLOBAL = _raw_pipelines.get("pipelines", {}).get("global", {})
