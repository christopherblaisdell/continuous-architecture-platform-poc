# Demo Baselines — NTK-10006 Real-Time Adventure Tracking

**Purpose**: Reference baselines for evaluating ECC-adapted Copilot prompts against NTK-10006.

**Ticket**: NTK-10006 — Real-Time Adventure Tracking and Emergency Alerting System
**Priority**: Critical
**Services**: svc-adventure-tracking (new), svc-emergency-response (new), svc-check-in, svc-notifications, svc-safety-compliance

---

## Baseline 1: Security Review

**Prompt**: `@workspace /security-review` → "Review the NTK-10006 solution design"

### Expected Findings (minimum quality bar)

| Severity | Finding | Category |
|----------|---------|----------|
| CRITICAL | Real-time GPS data is PII — location tracking of guests requires explicit consent and bounded retention | PII and Sensitive Data (OWASP A02) |
| HIGH | Two new services (svc-adventure-tracking, svc-emergency-response) need authentication and authorization schemes defined | Authentication and Identity (OWASP A07) |
| HIGH | WebSocket/streaming connections for real-time data need session binding and timeout policies | Cross-Service Communication (OWASP A08) |
| MEDIUM | Emergency alert broadcasting must not leak guest PII to unauthorized recipients | Authorization and Access Control (OWASP A01) |
| MEDIUM | GPS coordinate validation — out-of-range values could trigger false emergency alerts | Input Validation (OWASP A03) |
| LOW | New services must be added to cross-service-calls.yaml | Data Integrity and Ownership |

### Quality Indicators

- References ADR-005 (Pattern 3 default) for unknown adventure categories in tracking context
- Identifies GPS data as PII with retention concerns
- Checks data ownership: who owns tracking records? (should be svc-adventure-tracking)
- Considers insurance mandate compliance as a business logic check
- Produces severity-rated findings table with file path citations

---

## Baseline 2: Investigation

**Prompt**: `@workspace /investigation` → "Investigate NTK-10006"

### Expected Investigation Flow

1. **JIRA first**: Retrieves ticket via `python3 scripts/ticket-client.py --ticket NTK-10006`
2. **Elastic logs**: Searches for related errors in svc-check-in and svc-notifications (existing services that will integrate)
3. **GitLab MRs**: Checks for any related MRs in affected services
4. **Architecture context**: Reads OpenAPI specs for svc-check-in, svc-notifications, svc-safety-compliance

### Expected Findings

- NTK-10006 introduces two entirely new services — no existing specs to review
- Cross-service dependencies: svc-check-in must provide active adventure status, svc-notifications must support broadcast alerts
- Safety compliance integration: svc-safety-compliance must expose waiver and adventure classification data for tracking context
- No production logs for new services (they don't exist yet) — investigation pivots to dependency analysis

### Quality Indicators

- Follows strict tool sequence: ticket-client → Elastic → GitLab → architecture files
- Does not fabricate log data for non-existent services
- Identifies the ticket as a new-capability request (not a bug investigation)
- Documents which existing service endpoints need modification
- Produces structured report with evidence citations

---

## Baseline 3: Solution Design Verification

**Prompt**: `@workspace /solution-verification` → "Verify the NTK-10006 solution design"

### Expected Verification Checks

| Check | Expected Result |
|-------|----------------|
| Solution folder structure | `architecture/solutions/_NTK-10006-real-time-adventure-tracking/` exists but is incomplete (missing required subdirectories) |
| Master document | Missing — `NTK-10006-solution-design.md` not found |
| Requirements folder | Missing `1.requirements/` |
| Analysis folder | Missing `2.analysis/` |
| Capability changelog entry | Check `architecture/metadata/capability-changelog.yaml` for NTK-10006 |
| MADR decisions | Check for decisions in `3.solution/d.decisions/` |
| Impact assessments | Check for per-service impacts in `3.solution/i.impacts/` |
| Prior art search | Should find related tickets touching safety/tracking capabilities |
| Data ownership | Verify new services are registered as data owners in metadata |

### Quality Indicators

- Identifies that the solution design is largely incomplete (skeleton only)
- Does not fabricate content for missing files
- Cross-references the solution folder structure against copilot-instructions.md requirements
- Checks capability-changelog.yaml for NTK-10006 entries
- Runs prior-art discovery (ticket-client with capability filters)
- Produces a gap analysis showing what's missing vs. what's required

---

## Evaluation Criteria

For each demo, compare the AI output against these baselines:

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Tool usage sequence | 25% | Did it follow the prescribed tool order? |
| Evidence grounding | 25% | Are all claims supported by workspace evidence? |
| Domain rule application | 20% | Did it apply NovaTrek-specific rules (Pattern 3 default, data ownership, etc.)? |
| Output structure | 15% | Does the output match the expected format? |
| No fabrication | 15% | Did it avoid inventing data not present in the workspace? |
