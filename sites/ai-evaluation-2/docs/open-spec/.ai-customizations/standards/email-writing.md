# Email Writing Standards

**Applicable Modes**: Solution Architect, Orchestrator, Ask, Corporate Compliance

## Overview

Professional email communication is critical for stakeholder engagement, project coordination, and enterprise communication. This document defines standards for crafting clear, actionable, and professional emails.

## Email Structure

### Standard Email Format

```
Subject: [PROJECT] - [TOPIC] - [ACTION REQUIRED/FYI]

Purpose: [One sentence stating the email's purpose]

[Main Content - organized with clear sections]

Action Items:
- [Action 1] - [Owner] - [Due Date]
- [Action 2] - [Owner] - [Due Date]

Next Steps:
- [Clear next steps]

[Professional closing]
```

### Subject Line Standards

#### Format
`[PROJECT/SYSTEM] - [TOPIC] - [URGENCY]`

#### Urgency Indicators
- `ACTION REQUIRED` - Response needed
- `URGENT` - Time-sensitive (use sparingly)
- `FYI` - Information only, no action needed
- `DECISION NEEDED` - Requires decision
- `REVIEW REQUEST` - Document/design review

#### Examples
- `[UDX] - Architecture Review Meeting - ACTION REQUIRED`
- `[OrderService] - Deployment Schedule - FYI`
- `[Security] - Vulnerability Assessment Results - URGENT`
- `[API Gateway] - Design Proposal - REVIEW REQUEST`

## Email Categories and Templates

### 1. Architecture Decision Communication

```
Subject: [PROJECT] - Architecture Decision: [DECISION TOPIC] - FYI

Purpose: Communicate the decision regarding [specific architecture choice].

Background:
We evaluated options for [technical challenge/requirement].

Decision:
We have decided to implement [chosen solution] based on:
- [Reason 1]
- [Reason 2]
- [Reason 3]

Impact:
- Development: [impact description]
- Timeline: [impact description]
- Resources: [impact description]

Implementation:
- Phase 1: [timeline and scope]
- Phase 2: [timeline and scope]

Please direct questions to [contact person].

Best regards,
[Name]
```

### 2. Stakeholder Update

```
Subject: [PROJECT] - Weekly Status Update - FYI

Purpose: Provide weekly status update for [project name].

Progress This Week:
✓ Completed [achievement 1]
✓ Completed [achievement 2]
✓ Advanced [work item] to [percentage]%

Upcoming This Week:
- [Planned item 1]
- [Planned item 2]
- [Planned item 3]

Risks and Issues:
- [Risk/Issue]: [mitigation plan]

Metrics:
- On Schedule: [Yes/No - explanation if No]
- On Budget: [tracking status]
- Quality: [metrics if applicable]

Questions or concerns? Please contact me directly.

Thank you,
[Name]
```

### 3. Technical Review Request

```
Subject: [SYSTEM] - Technical Design Review Request - ACTION REQUIRED

Purpose: Request your review of the [component/system] design document.

Document: [Link to document]
Review Deadline: [Date]

Scope of Review:
Please focus your review on:
- Technical feasibility
- Security considerations
- Performance implications
- Integration concerns

Specific Questions:
1. [Specific question 1]?
2. [Specific question 2]?

Review Process:
- Add comments directly to the document
- Or send consolidated feedback via email
- Review meeting scheduled for [date/time] (optional)

Thank you for your expertise and time.

Best regards,
[Name]
```

### 4. Incident Communication

```
Subject: [SYSTEM] - Production Incident: [BRIEF DESCRIPTION] - URGENT

Purpose: Notify stakeholders of production incident affecting [system/service].

Incident Summary:
- Start Time: [timestamp with timezone]
- Severity: [P1/P2/P3]
- Impact: [user/business impact]
- Status: [Investigating/Identified/Resolving/Resolved]

Current Status:
[Detailed status of investigation/resolution]

Mitigation:
[Steps being taken to resolve]

Next Update:
[Time of next communication]

Incident Commander: [Name] - [Contact]
Technical Lead: [Name] - [Contact]

Thank you for your patience.

[Name]
```

### 5. Meeting Coordination

```
Subject: [PROJECT] - [Meeting Type] - [Date] - ACTION REQUIRED

Purpose: Schedule [meeting type] to discuss [topic].

Proposed Times: (Please select all that work)
- Option 1: [Date/Time with timezone]
- Option 2: [Date/Time with timezone]
- Option 3: [Date/Time with timezone]

Meeting Objective:
[Clear objective statement]

Agenda:
1. [Topic 1] - [time allocation]
2. [Topic 2] - [time allocation]
3. [Topic 3] - [time allocation]

Pre-Reading:
- [Document 1 with link]
- [Document 2 with link]

Expected Outcomes:
- [Outcome 1]
- [Outcome 2]

Please respond by [deadline] with your availability.

Thank you,
[Name]
```

## Professional Language Guidelines

### Do Use ✅
- Clear, concise sentences
- Active voice
- Specific details and examples
- Professional tone
- Bullet points for clarity
- Proper grammar and spelling

### Don't Use ❌
- Slang or colloquialisms
- Emotional language
- ALL CAPS (except for standard indicators)
- Excessive exclamation points
- Ambiguous pronouns
- Internal jargon with external stakeholders

## Stakeholder-Specific Guidelines

### Executive Communications
- Lead with business impact
- Keep to one page/screen
- Use executive summary format
- Include clear recommendations
- Provide appendices for details

### Technical Team Communications
- Include technical specifics
- Reference documentation
- Use appropriate technical terms
- Provide code/config examples
- Link to repositories/tickets

### External Stakeholder Communications
- Avoid internal acronyms
- Explain technical concepts simply
- Focus on business value
- Include clear timelines
- Provide contact information

## Email Etiquette

### Response Time Expectations
- Urgent: Within 2 hours
- Action Required: Within 24 hours
- FYI: No response required
- Review Request: By stated deadline

### CC and BCC Usage
- TO: People who need to take action
- CC: People who need to be informed
- BCC: Use sparingly, mainly for large distributions

### Reply vs Reply All
- Reply: For responses to sender only
- Reply All: When all recipients need the information
- Consider audience before Reply All

## Formatting Standards

### Text Formatting
```
Headers: Bold or increased font size
**Important Information**

Lists: Use bullets or numbers
• Point 1
• Point 2

Code/Commands: Use monospace font
`kubectl get pods -n production`

Links: Descriptive text
[Architecture Document](https://wiki.company.com/architecture)
```

### Attachments
- Prefer links to documents over attachments
- If attaching, mention in email body
- Keep attachments under 10MB
- Use clear, descriptive filenames

## Common Scenarios

### Escalation Email
```
Subject: [ESCALATION] - [ISSUE] - URGENT ACTION REQUIRED

Purpose: Escalate [issue] requiring management attention.

Issue Summary:
[Brief description of the issue]

Impact:
- Business: [impact]
- Technical: [impact]
- Timeline: [impact]

Actions Taken:
1. [Action 1 and result]
2. [Action 2 and result]

Escalation Reason:
[Why standard procedures aren't sufficient]

Required Decision/Action:
[Specific ask from management]

Recommendation:
[Your recommended course of action]

[Name]
[Contact Information]
```

### Follow-Up Email
```
Subject: [FOLLOW-UP] - [ORIGINAL TOPIC] - ACTION REQUIRED

Purpose: Follow up on [original topic] from [date].

Original Request:
[Brief summary of original request]

Current Status:
[What has/hasn't happened]

Outstanding Items:
- [Item 1] - Waiting on [person/thing]
- [Item 2] - Blocked by [reason]

Next Steps:
[Clear action items with owners]

Please respond by [date] with updates.

Thank you,
[Name]
```

## Email Security

### Sensitive Information
- Never include passwords or credentials
- Use secure file transfer for sensitive documents
- Mark confidential emails appropriately
- Verify recipient addresses before sending

### Example Confidentiality Notice
```
CONFIDENTIAL: This email contains proprietary information. 
Do not forward without authorization.
```

## Quality Checklist

Before sending any email:
- [ ] Subject line follows format standards
- [ ] Purpose statement in first line
- [ ] Clear action items with owners
- [ ] Professional tone throughout
- [ ] Proper grammar and spelling checked
- [ ] Appropriate recipients in TO/CC
- [ ] Attachments mentioned in body
- [ ] Links tested and working
- [ ] Signature block included
- [ ] Confidentiality marking if needed

## Email Signature Standards

```
Best regards,

[Full Name]
[Title]
[Department] | [Company]
[Phone] | [Email]
[Optional: LinkedIn or other professional link]
```

---

Professional email communication builds trust, ensures clarity, and drives action. Follow these standards to maintain effective stakeholder communication across all enterprise interactions.