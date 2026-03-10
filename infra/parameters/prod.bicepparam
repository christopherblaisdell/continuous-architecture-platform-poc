using '../main.bicep'

// ===========================================================================
// Production Parameters — Continuous Architecture Platform Documentation
// ===========================================================================

param staticWebAppName = 'swa-cap-docs-prod'

param location = 'eastus2'

param skuName = 'Free'

param repositoryUrl = 'https://github.com/christopherblaisdell/continuous-architecture-platform-poc-2'

param repositoryBranch = 'main'

param tags = {
  environment: 'production'
}

param customDomain = 'novatrek.cc'

// ---------------------------------------------------------------------------
// Vikunja Ticketing
// ---------------------------------------------------------------------------
param deployVikunja = true
param containerAppsEnvName = 'cae-cap-ticketing-prod'
param vikunjaAppName = 'ca-vikunja-prod'
param vikunjaJwtSecret = 'novatrek-poc-jwt-secret-2025'
param logAnalyticsWorkspaceName = 'cae-cap-ticketing-prod-logs'
