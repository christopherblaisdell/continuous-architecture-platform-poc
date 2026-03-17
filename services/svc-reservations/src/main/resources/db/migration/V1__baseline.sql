CREATE SCHEMA IF NOT EXISTS reservations;

CREATE TABLE reservations.participants (
    guest_id                       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    role                           VARCHAR(30) NOT NULL,
    waiver_signed                  BOOLEAN,
    medical_clearance              BOOLEAN,
    gear_assignment_id             UUID,
    checked_in                     BOOLEAN,
    check_in_time                  TIMESTAMPTZ,
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);

CREATE TABLE reservations.reservations (
    id                             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    guest_id                       UUID NOT NULL,
    trip_id                        UUID NOT NULL,
    status                         VARCHAR(30) NOT NULL,
    booking_source                 VARCHAR(30),
    gear_package_id                UUID,
    special_requirements           VARCHAR(255),
    payment_reference              VARCHAR(255),
    total_amount                   NUMERIC(10,2),
    currency                       VARCHAR(255),
    _rev                           VARCHAR(255) NOT NULL,
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);
