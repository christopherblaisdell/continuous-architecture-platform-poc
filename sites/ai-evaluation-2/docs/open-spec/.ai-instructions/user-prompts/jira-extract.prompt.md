---
description: "Extract JIRA tickets to markdown. List assigned tickets or extract a specific ticket with full details, comments, and metadata."
argument-hint: "Ticket key (e.g. UPT-193359) or leave blank to list assigned tickets"
tools: [execute, read, edit, search]
---

# JIRA Ticket Extraction

Extract JIRA tickets to well-formatted markdown using browser cookie authentication.

## Script Location

The extraction script is at a fixed path:
```
/Users/christopherblaisdell/Documents/cwb-roo-workspace-3/scripts/jira/working_jira_client.py
```

## Prerequisites

- Python 3 with `browser_cookie3` and `requests` installed
- User must be logged into JIRA in Chrome browser (cookies are used for auth)
- Set `JIRA_BASE_URL` env var if not using the default instance

## Procedure

### If no ticket key provided (list assigned tickets):

1. Run the script with no arguments:
   ```bash
   python3 /Users/christopherblaisdell/Documents/cwb-roo-workspace-3/scripts/jira/working_jira_client.py
   ```
2. Present the list of assigned tickets to the user
3. Ask which ticket(s) they want to extract

### If a ticket key is provided:

1. Run the script with the ticket key:
   ```bash
   python3 /Users/christopherblaisdell/Documents/cwb-roo-workspace-3/scripts/jira/working_jira_client.py <TICKET-KEY>
   ```
2. The script generates `<TICKET-KEY>.ticket.report.md` in the current directory
3. Read the generated report file
4. Ask the user where they want to place the file in their workspace (suggest the standard ticket folder structure if one exists)
5. Move the file to the chosen location

## Output Format

The script generates a comprehensive markdown report containing:
- Ticket summary and metadata (key, status, priority, type, project)
- Reporter and assignee
- Full description (converted from Atlassian Document Format to markdown)
- All comments with authors and timestamps
- Direct JIRA URL

## Error Handling

If authentication fails, instruct the user to:
1. Open Chrome browser
2. Navigate to their JIRA instance and log in
3. Retry the command
