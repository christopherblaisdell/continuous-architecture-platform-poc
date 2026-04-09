@description('Name of the Azure OpenAI resource')
param accountName string

@description('Azure region')
param location string = resourceGroup().location

@description('Model deployments to create')
param deployments deploymentConfig[]

@description('Tags for all resources')
param tags object = {}

type deploymentConfig = {
  @description('Deployment name (used as identifier)')
  name: string
  @description('Model name (e.g., gpt-4o-mini)')
  modelName: string
  @description('Model version')
  modelVersion: string
  @description('SKU name — Standard or GlobalStandard for pay-per-use (scales to zero)')
  skuName: string
  @description('SKU capacity (tokens-per-minute in thousands)')
  skuCapacity: int
}

// Azure OpenAI account — S0 is the only SKU, pay-per-use at the deployment level
resource openai 'Microsoft.CognitiveServices/accounts@2024-10-01' = {
  name: accountName
  location: location
  kind: 'OpenAI'
  sku: {
    name: 'S0'
  }
  properties: {
    customSubDomainName: accountName
    publicNetworkAccess: 'Enabled'
    disableLocalAuth: false
  }
  tags: tags
}

// Model deployments — GlobalStandard = pay-per-token, scales to zero
resource modelDeployments 'Microsoft.CognitiveServices/accounts/deployments@2024-10-01' = [
  for deployment in deployments: {
    parent: openai
    name: deployment.name
    sku: {
      name: deployment.skuName
      capacity: deployment.skuCapacity
    }
    properties: {
      model: {
        format: 'OpenAI'
        name: deployment.modelName
        version: deployment.modelVersion
      }
      versionUpgradeOption: 'OnceNewDefaultVersionAvailable'
    }
  }
]

@description('Azure OpenAI endpoint URL')
output endpoint string = openai.properties.endpoint

@description('Resource ID for key retrieval')
output resourceId string = openai.id

@description('Resource name')
output name string = openai.name
