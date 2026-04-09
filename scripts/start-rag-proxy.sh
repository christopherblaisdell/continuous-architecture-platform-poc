#!/usr/bin/env bash
# ===========================================================================
# Start the RAG Proxy with auto-configured Azure credentials
# ===========================================================================
# Retrieves all necessary keys from Azure and starts the proxy.
#
# Usage:
#   ./scripts/start-rag-proxy.sh          # Start proxy on port 8081
#   ./scripts/start-rag-proxy.sh 8082     # Start on custom port
# ===========================================================================

set -euo pipefail

RESOURCE_GROUP="rg-novatrek-ai-poc"
PORT="${1:-8081}"

echo "--- Retrieving Azure credentials ---"

# OpenAI endpoint and key
OPENAI_NAME=$(az cognitiveservices account list \
  --resource-group "${RESOURCE_GROUP}" \
  --query "[0].name" --output tsv)
export AZURE_OPENAI_ENDPOINT=$(az cognitiveservices account show \
  --resource-group "${RESOURCE_GROUP}" \
  --name "${OPENAI_NAME}" \
  --query "properties.endpoint" --output tsv)
export AZURE_OPENAI_API_KEY=$(az cognitiveservices account keys list \
  --resource-group "${RESOURCE_GROUP}" \
  --name "${OPENAI_NAME}" \
  --query "key1" --output tsv)

# Search endpoint and key
SEARCH_NAME=$(az search service list \
  --resource-group "${RESOURCE_GROUP}" \
  --query "[0].name" --output tsv)
export AZURE_SEARCH_ENDPOINT="https://${SEARCH_NAME}.search.windows.net"
export AZURE_SEARCH_API_KEY=$(az search admin-key show \
  --resource-group "${RESOURCE_GROUP}" \
  --service-name "${SEARCH_NAME}" \
  --query "primaryKey" --output tsv)

export AZURE_SEARCH_INDEX="architecture-content-index"
export RAG_PROXY_PORT="${PORT}"
export RAG_TOP_K=5

echo ""
echo "  OpenAI:  ${AZURE_OPENAI_ENDPOINT}"
echo "  Search:  ${AZURE_SEARCH_ENDPOINT}"
echo "  Index:   ${AZURE_SEARCH_INDEX}"
echo "  Port:    ${PORT}"
echo ""
echo "--- Starting RAG Proxy ---"
echo ""

python3 scripts/rag-proxy.py
