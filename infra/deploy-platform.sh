#!/usr/bin/env bash
# ===========================================================================
# Deploy NovaTrek Adventures Platform Infrastructure
# ===========================================================================
# Deploys the full microservices platform (ACA, PostgreSQL, Service Bus,
# Key Vault, Redis, ACR, monitoring) using Bicep.
#
# Prerequisites:
#   - Azure CLI installed and authenticated (az login)
#   - Contributor role on the target subscription
#
# Usage:
#   ./infra/deploy-platform.sh dev                    # Deploy dev
#   ./infra/deploy-platform.sh prod                   # Deploy prod
#   ./infra/deploy-platform.sh dev --what-if          # Preview changes
#   ./infra/deploy-platform.sh dev --teardown         # Destroy environment
# ===========================================================================

set -euo pipefail

ENVIRONMENT="${1:-dev}"
WHAT_IF="${2:-}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESOURCE_GROUP="rg-novatrek-${ENVIRONMENT}"
LOCATION="${LOCATION:-eastus2}"
PARAM_FILE="${SCRIPT_DIR}/parameters/${ENVIRONMENT}.platform.bicepparam"
TEMPLATE_FILE="${SCRIPT_DIR}/platform.bicep"

echo "======================================================================"
echo " NovaTrek Adventures — Platform Infrastructure"
echo "======================================================================"
echo " Environment:    ${ENVIRONMENT}"
echo " Resource Group: ${RESOURCE_GROUP}"
echo " Location:       ${LOCATION}"
echo " Parameters:     ${PARAM_FILE}"
echo " Template:       ${TEMPLATE_FILE}"
echo "======================================================================"

# ---------------------------------------------------------------------------
# Teardown mode
# ---------------------------------------------------------------------------

if [[ "${WHAT_IF}" == "--teardown" ]]; then
  echo ""
  echo "WARNING: This will DESTROY all resources in ${RESOURCE_GROUP}!"
  echo ""
  read -rp "Type 'DESTROY' to confirm: " confirm
  if [[ "${confirm}" != "DESTROY" ]]; then
    echo "Aborted."
    exit 1
  fi
  echo "Deleting resource group ${RESOURCE_GROUP}..."
  az group delete --name "${RESOURCE_GROUP}" --yes --no-wait
  echo "Deletion initiated (async). Resources will be removed within minutes."
  exit 0
fi

# ---------------------------------------------------------------------------
# Validate inputs
# ---------------------------------------------------------------------------

if [[ ! -f "${PARAM_FILE}" ]]; then
  echo "ERROR: Parameter file not found: ${PARAM_FILE}"
  echo "Available: dev.platform.bicepparam, prod.platform.bicepparam, ephemeral.platform.bicepparam"
  exit 1
fi

# ---------------------------------------------------------------------------
# Prompt for PostgreSQL password if not set
# ---------------------------------------------------------------------------

if [[ -z "${POSTGRES_ADMIN_PASSWORD:-}" ]]; then
  echo ""
  read -rsp "Enter PostgreSQL admin password: " POSTGRES_ADMIN_PASSWORD
  echo ""
fi

# ---------------------------------------------------------------------------
# Create resource group
# ---------------------------------------------------------------------------

echo ""
echo "--- Creating resource group (if needed) ---"
az group create \
  --name "${RESOURCE_GROUP}" \
  --location "${LOCATION}" \
  --tags project=novatrek-adventures environment="${ENVIRONMENT}" managedBy=bicep \
  --output table

# ---------------------------------------------------------------------------
# What-If mode
# ---------------------------------------------------------------------------

if [[ "${WHAT_IF}" == "--what-if" ]]; then
  echo ""
  echo "--- What-If Preview (no changes will be made) ---"
  az deployment group what-if \
    --resource-group "${RESOURCE_GROUP}" \
    --template-file "${TEMPLATE_FILE}" \
    --parameters "${PARAM_FILE}" \
    --parameters postgresAdminPassword="${POSTGRES_ADMIN_PASSWORD}"
  exit 0
fi

# ---------------------------------------------------------------------------
# Deploy
# ---------------------------------------------------------------------------

echo ""
echo "--- Deploying Platform Infrastructure ---"
DEPLOYMENT_NAME="deploy-$(date +%Y%m%d-%H%M%S)"

az deployment group create \
  --resource-group "${RESOURCE_GROUP}" \
  --template-file "${TEMPLATE_FILE}" \
  --parameters "${PARAM_FILE}" \
  --parameters postgresAdminPassword="${POSTGRES_ADMIN_PASSWORD}" \
  --name "${DEPLOYMENT_NAME}" \
  --output table

# ---------------------------------------------------------------------------
# Show outputs
# ---------------------------------------------------------------------------

echo ""
echo "======================================================================"
echo " Deployment Complete: ${DEPLOYMENT_NAME}"
echo "======================================================================"
echo ""

az deployment group show \
  --resource-group "${RESOURCE_GROUP}" \
  --name "${DEPLOYMENT_NAME}" \
  --query "properties.outputs" \
  --output table

echo ""
echo "Next steps:"
echo "  1. Push Docker images:  az acr login --name crnovatrek${ENVIRONMENT}"
echo "  2. Check services:      az containerapp list -g ${RESOURCE_GROUP} -o table"
echo "  3. View logs:           az containerapp logs show -n ca-svc-check-in -g ${RESOURCE_GROUP}"
echo "  4. Tear down:           ./infra/deploy-platform.sh ${ENVIRONMENT} --teardown"
