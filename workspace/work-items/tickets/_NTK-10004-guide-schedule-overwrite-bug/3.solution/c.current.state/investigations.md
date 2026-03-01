# Current State Investigation - NTK-10004: Guide Schedule Overwrite Bug

## Investigation Status: In Progress

Last updated: 2026-02-27

---

## 1. Elastic Search Query for Error Patterns

The following query was used to identify schedule overwrite events in production logs:

```json
{
  "query": {
    "bool": {
      "must": [
        { "match": { "service.name": "svc-scheduling-orchestrator" } },
        { "match": { "http.request.method": "PUT" } },
        { "wildcard": { "url.path": "/api/v1/guides/*/schedule" } }
      ],
      "filter": [
        { "range": { "@timestamp": { "gte": "2026-01-28", "lte": "2026-02-27" } } }
      ]
    }
  },
  "sort": [{ "@timestamp": "desc" }],
  "size": 200
}
```

**Results**: 847 PUT requests to guide schedule endpoints in the last 30 days. Cross-referencing with svc-guide-management PATCH/POST logs for manual adjustments, 23 guides had manual data in their schedule documents within 24 hours before an orchestrator PUT overwrote it.

## 2. Source Code Review: svc-scheduling-orchestrator

### GuideScheduleTransformer Class

Located in `src/services/optimization/transformers/GuideScheduleTransformer.ts`. Key findings:

- The `transformToOptimized()` method constructs an `OptimizedGuideSchedule` object containing only:
  - `assignedTrails: TrailAssignment[]`
  - `regionId: string`
  - `shiftPattern: ShiftPattern`
  - `effectiveDate: string`
- This DTO is serialized and sent as the full body of a PUT request
- No logic reads existing manual fields or merges them into the output
- The `SchedulePublisher` class calls `guideManagementClient.putSchedule(guideId, optimizedSchedule)` with no awareness of existing data

### Optimization Pipeline Flow

1. `ScheduleOptimizer.optimize(regionId)` reads all guide schedules for the region
2. Runs constraint-satisfaction algorithm to assign guides to trails
3. Passes results through `GuideScheduleTransformer.transformToOptimized()`
4. `SchedulePublisher.publish()` writes each guide schedule via PUT
5. No pre-write read or merge step exists in the pipeline

## 3. API Analysis: svc-guide-management

The svc-guide-management OpenAPI spec defines two update endpoints:

| Endpoint | Method | Semantics | Used By |
|----------|--------|-----------|---------|
| `/api/v1/guides/{guideId}/schedule` | PUT | Full replacement | svc-scheduling-orchestrator |
| `/api/v1/guides/{guideId}/schedule` | PATCH | Partial update (merge) | Guide Portal (frontend) |

The PATCH endpoint performs a deep merge, preserving fields not included in the request body. If the orchestrator used PATCH instead of PUT, manual fields would be preserved.

Neither endpoint implements optimistic locking. No `ETag`, `If-Match`, or `revision` field is present in request or response headers.

## 4. Timeline of Reported Incidents

| Date       | Region      | Guide(s) Affected | Data Lost | Trigger |
|------------|-------------|-------------------|-----------|---------|
| 2026-02-14 | Cascadia    | 3 guides          | Vacation blocks, medical note | Nightly optimization |
| 2026-02-14 | Sierra      | 1 guide (Jake Moreno) | Vacation block (Feb 22-28) | Ad-hoc optimization |
| 2026-02-22 | Appalachian | 1 guide           | Certification notes | Weekend optimization |

All three incidents follow the same pattern: manual data existed before optimization, was absent after.

## 5. Root Cause Hypothesis

The svc-scheduling-orchestrator optimization pipeline transforms guide data through a series of stages that model only orchestrator-owned fields. The `GuideScheduleTransformer` constructs a new DTO from optimization results, discarding any fields not in its schema. This is analogous to an ETL pipeline that strips unrecognized attributes during transformation - the data is not intentionally deleted, but it is not carried forward because the transformer has no knowledge of it.

The secondary race condition (concurrent regional optimizations) compounds the problem but is not the primary cause. Even a single optimization run will erase manual data.

**Root cause**: Data ownership violation. The orchestrator performs full-document replacement on a shared data structure it only partially owns.

## 6. Next Steps

- [ ] **Load test validation**: Simulate concurrent multi-region optimization to quantify race condition frequency and confirm whether data corruption occurs beyond the known overwrite
- [ ] **Propose solution options**: Two candidates under consideration:
  1. **Field-level merge**: Switch orchestrator from PUT to PATCH, sending only orchestrator-owned fields
  2. **Document separation**: Split guide schedule into two documents - one owned by orchestrator, one by guide management - with a read-time merge
- [ ] **Draft solution design**: Once load test results are in, select approach and write solution design document
- [ ] **Stakeholder review**: Present findings and proposed solution to Operations and Engineering leads
