#!/usr/bin/env bash
# ===========================================================================
# Deploy Ephemeral Azure AI POC for BYOK Validation
# ===========================================================================
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

if [[ "${1:-deploy}" == "teardown" ]]; then
  echo "Tearing down AI POC resources..."
  az group delete --name "${RESOURCE_GROUP}" --yes --no-wait
  echo "Resource group deletion initiated (async). Resources will be fully removed in ~5 minutes."
  exit 0
fi

echo "======================================================================"
echo " Option D — BYOK Validation POC"
echo "======================================================================"
echo " Resource Group: ${RESOURCE_GROUP}"
echo " Location:       ${LOCATION}"
echo " Cost model:     Pay-per-token only (scales to zero)"
echo " Tear down:      ./infra/deploy-ai-poc.sh teardown"
echo "======================================================================"

# Register required providers (idempotent)
echo ""
echo "--- Registering resource providers ---"
az provider register --namespace Microsoft.CognitiveServices --wait 2>/dev/null || true

# Create dedicated resource group (ephemeral — easy to delete)
echo ""
echo "--- Creating resource group ---"
az group create \
  --name "${RESOURCE_GROUP}" \
  --location "${LOCATION}" \
  --tags project=continuous-architecture-platform component=ai-byok-poc environment=ephemeral \
  --output table

# Deploy Bicep template
echo ""
echo "--- Deploying Azure OpenAI (pay-per-token, scales to zero) ---"
DEPLOYMENT_OUTPUT=$(az deployment group create \
  --resource-group "${RESOURCE_GROUP}" \
  --template-file "${SCRIPT_DIR}/ai-poc.bicep" \
  --parameters location="${LOCATION}" \
  --query 'properties.outputs' \
  --output json)

ENDPOINT=$(echo "${DEPLOYMENT_OUTPUT}" | python3 -c "import sys,json; print(json.load(sys.stdin)['openaiEndpoint']['value'])")
RESOURCE_NAME=$(echo "${DEPLOYMENT_OUTPUT}" | python3 -c "import sys,json; print(json.load(sys.stdin)['openaiName']['value'])")

# Retrieve API key
echo ""
echo "--- Retrieving API key ---"
API_KEY=$(az cognitiveservices account keys list \
  --resource-group "${RESOURCE_GROUP}" \
  --name "${RESOURCE_NAME}" \
  --query 'key1' \
  --output tsv)

echo ""
echo "======================================================================"
echo " DEPLOYMENT COMPLETE"
echo "======================================================================"
echo " Endpoint:  ${ENDPOINT}"
echo " API Key:   ${API_KEY:0:8}...${API_KEY: -4} (truncated)"
echo " Model:     gpt-4o-mini"
echo " Cost:      \$0 when idle — pay only for tokens consumed"
echo ""
echo " BYOK Registration (GitHub Enterprise Cloud admin):"
echo "   Endpoint URL: ${ENDPOINT}"
echo "   API Key:      (use full key from az cognitiveservices account keys list)"
echo "   Model ID:     gpt-4o-mini"
echo ""
echo " Quick test:"
echo "   curl ${ENDPOINT}openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-10-01-preview \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -H 'api-key: <KEY>' \\"
echo "     -d '{\"messages\":[{\"role\":\"user\",\"content\":\"Hello\"}]}'"
echo ""
echo " Tear down: ./infra/deploy-ai-poc.sh teardown"
echo "======================================================================"
