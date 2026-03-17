CREATE SCHEMA IF NOT EXISTS analytics;

CREATE TABLE analytics.guide_performances (
    guide_id                       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trips_led                      INTEGER,
    total_participants             INTEGER,
    average_guest_rating           NUMERIC(10,2),
    incident_count                 INTEGER,
    cancellation_rate              NUMERIC(10,2),
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);
