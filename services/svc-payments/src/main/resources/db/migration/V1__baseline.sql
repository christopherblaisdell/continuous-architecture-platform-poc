CREATE SCHEMA IF NOT EXISTS payments;

CREATE TABLE payments.payments (
    payment_id          UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    reservation_id      UUID            NOT NULL,
    guest_id            UUID            NOT NULL,
    amount              NUMERIC(10,2)   NOT NULL,
    currency            VARCHAR(3)      NOT NULL DEFAULT 'USD',
    status              VARCHAR(30)     NOT NULL DEFAULT 'PENDING',
    payment_method      VARCHAR(20)     NOT NULL,
    provider_reference  VARCHAR(100),
    failure_reason      TEXT,
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    processed_at        TIMESTAMPTZ,
    version             INTEGER         NOT NULL DEFAULT 0
);

CREATE INDEX idx_payments_reservation_id ON payments.payments(reservation_id);
CREATE INDEX idx_payments_guest_id        ON payments.payments(guest_id);
CREATE INDEX idx_payments_status          ON payments.payments(status);
