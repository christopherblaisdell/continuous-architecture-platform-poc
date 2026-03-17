CREATE SCHEMA IF NOT EXISTS payments;

CREATE TABLE payments.disputes (
    id                             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    payment_id                     UUID,
    reservation_id                 UUID,
    guest_id                       UUID,
    type                           VARCHAR(30),
    status                         VARCHAR(30),
    tier                           VARCHAR(30),
    amount_requested               NUMERIC(10,2),
    amount_approved                NUMERIC(10,2),
    resolution                     VARCHAR(30),
    justification                  VARCHAR(255),
    assigned_to                    VARCHAR(255),
    _rev                           INTEGER,
    resolved_at                    TIMESTAMPTZ,
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);

CREATE TABLE payments.payments (
    id                             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    reservation_id                 UUID,
    guest_id                       UUID,
    amount                         NUMERIC(10,2),
    currency                       VARCHAR(255),
    method                         VARCHAR(30),
    status                         VARCHAR(30),
    processor_reference            VARCHAR(255),
    refunded_amount                NUMERIC(10,2),
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);

CREATE TABLE payments.refunds (
    id                             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    payment_id                     UUID,
    amount                         NUMERIC(10,2),
    reason                         VARCHAR(255),
    status                         VARCHAR(30),
    processor_reference            VARCHAR(255),
    initiated_by                   VARCHAR(255),
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);
