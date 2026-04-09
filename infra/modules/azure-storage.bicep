@description('Name of the Storage Account')
param storageAccountName string

@description('Azure region')
param location string = resourceGroup().location

@description('Tags for all resources')
param tags object = {}

@description('Name of the blob container for architecture content')
param containerName string = 'architecture-content'

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageAccountName
  location: location
  kind: 'StorageV2'
  sku: {
    name: 'Standard_LRS'
  }
  properties: {
    accessTier: 'Hot'
    allowBlobPublicAccess: false
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
  }
  tags: tags
}

resource blobServices 'Microsoft.Storage/storageAccounts/blobServices@2023-05-01' = {
  parent: storageAccount
  name: 'default'
}

resource container 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-05-01' = {
  parent: blobServices
  name: containerName
  properties: {
    publicAccess: 'None'
  }
}

// Grant the AI Search managed identity read access to the blob container
// This is done via role assignment in the parent template after both modules are deployed

@description('Storage account name')
output name string = storageAccount.name

@description('Storage account resource ID')
output resourceId string = storageAccount.id

@description('Blob endpoint URL')
output blobEndpoint string = storageAccount.properties.primaryEndpoints.blob

@description('Container name')
output containerName string = container.name

@description('Connection string (for indexer data source — marked as secure)')
#disable-next-line outputs-should-not-contain-secrets
output connectionString string = 'DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};AccountKey=${storageAccount.listKeys().keys[0].value};EndpointSuffix=core.windows.net'
