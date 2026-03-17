CREATE SCHEMA IF NOT EXISTS transport_logistics;

CREATE TABLE transport_logistics.transport_routes (
    id                             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    origin_location_id             UUID NOT NULL,
    destination_location_id        UUID NOT NULL,
    route_name                     VARCHAR(255),
    distance_km                    NUMERIC(10,2) NOT NULL,
    duration_minutes               INTEGER NOT NULL,
    terrain_difficulty             VARCHAR(30),
    active                         BOOLEAN,
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);

CREATE TABLE transport_logistics.vehicles (
    id                             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    type                           VARCHAR(30) NOT NULL,
    capacity                       INTEGER NOT NULL,
    license_plate                  VARCHAR(255) NOT NULL,
    status                         VARCHAR(30) NOT NULL,
    assigned_location_id           UUID,
    mileage                        INTEGER,
    last_maintenance_date          DATE,
    next_maintenance_date          DATE,
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);
