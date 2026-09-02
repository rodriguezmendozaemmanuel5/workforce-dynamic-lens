-- =============================================================================
-- WORKFORCE DYNAMIC LENS — MODULE v0.6.0
-- Script 01: Database & Schema Setup
-- Engine Target: PostgreSQL 15+
-- Design Freeze Baseline: v1.0 (August 2026)
-- Author: Emmanuel Rodríguez Mendoza
-- =============================================================================

-- NOTE: CREATE DATABASE must be executed independently if running manually.
-- CREATE DATABASE workforce_db;
-- \c workforce_db;

-- 1. Create Data Warehouse Schema
CREATE SCHEMA IF NOT EXISTS people_analytics;

-- 2. Schema Documentation & Search Path
COMMENT ON SCHEMA people_analytics IS 'Core Data Warehouse schema for Workforce Dynamic Lens (Kimball Star Schema)';

SET search_path TO people_analytics, public;
