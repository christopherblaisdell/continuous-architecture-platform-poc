#!/usr/bin/env python3
"""Refactor generators to use load_metadata instead of inline data structures."""
import os

SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))


def refactor_microservice_generator():
    """Replace inline data in generate-microservice-pages.py with import."""
    path = os.path.join(SCRIPTS_DIR, "generate-microservice-pages.py")
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    start_idx = None
    for i, line in enumerate(lines):
        if line.strip() == "# Domain Configuration":
            start_idx = i
            break

    end_idx = None
    for i, line in enumerate(lines):
        if "C4 Context Diagram Generation" in line:
            j = i - 1
            while j > 0 and lines[j].strip() in ("", "# " + "=" * 60):
                j -= 1
            end_idx = j + 1
            break

    if start_idx is None or end_idx is None:
        print(f"ERROR: Could not find boundaries (start={start_idx}, end={end_idx})")
        return False

    import_block = [
        "# -- Metadata loaded from YAML files (portal/docs/metadata/) --\n",
        "# Architects edit YAML, commit, push -- CI rebuilds automatically.\n",
        "# No need to edit this Python file for metadata changes.\n",
        "import sys\n",
        "sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\n",
        "from load_metadata import (  # noqa: E402\n",
        "    DOMAINS, ALL_SERVICES, LABEL_TO_SVC,\n",
        "    PCI_SERVICES, PCI_EXTERNALS, PCI_DATA_FLOWS, is_pci_flow,\n",
        "    DATA_STORES, CROSS_SERVICE_CALLS,\n",
        "    EVENT_CATALOG, EVENTS_BY_PRODUCER, EVENTS_BY_CONSUMER,\n",
        "    APP_CONSUMERS, APP_TITLES, ACTORS, ACTOR_SERVICE_USAGE,\n",
        ")\n",
        "\n",
        "# Pre-loaded endpoint summaries: (svc_name, METHOD, /path) -> summary\n",
        "ALL_ENDPOINT_SUMMARIES = {}\n",
        "\n",
        "\n",
        "def heading_slug(method, path, summary):\n",
        '    """Reproduce MkDocs heading anchor from: ### METHOD `/path` -- Summary"""\n',
        '    text = f"{method} {path} -- {summary}"\n',
        "    text = unicodedata.normalize('NFKD', text)\n",
        "    text = re.sub(r'[^\\w\\s-]', '', text).strip().lower()\n",
        "    return re.sub(r'[-\\s]+', '-', text)\n",
        "\n",
        "\n",
        "def endpoint_anchor(target_svc, target_method, target_path):\n",
        '    """Get the MkDocs heading anchor for a specific endpoint on a target service."""\n',
        "    summary = ALL_ENDPOINT_SUMMARIES.get((target_svc, target_method, target_path), \"\")\n",
        "    if not summary:\n",
        '        return ""\n',
        '    return "#" + heading_slug(target_method, target_path, summary)\n',
        "\n",
        "\n",
    ]

    new_lines = lines[:start_idx] + import_block + lines[end_idx:]

    with open(path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    print(f"  generate-microservice-pages.py: {len(lines)} -> {len(new_lines)} lines (removed {len(lines) - len(new_lines)})")
    return True


def refactor_application_generator():
    """Replace inline APPLICATIONS dict in generate-application-pages.py with import."""
    path = os.path.join(SCRIPTS_DIR, "generate-application-pages.py")
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    start_idx = None
    for i, line in enumerate(lines):
        if "Application Definitions" in line and line.strip().startswith("#"):
            if i > 0 and "====" in lines[i - 1]:
                start_idx = i - 1
            else:
                start_idx = i
            break

    if start_idx is None:
        print("ERROR: Could not find Application Definitions section")
        return False

    end_idx = None
    in_apps = False
    brace_depth = 0
    for i, line in enumerate(lines):
        if i < start_idx:
            continue
        if not in_apps and "APPLICATIONS = {" in line:
            in_apps = True
            brace_depth = line.count("{") - line.count("}")
            continue
        if in_apps:
            brace_depth += line.count("{") - line.count("}")
            if brace_depth <= 0:
                end_idx = i + 1
                while end_idx < len(lines) and lines[end_idx].strip() == "":
                    end_idx += 1
                break

    if end_idx is None:
        print(f"ERROR: Could not find end of APPLICATIONS dict (start={start_idx})")
        return False

    import_block = [
        "# -- Application metadata loaded from YAML (portal/docs/metadata/applications.yaml) --\n",
        "import sys\n",
        "sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\n",
        "from load_metadata import APPLICATIONS  # noqa: E402\n",
        "\n",
    ]

    new_lines = lines[:start_idx] + import_block + lines[end_idx:]

    with open(path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    print(f"  generate-application-pages.py: {len(lines)} -> {len(new_lines)} lines (removed {len(lines) - len(new_lines)})")
    return True


if __name__ == "__main__":
    print("Refactoring generators to use load_metadata...")
    ok1 = refactor_microservice_generator()
    ok2 = refactor_application_generator()
    if ok1 and ok2:
        print("\nDone! All generators now load metadata from YAML files.")
    else:
        print("\nSome refactoring failed. Check errors above.")
