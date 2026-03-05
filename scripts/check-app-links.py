#!/usr/bin/env python3
"""Check which application step endpoints match spec paths."""
import yaml, os, re

specs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "portal", "docs", "specs")
summaries = {}
for f in sorted(os.listdir(specs_dir)):
    if not f.endswith(".yaml"):
        continue
    svc = f.replace(".yaml", "")
    with open(os.path.join(specs_dir, f)) as fh:
        spec = yaml.safe_load(fh)
    for path, pi in spec.get("paths", {}).items():
        for m in ["get", "post", "put", "patch", "delete"]:
            if m in pi:
                summaries[(svc, m.upper(), path)] = pi[m].get("summary", "")

exec_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "portal", "scripts", "generate-application-pages.py")
with open(exec_path) as f:
    content = f.read()

pattern = r'\("(\w+)",\s*"([^"]+)",\s*"(svc-[^"]+)",\s*"[^"]+",\s*"(GET|POST|PUT|PATCH|DELETE)",\s*"([^"]+)"'
matches = re.findall(pattern, content)

seen = set()
broken = []
ok = []
for alias, label, svc, method, path in matches:
    key = (svc, method, path)
    if key in seen:
        continue
    seen.add(key)
    s = summaries.get(key)
    if s is None:
        broken.append(key)
    else:
        ok.append(key)

print(f"\nOK: {len(ok)} endpoints matched")
print(f"BROKEN: {len(broken)} endpoints have no matching spec entry\n")

for svc, method, path in sorted(broken):
    # Find closest match
    close = [(s, m, p) for (s, m, p) in summaries if s == svc and m == method]
    close_paths = [p for (s, m, p) in close]
    print(f"  BROKEN: {svc:40s} {method:6s} {path}")
    if close_paths:
        print(f"          Available {method} paths: {close_paths}")
    print()
