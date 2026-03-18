-- =============================================================================
-- Schema Isolation Setup — Per-Service PostgreSQL Users
-- =============================================================================
-- Creates one user per microservice, each restricted to their own schema.
-- Prevents cross-schema queries at the database level.
--
-- Prerequisites:
--   - Connected as novatrekadmin (superuser) to novatrek_dev database
--   - All 22 schemas already exist (created by Flyway migrations)
--
-- Usage:
--   psql -h pg-novatrek-dev-smwd6ded4e3so.postgres.database.azure.com \
--        -U novatrekadmin -d novatrek_dev -f setup-schema-isolation.sql
-- =============================================================================

-- ---------------------------------------------------------------------------
-- 1. Revoke default public schema access from PUBLIC role
--    This prevents any user from accessing schemas they haven't been granted.
-- ---------------------------------------------------------------------------
REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE CREATE ON SCHEMA public FROM PUBLIC;

-- ---------------------------------------------------------------------------
-- 2. Create per-service users and grant schema-isolated permissions
--    Password convention: svc_{schema}_2026x (change in production)
-- ---------------------------------------------------------------------------

-- Helper function to set up a service user with isolated schema access
-- (PostgreSQL doesn't support parameterized DDL, so we use DO blocks)

DO $$
DECLARE
    svc RECORD;
BEGIN
    FOR svc IN
        SELECT * FROM (VALUES
            ('svc_analytics',                'analytics'),
            ('svc_check_in',                 'check_in'),
            ('svc_emergency_response',       'emergency_response'),
            ('svc_gear_inventory',           'gear_inventory'),
            ('svc_guest_profiles',           'guest_profiles'),
            ('svc_guide_management',         'guide_management'),
            ('svc_inventory_procurement',    'inventory_procurement'),
            ('svc_location_services',        'location_services'),
            ('svc_loyalty_rewards',          'loyalty_rewards'),
            ('svc_media_gallery',            'media_gallery'),
            ('svc_notifications',            'notifications'),
            ('svc_partner_integrations',     'partner_integrations'),
            ('svc_payments',                 'payments'),
            ('svc_reservations',             'reservations'),
            ('svc_reviews',                  'reviews'),
            ('svc_safety_compliance',        'safety_compliance'),
            ('svc_scheduling_orchestrator',  'scheduling_orchestrator'),
            ('svc_trail_management',         'trail_management'),
            ('svc_transport_logistics',      'transport_logistics'),
            ('svc_trip_catalog',             'trip_catalog'),
            ('svc_weather',                  'weather'),
            ('svc_wildlife_tracking',        'wildlife_tracking')
        ) AS t(username, schema_name)
    LOOP
        -- Create user if not exists
        IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = svc.username) THEN
            EXECUTE format('CREATE ROLE %I LOGIN PASSWORD %L',
                svc.username, svc.username || '_2026x');
            RAISE NOTICE 'Created user: %', svc.username;
        ELSE
            RAISE NOTICE 'User already exists: %', svc.username;
        END IF;

        -- Grant USAGE + CREATE on their own schema (allows seeing/creating objects)
        EXECUTE format('GRANT USAGE, CREATE ON SCHEMA %I TO %I',
            svc.schema_name, svc.username);

        -- Grant full DML + DDL on all existing tables (needed for Flyway migrations)
        EXECUTE format('GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA %I TO %I',
            svc.schema_name, svc.username);

        -- Grant USAGE on all sequences (needed for auto-increment PKs)
        EXECUTE format('GRANT USAGE ON ALL SEQUENCES IN SCHEMA %I TO %I',
            svc.schema_name, svc.username);

        -- Set default privileges for future tables created by this user or novatrekadmin
        EXECUTE format('ALTER DEFAULT PRIVILEGES IN SCHEMA %I GRANT ALL PRIVILEGES ON TABLES TO %I',
            svc.schema_name, svc.username);
        EXECUTE format('ALTER DEFAULT PRIVILEGES IN SCHEMA %I GRANT USAGE ON SEQUENCES TO %I',
            svc.schema_name, svc.username);

        RAISE NOTICE 'Granted schema % access to %', svc.schema_name, svc.username;
    END LOOP;
END $$;

-- ---------------------------------------------------------------------------
-- 3. Verify isolation — list per-user schema grants
-- ---------------------------------------------------------------------------
SELECT
    grantee,
    table_schema,
    string_agg(DISTINCT privilege_type, ', ' ORDER BY privilege_type) AS privileges
FROM information_schema.role_table_grants
WHERE grantee LIKE 'svc_%'
GROUP BY grantee, table_schema
ORDER BY grantee, table_schema;
