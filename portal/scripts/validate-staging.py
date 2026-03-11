#!/usr/bin/env python3
"""Validate staging files: check for title collisions and orphaned parents."""
import re, glob

titles = set()
parents = set()
for f in glob.glob("portal/confluence/**/*.md", recursive=True):
    with open(f) as fh:
        for line in fh:
            m = re.match(r"<!-- Title: (.+?) -->", line)
            if m:
                titles.add(m.group(1))
            m = re.match(r"<!-- Parent: (.+?) -->", line)
            if m:
                parents.add(m.group(1))

parents.discard("NovaTrek Architecture Portal")
orphans = parents - titles

if orphans:
    for o in sorted(orphans):
        print("ORPHANED PARENT:", repr(o))
else:
    print("All parent references valid.")

print("Titles:", len(titles), "| Unique parents:", len(parents))
