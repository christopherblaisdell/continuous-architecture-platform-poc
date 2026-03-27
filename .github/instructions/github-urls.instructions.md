---
description: "GitHub URL formatting rules — ensure all GitHub links are correct and don't include unnecessary fragments or incorrect paths"
applyTo: "**"
---

# GitHub URL Formatting Rules

When providing GitHub URLs in responses:

## Repository Secrets Page
- **Correct format**: `https://github.com/{owner}/{repo}/settings/secrets/actions`
- **Incorrect**: Any URL with `#2`, fragments, or incorrect paths
- **Example**: `https://github.com/christopherblaisdell/continuous-architecture-platform-poc-2/settings/secrets/actions`

## General Rules
- Always use the full path without fragments unless specifically needed
- Verify the URL structure matches GitHub's official documentation
- Do not include anchor links (#section) unless the user specifically requests a section
- Test URLs mentally before providing them

## Common Mistakes to Avoid
- Adding `#2` or other fragments to settings URLs
- Using incorrect paths like `/settings/secrets` instead of `/settings/secrets/actions`
- Providing links to non-existent pages

This instruction ensures all GitHub URLs provided are accurate and functional.