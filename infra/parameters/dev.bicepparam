using '../main.bicep'

// ===========================================================================
// Development Parameters — Continuous Architecture Platform Documentation
// ===========================================================================

param staticWebAppName = 'swa-cap-docs-dev'

param location = 'eastus2'

param skuName = 'Free'

param repositoryUrl = 'https://github.com/christopherblaisdell/continuous-architecture-platform-poc-2'

param repositoryBranch = 'develop'

param tags = {
  environment: 'development'
}
