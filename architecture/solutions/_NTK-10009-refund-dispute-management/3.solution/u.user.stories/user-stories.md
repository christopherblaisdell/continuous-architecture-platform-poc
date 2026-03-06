# User Stories — NTK-10009

## US-1: Guest Requests a Cancellation Refund

**As a** guest who needs to cancel an upcoming adventure,
**I want to** request a refund through the guest portal,
**So that** I receive the appropriate refund amount based on the cancellation policy.

### Acceptance Criteria

```gherkin
Given a guest with a reservation cancelling 48+ hours before the adventure
When the guest submits a refund request
Then the system auto-approves a 100% refund and notifies the guest

Given a guest with a reservation cancelling 24-48 hours before the adventure
When the guest submits a refund request
Then the system auto-approves a 50% refund and notifies the guest

Given a guest with a reservation cancelling less than 24 hours before the adventure
When the guest submits a refund request
Then the dispute is routed to agent review and the guest is notified of the review process
```

## US-2: Agent Reviews a Dispute

**As a** guest services agent,
**I want to** view my assigned dispute queue and resolve cases within my authority,
**So that** guest refund requests are handled efficiently and consistently.

### Acceptance Criteria

```gherkin
Given a dispute in UNDER_REVIEW status assigned to an agent
When the agent approves or denies the refund with a justification
Then the dispute is resolved, the refund is processed (if approved), and the guest is notified

Given a dispute that exceeds the agent's authority threshold
When the agent attempts to resolve it
Then the system blocks resolution and prompts escalation to a manager
```

## US-3: Manager Handles Escalated Disputes

**As a** guest services manager,
**I want to** review escalated disputes and make final refund decisions,
**So that** high-value and exception cases receive appropriate management oversight.

### Acceptance Criteria

```gherkin
Given an escalated dispute assigned to a manager
When the manager resolves it with a decision and justification
Then the dispute is resolved and the refund is processed according to the decision

Given a dispute requiring documentation
When the manager adds notes to the dispute record
Then the notes are preserved in the audit trail
```

## US-4: Guest Receives Status Updates

**As a** guest who submitted a refund request,
**I want to** receive email updates at each stage of the dispute process,
**So that** I know the status of my refund without having to contact guest services.

### Acceptance Criteria

```gherkin
Given a guest who submitted a dispute
When the dispute status changes (opened, under review, escalated, resolved)
Then the guest receives an email notification with the current status and next steps

Given a resolved dispute with an approved refund
When the guest receives the resolution notification
Then the email includes the refund amount and expected processing timeline
```

## US-5: Finance Auditor Reviews Refund Decisions

**As a** finance auditor,
**I want to** review the complete history of refund decisions with policy evaluations and justifications,
**So that** I can verify compliance with company refund policies.

### Acceptance Criteria

```gherkin
Given a resolved dispute
When an auditor views the dispute record
Then it shows the policy evaluation result, tier assignment, resolver identity, justification, and resolution outcome

Given a set of resolved disputes for a date range
When an auditor queries disputes by date
Then all disputes are returned with their full audit trail
```
