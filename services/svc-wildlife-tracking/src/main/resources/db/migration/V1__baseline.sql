CREATE SCHEMA IF NOT EXISTS wildlife_tracking;

CREATE TABLE wildlife_tracking.habitat_zones (
    zone_id                        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name                           VARCHAR(255),
    activity_level                 VARCHAR(30),
    season                         VARCHAR(255),
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);

CREATE TABLE wildlife_tracking.sightings (
    sighting_id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    species_id                     UUID,
    species_name                   VARCHAR(255),
    threat_level                   VARCHAR(255),
    reported_by                    VARCHAR(255),
    reporter_type                  VARCHAR(255),
    observation_notes              TEXT,
    animal_count                   INTEGER,
    behavior                       VARCHAR(255),
    photo_url                      VARCHAR(500),
    trail_id                       UUID,
    alert_triggered                BOOLEAN,
    reported_at                    TIMESTAMPTZ,
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);

CREATE TABLE wildlife_tracking.specieses (
    species_id                     UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    common_name                    VARCHAR(255),
    scientific_name                VARCHAR(255),
    threat_level                   VARCHAR(30),
    category                       VARCHAR(30),
    description                    TEXT,
    safety_guidance                VARCHAR(255),
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);

CREATE TABLE wildlife_tracking.wildlife_alerts (
    alert_id                       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    species_id                     UUID,
    species_name                   VARCHAR(255),
    sighting_id                    UUID,
    threat_level                   VARCHAR(255),
    status                         VARCHAR(255),
    radius_meters                  NUMERIC(10,2),
    recommended_action             VARCHAR(255),
    notes                          TEXT,
    issued_at                      TIMESTAMPTZ,
    expires_at                     TIMESTAMPTZ,
    cancelled_at                   TIMESTAMPTZ,
    _rev                           VARCHAR(255),
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);
