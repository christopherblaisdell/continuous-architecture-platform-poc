CREATE SCHEMA IF NOT EXISTS emergency_response;

CREATE TABLE emergency_response.dispatch_records (
    dispatch_id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    emergency_id                   UUID,
    rescue_team_id                 UUID,
    priority                       VARCHAR(255),
    status                         VARCHAR(30),
    dispatched_at                  TIMESTAMPTZ,
    eta_minutes                    INTEGER,
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);

CREATE TABLE emergency_response.emergencies (
    emergency_id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    guest_id                       UUID,
    reservation_id                 UUID,
    type                           VARCHAR(255),
    severity                       VARCHAR(255),
    status                         VARCHAR(255),
    description                    TEXT,
    reported_by                    VARCHAR(255),
    dispatch_id                    UUID,
    resolution_notes               TEXT,
    resolved_at                    TIMESTAMPTZ,
    _rev                           VARCHAR(255),
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);

CREATE TABLE emergency_response.rescue_teams (
    team_id                        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name                           VARCHAR(255),
    region                         VARCHAR(255),
    status                         VARCHAR(30),
    member_count                   INTEGER,
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);

CREATE TABLE emergency_response.timeline_entries (
    entry_id                       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    emergency_id                   UUID,
    event_type                     VARCHAR(30),
    description                    TEXT,
    actor                          VARCHAR(255),
    timestamp                      TIMESTAMPTZ,
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);
