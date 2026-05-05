# Global AI Tools Configuration Guide

This guide explains how to configure **Roo Code and VS Code** to use the source-controlled AI customizations from this repository. A single setup script handles everything.

## Quick Start

```bash
chmod +x .ai-customizations/setup-ai-tools.sh
./.ai-customizations/setup-ai-tools.sh
```

This one command sets up both tools. Run it once per machine.

## What the Setup Script Does

### 1. Roo Code
- Creates `~/.config/roo/` if it doesn't exist
- Symlinks `.ai-customizations/` to `~/.config/roo/ai-customizations`
- Creates `~/.config/roo/modes.yaml` with global mode definitions (if missing)

### 2. VS Code
- Creates `~/Library/Application Support/Code/User/prompts/` if it doesn't exist
- Symlinks each file in `.ai-customizations/user-prompts/` into that directory
- Supports `.prompt.md`, `.agent.md`, and `.instructions.md` files

## Architecture

```
This Repository (.ai-customizations/)
├── universal/                    # Standards loaded by ALL modes
├── methodologies/                # Workflow docs (4-phase, JIRA extraction, etc.)
├── standards/                    # Domain-specific standards
├── mode-customizations/          # Roo mode-specific instructions
├── user-prompts/                 # VS Code user-level prompt/agent/instruction files
│   └── jira-extract.prompt.md    #   → symlinked to VS Code user prompts dir
├── setup-ai-tools.sh             # One-time setup script
└── INDEX.md                      # Searchable index of everything
```

### Symlink Map

```
Source (this repo)                              Target (user-level config)
─────────────────                               ──────────────────────────
.ai-customizations/                          →  ~/.config/roo/ai-customizations
.ai-customizations/user-prompts/*.prompt.md  →  ~/Library/Application Support/Code/User/prompts/
.ai-customizations/user-prompts/*.agent.md   →  ~/Library/Application Support/Code/User/prompts/
```

### Shared Scripts

Scripts invoked by prompts and methodologies live in a fixed, known location:

```
/Users/christopherblaisdell/Documents/cwb-roo-workspace-3/scripts/jira/
└── working_jira_client.py    # JIRA ticket extraction (used by both tools)
```

Both the VS Code prompt (`jira-extract.prompt.md`) and the Roo methodology
(`methodologies/jira-extraction.md`) reference this same script path.

## How Each Tool Discovers Customizations

| Tool | What It Sees | How |
|------|-------------|-----|
| **Roo Code** | Methodologies, standards, mode instructions | Symlinked directory at `~/.config/roo/ai-customizations` |
| **VS Code** | `/` slash commands, agents, instructions | Individual file symlinks in `~/Library/Application Support/Code/User/prompts/` |
| **Both** | Shared scripts | Fixed path in `scripts/` directory of this repo |

## Adding New Customizations

### New VS Code prompt or agent
1. Create the file in `.ai-customizations/user-prompts/` (e.g., `my-task.prompt.md`)
2. Re-run `setup-ai-tools.sh` to create the symlink
3. Commit and push

### New Roo methodology or standard
1. Create the file in the appropriate directory (`methodologies/`, `standards/`, etc.)
2. Update `INDEX.md` with the new entry
3. No symlink re-run needed — Roo reads the directory through the existing symlink
4. Commit and push

### New shared script
1. Add the script to `scripts/` (e.g., `scripts/confluence/publish.py`)
2. Reference it from the relevant prompt and/or methodology
3. Commit and push

## Roo Modes Configuration Detail

The setup script creates `~/.config/roo/modes.yaml` with global mode definitions if it doesn't already exist. The modes.yaml content is embedded in the script itself. To update modes, edit the script and re-run it (or edit `~/.config/roo/modes.yaml` directly).

## Per-Project Overrides (Optional)

For each project where you want to ensure the same customizations are used, create a symlink to the master source:

```bash
# From any project directory
ln -s /Users/christopherblaisdell/Documents/cwb-roo-workspace-3/.ai-customizations .ai-customizations
```

## Benefits

1. **Single Source of Truth**: All customizations maintained in one Git repository
2. **No Drift**: Symlinks mean both tools always read the latest version
3. **Cross-Workspace**: Available from any VS Code workspace on this machine
4. **Cross-Tool**: Same underlying scripts serve multiple AI tools
5. **Version Controlled**: Full Git history for all customization changes
6. **One-Command Setup**: Run `setup-ai-tools.sh` once per machine

## Verification

Run the setup script — it includes built-in verification. Or manually:

```bash
# Check Roo symlink
ls -la ~/.config/roo/ai-customizations
# Should show: ai-customizations -> /Users/christopherblaisdell/Documents/cwb-roo-workspace-3/.ai-customizations

# Check VS Code prompts
ls -la ~/Library/Application\ Support/Code/User/prompts/
# Should show symlinked .prompt.md files

# Test JIRA script
python3 /Users/christopherblaisdell/Documents/cwb-roo-workspace-3/scripts/jira/working_jira_client.py --help 2>&1 || echo "Script found (no --help flag, but exists)"
```

## Troubleshooting

| Problem | Check |
|---------|-------|
| Roo not loading customizations | `ls -la ~/.config/roo/ai-customizations` — verify symlink is valid |
| VS Code `/` command not showing | `ls ~/Library/Application\ Support/Code/User/prompts/` — verify symlinks |
| JIRA script auth failure | Log into JIRA in Chrome browser, then retry |
| Customization not updating | Symlinks reference the source files — ensure you saved the source file |
| Conflicting `.roomodes` in project | Project-level `.roomodes` may override global modes |

## Maintenance Workflow

1. **Make changes** in the source repository:
   ```bash
   cd /Users/christopherblaisdell/Documents/cwb-roo-workspace-3
   # Edit files in .ai-customizations/
   ```

2. **Commit changes**:
   ```bash
   git add .ai-customizations/
   git commit -m "Update AI customization standards"
   ```

3. **Changes are immediately available** to all Roo instances (no restart required)

## Backup Recommendation

Since this is your single source of truth:

1. **Regular Git commits** to track changes
2. **Consider remote backup** (if security permits):
   ```bash
   # Create encrypted backup
   tar -czf - .ai-customizations | openssl enc -aes-256-cbc -out ai-customizations-backup.tar.gz.enc
   ```

---

This symlink-based approach ensures that your VS Code Roo installation always uses the same source-controlled customizations, maintaining consistency across all your development work.