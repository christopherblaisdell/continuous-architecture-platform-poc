CREATE SCHEMA IF NOT EXISTS gear_inventory;

CREATE TABLE gear_inventory.gear_assignments (
    id                             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    reservation_id                 UUID NOT NULL,
    participant_guest_id           UUID NOT NULL,
    assigned_at                    TIMESTAMPTZ NOT NULL,
    returned_at                    TIMESTAMPTZ,
    condition_on_return            VARCHAR(30),
    damage_notes                   TEXT,
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);

CREATE TABLE gear_inventory.gear_items (
    id                             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name                           VARCHAR(255) NOT NULL,
    category                       VARCHAR(30) NOT NULL,
    size                           VARCHAR(30) NOT NULL,
    condition                      VARCHAR(30) NOT NULL,
    location_id                    UUID NOT NULL,
    serial_number                  VARCHAR(255) NOT NULL,
    purchase_date                  DATE NOT NULL,
    last_maintenance               TIMESTAMPTZ,
    next_maintenance_due           DATE,
    status                         VARCHAR(30) NOT NULL,
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);

CREATE TABLE gear_inventory.gear_packages (
    id                             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name                           VARCHAR(255) NOT NULL,
    description                    TEXT NOT NULL,
    activity_type                  VARCHAR(30) NOT NULL,
    rental_price_per_day           NUMERIC(10,2) NOT NULL,
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);

CREATE TABLE gear_inventory.inventory_levels (
    location_id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    location_name                  VARCHAR(255),
    category                       VARCHAR(30) NOT NULL,
    total                          INTEGER NOT NULL,
    available                      INTEGER NOT NULL,
    assigned                       INTEGER NOT NULL,
    in_maintenance                 INTEGER NOT NULL,
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);

CREATE TABLE gear_inventory.maintenance_records (
    id                             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    gear_item_id                   UUID NOT NULL,
    type                           VARCHAR(30) NOT NULL,
    date                           TIMESTAMPTZ NOT NULL,
    technician                     VARCHAR(255) NOT NULL,
    notes                          TEXT,
    cost                           NUMERIC(10,2),
    next_due                       DATE,
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);
