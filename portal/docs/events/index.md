---
hide:
  - toc
tags:
  - events
  - kafka
---

<div class="hero" markdown>

# Event Catalog

<p class="subtitle">Domain Events Published and Consumed Across NovaTrek Services</p>

<span class="version-badge">7 Events &middot; 6 Producers &middot; 6 Consumers</span>

</div>

The NovaTrek platform uses **Apache Kafka** as its event bus for asynchronous inter-service communication. Each event is published to a dedicated channel and consumed by one or more downstream services.

---

## Event Flow Overview

<div class="diagram-wrap"><a href="../microservices/svg/event-flow.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../microservices/svg/event-flow.svg" type="image/svg+xml" style="width:100%;max-width:1400px"></object></div>

---

## Operations

| Event | Channel | Producer | Consumers | Schema |
|-------|---------|----------|-----------|--------|
| **checkin.completed** | `novatrek.operations.checkin.completed` | [svc-check-in](../microservices/svc-check-in/) | [svc-analytics](../microservices/svc-analytics/), [svc-notifications](../microservices/svc-notifications/) | [:material-code-json:](../events-ui/svc-check-in.html "View event schema") |
| **schedule.published** | `novatrek.operations.schedule.published` | [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator/) | [svc-guide-management](../microservices/svc-guide-management/), [svc-notifications](../microservices/svc-notifications/) | [:material-code-json:](../events-ui/svc-scheduling-orchestrator.html "View event schema") |

## Guest Identity

| Event | Channel | Producer | Consumers | Schema |
|-------|---------|----------|-----------|--------|
| **guest.registered** | `novatrek.guest-identity.guest.registered` | [svc-guest-profiles](../microservices/svc-guest-profiles/) | [svc-loyalty-rewards](../microservices/svc-loyalty-rewards/), [svc-analytics](../microservices/svc-analytics/) | [:material-code-json:](../events-ui/svc-guest-profiles.html "View event schema") |

## Booking

| Event | Channel | Producer | Consumers | Schema |
|-------|---------|----------|-----------|--------|
| **reservation.created** | `novatrek.booking.reservation.created` | [svc-reservations](../microservices/svc-reservations/) | [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator/), [svc-analytics](../microservices/svc-analytics/) | [:material-code-json:](../events-ui/svc-reservations.html "View event schema") |
| **reservation.status_changed** | `novatrek.booking.reservation.status-changed` | [svc-reservations](../microservices/svc-reservations/) | [svc-notifications](../microservices/svc-notifications/), [svc-analytics](../microservices/svc-analytics/) | [:material-code-json:](../events-ui/svc-reservations.html "View event schema") |

## Safety

| Event | Channel | Producer | Consumers | Schema |
|-------|---------|----------|-----------|--------|
| **incident.reported** | `novatrek.safety.incident.reported` | [svc-safety-compliance](../microservices/svc-safety-compliance/) | [svc-notifications](../microservices/svc-notifications/), [svc-analytics](../microservices/svc-analytics/) | [:material-code-json:](../events-ui/svc-safety-compliance.html "View event schema") |

## Support

| Event | Channel | Producer | Consumers | Schema |
|-------|---------|----------|-----------|--------|
| **payment.processed** | `novatrek.support.payment.processed` | [svc-payments](../microservices/svc-payments/) | [svc-reservations](../microservices/svc-reservations/), [svc-notifications](../microservices/svc-notifications/) | [:material-code-json:](../events-ui/svc-payments.html "View event schema") |

---

## Event Details

### checkin.completed

- **Channel:** `novatrek.operations.checkin.completed`
- **Producer:** [svc-check-in](../microservices/svc-check-in/)
- **Trigger:** [`POST /check-ins`](../microservices/svc-check-in/#post-check-ins-initiate-check-in-for-a-participant)
- **Domain:** Operations
- **Description:** Published when a guest completes the check-in process
- **Schema:** [:material-code-json: View Event Schema](../events-ui/svc-check-in.html)

**Consumers:**

- [svc-analytics](../microservices/svc-analytics/)
- [svc-notifications](../microservices/svc-notifications/)

### guest.registered

- **Channel:** `novatrek.guest-identity.guest.registered`
- **Producer:** [svc-guest-profiles](../microservices/svc-guest-profiles/)
- **Trigger:** [`POST /guests`](../microservices/svc-guest-profiles/#post-guests-register-a-new-guest)
- **Domain:** Guest Identity
- **Description:** Published when a new guest profile is created
- **Schema:** [:material-code-json: View Event Schema](../events-ui/svc-guest-profiles.html)

**Consumers:**

- [svc-loyalty-rewards](../microservices/svc-loyalty-rewards/)
- [svc-analytics](../microservices/svc-analytics/)

### incident.reported

- **Channel:** `novatrek.safety.incident.reported`
- **Producer:** [svc-safety-compliance](../microservices/svc-safety-compliance/)
- **Trigger:** [`POST /incidents`](../microservices/svc-safety-compliance/#post-incidents-file-an-incident-report)
- **Domain:** Safety
- **Description:** Published when a safety incident is reported
- **Schema:** [:material-code-json: View Event Schema](../events-ui/svc-safety-compliance.html)

**Consumers:**

- [svc-notifications](../microservices/svc-notifications/)
- [svc-analytics](../microservices/svc-analytics/)

### payment.processed

- **Channel:** `novatrek.support.payment.processed`
- **Producer:** [svc-payments](../microservices/svc-payments/)
- **Trigger:** [`POST /payments`](../microservices/svc-payments/#post-payments-process-a-payment)
- **Domain:** Support
- **Description:** Published when a payment is successfully processed
- **Schema:** [:material-code-json: View Event Schema](../events-ui/svc-payments.html)

**Consumers:**

- [svc-reservations](../microservices/svc-reservations/)
- [svc-notifications](../microservices/svc-notifications/)

### reservation.created

- **Channel:** `novatrek.booking.reservation.created`
- **Producer:** [svc-reservations](../microservices/svc-reservations/)
- **Trigger:** [`POST /reservations`](../microservices/svc-reservations/#post-reservations-create-a-new-reservation)
- **Domain:** Booking
- **Description:** Published when a new reservation is confirmed
- **Schema:** [:material-code-json: View Event Schema](../events-ui/svc-reservations.html)

**Consumers:**

- [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator/)
- [svc-analytics](../microservices/svc-analytics/)

### reservation.status_changed

- **Channel:** `novatrek.booking.reservation.status-changed`
- **Producer:** [svc-reservations](../microservices/svc-reservations/)
- **Trigger:** [`PUT /reservations/{reservation_id}/status`](../microservices/svc-reservations/#put-reservationsreservation_idstatus-transition-reservation-status)
- **Domain:** Booking
- **Description:** Published when a reservation status transitions
- **Schema:** [:material-code-json: View Event Schema](../events-ui/svc-reservations.html)

**Consumers:**

- [svc-notifications](../microservices/svc-notifications/)
- [svc-analytics](../microservices/svc-analytics/)

### schedule.published

- **Channel:** `novatrek.operations.schedule.published`
- **Producer:** [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator/)
- **Trigger:** [`POST /schedule-requests`](../microservices/svc-scheduling-orchestrator/#post-schedule-requests-request-optimal-schedule-for-a-trip)
- **Domain:** Operations
- **Description:** Published when a daily schedule is finalized
- **Schema:** [:material-code-json: View Event Schema](../events-ui/svc-scheduling-orchestrator.html)

**Consumers:**

- [svc-guide-management](../microservices/svc-guide-management/)
- [svc-notifications](../microservices/svc-notifications/)

---

## AsyncAPI Specifications

Each producing service has an AsyncAPI 3.0 specification file describing its published events in detail.

| Service | Spec File | Interactive Viewer |
|---------|-----------|-------------------|
| [svc-check-in](../microservices/svc-check-in/) | [`svc-check-in.events.yaml`](../events/svc-check-in.events.yaml) | [:material-code-json: View Schema](../events-ui/svc-check-in.html) |
| [svc-guest-profiles](../microservices/svc-guest-profiles/) | [`svc-guest-profiles.events.yaml`](../events/svc-guest-profiles.events.yaml) | [:material-code-json: View Schema](../events-ui/svc-guest-profiles.html) |
| [svc-payments](../microservices/svc-payments/) | [`svc-payments.events.yaml`](../events/svc-payments.events.yaml) | [:material-code-json: View Schema](../events-ui/svc-payments.html) |
| [svc-reservations](../microservices/svc-reservations/) | [`svc-reservations.events.yaml`](../events/svc-reservations.events.yaml) | [:material-code-json: View Schema](../events-ui/svc-reservations.html) |
| [svc-safety-compliance](../microservices/svc-safety-compliance/) | [`svc-safety-compliance.events.yaml`](../events/svc-safety-compliance.events.yaml) | [:material-code-json: View Schema](../events-ui/svc-safety-compliance.html) |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator/) | [`svc-scheduling-orchestrator.events.yaml`](../events/svc-scheduling-orchestrator.events.yaml) | [:material-code-json: View Schema](../events-ui/svc-scheduling-orchestrator.html) |
