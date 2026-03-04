# Infrastructure — Azure Static Web Apps for MkDocs Material

This directory contains the Infrastructure as Code (IaC) for deploying the Continuous Architecture Platform documentation site to Azure Static Web Apps.

## Architecture

```
┌──────────────────┐     ┌──────────────────────┐     ┌─────────────────────────┐
│  Git Push (main) │────>│  GitHub Actions       │────>│  Azure Static Web App   │
│                  │     │  1. checkout           │     │  - Global CDN           │
│                  │     │  2. pip install        │     │  - Free SSL/TLS         │
│                  │     │  3. mkdocs build       │     │  - Custom Domain        │
│                  │     │  4. deploy to Azure    │     │  - Azure AD Auth (opt)  │
└──────────────────┘     └──────────────────────┘     └─────────────────────────┘

┌──────────────────┐     ┌──────────────────────┐
│  Pull Request    │────>│  GitHub Actions       │────>  Staging Preview URL
│                  │     │  (same build steps)   │      (auto-created per PR)
└──────────────────┘     └──────────────────────┘
```

## Prerequisites

- Azure CLI installed and authenticated (`az login`)
- Contributor role on the target Azure subscription
- GitHub repository with Actions enabled
- `jq` installed (for deploy script output parsing)

## Quick Start

### 1. Deploy Azure Infrastructure

```bash
# Deploy production environment
./infra/deploy.sh

# Deploy development environment
./infra/deploy.sh dev

# Custom resource group
RESOURCE_GROUP=my-custom-rg ./infra/deploy.sh
```

The script will:
1. Create a resource group (`rg-cap-docs-prod` or `rg-cap-docs-dev`)
2. Deploy the Azure Static Web App via Bicep
3. Output the deployment token

### 2. Configure GitHub Secret

After deployment, add the deployment token as a GitHub repository secret:

```bash
# Using GitHub CLI (recommended)
gh secret set AZURE_STATIC_WEB_APPS_API_TOKEN --body "<token-from-deploy-output>"

# Or manually via GitHub UI:
# Settings > Secrets and variables > Actions > New repository secret
# Name: AZURE_STATIC_WEB_APPS_API_TOKEN
# Value: <token from deploy script output>
```

### 3. Push to Main

Once the secret is configured, any push to `main` that touches documentation files will automatically build and deploy the site.

### 4. Local Preview

```bash
# Install dependencies
pip install -r requirements-docs.txt

# Start local dev server
mkdocs serve

# Open http://localhost:8000
```

## File Structure

```
infra/
  main.bicep                  # Azure Static Web App resource definition
  deploy.sh                   # One-command deployment script
  parameters/
    prod.bicepparam           # Production parameters
    dev.bicepparam            # Development parameters

mkdocs.yml                    # MkDocs Material site configuration (repo root)
requirements-docs.txt         # Python dependencies for MkDocs (repo root)
staticwebapp.config.json      # Azure SWA routing and headers (repo root)
docs/
  index.md                    # Site landing page

.github/workflows/
  docs-deploy.yml             # CI/CD pipeline for build + deploy
```

## Environments

| Environment | Resource Group | Static Web App | Branch |
|-------------|---------------|----------------|--------|
| Production | `rg-cap-docs-prod` | `swa-cap-docs-prod` | `main` |
| Development | `rg-cap-docs-dev` | `swa-cap-docs-dev` | `develop` |
| PR Staging | (uses prod SWA) | Auto-created per PR | PR branch |

## Cost

| Component | Monthly Cost |
|-----------|-------------|
| Azure Static Web Apps (Free tier) | $0 |
| Custom domain + SSL | $0 (included) |
| GitHub Actions CI/CD | $0 (included in GitHub plan) |
| MkDocs Material (MIT core) | $0 |
| **Total** | **$0** |

Standard tier ($9/month) is available if Azure AD authentication or larger bandwidth is needed.

## Decision Record

Platform selection rationale is documented in [ADR-002: Documentation Publishing Platform](../decisions/ADR-002-documentation-publishing-platform.md).
