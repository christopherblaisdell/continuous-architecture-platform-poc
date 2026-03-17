CREATE SCHEMA IF NOT EXISTS notifications;

CREATE TABLE notifications.notifications (
    id                             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recipient_id                   UUID,
    channel                        VARCHAR(30),
    template_id                    UUID,
    reservation_id                 UUID,
    status                         VARCHAR(30),
    priority                       VARCHAR(30),
    rendered_subject               VARCHAR(255),
    error_message                  TEXT,
    queued_at                      TIMESTAMPTZ,
    sent_at                        TIMESTAMPTZ,
    delivered_at                   TIMESTAMPTZ,
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);

CREATE TABLE notifications.notification_templates (
    id                             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name                           VARCHAR(255),
    channel                        VARCHAR(30),
    subject                        VARCHAR(255),
    body_template                  TEXT,
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);
