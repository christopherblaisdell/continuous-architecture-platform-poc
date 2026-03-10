using '../platform.bicep'

// ===========================================================================
// Production Parameters — NovaTrek Adventures Platform
// ===========================================================================
// Production-grade with larger database, Standard Service Bus, Redis,
// and higher budget thresholds.
// ===========================================================================

param environment = 'prod'
param location = 'eastus2'

// All services deployed (update as waves complete)
param servicesToDeploy = []

// Database
param postgresAdminPassword = '' // Set via --parameters or env var at deploy time

// Features
param deployRedis = true
param deployServiceBus = true
param deployBudget = true
param budgetAmount = 200
param budgetStartDate = '2026-04-01'
