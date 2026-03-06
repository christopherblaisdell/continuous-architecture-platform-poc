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

// Uncomment and set when custom domain is ready:
// param customDomain = 'docs.novatrek.example.com'

// ---------------------------------------------------------------------------
// Vikunja Ticketing
// ---------------------------------------------------------------------------
param deployVikunja = true
param containerAppsEnvName = 'cae-cap-ticketing-prod'
param vikunjaAppName = 'ca-vikunja-prod'
param vikunjaJwtSecret = 'novatrek-poc-jwt-secret-2025'
