CREATE SCHEMA IF NOT EXISTS trail_management;

CREATE TABLE trail_management.trails (
    id                       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name                     VARCHAR(200)  NOT NULL,
    description              TEXT,
    region_id                UUID,
    distance_km              NUMERIC(8,2)  NOT NULL,
    elevation_gain_m         INTEGER,
    elevation_loss_m         INTEGER,
    estimated_duration_hours NUMERIC(6,1),
    difficulty               VARCHAR(20)   NOT NULL,
    max_group_size           INTEGER,
    permit_required          BOOLEAN       NOT NULL DEFAULT FALSE,
    dogs_allowed             BOOLEAN       NOT NULL DEFAULT FALSE,
    status                   VARCHAR(30)   NOT NULL DEFAULT 'OPEN',
    waypoint_count           INTEGER       DEFAULT 0,
    created_at               TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at               TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                  INTEGER       NOT NULL DEFAULT 0
);

CREATE INDEX idx_trails_status ON trail_management.trails(status);
CREATE INDEX idx_trails_difficulty ON trail_management.trails(difficulty);
