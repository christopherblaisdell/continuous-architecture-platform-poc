CREATE SCHEMA IF NOT EXISTS reviews;

CREATE TABLE reviews.rating_summaries (
    entity_id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    average_rating                 NUMERIC(10,2),
    total_reviews                  INTEGER,
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);

CREATE TABLE reviews.reviews (
    id                             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    reservation_id                 UUID,
    guest_id                       UUID,
    trip_id                        UUID,
    guide_id                       UUID,
    overall_rating                 INTEGER,
    title                          VARCHAR(255),
    body                           TEXT,
    visit_date                     DATE,
    moderation_status              VARCHAR(30),
    helpful_count                  INTEGER,
    _rev                           INTEGER,
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);
