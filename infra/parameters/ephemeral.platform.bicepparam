using '../platform.bicep'

// ===========================================================================
// Ephemeral Parameters — NovaTrek Adventures Platform
// ===========================================================================
// Minimal configuration for PR-based preview environments.
// Short-lived, destroyed on PR close.
// ===========================================================================

param environment = 'ephemeral'
param location = 'eastus2'

// Only deploy services changed in the PR (set dynamically by CI)
param servicesToDeploy = []

// Database
param postgresAdminPassword = '' // Generated at deploy time by CI

// Minimal features — no Redis, no budget alerts
param deployRedis = false
param deployServiceBus = true
param deployBudget = false
param budgetAmount = 10
param budgetStartDate = '2026-04-01'
