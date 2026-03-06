#!/usr/bin/env python3
"""Extract metadata from generator scripts into standalone YAML files.

This is a ONE-TIME migration script. After running, the YAML files become
the source of truth and this script can be deleted.
"""
import os
import sys
import yaml

# Add portal/scripts to path so we can import the generators
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
sys.path.insert(0, SCRIPT_DIR)

# We need to suppress the generator's main() from running
# Import the module data structures directly
import importlib.util

def load_module_data(module_path, module_name):
    """Load a Python module without executing its main()."""
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

# Load the microservice generator
micro_gen = load_module_data(
    os.path.join(SCRIPT_DIR, "generate-microservice-pages.py"),
    "generate_microservice_pages"
)

# Load the application generator
app_gen = load_module_data(
    os.path.join(SCRIPT_DIR, "generate-application-pages.py"),
    "generate_application_pages"
)

# Load the swagger generator
swagger_gen = load_module_data(
    os.path.join(SCRIPT_DIR, "generate-swagger-pages.py"),
    "generate_swagger_pages"
)

OUTPUT_DIR = os.path.join(WORKSPACE_ROOT, "portal", "docs", "metadata")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def write_yaml(filename, data, comment=""):
    """Write data to a YAML file."""
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w") as f:
        if comment:
            f.write(f"# {comment}\n")
            f.write(f"# Source of truth for portal generation.\n")
            f.write(f"# Edit this file, commit, push -- CI rebuilds the portal automatically.\n\n")
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True, width=120)
    print(f"  Written: {path}")


# ── 1. domains.yaml ──
print("Extracting domains...")
# Merge icon info from swagger generator
domains_data = {}
swagger_domains = getattr(swagger_gen, "DOMAINS", {})
for domain_name, domain_info in micro_gen.DOMAINS.items():
    domains_data[domain_name] = {
        "color": domain_info["color"],
        "icon": swagger_domains.get(domain_name, {}).get("icon", "cog"),
        "services": domain_info["services"],
    }
write_yaml("domains.yaml", domains_data, "Domain classification for NovaTrek microservices.")

# ── 2. label-to-svc.yaml ──
print("Extracting label mappings...")
write_yaml("label-to-svc.yaml", dict(micro_gen.LABEL_TO_SVC),
           "Mapping from short display labels to service names (used in PUML diagrams).")

# ── 3. pci.yaml ──
print("Extracting PCI configuration...")
pci_data = {
    "services": sorted(micro_gen.PCI_SERVICES),
    "externals": sorted(micro_gen.PCI_EXTERNALS),
    "data_flows": [list(pair) for pair in sorted(micro_gen.PCI_DATA_FLOWS)],
}
write_yaml("pci.yaml", pci_data, "PCI DSS compliance scope and sensitive data flow paths.")

# ── 4. data-stores.yaml ──
print("Extracting data stores (this is the big one)...")
# Convert tuples to lists for YAML serialization
def convert_data_stores(ds):
    result = {}
    for svc, info in ds.items():
        svc_data = {}
        for key, val in info.items():
            if key == "table_details":
                tables = {}
                for tbl_name, tbl_info in val.items():
                    tbl_data = {"description": tbl_info["description"]}
                    # Convert column tuples to dicts
                    tbl_data["columns"] = []
                    for col in tbl_info["columns"]:
                        col_dict = {"name": col[0], "type": col[1], "constraints": col[2]}
                        tbl_data["columns"].append(col_dict)
                    # Convert index tuples to dicts
                    tbl_data["indexes"] = []
                    for idx in tbl_info["indexes"]:
                        idx_dict = {"name": idx[0], "columns": idx[1]}
                        if len(idx) > 2:
                            idx_dict["type"] = idx[2]
                        tbl_data["indexes"].append(idx_dict)
                    tables[tbl_name] = tbl_data
                svc_data["table_details"] = tables
            elif key == "connection_pool":
                svc_data["connection_pool"] = dict(val)
            else:
                svc_data[key] = val
        result[svc] = svc_data
    return result

write_yaml("data-stores.yaml", convert_data_stores(micro_gen.DATA_STORES),
           "Database schemas, tables, and infrastructure for all 19 microservices.")

# ── 5. cross-service-calls.yaml ──
print("Extracting cross-service calls...")
def convert_cross_service_calls(csc):
    result = {}
    for (svc, method, path), targets in csc.items():
        svc_calls = result.setdefault(svc, {})
        endpoint_key = f"{method} {path}"
        calls = []
        for t in targets:
            call = {
                "alias": t[0],
                "label": t[1],
                "action": t[2],
                "async": t[3],
            }
            if t[4] is not None:
                call["target"] = {"method": t[4][0], "path": t[4][1]}
            calls.append(call)
        svc_calls[endpoint_key] = calls
    return result

write_yaml("cross-service-calls.yaml", convert_cross_service_calls(micro_gen.CROSS_SERVICE_CALLS),
           "Cross-service integration map showing which endpoints call which services.")

# ── 6. events.yaml ──
print("Extracting event catalog...")
def convert_events(ec):
    result = {}
    for evt_name, evt_info in ec.items():
        result[evt_name] = {
            "channel": evt_info["channel"],
            "producer": evt_info["producer"],
            "trigger": {"method": evt_info["trigger"][0], "path": evt_info["trigger"][1]},
            "consumers": evt_info["consumers"],
            "domain": evt_info["domain"],
            "summary": evt_info["summary"],
        }
    return result

write_yaml("events.yaml", convert_events(micro_gen.EVENT_CATALOG),
           "Domain event catalog -- channels, producers, consumers, and triggers.")

# ── 7. consumers.yaml ──
print("Extracting app consumers...")
def convert_consumers(ac):
    result = {}
    for svc, apps in ac.items():
        result[svc] = [{"app": a[0], "screen": a[1]} for a in apps]
    return result

write_yaml("consumers.yaml", convert_consumers(micro_gen.APP_CONSUMERS),
           "Per-service consuming application map (which app screens call which services).")

# ── 8. actors.yaml ──
print("Extracting actors...")
def convert_actors(actors):
    result = {}
    for name, info in actors.items():
        result[name] = dict(info)
    return result

write_yaml("actors.yaml", convert_actors(micro_gen.ACTORS),
           "External systems, frontend applications, human actors, and infrastructure.")

# ── 9. app-titles.yaml ──
print("Extracting app titles...")
write_yaml("app-titles.yaml", dict(micro_gen.APP_TITLES),
           "Display titles for frontend applications.")

# ── 10. applications.yaml ──
print("Extracting application definitions...")
def convert_applications(apps):
    result = {}
    for app_id, app_info in apps.items():
        app_data = {}
        for key, val in app_info.items():
            if key == "screens":
                screens = {}
                for screen_name, screen_info in val.items():
                    screen_data = {"description": screen_info["description"]}
                    steps = []
                    for step in screen_info["steps"]:
                        step_dict = {
                            "alias": step[0],
                            "label": step[1],
                        }
                        if step[2] is not None:
                            step_dict["service"] = step[2]
                        step_dict["action"] = step[3]
                        if step[4] is not None:
                            step_dict["method"] = step[4]
                        if step[5] is not None:
                            step_dict["path"] = step[5]
                        step_dict["async"] = step[6]
                        steps.append(step_dict)
                    screen_data["steps"] = steps
                    screens[screen_name] = screen_data
                app_data["screens"] = screens
            else:
                app_data[key] = val
        result[app_id] = app_data
    return result

write_yaml("applications.yaml", convert_applications(app_gen.APPLICATIONS),
           "Frontend application definitions with screen flows for user journey diagrams.")

print()
print(f"Done! All metadata extracted to {OUTPUT_DIR}/")
print("Files created:")
for f in sorted(os.listdir(OUTPUT_DIR)):
    if f.endswith(".yaml"):
        size = os.path.getsize(os.path.join(OUTPUT_DIR, f))
        print(f"  {f} ({size:,} bytes)")
