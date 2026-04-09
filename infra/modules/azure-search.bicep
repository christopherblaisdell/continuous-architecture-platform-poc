@description('Name of the Azure AI Search resource')
param searchName string

@description('Azure region')
param location string = resourceGroup().location

@description('SKU — basic for POC ($73/mo, 2GB, 15 indexes)')
@allowed(['free', 'basic', 'standard'])
param skuName string = 'basic'

@description('Number of replicas (1 for POC)')
param replicaCount int = 1

@description('Number of partitions (1 for POC)')
param partitionCount int = 1

@description('Tags for all resources')
param tags object = {}

@description('Enable semantic ranker (required for Foundry IQ agentic retrieval)')
param semanticSearchEnabled bool = true

resource search 'Microsoft.Search/searchServices@2024-06-01-preview' = {
  name: searchName
  location: location
  sku: {
    name: skuName
  }
  properties: {
    replicaCount: replicaCount
    partitionCount: partitionCount
    hostingMode: 'default'
    publicNetworkAccess: 'enabled'
    semanticSearch: semanticSearchEnabled ? 'standard' : 'disabled'
  }
  tags: tags
  identity: {
    type: 'SystemAssigned'
  }
}

@description('Azure AI Search endpoint URL')
output endpoint string = 'https://${search.name}.search.windows.net'

@description('Resource ID')
output resourceId string = search.id

@description('Search service name')
output name string = search.name

@description('Managed identity principal ID (for RBAC assignments)')
output principalId string = search.identity.principalId
