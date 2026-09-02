-- =============================================================================
-- WORKFORCE DYNAMIC LENS — MODULE v0.6.0
-- Script 03: Dimension Table — dim_departments
-- Engine Target: PostgreSQL 15+
-- Design Freeze Baseline: v1.0 (August 2026)
-- Author: Emmanuel Rodríguez Mendoza
-- =============================================================================

SET search_path TO people_analytics, public;

CREATE TABLE IF NOT EXISTS people_analytics.dim_departments (
    department_sk       BIGINT GENERATED ALWAYS AS IDENTITY,
    department_id       VARCHAR(20) NOT NULL,
    department_name     VARCHAR(100) NOT NULL,
    cost_center_code    VARCHAR(20) NOT NULL,
    vp_responsible      VARCHAR(100) NOT NULL,
    region              VARCHAR(20) NOT NULL,
    budget_annual_usd   NUMERIC(14,2) NOT NULL,
    target_headcount    INTEGER NOT NULL,
    strategic_level     VARCHAR(20) NOT NULL,

    CONSTRAINT pk_dim_departments PRIMARY KEY (department_sk),
    CONSTRAINT uq_dim_dept_id UNIQUE (department_id)
);

COMMENT ON TABLE people_analytics.dim_departments IS 'Department Dimension containing organizational structure and budgetary targets';
COMMENT ON COLUMN people_analytics.dim_departments.department_sk IS 'Surrogate Primary Key (Identity)';
COMMENT ON COLUMN people_analytics.dim_departments.department_id IS 'Natural Business Key (e.g., DEP_RD)';
