// ===========================================================================
// Azure Infrastructure for Continuous Architecture Platform Documentation
// Deploys: Azure Static Web App for MkDocs Material site
// ===========================================================================
// Usage:
//   az deployment group create \
//     --resource-group <rg-name> \
//     --template-file infra/main.bicep \
//     --parameters infra/parameters/prod.bicepparam
// ===========================================================================

targetScope = 'resourceGroup'

// ---------------------------------------------------------------------------
// Parameters
// ---------------------------------------------------------------------------

@description('Name of the Static Web App resource')
param staticWebAppName string

@description('Azure region for the Static Web App')
@allowed([
  'centralus'
  'eastus2'
  'eastasia'
  'westeurope'
  'westus2'
])
param location string = 'eastus2'

@description('SKU for Azure Static Web Apps. Free tier is sufficient for architecture docs.')
@allowed([
  'Free'
  'Standard'
])
param skuName string = 'Free'

@description('GitHub repository URL for the documentation source')
param repositoryUrl string

@description('Branch to deploy from')
param repositoryBranch string = 'main'

@description('Tags to apply to all resources')
param tags object = {}

@description('Custom domain to configure (optional, leave empty to skip)')
param customDomain string = ''

@description('Deploy Vikunja ticketing instance (requires Container Apps)')
param deployVikunja bool = false

@description('Name for the Container Apps Environment (used when deployVikunja is true)')
param containerAppsEnvName string = 'cae-cap-${uniqueString(resourceGroup().id)}'

@description('Name for the Vikunja Container App (used when deployVikunja is true)')
param vikunjaAppName string = 'ca-vikunja'

// ---------------------------------------------------------------------------
// Variables
// ---------------------------------------------------------------------------

var defaultTags = union({
  project: 'continuous-architecture-platform'
  component: 'documentation'
  managedBy: 'bicep'
  framework: 'mkdocs-material'
}, tags)

// ---------------------------------------------------------------------------
// Azure Static Web App
// ---------------------------------------------------------------------------

resource staticWebApp 'Microsoft.Web/staticSites@2023-12-01' = {
  name: staticWebAppName
  location: location
  tags: defaultTags
  sku: {
    name: skuName
    tier: skuName
  }
  properties: {
    repositoryUrl: repositoryUrl
    branch: repositoryBranch
    buildProperties: {
      // MkDocs builds to 'site/' directory — GitHub Actions handles the build
      // so we skip the Azure-managed build and deploy the pre-built output
      skipGithubActionWorkflowGeneration: true
    }
  }
}

// ---------------------------------------------------------------------------
// Custom Domain (optional)
// ---------------------------------------------------------------------------

resource customDomainResource 'Microsoft.Web/staticSites/customDomains@2023-12-01' = if (!empty(customDomain)) {
  parent: staticWebApp
  name: customDomain
  properties: {}
}

// ---------------------------------------------------------------------------
// Outputs
// ---------------------------------------------------------------------------

@description('The default hostname of the Static Web App')
output defaultHostname string = staticWebApp.properties.defaultHostname

@description('The URL of the deployed documentation site')
output siteUrl string = 'https://${staticWebApp.properties.defaultHostname}'

@description('The resource ID of the Static Web App')
output staticWebAppId string = staticWebApp.id

@description('The API key for CI/CD deployment (retrieve via az CLI after deployment)')
output deploymentTokenCommand string = 'az staticwebapp secrets list --name ${staticWebAppName} --query "properties.apiKey" -o tsv'

// ---------------------------------------------------------------------------
// Container Apps Environment (conditional — for Vikunja)
// ---------------------------------------------------------------------------

module containerAppsEnv 'modules/container-apps-env.bicep' = if (deployVikunja) {
  name: 'container-apps-env'
  params: {
    name: containerAppsEnvName
    location: location
    tags: defaultTags
  }
}

// ---------------------------------------------------------------------------
// Vikunja Ticketing (conditional)
// ---------------------------------------------------------------------------

module vikunja 'modules/vikunja.bicep' = if (deployVikunja) {
  name: 'vikunja'
  params: {
    name: vikunjaAppName
    location: location
    containerAppsEnvId: deployVikunja ? containerAppsEnv.outputs.id : ''
    tags: defaultTags
  }
}

@description('Vikunja URL (empty if not deployed)')
output vikunjaUrl string = deployVikunja ? vikunja.outputs.url : ''
