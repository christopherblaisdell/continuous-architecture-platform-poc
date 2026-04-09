// ===========================================================================
// Azure AI POC — Ephemeral BYOK proof infrastructure
// Deploys: Azure OpenAI with pay-per-token model (scales to zero)
// Tear down: az group delete --name rg-novatrek-ai-poc --yes --no-wait
// ===========================================================================

targetScope = 'resourceGroup'

@description('Azure region')
param location string = 'eastus2'

@description('Unique suffix for resource names')
param nameSuffix string = 'poc'

var tags = {
  project: 'continuous-architecture-platform'
  component: 'ai-byok-poc'
  environment: 'ephemeral'
  purpose: 'option-d-validation'
}

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

output openaiEndpoint string = openai.outputs.endpoint
output openaiResourceId string = openai.outputs.resourceId
output openaiName string = openai.outputs.name
output teardownCommand string = 'az group delete --name ${resourceGroup().name} --yes --no-wait'
