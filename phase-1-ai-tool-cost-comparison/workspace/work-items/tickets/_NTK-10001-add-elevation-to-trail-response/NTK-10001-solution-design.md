<!-- CONFLUENCE-PUBLISH -->

# NTK-10001 - Solution Design: Add Elevation Data to Trail Response

| Field | Value |
|-------|-------|
| Version | 1.0 |
| Date | 2024-04-15 |
| Author | Morgan Rivera |
| Status | APPROVED |
| Ticket | NTK-10001 |

## Problem Statement

The GET /trails/{trail_id} and GET /trails endpoints in svc-trail-management return trail metadata including distance and estimated duration, but do not include elevation gain and loss data. This data is required by ranger staff and trip planning tools to assess trail difficulty and provide gear recommendations. The elevation data already exists in the database but is not mapped to the API response.

## Solution Overview

Add `elevation_gain_meters` and `elevation_loss_meters` as nullable numeric fields to the `TrailResponseDto`. These fields will be mapped from the existing `elevation_gain_m` and `elevation_loss_m` columns in the `trails` database table via the `TrailMapper`. No database migration is required. The Swagger/OpenAPI specification will be updated to document the new fields.

This is an additive-only change with no impact on existing consumers.

## Impacted Components

| Component | Change Type | Risk |
|-----------|------------|------|
| svc-trail-management | DTO field addition, mapper update, Swagger update | Low |

## Changes Required

### 1 - TrailResponseDto Update

Add two new nullable fields to the Trail response DTO:

- `elevation_gain_meters` (BigDecimal, nullable)
- `elevation_loss_meters` (BigDecimal, nullable)

### 2 - TrailMapper Update

Map the existing database columns `elevation_gain_m` and `elevation_loss_m` to the new DTO fields in the TrailMapper class.

### 3 - Swagger/OpenAPI Specification Update

Add the two new fields to the Trail schema definition in the OpenAPI spec with appropriate descriptions and data types.

### 4 - Unit Test Update

Update existing TrailMapper and controller unit tests to verify the new fields are correctly mapped and returned in the API response.

## Deployment Notes

- **Backward Compatible**: Yes. This is an additive change only. No existing fields are modified or removed.
- **Database Migration**: None required. Data already exists in the trails table.
- **Feature Flag**: Not required. Safe to deploy directly.
- **Rollback**: Standard rollback procedure. Removing the fields from the DTO would revert to previous behavior.
- **Consumer Notification**: Not required. Additive fields do not break existing consumers.
