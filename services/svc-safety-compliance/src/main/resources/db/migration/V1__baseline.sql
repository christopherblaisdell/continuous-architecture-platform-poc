CREATE SCHEMA IF NOT EXISTS safety_compliance;

CREATE TABLE safety_compliance.incident_reports (
    id                             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    reservation_id                 UUID NOT NULL,
    guide_id                       UUID NOT NULL,
    type                           VARCHAR(30) NOT NULL,
    severity                       VARCHAR(30) NOT NULL,
    description                    TEXT NOT NULL,
    actions_taken                  VARCHAR(255),
    follow_up_required             BOOLEAN,
    follow_up_notes                TEXT,
    reported_at                    TIMESTAMPTZ NOT NULL,
    status                         VARCHAR(30) NOT NULL,
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);

CREATE TABLE safety_compliance.safety_inspections (
    id                             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    location_id                    UUID NOT NULL,
    inspector_id                   UUID NOT NULL,
    inspection_date                DATE NOT NULL,
    status                         VARCHAR(30) NOT NULL,
    notes                          TEXT,
    next_inspection_due            DATE,
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);

CREATE TABLE safety_compliance.waivers (
    id                             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    guest_id                       UUID NOT NULL,
    reservation_id                 UUID NOT NULL,
    waiver_type                    VARCHAR(30) NOT NULL,
    signed_at                      TIMESTAMPTZ NOT NULL,
    ip_address                     VARCHAR(255),
    status                         VARCHAR(30) NOT NULL,
    emergency_contact_name         VARCHAR(255),
    emergency_contact_phone        VARCHAR(255),
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);
