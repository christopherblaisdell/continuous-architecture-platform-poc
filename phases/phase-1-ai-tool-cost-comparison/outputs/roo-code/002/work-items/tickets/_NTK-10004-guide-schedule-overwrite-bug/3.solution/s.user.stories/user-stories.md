# NTK-10004: User Stories

## US-001: Preserve Manual Schedule Adjustments

**As a** NovaTrek adventure guide,
**I want** my manually entered availability exceptions, training blocks, and medical notes to persist across schedule optimization cycles,
**So that** I do not have to re-enter my information repeatedly and I am not assigned to trips that conflict with my availability or medical restrictions.

### Acceptance Criteria

- Vacation blocks entered through the Guide Portal remain after a nightly or on-demand optimization run
- Training day blocks remain after optimization
- Medical restriction notes remain after optimization
- Maximum group size overrides remain after optimization
- The guide receives no conflicting assignment notifications for dates they have blocked

---

## US-002: Safe Schedule Updates

**As an** operations manager triggering a schedule optimization,
**I want** the optimization process to update only scheduling-related fields without affecting guide-entered data,
**So that** I can confidently run optimizations without risking loss of safety-critical guide information.

### Acceptance Criteria

- Running an optimization for a region does not change any guide's personal notes, certifications, or availability exceptions
- If two optimizations run concurrently for overlapping regions, neither silently overwrites the other's changes
- The system clearly reports if a concurrent write conflict occurs

---

## US-003: Conflict Detection for Concurrent Updates

**As a** system administrator,
**I want** concurrent schedule modifications to be detected and handled gracefully,
**So that** simultaneous regional optimizations do not silently corrupt guide schedule data.

### Acceptance Criteria

- When two optimization processes attempt to update the same guide's schedule simultaneously, the system detects the conflict
- The conflicting update is retried automatically rather than silently overwriting
- If retries are exhausted, the failure is logged and an alert is raised

---

## US-004: Audit Trail for Schedule Changes

**As a** compliance officer,
**I want** an audit record of what changed a guide's schedule and when,
**So that** I can trace any data loss or incorrect assignment back to its source for safety compliance purposes.

### Acceptance Criteria

- Each schedule modification records who made the change and when
- The source of the change (optimization run, manual Guide Portal entry, API call) is identifiable
- Changes to safety-critical fields (medical notes, certifications) are logged with special visibility
