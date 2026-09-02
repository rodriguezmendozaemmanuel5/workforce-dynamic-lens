-- =============================================================================
-- WORKFORCE DYNAMIC LENS — MODULE v0.6.0
-- Script 04: Dimension Table — dim_positions
-- Engine Target: PostgreSQL 15+
-- Design Freeze Baseline: v1.0 (August 2026)
-- Author: Emmanuel Rodríguez Mendoza
-- =============================================================================

SET search_path TO people_analytics, public;

CREATE TABLE IF NOT EXISTS people_analytics.dim_positions (
    position_sk             BIGINT GENERATED ALWAYS AS IDENTITY,
    position_id             VARCHAR(20) NOT NULL,
    job_title               VARCHAR(100) NOT NULL,
    job_family              VARCHAR(50) NOT NULL,
    job_grade               VARCHAR(10) NOT NULL,
    career_level            VARCHAR(20) NOT NULL,
    is_critical_position    BOOLEAN NOT NULL DEFAULT FALSE,
    is_remote_eligible      BOOLEAN NOT NULL DEFAULT FALSE,
    market_scarcity_index   NUMERIC(3,2) NOT NULL,

    CONSTRAINT pk_dim_positions PRIMARY KEY (position_sk),
    CONSTRAINT uq_dim_pos_id UNIQUE (position_id)
);

COMMENT ON TABLE people_analytics.dim_positions IS 'Job Positions Dimension with career levels and market scarcity metrics';
COMMENT ON COLUMN people_analytics.dim_positions.position_sk IS 'Surrogate Primary Key (Identity)';
COMMENT ON COLUMN people_analytics.dim_positions.position_id IS 'Natural Business Key (e.g., POS_ENG_SR)';
