# Scenario 05: Complex Cross-Service Design from Scratch

## Scenario Overview

| Property | Value |
|----------|-------|
| **Scenario ID** | SC-05 |
| **Task** | Full Cross-Service Solution Design for Complex Feature |
| **Estimated Monthly Frequency** | 2 per month |
| **Complexity** | Very High |
| **Duration Target** | 90-180 minutes |
| **Skills Tested** | Multi-service analysis, API design, diagramming, decision analysis, security awareness |

## Pre-conditions

- All 19 Swagger specs available in `services/` directory
- All source code available in `source-code/` directory
- Architecture standards (arc42, C4, MADR templates) available in workspace instructions
- This is a greenfield feature requiring a new orchestration flow

## Exact Prompt to Use


## Expected AI Actions

### Phase 1: Research and Analysis
2. Read Swagger specs for affected services:
   - `svc-check-in.yaml` -- current check-in flow
   - `svc-guest-profiles.yaml` -- guest data model
   - `svc-safety-compliance.yaml` -- safety requirements
   - `svc-reservations.yaml` -- reservation lookup
3. Read relevant source code:
   - CheckInController.java -- current check-in logic
   - GuestProfileService.java -- guest creation/lookup
4. Review architecture standards for templates and conventions

### Phase 2: Solution Design
   - Proposed new endpoint: POST /check-in/self-service/unregistered
   - Request schema (reservation lookup fields, identity verification)
   - Response schema (temporary guest profile, check-in confirmation)
   - Orchestration flow across 4 services
   - Error handling and edge cases

### Phase 3: Architecture Diagrams
6. Create/update PlantUML C4 component diagram showing:
   - New self-service check-in component
   - Interactions with guest-profiles, reservations, safety-compliance
   - Data flow direction and protocols
7. Create PlantUML sequence diagram showing:
   - Guest initiates self-service check-in
   - Reservation lookup by confirmation code
   - Identity verification step
   - Temporary guest profile creation
   - Safety compliance check
   - Check-in confirmation

### Phase 4: Architecture Decisions
8. Create ADR: Identity Verification Approach
   - Options: confirmation code only, confirmation + ID scan, confirmation + biometric
   - Decision with rationale
9. Create ADR: Temporary Guest Profiles
   - Options: full profile creation, temporary/ephemeral profile, linked-to-reservation profile
   - Decision with rationale
10. Create ADR: Orchestration Pattern
    - Options: choreography (events), orchestration (central coordinator), hybrid
    - Decision with rationale

### Phase 5: Impact and Risk
11. Create impact assessments for each affected service:
    - svc-check-in: new endpoint, new controller logic
    - svc-guest-profiles: temporary profile creation API
    - svc-reservations: reservation lookup by confirmation code
12. Create risk assessment document:
    - Data risk: temporary profiles and data retention
    - Operational risk: increased load on check-in flow

### Phase 6: User Stories
13. Create user stories covering:
    - Guest perspective: self-service check-in without pre-registration
    - Staff perspective: assisting guests who fail self-service
    - System perspective: handling edge cases (expired reservation, safety hold)

## What to Watch For

- Does the AI identify ALL four affected services without being told which ones?
- Is the new API endpoint design complete (not just a stub)?
- Are PlantUML diagrams syntactically valid and semantically accurate?
- Do ADR decisions have genuine options analysis (not just rubber-stamping one option)?
- Are impact docs correctly scoped to each individual service?
- Are risks realistic with actionable mitigations?
- Do user stories cover all three perspectives (guest, staff, system)?
- Are security considerations front and center (identity verification)?

## Quality Rubric

Score each criterion 1-5:

- [ ] **Service Discovery**: Identified ALL 4 impacted services correctly
- [ ] **API Design**: New API endpoint design is complete (request/response schemas)
- [ ] **Diagram Validity**: PlantUML diagrams are syntactically valid
- [ ] **ADR Quality**: Decisions follow MADR format with genuine options analysis
- [ ] **Impact Precision**: Impact docs correctly identify API contract changes per service
- [ ] **Risk Realism**: Risks are realistic and have actionable mitigations
- [ ] **Story Coverage**: User stories cover guest, staff, and system perspectives
- [ ] **Security Awareness**: Security considerations addressed (identity verification)

**Maximum Score**: 40

## Token Cost Tracking

| Metric | Roo+Kong | Copilot |
|--------|----------|---------|
| Input tokens | | |
| Output tokens | | |
| Total tokens | | |
| Tool calls count | | |
| Files read | | |
| Files created | | |
| Diagrams created | | |
| ADRs created | | |
| Impact docs created | | |
| Time to complete (min) | | |
| Quality score (/40) | | |
| Cost per run ($) | | |
| Estimated monthly cost ($) | | |

## Complexity Factors

This is the most demanding scenario because it requires:
- Reading and synthesizing 4+ Swagger specs simultaneously
- Designing a new API from requirements (not modifying existing)
- Creating multiple diagram types (C4 component + sequence)
- Making interconnected architecture decisions
- Assessing impact across service boundaries
- Thinking about security in a guest-facing context
- Maintaining consistency across 10+ generated documents

## Scoring Guidance

**Score 1-2**: AI generates generic or incomplete output, misses services, or produces invalid diagrams
**Score 3**: AI covers the basics but misses nuance (e.g., identifies services but not specific API changes)
**Score 4**: AI produces solid output with minor gaps (e.g., ADR options are reasonable but not deeply analyzed)
**Score 5**: AI produces production-ready output that could be presented to a review board

## Notes

- This scenario represents the highest-value architecture work
- A tool that scores well here justifies significant cost
- Watch for the AI's ability to maintain coherence across many related documents
- The total token cost for this scenario is the best predictor of overall monthly spend
- If time runs out, note what was completed -- partial completion is still informative
