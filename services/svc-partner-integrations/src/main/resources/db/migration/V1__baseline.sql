CREATE SCHEMA IF NOT EXISTS partner_integrations;

CREATE TABLE partner_integrations.commission_line_items (
    booking_id                     UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    external_reference             VARCHAR(255),
    trip_date                      DATE,
    booking_total                  NUMERIC(10,2),
    commission_rate                NUMERIC(10,2),
    commission_amount              NUMERIC(10,2),
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);

CREATE TABLE partner_integrations.commission_reports (
    partner_id                     UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    period_start                   DATE NOT NULL,
    period_end                     DATE NOT NULL,
    total_bookings                 INTEGER,
    total_revenue                  NUMERIC(10,2),
    total_commission               NUMERIC(10,2),
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);

CREATE TABLE partner_integrations.partners (
    id                             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name                           VARCHAR(255) NOT NULL,
    type                           VARCHAR(30) NOT NULL,
    api_key_hash                   VARCHAR(255),
    commission_rate                NUMERIC(10,2) NOT NULL,
    status                         VARCHAR(30) NOT NULL,
    contact_email                  VARCHAR(255),
    callback_url                   VARCHAR(500),
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);

CREATE TABLE partner_integrations.partner_bookings (
    id                             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    partner_id                     UUID NOT NULL,
    external_reference             VARCHAR(255) NOT NULL,
    reservation_id                 UUID,
    status                         VARCHAR(30) NOT NULL,
    commission_rate                NUMERIC(10,2) NOT NULL,
    commission_amount              NUMERIC(10,2),
    booking_total                  NUMERIC(10,2),
    activity_id                    UUID,
    trip_date                      DATE,
    participant_count              INTEGER,
    confirmed_at                   TIMESTAMPTZ,
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);
