// ===========================================================================
// Azure Container Registry — NovaTrek Adventures
// Stores Docker images for all 22 microservices.
// ===========================================================================

@description('Name of the Container Registry (must be globally unique, alphanumeric only)')
param name string

@description('Azure region')
param location string

@description('SKU tier')
@allowed(['Basic', 'Standard', 'Premium'])
param sku string = 'Basic'

@description('Tags to apply')
param tags object = {}

@description('Enable admin user (disabled by default — use managed identity)')
param adminUserEnabled bool = false

// ---------------------------------------------------------------------------
// Container Registry
// ---------------------------------------------------------------------------

resource acr 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
  name: name
  location: location
  tags: tags
  sku: {
    name: sku
  }
  properties: {
    adminUserEnabled: adminUserEnabled
    policies: {
      retentionPolicy: {
        status: sku == 'Premium' ? 'enabled' : 'disabled'
        days: 30
      }
    }
  }
}

// ---------------------------------------------------------------------------
// Outputs
// ---------------------------------------------------------------------------

@description('Container Registry resource ID')
output id string = acr.id

@description('Container Registry name')
output name string = acr.name

@description('Container Registry login server (e.g., crnovatrekprod.azurecr.io)')
output loginServer string = acr.properties.loginServer
