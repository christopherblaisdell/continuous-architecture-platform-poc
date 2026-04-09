// ===========================================================================
// Azure AI POC — Ephemeral BYOK proof infrastructure
// Deploys: Azure OpenAI + Azure AI Search (Basic) + Storage Account
// Tear down: az group delete --name rg-novatrek-ai-poc --yes --no-wait
// ===========================================================================

targetScope = 'resourceGroup'

@description('Azure region for OpenAI and Storage')
param location string = 'eastus2'

@description('Azure region for AI Search (eastus2 may be capacity-constrained)')
param searchLocation string = 'eastus'

@description('Unique suffix for resource names')
param nameSuffix string = 'poc'

var tags = {
  project: 'continuous-architecture-platform'
  component: 'ai-byok-poc'
  environment: 'ephemeral'
  purpose: 'option-d-validation'
}

// --- Azure OpenAI ---
module openai 'modules/azure-openai.bicep' = {
  name: 'openai-${nameSuffix}'
  params: {
    accountName: 'oai-novatrek-${nameSuffix}'
    location: location
    tags: tags
    deployments: [
      {
        name: 'gpt-4o'
        modelName: 'gpt-4o'
        modelVersion: '2024-11-20'
        skuName: 'Standard'
        skuCapacity: 10 // 10K TPM — minimal, pay-per-token, scales to zero when idle
      }
    ]
  }
}

// --- Azure AI Search (Basic tier, semantic ranker enabled) ---
module search 'modules/azure-search.bicep' = {
  name: 'search-${nameSuffix}'
  params: {
    searchName: 'srch-novatrek-${nameSuffix}'
    location: searchLocation
    tags: tags
    skuName: 'basic'
    semanticSearchEnabled: true
  }
}

// --- Storage Account (Blob container for architecture content staging) ---
module storage 'modules/azure-storage.bicep' = {
  name: 'storage-${nameSuffix}'
  params: {
    storageAccountName: 'stnovatrek${nameSuffix}'
    location: location
    tags: tags
    containerName: 'architecture-content'
  }
}

// --- RBAC: Grant AI Search managed identity read access to Blob Storage ---
// Storage Blob Data Reader role
resource searchBlobReader 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid('stnovatrek${nameSuffix}', 'srch-novatrek-${nameSuffix}', '2a2b9908-6ea1-4ae2-8e65-a410df84e7d1')
  scope: resourceGroup()
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '2a2b9908-6ea1-4ae2-8e65-a410df84e7d1')
    principalId: search.outputs.principalId
    principalType: 'ServicePrincipal'
  }
}

// --- Outputs ---
output openaiEndpoint string = openai.outputs.endpoint
output openaiResourceId string = openai.outputs.resourceId
output openaiName string = openai.outputs.name
output searchEndpoint string = search.outputs.endpoint
output searchName string = search.outputs.name
output storageBlobEndpoint string = storage.outputs.blobEndpoint
output storageAccountName string = storage.outputs.name
output storageConnectionString string = storage.outputs.connectionString
output teardownCommand string = 'az group delete --name ${resourceGroup().name} --yes --no-wait'
