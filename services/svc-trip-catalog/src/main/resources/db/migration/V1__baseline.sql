CREATE SCHEMA IF NOT EXISTS trip_catalog;

CREATE TABLE trip_catalog.trips (
    id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name                  VARCHAR(200)  NOT NULL,
    description           TEXT,
    activity_type         VARCHAR(30)   NOT NULL,
    difficulty_level      VARCHAR(20)   NOT NULL,
    region_id             UUID,
    duration_hours        NUMERIC(6,1)  NOT NULL,
    min_participants      INTEGER,
    max_participants      INTEGER,
    base_price            NUMERIC(10,2) NOT NULL,
    status                VARCHAR(20)   NOT NULL DEFAULT 'DRAFT',
    age_minimum           INTEGER,
    fitness_level_required VARCHAR(20),
    created_by            VARCHAR(100),
    created_at            TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at            TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version               INTEGER       NOT NULL DEFAULT 0
);

CREATE INDEX idx_trips_status ON trip_catalog.trips(status);
CREATE INDEX idx_trips_activity ON trip_catalog.trips(activity_type);
