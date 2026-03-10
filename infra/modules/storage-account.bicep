// ===========================================================================
// Azure Storage Account — NovaTrek
// Media assets (svc-media-gallery), database backups, general blob storage.
// ===========================================================================

@description('Storage account name (must be globally unique, 3-24 chars, lowercase alphanumeric)')
param name string

@description('Azure region')
param location string

@description('Tags to apply')
param tags object = {}

@description('SKU name')
@allowed(['Standard_LRS', 'Standard_GRS', 'Standard_ZRS'])
param skuName string = 'Standard_LRS'

@description('Blob containers to create')
param containers array = []

@description('Enable lifecycle management (move to cool/archive)')
param enableLifecyclePolicy bool = false

// ---------------------------------------------------------------------------
// Storage Account
// ---------------------------------------------------------------------------

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: name
  location: location
  tags: tags
  sku: { name: skuName }
  kind: 'StorageV2'
  properties: {
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
    supportsHttpsTrafficOnly: true
    accessTier: 'Hot'
  }
}

// ---------------------------------------------------------------------------
// Blob Service + Containers
// ---------------------------------------------------------------------------

resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2023-05-01' = {
  parent: storageAccount
  name: 'default'
}

resource blobContainers 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-05-01' = [for container in containers: {
  parent: blobService
  name: container
  properties: {
    publicAccess: 'None'
  }
}]

// ---------------------------------------------------------------------------
// Lifecycle Management Policy
// ---------------------------------------------------------------------------

resource lifecyclePolicy 'Microsoft.Storage/storageAccounts/managementPolicies@2023-05-01' = if (enableLifecyclePolicy) {
  parent: storageAccount
  name: 'default'
  properties: {
    policy: {
      rules: [
        {
          name: 'move-to-cool'
          enabled: true
          type: 'Lifecycle'
          definition: {
            filters: {
              blobTypes: ['blockBlob']
            }
            actions: {
              baseBlob: {
                tierToCool: {
                  daysAfterModificationGreaterThan: 30
                }
                tierToArchive: {
                  daysAfterModificationGreaterThan: 90
                }
              }
            }
          }
        }
      ]
    }
  }
}

// ---------------------------------------------------------------------------
// Outputs
// ---------------------------------------------------------------------------

@description('Storage account resource ID')
output id string = storageAccount.id

@description('Storage account name')
output name string = storageAccount.name

@description('Blob endpoint URL')
output blobEndpoint string = storageAccount.properties.primaryEndpoints.blob
