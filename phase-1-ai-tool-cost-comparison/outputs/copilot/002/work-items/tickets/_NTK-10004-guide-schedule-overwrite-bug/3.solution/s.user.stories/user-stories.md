# NTK-10004: User Stories

## US-001 Guide Schedule Integrity During Optimization

**As a** trail guide,
**I want** my manually entered availability exceptions, training blocks, and notes to be preserved when the scheduling system runs optimization,
**so that** I do not have to re-enter my schedule information after every optimization cycle.

### Acceptance Criteria

- Vacation blocks entered through the Guide Portal survive nightly and on-demand optimization
- Medical restriction notes remain intact after optimization
- Certification records are not modified by the scheduling optimization
- The guide sees the same schedule information before and after optimization runs (for fields they manage)

---

## US-002 Guide Medical Safety Preservation

**As a** guide with a medical restriction,
**I want** my medical notes to remain in the system regardless of scheduling activities,
**so that** I am never assigned to a trail that conflicts with my current medical clearance.

### Acceptance Criteria

- Medical restriction notes (e.g., "No high-altitude trails until medical clearance") are never removed by system processes
- If a medical note is present, the guide is not assigned to conflicting activities
- Any attempt to overwrite medical notes by a system process is logged and prevented

---

## US-003 Operations Concurrent Schedule Safety

**As an** operations manager triggering optimization across regions,
**I want** the system to detect and handle concurrent schedule modifications safely,
**so that** guides assigned to cross-region trails do not have their schedules corrupted by competing optimization runs.

### Acceptance Criteria

- When two optimization processes attempt to update the same guide's schedule simultaneously, one succeeds and the other is notified of the conflict
- The conflicted optimization process retries with the current schedule data
- No schedule data is silently lost due to concurrent writes
- The system logs all conflict events for operational visibility

---

## US-004 Guide Schedule Audit Trail

**As an** operations manager investigating a scheduling issue,
**I want** to see a clear audit trail of what changed a guide's schedule and when,
**so that** I can trace the source of any schedule discrepancies.

### Acceptance Criteria

- Each schedule modification records who or what made the change (e.g., "scheduling-orchestrator", "guide-portal")
- The timestamp of each modification is recorded
- The version number of the schedule is visible, showing how many modifications have occurred
