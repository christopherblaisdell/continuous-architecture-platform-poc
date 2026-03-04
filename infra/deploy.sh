#!/usr/bin/env bash
# ===========================================================================
# Deploy Azure Infrastructure for Documentation Site
# ===========================================================================
# Prerequisites:
#   - Azure CLI installed and authenticated (az login)
#   - Contributor role on the target subscription
#
# Usage:
#   ./infra/deploy.sh                    # Deploy prod (default)
#   ./infra/deploy.sh dev                # Deploy dev
#   RESOURCE_GROUP=my-rg ./infra/deploy.sh  # Custom resource group
# ===========================================================================

set -euo pipefail

ENVIRONMENT="${1:-prod}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESOURCE_GROUP="${RESOURCE_GROUP:-rg-cap-docs-${ENVIRONMENT}}"
LOCATION="${LOCATION:-eastus2}"
PARAM_FILE="${SCRIPT_DIR}/parameters/${ENVIRONMENT}.bicepparam"

echo "======================================================================"
echo " Continuous Architecture Platform — Documentation Infrastructure"
echo "======================================================================"
echo " Environment:    ${ENVIRONMENT}"
echo " Resource Group: ${RESOURCE_GROUP}"
echo " Location:       ${LOCATION}"
echo " Parameters:     ${PARAM_FILE}"
echo "======================================================================"

# Validate parameter file exists
if [[ ! -f "${PARAM_FILE}" ]]; then
  echo "ERROR: Parameter file not found: ${PARAM_FILE}"
  echo "Available environments: prod, dev"
  exit 1
fi

# Create resource group if it does not exist
echo ""
echo "--- Creating resource group (if needed) ---"
az group create \
  --name "${RESOURCE_GROUP}" \
  --location "${LOCATION}" \
  --tags project=continuous-architecture-platform component=documentation environment="${ENVIRONMENT}" \
  --output table

# Deploy Bicep template
echo ""
echo "--- Deploying Bicep template ---"
DEPLOYMENT_OUTPUT=$(az deployment group create \
  --resource-group "${RESOURCE_GROUP}" \
  --template-file "${SCRIPT_DIR}/main.bicep" \
  --parameters "${PARAM_FILE}" \
  --output json)

# Extract outputs
DEFAULT_HOSTNAME=$(echo "${DEPLOYMENT_OUTPUT}" | jq -r '.properties.outputs.defaultHostname.value')
SITE_URL=$(echo "${DEPLOYMENT_OUTPUT}" | jq -r '.properties.outputs.siteUrl.value')
STATIC_WEB_APP_ID=$(echo "${DEPLOYMENT_OUTPUT}" | jq -r '.properties.outputs.staticWebAppId.value')
SWA_NAME=$(echo "${PARAM_FILE}" | xargs grep staticWebAppName | head -1 | awk -F"'" '{print $2}')

echo ""
echo "======================================================================"
echo " Deployment Complete"
echo "======================================================================"
echo " Site URL:        ${SITE_URL}"
echo " Hostname:        ${DEFAULT_HOSTNAME}"
echo " Resource ID:     ${STATIC_WEB_APP_ID}"
echo "======================================================================"

# Retrieve deployment token for GitHub Actions
echo ""
echo "--- Retrieving deployment token ---"
DEPLOYMENT_TOKEN=$(az staticwebapp secrets list \
  --name "${SWA_NAME:-swa-cap-docs-${ENVIRONMENT}}" \
  --query "properties.apiKey" \
  --output tsv 2>/dev/null || echo "FAILED — retrieve manually")

if [[ "${DEPLOYMENT_TOKEN}" != "FAILED — retrieve manually" ]]; then
  echo ""
  echo "====================================================================="
  echo " IMPORTANT: Add this as a GitHub repository secret"
  echo "====================================================================="
  echo " Secret name:  AZURE_STATIC_WEB_APPS_API_TOKEN"
  echo " Secret value: ${DEPLOYMENT_TOKEN}"
  echo ""
  echo " GitHub CLI:   gh secret set AZURE_STATIC_WEB_APPS_API_TOKEN --body \"${DEPLOYMENT_TOKEN}\""
  echo "====================================================================="
else
  echo ""
  echo " Could not retrieve token automatically. Run:"
  echo "   az staticwebapp secrets list --name swa-cap-docs-${ENVIRONMENT} --query 'properties.apiKey' -o tsv"
fi
