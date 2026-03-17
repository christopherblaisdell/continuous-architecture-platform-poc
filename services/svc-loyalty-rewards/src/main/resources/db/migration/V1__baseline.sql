CREATE SCHEMA IF NOT EXISTS loyalty_rewards;

CREATE TABLE loyalty_rewards.loyalty_members (
    guest_id                       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tier                           VARCHAR(30) NOT NULL,
    points_balance                 INTEGER NOT NULL,
    lifetime_points                INTEGER NOT NULL,
    tier_expiry                    DATE,
    enrolled_at                    TIMESTAMPTZ,
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);

CREATE TABLE loyalty_rewards.transactions (
    id                             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    type                           VARCHAR(30) NOT NULL,
    points                         INTEGER NOT NULL,
    source_reservation_id          UUID,
    description                    TEXT,
    timestamp                      TIMESTAMPTZ NOT NULL,
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);
