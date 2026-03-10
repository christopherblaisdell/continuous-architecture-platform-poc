using '../platform.bicep'

// ===========================================================================
// Development Parameters — NovaTrek Adventures Platform
// ===========================================================================
// Cheapest possible configuration for daily development and testing.
// Single PostgreSQL instance, Basic Service Bus (queues), no Redis.
// ===========================================================================

param environment = 'dev'
param location = 'eastus2'
param postgresLocation = 'centralus'  // eastus/eastus2 restricted for PostgreSQL on this subscription

// Wave 0 — infrastructure only, no services deployed yet
param servicesToDeploy = []

// Database
param postgresAdminPassword = '' // Set via --parameters or env var at deploy time

// Features
param deployRedis = false        // Enable at Wave 3 for svc-scheduling-orchestrator
param deployServiceBus = true
param deployBudget = true
param budgetAmount = 50
param budgetStartDate = '2026-04-01'
