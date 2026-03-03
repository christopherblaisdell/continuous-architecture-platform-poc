# NTK-10004: User Stories

## US-001: Preserve Guide Manual Adjustments

**As a** NovaTrek adventure guide,
**I want** my manually entered availability exceptions, training blocks, and special notes to survive schedule optimization cycles,
**So that** I do not have to repeatedly re-enter my information and my availability is correctly reflected in the system.

### Acceptance Criteria

- After a nightly optimization run, all manually entered availability exceptions remain in my profile
- After a region manager triggers on-demand optimization, my training day blocks are preserved
- Special notes (such as medical restrictions) are never removed by the optimization process
- I receive a notification if my schedule changes due to optimization, so I can verify the result

---

## US-002: Safety Restriction Preservation

**As an** operations manager,
**I want** guide medical restrictions and certification notes to be preserved during schedule optimization,
**So that** guides with altitude limits, equipment restrictions, or pending certifications are not assigned to inappropriate trails.

### Acceptance Criteria

- A guide with a note "No high-altitude trails until medical clearance" retains that note after optimization
- A guide with a vacation block is not assigned to any trail during that blocked period
- If a guide has a max-group-size override for a specific date, that override is honored by the optimization output

---

## US-003: Concurrent Optimization Conflict Detection

**As a** region manager triggering schedule optimization,
**I want** the system to detect and handle conflicting updates when multiple optimizations run simultaneously,
**So that** guides assigned to cross-region trails do not have their schedules silently overwritten by a competing optimization process.

### Acceptance Criteria

- If two optimization processes attempt to update the same guide schedule simultaneously, the second process receives a conflict notification
- The conflict is resolved through retry rather than silent overwrite
- An audit trail records which process modified the schedule and when

---

## US-004: Schedule Change Audit Trail

**As a** NovaTrek adventure guide,
**I want** to see who last modified my schedule and when,
**So that** I can understand why my schedule changed and raise concerns if the modification was unexpected.

### Acceptance Criteria

- My schedule shows the last modification date and the identity of the modifying system or user
- I can distinguish between changes made by the optimization system and changes I made through the Guide Portal
