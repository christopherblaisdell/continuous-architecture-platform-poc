# Fix Deploy Failures

**Date**: 2026-03-10
**Priority**: High
**Status**: Backlog

## Problem

Too many deploy failures across CI/CD pipelines. These need to be systematically identified, triaged, and fixed.

## Action Items

- [ ] Audit all GitHub Actions workflow runs and catalog recurring failures
- [ ] Identify root causes (flaky tests, misconfigured secrets, Bicep errors, SWA deploy issues, PlantUML timeouts, etc.)
- [ ] Fix each failure category and verify with a clean run
- [ ] Add failure alerting so regressions are caught immediately
- [ ] Consider adding retry logic for transient failures (network timeouts, rate limits)

## Context

This was flagged during the Azure implementation planning phase. Reliable CI/CD is a prerequisite for the incremental delivery plan outlined in `docs/AZURE-IMPLEMENTATION-PLAN.md`.
