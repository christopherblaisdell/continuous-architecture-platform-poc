CREATE SCHEMA IF NOT EXISTS check_in;

CREATE TABLE check_in.check_ins (
    id                             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    reservation_id                 UUID NOT NULL,
    participant_guest_id           UUID NOT NULL,
    status                         VARCHAR(30) NOT NULL,
    gear_verified                  BOOLEAN,
    waiver_verified                BOOLEAN,
    waiver_id                      UUID,
    checked_in_at                  TIMESTAMPTZ NOT NULL,
    checked_in_by                  UUID NOT NULL,
    completed_at                   TIMESTAMPTZ,
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);

CREATE TABLE check_in.gear_items (
    gear_inventory_id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    gear_type                      VARCHAR(255) NOT NULL,
    size                           VARCHAR(255),
    condition_on_issue             VARCHAR(30),
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);
