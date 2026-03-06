#!/usr/bin/env python3
"""Update condensed PowerPoint with vector database cost slide"""

import re

# Read both files
with open('generate-powerpoint-full.py', 'r') as f:
    full_content = f.read()

with open('generate-powerpoint.py.bak', 'r') as f:
    condensed_content = f.read()

# Extract the new add_cost_slide function from full version
cost_func_match = re.search(r'(def add_cost_slide\(prs\):.*?)(?=\ndef [a-z_]+\()', full_content, re.DOTALL)

if cost_func_match:
    new_cost_func = cost_func_match.group(1).rstrip()
    
    # Replace old add_cost_slide in condensed version
    condensed_updated = re.sub(
        r'def add_cost_slide\(prs\):.*?(?=\ndef [a-z_]+\()',
        new_cost_func + '\n\n',
        condensed_content,
        flags=re.DOTALL,
        count=1
    )
    
    with open('generate-powerpoint.py', 'w') as f:
        f.write(condensed_updated)
    
    print("✓ Updated add_cost_slide function with vector database emphasis")
else:
    print("✗ Could not extract cost function from full version")
