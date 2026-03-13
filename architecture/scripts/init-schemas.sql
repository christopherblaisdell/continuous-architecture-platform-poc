-- ===========================================================================
-- Initialize NovaTrek Database Schemas
-- ===========================================================================
-- Creates one schema per microservice (mirrors Azure PostgreSQL layout).
-- Run automatically by Docker Compose on first startup.
-- ===========================================================================

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "postgis";

-- Wave 1 — Guest Identity and Product Catalog
CREATE SCHEMA IF NOT EXISTS guests;
CREATE SCHEMA IF NOT EXISTS catalog;
CREATE SCHEMA IF NOT EXISTS trails;

-- Wave 2 — Booking and Payments
CREATE SCHEMA IF NOT EXISTS reservations;
CREATE SCHEMA IF NOT EXISTS payments;

-- Wave 3 — Day-of-Adventure Operations
CREATE SCHEMA IF NOT EXISTS checkin;
CREATE SCHEMA IF NOT EXISTS scheduling;
CREATE SCHEMA IF NOT EXISTS gear;
CREATE SCHEMA IF NOT EXISTS safety;

-- Wave 4 — Guide and Transport
CREATE SCHEMA IF NOT EXISTS guides;
CREATE SCHEMA IF NOT EXISTS transport;
CREATE SCHEMA IF NOT EXISTS location;

-- Wave 5 — Analytics, Loyalty, Media
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS loyalty;
CREATE SCHEMA IF NOT EXISTS media;

-- Wave 6 — External Integrations
CREATE SCHEMA IF NOT EXISTS partners;
CREATE SCHEMA IF NOT EXISTS weather;
CREATE SCHEMA IF NOT EXISTS procurement;
CREATE SCHEMA IF NOT EXISTS emergency;
CREATE SCHEMA IF NOT EXISTS wildlife;

-- Notifications is stateless (no schema needed)
