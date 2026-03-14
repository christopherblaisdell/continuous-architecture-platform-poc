CREATE SCHEMA IF NOT EXISTS notifications;

CREATE TABLE notifications.notifications (
    notification_id     UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    guest_id            UUID            NOT NULL,
    reservation_id      UUID,
    channel             VARCHAR(20)     NOT NULL,
    template            VARCHAR(50)     NOT NULL,
    status              VARCHAR(20)     NOT NULL DEFAULT 'PENDING',
    recipient_address   VARCHAR(255)    NOT NULL,
    subject             VARCHAR(255),
    body_preview        VARCHAR(500),
    provider_message_id VARCHAR(100),
    failure_reason      TEXT,
    sent_at             TIMESTAMPTZ,
    delivered_at        TIMESTAMPTZ,
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_notifications_guest_id       ON notifications.notifications(guest_id);
CREATE INDEX idx_notifications_reservation_id ON notifications.notifications(reservation_id);
CREATE INDEX idx_notifications_status         ON notifications.notifications(status);
CREATE INDEX idx_notifications_channel        ON notifications.notifications(channel);
