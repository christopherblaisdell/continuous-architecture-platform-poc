CREATE SCHEMA IF NOT EXISTS inventory_procurement;

CREATE TABLE inventory_procurement.purchase_orders (
    id                             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    supplier_id                    UUID NOT NULL,
    status                         VARCHAR(30) NOT NULL,
    total_amount                   NUMERIC(10,2) NOT NULL,
    currency                       VARCHAR(255),
    delivery_location_id           UUID,
    expected_delivery_date         DATE,
    notes                          TEXT,
    created_by                     UUID,
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);

CREATE TABLE inventory_procurement.reorder_alerts (
    id                             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    item_category                  VARCHAR(255),
    location_id                    UUID,
    current_on_hand                INTEGER,
    reorder_point                  INTEGER,
    recommended_order_quantity     INTEGER,
    severity                       VARCHAR(30),
    preferred_supplier_id          UUID,
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);

CREATE TABLE inventory_procurement.stock_adjustments (
    id                             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    item_category                  VARCHAR(255),
    location_id                    UUID,
    quantity_change                INTEGER,
    reason                         VARCHAR(255),
    notes                          TEXT,
    adjusted_by                    UUID,
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);

CREATE TABLE inventory_procurement.suppliers (
    id                             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name                           VARCHAR(255) NOT NULL,
    lead_time_days                 INTEGER NOT NULL,
    rating                         NUMERIC(10,2),
    active                         BOOLEAN,
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);
