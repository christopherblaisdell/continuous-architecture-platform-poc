using '../platform.bicep'

// ===========================================================================
// Ephemeral Parameters — NovaTrek Adventures Platform
// ===========================================================================
// Minimal configuration for PR-based preview environments.
// Uses Neon Serverless Postgres branch (instant copy-on-write clone).
// Short-lived, destroyed on PR close.
// ===========================================================================

param environment = 'ephemeral'
param location = 'eastus2'

// Only deploy services changed in the PR (set dynamically by CI)
param servicesToDeploy = []

// Database — Neon Serverless Postgres branch (set dynamically by CI)
param useExternalDatabase = true
param externalDatabaseHost = ''  // Set by CI: Neon branch endpoint
param externalDatabaseName = ''  // Set by CI: branch database name

// Minimal features — no Redis, no budget alerts
param deployRedis = false
param deployServiceBus = true
param deployBudget = false
param budgetAmount = 10
param budgetStartDate = '2026-04-01'
