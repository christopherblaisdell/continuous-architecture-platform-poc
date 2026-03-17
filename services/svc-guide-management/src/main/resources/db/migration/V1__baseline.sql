CREATE SCHEMA IF NOT EXISTS guide_management;

CREATE TABLE guide_management.availability_windows (
    id                             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    guide_id                       UUID NOT NULL,
    start_date                     DATE NOT NULL,
    end_date                       DATE NOT NULL,
    available                      BOOLEAN NOT NULL,
    notes                          TEXT,
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);

CREATE TABLE guide_management.guides (
    id                             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    first_name                     VARCHAR(255) NOT NULL,
    last_name                      VARCHAR(255) NOT NULL,
    email                          VARCHAR(255) NOT NULL,
    phone                          VARCHAR(255),
    years_experience               INTEGER,
    max_group_size                 INTEGER,
    status                         VARCHAR(30) NOT NULL,
    average_rating                 NUMERIC(10,2),
    total_trips_led                INTEGER,
    emergency_training_level       VARCHAR(30),
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);

CREATE TABLE guide_management.guide_certifications (
    id                             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    guide_id                       UUID,
    certification_type             VARCHAR(255) NOT NULL,
    issued_date                    DATE NOT NULL,
    expiry_date                    DATE,
    issuing_body                   TEXT NOT NULL,
    certificate_number             VARCHAR(255) NOT NULL,
    status                         VARCHAR(30) NOT NULL,
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);

CREATE TABLE guide_management.guide_ratings (
    id                             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    guide_id                       UUID,
    reservation_id                 UUID NOT NULL,
    guest_id                       UUID NOT NULL,
    rating                         INTEGER NOT NULL,
    review_text                    VARCHAR(255),
    date                           DATE NOT NULL,
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);

CREATE TABLE guide_management.guide_schedule_entries (
    id                             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    guide_id                       UUID,
    trip_id                        UUID,
    trip_name                      VARCHAR(255),
    departure_date                 DATE,
    return_date                    DATE,
    role                           VARCHAR(30),
    group_size                     INTEGER,
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);
