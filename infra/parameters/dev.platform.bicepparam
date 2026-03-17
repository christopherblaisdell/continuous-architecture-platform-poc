using '../platform.bicep'

// ===========================================================================
// Development Parameters — NovaTrek Adventures Platform
// ===========================================================================
// Cheapest possible configuration for daily development and testing.
// Uses Neon Serverless Postgres (free tier, scale-to-zero) instead of
// Azure PostgreSQL Flexible Server. No Redis.
// ===========================================================================

param environment = 'dev'
param location = 'eastus2'
param postgresLocation = 'centralus'  // unused when useExternalDatabase = true

// Wave 0 — infrastructure only, no services deployed yet
param servicesToDeploy = []

// Database — Neon Serverless Postgres (free tier, scale-to-zero)
param useExternalDatabase = true
param externalDatabaseHost = 'ep-novatrek-dev.us-east-2.aws.neon.tech'  // Update after Neon project creation
param externalDatabaseName = 'novatrek_dev'

// Features
param deployRedis = false        // Enable at Wave 3 for svc-scheduling-orchestrator
param deployServiceBus = true
param deployBudget = true
param budgetAmount = 35
param budgetStartDate = '2026-04-01'
