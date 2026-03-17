CREATE SCHEMA IF NOT EXISTS location_services;

CREATE TABLE location_services.locations (
    id                             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name                           VARCHAR(255) NOT NULL,
    type                           VARCHAR(30) NOT NULL,
    region_id                      UUID NOT NULL,
    capacity                       INTEGER,
    status                         VARCHAR(30) NOT NULL,
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);

CREATE TABLE location_services.location_capacities (
    location_id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    max_capacity                   INTEGER NOT NULL,
    current_occupancy              INTEGER NOT NULL,
    available_spots                INTEGER,
    utilization_percent            NUMERIC(10,2),
    as_of                          TIMESTAMPTZ,
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);
