CREATE SCHEMA IF NOT EXISTS reservations;

CREATE TABLE reservations.reservations (
    reservation_id      UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    guest_id            UUID            NOT NULL,
    trip_id             UUID            NOT NULL,
    status              VARCHAR(30)     NOT NULL DEFAULT 'PENDING',
    booking_source      VARCHAR(20)     DEFAULT 'WEB_DIRECT',
    num_participants    INTEGER         NOT NULL DEFAULT 1,
    total_amount        NUMERIC(10,2)   NOT NULL,
    deposit_amount      NUMERIC(10,2),
    special_requirements TEXT,
    scheduled_date      DATE            NOT NULL,
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    version             INTEGER         NOT NULL DEFAULT 0,
    _rev                VARCHAR(36)     NOT NULL DEFAULT gen_random_uuid()
);

CREATE INDEX idx_reservations_guest_id ON reservations.reservations(guest_id);
CREATE INDEX idx_reservations_status   ON reservations.reservations(status);
CREATE INDEX idx_reservations_scheduled_date ON reservations.reservations(scheduled_date);
