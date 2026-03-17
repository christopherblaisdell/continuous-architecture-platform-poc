CREATE SCHEMA IF NOT EXISTS scheduling_orchestrator;

CREATE TABLE scheduling_orchestrator.conflict_resolution_results (
    conflict_id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    resolution_status              VARCHAR(30) NOT NULL,
    applied_strategy               VARCHAR(255),
    resolved_at                    TIMESTAMPTZ,
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);

CREATE TABLE scheduling_orchestrator.guide_assignments (
    guide_id                       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    guide_name                     VARCHAR(255),
    date                           DATE NOT NULL,
    assignment_status              VARCHAR(30) NOT NULL,
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);

CREATE TABLE scheduling_orchestrator.resolution_options (
    id                             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    strategy                       VARCHAR(30) NOT NULL,
    description                    TEXT NOT NULL,
    impact_assessment              VARCHAR(255),
    estimated_affected_guests      INTEGER,
    requires_guest_notification    BOOLEAN,
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);

CREATE TABLE scheduling_orchestrator.schedule_conflicts (
    id                             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    type                           VARCHAR(30) NOT NULL,
    severity                       VARCHAR(30) NOT NULL,
    description                    TEXT,
    conflict_date                  DATE,
    region_id                      UUID,
    resolved                       BOOLEAN,
    resolved_at                    TIMESTAMPTZ,
    detected_at                    TIMESTAMPTZ NOT NULL,
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);
