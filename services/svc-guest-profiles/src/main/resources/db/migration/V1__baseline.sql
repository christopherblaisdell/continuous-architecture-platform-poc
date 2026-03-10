CREATE SCHEMA IF NOT EXISTS guest_profiles;

CREATE TABLE guest_profiles.guests (
    guest_id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    first_name      VARCHAR(100)  NOT NULL,
    last_name       VARCHAR(100)  NOT NULL,
    email           VARCHAR(255)  NOT NULL UNIQUE,
    phone           VARCHAR(20),
    date_of_birth   DATE,
    status          VARCHAR(20)   NOT NULL DEFAULT 'ACTIVE',
    loyalty_tier    VARCHAR(20)   DEFAULT 'EXPLORER',
    total_adventures INTEGER      DEFAULT 0,
    profile_image_url VARCHAR(500),
    preferred_language VARCHAR(10),
    created_at      TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version         INTEGER       NOT NULL DEFAULT 0
);

CREATE INDEX idx_guests_email ON guest_profiles.guests(email);
CREATE INDEX idx_guests_status ON guest_profiles.guests(status);
