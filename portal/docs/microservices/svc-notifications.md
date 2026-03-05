---
tags:
  - microservice
  - svc-notifications
  - support
---

# svc-notifications

**NovaTrek Notifications Service** &nbsp;|&nbsp; <span style="background: #64748b15; color: #64748b; border: 1px solid #64748b40; padding: 0.15rem 0.6rem; border-radius: 1rem; font-size: 0.8rem; font-weight: 600;">Support</span> &nbsp;|&nbsp; `v1.0.0` &nbsp;|&nbsp; *NovaTrek Platform Team*

> Sends notifications to guests and guides via email, SMS, push, and in-app channels.

[:material-api: Swagger UI](../services/api/svc-notifications.html){ .md-button .md-button--primary }
[:material-file-download: Download OpenAPI Spec](../specs/svc-notifications.yaml){ .md-button }

---

## :material-map: Integration Context

<div class="diagram-wrap"><a href="../svg/svc-notifications--c4-context.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-notifications--c4-context.svg" type="image/svg+xml" style="max-width: 100%;">svc-notifications C4 context diagram</object></div>


## :material-database: Data Store { #data-store }

### Overview

| Property | Detail |
|----------|--------|
| **Engine** | PostgreSQL 15 + Valkey 8 |
| **Schema** | `notifications` |
| **Tables** | `notifications`, `templates`, `delivery_log`, `channel_preferences` |
| **Estimated Volume** | ~15,000 notifications/day |
| **Connection Pool** | min 5 / max 25 / idle timeout 10min |
| **Backup Strategy** | Daily pg_dump, 30-day retention |

### Key Features

- Valkey queue for async delivery processing
- Template versioning with rollback support
- Multi-channel delivery: email, SMS, push, in-app

### Table Reference

#### `notifications`

*Notification dispatch records with delivery tracking*

| Column | Type | Constraints |
|--------|------|-------------|
| `notification_id` | `UUID` | PK |
| `recipient_id` | `UUID` | NOT NULL |
| `template_id` | `UUID` | NOT NULL, FK -> templates |
| `channel` | `VARCHAR(20)` | NOT NULL |
| `subject` | `VARCHAR(255)` | NULL |
| `body` | `TEXT` | NOT NULL |
| `status` | `VARCHAR(20)` | NOT NULL, DEFAULT 'queued' |
| `scheduled_at` | `TIMESTAMPTZ` | NULL |
| `sent_at` | `TIMESTAMPTZ` | NULL |
| `created_at` | `TIMESTAMPTZ` | NOT NULL |

**Indexes:**

- `idx_notif_recipient` on `recipient_id, created_at DESC`
- `idx_notif_status` on `status`
- `idx_notif_scheduled` on `scheduled_at` (WHERE status = 'scheduled')

#### `templates`

*Notification content templates with version history*

| Column | Type | Constraints |
|--------|------|-------------|
| `template_id` | `UUID` | PK |
| `name` | `VARCHAR(100)` | NOT NULL |
| `channel` | `VARCHAR(20)` | NOT NULL |
| `subject_template` | `TEXT` | NULL |
| `body_template` | `TEXT` | NOT NULL |
| `version` | `INTEGER` | NOT NULL, DEFAULT 1 |
| `active` | `BOOLEAN` | NOT NULL, DEFAULT TRUE |
| `created_at` | `TIMESTAMPTZ` | NOT NULL |

**Indexes:**

- `idx_tpl_name_channel` on `name, channel`

#### `delivery_log`

*Delivery attempt history for debugging and retry logic*

| Column | Type | Constraints |
|--------|------|-------------|
| `log_id` | `UUID` | PK |
| `notification_id` | `UUID` | NOT NULL, FK -> notifications |
| `attempt` | `SMALLINT` | NOT NULL |
| `status` | `VARCHAR(20)` | NOT NULL |
| `provider_response` | `JSONB` | NULL |
| `attempted_at` | `TIMESTAMPTZ` | NOT NULL |

**Indexes:**

- `idx_dlog_notif` on `notification_id`


---

## :material-api: Endpoints (6 total)

---

### GET `/notifications` -- List notifications { .endpoint-get }

> Returns notifications filtered by recipient and/or channel, ordered most-recent first.

[:material-open-in-new: View in Swagger UI](../services/api/svc-notifications.html#/Notifications/listNotifications){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-notifications--get-notifications.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-notifications--get-notifications.svg" type="image/svg+xml" style="max-width: 100%;">GET /notifications sequence diagram</object></div>

---

### POST `/notifications` -- Send a notification { .endpoint-post }

> Queues a notification for delivery via the specified channel.

[:material-open-in-new: View in Swagger UI](../services/api/svc-notifications.html#/Notifications/sendNotification){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-notifications--post-notifications.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-notifications--post-notifications.svg" type="image/svg+xml" style="max-width: 100%;">POST /notifications sequence diagram</object></div>

---

### GET `/notifications/{notification_id}` -- Retrieve notification details { .endpoint-get }

> Returns full details and delivery status of a single notification.

[:material-open-in-new: View in Swagger UI](../services/api/svc-notifications.html#/Notifications/getNotification){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-notifications--get-notifications-notification_id.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-notifications--get-notifications-notification_id.svg" type="image/svg+xml" style="max-width: 100%;">GET /notifications/{notification_id} sequence diagram</object></div>

---

### POST `/notifications/bulk` -- Send bulk notifications { .endpoint-post }

> Sends the same templated notification to multiple recipients.

[:material-open-in-new: View in Swagger UI](../services/api/svc-notifications.html#/Notifications/sendBulkNotifications){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-notifications--post-notifications-bulk.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-notifications--post-notifications-bulk.svg" type="image/svg+xml" style="max-width: 100%;">POST /notifications/bulk sequence diagram</object></div>

---

### GET `/templates` -- List notification templates { .endpoint-get }

> Returns all available notification templates, optionally filtered by channel.

[:material-open-in-new: View in Swagger UI](../services/api/svc-notifications.html#/Templates/listTemplates){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-notifications--get-templates.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-notifications--get-templates.svg" type="image/svg+xml" style="max-width: 100%;">GET /templates sequence diagram</object></div>

---

### POST `/templates` -- Create a notification template { .endpoint-post }

> Registers a new notification template with variable placeholders for dynamic content.

[:material-open-in-new: View in Swagger UI](../services/api/svc-notifications.html#/Templates/createTemplate){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-notifications--post-templates.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-notifications--post-templates.svg" type="image/svg+xml" style="max-width: 100%;">POST /templates sequence diagram</object></div>

---

## :material-cellphone-link: Consuming Applications

| Application | Screens Using This Service |
|-------------|---------------------------|
| [Guest Portal](../../applications/web-guest-portal/) | Reservation Management, Waiver Signing, Trip Gallery |
| [Operations Dashboard](../../applications/web-ops-dashboard/) | Safety Incident Board |
| [Adventure App](../../applications/app-guest-mobile/) | Photo Upload, Weather and Trail Alerts |

---

## :material-broadcast-off: Events Consumed

| Event | Producer | Channel |
|-------|----------|---------|
| [`reservation.status_changed`](/events/#reservationstatus_changed) | [svc-reservations](../svc-reservations/) | `novatrek.booking.reservation.status-changed` |
| [`checkin.completed`](/events/#checkincompleted) | [svc-check-in](../svc-check-in/) | `novatrek.operations.checkin.completed` |
| [`schedule.published`](/events/#schedulepublished) | [svc-scheduling-orchestrator](../svc-scheduling-orchestrator/) | `novatrek.operations.schedule.published` |
| [`payment.processed`](/events/#paymentprocessed) | [svc-payments](../svc-payments/) | `novatrek.support.payment.processed` |
| [`incident.reported`](/events/#incidentreported) | [svc-safety-compliance](../svc-safety-compliance/) | `novatrek.safety.incident.reported` |
