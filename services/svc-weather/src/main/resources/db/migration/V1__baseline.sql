CREATE SCHEMA IF NOT EXISTS weather;

CREATE TABLE weather.trail_conditions (
    trail_id                       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trail_name                     VARCHAR(255),
    assessed_at                    TIMESTAMPTZ,
    overall_status                 VARCHAR(30),
    surface_condition              VARCHAR(30),
    water_crossings_passable       BOOLEAN,
    ranger_notes                   TEXT,
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);

CREATE TABLE weather.weather_alerts (
    id                             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    region_id                      UUID,
    alert_type                     VARCHAR(30),
    severity                       VARCHAR(30),
    title                          VARCHAR(255),
    description                    TEXT,
    effective_from                 TIMESTAMPTZ,
    effective_until                TIMESTAMPTZ,
    is_active                      BOOLEAN,
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);
