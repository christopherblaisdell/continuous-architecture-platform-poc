# User Stories — NTK-10008

## US-1: Guest Submits a Trip Review

**As a** guest who completed an adventure,
**I want to** leave a star rating and written review for my trip,
**So that** my experience helps future guests make informed booking decisions.

### Acceptance Criteria

```gherkin
Given a guest with a COMPLETED reservation
When the guest submits a review with a 1-5 star rating
Then the review is saved with status PENDING_MODERATION
And the guest receives confirmation that the review was submitted

Given a guest with a reservation that is not COMPLETED
When the guest attempts to submit a review
Then the submission is rejected with a clear error message

Given a guest who has already reviewed a reservation
When the guest attempts to submit another review for the same reservation
Then the submission is rejected (one review per reservation)
```

## US-2: Guest Rates Multiple Aspects of Their Adventure

**As a** guest writing a review,
**I want to** rate individual aspects of my trip (safety, guide quality, value, scenery, difficulty accuracy),
**So that** my feedback is specific and actionable for NovaTrek.

### Acceptance Criteria

```gherkin
Given a guest submitting a review
When the guest provides category ratings in addition to the overall rating
Then each category rating is stored and used in aggregated summaries

Given a guest submitting a review
When the guest does not provide category ratings
Then the review is accepted with the overall rating only
```

## US-3: Future Guest Browses Trip Ratings

**As a** guest browsing the trip catalog,
**I want to** see the average rating, review count, and recent reviews for each trip,
**So that** I can compare adventures based on real guest experiences.

### Acceptance Criteria

```gherkin
Given a trip with approved reviews
When a guest views the trip detail page
Then the page shows the average rating, total review count, and rating distribution

Given a trip with no approved reviews
When a guest views the trip detail page
Then the page shows "No reviews yet — be the first to share your experience"
```

## US-4: Moderator Reviews Submitted Content

**As a** content moderator,
**I want to** review pending submissions and approve or reject them,
**So that** only appropriate content is published on the platform.

### Acceptance Criteria

```gherkin
Given a review in PENDING_MODERATION status
When a moderator approves the review
Then the review status changes to APPROVED and it becomes publicly visible

Given a review in PENDING_MODERATION status
When a moderator rejects the review with a reason
Then the review status changes to REJECTED and the guest is notified

Given multiple pending reviews
When a moderator views the moderation queue
Then reviews are ordered by submission date with flagged reviews prioritized
```

## US-5: Guest Marks a Review as Helpful

**As a** guest reading reviews,
**I want to** mark reviews that I find helpful,
**So that** the most useful reviews are surfaced for other guests.

### Acceptance Criteria

```gherkin
Given an approved review
When a guest marks it as helpful
Then the helpful count increments by one

Given a guest who has already marked a review as helpful
When the guest attempts to mark it again
Then the action is rejected (one vote per guest per review)
```
