#!/usr/bin/env bash
# ===========================================================================
# Deploy Ephemeral Azure AI POC for BYOK Validation
# ===========================================================================
# Deploys: Azure OpenAI + Azure AI Search (Basic) + Storage Account
# Scales to zero: GlobalStandard deployment = pay-per-token only
# Tear down:      az group delete --name rg-novatrek-ai-poc --yes --no-wait
#
# Usage:
#   ./infra/deploy-ai-poc.sh          # Deploy
#   ./infra/deploy-ai-poc.sh teardown # Destroy everything
# ===========================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESOURCE_GROUP="rg-novatrek-ai-poc"
LOCATION="eastus2"
SEARCH_LOCATION="eastus"

if [[ "${1:-deploy}" == "teardown" ]]; then
  echo "Tearing down AI POC resources..."
  az group delete --name "${RESOURCE_GROUP}" --yes --no-wait
  echo "Resource group deletion initiated (async). Resources will be fully removed in ~5 minutes."
  exit 0
fi

echo "======================================================================"
echo " BYOK Context Injection — Full Infrastructure Deployment"
echo "======================================================================"
echo " Resource Group: ${RESOURCE_GROUP}"
echo " Location:       ${LOCATION}"
echo " Components:     Azure OpenAI + AI Search (Basic) + Storage Account"
echo " Cost model:     ~\$91/month (OpenAI pay-per-token + Search \$73 + Storage ~\$0.24)"
echo " Tear down:      ./infra/deploy-ai-poc.sh teardown"
echo "======================================================================"

# Register required providers (idempotent)
echo ""
echo "--- Registering resource providers ---"
az provider register --namespace Microsoft.CognitiveServices --wait 2>/dev/null || true
az provider register --namespace Microsoft.Search --wait 2>/dev/null || true
az provider register --namespace Microsoft.Storage --wait 2>/dev/null || true

# Create dedicated resource group (ephemeral — easy to delete)
echo ""
echo "--- Creating resource group ---"
az group create \
  --name "${RESOURCE_GROUP}" \
  --location "${LOCATION}" \
  --tags project=continuous-architecture-platform component=ai-byok-poc environment=ephemeral \
  --output table

# Deploy Bicep template (all resources)
echo ""
echo "--- Deploying all resources (OpenAI + AI Search + Storage) ---"
DEPLOYMENT_OUTPUT=$(az deployment group create \
  --resource-group "${RESOURCE_GROUP}" \
  --template-file "${SCRIPT_DIR}/ai-poc.bicep" \
  --parameters location="${LOCATION}" searchLocation="${SEARCH_LOCATION}" \
  --query 'properties.outputs' \
  --output json)

ENDPOINT=$(echo "${DEPLOYMENT_OUTPUT}" | python3 -c "import sys,json; print(json.load(sys.stdin)['openaiEndpoint']['value'])")
RESOURCE_NAME=$(echo "${DEPLOYMENT_OUTPUT}" | python3 -c "import sys,json; print(json.load(sys.stdin)['openaiName']['value'])")
SEARCH_ENDPOINT=$(echo "${DEPLOYMENT_OUTPUT}" | python3 -c "import sys,json; print(json.load(sys.stdin)['searchEndpoint']['value'])")
SEARCH_NAME=$(echo "${DEPLOYMENT_OUTPUT}" | python3 -c "import sys,json; print(json.load(sys.stdin)['searchName']['value'])")
STORAGE_BLOB_ENDPOINT=$(echo "${DEPLOYMENT_OUTPUT}" | python3 -c "import sys,json; print(json.load(sys.stdin)['storageBlobEndpoint']['value'])")
STORAGE_ACCOUNT_NAME=$(echo "${DEPLOYMENT_OUTPUT}" | python3 -c "import sys,json; print(json.load(sys.stdin)['storageAccountName']['value'])")

# Retrieve API keys
echo ""
echo "--- Retrieving API keys ---"
API_KEY=$(az cognitiveservices account keys list \
  --resource-group "${RESOURCE_GROUP}" \
  --name "${RESOURCE_NAME}" \
  --query 'key1' \
  --output tsv)

SEARCH_ADMIN_KEY=$(az search admin-key show \
  --resource-group "${RESOURCE_GROUP}" \
  --service-name "${SEARCH_NAME}" \
  --query 'primaryKey' \
  --output tsv)

STORAGE_CONNECTION_STRING=$(az storage account show-connection-string \
  --resource-group "${RESOURCE_GROUP}" \
  --name "${STORAGE_ACCOUNT_NAME}" \
  --query 'connectionString' \
  --output tsv)

echo ""
echo "======================================================================"
echo " DEPLOYMENT COMPLETE"
echo "======================================================================"
echo ""
echo " --- Azure OpenAI ---"
echo " Endpoint:  ${ENDPOINT}"
echo " API Key:   ${API_KEY:0:8}...${API_KEY: -4} (truncated)"
echo " Model:     gpt-4o"
echo ""
echo " --- Azure AI Search ---"
echo " Endpoint:  ${SEARCH_ENDPOINT}"
echo " Admin Key: ${SEARCH_ADMIN_KEY:0:8}...${SEARCH_ADMIN_KEY: -4} (truncated)"
echo " SKU:       Basic (\$73/mo)"
echo ""
echo " --- Storage Account ---"
echo " Blob URL:  ${STORAGE_BLOB_ENDPOINT}"
echo " Account:   ${STORAGE_ACCOUNT_NAME}"
echo ""
echo " Quick test (OpenAI):"
echo "   curl ${ENDPOINT}openai/deployments/gpt-4o/chat/completions?api-version=2024-10-01-preview \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -H 'api-key: <KEY>' \\"
echo "     -d '{\"messages\":[{\"role\":\"user\",\"content\":\"Hello\"}]}'"
echo ""
echo " Tear down: ./infra/deploy-ai-poc.sh teardown"
echo "======================================================================"
